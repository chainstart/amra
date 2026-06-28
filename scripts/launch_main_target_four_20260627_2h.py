#!/usr/bin/env python3
"""Launch a 2h round for the four active main-target proof campaigns.

This round is deliberately main-target oriented.  Each task carries both:

- the actual final theorem being pursued; and
- the current first blocker from the previous campaign.

The statements instruct the inner proof loop to justify every stage theorem by
its role in closing the final theorem, and to return route obstructions instead
of iterating local lemmas that do not move the original problem.
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
FORMAL = REPO / "amra_library" / "formal"
LATEST = REPO / "artifacts" / "open_problem_screening" / "latest"
PREVIOUS = LATEST / "prooflab_route_repair_20260626_2h"
RUN_ROOT = LATEST / "main_target_four_20260627_2h"
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


def formal_file(relative: str) -> str:
    return str(FORMAL / relative)


def build_command(relative: str) -> str:
    return f"env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean {relative}"


def command_prefix(*, lean_heavy: bool) -> list[str]:
    command: list[str] = ["timeout", f"{HARD_TIMEOUT_SECONDS}s"]
    if shutil.which("systemd-run"):
        command += [
            "systemd-run",
            "--user",
            "--scope",
            "-p",
            "MemoryMax=7G" if lean_heavy else "MemoryMax=4G",
            "-p",
            "MemorySwapMax=9G" if lean_heavy else "MemorySwapMax=5G",
            "-p",
            "CPUQuota=130%" if lean_heavy else "CPUQuota=100%",
        ]
    command += ["nice", "-n", "10"]
    if shutil.which("ionice"):
        command += ["ionice", "-c2", "-n7"]
    return command


def main_target_discipline(final_target: str) -> str:
    return f"""
## Main-target discipline

The final target for this campaign is `{final_target}`.  Do not treat a stage
lemma as success unless the report explains exactly how it plugs into the proof
of `{final_target}`.

Required in every round:
- Restate the current first blocker between the stage theorem and `{final_target}`.
- If selecting a smaller theorem, state the parent theorem it closes and the
  remaining chain to `{final_target}`.
- If a route fails, return a concrete mathematical or source-policy obstruction;
  do not keep renaming nearby local lemmas.
- Prefer route validation and theorem packages over local syntax cleanup when
  the main theorem gap is still conceptual.
"""


def common_args(target: dict[str, Any], statement_file: Path, output_root: Path) -> list[str]:
    lean_heavy = bool(target.get("lean_heavy"))
    args = [
        *command_prefix(lean_heavy=lean_heavy),
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
        target.get("mode", "proof-lab"),
        "--rounds",
        "999",
        "--time-budget",
        str(TIME_BUDGET_SECONDS),
        "--proof-attempts",
        str(target.get("proof_attempts", 4)),
        "--proof-audits",
        "1",
        "--proof-grounding-timeout",
        str(target.get("grounding_timeout", 900)),
        "--proof-attempt-timeout",
        str(target.get("attempt_timeout", 1800)),
        "--proof-audit-timeout",
        "600",
        "--formalizer-attempts",
        str(target.get("formalizer_attempts", 6)),
        "--formalizer-attempt-timeout",
        str(target.get("formalizer_attempt_timeout", 1800)),
        "--formalizer-build-timeout",
        str(target.get("formalizer_build_timeout", 900)),
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
        "--final-target-theorem",
        target["final_target"],
    ]
    initial_target = str(target.get("initial_target") or "").strip()
    if initial_target:
        args += ["--initial-target-theorem", initial_target]
    workspace = str(target.get("workspace") or "").strip()
    if workspace:
        args += ["--workspace", workspace]
    target_file = str(target.get("target_file") or "").strip()
    if target_file:
        args += ["--target-file", target_file]
    command = str(target.get("build_command") or "").strip()
    if command:
        args += ["--build-command", command]
    for context in target.get("contexts", []):
        args += ["--context-file", context]
    for completed in target.get("completed", []):
        args += ["--completed-target-theorem", completed]
    return args


def build_targets() -> list[dict[str, Any]]:
    wowii16_summary = (
        PREVIOUS
        / "runs/wowii16-radius-tails-main-prooflab/wowii16-radius-tails-main-prooflab-2h/summary.md"
    )
    crystals_summary = (
        PREVIOUS
        / "runs/crystals-abz-descent-certificate-prooflab/crystals-abz-descent-certificate-prooflab-2h/summary.md"
    )
    erdos1_summary = (
        PREVIOUS
        / "runs/erdos1-harper-package-prooflab/erdos1-harper-package-prooflab-2h/summary.md"
    )
    wowii198a_summary = (
        PREVIOUS
        / "runs/wowii198a-minimal-intersection-fan-prooflab/wowii198a-minimal-intersection-fan-prooflab-2h/summary.md"
    )

    return [
        {
            "priority": 1,
            "slug": "wowii16-main-conjecture-route-audit",
            "problem_id": "formal-conjectures-conjecture16",
            "final_target": "conjecture16",
            "initial_target": "central_deficit_decoupled_base_oriented_component_shadow_local_capacity_from_base_parity",
            "mode": "proof-lab",
            "round_time_budget": 5400,
            "proof_attempts": 4,
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean"
            ),
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean"
            ),
            "completed": [
                "central_deficit_component_shadow_coloring_certificate",
                "central_deficit_component_shadow_coloring_from_safe_pool_hall",
                "central_deficit_component_shadow_coloring_from_component_capacity",
                "central_deficit_base_compatible_diametral_repair_obstruction",
            ],
            "statement": f"""
# WOWII16: prove the original Conjecture 16

Final theorem: `conjecture16`.

Current hard branch: connected finite graph, radius greater than two, and the
diameter branch does not already imply the lower bound for `b G`.

Current first blocker:
`central_deficit_decoupled_base_oriented_component_shadow_local_capacity_from_base_parity`.

Use this round to validate or refute the decoupled-base route as a route to the
original theorem.  The same-base diametral repair route is already obstructed by
`central_deficit_base_compatible_diametral_repair_obstruction`, so do not return
to it.

Required output:
- State the exact bridge from the decoupled-base theorem to the small-diameter
  branch of `conjecture16`, including what remains after this blocker.
- Define the two-base package explicitly: base vertex `b` for the independent
  neighbor data, diameter or geodesic path `p : G.Walk u w`, off-path
  components, assigned central shadows, and safe pools `B0/B1`.
- Audit shadow cover, component-local capacity, inter-component disjointness,
  same-color independence, distance thresholds from `b`, and forbidden
  adjacencies to `insert b P0` and `A union P1`.
- If the route fails, produce a finite obstruction specification precise enough
  to formalize; if it survives, output the Lean-ready theorem package and its
  proof chain to `conjecture16`.

{main_target_discipline("conjecture16")}
""",
            "contexts": existing(
                wowii16_summary,
                PREVIOUS
                / "runs/wowii16-radius-tails-main-prooflab/wowii16-radius-tails-main-prooflab-2h/supervisor/round-006/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore_proof_notes.md",
                RESOURCES,
            ),
        },
        {
            "priority": 2,
            "slug": "crystals-components-unique-main-descent",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "final_target": "crystals_components_unique",
            "initial_target": "odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ",
            "mode": "proof-lab",
            "round_time_budget": 3600,
            "proof_attempts": 4,
            "lean_heavy": True,
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean"
            ),
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean"
            ),
            "completed": [
                "odd_cross_halfShift_gap_AB_from_edges",
                "odd_cross_halfShift_gap_AB_add_ab_eq_YZ",
                "odd_cross_halfShift_gap_Y_dvd_AB_iff_Y_dvd_ab",
                "odd_cross_halfShift_gap_Z_quotient_data",
            ],
            "statement": f"""
# Crystals: prove the original components-unique target

Final theorem: `crystals_components_unique` from the arXiv 1601.03081 crystal
components uniqueness problem.

The local Lean staging file reduces the source problem to a Vieta/descent
arithmetic core for `IsCrystalWithComponents`.

Current first blocker:
`odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ`.

Required output:
- Explain the chain from this AB/Z divisibility blocker back to
  `no_odd_vieta_solution`, then to the source `crystals_components_unique`
  statement.  If a chain step is missing, identify it explicitly.
- Either prove or package the direct primitive bridge
  `odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ` from
  `odd_cross_halfShift_gap_Y_dvd_AB_iff_Y_dvd_ab`,
  `odd_cross_halfShift_gap_AB_add_ab_eq_YZ`, and
  `odd_cross_halfShift_gap_Z_quotient_data`; or replace it with a strictly
  better descent theorem that directly closes the same parent blocker.
- Do not use late contradiction wrappers such as `normalized_quotient_descent`,
  `normalized_common_M_descent`, `pre_common_M_obstruction`,
  later factor-2 wrappers, or `halfShift_cross_AB_Z_obstruction` unless the
  report proves that they are upstream of the main theorem rather than circular.

{main_target_discipline("crystals_components_unique")}
""",
            "contexts": existing(
                crystals_summary,
                PREVIOUS
                / "runs/crystals-abz-descent-certificate-prooflab/crystals-abz-descent-certificate-prooflab-2h/supervisor/round-003/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Subsets/FC100OpenSet1.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
                RESOURCES,
            ),
        },
        {
            "priority": 3,
            "slug": "erdos1-main-harper-source-transfer",
            "problem_id": "erdos-problem-1",
            "final_target": "erdos_1",
            "initial_target": "harper_boolean_halfInitialSegment_minimizes_closedNeighborhood_source",
            "mode": "proof-lab",
            "round_time_budget": 3600,
            "proof_attempts": 4,
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1HarperVertexBoundaryScratch.lean"
            ),
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1HarperVertexBoundaryScratch.lean"
            ),
            "completed": [
                "boolean_halfInitialSegment_card",
                "boolean_halfInitialSegment_closedNeighborhood_card",
                "boolean_boundary_card_ge_middle_of_closed_neighborhood",
            ],
            "statement": f"""
# Erdos1: prove the original sum-distinct lower bound

Final theorem: `erdos_1`.

Current first blocker:
`harper_boolean_halfInitialSegment_minimizes_closedNeighborhood_source`.

The Boolean boundary work is only useful if it is connected to the original
sum-distinct statement.  This round must not merely restate Harper; it must
either provide the source package and transfer chain to `erdos_1`, or explain
why the current route cannot be admitted under the source policy.

Required output:
- State the exact external Harper/Raty closed-neighborhood minimization theorem
  needed in Lean terms, including the even-dimensional half initial segment.
- Show how the verified counting lemmas imply the Boolean half-family boundary
  lower bound.
- State the transfer from Boolean subset-sum boundary expansion to the
  `IsSumDistinctSet A N` lower bound in `erdos_1`, including the remaining
  constants/asymptotic gaps.
- If the source theorem cannot be imported or declared, freeze the route with a
  precise source-policy obstruction rather than continuing local boundary work.

{main_target_discipline("erdos_1")}
""",
            "contexts": existing(
                erdos1_summary,
                PREVIOUS
                / "runs/erdos1-harper-package-prooflab/erdos1-harper-package-prooflab-2h/supervisor/round-009/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1_boolean_boundary_proof_notes.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1HarperVertexBoundaryScratch.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1_halfcube_notes.md",
                RESOURCES,
            ),
        },
        {
            "priority": 4,
            "slug": "wowii198a-main-fan-to-traceable",
            "problem_id": "formal-conjectures-conjecture198a",
            "final_target": "conjecture198a",
            "initial_target": "terminal_set_fan_splice_descent_left_of_hsep",
            "mode": "proof-lab",
            "round_time_budget": 3600,
            "proof_attempts": 4,
            "lean_heavy": True,
            "workspace": str(FORMAL),
            "target_file": formal_file(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"
            ),
            "build_command": build_command(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"
            ),
            "completed": [
                "exists_terminal_set_endpoint_avoiding_pair",
                "terminalPathPairWeightedMeasure_lt_of_commonCard_lt",
            ],
            "statement": f"""
# WOWII198a: prove the original traceability theorem

Final theorem: `conjecture198a`.

Current proof chain in the staging file goes through a Chvatal-Erdos style
traceability theorem:
`chvatal_erdos_connected_delete_connected_indepNum_le_three_traceable`, then
the source bridge to `conjecture198a`.

Current first blocker:
`terminal_set_fan_splice_descent_left_of_hsep`.

Required output:
- Explain the chain from the terminal-set fan lemma to the two-fan theorem,
  then to longest-path missed-vertex contradiction, then to
  `conjecture198a`.
- Prove or package the left splice descent with `hsep` and weighted-measure
  minimality: when a replacement path introduces a new non-apex intersection,
  construct a pair with smaller common support or strictly smaller weighted
  measure.
- State the symmetric right splice theorem or show how it follows by reversal.
- Do not return to the old singleton-path OR theorem unless the new statement
  explicitly handles newly introduced intersections.

{main_target_discipline("conjecture198a")}
""",
            "contexts": existing(
                wowii198a_summary,
                PREVIOUS
                / "runs/wowii198a-minimal-intersection-fan-prooflab/wowii198a-minimal-intersection-fan-prooflab-2h/supervisor/round-003/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
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
                "final_target": target["final_target"],
                "initial_target": target.get("initial_target", ""),
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
