# OPG-1757: complementary finite-sum endpoint-localization lemma

Date: 2026-07-30

## 0. Purpose

This note proves the missing \(x=1\) endpoint statement for the
normalized ordinary profiles.  It does not use finite-rank
interpolation.  The essential point is that the normalized Lagrange
sum has an exact symmetry in the edge count and its complement.  That
symmetry gives a second Cauchy integral in which the saddle
corresponding to the original \(y=2x\) saddle is \(v=1\), not
\(v=2(1-x)\).  The former remains regular and nondegenerate at
\(x=1\).

Throughout, \(n_{\underline i}=n(n-1)\cdots(n-i+1)\), and
\[
q=1-x,\qquad W=1-2x=2q-1.
\]

## 1. Exact complementary finite sum

For nonnegative integers \(J,Q\), define
\[
 {\mathcal S}_s(J,Q)
 =
 \sum_{i\geq0}
 \frac{J_{\underline i}Q_{\underline i}}{i!}
 \left(-\frac1{2s}\right)^i .
\tag{1}
\]
The sum terminates at \(\min(J,Q)\), and hence
\[
 {\mathcal S}_s(J,Q)={\mathcal S}_s(Q,J).
\tag{2}
\]
More usefully, the symmetry has the exact coefficient realization
\[
 \boxed{
 \frac{{\mathcal S}_s(J,Q)}{Q!}
 =
 [u^Q]\,e^u\left(1-\frac{u}{2s}\right)^J .
 }
\tag{3}
\]
Indeed, expanding the two factors on the right gives
\[
 Q!\sum_{i=0}^Q
 \frac{J_{\underline i}}{i!}
 \left(-\frac1{2s}\right)^i
 \frac1{(Q-i)!}
 =
 {\mathcal S}_s(J,Q).
\]
Thus (3), unlike a reversal of an index-\(J\) sum, is a genuine
length-\(Q\) complementary identity.

Let
\[
 E(s,c,J)=
 \sum_{i=0}^J
 \frac{(-1)^i c_{\underline i}s^{J-i}}
 {2^i i!(J-i)!},
 \qquad
 D(s,c,J)=E(s,c,J)-E(s,c,J-1).
\tag{4}
\]
Multiplication by the standard normalization gives
\[
 \frac{2^J J!}{s^J}E(s,Q,J)
 =2^J{\mathcal S}_s(J,Q)
\tag{5}
\]
and
\[
 \frac{2^J J!}{s^J}D(s,Q,J)
 =
 2^J\left\{
 {\mathcal S}_s(J,Q)
 -\frac Js{\mathcal S}_s(J-1,Q)
 \right\}.
\tag{6}
\]

Fix \(a\in\{0,2,4\}\), put
\[
 J=xs,\qquad Q=s-a-J=qs-a,
\tag{7}
\]
and consider the normalized main profile
\[
 \Phi_a^{\rm main}(s,x)
 =
 \frac{2^J J!}{s^{2J}}
 (s-a)_{\underline J}D(s,Q,J).
\tag{8}
\]
Using (3) separately in the two terms in braces in (6), and using
\(s-J=Q+a\), gives the exact identity
\[
\begin{aligned}
 &\frac1{Q!}
 \left\{
 {\mathcal S}_s(J,Q)
 -\frac Js{\mathcal S}_s(J-1,Q)
 \right\}\\
 &\qquad =
 \frac1s[u^Q]\,
 e^u\left(1-\frac{u}{2s}\right)^{J-1}
 \left(Q+a-\frac u2\right).
\end{aligned}
\tag{9}
\]
Since
\[
 \frac{(s-a)_{\underline J}}{s^J}
 =\frac{\Gamma(s-a+1)}{\Gamma(Q+1)s^J},
\]
the \(Q!\) in (9) cancels the complementary Gamma denominator.
After \(u=sv\), (8) becomes
\[
\boxed{
\begin{aligned}
 \Phi_a^{\rm main}(s,x)
 ={}&
 \Gamma(s-a+1)\,2^{xs}s^{a-s}\\
 &\times\frac1{2\pi i}\oint
 \widetilde g_a(v;q)e^{s\psi_q(v)}\,dv,
\end{aligned}}
\tag{10}
\]
where
\[
\boxed{
\begin{aligned}
 \psi_q(v)
 &=v+x\log(1-v/2)-q\log v,\\
 \widetilde g_a(v;q)
 &=\frac{v^{a-1}(q-v/2)}{1-v/2}.
\end{aligned}}
\tag{11}
\]
Equations (9)--(11) are exact whenever the integer parameters in
(7) are nonnegative.  No asymptotic cancellation has yet been used.

## 2. Which complementary saddle represents the original branch?

The stationary equation for (11) factors as
\[
 \psi_q'(v)
 =
 -\frac{(v-1)(v-2q)}
 {2v(1-v/2)}.
\tag{12}
\]
Thus the complementary representation has saddles \(v=1\) and
\(v=2q\).  The saddle corresponding to the original \(y=2x\) branch
is \(v=1\).

Here is a direct, nonformal way to identify it.  Take
\(0<x<1/2\), so \(q>1/2\), and let \(s\) run through sufficiently
large multiples of the denominator of \(x\).  On the coefficient
circle \(v=e^{i\theta}\),
\[
 \frac{d}{d\theta}\Re\psi_q(e^{i\theta})
 =
 \sin\theta
 \left(
 -1+\frac{2x}{5-4\cos\theta}
 \right)<0
\quad(0<\theta<\pi).
\tag{13}
\]
The inequality follows from \(2x<1<5-4\cos\theta\).  Hence \(v=1\)
is the unique maximum on \(|v|=1\), while the second saddle
\(v=2q\) lies strictly outside that circle.

On the same interval \(0<x<1/2\), the original exact Cauchy
representation has \(y=2x\) as its unique contributing saddle on
\(|y|=2x\).  Both integrals represent the same exact quantity (8).
Fix a rational \(x\) in this interval and let \(s\) tend to infinity
through multiples of its denominator.  The strict maximum in (13)
makes the part of the contour outside a fixed neighbourhood of
\(v=1\) exponentially smaller; the analogous statement holds at
\(y=2x\).  After the common exponential and power of \(s\) are
removed, uniqueness of a Poincare expansion forces equality
coefficient by coefficient at this \(x\).  After their displayed
square-root factors are removed, both saddle recurrences have
rational-function coefficients in \(x\).  Equality on the dense set
of rational points in \((0,1/2)\) is therefore equality as rational
functions of \(x\).

This argument is deliberately different from replacing
\(i\) by \(J-i\): the actual change from length \(J\) to length \(Q\)
is equation (3), and (13) identifies the required saddle branch.

## 3. Regularity at \(x=1\)

At the complementary saddle,
\[
 \psi_q(1)=1-x\log2,
\qquad
 \psi_q''(1)=2q-1=W.
\tag{14}
\]
The exponential \(e^{s\psi_q(1)}\) cancels
\(2^{xs}e^{-s}\) from the prefactor in (10).  Stirling's expansion of
\[
 \Gamma(s-a+1)s^{a-s}e^s
\tag{15}
\]
has the more explicit form
\[
\Gamma(s-a+1)s^{a-s}e^s
=\sqrt{2\pi s}
\left(1+\sum_{j\ge1}\gamma_{a,j}s^{-j}\right),
\tag{15a}
\]
where the coefficients \(\gamma_{a,j}\) depend only on \(a\).

All derivatives at \(v=1\) of \(\psi_q\) and
\(\widetilde g_a(v;q)\) are polynomial in \(q\) with rational
coefficients: the only local denominators are powers of \(v\) and
\(1-v/2\), both units at \(v=1\).  The stationary-phase recurrence
uses only these jets and inverse powers of the Hessian \(W\).
Because
\[
 W\big|_{q=0}=-1,
\tag{16}
\]
every coefficient in the \(v=1\) saddle expansion is regular at
\(q=0\).  The leading Gaussian factor is the same
\(\sqrt W\) fixed by matching on \(0<x<1/2\).  Concretely, the
angular Hessian is \(-W\), while
\(\widetilde g_a(1;q)=W\); hence the local integral in (10), after
removing \(e^{s\psi_q(1)}\), starts with
\(\sqrt W/\sqrt{2\pi s}\).  The prefactor in (10), after the
exponential cancellation, starts with \(\sqrt{2\pi s}\).
Consequently, if
\[
 \Phi_a^{\rm main}(s,x)
 \sim
 \sqrt W\sum_{r\geq0}C_{a,r}^{\rm main}(x)s^{-r}
\tag{17}
\]
denotes the original rational branch, then
\[
 \boxed{
 C_{a,r}^{\rm main}(x)\text{ is regular at }x=1
 \quad(a=0,2,4,\ r\geq0).
 }
\tag{18}
\]
For \(a=0\), the factor \(v^{a-1}=v^{-1}\) is harmless because the
local expansion is at the unit \(v=1\).  At \(q=0\) this is an
analytic continuation statement about the rational Poincare
coefficients; it does not assert that the finite parameter
\(Q=qs-a\) remains nonnegative there.

## 4. Exceptional \(h=2\) profile

The exceptional contribution is
\[
 \Phi^{\rm ex}(s,x)
 =
 \frac{8J}{s^2}
 \frac{(s-4)_{\underline{J-1}}}{s^{J-1}}
 \frac{2^{J-1}(J-1)!}{s^{J-1}}
 E(s,s-J-3,J-1).
\tag{19}
\]
Put
\[
 L=J-1,\qquad P=s-J-3=qs-3.
\tag{20}
\]
Then \(L+P=s-4\).  Applying (3) with \((J,Q)=(L,P)\)
gives, again exactly,
\[
\boxed{
\begin{aligned}
 \Phi^{\rm ex}(s,x)
 ={}&
 \frac{4x}{s}\Gamma(s-3)\,2^{xs}s^{4-s}\\
 &\times\frac1{2\pi i}\oint
 \widetilde g_*(v)e^{s\psi_q(v)}\,dv,
 \qquad
 \widetilde g_*(v)=\frac{v^2}{1-v/2}.
\end{aligned}}
\tag{21}
\]
The phase is exactly the phase in (11).  The factor \(s^{-1}\) in
(21) is the exceptional rank shift.  The amplitude
\(\widetilde g_*\) and all its derivatives are regular at \(v=1\);
the remaining prefactor depends on \(q\) only through the regular
factor \(x=1-q\).  The saddle-selection argument (13) and the
endpoint argument (14)--(16) therefore apply unchanged.  Hence every
exceptional coefficient is regular at \(x=1\).  More explicitly, its
amplitude value is \(\widetilde g_*(1)=2\).  Formula (15a) with
\(a=4\), together with the explicit \(4x/s\) in (21), gives leading
term \(8x/(s\sqrt W)\).  Thus after division of the full profile by
\(\sqrt W\), the exceptional block introduces \(8x/(sW)\), not a
factor \(q^{-1}\); \(W^{-1}\) is a unit at \(q=0\).

Combining (18) and (21) proves the promised endpoint statement:
\[
\boxed{
\text{For all }h\in\{0,1,2\}\text{ and }r\geq0,\qquad
\frac{F_{h,r}(x)}{\sqrt{1-2x}}
\text{ is regular at }x=1.
}
\tag{22}
\]

The proof is all-rank and uses only the exact finite Lagrange source,
the complementary identity (3), and ordinary one-saddle coefficient
uniqueness on the overlap \(0<x<1/2\).
