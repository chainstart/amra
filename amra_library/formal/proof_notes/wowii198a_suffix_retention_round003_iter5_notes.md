# WOWII198a suffix-retention iteration 5 notes

Date: 2026-06-27

Target:
`terminal_set_fan_left_suffix_retention_alt_intersections_control`

Current first blocker between the stage theorem and `conjecture198a`:
the suffix-retention branch needed by
`terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`.  Closing it
feeds `terminal_set_fan_splice_descent_left_of_hsep`, then the mirrored right
splice, `terminal_set_two_fan_of_no_small_endpoint_separator`, the two-fan
package, the longest-path missed-vertex contradiction, the
Chvatal-Erdos traceability bridge, and finally `conjecture198a`.

External sources:
none.  Only local Lean/mathlib files and local tool probes were used.

Tool checks:
- Lean/mathlib grep confirmed the available order lemma
  `Walk.notMem_support_takeUntil_support_takeUntil_subset`.
- A Python finite search checked the target theorem shape on all 5-vertex
  simple graphs under the encoded weighted-minimality condition and found no
  counterexample.  An exhaustive 6-vertex pass was started but interrupted
  after 60 seconds without a result, so it is not evidence.

Lean progress:
- Added local helper
  `not_mem_takeUntil_later_of_mem_takeUntil`.
- Added support-proof-erasing wrapper
  `not_mem_takeUntil_later_of_mem_takeUntil_of_support`.

Remaining mathematical package:
prove a first/last bad-pivot weighted-descent lemma.  In the bad branch where
`z ∈ rs.support ∩ altRight.support` but `z` is not an old erased common vertex,
the local support facts reduce to:
- if `z` lies on `oldLeft.takeUntil x`, then `z` is after the first hit `w` on
  `rs` and before `x` on old left; the needed descent splices
  `oldLeft.takeUntil z` with `rs.dropUntil z` and keeps old right.
- if `z` lies on `oldRight.dropUntil x` but not old left, the symmetric later
  pivot descent is needed.

The existing hypotheses do not directly prove either branch by local set
containment; weighted minimality must be used through an explicit lower-measure
terminal pair.
