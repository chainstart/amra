# Erdős #679 round-10 adversarial QA

Date: 2026-07-22

## 1. Claim-level ledger

### Unconditional theorems / exact identities

1. **Inherited-phase identity.** For every stopping conductor \(c<N\), the
   suffix shifts are
   \({\cal B}_{p,r,c}=c^{-1}({\cal A}_p-u_r)\), where \(u_r\) runs
   bijectively through the one block \((A-c,A]\). This is exact integer/CRT
   algebra.
2. **Top-band architecture barrier.** A family of valid crossing frontiers
   has normalized absolute cost at least
   \(X^{qC(1-o(1))}\exp\{L_2+o(L_2)\}\) if the suffix is bounded before
   joint frontier-phase cancellation. This is a no-go for that proof
   architecture, not a lower bound on the signed tail.
3. **Fixed-power sufficiency.** For fixed \(q\), \(qC>1\), any joint signed
   tail estimate \(O(X^{-\delta})\), \(\delta>0\), closes the relevant
   interval. In particular \(q=1,C>1\) is sufficient. Relative transfer to
   \(N\mu_q\) is not necessary.
4. **Primitive Fourier identity.** Every nonzero prefix frequency is
   primitive modulo its frontier conductor, with coefficient (3) of
   `primitive_phase_target.md`; the interval, terminal suffix, and inherited
   start remain coupled in (6). A finite independent evaluation of both
   formulas passed at errors below \(2.5\times10^{-15}\).
5. **Almost-all-phase theorem.** Uniformly averaging the interval start over
   the full CRT period, the fraction violating a fixed-power tail bound is
   polynomially small as in (10) of `almost_all_inherited_phases.md`.
6. **Exceptional-run reduction.** One original candidate forces
   \(Y+1\) consecutive exceptional canonical starts, with
   \(Y=\exp(L_2\sqrt{L_3})\). This follows from sliding the block through
   all \(K\in[Y,2Y]\).
7. **Uniform anti-clustering counterexample.** Somewhere modulo the full
   CRT period there is a run of \(Y\) consecutive canonical arguments on
   which every weight is \(X^{-o(1)}\). Hence a phase-uniform run exclusion
   is false; only an estimate using the actual location \(A\asymp X\) can
   serve as the missing theorem.

### Conditional statement

If a phase-preserving multilinear theorem proves the joint primitive sum is
\(O(X^{-\delta})\) for one fixed \(q,C\) with \(qC>1\), then #679's
candidate intervals are empty. Equivalently, it would suffice to prove the
local anti-clustering statement in Section 3 of
`exceptional_phase_run_reduction.md` **only for the actual dyadic range**.
Neither input is proved here; the arbitrary-start version of the latter is
disproved here.

### Heuristic only

Grouping prime factors turns the CRT inverses into phases resembling
Bettin--Chandee trilinear Kloosterman fractions. This is a route analogy,
not a theorem application. The checked results do not retain the growing
shift system and frontier-dependent suffix.

## 2. Probability-space audit of the almost-all theorem

The probability space in `almost_all_inherited_phases.md` is exactly

\[
 A\sim\operatorname{Unif}(\mathbb Z/Q\mathbb Z),
 \qquad Q=\prod_{H<p\le z}p.                          \tag{QA1}
\]

It is **not** randomness over primes, candidates, dyadic \(X\), or the
actual interval start. For

\[
 {\cal H}_{D,q}=\sum_{c(T)>D}F_T,
\]

ANOVA orthogonality on this probability space gives the exact variance
identity

\[
 \mathbb E_A|{\cal H}_{D,q}(A)|^2
 =\mu_q^2\sum_{c(T)>D}\prod_{p\in T}
 {\mathbb E d_p^2\over m_p^2}.                        \tag{QA2}
\]

The degree implication \(c(T)>D\Rightarrow
|T|\ge L_2-2L_3+O(1)\), together with
\(\sum_p\mathbb E d_p^2/m_p^2=O_C(q^2/L_2)\), yields

\[
 \mathbb E_A|{\cal H}_{D,q}(A)|^2
 \le\mu_q^2e^{-(2+o(1))L_2L_3}.                       \tag{QA3}
\]

For \(S_D(A)=\sum_{m\le N}{\cal H}_{D,q}(A+m)\), the
second-moment inequality is deliberately the safe Cauchy bound

\[
 \mathbb E_A|S_D(A)|^2\le N^2\mathbb E_A|{\cal H}_{D,q}(A)|^2, \tag{QA4}
\]

not a claimed decorrelation among the \(N\) shifts. Chebyshev applied to
(QA4) gives the stated exceptional fraction.

For fixed \(q\), the candidate Markov inequality is

\[
 1_{\rm good}\le t^{-qR}W^q,
 \qquad t^{-qR}=X^{o(1)}.                             \tag{QA5}
\]

When \(qC>1+\delta\), the uniformly transferred low part is
\(o(X^{-\delta})\), so a nonexceptional phase has total interval moment
\(O(X^{-\delta})\), and (QA5) makes its integer candidate count zero.

The inference stops there. Since \(Q\gg X^A\) for every fixed \(A\), a set
of density \(X^{-\sigma}\) modulo \(Q\) can contain an interval much longer
than \(X\), and can contain all deterministic dyadic starts. Neither
Chebyshev nor (QA3) rules that out. This is the precise obstruction to using
the theorem for the original binary interval starts.

## 3. Adversarial corrections and checks

* The top-band degree was changed from
  \(\lceil\log D/\log z\rceil\) to
  \(\lceil\log D/\log z\rceil+1\). Without the extra 1, an arbitrarily
  small fractional part could make the proposed \(y_0\) exceed \(z\).
  The correction guarantees a margin \(\gg\log z/L_2\) and changes no
  asymptotic exponent.
* The sliding-block formulas were re-read from rendered source: the
  canonical factor is \(1-a\,1_{\{0,\ldots,H-1\}}\), not a two-argument
  expression, and (6) uses the inequality \(\le\). The parameters
  \(H,z,a,t\) are fixed once from \(X\), rather than retuned with \(K\).
  Finally \(Y>K_\varepsilon\) and
  \(2Y+H<X\le n_0\) explicitly justify all shifted blocks.
* The almost-all energy uses the full high ANOVA tail. The stopping-line
  formula is an exact recombination of that same tail, so no terms are
  omitted or counted twice.
* The low-conductor moving-cutoff corollary is invoked for \(N\asymp X\),
  not for arbitrary short \(N\).
* The primitive finite audit uses one skipped prefix prime and a nontrivial
  suffix; it checks more than the suffix-free coefficient formula. It is
  only an algebra test.
* Walker's parameter \(Z\) is divisor support, not our prime endpoint
  \(z\). Confusing the two would be a fatal false application.
* Taking absolute values in the frontier index remains prohibited by the
  explicit top-band lower bound. None of the phase-average results silently
  reintroduces that step.
* Polynomially small phase density does not imply local anti-clustering.
  The explicit Chernoff--CRT construction supplies a length-\(Y\) bad run,
  so even strengthening Chebyshev without using \(A\asymp X\) cannot bridge
  the final quantifier.

## 4. Final status

* Original Erdős #679 first question: **OPEN**.
* Full deterministic interval transfer: **NOT PROVED**.
* Fixed-power joint high-tail estimate: **NOT PROVED**.
* New strongest unconditional result: **polynomially sparse exceptional
  set of complete-CRT interval phases, plus a long-exceptional-run necessary
  condition for any original candidate, plus a counterexample to uniform
  run anti-clustering**.
* Publication gate: **not reached**; these are rigorous reductions and a
  partial theorem, not a closure or a changed main exponent of the original
  problem.
