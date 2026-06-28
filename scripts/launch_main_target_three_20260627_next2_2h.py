#!/usr/bin/env python3
"""Launch the next 2h round for the three active main-target campaigns."""

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

base.PREVIOUS = base.LATEST / "main_target_three_20260627_next_2h"
base.RUN_ROOT = base.LATEST / "main_target_three_20260627_next2_fixed_2h"
base.TIME_BUDGET_SECONDS = 2 * 60 * 60
base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 10 * 60


def build_targets() -> list[dict[str, Any]]:
    previous = base.PREVIOUS / "runs"
    correction = (
        base.LATEST
        / "wowii198a_bad_pivot_correction_20260627_70m"
        / "runs"
        / "wowii198a-bad-pivot-extremal-lean"
        / "wowii198a-bad-pivot-extremal-lean-2h"
    )

    wowii16_run = (
        previous
        / "wowii16-selector-dichotomy-prooflab"
        / "wowii16-selector-dichotomy-prooflab-2h"
    )
    crystals_run = (
        previous
        / "crystals-contrapositive-parity-prooflab"
        / "crystals-contrapositive-parity-prooflab-2h"
    )

    return [
        {
            "priority": 1,
            "slug": "wowii16-dist-two-exchange-prooflab",
            "problem_id": "formal-conjectures-conjecture16",
            "final_target": "conjecture16",
            "initial_target": "central_deficit_dist_two_left_reserve_rebalance_forces_lex_improvement",
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
# WOWII16 next attack: certify the dist-two exchange constructor

Final theorem: `conjecture16`.

Current first blocker:
`central_deficit_exists_diametral_safe_candidate_data_disjoint_selector`.

Immediate stage target:
`central_deficit_dist_two_left_reserve_rebalance_forces_lex_improvement`.

Stay in proof-lab. Do not send the broad selector or the broad lexmax theorem
to Lean yet.

Round-7 conclusion to preserve:
- The fixed-package monotone two-outcome theorem is false.
- The selector route still looks right if it is phrased as lexicographic
  reselection of admissible tuples.
- The `dist b x = 2` constructor is viable only with explicit compatibility
  assumptions for moved vertices.

Required output:
- Decide between the two viable constructor shapes and state the Lean-ready
  theorem:
  1. safe-cardinality improvement with
     `B := P0.filter (fun y => G.Adj x y)`,
     `P0' := P0 \\ B`, `P1' := P1 union B`,
     `Q0' := insert x Q0`, `Q1' := Q1`; or
  2. strict fixed-package extension with
     `P0' := insert x (P0 \\ B)`,
     `P1' := P1 union B`, `Q0' := Q0`, `Q1' := Q1`.
- Quantify the selected diametral path `p : G.Walk u w`, `e = G.diam`,
  the demand interval `D`, old admissibility, freshness/off-path/fixed
  disjointness of `x`, `G.dist b x = 2`, and `forall q in Q0, not G.Adj x q`.
- Include the required move-compatibility clauses:
  moved `B` vertices are compatible with `A union P1`, and old `Q1` is
  preserved after moving `B`.
- Route failures of `hxQ0`, moved-left compatibility, or moved-`Q1`
  compatibility to the same-side blocker or path/fixed collision constructors.
- Explain exactly how this constructor plugs into the three-case exchange
  package, how that closes the lexmax selector, and how the selector chain
  reaches `conjecture16`.

Do not revisit the C6/refutation package, the false universal selector, the
unrestricted off-path refinement, completed wrappers, or local syntax cleanup.

{base.main_target_discipline("conjecture16")}
""",
            "contexts": base.existing(
                wowii16_run / "summary.md",
                wowii16_run / "supervisor/round-007/decision.md",
                wowii16_run / "proof_lab/round-007/summary.md",
                wowii16_run / "proof_lab/round-007/attempts/attempt_003_output.md",
                wowii16_run / "proof_lab/round-007/attempts/attempt_004_output.md",
                wowii16_run / "proof_lab/round-007/math_tools_report.md",
                wowii16_run / "proof_lab/round-007/grounding/source_grounding_output.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore_proof_notes.md",
                base.RESOURCES,
            ),
        },
        {
            "priority": 2,
            "slug": "crystals-mixed-abz-primepower-prooflab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "final_target": "crystals_components_unique",
            "initial_target": "odd_cross_halfShift_gap_no_unit_primepow_defect_of_exact_halved_ABZ",
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
# Crystals next attack: full AB/Z mixed prime-power theorem

Final theorem: `crystals_components_unique`.

Current first blocker:
`odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ`, through the disallowed
parent `odd_cross_halfShift_gap_Y_dvd_ab_mul_Z_quotient_of_exact_halved_ABZ`.

Round-4 conclusion to preserve:
- The local congruence layer allows unit-defect models and cannot prove
  `p^e | Y -> p^e | a*b*kZ` by itself.
- The square-kernel/parity route is not proof-ready.
- Formalizing `no_evenCoeff_odd_vieta_solution` alone is downstream and does
  not close the first arrow to `crystals_components_unique`.

Required output:
- Redesign around the first missing mixed AB/Z theorem. Either prove a
  Lean-ready prime-power certificate from the full exact halved AB/Z
  hypotheses plus square-kernel/defect data, or give a concrete algebraic
  obstruction and the minimal replacement theorem.
- The target shape to validate or refute is:
  `q | Y`, `0 < q`, `Nat.Coprime q (a*b*kZ)`, full exact halved AB/Z data,
  plus square-kernel/defect hypotheses imply `False`.
- If the no-unit theorem fails, identify which full AB/Z edge or
  square-kernel condition is insufficient, and state the smallest additional
  global descent/certificate that would still feed
  `odd_cross_halfShift_gap_Y_dvd_ab_mul_Z_quotient_of_exact_halved_ABZ`.
- Preserve the acyclic chain:
  prime-power/descent certificate ->
  `odd_cross_halfShift_gap_Y_dvd_ab_mul_Z_quotient_of_exact_halved_ABZ` ->
  `odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ` ->
  `odd_cross_halfShift_gap_exact_factor2_edges_obstruction_core` ->
  `no_odd_vieta_solution` / `no_odd_vieta_solution_exists` ->
  integration bridge to `crystals_components_unique`.

Do not use normalized/common-M, `pre_common_M`, later factor-2 wrappers,
`halfShift_cross_AB_Z_obstruction`, or upstream `False.elim`.

{base.main_target_discipline("crystals_components_unique")}
""",
            "contexts": base.existing(
                crystals_run / "summary.md",
                crystals_run / "supervisor/round-004/decision.md",
                crystals_run / "proof_lab/round-004/summary.md",
                crystals_run / "proof_lab/round-004/attempts/attempt_004_output.md",
                crystals_run / "proof_lab/round-004/attempts/attempt_005_output.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Subsets/FC100OpenSet1.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
                base.RESOURCES,
            ),
        },
        {
            "priority": 3,
            "slug": "wowii198a-extremal-bad-pivot-lean",
            "problem_id": "formal-conjectures-conjecture198a",
            "final_target": "conjecture198a",
            "initial_target": "terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent",
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
                "terminal_set_fan_left_first_crossing_splice_commonCard_lt_of_not_retained",
                "terminal_set_fan_splice_descent_left_of_hsep_of_first_crossing_not_retained",
            ],
            "statement": f"""
# WOWII198a next attack: finish the extremal bad-pivot helper

Final theorem: `conjecture198a`.

Current first build blocker:
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`.

Immediate Lean target:
`terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent`.

The previous correction run improved the state but did not verify the file.
Round 3 timed out after one attempt; it did not falsify the helper. Continue
Lean certification on the same helper, not first-crossing and not the arbitrary
bad-pivot body.

Formalization target:
```lean
lemma terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent
    {{α : Type*}} [Fintype α] [DecidableEq α]
    {{G : SimpleGraph α}} {{v s t x w : α}}
    {{pair : G.Path v s × G.Path v t}}
    {{rs : G.Walk v s}}
    (hpair_measure_min : ∀ pair' : G.Path v s × G.Path v t,
      terminalPathPairWeightedMeasure pair ≤ terminalPathPairWeightedMeasure pair')
    (hrsPath : rs.IsPath)
    (hx_left : x ∈ (pair.1 : G.Walk v s).support)
    (hx_right : x ∈ (pair.2 : G.Walk v t).support)
    (hxv : x ≠ v)
    (hx_rs : x ∉ rs.support)
    (hw_rs : w ∈ rs.support)
    (hw_right : w ∈ (pair.2 : G.Walk v t).support)
    (hw_not_left : w ∉ (pair.1 : G.Walk v s).support)
    (hwv : w ≠ v)
    (hfirst : ∀ y, y ∈ rs.support → y ≠ v →
      y ∈ (pair.1 : G.Walk v s).support ∨
      y ∈ (pair.2 : G.Walk v t).support →
      y = w ∨ y ∉ (rs.takeUntil w hw_rs).support)
    (hdirect : ¬ terminalPathPairCommonCard
      ((⟨rs, hrsPath⟩ : G.Path v s), pair.2) <
      terminalPathPairCommonCard pair)
    (hret : x ∈ ((pair.2 : G.Walk v t).dropUntil w hw_right).support)
    (hbad_exists :
      let altRight : G.Path v t :=
        (((pair.1 : G.Walk v s).takeUntil x hx_left).append
          ((pair.2 : G.Walk v t).dropUntil x hx_right)).toPath
      ∃ z : α, z ∈ rs.support ∧ z ≠ v ∧
        z ∈ (altRight : G.Walk v t).support ∧
        ¬ (z ∈ (pair.1 : G.Walk v s).support ∧
           z ∈ (pair.2 : G.Walk v t).support ∧ z ≠ x)) :
    ∃ pair' : G.Path v s × G.Path v t,
      terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair
```

Required output:
- Prove `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent`.
- Define the finite bad set from `hbad_exists`.
- Choose an order-extremal bad pivot on `rs` using the existing
  `exists_last_bad_pivot_on_rs` / `exists_first_bad_pivot_on_rs` helpers.
- Split the selected pivot by whether `altRight` membership comes from the
  old-left prefix to `x` or the old-right suffix from `x`.
- In the left-prefix branch, splice old-left prefix to the extremal pivot with
  `rs.dropUntil`; in the right-suffix branch, splice `rs.takeUntil` with the
  old-right suffix from the extremal pivot.
- Use extremality to close residual intersections. Where containment alone
  fails, prove common-card nonincrease plus strict support-length descent and
  contradict `hpair_measure_min` through the existing weighted-measure lemma.
- After this helper verifies, refactor
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent` to call it, using
  the arbitrary `z` only as the nonempty bad-set witness.
- Run and pass:
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean
  AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`.

Do not move to first-crossing or splice wrappers until this bad-pivot package
builds.

Main-target discipline: every report must state how this helper feeds
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`, then
`terminal_set_fan_left_suffix_retention_alt_intersections_control`,
`terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, the splice
descent chain, the two-fan theorem, Chvatal-Erdos traceability, and finally
`conjecture198a`.
""",
            "contexts": base.existing(
                correction / "summary.md",
                correction / "supervisor/round-003/decision.md",
                correction
                / "lean_formalizer/round-003-terminal-set-fan-left-suffix-retention-extremal-bad-pivot-descent/summary.md",
                correction
                / "lean_formalizer/round-003-terminal-set-fan-left-suffix-retention-extremal-bad-pivot-descent/attempts/attempt_001/attempt_report.json",
                correction
                / "lean_formalizer/round-003-terminal-set-fan-left-suffix-retention-extremal-bad-pivot-descent/attempts/attempt_001/backend_last_message.txt",
                correction
                / "lean_formalizer/round-002-terminal-set-fan-left-suffix-retention-extremal-bad-pivot-descent/summary.md",
                correction
                / "lean_formalizer/round-002-terminal-set-fan-left-suffix-retention-extremal-bad-pivot-descent/attempts/attempt_006/attempt_report.json",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost_formalizer_notes.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost_proof_notes.md",
                "amra_library/formal/proof_notes/wowii198a_bad_pivot_extremal_round002_iter6.md",
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
