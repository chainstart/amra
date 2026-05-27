#!/usr/bin/env python3
"""Fast metadata screen for Lean-suitable AMRA problem-bank entries.

This pass is intentionally shallow.  It does not claim that a problem is easy
or solved; it separates entries that are worth a first Lean/formalization pass
from entries that need statement recovery, literature work, or natural-language
research before Lean should be the main tool.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = REPO_ROOT / "data" / "bank_registry.yaml"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "artifacts" / "problem_screening"


MATHLIB_RICH_DOMAINS = {
    "number_theory",
    "graph_theory",
    "combinatorics",
    "algebra",
    "linear_algebra",
    "group_theory",
    "topology",
    "set_theory",
    "logic",
}

MATHLIB_RICH_SEMANTIC_DOMAINS = MATHLIB_RICH_DOMAINS | {
    "finite_combinatorics",
    "elementary_number_theory",
    "order_lattice",
    "real_analysis",
    "probability",
}

LLM_FRIENDLY_DOMAINS = {
    "number_theory",
    "graph_theory",
    "combinatorics",
    "geometry",
    "algebra",
    "ramsey_theory",
}

LLM_FRIENDLY_SEMANTIC_DOMAINS = LLM_FRIENDLY_DOMAINS | {
    "finite_combinatorics",
    "elementary_number_theory",
    "order_lattice",
}

LOW_LEAN_FIRST_DOMAINS = {
    "partial_differential_equations",
    "pdes",
    "mathematical_physics",
    "physics",
    "algebraic_geometry",
    "arithmetic_geometry",
    "biology",
}

HIGH_VALUE_TAGS = {
    "formalization_candidate",
    "starter_theorem",
    "finite_case",
    "lean4",
    "lean",
    "formal_conjectures",
    "formal_statement",
    "graph theory",
    "number theory",
    "combinatorics",
    "finite",
    "primes",
    "divisors",
}

DEFER_TAGS = {
    "open_problem_index",
    "problem_list_collection",
    "research_problem",
    "source_detail_page_required",
    "open_core",
}

ELEMENTARY_TEXT_SIGNALS = {
    "finite",
    "graph",
    "vertex",
    "edge",
    "tree",
    "cycle",
    "coloring",
    "integer",
    "prime",
    "divisor",
    "sequence",
    "polynomial",
    "sum",
    "set",
    "matrix",
    "lattice",
    "tiling",
}

FAMOUS_HARD_SIGNALS = {
    "abc conjecture",
    "beal conjecture",
    "birch",
    "collatz",
    "goldbach",
    "hodge",
    "jacobian conjecture",
    "millennium",
    "navier",
    "odd perfect",
    "p vs np",
    "perfect cuboid",
    "riemann",
    "twin prime",
    "yang-mills",
}

SOURCE_FILE_BONUS = {
    "ErdosProblems": 16,
    "OEIS": 16,
    "GreensOpenProblems": 10,
    "Books": 8,
    "Other": 4,
    "Arxiv": -8,
    "Kourovka": -10,
    "OpenQuantumProblems": -35,
    "Millenium": -60,
    "OptimizationConstants": -8,
}

AMS_DOMAIN_PREFIXES = {
    "03": "logic",
    "05": "combinatorics",
    "06": "order_lattice",
    "11": "number_theory",
    "12": "algebra",
    "13": "algebra",
    "14": "algebraic_geometry",
    "15": "linear_algebra",
    "16": "algebra",
    "18": "category_theory",
    "20": "group_theory",
    "26": "real_analysis",
    "28": "measure_theory",
    "30": "complex_analysis",
    "34": "ordinary_differential_equations",
    "35": "partial_differential_equations",
    "37": "dynamical_systems",
    "40": "analysis",
    "46": "functional_analysis",
    "51": "geometry",
    "52": "convex_geometry",
    "53": "geometry",
    "54": "topology",
    "55": "topology",
    "57": "topology",
    "60": "probability",
    "62": "statistics",
    "68": "computer_science",
    "81": "mathematical_physics",
    "90": "optimization",
}

SEMANTIC_DOMAIN_PATTERNS = [
    ("graph_theory", ("simplegraph", "graph.", "adj ", "edge", "vertex", "chromatic", "clique", "matching")),
    ("elementary_number_theory", ("nat.prime", "prime", "zmod", "padic", "modEq".lower(), "dvd", "divisor", "factorial")),
    ("finite_combinatorics", ("finset", "fintype", "list", "multiset", "card", "coloring", "subset", "partition")),
    ("algebra", ("monoid", "group", "ring", "field", "ideal", "submodule", "algebra", "linear_map")),
    ("linear_algebra", ("matrix", "linearindependent", "basis", "det", "rank", "module")),
    ("order_lattice", ("lattice", "order", "sup", "inf", "complete_lattice", "set.i")),
    ("topology", ("topological", "continuous", "compact", "closed", "filter", "tendsto")),
    ("real_analysis", ("ereal", "ennreal", "real", "sqrt", "deriv", "integral", "measure")),
    ("probability", ("probability", "measure", "random", "bernoulli", "independent")),
    ("geometry", ("euclidean", "affine", "convex", "sphere", "triangle", "angle")),
    ("set_theory", ("ordinal", "cardinal", "set.", "powerset")),
]


@dataclass(frozen=True)
class Bank:
    name: str
    path: Path
    category: str
    registered_count: int


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_registry(path: Path) -> list[Bank]:
    banks = []
    for item in read_yaml(path) or []:
        banks.append(
            Bank(
                name=str(item.get("name", "")),
                path=Path(str(item.get("path", ""))),
                category=str(item.get("category", "")),
                registered_count=int(item.get("problem_count") or 0),
            )
        )
    return banks


def load_bank_records(bank: Bank) -> list[dict[str, Any]]:
    data = read_yaml(bank.path)
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ("problems", "items", "entries", "candidates"):
            items = data.get(key)
            if isinstance(items, list):
                return [item for item in items if isinstance(item, dict)]
    return []


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def source_dir(record: dict[str, Any]) -> str:
    source_file = str((record.get("metadata") or {}).get("source_file") or "")
    parts = source_file.split("/")
    if len(parts) > 1 and parts[0] in {"FormalConjectures", "FormalConjecturesForMathlib"}:
        return parts[1]
    return ""


def statement_quality(record: dict[str, Any]) -> str:
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    return str(metadata.get("statement_quality") or record.get("statement_quality") or "")


def text_blob(record: dict[str, Any]) -> str:
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    tags = " ".join(str(tag) for tag in record.get("tags", []) or [])
    refs = " ".join(str(ref) for ref in record.get("references", []) or [])
    return clean_text(
        " ".join(
            [
                str(record.get("problem_id", "")),
                str(record.get("title", "")),
                str(record.get("statement", "")),
                str(record.get("domain", "")),
                str(record.get("source", "")),
                str(metadata.get("source_file", "")),
                str(metadata.get("declaration_name", "")),
                tags,
                refs,
            ]
        )
    ).lower()


def semantic_domain(record: dict[str, Any], bank: Bank) -> str:
    domain = str(record.get("domain") or "")
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    blob = text_blob(record)

    if domain and domain != "research_mathematics":
        return domain

    ams_codes = metadata.get("ams_codes")
    if isinstance(ams_codes, list):
        for code in ams_codes:
            prefix = str(code).strip()[:2]
            if prefix in AMS_DOMAIN_PREFIXES:
                return AMS_DOMAIN_PREFIXES[prefix]

    for inferred, signals in SEMANTIC_DOMAIN_PATTERNS:
        if any(signal in blob for signal in signals):
            return inferred

    if bank.name.startswith("erdos"):
        tags = {str(tag).lower() for tag in record.get("tags", []) or []}
        if "graph theory" in tags:
            return "graph_theory"
        if "number theory" in tags:
            return "number_theory"
        if "combinatorics" in tags or "additive combinatorics" in tags:
            return "combinatorics"

    return domain or "unknown"


def preview(text: Any, limit: int = 220) -> str:
    compact = clean_text(text)
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def fit_level(score: int) -> str:
    if score >= 18:
        return "high"
    if score >= 8:
        return "medium"
    return "low"


def suitability_tier(score: int) -> str:
    if score >= 85:
        return "A_lean_first"
    if score >= 70:
        return "B_good_lean_candidate"
    if score >= 55:
        return "C_nl_then_lean"
    if score >= 35:
        return "D_statement_or_domain_review"
    return "E_defer_not_lean_first"


def binary_bucket(score: int, tier: str) -> str:
    if tier in {"A_lean_first", "B_good_lean_candidate", "C_nl_then_lean"}:
        return "workable_first_pass"
    return "defer_first_pass"


def classify(record: dict[str, Any], bank: Bank) -> dict[str, Any]:
    score = 0
    mathlib_score = 0
    nl_score = 0
    reasons: list[str] = []
    domain = str(record.get("domain") or "")
    inferred_domain = semantic_domain(record, bank)
    tags = {str(tag) for tag in record.get("tags", []) or []}
    formalized = str(record.get("formalized", ""))
    quality = statement_quality(record)
    metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    status = str(metadata.get("status") or "")
    category = str(metadata.get("category") or "")
    open_problem = bool(record.get("open_problem"))
    blob = text_blob(record)

    if formalized == "lean4_statement":
        score += 32
        mathlib_score += 18
        reasons.append("has_lean4_statement")
    elif formalized in {"yes", "yes_external"}:
        score += 22
        mathlib_score += 12
        reasons.append("already_formalized_or_external")
    elif formalized in {"partial", "partial_external"}:
        score += 18
        mathlib_score += 10
        reasons.append("partial_formalization")

    if quality in {"formal_lean4", "formal_statement"}:
        score += 26
        mathlib_score += 16
        reasons.append(f"statement_quality_{quality}")
    elif quality == "index_snippet":
        score -= 16
        reasons.append("statement_is_index_snippet")
    elif quality == "placeholder":
        score -= 28
        reasons.append("statement_placeholder")

    if inferred_domain in MATHLIB_RICH_SEMANTIC_DOMAINS:
        score += 14
        mathlib_score += 14
        reasons.append(f"mathlib_rich_domain_{inferred_domain}")
    elif inferred_domain in LLM_FRIENDLY_SEMANTIC_DOMAINS:
        score += 10
        nl_score += 12
        reasons.append(f"llm_friendly_domain_{inferred_domain}")
    elif inferred_domain in LOW_LEAN_FIRST_DOMAINS:
        score -= 18
        mathlib_score -= 8
        reasons.append(f"low_lean_first_domain_{inferred_domain}")

    if inferred_domain in LLM_FRIENDLY_SEMANTIC_DOMAINS:
        nl_score += 12
    if inferred_domain in {"graph_theory", "combinatorics", "number_theory", "finite_combinatorics", "elementary_number_theory"}:
        nl_score += 8

    high_tags = sorted(tags & HIGH_VALUE_TAGS)
    if high_tags:
        score += min(22, 5 * len(high_tags))
        mathlib_score += min(14, 3 * len(high_tags))
        nl_score += min(10, 2 * len(high_tags))
        reasons.extend(f"tag_{tag}" for tag in high_tags[:6])

    defer_tags = sorted(tags & DEFER_TAGS)
    if defer_tags:
        score -= min(24, 8 * len(defer_tags))
        reasons.extend(f"defer_tag_{tag}" for tag in defer_tags[:4])

    if "computational_search" in tags:
        score += 8
        nl_score += 4
        reasons.append("computational_certificate_surface")

    if "finite_case" in tags or "finite" in blob:
        score += 10
        mathlib_score += 4
        nl_score += 6
        reasons.append("finite_case_signal")

    if open_problem:
        score -= 6
        reasons.append("open_problem_penalty")
    else:
        score += 8
        reasons.append("known_or_nonopen_bonus")

    if status == "solved":
        score += 12
        reasons.append("formal_conjectures_status_solved")
    elif status == "open":
        score -= 6
        reasons.append("formal_conjectures_status_open")

    if category == "textbook":
        score += 14
        nl_score += 6
        reasons.append("textbook_category")
    elif category == "test":
        score += 10
        reasons.append("test_category")
    elif category == "api":
        score += 4
        reasons.append("api_category")
    elif category == "research":
        score -= 4
        reasons.append("research_category")

    sd = source_dir(record)
    if sd:
        source_bonus = SOURCE_FILE_BONUS.get(sd, 0)
        score += source_bonus
        if source_bonus:
            reasons.append(f"source_dir_{sd}_{source_bonus:+d}")

    if bank.name == "aim_problem_lists":
        score -= 30
        reasons.append("aim_problem_list_source_inventory")
    elif bank.name == "unsolvedmath_index":
        score -= 14
        reasons.append("unsolvedmath_needs_detail_page")
    elif bank.name in {"curated_starters", "amicable_track", "unitary_perfect_track", "carmichael_track", "triangle_dissection_track"}:
        score += 12
        reasons.append("local_curated_track")
    elif bank.name == "ai_math_benchmark_2026":
        score += 14
        reasons.append("ai_math_benchmark_curated")

    elementary_hits = sorted(signal for signal in ELEMENTARY_TEXT_SIGNALS if signal in blob)
    if elementary_hits:
        score += min(12, 2 * len(elementary_hits))
        nl_score += min(14, 2 * len(elementary_hits))
        reasons.extend(f"elementary_signal_{hit}" for hit in elementary_hits[:5])

    hard_hits = sorted(signal for signal in FAMOUS_HARD_SIGNALS if signal in blob)
    if hard_hits:
        score -= min(45, 18 * len(hard_hits))
        reasons.extend(f"famous_hard_{hit.replace(' ', '_')}" for hit in hard_hits[:4])

    if len(clean_text(record.get("statement"))) < 50 and formalized != "lean4_statement":
        score -= 16
        reasons.append("short_or_missing_statement")

    score = max(0, min(100, score))
    mathlib_score = max(0, min(30, mathlib_score))
    nl_score = max(0, min(30, nl_score))
    tier = suitability_tier(score)

    problem_id = str(record.get("problem_id") or record.get("id") or record.get("title") or "")
    source = str(record.get("source") or bank.name)
    unique_key = f"{source}::{problem_id}"

    return {
        "unique_key": unique_key,
        "problem_id": problem_id,
        "title": clean_text(record.get("title")),
        "source": source,
        "bank": bank.name,
        "bank_category": bank.category,
        "domain": domain,
        "semantic_domain": inferred_domain,
        "open_problem": open_problem,
        "formalized": formalized,
        "statement_quality": quality,
        "metadata_status": status,
        "metadata_category": category,
        "score": score,
        "suitability_tier": tier,
        "binary_bucket": binary_bucket(score, tier),
        "mathlib_fit": fit_level(mathlib_score),
        "mathlib_score": mathlib_score,
        "llm_nl_fit": fit_level(nl_score),
        "llm_nl_score": nl_score,
        "reason_codes": reasons[:24],
        "statement_preview": preview(record.get("statement")),
        "references": record.get("references", []) or [],
        "source_file": metadata.get("source_file"),
        "declaration_name": metadata.get("declaration_name"),
    }


def best_unique(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["unique_key"]].append(row)
    best = []
    for key, candidates in grouped.items():
        candidates.sort(
            key=lambda row: (
                row["score"],
                row["mathlib_score"],
                row["llm_nl_score"],
                -len(str(row.get("statement_preview") or "")),
            ),
            reverse=True,
        )
        winner = dict(candidates[0])
        winner["duplicate_banks"] = sorted({row["bank"] for row in candidates})
        winner["duplicate_count"] = len(candidates)
        best.append(winner)
    best.sort(key=lambda row: (-row["score"], -row["mathlib_score"], row["unique_key"]))
    return best


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "score",
        "suitability_tier",
        "binary_bucket",
        "mathlib_fit",
        "llm_nl_fit",
        "problem_id",
        "title",
        "source",
        "bank",
        "domain",
        "semantic_domain",
        "open_problem",
        "formalized",
        "statement_quality",
        "reason_codes",
        "statement_preview",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            out = {field: row.get(field, "") for field in fields}
            out["reason_codes"] = ";".join(row.get("reason_codes") or [])
            writer.writerow(out)


def counter_by(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(Counter(str(row.get(field, "")) for row in rows).most_common())


def build_markdown(
    *,
    generated_at: str,
    banks: list[Bank],
    entry_rows: list[dict[str, Any]],
    unique_rows: list[dict[str, Any]],
    output_dir: Path,
) -> str:
    workable = [row for row in unique_rows if row["binary_bucket"] == "workable_first_pass"]
    defer = [row for row in unique_rows if row["binary_bucket"] == "defer_first_pass"]
    lines = [
        "# Lean Suitability Fast Screen",
        "",
        f"- Generated at: `{generated_at}`",
        f"- Registered banks scanned: {len(banks)}",
        f"- Bank entries scanned: {len(entry_rows)}",
        f"- Unique problems by source/problem_id: {len(unique_rows)}",
        f"- Workable first pass: {len(workable)}",
        f"- Defer first pass: {len(defer)}",
        "",
        "## Tier Counts",
        "",
    ]
    for tier, count in Counter(row["suitability_tier"] for row in unique_rows).most_common():
        lines.append(f"- `{tier}`: {count}")
    lines.extend(["", "## Binary Counts", ""])
    for bucket, count in Counter(row["binary_bucket"] for row in unique_rows).most_common():
        lines.append(f"- `{bucket}`: {count}")
    lines.extend(["", "## Workable Semantic Domains", ""])
    for domain, count in Counter(row["semantic_domain"] for row in workable).most_common(20):
        lines.append(f"- `{domain}`: {count}")
    lines.extend(["", "## Bank Coverage", ""])
    bank_entry_counts = Counter(row["bank"] for row in entry_rows)
    bank_unique_workable = Counter(row["bank"] for row in unique_rows if row["binary_bucket"] == "workable_first_pass")
    for bank in banks:
        lines.append(
            f"- `{bank.name}`: registered {bank.registered_count}, parsed {bank_entry_counts.get(bank.name, 0)}, "
            f"workable winners {bank_unique_workable.get(bank.name, 0)}"
        )
    lines.extend(["", "## Top Lean-First Candidates", ""])
    lines.append("| Rank | Score | Tier | Problem | Bank | Domain | Reason |")
    lines.append("| ---: | ---: | --- | --- | --- | --- | --- |")
    for idx, row in enumerate(unique_rows[:40], start=1):
        reason = ", ".join((row.get("reason_codes") or [])[:4])
        title = row["title"].replace("|", "\\|")
        lines.append(
            f"| {idx} | {row['score']} | `{row['suitability_tier']}` | `{row['problem_id']}` {title} | "
            f"`{row['bank']}` | `{row['semantic_domain']}` | {reason} |"
        )
    lines.extend(
        [
            "",
            "## Output Files",
            "",
            f"- `{output_dir / 'entries.jsonl'}`: all bank entries with labels",
            f"- `{output_dir / 'unique_best.jsonl'}`: deduplicated best label per source/problem_id",
            f"- `{output_dir / 'unique_best.csv'}`: spreadsheet-friendly deduplicated view",
            f"- `{output_dir / 'top_workable.json'}`: top workable candidates",
            f"- `{output_dir / 'counts.json'}`: machine-readable summary counts",
            "",
            "## Notes",
            "",
            "- This is a metadata screen, not a proof attempt.",
            "- `workable_first_pass` means suitable for a first Lean or natural-language-then-Lean pass.",
            "- `defer_first_pass` usually means missing statement detail, overly broad research target, or low Lean-first fit.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-name", default="")
    parser.add_argument("--top-k", type=int, default=300)
    args = parser.parse_args()

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_name = args.run_name or "lean-suitability-" + generated_at.replace(":", "").replace("+00:00", "Z")
    output_dir = args.output_root / run_name
    output_dir.mkdir(parents=True, exist_ok=True)

    banks = load_registry(args.registry)
    entry_rows: list[dict[str, Any]] = []
    bank_parse_counts: dict[str, int] = {}
    for bank in banks:
        records = load_bank_records(bank)
        bank_parse_counts[bank.name] = len(records)
        for record in records:
            entry_rows.append(classify(record, bank))

    unique_rows = best_unique(entry_rows)
    workable = [row for row in unique_rows if row["binary_bucket"] == "workable_first_pass"]
    top_workable = workable[: args.top_k]

    counts = {
        "schema_version": "amra.lean_suitability_screen.v1",
        "generated_at": generated_at,
        "registry": str(args.registry),
        "registered_bank_count": len(banks),
        "registered_problem_count_sum": sum(bank.registered_count for bank in banks),
        "parsed_entry_count": len(entry_rows),
        "unique_problem_count": len(unique_rows),
        "workable_first_pass_count": len(workable),
        "defer_first_pass_count": len(unique_rows) - len(workable),
        "bank_parse_counts": bank_parse_counts,
        "tier_counts": counter_by(unique_rows, "suitability_tier"),
        "binary_counts": counter_by(unique_rows, "binary_bucket"),
        "domain_counts": counter_by(unique_rows, "domain"),
        "semantic_domain_counts": counter_by(unique_rows, "semantic_domain"),
        "bank_counts": counter_by(unique_rows, "bank"),
        "workable_by_bank": dict(Counter(row["bank"] for row in workable).most_common()),
        "workable_by_domain": dict(Counter(row["domain"] for row in workable).most_common()),
        "workable_by_semantic_domain": dict(Counter(row["semantic_domain"] for row in workable).most_common()),
    }

    write_jsonl(output_dir / "entries.jsonl", entry_rows)
    write_jsonl(output_dir / "unique_best.jsonl", unique_rows)
    write_csv(output_dir / "unique_best.csv", unique_rows)
    (output_dir / "top_workable.json").write_text(
        json.dumps(top_workable, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "counts.json").write_text(
        json.dumps(counts, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "summary.md").write_text(
        build_markdown(
            generated_at=generated_at,
            banks=banks,
            entry_rows=entry_rows,
            unique_rows=unique_rows,
            output_dir=output_dir,
        ),
        encoding="utf-8",
    )

    latest = args.output_root / "latest"
    latest.mkdir(parents=True, exist_ok=True)
    for filename in ("counts.json", "summary.md", "top_workable.json", "unique_best.csv"):
        (latest / filename).write_text((output_dir / filename).read_text(encoding="utf-8"), encoding="utf-8")
    (latest / "run_path.txt").write_text(str(output_dir) + "\n", encoding="utf-8")

    print(json.dumps(counts, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
