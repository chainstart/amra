#!/usr/bin/env python3
"""Launch the 2026-06-28 2h continuation for the three main targets.

This round starts from ``main_target_three_20260627_next2_fixed_2h`` and
removes targets that the prior supervisor marked as cyclic or mis-specified.
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
BASE_PATH = REPO / "scripts" / "launch_main_target_four_20260627_2h.py"
spec = importlib.util.spec_from_file_location("main_target_four_base", BASE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load base launcher from {BASE_PATH}")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

base.PREVIOUS = base.LATEST / "main_target_three_20260627_next2_fixed_2h"
base.RUN_ROOT = base.LATEST / "main_target_three_20260628_next_2h"
base.TIME_BUDGET_SECONDS = 2 * 60 * 60
base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 10 * 60


def build_targets() -> list[dict[str, Any]]:
    previous = base.PREVIOUS / "runs"

    wowii16_run = (
        previous
        / "wowii16-dist-two-exchange-prooflab"
        / "wowii16-dist-two-exchange-prooflab-2h"
    )
    crystals_run = (
        previous
        / "crystals-mixed-abz-primepower-prooflab"
        / "crystals-mixed-abz-primepower-prooflab-2h"
    )
    wowii198a_run = (
        previous
        / "wowii198a-extremal-bad-pivot-lean"
        / "wowii198a-extremal-bad-pivot-lean-2h"
    )

    return [
        {
            "priority": 1,
            "slug": "wowii16-harvest-or-collision-prooflab",
            "problem_id": "formal-conjectures-conjecture16",
            "final_target": "conjecture16",
            "initial_target": "central_deficit_same_side_blocker_harvests_replacement_or_path_fixed_collision",
            "mode": "proof-lab",
            "round_time_budget": 3600,
            "proof_attempts": 5,
            "workspace": str(base.FORMAL),
            "target_file": base.formal_file(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean"
            ),
            "build_command": base.build_command(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean"
            ),
            "completed": [
                "central_deficit_dist_two_left_reserve_rebalance_forces_lex_improvement",
                "central_deficit_c6_exists_diametral_safe_candidate_data_disjoint",
                "central_deficit_exists_diametral_safe_candidate_data_disjoint_of_untagged",
                "central_deficit_exists_diametral_safe_candidate_data_disjoint_of_exists_untagged",
                "central_deficit_decoupled_assigned_radius_tail_component_safe_hall_of_exists_disjoint_candidate_data",
                "central_deficit_component_shadow_coloring_from_component_capacity",
            ],
            "statement": f"""
# WOWII16 next attack: harvest-or-collision for failed compatibility

Final theorem: `conjecture16`.

Current first blocker:
`central_deficit_exists_diametral_safe_candidate_data_disjoint_selector`.

Immediate target:
`central_deficit_same_side_blocker_harvests_replacement_or_path_fixed_collision`.

The dist-two branch is settled.  Do not retarget
`central_deficit_dist_two_left_reserve_rebalance_forces_lex_improvement`, and
do not use the Round-4 macro/vacuous same-side theorem as mathematical
evidence.

Required output:
- Define the exact `PathFixedCollision` alternative needed by the selector
  proof.  It must be strong enough to contradict the selected diametral path
  and fixed-package data, not just name a local obstruction.
- Prove or make Lean-ready the real harvest theorem: under old admissibility,
  selected path/demand data, fresh/off-path/fixed-disjoint `x`, `G.dist b x = 2`,
  and one failed branch among `exists q in Q0, G.Adj x q`, `not hBLeft`, or
  `not hBQ1`, conclude either explicit replacement data `S,C` or the named
  `PathFixedCollision`.
- Replacement data must feed the utility theorem:
  `S <= A`, `C` neighbors `b`, `C` independent, disjoint/cross-nonadjacent from
  `A \\ S`, and `S.card < C.card` imply a larger independent neighbor set.
- Explain exactly how this bad-branch theorem joins the verified dist-two good
  branch to prove `central_deficit_lexmax_safe_pool_deficit_forces_improvement_or_neighbor_gain`.
- Then state how lexmax plus maximality of `A` closes the selector and the
  existing wrapper/Hall/component-capacity/small-diameter chain to `conjecture16`.

If raw compatibility failure is too weak, report the concrete missing global
condition; do not restate a theorem that raw failure directly gives neighbor
gain.

{base.main_target_discipline("conjecture16")}
""",
            "contexts": base.existing(
                wowii16_run / "summary.md",
                wowii16_run / "supervisor/round-007/decision.md",
                wowii16_run / "proof_lab/round-007/summary.md",
                wowii16_run / "proof_lab/round-007/attempts/attempt_003_output.md",
                wowii16_run / "proof_lab/round-007/attempts/attempt_004_output.md",
                wowii16_run / "proof_lab/round-007/grounding/source_grounding_output.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore_proof_notes.md",
                base.RESOURCES,
            ),
        },
        {
            "priority": 2,
            "slug": "crystals-mixed-abz-coverage-prooflab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "final_target": "crystals_components_unique",
            "initial_target": "odd_cross_halfShift_gap_primepow_coverage_of_exact_halved_ABZ_canonicalSquareKernel",
            "mode": "proof-lab",
            "round_time_budget": 3600,
            "proof_attempts": 5,
            "lean_heavy": True,
            "workspace": str(base.FORMAL),
            "target_file": base.formal_file(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean"
            ),
            "build_command": base.build_command(
                "AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean"
            ),
            "completed": [
                "isCrystalWithComponents_halfShift_admissible",
                "no_odd_vieta_solution",
                "no_odd_vieta_solution_exists",
                "odd_cross_halfShift_gap_AB_add_ab_eq_YZ",
                "odd_cross_halfShift_gap_Y_dvd_AB_iff_Y_dvd_ab",
                "odd_cross_halfShift_gap_AB_from_edges",
                "odd_cross_halfShift_gap_Z_quotient_data",
                "odd_cross_halfShift_gap_exact_factor2_edges_obstruction_core",
            ],
            "statement": f"""
# Crystals next attack: mixed AB/Z prime-power coverage

Final theorem: `crystals_components_unique`.

Current first blocker:
`odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ`, through the disallowed
parent `odd_cross_halfShift_gap_Y_dvd_ab_mul_Z_quotient_of_exact_halved_ABZ`.

Immediate target:
`odd_cross_halfShift_gap_primepow_coverage_of_exact_halved_ABZ_canonicalSquareKernel`
or an explicit strict `BadPrimePowerABZ` descent replacing it.

Required output:
- Do not send the no-unit theorem, parity-only wrappers, or abstract
  `BadPrimePowerABZ -> exists smaller BadPrimePowerABZ` to Lean.
- Either prove a sourced mixed AB/Z square-kernel/descent theorem giving
  `Nat.Prime p -> 0 < e -> p^e | Y -> p^e | a*b*kZ`, or provide concrete Nat
  formulas for primed witnesses preserving the full exact halved AB/Z package.
- A valid descent certificate must preserve `(Y - 1)^2 = Z*kZ`,
  `Nat.Coprime Y kZ`, canonical square-kernel data, the same bad prime-power
  defect, and prove `Y' < Y`.
- The certificate must feed
  `odd_cross_halfShift_gap_Y_dvd_ab_mul_Z_quotient_of_exact_halved_ABZ`, then
  `odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ`, then the obstruction
  core, then `no_odd_vieta_solution` / `no_odd_vieta_solution_exists`, and
  finally the integration bridge to `crystals_components_unique`.
- If the needed square-kernel/descent theorem is not available from source or
  algebra, report the exact obstruction and the smallest additional global
  certificate that would be enough.

Do not use normalized/common-M, `pre_common_M`, later factor-2 wrappers,
`halfShift_cross_AB_Z_obstruction`, or upstream `False.elim`.

{base.main_target_discipline("crystals_components_unique")}
""",
            "contexts": base.existing(
                crystals_run / "summary.md",
                crystals_run / "supervisor/round-006/decision.md",
                crystals_run / "proof_lab/round-006/summary.md",
                crystals_run / "proof_lab/round-006/attempts/attempt_003_output.md",
                crystals_run / "proof_lab/round-006/attempts/attempt_004_output.md",
                crystals_run / "proof_lab/round-006/grounding/source_grounding_output.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
                base.RESOURCES,
            ),
        },
        {
            "priority": 3,
            "slug": "wowii198a-left-prefix-residual-lean",
            "problem_id": "formal-conjectures-conjecture198a",
            "final_target": "conjecture198a",
            "initial_target": "terminal_set_fan_left_suffix_retention_left_prefix_residual_bad_false",
            "mode": "lean-formalizer",
            "round_time_budget": 3600,
            "formalizer_attempts": 6,
            "formalizer_attempt_timeout": 1800,
            "formalizer_build_timeout": 1200,
            "lean_heavy": True,
            "workspace": str(base.FORMAL),
            "target_file": base.formal_file(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"
            ),
            "build_command": base.build_command(
                "AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean"
            ),
            "completed": [
                "exists_terminal_set_endpoint_avoiding_pair",
                "terminalPathPairWeightedMeasure_lt_of_commonCard_lt",
                "terminal_set_fan_left_first_crossing_splice_commonCard_lt_of_not_retained",
            ],
            "statement": f"""
# WOWII198a next attack: left-prefix residual under extremality

Final theorem: `conjecture198a`.

Current first blocker:
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`.

Immediate Lean target:
`terminal_set_fan_left_suffix_retention_left_prefix_residual_bad_false`.

The isolated weighted fallback target is mis-specified.  It lacks the
`hlast_bad` / no-later-bad control needed for later `rs.dropUntil` vertices
that meet `altRight`.  Work under the residual helper, or introduce only a
private helper that carries the same extremal hypothesis.

Required output:
- Prove the residual helper with `hlast_bad`.
- In the `hy_not_alt` branch, do not try to prove a standalone support-length
  descent from the old local hypotheses; a sequence probe showed that route is
  false as stated.
- Instead use last-bad extremality to control vertices of `rs.dropUntil z`
  meeting `altRight`, then prove either strict common-card descent for the
  fallback pair or the valid weighted-minimality contradiction available under
  the residual hypotheses.
- After this passes, wire it into
  `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent`, then
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`.
- Every report must state the chain to
  `terminal_set_fan_left_suffix_retention_alt_intersections_control`,
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, the splice
  descent chain, the two-fan theorem, Chvatal-Erdos traceability, and finally
  `conjecture198a`.

Run and pass:
`env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.
""",
            "contexts": base.existing(
                wowii198a_run / "summary.md",
                wowii198a_run / "supervisor/round-003/decision.md",
                wowii198a_run
                / "lean_formalizer/round-003-terminal-set-fan-left-suffix-retention-left-prefix-weighted-fallback-false/summary.md",
                wowii198a_run
                / "lean_formalizer/round-003-terminal-set-fan-left-suffix-retention-left-prefix-weighted-fallback-false/attempts/attempt_005/attempt_report.json",
                wowii198a_run
                / "lean_formalizer/round-003-terminal-set-fan-left-suffix-retention-left-prefix-weighted-fallback-false/attempts/attempt_005/backend_last_message.txt",
                wowii198a_run
                / "lean_formalizer/round-003-terminal-set-fan-left-suffix-retention-left-prefix-weighted-fallback-false/attempts/attempt_006/attempt_report.json",
                wowii198a_run
                / "lean_formalizer/round-003-terminal-set-fan-left-suffix-retention-left-prefix-weighted-fallback-false/attempts/attempt_006/backend_last_message.txt",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost_formalizer_notes.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost_proof_notes.md",
                base.RESOURCES,
            ),
        },
    ]


base.build_targets = build_targets


def launch_driver() -> dict[str, Any]:
    for subdir in ("statements", "logs", "pids", "runs"):
        (base.RUN_ROOT / subdir).mkdir(parents=True, exist_ok=True)
    targets = [base.prepare_target(target) for target in build_targets()]
    manifest = {
        "generated_at": base.utc_now(),
        "run_root": str(base.RUN_ROOT),
        "time_budget_seconds": base.TIME_BUDGET_SECONDS,
        "hard_timeout_seconds": base.HARD_TIMEOUT_SECONDS,
        "targets": [
            {
                "priority": target["priority"],
                "slug": target["slug"],
                "problem_id": target["problem_id"],
                "final_target": target["final_target"],
                "initial_target": target.get("initial_target", ""),
                "mode": target.get("mode", ""),
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
    base.write_json(base.RUN_ROOT / "manifest.json", manifest)
    driver_log = base.RUN_ROOT / "logs" / "driver.log"
    with driver_log.open("ab") as log:
        proc = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "--driver"],
            cwd=base.REPO,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    base.write_text(base.RUN_ROOT / "pids" / "driver.pid", str(proc.pid))
    manifest["driver_pid"] = proc.pid
    manifest["driver_log"] = str(driver_log)
    base.write_json(base.RUN_ROOT / "manifest.json", manifest)
    return manifest


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--driver":
        base.run_driver()
        return
    manifest = launch_driver()
    print(json.dumps({"run_root": manifest["run_root"], "driver_pid": manifest["driver_pid"]}, indent=2))


if __name__ == "__main__":
    main()
