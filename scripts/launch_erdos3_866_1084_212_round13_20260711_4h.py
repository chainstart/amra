#!/usr/bin/env python3
"""Launch round 13 for Erdos #866/#1084/#212 with supervised proof-lab loops."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
BASE_PATH = REPO / "scripts/launch_erdos3_866_1084_212_round11_20260710_4h.py"


def load_base():
    spec = importlib.util.spec_from_file_location("erdos_round11_launcher", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load launcher: {BASE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_base()
base.RUN_ROOT = (
    REPO
    / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round13_20260711_4h"
)


base.TARGETS = [
    {
        "priority": 1,
        "slug": "erdos866-k7-sumgraph-reduction",
        "problem_id": "erdos-866",
        "title": "Erdos #866 k=7 finite sum-graph reduction",
        "focus": """Treat the verified `k = 6` two-sided estimate and the verified general-`k` upper bound as closed. Do not reopen CES75 upper, Sidon, or asymptotic-majorant targets.

Begin the first genuinely open case `k = 7` by proving a faithful finite reduction to a `K_5`-free sum graph.

Required mathematical route:
1. Prove a witness-bounding lemma: if at least three distinct integers have every pairwise sum in `[1,2*N]`, then each witness lies in an explicit finite interval, preferably `[1-N, 2*N-1]` after checking integer rounding exactly.
2. Define a finite sum graph for `E`: vertices are the bounded possible witnesses and `x ~ y` iff `x != y` and `x+y ∈ E`.
3. Let `O_N` be all odd integers in `[1,2*N]`, let `E ⊆ [1,2*N]` consist only of integers congruent to `2 mod 4`, and set `A := O_N ∪ E`.
4. Prove that seven pairwise-sum witnesses for `A` contain at most two even witnesses and therefore five distinct odd witnesses whose ten pairwise sums all lie in `E`; equivalently the sum graph of `E` contains `K_5`.
5. Package the contrapositive as an exact Lean theorem such as `gFun_seven_gt_of_sumCliqueFree`, including the cardinality of `A` and the bridge to `gFun 7 N`.
6. In parallel, design a reproducible SAT/CP-SAT or lazy-clique search for small `N` maximizing `|E|` under the `K_5`-free constraint. Computation is conjecture evidence only and must be stored separately from the proof.

The deliverable is the verified reduction theorem plus a finite-search specification or initial data. Do not claim a new exponent, import an unverified extremal theorem, or confuse positive witnesses with arbitrary integer witnesses. The supervisor should promote only small exact Lean lemmas that lead to the final reduction.""",
        "contexts": base.existing(
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Base.lean",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866.lean",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round12_20260711_4h/runs/erdos866-general-k-upper/erdos866-general-k-upper-supervised-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round11_20260710_4h/runs/erdos866-g6-sqrt-lower-sidon/erdos866-g6-sqrt-lower-sidon-supervised-4h/summary.md",
            "artifacts/source_papers/ces75/text/choi_erdos_szemeredi_1975-39.txt",
        ),
    },
    {
        "priority": 2,
        "slug": "erdos1084-polygonal-addcircle-constructor",
        "problem_id": "erdos-1084",
        "title": "Erdos #1084 polygonal AddCircle constructor",
        "focus": """Treat `PolygonalCycleCertificate`, all endpoint-incidence lemmas, edge-path injectivity, `distinct_edge_eq_imp_cyclic_incidence`, and `polygonalCircleMap_injective_of_edgewise` as completed. Do not retry them or audit unrelated repository placeholders.

Construct the missing continuous piecewise-affine map from the additive circle to the polygonal cycle.

Required route:
1. Inspect and probe the exact installed APIs for `AddCircle.liftIco`, `AddCircle.liftIco_continuous`, quotient/descent maps, finite interval gluing, `Path.segment`, and `ContinuousMap`.
2. Define a piecewise function on one real period `[0,n]`: on `[i,i+1]` it must evaluate to the segment from `cert.vertex i.castSucc` to `cert.vertex i.succ` with local parameter `t-i`.
3. Prove adjacent pieces agree at integer endpoints and prove the `0/n` seam using `cert.closed`.
4. Descend the periodic function to `AddCircle (n : Real)` and prove continuity and the exact half-open edgewise evaluation law.
5. Verify `Erdos1084.exists_polygonalCircleMap_edgewise`; then apply the completed injectivity theorem to obtain a continuous injective polygonal circle map.
6. Only after that constructor is certified, formulate the smallest Jordan-separation theorem needed for the Harborth face/boundary argument.

Use read-only Lean probes before promotion. If the broad constructor remains underspecified, return the smallest exact seam-continuity or `liftIco` theorem and prove that instead. Do not assume Jordan separation, faces, Euler, or the final contact bound.""",
        "contexts": base.existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round12_20260711_4h/runs/erdos1084-cycle-jordan-bridge/erdos1084-cycle-jordan-bridge-supervised-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round12_20260711_4h/runs/erdos1084-cycle-jordan-bridge/erdos1084-cycle-jordan-bridge-supervised-4h/supervisor/round-018/decision.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round11_20260710_4h/runs/erdos1084-harborth-full-proof-route/erdos1084-harborth-full-proof-route-supervised-4h/summary.md",
        ),
    },
    {
        "priority": 3,
        "slug": "erdos212-algebraic-curve-special-case",
        "problem_id": "erdos-212",
        "title": "Erdos #212 unconditional algebraic-curve special case",
        "focus": """Treat the four-quadric first-obstruction theorem and the no-go result for unconditional cross-fiber projected non-density as closed. Do not retry Bombieri--Lang, fiberwise Faltings, height, thinness, or source-marker routes.

Switch to the independent unconditional theorem of Solymosi--de Zeeuw: an irreducible real plane algebraic curve containing an infinite rational-distance set must be a line or a circle. Primary source: arXiv:0806.3095v2, `On a question of Erdos and Ulam`.

Required route:
1. Recover and audit the exact theorem statement, definitions of rational set and irreducible algebraic curve, exceptional line/circle cases, and every dependency in the published proof.
2. Separate elementary Euclidean/algebraic reductions from deep arithmetic inputs such as Faltings. Classify each dependency as available in Mathlib, source theorem, new local lemma, or unavailable.
3. Choose a Lean representation for a real plane algebraic curve that is compatible with the existing complex-plane rational-distance definitions.
4. Prove the strongest unconditional elementary step that can be checked locally: normalization from three fixed curve points to the associated distance equations, the genus calculation interface, or the topological corollary that a finite rational-distance subset cannot be dense.
5. Produce an exact dependency graph toward `no_infinite_rational_distance_subset_irreducible_curve_unless_line_or_circle` and one Lean-ready next theorem header.

Do not represent the Solymosi--de Zeeuw theorem or Faltings as `True`, an axiom, an opaque/source declaration, or an unconditional Lean fact without proof. If the installed library cannot support the algebraic-geometry layer, return a rigorous source/formalization blocker and preserve the elementary theorem proved in this round.""",
        "contexts": base.existing(
            "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round12_20260711_4h/runs/erdos212-cross-fiber-degeneracy-search/erdos212-cross-fiber-degeneracy-search-supervised-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round12_20260711_4h/runs/erdos212-cross-fiber-degeneracy-search/erdos212-cross-fiber-degeneracy-search-supervised-4h/supervisor/round-001/decision.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round11_20260710_4h/runs/erdos212-unconditional-first-obstruction/erdos212-unconditional-first-obstruction-supervised-4h/summary.md",
            "artifacts/source_papers/abt/abt_bombieri_lang_consequence_source_certificate.md",
        ),
    },
]


def statement_for(target: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# Supervised 4h Proof Attack: {target['title']}",
            "",
            f"Problem id: `{target['problem_id']}`",
            "Batch: `erdos3_866_1084_212_round13_20260711_4h`",
            "",
            "Run policy:",
            "- Use AMRA `run-campaign-loop` in proof-lab mode.",
            "- Invoke the global Codex supervisor after every round.",
            "- Search and primary-source grounding are enabled.",
            "- Retarget only to exact intermediate theorems that advance the stated objective.",
            "- Use small Lean probes before any formalizer promotion.",
            "- Reject `sorry`, axioms, opaque/source-marker substitutions, and conditional-to-unconditional relabeling.",
            "- End with a verified theorem, precise next target, or rigorous freeze certificate.",
            "",
            "Focus:",
            target["focus"],
            "",
        ]
    )


base.statement_for = statement_for


def main() -> None:
    base.main()
    base.write_text(
        base.RUN_ROOT / "plan.md",
        """# Round 13 Plan

1. Erdos #866: reduce the first open case `k = 7` to a finite `K_5`-free sum-graph extremal problem and specify small-instance search.
2. Erdos #1084: construct the continuous piecewise-affine `AddCircle` map for a verified polygonal cycle certificate, then prepare the Jordan bridge.
3. Erdos #212: leave the frozen Bombieri--Lang surface route and formalize the unconditional algebraic-curve special case from Solymosi--de Zeeuw.
4. Run all three proof-lab campaigns in parallel for at most four hours with global supervisor review every round.
5. Reject `sorry`, axioms, opaque/source-marker substitutions, and conditional-to-unconditional relabeling.
""",
    )


if __name__ == "__main__":
    main()
