#!/usr/bin/env python3
"""Aggregate parallel MathScout reports for open-problem fine screening."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


RECOMMENDATION_BONUS = {
    "promote": 25,
    "formalize_known": 8,
    "defer_route": -4,
    "defer_source": -10,
    "freeze": -25,
    "unknown": -8,
}

EFFORT_BONUS = {
    "trivial": 18,
    "small": 14,
    "medium": 6,
    "large": -8,
    "research_program": -25,
    "not_assessable": -12,
}

BLOCKER_BONUS = {
    "formalization": 16,
    "certificate": 12,
    "computation": 8,
    "key_lemma": 4,
    "exact_statement": -8,
    "source_provenance": -10,
    "open_core": -22,
    "unknown": -8,
}

PROOF_STATUS_BONUS = {
    "rigorous_partial": 15,
    "heuristic_route": 6,
    "known_theorem": 2,
    "no_statement": -12,
    "failed": -12,
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ease_score(entry: dict[str, Any]) -> float:
    parsed = entry.get("parsed_probe") or {}
    feasibility = float(parsed.get("feasibility_score") or 0.0)
    recommendation = str(parsed.get("recommendation") or "unknown")
    effort = str(parsed.get("estimated_proof_effort") or "not_assessable")
    blocker = str(parsed.get("primary_blocker") or "unknown")
    proof_status = str(parsed.get("proof_attempt_status") or "failed")
    backend_status = str((entry.get("backend_report") or {}).get("status") or "")
    score = feasibility * 10
    score += RECOMMENDATION_BONUS.get(recommendation, RECOMMENDATION_BONUS["unknown"])
    score += EFFORT_BONUS.get(effort, EFFORT_BONUS["not_assessable"])
    score += BLOCKER_BONUS.get(blocker, BLOCKER_BONUS["unknown"])
    score += PROOF_STATUS_BONUS.get(proof_status, PROOF_STATUS_BONUS["failed"])
    if backend_status != "completed":
        score -= 30
    return round(score, 2)


def load_entries(report_paths: list[Path]) -> tuple[list[dict[str, Any]], list[str]]:
    entries: list[dict[str, Any]] = []
    missing: list[str] = []
    for path in report_paths:
        if not path.exists():
            missing.append(str(path))
            continue
        report = read_json(path)
        chunk = path.stem.replace("_report", "")
        for entry in report.get("entries", []):
            row = dict(entry)
            row["chunk"] = chunk
            row["fine_screen_ease_score"] = ease_score(row)
            entries.append(row)
    entries.sort(
        key=lambda row: (
            -float(row.get("fine_screen_ease_score") or 0.0),
            -float((row.get("parsed_probe") or {}).get("feasibility_score") or 0.0),
            str(row.get("problem_id") or ""),
        )
    )
    return entries, missing


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "rank",
        "fine_screen_ease_score",
        "feasibility_score",
        "recommendation",
        "estimated_proof_effort",
        "primary_blocker",
        "proof_attempt_status",
        "problem_id",
        "title",
        "domain",
        "chunk",
        "next_investment",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for idx, row in enumerate(rows, start=1):
            parsed = row.get("parsed_probe") or {}
            writer.writerow(
                {
                    "rank": idx,
                    "fine_screen_ease_score": row.get("fine_screen_ease_score"),
                    "feasibility_score": parsed.get("feasibility_score"),
                    "recommendation": parsed.get("recommendation"),
                    "estimated_proof_effort": parsed.get("estimated_proof_effort"),
                    "primary_blocker": parsed.get("primary_blocker"),
                    "proof_attempt_status": parsed.get("proof_attempt_status"),
                    "problem_id": row.get("problem_id"),
                    "title": row.get("title"),
                    "domain": row.get("domain"),
                    "chunk": row.get("chunk"),
                    "next_investment": parsed.get("next_investment"),
                }
            )


def markdown_summary(rows: list[dict[str, Any]], missing: list[str], output_dir: Path) -> str:
    lines = [
        "# Open Fine-Screen Aggregate",
        "",
        f"- Completed entries aggregated: {len(rows)}",
        f"- Missing report files: {len(missing)}",
        "",
        "## Recommendation Counts",
        "",
    ]
    rec_counts = Counter(str((row.get("parsed_probe") or {}).get("recommendation") or "unknown") for row in rows)
    for key, count in rec_counts.most_common():
        lines.append(f"- `{key}`: {count}")
    lines.extend(["", "## Effort Counts", ""])
    effort_counts = Counter(str((row.get("parsed_probe") or {}).get("estimated_proof_effort") or "unknown") for row in rows)
    for key, count in effort_counts.most_common():
        lines.append(f"- `{key}`: {count}")
    lines.extend(["", "## Top Easiest Candidates", ""])
    lines.append("| Rank | Ease | Feas. | Rec | Effort | Blocker | Problem | Domain |")
    lines.append("| ---: | ---: | ---: | --- | --- | --- | --- | --- |")
    for idx, row in enumerate(rows[:40], start=1):
        parsed = row.get("parsed_probe") or {}
        title = str(row.get("title") or "").replace("|", "\\|")
        lines.append(
            f"| {idx} | {row.get('fine_screen_ease_score')} | {parsed.get('feasibility_score')} | "
            f"`{parsed.get('recommendation')}` | `{parsed.get('estimated_proof_effort')}` | "
            f"`{parsed.get('primary_blocker')}` | `{row.get('problem_id')}` {title} | `{row.get('domain')}` |"
        )
    if missing:
        lines.extend(["", "## Missing Reports", ""])
        for item in missing:
            lines.append(f"- `{item}`")
    lines.extend(
        [
            "",
            "## Files",
            "",
            f"- `{output_dir / 'fine_screen_ranked.csv'}`",
            f"- `{output_dir / 'fine_screen_ranked.json'}`",
            f"- `{output_dir / 'fine_screen_summary.md'}`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports", nargs="+", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows, missing = load_entries(args.reports)
    write_csv(args.output_dir / "fine_screen_ranked.csv", rows)
    (args.output_dir / "fine_screen_ranked.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    payload = {
        "schema_version": "amra.open_fine_screen_aggregate.v1",
        "entry_count": len(rows),
        "missing_reports": missing,
        "recommendation_counts": dict(
            Counter(str((row.get("parsed_probe") or {}).get("recommendation") or "unknown") for row in rows)
        ),
        "effort_counts": dict(
            Counter(str((row.get("parsed_probe") or {}).get("estimated_proof_effort") or "unknown") for row in rows)
        ),
        "top_problem_ids": [row.get("problem_id") for row in rows[:20]],
    }
    (args.output_dir / "fine_screen_counts.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "fine_screen_summary.md").write_text(
        markdown_summary(rows, missing, args.output_dir),
        encoding="utf-8",
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
