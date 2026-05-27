#!/usr/bin/env python3
"""Build a conservative first-batch target list from Lean suitability labels."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = REPO_ROOT / "data" / "bank_registry.yaml"
DEFAULT_SCREENING_ROOT = REPO_ROOT / "artifacts" / "problem_screening"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "artifacts" / "target_shortlists"

MATURE_DOMAINS = {
    "number_theory",
    "elementary_number_theory",
    "graph_theory",
    "finite_combinatorics",
    "combinatorics",
    "linear_algebra",
    "algebra",
    "group_theory",
    "order_lattice",
    "set_theory",
}

LOW_PRIORITY_DOMAINS = {
    "algebraic_geometry",
    "arithmetic_geometry",
    "partial_differential_equations",
    "pdes",
    "mathematical_physics",
    "physics",
    "measure_theory",
    "functional_analysis",
}

SOURCE_DIR_BONUS = {
    "OEIS": 14,
    "Books": 12,
    "ErdosProblems": 8,
    "Wikipedia": 6,
    "Other": 4,
    "GreensOpenProblems": 2,
    "WrittenOnTheWallII": 1,
    "Paper": -6,
    "Arxiv": -10,
    "Mathoverflow": -12,
    "Kourovka": -16,
    "HilbertProblems": -22,
    "OpenQuantumProblems": -28,
    "Millenium": -40,
}

SOURCE_FILE_CAP = 4
DOMAIN_CAPS = {
    "number_theory": 32,
    "elementary_number_theory": 10,
    "graph_theory": 14,
    "finite_combinatorics": 12,
    "linear_algebra": 12,
    "algebra": 10,
    "group_theory": 8,
    "order_lattice": 8,
    "geometry": 8,
    "convex_geometry": 8,
    "topology": 6,
    "real_analysis": 6,
    "probability": 6,
    "set_theory": 5,
    "research_mathematics": 4,
}


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def load_records_by_key(registry: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for bank in read_yaml(registry) or []:
        bank_name = str(bank.get("name", ""))
        path = Path(str(bank.get("path", "")))
        data = read_yaml(path)
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = []
            for key in ("problems", "items", "entries", "candidates"):
                if isinstance(data.get(key), list):
                    items = data[key]
                    break
        else:
            items = []
        for item in items:
            if not isinstance(item, dict):
                continue
            problem_id = str(item.get("problem_id") or item.get("id") or item.get("title") or "")
            source = str(item.get("source") or bank_name)
            unique_key = f"{source}::{problem_id}"
            enriched = dict(item)
            enriched["_bank"] = bank_name
            records[unique_key] = enriched
    return records


def source_dir(source_file: str) -> str:
    parts = source_file.split("/")
    if len(parts) > 1 and parts[0] == "FormalConjectures":
        return parts[1]
    return parts[0] if parts else ""


def extract_lean_decl(statement: str) -> str:
    match = re.search(r"```lean\s*(.*?)```", statement, re.S)
    return clean_text(match.group(1) if match else statement)


def lean_complexity(lean_decl: str) -> dict[str, int]:
    return {
        "chars": len(lean_decl),
        "binders": lean_decl.count("(") + lean_decl.count("{") + lean_decl.count("["),
        "exists": lean_decl.count("∃"),
        "forall": lean_decl.count("∀"),
        "lets": len(re.findall(r"\bletI?\b", lean_decl)),
        "arrows": lean_decl.count("→") + lean_decl.count("↔"),
        "lines": max(1, lean_decl.count("\n") + 1),
    }


def score_candidate(row: dict[str, Any], full_record: dict[str, Any]) -> tuple[int, list[str], dict[str, int]]:
    statement = clean_text(full_record.get("statement") or row.get("statement_preview"))
    lean_decl = extract_lean_decl(statement)
    metrics = lean_complexity(lean_decl)
    category = str(row.get("metadata_category") or "")
    status = str(row.get("metadata_status") or "")
    domain = str(row.get("semantic_domain") or row.get("domain") or "")
    sf = str(row.get("source_file") or "")
    sd = source_dir(sf)
    open_problem = bool(row.get("open_problem"))

    score = int(row.get("score") or 0)
    reasons: list[str] = []

    if not open_problem:
        score += 28
        reasons.append("non_open_target")
    else:
        score -= 45
        reasons.append("open_problem_hold")

    if category == "test":
        score += 32
        reasons.append("formal_conjectures_test")
    elif category == "api":
        score += 28
        reasons.append("api_bridge_lemma")
    elif category == "textbook":
        score += 26
        reasons.append("textbook_or_standard")
    elif status == "solved":
        score += 20
        reasons.append("status_solved")
    elif status == "open":
        score -= 28
        reasons.append("status_open_hold")

    if domain in MATURE_DOMAINS:
        score += 16
        reasons.append(f"mature_mathlib_domain_{domain}")
    elif domain in LOW_PRIORITY_DOMAINS:
        score -= 18
        reasons.append(f"low_first_batch_domain_{domain}")

    source_bonus = SOURCE_DIR_BONUS.get(sd, 0)
    score += source_bonus
    if source_bonus:
        reasons.append(f"source_dir_{sd}_{source_bonus:+d}")

    if metrics["chars"] <= 120:
        score += 18
        reasons.append("short_lean_target")
    elif metrics["chars"] <= 240:
        score += 10
        reasons.append("moderate_lean_target")
    elif metrics["chars"] > 700:
        score -= 20
        reasons.append("long_lean_target")
    elif metrics["chars"] > 450:
        score -= 10
        reasons.append("large_lean_target")

    if metrics["binders"] <= 3:
        score += 10
        reasons.append("few_binders")
    elif metrics["binders"] >= 10:
        score -= 10
        reasons.append("many_binders")

    lower_decl = lean_decl.lower()
    if "answer(sorry)" in lower_decl or "answer (sorry)" in lower_decl:
        score -= 120
        reasons.append("contains_answer_sorry_placeholder")
    if "sorry" in lower_decl:
        score -= 80
        reasons.append("contains_sorry_token")
    if "set.infinite" in lower_decl or "∀ᶠ" in lean_decl or "atTop" in lean_decl:
        score -= 18
        reasons.append("asymptotic_or_infinite_surface")
    if "simplegraph" in lower_decl or "finset" in lower_decl or "fintype" in lower_decl:
        score += 8
        reasons.append("finite_discrete_surface")
    if "native_decide" in lower_decl or "decide" in lower_decl:
        score += 8
        reasons.append("decidable_computation_surface")

    return score, reasons, metrics


def target_lane(row: dict[str, Any], batch_score: int, reasons: list[str]) -> str:
    if "contains_answer_sorry_placeholder" in reasons or "contains_sorry_token" in reasons:
        return "hold_placeholder_statement"
    if bool(row.get("open_problem")):
        return "hold_open_research"
    if batch_score >= 170:
        return "batch1_direct"
    if batch_score >= 145:
        return "batch1_backup"
    return "later_review"


def balanced_take(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    chosen: list[dict[str, Any]] = []
    by_source_file: Counter[str] = Counter()
    by_domain: Counter[str] = Counter()
    for row in rows:
        domain = str(row.get("semantic_domain") or row.get("domain") or "")
        sf = str(row.get("source_file") or row.get("problem_id"))
        domain_cap = DOMAIN_CAPS.get(domain, 5)
        if by_source_file[sf] >= SOURCE_FILE_CAP:
            continue
        if by_domain[domain] >= domain_cap:
            continue
        chosen.append(row)
        by_source_file[sf] += 1
        by_domain[domain] += 1
        if len(chosen) >= limit:
            break
    if len(chosen) >= limit:
        return chosen
    chosen_keys = {row["unique_key"] for row in chosen}
    for row in rows:
        if row["unique_key"] in chosen_keys:
            continue
        sf = str(row.get("source_file") or row.get("problem_id"))
        if by_source_file[sf] >= SOURCE_FILE_CAP:
            continue
        chosen.append(row)
        by_source_file[sf] += 1
        if len(chosen) >= limit:
            break
    return chosen


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "batch_rank",
        "batch_score",
        "target_lane",
        "problem_id",
        "title",
        "semantic_domain",
        "metadata_category",
        "metadata_status",
        "source_file",
        "declaration_name",
        "complexity_chars",
        "complexity_binders",
        "first_batch_reasons",
        "statement_preview",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for idx, row in enumerate(rows, start=1):
            out = {field: row.get(field, "") for field in fields}
            out["batch_rank"] = idx
            out["first_batch_reasons"] = ";".join(row.get("first_batch_reasons") or [])
            writer.writerow(out)


def markdown_summary(output_dir: Path, candidates: list[dict[str, Any]], batch: list[dict[str, Any]], counts: dict[str, Any]) -> str:
    lines = [
        "# First Batch Lean Targets",
        "",
        f"- Generated at: `{counts['generated_at']}`",
        f"- Input workable problems: {counts['input_workable_count']}",
        f"- Direct pool: {counts['lane_counts'].get('batch1_direct', 0)}",
        f"- Backup pool: {counts['lane_counts'].get('batch1_backup', 0)}",
        f"- Balanced first batch: {len(batch)}",
        f"- Substantive first batch, excluding test-only targets: {counts['substantive_batch_size']}",
        "",
        "## Batch Domain Mix",
        "",
    ]
    for domain, count in Counter(str(row.get("semantic_domain")) for row in batch).most_common():
        lines.append(f"- `{domain}`: {count}")
    lines.extend(["", "## First 60 Targets", ""])
    lines.append("| Rank | Score | Lane | Problem | Domain | Category | Source |")
    lines.append("| ---: | ---: | --- | --- | --- | --- | --- |")
    for idx, row in enumerate(batch[:60], start=1):
        title = str(row.get("title") or "").replace("|", "\\|")
        lines.append(
            f"| {idx} | {row['batch_score']} | `{row['target_lane']}` | `{row['problem_id']}` {title} | "
            f"`{row.get('semantic_domain')}` | `{row.get('metadata_category') or row.get('metadata_status')}` | "
            f"`{row.get('source_file') or ''}` |"
        )
    lines.extend(
        [
            "",
            "## Files",
            "",
            f"- `{output_dir / 'batch1_targets.csv'}`: balanced first-batch spreadsheet",
            f"- `{output_dir / 'batch1_targets.json'}`: balanced first-batch machine-readable list",
            f"- `{output_dir / 'batch1_substantive_targets.csv'}`: balanced first-batch list excluding `test` targets",
            f"- `{output_dir / 'batch1_substantive_targets.json'}`: machine-readable substantive list",
            f"- `{output_dir / 'direct_pool.json'}`: all direct-pool targets before balancing",
            f"- `{output_dir / 'scored_candidates.jsonl'}`: all 2530 workable entries rescored",
            f"- `{output_dir / 'counts.json'}`: summary counts",
            "",
            "## Notes",
            "",
            "- This is a shallow target screen, not an attempted proof.",
            "- Open research statements and `answer(sorry)` placeholder contracts are deliberately held out of batch 1.",
            "- The balanced list caps repeated source files so one OEIS/Erdos file cannot dominate the first run.",
            "- Use the substantive list when the goal is real proof work rather than smoke-testing the harness.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screening-run", type=Path, default=None)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--run-name", default="")
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()

    screening_run = args.screening_run
    if screening_run is None:
        screening_run = Path((DEFAULT_SCREENING_ROOT / "latest" / "run_path.txt").read_text(encoding="utf-8").strip())

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_name = args.run_name or "first-batch-targets-" + generated_at.replace(":", "").replace("+00:00", "Z")
    output_dir = args.output_root / run_name
    output_dir.mkdir(parents=True, exist_ok=True)

    records = load_records_by_key(args.registry)
    rows = [json.loads(line) for line in (screening_run / "unique_best.jsonl").read_text(encoding="utf-8").splitlines()]
    workable = [row for row in rows if row.get("binary_bucket") == "workable_first_pass"]

    scored: list[dict[str, Any]] = []
    for row in workable:
        full_record = records.get(row["unique_key"], {})
        batch_score, reasons, metrics = score_candidate(row, full_record)
        lane = target_lane(row, batch_score, reasons)
        enriched = dict(row)
        enriched["batch_score"] = batch_score
        enriched["target_lane"] = lane
        enriched["first_batch_reasons"] = reasons
        enriched["complexity_chars"] = metrics["chars"]
        enriched["complexity_binders"] = metrics["binders"]
        enriched["complexity_exists"] = metrics["exists"]
        enriched["complexity_forall"] = metrics["forall"]
        enriched["complexity_arrows"] = metrics["arrows"]
        enriched["full_statement"] = full_record.get("statement") or row.get("statement_preview")
        scored.append(enriched)

    scored.sort(
        key=lambda row: (
            row["target_lane"] != "batch1_direct",
            -int(row["batch_score"]),
            int(row.get("complexity_chars") or 0),
            str(row.get("source_file") or ""),
            str(row.get("problem_id") or ""),
        )
    )
    direct_pool = [row for row in scored if row["target_lane"] == "batch1_direct"]
    backup_pool = [row for row in scored if row["target_lane"] == "batch1_backup"]
    batch = balanced_take(direct_pool + backup_pool, args.batch_size)
    for idx, row in enumerate(batch, start=1):
        row["batch_rank"] = idx
    substantive_pool = [
        row
        for row in direct_pool + backup_pool
        if row.get("metadata_category") != "test"
        and not str(row.get("source_file") or "").startswith("FormalConjectures/Util/")
    ]
    substantive_batch = balanced_take(substantive_pool, args.batch_size)
    for idx, row in enumerate(substantive_batch, start=1):
        row["batch_rank"] = idx

    counts = {
        "schema_version": "amra.first_batch_targets.v1",
        "generated_at": generated_at,
        "screening_run": str(screening_run),
        "input_workable_count": len(workable),
        "scored_candidate_count": len(scored),
        "batch_size": len(batch),
        "substantive_pool_count": len(substantive_pool),
        "substantive_batch_size": len(substantive_batch),
        "lane_counts": dict(Counter(row["target_lane"] for row in scored).most_common()),
        "batch_domain_counts": dict(Counter(str(row.get("semantic_domain")) for row in batch).most_common()),
        "batch_category_counts": dict(Counter(str(row.get("metadata_category") or row.get("metadata_status")) for row in batch).most_common()),
        "batch_source_dir_counts": dict(Counter(source_dir(str(row.get("source_file") or "")) for row in batch).most_common()),
        "substantive_batch_domain_counts": dict(
            Counter(str(row.get("semantic_domain")) for row in substantive_batch).most_common()
        ),
        "substantive_batch_category_counts": dict(
            Counter(str(row.get("metadata_category") or row.get("metadata_status")) for row in substantive_batch).most_common()
        ),
    }

    with (output_dir / "scored_candidates.jsonl").open("w", encoding="utf-8") as handle:
        for row in scored:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    write_json(output_dir / "direct_pool.json", direct_pool)
    write_json(output_dir / "batch1_targets.json", batch)
    write_json(output_dir / "batch1_substantive_targets.json", substantive_batch)
    write_csv(output_dir / "batch1_targets.csv", batch)
    write_csv(output_dir / "batch1_substantive_targets.csv", substantive_batch)
    write_json(output_dir / "counts.json", counts)
    (output_dir / "summary.md").write_text(markdown_summary(output_dir, scored, batch, counts), encoding="utf-8")

    latest = args.output_root / "latest"
    latest.mkdir(parents=True, exist_ok=True)
    for filename in (
        "summary.md",
        "counts.json",
        "batch1_targets.csv",
        "batch1_targets.json",
        "batch1_substantive_targets.csv",
        "batch1_substantive_targets.json",
        "direct_pool.json",
    ):
        (latest / filename).write_text((output_dir / filename).read_text(encoding="utf-8"), encoding="utf-8")
    (latest / "run_path.txt").write_text(str(output_dir) + "\n", encoding="utf-8")

    print(json.dumps(counts, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
