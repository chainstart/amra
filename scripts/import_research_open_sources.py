#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data"
RESEARCH_OPEN_ROOT = DATA_ROOT / "research_open"
RAW_ROOT = RESEARCH_OPEN_ROOT / "raw"
BANK_ROOT = DATA_ROOT / "banks"
REGISTRY_PATH = DATA_ROOT / "bank_registry.yaml"

FORMAL_CONJECTURES_REPO = "https://github.com/google-deepmind/formal-conjectures.git"
FORMAL_CONJECTURES_WEB = "https://github.com/google-deepmind/formal-conjectures"
FORMAL_CONJECTURES_RAW = RAW_ROOT / "formal_conjectures"
UNSOLVEDMATH_BASE = "https://www.unsolvedmath.com"
UNSOLVEDMATH_RAW = RAW_ROOT / "unsolvedmath"
AIM_PROBLEM_LISTS_URL = "https://aimath.org/problemlists/"
AIM_RAW = RAW_ROOT / "aim_problem_lists"
USER_AGENT = "amra-research-open-importer/0.1"


SCRIPT_STYLE_PATTERN = re.compile(r"<(script|style)\b.*?</\1>", re.IGNORECASE | re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")
URL_PATTERN = re.compile(r"https?://[^\s\"'<>)]+" )


@dataclass
class ImportCounts:
    formal_conjectures_total: int = 0
    formal_conjectures_open_research: int = 0
    unsolvedmath_total: int = 0
    aim_problem_lists_total: int = 0


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def fetch_text(url: str, *, timeout: int = 30) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="ignore")


def clean_html_text(payload: str) -> str:
    without_scripts = SCRIPT_STYLE_PATTERN.sub(" ", payload)
    without_tags = TAG_PATTERN.sub(" ", without_scripts)
    decoded = html.unescape(without_tags)
    decoded = decoded.replace("\xa0", " ")
    return WHITESPACE_PATTERN.sub(" ", decoded).strip()


def slugify(value: str) -> str:
    lowered = value.lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    return lowered.strip("-") or "item"


def normalize_domain(value: str) -> str:
    normalized = value.strip().lower().replace("&", "and")
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "research_mathematics"


def problem_record(
    *,
    problem_id: str,
    title: str,
    source: str,
    statement: str,
    domain: str,
    tags: list[str],
    open_problem: bool,
    formalized: str,
    notes: str,
    references: list[str],
    hypotheses: list[str],
    recommended_strategy: list[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    return {
        "problem_id": problem_id,
        "title": title,
        "source": source,
        "statement": statement,
        "domain": domain,
        "tags": tags,
        "open_problem": open_problem,
        "formalized": formalized,
        "notes": notes,
        "references": references,
        "hypotheses": hypotheses,
        "recommended_strategy": recommended_strategy,
        "metadata": metadata,
    }


def write_yaml(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
    )


def ensure_unique_problem_ids(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: dict[str, int] = {}
    for record in records:
        original = str(record["problem_id"])
        count = seen.get(original, 0)
        if count:
            metadata = record.get("metadata") or {}
            suffix_source = (
                str(metadata.get("source_file", ""))
                or str(metadata.get("topic", ""))
                or str(metadata.get("source_catalog", ""))
                or str(count + 1)
            )
            suffix = slugify(suffix_source)[-40:] or str(count + 1)
            candidate = f"{original}-{suffix}"
            while candidate in seen:
                count += 1
                candidate = f"{original}-{suffix}-{count + 1}"
            record["problem_id"] = candidate
            seen[candidate] = 1
        seen[original] = count + 1
    return records


def read_yaml(path: Path) -> Any:
    if not path.exists():
        return []
    return yaml.safe_load(path.read_text(encoding="utf-8")) or []


def clone_formal_conjectures() -> str:
    RAW_ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="amra-formal-conjectures-") as tmp:
        tmp_path = Path(tmp) / "formal_conjectures"
        subprocess.run(
            ["git", "clone", "--depth", "1", FORMAL_CONJECTURES_REPO, str(tmp_path)],
            check=True,
        )
        revision = subprocess.check_output(
            ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
            text=True,
        ).strip()
        if FORMAL_CONJECTURES_RAW.exists():
            shutil.rmtree(FORMAL_CONJECTURES_RAW)
        shutil.copytree(tmp_path, FORMAL_CONJECTURES_RAW, ignore=shutil.ignore_patterns(".git"))
    return revision


def current_formal_conjectures_revision() -> str:
    git_head = FORMAL_CONJECTURES_RAW / ".git" / "HEAD"
    if (FORMAL_CONJECTURES_RAW / ".git").exists():
        return subprocess.check_output(
            ["git", "-C", str(FORMAL_CONJECTURES_RAW), "rev-parse", "HEAD"],
            text=True,
        ).strip()
    manifest = RESEARCH_OPEN_ROOT / "collection.json"
    if not manifest.exists():
        manifest = RESEARCH_OPEN_ROOT / "suite.json"
    if manifest.exists():
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        for source in payload.get("sources", []):
            if source.get("id") == "formal_conjectures":
                return str(source.get("source_revision", ""))
    return ""


def trim_lean_declaration(lines: list[str]) -> str:
    text = "\n".join(lines).strip()
    text = re.split(r"\s*:=\s*by\b", text, maxsplit=1)[0].strip()
    text = re.split(r"\s*:=\s*sorry\b", text, maxsplit=1)[0].strip()
    return text


def parse_formal_conjecture_file(path: Path, *, revision: str) -> list[dict[str, Any]]:
    rel_path = path.relative_to(FORMAL_CONJECTURES_RAW)
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    records: list[dict[str, Any]] = []
    file_urls = sorted(set(URL_PATTERN.findall("\n".join(lines))))
    idx = 0

    while idx < len(lines):
        line = lines[idx].strip()
        if not line.startswith("@[category"):
            idx += 1
            continue

        attr_lines = [lines[idx].strip()]
        while "]" not in attr_lines[-1] and idx + 1 < len(lines):
            idx += 1
            attr_lines.append(lines[idx].strip())
        attr_text = " ".join(attr_lines)
        category_match = re.search(r"category\s+([A-Za-z_]+)(?:\s+([A-Za-z_]+))?", attr_text)
        category = category_match.group(1).lower() if category_match else "unknown"
        status = (category_match.group(2).lower() if category_match and category_match.group(2) else "")
        ams_codes = re.findall(r"\bAMS\s+([0-9 ]+)", attr_text)
        ams = ams_codes[0].split() if ams_codes else []

        idx += 1
        while idx < len(lines) and not lines[idx].strip():
            idx += 1

        decl_lines: list[str] = []
        while idx < len(lines) and len(decl_lines) < 80:
            decl_lines.append(lines[idx])
            if ":= by" in lines[idx] or ":= sorry" in lines[idx]:
                break
            idx += 1

        declaration = trim_lean_declaration(decl_lines)
        name_match = re.search(r"\b(theorem|lemma|def)\s+([^\s:]+)", declaration)
        if not name_match:
            idx += 1
            continue
        kind = name_match.group(1)
        name = name_match.group(2)

        source_url = f"{FORMAL_CONJECTURES_WEB}/blob/{revision}/{rel_path.as_posix()}"
        problem_id = "formal-conjectures-" + slugify(name.replace("«", "").replace("»", ""))
        is_open_research = category == "research" and status == "open"
        records.append(
            problem_record(
                problem_id=problem_id,
                title=f"Formal Conjectures: {name}",
                source="Google DeepMind Formal Conjectures",
                statement="Formal Lean declaration:\n\n```lean\n" + declaration + "\n```",
                domain="research_mathematics",
                tags=[
                    "formal_conjectures",
                    "lean4",
                    f"category_{category}",
                    f"status_{status or 'unspecified'}",
                    "research_open" if is_open_research else "research_statement_corpus",
                ],
                open_problem=is_open_research,
                formalized="lean4_statement",
                notes=(
                    "Imported from the Formal Conjectures Lean 4 repository. "
                    "The import records statement targets only; AMRA success requires replacing sorry with a no-sorry proof."
                ),
                references=[source_url, *file_urls[:8]],
                hypotheses=[
                    "Treat the Lean declaration as the research target contract.",
                    "Do not use external proof scripts during independence runs.",
                ],
                recommended_strategy=[
                    "Start with dependency discovery from imports and local definitions.",
                    "Attempt small verified lemmas before attacking the top-level conjecture.",
                    "Accept success only when the target closes without sorry/admit/axiom placeholders.",
                ],
                metadata={
                    "research_collection": "research_open_problem_collections",
                    "source_catalog": "formal_conjectures",
                    "source_revision": revision,
                    "source_file": str(rel_path),
                    "declaration_name": name,
                    "declaration_kind": kind,
                    "category": category,
                    "status": status,
                    "ams_codes": ams,
                    "statement_quality": "formal_lean4",
                },
            )
        )
        idx += 1

    return records


def import_formal_conjectures(*, refresh: bool) -> tuple[list[dict[str, Any]], str]:
    if refresh or not FORMAL_CONJECTURES_RAW.exists():
        revision = clone_formal_conjectures()
    else:
        revision = current_formal_conjectures_revision()
    if not revision:
        revision = "unknown"

    records: list[dict[str, Any]] = []
    for path in sorted((FORMAL_CONJECTURES_RAW / "FormalConjectures").rglob("*.lean")):
        records.extend(parse_formal_conjecture_file(path, revision=revision))

    ensure_unique_problem_ids(records)
    open_research = [record for record in records if record["open_problem"]]
    write_yaml(BANK_ROOT / "formal_conjectures_open_research.yaml", open_research)
    write_yaml(BANK_ROOT / "formal_conjectures_all.yaml", records)
    return records, revision


def fetch_unsolvedmath_pages(*, refresh: bool, delay: float) -> list[Path]:
    UNSOLVEDMATH_RAW.mkdir(parents=True, exist_ok=True)
    first_page = UNSOLVEDMATH_RAW / "problems_page_001.html"
    if refresh or not first_page.exists():
        first_page.write_text(
            fetch_text(f"{UNSOLVEDMATH_BASE}/problems?page=1"),
            encoding="utf-8",
        )
        time.sleep(delay)

    first_text = first_page.read_text(encoding="utf-8", errors="ignore")
    page_match = re.search(r"Page\s+1\s+of\s+(\d+)", clean_html_text(first_text))
    page_count = int(page_match.group(1)) if page_match else 1
    paths = [first_page]
    for page in range(2, page_count + 1):
        path = UNSOLVEDMATH_RAW / f"problems_page_{page:03d}.html"
        if refresh or not path.exists():
            path.write_text(
                fetch_text(f"{UNSOLVEDMATH_BASE}/problems?page={page}"),
                encoding="utf-8",
            )
            time.sleep(delay)
        paths.append(path)
    return paths


def parse_unsolvedmath_card(card_id: str, block: str, *, page: int) -> dict[str, Any] | None:
    title_match = re.search(r"<h3[^>]*>(.*?)</h3>", block, re.DOTALL)
    snippet_match = re.search(r"<p[^>]*>(.*?)</p>", block, re.DOTALL)
    spans = re.findall(r"<span[^>]*>(.*?)</span>", block, re.DOTALL)
    difficulty_match = re.search(r">L(?:<!--\s*-->)?(\d)<", block)
    status_match = re.search(r">(Open|Solved|Closed|Unknown)<", block)
    if not title_match:
        return None
    title = clean_html_text(title_match.group(1))
    snippet = clean_html_text(snippet_match.group(1)) if snippet_match else ""
    snippet = re.sub(r"\s*\.\.\.$", "", snippet).strip()
    category = clean_html_text(spans[-1]) if spans else "research_mathematics"
    level = int(difficulty_match.group(1)) if difficulty_match else None
    status = status_match.group(1).lower() if status_match else "open"
    reference = f"{UNSOLVEDMATH_BASE}/problems/{card_id}"
    return problem_record(
        problem_id=f"unsolvedmath-{card_id.lower()}",
        title=title,
        source="UnsolvedMath",
        statement=snippet or f"Open problem listed by UnsolvedMath as {card_id}. Fetch the detail page before proof search.",
        domain=normalize_domain(category),
        tags=["unsolvedmath", "open_problem_index", f"difficulty_L{level}" if level else "difficulty_unknown"],
        open_problem=status == "open",
        formalized="no",
        notes=(
            "Imported from the UnsolvedMath browse index. "
            "The index entry may contain a shortened statement; fetch the detail page before formal proof work."
        ),
        references=[reference],
        hypotheses=["Verify the exact statement and current status against the source page before any proof attempt."],
        recommended_strategy=[
            "Use this bank for triage, difficulty filtering, and source recovery.",
            "Promote selected entries to curated problem projects only after detail-page validation.",
        ],
        metadata={
            "research_collection": "research_open_problem_collections",
            "source_catalog": "unsolvedmath",
            "source_page": page,
            "source_id": card_id,
            "status": status,
            "difficulty_level": level,
            "category": category,
            "statement_quality": "index_snippet",
        },
    )


def import_unsolvedmath(*, refresh: bool, delay: float) -> list[dict[str, Any]]:
    paths = fetch_unsolvedmath_pages(refresh=refresh, delay=delay)
    records: dict[str, dict[str, Any]] = {}
    for path in paths:
        page_match = re.search(r"(\d+)", path.stem)
        page = int(page_match.group(1)) if page_match else 0
        text = path.read_text(encoding="utf-8", errors="ignore")
        for card_id, block in re.findall(r'<a href="/problems/([^"]+)"[^>]*>(.*?)</a>', text, re.DOTALL):
            record = parse_unsolvedmath_card(card_id, block, page=page)
            if record:
                records[record["problem_id"]] = record
    ordered = [records[key] for key in sorted(records)]
    ensure_unique_problem_ids(ordered)
    write_yaml(BANK_ROOT / "unsolvedmath_index.yaml", ordered)
    return ordered


def fetch_aim_problem_lists(*, refresh: bool) -> Path:
    AIM_RAW.mkdir(parents=True, exist_ok=True)
    path = AIM_RAW / "problemlists.html"
    if refresh or not path.exists():
        path.write_text(fetch_text(AIM_PROBLEM_LISTS_URL), encoding="utf-8")
    return path


def import_aim_problem_lists(*, refresh: bool) -> list[dict[str, Any]]:
    path = fetch_aim_problem_lists(refresh=refresh)
    text = path.read_text(encoding="utf-8", errors="ignore")
    records: list[dict[str, Any]] = []
    current_topic = "Other"
    pattern = re.compile(
        r'<h3 class="topic">(.*?)</h3>|'
        r'<div class="aimproblist"><a class="problist" href="([^"]+)">(.*?)</a>&nbsp;<span class="format">(.*?)</span></div>',
        re.DOTALL,
    )
    for match in pattern.finditer(text):
        if match.group(1) is not None:
            current_topic = clean_html_text(match.group(1))
            continue
        href = html.unescape(match.group(2) or "").strip()
        title = clean_html_text(match.group(3) or "")
        fmt = clean_html_text(match.group(4) or "")
        if not href or not title:
            continue
        url = urljoin(AIM_PROBLEM_LISTS_URL, href)
        records.append(
            problem_record(
                problem_id=f"aim-problem-list-{slugify(title)}",
                title=title,
                source="American Institute of Mathematics Problem Lists",
                statement=(
                    f"AIM workshop problem-list collection in {current_topic}: {title}. "
                    "This record points to a list of research problems rather than one atomic theorem."
                ),
                domain=normalize_domain(current_topic),
                tags=["aim_problem_lists", "problem_list_collection", normalize_domain(current_topic), fmt.lower()],
                open_problem=True,
                formalized="no",
                notes="Imported from the AIM Problem Lists index. Use as a source-list entry before extracting individual problems.",
                references=[url, AIM_PROBLEM_LISTS_URL],
                hypotheses=["Extract individual problem statements from the linked AimPL/PDF source before proof search."],
                recommended_strategy=[
                    "Prioritize AimPL HTML sources over PDFs for structured extraction.",
                    "Create curated sub-banks for domains where AMRA has supporting libraries.",
                ],
                metadata={
                    "research_collection": "research_open_problem_collections",
                    "source_catalog": "aim_problem_lists",
                    "topic": current_topic,
                    "format": fmt,
                    "statement_quality": "problem_list_pointer",
                },
            )
        )
    ensure_unique_problem_ids(records)
    write_yaml(BANK_ROOT / "aim_problem_lists.yaml", records)
    return records


def update_collection_json(
    *,
    counts: ImportCounts,
    formal_revision: str,
    generated_at: str,
) -> None:
    payload = {
        "collection_id": "research_open_problem_collections",
        "generated_at": generated_at,
        "purpose": (
            "Provide high-priority research-level open problem collections for AMRA triage, "
            "proof discovery, and Lean/formalization research planning."
        ),
        "raw_root": str(RAW_ROOT.relative_to(REPO_ROOT)),
        "banks": {
            "formal_conjectures_open_research": "data/banks/formal_conjectures_open_research.yaml",
            "formal_conjectures_all": "data/banks/formal_conjectures_all.yaml",
            "unsolvedmath_index": "data/banks/unsolvedmath_index.yaml",
            "aim_problem_lists": "data/banks/aim_problem_lists.yaml",
        },
        "sources": [
            {
                "id": "formal_conjectures",
                "name": "Formal Conjectures",
                "source_url": FORMAL_CONJECTURES_WEB,
                "source_revision": formal_revision,
                "license": "Apache-2.0 for software; CC-BY-4.0 and source-specific licenses for materials",
                "local_path": str(FORMAL_CONJECTURES_RAW.relative_to(REPO_ROOT)),
                "formats": ["lean4"],
                "modalities": ["formal_statement", "lean4_theorem_target"],
                "difficulty": "research_open_to_solved_research_target",
                "counts": {
                    "declarations_total": counts.formal_conjectures_total,
                    "open_research_declarations": counts.formal_conjectures_open_research,
                },
                "recommended_use": "Primary AMRA research target collection because statements are already formal Lean 4 targets.",
            },
            {
                "id": "unsolvedmath",
                "name": "UnsolvedMath",
                "source_url": UNSOLVEDMATH_BASE,
                "license": "Source-specific; verify before redistribution of detail pages",
                "local_path": str(UNSOLVEDMATH_RAW.relative_to(REPO_ROOT)),
                "formats": ["html_index"],
                "modalities": ["natural_language_problem_index", "difficulty_metadata", "category_metadata"],
                "difficulty": "advanced_to_millennium",
                "counts": {"index_records": counts.unsolvedmath_total},
                "recommended_use": "Large triage index; fetch and validate detail pages before proof work.",
            },
            {
                "id": "aim_problem_lists",
                "name": "AIM Problem Lists",
                "source_url": AIM_PROBLEM_LISTS_URL,
                "license": "Source-specific; verify each linked AimPL/PDF source",
                "local_path": str(AIM_RAW.relative_to(REPO_ROOT)),
                "formats": ["html_index", "aimpl", "pdf"],
                "modalities": ["problem_list_index"],
                "difficulty": "research_problem_lists",
                "counts": {"problem_list_records": counts.aim_problem_lists_total},
                "recommended_use": "Curated source-list inventory for extracting domain-specific research sub-banks.",
            },
        ],
        "independence_policy": {
            "formal_conjectures": [
                "Use Lean statement files and local imports as the research target contract.",
                "Do not expose external proof scripts during first-pass proof search.",
            ],
            "natural_language_collections": [
                "Recover exact statement and source metadata before creating proof tasks.",
                "Record status/date validation for open problems before attack runs.",
            ],
        },
    }
    RESEARCH_OPEN_ROOT.mkdir(parents=True, exist_ok=True)
    (RESEARCH_OPEN_ROOT / "collection.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def update_readme(counts: ImportCounts, formal_revision: str, generated_at: str) -> None:
    readme = f"""# Research Open Problem Collections

Generated: {generated_at}

This research source collection connects AMRA to high-priority research-level
open problem sources. It keeps raw source snapshots under `raw/` and normalized
AMRA bank records under `data/banks/`.

## Imported Sources

| Source | Bank | Count | Main use |
| --- | --- | ---: | --- |
| Formal Conjectures | `formal_conjectures_open_research` | {counts.formal_conjectures_open_research} | Lean 4 formal research conjecture proof targets |
| Formal Conjectures | `formal_conjectures_all` | {counts.formal_conjectures_total} | Full formal statement corpus, including solved/textbook/test categories |
| UnsolvedMath | `unsolvedmath_index` | {counts.unsolvedmath_total} | Large natural-language open problem triage index |
| AIM Problem Lists | `aim_problem_lists` | {counts.aim_problem_lists_total} | Curated research problem-list source inventory |

Formal Conjectures revision: `{formal_revision}`

## Usage Notes

- Formal Conjectures records are the best immediate research targets because the
  theorem statements are already Lean 4 declarations.
- UnsolvedMath records are imported from browse-index pages and may contain
  shortened statements. Fetch the detail page and validate status before proof
  search.
- AIM records point to problem-list collections, not single theorem statements.
  Extract individual problems into curated sub-banks before running agents.

## Refresh

```bash
python3 scripts/import_research_open_sources.py --refresh
```
"""
    RESEARCH_OPEN_ROOT.mkdir(parents=True, exist_ok=True)
    (RESEARCH_OPEN_ROOT / "README.md").write_text(readme, encoding="utf-8")


def update_registry(counts: ImportCounts, synced_at: str) -> None:
    entries = read_yaml(REGISTRY_PATH)
    replace_names = {
        "formal_conjectures_open_research",
        "formal_conjectures_all",
        "unsolvedmath_index",
        "aim_problem_lists",
    }
    entries = [entry for entry in entries if str(entry.get("name", "")) not in replace_names]
    def entry(name: str, path: Path, description: str, category: str, count: int, provenance: str, tags: list[str]) -> dict[str, Any]:
        return {
            "name": name,
            "path": str(path),
            "description": description,
            "category": category,
            "problem_count": count,
            "provenance": provenance,
            "focus_tags": tags,
            "synced_at": synced_at,
        }

    entries.extend(
        [
            entry(
                "formal_conjectures_open_research",
                BANK_ROOT / "formal_conjectures_open_research.yaml",
                "Open research conjectures imported from Google DeepMind Formal Conjectures as Lean 4 theorem targets.",
                "research_open_formal",
                counts.formal_conjectures_open_research,
                FORMAL_CONJECTURES_WEB,
                ["formal_conjectures", "lean4", "research_open", "formal_statement"],
            ),
            entry(
                "formal_conjectures_all",
                BANK_ROOT / "formal_conjectures_all.yaml",
                "Full Formal Conjectures declaration bank, including open, solved, textbook, and test categories.",
                "research_open_formal",
                counts.formal_conjectures_total,
                FORMAL_CONJECTURES_WEB,
                ["formal_conjectures", "lean4", "formal_statement_corpus"],
            ),
            entry(
                "unsolvedmath_index",
                BANK_ROOT / "unsolvedmath_index.yaml",
                "UnsolvedMath browse-index import for large-scale natural-language open problem triage.",
                "research_open_index",
                counts.unsolvedmath_total,
                UNSOLVEDMATH_BASE,
                ["unsolvedmath", "open_problem_index", "research_problem"],
            ),
            entry(
                "aim_problem_lists",
                BANK_ROOT / "aim_problem_lists.yaml",
                "AIM workshop problem-list source inventory for domain-specific research problem extraction.",
                "research_open_index",
                counts.aim_problem_lists_total,
                AIM_PROBLEM_LISTS_URL,
                ["aim_problem_lists", "problem_list_collection", "research_problem"],
            ),
        ]
    )
    write_yaml(REGISTRY_PATH, entries)


def existing_collection_timestamp() -> str:
    collection_path = RESEARCH_OPEN_ROOT / "collection.json"
    if not collection_path.exists():
        collection_path = RESEARCH_OPEN_ROOT / "suite.json"
    if not collection_path.exists():
        return ""
    try:
        payload = json.loads(collection_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    return str(payload.get("generated_at", ""))


def main() -> None:
    parser = argparse.ArgumentParser(description="Import high-priority research open problem collections into AMRA banks.")
    parser.add_argument("--refresh", action="store_true", help="Refetch raw sources before parsing.")
    parser.add_argument("--delay", type=float, default=0.25, help="Delay between UnsolvedMath index page requests.")
    args = parser.parse_args()
    generated_at = utc_now_iso() if args.refresh else (existing_collection_timestamp() or utc_now_iso())

    formal_records, formal_revision = import_formal_conjectures(refresh=args.refresh)
    unsolved_records = import_unsolvedmath(refresh=args.refresh, delay=max(args.delay, 0.0))
    aim_records = import_aim_problem_lists(refresh=args.refresh)
    counts = ImportCounts(
        formal_conjectures_total=len(formal_records),
        formal_conjectures_open_research=sum(1 for record in formal_records if record["open_problem"]),
        unsolvedmath_total=len(unsolved_records),
        aim_problem_lists_total=len(aim_records),
    )
    update_collection_json(counts=counts, formal_revision=formal_revision, generated_at=generated_at)
    update_readme(counts, formal_revision, generated_at)
    update_registry(counts, synced_at=generated_at)
    print(json.dumps(counts.__dict__, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
