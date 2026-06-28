## 2026-06-27 round-002 terminal-set left first-crossing uncrossing

Current first blocker between `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`
and `conjecture198a`:

`terminal_set_fan_left_suffix_retention_bad_pivot_descent`.

The configured verifier was run:

```text
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean
```

It fails at the two residual containment branches inside
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`:

```text
Wowii198aLeftmost.lean:4589:10: hpair_measure_min has weighted-minimality type
but Lean expects membership in the old erased common support with x removed.

Wowii198aLeftmost.lean:4676:12: the symmetric branch has the same mismatch.
```

The downstream theorem `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`
already has the intended direct/non-direct split and retained/non-retained
structure, and `#check` output from the same verifier run confirms these names
are visible:

- `terminal_set_fan_left_suffix_retention_bad_pivot_descent`
- `terminal_set_fan_left_suffix_retention_alt_intersections_control`
- `terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`

No external web or literature sources were used in this iteration.  The local
obstruction is not syntax: the arbitrary residual containment claims at the two
failing lines need to be replaced by the intended extremal bad-pivot or
weighted-measure descent argument.  That package closes
`terminal_set_fan_left_suffix_retention_alt_intersections_control`, then
`terminal_set_fan_left_first_crossing_uncrossing_commonCard_lt`, then the
left/right splice descent chain, two-fan theorem, longest-path missed-vertex
contradiction, Chvatal-Erdos traceability, and finally `conjecture198a`.
