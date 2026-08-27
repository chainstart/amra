# M10 round 1 checkpoint: an exact pair gap theorem and the distinguished-gap split

## Status

This round works only on the common-start anchored coordinate

\[
 {\cal A}_S=\{s:\ 0\le s\bmod p<p-k\text{ for every }p\in S\},      \tag{1}
\]

where the full 451 successor starts after `s=k-1` and gives
`n=s+k+1`.  The results below are unconditional except for the explicitly
labelled finite scans.  They do not prove a new upper bound for Erdos 451.

The main exact result is negative but exponent-level: a generalized
Jacobsthal inequality consisting only of `C^m` times reciprocal density is
false even for two actual 451 prime coordinates.  A polynomial factor of
order at least `k^(2-o(1))` is necessary for a theorem about the maximum
cyclic gap.  The same pair has distinguished successor only `O(k)` away,
so this obstruction does not refute a theorem for the distinguished gap.

## 1. Common-endpoint covering identity

For `p=k+b`, condition (1) fails exactly on the length-`k` blocks

\[
 [jp+b,(j+1)p-1]=[(j+1)p-k,(j+1)p-1].                \tag{2}
\]

Thus `s` is allowed exactly when the interval `(s,s+k]` contains no multiple
of any processed prime.  The successor problem is the first gap longer than
`k` in the ordered union of their positive multiples, with the starting
point fixed at `s=k-1`.  Equation (2) is used below only to retain the common
endpoint; a translate-average is not introduced.

## 2. Exact two-prime phase theorem

Let

\[
 k<q<p<2k,\qquad \Delta=p-q,\qquad a=q-k,
\]

and consider the two-coordinate box

\[
 {\cal A}_{q,p}=\{s:\ s\bmod q\in[0,a-1],\quad
                         s\bmod p\in[0,a+\Delta-1]\}.             \tag{3}
\]

Partition the line into the `q`-blocks

\[
 B_j=jq+[0,a-1],\qquad j\in\mathbb Z.                            \tag{4}
\]

Put `u_j=j Delta mod p`, represented in `[0,p-1]`.  On `B_j` write
`s=jq+r`.  Since `jq=-j Delta mod p`, the second condition in (3) asks that

\[
 r-u_j\bmod p\in[0,a+\Delta-1].                                  \tag{5}
\]

The two intervals in (5) are disjoint exactly when

\[
                       a\le u_j\le k.                              \tag{6}
\]

Indeed, for `u_j<a` one may take `r=u_j`; for `u_j>k` one may take `r=0`,
while for (6) neither the nonwrapped nor wrapped interval reaches
`[0,a-1]`.  This proves:

> **Two-prime empty-block theorem.**  The `q`-block `B_j` contains an
> element of (3) if and only if `u_j` is outside `[a,k]`.  Consequently a
> cyclic run of empty `q`-blocks has length at most
> \[
> R=\left\lfloor {k-a\over\Delta}\right\rfloor+1,                 \tag{7}
> \]
> and the maximum cyclic gap satisfies
> \[
> G({\cal A}_{q,p})\le (R+2)q.                                    \tag{8}
> \]

For (7), two consecutive phases that both lie in `[a,k]` cannot cross the
modular boundary, since `k+Delta<p`; they increase by the ordinary integer
`Delta`.  Bound (8) then allows the two nonempty boundary blocks in addition
to the empty run.

There is a matching coherent lower witness.  Set

\[
 j_0=\left\lfloor {a-1\over\Delta}\right\rfloor,
 \qquad
 j_1=\left\lfloor {k\over\Delta}\right\rfloor+1.                 \tag{9}
\]

The last allowed point in `B_(j_0)` is `j_0 q+a-1`; the first allowed point
in `B_(j_1)` is `j_1 q`; every intervening block is empty by (6).  Hence

\[
 \boxed{\quad
 G({\cal A}_{q,p})\ge (j_1-j_0)q-a+1.
 \quad}                                                           \tag{10}
\]

Equations (8)--(10) show that the true close-pair maximum-gap scale is

\[
                  G({\cal A}_{q,p})\asymp {q(2k-q)\over p-q}      \tag{11}
\]

whenever both `q-k` and `2k-q` are macroscopic and `p-q=o(k)`.

## 3. An unconditional actual-prime counterexample to pure density scale

By the prime number theorem, the interval

\[
 (3k/2,7k/4)
\]

contains `(1/4+o(1))k/log k` primes.  The sum of its adjacent prime gaps is
less than `k/4`, so for every sufficiently large `k` it contains adjacent
primes `q<p` with

\[
                  \Delta=p-q=O(\log k).                            \tag{12}
\]

For this pair, `a` and `2k-q=k-a` both have size at least `k/4`.
From (9)--(10),

\[
 G({\cal A}_{q,p})\gg {k^2\over\log k}.                           \tag{13}
\]

On the other hand its reciprocal density is bounded by an absolute constant:

\[
 {pq\over(q-k)(p-k)}\le 13                                       \tag{14}
\]

for all large `k` in this interval.  Therefore

\[
 {G({\cal A}_{q,p})\over pq/((q-k)(p-k))}
       \gg {k^2\over\log k}.                                     \tag{15}
\]

This rigorously refutes every universal bound

\[
                     G\le C^m{Q\over|A|}                          \tag{16}
\]

even when `m=2` and the two moduli are actual primes from the 451 interval.
It also shows that the polynomial exponent `B` in a bound
`k^B C^m Q/|A|` must satisfy `B>=2`; every fixed `B<2` is impossible.
This does **not** refute a `k^2 C^m` theorem, nor a theorem only for the full
451 distinguished successor.

## 4. Why pairwise composition still loses `exp(Theta(k))`

Pair consecutive primes in `(3k/2,7k/4)` and write their within-pair gaps as
`Delta_i`.  There are

\[
 r=(1/8+o(1)){k\over\log k}
\]

disjoint pairs and `sum_i Delta_i<=k/4`.  Any pair-factorized carry ledger
which multiplies the sharp phase condition numbers

\[
                     1+{2k-q_i\over\Delta_i}
\]

therefore pays at least

\[
 \prod_{i=1}^r {c k\over\Delta_i}
 \ge (4cr)^r=\exp(\Omega(k)),                                  \tag{17}
\]

where AM--GM was applied to the `Delta_i`.  The trivial upper bound
`Delta_i>=2` also makes this ledger at most `exp(O(k))`, so its exponent is
genuinely linear.  Thus a sequential proof that charges the close-pair
condition number independently at each merge cannot yield `exp(o(k))`.
The no-go is scoped to pair-factorized losses; a block-global signed or
many-seed cancellation is not addressed.

## 5. Distinguished successor behaves differently

For the close pair above, `Delta<a` for large `k`.  The single integer `s=p`
satisfies (3), because

\[
 p\bmod p=0,
 \qquad p\bmod q=p-q=\Delta<a.                                  \tag{18}
\]

Hence its distinguished successor after `s=k-1` is at distance at most
`p-k+1<k+1`, even while its maximum cyclic gap is
`Omega(k^2/log k)`.  This is a rigorous warning against replacing M10 by a
maximum-gap theorem: the latter needs a `k^2` loss created far from the
distinguished start, while the actual anchored start can be much easier.

For the full system, the guarded exact prefix sieve found:

| `k` | primes | exact `n_k` | distance after `s=k-1` | distance / reciprocal density |
|---:|---:|---:|---:|---:|
| 20 | 4 | 550 | 510 | 3.3658 |
| 30 | 7 | 21235 | 21175 | 0.8087 |
| 50 | 10 | 771892 | 771792 | 0.8805 |

No survivor occurred below `10^7` for the tested rows `k>=80`.  These are
finite facts only.  The values for `k=30,50` are compatible with the
reciprocal-density scale but do not prove a uniform bound.

## 6. First two-parameter composition test

A natural syndetic invariant would be

\[
 G(A\cap B)\le G(A)G(B)                                           \tag{19}
\]

for coprime periods.  It is false for arbitrary periodic sets: modulo `2`
take `A={0}` and modulo `5` take `B={0,2}`.  Their gaps are `2` and `3`, but
their CRT intersection has gap `8>6`.  An exact scan of `27900` anchored
two-interval systems with coprime moduli below `26` found no counterexample
to (19).  That anchored observation is finite evidence, not a theorem.
The subsequent multi-coordinate block search did find actual-prime 451
counterexamples to (19); see `evidence/m10_common_endpoint_fan_lemma.md`,
Section 8.  Thus the one-coordinate finite survivor is not promoted.

Even if (19) held for anchored intervals, composing its one-coordinate gaps
would give `(k+1)^m=exp((1+o(1))k)`, because every local gap is `k+1`.
Thus it is a genuine two-parameter invariant worth distinguishing from the
false arbitrary-set claim, but by itself its exponent is still linear and it
does not close M10.  A useful strengthening must amortize local gaps by the
seed counts/densities of whole blocks rather than multiply `k` once per
coordinate.

## 7. Guarded evidence

Compact data and exact commands are in
`evidence/m10_round1_finite_summary.json`.  The three accepted runs were:

1. pair scan: `openmath-task-20260826-223103-319131.scope`, exit `0`,
   `4.39s`, maximum RSS `82424 KiB`, swaps `0`;
2. full successor scan: `openmath-task-20260826-223107-319183.scope`, exit
   `0`, `4.37s`, maximum RSS `32124 KiB`, swaps `0`;
3. syndetic composition test: `openmath-task-20260826-223112-319202.scope`,
   exit `0`, `0.28s`, maximum RSS `11520 KiB`, swaps `0`.

One earlier overwide anchored enumeration in unit
`openmath-task-20260826-222759-318304.scope` was deliberately terminated and
is not used as evidence.  All finite claims remain classified as finite.

## 8. Current exact gap

The pure `C^m` generalized-Jacobsthal maximum-gap route is killed, and a
pairwise phase ledger is exponentially too expensive.  The surviving M10
target must be one of the following strictly narrower statements:

1. a distinguished-start inequality that may ignore remote coherent gaps
   such as (10); or
2. a block merge in which a single polynomial `k^2` loss is shared by an
   entire macroscopic block, while seed density is retained at reciprocal-
   density scale.

Neither statement is proved at this checkpoint.  The original exponent and
public problem are unchanged.
