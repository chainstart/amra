# OPG-1757: independent audit of the all-rank saddle-pole and degree argument

Date: 2026-07-30

## 0. Verdict

The all-rank MD2 Laurent cancellation passes the independent audit.
No counterexample or algebraic error was found in the Bell support,
the Gamma correction, the exceptional-profile cancellation, the
low-rank marked identities, the determinant convolution, or the final
coefficient extraction.

The final verdict on the cubic upper-degree theorem is

\[
\boxed{\texttt{PASS}.}
\]

The first audit correctly rejected an attempted endpoint extraction
and recorded an all-rank localization obligation.  That obligation
has since been discharged by the genuine complement-length identity
in `COMPLEMENTARY_ENDPOINT_LOCALIZATION_LEMMA.md`.  Its normalization,
saddle selection, Poincare matching, and \(x=1\) continuation pass the
separate independent audit
`COMPLEMENTARY_ENDPOINT_LOCALIZATION_INDEPENDENT_AUDIT.md`.

The independent executable certificate is
`independent_verify_all_rank_saddle_pole_valuation.py`.  It does not
import `verify_md2_laurent_identity.py`,
`verify_saddle_pole_orders.py`, or
`verify_all_rank_degree_localization.py`.

## 1. Bell support and the small-rank boundary

Write \(m\) for the amplitude-derivative order and \(n_p\) for the
multiplicity of the phase part indexed by \(p\).  The pole defect of a
configuration is
\[
d(m,(n_p))
=
\begin{cases}
0,&m=0,\\
m-1,&m\ge1,
\end{cases}
+
\sum_{p\ge2}
\left(p-1+\mathbf 1_{2\mid p}\right)n_p.
\]
Thus a part \(p\ge4\) already has defect at least four.  At defect at
most three, \(n_2,n_3\in\{0,1\}\), and direct enumeration gives exactly
the following eleven configurations:
\[
\begin{array}{c|c}
d&(m,n_2,n_3)\\ \hline
0&(0,0,0),(1,0,0)\\
1&(2,0,0)\\
2&(0,1,0),(0,0,1),(1,1,0),(1,0,1),(3,0,0)\\
3&(2,1,0),(2,0,1),(4,0,0).
\end{array}
\]

The saddle constraint is
\[
n_1=2r-m-2n_2-3n_3.
\]
For \(r\ge3\), all eleven configurations are feasible.  At \(r=2\),
only \((m,n_2,n_3)=(2,0,1)\) gives \(n_1=-1\).  Its polynomially
continued factorial ratio contains the factor
\[
\frac{(2r)!}{(2r-5)!}
=(2r)(2r-1)(2r-2)(2r-3)(2r-4),
\]
which vanishes at \(r=2\).  Hence the symbolic all-\(r\) identity does
not introduce a spurious small-rank term.

## 2. Gamma budget

A Gamma term of rank \(j\) lowers the integral rank by \(j\), losing
three leading \(W\)-pole orders.  Therefore a Laurent window of defect
at most three permits only \(\Gamma_0\) and \(\Gamma_1\).  The latter
can occur only in the defect-three layer.

Starting directly from \(B_2(z)=z^2-z+1/6\), the critical value is
\[
\Gamma_1^{(a)}(0)
=\frac1{12}+\frac a2-\frac{a^2}{2},
\]
in agreement with the claimed value.  No higher Gamma correction can
enter any of the four audited Laurent layers.

## 3. Main and exceptional Laurent layers

The main integral was independently reconstructed from exponential
partitions, amplitude derivatives, Gaussian moments, and the single
allowed Gamma correction.  Its second marked difference is
\[
\left(
0,\,
0,\,
\frac{24r}{(6r-5)(6r-1)},\,
\frac{24r(12r-11)}
{(6r-7)(6r-5)(6r-1)}
\right).
\]

The exceptional normalization gives independently
\[
\frac{4K^*_{r-1}}{K_r}
=-\frac{24r}{(6r-5)(6r-1)}.
\]
Its next layer is the exact negative of the fourth main layer.
Consequently all four total Laurent coefficients vanish identically
in \(r\).

This verifies the strengthened marked difference
\[
\varepsilon_r
=C_{2,r}-2C_{1,r}+C_{0,r}
\in W^{-(3r-4)}\mathbb Q[x]
\qquad(r\ge2)
\]
at its only high-risk saddle boundary \(W=0\), subject to the separate
endpoint-localization point in Section 7 below.

## 4. Low ranks and the repaired quantifier

The earlier MD2 presentation stated the identity for \(r\ge2\) but
the determinant argument used \(\varepsilon_b\) without first
excluding \(b=0,1\).  The total theorem now repairs this by proving
\[
\varepsilon_0=\varepsilon_1=0.
\]

Independently,
\(\varepsilon_0=1-2+1=0\), and substituting the printed rank-one
profiles into \(C_{2,1}-2C_{1,1}+C_{0,1}\) gives zero identically.
Thus the old quantifier gap has been closed and is not a current
theorem defect.

## 5. Determinant convolution and derivatives

The first determinant sum is antisymmetric only after summing the
complete convolution \(a+b=n\) and relabelling \(a\leftrightarrow b\).
It is generally false for one fixed pair \((a,b)\).  Independent tests
with arbitrary polynomial profile families verify the full
antisymmetry through total rank five and the vanishing of even
derivatives at \(x=1/2\).

For the remaining terms:

- \(\delta_0=0\) forces both ranks in
  \(\delta_a\delta_b\) to be positive, giving two pole-order gains on
  each side;
- \(\varepsilon_0=\varepsilon_1=0\) forces the second-difference rank
  to be at least two, where the four-order MD2 gain applies; and
- every \(x\)-derivative can add at most one pole after
  \(u=tx,\ v=t(1-x)\).

The last rule was checked exactly for all left/right pole pairs
between zero and four and derivative orders zero through six.  These
checks support
\[
\operatorname{pole}_{t=1}
\partial_x^mG_n(1/2,t)\le3n-5+m.
\]

## 6. The repaired removable \(t^4\) factor

The earlier text attributed \(t^4\mid H_n(t)\) only to the external
\(t^n\) in \(G_n\), overlooking the \(G_a\) terms with \(a<n\).  The
revised theorem now gives the correct central-summand argument.  In
the recurrence
\[
H_n
=
\sum_{a=2}^{n}
\sum_{\substack{0\le m\le2(n-a)\\m\ {\rm even}}}
\frac{\mu_{m,n-a}}{m!}
\partial_x^mG_a(1/2,t).
\]
If \(a=n\), the external factor is \(t^n\), which suffices for
\(n\ge4\).  If \(a<n\), then
\(\mu_{0,n-a}=0\), so every nonzero summand has even \(m\ge2\).
The chain rule supplies \(t^m\), while \(a\ge2\), and therefore
\[
t^{a+m}\mid\partial_x^mG_a(1/2,t),
\qquad a+m\ge4.
\]
This is the appropriate all-\(n\) proof and it now appears in the
theorem.  Together with the exact \(n=2,3\) identities, the
removability claim passes.

## 7. Endpoint-localization obligation: historical defect and resolution

The defect recorded below applied to the first attempted endpoint
sublemma and remains useful as a red-team record.  It is not a defect
of the current theorem.  The replacement starts from
\[
{\cal S}_s(J,Q)
=\sum_i\frac{J_{\underline i}Q_{\underline i}}{i!}
\left(-\frac1{2s}\right)^i
\]
and the exact complementary coefficient identity
\[
\frac{{\cal S}_s(J,Q)}{Q!}
=[u^Q]e^u(1-u/(2s))^J.
\]
This really changes the finite coefficient length from \(J\) to
\(Q=s-a-J\).  The resulting saddle at \(v=1\) agrees with the original
branch on \(0<x<1/2\), has Hessian \(1-2x\), and remains nondegenerate
at \(x=1\).  The main and exceptional profiles have separate exact
formulas.  Thus the old obligation is resolved for every rank.

### Rejected first attempt

The revised endpoint sublemma in
`ALL_RANK_ORDINARY_SYMBOL_DEGREE_THEOREM.md` is a material improvement:
it indexes a main term by
\[
\lambda=(a,b,m;(n_p)_{p\ge1}),
\quad
a+b=r,
\quad
m+\sum p n_p=2b,
\]
and derives the uniform finite degree bound \(4r+2\).

The remaining gap is the passage to its displayed equation (5f).
For a main profile with shift \(\alpha\), direct substitution of
\(D=E(\cdot,j)-E(\cdot,j-1)\) first gives
\[
\frac{(s-\alpha)_{\underline j}}{s^j}
\left\{
L_j(s-\alpha-j)
-\frac{2j}{s}L_{j-1}(s-\alpha-j)
\right\},
\]
where
\[
L_J(c)
=\sum_{i=0}^{J}\binom Ji2^{J-i}(-1)^i
\frac{(c)_{\underline i}}{s^i}.
\]
Identity (5c) evaluates each coefficient of \(L_J\) as a
falling-factorial polynomial.  It does not by itself produce the
subtracted transform value inside the claimed principal-part formula
\[
\sum_{i=0}^{J_e}\binom{J_e}{i}2^{J_e-i}(-1)^i
(i)_{\underline v}
-(-1)^v(J_e)_{\underline v}.
\]
Each brace is indeed zero.  However, the manuscript does not yet
display how the normalized exact formulas
\[
U_{0,j},\quad U_{1,j},\quad U_{2,j},
\qquad D=E-E(\,\cdot\,,\,\cdot\,,j-1),
\]
produce that subtracting falling-factorial term for every
\(\lambda,h,e,p\).  Without that map, (5f) contains the substantive
principal-part cancellation as an asserted extraction.

There is a second, more concrete indexing problem.  Replacing \(i\)
by \(j-i\) leaves the summation range \(0\le i\le j\); it does not
replace it by \(0\le i\le s-j\).  Hence the sentence assigning
\(J_1=s-j\) at the endpoint \(x=1\) does not follow from the stated
change of variables.  The exceptional term has upper index \(j-1\),
so its reversed range is still \(0,\ldots,j-1\), not
\(0,\ldots,s-j\).  A genuine complementary finite-sum identity, if
available, must be written down and proved.

The exceptional normalized term is explicitly of the form
\[
\frac{8j}{s^2}
\frac{(s-4)_{\underline{j-1}}}{s^{j-1}}
L_{j-1}(s-3-j).
\]
It is not indexed by the main tuple \(\lambda\) in (5d).  Therefore
the statement that one family of rational constants
\(q_{\lambda,v}\) covers all three profiles also needs an exceptional
tag or a separate formula.  Moreover, the coefficients
\(d_{\alpha,\ell,v}(J)\) in (5b) depend polynomially on \(J\);
calling the later \(q_{\lambda,v}\) rational constants requires the
missing endpoint-coefficient extraction.

A publication-ready closure would add one formula before (5f):
substitute the exact \(U/E/D\) definitions, identify the two
contributions that pair into the brace, and give the resulting
\(q_{\lambda,v}\) (or an explicit recurrence defining it).  This
would turn the current accurate proof sketch into a self-contained
all-rank localization proof.

No finite-rank counterexample was found; the existing exact finite
localization certificate passes through rank five.  The obligation is
therefore about the all-rank proof, not contrary computational
evidence.

The complementary coefficient identity displayed at the start of this
section supplies exactly the missing length-\(Q\) formula, without
trying to manufacture the invalid braces above.  The exceptional
profile is handled separately.  Hence this historical objection no
longer conditions the verdict.

## 8. Infinity and the exceptional profile

The infinity conclusion needed by Lemma 2 is boundedness, and that
conclusion is consistent with the saddle recurrence.  One displayed
intermediate assertion should nevertheless be corrected.

For the signed Gamma list
\[
\{(1,x,1),(1,1,1-a),(-1,1-x,1-a)\},
\]
the logarithmic rank-\(n\) coefficient contains the term
\(B_{n+1}(1-a)\) with denominator \(1^n\).  It generally approaches a
nonzero constant as \(x\to\infty\).  Thus a Gamma monomial of rank
\(a\) is \(O(1)\), not generally \(O(x^{-a})\).

This does not spoil the localization conclusion: an integral
rank-\(b\) Bell monomial is \(O(x^{-b})\), the Gamma factor is bounded,
and the exceptional multiplier \(8x/W\) is also bounded.  Every
profile is therefore \(O(1)\), which is all that is needed to obtain
\(\deg p\le q\) once the finite-pole claim is proved.

## 9. Final degree extraction and quantifiers

With profile localization now proved, the remaining degree argument is
correct.  If
\[
B_r(t)=\frac{N_r(t)}{(1-t)^{3r+1}},
\qquad
\deg N_r\le4r,
\qquad
t^r\mid N_r,
\]
then for every \(d\ge r\), coefficient extraction gives a polynomial
in \(d\) of degree at most \(3r\).  Terms with numerator exponent
\(j>d\) vanish because
\[
0\le j-d-1\le (4r)-(r)-1=3r-1,
\]
so the generalized binomial factor has an upper argument among
\(0,\ldots,3r-1\).  Independent exact regression through ranks zero
to five agrees with direct series extraction.

The central-binomial propagation also has the correct fixed-rank
quantifiers.  For each summand of \(H_n\),
\(a\le n\) and \(m\le2(n-a)\), so its \(t=1\) pole is at most
\(3n-5\).  Differentiating a localized profile after substituting
\(z=tx\) preserves \(O(t^{1/2})\) after the chain-rule power is
included, so a differentiated product is \(O(t)\) and the summand is
\(O(t^{a+1})\subseteq O(t^{n+1})\).  No uniformity in unbounded
derivative order is required: \(n\) is fixed in each coefficient.

## 10. Falling-triangle corollary

`ORDINARY_ALL_RANK_FALLING_TRIANGLE_COROLLARY.md` is correct
as a consequence of Theorem 1.

Comparing the coefficient of \(n^{d-\ell}\) gives the stated
triangular recurrence because
\[
[n^{d-\ell}](n+2)^{d-r}
=\binom{d-r}{\ell-r}2^{\ell-r},
\]
and
\([n^{d-\ell}](n)_{\underline{d-j}}
=s_{\ell-j}(d-j)\).
The degree induction then gives
\(\deg\mathfrak h_j\le3j\).

For \(j\le d\le2j-1\), the falling degree
\(d-j\) lies below \(\lceil d/2\rceil\), so the Poisson transform
forces \(h_{d,j}=0\).  Since all symbol polynomials used there satisfy
\(d\ge j\ge r\), no polynomial extension is evaluated outside the
range supplied by the main theorem.  These are exactly the \(j\)
roots \(j,\ldots,2j-1\).

The long-recurrence triangular identity has the correct shifts.  Its
finite difference lowers the degree by one, giving
\(\deg\mathfrak g_q\le3q+2\).  At \(d=2q\), both leading
\(\mathfrak h_{q+1}\) terms and every remaining
\(\mathfrak h_{q-i}(2(q-i)-1)\) term lie in their forced-zero ranges.
Thus \((d-2q)\mid\mathfrak g_q(d)\) for \(q\ge1\).  No all-rank
positivity or real-rootedness conclusion is silently added.

## 11. Reproduction

Run

```bash
python3 independent_verify_all_rank_saddle_pole_valuation.py
pytest -q \
  test_independent_verify_all_rank_saddle_pole_valuation.py \
  test_verify_md2_laurent_identity.py \
  test_verify_saddle_pole_orders.py \
  test_verify_all_rank_degree_localization.py \
  test_verify_all_rank_falling_triangle_corollary.py
```

At the time of this audit, the combined suite reports

```text
11 passed in 29.05s
```
