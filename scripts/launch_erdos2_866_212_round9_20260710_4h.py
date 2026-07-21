#!/usr/bin/env python3
"""Launch two faithful four-hour supervised Lean campaigns for Erdos #866/#212."""

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
RUN_ROOT = REPO / "artifacts/open_problem_screening/latest/erdos2_866_212_round9_20260710_4h"
TIME_BUDGET_SECONDS = 4 * 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 15 * 60


ERDOS866_STATEMENT = """\
# Erdos #866: finite equal-sum triple-pair extraction

Prove the exact Lean theorem
`ces75_open_dyadic_even_equal_sum_six_pair_count_stage` in
`MathProject/ErdosProblem866Core.lean`.

This is the repaired first formalization blocker in the CES75 residual
central-even branch.  The earlier square-root interface without `0 < n1` was
false at `n1 = 0`; do not retry or weaken that theorem.  This target instead
assumes the exact unordered-pair count needed for the pigeonhole argument.

Required route:
- count unordered pairs of distinct elements of `B`;
- map each pair to its even sum in the interval `(2*n1, 4*n1)`;
- use the strict pair-count hypothesis to obtain three representations of one
  sum;
- prove distinct equal-sum unordered pairs are disjoint;
- sort the six endpoints and use the existing ordered/symmetric-pair lemmas to
  obtain the requested `z1,...,z6` order.

Use the configured single-file verifier only.  Intermediate local lemmas are
allowed, but the final declaration must match the expected target header.
Do not add `sorry`, `admit`, axioms, constants, opaque declarations, source
markers, or new trusted assumptions.  The supervisor must review every round
and retarget only to faithful intermediate lemmas that lead back to this exact
theorem.
"""


ERDOS866_HEADER = """\
theorem ces75_open_dyadic_even_equal_sum_six_pair_count_stage
    (A B : Finset Int) (n1 : Nat)
    (hBA : B ⊆ A)
    (hBeven : forall x : Int, x ∈ B -> Even x)
    (hBopen : forall x : Int, x ∈ B -> (n1 : Int) < x and x < 2 * (n1 : Int))
    (hpairCount : 2 * (n1 + 1) < B.card * (B.card - 1) / 2) :
    ∃ (z1 z2 z3 z4 z5 z6 : Int),
      z1 ∈ A and z2 ∈ A and z3 ∈ A and
      z4 ∈ A and z5 ∈ A and z6 ∈ A and
      Even z1 and Even z2 and Even z3 and
      Even z4 and Even z5 and Even z6 and
      z1 + z2 = z3 + z4 and
      z3 + z4 = z5 + z6 and
      (n1 : Int) < z5 and z5 < z3 and z3 < z1 and
      z1 < z2 and z2 < z4 and z4 < z6 and
      z6 < 2 * (n1 : Int)
"""


ERDOS212_STATEMENT = """\
# Erdos #212: line/circle finite-exception closed proper container

Prove the exact Lean theorem
`lineOrCircleUnionFinsetClosedProperContainer` in
`AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean`.

The theorem must inhabit the real proposition
`LineOrCircleUnionFinsetClosedProperContainerSource`: every subset of a real
affine line or metric circle together with a finite exceptional set is
contained in a closed proper subset of `ℂ`.

Required route:
- handle the affine-line and circle branches separately;
- prove the corresponding line/circle union finite set is closed;
- construct or obtain a point outside that union to prove properness;
- package the original subset into `ClosedProperContainer`.

Do not use or modify the `sourcePropTheorem` macro, and do not prove a marker
whose elaborated type is merely `True`.  Intermediate topology/cardinality
lemmas are allowed, but the final declaration must match the expected target
header.  Do not add `sorry`, `admit`, axioms, constants, opaque declarations,
source markers, or new trusted assumptions.  The supervisor must review every
round and keep all work directed toward this exact local theorem.
"""


ERDOS212_HEADER = """\
theorem lineOrCircleUnionFinsetClosedProperContainer :
    LineOrCircleUnionFinsetClosedProperContainerSource
"""


TARGETS: list[dict[str, Any]] = [
    {
        "slug": "erdos866-open-dyadic-pair-count",
        "target_theorem": "ces75_open_dyadic_even_equal_sum_six_pair_count_stage",
        "workspace": REPO / "projects/erdos-866-ai-continuation-20260505/formal",
        "target_file": REPO
        / "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Core.lean",
        "statement": ERDOS866_STATEMENT,
        "header": ERDOS866_HEADER,
        "contexts": [
            REPO / "artifacts/source_papers/ces75/ces75_ordered_equal_sum_six_source_certificate.md",
            REPO
            / "artifacts/source_papers/ces75/ces75_residual_central_even_to_ordered_equal_sum_six_contract.md",
            REPO / "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ProofNotes.md",
            REPO
            / "artifacts/open_problem_screening/latest/erdos2_866_212_round8_20260709_4h/source_runs/erdos866-open-dyadic-pair-count-stage-formalizer/statement.md",
        ],
    },
    {
        "slug": "erdos212-line-circle-closed-proper-container",
        "target_theorem": "lineOrCircleUnionFinsetClosedProperContainer",
        "workspace": REPO / "amra_library/formal",
        "target_file": REPO
        / "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
        "statement": ERDOS212_STATEMENT,
        "header": ERDOS212_HEADER,
        "contexts": [
            REPO / "artifacts/source_papers/abt/abt_bombieri_lang_consequence_source_certificate.md",
            REPO / "artifacts/source_papers/abt/abt_closed_proper_plane_image_source_certificate.md",
            REPO
            / "artifacts/open_problem_screening/latest/erdos2_866_212_round8_20260709_4h/source_runs/erdos212-bl-consequence/summary.md",
        ],
    },
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


def build_command(target: dict[str, Any]) -> str:
    relative = Path(target["target_file"]).resolve().relative_to(
        Path(target["workspace"]).resolve()
    )
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


def campaign_command(
    target: dict[str, Any], statement_path: Path, header_path: Path, output_root: Path
) -> list[str]:
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
        str(target["workspace"]),
        "--target-file",
        str(target["target_file"]),
        "--expected-target-header-file",
        str(header_path),
        "--build-command",
        build_command(target),
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
        str(target["target_theorem"]),
        "--final-target-theorem",
        str(target["target_theorem"]),
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
        f"{target['slug']}-supervised-4h",
        "--reasoning-effort",
        "high",
        "--max-stalled-rounds",
        "8",
    ]
    for context in target["contexts"]:
        if Path(context).exists():
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
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    env = process_env()
    launched: list[dict[str, Any]] = []
    for target in TARGETS:
        slug = str(target["slug"])
        statement_path = RUN_ROOT / "statements" / f"{slug}.md"
        header_path = RUN_ROOT / "headers" / f"{slug}.lean"
        output_root = RUN_ROOT / "runs" / slug
        log_path = RUN_ROOT / "logs" / f"{slug}.log"
        write_text(statement_path, str(target["statement"]))
        write_text(header_path, str(target["header"]))
        command = campaign_command(target, statement_path, header_path, output_root)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("ab") as log:
            process = subprocess.Popen(
                command,
                cwd=REPO,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
        launched.append(
            {
                "slug": slug,
                "pid": process.pid,
                "target_theorem": target["target_theorem"],
                "workspace": str(target["workspace"]),
                "target_file": str(target["target_file"]),
                "statement_path": str(statement_path),
                "expected_target_header_path": str(header_path),
                "output_root": str(output_root),
                "log_path": str(log_path),
                "build_command": build_command(target),
                "command": command,
            }
        )
    payload = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "supervisor_every_rounds": 1,
        "targets": launched,
    }
    write_json(RUN_ROOT / "launch.json", payload)
    return payload


def main() -> None:
    print(json.dumps(launch(), indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
