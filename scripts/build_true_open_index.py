#!/usr/bin/env python3
"""Build a conservative index of genuinely open mathematics targets.

The repository contains several "open" banks whose meaning is not uniform:
some entries are genuine research problems, some are known theorems awaiting
formalization, and some are pointers to problem lists rather than atomic
statements.  This script builds an auditable index by keeping entries with
local evidence of open research status and excluding entries with local evidence
that they are solved, textbook/test/API targets, or known-theorem formalization
tasks.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[1]
OPEN_UNIQUE = REPO / "artifacts/open_problem_screening/open-problem-screen-20260523/open_unique.jsonl"
FINE_SCREEN = REPO / "artifacts/open_problem_screening/open-problem-screen-20260523/fine_screen/fine_screen_ranked.csv"
OUT_DIR = REPO / "data/research_open/true_open_index"

SOLVED_WORDS = {
    "closed",
    "disproved",
    "false",
    "known",
    "proved",
    "refuted",
    "solved",
    "theorem",
}
NON_RESEARCH_CATEGORIES = {
    "api",
    "benchmark",
    "exercise",
    "solved",
    "test",
    "textbook",
}
NON_ATOMIC_STATEMENT_QUALITIES = {
    "index_snippet",
    "placeholder",
    "problem_list_pointer",
}
NON_MATH_SOURCE_FRAGMENTS = {
    "/test",
    "/tests",
    "/util/",
    "formalconjecturestest/",
    "linters/",
}
NON_MATH_TITLE_FRAGMENTS = {
    "flagged",
    "linter",
    "missing-docstring",
    "not-flagged",
    "without-docstring",
}
KNOWN_PROOF_STATUSES = {
    "known_theorem",
    "proved",
    "solved",
    "source_theorem",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_fine_screen(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as handle:
        return {row["problem_id"]: row for row in csv.DictReader(handle)}


def norm(value: Any) -> str:
    return str(value or "").strip().lower()


def has_solved_word(*values: Any) -> bool:
    text = " ".join(norm(value) for value in values)
    return any(word in text for word in SOLVED_WORDS)


def classify(row: dict[str, Any], fine: dict[str, str]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    metadata_status = norm(row.get("metadata_status"))
    metadata_category = norm(row.get("metadata_category"))
    statement_quality = norm(row.get("statement_quality"))
    formalized = norm(row.get("formalized"))
    bank = norm(row.get("bank"))
    reason_codes = {norm(item) for item in row.get("reason_codes", [])}
    recommendation = norm(fine.get("recommendation"))
    proof_attempt_status = norm(fine.get("proof_attempt_status"))
    fine_blocker = norm(fine.get("primary_blocker"))
    source_file = norm(row.get("source_file"))
    problem_id = norm(row.get("problem_id"))
    title = norm(row.get("title"))

    if not row.get("open_problem"):
        return "excluded_not_open", ["open_problem is false"]

    if metadata_status and metadata_status != "open":
        return "excluded_solved_or_nonopen", [f"metadata_status={metadata_status}"]

    if has_solved_word(row.get("metadata_status"), row.get("bank_category"), row.get("title")):
        # Keep explicit "open" status from authoritative open banks; this guard
        # mainly catches solved/proved banks that still appear in merged data.
        if metadata_status != "open":
            return "excluded_solved_or_nonopen", ["status text contains solved/proved/refuted signal"]

    if metadata_category in NON_RESEARCH_CATEGORIES:
        return "excluded_non_research", [f"metadata_category={metadata_category}"]

    if reason_codes & NON_RESEARCH_CATEGORIES:
        return "excluded_non_research", [f"reason_codes include {sorted(reason_codes & NON_RESEARCH_CATEGORIES)}"]

    if any(fragment in source_file for fragment in NON_MATH_SOURCE_FRAGMENTS):
        return "excluded_non_research", [f"non-math source_file={source_file}"]

    if any(fragment in problem_id or fragment in title for fragment in NON_MATH_TITLE_FRAGMENTS):
        return "excluded_non_research", ["title/problem_id indicates linter or metadata test target"]

    if proof_attempt_status in KNOWN_PROOF_STATUSES:
        return "excluded_known_proof", [f"fine_screen.proof_attempt_status={proof_attempt_status}"]

    if recommendation == "formalize_known" and proof_attempt_status == "known_theorem":
        return "excluded_known_proof", ["fine_screen marks formalize_known + known_theorem"]

    if statement_quality in NON_ATOMIC_STATEMENT_QUALITIES:
        # These may be genuine open research areas, but not atomic theorem targets.
        return "needs_statement_recovery", [f"statement_quality={statement_quality}"]

    if formalized not in {"lean4_statement", "no", "yes", "curated", ""}:
        reasons.append(f"unusual formalized={formalized}")

    if metadata_status == "open":
        reasons.append("metadata_status=open")
    if metadata_category == "research":
        reasons.append("metadata_category=research")
    if bank in {
        "formal_conjectures_open_research",
        "erdos_open_637",
        "erdos_open_shortlist_refreshed",
        "triangle_dissection_track",
        "amicable_track",
        "unitary_perfect_track",
        "weird_numbers_track",
        "carmichael_track",
    }:
        reasons.append(f"open research bank={bank}")
    if recommendation:
        reasons.append(f"fine_screen.recommendation={recommendation}")
    if proof_attempt_status:
        reasons.append(f"fine_screen.proof_attempt_status={proof_attempt_status}")
    if fine_blocker:
        reasons.append(f"fine_screen.primary_blocker={fine_blocker}")

    if metadata_status == "open" or "research_open_formal" in norm(row.get("bank_category")):
        return "candidate_true_open", reasons or ["open research metadata"]

    # Curated local tracks are accepted as candidate open only if they are atomic.
    if bank.endswith("_track") and statement_quality not in NON_ATOMIC_STATEMENT_QUALITIES:
        return "candidate_true_open", reasons or [f"curated track={bank}"]

    return "uncertain", reasons or ["no decisive local true-open evidence"]


def compact_record(row: dict[str, Any], fine: dict[str, str], status: str, reasons: list[str]) -> dict[str, Any]:
    return {
        "problem_id": row.get("problem_id"),
        "title": row.get("title"),
        "source": row.get("source"),
        "bank": row.get("bank"),
        "domain": row.get("semantic_domain") or row.get("domain"),
        "statement_preview": row.get("statement_preview"),
        "statement_quality": row.get("statement_quality"),
        "formalized": row.get("formalized"),
        "metadata_status": row.get("metadata_status"),
        "metadata_category": row.get("metadata_category"),
        "declaration_name": row.get("declaration_name"),
        "source_file": row.get("source_file"),
        "references": row.get("references", []),
        "open_research_tier": row.get("open_research_tier"),
        "open_research_score": row.get("open_research_score"),
        "fine_screen": {
            "recommendation": fine.get("recommendation"),
            "proof_attempt_status": fine.get("proof_attempt_status"),
            "primary_blocker": fine.get("primary_blocker"),
            "estimated_proof_effort": fine.get("estimated_proof_effort"),
            "feasibility_score": fine.get("feasibility_score"),
            "fine_screen_ease_score": fine.get("fine_screen_ease_score"),
        }
        if fine
        else {},
        "classification": status,
        "classification_reasons": reasons,
    }


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Any) -> None:
    path.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False), encoding="utf-8")


def render_md(payload: dict[str, Any]) -> str:
    lines = [
        "# True Open Problem Index",
        "",
        f"Generated at: `{payload['generated_at']}`",
        "",
        "This is a conservative local index. It uses repository metadata and AMRA fine-screen evidence; it is not a live literature audit.",
        "",
        "## Counts",
        "",
    ]
    for key, value in payload["counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines += [
        "",
        "## Inclusion Rule",
        "",
        "A record is included as `candidate_true_open` when it has local open-research evidence and no local evidence that it is a known theorem, test/API/textbook target, solved/refuted item, or non-atomic problem-list pointer.",
        "",
        "## Exclusion Rule",
        "",
        "Records are excluded when fine-screen marks `proof_attempt_status=known_theorem`, metadata/category marks non-research or solved/proved/refuted status, or the statement is only an index/list/placeholder requiring statement recovery.",
        "",
        "## Candidate True-Open Entries",
        "",
        "| # | Problem id | Domain | Source | Evidence |",
        "| ---: | --- | --- | --- | --- |",
    ]
    for index, row in enumerate(payload["candidate_true_open"], start=1):
        evidence = "; ".join(row["classification_reasons"][:3])
        lines.append(
            f"| {index} | `{row['problem_id']}` | `{row.get('domain') or ''}` | {row.get('source') or ''} | {evidence} |"
        )
    lines += [
        "",
        "## Known-Proof/Formalization-Only Exclusions",
        "",
        "| # | Problem id | Reason |",
        "| ---: | --- | --- |",
    ]
    for index, row in enumerate(payload["excluded_known_proof"][:100], start=1):
        reason = "; ".join(row["classification_reasons"])
        lines.append(f"| {index} | `{row['problem_id']}` | {reason} |")
    if len(payload["excluded_known_proof"]) > 100:
        lines.append(f"| ... | ... | {len(payload['excluded_known_proof']) - 100} more in JSON |")
    return "\n".join(lines) + "\n"


def main() -> None:
    rows = load_jsonl(OPEN_UNIQUE)
    fine_by_id = load_fine_screen(FINE_SCREEN)
    buckets: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        fine = fine_by_id.get(str(row.get("problem_id")), {})
        status, reasons = classify(row, fine)
        buckets.setdefault(status, []).append(compact_record(row, fine, status, reasons))

    for records in buckets.values():
        records.sort(key=lambda item: (str(item.get("domain") or ""), str(item.get("problem_id") or "")))

    counts = Counter({key: len(value) for key, value in buckets.items()})
    payload = {
        "schema_version": "amra.true_open_index.v1",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_open_inventory": str(OPEN_UNIQUE.relative_to(REPO)),
        "source_fine_screen": str(FINE_SCREEN.relative_to(REPO)),
        "method": {
            "scope": "local repository metadata and AMRA fine-screen evidence only",
            "included": "open research candidates without known-proof/formalization-only, non-research, solved/refuted, or non-atomic statement evidence",
            "not_included": "records requiring statement recovery, known theorem formalization tasks, tests/API/textbook tasks, solved/refuted tasks",
        },
        "counts": dict(sorted(counts.items())),
        "candidate_true_open": buckets.get("candidate_true_open", []),
        "needs_statement_recovery": buckets.get("needs_statement_recovery", []),
        "uncertain": buckets.get("uncertain", []),
        "excluded_known_proof": buckets.get("excluded_known_proof", []),
        "excluded_non_research": buckets.get("excluded_non_research", []),
        "excluded_not_open": buckets.get("excluded_not_open", []),
        "excluded_solved_or_nonopen": buckets.get("excluded_solved_or_nonopen", []),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "true_open_index.json", payload)
    write_yaml(OUT_DIR / "true_open_index.yaml", payload["candidate_true_open"])
    (OUT_DIR / "README.md").write_text(render_md(payload), encoding="utf-8")


if __name__ == "__main__":
    main()
