# WOWII198a left first-crossing round 008

Current first blocker between the stage theorem
`terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt` and
`conjecture198a` is still the retained-suffix package
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`, which feeds
`terminal_set_fan_left_suffix_retention_alt_intersections_control`, then the
left first-crossing lemma, the splice descents, the two-fan theorem, and the
traceability contradiction chain.

No external web or literature sources were used.

## Lean action

Updated `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt` so its
non-retained branch calls the existing proved package
`terminal_set_fan_left_first_crossing_splice_commonCard_lt_of_not_retained`
directly.  Added `#check`s for:

- `terminal_set_fan_left_suffix_retention_bad_pivot_descent`
- `terminal_set_fan_left_suffix_retention_alt_intersections_control`
- `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`

The configured verifier still fails before the target theorem because
`terminal_set_fan_left_suffix_retention_bad_pivot_descent` has two stale
arbitrary-pivot containment holes.

## Tool check

I ran a small Python support-order sanity check:

```text
rs        = [v, w, z, y, s]
old_left  = [v, z, x, s]
old_right = [v, w, y, x, t]
```

Here `w` is the first old-support hit on `rs`, `x` is retained in the old-right
suffix after `w`, and `z` is a retained-branch bad pivot from the old-left
prefix of `altRight`.  Splicing old-left-to-`z` with `rs.dropUntil z` gives
`[v, z, y, s]`, whose old-right common non-apex support is `{y}`, while the old
common non-apex support was `{x}`.  Thus the local claim
`new_common.erase v ⊆ (old_common.erase v).erase x` is false for an arbitrary
bad pivot.

This matches the two Lean failures at lines 4589 and 4676: both try to prove
erased-common membership for an arbitrary secondary vertex by using
`hpair_measure_min`, whose type is only weighted-measure minimality.

## Next target

Replace the arbitrary-pivot proof inside
`terminal_set_fan_left_suffix_retention_bad_pivot_descent` with the intended
extremal/weighted-measure argument.  The proof must choose a first/last bad
pivot on `rs`, then either prove the secondary splice containment for that
extremal pivot or derive equal common-card with strictly smaller support length
contradicting `hpair_measure_min`.
