# WOWII198a bad-pivot extremal round 002

Current first blocker between the retained-suffix package and `conjecture198a`:
`terminal_set_fan_left_suffix_retention_bad_pivot_descent`.

External web or literature sources used: none.  Local run context was read from
the supplied `context_bundle.md` and `math_tools_report.md`.

Lean work:
- Inserted the requested declaration
  `terminal_set_fan_left_suffix_retention_extremal_bad_pivot_descent` with the
  exact supervisor statement.
- Rewired
  `terminal_set_fan_left_suffix_retention_alt_intersections_control` so a bad
  arbitrary `z` is packaged as the existential bad witness and routed through
  the new extremal package.

Verifier:
```text
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/VerifiedOpen20260609/Wowii198aLeftmost.lean
```

Result: failed with the same two residual containment errors inside the older
arbitrary-pivot theorem:

```text
Wowii198aLeftmost.lean:4745:10: hpair_measure_min has weighted-minimality type
but Lean expects membership in the old erased common support with x removed.

Wowii198aLeftmost.lean:4832:12: hpair_measure_min has weighted-minimality type
but Lean expects membership in the old erased common support with x removed.
```

Next proof step:
- Replace the body of
  `terminal_set_fan_left_suffix_retention_bad_pivot_descent` with a call to a
  genuinely proved extremal bad-pivot descent, not the current arbitrary-pivot
  local containment proof.
- The extremal proof still needs first/last bad-pivot selection on `rs` and, in
  the exposed replacement-side residual cases, either erased-common containment
  from extremality or the weighted-measure contradiction via
  `false_of_weighted_min_and_commonCard_le_supportLength_lt`.
