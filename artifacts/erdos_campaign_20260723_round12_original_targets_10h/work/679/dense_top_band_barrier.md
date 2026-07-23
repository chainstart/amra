# #679: simultaneous energy-and-support saturation near the cutoff

Date: 2026-07-23

This note strengthens `sharp_near_cutoff_energy_witness.md`.  The earlier
witness used primes near \(HL\), and therefore involved only
\(\exp\{O(H)\}\) different conductors.  Here the primes are taken from the
top of the available range.  In one narrow conductor band, both the ANOVA
energy exponent and the raw primitive-frequency count simultaneously
saturate the two inputs of the pooled Farey argument.

This is a rigorous barrier for methods using only band energy plus raw
support size or generic Farey separation.  It does not rule out cancellation
from the actual Fourier coefficients and does not close Erdős #679.

## 1. A top-prime conductor band

Use the parameters

\[
 H=\lfloor(\log X)^d\rfloor,\qquad
 z=\exp\{L_1/L_2\},\qquad
 L=\sum_{H<p\le z}{1\over p},
\]

with fixed \(d\ge1\), and the optimised hit value
\(\rho=R/(HL)\), \(b=1-\rho\).  Fix a constant \(\sigma>0\), bounded away
from zero and infinity, and put

\[
 {\cal B}=\{p:z/2<p\le z\},\qquad
 M=|{\cal B}|,
 \qquad
 r=\left\lfloor{\sigma HL\over\log z}\right\rfloor. \tag{1}
\]

The prime number theorem and the definitions give

\[
 M=(1+o(1)){z\over2\log z},
 \qquad
 r=(\sigma+o(1)){HL L_2\over L_1},                 \tag{2}
\]

so \(r=M^{o(1)}\), in particular \(r<M/2\).  Every \(r\)-set
\(T\subseteq{\cal B}\) satisfies

\[
 \sigma HL-O_d(H)\le\log c(T)\le\sigma HL.         \tag{3}
\]

Indeed the upper bound follows from \(c(T)\le z^r\), and the lower bound
loses only \(r\log2+O(\log z)=O_d(H)\).  Thus the whole family lies in a
single logarithmically narrow band just below \(\exp(\sigma HL)\).

## 2. There are essentially as many conductors as the cutoff permits

Let

\[
 D_{{\cal B},r}={M\choose r}.
\]

Stirling's formula, (1), and \(\log M=\log z-\log\log z+O(1)\) give

\[
 \begin{aligned}
 \log D_{{\cal B},r}
 &=r\log(M/r)+O(r)\\
 &=\sigma HL-o_d(HL).                               \tag{4}
 \end{aligned}
\]

To check the error explicitly,

\[
 r\{\log\log z+\log r+O(1)\}
 \ll_d {HL L_2^2\over L_1}=o(HL).                  \tag{5}
\]

Distinct \(T\)'s have distinct squarefree conductors.  Moreover every local
nonzero Fourier coefficient is nonzero: for \(p>H\), the geometric sum
\(\sum_{j<H}e(hj/p)\) cannot vanish when \(h\not\equiv0\pmod p\), since
\(p\nmid H\).  Hence the exact number of primitive frequencies in this band
is

\[
 F_{{\cal B},r}=\sum_{\substack{T\subseteq{\cal B}\\|T|=r}}\varphi(c(T)).
\]

For \(p\in{\cal B}\), \(\prod_{p\in T}(1-1/p)=1-o(1)\).  Combining this
with (3)--(4) yields

\[
 \boxed{\log F_{{\cal B},r}=2\sigma HL-o_d(HL).}    \tag{6}
\]

Thus the raw support count has the same leading exponent as the generic
\({\cal C}^2\) Farey count for \({\cal C}=\exp(\sigma HL)\).  Mere support
sparsity cannot save a fixed proportion in the exponent.

This also shows that the minimum-spacing exponent itself is sharp for the
actual support.  If \(\delta_{{\cal B},r}\) is the least circular distance
between two distinct frequencies in this family, Farey separation and
pigeonhole give respectively

\[
 e^{-2\sigma HL}\le\delta_{{\cal B},r}
 \le F_{{\cal B},r}^{-1}
 =e^{-2\sigma HL+o_d(HL)}.                          \tag{6a}
\]

Thus one cannot gain \(e^{-\delta HL}\) merely by proving a better
minimum-spacing bound for these frequencies.

## 3. The same family carries the full low-tail energy exponent

Under normalised ANOVA energy, subset membership is independent with

\[
 \theta_p={b^2x_p(1-x_p)\over1-(1-\rho^2)x_p},
 \qquad x_p={H\over p}.
\]

Uniformly on \({\cal B}\),

\[
 {\theta_p\over1-\theta_p}\ge c{H\over z}           \tag{7}
\]

for an absolute \(c>0\) and all sufficiently large \(X\).  As in the
lower-band witness, the exact probability of the empty subset is

\[
 \prod_p(1-\theta_p)={\mu^2\over M_2}
 =\exp\{-b^2HL+O(H)\}.                              \tag{8}
\]

It follows that the probability of selecting exactly \(r\) primes from
\({\cal B}\) and no primes outside it is at least

\[
 \begin{aligned}
 P_{{\cal B},r}
 &\ge \exp\{-b^2HL+O(H)\}
       {M\choose r}\left(c{H\over z}\right)^r\\
 &\ge \exp\{-b^2HL-o_d(HL)\}.                      \tag{9}
 \end{aligned}
\]

For the last line, the additional logarithmic cost is

\[
 r\log{rz\over MH}=O_d(rL_3)=o(HL),                \tag{10}
\]

because \(M\asymp z/\log z\) and
\(r\log z/H\asymp L\asymp L_2\).

Since \(M_2=\exp\{-(1-\rho^2)HL+O(H)\}\), the actual,
unnormalised Fourier energy of this same family satisfies

\[
 \boxed{
 \sum_{\substack{T\subseteq{\cal B}\\|T|=r}}
       \sum_u^*|\widehat F_T(u)|^2
 \ge\exp\{-2bHL-o_d(HL)\}.}                        \tag{11}
\]

This matches the leading exponent of the general low-conductor upper
bound.

The energy is not hidden in an exponentially tiny part of the raw support.
Let \({\cal A}_{{\cal B},r}\) be the coefficient vector in (11), let
\(E=\sum_{a\in{\cal A}}|a|^2\), and put

\[
 P_{\rm eff}={E^2\over\sum_{a\in{\cal A}}|a|^4}
\]

for its inverse-participation (effective support) number.  The exact local
coefficient formula and \(|\sum_{j<H}e(hj/p)|\le H\) give, uniformly for
\(p\in{\cal B}\),

\[
 \max_{a\in{\cal A}}|a|^2
 \le \mu^2\left(O(H^2/z^2)\right)^r
 \le\exp\{-2bHL-2\sigma HL+o_d(HL)\}.               \tag{12}
\]

Since \(\sum|a|^4\le(\max|a|^2)E\), (6), (11), and (12)
show

\[
 \boxed{\log P_{\rm eff}=2\sigma HL+o_d(HL).}       \tag{13}
\]

The upper bound here is simply \(P_{\rm eff}\le F_{{\cal B},r}\).
Thus, on the exponential scale, the energy occupies the full primitive
support rather than a sparse exceptional collection of coefficients.

## 4. Exact scope of the barrier

Equations (3), (6), and (11) hold simultaneously in one narrow conductor
band.  Consequently neither of the following can by itself improve the
pooled argument by \(\exp\{-\delta HL\}\) for fixed \(\delta>0\):

1. a better estimate for only the total band \(L^2\)-energy;
2. replacing worst-case Farey spacing merely by the number of frequencies
   in the band, by a sharper minimum-spacing estimate, or by discarding an
   exponentially small effective support.

The surviving possibility is genuinely coefficient-sensitive: one must
show cancellation or anti-clustering for the particular primitive
frequencies and their Dirichlet-kernel phases at the self-consistent
physical start \(A\asymp X\).  Equations (6) and (11) do **not** prove that
the relevant large-sieve operator norm is attained, nor that the signed
band sum is large.  Therefore this is an architecture barrier, not a
no-go theorem for phase-sensitive methods and not a proof or disproof of
the original question.
