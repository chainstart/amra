# Erdős #679 round-11 actual-phase attempt log

Unified charged window: `2026-07-22T22:15:18+08:00` through
`2026-07-23T00:15:18+08:00`, exactly 7,200 seconds.

Resource rule: symbolic work by default. Any finite verification is pinned
to core 7 with `nice -n 10`, and at most one process is used.

## Frozen starting boundary

Round 10 proved an almost-all interval-start theorem only for
\(A\) uniform modulo the full CRT period \(Q\). It also gave an explicit
Chernoff--CRT construction of a length
\(Y=\exp\{L_2\sqrt{L_3}\}\) arbitrary-start exceptional run. Therefore:

* complete-period density cannot be promoted to the actual dyadic start;
* a phase-uniform pointwise or run anti-clustering black box is false;
* every new estimate must use \(A\asymp X\), or retain the joint terminal
  suffix/frontier phase strongly enough to imply a fixed-power signed-tail
  estimate there.

No Round-10 theorem is counted as a deterministic interval transfer.

## Status and source refresh

At 2026-07-22 23:29 HKT the official #679 page was fetched again and
still displayed **Open**. The arXiv API returned Bettin--Chandee
1502.00769, Wright 2604.25177v1 (2026-04-28), and van Doorn--Tang
2606.19863v1 (2026-06-18). The latter theorem statement was also checked
in the rendered primary text, including the endpoint
\(\exp(\log^2k/(20\log\log k))\) and prime interval
\((k,k+3k^\theta)\).

The rendered primary text and TeX source of Tao--Teräväinen
2512.01739v2 (v1 2025-12-01, v2 2026-04-25) were also checked. Its
Theorem 1.1 closes #248 with the much
weaker bound \(\Omega(n+k)\le Ck\); its Remark 1.2 states the exact #679
target and explicitly assesses it as beyond the present method. The
construction handles \(O(\log_2X)\) simultaneous shifts using a product
of one-dimensional smooth Selberg sieves, not the
\(H=(\log X)^2\)-shift signed ultra-high-conductor tail left here. The
detailed comparison is in tao_teravainen_high_dimensional_sieve_audit.md.

A final forward-citation check located Lau 2604.15042v2 (v1 2026-04-16,
v2 2026-06-24). Its Theorem 1.3 is directly about the minus shifts and
proves \(\omega(n-k)\le\Omega(n-k)\le C\log k\) for all \(1<k<n\) for
infinitely many \(n\). The paper itself notes the remaining
\(\log\log k\) factor to #679. Its proposed optimality and Section 7
negative conclusion are conditional conjectural evidence, not a closure.
See lau_2026_direct_boundary_audit.md.

A final arXiv title/full-text forward scan at 00:00 HKT found no later
unconditional #679 closure. This negative search is recorded only as
bibliographic evidence, not as proof that no unindexed result exists.

## Fixed-moment Rankin improvement

`rankin_conductor_mass_improvement.md` replaces the degree-only conductor
mass estimate by Rankin's trick with \(s=1/\log H\). Chebyshev's prime
upper bound gives \(\sum_{p>H}p^{-1-s}=O(1)\), hence for fixed \(q,C\),

\[
 {\cal F}(Y)\le z^{K(q,C)}\qquad(Y\le Xz).
\]

Choosing \(D=N z^{-B}\), \(B>K+4\), proves the deterministic transfer
\(\sum_I{\cal L}_{D,q}=N\mu_q(1+O(z^{-4}))\). A stopping frontier now leaves
an inherited suffix interval of length between \(z^{B-1}\) and \(z^B\),
rather than \(\exp(\Theta(\Phi))=z^{\Theta(L_3)}\). The signed aggregate at
this new frontier remains open.

## Actual-representative audit

`actual_representative_and_recent_input_audit.md` compares the forced run
length with the June 2026 van Doorn--Tang theorem. At
\(Y=\exp(L_2\sqrt{L_3})\), that theorem controls endpoints only through
\(\exp(O(L_2^2))\), whereas the required endpoint is
\(X=\exp(L_1)\). Exact cycling of primes \(p\le Y\) supplies only
\(O(L_4)\) reciprocal-prime mass, versus the
\(L_2/\sqrt{L_3}\) candidate threshold. This route therefore does not
produce a small representative or a contradiction.

## Primitive large-sieve middle range

`primitive_large_sieve_middle_range.md` uses the fact that every ANOVA
frequency is primitive at its full conductor. For the Rankin cutoff
\(D=Nz^{-B}\), the local variance mass above \(D\) is

\[
 \sum_{c(T)>D}\prod_{p\in T}v_p
 \le\exp\{-(2+o(1))L_2L_3\}.
\]

The Farey large sieve consequently gives, for every fixed \(A\ge1\),

\[
 \left|\sum_I\sum_{D<c(T)\le X^A}F_T\right|
 \le X^{A+1/2-qC+o(1)}e^{-(1+o(1))L_2L_3}.
\]

Choosing a fixed moment with \(qC>A+1/2+\delta\) makes this a fixed-power
deterministic estimate. Hence all low conductors and any prescribed fixed
polynomial conductor window are now removed. The aggregate with
\(c(T)>X^A\) remains outside this argument; taking its absolute value or
applying an unrestricted Farey norm recreates the known extreme-conductor
barrier.

## Growing-moment ultra-high-conductor reduction

The file growing_moment_ultrahigh_conductor_reduction.md lets
\(q=\lfloor s/a\rfloor\), where \(s\to\infty\) and \(s=o(L_3)\). Then the
local deletion strengths in \(W^q\) and \(W^{2q}\) both tend to one, and the
exact complete moments satisfy

\[
 \log\mu_q=-(1+o(1))HL,\qquad
 \log M_{2,q}=-(1+o(1))HL.
\]

The proof splits \(H<p<2H\) from \(p\ge2H\), so it does not make the false
uniform assertion that \(1-H/p=1-o(1)\) at the lower endpoint.

Primitive Fourier support and the additive large sieve now control, at
every actual interval start, the entire nonconstant range

\[
c(T)\le
 \exp\{(1-\eta)HL\}
 =X^{(1-\eta+o(1))L_1L_2}
\]

by \(\exp\{-(\eta-o(1))HL\}\), for each fixed \(0<\eta<1\). The factor
\(1\), improving the preliminary factor \(1/2\), comes from normalizing
the ANOVA energies: the selected-prime count is a non-iid
Poisson--binomial variable of mean \((1+o(1))HL\), while
\(c(T)\le e^{\alpha HL}\) forces only \(O_\alpha(H)\) selected primes.
Its lower-tail probability is \(e^{-(1-o(1))HL}\), so the unnormalized
low-conductor Fourier energy is \(e^{-(2-o(1))HL}\).

The candidate threshold costs only
\(\exp(o(HL))\). Hence a candidate would force the complementary **signed**
ultra-high-conductor aggregate to be positive and at least
\(\exp\{-o(HL)\}\). This is a much later conductor boundary than every
fixed \(X^A\), but the required upper bound on that final aggregate remains
open. The Kloosterman re-audit records that the old terminal suffix is gone,
but ultra-high many-prime conductors, growing shifted dimension, and the
subunit target normalization remain outside the checked theorems.

The final parameter audit shows that the argument is stable under
\(H=\lfloor L_1^d\rfloor\) for every fixed \(d\ge1\). The entropy cutoff
becomes \(r_\alpha=(\alpha/d+o(1))H\), the usable conductor is
\(X^{(1-\eta+o(1))L_1^{d-1}L_2}\), and the candidate coefficient is \(d\).
All error ratios remain \(o(HL)\). This matches the free fixed exponent in
Lau's short-interval template but does not prove its density premise.

## Finite normalization check

The file **verify_growing_moment.py** was rerun after the energy-law checks
were added and reproduced its recorded output byte for byte, always with
one pinned, low-priority process
on the toy system \(H=2\), primes \(5,7,11\), and
\(q=17\). It independently checks ANOVA reconstruction, Fourier inversion,
vanishing of nonprimitive coefficients, Parseval/second-moment
normalization, the product-Bernoulli energy law and
\(\theta_p\le H/p\), Farey spacing, and the finite large-sieve inequality.
All checks pass; the largest Fourier inversion error is
\(7.19\mathbin{\cdot}10^{-15}\). This is only a finite algebra audit and
is not used as evidence for any asymptotic assertion.

## Energy-only endpoint audit

The file **coefficient_one_energy_barrier.md** proves that the coefficient
\(1\) is the exact ceiling of the present pooled
energy--global-Farey--Cauchy estimate.
The low energy cannot have exponent better than \(2HL\), because the empty
ANOVA component already has energy \(\mu_q^2=e^{-(2+o(1))HL}\).
Consequently a cutoff \(e^{\alpha HL}\) yields only
\(e^{(\alpha-1+o(1))HL}\), which is useful for fixed \(\alpha<1\) and
loses its fixed saving at \(\alpha=1\). This does not rule out a
conductor-stratified norm: the one-prime lower bound lies at much smaller
conductors and proves energy sharpness, not sharpness of the global
worst-case spacing factor.

An arbitrary CRT point avoiding all local forbidden residues has
\(W^q=1\); at that point the low range is exponentially small, so the
high signed value is \(1-o(1)\). More strongly, put that point inside an
arbitrary-start interval of length \(N\asymp X\). Positivity makes the
whole \(W^q\)-sum at least one, while the zero and low terms remain
exponentially small, so the high signed interval aggregate is at least
\(1-o(1)\). Thus arbitrary-start interval closure is false. The CRT
representative is not self-consistently of size \(X\); an interval theorem
restricted to \(A\asymp X\) remains the exact target.

## Growing-moment exceptional-phase density

For \(A\) uniform modulo the full CRT period, translation invariance gives
\[
 \mathbb E_A\sum_{1\le m\le N}W(A+m)^q=N\mu_q.
\]
An interval containing one local candidate has this sum at least
\(t^{qR}\). Hence the proportion of exceptional interval starts is at
most
\[
 Nt^{-qR}\mu_q=e^{-(1-o(1))HL}.
\]
This strengthens the round-10 polynomial exceptional-density bound.
It still does not control the actual start: \(\log Q\sim z\gg HL\), and
one CRT spike creates roughly \(N\) consecutive exceptional interval
starts.

## Unified freeze

The scheduled hard boundary was 2026-07-23 00:15:18 HKT, exactly 7,200
charged seconds after the start. It was observed at 00:15:36; no new proof
or literature search was performed after the scheduled boundary. The
pre-existing finite verifier was rerun at 00:15:43 with one low-priority
process pinned to core 7, and its stdout was byte-identical to
verify_growing_moment.out.
