# High-rank one-sided bridge to the rank-eight entry

## Definitions

For the exact shortened orbit at parameter `V`, put

\[
 W_r(V)=D^{[V]}_{r+2}-{V-12\choose r+2}-{V-13\choose r+1}
 \qquad(6\le r\le14).                                  \tag{1}
\]

The proposed high-rank lemma is the following single all-parameter statement.

> For every integer `V>=125`,
> \[
> 0\le W_r(V)<{V-13\choose r}\quad(7\le r\le14),       \tag{H1}
> \]
> and
> \[
> W_{14}(V+1)-W_{14}(V)\le1.                            \tag{H2}
> \]

This is not proved.  It is independent of the desired rank-six cap: (H1)
stops at rank seven.

## Exact one-sided carry lemma

For all nonnegative integers `x,h` and every rank `r>=1`,

\[
 \operatorname{KK}_r(x+h)-\operatorname{KK}_r(x)
 \le \operatorname{KK}_r(h)\le rh.                    \tag{2}
\]

For the first inequality, take shadow-minimizing `r`-uniform families of
sizes `x` and `h` on disjoint ground sets.  Their union has `x+h` sets and
shadow size **at most** `KK_r(x)+KK_r(h)`, while `KK_r(x+h)` is the minimum
possible shadow size.  (For `r=1` the two 0-shadows both contain the empty
set and are not disjoint; “at most” handles this case.  The campaign's actual
use has `r>=7`.)  The second inequality follows termwise from a canonical
expansion, since

\[
 {a\choose i-1}=\frac{i}{a-i+1}{a\choose i}
 \le i{a\choose i}\le r{a\choose i}.
\]

If `y<=x`, monotonicity gives `KK_r(y)-KK_r(x)<=0`.  Combining the two cases,

\[
 \operatorname{KK}_r(y)-\operatorname{KK}_r(x)
 \le r\max(0,y-x).                                    \tag{3}
\]

This bound is deliberately one-sided and remains valid across a carry wall;
it assumes no common canonical prefix.

## (H1)--(H2) imply the adjacent rank-six loss bound

Condition (H1) makes the two displayed binomial terms in (1) a canonically
separated prefix.  Exact shadowing therefore gives, for `7<=r<=14`,

\[
 W_{r-1}(V)=V+\operatorname{KK}_r(W_r(V)).              \tag{4}
\]

Write `delta_r=W_r(V+1)-W_r(V)`.  Equations (3)--(4) give

\[
 \delta_{r-1}\le1+r\max(0,\delta_r).                   \tag{5}
\]

Starting with (H2), define `b_14=1` and
`b_(r-1)=1+r b_r`.  The exact values are

| r | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 7 | 6 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `b_r` | 1 | 15 | 196 | 2353 | 25884 | 258841 | 2329570 | 18636561 | 130455928 |

Thus

\[
 W_6(V+1)-W_6(V)\le130455928.                          \tag{6}
\]

At the analytic start,

\[
 130455928<{112\choose5}=134153712,
\]

and `binom(V-13,5)` is increasing.  Therefore, for every `V>=125`,

\[
 W_6(V+1)-W_6(V)<{V-13\choose5}.                       \tag{7}
\]

The independent exact engine checks the target entry for every
`40<=V<=125`, including

\[
 M(125)={112\choose6}-W_6(125)=2392397730>0.            \tag{8}
\]

With

\[
 M(V)={V-13\choose6}-W_6(V),\quad
 c_V={V-13\choose5},\quad
 j_V=W_6(V+1)-W_6(V),
\]

Pascal gives the exact identity

\[
 M(V+1)=M(V)+c_V-j_V.                                  \tag{9}
\]

Hence (7)--(9) prove `M(V)>0` for every `V>=40`, which is exactly the
all-parameter rank-eight entry.

The strong condition `j_V<c_V` is sufficient, not necessary.  Given the
integer invariant `M(V)>=1`, the exact necessary-and-sufficient next-step
condition is

\[
 j_V\le c_V+M(V)-1.                                    \tag{10}
\]

## Adversarial carry checks and exact gap

A direct claim that adjacent residual words always share a high prefix is
false.  At `V=56 -> 57`, the rank-seven residual rises from `19443` to
`19451`, but its first canonical term changes from `binom(16,7)` to
`binom(17,7)`.  The shadow jump is nevertheless only `15`, exactly the type
of crossing covered by (2).

Two earlier rank-six cell walls are also explicit:

- `V=42 -> 43`: the word length changes from six terms to five and `W_6`
  drops from `26586` to `22627`;
- `V=50 -> 51`: `W_6` rises from `12423` to `12425`, so scalar
  nonincrease fails.

The verifier finds no failure of (H1), and no rank-14 adjacent jump above
one, for `40<=V<=500`.  This bounded result is only a kill test.  The exact
remaining theorem is (H1)--(H2) for all `V>=125`; no finite carry chart proves
it.

## Alternative survivor: logarithmic rank-six top

If `W_6(V)<=0`, the entry is immediate.  Otherwise, if its nonempty
six-canonical top
is at most `ceil(log_2 V)+13`, then

\[
 W_6(V)<{\lceil\log_2V\rceil+14\choose6}
 \le {V-13\choose6}\qquad(V\ge40).
\]

The last inequality follows from
`ceil(log_2 V)+14<=V-13`, true at `V=40` and preserved thereafter.  What is
missing is an all-parameter charging theorem for top-index carry walls.
