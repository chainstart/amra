#!/usr/bin/env python3
"""Launch a 2h supervised proof-lab attack for the verified three open targets.

This batch intentionally excludes WOWII Conjecture 327, which the 2026-06-09
source audit marked as resolved false by counterexample.

The current machine already has Lean-heavy formalizer work running, so this
launcher starts only natural-language proof-lab loops with supervisor review.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[1]
RUN_ROOT = REPO / "artifacts" / "open_problem_screening" / "latest" / "verified_three_open_attack_20260609_2h_v2"

TIME_BUDGET_SECONDS = 2 * 60 * 60
WALL_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 10 * 60
ROUND_TIME_BUDGET_SECONDS = 30 * 60

AUDIT_MD = REPO / "data" / "research_open" / "true_open_index" / "four_problem_source_audit_20260609.md"
AUDIT_YAML = REPO / "data" / "research_open" / "true_open_index" / "verified_four_problem_index_20260609.yaml"
BANK_YAML = REPO / "data" / "banks" / "formal_conjectures_open_research.yaml"
RAW_ROOT = REPO / "data" / "research_open" / "raw" / "formal_conjectures"


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "problem_id": "formal-conjectures-conjecture198a",
        "slug": "wowii-conjecture198a",
        "short_name": "WOWII 198a",
        "source_file": "FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
        "focus": (
            "Attack the original WOWII 198a theorem, not the solved Conjecture 198 variant. "
            "Main route: analyze whether b(G) <= 2 + average eccentricity forces a traceable graph. "
            "First try to prove or refute strong structural bridges relating largest induced bipartite "
            "subgraphs, geodesic layers, average eccentricity, and Hamiltonian-path obstructions. "
            "If a proof does not close, produce the smallest exact blocker or a concrete counterexample "
            "search contract."
        ),
        "special_warning": (
            "Do not confuse this with WOWII Conjecture 198, which uses ecc_avg(M) over maximum-degree "
            "vertices and is already marked true. This target uses ecc_avg(G)."
        ),
    },
    {
        "priority": 2,
        "problem_id": "formal-conjectures-conjecture200",
        "slug": "wowii-conjecture200",
        "short_name": "WOWII 200",
        "source_file": "FormalConjectures/WrittenOnTheWallII/GraphConjecture200.lean",
        "focus": (
            "Attack the original WOWII 200 theorem. Main route: understand the extremal equality "
            "tree(G) = ceil(1 + l_avg(G)), where tree(G) is largest induced tree size and l_avg(G) "
            "is average local neighborhood independence. Search for a proof that equality forces "
            "traceability, or isolate a counterexample family. Prioritize theorem-level bridges: "
            "local independence constraints, induced-tree saturation, path-extension obstructions, "
            "and Hamiltonian-path sufficient conditions."
        ),
        "special_warning": (
            "Do not replace the equality by a weaker inequality unless it is explicitly proved equivalent "
            "under connectedness."
        ),
    },
    {
        "priority": 3,
        "problem_id": "formal-conjectures-crystals-components-unique",
        "slug": "crystals-components-unique",
        "short_name": "Crystal components uniqueness",
        "source_file": "FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
        "focus": (
            "Attack Conjecture 4.5 from Abrate-Barbero-Cerruti-Murru, The Biharmonic mean. "
            "Use the paper's classification of crystals by recurrent sequences and conics. "
            "Main route: prove uniqueness of unordered components from the recurrence/conic "
            "parameterization, or find a genuine counterexample. Combine symbolic number-theory "
            "reasoning with bounded computational probes, but label computation as evidence unless "
            "converted into a certificate."
        ),
        "special_warning": (
            "Do not claim the theorem from Theorem 5 alone; Theorem 5 classifies crystal pairs but the "
            "remaining issue is whether two different pairs can yield the same product."
        ),
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def load_bank() -> dict[str, dict[str, Any]]:
    rows = yaml.safe_load(BANK_YAML.read_text(encoding="utf-8"))
    return {row["problem_id"]: row for row in rows}


def load_verified_index() -> dict[str, Any]:
    return yaml.safe_load(AUDIT_YAML.read_text(encoding="utf-8"))


def existing(paths: list[Path]) -> list[str]:
    return [str(path) for path in paths if path.exists()]


def render_statement(target: dict[str, Any], record: dict[str, Any], verified_entry: dict[str, Any]) -> str:
    references = record.get("references") or []
    status_basis = verified_entry.get("status_basis") or []
    lines = [
        f"# Supervised Proof-Lab Attack: {target['short_name']}",
        "",
        f"Problem id: `{target['problem_id']}`",
        "Batch: `verified_three_open_attack_20260609_2h`",
        "Mode: supervised natural-language proof-lab; no Lean-heavy compilation in this run.",
        "",
        "## Verified Open Status",
        "",
        f"- Source: {verified_entry.get('source', '')}",
        f"- Confidence: {verified_entry.get('confidence', '')}",
    ]
    for item in status_basis:
        lines.append(f"- {item}")
    lines += [
        "",
        "## Statement",
        "",
        str(record.get("statement") or "").strip(),
        "",
        "## Focus For This 2h Run",
        "",
        target["focus"],
        "",
        "## Target-Specific Warning",
        "",
        target["special_warning"],
        "",
        "## Required Output",
        "",
        "- Restate the exact original theorem in ordinary mathematical language.",
        "- Give the strongest proof route or counterexample route found in this run.",
        "- Identify each nontrivial bridge as: proved, plausible but unproved, false, computational, or source theorem.",
        "- If the main theorem is not solved, isolate the smallest next target that would materially move the main theorem.",
        "- Produce a Leanization plan only at the theorem-contract level; do not start heavy Lean formalization.",
        "- The global supervisor must reassess the route every round and reject local work that does not move the main theorem.",
    ]
    if references:
        lines += ["", "## Bank References", ""]
        lines += [f"- {ref}" for ref in references]
    return "\n".join(lines).rstrip() + "\n"


def render_readme(manifest: dict[str, Any]) -> str:
    lines = [
        "# Verified Three Open Attack 2026-06-09",
        "",
        f"Run root: `{manifest['run_root']}`",
        f"Per-target time budget: {manifest['time_budget_seconds_per_target']} seconds",
        "",
        "This batch uses supervised proof-lab only. It excludes `formal-conjectures-conjecture327` because the source audit found a current counterexample/formal-proof record.",
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
    return "\n".join(lines).rstrip() + "\n"


def command_prefix() -> list[str]:
    cmd = ["timeout", f"{WALL_TIMEOUT_SECONDS}s", "nice", "-n", "10"]
    if shutil.which("ionice"):
        cmd += ["ionice", "-c2", "-n7"]
    return cmd


def launch() -> dict[str, Any]:
    bank = load_bank()
    verified = load_verified_index()
    verified_by_id = {row["problem_id"]: row for row in verified.get("verified_open", [])}

    statements_dir = RUN_ROOT / "statements"
    logs_dir = RUN_ROOT / "logs"
    pids_dir = RUN_ROOT / "pids"
    runs_dir = RUN_ROOT / "runs"
    for path in [statements_dir, logs_dir, pids_dir, runs_dir]:
        path.mkdir(parents=True, exist_ok=True)

    launched: list[dict[str, Any]] = []
    for target in TARGETS:
        problem_id = target["problem_id"]
        record = bank[problem_id]
        verified_entry = verified_by_id[problem_id]

        statement_path = statements_dir / f"{target['priority']:02d}-{target['slug']}.md"
        write_text(statement_path, render_statement(target, record, verified_entry))

        output_root = runs_dir / target["slug"]
        run_name = f"{target['slug']}-prooflab-2h"
        log_path = logs_dir / f"{target['priority']:02d}-{target['slug']}.log"
        pid_path = pids_dir / f"{target['priority']:02d}-{target['slug']}.pid"

        cmd = command_prefix() + [
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
            "900",
            "--proof-audit-timeout",
            "300",
            "--proof-grounding-timeout",
            "450",
            "--supervisor-backend",
            "codex",
            "--supervisor-every-rounds",
            "1",
            "--supervisor-timeout",
            "450",
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
        for context in existing(
            [
                AUDIT_MD,
                AUDIT_YAML,
                RAW_ROOT / target["source_file"],
            ]
        ):
            cmd += ["--context-file", context]

        env = os.environ.copy()
        # These are non-Lean proof-lab runs. Keep memory guarding, but do not let
        # current Lean-heavy load block natural-language source/proof attempts.
        env.setdefault("ARA_MATH_MIN_AVAILABLE_MEMORY_MB", "1024")
        env["ARA_MATH_MAX_LOAD_PER_CPU"] = "100"
        env.setdefault("ARA_MATH_SYSTEM_WAIT_SECONDS", "5")

        with log_path.open("ab") as log:
            proc = subprocess.Popen(
                cmd,
                cwd=REPO,
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                env=env,
                start_new_session=True,
            )
        write_text(pid_path, str(proc.pid))
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
                "mode": "proof-lab",
                "command": cmd,
            }
        )

    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds_per_target": TIME_BUDGET_SECONDS,
        "round_time_budget_seconds": ROUND_TIME_BUDGET_SECONDS,
        "wall_timeout_seconds": WALL_TIMEOUT_SECONDS,
        "lean_policy": "no new Lean-heavy process; proof-lab load guard relaxed because existing machine already has two Lean-heavy jobs",
        "excluded_problem_ids": ["formal-conjectures-conjecture327"],
        "source_audit": str(AUDIT_MD),
        "verified_index": str(AUDIT_YAML),
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    write_text(RUN_ROOT / "README.md", render_readme(manifest))
    return manifest


if __name__ == "__main__":
    result = launch()
    print(json.dumps({"run_root": result["run_root"], "targets": result["targets"]}, indent=2, ensure_ascii=False))
