# Survivor deepening: the logarithmic fractional transversal

## The bad-relation hypergraph

Let `V_N={2,...,N}`.  A bad relation is a pair of disjoint Finsets
`S,T subset V_N` such that

\[
 \prod_{n\in S}n=\prod_{n\in T}n,
 \qquad |S|\ne |T|.
\]

Let `H_N` be the hypergraph whose edges are the supports `S union T` of all
such relations (equivalently, it is enough to retain inclusion-minimal
supports).  An admissible `A subset V_N` is exactly an independent set of
`H_N`; its complement is a vertex transversal.  Thus the finite public
assertion is exactly

\[
 \tau(H_N)=o(N).                                    \tag{1}
\]

This equivalence is a fixed-`N` reformulation, not progress by itself.

## Proved all-parameter fractional theorem

### Theorem 786.F (log-defect fractional transversal)

For every `N>=2`, define

\[
 w_N(n)=\frac{\log(N/n)}{\log N}\qquad(2\le n\le N).
                                                               \tag{2}
\]

Then `w_N` is a fractional vertex cover of `H_N`: every bad support `E`
satisfies

\[
 \sum_{n\in E}w_N(n)\ge1.                           \tag{3}
\]

Moreover

\[
 \sum_{n=2}^N w_N(n)
 =\frac{N\log N-\log(N!)}{\log N}-1
 =\left(1+o(1)\right)\frac N{\log N}.              \tag{4}
\]

#### Proof

Orient a bad relation so that `r=|S|>|T|=s`.  Equality of products gives
equality of logarithmic sums.  Hence

\[
\begin{aligned}
 \sum_{n\in S}w_N(n)-\sum_{n\in T}w_N(n)
 &=\frac{r\log N-\sum_{S}\log n
          -s\log N+\sum_T\log n}{\log N}\\
 &=r-s\ge1.                                         \tag{5}
\end{aligned}
\]

All weights are nonnegative, so the weight of `S union T` is at least the
weight of `S`, which by (5) is at least one.  This proves (3).  Summing (2)
gives the exact first identity in (4), and Stirling's formula gives the
asymptotic identity.  The proof uses each element only once on its side and
does not invoke the repetitions-allowed additive-function argument.  QED.

Thus the complete covering LP already has a feasible solution of `o(N)`
cost.  The missing finite theorem is purely an **integrality/structure**
step for this particular prime-exponent circuit hypergraph.

## The high-tail theorem is threshold rounding

For an integer `L>=2`, delete every vertex with `w_N(n)>=1/L`; this is exactly

\[
 n\le N^{1-1/L}.
\]

If `L=o(log N)`, the deleted set has size `o(N)`.  In the residual hypergraph
every individual weight is below `1/L`, while every edge has total weight at
least one, so every residual bad support has more than `L` vertices.  The
stronger magnitude calculation in the obstruction note shows that its
larger shore itself has more than `L` vertices.

This explains both the power and the exact failure of a hard threshold:
threshold rounding eliminates every short circuit, while `K_(s+1,s)` gives
long minimal circuits whose small weights add almost exactly to one.

## Tightness on the bipartite prime circuits

Take comparable edge primes in `K_(s+1,s)`.  With `N` at the right-shore
scale, the `s+1` left vertices have logarithmic weight tending to
`1/(s+1)`, and the `s` right vertices have weight tending to zero.  The
longer-shore total tends to one, exactly saturating (3).  These circuits do
not refute an `o(N)` integral cover: a disjoint packing of them costs only
one deletion per `2s+1` vertices.  They do prove that rounding must use
overlap and prime-incidence rank rather than a larger pointwise threshold.

## M786-01 proof attempt: direct transversal

The direct surviving claim is now precise.  Start with the high tail for
`L=floor(sqrt(log N))`, then cover its long minimal circuits.  A theorem of
the form

\[
 \tau(H_N)\le g(N)\sum_n w_N(n),
 \qquad g(N)=o(\log N),                             \tag{6}
\]

would prove (1).  General hypergraph rounding does not give (6): edge sizes
are unbounded and the number and dependency degree of circuits can be
exponential.  The `K_(s+1,s)` atlas kills any proof that replaces all long
edges by a bounded subedge.

No linear transversal lower bound is known from the atlas.  The precise gap
is a structural rounding inequality, not the existence of a fractional
cover.

## M786-09 proof attempt: largest-prime fibre rounding

Choose a slowly growing `L` and `y=N^(1/L)`.  The standard smooth-number
estimate makes the `y`-smooth vertices an `o(N)` exceptional set.  Every
remaining vertex has a prime factor above `y`.  In a signed circuit, the
valuation equation at each such prime balances its total exponent between
the two shores.

The desired peeling statement is:

> Charge every minimal circuit to its largest active prime and choose an
> exposed endpoint so that the total number of chosen endpoints is at most
> `O(log log N) sum_n w_N(n)`.

This would be `O(N log log N/log N)=o(N)` and close the finite part.  It
allows reused prime fibres and therefore survives the `pi(N)` private-label
obstruction.  It is unproved.  The complete bipartite edge-prime circuits
show the hard case: every large prime has exactly two endpoints, but a
single integer participates in many fibres.  A proof needs a coarea or
ownership rule preventing the same logarithmic weight from being charged at
many prime scales.

The smooth-number estimate alone is not promoted: it only removes the zero-
large-prime branch and supplies no endpoint cover.

## M786-11 proof attempt: rank-sensitive LP rounding

The exact ILP is

\[
 \min\sum_n x_n,
 \qquad \sum_{n\in E}x_n\ge1\quad(E\in H_N),
 \qquad x_n\in\{0,1\}.                              \tag{7}
\]

Theorem 786.F supplies the explicit feasible relaxation `x_n=w_N(n)`.
Ordinary size-based rounding loses up to the unbounded circuit length.  The
surviving target is a rounding loss `O(log log N)` controlled by the rank or
largest-prime fibre depth of the signed exponent matrix.  The fixed-`N`
solver through `N=18` is complete but proves no such uniform bound.

The computational data are useful only for falsification: optimum sizes on
`[2,N]` for `N<=18` range from 1 to 11 and do not exhibit an asymptotic
certificate.  A valid next experiment must output a symbolic dual/rounding
rule, not a larger optimum table.

## Infinite-density interface remains separate

Even a proof of (1) settles only the finite subproblem.  The infinite result
follows from a genuinely natural-density construction, and independently
optimized complements of `H_N` need not be nested.  The union example
`{2,3}` with `{6}` proves that marker-free block gluing is invalid.

A complete campaign therefore needs either:

1. a coherent rounding rule whose decisions stabilize on every fixed
   integer and whose deletion set has upper density zero; or
2. a separate periodic/profinite construction with density above
   `1-epsilon` and an audited cross-cylinder relation theorem.

Neither interface is proved here.

## Evidence classification

* Theorem 786.F: `proved`, author-level natural proof with exact finite replay.
* High-tail bounded-length theorem: `proved`, all parameters.
* `K_(s+1,s)` minimal circuit family: `proved`, all `s`.
* M786-01, M786-09, M786-11 rounding claims: `conditional/open`.
* Finite public density-one statement: open.
* Infinite natural-density statement: open.
* Repetitions-allowed additive argument: variant mismatch and excluded.

The verifier command is

```text
python3 evidence/verify_distinct_factor_obstructions.py
```

with SHA-256

```text
54e089a1f37b0b1332b1de738318900744f4837f6f62ff4b8a8e3355e0724996
```

It checks every minimal bad support through `N=18` has logarithmic weight at
least one, in addition to the earlier falsification atlas.  The universal
proof is equation (5), not the finite loop.
