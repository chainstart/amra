# Adversarial author audit: violation generating polynomial

Scope: this is an adversarial self-audit by the author of
evidence/violation_generating_polynomial_dual_no_go.md.  It is not an
independent-agent reconstruction and does not upgrade the evidence class.

## Verdict

PASS, with the limitations below enforced.  The note proves exact
identities and two universal method no-go theorems, and leaves one
conditional arithmetic endpoint lemma.  It does not prove Erdos 451,
improve the known exponent unconditionally, or exhibit a counterexample
inside the actual product multiset.

## Checks

### 1. Generating-polynomial normalization: PASS

For every point,

\[
 z^{V(x)}=\prod_p\bigl(I_p(x)+z(1-I_p(x))\bigr)
          =\prod_p\bigl(z+(1-z)I_p(x)\bigr).
\]

Selecting the \(I_p\) term on \(T\) gives exactly
\(z^{m-|T|}(1-z)^{|T|}N_{P_T}\).  Replacing
\(N_{P_T}\) by \(\delta_TN+{\cal E}_{P_T}\) gives the principal product
\(\prod_p(\delta_p+q_pz)\).  At \(z=0\), all proper \(T\) vanish and only
\(N_P\) remains.  No Bonferroni remainder has been estimated separately.

### 2. Local character coefficient and absorber phase: PASS

The allowed unit residues at \(p\) are
\(-Q_0^{-1}j\), \(1\leq j\leq d_p\).  With the convention

\[
 {\bf 1}_{A_p}(x)=\sum_{\psi\bmod p}
 \left({1\over p-1}\sum_{a\in A_p}\overline{\psi(a)}\right)\psi(x),
\]

one has

\[
 \overline{\psi(-Q_0^{-1}j)}
 =\psi(-Q_0)\overline{\psi(j)}.
\]

This confirms the phase and conjugation in (9)-(13).  Summing over
\(x=ut\) produces the complex square \((S_X^P(\chi))^2\), not its absolute
square.  The factor \(1/\varphi(P)\) in the endpoint formula is the product
of the local \(1/(p-1)\) normalizations.

### 3. Proper-degree cube dual: PASS

For a multilinear polynomial, the alternating sum of all vertex values is
its top coefficient, so it is zero at total degree less than \(m\).  The
sign in

\[
 Q(0)=\sum_{S\neq\varnothing}(-1)^{|S|+1}Q({\bf 1}_S)
\]

is correct.  Under the product law,
\(\mu(S)/\mu(\varnothing)=\prod_{i\in S}q_i/\delta_i\geq1\).
The coefficient in the reconstructed expectation is positive for odd
\(|S|\) and nonnegative for even \(|S|\).  Thus pointwise nonpositivity on
all nonempty vertices forces nonpositive expectation.

Scope check: this kills proper-degree pointwise one-sided polynomial
certificates, including nonsymmetric ones.  It does not kill arbitrary
signed proper-degree estimates that use arithmetic deviations from the
principal product law.

### 4. Proper-marginal comparator: PASS

Every product atom is at least
\(\delta=\prod_i\delta_i\), because \(q_i\geq\delta_i\).  Hence both
\(\mu(S)\pm\delta(-1)^{|S|}\) are nonnegative.  Their total perturbation is
zero.  Summation over any omitted coordinate cancels the perturbation, so
all proper marginals agree.  The empty atom is respectively \(2\delta\)
and zero.  Rationality permits exact finite-multiset realization after a
common denominator is cleared.

Scope check: neither finite multiset is claimed to have the special form
\(\{Q_0ut\}\).  This is a distribution-free information barrier only.

### 5. Contour condition number: PASS

Testing endpoint evaluation on \((1-z)^m\) gives operator norm at least
\(r^{-m}\) on the closed disc \(|1-z|\leq r\).  Therefore subexponential
conditioning requires \(r=1-o(1)\).  This applies to a universal linear
continuation from that norm; it does not exclude arithmetic cancellation
within a specially phased contour integrand.

### 6. Conditional endpoint implication: PASS

The full-modulus formula partitions exactly into the principal term,
the already proved aggregate \(1<f_\chi\leq X^{4/3-\eta}\), and the
single high-conductor sum in (25).  The outer unit restriction loses only
\(O(\sum_{p\in{\cal P}}1/p)+O(m/X)=o(1)\), so \(N\sim X^2\).
Assumption (26), together with the prior low-conductor theorem, makes
\(F_X(0)>0\).  Such a product gives \(n=Q_0ut\); small-offset primes divide
\(Q_0\), remaining primes are handled by \(V=0\), and
\(\log(Q_0X^2)=(2\gamma+o(1))k/\log k\).

Scope check: (26) is an open hypothesis about one signed complex sum.  It
must not be reported as an unconditional lemma or as a closed campaign
claim.  The structured artifact must retain closes equal to the empty
list and survivor_deepening.

## Adversarial failure modes rejected

- Replacing the square in (12), (13), or (25) by an absolute square changes
  the identity.
- Bounding each support, conductor, or Bonferroni term separately recreates
  the already proved exponential entropy loss.
- A proper-degree certificate that is not pointwise nonpositive lies
  outside the dual theorem and cannot certify the endpoint without an
  additional signed expectation estimate.
- The comparator measures and contour test are method no-go witnesses, not
  actual lower bounds for the 451 endpoint error.
- The prior low-conductor theorem is used as an inherited proved input; it
  is not reproved in the new evidence note.

Final classification: exact identities plus unconditional scoped no-go;
one conditional decisive endpoint lemma; no public problem closure.
