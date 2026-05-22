#!/usr/bin/env python3
"""Build a conservative IMO P6+ shortlist from imported open problem banks.

The goal is not to certify that a problem is easy. Open problems can have
elementary statements and still be far beyond current mathematics. This script
does the first broad-screening stage: keep records whose metadata suggests an
elementary, contest-adjacent attack surface, demote famous hard problems, and
write a candidate pool for active math-scout probes.

The script intentionally avoids importing AMRA modules so it can run even when
CLI imports are temporarily broken by unrelated work.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data"
BANK_ROOT = DATA_ROOT / "banks"
DEFAULT_OUTPUT_DIR = DATA_ROOT / "research_open" / "shortlists"

UNSOLVED_BANK = BANK_ROOT / "unsolvedmath_index.yaml"
FORMAL_BANK = BANK_ROOT / "formal_conjectures_open_research.yaml"

TARGET_DOMAINS = {
    "number_theory",
    "combinatorics",
    "graph_theory",
    "geometry",
    "algebra",
}

ADVANCED_DOMAINS = {
    "algebraic_geometry",
    "analysis",
    "dynamical_systems",
    "group_theory",
    "logic",
    "mathematical_physics",
    "partial_differential_equations",
    "probability",
    "set_theory",
    "topology",
}

FAMOUS_HARD_KEYWORDS = {
    "abc conjecture",
    "beal conjecture",
    "birch",
    "borsuk",
    "bounded burnside",
    "brocard",
    "casas-alvero",
    "collatz",
    "crouzeix",
    "diagonal ramsey",
    "erdos discrepancy",
    "erdos-selfridge",
    "four color theorem",
    "gilbreath",
    "goldbach",
    "hadamard",
    "hodge",
    "hilbert's 17th",
    "hilbert's 18th",
    "inverse galois",
    "jacobian conjecture",
    "lonely runner",
    "millennium",
    "navier",
    "odd perfect",
    "p vs np",
    "perfect cuboid",
    "poincare",
    "riemann",
    "sofic",
    "sunflower",
    "swinnerton-dyer",
    "tate conjecture",
    "twin prime",
    "union-closed",
    "yang-mills",
}

FAMOUS_HARD_PATTERNS = {
    "abc": re.compile(r"\babc\b"),
    "ramsey": re.compile(r"\bramsey\b"),
}

ELEMENTARY_SIGNAL_KEYWORDS = {
    "coloring",
    "combinatorial",
    "consecutive",
    "covering",
    "diophantine",
    "divisor",
    "edge",
    "erdos",
    "finite",
    "graph",
    "grid",
    "integer",
    "lattice",
    "matrix",
    "number",
    "oeis",
    "partition",
    "polynomial",
    "prime",
    "sequence",
    "set",
    "sum",
    "tiling",
    "tree",
    "vertex",
}

FORMAL_SOURCE_SCORE = {
    "ErdosProblems": 30,
    "OEIS": 28,
    "Wikipedia": 16,
    "GreensOpenProblems": 14,
    "Mathoverflow": 8,
    "WrittenOnTheWallII": 8,
    "Books": 4,
    "Other": 2,
    "OptimizationConstants": -8,
    "Paper": -10,
    "Arxiv": -12,
    "Kourovka": -18,
    "HilbertProblems": -35,
    "OpenQuantumProblems": -45,
    "Millenium": -70,
}


def _read_yaml(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def _source_dir(record: dict[str, Any]) -> str:
    source_file = str(record.get("metadata", {}).get("source_file", ""))
    parts = source_file.split("/")
    return parts[1] if len(parts) > 1 and parts[0] == "FormalConjectures" else ""


def _text_blob(record: dict[str, Any]) -> str:
    metadata = record.get("metadata", {})
    raw = " ".join(
        [
            str(record.get("problem_id", "")),
            str(record.get("title", "")),
            str(record.get("statement", "")),
            str(record.get("domain", "")),
            str(metadata.get("source_file", "")),
            str(metadata.get("declaration_name", "")),
            " ".join(str(tag) for tag in record.get("tags", []) or []),
        ]
    )
    normalized = unicodedata.normalize("NFKD", raw).encode("ascii", "ignore").decode("ascii")
    return normalized.lower()


def _count_keyword_hits(text: str, keywords: set[str]) -> int:
    return sum(1 for keyword in keywords if keyword in text)


def _hard_hits(text: str) -> list[str]:
    hits = [keyword for keyword in FAMOUS_HARD_KEYWORDS if keyword in text]
    hits.extend(name for name, pattern in FAMOUS_HARD_PATTERNS.items() if pattern.search(text))
    return sorted(set(hits))


def _preview(statement: str, limit: int = 280) -> str:
    compact = re.sub(r"\s+", " ", statement).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def _tier(score: int) -> str:
    if score >= 85:
        return "A_active_scout_first"
    if score >= 70:
        return "B_good_scout_candidate"
    if score >= 55:
        return "C_manual_review"
    return "D_hold"


def _record_base(record: dict[str, Any], *, bank: str) -> dict[str, Any]:
    metadata = record.get("metadata", {}) if isinstance(record.get("metadata"), dict) else {}
    references = record.get("references", []) or []
    return {
        "problem_record": record,
        "problem_id": str(record.get("problem_id", "")),
        "title": str(record.get("title", "")),
        "bank": bank,
        "source": str(record.get("source", "")),
        "domain": str(record.get("domain", "")),
        "difficulty_level": metadata.get("difficulty_level"),
        "statement_quality": metadata.get("statement_quality"),
        "formalized": str(record.get("formalized", "no")),
        "source_file": metadata.get("source_file"),
        "reference": references[0] if references else "",
        "statement_preview": _preview(str(record.get("statement", ""))),
    }


def score_unsolved(record: dict[str, Any]) -> tuple[int, list[str], list[str]]:
    score = 20
    reasons: list[str] = ["unsolvedmath_index"]
    risks: list[str] = ["source_detail_page_required"]
    metadata = record.get("metadata", {}) if isinstance(record.get("metadata"), dict) else {}
    level = metadata.get("difficulty_level")
    domain = str(record.get("domain", ""))
    text = _text_blob(record)

    if level == 3:
        score += 34
        reasons.append("difficulty_L3_contest_adjacent")
    elif level == 4:
        score += 20
        reasons.append("difficulty_L4_research_entry")
    elif level == 2:
        score += 2
        reasons.append("difficulty_L2_may_be_too_easy")
        risks.append("below_target_band")
    elif level == 1:
        score -= 28
        risks.append("below_target_band")
    elif level == 5:
        score -= 75
        risks.append("far_above_target_band")

    if domain in TARGET_DOMAINS:
        score += 18
        reasons.append(f"target_domain_{domain}")
    elif domain in ADVANCED_DOMAINS:
        score -= 26
        risks.append(f"advanced_domain_{domain}")
    else:
        score -= 6
        risks.append(f"non_target_domain_{domain}")

    elementary_hits = _count_keyword_hits(text, ELEMENTARY_SIGNAL_KEYWORDS)
    if elementary_hits:
        score += min(18, elementary_hits * 3)
        reasons.append(f"elementary_signal_hits_{elementary_hits}")

    if str(metadata.get("statement_quality", "")) == "index_snippet":
        score -= 8

    statement_len = len(str(record.get("statement", "")))
    if 80 <= statement_len <= 700:
        score += 7
        reasons.append("compact_statement")
    elif statement_len < 40:
        score -= 12
        risks.append("statement_too_short")
    elif statement_len > 1400:
        score -= 8
        risks.append("statement_long")

    hard_hits = _hard_hits(text)
    if hard_hits:
        score -= 65
        risks.append("famous_hard:" + ",".join(sorted(hard_hits)[:3]))

    return score, reasons, risks


def score_formal(record: dict[str, Any]) -> tuple[int, list[str], list[str]]:
    score = 36
    reasons: list[str] = ["formal_lean4_statement"]
    risks: list[str] = ["open_research_core_unproven"]
    text = _text_blob(record)
    source_dir = _source_dir(record)
    source_score = FORMAL_SOURCE_SCORE.get(source_dir, -4)
    score += source_score
    if source_dir:
        reasons.append(f"formal_source_{source_dir}")
    if source_score < 0:
        risks.append(f"lower_priority_source_{source_dir}")

    if str(record.get("formalized", "")) == "lean4_statement":
        score += 14
        reasons.append("exact_formal_contract")

    elementary_hits = _count_keyword_hits(text, ELEMENTARY_SIGNAL_KEYWORDS)
    if elementary_hits:
        score += min(18, elementary_hits * 3)
        reasons.append(f"elementary_signal_hits_{elementary_hits}")

    statement_len = len(str(record.get("statement", "")))
    if statement_len <= 800:
        score += 10
        reasons.append("short_formal_statement")
    elif statement_len <= 1800:
        score += 3
    else:
        score -= 12
        risks.append("large_formal_statement")

    hard_hits = _hard_hits(text)
    if hard_hits:
        score -= 70
        risks.append("famous_hard:" + ",".join(sorted(hard_hits)[:3]))

    if "Axiom" in str(record.get("statement", "")):
        score -= 8
        risks.append("may_depend_on_custom_axioms")

    return score, reasons, risks


def _balance_key(item: dict[str, Any]) -> str:
    bank = str(item.get("bank", ""))
    if bank == "formal_conjectures_open_research":
        source_file = str(item.get("source_file") or "")
        parts = source_file.split("/")
        source_dir = parts[1] if len(parts) > 1 and parts[0] == "FormalConjectures" else "Other"
        return f"{bank}:{source_dir}"
    return f"{bank}:L{item.get('difficulty_level')}:{item.get('domain')}"


def _balanced_shortlist(candidates: list[dict[str, Any]], *, limit: int) -> list[dict[str, Any]]:
    eligible = [item for item in candidates if item["tier"] != "D_hold"]
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in eligible:
        grouped.setdefault(_balance_key(item), []).append(item)
    for rows in grouped.values():
        rows.sort(key=lambda item: (-int(item["imo_p6_plus_score"]), str(item["problem_id"])))

    group_order = sorted(
        grouped,
        key=lambda key: (
            -int(grouped[key][0]["imo_p6_plus_score"]),
            -len(grouped[key]),
            key,
        ),
    )
    selected: list[dict[str, Any]] = []
    index = 0
    while len(selected) < limit:
        advanced = False
        for key in group_order:
            rows = grouped[key]
            if index >= len(rows):
                continue
            selected.append(rows[index])
            advanced = True
            if len(selected) >= limit:
                break
        if not advanced:
            break
        index += 1
    return selected


def build_candidates(*, limit: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    source_counts: Counter[str] = Counter()
    tier_counts: Counter[str] = Counter()

    for record in _read_yaml(UNSOLVED_BANK):
        if not record.get("open_problem", True):
            continue
        score, reasons, risks = score_unsolved(record)
        item = _record_base(record, bank="unsolvedmath_index")
        item.update(
            {
                "imo_p6_plus_score": score,
                "tier": _tier(score),
                "reason_codes": reasons,
                "risk_flags": risks,
                "recommended_next_action": "fetch_detail_page_then_active_math_scout",
            }
        )
        candidates.append(item)

    for record in _read_yaml(FORMAL_BANK):
        if not record.get("open_problem", True):
            continue
        score, reasons, risks = score_formal(record)
        item = _record_base(record, bank="formal_conjectures_open_research")
        item.update(
            {
                "imo_p6_plus_score": score,
                "tier": _tier(score),
                "reason_codes": reasons,
                "risk_flags": risks,
                "recommended_next_action": "active_math_scout_then_lean_dependency_probe",
            }
        )
        candidates.append(item)

    candidates.sort(key=lambda item: (-int(item["imo_p6_plus_score"]), str(item["problem_id"])))
    for item in candidates:
        source_counts[str(item["bank"])] += 1
        tier_counts[str(item["tier"])] += 1

    shortlisted = _balanced_shortlist(candidates, limit=limit)
    shortlist_counts: Counter[str] = Counter(str(item["bank"]) for item in shortlisted)
    shortlist_groups: Counter[str] = Counter(_balance_key(item) for item in shortlisted)
    summary = {
        "schema_version": "amra.imo_p6_plus_shortlist.v1",
        "method": "metadata_prefilter_for_active_math_scout_balanced_by_source_and_domain",
        "source_banks": [str(UNSOLVED_BANK.relative_to(REPO_ROOT)), str(FORMAL_BANK.relative_to(REPO_ROOT))],
        "shortlist_problem_bank": "data/research_open/shortlists/imo_p6_plus_problem_bank.yaml",
        "math_scout_seed_report": "data/research_open/shortlists/imo_p6_plus_scout_seed.json",
        "candidate_count": len(candidates),
        "shortlist_count": len(shortlisted),
        "tier_counts_all_candidates": dict(sorted(tier_counts.items())),
        "bank_counts_all_candidates": dict(sorted(source_counts.items())),
        "bank_counts_shortlist": dict(sorted(shortlist_counts.items())),
        "source_domain_groups_shortlist": dict(sorted(shortlist_groups.items())),
        "interpretation": (
            "This shortlist is a broad-screening input, not a proof of easiness. "
            "Run MathScoutRunner on tier A/B items to validate exact statements and blockers."
        ),
    }
    return shortlisted, summary


def write_outputs(candidates: list[dict[str, Any]], summary: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    public_candidates = [
        {key: value for key, value in item.items() if key != "problem_record"}
        for item in candidates
    ]
    problem_bank = []
    for item in candidates:
        record = dict(item["problem_record"])
        metadata = dict(record.get("metadata", {}) if isinstance(record.get("metadata"), dict) else {})
        metadata["imo_p6_plus_shortlist"] = {
            "score": item["imo_p6_plus_score"],
            "tier": item["tier"],
            "reason_codes": item["reason_codes"],
            "risk_flags": item["risk_flags"],
            "source_shortlist": "data/research_open/shortlists/imo_p6_plus_candidates.json",
        }
        record["metadata"] = metadata
        problem_bank.append(record)

    payload = {**summary, "candidates": public_candidates}
    (output_dir / "imo_p6_plus_candidates.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "imo_p6_plus_candidates.yaml").write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    (output_dir / "imo_p6_plus_problem_bank.yaml").write_text(
        yaml.safe_dump(problem_bank, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    scout_seed_candidates = []
    for rank, item in enumerate(public_candidates, start=1):
        scout_seed_candidates.append(
            {
                **item,
                "rank": rank,
                "score": item["imo_p6_plus_score"],
                "readiness_tier": item["tier"],
                "investment_class": "imo_p6_plus_active_scout",
                "blocker_class": ",".join(item["risk_flags"]),
                "shallow_reasoning": item["reason_codes"],
            }
        )
    (output_dir / "imo_p6_plus_scout_seed.json").write_text(
        json.dumps(
            {
                "schema_version": "amra.math_scout_seed.v1",
                "mode": "imo_p6_plus_shortlist_seed",
                "top_candidates": scout_seed_candidates,
                "shortlist_candidates": [],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# IMO P6+ Open Problem Shortlist",
        "",
        summary["interpretation"],
        "",
        f"- Candidate records scanned: {summary['candidate_count']}",
        f"- Shortlist size: {summary['shortlist_count']}",
        f"- Source banks: {', '.join(summary['source_banks'])}",
        "",
        "## Top Candidates",
        "",
        "| Rank | Score | Tier | Problem | Bank | Domain | Main risks |",
        "| ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    for idx, item in enumerate(public_candidates[:50], start=1):
        risks = ", ".join(item["risk_flags"][:3])
        title = str(item["title"]).replace("|", "\\|")
        lines.append(
            f"| {idx} | {item['imo_p6_plus_score']} | {item['tier']} | "
            f"{title} (`{item['problem_id']}`) | {item['bank']} | {item['domain']} | {risks} |"
        )
    lines.extend(["", "## Required Follow-up", ""])
    lines.extend(
        [
            "1. Fetch detail pages for UnsolvedMath index records before proof work.",
            "2. Run active `MathScoutRunner` probes on tier A/B candidates.",
            "3. Promote only candidates whose probe returns a concrete route, finite certificate, or reusable Lean dependency plan.",
        ]
    )
    (output_dir / "imo_p6_plus_candidates.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=100, help="Maximum number of shortlist entries to write.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    candidates, summary = build_candidates(limit=max(1, args.limit))
    write_outputs(candidates, summary, args.output_dir)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Wrote {len(candidates)} candidates to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
