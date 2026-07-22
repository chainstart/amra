# #679: Kloosterman re-audit after removing the terminal suffix

Date: 2026-07-22

Round 10's Kloosterman audit concerned a stopping-frontier expansion and
listed a coefficient-dependent terminal suffix as one obstruction. The
growing-moment ANOVA expansion has no such suffix. This note redoes the
comparison for the new, simpler object rather than carrying that obsolete
obstruction forward.

## 1. Exact object still to be bounded

Let \(b=1-t^q=1-o(1)\), and write

\[
 W(n)^q=\sum_TF_T(n),\qquad
 \gamma_T=\prod_{p\notin T}\left(1-{bH\over p}\right),
 \qquad c=c(T).
\]

For \(T\ne\varnothing\), CRT Fourier inversion gives the same primitive
local formula as before, now without a suffix:

\[
 \widehat F_T(u)=
 \gamma_T{(-b)^{|T|}\over c}e(-uK/c)
 \prod_{p\mid c}D_H\!\left({h_p(u)\over p}\right),
 \qquad (u,c)=1,                                    \tag{1}
\]

where

\[
 h_p(u)\equiv u(c/p)^{-1}\pmod p,\qquad
 D_H(\theta)=\sum_{j<H}e(-j\theta),\qquad
 D_N^+(\theta)=\sum_{1\le m\le N}e(m\theta).
\]

Thus the unresolved interval sum is exactly

\[
 \sum_{c(T)>{\cal C}_X}{\gamma_T(-b)^{|T|}\over c(T)}
 \sum_{u\bmod c(T)}^*
 e\!\left({u(A-K)\over c(T)}\right)
 D_N^+\!\left({u\over c(T)}\right)
 \prod_{p\mid c(T)}D_H\!\left({h_p(u)\over p}\right). \tag{2}
\]

Here

\[
 \log {\cal C}_X=(1-\eta)HL,\qquad
 \sum_{T,u}|\widehat F_T(u)|^2=\exp\{-(1+o(1))HL\}. \tag{3}
\]

Formula (2), rather than the round-10 frontier expression, is the correct
target for any new exponential-sum theorem.

## 2. Where the spectral mass actually lies

Normalize the ANOVA energies in (3). The resulting choice of whether
\(p\in T\) is Bernoulli with parameter

\[
 \theta_p={\mathbb E d_p^2\over m_p^2+\mathbb E d_p^2}.
\]

For \(p\ge2H\), \(b=1-o(1)\) gives

\[
 \theta_p=(1+o(1)){H\over p}.
\]

Consequently the energy-typical conductor has

\[
 \mathbb E|T|=(1+o(1))HL,
 \qquad
 \mathbb E\log c(T)
 =(1+o(1))H\sum_{H<p\le z}{\log p\over p}
 =(1+o(1))H\log z.                                 \tag{4}
\]

With \(H=L_1^2\), \(L\sim L_2\), and
\(\log z=L_1/L_2\), the two logarithmic scales are

\[
 \log {\cal C}_X\asymp L_1^2L_2,\qquad
 \mathbb E\log c(T)\asymp {L_1^3\over L_2}.        \tag{5}
\]

Their ratio tends to infinity like \(L_1/L_2^3\). This can be upgraded
from a comparison of means to a concentration statement. Directly from
the local formulas,

\[
 \theta_p\le {H\over p},
 \qquad
 \operatorname {Var}(\log c(T))
 \le H\sum_{p\le z}{(\log p)^2\over p}
 =O\!\left(H(\log z)^2\right).                     \tag{6}
\]

The standard deviation is only \(O(H^{-1/2})\) of the mean in (4), while
\(\log{\cal C}_X=o(H\log z)\). Thus even Chebyshev shows that the
ultra-high range contains \((1-o(1))M_{2,q}\) of the nonnegative spectral
energy. The sharper counting small-deviation argument in
**growing_moment_ultrahigh_conductor_reduction.md** gives

\[
 {1\over M_{2,q}}
 \sum_{c(T)\le \exp(\alpha HL)}\sum_u^*
 |\widehat F_T(u)|^2
 \le \exp\{-(1-o(1))HL\}                            \tag{7}
\]

for every fixed \(\alpha>0\). Hence the unnormalized low energy is
\(\exp\{-(2-o(1))HL\}\). This extra exponent is what moves the usable
large-sieve cutoff from \(e^{(1/2-\eta)HL}\) to
\(e^{(1-\eta)HL}\). It does not imply that the complementary signed
interval sum is large or small.

## 3. Rechecked literature interface

[Bettin--Chandee](https://arxiv.org/abs/1502.00769) bounds trilinear sums
with Kloosterman-fraction phase and arbitrary coefficient sequences.
[Wright 2026](https://arxiv.org/abs/2604.25177) improves a partially fixed
modulus configuration and obtains applications to particular unbalanced
multiplicative convolutions. The inverse factors \(h_p(u)\) in (1) make
these results structurally relevant, but neither paper states a bound for
(2).

After the growing-moment simplification, the honest mismatch list has
three items, not four:

1. **Ultra-high, many-prime conductors.** By (4)--(6), an energy-typical
   term involves \((1+o(1))HL\) selected primes and conductor logarithm
   \((1+o(1))H\log z\). A three-variable grouping must preserve the
   internal CRT inverses from all of these primes; it is not a direct
   dyadic trilinear box from the cited theorems.
2. **Growing shifted dimension.** The factor
   \(\prod_{p\mid c}D_H(h_p(u)/p)\) represents
   \(H=(\log X)^2\) shifted residue classes. It is not a divisor-bounded
   convolution with a fixed number of factors or a Siegel--Walfisz factor
   of the kind used in the stated distribution applications.
3. **Required normalization.** A candidate forces (2) to be at least
   \(\exp\{-o(HL)\}\). The needed theorem must therefore give an aggregate
   \(o(\exp\{-o(HL)\})\) bound at the prescribed \(A\asymp X\). No checked
   result supplies this normalization after summing all conductor
   factorizations and primitive \(u\)'s.

The round-10 terminal-suffix obstruction is genuinely gone. This is real
simplification, but it is not by itself a theorem application.

Nor can (8) below be requested uniformly over arbitrary interval starts.
CRT gives a point \(n_0\) with \(W(n_0)^q=1\); every length-\(X\)
interval containing it has total moment at least one. The zero and low
parts are uniformly exponentially small, so its high signed sum is at
least \(1-o(1)\). The required theorem must use the self-consistent
location \(A\asymp X\), which this CRT representative does not satisfy.

## 4. Precise conditional target

It would suffice to prove, uniformly for the actual interval start
\(A\asymp X\),

\[
 \left|\text{the expression in (2)}\right|
 \le \exp\{-\delta HL\}                             \tag{8}
\]

for one fixed \(\delta>0\). More generally, any bound
\(o(t^{qR})\) suffices. Equations (1)--(2) give an exact interface for a
future phase-preserving multilinear theorem; the currently checked
Kloosterman-fraction results do not establish (8).

Strict status: **one former obstruction removed; three quantified
obstructions remain; no black-box Kloosterman closure and no proof of
Erdős #679**.
