# Canonical absorber versus fixed-pattern cluster resonance

This note stays in `survivor_deepening` with `closes=[]`.  It transports the
exact bounded-cluster resonance through the canonical absorber, proves the
available divisor-counting stratification, and records why it does not yet
give a block estimate or an affine counterexample of the original strength.

## 1. The transported frequency is `Q ell`, not `Q^{-1} ell`

Let a fixed offset pattern be

\[
 p_i=x+d_i,\qquad 0=d_1<\cdots<d_r,qquad
 P=\prod_i p_i,
\]

and put

\[
 L=\prod_{i<j}(d_j-d_i),\qquad
 \epsilon=(-1)^{r+1},\qquad \ell_0=\epsilon L.
\]

For the direct common-start product

\[
 f(s)=\prod_iG_{p_i}(s),qquad
 \widehat f(\ell)=\frac1P\sum_{s\bmod P}f(s)e_P(-\ell s),
\]

the bounded-cluster calculation gives

\[
 |\widehat f(\ell_0)|\ge\eta_rP                       \tag{1}
\]

along its fixed-pattern prime subsequence.  Now take

\[
 A=\lfloor k/\log^2k\rfloor,qquad
 Q={k+A\choose A},qquad g(t)=f(Qt-(k+1)).
\]

Every selected prime is larger than `k+A` for sufficiently large members of
the subsequence, since `k=floor(alpha*x)` with fixed `1/2<alpha<1`; hence
`gcd(Q,P)=1`.  If `Qbar` is the inverse of `Q mod P`, changing variables
`s=Qt-(k+1)` proves the exact Fourier transport

\[
 \widehat g(a)
 =e_P(-a\overline Q(k+1))\widehat f(a\overline Q).    \tag{2}
\]

Consequently the large coefficient (1) moves to

\[
 a_0\equiv Q\ell_0\pmod P,qquad
 |\widehat g(a_0)|=|\widehat f(\ell_0)|.             \tag{3}
\]

The translation changes only the unit phase.  Formula (3) also agrees with
the local inverse-binomial/Vandermonde expression: demanding the old local
frequency `h_i` gives
`a_0(QP/p_i)^{-1}=h_i mod p_i`, hence `a_0=Q ell_0 mod P`.

Let

\[
 \langle y\rangle_P\in(-P/2,P/2]
\]

denote the centered representative and write

\[
 a=\langle Q\ell_0\rangle_P.                         \tag{4}
\]

Since every `p_i` eventually exceeds `|L|` and is coprime to `Q`, one has
`a!=0`.  Abel summation applied to (1)--(3) gives the exact surviving lower
interface

\[
 \max_J\left|\sum_{t\in J}g(t)\right|
 \ge \frac{\eta_rP}{|1-e_P(-a)|}
 \ge \frac{\eta_rP^2}{2\mathop{\rm pi}|a|}.          \tag{5}
\]

Thus absorption changes only the distance of the resonant frequency from the
prefix pole.

## 2. The zero-dividend and `Q>P` audit

The centered congruence (4) is exactly

\[
 P\mid Q\ell_0-a.                                    \tag{6}
\]

One may use `P<=|Q ell_0-a|` only when the integer on the right is nonzero.
The excluded identity occurs precisely when the unreduced integer
`Q ell_0` already lies in the centered interval and `a=Q ell_0`.  It must be
split off whenever `Q|L|<=P/2` and the low-frequency radius reaches
`Q|L|`.

For the fixed-rank Maynard pattern this zero case is absent eventually.  For
all sufficiently large `k`,

\[
 A\log\frac{k}{A}
 \le\log Q\le A\log\frac{e(k+A)}A,
 \qquad
 \log Q=\Theta\left(\frac{k\log\log k}{\log^2k}\right).          \tag{7}
\]

The lower bound follows because every factor `(k+j)/j` is at least `k/A`;
the upper bound is the standard binomial estimate.  Since
`log P=O_r(log k)`, one has `Q>P` for every fixed `r` and all sufficiently
large `k`, so a centered `a` cannot equal the integer `Q ell_0`.
This observation does **not** make (6) contradictory: `Q ell_0-a` can be a
large nonzero multiple of `P`.  The frequently tempting estimate
`P>|Q ell_0-a|` goes in the wrong direction here.

The floor choices `k=floor(alpha*x)` and
`A=floor(k/log^2 k)` cause no hidden smoothness assumption in (2), (6), or
(7).  They only give `P=Theta_r(k^r)`, the remaining-prime condition
`p_i>k+A`, and the pointwise binomial size bound (7).  No polynomial or
equidistribution law for `Q mod P` is being assumed.

## 3. A proved low-pole rank stratification

The elementary information in (6) can be stated without fixing `r`.

> **Absorbed resonance rank lemma.**  Let `S` contain `r` primes in `(k,2k)`,
> let `P` be their product, and suppose an integer `L!=0` produces a
> transported centered frequency `a=<QL>_P` with `|a|<=R`.  If
> `QL-a!=0`, then
> \[
> r\log k<\log P\le\log(Q|L|+R).                     \tag{8}
> \]

**Proof.**  Divisibility gives `P<=|QL-a|`, while every prime factor of `P`
is larger than `k`.  The triangle inequality gives the last bound. `square`

In particular, for a fixed offset pattern, `L` is fixed.  More generally, if

\[
 \log|L|=o(k),\qquad \log R=o(k),                    \tag{9}
\]

then (7)--(8) imply

\[
 r\log k=o(k),\qquad k^r=\exp(o(k)).                 \tag{10}
\]

Thus any nonzero low-pole resonance of bounded algebraic complexity is
confined to a rank whose full polynomial `k^r` ledger is still
subexponential.  This is a genuine scale-dependent stratification and
explains why the fixed-rank direct no-go does not by itself refute every
absorbed global proof.

The hypothesis on `L` matters.  For an arbitrary large support the
Vandermonde product can have
`log|L|` comparable to `r^2 log k`, making (8) vacuous.  The bounded-prime-
cluster theorem fixes `r` before `k` grows and supplies no growing-rank
control of this term.

## 4. A proved exceptional-prime count for finitely many patterns

There is also a uniform divisor count at genuinely small centered radius.
Let `mathcal L` be a fixed finite set of nonzero signed pattern values and
define

\[
 E_k(R)=\{p\in(k,2k):p\mid Q\lambda-a
 \text{ for some }\lambda\in\mathcal L,
 |a|\le R\}.                                        \tag{11}
\]

Assume `R<Q min_{lambda in mathcal L}|lambda|`, so none of the integers in
(11) is zero.  Multiplying all of them and counting prime divisors gives

\[
 |E_k(R)|\log k
 \le\sum_{\lambda\in\mathcal L}\sum_{|a|\le R}
       \log|Q\lambda-a|
 \ll_{\mathcal L}(2R+1)(\log Q+1).                  \tag{12}
\]

Combining (7) and (12),

\[
 |E_k(R)|
 =O_{\mathcal L}\left(
 R\frac{k\log\log k}{\log^3k}
 \right).                                           \tag{13}
\]

Therefore, if

\[
 R=o(\log^2k/\log\log k),                            \tag{14}
\]

then `|E_k(R)|=o(k/log k)` and even

\[
 \log\prod_{p\in E_k(R)}p=o(k).                    \tag{15}
\]

If a fixed-pattern cluster has centered transported frequency at most `R`,
every one of its primes belongs to `E_k(R)`.  Equations (12)--(15) are an
honest exceptional-prime ledger; finite differencing is not used.

They are not yet a block recursion.  Imposing the exceptional congruences by
multiplying them into the absorber changes `Q` and hence changes the set
(11).  Likewise, merely knowing that all bad supports use a small prime
universe does not provide the signed cancellation between those supports.
No iterative absorption or fixed-prefix transfer is claimed here.

## 5. Why the available radius is insufficient

For the affine version of a putative fixed-`D` rank-`r` bound, (5) is
compatible with

\[
 \max_J|\sum_Jg(t)|\ll C^r k^{r+D}
\]

only if the transported resonance satisfies, up to a rank-dependent
constant,

\[
 |a|\gg_r k^{r-D}.                                  \tag{16}
\]

When `r>D`, this is a polynomial radius.  The affordable divisor range (14)
is only polylogarithmic and therefore falls far short of (16).  The rank
lemma (8) shows that a low resonance has an `exp(o(k))` polynomial ledger
when `log|L|=o(k)`, but it does not bound the sum of all such Fourier
supports.

Conversely, a strict affine counterexample of the old strength would require
an infinite fixed-pattern prime-cluster subsequence on which

\[
 |\langle Q(k)L\rangle_{P(k)}|
 \le k^{r-D-\delta}                                 \tag{17}
\]

for suitable fixed `r>D` and `delta>0` (constant centered residue would be
stronger).  Maynard's bounded-cluster theorem supplies the prime pattern but
contains no information on the varying binomial residue `Q(k) mod P(k)`.
Neither (17) nor its required opposite is proved here.

## 6. Closure boundary

- The exact affine image of the direct resonance is `a=<epsilon QL>_P`.
- The zero-dividend case is explicitly separated; for every fixed cluster
  rank, `Q>P` eventually and the nonzero divisor inequality applies.
- Low-pole resonances with `log|L|=o(k)` have only an `exp(o(k))` polynomial
  rank ledger, and finitely many fixed patterns have the exceptional-prime
  count (12)--(15).
- These results do not reach the polynomial radius (16), do not sum the bad
  Fourier supports, and do not construct the infinite residue family (17).

Accordingly, this round proves a reusable resonance-stratification lemma but
neither a dyadic block estimate nor an affine no-go theorem.  The phase and
`closes=[]` remain unchanged.
