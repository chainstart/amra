# Far-scale negative rank-six wall probe

This exact finite probe tests the surviving applicability claim
`M304-negative-forces-noborrow` well beyond the scales used in the first
round-three search.  It evaluates every divisibility-compatible `r <= 1000`
and 17 points around the first-tail wall for

- `j in {56,60,64,80,100,120}`;
- `2 <= k <= 80`.

The bounded run evaluates 37,788 compatible parameter triples and accepts
20,086 actual `(--)->(++)` states.  Of these, 17,483 have `gamma5 < 0`.
None has a rank-six borrow (`P < 0` or `V < 0`), so M304 survives this
domain.  This is finite falsification evidence only, not a proof of M304.

The same run finds 2,304 states with both `gamma5 < 0` and `gamma6 < 0`.
Thus non-borrow applicability is not itself recovery: even when the
rank-six formula is legal, its surplus can remain negative.  The most
negative sampled `gamma6` occurs at `(j,k,r)=(120,4,10)` and is recorded
exactly in `negative_rank6_walls_far.json`.

Two broader versions of this experiment hit their declared 600-second and
180-second limits without producing output.  They are not evidence.  The
frozen domain above reruns in about 25 seconds under the 2 GiB/120-second
wrapper and is the only far-scale run used here.

This does not close the public antichain problem.  It preserves M304 only
as an applicability lemma candidate and reconfirms that any recovery tree
must adapt beyond rank six.
