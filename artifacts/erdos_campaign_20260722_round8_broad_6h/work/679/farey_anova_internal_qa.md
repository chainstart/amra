# #679: adversarial QA of the Farey--ANOVA reduction

Date: 2026-07-22 (Asia/Hong_Kong)

Verdict: **PASS_REDUCTION / ONE_SIDED_TAIL_OPEN**.  The identities and the
implication from the isolated one-sided tail estimate to the negative answer
are strict.  The tail estimate itself is not proved.

## 1. Exactness of the ANOVA layer

Write the normalized local Fourier decomposition as

\[
 W_p(n)=m_p+d_p(n),\qquad {1\over p}\sum_{n\bmod p}d_p(n)=0.
\]

In the product over primes, choosing the constant term at primes outside
\(S\) and a nonzero local frequency at primes in \(S\) gives precisely the
global frequencies whose reduced conductor is \(\prod_{p\in S}p\).  Hence,
with no inequality or normalization loss,

\[
 F_S(n)=\prod_{p\notin S}m_p\prod_{p\in S}d_p(n).
\]

For the \(H\)-residue block and \(a=1-t\),

\[
 d_p(n)=\begin{cases}
 -a(1-H/p),&n\bmod p\in{\cal K},\\
 aH/p,&n\bmod p\notin{\cal K}.
 \end{cases}
\]

Because every selected prime satisfies \(p>H\), both magnitudes are strictly
less than \(a\).  In particular the actual full-conductor contribution is at
most \(Na^M\), where \(M=|{\cal P}|\).  This validates the correction that the
full-conductor energy-Cauchy explosion is a method pseudo-obstruction.
The finite DFT audit in `verify_conductor_ledger.py` separately reconstructs
all eight ANOVA/conductor layers for \(Q=3\cdot5\cdot7\); its maximum numerical
layer error is \(1.559\times10^{-14}\).

## 2. Low-degree cutoff

If \(|S|\le\kappa L_2\), then

\[
 c(S)\le z^{\kappa L_2}=X^\kappa.
\]

Summing the complete-period dyadic estimate through \(X^\kappa\) and using
Cauchy only across the \(O(\log X)\) dyadic blocks gives

\[
 { |E_{\rm low}|\over N\mu}
 \ll
 \left({M_2\over\mu^2}\right)^{1/2}
 X^{3\kappa/2-1}\sqrt{\log X}
 =X^{3\kappa/2-1+o(1)}.
\]

Thus every fixed \(\kappa<2/3\) gives \(E_{\rm low}=o(N\mu)\) for the sum of
**all** layers with \(c(S)\le X^\kappa\).  This is stronger than merely
controlling \(|S|\le\kappa L_2\): some higher-degree sets also have small
conductor.  The check uses conductor blocks, not a count of subsets, so no
hidden \(\binom Mr\) factor is introduced.

## 3. Exact strength needed for closure

Let

\[
 E_{\rm high}=
 \sum_{n\in I}\sum_{c(S)>X^\kappa}F_S(n).
\]

The full asymptotic would follow from \(|E_{\rm high}|=o(N\mu)\).  For the
negative direction of #679, however, it suffices to have the weaker one-sided
estimate

\[
 E_{\rm high}\le N\mu X^{o(1)}.                         \tag{QA-target}
\]

Indeed the low-degree audit then gives
\(\sum_IW\le N\mu X^{o(1)}\).  Every candidate counted in the preceding
zero-mode reduction has weight at least \(t^R\), while that reduction proves

\[
 t^{-R}\mu\le X^{-C_0+o(1)}
\]

for any fixed \(C_0>1\).  Since \(N\asymp X\), the candidate count is at most
\(X^{1-C_0+o(1)}<1\).  The strict fixed margin \(C_0-1\) absorbs every
subpower loss in (QA-target).

## 4. Remaining caveat

Neither the pointwise absolute ANOVA sum nor finite Bonferroni truncation
proves (QA-target).  This is not an artefact of using degree in place of
conductor: choosing \(r=(\kappa+\delta)L_2\) primes from \((z/2,z]\) gives
\(c(S)>X^\kappa\), while the resulting (13)-based absolute combinatorial sum
is already \(X^{\kappa+\delta+o(1)}\).  More broadly, the natural absolute or
Bonferroni degree is \(aHL\asymp\log X\), whereas the guaranteed
period-controllable degree is only \(O(L_2)\).  Therefore this QA certifies
the reduction and its constants, not the missing signed-tail theorem and not
a solution of #679.
