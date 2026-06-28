# Round 011 Harper Source Blocker

Target:
`harper_boolean_halfInitialSegment_minimizes_closedNeighborhood_source`

Current first blocker:
the target theorem is exactly Harper's Boolean-cube closed-neighborhood
minimization specialized to the local `booleanHalfInitialSegment`. The scratch
file has the downstream transfer lemma, but Mathlib in this workspace does not
expose Harper's theorem under the current imports, and the target cannot be
proved from the local definitions alone without formalizing that theorem.

External source reliance recorded for the route:
- Raty, arXiv:1806.11061, for Harper's simplicial-order Boolean-cube
  neighborhood minimization.
- Przykucki--Roberts, arXiv:1808.02572, for the closed-neighborhood/Hamming-ball
  formulation used by the transfer plan.

Lean/tool checks this iteration:
- `rg` search found no Harper/simplicial-order closed-neighborhood minimization
  theorem in the installed Mathlib tree.
- Mathlib does contain `Finset.kruskal_katona` and related shadow results in
  `Mathlib.Combinatorics.SetFamily.KruskalKatona`, but these are uniform-layer
  shadow minimization theorems and do not directly instantiate the arbitrary
  half-family closed-neighborhood target.
- A Lean `native_decide` probe confirmed the open quantified target shape cannot
  be closed by computation; Lean reports that the expected type must not contain
  free variables.

Next source-policy target:
provide either a formal import/proof of Harper's closed-neighborhood theorem or
a policy-approved source theorem interface for the exact statement before
returning to Lean proof repair.

Iteration 2 update:
- Re-read the round 011 context bundle and math tools report.
- Re-ran focused local `rg` searches over the installed Mathlib combinatorics
  tree. Mathlib exposes shadow, LYM, colex, and Kruskal-Katona infrastructure,
  but still no Harper/simplicial-order Boolean-cube closed-neighborhood
  minimization theorem that can instantiate the current source target.
- The scratch file remains build-clean and contains the transfer lemma, but
  adding
  `harper_boolean_halfInitialSegment_minimizes_closedNeighborhood_source`
  without importing/formalizing Harper would require a trusted assumption, which
  is forbidden for this run.
