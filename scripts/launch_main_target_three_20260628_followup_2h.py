#!/usr/bin/env python3
"""Launch the 2026-06-28 follow-up 2h campaign for the three main targets.

This round starts from ``main_target_three_20260628_next_2h``.  The focus is
not to repeat recently frozen Lean targets, but to repair the next real
mathematical certificates identified by the prior supervisors.
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

base.PREVIOUS = base.LATEST / "main_target_three_20260628_next_2h"
base.RUN_ROOT = base.LATEST / "main_target_three_20260628_followup_2h"
base.TIME_BUDGET_SECONDS = 2 * 60 * 60
base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 10 * 60


def build_targets() -> list[dict[str, Any]]:
    previous = base.PREVIOUS / "runs"

    wowii16_run = (
        previous
        / "wowii16-harvest-or-collision-prooflab"
        / "wowii16-harvest-or-collision-prooflab-2h"
    )
    crystals_run = (
        previous
        / "crystals-mixed-abz-coverage-prooflab"
        / "crystals-mixed-abz-coverage-prooflab-2h"
    )
    wowii198a_run = (
        previous
        / "wowii198a-left-prefix-residual-lean"
        / "wowii198a-left-prefix-residual-lean-2h"
    )

    return [
        {
            "priority": 1,
            "slug": "wowii16-hard-selector-normal-form-prooflab",
            "problem_id": "formal-conjectures-conjecture16",
            "final_target": "conjecture16",
            "initial_target": "CentralDeficitSameSideBadBranchAbsorptionNormalForm",
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
                "central_deficit_same_side_blocker_replacement_forces_neighbor_gain",
                "central_deficit_selected_lexmax_package_no_path_fixed_collision",
                "central_deficit_same_side_bad_branch_absorption_under_hard_selector",
                "central_deficit_c6_exists_diametral_safe_candidate_data_disjoint",
                "central_deficit_exists_diametral_safe_candidate_data_disjoint_of_untagged",
                "central_deficit_exists_diametral_safe_candidate_data_disjoint_of_exists_untagged",
                "central_deficit_decoupled_assigned_radius_tail_component_safe_hall_of_exists_disjoint_candidate_data",
                "central_deficit_component_shadow_coloring_from_component_capacity",
            ],
            "statement": f"""
# WOWII16 follow-up: prove the real hard-selector normal form

Final theorem: `conjecture16`.

Current first blocker:
`central_deficit_exists_diametral_safe_candidate_data_disjoint_selector`.

Immediate proof-lab target:
`CentralDeficitSameSideBadBranchAbsorptionNormalForm`.

Verified assets now available:
- `central_deficit_dist_two_left_reserve_rebalance_forces_lex_improvement`
- `central_deficit_same_side_blocker_replacement_forces_neighbor_gain`
- `central_deficit_selected_lexmax_package_no_path_fixed_collision`
- `central_deficit_same_side_bad_branch_absorption_under_hard_selector`

The last theorem is only an assumption-to-contradiction wrapper: if
`CentralDeficitSameSideBadBranchAbsorptionNormalForm` is supplied, then bad
compatibility branches contradict maximality of `A` or selected lexmax.  The
missing theorem is non-circular construction of that normal form from the real
hard-selector/global hypotheses.

Required output:
- Do not send another Lean formalizer round until the statement is repaired.
- Do not use the old raw per-witness harvest theorem; finite C7/n=8
  counter-shapes show it is too weak.
- Define the active/tight selector-deficit witness predicate explicitly.
- State exactly which hard-selector/Hall/global hypotheses imply that every
  failed branch
  `∃ q ∈ Q0, G.Adj x q`, `¬ hBLeft`, or `¬ hBQ1`
  is charged either to `CentralDeficitReplacementCertificate G b A S C` or to
  `CentralDeficitPathFixedCollision G b A p e D P0 P1 Q0 Q1`.
- Explain how this closes
  `central_deficit_lexmax_safe_pool_deficit_forces_improvement_or_neighbor_gain`,
  then the selector, then the existing untagged/Hall/component-capacity/
  small-diameter chain to `conjecture16`.
- If the real normal form still needs an extra selector invariant, name the
  smallest invariant and provide a Lean declaration for it.

{base.main_target_discipline("conjecture16")}
""",
            "contexts": base.existing(
                wowii16_run / "summary.md",
                wowii16_run / "supervisor/round-007/decision.md",
                wowii16_run
                / "lean_formalizer/round-007-central-deficit-same-side-bad-branch-absorption-under-hard-selector/summary.md",
                wowii16_run
                / "proof_lab/round-006/summary.md",
                wowii16_run
                / "proof_lab/round-006/attempts/attempt_005_output.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore_proof_notes.md",
                base.RESOURCES,
            ),
        },
        {
            "priority": 2,
            "slug": "crystals-mixed-abz-certificate-source-prooflab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "final_target": "crystals_components_unique",
            "initial_target": "odd_cross_halfShift_gap_residual_bad_primepow_cases_impossible_of_exact_halved_ABZ_canonicalSquareKernel",
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
# Crystals follow-up: find the missing mixed AB/Z certificate

Final theorem: `crystals_components_unique`.

Current first blocker:
`odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ`, through the disallowed
ex-falso parent `odd_cross_halfShift_gap_Y_dvd_ab_mul_Z_quotient_of_exact_halved_ABZ`.

Immediate proof-lab target:
`odd_cross_halfShift_gap_residual_bad_primepow_cases_impossible_of_exact_halved_ABZ_canonicalSquareKernel`.

Do not repeat p-adic bookkeeping as the main result: prior rounds already
reduce any bad prime-power witness to unit/unit or one-sided residual cases.
Do not send coverage, no-unit, parity-only, normalized/common-M, or abstract
descent wrappers to Lean.

Required output:
- Either source/prove a theorem that full exact halved AB/Z plus canonical
  square-kernel hypotheses imply
  `Nat.Prime p -> 0 < e -> p^e ∣ Y -> p^e ∣ a*b*kZ`;
  or give explicit Nat formulas for a strict `BadPrimePowerABZ` descent.
- A descent certificate must preserve full exact AB/Z,
  `(Y' - 1)^2 = Z' * kZ'`, `Nat.Coprime Y' kZ'`, canonical square-kernel data,
  the same bad prime-power defect, and prove `Y' < Y`.
- If using a source, identify the exact statement and how it maps to local
  variables `a b h u Y kZ R S X W C`.
- If no certificate is available, freeze the branch and state the smallest
  additional global theorem needed; do not return a Lean target.

{base.main_target_discipline("crystals_components_unique")}
""",
            "contexts": base.existing(
                crystals_run / "summary.md",
                crystals_run / "supervisor/round-005/decision.md",
                crystals_run / "proof_lab/round-005/summary.md",
                crystals_run / "proof_lab/round-005/attempts/attempt_002_output.md",
                crystals_run / "proof_lab/round-005/attempts/attempt_004_output.md",
                crystals_run / "proof_lab/round-005/grounding/source_grounding_output.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
                base.RESOURCES,
            ),
        },
        {
            "priority": 3,
            "slug": "wowii198a-bypass-obstruction-prooflab",
            "problem_id": "formal-conjectures-conjecture198a",
            "final_target": "conjecture198a",
            "initial_target": "terminal_set_fan_left_suffix_retention_left_prefix_residual_bad_false",
            "mode": "proof-lab",
            "round_time_budget": 3600,
            "proof_attempts": 4,
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
# WOWII198a follow-up: bypass obstruction before more Lean

Final theorem: `conjecture198a`.

Current first blocker:
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`.

Immediate proof-lab target:
the theorem-level bypass obstruction needed for
`terminal_set_fan_left_suffix_retention_left_prefix_residual_bad_false`.

The latest Lean rounds added useful support helpers, but the main file still
fails at:
- left-prefix fallback: need strict `terminalPathPairCommonCard fallbackPair <
  terminalPathPairCommonCard pair`;
- old-right-suffix branch: need the corresponding residual `False`.

Required output:
- Do not spend this round on local Lean syntax.
- Prove or state a Lean-ready bypass obstruction for
  `((oldLeft.takeUntil x).append (oldRight.dropUntil x)).toPath`: if a non-left
  vertex of `oldRight.dropUntil x` is absent from the resulting path, produce a
  later right-suffix vertex returning to `oldLeft.takeUntil x`, or give the
  exact alternative that yields common-card descent.
- Use this to explain how the residual fallback contradiction closes the
  `hy_not_alt` branch.
- Then state how to refactor the old-right-suffix branch through
  `exists_first_bad_pivot_on_rs`.
- End with the exact Lean declaration for the next formalizer round.

{base.main_target_discipline("conjecture198a")}
""",
            "contexts": base.existing(
                wowii198a_run / "summary.md",
                wowii198a_run / "supervisor/round-004/decision.md",
                wowii198a_run
                / "lean_formalizer/round-004-terminal-set-fan-left-suffix-retention-left-prefix-residual-bad-false/summary.md",
                wowii198a_run
                / "lean_formalizer/round-004-terminal-set-fan-left-suffix-retention-left-prefix-residual-bad-false/attempts/attempt_004/backend_last_message.txt",
                wowii198a_run
                / "lean_formalizer/round-004-terminal-set-fan-left-suffix-retention-left-prefix-residual-bad-false/attempts/attempt_005/backend_last_message.txt",
                wowii198a_run
                / "lean_formalizer/round-004-terminal-set-fan-left-suffix-retention-left-prefix-residual-bad-false/attempts/attempt_006/backend_last_message.txt",
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
