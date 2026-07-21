#!/usr/bin/env python3
"""Launch two direct proof-lab slots with only light local Lean probing allowed."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
RUN_ROOT = (
    REPO
    / "artifacts"
    / "open_problem_screening"
    / "latest"
    / "erdos2_light_lean_prooflab_20260702_4h"
)

TIME_BUDGET_SECONDS = 4 * 60 * 60
WALL_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 15 * 60
MAX_SLOTS = 2


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def existing(*paths: str | Path) -> list[str]:
    out: list[str] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO / path
        if path.exists():
            out.append(str(path))
    return out


def resource_prefix() -> list[str]:
    if not shutil.which("systemd-run"):
        return []
    return [
        "systemd-run",
        "--user",
        "--scope",
        "-p",
        "MemoryMax=4G",
        "-p",
        "MemorySwapMax=5G",
        "-p",
        "CPUQuota=100%",
    ]


def nice_prefix() -> list[str]:
    command = ["timeout", f"{WALL_TIMEOUT_SECONDS}s", "nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


GLOBAL_INSTRUCTIONS = """
Mode: direct AMRA `run-ai-proof-lab`, not campaign-loop.

Hard constraints for this run:

- There are exactly two active slots in this launcher. Do not spawn child
  proof campaigns or additional parallel agents.
- Do not edit repository files.
- Do not run `lake build`, `lake update`, `lake exe cache get`, full-library
  imports, aggregate `AmraLibrary.lean` checks, or any whole-project build.
- Lean is allowed only for small local probes: a single target file, a tiny
  scratch expression, or `#check`/`#eval` style API inspection. If a command
  would compile a broad dependency tree, skip it and explain why.
- The proof-lab output must distinguish: proved locally, small Lean probe,
  source theorem, plausible lemma, unknown, false, and frozen branch.
- Prefer theorem contracts and dependency repair over broad literature prose.
"""


TARGETS: list[dict[str, Any]] = [
    {
        "priority": 1,
        "slug": "erdos866-ces75-source-contract-light-lean",
        "title": "Erdos 866 CES75 source-contract extraction",
        "contexts": existing(
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/GeneratedClaims.lean",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/MainClaim.lean",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ProofNotes.md",
            "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos866-g6-sidon-ces75-route/erdos866-g6-sidon-ces75-route-prooflab-4h/proof_lab/round-006/summary.md",
        ),
        "statement": f"""
# Erdos 866: CES75 source-contract extraction with light Lean probes

{GLOBAL_INSTRUCTIONS}

Current state:

The `gFun 6` square-root upper route is already reduced to the CES75 source
fact. The previous run located the current blocker as the source-level CES75
case reduction, not the final-window lemma or the `gFun` bridge.

Target for this slot:

Extract a Lean-ready natural-language theorem contract for
`ces75_theorem4_even_count_case_reduction_source`.

Required deliverable:

1. State the exact theorem contract with variables `A`, `n`, `m`, even count
   `t`, central-even set, constants `K`, `cCES`, `Nces`, and assumptions
   `A ⊆ Icc 1 (2*n)`, `A.card = n + m`, `K * sqrt n < m`.
2. Classify each premise as source theorem, standard counting, proved local,
   plausible new lemma, unknown, or false.
3. Explain precisely how this source contract feeds the already verified
   final-window lemma and the existing `CES75Theorem4... ↔ gFun 6` bridge.
4. Use only small Lean probes if needed to inspect local declarations; do not
   run full builds.
5. End with a freeze list and the next one theorem to attack.
""",
    },
    {
        "priority": 2,
        "slug": "erdos1084-harborth-upper-contract-light-lean",
        "title": "Erdos 1084 Harborth upper contract",
        "contexts": existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
            "artifacts/open_problem_screening/latest/lean_loop_8_20260527_5h/final_lean/02_erdos_1084_triangular_d2.lean",
            "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos1084-triangular-contact-route/erdos1084-triangular-contact-route-prooflab-4h/proof_lab/round-003/summary.md",
            "artifacts/open_problem_screening/latest/erdos5_nl_path_search_20260702_4h/runs/erdos1084-triangular-contact-route/erdos1084-triangular-contact-route-prooflab-4h/supervisor/round-003/decision.md",
        ),
        "statement": f"""
# Erdos 1084: Harborth upper bound in local `unitDistNum` convention

{GLOBAL_INSTRUCTIONS}

Current state:

The triangular floor arithmetic is already available as an artifact. The
hexagonal patch lower construction is mathematically clear. The unresolved
blocker is the planar Harborth contact-number upper bound translated into the
local `f 2 N` / `unitDistNum` convention.

Target for this slot:

Extract and test the theorem contract
`Erdos1084.harborth_unitDistNum_upper_ge4`.

Required deliverable:

1. State the exact source-contract theorem for finite `1`-separated point sets
   in `ℝ^2` with unordered `unitDistNum` pairs and `N ≥ 4`.
2. State the disk-center bridge from radius-`1/2` congruent disk contacts to
   unit-distance pairs.
3. Check whether the target should be an imported source theorem, a standard
   bridge lemma, or a triangular-only upper route.
4. Use only small Lean probes if needed to inspect names/types; do not run
   `lake build` or any full library check.
5. End with a ranked next theorem package and freeze branches that try to
   reprove Harborth from scratch.
""",
    },
]


def prepare_command(target: dict[str, Any], statement_path: Path, output_root: Path) -> list[str]:
    command = [
        *resource_prefix(),
        *nice_prefix(),
        sys.executable,
        "run.py",
        "run-ai-proof-lab",
        "--statement-file",
        str(statement_path),
        "--backend",
        "codex",
        "--search",
        "--source-first",
        "--attempts",
        "4",
        "--audits",
        "2",
        "--time-budget",
        str(TIME_BUDGET_SECONDS),
        "--attempt-timeout",
        "1200",
        "--audit-timeout",
        "600",
        "--grounding-timeout",
        "600",
        "--math-tools-profile",
        "essential",
        "--no-install-missing-math-tools",
        "--no-math-tool-smoke",
        "--output-root",
        str(output_root),
        "--run-name",
        f"{target['slug']}-4h",
        "--reasoning-effort",
        "high",
    ]
    for context in target["contexts"]:
        command += ["--context-file", context]
    return command


def launch() -> dict[str, Any]:
    if len(TARGETS) > MAX_SLOTS:
        raise RuntimeError(f"Refusing to launch {len(TARGETS)} targets; MAX_SLOTS={MAX_SLOTS}")

    statements_dir = RUN_ROOT / "statements"
    logs_dir = RUN_ROOT / "logs"
    pids_dir = RUN_ROOT / "pids"
    runs_dir = RUN_ROOT / "runs"
    for path in [statements_dir, logs_dir, pids_dir, runs_dir]:
        path.mkdir(parents=True, exist_ok=True)

    launched: list[dict[str, Any]] = []
    for target in TARGETS:
        statement_path = statements_dir / f"{target['priority']:02d}-{target['slug']}.md"
        log_path = logs_dir / f"{target['priority']:02d}-{target['slug']}.log"
        pid_path = pids_dir / f"{target['priority']:02d}-{target['slug']}.pid"
        output_root = runs_dir / target["slug"]
        write_text(statement_path, str(target["statement"]))

        command = prepare_command(target, statement_path, output_root)
        env = os.environ.copy()
        env.update(
            {
                "LEAN_NUM_THREADS": "1",
                "OMP_NUM_THREADS": "1",
                "ARA_MATH_MIN_AVAILABLE_MEMORY_MB": "1024",
                "ARA_MATH_MAX_LOAD_PER_CPU": "100",
                "ARA_MATH_SYSTEM_WAIT_SECONDS": "5",
                "ARA_MATH_BACKEND_MAX_MEMORY_MB": "3072",
                "ARA_PROOF_LAB_BACKEND_MAX_MEMORY_MB": "3072",
            }
        )
        with log_path.open("ab") as log:
            proc = subprocess.Popen(
                command,
                cwd=REPO,
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                env=env,
            )
        write_text(pid_path, str(proc.pid))
        launched.append(
            {
                "priority": target["priority"],
                "slug": target["slug"],
                "title": target["title"],
                "pid": proc.pid,
                "started_at": utc_now(),
                "statement_path": str(statement_path),
                "log_path": str(log_path),
                "output_root": str(output_root),
                "context_count": len(target["contexts"]),
                "time_budget_seconds": TIME_BUDGET_SECONDS,
                "wall_timeout_seconds": WALL_TIMEOUT_SECONDS,
                "mode": "direct run-ai-proof-lab",
                "slot_policy": f"max {MAX_SLOTS} active slots",
                "lean_policy": "light local probes only; no lake build or full Lean compilation",
                "command": command,
            }
        )

    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "max_slots": MAX_SLOTS,
        "active_slots": len(launched),
        "time_budget_seconds_per_target": TIME_BUDGET_SECONDS,
        "lean_policy": "light local probes only; no lake build or full Lean compilation",
        "targets": launched,
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    write_text(
        RUN_ROOT / "README.md",
        "# Erdos 2 Light-Lean Proof-Lab 2026-07-02\n\n"
        f"Run root: `{RUN_ROOT}`\n\n"
        "Direct `run-ai-proof-lab` only. No campaign-loop, no supervisor "
        "formalizer promotion. Max active slots: 2.\n",
    )
    return manifest


if __name__ == "__main__":
    result = launch()
    print(
        json.dumps(
            {
                "run_root": result["run_root"],
                "max_slots": result["max_slots"],
                "targets": [
                    {
                        "slug": target["slug"],
                        "pid": target["pid"],
                        "log_path": target["log_path"],
                        "context_count": target["context_count"],
                    }
                    for target in result["targets"]
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
