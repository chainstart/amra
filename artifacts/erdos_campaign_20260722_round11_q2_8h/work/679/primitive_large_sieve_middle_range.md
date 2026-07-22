# #679: the primitive large sieve removes every fixed polynomial conductor range

Date: 2026-07-22

This note uses the primitive Fourier support from round 10 together with the
fixed-moment variance ledger. It gives a deterministic estimate for the
previously unresolved ANOVA terms whose full conductor is between the new
Rankin cutoff and any prescribed fixed power of the interval length. It does
not estimate the aggregate beyond the prescribed polynomial cutoff.

## 1. Local variance mass

Use the notation of `rankin_conductor_mass_improvement.md`. Thus

\[
 H=\lfloor L_1^2\rfloor,\qquad z=\exp(L_1/L_2),
 \qquad b=1-(1-a)^q,
\]

where \(q\) and \(C\) are fixed, and

\[
 W(n)^q=\mu_q\prod_{H<p\le z}(1+\delta_p(n)),
 \qquad \delta_p=d_p/m_p .                            \tag{1}
\]

Put

\[
 v_p={\mathbb E_p d_p^2\over m_p^2}.
\]

Since \(m_p=1-bH/p=1-o(1)\), \(b\le qa\), and

\[
 \mathbb E_p d_p^2=b^2{H\over p}\left(1-{H\over p}\right),
\]

we have, uniformly in the prime band,

\[
 v_p\le {2b^2H\over p},\qquad
 V:=\sum_{H<p\le z}v_p=O_{q,C}(1/L_2).                \tag{2}
\]

If \(c(T)=\prod_{p\in T}p>D\), then \(c(T)\le z^{|T|}\)
forces

\[
 |T|\ge r:=\left\lfloor{\log D\over\log z}\right\rfloor+1.
                                                                    \tag{3}
\]

For the Rankin cutoff \(D=N z^{-B}\), where \(B\) is fixed and
\(N\asymp X\), this is

\[
 r=L_2-B+O(1).                                        \tag{4}
\]

The elementary-symmetric estimate therefore gives

\[
 \begin{aligned}
 \sum_{c(T)>D}\prod_{p\in T}v_p
 &\le \sum_{j\ge r}{V^j\over j!}\\
 &\le \exp\{-(2+o_{q,C}(1))L_2L_3\}.                 \tag{5}
 \end{aligned}
\]

Indeed \(V=O(1/L_2)\), \(r=(1+o(1))L_2\), and Stirling gives
\(r\log(r/V)=(2+o(1))L_2L_3\). The tail after its first term is
geometrically decreasing for large \(X\).

## 2. Primitive fractions do not collide

For \(T\ne\varnothing\), let

\[
 F_T(n)=\mu_q\prod_{p\in T}\delta_p(n).
\]

It has period \(c(T)\). The round-10 local Fourier calculation shows that
every nonzero coefficient is supported on a primitive frequency
\(u/c(T)\), \((u,c(T))=1\). Hence two Fourier frequencies arising from
different conductors cannot be the same rational number: equality of two
reduced fractions forces equality of their denominators.

Local Parseval and CRT orthogonality give the exact energy identity

\[
 \sum_{u\bmod c(T)}^{*}|\widehat F_T(u)|^2
 ={1\over c(T)}\sum_{n\bmod c(T)}|F_T(n)|^2
 =\mu_q^2\prod_{p\in T}v_p.                           \tag{6}
\]

## 3. A deterministic middle-conductor theorem

Fix a constant \(A\ge1\), and define

\[
 {\cal M}_{D,A}(n)=
 \sum_{D<c(T)\le X^A}F_T(n).                         \tag{7}
\]

All reduced fractions in the Fourier expansion of (7) have denominators at
most \(X^A\), so distinct ones are separated by at least \(X^{-2A}\).
The classical large sieve for additive characters, followed by (5)--(6),
therefore yields for every interval \(I\) of \(N\asymp X\) consecutive
integers

\[
 \begin{aligned}
 \sum_{n\in I}|{\cal M}_{D,A}(n)|^2
 &\le (N-1+X^{2A})
       \sum_{D<c(T)\le X^A}\sum_u^*|\widehat F_T(u)|^2\\
 &\le X^{2A+o(1)}\mu_q^2
       \exp\{-(2+o(1))L_2L_3\}.                     \tag{8}
 \end{aligned}
\]

One final Cauchy inequality in the physical interval gives

\[
 \boxed{
 \left|\sum_{n\in I}{\cal M}_{D,A}(n)\right|
 \le X^{A+1/2-qC+o(1)}
       \exp\{-(1+o(1))L_2L_3\}.}                    \tag{9}
\]

Here \(\mu_q=X^{-qC+o(1)}\). In particular, if

\[
 qC>A+{1\over2}+\delta,                              \tag{10}
\]

then (9) is \(O(X^{-\delta/2})\), after harmlessly shrinking the fixed
margin for sufficiently large \(X\).

The theorem is uniform in the actual start of \(I\); it uses no averaging
over the full CRT period. For example, any fixed \(C>1\), \(q=2\), and
\(A=1\) give a fixed-power estimate for the whole range

\[
 Nz^{-B}<c(T)\le X.                                  \tag{11}
\]

## 4. Exact remaining boundary

Combining the new Rankin transfer with (9) removes

* all conductors \(c(T)\le D=Nz^{-B}\), by incomplete-period transfer;
* every prescribed fixed-polynomial range \(D<c(T)\le X^A\), after choosing
  a fixed moment with (10).

What is not controlled is

\[
 \boxed{{\cal U}_A(n)=\sum_{c(T)>X^A}F_T(n).}         \tag{12}
\]

The Farey spacing constant for (12) is no longer a fixed power of \(X\),
and an energy-only sum over all such denominators has the same extreme-layer
problem identified in round 8. Equation (5) is only an
\(\exp\{-\Theta(L_2L_3)\}\) variance saving, not a fixed power of \(X\), so
it cannot absorb an unrestricted denominator norm. Taking absolute values
in (12) is also invalid because arbitrary CRT phases can make the
high-conductor aggregate order one.

The quantifiers are important: (A) is prescribed first and the fixed
moment (q) may then be chosen using (10). This does not give simultaneous
control for all (A) from one moment.

Strict status: **new deterministic fixed-polynomial middle-range theorem;
the signed aggregate beyond the chosen cutoff and Erdős #679 remain open**.
