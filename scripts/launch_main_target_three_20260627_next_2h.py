#!/usr/bin/env python3
"""Launch the next 2h round for the three active main-target campaigns.

This round starts from ``main_target_three_20260627_followup_2h``:

- WOWII198a continues Lean work on the live first-crossing theorem.
- WOWII16 stays in proof-lab to make the selector dichotomy Lean-ready.
- Crystals stays in proof-lab to force the square-kernel parity/descent audit.
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

base.PREVIOUS = base.LATEST / "main_target_three_20260627_followup_2h"
base.RUN_ROOT = base.LATEST / "main_target_three_20260627_next_2h"


def build_targets() -> list[dict[str, Any]]:
    previous = base.PREVIOUS / "runs"

    wowii198a_run = (
        previous
        / "wowii198a-bad-pivot-descent-lean/wowii198a-bad-pivot-descent-lean-2h"
    )
    wowii16_run = (
        previous
        / "wowii16-selector-main-chain/wowii16-selector-main-chain-2h"
    )
    crystals_run = (
        previous
        / "crystals-square-kernel-parity-prooflab/crystals-square-kernel-parity-prooflab-2h"
    )

    return [
        {
            "priority": 1,
            "slug": "wowii198a-left-first-crossing-lean",
            "problem_id": "formal-conjectures-conjecture198a",
            "final_target": "conjecture198a",
            "initial_target": "terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt",
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
                "not_mem_dropUntil_of_mem_dropUntil_reverse_on_isPath",
                "terminal_set_fan_left_suffix_retention_bad_pivot_descent",
                "terminal_set_fan_left_suffix_retention_alt_intersections_control",
                "terminal_set_fan_left_first_crossing_splice_commonCard_lt_of_not_retained",
                "terminal_set_fan_splice_descent_left_of_hsep_of_first_crossing_not_retained",
            ],
            "statement": f"""
# WOWII198a next attack: close the live left first-crossing theorem

Final theorem: `conjecture198a`.

Current first blocker:
`terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`.

This is the live Lean target.  The previous run verified
`not_mem_dropUntil_of_mem_dropUntil_reverse_on_isPath`, and the suffix-retention
package `terminal_set_fan_left_suffix_retention_bad_pivot_descent` plus
`terminal_set_fan_left_suffix_retention_alt_intersections_control` is already
Lean-visible in `Wowii198aLeftmost.lean`.  Use these lemmas; do not reopen their
proofs or retarget to them.

Required output:
- Continue Lean implementation of
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`.
- First check that the two suffix-retention lemmas and the not-retained splice
  lemma are available by name, then use them directly.
- Split on the direct replacement pair
  `((<rs, hrsPath> : G.Path v s), pair.2)`.
- In the non-direct branch define
  `spliceRight := ((rs.takeUntil w hw_rs).append
    ((pair.2 : G.Walk v t).dropUntil w hw_right)).toPath`.
- If `x` is not retained in the old-right suffix, finish with
  `terminal_set_fan_left_first_crossing_splice_commonCard_lt_of_not_retained`
  or the existing not-retained splice package.
- If `x` is retained, define `altRight` from the old-left prefix to `x` plus
  the old-right suffix from `x`, apply
  `terminal_set_fan_left_suffix_retention_alt_intersections_control`, prove the
  erased common-support containment with `x` removed, and finish through
  `common_support_erase_card_lt_of_subset_erase_common`.
- End by making
  `#check terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`
  pass in the target file.

Chain to the main theorem:
`terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt` ->
left splice descent -> mirrored right splice -> two-fan theorem ->
longest-path missed-vertex contradiction -> Chvatal-Erdos traceability ->
`conjecture198a`.

Do not broaden to the splice wrapper before this theorem builds, and do not
retry the old direct suffix-exclusion route.

{base.main_target_discipline("conjecture198a")}
""",
            "contexts": base.existing(
                wowii198a_run / "summary.md",
                wowii198a_run / "supervisor/round-007/decision.md",
                wowii198a_run
                / "lean_formalizer/round-007-terminal-set-fan-left-first-crossing-uncrossing-commoncard-lt/summary.md",
                wowii198a_run
                / "lean_formalizer/round-007-terminal-set-fan-left-first-crossing-uncrossing-commoncard-lt/attempts/attempt_003/attempt_report.json",
                wowii198a_run
                / "lean_formalizer/round-004-terminal-set-fan-left-suffix-retention-bad-pivot-descent/summary.md",
                wowii198a_run
                / "proof_lab/round-005/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost_formalizer_notes.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost_proof_notes.md",
                base.RESOURCES,
            ),
        },
        {
            "priority": 2,
            "slug": "wowii16-selector-dichotomy-prooflab",
            "problem_id": "formal-conjectures-conjecture16",
            "final_target": "conjecture16",
            "initial_target": "central_deficit_exists_diametral_safe_candidate_data_disjoint_selector",
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
                "central_deficit_diametral_safe_candidate_data_c6_obstruction",
                "central_deficit_diametral_safe_candidate_data_universal_refuted",
                "central_deficit_diametral_disjoint_selector_universal_refuted",
                "central_deficit_c6_exists_diametral_safe_candidate_data_disjoint",
                "central_deficit_exists_diametral_safe_candidate_data_disjoint_of_untagged",
                "central_deficit_exists_diametral_safe_candidate_data_disjoint_of_exists_untagged",
                "central_deficit_decoupled_assigned_radius_tail_component_safe_hall_of_exists_disjoint_candidate_data",
                "central_deficit_component_shadow_coloring_from_component_capacity",
                "central_deficit_off_path_safe_pool_refinement_of_fixed_color_witness_refuted",
            ],
            "statement": f"""
# WOWII16 next attack: make the selector route Lean-ready

Final theorem: `conjecture16`.

Current first blocker:
`central_deficit_exists_diametral_safe_candidate_data_disjoint_selector`.

Stay in proof-lab.  Do not start another Lean formalizer pass on the broad
selector until the missing theorem-level dichotomy is precise enough to state
in Lean.

Required output:
- Produce a fully Lean-ready theorem-level blocker-to-augmentation dichotomy,
  not a schematic lemma.
- The theorem must quantify a selected diametral path `p : G.Walk u w`, its
  length `e = G.diam`, the demand interval
  `D = Finset.Icc (e - G.radius.toNat + 2) (G.radius.toNat - 1)`, fixed-color
  sides `P0/P1`, and the failed disjoint safe-pool capacity condition.
- The conclusion must be exactly one of:
  (1) a strictly larger compatible fixed-color bipartite extension than the
  current `A union P1` / `insert b P0` package; or
  (2) an independent neighbor set at `b` with cardinality larger than `A`.
- Split the proof route into the documented obstruction cases:
  same-side adjacency blockers, path/fixed collisions, and the `dist b x = 2`
  left-reserve obstruction.
- Explain how this dichotomy proves
  `central_deficit_exists_diametral_safe_candidate_data_disjoint_selector`,
  then how the selector feeds
  `central_deficit_exists_diametral_safe_candidate_data_disjoint_of_exists_untagged`,
  assigned safe-Hall, component capacity, max-star bipartite witness bound,
  the small-diameter bridge, and finally `conjecture16`.
- If the dichotomy is false or under-specified, return the precise finite
  obstruction and the exact replacement theorem that would still feed the same
  selector parent.

Do not revisit Erdos1, the C6 audit/refutation package, the malformed header
issue, the false universal selector, completed wrapper/cardinality lemmas, or
the refuted unrestricted theorem
`central_deficit_off_path_safe_pool_refinement_of_fixed_color_witness`.

{base.main_target_discipline("conjecture16")}
""",
            "contexts": base.existing(
                wowii16_run / "summary.md",
                wowii16_run / "supervisor/round-004/decision.md",
                wowii16_run / "proof_lab/round-004/summary.md",
                wowii16_run / "proof_lab/round-003/summary.md",
                wowii16_run
                / "lean_formalizer/round-002-central-deficit-off-path-safe-pool-refinement-of-fixed-color-witness/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore_proof_notes.md",
                "amra_library/formal/proof_notes/wowii16_central_deficit_candidate_data_round003.md",
                base.RESOURCES,
            ),
        },
        {
            "priority": 3,
            "slug": "crystals-contrapositive-parity-prooflab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "final_target": "crystals_components_unique",
            "initial_target": "odd_cross_halfShift_gap_squareKernel_coeff_two_of_not_Y_dvd_ab_mul_Z_quotient",
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
                "odd_cross_halfShift_gap_fourth_edge_of_modular_edges_and_Y_dvd_AB",
            ],
            "statement": f"""
# Crystals next attack: focused parity/descent route audit

Final theorem: `crystals_components_unique`.

Current first blocker:
`odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ`, through the unresolved
and currently disallowed parent
`odd_cross_halfShift_gap_Y_dvd_ab_mul_Z_quotient_of_exact_halved_ABZ`.

Sharper proof-lab target:
`odd_cross_halfShift_gap_squareKernel_coeff_two_of_not_Y_dvd_ab_mul_Z_quotient`.

Stay in proof-lab.  Stop broad independent attempts.  The next useful output is
one of the following two concrete certificates:
- Prove the contrapositive defect lemma from the full exact halved AB/Z data
  plus square-kernel data `A = R*X^2`, `B = S*W^2`,
  `N = C*R*S*X*W`:
  `Odd C or Even X or Even W -> Y dvd a*b*kZ`.
- Or return explicit strict odd-rectangle descent formulas constructing a
  smaller witness, with every variable and inequality stated in Lean-ready Nat
  form.

The report must restate and preserve the acyclic chain:
parity/descent certificate ->
`odd_cross_halfShift_gap_Y_dvd_ab_mul_Z_quotient_of_exact_halved_ABZ` ->
`odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ` ->
`odd_cross_halfShift_gap_exact_factor2_edges_obstruction_core` ->
`no_odd_vieta_solution` / `no_odd_vieta_solution_exists` ->
remaining integration bridge to `crystals_components_unique`.

Do not use normalized/common-M, `pre_common_M`, later factor-2 wrappers,
`halfShift_cross_AB_Z_obstruction`, or any upstream `False.elim`.
If the parity route fails, return a concrete algebraic obstruction and the
minimal replacement theorem instead of another renamed local witness lemma.

{base.main_target_discipline("crystals_components_unique")}
""",
            "contexts": base.existing(
                crystals_run / "summary.md",
                crystals_run / "supervisor/round-004/decision.md",
                crystals_run / "proof_lab/round-004/summary.md",
                crystals_run / "proof_lab/round-003/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Subsets/FC100OpenSet1.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
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
