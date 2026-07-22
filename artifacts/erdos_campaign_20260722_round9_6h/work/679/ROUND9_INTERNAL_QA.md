# Erdős #679 round-9 adversarial QA

Date: 2026-07-22

Verdict: **PASS_PARTIAL_RESULTS / INTERVAL TRANSFER OPEN / NO CLOSURE**.

## 1. Fixed-exponent window

For \(H=(\log X)^2\),

\[
 L=\sum_{H<p\le z}p^{-1}
  =L_2-2L_3-\log2+o(1).
\]

With \(a=CL_1/(HL)\), the main exponent is exactly \(HaL=CL_1\).
The threshold-to-main ratio is

\[
 {R\log(1/t)\over HaL}
 \le (2+o_\varepsilon(1))/L_3=o(1).
\]

The exact local variance formula gives

\[
 Ha^2L=C^2/L_2\{1+o(1)\}.
\]

For \(q=\lfloor L_3\rfloor\), both \(qa=o(1)\) and
\(q^2Ha^2L=O(L_3^2/L_2)=o(1)\). The same \(q\) multiplies the zero exponent
and threshold loss, so no hidden \(q/L_3\) relative error occurs.
The complete-period statements in fixed_exponent_tilt_refinement.md pass.

Fatal boundary: these are complete-CRT-period statements. Neither
\(M_2/\mu^2=1+o(1)\) nor
\(\mathbb P_2(C(h)>1)=o(1)\) controls sampling by a particular
\(X\)-interval when \(Q/X\) is enormous.

## 2. Polynomial-level denominator barrier

For the soft moment tilt \(b=1-(1-a)^q\), the effective local mass obeys
\(S=O(qL_1)\). A modulus \(d\le X^\theta\) contains at most
\((\theta+o(1))L_1/(BL_2)\) selected primes. Therefore

\[
 \log G_q(X^\theta)
 \ll {L_1\over BL_2}\log\{O(qBL_2)\}=o(qL_1)
\]

uniformly for \(q\ge1\). The monotonicity check for
\(\log(Aq)/q\) makes the uniformity valid. This excludes only the canonical
polynomial-level Selberg denominator interface; it is not an impossibility
theorem for signed or phase-sensitive methods.

The Ramaré preprint arXiv:2605.29470 is not evidence: its current arXiv
record marks it withdrawn after an important miscalculation.

## 3. Conditional stopping line

For \(W^q\), direct computation gives

\[
 d_p=-b(X_p-H/p),\quad
 \mathbb E|d_p|=2b(H/p)(1-H/p),\quad
 \rho_p\le3bH/p.
\]

The conductor cap and elementary-symmetric bound then give

\[
 \log{\cal F}(X^\kappa z)=O(L_1L_3/L_2)=o(L_1).
\]

For a nonempty conductor-\(c\) ANOVA term, one incomplete period is bounded
by \(c\) times its exact period \(L^1\) mean. Summing the local absolute
ratios verifies

\[
 \sum_IW_{\le X^\kappa}
 =N\mu\{1+O(X^{-1+\kappa+o(1)})\}
\]

for every fixed \(\kappa<1\). This is a genuine truncated interval theorem.
Moreover, since the conductor mass is at most
\(\exp\{(1/2+o_C(1))L_1L_3/L_2\}\), choosing
\[
 D=X\exp\{-2L_1L_3/L_2\}
\]
gives relative error
\(O(\exp\{-L_1L_3/L_2\})\) and still has \(Dz<X\). The moving-cutoff
corollary is therefore also valid.

For a frontier conductor \(c\), the map \(n=r+c\ell\) is invertible modulo
every suffix prime. It preserves the cardinality \(H\) of each forbidden
set, so the conditional suffix really is a member of the enlarged
arbitrary-residue family. Splitting into residues modulo \(c\), using
positivity for the suffix discrepancy and the exact period-\(c\)
\(L^1\) norm of the frontier, verifies inequality (10) in
stopping_line_conditional_suffix.md.

Fatal boundary: inequality (10) assumes precisely the uniform relative
suffix estimate that is missing. Iterating it without tracking the
prime-endpoint state is circular; the trivial terminal estimate may cost
\(\mu_{\rm suf}^{-1}\). Accordingly (10) is a strict reduction, not a
transfer theorem.

Moreover, a black-box estimate uniform over every starting interval is
impossible: CRT supplies an all-inactive suffix residue with weight one, so
an interval containing it has relative factor at least
\((M\mu_{\rm suf})^{-1}\). At the recursive scale this is superpolynomial.
Any viable continuation must preserve the inherited starting phase and its
dependence on the crossing residue.

## 4. Finite checks and claim hygiene

* verify_stopping_line.py exhausts all 15015 residues for its stated toy
  model and checks only the algebraic identity.
* minimax_majorant_probe.py is a finite LP. Its output refutes a blanket
  finite non-SOS obstruction but supplies no asymptotic majorant.
* Numerically unstable symmetric-binomial LP runs were discarded and are
  not evidence.
* No accepted proof was contradicted; no official status change, complete
  proof, preprint-ready theorem about the original problem, or SCI-Q2 claim
  is made.

Final QA status:

* strongest new strict result: **fixed \(H=(\log X)^2\) complete-period
  superpolynomial sparsity with vanishing relative energy**;
* strongest strict interval result: **ANOVA transfer through
  \(D=X\exp\{-2L_1L_3/L_2\}\), but only for the signed truncation**;
* strongest new route reduction: **subpower stopping frontier plus exact
  conditional suffix reparametrization**;
* missing lemma: **uniform transformed-suffix interval bound**;
* Erdős #679: **OPEN**.
