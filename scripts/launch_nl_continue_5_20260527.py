#!/usr/bin/env python3
"""Continue five natural-language proof attacks for four hours each."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
PREV_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "nl_attack_10_20260526"
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "nl_continue_5_20260527"
TIME_BUDGET_SECONDS = 4 * 60 * 60
ROUND_TIME_BUDGET_SECONDS = 60 * 60


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "independent-domination-even",
        "problem_id": "formal-conjectures-independentdominationeven",
        "previous_statement": "statements/02-independent-domination-even.md",
        "previous_run": "runs/independent-domination-even/independent-domination-even-nl-8h",
        "focus": "Continue source-grounded proof recovery for the even case; either close the arithmetic specialization or isolate the exact CKKO theorem contract needed for Lean.",
    },
    {
        "priority": 2,
        "slug": "independent-domination-odd",
        "problem_id": "formal-conjectures-independentdominationodd",
        "previous_statement": "statements/04-independent-domination-odd.md",
        "previous_run": "runs/independent-domination-odd/independent-domination-odd-nl-8h",
        "focus": "Continue the odd specialization; separate local floor/scaling arithmetic from the external Cho-Kim-Kim-Oum dependency.",
    },
    {
        "priority": 3,
        "slug": "erdos-1084-triangular-d2",
        "problem_id": "formal-conjectures-erdos-1084-variants-triangular-optimal-d2",
        "previous_statement": "statements/05-erdos-1084-triangular-d2.md",
        "previous_run": "runs/erdos-1084-triangular-d2/erdos-1084-triangular-d2-nl-8h",
        "focus": "Continue Harborth/contact-number source recovery and produce the narrowest theorem dependency for the triangular-lattice d=2 specialization.",
    },
    {
        "priority": 4,
        "slug": "triangle-dissection-13",
        "problem_id": "triangle-dissection-13",
        "previous_statement": "statements/03-triangle-dissection-13.md",
        "previous_run": "runs/triangle-dissection-13/triangle-dissection-13-nl-8h",
        "focus": "Continue source-faithful finite-case analysis for N=13; determine whether the route is a Beeson theorem instance or needs a separate certificate.",
    },
    {
        "priority": 5,
        "slug": "triangle-dissection-17",
        "problem_id": "triangle-dissection-17",
        "previous_statement": "statements/07-triangle-dissection-17.md",
        "previous_run": "runs/triangle-dissection-17/triangle-dissection-17-nl-8h",
        "focus": "Continue the N=17 companion case and isolate reusable theorem contracts shared with N=13 and N=19.",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def latest_numbered_file(run_dir: Path, subdir: str, filename: str) -> Path | None:
    root = run_dir / subdir
    if not root.exists():
        return None
    candidates = sorted(root.glob(f"round-*/{filename}"))
    return candidates[-1] if candidates else None


def context_files(target: dict[str, Any]) -> list[str]:
    paths: list[Path] = []
    statement = PREV_ROOT / target["previous_statement"]
    run_dir = PREV_ROOT / target["previous_run"]
    for path in [
        statement,
        run_dir / "summary.md",
        latest_numbered_file(run_dir, "proof_lab", "summary.md"),
        latest_numbered_file(run_dir, "supervisor", "decision.md"),
    ]:
        if path and path.exists():
            paths.append(path)
    deduped: list[str] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve(strict=False)
        if resolved in seen:
            continue
        seen.add(resolved)
        deduped.append(str(path))
    return deduped


def render_statement(target: dict[str, Any]) -> str:
    previous_statement = PREV_ROOT / target["previous_statement"]
    prior = previous_statement.read_text(encoding="utf-8", errors="ignore") if previous_statement.exists() else ""
    return (
        f"# Natural-Language Continuation: {target['slug']}\n\n"
        f"Problem id: `{target['problem_id']}`\n"
        "Batch: `nl_continue_5_20260527`\n"
        "Budget: 4 hours.\n\n"
        "## Continuation Focus\n\n"
        f"{target['focus']}\n\n"
        "## Prior Statement And Screening Context\n\n"
        f"{prior.strip()}\n\n"
        "## Required Output Shape\n\n"
        "- State whether the route is now closed, conditional on a named external theorem, blocked by a certificate gap, or unsuitable.\n"
        "- Give a concise proof route or the first fatal gap.\n"
        "- End with a Leanization contract if the route is still viable.\n"
    )


def launch() -> dict[str, Any]:
    for path in [RUN_ROOT / "statements", RUN_ROOT / "logs", RUN_ROOT / "pids", RUN_ROOT / "runs"]:
        path.mkdir(parents=True, exist_ok=True)
    launched: list[dict[str, Any]] = []
    shared_context = REPO / "artifacts" / "paper_targets_20260523" / "statements" / "shared_context.md"
    for target in TARGETS:
        statement_path = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
        statement_path.write_text(render_statement(target), encoding="utf-8")
        output_root = RUN_ROOT / "runs" / target["slug"]
        run_name = f"{target['slug']}-nl-continue-4h"
        log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
        pid_path = RUN_ROOT / "pids" / f"{target['priority']:02d}-{target['slug']}.pid"
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
        for context in context_files(target):
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
                "slug": target["slug"],
                "problem_id": target["problem_id"],
                "pid": proc.pid,
                "statement_path": str(statement_path),
                "log_path": str(log_path),
                "output_root": str(output_root),
                "run_name": run_name,
                "contexts": context_files(target),
                "time_budget_seconds": TIME_BUDGET_SECONDS,
                "command": cmd,
            }
        )
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds_per_target": TIME_BUDGET_SECONDS,
        "round_time_budget_seconds": ROUND_TIME_BUDGET_SECONDS,
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    (RUN_ROOT / "README.md").write_text(render_readme(manifest), encoding="utf-8")
    return manifest


def render_readme(manifest: dict[str, Any]) -> str:
    lines = [
        "# NL Continuation Batch 2026-05-27",
        "",
        f"Run root: `{manifest['run_root']}`",
        f"Per-target time budget: {manifest['time_budget_seconds_per_target']} seconds",
        "",
        "| Priority | Problem id | PID | Log | Output root |",
        "| ---: | --- | ---: | --- | --- |",
    ]
    for target in manifest["targets"]:
        lines.append(
            "| {priority} | `{problem_id}` | {pid} | `{log_path}` | `{output_root}` |".format(**target)
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(json.dumps(launch(), indent=2, ensure_ascii=False))
