# WOWII198a left first-crossing round 009

Current first blocker between `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`
and `conjecture198a` is still
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`.  That lemma feeds
`terminal_set_fan_left_suffix_retention_alt_intersections_control`, then the
left first-crossing uncrossing lemma, left and right splice descents, the
two-fan theorem, the longest-path missed-vertex contradiction, Chvatal-Erdos
traceability, and finally `conjecture198a`.

External sources relied on:
- None from web or literature in this iteration.
- Local run context was read from the supplied `context_bundle.md` and
  `math_tools_report.md`.

Verifier:
- Command:
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`
- Result: failed.
- Lean reports exactly two type mismatches in
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, at lines 4589 and
  4676.  Both branches attempt to use `hpair_measure_min`, whose type is
  weighted-measure minimality, as a membership proof in
  `(((pair.1).support.toFinset ∩ (pair.2).support.toFinset).erase v).erase x`.

Tool check:
- Reran `proof_notes/wowii198a_suffix_retention_round003_countermodel_search.py`.
- Output:
  - `no countermodel in shaped six-vertex search`
  - `no countermodel in 2000 random six-vertex graphs`
- This supports the intended extremal/weighted route but is not a Lean proof.

Next proof target:
- Replace the arbitrary-pivot containment inside
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent` with an
  order-extremal bad pivot on `rs`.
- For that extremal pivot, prove the secondary splice containment, or derive a
  strict weighted-measure descent contradicting `hpair_measure_min`.
