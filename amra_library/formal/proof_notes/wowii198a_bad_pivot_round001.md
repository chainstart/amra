# WOWII198a bad-pivot round 001

Current first blocker toward `conjecture198a`:
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`.

The required Lean verifier currently fails at the two residual containment
branches inside this theorem.  In both places, the proof tries to use
`hpair_measure_min` where Lean needs membership in
`(((pair.1.support.toFinset ∩ pair.2.support.toFinset).erase v).erase x)`.

No external web or literature sources were used.  Sources relied on in this
round were the local context bundle, local math tools report, and the Lean file.

## Local order obstruction

Python sanity model:

```text
L  = [v, z, x, s]
R  = [v, w, y, x, t]
rs = [v, w, z, y, s]
```

This satisfies the local facts used in the failed left-prefix containment
branch:

- `z ∈ rs.support`
- `z ∈ (L.takeUntil x).support`
- `z ∉ R.support`
- `z ∉ (rs.takeUntil w).support`
- `y ∈ (rs.dropUntil z).support`
- `y ∈ R.support`
- `y ≠ v`, `y ≠ w`

But `y ∉ L.support`, so `y` is not in the old erased common support with `x`
removed.  Thus the bare residual containment claim is false as a local support
fact.  The right-prefix branch has the symmetric issue.

## Replacement theorem shape

The replacement needed to keep the chain to `conjecture198a` is not a bare
containment lemma.  It must include the weighted-minimality conclusion:

```lean
-- schematic only
lemma bad_later_pivot_weighted_descent :
  -- first/last bad pivot chosen on rs, under the existing first-hit hypotheses
  -- and terminalPathPairWeightedMeasure minimality
  (∃ pair', terminalPathPairCommonCard pair' <
      terminalPathPairCommonCard pair)
  ∨
  (∃ pair', terminalPathPairCommonCard pair' =
      terminalPathPairCommonCard pair ∧
    terminalPathPairSupportLength pair' <
      terminalPathPairSupportLength pair)
```

The second disjunct contradicts `hpair_measure_min` after expanding
`terminalPathPairWeightedMeasure`.  This helper should be used inside
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`, then
`terminal_set_fan_left_suffix_retention_alt_intersections_control`, then
`terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, and from there
the left/right splice descent, two-fan theorem, longest-path missed-vertex
contradiction, Chvatal-Erdos traceability, and `conjecture198a`.

## Iteration 1 update, 2026-06-27

Re-read the requested context bundle and math tools report.  No web or
literature sources were used.

Reran the required verifier.  It still fails only at the two residual
containment branches inside
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`, where
`hpair_measure_min` is used as membership in the old erased common support.

Ran a fresh bounded Python search over labelled simple graphs through six
vertices, enforcing:

- global weighted minimality of `pair`;
- `hdirect`;
- first-hit control `hfirst`;
- suffix retention `hret`;
- existence of a bad `z` in `rs.support ∩ altRight.support`.

The search reported no counterexample through six vertices.  This is consistent
with the earlier searches: the theorem-level statement still appears viable,
but the local arbitrary-pivot containment is false without an extremal
first/last bad-pivot or weighted-measure descent argument.

## Iteration 2 update, 2026-06-27

Re-read the supplied context bundle and math tools report.  No external web or
literature sources were used; the only sources relied on were local run
context, local proof notes, local mathlib/Lean source grep results, and the
configured Lean verifier.

Lean progress:
- Added checked arithmetic helper
  `terminalPathPairWeightedMeasure_lt_of_commonCard_le_supportLength_lt`.
  It proves that a candidate terminal path pair with nonincreased
  `terminalPathPairCommonCard` and strictly smaller
  `terminalPathPairSupportLength` has strictly smaller
  `terminalPathPairWeightedMeasure`.
- Added checked contradiction wrapper
  `false_of_weighted_min_and_commonCard_le_supportLength_lt`, packaging the
  exact way such a lexicographic descent contradicts `hpair_measure_min`.

Verifier result:
- The helper compiles under the required command.
- The target theorem remains blocked at the same two conceptual branches,
  shifted to lines 4631 and 4718 after the helper insertion.  Both still ask
  for membership in
  `(((pair.1.support.toFinset ∩ pair.2.support.toFinset).erase v).erase x)`
  while the available term `hpair_measure_min` has only weighted-minimality
  type.

Next Lean step:
- Prove the extremal bad-pivot package that supplies, for the secondary splice,
  either erased-common containment or the common-card-nonincreasing plus strict
  support-length descent now packaged by the new helper.

## Iteration 3 update, 2026-06-27

Re-read the supplied context bundle and math tools report.  No external web or
literature sources were used; the only sources relied on were local run
context, local proof notes, local Lean/mathlib source, and the configured Lean
verifier.

Tool check:
- Ran a bounded Python graph/path check on the earlier local obstruction shape
  with vertices `v,w,z,y,x,s,t`, old paths `v-z-x-s` and `v-w-y-x-t`, and
  replacement path `v-w-z-y-s`.
- Enumerating simple `v-s` and `v-t` paths in the generated graph found lower
  weighted pairs, including common-support-zero alternatives.  Thus the local
  support obstruction is not a counterexample once global weighted minimality
  is enforced.

Lean progress:
- Added checked helper
  `exists_last_mem_support_forall_mem_dropUntil_imp_eq`.  It chooses a last
  member of a finite support subset along a simple walk, measured by
  `takeUntil` length, and proves that any member of the same finite set in the
  resulting `dropUntil` suffix is equal to the chosen vertex.

Verifier result:
- The new helper compiles.
- The required verifier still fails in
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent` at the two
  residual containment branches, now shifted to lines 4686 and 4773.  Both
  branches still try to use `hpair_measure_min` where Lean needs membership in
  the old erased common support with `x` erased.

Next Lean step:
- Refactor `terminal_set_fan_left_suffix_retention_bad_pivot_descent` to choose
  a last bad pivot from the finite set of bad `rs ∩ altRight` vertices using
  `exists_last_mem_support_forall_mem_dropUntil_imp_eq`; use maximality to rule
  out later residual bad vertices, and use the weighted descent helper for the
  remaining nonincreasing-common-card/strict-support-length case.

## Iteration 4 update, 2026-06-27

Re-read the supplied context bundle and math tools report.  No external web or
literature sources were used; the only sources relied on were local run
context, local proof notes, local Lean/mathlib source, and the configured Lean
verifier.

Lean progress:
- Added checked helper
  `exists_first_mem_support_forall_mem_takeUntil_imp_eq`.  It is the symmetric
  first-on-support counterpart to the existing last-on-support helper and
  proves that, after choosing the first member of a finite support subset along
  a walk, every member of the same subset in the corresponding `takeUntil`
  prefix is equal to the chosen vertex.

Verifier result:
- The new helper compiles under the required command.
- The required verifier still fails only in
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, with the same two
  residual containment obligations shifted to lines 4699 and 4786.  Both still
  require membership in
  `(((pair.1.support.toFinset ∩ pair.2.support.toFinset).erase v).erase x)`,
  while the available term `hpair_measure_min` has weighted-minimality type.

Next Lean step:
- Refactor the bad-pivot theorem around an extremal bad set rather than the
  current arbitrary `z`: use the last helper for old-left-prefix bad pivots and
  the new first helper for old-right-suffix bad pivots, then close the residual
  cases by erased-common containment or by the existing weighted
  common-card/support-length contradiction helper.

## Iteration 5 update, 2026-06-27

Re-read the supplied context bundle and math tools report. No external web or
literature sources were used; the only sources relied on were local run
context, local proof notes, local Lean/mathlib source, and the configured Lean
verifier.

Tool check:
- Reran `proof_notes/wowii198a_suffix_retention_round003_countermodel_search.py`.
- Output:
  - `no countermodel in shaped six-vertex search`
  - `no countermodel in 2000 random six-vertex graphs`

This remains route evidence only. It supports continuing the extremal
bad-pivot/weighted-measure route, but it is not a Lean proof.

Lean progress:
- Added checked helpers
  `mem_erase_common_without_x_or_not_common_triple` and
  `mem_erase_common_without_x_or_not_common_triple_left`. They package each
  residual intersection as either membership in the old erased common support
  with `x` removed, or as a genuine non-common bad pivot. This is the local
  classification needed by the extremal bad-pivot argument.

Verifier result:
- The helpers compile under the required command.
- The required verifier still fails only in
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, with the same two
  residual containment obligations shifted to lines 4745 and 4832. Both still
  require membership in
  `(((pair.1.support.toFinset ∩ pair.2.support.toFinset).erase v).erase x)`,
  while the available term `hpair_measure_min` has weighted-minimality type.

Next Lean step:
- Use the new classification helpers inside an extremal bad set on `rs`.
  The left-splice residual branch needs last-bad-pivot control for later
  replacement-side intersections; the right-splice residual branch needs
  first-bad-pivot control for earlier replacement-side intersections. If the
  extremal containment is not immediate, close the branch by the existing
  weighted common-card/support-length contradiction wrapper.

## Iteration 6 update, 2026-06-27

Re-read the supplied context bundle and math tools report. No external web or
literature sources were used; the sources relied on were local run context,
local proof notes, local Lean source, and the configured Lean verifier.

Verifier result:
- The required verifier still fails only in
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`.
- The two failures are the residual containment branches at lines 4745 and
  4832, where the proof still tries to use `hpair_measure_min` as membership
  in the old erased common support with `x` removed.

Lean assessment:
- The already-recorded support-order obstruction shows the bare local
  containment is false without converting the residual non-common intersection
  into an actual extremal bad-pivot or weighted-measure descent.
- The theorem-level statement is still supported by the prior finite searches
  under global weighted minimality, but the current proof body has not yet
  formalized the missing package.

Next Lean step:
- Prove a dedicated extremal helper: from a residual non-common vertex in the
  left branch, select the correct last bad pivot or derive
  common-card-nonincreasing plus strict support-length descent; mirror this
  with a first bad pivot for the right branch. Use the existing
  `false_of_weighted_min_and_commonCard_le_supportLength_lt` wrapper to turn
  the support-length descent into contradiction with `hpair_measure_min`.
