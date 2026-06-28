#!/usr/bin/env python3
"""Launch a 2h proof-lab route-repair round after restart_four_20260625_2h.

Priority:
1. WOWII16: continue the promising central-deficit route, now focused on the
   real geometric/source theorem after three verified bridge lemmas.
2. Crystals, Erdos1, WOWII198a: proof-lab only route repair. They should return
   checkable theorem packages before more Lean formalizer work.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
LATEST = REPO / "artifacts" / "open_problem_screening" / "latest"
PREVIOUS = LATEST / "restart_four_20260625_2h"
RUN_ROOT = LATEST / "prooflab_route_repair_20260626_2h"
RESOURCES = LATEST / "resources_20260626_next_round.json"

TIME_BUDGET_SECONDS = 2 * 60 * 60
HARD_TIMEOUT_SECONDS = TIME_BUDGET_SECONDS + 10 * 60


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def existing(*paths: str | Path) -> list[str]:
    found: list[str] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO / path
        if path.exists():
            found.append(str(path))
    return found


def command_prefix() -> list[str]:
    command: list[str] = ["timeout", f"{HARD_TIMEOUT_SECONDS}s"]
    if shutil.which("systemd-run"):
        command += [
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
    command += ["nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


def common_args(target: dict[str, Any], statement_file: Path, output_root: Path) -> list[str]:
    args = [
        *command_prefix(),
        sys.executable,
        "run.py",
        "run-campaign-loop",
        "--statement-file",
        str(statement_file),
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
        "--proof-attempts",
        str(target.get("proof_attempts", 3)),
        "--proof-audits",
        "1",
        "--proof-grounding-timeout",
        str(target.get("grounding_timeout", 900)),
        "--proof-attempt-timeout",
        str(target.get("attempt_timeout", 1800)),
        "--proof-audit-timeout",
        "600",
        "--supervisor-backend",
        "codex",
        "--supervisor-every-rounds",
        "1",
        "--supervisor-timeout",
        "600",
        "--math-tools-profile",
        "essential",
        "--no-install-missing-math-tools",
        "--no-math-tool-smoke",
        "--output-root",
        str(output_root),
        "--run-name",
        f"{target['slug']}-2h",
        "--reasoning-effort",
        "high",
        "--round-time-budget",
        str(target.get("round_time_budget", 3600)),
    ]
    for context in target.get("contexts", []):
        args += ["--context-file", context]
    for completed in target.get("completed", []):
        args += ["--completed-target-theorem", completed]
    return args


def build_targets() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "slug": "wowii16-radius-tails-main-prooflab",
            "problem_id": "formal-conjectures-conjecture16",
            "proof_attempts": 4,
            "round_time_budget": 5400,
            "statement": """
# WOWII16 main route: oriented component shadows and local capacity

Continue from `restart_four_20260625_2h`, where three bridge lemmas were Lean
verified:
`central_deficit_component_shadow_coloring_certificate`,
`central_deficit_component_shadow_coloring_from_safe_pool_hall`, and
`central_deficit_component_shadow_coloring_from_component_capacity`.

Proof-lab task: produce the exact theorem package for
`central_deficit_oriented_component_shadow_local_capacity_from_base_parity`.

Required output:
- Define the actual off-path components of `p.support.toFinset`.
- Define oriented/assigned central-index shadows, not raw overlapping shadows.
- Define base parity data `P0`, `P1`, and `A`, and safe pools `B0/B1`.
- Prove or source-audit local capacity for each component, shadow cover of
  `D = Finset.Icc (e - r + 2) (r - 1)`, inter-component candidate disjointness,
  same-color independence, distance thresholds, and base forbidden adjacencies.
- Decide whether repeated radius witnesses and overlapping tails break the
  component-local capacity theorem. If they do, return a finite/source
  obstruction instead of a Lean target.

Do not retarget the already verified Hall/certificate bridge lemmas.
""",
            "completed": [
                "central_deficit_component_shadow_coloring_certificate",
                "central_deficit_component_shadow_coloring_from_safe_pool_hall",
                "central_deficit_component_shadow_coloring_from_component_capacity",
            ],
            "contexts": existing(
                PREVIOUS / "runs/wowii16-central-deficit-prooflab/wowii16-central-deficit-prooflab-2h/summary.md",
                PREVIOUS / "runs/wowii16-central-deficit-prooflab/wowii16-central-deficit-prooflab-2h/supervisor/round-009/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore_proof_notes.md",
                RESOURCES,
            ),
        },
        {
            "priority": 2,
            "slug": "crystals-abz-descent-certificate-prooflab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "statement": """
# Crystals AB/Z descent certificate

Continue proof-lab route repair for the blocker in
`odd_cross_halfShift_gap_exact_factor2_edges_obstruction_core`.

Required output: a concrete theorem-level certificate before any more Lean work.
Produce either:
- an explicit descent-step lemma constructing smaller odd parameters
  `h' u' H' U'` or equivalent with preserved AB/Z or exact-triple hypotheses
  and a strict measure decrease such as `h' * u' < h * u`; or
- a direct primitive proof of the halved AB/Z obstruction.

Do not propose wrapper-only targets. Do not use `normalized_quotient_descent`,
`normalized_common_M_descent`, `pre_common_M_obstruction`, later factor-2
wrappers, or the late `halfShift_cross_AB_Z_obstruction` alias route.
""",
            "contexts": existing(
                PREVIOUS / "runs/crystals-factor2-edges-core-lean/crystals-factor2-edges-core-lean-2h/summary.md",
                PREVIOUS / "runs/crystals-factor2-edges-core-lean/crystals-factor2-edges-core-lean-2h/supervisor/round-006/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
                RESOURCES,
            ),
        },
        {
            "priority": 3,
            "slug": "erdos1-harper-package-prooflab",
            "problem_id": "erdos-problem-1",
            "statement": """
# Erdos1 Harper transfer package repair

Continue proof-lab source/theorem-package repair. The next useful output is not
local boundary algebra; it is a precise Harper/Raty package.

Required output:
- Define the actual simplicial-order half initial segment/minimizer in Lean
  terms, including the even-dimensional middle-layer half.
- State the closed-neighborhood cardinal theorem for that segment.
- State the Harper/Raty minimization theorem that carries the external content.
- Prove on paper how these imply
  `boolean_half_family_closedNeighborhood_card_ge_middle`, then
  `boolean_half_family_vertexBoundary_card_ge_middle`.
- Identify exactly which declaration should contain the external Harper/Raty
  theorem content and record source provenance.

Do not revisit Sperner/LYM shortcuts, SCD separator routes, complement-dual
routes, or wrapper-only renamings.
""",
            "contexts": existing(
                PREVIOUS
                / "runs/erdos1-harper-vertex-boundary-scratch-lean/erdos1-harper-vertex-boundary-scratch-lean-2h/summary.md",
                PREVIOUS
                / "runs/erdos1-harper-vertex-boundary-scratch-lean/erdos1-harper-vertex-boundary-scratch-lean-2h/supervisor/round-014/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1HarperVertexBoundaryScratch.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1_halfcube_notes.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean",
                RESOURCES,
            ),
        },
        {
            "priority": 4,
            "slug": "wowii198a-minimal-intersection-fan-prooflab",
            "problem_id": "formal-conjectures-conjecture198a",
            "statement": """
# WOWII198a terminal-set fan augmentation repair

Continue proof-lab route repair for
`terminal_set_fan_augmentation_from_endpoint_avoiding_pair`.

The previous singleton-path replacement lemma is too weak: a replacement path
can introduce a new non-apex intersection. Design a corrected theorem-level
blocker that either:
- carries the full terminal-set `hsep` through the rerouting step; or
- states a genuine finite minimal-intersection principle with an explicit
  measure showing the replacement pair has fewer non-apex common support
  vertices.

Required output: exact Lean declaration for the corrected reduction lemma and
a proof sketch explaining why newly introduced intersections can be eliminated.
Do not retry the old OR theorem, public wrappers, or
`terminal_set_fan_intersection_reduction_from_singleton_path` unchanged.
""",
            "contexts": existing(
                PREVIOUS
                / "runs/wowii198a-side-fan-spec-repair-prooflab/wowii198a-side-fan-spec-repair-prooflab-2h/summary.md",
                PREVIOUS
                / "runs/wowii198a-side-fan-spec-repair-prooflab/wowii198a-side-fan-spec-repair-prooflab-2h/supervisor/round-004/decision.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost_formalizer_notes.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost_proof_notes.md",
                RESOURCES,
            ),
        },
    ]


def prepare_target(target: dict[str, Any]) -> dict[str, Any]:
    statement_file = RUN_ROOT / "statements" / f"{target['priority']:02d}-{target['slug']}.md"
    output_root = RUN_ROOT / "runs" / target["slug"]
    log_path = RUN_ROOT / "logs" / f"{target['priority']:02d}-{target['slug']}.log"
    write_text(statement_file, target["statement"])
    command = common_args(target, statement_file, output_root)
    return {
        **target,
        "statement_file": str(statement_file),
        "output_root": str(output_root),
        "log_path": str(log_path),
        "command": command,
    }


def start_process(target: dict[str, Any]) -> subprocess.Popen[bytes]:
    log_path = Path(target["log_path"])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(
        {
            "LEAN_NUM_THREADS": "1",
            "OMP_NUM_THREADS": "1",
            "ARA_MATH_BACKEND_MAX_MEMORY_MB": "4096",
            "ARA_GLOBAL_SUPERVISOR_BACKEND_MAX_MEMORY_MB": "4096",
            "ARA_MATH_MIN_AVAILABLE_MEMORY_MB": "1024",
            "ARA_MATH_MAX_LOAD_PER_CPU": "140",
            "ARA_MATH_SYSTEM_WAIT_SECONDS": "5",
        }
    )
    with log_path.open("ab") as log:
        proc = subprocess.Popen(
            target["command"],
            cwd=REPO,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            env=env,
        )
    write_text(RUN_ROOT / "pids" / f"{target['priority']:02d}-{target['slug']}.pid", str(proc.pid))
    return proc


def active_status(active: list[tuple[dict[str, Any], subprocess.Popen[bytes]]]) -> list[dict[str, Any]]:
    return [{"slug": target["slug"], "pid": proc.pid} for target, proc in active]


def write_driver_status(status: dict[str, Any]) -> None:
    status["updated_at"] = utc_now()
    write_json(RUN_ROOT / "driver_status.json", status)


def run_driver() -> None:
    pending = [prepare_target(target) for target in build_targets()]
    active: list[tuple[dict[str, Any], subprocess.Popen[bytes]]] = []
    completed: list[dict[str, Any]] = []
    status: dict[str, Any] = {
        "driver_pid": os.getpid(),
        "started_at": utc_now(),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "hard_timeout_seconds": HARD_TIMEOUT_SECONDS,
        "pending": [target["slug"] for target in pending],
        "active": [],
        "completed": [],
    }
    write_driver_status(status)
    while pending or active:
        while pending:
            target = pending.pop(0)
            active.append((target, start_process(target)))
        still_active: list[tuple[dict[str, Any], subprocess.Popen[bytes]]] = []
        for target, proc in active:
            code = proc.poll()
            if code is None:
                still_active.append((target, proc))
            else:
                completed.append(
                    {
                        "slug": target["slug"],
                        "returncode": code,
                        "completed_at": utc_now(),
                        "log_path": target["log_path"],
                        "output_root": target["output_root"],
                    }
                )
        active = still_active
        status["pending"] = [target["slug"] for target in pending]
        status["active"] = active_status(active)
        status["completed"] = completed
        write_driver_status(status)
        if pending or active:
            time.sleep(20)
    status["finished_at"] = utc_now()
    write_driver_status(status)


def launch_driver() -> dict[str, Any]:
    for subdir in ("statements", "logs", "pids", "runs"):
        (RUN_ROOT / subdir).mkdir(parents=True, exist_ok=True)
    targets = [prepare_target(target) for target in build_targets()]
    manifest = {
        "generated_at": utc_now(),
        "run_root": str(RUN_ROOT),
        "time_budget_seconds": TIME_BUDGET_SECONDS,
        "hard_timeout_seconds": HARD_TIMEOUT_SECONDS,
        "targets": [
            {
                "priority": target["priority"],
                "slug": target["slug"],
                "problem_id": target["problem_id"],
                "statement_file": target["statement_file"],
                "output_root": target["output_root"],
                "log_path": target["log_path"],
                "context_count": len(target.get("contexts", [])),
                "completed": target.get("completed", []),
                "command": target["command"],
            }
            for target in targets
        ],
    }
    write_json(RUN_ROOT / "manifest.json", manifest)
    driver_log = RUN_ROOT / "logs" / "driver.log"
    with driver_log.open("ab") as log:
        proc = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--driver"],
            cwd=REPO,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    write_text(RUN_ROOT / "pids" / "driver.pid", str(proc.pid))
    manifest["driver_pid"] = proc.pid
    manifest["driver_log"] = str(driver_log)
    write_json(RUN_ROOT / "manifest.json", manifest)
    return manifest


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--driver":
        run_driver()
        return
    manifest = launch_driver()
    print(json.dumps({"run_root": manifest["run_root"], "driver_pid": manifest["driver_pid"]}, indent=2))


if __name__ == "__main__":
    main()
