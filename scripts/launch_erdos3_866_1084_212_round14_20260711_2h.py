#!/usr/bin/env python3
"""Launch round 14 for Erdos #866/#1084/#212 with two-hour supervised loops."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROUND13_PATH = REPO / "scripts/launch_erdos3_866_1084_212_round13_20260711_4h.py"


def load_round13():
    spec = importlib.util.spec_from_file_location("erdos_round13_launcher", ROUND13_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load launcher: {ROUND13_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


round13 = load_round13()
base = round13.base
base.RUN_ROOT = (
    REPO
    / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round14_20260711_2h"
)
base.TIME_BUDGET_SECONDS = 2 * 60 * 60
base.ROUND_TIME_BUDGET_SECONDS = 30 * 60
base.HARD_TIMEOUT_SECONDS = base.TIME_BUDGET_SECONDS + 15 * 60


base.TARGETS = [
    {
        "priority": 1,
        "slug": "erdos866-k7-seven-distinct-pairsums",
        "problem_id": "erdos-866",
        "title": "Erdos #866 k=7 seven-distinct-pair-sums lemma",
        "focus": """Treat the complete finite `k = 7` reduction, hyperedge characterization, optimizer bound, and executable checker from round 13 as closed. Do not repeat the finite reduction, CES75, the `k = 6` proof, or the general upper bound. Do not spend this round rebuilding the optional small-N optimizer.

Open the probabilistic/deletion route toward a genuine asymptotic lower bound for `gFun 7`. The first exact combinatorial input is that five distinct integers determine at least seven distinct unordered pair sums.

Required route:
1. Prove the exact Lean theorem
   ```lean
   theorem sumK5PairSums_card_ge_seven
       (C : Finset ℤ) (hC : C.card = 5) :
       7 ≤ (sumK5PairSums C).card
   ```
   Prefer an ordered enumeration `a₀ < ... < a₄` and the strict chain
   `a₀+a₁ < a₀+a₂ < a₀+a₃ < a₀+a₄ < a₁+a₄ < a₂+a₄ < a₃+a₄`.
2. Package the consequence that every `S ∈ sumK5Hyperedges N` has `7 ≤ S.card`.
3. Audit the finite count of possible five-witness sets in `sumK5Witnesses N` and state a Lean-ready upper bound on `sumK5Hyperedges N.card` sufficient for a random-subset/deletion argument.
4. If time remains, formulate the exact finite hypergraph deletion lemma needed to obtain an admissible `E` of order `N^(3/7)`; keep probability expectations and integer rounding explicit.

The primary deliverable is the marker-free Lean proof of the seven-distinct-sums theorem and its hyperedge corollary. Do not claim the `3/7` exponent until the random construction, bad-edge deletion, constants, and final bridge to `gFun 7` are all proved.""",
        "contexts": base.existing(
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Base.lean",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866.lean",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round13_20260711_4h/runs/erdos866-k7-sumgraph-reduction/erdos866-k7-sumgraph-reduction-supervised-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round13_20260711_4h/runs/erdos866-k7-sumgraph-reduction/erdos866-k7-sumgraph-reduction-supervised-4h/supervisor/round-017/decision.md",
        ),
    },
    {
        "priority": 2,
        "slug": "erdos1084-jordan-dependency-integration",
        "problem_id": "erdos-1084",
        "title": "Erdos #1084 Jordan dependency integration",
        "focus": """Treat the polygonal period map, continuous `AddCircle` map, and injective wrapper from round 13 as closed. Do not reprove constructors, edgewise evaluation, or injectivity. This is a separately scoped dependency-integration and theorem-adapter campaign for the first Jordan-separation node.

Required route:
1. Locate the exact upstream `epfl-lara/jordan-curve-theorem` / `HOLLight-Lean` repository, pin a commit, record its Lean and mathlib toolchain, and identify the exact Jordan separation declarations and hypotheses. Use only primary repository files and checked source.
2. In an isolated artifact/dependency workspace, compile the upstream theorem under its pinned toolchain and run `#print axioms` on every declaration proposed for import. Do not modify the production lake configuration until the isolated build succeeds.
3. Determine whether a theorem can be transported to the current map supplied by `Erdos1084.exists_injective_polygonalCircleMap`. State the exact adapter theorem relating the upstream simple-closed-curve predicate to the current continuous injective `AddCircle` map.
4. If the upstream development can be integrated safely, compile the smallest adapter and prove a separation statement giving two complementary components with the polygonal image as common frontier.
5. If version incompatibility remains, switch once to a local polygonal route and prove the smallest exact ray-crossing/parity lemma for a non-self-intersecting polygonal cycle. Return a concrete compiler diagnostic and compatibility matrix rather than another generic freeze report.

Reject `sorry`, axioms, opaque/source markers, theorem-name guesses, and unchecked imports. Success means a compiled and axiom-audited Jordan declaration plus a Lean-ready adapter, or a verified local polygonal separation lemma that strictly advances the face argument.""",
        "contexts": base.existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round13_20260711_4h/runs/erdos1084-polygonal-addcircle-constructor/erdos1084-polygonal-addcircle-constructor-supervised-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round13_20260711_4h/runs/erdos1084-polygonal-addcircle-constructor/erdos1084-polygonal-addcircle-constructor-supervised-4h/supervisor/round-007/decision.md",
        ),
    },
    {
        "priority": 3,
        "slug": "erdos212-inversion-zero-locus-transfer",
        "problem_id": "erdos-212",
        "title": "Erdos #212 inversion zero-locus transfer",
        "focus": """Treat all round-13 normalization, descent, irreducibility, homogenization, prime/homogeneous ideal, rational-distance inversion, inversion-evaluation, and divisibility-equivalence declarations as Lean-verified and closed. In particular, do not spend a round recertifying `unitCirclePolynomial_dvd_planePolynomialUnitCircleInversion_iff`; it has already passed a fresh full-file Lean build.

Continue the Solymosi--de Zeeuw low-degree inversion branch by proving that the polynomial pullback has exactly the expected zero locus away from the inversion center.

Required route:
1. Prove the exact algebraic target, or an equivalent header with the denominator named by `let`:
   ```lean
   theorem planePolynomialUnitCircleInversion_eval_inverted_eq_zero_iff
       {K : Type*} [Field K]
       (f : MvPolynomial (Fin 2) K) (x y : K)
       (hQ : x ^ 2 + y ^ 2 ≠ 0) :
       MvPolynomial.eval
           ![x / (x ^ 2 + y ^ 2), y / (x ^ 2 + y ^ 2)]
           (planePolynomialUnitCircleInversion f) = 0 ↔
         MvPolynomial.eval ![x, y] f = 0
   ```
   Derive it from `planePolynomialUnitCircleInversion_eval`, the involutivity calculation, and nonvanishing of the scalar factor.
2. Package the pointwise result as a set-level zero-locus transfer under unit-circle inversion away from `x²+y²=0`.
3. Combine that transfer with `euclideanPairwiseRationalDistances_rationalRadiusInversion` to state the exact next curve-level theorem for an infinite rational-distance subset.
4. Audit the next strict-transform issue: identify precisely which `Q` factor must be removed and formulate a theorem connecting the verified divisibility iff to the non-line/non-circle hypothesis. Do not assert irreducibility or degree growth without proof.

The deliverable is a marker-free Lean zero-locus transfer theorem and one exact next strict-transform contract. Do not introduce normalization, genus, Bézout, Riemann--Hurwitz, Faltings, or source wrappers as unconditional facts.""",
        "contexts": base.existing(
            "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round13_20260711_4h/runs/erdos212-algebraic-curve-special-case/erdos212-algebraic-curve-special-case-supervised-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round13_20260711_4h/runs/erdos212-algebraic-curve-special-case/erdos212-algebraic-curve-special-case-supervised-4h/supervisor/round-024/decision.md",
        ),
    },
]


def statement_for(target: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# Supervised 2h Proof Attack: {target['title']}",
            "",
            f"Problem id: `{target['problem_id']}`",
            "Batch: `erdos3_866_1084_212_round14_20260711_2h`",
            "",
            "Run policy:",
            "- Use AMRA `run-campaign-loop` in proof-lab mode.",
            "- Invoke the global Codex supervisor after every round.",
            "- Search and primary-source grounding are enabled.",
            "- Retarget only to exact intermediate theorems advancing this objective.",
            "- Use isolated probes before formalizer promotion or dependency changes.",
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
    command[run_name_index] = f"{target['slug']}-supervised-2h"
    return command


base.campaign_command = campaign_command


def main() -> None:
    base.main()
    base.write_text(
        base.RUN_ROOT / "plan.md",
        """# Round 14 Plan

1. Erdos #866: prove five integers have at least seven distinct pair sums, then transfer the bound to every finite reduction hyperedge.
2. Erdos #1084: pin, compile, and axiom-audit the Jordan development, then build the smallest adapter to the verified polygonal circle map; use a local polygonal parity lemma only if integration fails concretely.
3. Erdos #212: prove inversion zero-locus equivalence away from the center, package set-level transfer, and isolate the strict-transform factor-removal theorem.
4. Run all three supervised proof-lab campaigns in parallel for at most two hours with global review after every round.
5. Reject `sorry`, axioms, opaque/source-marker substitutions, unchecked imports, and conditional-to-unconditional relabeling.
""",
    )


if __name__ == "__main__":
    main()
