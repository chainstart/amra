# #679: the coefficient-one ceiling of the energy-only argument

Date: 2026-07-22

This note records what the strengthened low-conductor estimate can and
cannot do. It is an architectural no-go statement, not a no-go theorem
for every possible proof.

## 1. Why the coefficient \(1\) is the natural endpoint

For every fixed \(\alpha>0\), the growing-moment calculation gives

\[
 {\cal V}_{\le e^{\alpha HL}}
 :=\sum_{c(T)\le e^{\alpha HL}}\sum_u^*
       |\widehat F_T(u)|^2
 \le e^{-(2-o(1))HL}.                              \tag{1}
\]

This exponential scale cannot be improved for the full low collection:
the empty ANOVA component alone has energy

\[
 |\widehat F_\varnothing(0)|^2
 =\mu_q^2=e^{-(2+o(1))HL}.                         \tag{2}
\]

Even after removing the zero mode, the one-prime layers have the same
exponential scale. Uniformly for \(p\ge2H\),
\[
 {\mathbb E d_p^2\over m_p^2}
 ={H/p\over1-H/p}(1+o(1)),
\]
and summing this over \(2H\le p\le z\) gives \((1+o(1))HL\).
Thus their total energy is
\[
 \mu_q^2(1+o(1))HL=e^{-(2+o(1))HL}.
\]
So (2) is not merely a zero-mode notation artefact.

Suppose only primitive Farey separation, the energy (1), and a physical
interval Cauchy inequality are used. For a conductor cutoff
\({\cal C}=e^{\alpha HL}\), they give

\[
 \left|\sum_{n\in I}{\cal E}_{\le{\cal C}}(n)\right|
 \le N^{1/2}(N-1+{\cal C}^2)^{1/2}
       {\cal V}_{\le{\cal C}}^{1/2}
 \le e^{(\alpha-1+o(1))HL}.                        \tag{3}
\]

Thus the pooled estimate (3) is exponentially useful for fixed
\(\alpha<1\). At \(\alpha=1\) its displayed exponent loses the fixed
saving, and for \(\alpha>1\) this estimate is useless. This proves that
coefficient \(1\) is the ceiling of the current **single pooled energy +
global worst-case spacing + Cauchy** calculation.

There is an important limitation to this ceiling statement. The
one-prime lower bound proves that the cumulative low energy cannot have a
better logarithmic exponent, but those one-prime frequencies have much
smaller conductors than \(e^{\alpha HL}\). It does not prove sharpness of
the worst-case spacing factor for every energy layer. A
conductor-stratified estimate, or cancellation using the coefficient
structure inside each layer, is not ruled out by (1)--(3).

## 2. Most energy is beyond the cutoff

Under normalized ANOVA energy, the conductor logarithm has

\[
 \mathbb E\log c(T)=(1+o(1))H\log z,\qquad
 \operatorname {Var}(\log c(T))=O(H(\log z)^2).
\]

Since \(H\log z/(HL)=L_1/L_2^2\to\infty\), every fixed
\(e^{\alpha HL}\) lies far below the energy-typical conductor.
Consequently

\[
 {\cal V}_{>e^{\alpha HL}}=(1-o(1))M_{2,q}.         \tag{4}
\]

Equation (4) is a statement about nonnegative spectral energy. It gives
neither a lower nor an upper bound for the signed physical-interval
aggregate.

## 3. Even an arbitrary-start length-\(X\) interval bound is false

For every prime \(p>H\), choose a residue outside its \(H\) forbidden
classes. CRT supplies an integer \(n_0\bmod Q\) avoiding every local
forbidden block, so

\[
 W(n_0)^q=1.
\]

Applying (1) and Farey spacing with a one-point physical interval shows,
for fixed \(\alpha<1\),

\[
 |{\cal E}_{\le e^{\alpha HL}}(n_0)|
 \le e^{-(1-\alpha-o(1))HL},
\]

and the zero mode is also exponentially small. Hence the complementary
high-conductor signed value satisfies

\[
 {\cal E}_{>e^{\alpha HL}}(n_0)=1-o(1).             \tag{5}
\]

Now put this \(n_0\) into any interval \(I\) of length \(N\asymp X\).
Because \(W^q\ge0\) everywhere,

\[
 \sum_{n\in I}W(n)^q\ge1.
\]

The low-conductor large-sieve estimate is uniform in the interval start,
so its total signed contribution on this \(I\) is exponentially small;
the zero mode \(N\mu_q\) is also exponentially small. Exact decomposition
therefore gives the stronger statement

\[
 \sum_{n\in I}{\cal E}_{>e^{\alpha HL}}(n)\ge1-o(1).
                                                            \tag{6}
\]

Thus no phase-uniform smallness theorem for the remaining tail can hold
even after summing an arbitrary-start interval of length \(X\). The
essential caveat is self-consistency: a CRT representative supplied this
way is generally of size comparable to the enormous period \(Q\), not of
size comparable to the parameter \(X\). Hence (6) does not obstruct a
theorem restricted to the required actual location \(A\asymp X\).

## 4. Exact next interface

Crossing coefficient \(1\), or closing #679 at the existing cutoff,
requires information absent from (1)--(3), such as:

* a conductor-stratified energy/spacing estimate that beats the pooled
  worst-case norm;
* cancellation in the joint many-prime inverse phases;
* an interval-sum theorem using the prescribed, self-consistent start
  \(A\asymp X\);
* or a multilinear factorization retaining all primitive frequencies
  while beating the generic Farey norm.

Strict status: **coefficient-one ceiling for the present pooled
energy--spacing calculation; no exclusion of conductor-stratified or
phase-sensitive continuations and no closure of Erdős #679**.
