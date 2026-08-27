# Mechanism falsification

## Executed replay

The exact guard is

```text
python3 evidence/verify_distinct_factor_obstructions.py
```

and its SHA-256 is

```text
54e089a1f37b0b1332b1de738318900744f4837f6f62ff4b8a8e3355e0724996
```

It exhausts the fixed-`N` forbidden-support ILP through `N=18`, independently
replays every maximizing set by subset products, checks the `{2,4}` variant
mismatch, checks `K_(s+1,s)` circuits through `s=6`, and guards the exact
high-tail and additive-level formulas.  Its finite optima are diagnostic and
are not used as asymptotic evidence.

## Killed mechanisms

### M786-02: no short-circuit compression

For arbitrary `s`, the edge-prime construction on `K_(s+1,s)` is a minimal
bad relation of support `2s+1`.  Connectivity proves that it has no proper
bad subrelation.  Taking comparable large edge primes places every vertex
above `N^(1-1/L)` whenever `s+1>L`.  Thus neither the high tail nor binary
squarefree exponents force a short bad subrelation.

### M786-03: squarefree is not enough

Every vertex in the same `K_(s+1,s)` construction is squarefree, each prime
has exponent zero or one, and the two shores have sizes `s+1` and `s`.
This is an all-parameter refutation, not merely a finite example.

### M786-04: additive separator is a repeated-variant theorem

The Finset set `{2,4}` has subset products `1,2,4,8`, so it is admissible.
But `2v(2)-v(4)=0` has coefficient sum one.  Hence no rational additive
functional can take value one on both vectors.  The linear-functional
characterization requires arbitrary repeated multiplicities and is excluded.

### M786-05: the exact-one density ceiling

For a finite selected-prime set `P`, the exact-one cylinder has density

\[
 \prod_{p\in P}(1-1/p)\sum_{p\in P}1/p.
\]

Writing `lambda=sum 1/p`, this is at most
`lambda exp(-lambda)<=1/e`.  Enlarging the prime set cannot approach one.
A union governed by different additive functions would be a new mechanism
and would need a cross-cylinder relation proof.

### M786-06: common dilation has the wrong degree

An `r`-factor side multiplied termwise by a common parameter `x` acquires
`x^r`; the other side acquires `x^s`.  When `r!=s`, the intended unbalanced
relation is not preserved.  This is the exact homogeneity obstruction to
importing a repeated-factor certificate.

### M786-07: density does not supply nonlinear auxiliary loci

The finite high tail `(N^(2/3),N]` has size `N-o(N)` and contains no
two-versus-one product relation at all: a product of two members exceeds
`N^(4/3)>N`.  It can therefore delete every in-range occurrence of a
polarization pattern such as `(2x)(2y)=4xy` at zero relative cost.  Natural
density alone supplies no theorem on the sparse nonlinear image `xy`.

### M786-08: private primes have sublinear capacity

An injective assignment of one prime divisor to every admitted integer uses
at most `pi(N)=o(N)` integers.  Hall matching with genuinely private labels
cannot certify a density-one subset.  The surviving large-prime route must
reuse fibres and exploit their order.

### M786-10: dimension without height is insufficient

For every `m`, the one-prime family

\[
 \{2^{2^0},2^{2^1},\ldots,2^{2^{m-1}}\}
\]

has unique subset products, hence is admissible, while all exponent vectors
are one-dimensional.  Any bounded-dimension theorem must retain exponent
height or ambient interval size; dimension alone gives no absolute bound.

### M786-12: admissible blocks do not concatenate

`{2,3}` and `{6}` are individually admissible, but their union contains
`2*3=6`.  Marker-free gluing is false.  A marker construction would be new
and must prove both cross-block isolation and negligible natural-density
loss.

## Surviving mechanisms

### M786-01: full minimal-circuit transversal

The high-tail lemma already deletes `o(N)` vertices and disposes of every
bad circuit up to `L(N)=o(log N)`.  What remains is a precise extremal
question: does the hypergraph of all longer minimal circuits have an
`o(N)` transversal?  The long bipartite circuits show why the word "all" is
essential but do not prove a linear transversal lower bound.

### M786-09: ordered largest-prime peeling

Removing the `N^(1/L)`-smooth core costs `o(N)` for `L->infinity` slowly.
Every surviving integer has a large prime, and every minimal relation must
balance every large-prime fibre.  A bounded-congestion endpoint selection
could yield the transversal in M786-01.  The complete bipartite circuits are
the first exact congestion test; private-prime deletion is excluded.

### M786-11: fractional cover plus rank-sensitive rounding

The forbidden-support ILP is exact at every fixed cutoff.  The surviving
claim asks for new mathematics: an explicit `o(N)` fractional cover on the
high tail and a rounding theorem whose loss depends on exponent-circuit
rank rather than maximum hyperedge size.  Finite optima through `N=18` do
not support the asymptotic claim, but they provide a complete falsification
host for candidate dual weights.

## Exact finite optimizer boundary

The optimum sizes for `[2,N]`, `2<=N<=18`, are

```text
1,2,3,4,4,5,6,6,7,8,8,9,9,10,10,11,11.
```

These values are not monotone-density evidence and do not decide either
public subproblem.  The only reusable theorem is the exact ILP equivalence:
an admitted set is precisely a vertex set containing no inclusion-minimal
unbalanced relation support.
