# Independent audit of the top-six Newton tail

Date: 2026-07-30

Audited files:

- `TOP_SIX_NEWTON_TAIL_THEOREM.md`;
- `verify_top_six_newton_tail.py`;
- `test_verify_top_six_newton_tail.py`.

This audit did not modify those files.

## 1. Verdict

The current theorem statement passes the normalization, symbolic-formula,
boundary-range, sign, and finite-interpolation checks.

In particular:

1. the current normalization in (12) is correct;
2. the six formulas (1)--(6) agree with an independently constructed
   weighted-Cayley forest recursion for every \(2\leq k\leq12\);
3. the exceptional \(k=2,3,4\) rows are handled correctly;
4. the stated signs hold exactly on the ranges where the layers exist;
5. the interpolation sample count is more than sufficient, conditional on
   the human degree lemma;
6. the bundled verifier is exact but is not fully independent of
   (7)--(11), because its direct-row regression reuses the same profile
   function and determinant formula.

No mathematical error was found in the present formulas.  The principal
publication-level vulnerability is expository: the polynomial-degree lemma
is the premise that turns finitely many profile checks into all-\(j\)
identities.  The present cycle-union proof gives the right bound, but a final
manuscript should spell its finite-type expansion out rather than relying on
the verifier.

## 2. Normalization chain

Write
\[
m=2k-4,\qquad q=m-d.
\]
The theorem defines
\[
c_k(s)=\frac{(k-2)!}{2}C_k(s)
=\sum_q a_{k,q}\binom{s-4}{q}
\]
and
\[
p_{k,d}=\frac{a_{k,m-d}}{(m-d)!}.
\]
Since
\[
\binom{s-4}{q}=\frac{(s-4)_{\underline q}}{q!},
\]
the conversion
\[
c_k(s)=\sum_d p_{k,d}(s-4)_{\underline{m-d}}
\]
in (16) is exactly normalized.  There is no missing factorial in the
definition of \(p_{k,d}\).

The determinant prefactor is also correct:
\[
\frac{k!}{2k(k-1)}=\frac{(k-2)!}{2}.
\]
Thus (11) agrees with the original normalization of \(c_k\).

## 3. Audit of equation (12)

The current equation is
\[
\boxed{
U_{h,j}(s)=\frac1{2^j j!}
\sum_{\ell\geq0}R_{\ell,h}(j)s^{2j-\ell},
\qquad R_{0,h}(j)=1.
}
\tag{A1}
\]
This is the correct orientation of the factor \(2^j j!\).

Combinatorially, after the prescribed matching is fixed, the leading
configuration consists of \(j\) disjoint additional edges.  Its count is
\[
\frac{s^{2j}}{2^j j!}+O_j(s^{2j-1}),
\]
uniformly for \(h=0,1,2\).  Hence the leading coefficient of \(U_{h,j}\)
is \(1/(2^j j!)\), which is exactly (A1).

The first profiles give a direct check:
\[
\begin{array}{c|ccc}
 &h=0&h=1&h=2\\ \hline
j=0&1&1&1\\[1mm]
j=1&
\frac{s(s-1)}2&
\frac{(s-2)(s+1)}2&
\frac{s^2-s-4}2
\end{array}
\]
and all three \(j=1\) profiles have leading coefficient \(1/2\).
For \(j=2\), all three have leading coefficient \(1/8\).

Therefore any version of (12) with \(2^j j!\) multiplying the series,
or with \(R_{0,h}\neq1\), would be incorrectly normalized.  The current
version is consistent with (7)--(10), (11), and the final monic coefficient
\(p_{k,0}=1\).

## 4. Binomial convolution and the four-drop cancellation

Substitution of (A1) into (11) uses
\[
\frac1{2^k j!(k-j)!}
=\frac1{k!}\frac{\binom kj}{2^k}.
\]
After multiplication by \(k!/[2k(k-1)]\), the coefficient at one fixed
profile drop is therefore
\[
\frac1{2k(k-1)}
\mathbb E[\text{profile kernel}],
\qquad J\sim{\rm Bin}(k,\tfrac12),
\]
which is exactly what `determinant_power_coefficients` implements.

The product profiles have formal degree \(2k\), while the determinant
cancels drops \(0,1,2,3\).  Hence \(c_k\) starts in degree
\[
2k-4=m.
\]
To obtain the six powers
\[
s^m,s^{m-1},\ldots,s^{m-5},
\]
one needs total profile drops \(4,\ldots,9\).  It is therefore necessary
and sufficient for the verifier to record
\[
R_{\ell,h}\qquad(0\leq\ell\leq9).
\]
Its convolution loop over `drop in range(4, 10)` has the correct endpoints.

## 5. Finite interpolation sufficiency

The current Lemma 1 states
\[
\deg_j R_{\ell,h}(j)\leq\ell.
\tag{A2}
\]
The hard-coded expressions satisfy this bound:

- the expressions for \(\ell\leq6\) have degree at most \(\ell\);
- the three \(\ell=7\) expressions have degree \(7\);
- the three \(\ell=8\) expressions have degree \(8\);
- the three \(\ell=9\) expressions have degree \(9\).

Once (A2) is known, equality at
\[
j=0,1,\ldots,\ell
\]
is sufficient.  The verifier instead checks
\[
j=0,1,\ldots,2\ell+2,
\]
so it uses \(\ell+2\) redundant points beyond the minimum.  Its total is
\[
3\sum_{\ell=0}^9(2\ell+3)=360,
\]
matching the test.

The finite checks do **not** prove (A2); they prove the recorded identities
only after (A2) is supplied.  The present human proof has the correct
ledger:

1. without acyclicity, a loss \(2r+t=\ell\) has \(j\)-degree at most
   \(2r+t=\ell\);
2. a cycle-union core with \(e\) nonprescribed edges and \(v\) nonfixed
   vertices has
   \[
   \delta=2e-v\geq e;
   \]
3. choosing the core has \(j\)-degree at most \(e\), while the residual
   expansion has degree at most \(\ell-\delta\);
4. hence the total degree is
   \[
   e+\ell-\delta\leq\ell.
   \]

This establishes the required bound in outline.  For a publication proof,
the phrase “apply inclusion--exclusion over cycles” should be expanded into
a finite sum over cycle-union types, recording its automorphism factor and
the falling factorial in \(j\).  That would make exact polynomiality for
all small \(j\), rather than eventual polynomiality, completely explicit.
This is a proof-presentation recommendation, not a detected counterexample.

## 6. Independent exact-row reconstruction

The bundled `direct_newton_row` is not an independent check of
(7)--(11): it calls the same `profile` function used in the symbolic
extraction and applies the same determinant.

I therefore recomputed the rows by a different method already available
in `verify_first_active_newton_theorem.py`:

1. contract the \(h\) prescribed disjoint edges into \(h\) vertices of
   weight two;
2. count a tree component with \(t\) weight-two vertices and \(u\)
   ordinary vertices by weighted Cayley,
   \[
   2^t(2t+u)^{t+u-2};
   \]
3. recursively select the component of the first remaining vertex;
4. read the coefficient with \(j\) additional edges;
5. form the determinant and take forward differences at
   \(s=4,\ldots,4+m\).

This recursion does not call the top-six Lagrange \(E,D\) formulas.
For \(2\leq k\leq12\), every existing member of the six-layer tail agrees
with (1)--(6).

The smallest complete normalized rows \(p_{k,d}\) are:
\[
\begin{array}{c|c|l}
k&m& (p_{k,0},p_{k,1},\ldots)\\ \hline
2&0&(1)\\
3&2&(1,10,2)\\
4&4&(1,24,147,84,0)\\
5&6&(1,42,587,2972,2958,300).
\end{array}
\tag{A3}
\]
For reference, the corresponding unnormalized top coefficients
\(a_{k,m-d}=p_{k,d}(m-d)!\) are
\[
\begin{array}{c|l}
k&(a_{k,m},a_{k,m-1},\ldots)\\ \hline
2&(1)\\
3&(2,10,2)\\
4&(24,144,294,84,0)\\
5&(720,5040,14088,17832,5916,300).
\end{array}
\tag{A4}
\]

This catches both possible factorial mistakes in (12)/(16) and
off-by-one mistakes in the top index \(m-d\).

## 7. Boundary and support audit

A layer exists exactly when
\[
m-d=2k-4-d\geq0.
\]
Consequently:

- \(k=2\): only \(d=0\) exists, and \(a_{2,0}=p_{2,0}=1\);
- \(k=3\): only \(d=0,1,2\) exist, all positive;
- \(k=4\): \(d=0,\ldots,4\) exist; the final value is
  \(p_{4,4}=a_{4,0}=0\);
- \(k\geq5\): all six displayed layers exist.

For \(k=4\),
\[
q_0=\left\lfloor\frac{k-2}{2}\right\rfloor=1,
\]
so \(q=0\) is below the active support.  The zero \(p_{4,4}\) is therefore
consistent with the lower-tail capacity theorem and is not a missing
positive case.

The positivity ranges in the theorem are exact:

- \(p_{k,1}\) and \(p_{k,2}\) are positive from their first existing
  case \(k=3\);
- \(p_{k,3}\) first exists and is positive at \(k=4\);
- \(p_{k,4}=0\) at \(k=4\), and is positive for \(k\geq5\);
- \(p_{k,5}\) first exists and is positive at \(k=5\).

No formula is being used at a negative Newton index.

## 8. Sign audit

The shifted-polynomial proofs in Section 4 are valid.

- In (3), the bracket at \(k=x+3\) has coefficients
  \[
  12,116,301,12,
  \]
  all positive.
- In (4), the bracket at \(k=x+4\) has coefficients
  \[
  4,68,407,881,126,
  \]
  all positive.
- In (5), the bracket at \(k=x+5\) has all positive coefficients.
- In (6), the only negative shifted coefficient is
  \(-258741x\), and for integer \(x\geq1\),
  \[
  515348x^2-258741x>0.
  \]
  At \(x=0\), the bracket is \(9000>0\).

Together with the explicit prefactors, these prove all claimed signs.

## 9. Verifier and test independence

The verifier has three logically distinct parts:

1. **Profile samples.**  These substitute integer \(j\) into the exact
   Lagrange formulas and compare the selected power coefficient with the
   hard-coded \(R_{\ell,h}\).  This is exact and, with Lemma 1, sufficient.
2. **Symbolic convolution and Newton conversion.**  These independently
   perform the binomial moment calculation and triangular basis conversion.
   They directly audit (13) and (1)--(6).
3. **Direct Newton rows.**  These evaluate the same `profile` function at
   integer \(s\), form the same determinant, and take forward differences.
   This catches conversion and indexing errors but is not independent of
   (7)--(11).

The pytest file only invokes `audit` and checks output sizes.  The substantive
formula assertions live inside `audit`; therefore a formula failure still
fails pytest, but the test file itself does not provide a second
implementation.

The weighted-Cayley reconstruction in Section 6 supplies the missing
independent implementation for \(2\leq k\leq12\).  Direct edge-subset
enumeration in `independent_newton_audit_2026-07-30/` additionally checks
the prescribed-edge forest interpretation for \(4\leq s\leq7\).

## 10. Executed checks

The following repository tests passed:

```text
pytest -q \
  top_newton_tail_2026-07-30/test_verify_top_six_newton_tail.py \
  independent_newton_audit_2026-07-30/test_independent_verify_newton.py

2 passed
```

The top verifier was also run through \(k=16\):

```text
python3 verify_top_six_newton_tail.py --maximum-regression-k 16
```

It completed:

- 360 exact profile-identity checks;
- symbolic recovery of all six power coefficients;
- symbolic recovery of all six normalized Newton formulas;
- exact regression rows for \(k=2,\ldots,16\).

Finally, the independent weighted-Cayley recursion checked all existing
top-six entries for \(k=2,\ldots,12\).  No discrepancy was found.

## 11. Final claim status

The correct present claim is:

> For every \(k\geq2\), every existing coefficient among the six highest
> base-four Newton indices has the value stated in (1)--(6) and is
> nonnegative, with the sole zero \(p_{4,4}=0\).

This result concerns six fixed layers at the top of the coefficient array.
It does not control the linear-width middle and does not by itself prove
the full complete-split coefficientwise inequality or OPG-1757.
