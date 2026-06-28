#!/usr/bin/env python3
"""Launch the next 2h round for the three active main-target campaigns.

Erdos1 is intentionally omitted.  The previous round froze it until a genuinely
new fixed-constant weighted source/certificate is available.
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

base.PREVIOUS = base.LATEST / "main_target_four_20260627_followup_2h"
base.RUN_ROOT = base.LATEST / "main_target_three_20260627_followup_2h"


def build_targets() -> list[dict[str, Any]]:
    previous = base.PREVIOUS / "runs"

    wowii16_run = (
        previous
        / "wowii16-c6-obstruction-main-route-repair/wowii16-c6-obstruction-main-route-repair-2h"
    )
    crystals_run = (
        previous
        / "crystals-odd-vieta-certificate-prooflab/crystals-odd-vieta-certificate-prooflab-2h"
    )
    wowii198a_run = (
        previous
        / "wowii198a-left-uncrossing-main-chain/wowii198a-left-uncrossing-main-chain-2h"
    )

    return [
        {
            "priority": 1,
            "slug": "wowii16-selector-main-chain",
            "problem_id": "formal-conjectures-conjecture16",
            "final_target": "conjecture16",
            "initial_target": "central_deficit_exists_diametral_safe_candidate_data_disjoint_selector",
            "mode": "lean-formalizer",
            "round_time_budget": 3600,
            "formalizer_attempts": 6,
            "formalizer_attempt_timeout": 1800,
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
            ],
            "statement": f"""
# WOWII16 next attack: prove the selector, then close Conjecture 16

Final theorem: `conjecture16`.

Erdos1 is frozen and must not be revived in this run.  For WOWII16, the false
universal predicate route is closed: the C6 obstruction and universal refutation
package are already present.  The live route is the existential-disjoint
candidate package.

Current first blocker:
`central_deficit_exists_diametral_safe_candidate_data_disjoint_selector`.

Required output:
- Prove the selector theorem, constructing compatible witnesses
  `u w p e D P0 P1 Q0 Q1` under the hard branch.
- Preserve the exact clauses needed by
  `centralDeficitExistsDiametralSafeCandidateDataDisjoint`: path/diameter data,
  demand interval cardinality, independent fixed-color sets, disjoint fixed
  colors, off-path safe pools, Q0/Q1 independence and disjointness, Q0 distance
  threshold `2 <= G.dist b x`, Q1 threshold `3 <= G.dist b x`, forbidden
  adjacencies to `insert b P0` and `A union P1`, `D.card <= (Q0 union Q1).card`,
  and disjointness of safe pools from fixed-color vertices.
- If direct proof stalls, isolate the blocker-to-augmentation dichotomy as a
  theorem-level lemma: insufficient disjoint safe capacity must force either a
  larger fixed-color bipartite extension or an independent neighborhood larger
  than `A`.
- After proving the selector, close
  `central_deficit_exists_diametral_safe_candidate_data_disjoint` via the
  existing wrapper, then feed the assigned safe-Hall package, component
  capacity, max-star bipartite witness bound, small-diameter bridge, and finally
  `conjecture16`.
- Do not revisit the C6 audit, malformed header issue, the false universal
  candidate-data theorem, or completed packaging/cardinality lemmas.

Formalization target:
```lean
theorem central_deficit_exists_diametral_safe_candidate_data_disjoint_selector
    {{alpha : Type*}} [Fintype alpha] [DecidableEq alpha] [Nontrivial alpha]
    (G : SimpleGraph alpha) [DecidableRel G.Adj] (hG : G.Connected)
    (b : alpha) (A : Finset alpha)
    (hRadius : 2 < G.radius.toNat)
    (hDiamSmall : not (2 * G.radius.toNat : Nat) <= G.diam + 1)
    (hAcard : A.card = SimpleGraph.maxIndepNeighborsCard G)
    (hAneigh : forall a, a in A -> G.Adj b a)
    (hAind : G.IsIndepSet (A : Set alpha)) :
    exists u w : alpha, exists p : G.Walk u w, exists e : Nat, exists D : Finset Nat,
    exists P0 P1 Q0 Q1 : Finset alpha,
      p.IsPath and p.length = e and e = G.diam and
      D = Finset.Icc (e - G.radius.toNat + 2) (G.radius.toNat - 1) and
      D.card = 2 * G.radius.toNat - 2 - e and
      G.IsIndepSet ((A union P1 : Finset alpha) : Set alpha) and
      G.IsIndepSet ((insert b P0 : Finset alpha) : Set alpha) and
      Disjoint (A union P1) (insert b P0) and
      A.card + e <= ((A union P1) union insert b P0).card and
      (forall x, x in Q0 union Q1 -> x notin p.support.toFinset) and
      G.IsIndepSet (Q0 : Set alpha) and G.IsIndepSet (Q1 : Set alpha) and
      Disjoint Q0 Q1 and
      (forall x, x in Q0 -> 2 <= G.dist b x and forall y, y in insert b P0 -> not G.Adj x y) and
      (forall x, x in Q1 -> 3 <= G.dist b x and forall y, y in A union P1 -> not G.Adj x y) and
      D.card <= (Q0 union Q1).card and
      Disjoint (Q0 union Q1) ((A union P1) union insert b P0)
```

{base.main_target_discipline("conjecture16")}
""",
            "contexts": base.existing(
                wowii16_run / "summary.md",
                wowii16_run / "proof_lab/round-004/summary.md",
                wowii16_run / "supervisor/round-004/decision.md",
                wowii16_run
                / "lean_formalizer/round-003-central-deficit-exists-diametral-safe-candidate-data-disjoint/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore_proof_notes.md",
                "amra_library/formal/proof_notes/wowii16_central_deficit_candidate_data_round003.md",
                base.RESOURCES,
            ),
        },
        {
            "priority": 2,
            "slug": "crystals-square-kernel-parity-prooflab",
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
# Crystals next attack: square-kernel parity certificate

Final theorem: `crystals_components_unique`.

Current first blocker:
`odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ`.

Sharper active target:
`odd_cross_halfShift_gap_squareKernel_coeff_two_of_not_Y_dvd_ab_mul_Z_quotient`.

Required output:
- Stay in proof-lab.  Do not start Lean editing until there is an explicit
  acyclic certificate.
- From the full exact halved AB/Z hypotheses plus
  `not Y | a*b*kZ`, prove the square-kernel parity certificate for
  `A = R*X^2`, `B = S*W^2`, `N = C*R*S*X*W`: ideally
  `C = 2 and Odd X and Odd W`.
- If that certificate cannot be proved, replace it with explicit strict
  odd-rectangle descent formulas constructing a smaller witness.
- The acyclic dependency graph must be:
  parity/descent certificate ->
  `odd_cross_halfShift_gap_Y_dvd_ab_mul_Z_quotient_of_exact_halved_ABZ` ->
  `odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ` ->
  `odd_cross_halfShift_gap_exact_factor2_edges_obstruction_core` ->
  `no_odd_vieta_solution` / `no_odd_vieta_solution_exists` ->
  remaining integration bridge to `crystals_components_unique`.
- Do not use normalized/common-M, `pre_common_M`, later factor-2 wrappers,
  `halfShift_cross_AB_Z_obstruction`, or any `False.elim` bridge upstream.
- If the parity route fails, return a concrete algebraic obstruction rather than
  cycling through renamed local witness lemmas.

{base.main_target_discipline("crystals_components_unique")}
""",
            "contexts": base.existing(
                crystals_run / "summary.md",
                crystals_run / "proof_lab/round-004/summary.md",
                crystals_run / "supervisor/round-004/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Subsets/FC100OpenSet1.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
                base.RESOURCES,
            ),
        },
        {
            "priority": 3,
            "slug": "wowii198a-bad-pivot-descent-lean",
            "problem_id": "formal-conjectures-conjecture198a",
            "final_target": "conjecture198a",
            "initial_target": "terminal_set_fan_left_suffix_retention_bad_pivot_descent",
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
                "terminal_set_fan_left_suffix_retention_alt_intersections_control",
            ],
            "statement": f"""
# WOWII198a next attack: bad-pivot descent for suffix retention

Final theorem: `conjecture198a`.

Current first blocker between the left first-crossing uncrossing lemma and the
main theorem:
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`.

Required output:
- Continue Lean implementation of this theorem.  The declaration matched in the
  previous round; the stop reason was time budget, not route failure.
- Split a bad `z in rs.support inter altRight.support` by whether the
  `altRight` membership comes from the old-left prefix to `x` or the old-right
  suffix from `x`.
- In the old-left-prefix branch, splice the old-left prefix to `z` with
  `rs.dropUntil z`.
- In the old-right-suffix branch, splice `rs.takeUntil z` with the old-right
  suffix from `z`.
- In each branch, prove erased common-support containment with `x` removed; if
  strict common-card descent is not immediate, derive equal common-card with
  strictly smaller support length and contradict `hpair_measure_min` via
  `terminalPathPairWeightedMeasure`.
- Closing this theorem must feed
  `terminal_set_fan_left_suffix_retention_alt_intersections_control`, then
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, the left
  splice descent, mirrored right splice, two-fan theorem, longest-path
  missed-vertex contradiction, Chvatal-Erdos traceability, and finally
  `conjecture198a`.
- Do not retry direct suffix exclusion `x notin oldRight.dropUntil w`, do not
  broaden to the two-fan wrapper, and do not revive the singleton-path OR
  theorem.

{base.main_target_discipline("conjecture198a")}
""",
            "contexts": base.existing(
                wowii198a_run / "summary.md",
                wowii198a_run / "supervisor/round-003/decision.md",
                wowii198a_run / "supervisor/round-004/decision.md",
                wowii198a_run
                / "lean_formalizer/round-004-terminal-set-fan-left-suffix-retention-bad-pivot-descent/summary.md",
                wowii198a_run
                / "lean_formalizer/round-004-terminal-set-fan-left-suffix-retention-bad-pivot-descent/attempts/attempt_003/attempt_report.json",
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
