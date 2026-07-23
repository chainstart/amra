# #679: entropy-optimised moving conductor cutoff

Date: 2026-07-23

This note strengthens the fixed-\(\eta\) cutoff from round 11.  It is an
unconditional reduction at the prescribed physical interval, not a proof or
disproof of Erdős #679.

## 1. Parameters and the exact candidate ratio

Fix the original \(\varepsilon>0\) and a fixed real \(d\ge1\).  Put

\[
 L_j=\log_jX,\qquad H=\lfloor L_1^d\rfloor,
 \qquad z=\exp(L_1/L_2),
 \qquad L=\sum_{H<p\le z}{1\over p}.
\]

Use the consecutive shifts

\[
 k_j=H+j\qquad(0\le j<H).
\]

For an integer-valued formulation of the strict target, let

\[
 r_\varepsilon(k)=
 \left\lceil(1+\varepsilon){\log k\over\log\log k}\right\rceil-1,
 \qquad
 R=\sum_{j<H}r_\varepsilon(k_j),
 \qquad
 \rho={R\over HL}.                                  \tag{1}
\]

The prime number theorem and Mertens' theorem give

\[
 L=L_2-2L_3-\log d+o(1),
 \qquad
 \rho={(1+\varepsilon)d+o(1)\over L_3}.             \tag{2}
\]

In particular \(0<\rho<1\) for all sufficiently large \(X\).  Defining
\(\rho\) by (1), rather than replacing it by its asymptotic expression, is
important: every candidate has the exact incidence bound used below, with
no hidden rounding or \(\varepsilon\)-loss.

For \(p\in(H,z]\), let \(X_p(n)\) indicate that \(p\) divides one of
\(n-k_j\), \(0\le j<H\), and put

\[
 T(n)=\sum_{H<p\le z}X_p(n),
 \qquad
 V(n)=\rho^{T(n)}.                                  \tag{3}
\]

Since \(p>H\), a prime hits at most one of the \(H\) shifts.  If \(n\) is
an original #679 candidate and \(H\) is beyond its fixed
\(K_\varepsilon\), then

\[
 T(n)\le\sum_{j<H}\omega(n-k_j)\le R,
 \qquad V(n)\ge\rho^R.                              \tag{4}
\]

## 2. Complete moments and ANOVA energy

Write \(b=1-\rho\).  Over the complete CRT period, the exact first and
second moments are

\[
 \mu=\mathbb E V
 =\prod_{H<p\le z}\left(1-{bH\over p}\right),
 \qquad
 M_2=\mathbb E V^2
 =\prod_{H<p\le z}\left(1-{(1-\rho^2)H\over p}\right).       \tag{5}
\]

The dangerous segment \(H<p<2H\) is treated without a uniform Taylor
expansion.  It has \(O(H/\log H)\) primes, every factor in (5) is at least
\(1-H/p\ge(2H)^{-1}\), and hence its total possible logarithmic error is
\(O(H)\).  On \(p\ge2H\), Taylor's formula and
\(H^2\sum_{p\ge2H}p^{-2}=O(H)\) give, uniformly as \(\rho\to0\),

\[
 \log\mu=-bHL+O(H),
 \qquad
 \log M_2=-(1-\rho^2)HL+O(H).                       \tag{6}
\]

Expand \(V=\sum_TF_T\) in its local mean-zero ANOVA components.  After
normalising the exact Parseval energies by \(M_2\), the random subset
\(T\) has independent Bernoulli coordinates

\[
 \theta_p={b^2x_p(1-x_p)\over1-(1-\rho^2)x_p},
 \qquad x_p={H\over p}.                             \tag{7}
\]

For \(p\ge2H\),

\[
 \theta_p=b^2x_p+O(\rho^2x_p^2),
\]

while the whole lower segment contributes \(O(H/\log H)\).  Consequently

\[
 \Lambda:=\sum_p\theta_p=b^2HL+O(H).                \tag{8}
\]

All constants in (6)--(8) are uniform for the present
\(\rho\asymp1/L_3\).

## 3. A moving cutoff approaching coefficient one

Let

\[
 I(u)=1-u+u\log u,
 \qquad
 \Delta={1\over L_3},
 \qquad
 \sigma=I(\rho)-\Delta,
 \qquad
 \mathcal C_X=\exp(\sigma HL).                      \tag{9}
\]

For large \(X\), \(\sigma>0\).  If \(c(T)=\prod_{p\in T}p\le\mathcal C_X\),
then

\[
 |T|\le r_0={\sigma HL\over\log H}=O_d(H).
\]

The exponential Markov bound for the Poisson-binomial variable \(|T|\)
gives

\[
 \mathbb P(|T|\le r_0)
 \le\exp\{-\Lambda+r_0+r_0\log(\Lambda/r_0)\}
 \le\exp\{-b^2HL+O_d(HL_3)\}.                      \tag{10}
\]

Multiplying (10) by (6) yields the conductor-localised Fourier energy

\[
 \boxed{
 \sum_{c(T)\le\mathcal C_X}\sum_u^*
 |\widehat F_T(u)|^2
 \le\exp\{-2bHL+O_d(HL_3)\}.}                      \tag{11}
\]

The empty component may be retained in (11); it is separated below when
summing in physical space.  Local mean zero makes every non-empty
frequency primitive, and distinct squarefree conductors give distinct
reduced fractions.

For every prescribed interval \(J\) of \(N\asymp X\) consecutive
integers, the additive large sieve, (11), and physical Cauchy give

\[
 \begin{aligned}
 \left|\sum_{n\in J}\sum_{1<c(T)\le\mathcal C_X}F_T(n)\right|
 &\le N^{1/2}(N-1+\mathcal C_X^2)^{1/2}
       \exp\{-bHL+O_d(HL_3)\}\\
 &\le
 \exp\{-(\rho\log(1/\rho)+\Delta-o(\Delta))HL\}.  \tag{12}
 \end{aligned}
\]

The last line uses the exact identity

\[
 b-I(\rho)=\rho\log(1/\rho),                        \tag{13}
\]

as well as

\[
 \log N+HL_3=o(\Delta HL).
\]

The latter uniformity check is valid even at \(d=1\): then
\(HL\asymp L_1L_2\), so both ratios are
\(O(L_3/L_2)\) or smaller.  This explicitly verifies that the moving
\(\rho\to0\) does not consume the \(HL/L_3\) safety margin.

## 4. What a genuine candidate now forces

The zero component on \(J\) is

\[
 N\mu=\exp\{-bHL+o(HL)\}
      =o(\rho^R),                                   \tag{14}
\]

because \(R=\rho HL\) exactly and

\[
 b-\rho\log(1/\rho)=I(\rho)>0.
\]

If \(J\) contains an original candidate, non-negativity and (4) give
\(\sum_{n\in J}V(n)\ge\rho^R\).  Splitting the exact ANOVA identity into
the zero component, (12), and its complement therefore proves

\[
 \boxed{
 \sum_{n\in J}\sum_{c(T)>\mathcal C_X}F_T(n)
 \ge(1-o(1))\rho^R
 =\exp\{-(1+o(1))\rho\log(1/\rho)HL\}>0.}           \tag{15}
\]

Thus the fixed round-11 threshold
\(\exp((1-\eta)HL)\), where \(\eta>0\) had to be fixed first, improves to

\[
 \boxed{
 \log\mathcal C_X=
 \left[1-{(1+\varepsilon)d\over L_3}
 \left(1+\log{L_3\over(1+\varepsilon)d}\right)
 -{1+o(1)\over L_3}\right]HL.}                    \tag{16}
\]

In particular the coefficient is \(1-O_{d,\varepsilon}(L_4/L_3)\), which
tends to one.  The choice \(V=\rho^T\) is the entropy optimiser: for a
general local hit value \(y\), the available exponent is
\(1-y+\rho\log y\), maximised at \(y=\rho\), with value \(I(\rho)\).

## 5. Strict boundary

Equation (15) is a stronger necessary condition for a candidate, not an
upper bound for the complementary signed sum.  Most normalised Fourier
energy still lies much farther out, around

\[
 \log c(T)\asymp H\log z,
 \qquad {H\log z\over HL}\asymp{L_1\over L_2^2}\to\infty.
\]

No argument here controls the signed tail in (15) at the actual start.
Consequently the original first question remains open and the closure
count is zero.

