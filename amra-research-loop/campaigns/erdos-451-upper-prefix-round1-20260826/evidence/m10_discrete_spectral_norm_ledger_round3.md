# M10 round 3: discrete spectral norm ledger

Date: 2026-08-27

Status: **proved local norm formulae, proved a scoped exponential no-go for
standard separated estimates, and isolated a sufficient joint arc theorem.**
The joint arc theorem remains open; no upper bound for Erdos 451 is claimed.

This note audits the exact discrete bridge in
`work/m10_round1/discrete_time_fejer_bridge_round3.md`.  Keep its notation:
`p=k+d`, balanced `r+s=d+1`,
`tau=lambda_r*lambda_s`, and `T=F tau` with the unnormalized finite Fourier
transform.

## 1. Exact local norms

Finite Parseval gives

\[
 \sum_{a\bmod p}|\widehat{\lambda_r}(a)|^2={p\over r},
 \qquad
 \sum_{a\bmod p}|\widehat{\lambda_s}(a)|^2={p\over s}.
\]

Since `T=widehat(lambda_r) widehat(lambda_s)`, Cauchy--Schwarz proves

\[
       \|T\|_1\le {p\over\sqrt{rs}}\le {2p\over d}.       \tag{1}
\]

For the square norm, Parseval and Young's convolution inequality give the
slightly sharper estimate

\[
 \sum_{a\bmod p}|T(a)|^2
   =p\sum_x\tau(x)^2
   \le {p\over s}\le {2p\over d}.                         \tag{2}
\]

The local square sum can also be written exactly (for `r<=s`) as

\[
 {p\over r^2s^2}
 \left(2\sum_{j=1}^{r-1}j^2+(s-r+1)r^2\right).            \tag{3}
\]

The CRT frequency map is bijective.  Hence, for
`Gamma(A)=product_i |T_i(a_i(A))|`, `D=product_i d_i`,

\[
 \Lambda_1:=\sum_A\Gamma(A)\le 2^m{P\over D},
 \qquad
 \Lambda_2:=\sum_A\Gamma(A)^2\le 2^m{P\over D}.           \tag{4}
\]

These are global norm statements; they retain no information about where
the mass lies under the CRT map.

For completeness, after the width-one coordinate has been eliminated,
the `L1` mass is genuinely exponential and not merely bounded above by an
exponential.  For every remaining `d>=2`, both `r/p` and `s/p` are below
`1/2`.  The elementary inequality `sin x>=2x/pi` on `[0,pi/2]` yields

\[
 |\widehat{\lambda_r}(1)|\ge {2\over\pi},\qquad
 |\widehat{\lambda_s}(1)|\ge {2\over\pi}.
\]

Thus

\[
       \|T\|_1\ge1+2|T(1)|\ge1+{8\over\pi^2},             \tag{5}
\]

and `Lambda_1 >= (1+8/pi^2)^m`.  This only diagnoses the loss of the
location-free `L1` ledger; it is not a lower bound for the actual Fejer
weighted sum.

## 2. Time-Fejer near/far decomposition

For the centered representative `0<|A|_P<=P/2`, the Dirichlet-kernel
bound gives

\[
 {W_h(A/P)\over h}
 \le \min\left\{1,{P^2\over4h^2|A|_P^2}\right\}.          \tag{6}
\]

Let `X_0=P/h`.  On the near arc `|A|_P<=X_0`, Cauchy--Schwarz and (4)
give

\[
 \sum_{0<|A|_P\le X_0}\Gamma(A)
       \le (2X_0\Lambda_2)^{1/2}.                          \tag{7}
\]

On the shell `2^jX_0<|A|_P<=2^(j+1)X_0`, use the same estimate and the
factor `O(4^(-j))` from (6).  The shell series converges, so the complete
standard separated `L2` ledger is

\[
 {1\over h}\sum_{A\ne0}W_h(A/P)\Gamma(A)
 \ll \left({P\over h}\Lambda_2\right)^{1/2}
 \le \left({2^mP^2\over hD}\right)^{1/2}.                 \tag{8}
\]

At the desired density scale

\[
                         h=k^B C_0^m{P\over D},            \tag{9}
\]

the right side of (8) is

\[
          k^{-B/2}P^{1/2}\left({2\over C_0}\right)^{m/2}.
                                                                    \tag{10}
\]

For every fixed `C_0`, its logarithm is
`(1/2+o(1))log P=Theta(k)`, because `m=Theta(k/log k)`.
Even replacing the fixed multiplier by `polylog(k)^m` only subtracts
`O(m log log k)=o(k)`.  Repaying the conductor square root would require
`m log C_0` on the order of `log P`, hence an `exp(Theta(k))` physical
window.  Therefore global `L2` followed by interval Cauchy--Schwarz cannot
prove an `exp(o(k))` result.

The still cruder bound `W_h<=h` gives `Lambda_1-1`; (5) shows that this
particular location-free ledger is already exponentially larger than one.
These are scoped method no-goes.  They do not say that the true coupled
sum is large.

The same calculation settles the scoped fixed higher-Holder ledger.  For every
real `q>=2`, `Gamma<=1` implies
`sum_A Gamma(A)^q<=Lambda_2`.  Holder on the near arc and then on each
doubling shell gives

\[
 {1\over h}\sum_{A\ne0}W_h(A/P)\Gamma(A)
 \ll_q \left({P\over h}\right)^{1-1/q}\Lambda_2^{1/q}.
                                                                    \tag{10a}
\]

At (9), its parameter ledger is

\[
 k^{-B(1-1/q)}C_0^{-m(1-1/q)}2^{m/q}
 P^{1/q}D^{1-2/q}.                                      \tag{10b}
\]

For `q=2` this is (10).  Every fixed `q>2` additionally retains the
positive power `D^(1-2/q)=exp(Theta(k))`; slowly growing `q` tends toward
the still worse support-scale factor `D`.  Thus fixed/higher Holder moments
do not remove the conductor loss in this separated ledger.  The implied
constant in (10a) is harmless for fixed `q`; allowing it to grow cannot
repair the displayed `Theta(k)` exponent without new localized structure.

## 3. Exact sufficient joint theorem

Define the centered cumulative mass, with the principal atom removed,

\[
 M_\gamma(X)=
 \sum_{0<|\gamma A|_P\le X}\Gamma(A),
 \qquad P/h\le X\le P/2,                                  \tag{11}
\]

where only the two relevant dilations are considered: `gamma=1` in the
original system, and the specific `gamma=p_0 (mod P')` after exact
elimination of a width-one prime.  In the latter case `P,h,m,D` in this
section mean the reduced quantities `P',H,m-1,D'`.  The following is sufficient:

\[
             M_\gamma(X)\le K^m{X\over P}\Lambda_1        \tag{12}
\]

for one absolute `K`, uniformly at all the displayed scales.  Applying
(12) to the near arc and each doubling arc in (6) gives

\[
 {1\over h}\sum_{A\ne0}W_h(\gamma A/P)\Gamma(A)
       \ll {K^m\Lambda_1\over h}
       \le k^{-B}O\left({2K\over C_0}\right)^m.           \tag{13}
\]

One fixed `C_0` larger than the absolute dyadic constant times `2K`
makes (13) less than one and proves the discrete sufficient inequality.
Because `log h=O(log k)+m log C_0+log(P/D)=o(k)`, this would give
`n_k=exp(o(k))`.

Equation (12) is a real location theorem, not another norm reformulation:
it asks for weighted CRT equidistribution down to arcs of length `P/h`.
It must retain the inverse-cofactor joint phases.  It is also not formally
invariant under every unit dilation.  In fact take the unit frequency
`A_0` corresponding to the local word `a_i=1` for every coordinate.
Equation (5) gives `Gamma(A_0)>=(4/pi^2)^m`.  The dilation
`gamma=A_0^(-1)` puts that atom at residue one, whereas at `X=P/h` the
right side of (12) is at most `k^(-B)(2K/C_0)^m`.  Choosing
`C_0>(pi^2/2)K` contradicts the all-unit version for large `k`.  Only the
undilated map and the one explicit width-one dilation are part of the
sufficient interface.

## 4. Narrow survivor

There is a useful exact dual narrowing before stating the survivor.  Put

\[
 R_{i,t}(a)=|\widehat{\lambda_t}(a)|^2,
 \qquad
 G_i(a)={R_{i,r_i}(a)+R_{i,s_i}(a)\over2}.                \tag{14}
\]

Arithmetic--geometric mean gives `|T_i(a)|<=G_i(a)`, with equality at
`a=0`.  Its mass is

\[
 L_i^G:=\sum_{a\bmod p_i}G_i(a)
 ={p_i\over2}\left({1\over r_i}+{1\over s_i}\right)
 ={p_i(r_i+s_i)\over2r_is_i}\le {2p_i\over d_i}.         \tag{15}
\]

Unlike `|T_i|` itself, this majorant has a nonnegative compactly supported
local Fourier transform.  For centered `|ell|_(p_i)<=p_i/2`, exact finite
Fourier inversion gives

\[
 \rho_i(\ell):=\sum_{a\bmod p_i}G_i(a)e_{p_i}(a\ell)
 ={p_i\over2}\left{
 { (r_i-|\ell|_{p_i})_+\over r_i^2}
 +{ (s_i-|\ell|_{p_i})_+\over s_i^2}
 \right}\ge0.                                           \tag{16}
\]

Let `L_G=product_i L_i^G` and `phi_i=rho_i/L_i^G`.  For the global product
majorant `G(A)=product_i G_i(a_i(A))`, CRT gives the exact factorization

\[
 \sum_{A\bmod P}G(A)e_P(\ell A)
                         =\prod_i\rho_i(\ell).            \tag{17}
\]

Let `gamma=1` in the original system; after exact removal of the
width-one prime, let `gamma=p_0 (mod P')` and replace `P,h` below by
`P',H`.  The integer Fejer expansion and `h<P` now prove in either case

\[
 \sum_{A\bmod P}W_h(\gamma A/P)G(A)
 =L_G Q_{h,\gamma},
\quad
 Q_{h,\gamma}:=\sum_{|\ell|<h}\left(1-{ |\ell|\over h}\right)
                         \prod_i\phi_i(\gamma\ell).       \tag{18}
\]

The original zero word and its majorant both have weight one.  Therefore

\[
 \sum_{A\ne0}W_h(\gamma A/P)\Gamma(A)
 \le L_GQ_{h,\gamma}-h.                                  \tag{19}
\]

This proves the following genuinely narrower sufficient statement:

> **Homogeneous weighted-prefix lemma (open).**  For integral `1<=h<P`, if
> \[
>                  Q_{h,\gamma}<{2h\over L_G},             \tag{20}
> \]
> then the discrete joint spectral inequality holds.

The normalization in (20) is exact rather than heuristic.  Over a complete
period,

\[
 {1\over P}\sum_{\ell\bmod P}\prod_i\phi_i(\ell)
 ={1\over L_G},                                           \tag{21}
\]

because the global product majorant has `G(0)=1`.  Thus (20) asks that the
triangular initial prefix, with the one explicitly required common
dilation, have less than twice its full-period density.  It keeps a common
integer `ell` in every local compact support and is not a separated norm
estimate.  Identity (18) is valid for every unit `gamma`, but no estimate
uniform over arbitrary units is claimed.

The zero dual frequency gives a sharp rigorous threshold for the
exponential window base.  Since `Q_(h,gamma)>=1`, (20) necessarily requires

\[
                         {L_G\over h}<2.                  \tag{21a}
\]

At `h=k^B C_0^mP/D`, write

\[
 {L_GD\over P}=\prod_i\kappa(d_i),\qquad
 \kappa(d)=
 \begin{cases}
 2(1-1/(d+1)),&d\text{ odd},\\
 2(1-1/(d+2)),&d\text{ even}.
 \end{cases}                                             \tag{21b}
\]

The offsets `d_i` are distinct.  Therefore
`sum_i 1/d_i=O(log k)` and

\[
                 2^m k^{-O(1)}\le\prod_i\kappa(d_i)\le2^m. \tag{21c}
\]

It follows that every fixed `C_0<2` violates (21a) for all sufficiently
large `k`, even after any fixed polynomial factor `k^B`.  Thus base two is
a genuine necessary exponential threshold for this positive majorant.
This does not decide `C_0=2` or any `C_0>2`; it does show that a proof based
on (20) cannot lower the base below two by sharper prefix cancellation.

Fejer monotonicity or averaging in the window length supplies no automatic
extra transfer.  For any nonnegative periodic function `f`, put
`S_f(t)=sum_(|ell|<t)f(ell)`.  Directly counting how often a fixed `ell`
appears proves the exact Cesaro identity

\[
 \sum_{|\ell|<h}\left(1-{|\ell|\over h}\right)f(\ell)
                         ={1\over h}\sum_{t=1}^hS_f(t).    \tag{21d}
\]

The data `0<=f<=1`, `f(0)=1`, and complete-period mean `1/L_G` do not
control the right side.  Whenever `2h-1<=P/L_G`, take `f=1` on
`|ell|<h` and distribute the remaining required mass symmetrically outside
that arc.  It has the prescribed mean, while the left side of (21d) is
exactly `h`, which violates the factor-two target for `L_G>2`.  This is a
strict no-go for **generic** Fejer averaging plus full-period mean.  The
inequality `2h-1<=P/L_G` holds in the 451 target range because
`P/L_G>=D/2^m=exp(Theta(k))` whereas `h=exp(o(k))`.  The
constructed `f` need not factor into the special triangles (16), so it
does not refute the surviving arithmetic product theorem.

This dualization does not itself prove (20).  Bounding the number or total
weight of the common-start residues by support size alone is precisely a
short-prefix density-transfer problem.  M05 Theorem 4.1 supplies an
anchored successor in a dyadic block; it does not give the required upper
bound on the weighted number of common-start dual residues.  Consequently
(20) is narrower and executable, but remains open.

The factor two in (20) is substantive.  A bound merely of the form
`Q_(h,gamma)<=K^m h/L_G` does **not** close (20), and increasing the window
constant does not formally absorb this relative density loss.  Thus this
positive AM--GM dual is a stricter residual than the fixed-exponential arc
lemma (12), not a replacement for its more flexible conclusion.

An additive, rather than relative, discrepancy is sufficient and is the
most useful formulation of the residual:

\[
                  Q_{h,\gamma}\le {h\over L_G}+K^m.       \tag{21e}
\]

Indeed `L_G<=2^mP/D`, so at `h=k^B C_0^mP/D`,

\[
                         {h\over L_G}\ge k^B(C_0/2)^m.    \tag{21f}
\]

One fixed `C_0>2K` makes the additive error smaller than the main term and
proves (20).  More generally an error `R(k)^m` can be absorbed by putting
the same factor into the window whenever `m log R(k)=o(k)`; this includes
polylogarithmic `R`.  At the boundary `C_0=2`, a polynomial additive error
could instead be absorbed by increasing the fixed power `B`, whereas a
genuine `K^m`, `K>1`, cannot.

Fixed low dual frequencies can be peeled off at exactly this additive
cost.  Since every `0<=phi_i<=1`, for every integer `R<h`,

\[
 \sum_{|\ell|\le R}\left(1-{|\ell|\over h}\right)
                  \prod_i\phi_i(\gamma\ell)\le2R+1.      \tag{21f'}
\]

Consequently, after choosing `R=floor(K^m)`, a tail estimate

\[
 \sum_{R<|\ell|<h}\left(1-{|\ell|\over h}\right)
                  \prod_i\phi_i(\gamma\ell)
       \le {h\over L_G}+O(K^m)                           \tag{21f''}
\]

is sufficient, with the absolute constant absorbed by increasing the
fixed closing base.  Thus the universal `ell=1` word and every other fixed
bounded-prefix resonance cannot obstruct a `C_0>2K` theorem.  The true
moving survivor is the weighted tail `|ell|>K^m`.  This is an exact
reduction, not an estimate for that tail.

The exact triangles turn that tail into a coefficient-aware lattice-energy
problem.  If `x=|gamma ell|_p` is the centered local residue, direct use of
(16) in the two parity cases gives

\[
       0\le\phi_i(\gamma\ell)
       \le\left(1-{2x\over d_i+1}\right)_+.              \tag{21f1}
\]

For odd `d`, this is the usual normalized triangle.  For even `d`, there
is no integer strictly between the balanced lengths `r` and `s=r+1`, and
the same bound holds at the last possible point by direct substitution.
Consequently, with

\[
             \mathcal E_\gamma(\ell)
             :=\sum_i{|\gamma\ell|_{p_i}\over d_i+1},     \tag{21f2}
\]

one has

\[
                  \prod_i\phi_i(\gamma\ell)
                  \le e^{-2\mathcal E_\gamma(\ell)}.     \tag{21f3}
\]

For every threshold `eta>0`, the moving tail is therefore at most

\[
 \#\{R<|\ell|<h:\mathcal E_\gamma(\ell)<\eta m\}
                         +2h e^{-2\eta m}.                \tag{21f4}
\]

This exposes, but does not solve, a special-lattice interface.  In fact the
naive threshold plus trivial-cardinality use of (21f4) is itself too weak.
On the positive support every summand in `E_gamma` is below `1/2`, so
`E_gamma<m/2`.  At the same time (21j) below gives `L_G>3^m`.  Even the
formally strongest pointwise damping supplied by (21f3), namely `e^(-m)`,
leaves the ledger

\[
                         h e^{-m}>{h\over L_G}.           \tag{21f5}
\]

Moreover, once `h/L_G` dominates the allowed additive `K^m`, the same
ledger exceeds `K^m` by at least `(3/e)^m`.  Thus an energy cutoff followed
by counting all remaining integers cannot close the additive theorem.
The surviving statement must bound the **weighted distribution** of the
joint energies (or count exceptional energies at the density scale) more
sharply than (21f4).  Marginal residue sizes and the number of divisible
coordinates alone do not do this.  No such weighted theorem is proved
here.

There is one unconditional localized theorem for the undilated case.
When `gamma=1` and `0<|ell|<k/2`, every `p_i>k` sees the ordinary residue
`|ell|`, without wraparound.  Since `d_i+1<=k`, (21f1) gives

\[
 \prod_i\phi_i(\ell)
 \le\exp\left(-2|\ell|\sum_i{1\over d_i+1}\right)
 \le\exp(-2m|\ell|/k).                                  \tag{21k}
\]

Consequently, for the target range `h>k/2`, the entire undilated small arc
has the proved bound

\[
 \sum_{|\ell|<k/2}\left(1-{|\ell|\over h}\right)
                 \prod_i\phi_i(\ell)
 \le1+{2\over e^{2m/k}-1}\le1+{k\over m}=O(\log k).     \tag{21l}
\]

This is an affordable additive error, including at the boundary base two
after a polynomial window factor.  It does not use a prime-gap estimate.
For the actual target `h>k`, the same bound holds with the left arc enlarged to `|ell|<k`:
for `k/2<=|ell|<k`, the exact quotient condition (21m) below has neither
an admissible `q=0` prime below `2k` nor an admissible `q>=1` prime above
`k`, so the product is identically zero.

The lemma is not dilation invariant.  For the exceptional dilation
`gamma=p_0=k+1`, the local residue is
`(1-d_i)ell (mod k+d_i)`, so even small `ell` can wrap and no interval of
length `k/2` has the preceding common residue.  There is nevertheless the
exact isolated fact that `ell=+-1` is annihilated whenever one remaining
offset has `d_i>=3`: its centered residue has size `d_i-1`, outside the
support `|x|<s_i<= (d_i+2)/2` (with the equality cases checked directly).
This single-frequency fact is not a replacement for (21l).

Removing the `O(k)` small arc does not repair the standard larger-sieve
denominator (22): the remaining prefix still has length `h=exp(o(k))`, so
the negative `-log h` term is unchanged at main order.  Thus (21l) does not
connect to a support-only middle/high-frequency estimate.  The unresolved
piece is precisely the weighted joint tail for `|ell|>=k` when
`gamma=1`, and essentially the whole moving tail for `gamma=p_0`.

The exact quotient form explains why the small-arc estimate does not
extend by routine prime counting.  For `ell>0`, let `N=gamma ell` as an ordinary
integer (`gamma=1` or `p_0` in the two required cases).  The balanced local
support is, for integer residues, exactly

\[
                   2|N-qp|\le p-k                         \tag{21m}
\]

for the nearest appropriate integer quotient `q`.  For `q>=1`, (21m) is
equivalent to

\[
 {2N+k\over2q+1}\le p\le {2N-k\over2q-1}.               \tag{21n}
\]

The upper endpoint for quotient `q+1` and the lower endpoint for quotient
`q` leave the exact forbidden gap

\[
 {2N+k\over2q+1}-{2N-k\over2q+1}
                         ={2k\over2q+1}.                  \tag{21o}
\]

Thus a nonzero product requires every actual prime in `(k,2k)` to lie in
the union of the quotient intervals (21n); every intervening gap that
meets `(k,2k)` must be prime-free.  For the active quotients
`q asymp N/k`, the gap scale is `k^2/N`.  It becomes shorter than one once
`N` exceeds a fixed constant multiple of `k^2` (for example, `N>2k^2`
puts every active quotient beyond the unit-gap threshold, up to harmless
endpoint rounding), so prime-gap information cannot treat the long
tail `N` up to `gamma h=exp(o(k))`.

Nor does counting primes separately in each fixed-`q` interval bound the
weighted product.  The factor in (21f1) depends on the locations
`|N-qp|/(p-k+1)` inside every interval, and all quotient intervals together
must account for **every** prime coordinate.  Separate interval counts
discard this joint product, while multiplying independent upper bounds
reintroduces the already-failed coordinatewise exponential ledger.  For
large `q` the interval and gap scales are also below the range of available
uniform short-interval prime estimates.  Hence (21m)--(21o) are an exact
quotient-gap reparameterization of the original multiple-free obstruction,
not a new weighted middle-frequency theorem.  The exceptional dilation
only restricts `N` to multiples of `p_0`; it does not change this gap
identity.

This additive statement is exactly the positive-majorant dual of an arc
dispersion theorem, not a free consequence of smoothing.  From (18),

\[
 L_GQ_{h,\gamma}-h
   =\sum_{A\ne0}W_h(\gamma A/P)G(A).                      \tag{21g}
\]

Applying the centered-arc lemma (12) with `Gamma` replaced by `G` and
`Lambda_1` by `L_G` bounds the right side by `O(K^mL_G)`, which is precisely
(21e), up to the absolute dyadic constant.  The original `Gamma`-arc lemma
does not imply this `G` version merely from `Gamma<=G`.

Nor does standard period conditioning establish (21e).  This can be made
exact.  For a subset `J`, put `P_J=product_(i in J)p_i`,
`L_J=product_(i in J)L_i^G`, and
`f_J(ell)=product_(i in J)phi_i(gamma ell)`.  It is nonnegative,
`P_J`-periodic, at most one, and has one-period mass `P_J/L_J`.
Every interval of `N` consecutive integers therefore has `f_J`-mass at
most `N/L_J+P_J/L_J`.  Using the Cesaro identity (21d) gives

\[
 Q_{h,\gamma}\le Q_{h,\gamma}^{(J)}
                  \le {h+P_J\over L_J}.                  \tag{21h}
\]

If `J` is proper, the main term on the right is

\[
 {h\over L_J}=L_{J^c}{h\over L_G}.                       \tag{21i}
\]

Moreover

\[
 L_i^G={p_i(d_i+1)\over2r_is_i}
       \ge {2p_i\over d_i+1}>3                           \tag{21j}
\]

for the relevant `k>=3`, `1<=d_i<k`.  Thus disposing of even one coordinate
makes the available main ledger already exceed the factor-two target.  If
`J` is the full set, (21h) instead pays the boundary `P/L_G=exp(Theta(k))`
because `P>>h`.  This rigorously kills this **subset disposal plus complete
periods** proof class.  It does not lower-bound the true `Q`, since the
omitted factors can create essential suppression.  Generic Fejer averaging
is already killed by (21d); only the special full product of triangles can
still prove (21e).

The standard support-only larger sieve cannot prove (20).  From (16), a
surviving `ell` lies in at most `2s_i-1` residue classes modulo `p_i`.
Its larger-sieve denominator is bounded above by

\[
 \sum_i{\log p_i\over 2s_i-1}-\log(2h)
 \le \sum_i{\log(2k)\over d_i}-\log(2h)
 =O((\log k)^2)-\Omega(k/\log k)<0,                       \tag{22}
\]

for the target fixed-exponential window.  This is a rigorous no-go for
that support-only tool, not for a weighted common-start argument retaining
the triangular values in (16).

The guarded finite companion
`evidence/m10_discrete_positive_prefix_round3.md` separates the constant
threshold from the asymptotic claim.  Its exhaustive eligible sweep for
`10<=k<=50` found four genuine failures at the `B=0` specialization
`h=ceil(2^mP/D)`, with normalized ratios between `2.0410` and `2.1606`;
hence that literal finite `C_0=2,B=0` form of (20) is false.  All 33
eligible systems passed at `C_0=5/2,B=0`, with maximum ratio `1.59945`, and
selected `C_0=3` ratios were near one.  This leaves some fixed
`C_0>=5/2` at `B=0` as a **finite survivor only**; it does not refute a
polynomially enlarged `k^B` form.  The data show that constant window
enlargement smooths the observed spikes, not that one fixed constant works
as `k` and the rank tend to infinity.

## 5. Final survivor

The standard global `L1`, global `L2`, support-only entropy, and sequential
complete-period ledgers all lose `exp(Theta(k))`.  The narrow survivor is
therefore:

```text
prove weighted centered-arc equidistribution (12), with fixed-exponential
loss per prime, for the actual inverse-cofactor CRT phases and for the one
explicit width-one dilation.
```

A `polylog(k)^(O(m))` loss would also be affordable after multiplying the
window by the same factor, since its logarithm is `o(k)`.  No such theorem
is proved here.  M05 Theorem 4.1 does not supply it: that theorem controls
an anchored homogeneous successor in one dyadic block, not the mass in
arbitrary centered CRT arcs for the full inhomogeneous system.

Equivalently, one may attack the still narrower positive form (20): prove
a factor-two short-prefix density upper bound for the compact triangular
dual weights (16).  This equivalence is one-way as written--(20) is a
sufficient majorant--and no claim is made that every proof of (12) must
pass through it.

Within that positive form, the final executable target is the additive
discrepancy (21e), after peeling the proved `O(log k)` undilated arc
`|ell|<k` (or an affordable `K^m` prefix).  The remaining sums are the
weighted joint tail `|ell|>=k` for `gamma=1` and the corresponding moving
tail for the one specific `gamma=p_0`.  Equations (21m)--(21o) show that
fixed-quotient prime counts alone only re-express this tail; the missing
input is a density-scale bound that keeps the full triangular product
across all quotient intervals.
