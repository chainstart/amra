# Correlated inverse-binomial dyadic-block audit

This note remains in `survivor_deepening` and keeps `closes=[]`.  It attacks
only the canonical inverse-binomial covering-radius interface isolated in the
previous round.

## 1. Exact one-sided and absorbed coordinates

For `p=k+b`, put

\[
 s=n-(k+1).
\]

Then the 451 condition at `p` has the exact common-start form

\[
 n\bmod p\notin[1,k]
 \quad\Longleftrightarrow\quad
 s\bmod p\in[0,b-1].                                  \tag{1}
\]

The residue `n=0` maps to `s=b-1`, and the residues `k+1,...,k+b-1`
map to `0,...,b-2`, proving (1).  The original upper-bound problem asks for
the successor of this one-sided box after `s=k-1`; a symmetric recurrence in
`[-b,b]` is not enough.

Fix

\[
 A=\left\lfloor\frac{k}{\log^2 k}\right\rfloor,
 \qquad Q={k+A\choose A}.
\]

Writing `n=Qt`, every prime `k<p<=k+A` is absorbed.  For a remaining
`p=k+b`, (1) becomes

\[
 t\bmod p\in\{0,-c_p,\ldots,-(b-1)c_p\},
 \qquad
 c_p=\left((-1)^A{b-1\choose A}\right)^{-1}\pmod p.  \tag{2}
\]

## 2. The precise dyadic fixed-prefix target

For `A<=B<k`, let

\[
 T_B=\{p=k+b:\ p\text{ prime},\ B<b\le\min(2B,k)\},
 \qquad r_B=|T_B|,
\]

and put `delta_B=product_{p in T_B}(p-k)/p`.  Order the nonempty blocks by
increasing `B`.  For a fixed integer interval `J`, define recursively

\[
 X_0=J,\qquad
 X_j=\{t\in X_{j-1}:t\text{ satisfies (2) for every }p\in T_{B_j}\}.
                                                                    \tag{3}
\]

The sufficient pointwise block statement is

> **Fixed-prefix block-survival lemma (open).**  There are absolute `C,D`
> such that, for the actual canonical history (3),
> \[
> |X_j|\ge
> \frac{\delta_{B_j}}{k^D(\log k)^{C r_{B_j}}}|X_{j-1}|             \tag{4}
> \]
> whenever the right side is at least one.

This is not an average over translates and is not a claim for an arbitrary
set `X`.  If (4) holds, take

\[
 |J|>k^{D L}(\log k)^{C m_A}
       \prod_{k+A<p<2k}\frac p{p-k},                               \tag{5}
\]

where `L=O(log log k)` is the number of dyadic blocks and
`m_A=sum_B r_B`.  Every intermediate lower bound is then at least the final
one, so induction leaves a point.  The logarithm of the overhead in (5) is

\[
 O(L\log k+m_A\log\log k)=o(k).                                   \tag{6}
\]

Together with `log Q=o(k)`, this proves the desired `n_k=exp(o(k))`.  Thus
(4), unlike a translate-average or a single-seed statement, is a correct
block interface.  It remains open.

## 3. A proved fixed-set signed large-sieve lemma

Let `X` be any set of `N` integers in an interval of length at most `H`, and
for `p=k+b` define

\[
 N_p=|\{x\in X:Qx\bmod p\in\{0,-1,\ldots,-(b-1)\}\}|,
 \quad D_p=N_p-\frac bpN.                                           \tag{7}
\]

> **Dense-seed signed block lemma.**  For every set `T` of remaining primes,
> \[
> \sum_{p\in T}\frac p b|D_p|^2\le(H-1+4k^2)N.                    \tag{8}
> \]
> Consequently, for `0<theta<1`, if
> \[
> N>\frac{H-1+4k^2}{\theta^2\sum_{p\in T}b/p},                    \tag{9}
> \]
> at least one `p in T` satisfies
> \[
> N_p\ge(1-\theta)\frac bpN.                                      \tag{10}
> \]

**Proof.**  Put `S_X(alpha)=sum_{x in X} exp(2 pi i alpha x)` and
`K_b(h)=sum_{j=0}^{b-1}exp(2 pi i h j/p)`.  Fourier inversion and the change
of variable induced by `Q` give

\[
 D_p=\frac1p\sum_{h\ne0}K_b(h)S_X(hQ/p).                           \tag{11}
\]

Parseval gives `sum_{h ne 0}|K_b(h)|^2=b(p-b)`.  Cauchy's inequality therefore
bounds `(p/b)|D_p|^2` by `sum_{h ne 0}|S_X(hQ/p)|^2`.  The fractions
`(hQ mod p)/p`, over all `p` and nonzero `h`, are distinct reduced fractions
separated by at least `1/(4k^2)`.  The additive large sieve proves (8).
If (10) fails for every `p`, the left side of (8) is at least
`theta^2 N^2 sum b/p`, contradicting (9).  `square`

For a dyadic block, `sum b/p` has scale `B^2/(k log k)`.  Once `H` is much
larger than `k^2`, (9) requires the relative seed density to exceed roughly

\[
 \frac NH\gg\frac{k\log k}{B^2}.                                  \tag{12}
\]

The canonical history eventually has density `exp(-Theta(k/log k))`, so (8)
stops at polynomial density.  In the first block it can process only about
`log k/log(k/B)` successive half-density-scale constraints before (12)
fails, rather than all `r_B` constraints.  This is a true pointwise lemma,
but it is not (4).

Equation (11) also shows why a phase-aware large sieve based only on frequency
separation does not improve (8): multiplication by `Q` is merely a
permutation of the `p-1` nonzero frequencies at each prime.  The binomial
correlation disappears from the large-sieve norm.

## 4. Why one-frequency divisor bounds and finite differences do not scale

The large local Fourier coefficients in (11) have `|h|` on the scale
`p/b<=k/B`.  A bad dual phase `hQ congruent a (mod p)` is equivalent to

\[
 p\mid hQ-a.                                                        \tag{13}
\]

The divisor-product argument in the previous note bounds the union over
`h<=L, 0<|a|<=R<Q` by

\[
 2LR\frac{\log(LQ+R)}{\log k}.                                    \tag{14}
\]

At `A=k/log^2 k`, this is `o(k/log k)` only for
`LR=o(log^2 k/log log k)`.  A discrepancy estimate at the first block needs
frequencies through `L` of order `k/B=log^2 k` together with nontrivial phase
separation, already beyond (14).

The polynomial identity for `Q` does not improve the single-frequency
divisibility problem.  If `R_A(b)=(-1)^A binom(b-1,A)`, then

\[
 hR_A(b)-a\pmod{k+b}=hQ-a\pmod{k+b}.                               \tag{15}
\]

Thus applying finite differences to `R_A(b)` and then reducing at the moving
modulus `p=k+b` returns the fixed integer in (13).  Any stronger count here
requires new information on prime divisors of the binomial linear forms
`hQ-a`; degree-`A` finite differences alone do not supply it.  The analogous
inverse-phase condition reduces to `p | h-aQ`.

This kills only the proposed upgrade of (14) by formal finite differencing.
It does not rule out cancellation after several primes are coupled.

## 5. Exact coupled Fourier/Vandermonde structure

Coupling an entire block produces a new exact algebraic object.  Put

\[
 P_B=\prod_{p\in T_B}p,
 \qquad F_B(x)=\prod_{p=k+b\in T_B}(x-b).
\]

Let `mu_B` be the uniform probability measure on the CRT product set (2)
modulo `P_B`.  For an integer global frequency `a`, CRT factorization gives

> **Inverse-binomial Vandermonde Fourier lemma.**
> \[
> \widehat\mu_B(a)=
> \prod_{p=k+b\in T_B}
> \frac1b\sum_{j=0}^{b-1}e_p(-h_{p,a}j),             \tag{16}
> \]
> where
> \[
> h_{p,a}\equiv
> a(-1)^{A+r_B-1}
> \left({b-1\choose A}F_B'(b)\right)^{-1}\pmod p.    \tag{17}
> \]

**Proof.**  The local frequency induced by the global character `e_{P_B}(at)`
is `a(P_B/p)^{-1}`.  Multiplying the local progression step `c_p=Q^{-1}`
gives `h_{p,a}=a(QP_B/p)^{-1}`.  Modulo `p=k+b`,

\[
 \frac{P_B}{p}\equiv
 \prod_{b'\ne b}(b'-b)=(-1)^{r_B-1}F_B'(b),
\]

and (17) follows from the canonical binomial congruence.  `square`

This is the first block formula that retains both the inverse-binomial phase
and every other prime in the block.  It also exposes the remaining obstacle:
the cofactor inserts the derivative of the irregular prime-offset polynomial.
The fixed-field identities for `R_A` no longer control the product
`binom(b-1,A)F_B'(b)`, and the modulus still varies with `b`.

There is an unconditional near-resonance warning independent of the choice of
`Q`.  Let `r=r_B` and `L<min_{p in T_B}p`.  Map each vector
`u in {0,...,L}^r` to the global frequency whose local normalized coordinates
are `u_p`.  The map is injective.  Two of its `(L+1)^r` points on the circle
are at cyclic distance at most `P_B/(L+1)^r`.  Subtracting gives:

> **Small-vector near-resonance lemma.**  There is a nonzero frequency `a`
> with
> \[
> 0<|a|_{P_B}\le\frac{P_B}{(L+1)^r}                 \tag{18}
> \]
> and local coordinates `|h_{p,a}|<=L` for every `p`.

If `B<b<=2B` and `L<=k/(8B)`, the elementary sine bounds in (16) give

\[
 |\widehat\mu_B(a)|\ge(2/\mathop{\rm pi})^r.          \tag{19}
\]

Thus support-size splitting cannot simply assert that every high-support
character is far from the short-prefix pole.  This does not refute a *signed*
Fourier theorem: (19) is exponentially smaller than the main coefficient,
and cancellation between many global frequencies remains possible.  It does
refute a phase-separation proof that treats the canonical multiplier alone as
removing all high-support near resonances.

## 6. Admissible-lattice and one-sided Dirichlet audit

For the untwisted coordinate (1), introduce

\[
 \Lambda=\{(s,y_p)\in\mathbb Z^{1+m}:
             y_p\equiv s\pmod p\text{ for every }p\}.              \tag{20}
\]

It has determinant `product p`, and the target is an anchored positive box
with `s>k-1` and `0<=y_p<b`.  After absorption, one replaces the difference
lattice by `y_p congruent Qt (mod p)` and translates the `y`-box by `-(k+1)`.

Symmetric Minkowski controls `|y_p|<b` and permits independent mixed signs;
it does not prove (1).  A generic positive-orthant or simplex loss
`m^{O(m)}` has logarithm `Theta(m log m)=Theta(k)` because
`m=Theta(k/log k)`, so it is also quantitatively insufficient.  The required
loss is at most `C^m` or `(log k)^{O(m)}`.

Standard admissible-lattice discrepancy theorems do not apply directly:
`Lambda` contains nonzero coordinate-hyperplane vectors, for example the
vector with `s=0`, `y_p=p`, and all other `y`-coordinates zero.  Its primal
coordinate product is zero.  The dual lattice similarly has characters
supported on proper subsets of the primes.  Splitting by support returns the
high-support near-resonance issue (18), while absolute Fourier mass returns
the already killed M06 bridge.

The surviving lattice formulation is therefore precise but open: prove a
one-sided dispersion bound for this special CRT lattice, with coordinate-zero
subspaces separated and total loss `(log k)^{O(m)}`, and retain the affine
inverse-binomial phases in the full-support term.  A symmetric short vector or
a generic `m^{O(m)}` orthant theorem would not suffice.

## 7. Guarded finite audit and current boundary

The script `work/inverse_binomial_block_spectrum.py` verifies (17) exactly and
scans global frequencies `1<=a<=512`.  At `k=10000,A=117`, the first block
has `r=12`; its largest scanned normalized coefficient has logarithm
`-47.26`.  Later blocks have still smaller scanned coefficients.  At the
one-frequency scale `L=R=floor(k/(2B))`, only one bad `(p,h)` pair appears in
each of the first two blocks and none later, while the proved union bound
(14) is much larger than the total number of tested pairs.

These observations are favorable falsification data only.  The necessary
global frequency range grows exponentially with the block rank, and the exact
near-resonance lemma (18) guarantees frequencies not seen by the scan.  No
empirical pattern has been promoted to a theorem.

The round therefore produces three unconditional reusable results -- (8),
(16)--(17), and (18)--(19) -- but not the fixed-prefix block lemma (4).
The next smallest closure gap is a signed, support-stratified discrepancy
bound for the special affine CRT lattice, not another one-frequency phase
estimate.
