#!/usr/bin/env python3
"""Open-problem-only screen for AMRA problem banks.

This pass deliberately excludes solved/textbook/api/test-style targets and
keeps only records marked as open research problems.  It then ranks the open
set by statement readiness, mathlib/domain fit, and likely first-pass
formalization tractability.
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
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "artifacts" / "open_problem_screening"

FORMAL_READY_BANKS = {"formal_conjectures_open_research", "formal_conjectures_all"}
STATEMENT_RECOVERY_BANKS = {"unsolvedmath_index", "aim_problem_lists", "erdos_open_637", "erdos_full_1120"}

MATHLIB_RICH_DOMAINS = {
    "number_theory",
    "elementary_number_theory",
    "graph_theory",
    "finite_combinatorics",
    "combinatorics",
    "algebra",
    "group_theory",
    "linear_algebra",
    "order_lattice",
    "set_theory",
    "logic",
}

LLM_FRIENDLY_DOMAINS = {
    "number_theory",
    "elementary_number_theory",
    "graph_theory",
    "finite_combinatorics",
    "combinatorics",
    "geometry",
    "convex_geometry",
    "ramsey_theory",
}

LOW_FIRST_PASS_DOMAINS = {
    "algebraic_geometry",
    "arithmetic_geometry",
    "partial_differential_equations",
    "pdes",
    "mathematical_physics",
    "physics",
    "biology",
    "representation_theory",
    "functional_analysis",
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
    "35": "partial_differential_equations",
    "37": "dynamical_systems",
    "46": "functional_analysis",
    "51": "geometry",
    "52": "convex_geometry",
    "54": "topology",
    "55": "topology",
    "57": "topology",
    "60": "probability",
    "68": "computer_science",
    "81": "mathematical_physics",
    "90": "optimization",
}

SEMANTIC_DOMAIN_PATTERNS = [
    ("graph_theory", ("simplegraph", "graph.", "adj ", "edge", "vertex", "chromatic", "clique", "matching")),
    ("elementary_number_theory", ("nat.prime", "prime", "zmod", "modEq".lower(), "dvd", "divisor", "factorial")),
    ("finite_combinatorics", ("finset", "fintype", "list", "multiset", "card", "coloring", "subset", "partition")),
    ("algebra", ("monoid", "group", "ring", "field", "ideal", "submodule", "algebra", "polynomial")),
    ("linear_algebra", ("matrix", "linearindependent", "basis", "det", "rank", "module")),
    ("order_lattice", ("lattice", "order", "sup", "inf", "complete_lattice", "set.i")),
    ("topology", ("topological", "continuous", "compact", "closed", "filter", "tendsto")),
    ("real_analysis", ("ereal", "ennreal", "real", "sqrt", "deriv", "integral", "measure")),
    ("probability", ("probability", "measure", "random", "bernoulli", "independent")),
    ("geometry", ("euclidean", "affine", "convex", "sphere", "triangle", "angle")),
    ("set_theory", ("ordinal", "cardinal", "set.", "powerset")),
]

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

HIGH_PROFILE_OPEN_IDENTIFIERS = {
    "abc.lean",
    "agohgiuga",
    "agrawal",
    "algebraicindependent_e_pi",
    "andrica",
    "artinprimitiveroots",
    "babai_seress",
    "balancedprimes",
    "batemanhorn",
    "bealconjecture",
    "bloch.lean",
    "brennanconjecture",
    "brocardconjecture",
    "buchi.lean",
    "bunyakovsky",
    "boundedburnside",
    "carmichaeltotient",
    "casasalvero",
    "classnumberproblem",
    "collatz",
    "determinantalconjecture",
    "eulerbrick",
    "exponentials.lean",
    "fermat.lean",
    "goldbach",
    "gottschalk",
    "hadamard.lean",
    "hodge",
    "invariantsubspaceproblem",
    "inversegalois",
    "irrational.lean",
    "kakeya",
    "kaplansky",
    "leinster",
    "mandelbrot",
    "perfectcuboid",
    "riemann",
    "sendov",
    "twinprime",
}


@dataclass(frozen=True)
class Bank:
    name: str
    path: Path
    category: str
    registered_count: int


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_registry(path: Path) -> list[Bank]:
    banks: list[Bank] = []
    for item in read_yaml(path) or []:
        banks.append(
            Bank(
                name=str(item.get("name") or ""),
                path=Path(str(item.get("path") or "")),
                category=str(item.get("category") or ""),
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


def metadata(record: dict[str, Any]) -> dict[str, Any]:
    return record.get("metadata") if isinstance(record.get("metadata"), dict) else {}


def status(record: dict[str, Any]) -> str:
    md = metadata(record)
    return str(md.get("status") or md.get("status_state") or "").lower()


def statement_quality(record: dict[str, Any]) -> str:
    md = metadata(record)
    return str(md.get("statement_quality") or record.get("statement_quality") or "")


def is_open_record(record: dict[str, Any]) -> bool:
    st = status(record)
    if st in {"solved", "closed", "disproved", "false", "resolved"}:
        return False
    return bool(record.get("open_problem")) or st == "open"


def text_blob(record: dict[str, Any]) -> str:
    md = metadata(record)
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
                str(md.get("source_file", "")),
                str(md.get("declaration_name", "")),
                tags,
                refs,
            ]
        )
    ).lower()


def semantic_domain(record: dict[str, Any]) -> str:
    domain = str(record.get("domain") or "")
    if domain and domain != "research_mathematics":
        return domain
    md = metadata(record)
    ams_codes = md.get("ams_codes")
    if isinstance(ams_codes, list):
        for code in ams_codes:
            inferred = AMS_DOMAIN_PREFIXES.get(str(code).strip()[:2])
            if inferred:
                return inferred
    blob = text_blob(record)
    for inferred, signals in SEMANTIC_DOMAIN_PATTERNS:
        if any(signal in blob for signal in signals):
            return inferred
    return domain or "unknown"


def source_dir(record: dict[str, Any]) -> str:
    sf = str(metadata(record).get("source_file") or "")
    parts = sf.split("/")
    if len(parts) > 1 and parts[0] == "FormalConjectures":
        return parts[1]
    return parts[0] if parts else ""


def preview(value: Any, limit: int = 260) -> str:
    text = clean_text(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def source_problem_key(record: dict[str, Any], bank: Bank) -> str:
    problem_id = str(record.get("problem_id") or record.get("id") or record.get("title") or "")
    source = str(record.get("source") or bank.name)
    return f"{source}::{problem_id}"


def score_open_candidate(record: dict[str, Any], bank: Bank) -> tuple[int, str, list[str]]:
    score = 0
    reasons: list[str] = []
    quality = statement_quality(record)
    formalized = str(record.get("formalized") or "")
    category = str(metadata(record).get("category") or "")
    domain = semantic_domain(record)
    blob = text_blob(record)
    stmt = clean_text(record.get("statement"))

    if bank.name in FORMAL_READY_BANKS and formalized == "lean4_statement":
        score += 42
        reasons.append("has_formal_lean4_statement")
    elif formalized in {"yes", "yes_external", "partial", "partial_external"}:
        score += 16
        reasons.append("has_some_formalization_metadata")

    if quality == "formal_lean4":
        score += 38
        reasons.append("formal_statement_ready")
    elif quality == "curated":
        score += 22
        reasons.append("curated_statement")
    elif quality == "index_snippet":
        score += 4
        reasons.append("index_snippet_needs_detail_page")
    elif quality == "placeholder":
        score -= 22
        reasons.append("placeholder_statement")
    elif quality == "problem_list_pointer":
        score -= 35
        reasons.append("problem_list_pointer")

    if domain in MATHLIB_RICH_DOMAINS:
        score += 18
        reasons.append(f"mathlib_rich_domain_{domain}")
    elif domain in LLM_FRIENDLY_DOMAINS:
        score += 12
        reasons.append(f"llm_friendly_domain_{domain}")
    elif domain in LOW_FIRST_PASS_DOMAINS:
        score -= 18
        reasons.append(f"low_first_pass_domain_{domain}")

    if bank.name == "formal_conjectures_open_research":
        score += 22
        reasons.append("formal_conjectures_open_research_bank")
    elif bank.name in {"curated_starters", "amicable_track", "unitary_perfect_track", "carmichael_track", "triangle_dissection_track"}:
        score += 18
        reasons.append("local_curated_open_track")
    elif bank.name == "unsolvedmath_index":
        score -= 8
        reasons.append("unsolvedmath_requires_source_recovery")
    elif bank.name == "aim_problem_lists":
        score -= 32
        reasons.append("aim_list_requires_problem_extraction")
    elif bank.name.startswith("erdos"):
        score -= 10
        reasons.append("erdos_import_placeholder")

    sd = source_dir(record)
    if sd in {"ErdosProblems", "OEIS", "Wikipedia", "GreensOpenProblems", "WrittenOnTheWallII"}:
        score += 8
        reasons.append(f"tractable_source_family_{sd}")
    elif sd in {"Millenium", "HilbertProblems", "OpenQuantumProblems", "Kourovka"}:
        score -= 24
        reasons.append(f"hard_source_family_{sd}")

    if "answer(sorry)" in blob or "answer (sorry)" in blob:
        score -= 28
        reasons.append("formal_contract_has_answer_sorry_placeholder")
    elif "sorry" in blob:
        score -= 16
        reasons.append("formal_contract_mentions_sorry")

    if "set.infinite" in blob or "infinitely many" in blob or "∀ᶠ" in stmt or "attop" in blob:
        score -= 12
        reasons.append("infinite_or_asymptotic_surface")

    if any(signal in blob for signal in ("finite", "finset", "fintype", "simplegraph", "matrix", "zmod", "nat.prime")):
        score += 12
        reasons.append("discrete_formal_surface")

    hard_hits = sorted(signal for signal in FAMOUS_HARD_SIGNALS if signal in blob)
    if hard_hits:
        score -= min(55, 22 * len(hard_hits))
        reasons.extend(f"famous_hard_{hit.replace(' ', '_')}" for hit in hard_hits[:3])

    high_profile_hits = sorted(signal for signal in HIGH_PROFILE_OPEN_IDENTIFIERS if signal in blob)
    if high_profile_hits:
        score -= 45
        reasons.extend(f"high_profile_open_{hit.replace('.', '_')}" for hit in high_profile_hits[:3])

    if len(stmt) < 50:
        score -= 18
        reasons.append("short_statement")
    elif len(stmt) <= 260:
        score += 5
        reasons.append("compact_statement")
    elif len(stmt) > 1200:
        score -= 10
        reasons.append("long_statement")

    if category and category != "research":
        score -= 60
        reasons.append(f"non_research_category_{category}")

    score = max(0, min(100, score))
    if any(reason.startswith("formal_contract_has_answer_sorry") for reason in reasons):
        score = min(score, 58)
    if any(reason.startswith("high_profile_open_") or reason.startswith("famous_hard_") for reason in reasons):
        score = min(score, 55)
    if str(metadata(record).get("source_file") or "").startswith("FormalConjectures/Util/"):
        score = min(score, 35)
        reasons.append("formal_conjectures_util_file")
    if score >= 75 and quality == "formal_lean4":
        tier = "A_open_formal_ready"
    elif score >= 60:
        tier = "B_open_promising"
    elif score >= 40:
        tier = "C_open_needs_statement_or_domain_work"
    else:
        tier = "D_open_defer"
    return score, tier, reasons


def row_for(record: dict[str, Any], bank: Bank) -> dict[str, Any]:
    md = metadata(record)
    score, tier, reasons = score_open_candidate(record, bank)
    problem_id = str(record.get("problem_id") or record.get("id") or record.get("title") or "")
    source = str(record.get("source") or bank.name)
    return {
        "unique_key": source_problem_key(record, bank),
        "problem_id": problem_id,
        "title": clean_text(record.get("title")),
        "source": source,
        "bank": bank.name,
        "bank_category": bank.category,
        "domain": str(record.get("domain") or ""),
        "semantic_domain": semantic_domain(record),
        "formalized": str(record.get("formalized") or ""),
        "statement_quality": statement_quality(record),
        "metadata_status": status(record),
        "metadata_category": str(md.get("category") or ""),
        "open_problem": bool(record.get("open_problem")),
        "open_research_score": score,
        "open_research_tier": tier,
        "reason_codes": reasons[:28],
        "statement_preview": preview(record.get("statement")),
        "source_file": md.get("source_file"),
        "declaration_name": md.get("declaration_name"),
        "references": record.get("references", []) or [],
    }


def best_unique(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["unique_key"]].append(row)
    out: list[dict[str, Any]] = []
    for candidates in grouped.values():
        candidates.sort(
            key=lambda row: (
                row["open_research_score"],
                row["statement_quality"] == "formal_lean4",
                row["bank"] == "formal_conjectures_open_research",
                row["formalized"] == "lean4_statement",
            ),
            reverse=True,
        )
        winner = dict(candidates[0])
        winner["duplicate_banks"] = sorted({row["bank"] for row in candidates})
        winner["duplicate_count"] = len(candidates)
        out.append(winner)
    out.sort(key=lambda row: (-row["open_research_score"], row["unique_key"]))
    return out


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "open_research_score",
        "open_research_tier",
        "problem_id",
        "title",
        "source",
        "bank",
        "semantic_domain",
        "formalized",
        "statement_quality",
        "metadata_status",
        "metadata_category",
        "source_file",
        "declaration_name",
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


def balanced_first_batch(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    def eligible(row: dict[str, Any]) -> bool:
        reasons = row.get("reason_codes") or []
        if row["open_research_tier"] not in {"A_open_formal_ready", "B_open_promising"}:
            return False
        if any(reason.startswith("formal_contract_has_answer_sorry") for reason in reasons):
            return False
        if any(reason.startswith("high_profile_open_") or reason.startswith("famous_hard_") for reason in reasons):
            return False
        if str(row.get("source_file") or "").startswith("FormalConjectures/Util/"):
            return False
        if row.get("metadata_category") and row.get("metadata_category") != "research":
            return False
        return True

    eligible_rows = [row for row in rows if eligible(row)]
    source_file_counts: Counter[str] = Counter()
    domain_counts: Counter[str] = Counter()
    chosen: list[dict[str, Any]] = []
    for row in eligible_rows:
        sf = str(row.get("source_file") or row.get("unique_key"))
        domain = str(row.get("semantic_domain") or "")
        if source_file_counts[sf] >= 3:
            continue
        if domain_counts[domain] >= 18:
            continue
        chosen.append(row)
        source_file_counts[sf] += 1
        domain_counts[domain] += 1
        if len(chosen) >= limit:
            break
    return chosen


def markdown_summary(output_dir: Path, banks: list[Bank], raw_rows: list[dict[str, Any]], unique_rows: list[dict[str, Any]], batch: list[dict[str, Any]], generated_at: str) -> str:
    lines = [
        "# Open Research Problem Screen",
        "",
        f"- Generated at: `{generated_at}`",
        f"- Registered banks scanned: {len(banks)}",
        f"- Raw open records: {len(raw_rows)}",
        f"- Unique open problems: {len(unique_rows)}",
        f"- First open batch: {len(batch)}",
        "",
        "## Tier Counts",
        "",
    ]
    for tier, count in Counter(row["open_research_tier"] for row in unique_rows).most_common():
        lines.append(f"- `{tier}`: {count}")
    lines.extend(["", "## Open Problems By Bank", ""])
    for bank, count in Counter(row["bank"] for row in unique_rows).most_common():
        lines.append(f"- `{bank}`: {count}")
    lines.extend(["", "## Statement Readiness", ""])
    for quality, count in Counter(row["statement_quality"] for row in unique_rows).most_common():
        lines.append(f"- `{quality}`: {count}")
    lines.extend(["", "## First Batch Domains", ""])
    for domain, count in Counter(row["semantic_domain"] for row in batch).most_common():
        lines.append(f"- `{domain}`: {count}")
    lines.extend(["", "## Top Open Candidates", ""])
    lines.append("| Rank | Score | Tier | Problem | Domain | Bank | Source File |")
    lines.append("| ---: | ---: | --- | --- | --- | --- | --- |")
    for idx, row in enumerate(batch[:80], start=1):
        title = str(row["title"]).replace("|", "\\|")
        lines.append(
            f"| {idx} | {row['open_research_score']} | `{row['open_research_tier']}` | "
            f"`{row['problem_id']}` {title} | `{row['semantic_domain']}` | `{row['bank']}` | "
            f"`{row.get('source_file') or ''}` |"
        )
    lines.extend(
        [
            "",
            "## Files",
            "",
            f"- `{output_dir / 'open_unique.csv'}`: all deduplicated open problems",
            f"- `{output_dir / 'open_unique.jsonl'}`: machine-readable deduplicated open inventory",
            f"- `{output_dir / 'open_first_batch.csv'}`: first open-problem attack batch",
            f"- `{output_dir / 'open_first_batch.json'}`: machine-readable first batch",
            f"- `{output_dir / 'counts.json'}`: summary counts",
            "",
            "## Notes",
            "",
            "- Solved, disproved, textbook, api, and test-style records are excluded unless the record is explicitly marked open; non-research categories are strongly penalized and do not enter the first batch.",
            "- `A_open_formal_ready` means open and already expressed as a Lean 4 target, not that the theorem is easy.",
            "- Index-only sources such as UnsolvedMath and AIM are retained in the open inventory but ranked lower until exact statements are recovered.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-name", default="")
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_name = args.run_name or "open-problem-screen-" + generated_at.replace(":", "").replace("+00:00", "Z")
    output_dir = args.output_root / run_name
    output_dir.mkdir(parents=True, exist_ok=True)

    banks = load_registry(args.registry)
    raw_rows: list[dict[str, Any]] = []
    for bank in banks:
        for record in load_bank_records(bank):
            if is_open_record(record):
                raw_rows.append(row_for(record, bank))
    unique_rows = best_unique(raw_rows)
    batch = balanced_first_batch(unique_rows, args.batch_size)
    for idx, row in enumerate(batch, start=1):
        row["open_batch_rank"] = idx

    counts = {
        "schema_version": "amra.open_problem_screen.v1",
        "generated_at": generated_at,
        "registered_bank_count": len(banks),
        "registered_problem_count_sum": sum(bank.registered_count for bank in banks),
        "raw_open_record_count": len(raw_rows),
        "unique_open_problem_count": len(unique_rows),
        "first_batch_count": len(batch),
        "tier_counts": dict(Counter(row["open_research_tier"] for row in unique_rows).most_common()),
        "open_by_bank": dict(Counter(row["bank"] for row in unique_rows).most_common()),
        "open_by_statement_quality": dict(Counter(row["statement_quality"] for row in unique_rows).most_common()),
        "open_by_formalized": dict(Counter(row["formalized"] for row in unique_rows).most_common()),
        "open_by_semantic_domain": dict(Counter(row["semantic_domain"] for row in unique_rows).most_common()),
        "first_batch_by_semantic_domain": dict(Counter(row["semantic_domain"] for row in batch).most_common()),
        "first_batch_by_bank": dict(Counter(row["bank"] for row in batch).most_common()),
    }

    write_jsonl(output_dir / "open_raw.jsonl", raw_rows)
    write_jsonl(output_dir / "open_unique.jsonl", unique_rows)
    write_csv(output_dir / "open_unique.csv", unique_rows)
    write_csv(output_dir / "open_first_batch.csv", batch)
    (output_dir / "open_first_batch.json").write_text(
        json.dumps(batch, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "counts.json").write_text(
        json.dumps(counts, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "summary.md").write_text(
        markdown_summary(output_dir, banks, raw_rows, unique_rows, batch, generated_at),
        encoding="utf-8",
    )

    latest = args.output_root / "latest"
    latest.mkdir(parents=True, exist_ok=True)
    for filename in ("summary.md", "counts.json", "open_unique.csv", "open_first_batch.csv", "open_first_batch.json"):
        (latest / filename).write_text((output_dir / filename).read_text(encoding="utf-8"), encoding="utf-8")
    (latest / "run_path.txt").write_text(str(output_dir) + "\n", encoding="utf-8")

    print(json.dumps(counts, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
