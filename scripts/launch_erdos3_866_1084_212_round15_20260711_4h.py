#!/usr/bin/env python3
"""Launch round 15 for Erdos #866/#1084/#212 with four-hour supervised loops."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROUND14_PATH = REPO / "scripts/launch_erdos3_866_1084_212_round14_20260711_2h.py"


def load_round14():
    spec = importlib.util.spec_from_file_location("erdos_round14_launcher", ROUND14_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load launcher: {ROUND14_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


round14 = load_round14()
base = round14.base
base.RUN_ROOT = (
    REPO
    / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round15_20260711_4h"
)
base.TIME_BUDGET_SECONDS = 4 * 60 * 60
base.ROUND_TIME_BUDGET_SECONDS = 45 * 60
base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 15 * 60


base.TARGETS = [
    {
        "priority": 1,
        "slug": "erdos866-k7-all-n-lower-transfer",
        "problem_id": "erdos-866",
        "title": "Erdos #866 k=7 lower-bound transfer beyond seventh powers",
        "focus": """Treat all round-14 finite sum-graph, seven-distinct-sums, hyperedge-counting, Bernoulli deletion, and seventh-power construction theorems as marker-free Lean-verified and closed. Do not reprove them or rerun finite optimization.

The verified endpoint is `exists_sumK5Free_at_seventh_power`; the immediate missing bridge and the real objective of this round are to turn it into a `gFun 7` lower bound and extend it from perfect seventh powers to arbitrary larger ambient intervals.

Required route:
1. First prove the exact low-risk theorem
   ```lean
   theorem gFun_seven_lower_at_seventh_power
       (t : ℕ) (ht : 1 ≤ t) :
       t ^ 3 < 9 * gFun 7 (t ^ 7)
   ```
   by composing the verified construction with `gFun_seven_gt_of_sumCliqueFree`.
2. Prove an ambient-transfer lemma: if `M ≤ N`, `E ⊆ sumK5Candidates M`, and `SumK5Free M E`, then `SumK5Free N E`. For a hypothetical larger-ambient witness, use its sums in `E ⊆ [1,2M]` and `witness_bounded_of_three_sums M` to recover the smaller witness bounds.
3. Deduce a parameterized all-ambient theorem such as
   ```lean
   theorem gFun_seven_lower_of_seventh_power_le
       (t N : ℕ) (ht : 1 ≤ t) (hpow : t ^ 7 ≤ N) :
       t ^ 3 < 9 * gFun 7 N
   ```
   without assuming an unproved monotonicity property of `gFun`.
4. Formalize a seventh-root selection lemma with explicit constants and use it to derive a genuine all-large-`N` lower bound of order `N^(3/7)`, preferably first as a natural-power inequality and only then as a real asymptotic statement.
5. State precisely how this lower bound compares with the already verified general upper bound; do not claim a sharp exponent unless both sides match.

Reject `sorry`, axioms, opaque/source markers, numerical evidence as proof, and hidden positivity assumptions on witnesses. The minimum success criterion is the first two displayed `gFun` theorems; the preferred result is an all-large-`N` `3/7` lower bound with explicit constants.""",
        "contexts": base.existing(
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Base.lean",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866.lean",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round14_20260711_2h/runs/erdos866-k7-seven-distinct-pairsums/erdos866-k7-seven-distinct-pairsums-supervised-2h/summary.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round14_20260711_2h/runs/erdos866-k7-seven-distinct-pairsums/erdos866-k7-seven-distinct-pairsums-supervised-2h/supervisor/round-021/decision.md",
        ),
    },
    {
        "priority": 2,
        "slug": "erdos1084-polygonal-ray-crossing-parity",
        "problem_id": "erdos-1084",
        "title": "Erdos #1084 local polygonal ray-crossing parity",
        "focus": """Treat the polygonal `AddCircle` constructor, injectivity theorem, standard-circle reparametrization, exterior path-connectedness, and conditional partition boundedness theorem as marker-free local results. The external Jordan repository acquisition failed in round 14; do not repeat network checkout, theorem-name guessing, or an unverified adapter in this campaign.

Open a self-contained polygonal Jordan route using horizontal-ray crossing parity for `PolygonalCycleCertificate`.

Required route:
1. Define a transparent orientation/cross-product predicate and a half-open horizontal-ray crossing predicate for a directed segment. The endpoint convention must count a vertex exactly once and exclude horizontal edges and points on the polygon.
2. Prove the first exact segment theorem: when the endpoint heights strictly straddle a generic horizontal level, the affine segment has a unique parameter at that level, and the crossing predicate is equivalent to the resulting intersection lying to the right of the query point.
3. Package the finite crossing count/parity for all certified polygon edges. Prove invariance under cyclic reindexing and prove that far-right/far-left exterior points have the expected parity using compact boundedness.
4. Prove local constancy of crossing parity along a path disjoint from the polygonal image, first for one segment and then for the finite cycle. Handle vertex events with the half-open convention rather than informal perturbation.
5. Use parity `0/1` to construct two disjoint open subsets of the complement, prove the exterior lies in parity `0`, and state the exact remaining connectedness/frontier theorem needed to instantiate `jordanPartition_exactlyOne_bounded`.

Use small Lean probes to select APIs, but promote only exact theorem declarations. If the full parity invariant is too broad, prove the unique segment-level intersection theorem and one endpoint-counting lemma rather than freezing. Reject `sorry`, axioms, opaque/source markers, imported Jordan claims, and non-executable prose-only blockers.""",
        "contexts": base.existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round14_20260711_2h/runs/erdos1084-jordan-dependency-integration/erdos1084-jordan-dependency-integration-supervised-2h/summary.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round14_20260711_2h/runs/erdos1084-jordan-dependency-integration/erdos1084-jordan-dependency-integration-supervised-2h/supervisor/round-007/decision.md",
        ),
    },
    {
        "priority": 3,
        "slug": "erdos212-quadratic-to-irreducible-cubic",
        "problem_id": "erdos-212",
        "title": "Erdos #212 quadratic-to-irreducible-cubic inversion package",
        "focus": """Treat every round-14 inversion theorem as closed, including `homogeneousComponent_one_ne_zero_of_irreducible_quadratic_of_nonzero_zero`: a fresh full-file build and `#print axioms` audit found only standard Lean axioms and no `sorryAx`. Do not spend a round recertifying it.

Finish and package the Solymosi--de Zeeuw degree-two inversion branch: a noncircle irreducible quadratic through a nonzero inversion point should pull back to an irreducible cubic carrying the inverted infinite rational-distance set.

Required route:
1. Combine `homogeneousComponent_one_ne_zero_of_irreducible_quadratic_of_nonzero_zero` with `planePolynomialUnitCircleInversion_totalDegree_eq_three` into an exact theorem giving total degree `3` under irreducibility, degree `2`, vanishing constant component, and one nonzero real zero.
2. Add the noncircle hypothesis and use the verified nondivisibility and irreducibility theorems to prove the inversion polynomial is simultaneously irreducible and degree `3`.
3. Package the zero-locus and rational-distance transfer: from an infinite rational-distance subset of the original quadratic away from the inversion center, construct an infinite rational-distance subset of the transformed irreducible cubic and prove all image points satisfy the transformed equation.
4. Audit injectivity/involutivity of rational-radius inversion on the punctured plane so infinitude is preserved by an explicit Lean theorem, not an informal image claim.
5. State the exact next genus-level contract for the irreducible cubic. Search installed Mathlib for normalization, nonsingularity, genus, and birational-invariance APIs; if unavailable, return a declaration-level blocker and prove the strongest elementary singularity or degree lemma that advances that contract.

Do not encode normalization, genus, Bézout, Riemann--Hurwitz, Faltings, or the Solymosi--de Zeeuw conclusion as axioms, opaque declarations, source wrappers, or `True`. The minimum deliverable is a marker-free irreducible-degree-three inversion theorem; the preferred deliverable also transports the infinite rational-distance zero locus.""",
        "contexts": base.existing(
            "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round14_20260711_2h/runs/erdos212-inversion-zero-locus-transfer/erdos212-inversion-zero-locus-transfer-supervised-2h/summary.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round14_20260711_2h/runs/erdos212-inversion-zero-locus-transfer/erdos212-inversion-zero-locus-transfer-supervised-2h/supervisor/round-018/decision.md",
        ),
    },
]


def statement_for(target: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# Supervised 4h Proof Attack: {target['title']}",
            "",
            f"Problem id: `{target['problem_id']}`",
            "Batch: `erdos3_866_1084_212_round15_20260711_4h`",
            "",
            "Run policy:",
            "- Use AMRA `run-campaign-loop` in proof-lab mode.",
            "- Invoke the global Codex supervisor after every round.",
            "- Search and primary-source grounding are enabled where relevant.",
            "- Retarget only to exact intermediate theorems advancing the stated route.",
            "- Use isolated Lean probes before formalizer promotion.",
            "- Reject `sorry`, axioms, opaque/source-marker substitutions, and conditional-to-unconditional relabeling.",
            "- End with a verified theorem, exact next contract, or diagnostic-backed blocker.",
            "",
            "Focus:",
            target["focus"],
            "",
        ]
    )


base.statement_for = statement_for
original_campaign_command = base.campaign_command


def campaign_command(
    target: dict[str, Any], statement_path: Path, output_root: Path
) -> list[str]:
    command = original_campaign_command(target, statement_path, output_root)
    run_name_index = command.index("--run-name") + 1
    command[run_name_index] = f"{target['slug']}-supervised-4h"
    return command


base.campaign_command = campaign_command


def main() -> None:
    base.main()
    base.write_text(
        base.RUN_ROOT / "plan.md",
        """# Round 15 Plan

1. Erdos #866: compose the verified seventh-power construction into a `gFun 7` bound, transfer `SumK5Free` to larger ambient intervals, and derive an all-large-`N` `3/7` lower bound with explicit constants.
2. Erdos #1084: abandon the blocked external checkout for this round and formalize a local half-open horizontal-ray crossing parity route for the verified non-self-intersecting polygonal cycle.
3. Erdos #212: package inversion of a noncircle irreducible quadratic as an irreducible cubic carrying an infinite rational-distance zero locus, then isolate the exact genus-level blocker.
4. Run all three supervised proof-lab campaigns in parallel for at most four hours with global review after every round.
5. Reject `sorry`, axioms, opaque/source-marker substitutions, unchecked Jordan imports, and conditional-to-unconditional relabeling.
""",
    )


if __name__ == "__main__":
    main()
