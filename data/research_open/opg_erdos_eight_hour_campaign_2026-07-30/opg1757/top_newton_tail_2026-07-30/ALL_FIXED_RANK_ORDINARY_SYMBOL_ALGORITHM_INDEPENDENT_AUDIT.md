# Independent audit of the all-fixed-rank ordinary-symbol algorithm

Date: 2026-07-30

## Verdict

\[
\boxed{\text{PASS AFTER A MINOR EXPLICITNESS REPAIR}}
\]

The fixed-\(R\) algorithm, exceptional rank shift, determinant loss
marker, central-moment indexing, \(N_L(k)\) powers, division by
\(2k(k-1)\), and resource bounds are consistent.  No off-by-one error
was found.

The audited draft said that a binomial cumulant recurrence computed the
constants \(\mu_{m,q}\), but did not state that recurrence.  The revised
theorem now includes the exact finite factorial-moment formula
\[
\mathbb E\delta^m
=
k^{-m}\sum_{u=0}^{m}\binom mu(-k/2)^{m-u}
\sum_{v=0}^{u}{u\brace v}(k)_{\underline v}2^{-v}.
\]
It also makes the convention \(\mu_{0,q}=0\) for \(q>0\) explicit.
This was an auditability gap, not a false formula.

The revision additionally records the new theorem-level rank-three
consequence \(H_5,B_3,\beta_{d,3}\).  The independent verifier imports
no existing OPG verifier or stored rank-four/rank-five profile.

## 1. Arbitrary fixed profile rank

The exponential recurrence
\[
nE_n(z)
=\sum_{p=1}^{n}
p\,\frac{\phi_{p+2}}{(p+2)!}z^{p+2}E_{n-p}(z)
\]
is the coefficient recurrence for
\[
\exp\!\left(
\sum_{p\ge1}
\frac{\phi_{p+2}}{(p+2)!}z^{p+2}\varepsilon^p
\right).
\]
To obtain saddle rank \(r\), the amplitude/Gaussian sum uses
\(E_{2r-m}\), \(0\le m\le2r\).  Thus \(E_0,\ldots,E_{2r}\) and phase
derivatives only through \(2r+2\) are sufficient.

The Gamma logarithm at inverse rank \(r\) contains
\(B_{r+1}(c)\).  Exponentiating it by the displayed recurrence gives
all corrections through rank \(r\); no higher Bernoulli polynomial is
implicitly used.

For the exceptional profile, the exact Cauchy integral has leading
prefactor
\[
\frac{8x}{s\sqrt{1-2x}}.
\]
Therefore its saddle coefficient \(C_q(g_*,{\cal A}_*)\) contributes
to profile rank \(q+1\), exactly as
\[
F_{2,r}
=F^{\rm main}_{4,r}
+\frac{8x}{\sqrt{1-2x}}C_{r-1}(g_*,{\cal A}_*).
\]
The independent implementation retained this shift rather than
copying a stored rank-four formula.

Through loss \(10\), it checked all profile subdegrees at ranks
\(0,\ldots,5\):
\[
\sum_{h=0}^{2}\sum_{r=0}^{5}(10-r+1)=153
\]
exact identities against profiles reconstructed from the finite
Lagrange sums.  The six \(h=2\), rank-five checks explicitly include
the exceptional summand.

## 2. The \(t^n\) factor in \(G_n\)

The profile term of rank \(a\) is
\[
k^{-a}t^aF_{h,a}(tx).
\]
Multiplying ranks \(a\) and \(b\) with \(a+b=n\) necessarily gives the
factor \(k^{-n}t^n\).  The powers inside
\(F_{h,a}(tx)F_{h,b}(t(1-x))\) record the remaining profile loss.
Thus
\[
G_n=t^n\sum_{a+b=n}(\cdots)
\]
has the correct total-loss marker.  Omitting or doubling this factor
would already contradict the independently recovered \(H_2\).

The implementation also obtained
\[
G_0=0,\qquad G_1(1-x,t)=-G_1(x,t)
\]
symbolically, so the \(n=0,1\) expectation terms vanish for the stated
reasons.

## 3. Central moments and finiteness of \(H_n\)

For a determinant rank \(a\), the coefficient at total inverse rank
\(n\) uses the coefficient of \(k^{-(n-a)}\) in the central moment.
Hence
\[
H_n
=\sum_{a=2}^{n}
\sum_{\substack{m\le2(n-a)\\m\ {\rm even}}}
\frac{\mu_{m,n-a}}{m!}G_a^{(m)}(1/2,t).
\]
The upper bound on \(m\) follows from
\(\mu_{m,q}=0\) for \(m>2q\); it makes every \(H_n\) a finite
calculation.  For a fixed coefficient of \(t\), each \(G_a\) is a
polynomial in \(x\), so its Taylor expansion is finite as well.

The first nontrivial moments are
\[
\mathbb E\delta^2=\frac1{4k},
\qquad
\mathbb E\delta^4=\frac3{16k^2}-\frac1{8k^3},
\]
\[
\mathbb E\delta^6
=\frac{15}{64k^3}-\frac{15}{32k^4}+\frac1{4k^5}.
\]
Consequently the rank-five kernel must contain both fourth-moment
terms:
\[
\begin{aligned}
H_5={}&G_5+\frac18G_4''
+\frac1{128}G_3^{(4)}
-\frac1{192}G_2^{(4)}
+\frac1{3072}G_2^{(6)},
\end{aligned}
\]
all evaluated at \(x=1/2\).  The generic implementation reproduces
this formula.  It performed 18 central-moment support and symmetry
checks, including odd moments and \(\mu_{0,q>0}=0\).

## 4. \(N_L(k)\), denominator expansion, and \(B_r\)

A profile coefficient at total loss \(L\) has leading scaling \(k^L\).
Since \(H_n\) is the coefficient of \(k^{-n}\) in the normalized
expectation,
\[
N_L(k)
=\sum_{n\ge2}k^{L-n}[t^L]H_n(t)
\]
has the correct power.  Multiplication by
\[
\frac1{2k(k-1)}
=\frac1{2k^2}\sum_{q\ge0}k^{-q}
\]
shows that \(k^{d-r}\), with \(L=d+4\), occurs precisely when
\[
L-n-2-q=d-r,
\qquad\text{i.e.}\qquad n+q=r+2.
\]
Summing \(q\ge0\) gives
\[
\beta_{d,r}
=\frac12[t^{d+4}]
\sum_{n=2}^{r+2}H_n(t),
\]
and therefore
\[
B_r(t)
=\frac1{2t^4}\sum_{n=2}^{r+2}H_n(t).
\]
The apparent coefficients below \(t^r\) cancel because
\(b_{k,d}\) is a polynomial of degree at most \(d\).  The revised
theorem now states this explicitly.

## 5. Independent rank-five and rank-three results

The new independent calculation gives
\[
\begin{aligned}
H_5(t)
=-\frac{t^6}{3240(1-t)^{10}}\bigl(&
825719t^{10}-7431471t^9+29112669t^8\\
&-64490751t^7+87663474t^6-74537550t^5\\
&+40641750t^4-17199000t^3+8377560t^2\\
&+1202040t+272160\bigr).
\end{aligned}
\]
It then verifies the rational identity
\[
B_3(t)=\frac{H_2+H_3+H_4+H_5}{2t^4}
\]
and the degree-nine formula for \(\beta_{d,3}\) printed in the revised
theorem.  For \(0\le d\le8\), 30 exact symbols with
\(0\le r\le\min(3,d)\) agree with complete \(b_{k,d}\) polynomials
reconstructed independently from the source profiles.  The six
rank-three comparisons are
\[
\begin{array}{c|rrrrrr}
d&3&4&5&6&7&8\\ \hline
\beta_{d,3}
&-327&-12583/3&-77125/3&-1337281/12
&-4604819/12&-134436031/120.
\end{array}
\]
Each exact polynomial uses two interpolation-external values of \(k\).

## 6. Resource bounds and claim boundary

To compute \(B_0,\ldots,B_R\), the largest required \(H_n\) is
\(H_{R+2}\), so the largest profile rank is
\[
M=R+2.
\]
The main saddle therefore needs phase derivatives through
\[
2M+2=2R+6.
\]
Its Gamma correction needs logarithmic ranks through \(M\), whose
largest Bernoulli-polynomial index is
\[
M+1=R+3.
\]
The exceptional profile starts one rank later and requires no larger
resource.  These are valid upper bounds for every fixed \(R\), not
uniform estimates in \(R\).

Accordingly the all-fixed-rank theorem passes.  It proves finite
computability at each fixed rank, but supplies no uniform-in-\(R\)
coefficient bound and does not prove the weighted \(C=3\) conjecture
or the cubic top window.
