# #679: sharp energy witness in a narrow conductor band

Date: 2026-07-23

This note stress-tests the conductor-localised estimate in
`moving_cutoff_entropy_optimization.md`.  It proves that its exponential
energy loss is already attained in a narrow band immediately below any
cutoff of size \(\exp(\sigma HL)\), for fixed \(0<\sigma<2\).  Thus merely
splitting the low-conductor energy more finely cannot improve the leading
\(-2(1-\rho)HL\) exponent.  This is a method barrier, not a barrier to all
possible proofs of Erdős #679.

## 1. Setup

Retain the notation of the moving-cutoff note:

\[
 H=\lfloor(\log X)^d\rfloor,\quad
 L=\sum_{H<p\le z}{1\over p},\quad
 \rho={R\over HL},\quad b=1-\rho,
\]

and let \(\theta_p\) be the exact independent Bernoulli parameters of the
normalised ANOVA energy,

\[
 \theta_p={b^2x_p(1-x_p)\over1-(1-\rho^2)x_p},
 \qquad x_p={H\over p}.
\]

Fix \(0<\sigma<2\) and a constant \(A>4\sigma\).  Put

\[
 Y=AHL,
 \qquad {\cal B}=\{p:Y<p\le2Y\},
 \qquad M=|{\cal B}|,
 \qquad r=\left\lfloor{\sigma HL\over\log(2Y)}\right\rfloor.
                                                        \tag{1}
\]

For fixed \(d\), the prime number theorem gives

\[
 M=(1+o(1)){AHL\over\log Y}=(1+o(1)){AH\over d},
 \qquad r=(1+o(1)){\sigma H\over d}.                \tag{2}
\]

Hence \(r<M/2\) for large \(X\).  Also \(2Y<z\), so the block lies inside
the prime set used by the ANOVA expansion.

## 2. The band is immediately below the cutoff

If \(T\subseteq{\cal B}\) and \(|T|=r\), then

\[
 r\log Y\le\log c(T)\le r\log(2Y)\le\sigma HL.
\]

Since \(\log(2Y)-\log Y=\log2\), (1) also gives

\[
 \log c(T)\ge\sigma HL-O_d(H).                     \tag{3}
\]

Thus every such component has conductor in the narrow band

\[
 \exp\{\sigma HL-O_d(H)\}\le c(T)\le\exp(\sigma HL).
                                                               \tag{4}
\]

The width \(O(H)\) in logarithmic conductor is negligible compared with
\(HL\).

## 3. Normalised energy in that band

Let \({\mathbb P}_\theta\) denote the product Bernoulli law with parameters
\(\theta_p\).  Its empty-set probability is exactly

\[
 \prod_p(1-\theta_p)={\mu^2\over M_2}.
\]

The exact complete-moment asymptotics therefore give

\[
 \log\prod_p(1-\theta_p)
 =-b^2HL+O(H).                                      \tag{5}
\]

For \(p\in{\cal B}\), one has \(x_p\asymp_A1/L\).  Uniformly for large
\(X\),

\[
 {\theta_p\over1-\theta_p}\ge {c_A\over L}          \tag{6}
\]

with some fixed \(c_A>0\).  Consequently, the probability that all
coordinates outside \({\cal B}\) vanish and exactly \(r\) coordinates in
\({\cal B}\) equal one is

\[
 \begin{aligned}
 P_{\cal B,r}
 &=\prod_p(1-\theta_p)\,
   e_r\!\left({\theta_p\over1-\theta_p}:p\in{\cal B}\right)\\
 &\ge \exp\{-b^2HL+O(H)\}
       {M\choose r}\left({c_A\over L}\right)^r\\
 &\ge \exp\{-b^2HL-O_d(HL_3)\}.                    \tag{7}
 \end{aligned}
\]

Here \({M\choose r}\ge(M/r)^r\), and \(r=O_d(H)\).  Notice that the
cost \(HL_3\) of forcing \(r\asymp H\) successes in this block is
lower-order than \(HL\).

## 4. Unnormalised Fourier energy and consequence

Multiplying (7) by

\[
 M_2=\exp\{-(1-\rho^2)HL+O(H)\}

gives the lower bound

\[
 \boxed{
 \sum_{\substack{T\subseteq{\cal B},\ |T|=r}}
       \sum_u^*|\widehat F_T(u)|^2
 \ge \exp\{-2bHL-O_d(HL_3)\}.}                    \tag{8}
\]

Indeed \(b^2+(1-\rho^2)=2(1-\rho)=2b\).  By (4), all the energy in (8)
lies in a logarithmically narrow band immediately below
\(\exp(\sigma HL)\).

The upper bound from the moving-cutoff argument is

\[
 \sum_{c(T)\le\exp(\sigma HL)}\sum_u^*
 |\widehat F_T(u)|^2
 \le\exp\{-2bHL+O_d(HL_3)\}.
\]

Hence its leading \(HL\)-scale exponent is sharp, even after conductor
stratification.  Any improvement sufficient to control the complementary
tail must exploit additional cancellation, arithmetic spacing, or a
different representation; it cannot come from a stronger estimate for
the total ANOVA energy in low-conductor bands alone.

This result does not control the signed interval sum and therefore does
not close the original first question.
