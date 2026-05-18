from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from typing import Any, Callable
from urllib.parse import quote
from urllib.request import Request, urlopen

from ara_math.models import ProblemRecord
from ara_math.workspace import utc_now_iso


USER_AGENT = "amra/0.2"
ARXIV_ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}

SCRIPT_STYLE_PATTERN = re.compile(r"<(script|style)\b.*?</\1>", re.IGNORECASE | re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
WHITESPACE_PATTERN = re.compile(r"\s+")
OFFICIAL_STATUS_PATTERN = re.compile(r"\b(OPEN|PROVED|DISPROVED)\b")
STATUS_SENTENCE_PATTERN = re.compile(
    r"\b(OPEN|PROVED|DISPROVED)\b\s+(This[^.]+(?:\.[^.]+)?)",
    re.IGNORECASE,
)
LAST_EDITED_PATTERN = re.compile(r"This page was last edited ([^.]+)\.", re.IGNORECASE)
STRONG_SOLUTION_PATTERNS = (
    "solution of erdős problem {problem_id}",
    "solution of erdos problem {problem_id}",
    "settling erdős problem {problem_id}",
    "settling erdos problem {problem_id}",
    "solves erdős problem {problem_id}",
    "solves erdos problem {problem_id}",
)


def fetch_text(url: str, *, timeout: int = 8) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="ignore")


def html_to_text(payload: str) -> str:
    without_scripts = SCRIPT_STYLE_PATTERN.sub(" ", payload)
    without_tags = TAG_PATTERN.sub(" ", without_scripts)
    decoded = html.unescape(without_tags)
    return WHITESPACE_PATTERN.sub(" ", decoded).strip()


def parse_official_status_page(payload: str) -> dict[str, str]:
    text = html_to_text(payload)
    lowered = text.lower()

    sentence_match = STATUS_SENTENCE_PATTERN.search(text)
    if sentence_match:
        headline = sentence_match.group(1).upper()
        status = headline.lower()
        summary = f"{headline} {sentence_match.group(2).strip()}"
    else:
        if "this has been solved" in lowered:
            status = "proved"
        elif "disproved" in lowered or "counterexample" in lowered:
            status = "disproved"
        elif " open " in f" {lowered} ":
            status = "open"
        else:
            status = "unknown"
        match = OFFICIAL_STATUS_PATTERN.search(text)
        headline = match.group(1) if match else ""
        summary = text[:600]

    edited_match = LAST_EDITED_PATTERN.search(text)
    return {
        "status": status,
        "headline": headline,
        "last_edited": edited_match.group(1).strip() if edited_match else "",
        "summary": summary,
    }


def _arxiv_query(problem_id: str) -> str:
    exact_id = str(problem_id).strip()
    terms = [
        f'ti:"Erdos Problem {exact_id}"',
        f'ti:"Erdős Problem {exact_id}"',
        f'abs:"Erdos Problem {exact_id}"',
        f'abs:"Erdős Problem {exact_id}"',
        f'ti:"Solution of Erdos Problem {exact_id}"',
        f'ti:"Solution of Erdős Problem {exact_id}"',
        f'abs:"settling Erdos Problem {exact_id}"',
        f'abs:"settling Erdős Problem {exact_id}"',
    ]
    return " OR ".join(terms)


def parse_arxiv_solution_feed(payload: str, *, problem_id: str) -> list[dict[str, str]]:
    root = ET.fromstring(payload)
    candidates: list[dict[str, str]] = []
    patterns = [item.format(problem_id=problem_id).lower() for item in STRONG_SOLUTION_PATTERNS]

    for entry in root.findall("atom:entry", ARXIV_ATOM_NS):
        title = (entry.findtext("atom:title", default="", namespaces=ARXIV_ATOM_NS) or "").strip()
        summary = (entry.findtext("atom:summary", default="", namespaces=ARXIV_ATOM_NS) or "").strip()
        entry_id = (entry.findtext("atom:id", default="", namespaces=ARXIV_ATOM_NS) or "").strip()
        published = (entry.findtext("atom:published", default="", namespaces=ARXIV_ATOM_NS) or "").strip()
        haystack = f"{title}\n{summary}".lower()
        confidence = "mention"
        if any(pattern in haystack for pattern in patterns):
            confidence = "strong_solution_signal"
        candidates.append(
            {
                "title": title,
                "summary": summary,
                "url": entry_id,
                "published": published,
                "confidence": confidence,
            }
        )
    return candidates


def query_arxiv_solution_candidates(
    problem_id: str,
    *,
    fetcher: Callable[[str], str] = fetch_text,
    max_results: int = 5,
) -> list[dict[str, str]]:
    query = _arxiv_query(problem_id)
    url = (
        "http://export.arxiv.org/api/query?search_query="
        + quote(query)
        + f"&start=0&max_results={max_results}"
    )
    payload = fetcher(url)
    return parse_arxiv_solution_feed(payload, problem_id=problem_id)


def _is_erdos_problem(problem: ProblemRecord) -> bool:
    source_catalog = str((problem.metadata or {}).get("source_catalog", "")).strip().lower()
    return problem.source == "Erdős Problems" or source_catalog == "erdosproblems"


def _official_problem_url(problem: ProblemRecord) -> str:
    for reference in problem.references:
        if "erdosproblems.com" in reference:
            return reference
    return f"https://www.erdosproblems.com/{problem.problem_id}"


def refresh_erdos_problem_record(
    problem: ProblemRecord,
    *,
    fetcher: Callable[[str], str] = fetch_text,
) -> ProblemRecord:
    if not _is_erdos_problem(problem):
        return problem

    metadata = dict(problem.metadata or {})
    remote_status: dict[str, Any] = {
        "checked_at": utc_now_iso(),
        "official_url": _official_problem_url(problem),
        "official_status": "unknown",
        "official_last_edited": "",
        "official_summary": "",
        "solution_candidates": [],
    }

    try:
        official_payload = fetcher(remote_status["official_url"])
        official_status = parse_official_status_page(official_payload)
        remote_status["official_status"] = official_status["status"]
        remote_status["official_last_edited"] = official_status["last_edited"]
        remote_status["official_summary"] = official_status["summary"]
        remote_status["official_headline"] = official_status["headline"]
    except Exception as exc:  # pragma: no cover - exercised via metadata in tests
        remote_status["official_error"] = str(exc)

    if remote_status["official_status"] in {"open", "unknown"}:
        try:
            candidates = query_arxiv_solution_candidates(problem.problem_id, fetcher=fetcher)
            remote_status["solution_candidates"] = candidates
        except Exception as exc:  # pragma: no cover - exercised via metadata in tests
            remote_status["solution_candidate_error"] = str(exc)

    strong_candidates = [
        candidate
        for candidate in remote_status["solution_candidates"]
        if candidate.get("confidence") == "strong_solution_signal"
    ]

    status_state = str(metadata.get("status_state", "open")).strip().lower() or "open"
    open_problem = bool(problem.open_problem)
    if remote_status["official_status"] in {"proved", "disproved"}:
        status_state = remote_status["official_status"]
        open_problem = False
    elif strong_candidates:
        status_state = "likely_solved_preprint"
        open_problem = False

    metadata["status_state"] = status_state
    metadata["remote_status"] = remote_status
    metadata["remote_solution_signal_count"] = len(strong_candidates)
    metadata["statement_quality"] = str(metadata.get("statement_quality", "placeholder"))

    return ProblemRecord(
        problem_id=problem.problem_id,
        title=problem.title,
        source=problem.source,
        statement=problem.statement,
        domain=problem.domain,
        tags=list(problem.tags),
        open_problem=open_problem,
        formalized=problem.formalized,
        notes=problem.notes,
        references=list(problem.references),
        hypotheses=list(problem.hypotheses),
        recommended_strategy=list(problem.recommended_strategy),
        metadata=metadata,
    )
