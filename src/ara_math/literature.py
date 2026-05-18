from __future__ import annotations

import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.parse import urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

from ara_math.context import has_exact_statement, read_exact_statement, set_exact_statement
from ara_math.models import ProblemRecord
from ara_math.workspace import (
    load_project_manifest,
    read_json,
    slugify,
    utc_now_iso,
    write_json,
    write_text,
)


class _HTMLTextExtractor(HTMLParser):
    def __init__(self, *, base_url: str = "") -> None:
        super().__init__()
        self.base_url = base_url
        self.title = ""
        self._in_title = False
        self._skip_depth = 0
        self._parts: list[str] = []
        self.links: list[dict[str, str]] = []
        self._current_link_href = ""
        self._current_link_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag_lower = tag.lower()
        attrs_map = {key.lower(): value or "" for key, value in attrs}
        if tag_lower == "title":
            self._in_title = True
        if tag_lower in {"script", "style", "noscript"}:
            self._skip_depth += 1
        if tag_lower == "a":
            href = attrs_map.get("href", "").strip()
            if href:
                self._current_link_href = urljoin(self.base_url, href)
                self._current_link_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag_lower = tag.lower()
        if tag_lower == "title":
            self._in_title = False
        if tag_lower in {"script", "style", "noscript"} and self._skip_depth > 0:
            self._skip_depth -= 1
        if tag_lower == "a" and self._current_link_href:
            link_text = " ".join(part for part in self._current_link_parts if part).strip()
            self.links.append({"href": self._current_link_href, "text": link_text})
            self._current_link_href = ""
            self._current_link_parts = []

    def handle_data(self, data: str) -> None:
        if self._skip_depth > 0:
            return
        cleaned = data.strip()
        if not cleaned:
            return
        if self._in_title and not self.title:
            self.title = cleaned
        self._parts.append(cleaned)
        if self._current_link_href:
            self._current_link_parts.append(cleaned)

    def text(self) -> str:
        return "\n".join(self._parts)


class LiteratureHarvester:
    def __init__(self, *, formal_math_root: Path | None = None) -> None:
        self.formal_math_root = formal_math_root

    STATEMENT_PATTERNS: list[tuple[re.Pattern[str], int, str]] = [
        (re.compile(r"^\*\*Problem Statement\*\*:\s*(.+)$", re.IGNORECASE), 6, ""),
        (re.compile(r"^Problem Statement:\s*(.+)$", re.IGNORECASE), 6, ""),
        (re.compile(r"^\*\*问题陈述\*\*[:：]\s*(.+)$", re.IGNORECASE), 6, ""),
        (re.compile(r"^问题陈述[:：]\s*(.+)$", re.IGNORECASE), 6, ""),
        (re.compile(r"^\*\*原始问题\*\*[:：]\s*(.+)$", re.IGNORECASE), 6, ""),
        (re.compile(r"^原始问题[:：]\s*(.+)$", re.IGNORECASE), 6, ""),
        (re.compile(r"^\*\*Conjecture\*\*:\s*(.+)$", re.IGNORECASE), 5, "open_gap"),
        (re.compile(r"^Conjecture:\s*(.+)$", re.IGNORECASE), 5, "open_gap"),
        (re.compile(r"^\*\*The Question\*\*:\s*(.+)$", re.IGNORECASE), 5, "open_gap"),
        (re.compile(r"^The Question:\s*(.+)$", re.IGNORECASE), 5, "open_gap"),
        (re.compile(r"^\*\*核心问题\*\*[:：]\s*(.+)$", re.IGNORECASE), 5, ""),
        (re.compile(r"^核心问题[:：]\s*(.+)$", re.IGNORECASE), 5, ""),
        (re.compile(r"^\*\*核心\*\*[:：]\s*(.+)$", re.IGNORECASE), 5, ""),
        (re.compile(r"^核心[:：]\s*(.+)$", re.IGNORECASE), 5, ""),
        (re.compile(r"^\d+\.\s+\*\*[^*]+\*\*:\s*(.+)$", re.IGNORECASE), 4, ""),
        (re.compile(r"^-\s+\*\*[^*]+\*\*:\s*(.+)$", re.IGNORECASE), 4, ""),
        (re.compile(r"^(Determine whether .+)$", re.IGNORECASE), 4, "open_gap"),
        (re.compile(r"^(Find .+)$", re.IGNORECASE), 4, "open_gap"),
        (re.compile(r"^(For which values of .+)$", re.IGNORECASE), 4, "open_gap"),
        (re.compile(r"^(Does every .+)$", re.IGNORECASE), 4, "open_gap"),
        (re.compile(r"^(Does there exist .+)$", re.IGNORECASE), 4, "open_gap"),
        (re.compile(r"^(Prove that .+)$", re.IGNORECASE), 4, ""),
        (re.compile(r"^(This is essentially asking for .+)$", re.IGNORECASE), 2, "open_gap"),
        (re.compile(r"^(For all sufficiently large .+)$", re.IGNORECASE), 3, "open_gap"),
    ]
    OPEN_GAP_CUES = (
        "determine whether",
        "for which values",
        "does every",
        "does there exist",
        "question",
        "conjecture",
        "open problem",
        "unknown",
        "remains open",
        "unresolved",
    )
    KNOWN_RESULT_CUES = (
        "there are finitely many",
        "the only",
        "are exactly",
        "no odd",
        "nonexistence",
        "classification",
        "characterization",
        "upper bound",
        "lower bound",
        "is bounded",
        "exists",
    )
    PROOF_INGREDIENT_CUES = (
        "bound",
        "compactness",
        "multiplicative",
        "prime-power",
        "subset-sum",
        "certificate",
        "search",
        "parity",
        "congruence",
        "factorization",
        "criterion",
        "decomposition",
        "graph",
        "encoding",
        "lemma",
        "case split",
        "divisor",
    )
    MODERN_TOOL_CUES = (
        "lean",
        "formalization",
        "mathlib",
        "machine-verified",
        "sat",
        "bounded search",
        "finite search",
        "certificate",
        "constraint",
        "encoding",
        "computation",
        "graph-theoretic",
    )
    ERDOS_REFERENCE_PATTERN = re.compile(r"(?:问题\s*#|Erd[őo]s\s*#)(\d{1,4})", re.IGNORECASE)
    ERDOS_SOURCE_PATTERN = re.compile(r"(?:erdos[-_/ ]|问题\s*#|Erd[őo]s\s*#)(\d{1,4})", re.IGNORECASE)
    SHELLISH_TOKENS = (
        "python",
        "python3",
        "nohup",
        "tail -f",
        "cat ",
        "rg ",
        "grep ",
        "lake build",
        "search.log",
        "src/",
        "docs/",
        "results/",
        "read ",
        "阅读 ",
    )
    PAPER_SEARCH_STOPWORDS = {
        "a",
        "an",
        "and",
        "are",
        "be",
        "before",
        "begins",
        "by",
        "can",
        "detailed",
        "does",
        "every",
        "find",
        "for",
        "from",
        "full",
        "imported",
        "into",
        "is",
        "least",
        "mathematical",
        "of",
        "one",
        "problem",
        "proof",
        "question",
        "source",
        "statement",
        "such",
        "that",
        "the",
        "their",
        "there",
        "these",
        "this",
        "values",
        "whether",
        "with",
        "which",
    }
    FAMILY_QUERY_HINTS: dict[str, tuple[str, ...]] = {
        "triangle_dissection": (
            "triangle tiling nonexistence theorem",
            "equilateral triangle dissection congruent triangles",
            "seven tiling eleven tiling triangle",
            "Tutte equilateral triangle dissection",
            "Beeson triangle tiling nonexistence",
        ),
        "unitary_perfect": (
            "unitary perfect number",
            "odd unitary perfect numbers",
            "unitary harmonic numbers",
            "Subbarao Warren unitary perfect",
            "Wall fifth unitary perfect number",
            "Goto unitary perfect numbers",
        ),
        "prime_gap_spectrum": (
            "normalized prime gaps limit points",
            "distribution of gaps between consecutive primes",
            "prime gap spectrum interval theorem",
        ),
        "prime_plus_two_powers": (
            "prime plus two powers of two",
            "integers not of the form p plus 2^a plus 2^b",
            "Crocker Pan two powers of two",
        ),
        "minimum_overlap": (
            "minimum overlap problem",
            "partition overlap lower bound",
            "White Haugland minimum overlap",
        ),
        "weird_numbers": (
            "weird numbers abundance index",
            "primitive weird numbers",
            "weird number conjecture",
        ),
    }
    FAMILY_POSITIVE_MARKERS: dict[str, tuple[str, ...]] = {
        "triangle_dissection": (
            "triangle tiling",
            "equilateral triangle",
            "dissection",
            "tiling",
            "congruent triangles",
            "7-tiling",
            "11-tiling",
            "tutte",
            "beeson",
        ),
        "unitary_perfect": (
            "unitary perfect",
            "perfect numbers",
            "unitary harmonic",
            "divisor",
            "divisors",
            "subbarao",
            "warren",
            "wall",
            "goto",
            "bi-unitary",
        ),
        "prime_gap_spectrum": (
            "prime gap",
            "prime gaps",
            "normalized prime gaps",
            "consecutive primes",
            "limit points",
            "pintz",
            "maynard",
        ),
        "prime_plus_two_powers": (
            "2^a",
            "2^b",
            "powers of two",
            "prime",
            "odd integers",
            "crocker",
            "pan",
        ),
        "minimum_overlap": (
            "minimum overlap",
            "overlap problem",
            "balanced partition",
            "difference multiplicity",
            "white",
            "haugland",
        ),
        "weird_numbers": (
            "weird number",
            "weird numbers",
            "abundance index",
            "abundant",
            "semiperfect",
        ),
    }
    FAMILY_NEGATIVE_MARKERS: dict[str, tuple[str, ...]] = {
        "triangle_dissection": (
            "unitary perfect",
            "unitary cayley",
            "entanglement",
            "qudit",
            "amicable numbers theory",
        ),
        "unitary_perfect": (
            "unitary cayley",
            "cayley graph",
            "cayley graphs",
            "entanglement",
            "qudit",
            "locc",
            "unitary operations",
            "discrimination between unitary operations",
            "equilateral triangle",
            "triangle tiling",
            "amicable numbers theory",
            "amicable pair",
        ),
        "prime_gap_spectrum": (
            "unitary perfect",
            "triangle tiling",
            "weird number",
        ),
        "prime_plus_two_powers": (
            "unitary perfect",
            "triangle tiling",
            "weird number",
        ),
        "minimum_overlap": (
            "triangle tiling",
            "unitary perfect",
            "powers of two",
        ),
        "weird_numbers": (
            "triangle tiling",
            "unitary perfect",
            "prime gaps",
        ),
    }
    ACADEMIC_HOST_HINTS = (
        "arxiv.org",
        "doi.org",
        "cambridge.org",
        "eudml.org",
        "euclid.org",
        "projecteuclid.org",
        "impan.pl",
        "ams.org",
        "hal.science",
        "zenodo.org",
        "researchgate.net",
        "springer.com",
        "link.springer.com",
        "mdpi.com",
        "frontiersin.org",
        "academic.oup.com",
        "sciencedirect.com",
        "jstor.org",
        "degruyter.com",
    )
    PDF_LINK_TOKENS = (".pdf", "/pdf", "download", "fulltext", "viewcontent.cgi")
    PLACEHOLDER_STATEMENT_TOKENS = (
        "detailed statement should be imported",
        "placeholder",
        "authoritative source before claiming proof progress",
    )
    CITATION_TOKEN_PATTERN = re.compile(r"\b(?:[A-Z]{2,5}|[A-Z][a-z]{0,3})\d{2}[a-z]?\b")
    THEOREM_HEADING_PATTERN = re.compile(
        r"^\s*(Theorem|Lemma|Corollary|Proposition|Claim|Remark)\s*([0-9A-Za-z.\-()]*)\.?\s*(.*)$",
        re.IGNORECASE,
    )

    def _erdos_problem_number(self, problem: ProblemRecord) -> str:
        return str(problem.problem_id).replace("erdos-", "").strip()

    def _default_formal_math_root(self) -> Path | None:
        if self.formal_math_root and self.formal_math_root.exists():
            return self.formal_math_root
        candidate = Path(__file__).resolve().parents[3] / "formal-math"
        if candidate.exists():
            return candidate
        return None

    def _is_erdos_problem(self, problem: ProblemRecord) -> bool:
        metadata = problem.metadata or {}
        source_catalog = str(metadata.get("source_catalog", "")).strip().lower()
        return problem.source == "Erdős Problems" or source_catalog == "erdosproblems"

    @staticmethod
    @lru_cache(maxsize=8)
    def _scan_erdos_doc_sources(formal_math_root_str: str) -> dict[str, list[str]]:
        root = Path(formal_math_root_str)
        if not root.exists():
            return {}

        candidate_paths: list[Path] = []
        for fixed_path in (root / "README.md", root / "docs"):
            if fixed_path.is_file():
                candidate_paths.append(fixed_path)
            elif fixed_path.is_dir():
                candidate_paths.extend(sorted(fixed_path.rglob("*.md")))
        for project_dir in sorted(root.glob("erdos-*")):
            if not project_dir.is_dir():
                continue
            candidate_paths.extend(sorted(project_dir.rglob("*.md")))

        ranking: dict[str, list[tuple[int, str]]] = {}
        for path in candidate_paths:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            numbers = {match.group(1) for match in LiteratureHarvester.ERDOS_REFERENCE_PATTERN.finditer(text)}
            if not numbers:
                continue
            path_score = 0
            lower_path = str(path).lower()
            if "simple_problems_analysis" in lower_path:
                path_score += 5
            if "problem_" in lower_path:
                path_score += 4
            if path.name.lower() == "readme.md":
                path_score += 2
            if "open_problems_summary" in lower_path:
                path_score += 1
            for number in numbers:
                score = path_score
                if number in lower_path:
                    score += 4
                if f"erdos-{number}" in lower_path:
                    score += 6
                ranking.setdefault(number, []).append((score, str(path)))

        results: dict[str, list[str]] = {}
        for number, items in ranking.items():
            deduped: list[str] = []
            seen: set[str] = set()
            for _, path_str in sorted(items, key=lambda item: (-item[0], len(item[1]), item[1])):
                if path_str in seen:
                    continue
                seen.add(path_str)
                deduped.append(path_str)
            results[number] = deduped
        return results

    def _infer_erdos_doc_sources(self, problem: ProblemRecord) -> list[str]:
        if not self._is_erdos_problem(problem):
            return []
        formal_math_root = self._default_formal_math_root()
        if formal_math_root is None:
            return []
        number = str(problem.problem_id).replace("erdos-", "")
        return self._scan_erdos_doc_sources(str(formal_math_root)).get(number, [])[:6]

    def _canonical_source(self, source: str) -> str:
        path = Path(source)
        if not path.exists():
            return source
        if path.is_dir():
            for candidate_name in ("README.md", "LITERATURE.md", "STRATEGY.md"):
                candidate = path / candidate_name
                if candidate.exists():
                    return str(candidate)
            markdown_files = sorted(path.glob("*.md"))
            if markdown_files:
                return str(markdown_files[0])
        return str(path)

    def _is_placeholder_statement(self, statement: str) -> bool:
        lowered = statement.strip().lower()
        if not lowered:
            return True
        return any(token in lowered for token in self.PLACEHOLDER_STATEMENT_TOKENS)

    def _looks_like_definition_statement(self, statement: str) -> bool:
        lowered = statement.strip().lower()
        if not lowered:
            return False
        if any(token in lowered for token in (" iff ", " if and only if ", " when and only when ", " is defined as ")):
            return True
        if "当且仅当" in statement or "定义为" in statement or "称为" in statement:
            return True
        if "unitary divisor" in lowered and "gcd" in lowered:
            return True
        return False

    def _candidate_target_bonus(self, *, problem: ProblemRecord, family: str, statement: str) -> int:
        lowered = statement.lower().strip()
        bonus = 0
        if self._looks_like_definition_statement(statement):
            bonus -= 8 if problem.open_problem else 4
        if problem.open_problem and any(
            cue in lowered
            for cue in (
                "determine whether",
                "for which values",
                "does every",
                "does there exist",
                "finitely many",
                "only finitely many",
                "find all",
                "找出所有",
                "是否只有有限",
            )
        ):
            bonus += 3
        if family == "unitary_perfect":
            if "finitely many unitary perfect" in lowered or "only finitely many unitary perfect" in lowered:
                bonus += 8
            elif "unitary perfect" in lowered and "finitely many" in lowered:
                bonus += 6
            if "no odd unitary perfect" in lowered:
                bonus += 3
            if "unitary divisor" in lowered and "gcd" in lowered:
                bonus -= 10
        if family == "triangle_dissection":
            if "for which values of n" in lowered or ("triangle" in lowered and "congruent" in lowered):
                bonus += 6
            if "找出所有" in statement and "三角形" in statement:
                bonus += 6
        return bonus

    def _clean_query_text(self, text: str) -> str:
        normalized = re.sub(r"[_*`#|]+", " ", text)
        normalized = re.sub(r"https?://\S+", " ", normalized)
        normalized = re.sub(r"[^A-Za-z0-9+\- ]+", " ", normalized)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    def _query_tokens(self, text: str) -> list[str]:
        tokens: list[str] = []
        for token in re.findall(r"[A-Za-z0-9+\-]+", text.lower()):
            if len(token) <= 2:
                continue
            if token in self.PAPER_SEARCH_STOPWORDS:
                continue
            if token.isdigit():
                continue
            tokens.append(token)
        deduped: list[str] = []
        seen: set[str] = set()
        for token in tokens:
            if token in seen:
                continue
            seen.add(token)
            deduped.append(token)
        return deduped

    def _problem_query_seeds(
        self,
        problem: ProblemRecord,
        *,
        recovered_statement: str,
        evidence: dict[str, Any],
    ) -> list[str]:
        family = self._infer_problem_family(problem, recovered_statement=recovered_statement, evidence=evidence)
        seeds: list[str] = []
        title = re.sub(r"^Erd[őo]s Problem #?\d+\s*", "", problem.title, flags=re.IGNORECASE).strip()
        if title:
            seeds.append(title)
        if recovered_statement and not self._is_placeholder_statement(recovered_statement):
            seeds.append(recovered_statement)
        if problem.statement and not self._is_placeholder_statement(problem.statement):
            seeds.append(problem.statement)
        core_text = " ".join(seeds)
        core_tokens = set(self._query_tokens(core_text))
        if len(core_tokens) < 2:
            for bucket in ("open_gaps", "known_results", "proof_ingredients"):
                for item in evidence.get(bucket, [])[:4]:
                    statement = str(item.get("statement", "")).strip()
                    tokens = self._query_tokens(statement)
                    if len(tokens) < 3:
                        continue
                    seeds.append(statement)
                    core_tokens.update(tokens)
                    if len(core_tokens) >= 4:
                        break
                if len(core_tokens) >= 4:
                    break
        if problem.tags:
            tag_seed = " ".join(str(tag) for tag in problem.tags[:5])
            if len(self._query_tokens(tag_seed)) >= 2:
                seeds.append(tag_seed)
        seeds.extend(self.FAMILY_QUERY_HINTS.get(family, ()))
        for bucket in ("known_results", "proof_ingredients", "modern_tools"):
            for item in evidence.get(bucket, [])[:2]:
                statement = str(item.get("statement", "")).strip()
                if statement:
                    statement_tokens = set(self._query_tokens(statement))
                    if core_tokens and not (statement_tokens & core_tokens):
                        continue
                    seeds.append(statement)

        queries: list[str] = []
        seen: set[str] = set()
        for seed in seeds:
            cleaned = self._clean_query_text(seed)
            if not cleaned:
                continue
            tokens = self._query_tokens(cleaned)
            if len(tokens) < 2:
                continue
            query = " ".join(tokens[:8]).strip()
            if len(query) < 8 or query in seen:
                continue
            seen.add(query)
            queries.append(query)
            if len(queries) >= 6:
                break
        return queries

    def _infer_problem_family(
        self,
        problem: ProblemRecord,
        *,
        recovered_statement: str,
        evidence: dict[str, Any],
    ) -> str:
        text = " ".join(
            [
                problem.problem_id,
                problem.title,
                problem.statement,
                recovered_statement,
                " ".join(problem.tags),
                " ".join(str(item.get("statement", "")) for bucket in ("known_results", "proof_ingredients") for item in evidence.get(bucket, [])[:4]),
                str(problem.metadata or {}),
            ]
        ).lower()
        if "triangle" in text or "equilateral" in text or "dissection" in text or "tiling" in text:
            return "triangle_dissection"
        if "unitary" in text and "perfect" in text:
            return "unitary_perfect"
        if "weird" in text:
            return "weird_numbers"
        if "2^a" in text or "2^b" in text or "2^k + 2^l" in text or "powers of two" in text:
            return "prime_plus_two_powers"
        if "minimum overlap" in text or ("overlap" in text and "partition" in text):
            return "minimum_overlap"
        if "prime" in text and "gap" in text:
            return "prime_gap_spectrum"
        return "generic"

    def _paper_inventory_path(self, project_dir: Path) -> Path:
        return project_dir / "idea" / "paper_inventory.json"

    def _paper_theorem_inventory_path(self, project_dir: Path) -> Path:
        return project_dir / "idea" / "paper_theorem_inventory.json"

    def _normalize_doi(self, value: str) -> str:
        lowered = value.strip()
        if lowered.startswith("https://doi.org/"):
            return lowered.removeprefix("https://doi.org/")
        if lowered.startswith("http://doi.org/"):
            return lowered.removeprefix("http://doi.org/")
        return lowered

    def _paper_key(self, candidate: dict[str, Any]) -> str:
        doi = self._normalize_doi(str(candidate.get("doi", "")).strip())
        if doi:
            return f"doi:{doi.lower()}"
        title = re.sub(r"[^a-z0-9]+", "-", str(candidate.get("title", "")).lower()).strip("-")
        if title:
            return f"title:{title}"
        url = str(candidate.get("source_url", "")).strip() or str(candidate.get("pdf_url", "")).strip()
        return f"url:{url}"

    def _looks_like_academic_url(self, url: str) -> bool:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        if any(hint in host for hint in self.ACADEMIC_HOST_HINTS):
            return True
        lowered = url.lower()
        return any(token in lowered for token in self.PDF_LINK_TOKENS)

    def _download_binary(self, url: str) -> tuple[bytes, str]:
        request = Request(url, headers={"User-Agent": "amra/0.2"})
        with urlopen(request, timeout=20) as response:
            return response.read(), response.headers.get("Content-Type", "")

    def _fetch_remote_payload(self, url: str) -> dict[str, Any]:
        request = Request(url, headers={"User-Agent": "amra/0.2"})
        with urlopen(request, timeout=15) as response:
            raw = response.read()
            content_type = response.headers.get("Content-Type", "")
        if "pdf" in content_type.lower() or url.lower().endswith(".pdf"):
            return {
                "title": Path(urlparse(url).path).name or url,
                "text": "",
                "content_kind": "pdf",
                "links": [],
                "raw_bytes": raw,
            }
        text = raw.decode("utf-8", errors="ignore")
        if "html" in content_type.lower() or "<html" in text.lower():
            parser = _HTMLTextExtractor(base_url=url)
            parser.feed(text)
            return {
                "title": parser.title or url,
                "text": parser.text(),
                "content_kind": "html",
                "links": parser.links,
                "raw_bytes": raw,
            }
        return {
            "title": url,
            "text": text,
            "content_kind": "text",
            "links": [],
            "raw_bytes": raw,
        }

    def _search_openalex(self, query: str, *, max_results: int = 5) -> list[dict[str, Any]]:
        url = "https://api.openalex.org/works?" + urlencode({"search": query, "per-page": max_results})
        request = Request(url, headers={"User-Agent": "amra/0.2"})
        try:
            with urlopen(request, timeout=20) as response:
                payload = response.read().decode("utf-8", errors="ignore")
        except (URLError, TimeoutError, OSError):
            return []
        data = json.loads(payload)
        results: list[dict[str, Any]] = []
        for item in data.get("results", [])[:max_results]:
            title = str(item.get("display_name") or item.get("title") or "").strip()
            if not title:
                continue
            primary_location = item.get("primary_location") or {}
            best_oa = item.get("best_oa_location") or {}
            open_access = item.get("open_access") or {}
            pdf_url = (
                str(best_oa.get("pdf_url") or "").strip()
                or str(primary_location.get("pdf_url") or "").strip()
                or (
                    str(open_access.get("oa_url") or "").strip()
                    if str(open_access.get("oa_url") or "").strip().lower().endswith(".pdf")
                    else ""
                )
            )
            landing_page_url = (
                str(best_oa.get("landing_page_url") or "").strip()
                or str(primary_location.get("landing_page_url") or "").strip()
                or str(open_access.get("oa_url") or "").strip()
            )
            venue = str(((primary_location.get("source") or {}).get("display_name")) or "").strip()
            authors = [
                str((authorship.get("author") or {}).get("display_name") or "").strip()
                for authorship in item.get("authorships", [])[:6]
                if str((authorship.get("author") or {}).get("display_name") or "").strip()
            ]
            results.append(
                {
                    "provider": "openalex",
                    "query": query,
                    "title": title,
                    "authors": authors,
                    "year": item.get("publication_year"),
                    "venue": venue,
                    "doi": self._normalize_doi(str(item.get("doi") or "").strip()),
                    "source_url": landing_page_url or str(item.get("id") or "").strip(),
                    "landing_page_url": landing_page_url,
                    "pdf_url": pdf_url,
                    "metadata_only": not bool(pdf_url or landing_page_url),
                }
            )
        return results

    def _search_arxiv(self, query: str, *, max_results: int = 4) -> list[dict[str, Any]]:
        tokens = self._query_tokens(query)[:5]
        if len(tokens) < 2:
            return []
        search_query = " AND ".join(f"all:{token}" for token in tokens)
        url = "https://export.arxiv.org/api/query?" + urlencode(
            {"search_query": search_query, "start": 0, "max_results": max_results}
        )
        request = Request(url, headers={"User-Agent": "amra/0.2"})
        try:
            with urlopen(request, timeout=20) as response:
                payload = response.read().decode("utf-8", errors="ignore")
        except (URLError, TimeoutError, OSError):
            return []
        root = ET.fromstring(payload)
        namespace = {"atom": "http://www.w3.org/2005/Atom"}
        results: list[dict[str, Any]] = []
        for entry in root.findall("atom:entry", namespace):
            title = " ".join((entry.findtext("atom:title", default="", namespaces=namespace) or "").split())
            if not title:
                continue
            authors = [
                " ".join((author.findtext("atom:name", default="", namespaces=namespace) or "").split())
                for author in entry.findall("atom:author", namespace)
            ]
            abs_url = " ".join((entry.findtext("atom:id", default="", namespaces=namespace) or "").split())
            pdf_url = ""
            for link in entry.findall("atom:link", namespace):
                if link.attrib.get("type") == "application/pdf":
                    pdf_url = str(link.attrib.get("href", "")).strip()
                    break
            summary = " ".join((entry.findtext("atom:summary", default="", namespaces=namespace) or "").split())
            published = str(entry.findtext("atom:published", default="", namespaces=namespace) or "").strip()
            year = int(published[:4]) if len(published) >= 4 and published[:4].isdigit() else None
            results.append(
                {
                    "provider": "arxiv",
                    "query": query,
                    "title": title,
                    "authors": [author for author in authors if author],
                    "year": year,
                    "venue": "arXiv",
                    "doi": "",
                    "source_url": abs_url,
                    "landing_page_url": abs_url,
                    "pdf_url": pdf_url,
                    "summary": summary,
                    "metadata_only": not bool(pdf_url),
                }
            )
        return results

    def _source_entries(self, project_dir: Path, problem: ProblemRecord) -> list[dict[str, str]]:
        references_payload = read_json(project_dir / "idea" / "references.json", default={"references": []})
        references = [str(item).strip() for item in references_payload.get("references", []) if str(item).strip()]
        source_entries: list[dict[str, str]] = [{"source": item, "kind": "reference"} for item in references]
        papers_dir = project_dir / "idea" / "papers"
        if papers_dir.exists():
            for candidate in sorted(papers_dir.iterdir()):
                if not candidate.is_file():
                    continue
                if candidate.suffix.lower() not in {".pdf", ".md", ".txt", ".tex"}:
                    continue
                source_entries.append({"source": str(candidate), "kind": "project_paper"})

        proof_path = read_json(project_dir / "idea" / "proof_path_assessment.json", default={})
        for asset in proof_path.get("local_assets", []):
            path = str(asset.get("path", "")).strip()
            if path:
                source_entries.append({"source": path, "kind": str(asset.get("kind", "local_asset"))})

        metadata = problem.metadata or {}
        for key in ("local_readme_path", "local_project_dir"):
            value = str(metadata.get(key, "")).strip()
            if value:
                source_entries.append({"source": value, "kind": key})
        for source in self._infer_erdos_doc_sources(problem):
            source_entries.append({"source": source, "kind": "erdos_doc"})

        deduped: list[dict[str, str]] = []
        seen: set[str] = set()
        for entry in source_entries:
            source = self._canonical_source(entry["source"])
            if source in seen:
                continue
            seen.add(source)
            deduped.append({"source": source, "kind": entry["kind"]})
        return deduped

    def _discover_linked_candidates(self, snapshots: list[dict[str, Any]]) -> list[dict[str, Any]]:
        candidates: list[dict[str, Any]] = []
        for snapshot in snapshots:
            source = str(snapshot.get("source", "")).strip()
            for link in snapshot.get("links", []):
                href = str(link.get("href", "")).strip()
                if not href or not self._looks_like_academic_url(href):
                    continue
                link_text = str(link.get("text", "")).strip()
                parsed = urlparse(href)
                pdf_url = href if href.lower().endswith(".pdf") or any(token in href.lower() for token in self.PDF_LINK_TOKENS) else ""
                if "arxiv.org/abs/" in href and not pdf_url:
                    pdf_url = href.replace("/abs/", "/pdf/")
                title = link_text or Path(parsed.path).name or href
                candidates.append(
                    {
                        "provider": "linked_reference",
                        "query": f"linked from {source}",
                        "title": title,
                        "authors": [],
                        "year": None,
                        "venue": parsed.netloc,
                        "doi": self._normalize_doi(href) if "doi.org/" in href else "",
                        "source_url": href,
                        "landing_page_url": href,
                        "pdf_url": pdf_url,
                        "metadata_only": False,
                    }
                )
        return candidates

    def _discover_citation_tokens(self, snapshots: list[dict[str, Any]]) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        seen: set[str] = set()
        for snapshot in snapshots:
            text = "\n".join(
                [
                    str(snapshot.get("title", "")).strip(),
                    str(snapshot.get("excerpt", "")).strip(),
                ]
            )
            for token in self.CITATION_TOKEN_PATTERN.findall(text):
                if token in seen:
                    continue
                seen.add(token)
                items.append(
                    {
                        "provider": "citation_token",
                        "query": f"citation token from {snapshot.get('source', '')}",
                        "title": token,
                        "authors": [],
                        "year": None,
                        "venue": "",
                        "doi": "",
                        "source_url": str(snapshot.get("source", "")).strip(),
                        "landing_page_url": "",
                        "pdf_url": "",
                        "metadata_only": True,
                        "status": "manual_followup_required",
                        "notes": f"Citation token discovered in source text: {token}",
                    }
                )
        return items

    def _candidate_overlap_score(self, candidate: dict[str, Any], *, keywords: list[str], family: str) -> int:
        haystack = " ".join(
            [
                str(candidate.get("title", "")),
                str(candidate.get("venue", "")),
                str(candidate.get("summary", "")),
                str(candidate.get("doi", "")),
                " ".join(str(author) for author in candidate.get("authors", [])),
            ]
        ).lower()
        score = sum(1 for keyword in keywords if keyword in haystack)
        positive_markers = self.FAMILY_POSITIVE_MARKERS.get(family, ())
        negative_markers = self.FAMILY_NEGATIVE_MARKERS.get(family, ())
        score += sum(2 for marker in positive_markers if marker in haystack)
        score -= sum(4 for marker in negative_markers if marker in haystack)
        if family == "unitary_perfect" and "unitary perfect" in haystack:
            score += 4
        if family == "triangle_dissection" and any(token in haystack for token in ("7-tiling", "11-tiling", "n-tilings", "congruent triangles")):
            score += 4
        return score

    def _search_related_candidates(
        self,
        problem: ProblemRecord,
        *,
        recovered_statement: str,
        evidence: dict[str, Any],
    ) -> list[dict[str, Any]]:
        queries = self._problem_query_seeds(problem, recovered_statement=recovered_statement, evidence=evidence)
        family = self._infer_problem_family(problem, recovered_statement=recovered_statement, evidence=evidence)
        keyword_tokens = self._query_tokens(" ".join(queries))[:8]
        ranked: list[tuple[int, dict[str, Any]]] = []
        for query in queries:
            for candidate in self._search_openalex(query, max_results=4):
                overlap = self._candidate_overlap_score(candidate, keywords=keyword_tokens, family=family)
                if overlap < 2 and candidate.get("provider") == "openalex":
                    continue
                ranked.append((overlap + 2, candidate))
            for candidate in self._search_arxiv(query, max_results=3):
                overlap = self._candidate_overlap_score(candidate, keywords=keyword_tokens, family=family)
                if overlap < 2:
                    continue
                ranked.append((overlap + 1, candidate))
        deduped: list[dict[str, Any]] = []
        seen: set[str] = set()
        for _, candidate in sorted(ranked, key=lambda item: (-item[0], len(str(item[1].get("title", ""))))):
            key = self._paper_key(candidate)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(candidate)
            if len(deduped) >= 8:
                break
        return deduped

    def _materialize_paper_candidate(
        self,
        *,
        candidate: dict[str, Any],
        project_dir: Path,
        cache_dir: Path,
    ) -> dict[str, Any]:
        papers_dir = project_dir / "idea" / "papers"
        papers_dir.mkdir(parents=True, exist_ok=True)
        title = str(candidate.get("title", "")).strip() or "paper"
        stem = slugify(title) or "paper"
        base_record = {
            "provider": str(candidate.get("provider", "")).strip(),
            "query": str(candidate.get("query", "")).strip(),
            "title": title,
            "authors": list(candidate.get("authors", [])),
            "year": candidate.get("year"),
            "venue": str(candidate.get("venue", "")).strip(),
            "doi": self._normalize_doi(str(candidate.get("doi", "")).strip()),
            "source_url": str(candidate.get("source_url", "")).strip(),
            "landing_page_url": str(candidate.get("landing_page_url", "")).strip(),
            "pdf_url": str(candidate.get("pdf_url", "")).strip(),
            "status": str(candidate.get("status", "")).strip() or "metadata_only",
            "local_path": "",
            "notes": str(candidate.get("notes", "")).strip(),
        }
        if base_record["provider"] == "citation_token":
            base_record["status"] = "manual_followup_required"
            return base_record
        pdf_url = base_record["pdf_url"]
        if pdf_url:
            target_path = papers_dir / f"{stem}.pdf"
            if target_path.exists() and target_path.stat().st_size > 0:
                base_record["status"] = "existing_local_copy"
                base_record["local_path"] = str(target_path)
                return base_record
            try:
                raw, content_type = self._download_binary(pdf_url)
            except (OSError, URLError, TimeoutError) as exc:
                base_record["status"] = "download_error"
                base_record["notes"] = (base_record["notes"] + f" download failed: {exc}").strip()
                return base_record
            if "pdf" in content_type.lower() or raw[:4] == b"%PDF":
                target_path.write_bytes(raw)
                base_record["status"] = "downloaded_pdf"
                base_record["local_path"] = str(target_path)
                return base_record

        if base_record["provider"] in {"openalex", "arxiv"}:
            return base_record

        landing_page_url = base_record["landing_page_url"] or base_record["source_url"]
        if landing_page_url and landing_page_url.startswith(("http://", "https://")):
            try:
                payload = self._fetch_remote_payload(landing_page_url)
            except (OSError, URLError, TimeoutError, ET.ParseError) as exc:
                base_record["status"] = "metadata_only"
                base_record["notes"] = (base_record["notes"] + f" landing page fetch failed: {exc}").strip()
                return base_record
            pdf_links = [
                str(link.get("href", "")).strip()
                for link in payload.get("links", [])
                if str(link.get("href", "")).strip() and self._looks_like_academic_url(str(link.get("href", "")).strip())
            ]
            for discovered_url in pdf_links:
                if not any(token in discovered_url.lower() for token in self.PDF_LINK_TOKENS) and not discovered_url.lower().endswith(".pdf"):
                    continue
                fallback_candidate = {**candidate, "pdf_url": discovered_url}
                return self._materialize_paper_candidate(candidate=fallback_candidate, project_dir=project_dir, cache_dir=cache_dir)
            text = str(payload.get("text", "")).strip()
            if text:
                cache_path = cache_dir / f"paper-{stem}.txt"
                write_text(cache_path, text + "\n")
                base_record["status"] = "saved_landing_snapshot"
                base_record["local_path"] = str(cache_path)
                return base_record
        return base_record

    def _acquire_related_papers(
        self,
        project_dir: Path,
        problem: ProblemRecord,
        *,
        recovered_statement: str,
        evidence: dict[str, Any],
        snapshots: list[dict[str, Any]],
        cache_dir: Path,
    ) -> dict[str, Any]:
        linked_candidates = self._discover_linked_candidates(snapshots)
        searched_candidates = self._search_related_candidates(
            problem,
            recovered_statement=recovered_statement,
            evidence=evidence,
        )
        citation_tokens = self._discover_citation_tokens(snapshots)

        all_candidates: list[dict[str, Any]] = []
        seen: set[str] = set()
        for candidate in linked_candidates + searched_candidates + citation_tokens:
            key = self._paper_key(candidate)
            if key in seen:
                continue
            seen.add(key)
            all_candidates.append(candidate)

        records = [
            self._materialize_paper_candidate(candidate=candidate, project_dir=project_dir, cache_dir=cache_dir)
            for candidate in all_candidates
        ]
        for record in records:
            theorem_snippets = self._theorem_snippets_from_record(record)
            record["theorem_snippets"] = theorem_snippets
            record["theorem_snippet_count"] = len(theorem_snippets)
        downloaded_count = sum(1 for record in records if record.get("status") in {"downloaded_pdf", "existing_local_copy"})
        return {
            "generated_at": utc_now_iso(),
            "problem_id": problem.problem_id,
            "query_count": len(self._problem_query_seeds(problem, recovered_statement=recovered_statement, evidence=evidence)),
            "candidate_count": len(all_candidates),
            "downloaded_pdf_count": downloaded_count,
            "manual_followup_count": sum(1 for record in records if str(record.get("status", "")).startswith("manual")),
            "theorem_snippet_count": sum(int(record.get("theorem_snippet_count", 0)) for record in records),
            "records": records,
        }

    def _extract_pdf_text(self, path: Path) -> str:
        pdftotext = shutil.which("pdftotext")
        if not pdftotext:
            return ""
        try:
            result = subprocess.run(
                [pdftotext, str(path), "-"],
                check=True,
                capture_output=True,
                text=True,
                timeout=20,
            )
        except (OSError, subprocess.SubprocessError, UnicodeDecodeError):
            return ""
        return result.stdout.strip()

    def _normalize_theorem_line(self, line: str) -> str:
        line = re.sub(r"\s+", " ", line).strip()
        if not line:
            return ""
        if len(line) <= 2 and line.isdigit():
            return ""
        if re.fullmatch(r"[ivxlcdm]+", line.lower()):
            return ""
        if line.lower().startswith(("arxiv:", "doi:", "references", "bibliography")):
            return ""
        return line

    def _extract_theorem_snippets(self, text: str, *, limit: int = 8) -> list[dict[str, Any]]:
        snippets: list[dict[str, Any]] = []
        lines = text.splitlines()
        seen: set[str] = set()
        for index, raw_line in enumerate(lines):
            line = self._normalize_theorem_line(raw_line)
            if not line:
                continue
            match = self.THEOREM_HEADING_PATTERN.match(line)
            if not match and "main theorem is that" not in line.lower():
                continue
            heading_kind = "theorem"
            label = ""
            statement_parts: list[str] = []
            if match:
                heading_kind = match.group(1).lower()
                label = match.group(2).strip()
                trailing = match.group(3).strip()
                if trailing:
                    statement_parts.append(trailing)
            else:
                statement_parts.append(line)
            for follow in lines[index + 1 : index + 6]:
                normalized = self._normalize_theorem_line(follow)
                if not normalized:
                    if statement_parts:
                        break
                    continue
                if self.THEOREM_HEADING_PATTERN.match(normalized):
                    break
                statement_parts.append(normalized)
                if len(" ".join(statement_parts)) >= 360:
                    break
            statement = re.sub(r"\s+", " ", " ".join(statement_parts)).strip()
            if not statement:
                continue
            if len(statement) < 24:
                continue
            key = f"{heading_kind}:{label}:{statement}".lower()
            if key in seen:
                continue
            seen.add(key)
            snippets.append(
                {
                    "kind": heading_kind,
                    "label": label,
                    "statement": statement,
                }
            )
            if len(snippets) >= limit:
                break
        return snippets

    def _theorem_snippets_from_record(self, record: dict[str, Any]) -> list[dict[str, Any]]:
        local_path = str(record.get("local_path", "")).strip()
        if not local_path:
            return []
        path = Path(local_path)
        if not path.exists():
            return []
        if path.suffix.lower() == ".pdf":
            text = self._extract_pdf_text(path)
        else:
            text = path.read_text(encoding="utf-8", errors="ignore")
        if not text.strip():
            return []
        return self._extract_theorem_snippets(text)

    def _fetch_remote(self, url: str) -> tuple[str, str, str]:
        payload = self._fetch_remote_payload(url)
        return str(payload.get("title", url)), str(payload.get("text", "")), str(payload.get("content_kind", "text"))

    def _read_source(self, source: str, *, allow_network: bool) -> dict[str, Any]:
        path = Path(source)
        if path.exists():
            if path.is_dir():
                for candidate_name in ("README.md", "LITERATURE.md", "STRATEGY.md"):
                    candidate = path / candidate_name
                    if candidate.exists():
                        path = candidate
                        break
                else:
                    markdown_files = sorted(path.glob("*.md"))
                    if markdown_files:
                        path = markdown_files[0]
                    else:
                        return {
                            "status": "directory_without_text_source",
                            "source": source,
                            "source_type": "local_directory",
                            "title": path.name,
                            "text": "",
                            "links": [],
                        }
            if path.suffix.lower() == ".pdf":
                text = self._extract_pdf_text(path)
                if not text:
                    return {
                        "status": "local_pdf_without_text",
                        "source": source,
                        "source_type": "local_pdf",
                        "title": path.name,
                        "text": "",
                        "links": [],
                    }
                return {
                    "status": "ok",
                    "source": source,
                    "source_type": "local_pdf",
                    "title": path.name,
                    "text": text,
                    "links": [],
                }
            text = path.read_text(encoding="utf-8", errors="ignore")
            return {
                "status": "ok",
                "source": source,
                "source_type": "local_path",
                "title": path.name,
                "text": text,
                "links": [],
            }
        if source.startswith("http://") or source.startswith("https://"):
            if not allow_network:
                return {
                    "status": "skipped_network_disabled",
                    "source": source,
                    "source_type": "remote_url",
                    "title": source,
                    "text": "",
                    "links": [],
                }
            try:
                payload = self._fetch_remote_payload(source)
                return {
                    "status": "ok",
                    "source": source,
                    "source_type": f"remote_{payload.get('content_kind', 'text')}",
                    "title": str(payload.get("title", source)),
                    "text": str(payload.get("text", "")),
                    "links": payload.get("links", []),
                }
            except (OSError, URLError, TimeoutError) as exc:
                return {
                    "status": "fetch_error",
                    "source": source,
                    "source_type": "remote_url",
                    "title": source,
                    "text": "",
                    "error": str(exc),
                }
        return {
            "status": "missing",
            "source": source,
            "source_type": "unknown",
            "title": source,
            "text": "",
            "links": [],
        }

    def _iter_contextual_lines(self, text: str) -> list[tuple[str, list[str]]]:
        contextual_lines: list[tuple[str, list[str]]] = []
        active_numbers: set[str] = set()
        active_number_ttl = 0
        for raw_line in text.splitlines():
            line = " ".join(raw_line.strip().split())
            if not line:
                continue
            referenced_numbers = {match.group(1) for match in self.ERDOS_REFERENCE_PATTERN.finditer(line)}
            if referenced_numbers:
                active_numbers = referenced_numbers
                active_number_ttl = 6
            elif active_number_ttl > 0:
                active_number_ttl -= 1
            else:
                active_numbers = set()
            contextual_lines.append((line, sorted(active_numbers)))
        return contextual_lines

    def _extract_candidates(self, text: str, *, source_type: str) -> list[dict[str, Any]]:
        candidates: list[dict[str, Any]] = []
        contextual_lines = self._iter_contextual_lines(text)
        for index, (line, context_numbers) in enumerate(contextual_lines):
            for pattern, weight, kind_hint in self.STATEMENT_PATTERNS:
                match = pattern.match(line)
                if not match:
                    continue
                statement = match.group(1).strip().strip("`")
                if statement.lower().endswith("the following holds.") and index + 1 < len(contextual_lines):
                    continuation = contextual_lines[index + 1][0].strip()
                    if continuation and continuation[0].isupper():
                        statement = f"{statement} {continuation}"
                if len(statement) < 20 or len(statement) > 300:
                    continue
                if "http://" in statement or "https://" in statement:
                    continue
                score = weight + (2 if source_type == "local_path" else 0)
                candidates.append(
                    {
                        "statement": statement,
                        "score": score,
                        "kind_hint": kind_hint,
                        "context_numbers": context_numbers,
                    }
                )
                break
        return candidates

    def _normalize_evidence_line(self, raw_line: str) -> str:
        line = " ".join(raw_line.strip().split())
        line = re.sub(r"^\d+\.\s+", "", line)
        line = re.sub(r"^[-*]\s+", "", line)
        if line.startswith("#") or line.startswith("|") or line.startswith("```"):
            return ""
        if line.startswith("[ ]") or line.startswith("[x]") or line.startswith("http://") or line.startswith("https://"):
            return ""
        if line.lower().startswith("read ") or line.startswith("阅读 "):
            return ""
        if re.fullmatch(r"https?://\S+", line):
            return ""
        if "└──" in line or "├──" in line or line.lower().startswith("**month"):
            return ""
        lowered = line.lower()
        if (
            lowered.startswith("function ")
            or lowered.startswith("const ")
            or lowered.startswith("let ")
            or lowered.startswith("var ")
            or "window.location" in lowered
            or "document." in lowered
            or "addEventListener" in line
            or "=>" in line
            or re.search(r"\breturn\s+[A-Za-z0-9_.$()]+;?$", line)
        ):
            return ""
        if lowered in {
            "create a formalisation here",
            "currently working on this problem",
            "this problem looks difficult",
            "this problem looks tractable",
            "the results on this problem could be formalisable",
            "i am working on formalising the results on this problem",
        }:
            return ""
        lowered = line.lower()
        if any(token in lowered for token in self.SHELLISH_TOKENS):
            return ""
        if "`" in line and re.search(r"`[^`]+`", line):
            return ""
        if re.search(r"(?:^|[\s(])(?:src|docs|results|data)/\S+", line):
            return ""
        if re.search(r"\b\S+\.(?:py|md|lean|json|yaml|yml|sh|log)\b", line) and not any(
            cue in lowered for cue in ("problem", "theorem", "lemma", "conjecture", "bound", "impossible", "possible")
        ):
            return ""
        return line.strip()

    def _candidate_evidence_kind(self, candidate: dict[str, Any]) -> str:
        kind_hint = str(candidate.get("kind_hint", "")).strip()
        if kind_hint:
            return kind_hint
        statement = str(candidate.get("statement", "")).strip()
        lower = statement.lower()
        if any(cue in lower for cue in self.OPEN_GAP_CUES):
            return "open_gap"
        if any(cue in lower for cue in self.KNOWN_RESULT_CUES):
            return "known_result"
        if any(cue in lower for cue in self.MODERN_TOOL_CUES):
            return "modern_tool"
        if any(cue in lower for cue in self.PROOF_INGREDIENT_CUES):
            return "proof_ingredient"
        return "proof_ingredient"

    def _extract_evidence_items(
        self,
        text: str,
        *,
        problem: ProblemRecord,
        source: str,
        title: str,
        candidate_statements: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        problem_number = self._erdos_problem_number(problem) if self._is_erdos_problem(problem) else ""
        source_descriptor = f"{source} {title}"
        source_numbers = {match.group(1) for match in self.ERDOS_SOURCE_PATTERN.finditer(source_descriptor)}
        source_problem_mismatch = bool(problem_number and source_numbers and problem_number not in source_numbers)
        candidate_strings: list[str] = []
        for candidate in candidate_statements:
            statement = str(candidate.get("statement", "")).strip()
            if not statement:
                continue
            context_numbers = {str(number) for number in candidate.get("context_numbers", []) if str(number).strip()}
            if problem_number:
                if context_numbers and problem_number not in context_numbers:
                    continue
                if not context_numbers and source_numbers and problem_number not in source_numbers:
                    continue
            candidate_strings.append(statement.lower())
            kind = self._candidate_evidence_kind(candidate)
            items.append(
                {
                    "kind": kind,
                    "statement": statement,
                    "score": int(candidate.get("score", 0)) + 3,
                    "source": source,
                    "title": title,
                }
            )

        for raw_line, active_numbers in self._iter_contextual_lines(text):
            line = self._normalize_evidence_line(raw_line)
            if len(line) < 24 or len(line) > 220:
                continue
            lower = line.lower()
            if problem_number:
                referenced_numbers = {match.group(1) for match in self.ERDOS_REFERENCE_PATTERN.finditer(line)}
                if source_problem_mismatch and problem_number not in referenced_numbers and problem_number not in active_numbers:
                    continue
                if referenced_numbers and problem_number not in referenced_numbers:
                    continue
                if active_numbers and problem_number not in active_numbers:
                    continue
            if any(candidate in lower for candidate in candidate_strings):
                continue
            matched_kinds: list[tuple[str, int]] = []
            has_open_gap = any(cue in lower for cue in self.OPEN_GAP_CUES)
            if has_open_gap:
                matched_kinds.append(("open_gap", 2))
            if not has_open_gap and any(cue in lower for cue in self.KNOWN_RESULT_CUES):
                matched_kinds.append(("known_result", 3))
            if any(cue in lower for cue in self.PROOF_INGREDIENT_CUES):
                matched_kinds.append(("proof_ingredient", 2))
            if any(cue in lower for cue in self.MODERN_TOOL_CUES):
                matched_kinds.append(("modern_tool", 2))
            for kind, score in matched_kinds:
                items.append(
                    {
                        "kind": kind,
                        "statement": line,
                        "score": score,
                        "source": source,
                        "title": title,
                    }
                )
        return items

    def _synthesize_evidence(self, snapshots: list[dict[str, Any]]) -> dict[str, Any]:
        raw_items: list[dict[str, Any]] = []
        for snapshot in snapshots:
            raw_items.extend(snapshot.get("evidence_items", []))

        deduped: dict[tuple[str, str], dict[str, Any]] = {}
        for item in raw_items:
            statement = str(item.get("statement", "")).strip()
            kind = str(item.get("kind", "")).strip()
            if not statement or not kind:
                continue
            key = (kind, statement.lower())
            current = deduped.get(key)
            if current is None or int(item.get("score", 0)) > int(current.get("score", 0)):
                deduped[key] = dict(item)

        grouped: dict[str, list[dict[str, Any]]] = {
            "known_results": [],
            "proof_ingredients": [],
            "modern_tools": [],
            "open_gaps": [],
        }
        name_map = {
            "known_result": "known_results",
            "proof_ingredient": "proof_ingredients",
            "modern_tool": "modern_tools",
            "open_gap": "open_gaps",
        }
        for item in deduped.values():
            bucket = name_map.get(str(item["kind"]))
            if not bucket:
                continue
            grouped[bucket].append(item)

        for bucket in grouped.values():
            bucket.sort(key=lambda entry: (-int(entry.get("score", 0)), len(str(entry.get("statement", "")))))

        attributed_sources = sorted({str(item.get("source", "")) for item in deduped.values() if str(item.get("source", "")).strip()})
        return {
            "counts": {name: len(items) for name, items in grouped.items()},
            "source_attribution_count": len(attributed_sources),
            "sources": attributed_sources,
            "known_results": grouped["known_results"][:6],
            "proof_ingredients": grouped["proof_ingredients"][:6],
            "modern_tools": grouped["modern_tools"][:6],
            "open_gaps": grouped["open_gaps"][:6],
        }

    def _select_candidate(self, problem: ProblemRecord, snapshots: list[dict[str, Any]]) -> dict[str, Any]:
        title_tokens = [token.lower() for token in re.findall(r"[A-Za-z0-9]+", problem.title) if len(token) >= 4]
        problem_number = self._erdos_problem_number(problem) if self._is_erdos_problem(problem) else ""
        family = self._infer_problem_family(
            problem,
            recovered_statement=problem.statement,
            evidence={"known_results": [], "proof_ingredients": [], "modern_tools": [], "open_gaps": []},
        )
        ranked: list[dict[str, Any]] = []
        seen: set[str] = set()
        for snapshot in snapshots:
            snapshot_kind = str(snapshot.get("kind", "")).strip()
            source_descriptor = f"{snapshot.get('source', '')} {snapshot.get('title', '')}"
            source_numbers = {match.group(1) for match in self.ERDOS_SOURCE_PATTERN.finditer(source_descriptor)}
            for candidate in snapshot.get("candidate_statements", []):
                statement = str(candidate["statement"]).strip()
                if statement in seen:
                    continue
                seen.add(statement)
                score = int(candidate["score"])
                statement_lower = statement.lower()
                context_numbers = {str(number) for number in candidate.get("context_numbers", []) if str(number).strip()}
                if problem_number and source_numbers and problem_number not in source_numbers and problem_number not in context_numbers:
                    continue
                for token in title_tokens:
                    if token in statement_lower:
                        score += 1
                score += self._candidate_target_bonus(problem=problem, family=family, statement=statement)
                if problem.open_problem:
                    if any(
                        cue in statement_lower
                        for cue in (
                            "finitely many",
                            "determine whether",
                            "for which values",
                            "does every",
                            "does there exist",
                            "conjecture",
                        )
                    ):
                        score += 2
                if "equivalently" in statement_lower:
                    score += 1
                if snapshot_kind.startswith("companion_"):
                    score -= 3
                if problem_number:
                    if problem_number in context_numbers:
                        score += 5
                    elif context_numbers:
                        score -= 5
                    if problem_number in source_numbers:
                        score += 3
                    elif source_numbers:
                        score -= 4
                ranked.append(
                    {
                        "statement": statement,
                        "score": score,
                        "source": snapshot["source"],
                        "title": snapshot["title"],
                        "context_numbers": sorted(context_numbers),
                        "kind": snapshot_kind,
                    }
                )
        ranked.sort(key=lambda item: (-item["score"], len(item["statement"])))
        if ranked:
            return ranked[0]
        return {}

    def probe_sources(
        self,
        source_entries: list[dict[str, str]],
        *,
        problem: ProblemRecord,
        allow_network: bool = False,
        cache_dir: Path | None = None,
    ) -> dict[str, Any]:
        snapshots: list[dict[str, Any]] = []
        skipped_sources: list[dict[str, Any]] = []
        if cache_dir is not None:
            cache_dir.mkdir(parents=True, exist_ok=True)
        for index, entry in enumerate(source_entries, start=1):
            raw_snapshot = self._read_source(entry["source"], allow_network=allow_network)
            if raw_snapshot["status"] != "ok":
                skipped_sources.append(raw_snapshot)
                continue
            text = str(raw_snapshot["text"]).strip()
            if not text:
                skipped_sources.append({**raw_snapshot, "status": "empty"})
                continue
            snapshot: dict[str, Any] = {
                "source": raw_snapshot["source"],
                "kind": entry["kind"],
                "source_type": raw_snapshot["source_type"],
                "title": raw_snapshot["title"],
                "excerpt": text[:800],
                "links": raw_snapshot.get("links", []),
                "candidate_statements": self._extract_candidates(text, source_type=str(raw_snapshot["source_type"])),
            }
            snapshot["evidence_items"] = self._extract_evidence_items(
                text,
                problem=problem,
                source=str(raw_snapshot["source"]),
                title=str(raw_snapshot["title"]),
                candidate_statements=snapshot["candidate_statements"],
            )
            if cache_dir is not None:
                cache_path = cache_dir / f"{index:02d}-{slugify(raw_snapshot['title']) or 'source'}.txt"
                write_text(cache_path, text + "\n")
                snapshot["cache_path"] = str(cache_path)
            snapshots.append(snapshot)

        best_candidate = self._select_candidate(problem, snapshots)
        return {
            "source_count": len(source_entries),
            "snapshot_count": len(snapshots),
            "skipped_source_count": len(skipped_sources),
            "snapshots": snapshots,
            "skipped_sources": skipped_sources,
            "best_candidate": best_candidate,
            "evidence": self._synthesize_evidence(snapshots),
        }

    def harvest(self, project_dir: Path, problem: ProblemRecord, *, allow_network: bool = False) -> dict[str, Any]:
        manifest = load_project_manifest(project_dir)
        cache_dir = project_dir / "idea" / "reference_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        paper_inventory_path = self._paper_inventory_path(project_dir)
        existing_inventory = read_json(paper_inventory_path, default={})
        default_inventory: dict[str, Any] = {
            "generated_at": utc_now_iso(),
            "problem_id": problem.problem_id,
            "query_count": 0,
            "candidate_count": 0,
            "downloaded_pdf_count": 0,
            "manual_followup_count": 0,
            "records": [],
        }
        paper_inventory: dict[str, Any] = (
            existing_inventory if isinstance(existing_inventory, dict) and existing_inventory else default_inventory
        )

        initial_source_entries = self._source_entries(project_dir, problem)
        initial_probe = self.probe_sources(
            initial_source_entries,
            problem=problem,
            allow_network=allow_network,
            cache_dir=None,
        )
        recovered_statement_seed = str(initial_probe.get("best_candidate", {}).get("statement", "")).strip()
        if allow_network:
            paper_inventory = self._acquire_related_papers(
                project_dir,
                problem,
                recovered_statement=recovered_statement_seed,
                evidence=initial_probe.get("evidence", {}),
                snapshots=initial_probe.get("snapshots", []),
                cache_dir=cache_dir,
            )
            write_json(paper_inventory_path, paper_inventory)

        source_entries = self._source_entries(project_dir, problem)
        probe = self.probe_sources(source_entries, problem=problem, allow_network=allow_network, cache_dir=cache_dir)
        snapshots = probe["snapshots"]
        skipped_sources = probe["skipped_sources"]
        best_candidate = probe["best_candidate"]
        evidence = probe["evidence"]
        exact_statement_before = has_exact_statement(project_dir)
        current_statement = read_exact_statement(project_dir).strip()
        current_context = read_json(project_dir / "idea" / "problem_context.json", default={})
        current_source = str(current_context.get("exact_statement_source", "")).strip()
        auto_managed_statement = current_source.startswith("literature recovery from ")
        problem_statement = str(problem.statement).strip()
        if not exact_statement_before and problem_statement and not self._is_placeholder_statement(problem_statement):
            set_exact_statement(project_dir, problem_statement, source="problem bank")
            exact_statement_before = True
            current_statement = problem_statement
            current_source = "problem bank"
            auto_managed_statement = False
        recovered_status = "not_found"
        applied_statement = ""
        if best_candidate and (
            not exact_statement_before
            or (auto_managed_statement and current_statement != str(best_candidate.get("statement", "")).strip())
        ):
            applied_statement = str(best_candidate["statement"]).strip()
            set_exact_statement(
                project_dir,
                applied_statement,
                source=f"literature recovery from {best_candidate['source']}",
            )
            recovered_status = "updated" if exact_statement_before else "recovered"
        elif best_candidate:
            recovered_status = "candidate_found_existing_statement_kept"

        report = {
            "generated_at": utc_now_iso(),
            "project_name": manifest["project_name"],
            "problem_id": problem.problem_id,
            "allow_network": allow_network,
            "source_count": probe["source_count"],
            "snapshot_count": probe["snapshot_count"],
            "skipped_source_count": probe["skipped_source_count"],
            "paper_inventory": {
                "path": str(self._paper_inventory_path(project_dir)),
                "candidate_count": int(paper_inventory.get("candidate_count", 0)),
                "downloaded_pdf_count": int(paper_inventory.get("downloaded_pdf_count", 0)),
                "manual_followup_count": int(paper_inventory.get("manual_followup_count", 0)),
                "theorem_snippet_count": int(paper_inventory.get("theorem_snippet_count", 0)),
            },
            "recovered_statement": {
                "status": recovered_status,
                "statement": applied_statement or str(best_candidate.get("statement", "")),
                "source": str(best_candidate.get("source", "")),
                "score": int(best_candidate.get("score", 0)),
            },
            "evidence": evidence,
            "snapshots": snapshots,
            "skipped_sources": skipped_sources,
        }

        digest_lines = [
            f"# Literature Digest for {problem.title}",
            "",
            f"- Sources inspected: `{len(source_entries)}`",
            f"- Snapshots collected: `{len(snapshots)}`",
            f"- Network enabled: `{allow_network}`",
            f"- Paper candidates tracked: `{int(paper_inventory.get('candidate_count', 0))}`",
            f"- Downloaded/open local papers: `{int(paper_inventory.get('downloaded_pdf_count', 0))}`",
            f"- Theorem snippets extracted from papers: `{int(paper_inventory.get('theorem_snippet_count', 0))}`",
            "",
            "## Statement Recovery",
            "",
        ]
        recovered_statement = report["recovered_statement"]
        if recovered_statement["statement"]:
            digest_lines.extend(
                [
                    f"- Status: `{recovered_statement['status']}`",
                    f"- Source: {recovered_statement['source']}",
                    f"- Candidate: {recovered_statement['statement']}",
                    "",
                ]
            )
        else:
            digest_lines.extend(["- No candidate statement recovered yet.", ""])

        digest_lines.extend(["## Literature Evidence", ""])
        if evidence["known_results"]:
            digest_lines.append("### Known Results")
            digest_lines.append("")
            for item in evidence["known_results"][:4]:
                digest_lines.append(f"- {item['statement']}  Source: {item['source']}")
            digest_lines.append("")
        if evidence["proof_ingredients"]:
            digest_lines.append("### Proof Ingredients")
            digest_lines.append("")
            for item in evidence["proof_ingredients"][:4]:
                digest_lines.append(f"- {item['statement']}  Source: {item['source']}")
            digest_lines.append("")
        if evidence["modern_tools"]:
            digest_lines.append("### Modern Tools")
            digest_lines.append("")
            for item in evidence["modern_tools"][:4]:
                digest_lines.append(f"- {item['statement']}  Source: {item['source']}")
            digest_lines.append("")
        if evidence["open_gaps"]:
            digest_lines.append("### Open Gaps")
            digest_lines.append("")
            for item in evidence["open_gaps"][:4]:
                digest_lines.append(f"- {item['statement']}  Source: {item['source']}")
            digest_lines.append("")

        digest_lines.extend(["## Source Notes", ""])
        for snapshot in snapshots[:6]:
            digest_lines.extend(
                [
                    f"### {snapshot['title']}",
                    "",
                    f"- Source: {snapshot['source']}",
                    f"- Kind: `{snapshot['kind']}`",
                    f"- Candidate statements found: `{len(snapshot['candidate_statements'])}`",
                    "",
                ]
            )
        if paper_inventory.get("records"):
            digest_lines.extend(["## Paper Inventory", ""])
            for record in paper_inventory["records"][:8]:
                digest_lines.append(
                    f"- {record['title']}  Status: `{record['status']}`  Source: {record.get('source_url') or record.get('landing_page_url')}"
                )
                for snippet in record.get("theorem_snippets", [])[:2]:
                    label = f" {snippet['label']}" if snippet.get("label") else ""
                    digest_lines.append(f"  - {snippet['kind'].title()}{label}: {snippet['statement']}")
            digest_lines.append("")
        if skipped_sources:
            digest_lines.extend(["## Skipped Sources", ""])
            for skipped in skipped_sources[:6]:
                digest_lines.append(f"- {skipped['source']}: `{skipped['status']}`")
            digest_lines.append("")

        paper_theorem_inventory = {
            "generated_at": utc_now_iso(),
            "problem_id": problem.problem_id,
            "paper_count": len(paper_inventory.get("records", [])),
            "theorem_snippet_count": int(paper_inventory.get("theorem_snippet_count", 0)),
            "papers": [
                {
                    "title": record.get("title", ""),
                    "doi": record.get("doi", ""),
                    "status": record.get("status", ""),
                    "local_path": record.get("local_path", ""),
                    "theorem_snippets": record.get("theorem_snippets", []),
                }
                for record in paper_inventory.get("records", [])
                if record.get("theorem_snippets")
            ],
        }

        write_json(project_dir / "idea" / "reference_snapshots.json", report)
        write_json(paper_inventory_path, paper_inventory)
        write_json(self._paper_theorem_inventory_path(project_dir), paper_theorem_inventory)
        write_json(project_dir / "idea" / "statement_recovery.json", report["recovered_statement"])
        write_json(project_dir / "idea" / "literature_evidence.json", evidence)
        write_text(project_dir / "idea" / "literature_digest.md", "\n".join(digest_lines) + "\n")
        return report
