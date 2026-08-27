# Independent audit of the arithmetic-alteration obstructions

## Pre-proof reconstruction from the proposition statements

This section records the independent reconstruction made from Propositions A
and B, the stated prime-labelled-path interface, and the exact definition
`w_N(n)=log(N/n)/log N`, before reading the proposition proofs or verifier.
Here `N=2^K`, all logarithms in exponents are base two, and a circuit is a
support-minimal unequal-cardinality equal-product relation of distinct
integers.

### A. Expected shared-vertex star and raw dependency obstruction

Take a path `v_0...v_(2s)` with `s=floor(K/4)` and an odd internal vertex
`v_r`.  Label its incident edges by 3 and 5 and all other edges by
path-specific primes in `[N^(1/16),N^(1/8)]`.  The raw odd part at `v_r` is
15.  Because the smaller, odd-indexed shore is not decremented in the path
padding, the common padded integer must be

\[
 x_K=2^{K-\lceil\log_2 15\rceil}15=15N/16.
\]

Disjoint path-specific prime pools make every other odd support unique.
Thus different paths should intersect in exactly `{x_K}`; their dependency
graph is a clique and its raw maximum degree is at least `M_K-1`.

There are `2s-2=Theta(K)` path-specific primes per circuit.  The prime number
theorem-level elementary estimate
`pi(X) >= cX/log X` for sufficiently large `X` gives

\[
 \#\{p:N^{1/16}\le p\le N^{1/8}\}
       \gg {N^{1/8}\over K}.
\]

Since `N^(1/8)/(K)` dominates `N^(1/10)`, disjoint blocks can supply

\[
 M_K\ge {N^{1/10}\over K}={2^{K/10}\over K}
\]

paths for all sufficiently large `K`.  Endpoint conventions and the removal
of the fixed labels 3 and 5 can change only constants, not this displayed
lower bound; the proof nevertheless must make the block count explicit.

For the path padding, put `c_i=ceil(log_2 q_i)` and
`epsilon_i=c_i-log_2(q_i)`.  If even-shore decrements have total

\[
 \Delta=K-\left(\sum_{i\ even}c_i-\sum_{i\ odd}c_i\right),
\]

then equality of the unpadded products gives
`sum_even log q_i=sum_odd log q_i`, hence

\[
 \sum_i w_N(a_i)
 = {\sum_i\epsilon_i+\Delta\over K}
 = 1+{2\over K}\sum_{i\ odd}\epsilon_i.             \tag{RA.1}
\]

There are `s` odd vertices, so

\[
 1\le W(C)<1+2s/K\le3/2.                              \tag{RA.2}
\]

The even decrements are at most five when `s=floor(K/4)`, while odd
vertices have no decrement.  Consequently every vertex has
`w_N(a)<6/K`, and all values lie in `(N/64,N]`.

To see the precise consequence for *raw symmetric max-degree LLL*, suppose
the independent rounding deletes `a` with probability `g w_N(a)` and
`g<K/12`.  Then every deletion probability is below `1/2`.  The probability
that a circuit survives satisfies

\[
 p_C=\prod_{a\in C}(1-gw_N(a))
 \ge \exp\left(-2g\sum_{a\in C}w_N(a)\right)
 >e^{-3g}.                                            \tag{RA.3}
\]

The raw dependency degree `D` is at least `M_K-1`.  Thus the symmetric
criterion `e p_C(D+1)<=1`, if it is to hold, forces

\[
 g\ge {1+\log M_K\over3}=\Omega(K).
\]

If `g>=K/12` the same conclusion is immediate.  Therefore this construction
kills an argument based on the raw maximum dependency degree with
`g=o(log N)`.  It does not kill an alteration which first contracts all
events sharing `x_K`, uses a lopsided/cluster dependency object, or coordinates
several clusters.

### B. Expected core with pairwise-disjoint private satellites

Build a core path `C={a_0,...,a_(2s)}` using distinct primes
`N^(1/16)<ell_1<...<ell_(2s)<N^(1/8)`.  Its internal values have the form

\[
 a_i=2^{t_i}\ell_i\ell_{i+1}.
\]

For each `2<=i<=2s-2`, build a new path whose shared vertex is `v_1`, on
the smaller shore.  Give its first two edge labels

\[
 A_i=2^{t_i}\ell_i,\qquad B_i=\ell_{i+1},
\]

so their product at `v_1` is exactly `a_i`.  All remaining edge labels must
be fresh odd primes, disjoint across satellites and from every `ell_j`.
The labels in one satellite remain pairwise coprime: only `A_i` is even,
and its private odd prime is `ell_i`; `B_i` has private prime
`ell_(i+1)`; every later edge has its own fresh prime.  Hence the edge-prime
equations force every subrelation indicator to be constant along the path,
proving support minimality.

The nontrivial padding requirement is to keep `v_1` fixed.  For the satellite
raw values `q_j`, let `c_j=ceil(log_2 q_j)` and `h_j=K-c_j`.  Start with
external exponent `h_j` at every vertex except set the exponent at `v_1` to
zero.  Since `a_i>N/64`,

\[
 0\le h_1\le5.                                        \tag{RB.1}
\]

The initial even-minus-odd external exponent imbalance is
`Delta+h_1`, where `Delta<K+s`.  Decrease the `s+1` even-shore exponents by
nonnegative integers with this total.  Even distribution gives

\[
 \max d_j\le
 \left\lceil{K+s+h_1\over s+1}\right\rceil\le6       \tag{RB.2}
\]

for all sufficiently large `K`.  The only potentially large even raw value
is the endpoint `q_0=A_i=a_i/ell_(i+1)<N^(15/16)`; every other nonshared raw
value is at most a product of two `N^(1/8)`-scale primes.  Therefore their
available exponents satisfy `h_j>=K/16-1>6` for large `K`, so the decrements
are legal.  Baseline padding puts a nonshared value in `(N/2,N]`; (RB.2)
then leaves it in `(N/128,N]`.  The fixed shared value is already in
`(N/64,N]`.

Odd-prime supports now give the intersection statements.  Within satellite
`S_i`, the only core two-prime support is
`{ell_i,ell_(i+1)}`, at the fixed vertex `a_i`.  Its endpoint support
`{ell_i}` cannot be a core endpoint because `2<=i<=2s-2`; every other support
contains a satellite-private prime.  Thus

\[
 S_i\cap C=\{a_i\}.
\]

For `i!=j`, the singleton endpoint supports, intended core supports, and all
private-prime supports are distinct.  Hence
`(S_i\setminus{a_i})` and `(S_j\setminus{a_j})` are disjoint.

Finally, if a representative set is required to satisfy `R subset C` and to
hit every circuit meeting `C`, then hitting `S_i` is possible only through
`a_i`.  It must contain every `a_i`, `2<=i<=2s-2`, whence

\[
 |R|\ge2s-3\ge K/2-5.                                \tag{RB.3}
\]

This refutes only a scheme which assigns each packed circuit its own
`o(log N)` internal representatives.  A global deletion may instead choose a
petal vertex, reuse a deletion across other clusters, or optimize interacting
clusters; none of those cross-cluster versions of `M786R-04` is refuted.

## Post-proof audit

### Verdict and exact scope

**PASS**, with one harmless choice-of-index clarification recorded below.
Both propositions are proved with the claimed all-sufficiently-large-`K`
quantifiers.

- Proposition A kills the **raw variable-overlap maximum-degree symmetric
  LLL** implementation: without first contracting the common-`x_K` cluster,
  its criterion forces `g(K)=Omega(K)=Omega(log N)`.
- Proposition B kills **per-packed-circuit independent representatives chosen
  inside that circuit**: one packed circuit can require at least
  `K/2-5` such representatives.
- Neither result kills `M786R-04` in its surviving cross-cluster form.  A
  global alteration may contract common witnesses, delete petal vertices, and
  amortize one choice across interacting clusters.  No `o(N)` transversal or
  coherent density-one set follows from these negative results.

### Check of Proposition A

The author proof agrees with (RA.1)--(RA.3).

1. The fixed labels 3 and 5 make the odd internal vertex exactly
   `x_K=15*2^(K-4)=15N/16`; because decrements occur only on the even shore,
   this value is identical in every path.
2. After reserving the two fixed edges, a path consumes `2s-2=Theta(K)`
   path-specific primes.  From
   `pi(N^(1/8))-pi(N^(1/16)) >> N^(1/8)/K`, the number of disjoint blocks is
   `>>N^(1/8)/K^2`, which exceeds `N^(1/10)/K` because
   `N^(1/40)/K -> infinity`.  Thus the displayed `M_K` lower bound is valid.
3. Unique path-specific odd supports imply that different padded circuits
   have no common integer except `x_K`.  Strictly, the chosen odd index should
   be at least three and at most `2s-3`; otherwise an endpoint adjacent to a
   fixed label need not contain a path-specific prime.  Since the proposition
   is existential and `s=floor(K/4)` is large, choosing `r=3` supplies the
   claimed construction without changing any bound.  The phrase "an odd
   internal path index" should be read with this harmless safe choice, not as
   a claim for every internal index.
4. The exact weight identity is correct.  Equality of unpadded products turns
   the ceiling imbalance into
   `C=sum_even epsilon_i-sum_odd epsilon_i`, yielding
   `W=1+(2/K)sum_odd epsilon_i`.  Hence `1<=W<3/2`, while the decrement-five
   bound gives every `w_N(a)<6/K` and every `a>N/64`.
5. For arbitrary independent deletion probabilities
   `p_v<=g(K)w_N(v)` with `g=o(K)`, every `p_v=o(1)` and
   `log(1-z)>=-z/(1-z)` gives uniformly
   `Pr(A_j)>=exp(-(3/2+o(1))g)`.  The raw overlap graph contains the
   `M_K`-clique, so its maximum degree is at least `M_K-1`.  Substitution into
   `e Pr(A_j)(D_K+1)<=1` forces
   `g >= ((log 2)/15+o(1))K`, in particular `g=Omega(K)`.  (The exact constant
   is irrelevant.)  This is a necessary obstruction only for that raw
   symmetric criterion, not an integrality-gap lower bound or a no-go for
   cluster/lopsided alterations.

### Check of Proposition B

The author's two-adic correction (3.7) is exact.  There are `s+1` even
vertices and `s` odd vertices, and the fixed root `v_1` is odd.  Starting all
nonroots with exponent `K-c_j` but replacing the root exponent
`K-c_root` by zero changes the even-minus-odd exponent imbalance from
`K-C_i` to

\[
 K-C_i+(K-c_{root}),
\]

exactly the total decremented from the even shore.  The bounds
`-s<C_i<s+1` and `0<=K-c_root<=5` give a maximum decrement at most six after
even distribution.  The endpoint raw value
`A_i=a_i/ell_(i+1)<N^(15/16)` is the largest possible nonroot obstruction;
all other nonroot raw products are at most `N^(1/4)`.  Thus every even
baseline has more than six available powers of two for sufficiently large
`K`.  A baseline value lies in `(N/2,N]`, so decrementing by at most six
places it strictly in `(N/128,N]`; the fixed root already lies in
`(N/64,N]`.

Private-prime minimality is also valid despite `A_i` carrying a power of two.
Its odd prime `ell_i` is private to the first satellite edge,
`ell_(i+1)` is private to the second, and every later edge has its own fresh
odd prime.  In an equal-product subrelation each private valuation equates
the two endpoint indicators; connectivity forces the empty or full path.
The external powers of two do not weaken this propagation.

The intersection audit gives exactly the claimed result.

- The satellite root has odd support `{ell_i,ell_(i+1)}` and equals `a_i`.
- Its first endpoint has singleton odd support `{ell_i}`.  Because
  `2<=i<=2s-2`, this is neither core endpoint support `{ell_1}` nor
  `{ell_(2s)}`.
- Every remaining nonroot contains a satellite-private prime.
- Fresh-prime pools are disjoint across satellites; their singleton first
  endpoints use different `ell_i`, and their distinct roots are different
  core values.

Therefore `S_i intersect C={a_i}` and all petals are pairwise disjoint.
Any `R subset C` hitting every circuit meeting `C` must contain all
`a_i`, `2<=i<=2s-2`, so
`|R|>=2s-3>=K/2-5`.  The quantifier `R subset C` is essential: a coordinated
global alteration remains free to hit `S_i` outside the core.

### Executable and campaign checks

No dedicated verifier for `INDEPENDENT_ARITHMETIC_ALTERATION.md` is present
in `evidence/`; `verify_residue_aware_kills.py` predates and does not certify
these two propositions.  The universal verdict therefore rests on the
independently reconstructed symbolic proof, not on finite extrapolation.

As an additional falsifier, I independently instantiated the complete core
and all 77 satellites at `K=160`, checking exact equal products, the
`(N/128,N]` band, singleton core intersections, and pairwise petal
disjointness.  This finite replay passed, but is only corroborative.  The
campaign validator also passes after adding this audit file.
