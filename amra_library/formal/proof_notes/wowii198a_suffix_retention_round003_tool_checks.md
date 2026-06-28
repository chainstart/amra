# WOWII198a suffix-retention round 003 tool checks

Date: 2026-06-27

No external sources were used.

Finite route checks:

- A path-only Python search found a countermodel to the requested
  intersection-control conclusion if weighted minimality is omitted. This
  confirms the lemma must use `hpair_measure_min`, not just support containment
  and the first-hit hypothesis.
- Exhaustive Python search over all simple graphs on 5 vertices, enforcing that
  `pair` is globally minimal for `terminalPathPairWeightedMeasure` among simple
  terminal paths, found no counterexample.
- Exhaustive Python search over all simple graphs on 6 vertices with terminal
  paths from `v = 0` to `s = 1` and `t = 2` also found no counterexample
  (`29148` graphs with both terminal path families nonempty checked).
- Iteration 2 reran an independent exhaustive Python check over all simple
  graphs through 5 vertices, this time approximating `Walk.toPath` by
  chronological loop erasure of the explicit alternate walk
  `oldLeft.takeUntil x ++ oldRight.dropUntil x`.  Under global weighted
  minimality, `hdirect`, `hfirst`, and suffix retention, it again found no
  counterexample to the requested alternate-intersection control statement.
- Iteration 3 added
  `proof_notes/wowii198a_suffix_retention_round003_countermodel_search.py`.
  The script checked a hand-shaped six-vertex later-crossing pattern and 2000
  random six-vertex graphs.  It found no countermodel once global weighted
  minimality was enforced.  This supports the same conclusion as the earlier
  checks: the missing Lean ingredient is a first/last bad-pivot weighted
  descent, not a direct suffix-exclusion fact.

Lean audit remains authoritative; these checks only validate that the current
missing proof obligation is plausibly a weighted-minimality descent rather than
a false theorem statement.

Iteration 4 update:

- Re-read the proof-lab context bundle and math tools report before editing.
  No external web/literature sources were used.
- Reran `proof_notes/wowii198a_suffix_retention_round003_countermodel_search.py`.
  It again reported no countermodel in the shaped six-vertex search and no
  countermodel in 2000 random six-vertex graphs.
- Local Lean inspection shows the two target-theorem failures are exactly the
  two bad-pivot branches:
  `z ∈ rs.support ∩ (oldLeft.takeUntil x).support` with `z ∉ oldRight.support`,
  and `z ∈ rs.support ∩ (oldRight.dropUntil x).support` with
  `z ∉ oldLeft.support`.
- The downstream wrapper failures at the left/right splice lemmas are not
  independent syntax problems.  A direct call to the left first-crossing lemma
  is blocked because the wrapper currently obtains a first-hit fact only for
  the opposite old path, while the parent lemma requires first-hit control for
  the union of both old supports.  The needed next package is therefore still a
  first/last bad-pivot weighted-descent lemma under global weighted minimality.
