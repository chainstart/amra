# Round 4: full-residue owner flow and two exact no-go books

## Scope and outcome

This note tests two explicit, noncircular owner definitions for the
distinct-Finset hypergraph `H_N`.  Every bad relation is first cancelled and
written as

\[
 z\in\{-1,0,1\}^{\{2,\ldots,N\}},\qquad Az=0,
 \qquad \delta(z)=\sum_n z_n\ne0,
\]

where `A` is the prime-valuation matrix.  Orient it by `delta(z)>0`.

Both states below retain the largest active prime and the **complete signed
cofactor ratio**.  Neither state lists a hitting set, optimizes over other bad
relations, or stores the full lower-prime incidence component.  Thus each is
a strict quotient of the original relation-hitting problem.  Nevertheless:

1. a top-fibre residue-comparison owner has a positive-density set of owners
   on an overlapping double-star book, so it fails the desired global
   aggregate bound;
2. a first compensating-boundary owner has arbitrarily large load even on a
   family with one common hitter, so its proposed `o(log N)` per-cluster load
   theorem fails.

Both mechanisms are killed.  No owner definition is retained.  These results
do **not** refute a global flow which simultaneously retains full residue,
common-cluster geometry, and normalized defect, and they do not prove
`tau(H_N)=o(N)` or the coherent infinite density assertion.

## 1. Exact full-residue state

For the largest prime `p` dividing the support of `z`, write

\[
 \bar n_p=\frac{n}{p^{\nu_p(n)}}
 \quad(p\mid n),
\]

and define

\[
 \rho_p(z)=
 \prod_{p\mid n}\bar n_p^{,z_n}=\frac UV,
 \qquad (U,V)=1.                                      \tag{1.1}
\]

The pair `(U,V)`, not a bounded alphabet, hash, support size, or list of only
the largest few residual primes, is retained exactly.  Since `Az=0`, the
`p`-free portion of the relation has signed product `V/U`.  In particular,
if a prime `q` has `nu_q(U/V)>0`, some `p`-free negative term is divisible by
`q`; if `nu_q(U/V)<0`, some `p`-free positive term is divisible by `q`.

This state is still strictly smaller than hitting the relation: it forgets
how `U` and `V` are distributed among the `p`-free terms and forgets every
intersection with other bad supports.  The counterfamilies below identify
which of these two losses is fatal for each proposed owner.

## 2. Owner I: residue-side top owner

For each sign, order the `p`-divisible terms by the pair
`(bar(n)_p,n)`.  Define `O_top(z)` as follows:

- if `U>V`, choose the maximum pair on the positive top fibre;
- if `V>U`, choose the maximum pair on the negative top fibre;
- if `U=V`, choose the maximum pair on their union.

The certificate consists only of `(p,U,V)` and the two top-fibre extrema.
It retains the full signed ratio and forgets all `p`-free incidence data.
It is therefore explicit and noncircular.

### Proposition 2.1 (positive-density overlapping double-star book)

Let `Q_N` be the odd squarefree integers `n` in `(N/2,N]` having at least
three prime factors.  Then every `n in Q_N` is `O_top(z_n)` for a
support-minimal bad relation `z_n` in `H_N`.  Moreover,

\[
 |Q_N|=\left(\frac2{\pi^2}+o(1)\right)N.             \tag{2.1}
\]

Consequently, if

\[
 \mathcal O_{top}(N)=\{O_{top}(z):z\text{ is a minimal bad relation in }
 H_N\},
\]

then `|mathcal O_top(N)|` has positive lower density.  There are no functions
`g(N)=o(log N)` and `r(N)=o(N)` for which

\[
 |\mathcal O_{top}(N)|
 \le g(N)\sum_{m=2}^N w_N(m)+r(N)                    \tag{2.2}
\]

holds for all large `N`.

#### Proof

Fix `n in Q_N`, let `p=P^+(n)`, put `Y=n/p`, and let `B` be the set of
prime divisors of `Y`.  Take `A={2}`.  The two shores

\[
 B\cup\{2p\}qquad\text{and}\qquad\{2,n\}            \tag{2.3}
\]

have equal product `2n`, and their cardinalities are respectively
`|B|+1>=3` and 2.  They are disjoint: `n` is odd, `Y` has at least two odd
prime factors, and `2p<n`.  Every member is at most `N`.

The full prime-occurrence graph of (2.3) is a double-star tree.  Each
`q in B` joins the singleton `q` to `n`, the prime 2 joins 2 to `2p`, and
`p` joins `n` to `2p`.  Every edge-prime valuation forces its endpoint
indicators to agree, and connectedness forces the empty or full
subrelation.  Hence (2.3) is support-minimal.

The largest active prime is `p`.  Its positive cofactor is 2 and its negative
cofactor is `Y`, so

\[
 \rho_p(z_n)=\frac2Y,qquad Y\ge15.                   \tag{2.4}
\]

The denominator side is larger, and its only top-fibre member is `n`.
Thus `O_top(z_n)=n`.

The standard squarefree count gives

\[
 \#\{m\le x:m\text{ odd and squarefree}\}
   =\frac4{\pi^2}x+o(x).
\]

Subtracting its values at `N` and `N/2` gives `2N/pi^2+o(N)` candidates.
The odd squarefree integers with one or two prime factors are `o(N)`:
primes are `O(N/log N)`, and the semiprime count is
`O(N log log N/log N)` by the usual prime-counting upper bound and
`sum_(p<=x)1/p=O(log log x)`.  This proves (2.1).

Finally Stirling gives the already audited identity

\[
 \sum_{m=2}^N w_N(m)=(1+o(1))\frac N{\log N}.         \tag{2.5}
\]

For `g=o(log N)`, the right side of (2.2) is `o(N)`, contradicting (2.1).
Notice that every relation (2.3) contains the common vertex 2: one deletion
repairs the entire displayed book.  The positive owner density is a failure
of this owner rule, not an integrality-gap lower bound.  ∎

## 3. Owner II: first full-residue compensating boundary

When `rho_p(z)!=1`, let

\[
 q(z)=\max\{q:\nu_q(\rho_p(z))\ne0\}.                \tag{3.1}
\]

If `nu_q(rho)>0`, define `O_partial(z)` to be the least `p`-free negative
term divisible by `q`; if `nu_q(rho)<0`, take the least `p`-free positive
term divisible by `q`.  The balance following (1.1) proves that the required
set is nonempty.  For `rho=1`, use the least top-fibre term as a fixed
fallback.

The certificate `(p,U,V,q,sign(nu_q(rho)),O_partial(z))` retains the full
ratio but only one compensating boundary witness.  It discards the rest of
the lower component and all intersections with other relations.  On the
double stars (2.3) it selects a lower prime divisor of `Y`, rather than the
positive-density top vertex `n`, so Proposition 2.1 does not kill it.

A natural strictly simpler load theorem for this owner is:

> **CL(h).** For every family `B` of minimal bad supports in `H_N` having a
> common vertex, the number of distinct `O_partial` owners is at most `h(N)`.

If `h=o(log N)`, this would give the required cost for the easiest possible
contracted cluster, whose transversal number and packing contribution are
both one.  The theorem is false by an all-parameter family.

### Proposition 3.2 (common-root long-path books)

For every sufficiently large `K`, with `N=2^K`, there are

\[
 M_K\ge\frac{N^{1/10}}K                              \tag{3.2}
\]

support-minimal path circuits `C_1,...,C_(M_K)` contained in `(N/64,N]`
such that

\[
 C_i\cap C_j=\{x_K\}\quad(i\ne j),
 \qquad
 O_\partial(C_i)\ne O_\partial(C_j).                 \tag{3.3}
\]

Thus `CL(h)` fails for every `h(N)=o(log N)` (indeed for every
`h(N)<N^(1/10)/K` eventually).

#### Proof

Take `s=floor(K/4)` and paths `v_0...v_(2s)`.  At the safe odd internal
vertex `v_3`, label the incident edges by 3 and 5.  For each path choose a
disjoint block of `2s-2` primes in `[N^(1/16),N^(1/8)]`; order the block so
the final edge label `p=b_(2s)` is largest and
`q=b_(2s-1)` is second largest.  The elementary prime count provides the
number of blocks in (3.2).

Apply the exact path padding, decrementing only the even shore.  Its maximum
decrement is five, all exponents are nonnegative, and all values lie in
`(N/64,N]`.  The common odd vertex is undecremented and equals

\[
 x_K=15\,2^{K-4}=15N/16.                             \tag{3.4}
\]

Every other vertex contains a path-specific odd prime, so different circuits
intersect only at `x_K`.  Private edge primes force support minimality.

Orient the even shore positively.  At the top prime `p`, the two fibre terms
are the even endpoint

\[
 a_{2s}=2^\alpha p
\]

and its odd neighbour

\[
 a_{2s-1}=2^\beta qp.
\]

Therefore the reduced full ratio has the form

\[
 \rho_p=\frac{2^d}{q}\quad\text{or}\quad
 \frac1{2^d q}                                       \tag{3.5}
\]

for some `d>=0`.  In particular `q` is exactly the largest prime in
`UV`.  Outside the top fibre, the only term divisible by `q` is
`a_(2s-2)`, on the positive shore.  Hence

\[
 O_\partial(C_i)=a_{2s-2}^{(i)}.                     \tag{3.6}
\]

The path-specific prime `q` makes these owners distinct across paths.  This
proves (3.3) and refutes `CL(h)`.  ∎

This is not the already-closed assertion that peel depth is bounded.  Only
one top-prime transition is used per circuit.  The obstruction is global:
after all circuits have been recognized as a single common-hitter cluster,
the local full-residue boundary rule still insists on a different paid owner
for each member because it discarded the cluster intersection.

## 4. Comparison and classification

| owner mechanism | exact retained state | killed by | exact failure | status |
|---|---|---|---|---|
| `O_top` | top prime, full `U/V`, two top extrema | positive-density double-star book | its global distinct-owner set has positive density | killed |
| `O_partial` | top prime, full `U/V`, largest signed residue prime and first compensator | common-root long-path book | no `o(log N)` common-cluster load | killed |

The mechanisms lose complementary global information.  `O_top` forgets the
lower factorization and misses the common vertex 2.  `O_partial` enters the
lower component but forgets that many complete relations share `x_K`.
Keeping both full residue and the complete relation-cluster intersection
would evade the two counterexamples, but its state is no longer certified to
be strictly simpler than the original hitting problem.  A new theorem would
need an independently bounded quotient of that joint state; merely naming it
"global owner flow" is circular.

Accordingly no Round-4 owner survives this comparison.  The global
full-cofactor-residue owner-flow interface remains open, as do the finite
`o(N)` transversal and coherent natural-density targets.

## 5. Executable evidence

Run

```text
python3 evidence/verify_round4_full_residue_owner_flow.py
```

The verifier checks exact small double-star minimality and owners, finite
odd-squarefree density guards, a fully padded `K=80` four-path common-root
book, the exact top ratios, singleton intersections, and distinct boundary
owners.  Its finite loops are corroborative only.  The universal claims are
the symbolic density proof and prime-block path construction above.
