# Independent attack on the base-leading top-index lemma

## Status

The proposed inequality

\[
 L(a,c,d):=\binom d4-\binom{c+1}4-\binom{a+1}3\ge 0
\]

survived the independent carry-aware search described below, but this is
finite falsification evidence, not a proof.  The natural proof attempt does
give an exact reduction and identifies the remaining crossing lemma.

Here `a=top_2(alpha)`, `c=top_3(p)`, and `d=top_3(v)`.  The search is in the
actual `c=1` target chamber, so it includes `gamma3<0` as well as the stated
`(++ -> ++)` and `gamma4<0` conditions.

## 1. Why the candidate is sufficient

For every rank `s` Macaulay word with leading index `t`,

\[
 \binom{t}{s+1}\le U_s(N)\le \binom{t+1}{s+1}-1.
\]

The upper bound follows by induction from
`N=C(t,s)+R<C(t+1,s)` and Pascal's identity; the strict cap is an
integer strictness, not an asymptotic estimate.  Hence

\[
 U_3(v)\ge\binom d4,\quad
 U_3(p)\le\binom{c+1}4-1,\quad
 U_2(\alpha)\le\binom{a+1}3-1.
\]

Using the exact orbit identity

\[
 \gamma _5=U_3(v)-U_3(p)-U_2(\alpha)-1,
\]

one obtains

\[
 \gamma _5\ge L(a,c,d)+1.
\]

Thus the proposed inequality would prove strict rank-five recovery, with one
unit to spare.

## 2. Exact dyadic normal-form compression

Put `u=r+k-1`.  Substitution of

\[
 \tau=kq+\binom k2+1-r,
 \qquad
 \alpha=\binom{r+1}2-kq-\binom k2
\]

gives the two exact complement identities

\[
 \boxed{\alpha+\tau-1=\binom r2},\qquad
 \boxed{\beta+\tau=\binom u2}.
\]

If the rank-two canonical words are

\[
 \alpha=\binom a2+e,\qquad
 \beta=\binom A2+E,
\]

then `0<=e<a`, `0<=E<A`, and the second-stage inputs become

\[
 \boxed{p=\binom{a+1}3+\binom{e+1}2-\binom r2},
\]

\[
 \boxed{v=\binom{A+1}3+\binom{E+1}2-\binom u2}.
\]

The failed rank-four condition also loses all shadow notation:

\[
 \boxed{\gamma _4=v-p-\binom r2}.
\]

Therefore `gamma4<0` is exactly `v-p<C(r,2)`.  Likewise
`gamma3<0` is exactly `beta<=C(r,2)`.  These identities are the useful
copyable part of the proof attempt: the dyadic congruence first produces an
exact complementary binomial cap, and only then should canonical carries be
analysed.

## 3. Conditional proof and smallest remaining gap

Whenever `d>=c+1`, Pascal telescoping gives

\[
 \binom d4-\binom{c+1}4
   =\sum_{x=c+1}^{d-1}\binom x3.
\]

Consequently the candidate is immediate in the easy cell

\[
 d\ge\max(a,c)+2,
\]

because the sum contains a term at least `C(a+1,3)`.  A universal proof must
first exclude `d<=c+1`, where the candidate cannot hold for positive
`alpha`, and then handle the genuine multi-cap cell

\[
 \boxed{c<a,\qquad c+2\le d\le a+1.}
\]

All 18,081 sampled target states landed in this hard cell.  Thus the easy
single-cap argument does not address even the observed generic mechanism.
The minimal open statement is now:

> From the two complement identities, the actual divisibility/legal
> constraints, `p,v>=0`, `beta<=C(r,2)`, and
> `v-p<C(r,2)`, prove that the complete rank-three caps crossed by `[p,v]`
> have total rank-four weight at least `C(a+1,3)`.

Equivalently, one must prove

\[
 \sum_{x=c+1}^{d-1}\binom x3\ge\binom{a+1}3
\]

in that hard cell.  This is not merely a top-gap lemma: for example the
actual state `(j,k,r)=(21,4,26466)` has `(a,c,d)=(8606,8597,8606)`, so
`d<a+2`, yet the many smaller crossed caps give exact margin
`741991397675`.

## 4. Independent carry-aware falsification

[`search_base_leading_top_index.py`](search_base_leading_top_index.py)
implements the normal form and Macaulay arithmetic from scratch and imports
none of the existing campaign probes.  For each dyadic `(j,k)` fibre it:

1. generates only congruence-compatible legal `r` values;
2. centres windows at the exact `alpha=0` and `p=0` walls, logarithmic rays,
   deterministic interior points, and the legal endpoint;
3. detects top-digit changes and lower-digit resets in the canonical words
   of `alpha`, `p`, and `v`, then adds both sides of each detected carry;
4. evaluates the proposed inequality only on actual target states.

The frozen run used `j=5,...,10` together with high-scale stress values
`80,96,112,128`, `4<=k<=8`, radius 8, and seed 776043.  It checked 58,026
distinct compatible points on 50 fibres; 57,976 were actual double-positive
states and 18,081 were in the target chamber.  Of the target points, 2,620
were newly added specifically next to detected carries.  No negative
candidate margin occurred.  The smallest exact margin was 83,805 at

\[
 (j,k,r,q)=(6,4,145,2436),\quad (a,c,d)=(41,20,41),
\]

with `gamma4=-525` and `gamma5=89319`.

The machine-readable result is
[`base_leading_top_index_search.json`](base_leading_top_index_search.json).
The bounded reproduction command is

```bash
AMRA_MEMORY_KIB=2097152 AMRA_TIMEOUT_SECONDS=180 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/erdos-776-c1-round3/evidence/search_base_leading_top_index.py \
  --output amra-research-loop/campaigns/erdos-776-c1-round3/evidence/base_leading_top_index_search.json \
  --max-j 10 --max-k 8 --radius 8
```

The run completed in 31.1 seconds and stayed far below the 2 GiB virtual
memory ceiling.  It does not exhaust any large fibre: logarithmic and binary
centres are search devices only, so finite absence is not promoted to a
proof.

