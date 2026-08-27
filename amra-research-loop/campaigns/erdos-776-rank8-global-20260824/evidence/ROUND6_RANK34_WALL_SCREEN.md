# Round 6: rank-three/rank-four wall screen

## Verdict

The actual rank-three and rank-four adjoint-budget targets survive a guarded
finite falsifier on every adjacent wall `V -> V+1` for `125 <= V <= 2000`.
This is negative evidence against easy counterexamples, not an all-parameter
proof.  The round does not promote the campaign and does not prove LTJ, H2,
the rank-eight entry, or Erdős #776.

The scan also gives an exact obstruction to the simplest symbolic route:
neither canonical level has a uniformly positive common-prefix length.  Thus
a proof that cancels one fixed leading term at every wall is unavailable.

## Guarded finite falsifier

The executable `probe_round6_rank34_suffix_budget.py` reconstructs each exact
compressed orbit once per worker chunk and reuses it for both adjacent
comparisons.  It was run under the OpenMath cgroup guard with `MemoryHigh=30G`,
`MemoryMax=34G`, `MemorySwapMax=4G`, and `TasksMax=512`.

There were 1,876 adjacent comparisons.  No failure was found for

\[
 (\delta_3)_+\le U_2(a-1)
 \quad\hbox{or}\quad
 (\delta_4)_+\le U_3(U_2(a-1)-1).
\]

The tightest numerical cases were still far from equality:

| target | wall | increment | budget | margin |
|---|---:|---:|---:|---:|
| rank three | `132 -> 133` | `2` | `66` | `64` |
| rank four | `137 -> 138` | `4` | `77` | `73` |
| LTJ | `127 -> 128` | `1` | `a=34` | `33` |

The complete compact certificate, including all ten observed prefix-length
classes, is retained in `round6_rank34_falsifier_125_2000.json`.

## Exact failure of fixed leading-prefix cancellation

At the actual wall `V=300 -> 301`, the rank-three words change from

\[
 \binom{30}{3}+\binom{29}{2}+\binom{28}{1}
 \quad\hbox{to}\quad
 \binom{31}{3}+\binom{2}{2}.
\]

Their common canonical prefix has length zero.  The wall still has
`delta_3=2 <= 85`, so it is not a counterexample to the budget target; it is
a counterexample only to a proof architecture demanding cancellation of a
fixed positive number of leading rank-three terms.  The full scan contains
six rank-three zero-prefix walls and one rank-four zero-prefix wall.

## Fail-closed decision

The ten observed prefix-length labels are not a proved all-parameter wall
taxonomy.  Within each label the binomial digits remain parameter-dependent,
and this round supplies no finite state reduction that controls them.  Hence
the success gate is unmet: there is neither an actual counterexample nor a
complete symbolic classification.

Larger ordinary scans are now frozen as non-progress.  `M776G-01` remains in
`survivor_deepening` only for a materially new all-parameter invariant, such
as a plateau-position inequality or a joint multirank compensation law that
does not assume a fixed common prefix.  Without such an invariant the route
should stay paused rather than consume another compute round.
