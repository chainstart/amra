# WOWII198a finite two-fan round 003 notes

Date: 2026-06-26

Target:
`finite_two_fan_to_pair_of_terminal_set_no_small_endpoint_separator`

External sources:
None.

Tool check:
Ran a Python brute-force sanity check over all labelled simple graphs on
3, 4, and 5 vertices and all ordered distinct triples `(v, s, t)`. The check
tested the exact terminal-set separator hypothesis against existence of
simple `v-s` and `v-t` paths whose supports meet only at `v`.

Result:
No counterexamples up to 5 vertices. An attempted run through 6 vertices was
stopped because it was not useful for this Lean iteration.

Current Lean blocker:
Inside the positive branch of
`finite_two_fan_to_pair_of_terminal_set_no_small_endpoint_separator`, after
choosing a weighted-minimal terminal path pair with positive non-apex common
support and a singleton-avoiding terminal replacement path from `hsep`, the
missing formal step is the splicing/descent lemma:

Given the minimal pair, a non-apex common vertex `x`, and a terminal path
avoiding `{x}`, construct a new `G.Path v s × G.Path v t` whose
`terminalPathPairCommonCard` is strictly smaller. The construction must handle
new intersections introduced by the replacement path, likely by first/last
intersection splicing and the secondary support-length component of
`terminalPathPairWeightedMeasure`.

Iteration 2:
- External sources: none beyond the supplied local context bundle and math
  tools report.
- Lean/mathlib search: rechecked the local checkout for `SimpleGraph`
  Menger/Fan, max-flow/min-cut, separator, and vertex-disjoint path theorems;
  no usable checked theorem was found.
- Lean edit: replaced the final uninformative `exact hsep` branch with an
  explicit local obligation
  `∃ pair' : G.Path v s × G.Path v t,
    terminalPathPairCommonCard pair' < terminalPathPairCommonCard pair`,
  followed by the already-checked contradiction through
  `hpair_no_common_decrease`.
- Remaining blocker: prove that descent obligation from the minimal pair,
  non-apex common vertex `x`, and the `hsep` singleton-avoiding terminal path.

Iteration 3:
- External sources: none beyond the supplied local context bundle and math
  tools report.
- Python tool check: extended the brute-force sanity check to all labelled
  simple graphs on 6 vertices and all ordered distinct triples `(v, s, t)`.
  The script tested the exact terminal-set separator hypothesis against
  existence of simple `v-s` and `v-t` paths meeting only at `v`.
- Result: no counterexamples on 6 vertices.
- Lean edit: expanded the local `hdescent` obligation. The no-new-intersection
  branches now construct an explicit replacement `G.Path v s × G.Path v t`
  and prove its `terminalPathPairCommonCard` is smaller because the replacement
  pair has zero erased common support while the original minimal pair has
  positive erased common support.
- Remaining blocker: both symmetric splice cases remain. In each case, the
  singleton-avoiding replacement path avoids the old common vertex `x` but
  introduces a new non-apex intersection `y` with the opposite minimal path.
  The next proof step must splice at that intersection and use weighted
  minimality to produce a smaller common-support pair.

Iteration 4:
- External sources: none beyond the supplied local context bundle and math
  tools report.
- Python tool check: reran a bounded sanity check over all labelled simple
  graphs on 3, 4, and 5 vertices and all ordered distinct triples `(v, s, t)`.
  The script tested the exact terminal-set separator hypothesis against
  existence of simple `v-s` and `v-t` paths meeting only at `v`.
- Result: no counterexamples up to 5 vertices. A broader run toward 6 vertices
  was interrupted after it exceeded the useful time budget for this iteration.
- Current first blocker: the same two symmetric splice cases inside
  `finite_two_fan_to_pair_of_terminal_set_no_small_endpoint_separator`. The
  replacement path avoids `x` but has a new non-apex meeting point `y`; the
  missing Lean lemma must turn that configuration into a smaller
  `terminalPathPairCommonCard` witness or a weighted-minimality contradiction.

Iteration 5:
- External sources: none beyond the supplied local context bundle,
  `math_tools_report.md`, local mathlib grep/file inspection, and existing
  workspace proof notes. No web or literature search was used.
- Local mathlib check: searched the checked SimpleGraph connectivity files for
  Menger, fan, separator, and vertex-disjoint path theorems. No usable
  theorem-level result was present in this checkout.
- Lean edit: replaced the accidental `exact hsep` terms in the two symmetric
  splice branches with explicit missing lemma names:
  `terminal_set_fan_splice_descent_left_of_hsep` and
  `terminal_set_fan_splice_descent_right_of_hsep`.
- Current first blocker: prove either of those splice descent lemmas, or better
  one symmetric lemma parameterized by terminal order, constructing a new
  `G.Path v s × G.Path v t` with strictly smaller
  `terminalPathPairCommonCard` from the weighted-minimal pair, the old common
  non-apex vertex `x`, and the singleton-avoiding replacement path that meets
  the opposite path at a new non-apex vertex `y`.

Iteration 6:
- External sources: none beyond the supplied local context bundle,
  `math_tools_report.md`, local mathlib grep/file inspection, and existing
  workspace proof notes. No web or literature search was used.
- Required context review: reread the run `context_bundle.md` and
  `math_tools_report.md` before local work.
- Verifier baseline:
  `lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean`
  fails only on the two missing splice identifiers.
- Python tool check: reran a bounded brute-force sanity check over all labelled
  simple graphs on 3, 4, and 5 vertices and all ordered distinct triples
  `(v, s, t)`. The exact terminal-set separator hypothesis again produced no
  counterexample to the desired two-terminal fan conclusion. A 6-vertex sweep
  was interrupted as too slow for this iteration.
- Local mathlib check: searched the imported SimpleGraph connectivity/path
  files for Menger, fan, separator, vertex-disjoint path, and deletion
  reachability theorems. No checked theorem in this checkout directly supplies
  the needed two-fan/min-cut step.
- Current first blocker: the missing theorem-level uncrossing lemma. In the
  left branch, from a weighted-minimal pair `(qsMin, qtMin)`, non-apex common
  vertex `x`, and a replacement `r : G.Walk v s` avoiding `x` but meeting
  `qtMin` at a new non-apex vertex, construct a new terminal path pair with
  smaller `terminalPathPairCommonCard` or derive a smaller
  `terminalPathPairWeightedMeasure` contradiction. The right branch is the
  symmetric version.
