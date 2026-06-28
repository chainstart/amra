#!/usr/bin/env python3
"""Launch the follow-up 2h round for the four main-target campaigns.

This wrapper reuses the generic driver helpers from the previous launcher, but
updates the run root and the next targets to the latest supervisor decisions:

- WOWII16: certify the C6 obstruction, then redesign the candidate package.
- Crystals: continue proof-lab on the acyclic quotient/odd-Vieta certificate.
- Erdos1: do not continue Harper; search for a replacement constant-scale
  weighted certificate or freeze.
- WOWII198a: prove the left first-crossing uncrossing core.
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

base.PREVIOUS = base.LATEST / "main_target_four_20260627_2h"
base.RUN_ROOT = base.LATEST / "main_target_four_20260627_followup_2h"


def build_targets() -> list[dict[str, Any]]:
    previous = base.PREVIOUS / "runs"

    wowii16_run = previous / "wowii16-main-conjecture-route-audit/wowii16-main-conjecture-route-audit-2h"
    crystals_run = previous / "crystals-components-unique-main-descent/crystals-components-unique-main-descent-2h"
    erdos_run = previous / "erdos1-main-harper-source-transfer/erdos1-main-harper-source-transfer-2h"
    wowii198a_run = previous / "wowii198a-main-fan-to-traceable/wowii198a-main-fan-to-traceable-2h"

    return [
        {
            "priority": 1,
            "slug": "wowii16-c6-obstruction-main-route-repair",
            "problem_id": "formal-conjectures-conjecture16",
            "final_target": "conjecture16",
            "initial_target": "central_deficit_diametral_safe_candidate_data_c6_obstruction",
            "mode": "lean-formalizer",
            "round_time_budget": 3600,
            "formalizer_attempts": 6,
            "formalizer_attempt_timeout": 1500,
            "workspace": str(base.FORMAL),
            "target_file": base.formal_file(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean"
            ),
            "build_command": base.build_command(
                "AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean"
            ),
            "completed": [
                "central_deficit_component_shadow_coloring_certificate",
                "central_deficit_component_shadow_coloring_from_safe_pool_hall",
                "central_deficit_component_shadow_coloring_from_component_capacity",
                "central_deficit_base_compatible_diametral_repair_obstruction",
            ],
            "statement": f"""
# WOWII16 follow-up: certify the C6 obstruction, then repair the route

Final theorem: `conjecture16`.

The previous route through universal
`centralDeficitDiametralSafeCandidateData G b A` is false.  The C6 obstruction
has edges `(0,4), (0,5), (1,3), (1,5), (2,3), (2,4)`, base `b = 0`,
max independent neighbor set `A = {{4,5}}`, diametral path `[1,3,2,4]`,
radius `3`, diameter `3`, and nonempty demand interval `D = {{2}}`, while
the strict off-path Q0/Q1 distance thresholds force both pools empty.

Current executable target:
`central_deficit_diametral_safe_candidate_data_c6_obstruction`.

Required output:
- Prove or package the C6 obstruction theorem in Lean.
- State the universal-refutation corollary clearly.
- After certification, return to proof-lab and design a replacement
  existential or compatibility-restricted two-base candidate package that can
  still feed
  `central_deficit_decoupled_assigned_radius_tail_component_safe_hall_of_candidate_data`
  and then the small-diameter branch bridge to `conjecture16`.
- Do not attempt to prove the false universal candidate-data theorem.

{base.main_target_discipline("conjecture16")}
""",
            "contexts": base.existing(
                wowii16_run / "summary.md",
                wowii16_run / "supervisor/round-003/decision.md",
                wowii16_run / "lean_formalizer/round-003-central-deficit-diametral-safe-candidate-data/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture16.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore_proof_notes.md",
                "amra_library/formal/proof_notes/wowii16_central_deficit_candidate_data_round003.md",
                base.RESOURCES,
            ),
        },
        {
            "priority": 2,
            "slug": "crystals-odd-vieta-certificate-prooflab",
            "problem_id": "formal-conjectures-crystals-components-unique",
            "final_target": "crystals_components_unique",
            "initial_target": "odd_cross_halfShift_gap_odd_vieta_witness_of_not_Y_dvd_ab_mul_Z_quotient",
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
                "odd_cross_halfShift_gap_AB_from_edges",
                "odd_cross_halfShift_gap_AB_add_ab_eq_YZ",
                "odd_cross_halfShift_gap_Y_dvd_AB_iff_Y_dvd_ab",
                "odd_cross_halfShift_gap_Z_quotient_data",
            ],
            "statement": f"""
# Crystals follow-up: acyclic quotient or odd-Vieta certificate

Final theorem: `crystals_components_unique`.

Current first blocker:
`odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ`.

Sharper unsolved node:
`odd_cross_halfShift_gap_odd_vieta_witness_of_not_Y_dvd_ab_mul_Z_quotient`.

Required output:
- Continue proof-lab, not Lean editing, until there is an explicit acyclic
  certificate.
- Either give explicit formulas for `R S X W` from the full exact halved
  AB/Z hypotheses plus `not Y | a*b*kZ`, or replace this with a strict
  odd-rectangle descent lemma constructing a smaller witness.
- Give the dependency graph from the certificate to
  `odd_cross_halfShift_gap_Y_dvd_ab_mul_Z_quotient_of_exact_halved_ABZ`,
  then to `odd_cross_halfShift_gap_Y_dvd_AB_of_exact_halved_ABZ`, then to
  `odd_cross_halfShift_gap_exact_factor2_edges_obstruction_core`, then to
  `no_odd_vieta_solution`, and finally identify the remaining integration gap
  to `crystals_components_unique`.
- Do not use normalized/common-M, `pre_common_M`, later factor-2 wrappers,
  `halfShift_cross_AB_Z_obstruction`, or any `False.elim` bridge as an
  upstream dependency.

{base.main_target_discipline("crystals_components_unique")}
""",
            "contexts": base.existing(
                crystals_run / "summary.md",
                crystals_run / "supervisor/round-004/decision.md",
                crystals_run / "proof_lab/round-004/summary.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/Subsets/FC100OpenSet1.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent.lean",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/TrueOpenNextRound20260606/07_crystals_odd_vieta_descent_proof_notes.md",
                base.RESOURCES,
            ),
        },
        {
            "priority": 3,
            "slug": "erdos1-constant-scale-replacement-prooflab",
            "problem_id": "erdos-problem-1",
            "final_target": "erdos_1",
            "initial_target": "erdos1_constant_scale_weighted_dichotomy_certificate",
            "mode": "proof-lab",
            "round_time_budget": 3600,
            "proof_attempts": 4,
            "workspace": str(base.FORMAL),
            "target_file": base.formal_file(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1HarperVertexBoundaryScratch.lean"
            ),
            "build_command": base.build_command(
                "AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1HarperVertexBoundaryScratch.lean"
            ),
            "completed": [
                "boolean_halfInitialSegment_card",
                "boolean_halfInitialSegment_closedNeighborhood_card",
                "boolean_boundary_card_ge_middle_of_closed_neighborhood",
            ],
            "statement": f"""
# Erdos1 follow-up: find a replacement route to the original theorem

Final theorem: `erdos_1`.

The Harper/Raty closed-neighborhood route is frozen for the original theorem:
it gives only middle-binomial scale `2^n / sqrt(n)`, while `erdos_1` needs a
fixed constant multiple of `2^|A|`.

Current target:
`erdos1_constant_scale_weighted_dichotomy_certificate`.

Required output:
- Do not continue the Harper middle-binomial route.
- Either identify an admissible source theorem or construct a Lean-ready
  certificate proving a constant-scale weighted dichotomy strong enough for
  `erdos_1`; or freeze the route again with a precise obstruction.
- If a weaker theorem is the only available path, state it as a separate
  variant and explain exactly why it does not prove `erdos_1`.
- The report must include the remaining chain from the proposed certificate to
  `IsSumDistinctSet A N -> exists C > 0, C * 2^A.card < N`.

{base.main_target_discipline("erdos_1")}
""",
            "contexts": base.existing(
                erdos_run / "summary.md",
                erdos_run / "supervisor/round-005/decision.md",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1.lean",
                "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1_boolean_boundary_proof_notes.md",
                "amra_library/formal/AmraLibrary/OpenProblemBatches/NewCandidates20260612/Erdos1HarperVertexBoundaryScratch.lean",
                base.RESOURCES,
            ),
        },
        {
            "priority": 4,
            "slug": "wowii198a-left-uncrossing-main-chain",
            "problem_id": "formal-conjectures-conjecture198a",
            "final_target": "conjecture198a",
            "initial_target": "terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt",
            "mode": "lean-formalizer",
            "round_time_budget": 3600,
            "formalizer_attempts": 6,
            "formalizer_attempt_timeout": 1500,
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
            ],
            "statement": f"""
# WOWII198a follow-up: left first-crossing uncrossing core

Final theorem: `conjecture198a`.

Current first blocker:
`terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`.

Required output:
- Prove the left uncrossing core from the explicit spliced construction:
  `rs.takeUntil w` appended to `(pair.2 : G.Walk v t).dropUntil w`, converted
  with `toPath`.
- Use the union-first-hit fact to show the replacement prefix avoids every old
  support vertex except possibly `v` and `w`; use `hw_not_left` and `hx_rs` to
  remove the old common vertex `x`.
- Finish by proving erased common support containment in the old erased common
  support with `x` removed, or derive equal common-card but smaller support
  length contradicting weighted-measure minimality.
- Then state how this wraps into `terminal_set_fan_splice_descent_left_of_hsep`,
  mirrors to the right splice, closes the two-fan theorem, the longest-path
  missed-vertex contradiction, Chvatal-Erdos traceability, and `conjecture198a`.
- Do not broaden back to the whole two-fan wrapper and do not revive the old
  singleton-path OR theorem.

{base.main_target_discipline("conjecture198a")}
""",
            "contexts": base.existing(
                wowii198a_run / "summary.md",
                wowii198a_run / "supervisor/round-004/decision.md",
                wowii198a_run / "lean_formalizer/round-004-terminal-set-fan-splice-descent-left-of-hsep/summary.md",
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
