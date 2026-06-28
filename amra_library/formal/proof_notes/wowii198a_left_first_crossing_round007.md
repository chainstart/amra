# Round 007 terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt

- External sources used: none.
- Local verifier initially fails at `Wowii198aLeftmost.lean:4589:10` and `4676:12`: both are residual membership obligations inside `terminal_set_fan_left_suffix_retention_bad_pivot_descent` where `hpair_measure_min` was left as a placeholder.
- Current first blocker to `conjecture198a`: prove or replace the suffix-retention bad-pivot descent needed by `terminal_set_fan_left_suffix_retention_alt_intersections_control`, then the left first-crossing uncrossing lemma, left/right splice descents, two-fan theorem, longest-path missed-vertex contradiction, Chvatal-Erdos traceability.
- Tool check: a small Python order/support model showed the local left-branch residual containment is not implied by the current local hypotheses alone. In the model, `hfirst` holds, `z` is a left-prefix bad pivot after `w`, and a residual `y` lies in `rs.dropUntil z` and old-right support while not lying in old-left support or `altRight`. This falsifies the direct proof obligation at line 4589 as a standalone containment claim; the branch needs the intended extremal or weighted-measure argument.

## Round 001 follow-up

- External sources used: none.
- Current first blocker remains between `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt` and `conjecture198a`: the live Lean file does not yet prove `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, which is required by `terminal_set_fan_left_suffix_retention_alt_intersections_control`, then by the left first-crossing uncrossing lemma, left/right splice descents, the two-fan theorem, longest-path missed-vertex contradiction, Chvatal-Erdos traceability, and finally `conjecture198a`.
- Direct verifier failure is still the two residual erased-common containment branches inside `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, where the file tries to use weighted minimality as a membership proof. The theorem-level repair must select an extremal bad pivot or derive an actual weighted-measure contradiction for the residual intersections.

## Round 002 follow-up

- External sources used: none.
- Read the supplied `context_bundle.md` and `math_tools_report.md`; no web or
  literature source was used.
- Required verifier still fails before reaching
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, at the two
  residual membership goals in
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`.
- Python support-order probe for the old-left-prefix branch:
  `rs = [v,w,z,y,s]`, `old_left = [v,z,x,s]`,
  `old_right = [v,w,x,y,t]`.  Here `hfirst` holds with first old-support hit
  `w`, `x` is retained in `old_right.dropUntil w`, `z` is a bad pivot in
  `altRight`, and the secondary left splice has erased common support `{y}`.
  Since the old common support is `{x}`, the needed containment into
  `oldCommon.erase x` is false for an arbitrary bad pivot.
- This confirms the next Lean target should not be another local rewrite at
  lines 4589/4676.  The missing theorem-level package is an extremal bad-pivot
  or weighted-measure descent lemma that selects the relevant first/last bad
  pivot before constructing the secondary splice.

## Round 003 follow-up

- External sources used: none.
- Current first blocker remains
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, which is needed
  by `terminal_set_fan_left_suffix_retention_alt_intersections_control`, then
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, then the
  left/right splice descents, the two-fan theorem, longest-path missed-vertex
  contradiction, Chvatal-Erdos traceability, and finally `conjecture198a`.
- Required verifier command:
  `env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`
  failed with the same two Lean errors at lines 4589 and 4676.  In both
  branches the proof term `hpair_measure_min` is being used where Lean needs a
  membership proof
  `y ∈ (((pair.1.support.toFinset ∩ pair.2.support.toFinset).erase v).erase x)`.
- A bounded Python search over small path-pair configurations was started to
  look for a full finite counterexample to the arbitrary-pivot statement, but
  was interrupted after it did not finish quickly.  The earlier local
  support-order model remains the useful obstruction: arbitrary bad pivots do
  not give the erased-common containment directly.  The next repair should
  prove an extremal bad-pivot/weighted-measure descent package instead of
  replacing the two `hpair_measure_min` occurrences with local membership
  rewrites.

## Round 004 follow-up

- External sources used: none.
- Read the supplied `context_bundle.md` and `math_tools_report.md`; no web or
  literature source was used.
- The current first blocker is still
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, needed by
  `terminal_set_fan_left_suffix_retention_alt_intersections_control`, then
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, then the
  left/right splice descents, the two-fan theorem, the longest-path missed
  vertex contradiction, Chvatal-Erdos traceability, and `conjecture198a`.
- Required verifier command failed only at the same two residual support
  obligations:
  `Wowii198aLeftmost.lean:4589:10` and `4676:12`, where
  `hpair_measure_min` is used as a membership proof in
  `(((pair.1.support.toFinset ∩ pair.2.support.toFinset).erase v).erase x)`.
- Python support-order check for both residual branches:
  left branch `rs = [v,w,z,y,s]`, `old_left = [v,z,x,s]`,
  `old_right = [v,w,y,x,t]`; right branch `rs = [v,w,y,z,s]`,
  `old_left = [v,y,x,s]`, `old_right = [v,w,x,z,t]`.
  In both models the local first-hit/support premises hold at the level of
  path order, the new splice common support is `{y}`, and the old common
  support with `x` erased is empty.  Thus the exact containment obligations at
  lines 4589 and 4676 are false as local arbitrary-pivot claims.
- Next Lean repair should introduce or prove the missing extremal-pivot or
  weighted-measure descent package.  A direct proof of the current containment
  goals by local support rewriting is not a viable route.

## Round 005 follow-up

- External sources used: none.  I used only the supplied local context bundle,
  supplied math tools report, local Lean source, and local proof notes.
- Current first blocker remains
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent`, which is needed
  by `terminal_set_fan_left_suffix_retention_alt_intersections_control`, then
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, then the
  left/right splice descents, the two-fan theorem, the longest-path missed
  vertex contradiction, Chvatal-Erdos traceability, and `conjecture198a`.
- The required verifier still fails before it can certify
  `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`: the two
  stale proof terms at lines 4589 and 4676 use `hpair_measure_min` where Lean
  needs membership in
  `(((pair.1.support.toFinset ∩ pair.2.support.toFinset).erase v).erase x)`.
- Reran `proof_notes/wowii198a_suffix_retention_round003_countermodel_search.py`.
  It again reported no countermodel in the shaped six-vertex search and no
  countermodel in 2000 random six-vertex graphs under the encoded
  weighted-minimality assumptions.
- Also scanned the target file for `sorry`, `admit`, `axiom`, `constant`,
  `opaque`, and ARA placeholder markers; none were present.
- The next Lean edit should not try to fill those two membership goals
  directly.  The required theorem-level package must select an order-extremal
  bad pivot on `rs` and then prove either the secondary splice containment for
  that extremal pivot or a strict `terminalPathPairWeightedMeasure` descent
  contradicting `hpair_measure_min`.
