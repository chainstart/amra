#!/usr/bin/env python3
"""Launch the next four-hour supervised round for Erdos #866/#1084/#212."""

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
    / "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round12_20260711_4h"
)


base.TARGETS = [
    {
        "priority": 1,
        "slug": "erdos866-general-k-upper",
        "problem_id": "erdos-866",
        "title": "Erdos #866 general-k CES upper bound",
        "focus": """The complete `k = 6` estimate `gFun 6 N = Theta(sqrt N)` is Lean-verified. Treat that route as closed.

Promote the known general Choi--Erdos--Szemeredi upper bound into the current checked workspace:

```lean
theorem erdos866_general_upper (k : Nat) (hk : 3 <= k) :
  exists N0 : Nat, forall n : Nat, N0 <= n ->
    gFun k n <= hFun k n and
    (hFun k n : Real) <
      4 * (n : Real) ^ ((1 : Real) - 1 / 2 ^ ((k : Real) - 2))
```

Required route:
1. Audit the archived declarations `ceslemgeneral_pos_with_bound`, `hk_upper_aux`, `hk_upper`, and `generalupper`; accept no theorem merely because it appears in an old artifact.
2. Map every dependency to the current `ErdosProblem866Base.lean` definitions and identify the first missing checked helper.
3. Reprove or faithfully port the missing `boundPos_n` comparison and asymptotic real-power estimates with current Mathlib APIs.
4. Verify `gFun_le_hFun` under the integer-versus-positive witness conventions.
5. Build the exact final theorem with no `sorry`, new axioms, opaque constants, source markers, or reliance on the completed special `k = 6` theorem.

Use proof-lab to select Lean-ready intermediate declarations and let the supervisor promote them sequentially. The result is a known general upper bound, not a claim that the full open problem is solved.""",
        "contexts": base.existing(
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866Base.lean",
            "projects/erdos-866-ai-continuation-20260505/formal/MathProject/ErdosProblem866.lean",
            "artifacts/proof_lab/erdos866_sources_20260506/ErdosProblem866.lean",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round11_20260710_4h/runs/erdos866-g6-sqrt-lower-sidon/erdos866-g6-sqrt-lower-sidon-supervised-4h/summary.md",
            "artifacts/source_papers/ces75/text/choi_erdos_szemeredi_1975-39.txt",
        ),
    },
    {
        "priority": 2,
        "slug": "erdos1084-cycle-jordan-bridge",
        "problem_id": "erdos-1084",
        "title": "Erdos #1084 cycle realization and Jordan bridge",
        "focus": """Treat the verified contact-neighbor angle lemmas, contact-edge open-segment disjointness lemmas, `StraightLinePlaneDrawing`, the contact-graph drawing constructor, and `edge_segments_inter_subset_common_endpoints` as completed. Do not retry them.

Attack the next exact Harborth blocker: realize a simple graph cycle in a straight-line plane drawing as a simple polygonal loop, cleanly separating the finite combinatorial geometry from the later Jordan-separation theorem.

Required route:
1. Inspect `SimpleGraph.Walk`, `Walk.IsCycle`, support/edge APIs, cyclic lists, `Path`, `ContinuousMap`, and piecewise-linear segment APIs in the installed Mathlib.
2. Select a minimal project-local representation of a cycle's ordered vertices and polygonal edges.
3. Prove injectivity of cycle vertices and disjointness of nonadjacent edge interiors using the completed straight-line drawing certificate.
4. Produce and typecheck the first executable Lean theorem header for polygonal simplicity.
5. Audit whether Mathlib contains a Jordan theorem applicable to this representation. If not, state the minimal local Jordan polygon contract, its precise hypotheses, and the proof route needed before Euler/face and Harborth boundary estimates.

Do not assume faces, an outer cycle, Euler's formula for the drawing, or the final Harborth inequality. No source proposition, axiom, opaque declaration, or unrelated repository-wide `sorry` audit is allowed.""",
        "contexts": base.existing(
            "data/research_open/raw/formal_conjectures/FormalConjectures/ErdosProblems/1084.lean",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round11_20260710_4h/runs/erdos1084-harborth-full-proof-route/erdos1084-harborth-full-proof-route-supervised-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round11_20260710_4h/runs/erdos1084-harborth-full-proof-route/erdos1084-harborth-full-proof-route-supervised-4h/supervisor/round-013/decision.md",
            "artifacts/open_problem_screening/latest/lean_loop_8_20260527_5h/source_statements/02-source-harborth-erdos1084.md",
        ),
    },
    {
        "priority": 3,
        "slug": "erdos212-cross-fiber-degeneracy-search",
        "problem_id": "erdos-212",
        "title": "Erdos #212 unconditional cross-fiber degeneracy search",
        "focus": """Treat `dense_euclidean_rational_distance_fourQuadric_firstObstruction` and its normalization, lift, and general-position dependencies as completed. Do not redo the topology container, conditional Bombieri--Lang endgame, or vertical-fiber finiteness surrogate.

Reopen the arithmetic route only to search for a genuine unconditional cross-fiber mechanism applicable to the forced general-position four-quadric family.

Required route:
1. Audit primary literature after ABT for unconditional results on rational points in this exact family, including uniformity, degeneracy, thin-set, Hilbert irreducibility, determinant-method, or special complete-intersection results.
2. Determine whether the special four-quadric surfaces have additional structure not used by the generic Bombieri--Lang argument.
3. Test concrete algebraic eliminations and low-degree exceptional loci symbolically, but clearly separate computation from proof.
4. State and prove a cross-fiber lemma only if it is unconditional and strong enough to constrain a dense union of fibers. A theorem controlling each fiber separately is insufficient.
5. If no such result exists, produce a rigorous no-go certificate identifying exactly why each candidate route fails and which statement would imply the original open problem.

Do not create another conditional wrapper, `True`-elaborating source declaration, trusted assumption, or projected-non-density theorem without proof. The supervisor should freeze promptly if source and structural audits yield no credible unconditional route.""",
        "contexts": base.existing(
            "amra_library/formal/AmraLibrary/OpenProblemBatches/ErdosFiveQueue20260704/Erdos212.lean",
            "artifacts/source_papers/abt/abt_bombieri_lang_consequence_source_certificate.md",
            "artifacts/source_papers/abt/abt_closed_proper_plane_image_source_certificate.md",
            "artifacts/source_papers/abt/abt_compactified_split_surface_objects_source_certificate.md",
            "artifacts/source_papers/abt/abt_projection_finite_away_from_bad_locus_source_certificate.md",
            "artifacts/source_papers/abt/abt_scaled_resolution_transport_source_certificate.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round11_20260710_4h/runs/erdos212-unconditional-first-obstruction/erdos212-unconditional-first-obstruction-supervised-4h/summary.md",
            "artifacts/open_problem_screening/latest/erdos3_866_1084_212_round11_20260710_4h/runs/erdos212-unconditional-first-obstruction/erdos212-unconditional-first-obstruction-supervised-4h/supervisor/round-011/decision.md",
        ),
    },
]


def statement_for(target: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# Supervised 4h Proof Attack: {target['title']}",
            "",
            f"Problem id: `{target['problem_id']}`",
            "Batch: `erdos3_866_1084_212_round12_20260711_4h`",
            "",
            "Run policy:",
            "- Use AMRA `run-campaign-loop` in proof-lab mode.",
            "- Invoke the global Codex supervisor after every round.",
            "- Search and source grounding are enabled.",
            "- Retarget only to faithful intermediate theorems that advance the stated objective.",
            "- Tiny Lean probes are allowed; full formalizer work starts only after supervisor promotion.",
            "- Reject `sorry`, axioms, opaque/source-marker substitutions, and conditional-to-unconditional relabeling.",
            "- End with a verified theorem, a precise next target, or a rigorous freeze certificate.",
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
        """# Round 12 Plan

1. Erdos #866: keep the completed `k = 6` theorem closed and promote the known general-`k` CES upper bound into the current checked workspace.
2. Erdos #1084: build the graph-cycle polygonal realization and isolate the exact Jordan bridge needed before face counting and Harborth boundary estimates.
3. Erdos #212: search only for a genuine unconditional cross-fiber degeneracy theorem; otherwise produce a rigorous freeze certificate.
4. Run all three proof-lab campaigns in parallel for at most four hours with global supervisor review every round.
5. Reject `sorry`, axioms, opaque/source-marker substitutions, and conditional-to-unconditional relabeling.
""",
    )


if __name__ == "__main__":
    main()
