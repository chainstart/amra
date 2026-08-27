# Survivor deepening: what remains after moving thin-tail obstruction

## Decisive proved countermechanism

### IR.1 (moving thin-tail minimal-circuit theorem)

Let `eta_K>0` be any sequence with `K eta_K -> infinity`.  For every
sufficiently large integer `K`, put `N=2^K`.  Then the strict tail

\[
(N^{1-\eta_K},N]
\]

contains `2s_K+1` distinct integers forming a support-minimal equal-product
relation with shore sizes `s_K+1` and `s_K`.  One may take

\[
s_K=\left\lceil\frac4{\min(\eta_K,1)}\right\rceil.
\]

The complete proof is in `evidence/OBSTRUCTION_ANALYSIS.md`.  Its mechanism
is an odd edge-prime path circuit followed by nonuniform powers of two whose
total exponents agree on the two shores.  Unique odd edge primes prove
support minimality; the balanced padding moves every vertex into the desired
tail without changing equality or distinctness.

This theorem is stronger than a fixed-`eta` example.  If deleting
`n<=N^(1-eta_K)` has size `o(N)`, then necessarily `K eta_K->infinity` along
`N=2^K`, exactly the hypothesis of IR.1.  Consequently:

1. every hard lower-power-tail rounding of `o(N)` cost fails;
2. every finite union of nested log-defect thresholds of `o(N)` cost fails;
3. if independent deletion probabilities satisfy
   `q_N(n)<=g_N w_N(n)` with `g_N=o(log N)`, the output cannot be a
   transversal almost surely without alteration: IR.1 with
   `eta_K=1/(2 max(1,g_N))` gives an edge missed with positive probability.

The conclusion is sharply scoped.  It does not give an integral lower bound
for `tau(H_N)`, because one deletion hits each displayed circuit.  It does
not refute prime-incidence alteration or the smooth-core route: the common
padding prime deliberately makes these circuits eligible for the smooth
exception.

## Exact rough-part host shared by the survivors

Choose `L=L(N)->infinity` slowly with `L=o(log N)` and put `y=N^(1/L)`.
The intended exceptional set contains:

* the lower tail `n<=N^(1-1/L)`;
* the `y`-smooth integers;
* integers divisible by `p^2` for some prime `p>y`.

For a standard sufficiently slow choice of `L`, all three parts have size
`o(N)`: the first by `N^(-1/L)->0`, the second by the standard smooth-number
estimate with smoothness parameter `u=L->infinity`, and the third by
`N sum_(p>y)p^(-2)=o(N)`.

On the residual set every integer has a nonempty squarefree active-prime set

\[
P_y(n)=\{p>y:p\mid n\},\qquad 1\le |P_y(n)|\le L.    \tag{6}
\]

For every signed product relation, each active-prime incidence balances
between shores.  Summing the valuation equations gives the exact identity

\[
\sum_{n\in S}|P_y(n)|=\sum_{n\in T}|P_y(n)|.         \tag{7}
\]

Equation (7) is not term-count balance because active degrees vary.  It is
the common noncircular input to the three survivors.

## M786I-05: arithmetic resampling target

Freeze the residual hypergraph after the exceptional deletion above and the
proved high-tail elimination of short circuits.  The survivor asks for a
dependent sampling/alteration theorem with an explicit arithmetic witness
map and

\[
\mathbb E|D_N|
\le g(N)\sum_{n=2}^N w_N(n)+o(N),
\qquad g(N)=o(\log N),                               \tag{8}
\]

such that `D_N` hits every residual bad support.  A useful target is
`g(N)=O(log log N)`.  Per-edge miss probability, an unnamed LLL, or a bound
in terms of the total number of bad supports is not (8).  No dependency-
compression theorem proving (8) is currently available.

IR.1 forces alteration: one-shot independent sampling at any affordable
global multiple has positive miss probability on a padded edge.  It does not
show that missed edges cannot be repaired cheaply using overlap.

## M786I-06: deterministic largest-prime ownership target

For every residual inclusion-minimal bad support `E`, expose its largest
active prime together with the signed cofactor residue below that prime and
choose an owner `owner(E) in E`.  The exact target is

\[
\left|\{owner(E):E\text{ minimal residual bad}\}\right|
\le g(N)\sum_n w_N(n)+o(N),
\qquad g(N)=o(\log N).                               \tag{9}

The owner must be defined locally from the ordered valuation/cofactor state,
not by first solving the transversal.  The relation `2*3=6` proves that
largest-prime cardinality balance without the cofactor residue is invalid.
With the residue included, no all-parameter congestion bound or obstruction
to (9) is known in this campaign.

## M786I-12: recursive token potential and coherence target

Process active primes in descending order.  At a prime `p`, match the equal
numbers of `p`-incidences across the two shores, strip `p`, and retain the two
cofactors as a signed residue token.  The target is a potential `Phi` with:

1. `Phi` is determined by the current signed cofactor tokens and remaining
   prime order;
2. every unresolved unbalanced component forces a paid deletion or a strict
   decrease of `Phi`;
3. the total paid load over a vertex is `o(log N)` relative to `w_N`;
4. for the infinite version, the rule is compatible as the controlled prime
   set grows and its deletion set has upper density zero.

This formulation explicitly retains the residue lost by M786I-07.  It is
not a theorem: no bounded potential meeting items 2--3 has been found, and
item 4 is an additional coherence interface rather than a consequence of a
finite recursion.

## Evidence classification and stopping point

* IR.1 and its three stated rounding corollaries: `proved`, all parameters.
* Rough-part identities (6)--(7): `proved`; the standard smooth-number bound
  is background and supplies only an exceptional-set estimate.
* M786I-05, M786I-06, M786I-12: `conditional/open` with exact targets
  (8), (9), and the four potential requirements.
* `tau(H_N)=o(N)`: open.
* The infinite natural-density assertion: open.
* Original distinct-Finset Erdős #786: open.

The author campaign stops in `survivor_deepening`.  IR.1 is suitable for
independent audit only as a scoped standalone countermechanism theorem; this
file makes no promotion decision and performs no self-audit.
