from __future__ import annotations

import hashlib
import html
import json
import re
import time
import unicodedata
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import yaml


UNSOLVEDMATH_BASE_URL = "https://www.unsolvedmath.com"
UNSOLVEDMATH_USER_AGENT = "amra-unsolvedmath-importer/1.0"
ERDOS_SET_ID = 8

SCRIPT_STYLE_PATTERN = re.compile(r"<(script|style)\b.*?</\1>", re.IGNORECASE | re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")
FLIGHT_CHUNK_PATTERN = re.compile(
    r"self\.__next_f\.push\(\[1,(\"(?:\\.|[^\"\\])*\")\]\)</script>"
)
UNICODE_PUNCTUATION_TRANSLATION = str.maketrans(
    {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2015": "-",
        "\u2212": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
    }
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def clean_html_text(payload: str) -> str:
    without_scripts = SCRIPT_STYLE_PATTERN.sub(" ", payload)
    without_tags = TAG_PATTERN.sub(" ", without_scripts)
    decoded = html.unescape(without_tags).replace("\xa0", " ")
    return WHITESPACE_PATTERN.sub(" ", decoded).strip()


def normalize_domain(value: str) -> str:
    normalized = value.strip().lower().replace("&", "and")
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "research_mathematics"


def normalize_for_comparison(value: str) -> str:
    value = html.unescape(value).translate(UNICODE_PUNCTUATION_TRANSLATION).lower()
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"\\[a-zA-Z]+", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return WHITESPACE_PATTERN.sub(" ", value).strip()


def normalized_problem_title(value: str, *, domain: str = "") -> str:
    value = html.unescape(value).translate(UNICODE_PUNCTUATION_TRANSLATION).lower()
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"['’]s\b", "", value)
    tokens = re.sub(r"[^a-z0-9]+", " ", value).split()
    generic = {"a", "an", "the", "conjecture", "open", "problem", "problems", "question"}
    tokens = [token for token in tokens if token not in generic]
    if not any(len(token) >= 5 for token in tokens):
        return ""
    key = " ".join(tokens)
    # The Whitehead problem in abelian-group theory is distinct from the
    # Whitehead conjecture in low-dimensional topology.
    if key == "whitehead":
        key = f"{key}:{domain}"
    return key


def slugify(value: str) -> str:
    value = normalize_for_comparison(value)
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "variant"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def _write_json(path: Path, payload: Any) -> None:
    _atomic_write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def _write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    body = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    _atomic_write_text(path, body)


def _write_yaml(path: Path, payload: Any) -> None:
    _atomic_write_text(
        path,
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=100),
    )


def fetch_text(
    url: str,
    *,
    timeout: int = 30,
    retries: int = 3,
    user_agent: str = UNSOLVEDMATH_USER_AGENT,
) -> str:
    last_error: Exception | None = None
    for attempt in range(max(1, retries)):
        try:
            request = Request(url, headers={"User-Agent": user_agent})
            with urlopen(request, timeout=timeout) as response:
                return response.read().decode("utf-8", errors="replace")
        except Exception as exc:  # urllib exposes several transport-specific exception types.
            last_error = exc
            if attempt + 1 < max(1, retries):
                time.sleep(0.5 * (2**attempt))
    assert last_error is not None
    raise last_error


def parse_unsolvedmath_detail_page(payload: str, *, expected_source_id: str = "") -> dict[str, Any]:
    chunks: list[str] = []
    for match in FLIGHT_CHUNK_PATTERN.finditer(payload):
        try:
            chunks.append(json.loads(match.group(1)))
        except json.JSONDecodeError:
            continue
    flight_payload = "".join(chunks)
    decoder = json.JSONDecoder()
    cursor = 0
    while True:
        marker = flight_payload.find('"problem":', cursor)
        if marker < 0:
            break
        start = marker + len('"problem":')
        try:
            problem, _ = decoder.raw_decode(flight_payload, start)
        except json.JSONDecodeError:
            cursor = start
            continue
        if isinstance(problem, dict):
            source_id = str(problem.get("problem_number", "")).strip()
            if not expected_source_id or source_id == expected_source_id:
                return problem
        cursor = start
    raise ValueError(f"detail page did not contain a decodable problem payload for {expected_source_id!r}")


def parse_unsolvedmath_index_card(card_id: str, block: str, *, page: int) -> dict[str, Any] | None:
    title_match = re.search(r"<h3[^>]*>(.*?)</h3>", block, re.DOTALL)
    snippet_match = re.search(r"<p[^>]*>(.*?)</p>", block, re.DOTALL)
    spans = re.findall(r"<span[^>]*>(.*?)</span>", block, re.DOTALL)
    difficulty_match = re.search(r">L(?:<!--\s*-->)?(\d)<", block)
    status_match = re.search(r">(Open|Solved|Closed|Unknown)<", block)
    if not title_match:
        return None
    snippet = clean_html_text(snippet_match.group(1)) if snippet_match else ""
    return {
        "source_id": card_id,
        "source_page": page,
        "title": clean_html_text(title_match.group(1)),
        "statement": re.sub(r"\s*\.\.\.$", "", snippet).strip(),
        "category": clean_html_text(spans[-1]) if spans else "Research Mathematics",
        "difficulty_level": int(difficulty_match.group(1)) if difficulty_match else None,
        "status": status_match.group(1).lower() if status_match else "unknown",
    }


def parse_unsolvedmath_index_page(payload: str, *, page: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    for card_id, block in re.findall(r'<a href="/problems/([^"?]+)"[^>]*>(.*?)</a>', payload, re.DOTALL):
        if card_id in seen:
            continue
        record = parse_unsolvedmath_index_card(card_id, block, page=page)
        if record:
            records.append(record)
            seen.add(card_id)
    return records


def parse_unsolvedmath_sets_page(payload: str) -> list[dict[str, Any]]:
    sets: list[dict[str, Any]] = []
    for set_id, block in re.findall(
        r'<a href="/problems\?set=(\d+)"[^>]*>(.*?)</a>',
        payload,
        re.DOTALL,
    ):
        title_match = re.search(r"<h3[^>]*>(.*?)<svg", block, re.DOTALL)
        description_match = re.search(r"<p[^>]*>(.*?)</p>", block, re.DOTALL)
        text = clean_html_text(block)
        count_match = re.search(r"(\d+)\s+problems", text)
        sets.append(
            {
                "set_id": int(set_id),
                "name": clean_html_text(title_match.group(1)) if title_match else f"Set {set_id}",
                "description": clean_html_text(description_match.group(1)) if description_match else "",
                "reported_problem_count": int(count_match.group(1)) if count_match else None,
            }
        )
    return sets


def _page_count(payload: str) -> int:
    match = re.search(r"Page\s+1\s+of\s+(\d+)", clean_html_text(payload))
    return int(match.group(1)) if match else 1


def _load_jsonl(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        source_id = str(row.get("source_id", "")).strip()
        if source_id:
            rows[source_id] = row
    return rows


class UnsolvedMathImporter:
    def __init__(
        self,
        *,
        repo_root: Path,
        base_url: str = UNSOLVEDMATH_BASE_URL,
        timeout: int = 30,
        workers: int = 6,
        request_delay: float = 0.05,
    ) -> None:
        self.repo_root = repo_root.expanduser().resolve()
        self.base_url = base_url.rstrip("/")
        self.timeout = max(1, int(timeout))
        self.workers = max(1, int(workers))
        self.request_delay = max(0.0, float(request_delay))
        self.raw_root = self.repo_root / "data" / "research_open" / "raw" / "unsolvedmath"
        self.bank_root = self.repo_root / "data" / "banks"
        self.details_path = self.raw_root / "problem_details.jsonl"
        self.detail_errors_path = self.raw_root / "problem_detail_errors.json"
        self.snapshot_path = self.repo_root / "data" / "research_open" / "unsolvedmath_snapshot.json"

    def _fetch_cached(self, url: str, path: Path, *, refresh: bool) -> str:
        if refresh or not path.exists():
            payload = fetch_text(url, timeout=self.timeout)
            _atomic_write_text(path, payload)
            if self.request_delay:
                time.sleep(self.request_delay)
            return payload
        return path.read_text(encoding="utf-8", errors="replace")

    def _fetch_index(
        self,
        *,
        refresh: bool,
    ) -> tuple[list[dict[str, Any]], dict[str, int]]:
        first_path = self.raw_root / "problems_page_001.html"
        first = self._fetch_cached(f"{self.base_url}/problems?page=1", first_path, refresh=refresh)
        page_count = _page_count(first)
        records = parse_unsolvedmath_index_page(first, page=1)
        for page in range(2, page_count + 1):
            path = self.raw_root / f"problems_page_{page:03d}.html"
            payload = self._fetch_cached(
                f"{self.base_url}/problems?{urlencode({'page': page})}",
                path,
                refresh=refresh,
            )
            records.extend(parse_unsolvedmath_index_page(payload, page=page))
        occurrences: dict[str, int] = {}
        deduplicated: dict[str, dict[str, Any]] = {}
        for record in records:
            source_id = str(record["source_id"])
            occurrences[source_id] = occurrences.get(source_id, 0) + 1
            deduplicated[source_id] = record
        return records, {
            "page_count": page_count,
            "card_rows": len(records),
            "unique_source_ids": len(deduplicated),
            "duplicate_card_occurrences": len(records) - len(deduplicated),
            "source_ids_repeated_across_pages": sum(
                1 for count in occurrences.values() if count > 1
            ),
        }

    def _fetch_sets(self, *, refresh: bool) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
        sets_payload = self._fetch_cached(
            f"{self.base_url}/sets",
            self.raw_root / "sets.html",
            refresh=refresh,
        )
        sets = parse_unsolvedmath_sets_page(sets_payload)
        memberships: dict[str, list[dict[str, Any]]] = {}
        for item in sets:
            set_id = int(item["set_id"])
            first_path = self.raw_root / f"set_{set_id:03d}_page_001.html"
            first = self._fetch_cached(
                f"{self.base_url}/problems?{urlencode({'set': set_id, 'page': 1})}",
                first_path,
                refresh=refresh,
            )
            page_count = _page_count(first)
            member_ids = {
                record["source_id"]
                for record in parse_unsolvedmath_index_page(first, page=1)
            }
            for page in range(2, page_count + 1):
                payload = self._fetch_cached(
                    f"{self.base_url}/problems?{urlencode({'set': set_id, 'page': page})}",
                    self.raw_root / f"set_{set_id:03d}_page_{page:03d}.html",
                    refresh=refresh,
                )
                member_ids.update(
                    record["source_id"]
                    for record in parse_unsolvedmath_index_page(payload, page=page)
                )
            item["downloaded_problem_count"] = len(member_ids)
            item["page_count"] = page_count
            membership = {"set_id": set_id, "name": item["name"]}
            for source_id in member_ids:
                memberships.setdefault(source_id, []).append(membership)
        for source_memberships in memberships.values():
            source_memberships.sort(key=lambda row: int(row["set_id"]))
        return sets, memberships

    def _fetch_one_detail(self, source_id: str) -> dict[str, Any]:
        url = f"{self.base_url}/problems/{source_id}"
        payload = fetch_text(url, timeout=self.timeout)
        problem = parse_unsolvedmath_detail_page(payload, expected_source_id=source_id)
        if self.request_delay:
            time.sleep(self.request_delay)
        return {
            "source_id": source_id,
            "source_url": url,
            "fetched_at": utc_now_iso(),
            "source_page_sha256": sha256_text(payload),
            "problem": problem,
        }

    def _fetch_details(
        self,
        source_ids: list[str],
        *,
        refresh: bool,
    ) -> tuple[dict[str, dict[str, Any]], list[dict[str, str]]]:
        details = {} if refresh else _load_jsonl(self.details_path)
        source_id_set = set(source_ids)
        details = {
            source_id: record
            for source_id, record in details.items()
            if source_id in source_id_set
        }
        pending = [source_id for source_id in source_ids if source_id not in details]
        errors: list[dict[str, str]] = []
        if pending:
            with ThreadPoolExecutor(max_workers=self.workers) as executor:
                futures = {
                    executor.submit(self._fetch_one_detail, source_id): source_id
                    for source_id in pending
                }
                completed = 0
                for future in as_completed(futures):
                    source_id = futures[future]
                    try:
                        details[source_id] = future.result()
                    except Exception as exc:
                        errors.append(
                            {
                                "source_id": source_id,
                                "source_url": f"{self.base_url}/problems/{source_id}",
                                "error": f"{type(exc).__name__}: {exc}",
                            }
                        )
                    completed += 1
                    if completed % 25 == 0:
                        _write_jsonl(
                            self.details_path,
                            (details[key] for key in sorted(details)),
                        )
        _write_jsonl(self.details_path, (details[key] for key in sorted(details)))
        _write_json(self.detail_errors_path, errors)
        return details, errors

    def _problem_record(
        self,
        index_record: dict[str, Any],
        detail_record: dict[str, Any] | None,
        memberships: list[dict[str, Any]],
        *,
        source_id_collision: bool = False,
        source_pages: list[int] | None = None,
        canonical_problem_id: str | None = None,
    ) -> dict[str, Any]:
        source_id = str(index_record["source_id"])
        detail = {} if source_id_collision else dict((detail_record or {}).get("problem") or {})
        title = str(detail.get("title") or index_record.get("title") or source_id).strip()
        statement = str(detail.get("statement") or index_record.get("statement") or "").strip()
        background = str(detail.get("background") or "").strip()
        detail_category = detail.get("category") if isinstance(detail.get("category"), dict) else {}
        category = str(
            detail_category.get("display_name")
            or detail_category.get("name")
            or index_record.get("category")
            or "Research Mathematics"
        ).strip()
        detail_difficulty = detail.get("difficulty") if isinstance(detail.get("difficulty"), dict) else {}
        difficulty_level = detail_difficulty.get("level", detail.get("difficulty_level_id"))
        if difficulty_level is None:
            difficulty_level = index_record.get("difficulty_level")
        detail_status = str(detail.get("status") or "").strip().lower()
        index_status = str(index_record.get("status") or "unknown").strip().lower()
        status = detail_status or index_status
        published = bool(detail.get("published", True))
        set_ids = {int(item["set_id"]) for item in memberships}
        erdos_member = ERDOS_SET_ID in set_ids or bool(re.fullmatch(r"EP-\d+", source_id, re.IGNORECASE))
        consistency_flags: list[str] = []
        index_title = str(index_record.get("title") or "").strip()
        index_statement = str(index_record.get("statement") or "").strip()
        if detail and normalize_for_comparison(title) != normalize_for_comparison(index_title):
            consistency_flags.append("title_conflict")
        normalized_index_statement = normalize_for_comparison(index_statement)
        normalized_detail_statement = normalize_for_comparison(statement)
        if (
            detail
            and normalized_index_statement
            and not normalized_detail_statement.startswith(normalized_index_statement)
            and not normalized_index_statement.startswith(normalized_detail_statement)
        ):
            consistency_flags.append("statement_conflict")
        if detail_status and index_status not in {"", "unknown"} and detail_status != index_status:
            consistency_flags.append("status_conflict")
        if source_id_collision:
            consistency_flags.extend(
                ["source_id_collision", "detail_statement_unavailable_for_index_variant"]
            )
        elif not detail:
            consistency_flags.append("detail_fetch_failed")
        detail_url = f"{self.base_url}/problems/{source_id}"
        tags = [
            "unsolvedmath",
            "research_problem",
            f"difficulty_L{difficulty_level}" if difficulty_level is not None else "difficulty_unknown",
            (
                "index_collision_variant"
                if source_id_collision
                else "detail_statement"
                if detail
                else "index_statement_fallback"
            ),
        ]
        if erdos_member:
            tags.append("erdos_set_member")
        tags.extend(f"unsolvedmath_set_{item['set_id']}" for item in memberships)
        if consistency_flags:
            tags.append("source_data_conflict")
        if source_id_collision:
            notes = (
                "Imported from an UnsolvedMath browse-index card whose source id is also used by a "
                "different detail-page problem. Recover an authoritative detail statement before attack."
            )
        elif detail:
            notes = "Imported from the UnsolvedMath detail page."
        else:
            notes = "Imported from the UnsolvedMath browse index because the detail page was unavailable."
        if background:
            notes += f"\n\nBackground: {background}"
        return {
            "problem_id": (
                f"unsolvedmath-{source_id.lower()}-collision-{slugify(title)[:36]}-"
                f"{sha256_text(normalize_for_comparison(title))[:8]}"
                if source_id_collision
                else f"unsolvedmath-{source_id.lower()}"
            ),
            "title": title,
            "source": "UnsolvedMath",
            "statement": statement or f"UnsolvedMath record {source_id} has no recoverable statement.",
            "domain": normalize_domain(category),
            "tags": tags,
            "open_problem": status == "open" and published,
            "formalized": "no",
            "notes": notes,
            "references": (
                [
                    f"{self.base_url}/problems?page={index_record.get('source_page')}",
                    detail_url,
                ]
                if source_id_collision
                else [detail_url]
            ),
            "hypotheses": [
                "Treat a counterexample as provisional until its witness is checked by an independent verifier.",
                "A bounded search without a witness is evidence only for the stated finite range.",
            ],
            "recommended_strategy": [
                "Normalize the exact quantifiers and definitions before executable search.",
                "Search the smallest admissible objects first and persist a reproducible witness certificate.",
                "If the full claim is not finitely refutable, isolate universal or equivalence subclaims.",
            ],
            "metadata": {
                "research_collection": "research_open_problem_collections",
                "source_catalog": "unsolvedmath",
                "source_id": source_id,
                "source_page": index_record.get("source_page"),
                "source_pages": sorted(
                    set(source_pages or [int(index_record.get("source_page") or 0)])
                ),
                "source_url": detail_url,
                "source_internal_id": detail.get("id"),
                "status": status,
                "index_status": index_status,
                "detail_status": detail_status or None,
                "published": published,
                "difficulty_level": difficulty_level,
                "difficulty_name": detail_difficulty.get("name"),
                "category": category,
                "proposed_by": detail.get("proposed_by"),
                "proposed_year": detail.get("proposed_year"),
                "source_created_at": detail.get("created_at"),
                "source_updated_at": detail.get("updated_at"),
                "detail_fetched_at": (
                    None if source_id_collision else (detail_record or {}).get("fetched_at")
                ),
                "source_page_sha256": (
                    None
                    if source_id_collision
                    else (detail_record or {}).get("source_page_sha256")
                ),
                "statement_quality": (
                    "index_collision_snippet"
                    if source_id_collision
                    else "detail_page"
                    if detail
                    else "index_snippet_fallback"
                ),
                "index_title": index_title,
                "index_statement": index_statement,
                "source_consistency_flags": consistency_flags,
                "sets": memberships,
                "erdos_set_member": erdos_member,
                "source_id_collision": source_id_collision,
                "canonical_source_record_id": canonical_problem_id,
            },
        }

    @staticmethod
    def _mark_duplicates(records: list[dict[str, Any]]) -> dict[str, int]:
        parents = list(range(len(records)))

        def find(index: int) -> int:
            while parents[index] != index:
                parents[index] = parents[parents[index]]
                index = parents[index]
            return index

        def union(left: int, right: int) -> None:
            left_root = find(left)
            right_root = find(right)
            if left_root != right_root:
                parents[right_root] = left_root

        fingerprints: dict[str, int] = {}
        title_keys: dict[str, int] = {}
        for index, record in enumerate(records):
            fingerprint_input = " ".join(
                [
                    normalize_for_comparison(str(record.get("title", ""))),
                    normalize_for_comparison(str(record.get("statement", ""))),
                ]
            ).strip()
            fingerprint = sha256_text(fingerprint_input)
            record["metadata"]["content_fingerprint"] = fingerprint
            previous_fingerprint = fingerprints.get(fingerprint)
            if previous_fingerprint is None:
                fingerprints[fingerprint] = index
            else:
                union(previous_fingerprint, index)
            title_key = normalized_problem_title(
                str(record.get("title", "")),
                domain=str(record.get("domain", "")),
            )
            record["metadata"]["normalized_title_key"] = title_key or None
            if title_key:
                previous_title = title_keys.get(title_key)
                if previous_title is None:
                    title_keys[title_key] = index
                else:
                    union(previous_title, index)

        components: dict[int, list[int]] = {}
        for index in range(len(records)):
            components.setdefault(find(index), []).append(index)

        exact_duplicates = 0
        title_duplicates = 0
        duplicate_records = 0
        for members in components.values():
            canonical_index = min(
                members,
                key=lambda index: (
                    records[index]["metadata"].get("statement_quality") != "detail_page",
                    "title_conflict"
                    in records[index]["metadata"].get("source_consistency_flags", []),
                    "status_conflict"
                    in records[index]["metadata"].get("source_consistency_flags", []),
                    "statement_conflict"
                    in records[index]["metadata"].get("source_consistency_flags", []),
                    not bool(records[index]["metadata"].get("sets")),
                    str(records[index]["problem_id"]),
                ),
            )
            canonical = records[canonical_index]
            for index in members:
                record = records[index]
                if index == canonical_index:
                    record["metadata"]["duplicate_of"] = None
                    record["metadata"]["duplicate_match"] = None
                    continue
                exact = (
                    record["metadata"]["content_fingerprint"]
                    == canonical["metadata"]["content_fingerprint"]
                )
                record["metadata"]["duplicate_of"] = canonical["problem_id"]
                record["metadata"]["duplicate_match"] = (
                    "exact_content" if exact else "normalized_title"
                )
                record["tags"].append("duplicate_record")
                duplicate_records += 1
                if exact:
                    exact_duplicates += 1
                else:
                    title_duplicates += 1
        return {
            "duplicate_records": duplicate_records,
            "exact_content_duplicates": exact_duplicates,
            "normalized_title_duplicates": title_duplicates,
        }

    def _update_registry(self, *, generated_at: str, counts: dict[str, int]) -> None:
        registry_path = self.repo_root / "data" / "bank_registry.yaml"
        entries = yaml.safe_load(registry_path.read_text(encoding="utf-8")) or []
        names = {
            "unsolvedmath_index",
            "unsolvedmath_all",
            "unsolvedmath_open",
            "unsolvedmath_open_non_erdos",
            "unsolvedmath_source_id_collisions",
        }
        entries = [entry for entry in entries if str(entry.get("name", "")) not in names]

        def entry(name: str, filename: str, description: str, count: int, tags: list[str]) -> dict[str, Any]:
            return {
                "name": name,
                "path": str(self.bank_root / filename),
                "description": description,
                "category": "research_open_natural_language",
                "problem_count": count,
                "provenance": self.base_url,
                "focus_tags": tags,
                "synced_at": generated_at,
            }

        entries.extend(
            [
                entry(
                    "unsolvedmath_index",
                    "unsolvedmath_index.yaml",
                    "Compatibility alias for the full normalized UnsolvedMath concept snapshot.",
                    counts["all_records"],
                    ["unsolvedmath", "research_problem", "compatibility_alias"],
                ),
                entry(
                    "unsolvedmath_all",
                    "unsolvedmath_all.yaml",
                    "Full UnsolvedMath snapshot with detail statements, source status, set membership, and data-quality flags.",
                    counts["all_records"],
                    ["unsolvedmath", "detail_statement", "research_problem"],
                ),
                entry(
                    "unsolvedmath_open",
                    "unsolvedmath_open.yaml",
                    "All records currently marked open by the UnsolvedMath detail snapshot.",
                    counts["open_records"],
                    ["unsolvedmath", "open_problem", "detail_statement"],
                ),
                entry(
                    "unsolvedmath_open_non_erdos",
                    "unsolvedmath_open_non_erdos.yaml",
                    "Canonical open UnsolvedMath records excluding the Erdos set and normalized duplicate records.",
                    counts["open_non_erdos_canonical"],
                    ["unsolvedmath", "open_problem", "non_erdos", "counterexample_campaign"],
                ),
                entry(
                    "unsolvedmath_source_id_collisions",
                    "unsolvedmath_source_id_collisions.yaml",
                    "Browse-index records whose source id resolves to a different UnsolvedMath detail-page problem.",
                    counts["source_id_collision_records"],
                    ["unsolvedmath", "source_id_collision", "source_audit"],
                ),
            ]
        )
        _write_yaml(registry_path, entries)

    def _update_collection_metadata(self, *, generated_at: str, counts: dict[str, int]) -> None:
        collection_path = self.repo_root / "data" / "research_open" / "collection.json"
        if collection_path.exists():
            collection = json.loads(collection_path.read_text(encoding="utf-8"))
        else:
            collection = {
                "collection_id": "research_open_problem_collections",
                "purpose": "Provide research-level open problem collections for AMRA.",
                "sources": [],
            }
        collection["generated_at"] = generated_at
        banks = dict(collection.get("banks") or {})
        banks.update(
            {
                "unsolvedmath_index": "data/banks/unsolvedmath_index.yaml",
                "unsolvedmath_all": "data/banks/unsolvedmath_all.yaml",
                "unsolvedmath_open": "data/banks/unsolvedmath_open.yaml",
                "unsolvedmath_open_non_erdos": "data/banks/unsolvedmath_open_non_erdos.yaml",
                "unsolvedmath_source_id_collisions": (
                    "data/banks/unsolvedmath_source_id_collisions.yaml"
                ),
            }
        )
        collection["banks"] = banks
        source = {
            "id": "unsolvedmath",
            "name": "UnsolvedMath",
            "source_url": self.base_url,
            "synced_at": generated_at,
            "license": "Source-specific; raw detail HTML is not redistributed by this snapshot",
            "local_path": str(self.raw_root.relative_to(self.repo_root)),
            "formats": ["html_index", "nextjs_problem_payload", "jsonl", "yaml"],
            "modalities": [
                "natural_language_problem_statement",
                "difficulty_metadata",
                "category_metadata",
                "problem_set_membership",
                "source_consistency_audit",
            ],
            "difficulty": "advanced_to_millennium",
            "counts": counts,
            "recommended_use": (
                "Use the canonical non-Erdos open bank for counterexample campaigns; reconcile records "
                "with title conflicts before mathematical attack."
            ),
        }
        sources = [
            item
            for item in list(collection.get("sources") or [])
            if str(item.get("id", "")) != "unsolvedmath"
        ]
        insertion = next(
            (
                index + 1
                for index, item in enumerate(sources)
                if str(item.get("id", "")) == "formal_conjectures"
            ),
            len(sources),
        )
        sources.insert(insertion, source)
        collection["sources"] = sources
        _write_json(collection_path, collection)

        readme_path = self.repo_root / "data" / "research_open" / "README.md"
        if not readme_path.exists():
            return
        readme = readme_path.read_text(encoding="utf-8")
        readme = re.sub(r"^Generated: .*$", f"Generated: {generated_at}", readme, flags=re.MULTILINE)
        unsolved_rows = "\n".join(
            [
                f"| UnsolvedMath | `unsolvedmath_all` | {counts['all_records']} | Full normalized snapshot and source audit |",
                f"| UnsolvedMath | `unsolvedmath_open` | {counts['open_records']} | Records currently marked open |",
                (
                    f"| UnsolvedMath | `unsolvedmath_open_non_erdos` | "
                    f"{counts['open_non_erdos_canonical']} | Canonical non-Erdos counterexample queue |"
                ),
                (
                    f"| UnsolvedMath | `unsolvedmath_source_id_collisions` | "
                    f"{counts['source_id_collision_records']} | Ambiguous index records requiring source recovery |"
                ),
            ]
        )
        readme = re.sub(
            r"(?:^\| UnsolvedMath \|.*$\n?)+",
            unsolved_rows + "\n",
            readme,
            flags=re.MULTILINE,
        )
        readme = re.sub(
            r"- UnsolvedMath records are imported from browse-index pages and may contain\n"
            r"  shortened statements\. Fetch the detail page and validate status before proof\n"
            r"  search\.",
            (
                "- UnsolvedMath detail statements, statuses, set memberships, and source-page hashes are\n"
                "  stored locally. Records with index/detail title conflicts require source reconciliation\n"
                "  before proof or counterexample work."
            ),
            readme,
        )
        if "scripts/import_unsolvedmath.py --refresh" not in readme:
            readme = readme.rstrip() + (
                "\n\nRefresh only UnsolvedMath:\n\n"
                "```bash\npython3 scripts/import_unsolvedmath.py --refresh\n```\n"
            )
        _atomic_write_text(readme_path, readme)

    def run(
        self,
        *,
        refresh: bool = False,
        refresh_details: bool = False,
    ) -> dict[str, Any]:
        generated_at = utc_now_iso()
        previous_snapshot: dict[str, Any] = {}
        if self.snapshot_path.exists():
            try:
                previous_snapshot = json.loads(
                    self.snapshot_path.read_text(encoding="utf-8")
                )
            except (OSError, json.JSONDecodeError):
                previous_snapshot = {}
        self.raw_root.mkdir(parents=True, exist_ok=True)
        index_occurrences, index_stats = self._fetch_index(refresh=refresh)
        sets, memberships = self._fetch_sets(refresh=refresh)
        source_ids = sorted({str(record["source_id"]) for record in index_occurrences})
        details, detail_errors = self._fetch_details(source_ids, refresh=refresh_details)
        occurrences_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for occurrence in index_occurrences:
            occurrences_by_source[str(occurrence["source_id"])].append(occurrence)

        records: list[dict[str, Any]] = []
        source_ids_with_title_collisions = 0
        source_id_collision_records = 0
        index_title_concepts = 0
        for source_id in source_ids:
            occurrences = occurrences_by_source[source_id]
            title_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for occurrence in occurrences:
                title_key = (
                    normalized_problem_title(str(occurrence.get("title", "")))
                    or normalize_for_comparison(str(occurrence.get("title", "")))
                )
                title_groups[title_key].append(occurrence)
            index_title_concepts += len(title_groups)
            if len(title_groups) > 1:
                source_ids_with_title_collisions += 1

            detail_record = details.get(source_id)
            detail = dict((detail_record or {}).get("problem") or {})
            detail_title = normalize_for_comparison(str(detail.get("title", "")))
            primary_key = next(
                (
                    key
                    for key, group in title_groups.items()
                    if any(
                        normalize_for_comparison(str(item.get("title", ""))) == detail_title
                        for item in group
                    )
                ),
                next(iter(title_groups)),
            )
            group_summaries = [
                {
                    "normalized_title": key,
                    "titles": sorted(
                        {str(item.get("title", "")).strip() for item in group}
                    ),
                    "source_pages": sorted(
                        {int(item.get("source_page") or 0) for item in group}
                    ),
                }
                for key, group in sorted(title_groups.items())
            ]

            primary_group = title_groups[primary_key]
            primary_occurrence = max(
                primary_group,
                key=lambda item: len(str(item.get("statement", ""))),
            )
            primary_problem_id = f"unsolvedmath-{source_id.lower()}"
            primary_record = self._problem_record(
                primary_occurrence,
                detail_record,
                memberships.get(source_id, []),
                source_pages=[
                    int(item.get("source_page") or 0)
                    for item in primary_group
                ],
                canonical_problem_id=primary_problem_id,
            )
            if len(title_groups) > 1:
                primary_record["metadata"]["source_id_index_title_groups"] = group_summaries
            records.append(primary_record)

            for title_key, group in sorted(title_groups.items()):
                if title_key == primary_key:
                    continue
                collision_occurrence = max(
                    group,
                    key=lambda item: len(str(item.get("statement", ""))),
                )
                collision_record = self._problem_record(
                    collision_occurrence,
                    None,
                    [],
                    source_id_collision=True,
                    source_pages=[
                        int(item.get("source_page") or 0)
                        for item in group
                    ],
                    canonical_problem_id=primary_problem_id,
                )
                collision_record["metadata"]["source_id_index_title_groups"] = group_summaries
                records.append(collision_record)
                source_id_collision_records += 1
        records.sort(key=lambda record: str(record["problem_id"]))
        duplicate_counts = self._mark_duplicates(records)
        open_records = [record for record in records if record["open_problem"]]
        open_non_erdos = [
            record
            for record in open_records
            if not record["metadata"]["erdos_set_member"]
        ]
        attack_records = [
            record
            for record in open_non_erdos
            if not record["metadata"].get("duplicate_of")
        ]
        collision_records = [
            record for record in records if record["metadata"].get("source_id_collision")
        ]

        _write_yaml(self.bank_root / "unsolvedmath_all.yaml", records)
        _write_yaml(self.bank_root / "unsolvedmath_open.yaml", open_records)
        _write_yaml(self.bank_root / "unsolvedmath_open_non_erdos.yaml", attack_records)
        _write_yaml(
            self.bank_root / "unsolvedmath_source_id_collisions.yaml",
            collision_records,
        )
        # Preserve the historical bank name while upgrading it to the current full index.
        _write_yaml(self.bank_root / "unsolvedmath_index.yaml", records)

        counts = {
            "index_records": len(source_ids),
            "index_page_count": index_stats["page_count"],
            "index_card_rows": index_stats["card_rows"],
            "index_unique_source_ids": index_stats["unique_source_ids"],
            "index_title_concepts": index_title_concepts,
            "index_duplicate_card_occurrences": index_stats["duplicate_card_occurrences"],
            "index_source_ids_repeated_across_pages": index_stats[
                "source_ids_repeated_across_pages"
            ],
            "source_ids_with_title_collisions": source_ids_with_title_collisions,
            "source_id_collision_records": source_id_collision_records,
            "detail_records": len(details),
            "detail_errors": len(detail_errors),
            "all_records": len(records),
            "open_records": len(open_records),
            "erdos_open_records": sum(
                1 for record in open_records if record["metadata"]["erdos_set_member"]
            ),
            "open_non_erdos_records": len(open_non_erdos),
            "open_non_erdos_canonical": len(attack_records),
            "duplicate_records": duplicate_counts["duplicate_records"],
            "exact_content_duplicate_records": duplicate_counts["exact_content_duplicates"],
            "normalized_title_duplicate_records": duplicate_counts["normalized_title_duplicates"],
            "source_conflict_records": sum(
                1 for record in records if record["metadata"]["source_consistency_flags"]
            ),
            "canonical_source_conflict_records": sum(
                1
                for record in records
                if record["metadata"]["source_consistency_flags"]
                and not record["metadata"].get("source_id_collision")
            ),
        }
        detail_fetch_times = sorted(
            str(record.get("fetched_at"))
            for record in details.values()
            if record.get("fetched_at")
        )
        index_snapshot_path = self.raw_root / "problems_page_001.html"
        index_mtime = (
            datetime.fromtimestamp(
                index_snapshot_path.stat().st_mtime,
                timezone.utc,
            )
            .replace(microsecond=0)
            .isoformat()
            if index_snapshot_path.exists()
            else None
        )
        last_index_refresh_at = (
            generated_at
            if refresh
            else previous_snapshot.get("last_index_and_sets_refresh_at")
            or index_mtime
        )
        snapshot = {
            "schema_version": "amra.unsolvedmath_snapshot.v1",
            "generated_at": generated_at,
            "source_url": self.base_url,
            "index_and_sets_refreshed_this_run": refresh,
            "details_refreshed_this_run": refresh_details,
            "last_index_and_sets_refresh_at": last_index_refresh_at,
            "detail_fetch_window": {
                "started_at": detail_fetch_times[0] if detail_fetch_times else None,
                "finished_at": detail_fetch_times[-1] if detail_fetch_times else None,
            },
            "counts": counts,
            "sets": sets,
            "artifacts": {
                "raw_index_root": str(self.raw_root),
                "detail_snapshot": str(self.details_path),
                "detail_errors": str(self.detail_errors_path),
                "all_bank": str(self.bank_root / "unsolvedmath_all.yaml"),
                "open_bank": str(self.bank_root / "unsolvedmath_open.yaml"),
                "open_non_erdos_bank": str(self.bank_root / "unsolvedmath_open_non_erdos.yaml"),
                "source_id_collisions_bank": str(
                    self.bank_root / "unsolvedmath_source_id_collisions.yaml"
                ),
            },
            "checksums_sha256": {
                "detail_snapshot": sha256_file(self.details_path),
                "all_bank": sha256_file(self.bank_root / "unsolvedmath_all.yaml"),
                "open_bank": sha256_file(self.bank_root / "unsolvedmath_open.yaml"),
                "open_non_erdos_bank": sha256_file(
                    self.bank_root / "unsolvedmath_open_non_erdos.yaml"
                ),
                "source_id_collisions_bank": sha256_file(
                    self.bank_root / "unsolvedmath_source_id_collisions.yaml"
                ),
            },
            "policy": {
                "open_status_source": "detail page when available; browse index fallback otherwise",
                "erdos_exclusion": "membership in UnsolvedMath set 8 or EP-{number} source id",
                "deduplication": (
                    "exact normalized title-plus-statement fingerprint plus conservative normalized-title aliases; "
                    "the canonical record is chosen by source-consistency quality"
                ),
                "source_id_collisions": (
                    "Distinct browse-index titles sharing one source id are preserved as index-collision "
                    "records; they require statement recovery because the shared detail URL is ambiguous"
                ),
                "detail_storage": "extracted Next.js problem payload plus source page SHA-256; raw detail HTML is not redistributed",
            },
        }
        _write_json(self.snapshot_path, snapshot)
        self._update_registry(generated_at=generated_at, counts=counts)
        self._update_collection_metadata(generated_at=generated_at, counts=counts)
        return snapshot


def import_unsolvedmath_snapshot(
    *,
    repo_root: Path,
    refresh: bool = False,
    refresh_details: bool = False,
    timeout: int = 30,
    workers: int = 6,
    request_delay: float = 0.05,
    base_url: str = UNSOLVEDMATH_BASE_URL,
) -> dict[str, Any]:
    return UnsolvedMathImporter(
        repo_root=repo_root,
        base_url=base_url,
        timeout=timeout,
        workers=workers,
        request_delay=request_delay,
    ).run(refresh=refresh, refresh_details=refresh_details)


__all__ = [
    "ERDOS_SET_ID",
    "UNSOLVEDMATH_BASE_URL",
    "UnsolvedMathImporter",
    "clean_html_text",
    "import_unsolvedmath_snapshot",
    "normalize_for_comparison",
    "normalized_problem_title",
    "parse_unsolvedmath_detail_page",
    "parse_unsolvedmath_index_page",
    "parse_unsolvedmath_sets_page",
    "sha256_file",
]
