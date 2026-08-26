# Weighted multiplicative characters: a low-conductor theorem and two high-conductor no-go results

This note continues `survivor_deepening` from the exact unit-group identity
in `free_multiplier_bilinear_counting_audit.md`.  It proves that the entire
low-conductor character contribution is negligible at an affordable
`exp(O(k/log k))` rectangle.  It then proves two delimited no-go theorems:
support-wise separated Hilbert-space duality still pays the full CRT product,
and a small-prime multiplicative random walk cannot repair that loss within
an `exp(o(k))` value budget.  None of these results proves Erdos 451;
`closes=[]` remains unchanged.

## 1. Exact primitive-conductor decomposition

Retain the notation

\[
 A=\lfloor k/\log ^2k\rfloor,
 \quad \mathcal P=\{p:k+A<p<2k\},
 \quad P=\prod_{p\in\mathcal P}p.
\]

For `p=k+b`, put `d_p=b-1` and

\[
 \mathcal A_p^\times
 =\{-Q_0^{-1},-2Q_0^{-1},\ldots,-d_pQ_0^{-1}\}\pmod p,
 \qquad
 \delta_p={d_p\over p-1},
 \quad \delta=\prod_p\delta_p.                     \tag{1}
\]

Every multiplicative character modulo the squarefree `P` is a tuple
`chi=(chi_p)_p`.  Its support is

\[
 S(\chi)=\{p:\chi_p\ne1\},
 \qquad f_\chi=\prod_{p\in S(\chi)}p.              \tag{2}
\]

Because every nonprincipal character modulo a prime is primitive, `f_chi`
is exactly the primitive conductor.  Define the relative local coefficient

\[
 \rho_{p,\psi}
 ={1\over d_p}\sum_{x\in\mathcal A_p^\times}\overline{\psi(x)}.
                                                               \tag{3}
\]

The normalized group Fourier coefficient factors exactly as

\[
 c_\chi=\delta\prod_{p\in S(\chi)}\rho_{p,\chi_p}.  \tag{4}
\]

If `chi^*` is the primitive character modulo `f_chi`, its interval sum with
the remaining-prime unit sieve is

\[
 S_X^P(\chi)=\sum_{n\le X}\chi^*(n)
                  {\bf1}_{(n,P/f_\chi)=1}.
\]

Möbius inversion gives the exact support/conductor formula

\[
 S_X^P(\chi)=
 \sum_{\substack{e\mid P/f_\chi\\ e\le X}}
   \mu(e)\chi^*(e)
   \sum_{m\le X/e}\chi^*(m).                      \tag{5}
\]

This is the precise cost of the outer principal components; treating
`S_X^P(chi)` as an unsieved primitive sum would be incorrect.

## 2. Local interval coefficients

The absorber phase is explicit:

\[
 \rho_{p,\psi}
 =\psi(-Q_0){1\over d_p}sum_{j=1}^{d_p}\overline{\psi(j)}.
                                                               \tag{6}
\]

Thus `Q_0` affects the signed character sum, but disappears from every
absolute moment.  Multiplicative Parseval gives

\[
 \sum_{\psi\bmod p}|\rho_{p,\psi}|^2={p-1\over d_p},
 \qquad
 \sum_{\psi\ne1}|\rho_{p,\psi}|^2={k\over d_p}.    \tag{7}
\]

More generally, for every integer `nu>=1`,

\[
 \sum_{\psi\bmod p}|\rho_{p,\psi}|^{2\nu}
 ={p-1\over d_p^{2\nu}}E_{p,\nu}(d_p),             \tag{8}
\]

where

\[
 E_{p,\nu}(d)=\#\{x_1\cdots x_\nu\equiv
 y_1\cdots y_\nu\pmod p:1\le x_i,y_i\le d\}.     \tag{9}
\]

Equations (7)--(9) are exact.  They show why an absolute high-moment method
cannot use the inverse-binomial phase: the phase has already canceled.

Let

\[
 L_p=\sum_{\psi\ne1}|\rho_{p,\psi}|.
\]

Cauchy--Schwarz and (7) give

\[
 L_p\le\sqrt{(p-2)k/d_p}.                          \tag{10}
\]

For a bulk prime, say `3k/2<p<7k/4`, one also has the matching exponent

\[
 {c\sqrt k\over\log k}\le L_p\le C\sqrt k.        \tag{11}
\]

Indeed (7) is bounded below by an absolute constant in this range, while
Polya--Vinogradov gives

\[
 \max_{\psi\ne1}|\rho_{p,\psi}|
 \ll {\sqrt p\log p\over d_p}\ll{\log k\over\sqrt k}.
\]

Since `sum |rho|^2 <= (max |rho|) sum |rho|`, this proves the lower bound in
(11); (10) proves the upper bound.  Consequently the exact-support
absolute coefficient ledger on `r` bulk primes is

\[
 \prod_{p\in S}L_p=k^{r/2+o(r)}=f_S^{1/2+o(1)}.     \tag{12}
\]

The factor `k^(r/2)` is therefore real coefficient entropy, not merely a
loose application of Cauchy--Schwarz.

## 3. The outer unit sieve is subexponential

Let `m=|mathcal P|=O(k/log k)`.  Every divisor `e|P/f` with `e<=X` contains
at most

\[
 J_X=\left\lfloor{\log X\over\log k}\right\rfloor \tag{13}
\]

remaining primes.  Hence, uniformly in the conductor `f`,

\[
 D_X(f):=\#\{e:e\mid P/f,\ e\le X\}
 \le D_X:=\sum_{0\le j\le J_X}{m\choose j}.         \tag{14}
\]

If

\[
 x=\log X=\gamma{k\over\log k}
\]

for any fixed `gamma>0`, then

\[
 \log D_X
 =O\left({k\log\log k\over\log ^2k}\right)=o(x). \tag{15}
\]

For every nonprincipal `chi`, (5) and Polya--Vinogradov therefore prove the
uniform, fully sieved estimate

\[
 |S_X^P(\chi)|
 \ll D_X\sqrt{f_\chi}\log f_\chi.                 \tag{16}
\]

This is stronger than the earlier `O(X/log k)` comparison with the
unsieved sum and is sufficient to settle a genuine low-conductor range.

## 4. An unconditional low-conductor aggregate theorem

Fix `gamma>0` and `0<eta<4/3`, and take

\[
 x=\gamma{k\over\log k},\qquad X=\lfloor e^x\rfloor,
 \qquad Y=\exp((4/3-\eta)x).                        \tag{17}
\]

> **Low-conductor character theorem.**
> \[
> \sum_{\substack{\chi\ne1\\f_\chi\le Y}}
> |c_\chi|\,|S_X^P(\chi)|^2=o(\delta X^2).         \tag{18}
> \]

**Proof.**  For an exact support `S`, (4) gives

\[
 \sum_{S(\chi)=S}|c_\chi|
 =\delta\prod_{p\in S}L_p.                         \tag{19}
\]

By (16), the left side of (18), divided by `delta X^2`, is at most

\[
 {C D_X^2\over X^2}
 \sum_{\substack{S\ne\emptyset\\P_S\le Y}}
 P_S(\log P_S)^2\prod_{p\in S}L_p.                \tag{20}
\]

Every such support has

\[
 |S|\le R={\log Y\over\log k}.
\]

For large `k`, `d_p>=A`, so (10) gives
`L_p<=C sqrt(k) log k`; also `p<2k`.  Enlarging (20) to every support of
rank at most `R` gives

\[
 \sum_{r\le R}{m\choose r}
      (Ck^{3/2}\log k)^r\,(\log Y)^2.               \tag{21}
\]

Here `R=O(k/log^2 k)` and

\[
 \log {m\choose R}=O(R\log(em/R))=o(x).
\]

The logarithm of (21) is therefore at most

\[
 {3\over2}R\log k+o(x)
 \le (2-3\eta/2)x+o(x).                            \tag{22}
\]

Equations (15), (20), and (22) give
`exp(-(3eta/2)x+o(x))`, proving (18). `square`

Thus the outer unit sieve and **all** characters through conductor
`X^(4/3-eta)` are no longer an open part of the interface.  This does not
prove a positive count because the full conductor is
`P=exp((1+o(1))k)`, far beyond `Y=exp(O(k/log k))`.

## 5. Why standard pointwise conductor splitting stops at `4/3`

The threshold in (18) is not an arbitrary use of Polya--Vinogradov.  Apply
the `nu`-th Burgess estimate termwise in (5).  Suppressing powers
`f^epsilon` and the common `D_X=exp(o(x))`, it gives

\[
 |S_X^P(\chi)|
 \ll X^{1-1/\nu}
       f_\chi^{(\nu+1)/(4\nu^2)+o(1)}.              \tag{23}
\]

On bulk supports the exact coefficient ledger (12) then makes the absolute
triangle bound, relative to `delta X^2`, have exponential scale

 \[
 X^{-2/\nu}
 f^{1/2+(\nu+1)/(2\nu^2)+o(1)}.                   \tag{24}
\]

It can decay only when

\[
 {\log f\over\log X}
 <{4\nu\over\nu^2+\nu+1}.                          \tag{25}
\]

For integer `nu>=1`, the right side is maximized at `nu=1`, where it equals
`4/3`; `nu=2` already gives `8/7`, and the values then decrease.  Therefore
higher Burgess moments do not extend the conductor range after the true
`f^(1/2+o(1))` coefficient entropy is included.

This is a rigorous no-go for the method class that applies a uniform
pointwise primitive-character bound and then sums characters and supports
absolutely.  It is not a lower bound for the actual signed high-conductor
contribution.

## 6. Support-aware duality still pays the full CRT modulus

One might instead apply Cauchy--Schwarz separately on each exact support.
The full support already rules this out.

Let `mathcal W` be any multiset of `N=exp(o(k))` positive units modulo `P`,
all represented by integers at most `T=exp(o(k))`, and put

\[
 K_\chi(\mathcal W)=\sum_{w\in\mathcal W}\chi(w).
\]

Orthogonality over characters nonprincipal at **every** local prime gives
the exact identity

\[
 \sum_{S(\chi)=\mathcal P}|K_\chi(\mathcal W)|^2
 =\sum_{x,y\in\mathcal W}
   \prod_{p\in\mathcal P}
   \begin{cases}
     p-2,&x\equiv y\pmod p,\\
     -1,&x\not\equiv y\pmod p.
   \end{cases}                                      \tag{26}
\]

The `N` identical-index terms contribute

\[
 N\prod_{p\in\mathcal P}(p-2)=N\exp((1+o(1))k).    \tag{27}
\]

For distinct integer values `x ne y`, only primes dividing `x-y` select the
large local factor.  There are at most

\[
 {\log T\over\log k}=o(k/\log k)
\]

such primes, so one off-diagonal term has magnitude `exp(o(k))`; all
off-diagonal terms together have magnitude `exp(o(k))`.  Equal values from
different multiset indices only add further positive copies of (27).
Consequently

\[
 \sum_{S(\chi)=\mathcal P}|K_\chi(\mathcal W)|^2
 \ge(1-o(1))N\prod_p(p-2).                          \tag{28}
\]

The exact full-support coefficient square mass is

\[
 \sum_{S(\chi)=\mathcal P}|c_\chi|^2
 =\prod_{p\in\mathcal P}\delta_p(1-\delta_p)
 =\exp(-\Theta(k/\log k)).                          \tag{29}
\]

For the upper bound on `-log delta`, split the offsets into dyadic blocks
`B<b<=2B`.  The standard prime upper bound gives `O(B/log k)` primes in a
block, whose total contribution is
`O((B/log k)log(2k/B))`; summing from `A` to `k` is `O(k/log k)`.
Also `-log(1-delta_p)=log((p-1)/k)=O(1)` for every `p`.  The matching lower
bounds follow by restricting to `3k/2<p<7k/4`, where both factors are
bounded away from zero and one and there are `Theta(k/log k)` primes.

Therefore the **numerical right side** produced by separated Cauchy--Schwarz
on this one conductor slice, relative to its density-scale main term, is

\[
 \exp((1/2+o(1))k)                                  \tag{30}
\]

for every affordable `N=exp(o(k))`.  This strengthens the earlier global
large-sieve no-go: decomposing by exact support before taking separate
`L^2` norms does not remove the exponential loss.  Equation (30) is a
method-ledger lower bound, not a lower bound for the signed Fourier error.

This applies directly to the bilinear rectangle in (18): take `mathcal W`
to be the multiset

\[
 \{ut:u,t\le X,\ (ut,P)=1\}.
\]

Then `N=|mathcal U_X|^2=(1+o(1))X^2=exp(o(k))`, every represented value is
at most `T=X^2=exp(o(k))`, and
`K_chi(mathcal W)=S_X^P(chi)^2`.

## 7. A distinct kill test: small-prime multiplicative walks

Let `G` be any set of `g` primes at most `k`, and form multipliers

\[
 u=g_1\cdots g_L,\qquad g_i\in G.                  \tag{31}
\]

They are automatically units modulo `P`.  The character kernel is

\[
 K_\chi=\left(\sum_{g\in G}\chi(g)\right)^L.       \tag{32}
\]

If `k^L<P`, unique factorization gives the exact moment

\[
 \sum_{\chi\bmod P}
   \left|\sum_{g\in G}\chi(g)\right|^{2L}
 =\varphi(P)E_L(G),                                 \tag{33}
\]

where `E_L(G)` counts two ordered length-`L` prime words with the same
multiset.  In particular

\[
 g^L\le E_L(G)\le L!g^L.                            \tag{34}
\]

The upper bound follows by fixing the first word and permuting it; repeated
letters only reduce the number of permutations.

More decisively, the multiset of all `N=g^L` word products satisfies the
full-support lower bound (28) whenever `L log k=o(k)`.  Hence support-wise
duality can cease paying `sqrt(P/N)` only if

\[
 N\ge P^{1-o(1)},\qquad
 L\log g\ge(1-o(1))k.                               \tag{35}
\]

Since `g<=pi(k)` and `log g<=(1+o(1))log k`, (35) forces

\[
 L\log k\ge(1-o(1))k.                              \tag{36}
\]

But `L log k` is already the logarithmic size budget of the product in
(31).  Thus this walk cannot achieve full-support Hilbert-space mixing while
keeping the multiplier `exp(o(k))`.  Collisions between permutations only
increase (28), so the unique-factorization energy does not rescue it.

This no-go is structurally different from Burgess and interval large sieve:
it applies to a deliberately multiplicative, automatically unit-supported
multiplier family.  It rules out only the plan of proving positivity through
separate spectral `L^2` mixing of that walk; special signed correlation with
the allowed-set coefficients is not excluded.

## 8. Exact inverse transform and a cumulant kill test

The surviving signed slice has a direct physical-space form.  With the
Fourier convention in (3), inversion is

\[
 {\bf1}_{\mathcal A_p^\times}(x)
 =\sum_{\psi\bmod p}c_{p,\psi}\psi(x),
 \qquad c_{p,1}=\delta_p.
\]

Therefore, for every support `S` and every multiset `mathcal W` of units,

\[
 \sum_{S(\chi)=S}c_\chi K_\chi(\mathcal W)
 =\left(\prod_{p\notin S}\delta_p\right)
   \sum_{x\in\mathcal W}
   \prod_{p\in S}
     \left({\bf1}_{\mathcal A_p^\times}(x)-\delta_p\right).       \tag{37}
\]

In particular, the exact-full-support slice is

\[
 \sum_{S(\chi)=\mathcal P}c_\chi K_\chi(\mathcal W)
 =\sum_{x\in\mathcal W}\prod_{p\in\mathcal P}
   \left({\bf1}_{\mathcal A_p^\times}(x)-\delta_p\right).         \tag{38}
\]

There is no missing conjugate: (3) uses `overline(psi)` in the coefficient,
so inversion uses `psi(x)`.  The `Q_0` scaling is already present in the
sets `mathcal A_p^times`; equivalently it is the phase `psi(-Q_0)` in (6).
For the two-variable rectangle, take `mathcal W` to be the multiset of all
products `ut`; then `K_chi(mathcal W)=S_U^P(chi)S_H^P(chi)`.

Equation (38) is the highest-order centered correlation.  It also gives an
active kill test for a bounded-order cluster or cumulant closure.  On the
abstract product cube with `delta_p=1/2`, the uniform measures on the even-
and odd-parity halves have identical marginals and identical centered
correlations on every proper support, while their full centered products
have opposite signs.  Depending on the parity of the dimension, exactly
one of the two halves contains the all-allowed vertex.  Hence bounded-order
centered correlations cannot certify an all-allowed point for arbitrary
product boxes.  Separately, a singleton with exactly two violated
coordinates has, when every `delta_p=1/2`, the same positive full centered
product as the all-allowed singleton.  Thus even the sign and magnitude of
(38) alone do not certify an all-allowed point.

This parity witness does not imitate the special 451 product multiset and
does not refute a 451-specific high-order theorem.  It does show that a
generic cumulant truncation cannot be the missing handoff.  Moreover, for
one point `x`, the sign in (38) is the parity of the number of violated
coordinates, but its magnitude is

\[
 \prod_{p:\,x\text{ is allowed}}(1-\delta_p)
 \prod_{p:\,x\text{ is forbidden}}\delta_p.         \tag{39}
\]

Thus violation parity alone even discards the varying weights needed by the
exact correlation.

## 9. The unique remaining interface

The low-conductor portion through `X^(4/3-eta)` is proved negligible.  The
following three proposed high-conductor handoffs are killed:

1. uniform primitive-character bounds plus absolute conductor entropy;
2. global or support-wise separated `L^2` duality, including affordable
   small-prime multiplicative walks; and
3. generic bounded-cumulant or violation-parity closure.

All absolute local moments erase the phase `chi(-Q_0)` in (6).  The sole
remaining multiplicative-character interface is therefore a **signed
high-conductor estimate**

\[
 \sum_{f_\chi>X^{4/3-\eta}}
 c_\chi S_X^P(\chi)^2=o(\delta X^2),                \tag{40}
\]

or a one-sided lower bound of the same strength.  By (37), this is exactly a
weighted sum of high-support centered correlations, not merely abstract
character entropy.  It must keep the joint `Q_0` phase coupled to both
sieved character sums and must use the special product multiset strongly
enough to evade the parity counterexample.  This is a strictly narrower
target than the original full character identity because (18) has removed
every low conductor unconditionally.  It remains open, and no current
large-sieve, Burgess, conductor-entropy, bounded-cumulant, or random-walk
moment bound proves it.
