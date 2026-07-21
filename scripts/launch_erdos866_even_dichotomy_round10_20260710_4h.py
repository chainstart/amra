#!/usr/bin/env python3
"""Launch the next faithful four-hour supervised Lean campaign for Erdos #866."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path("/home/biostar/work/projects/amra")
WORKSPACE = REPO / "projects/erdos-866-ai-continuation-20260505/formal"
TARGET_FILE = WORKSPACE / "MathProject/ErdosProblem866Core.lean"
RUN_ROOT = (
    REPO
    / "artifacts/open_problem_screening/latest/erdos866_even_dichotomy_round10_20260710_4h"
)
TIME_BUDGET_SECONDS = 4 * 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 15 * 60
TARGET_THEOREM = "ces75_even_count_ge_excess"
SLUG = "erdos866-even-count-ge-excess"
RUN_NAME = "erdos866-even-count-ge-excess-supervised-4h"


STATEMENT = """\
# Erdos #866: even count dominates the excess

Prove the exact Lean theorem `ces75_even_count_ge_excess` in
`MathProject/ErdosProblem866Core.lean`.

This is the first unverified local node in the CES75 Theorem 4 even-count
dichotomy.  If `A` has `n + m` elements in `[1, 2*n]` and exactly `t` of its
elements are even, then `m <= t`, because the ambient interval contains only
`n` odd integers.

Required route:
- partition `A` into its even and non-even filters;
- identify or inject the non-even filter into the odd elements of
  `Finset.Icc 1 (2*n)`;
- prove that this odd ambient set has cardinality exactly `n`;
- combine the partition with `A.card = n + m` and
  `t = (A.filter fun x => Even x).card`.

The nearby verified theorem `ces75_missing_odd_card_le_even_card` contains a
source-faithful odd-ambient enumeration that may be factored into a reusable
local helper.  Do not weaken the target and do not assume the conclusion.

Use the configured single-file verifier only.  Intermediate local lemmas are
allowed, but the final declaration must match the expected target header.
Do not add `sorry`, `admit`, axioms, constants, opaque declarations, source
markers, or new trusted assumptions.  The supervisor must review every round
and keep all retargeting on the exact CES75 even-count reduction path.
"""


HEADER = """\
theorem ces75_even_count_ge_excess
    (A : Finset Int) (n m t : Nat)
    (hA : A ⊆ Finset.Icc (1 : Int) (2 * (n : Int)))
    (hcard : A.card = n + m)
    (ht : t = (A.filter fun x => Even x).card) :
    m ≤ t
"""


CONTEXTS = [
    REPO / "artifacts/source_papers/ces75/ces75_theorem4_source_locator.md",
    REPO / "artifacts/literature/ces75/theorem4_engineering_decomposition_20260510.md",
    REPO / "artifacts/source_papers/ces75/text/choi_erdos_szemeredi_1975-39.txt",
    WORKSPACE / "MathProject/ProofNotes.md",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_command() -> str:
    relative = TARGET_FILE.resolve().relative_to(WORKSPACE.resolve())
    return " ".join(
        [
            "env",
            "LEAN_NUM_THREADS=1",
            "OMP_NUM_THREADS=1",
            "lake",
            "env",
            "lean",
            shlex.quote(str(relative)),
        ]
    )


def campaign_command(statement_path: Path, header_path: Path, output_root: Path) -> list[str]:
    command = [
        "/usr/bin/timeout",
        f"{HARD_TIMEOUT_SECONDS}s",
        "nice",
        "-n",
        "10",
        sys.executable,
        "run.py",
        "run-campaign-loop",
        "--statement-file",
        str(statement_path),
        "--workspace",
        str(WORKSPACE),
        "--target-file",
        str(TARGET_FILE),
        "--expected-target-header-file",
        str(header_path),
        "--build-command",
        build_command(),
        "--backend",
        "codex",
        "--closed-book",
        "--mode",
        "lean-formalizer",
        "--rounds",
        "999",
        "--time-budget",
        str(TIME_BUDGET_SECONDS),
        "--round-time-budget",
        str(40 * 60),
        "--formalizer-attempts",
        "3",
        "--formalizer-attempt-timeout",
        str(25 * 60),
        "--formalizer-build-timeout",
        str(10 * 60),
        "--initial-target-theorem",
        TARGET_THEOREM,
        "--final-target-theorem",
        TARGET_THEOREM,
        "--proof-attempts",
        "0",
        "--proof-audits",
        "0",
        "--supervisor-backend",
        "codex",
        "--supervisor-every-rounds",
        "1",
        "--supervisor-timeout",
        str(10 * 60),
        "--math-tools-profile",
        "essential",
        "--no-install-missing-math-tools",
        "--no-math-tool-smoke",
        "--output-root",
        str(output_root),
        "--run-name",
        RUN_NAME,
        "--reasoning-effort",
        "high",
        "--max-stalled-rounds",
        "8",
    ]
    for context in CONTEXTS:
        if context.exists():
            command.extend(["--context-file", str(context)])
    return command


def process_env() -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "LEAN_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "AMRA_SKIP_TOOL_SMOKE": "1",
        }
    )
    return env


def launch() -> dict[str, Any]:
    statement_path = RUN_ROOT / "statements" / f"{SLUG}.md"
    header_path = RUN_ROOT / "headers" / f"{SLUG}.lean"
    output_root = RUN_ROOT / "runs" / SLUG
    log_path = RUN_ROOT / "logs" / f"{SLUG}.log"
    write_text(statement_path, STATEMENT)
    write_text(header_path, HEADER)
    command = campaign_command(statement_path, header_path, output_root)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("ab") as log:
        process = subprocess.Popen(
            command,
            cwd=REPO,
            env=process_env(),
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    payload = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "supervisor_every_rounds": 1,
        "target": {
            "slug": SLUG,
            "pid": process.pid,
            "target_theorem": TARGET_THEOREM,
            "workspace": str(WORKSPACE),
            "target_file": str(TARGET_FILE),
            "statement_path": str(statement_path),
            "expected_target_header_path": str(header_path),
            "output_root": str(output_root),
            "log_path": str(log_path),
            "build_command": build_command(),
            "command": command,
        },
    }
    write_json(RUN_ROOT / "launch.json", payload)
    return payload


def main() -> None:
    print(json.dumps(launch(), indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
