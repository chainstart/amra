#!/usr/bin/env python3
"""Launch the 2026-05-26 open-problem natural-language attack batch.

This creates a reproducible run manifest, per-target statement files, and
detached proof-lab processes with an eight-hour wall-clock budget each.
"""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[1]
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "nl_attack_10_20260526"

TIME_BUDGET_SECONDS = 8 * 60 * 60
ROUND_TIME_BUDGET_SECONDS = 60 * 60


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "problem_id": "formal-conjectures-kotherconjecture-variants-le-kotherradical",
        "slug": "kothe-radical",
        "focus": "Recover a paper-faithful proof route for le_KotherRadical, then isolate the shortest Lean theorem chain around KotheRadical membership.",
        "probe": "artifacts/math_scout/open-fine-screen-chunk-3-20260523/problems/0007-formal-conjectures-kotherconjecture-variants-le-kotherradical/probe_output.md",
    },
    {
        "priority": 2,
        "problem_id": "formal-conjectures-independentdominationeven",
        "slug": "independent-domination-even",
        "focus": "Recover the exact Cho-Kim-Kim-Oum theorem dependency and derive the even arithmetic specialization in a Lean-ready way.",
        "probe": "artifacts/math_scout/open-fine-screen-chunk-2-20260523/problems/0029-formal-conjectures-independentdominationeven/probe_output.md",
    },
    {
        "priority": 3,
        "problem_id": "triangle-dissection-13",
        "slug": "triangle-dissection-13",
        "focus": "Decide whether the N=13 case reduces to prime-exclusion or needs a separate finite certificate; output a Lean-ready theorem contract.",
        "probe": "artifacts/math_scout/open-fine-screen-chunk-3-20260523/problems/0030-triangle-dissection-13/probe_output.md",
        "extra_context": ["artifacts/open_problem_screening/latest/easiest_10_nl_lean_candidates_20260526.md"],
    },
    {
        "priority": 4,
        "problem_id": "formal-conjectures-independentdominationodd",
        "slug": "independent-domination-odd",
        "focus": "Recover the exact Cho-Kim-Kim-Oum theorem dependency and derive the odd arithmetic specialization in a Lean-ready way.",
        "probe": "artifacts/math_scout/open-fine-screen-chunk-3-20260523/problems/0003-formal-conjectures-independentdominationodd/probe_output.md",
    },
    {
        "priority": 5,
        "problem_id": "formal-conjectures-erdos-1084-variants-triangular-optimal-d2",
        "slug": "erdos-1084-triangular-d2",
        "focus": "Recover Harborth/contact-number source theorem and derive the d=2 triangular-lattice formula with explicit formal dependencies.",
        "probe": "artifacts/math_scout/open-fine-screen-chunk-2-20260523/problems/0002-formal-conjectures-erdos-1084-variants-triangular-optimal-d2/probe_output.md",
    },
    {
        "priority": 6,
        "problem_id": "triangle-dissection-19",
        "slug": "triangle-dissection-19",
        "focus": "Recover the exact Beeson/Tutte theorem chain for N=19 and map it to a Lean-checkable finite dissection contract.",
        "probe": "artifacts/math_scout/open-fine-screen-chunk-3-20260523/problems/0032-triangle-dissection-19/probe_output.md",
        "extra_context": ["artifacts/open_problem_screening/latest/easiest_10_nl_lean_candidates_20260526.md"],
    },
    {
        "priority": 7,
        "problem_id": "triangle-dissection-17",
        "slug": "triangle-dissection-17",
        "focus": "Treat N=17 as a companion finite case and isolate the reusable prime-exclusion/certificate lemmas shared with N=13 and N=19.",
        "probe": "artifacts/math_scout/open-fine-screen-chunk-3-20260523/problems/0031-triangle-dissection-17/probe_output.md",
        "extra_context": ["artifacts/open_problem_screening/latest/easiest_10_nl_lean_candidates_20260526.md"],
    },
    {
        "priority": 8,
        "problem_id": "formal-conjectures-conjecture19",
        "slug": "wowii-conjecture19",
        "focus": "Attack the reduction to the self-centered case using the known b(G) >= diam(G)+lambda(G)-1 route and local WOWII definitions.",
        "probe": "artifacts/math_scout/open-fine-screen-chunk-1-20260523/problems/0015-formal-conjectures-conjecture19/probe_output.md",
    },
    {
        "priority": 9,
        "problem_id": "formal-conjectures-exists-maximal-star",
        "slug": "exists-maximal-star",
        "focus": "Do not try to close the full problem first; prove or refute the rank <= 2 hereditary-family checkpoint and identify Lean statements.",
        "probe": "artifacts/math_scout/open-fine-screen-chunk-2-20260523/problems/0023-formal-conjectures-exists-maximal-star/probe_output.md",
    },
    {
        "priority": 10,
        "problem_id": "formal-conjectures-beaver-math-olympiad-problem-2-antihydra",
        "slug": "antihydra",
        "focus": "Search for a finite odd-block quotient and potential-function certificate for the antihydra recurrence; keep the output Lean-certificate oriented.",
        "probe": "artifacts/math_scout/open-fine-screen-chunk-1-20260523/problems/0003-formal-conjectures-beaver-math-olympiad-problem-2-antihydra/probe_output.md",
    },
]


def load_yaml_records(path: Path) -> dict[str, dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        rows = yaml.safe_load(handle)
    return {row["problem_id"]: row for row in rows}


def load_fine_screen(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return {row["problem_id"]: row for row in csv.DictReader(handle)}


def existing_contexts(target: dict[str, Any], record: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    probe = target.get("probe")
    if probe and (REPO / probe).exists():
        paths.append(str(REPO / probe))
    source_file = (record.get("metadata") or {}).get("source_file")
    if source_file:
        raw_path = REPO / "data" / "research_open" / "raw" / "formal_conjectures" / source_file
        if raw_path.exists():
            paths.append(str(raw_path))
    for rel in target.get("extra_context", []):
        if (REPO / rel).exists():
            paths.append(str(REPO / rel))
    return paths


def render_statement(target: dict[str, Any], record: dict[str, Any], fine: dict[str, str]) -> str:
    metadata = record.get("metadata") or {}
    references = record.get("references") or []
    strategies = record.get("recommended_strategy") or []
    lines = [
        f"# Natural-Language Proof Attack: {record.get('title', target['problem_id'])}",
        "",
        f"Problem id: `{target['problem_id']}`",
        f"Priority: {target['priority']}",
        "Batch: `nl_attack_10_20260526`",
        "",
        "Target: produce a paper-faithful natural-language proof route, or isolate the exact remaining lemma/counterexample/certificate route.",
        "",
        "## Statement",
        "",
        str(record.get("statement") or "").strip(),
        "",
        "## Focus For This 8h Run",
        "",
        target["focus"],
        "",
        "## Screening Metadata",
        "",
        f"- open_problem: {record.get('open_problem')}",
        f"- metadata.status: {metadata.get('status')}",
        f"- metadata.category: {metadata.get('category')}",
        f"- fine_screen_rank: {fine.get('rank', '')}",
        f"- fine_screen_ease_score: {fine.get('fine_screen_ease_score', '')}",
        f"- feasibility_score: {fine.get('feasibility_score', '')}",
        f"- recommendation: {fine.get('recommendation', '')}",
        f"- estimated_proof_effort: {fine.get('estimated_proof_effort', '')}",
        f"- primary_blocker: {fine.get('primary_blocker', '')}",
        f"- proof_attempt_status: {fine.get('proof_attempt_status', '')}",
        f"- next_investment: {fine.get('next_investment', '')}",
        "",
        "## Required Output Shape",
        "",
        "- Restate the exact theorem/claim in ordinary mathematical language.",
        "- Give the strongest natural-language proof route found.",
        "- Name every nontrivial dependency as a theorem, source theorem, finite certificate, computation, or Lean helper lemma.",
        "- If the full route fails, identify the first fatal gap and the narrowest next target.",
        "- End with a Leanization plan: theorem statements, definitions to inspect, and expected formal blockers.",
    ]
    if references:
        lines += ["", "## References From Bank", ""]
        lines += [f"- {ref}" for ref in references]
    if strategies:
        lines += ["", "## Bank Recommended Strategy", ""]
        lines += [f"- {item}" for item in strategies]
    return "\n".join(lines).rstrip() + "\n"


def launch() -> dict[str, Any]:
    formal_records = load_yaml_records(REPO / "data" / "banks" / "formal_conjectures_open_research.yaml")
    triangle_records = load_yaml_records(REPO / "data" / "banks" / "triangle_dissection_track.yaml")
    records = {**formal_records, **triangle_records}
    fine = load_fine_screen(
        REPO
        / "artifacts"
        / "open_problem_screening"
        / "open-problem-screen-20260523"
        / "fine_screen"
        / "fine_screen_ranked.csv"
    )

    statements_dir = RUN_ROOT / "statements"
    logs_dir = RUN_ROOT / "logs"
    pids_dir = RUN_ROOT / "pids"
    runs_dir = RUN_ROOT / "runs"
    for path in [statements_dir, logs_dir, pids_dir, runs_dir]:
        path.mkdir(parents=True, exist_ok=True)

    launched = []
    generated_at = datetime.now(timezone.utc).isoformat()
    shared_context = REPO / "artifacts" / "paper_targets_20260523" / "statements" / "shared_context.md"

    for target in TARGETS:
        problem_id = target["problem_id"]
        record = records.get(problem_id)
        if record is None:
            raise KeyError(f"Missing bank record for {problem_id}")
        fine_row = fine.get(problem_id, {})
        statement_path = statements_dir / f"{target['priority']:02d}-{target['slug']}.md"
        statement_path.write_text(render_statement(target, record, fine_row), encoding="utf-8")

        output_root = runs_dir / target["slug"]
        run_name = f"{target['slug']}-nl-8h"
        log_path = logs_dir / f"{target['priority']:02d}-{target['slug']}.log"
        pid_path = pids_dir / f"{target['priority']:02d}-{target['slug']}.pid"

        cmd = [
            "nice",
            "-n",
            "10",
            sys.executable,
            "run.py",
            "run-campaign-loop",
            "--statement-file",
            str(statement_path),
            "--backend",
            "codex",
            "--search",
            "--source-first",
            "--mode",
            "proof-lab",
            "--rounds",
            "999",
            "--time-budget",
            str(TIME_BUDGET_SECONDS),
            "--round-time-budget",
            str(ROUND_TIME_BUDGET_SECONDS),
            "--proof-attempts",
            "2",
            "--proof-audits",
            "1",
            "--proof-attempt-timeout",
            "1800",
            "--proof-audit-timeout",
            "600",
            "--proof-grounding-timeout",
            "600",
            "--supervisor-backend",
            "codex",
            "--supervisor-every-rounds",
            "1",
            "--supervisor-timeout",
            "900",
            "--math-tools-profile",
            "essential",
            "--no-install-missing-math-tools",
            "--no-math-tool-smoke",
            "--output-root",
            str(output_root),
            "--run-name",
            run_name,
            "--reasoning-effort",
            "high",
        ]
        if shared_context.exists():
            cmd += ["--context-file", str(shared_context)]
        for context in existing_contexts(target, record):
            cmd += ["--context-file", context]

        with log_path.open("ab") as log:
            proc = subprocess.Popen(
                cmd,
                cwd=REPO,
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        pid_path.write_text(f"{proc.pid}\n", encoding="ascii")
        launched.append(
            {
                "priority": target["priority"],
                "problem_id": problem_id,
                "slug": target["slug"],
                "pid": proc.pid,
                "statement_path": str(statement_path),
                "log_path": str(log_path),
                "output_root": str(output_root),
                "run_name": run_name,
                "time_budget_seconds": TIME_BUDGET_SECONDS,
                "command": cmd,
            }
        )

    manifest = {
        "generated_at": generated_at,
        "run_root": str(RUN_ROOT),
        "time_budget_seconds_per_target": TIME_BUDGET_SECONDS,
        "round_time_budget_seconds": ROUND_TIME_BUDGET_SECONDS,
        "targets": launched,
        "replacement_note": "Replaced formal-conjectures-hasaddvcndimatmost-n-one-of-convex-rn-add-one with formal-conjectures-beaver-math-olympiad-problem-2-antihydra because the additive VC target had prior counterexample/gap risk.",
    }
    (RUN_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (RUN_ROOT / "README.md").write_text(render_readme(manifest), encoding="utf-8")
    return manifest


def render_readme(manifest: dict[str, Any]) -> str:
    lines = [
        "# Open NL Attack Batch 2026-05-26",
        "",
        f"Run root: `{manifest['run_root']}`",
        f"Per-target time budget: {manifest['time_budget_seconds_per_target']} seconds",
        "",
        "## Targets",
        "",
        "| Priority | Problem id | PID | Log | Output root |",
        "| ---: | --- | ---: | --- | --- |",
    ]
    for target in manifest["targets"]:
        lines.append(
            "| {priority} | `{problem_id}` | {pid} | `{log_path}` | `{output_root}` |".format(**target)
        )
    lines += [
        "",
        "## Replacement",
        "",
        manifest["replacement_note"],
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    result = launch()
    print(json.dumps({"run_root": result["run_root"], "targets": result["targets"]}, indent=2, ensure_ascii=False))
