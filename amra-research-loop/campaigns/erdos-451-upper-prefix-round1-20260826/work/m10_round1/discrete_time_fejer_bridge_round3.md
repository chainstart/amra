# Round 3: an exact discrete-time Fejer bridge

Date: 2026-08-27

Status: **proved reduction; joint spectral inequality open.**  This bridge
is introduced because the continuous all-translate box-spline requires a
separate common-time integrality reconstruction.  Here every time variable
is an integer from the outset.

## 1. Local positive functions with exact allowed support

For every prime `p_i=k+d_i` in `(k,2k)`, choose positive integers `r_i,s_i`
with

\[
                         r_i+s_i=d_i+1.                     \tag{1}
\]

On `Z/p_i Z`, let `lambda_r` be the uniform probability measure on
`{0,...,r-1}` and put

\[
                  \tau_i=\lambda_{r_i}*\lambda_{s_i}.       \tag{2}
\]

There is no wraparound because `d_i<p_i`.  Thus `tau_i` is nonnegative,
has total mass one, and has positive support exactly
`{0,...,d_i-1}`.  The balanced choice

\[
 r_i=\lfloor(d_i+1)/2\rfloor,\qquad
 s_i=\lceil(d_i+1)/2\rceil                                \tag{3}
\]

maximizes the two smoothing lengths.  When `d_i=1`, (2) is simply the
point mass at zero, with no artificial factor two.

Use the unnormalized local Fourier transform

\[
 \mathcal F_i f(a)=\sum_{x\bmod p_i}f(x)e_{p_i}(-ax).
\]

Then

\[
 T_i(a):=\mathcal F_i\tau_i(a)
 = {1\over r_i}\sum_{u=0}^{r_i-1}e_{p_i}(-au)
   {1\over s_i}\sum_{v=0}^{s_i-1}e_{p_i}(-av),             \tag{4}
\]

so `T_i(0)=1` and `|T_i(a)|<=1`.

## 2. Exact integer-time count

Put `P=product_i p_i`.  For a word `a=(a_i mod p_i)`, define its global
character frequency

\[
          A(a)=\sum_i a_i{P\over p_i}\pmod P.              \tag{5}
\]

This is a bijection from the local frequency words to `Z/PZ`.  Define the
integer triangular window

\[
 \omega_h(t)=\left(1-{|t|\over h}\right)_+\quad(t\in\mathbb Z),
 \qquad
 W_h(\alpha)=\sum_{t\in\mathbb Z}\omega_h(t)e(\alpha t).
                                                                    \tag{6}
\]

For integral `h>=1`, the elementary convolution identity gives

\[
 W_h(\alpha)={1\over h}\left|\sum_{u=0}^{h-1}e(\alpha u)\right|^2
 \ge0,\qquad W_h(0)=h.                                    \tag{7}
\]

For any integer center `c`, consider

\[
 N(c)=\sum_{t\in\mathbb Z}\omega_h(t)
             \prod_i\tau_i(c+t\bmod p_i).                  \tag{8}
\]

Every summand is nonnegative.  Therefore `N(c)>0` supplies an integer
`c+t` with `|t|<h` satisfying every actual 451 residue condition.  Fourier
inversion on each local prime and (5) give the exact identity

\[
 N(c)={1\over P}\sum_{a}
 W_h\left({A(a)\over P}\right)e_P(A(a)c)\prod_iT_i(a_i).
                                                                    \tag{9}
\]

The zero word contributes exactly `h/P`.  Consequently the following is a
rigorous sufficient condition, with no continuous reconstruction step:

> **Discrete joint spectral lemma (open).**  If
> \[
> \boxed{\quad
> \sum_{a\ne0}W_h\left({A(a)\over P}\right)
>                    \prod_i|T_i(a_i)|<h,
> \quad}                                                     \tag{10}
> \]
> then `N(c)>0` for every integer center `c`.

The phase at a particular center could only improve (10); taking absolute
values makes this an all-center sufficient strengthening.

## 3. Consequence for Erdos 451

Take `c=k+h` in (8).  A positive term has

\[
                    k<c+t<k+2h,                            \tag{11}
\]

up to the harmless open endpoints.  With the coordinate
`n=s+k+1` used in the campaign, this gives

\[
                         2k<n<2k+2h+1.                     \tag{12}
\]

Thus a proof of (10) at

\[
       h=k^{O(1)}C^m\prod_{k<p<2k}{p\over p-k}             \tag{13}
\]

for one fixed `C` would directly yield `n_k=exp(o(k))` by the already
audited exponent ledger.  No block merger is needed because (8) contains
all primes simultaneously.

## 4. Exact remaining difficulty

Equation (10) is not proved here.  It replaces the compact small-lift word
sum by a full frequency sum with products of two normalized Dirichlet
kernels.  Its advantages are exact integer time, exact one-sided allowed
support, and a nondegenerate `d_i=1` coordinate.  Its cost is that the local
Fourier support is no longer compact, so the high-support joint CRT phase
problem remains rather than disappearing.

The next proof attempt should keep the coupled frequency `A(a)` in (7)--
(10).  Separating the local Dirichlet masses or discarding complementary
coordinates recreates the constant-exponential/high-support losses already
audited in rounds 2--3.

## 5. Exact removal of the width-one prime

The exceptional coordinate `d_0=1`, when present, has `p_0=k+1` and
`T_0(a)=1` for every frequency.  Unlike the continuous majorant, it can be
removed exactly here.  Choose `h=p_0H`.  Writing

\[
 D_M(x)=\sum_{u=0}^{M-1}e(xu),
 \qquad W_M(x)=M^{-1}|D_M(x)|^2,
\]

the factorization into `p_0` residue classes gives

\[
 D_{p_0H}(x)=D_{p_0}(x)D_H(p_0x).                          \tag{14}
\]

For any real `alpha`, finite Parseval on the `p_0` equally spaced shifts
gives

\[
 \sum_{a_0\bmod p_0}|D_{p_0}(\alpha+a_0/p_0)|^2=p_0^2.
                                                                    \tag{15}
\]

Combining (14)--(15),

\[
 \sum_{a_0\bmod p_0}
 W_{p_0H}(\alpha+a_0/p_0)=p_0W_H(p_0\alpha).               \tag{16}
\]

For the all-zero remaining word, the left side of (16) is exactly `h`,
entirely from `a_0=0`; hence removing the global zero word removes this
whole term.  For every nonzero remaining word, summing its `a_0` fibre in
(10) and using (16) turns (10) exactly into

\[
 \sum_{a'\ne0}W_H\left({p_0A'(a')\over P'}\right)
                    \prod_{i\ne0}|T_i(a_i)|<H,             \tag{17}
\]

where `P'=P/p_0` and `A'(a')=sum_(i ne 0)a_iP'/p_i`.
Multiplication by `p_0` is invertible modulo `P'`; it is a genuine joint
dilation, not a loss of frequencies.  Thus the width-one coordinate costs
only the polynomial factor `p_0=O(k)` in the physical window and leaves a
same-form discrete joint spectral problem on the other primes.  This is the
exact-carry/dilate-aware reduction that the continuous bridge lacked.

## 6. A fixed-exponential arc-dispersion lemma would close

Put

\[
 w(A(a))=\prod_i|T_i(a_i)|,
 \qquad L=\sum_{A\bmod P}w(A)=\prod_i\sum_{a_i}|T_i(a_i)|. \tag{18}
\]

Parseval and Cauchy--Schwarz in one coordinate give the exact useful ledger

\[
 \sum_{a_i\bmod p_i}|T_i(a_i)|
 \le {p_i\over\sqrt{r_is_i}}
 \le {2p_i\over d_i},
 \qquad L\le2^m{P\over D}.                                \tag{19}
\]

The first inequality uses
`sum_a |F lambda_r(a)|^2=p_i/r`.  The second follows from the balanced
choice (3).

For `0<X<=P/2`, define the centered arc mass

\[
                 M(X)=\sum_{0<|A|_P\le X}w(A).             \tag{20}
\]

The following fixed-exponential discrepancy estimate is sufficient:

> **Joint arc-dispersion lemma (open).**  There is an absolute `K` such
> that, uniformly for all relevant systems and all `P/h<=X<=P/2`,
> \[
>                     M(X)\le K^m{X\over P}L.              \tag{21}
> \]
> If the width-one coordinate was removed, the same estimate is additionally
> required for the one specific dilation `A -> p_0A (mod P')` in (17).

Indeed

\[
 {W_h(A/P)\over h}\ll
       \min\left\{1,\left({P\over h|A|_P}\right)^2\right\}. \tag{22}
\]

Apply (21) first at `X=P/h` and then on doubling arcs.  Partial summation,
or the direct dyadic bound, gives

\[
 {1\over h}\sum_{A\ne0}W_h(A/P)w(A)
       \ll K^m{L\over h}.                                  \tag{23}
\]

At `h=k^B C^mP/D`, (19) makes the right side at most
`k^{-B} O(2K/C)^m`.  Choosing one fixed `C` larger than the implied
constant times `2K` proves (10), while `log h=o(k)` remains unchanged.

Thus (21), rather than a pointwise inverse-cofactor estimate, is a clean
current decisive lemma.  It allows a constant loss per prime and asks only
for arc scales at least `P/h`.  The exceptional-prime case requires the
particular dilation by `p_0` proved in section 5; no uniform claim over all
units is intended.  Such a uniform claim would generally be false, since a
unit can move a selected high-weight nonzero frequency next to zero.  No
proof of (21), even for the two required undilated/specially dilated cases,
is claimed in this round.
