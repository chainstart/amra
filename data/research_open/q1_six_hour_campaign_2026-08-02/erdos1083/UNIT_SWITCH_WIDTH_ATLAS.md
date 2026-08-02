# Erdős #1083: the augmentation-unit residual is a subset-sum height atlas

Date: 2026-08-02

## 0. Result

The heavy-skeleton theorem gives a common-tangent family \(L'\) of
size

\[
 K:=|L'|\ge t^{\beta+o(1)},\qquad
 \beta=0.2610894430\ldots,
\tag{0.1}
\]

and factorizations in one Laurent UFD

\[
 F_j=P_{\lambda_jX}=HE_j,\qquad
 |H(1)|=S,\qquad |E_j(1)|=1.
\tag{0.2}
\]

This note quantifies the surviving \(E_j\)'s.  Put

\[
 B=P_{A_0}/H.
\tag{0.3}
\]

Then every \(E_j\mid B\), and all irreducible factors of \(E_j\)
have augmentation magnitude one.

Assume \(K\ge3\).  Let \(R_{\rm unit}(B)\) denote the number, with multiplicity, of
nonconstant irreducible factors \(G\mid B\) satisfying
\(|G(1)|=1\).  Then

\[
 \boxed{
 R_{\rm unit}(B)
 \ge
 \log_2\left(\max\left\{1,\frac{K-2}{2}\right\}\right).}
\tag{0.4}
\]

At the endpoint this is

\[
 R_{\rm unit}(B)
 \ge(\beta+o(1))\log_2t.
\tag{0.5}
\]

More concretely, pass to at least \(K/2\) leaves on which the distinct
scalars \(\lambda_j\) have one sign.  If

\[
 D=\max X-\min X,\qquad a=\operatorname{wd}(H),
\tag{0.6}
\]

and \(d_\nu>0\) are the numerical widths of the augmentation-unit
factor occurrences of \(B\), then each such leaf has a multiplicity
vector \(\epsilon_j\) for which

\[
\begin{aligned}
 b_j&=\operatorname{wd}(E_j)
      =\sum_\nu\epsilon_{j,\nu}d_\nu,\\
 |\lambda_j|&=\frac{a+b_j}{D},\\
 |z_j|&=\frac{a+b_j}{2\rho D},\\
 w_j&=\frac{\sigma hD}{a+b_j}
 \qquad(\sigma=\operatorname{sgn}\lambda_j).
\end{aligned}
\tag{0.7}
\]

The \(b_j\)'s are distinct.  Thus the ruled-chart parameters \(w_j\)
are reciprocals of \(K/2\) distinct weighted subset sums from one
common augmentation-unit factor multiset.

This is a strictly more explicit form of the denominator-free ruled
chart.  It also exposes a sharp obstruction: arithmetic-progression
source masks admit arbitrarily many such positive scalar copies
through cyclotomic augmentation-unit switches.  Therefore positivity
of the source masks and of the common centre complement alone cannot
bound the atlas; the still-unused input is positivity of **every**
leaf complement together with the common-tangent Euclidean
realization.

## 1. Residual divisor count

Since \(F_j\mid P_{A_0}\) and \(F_j=HE_j\), cancellation in the
domain gives

\[
 E_j\mid B.
\tag{1.1}
\]

Factor the augmentation-unit part of \(B\) as

\[
 \prod_{\nu=1}^rG_\nu^{m_\nu},
\qquad |G_\nu(1)|=1.
\tag{1.2}
\]

Write

\[
 R_{\rm unit}(B)=\sum_{\nu=1}^rm_\nu.
\tag{1.3}
\]

Up to Laurent associates, a divisor supported on these factors is
specified by an exponent vector

\[
 (e_1,\ldots,e_r),\qquad 0\le e_\nu\le m_\nu.
\tag{1.4}
\]

The number of possibilities is

\[
 \prod_{\nu=1}^r(m_\nu+1)
 \le\prod_{\nu=1}^r2^{m_\nu}
 =2^{R_{\rm unit}(B)}.
\tag{1.5}
\]

The support audit in `HEAVY_SKELETON_RULED_CHART.md` proves that
every residual associate class contains at most two distinct row
scalars.  At most two leaves have unit residual.  Hence the nonunit
residuals occupy at least

\[
 \frac{K-2}{2}
\tag{1.6}
\]

associate classes.  Equations (1.5)--(1.6) prove (0.4).  For
\(K=3,4\), the displayed logarithmic bound is merely the trivial
nonnegative bound; its endpoint use has \(K\to\infty\).

This is a factor-occurrence bound, not a bound for distinct
irreducibles.  Repeated factors are deliberately counted with
multiplicity.

## 2. Numerical width linearizes the scalar parameters

For a nonzero Laurent polynomial

\[
 P=\sum_{\gamma\in\Gamma}c_\gamma[\gamma]
\]

with real exponents, define

\[
 \operatorname{wd}(P)
 =\max\{\gamma:c_\gamma\ne0\}
  -\min\{\gamma:c_\gamma\ne0\}.
\tag{2.1}
\]

The usual order on \(\mathbb R\) makes extreme exponents unique.
For nonzero \(P,Q\), the minimum exponent of \(PQ\) is the sum of
the two minimum exponents, with nonzero coefficient; similarly for
the maximum.  Therefore

\[
 \boxed{\operatorname{wd}(PQ)
 =\operatorname{wd}(P)+\operatorname{wd}(Q).}
\tag{2.2}
\]

This identity is immune to all interior coefficient cancellation,
including the signed-quotient firewall.

Every nonconstant irreducible Laurent factor has positive numerical
width.  List the augmentation-unit factor occurrences of \(B\) and
their widths as

\[
 d_1,\ldots,d_R>0.
\tag{2.3}
\]

Because \(E_j\mid B\), unique factorization and (2.2) give

\[
 \operatorname{wd}(E_j)
 =\sum_{\nu=1}^R\epsilon_{j,\nu}d_\nu,
\qquad \epsilon_{j,\nu}\in\{0,1\},
\tag{2.4}
\]

after repeated occurrences are labelled.  On the other hand,

\[
 \operatorname{wd}(F_j)
 =\operatorname{wd}(P_{\lambda_jX})
 =|\lambda_j|D.
\tag{2.5}
\]

Equations (0.2), (2.2), and (2.5) prove the first three identities
in (0.7).

Choose one sign \(\sigma\) containing at least \(\lceil K/2\rceil\)
scalars.
The row scalars are distinct, so their absolute values, and hence the
subset sums \(b_j\), are distinct on this subfamily.  Finally the
common Newton direction obeys \(h=\lambda_jw_j\), which proves the
last identity in (0.7).

The same formula gives a literal distance interpretation.  For two
selected common-tangent targets,

\[
 \|q_{j,\tau_0}-q_{k,\tau_0}\|^2
 =\frac{(b_j-b_k)^2}{4\rho^2D^2}.
\tag{2.6}
\]

Fixing the smallest \(b_j\) yields at least \(K/2-1\) distinct
target--target distances.  This is sharp for arbitrary collinear
points and far below the \(t^3\) target, but it identifies exactly
which subset-difference set a stronger argument must expand.

The source--target cells become the additive-parameter parabolic
chart

\[
 \rho^2+\tau_0+
 \frac{(a+b_j)^2}{4\rho^2D^2}
 +\frac{\sigma(a+b_j)}D X.
\tag{2.7}
\]

## 3. Sharp positive-mask boundary: cyclotomic scalar switches

The subset-sum atlas cannot be bounded using only the facts that
\(F_j\) and \(P_{A_0}\) are positive \(0/1\) masks.

Fix a prime \(S\), and let

\[
 X=\{0,1,\ldots,S-1\},
\qquad
 F_m(x)=P_{mX}
       =1+x^m+\cdots+x^{(S-1)m}.
\tag{3.1}
\]

If \(\gcd(m,S)=1\), every nontrivial \(S\)-th root of unity remains
nontrivial after raising to the \(m\)-th power.  Consequently

\[
 F_1\mid F_m,\qquad
 E_m:=F_m/F_1\in\mathbb Z[x],\qquad
 E_m(1)=1.
\tag{3.2}
\]

Now choose \(M\) coprime to \(S\).  Whenever \(m\mid M\), the quotient
\(M/m\) is also coprime to \(S\), and the same root argument gives

\[
 F_m\mid F_M.
\tag{3.3}
\]

If \(M\) is the product of \(k\) distinct primes not dividing \(S\),
the positive \(S\)-term mask \(F_M\) is divisible by the \(2^k\)
different positive scalar-copy masks \(F_m\), one for every
\(m\mid M\).  Since \(S\) is prime, \(F_1=\Phi_S\) is irreducible
with augmentation \(S\); it is exactly the common heavy skeleton.
All variation is carried by \(E_m(1)=1\).

To prescribe a larger centre-complement size \(U=SC\), multiply
\(F_M\) by a \(C\)-term mask in an independent variable.  The result
is still a positive \(U\)-term mask and is still divisible by all
\(F_m\).  Taking \(C<S\) respects \(U<S^2\).

This is an exact counterexample to any claim that:

- positive source masks;
- a positive common complement of size \(U<S^2\);
- common heavy augmentation \(S\); and
- scalar-copy support

alone bound the number of augmentation-unit switches.

It is **not** an exact common-spectrum #1083 block: it does not
construct positive leaf complements \(A_j\) with
\(P_V=P_{A_j}F_j\) for all \(j\), nor the required Euclidean tangent
sets.  Those are now the precise remaining inputs.

## 4. Audited interface

The strengthened exact chain is

```text
fixed-tangent exact transverse windmill
 -> heavy skeleton H on t^(beta+o(1)) rows
 -> one residual B with Omega(log t) augmentation-unit factors
 -> t^(beta+o(1)) distinct weighted subset sums b_j
 -> height chart z_j = sign*(a+b_j)/(2 rho diam(X))
 -> reciprocal parameters w_j = sign*h*diam(X)/(a+b_j).
```

Quantifier firewalls:

- factor occurrences, not only distinct factors, are counted;
- repeated irreducibles are handled by exponent vectors;
- \(C=U/S\) is an integer because one transverse leaf already gives
  \(F_j\mid P_{A_0}\);
- every residual associate class has at most two rows, not just the
  unit class;
- numerical width is used only after passing to one scalar sign;
- the \(K/2-1\) distance gain is recorded but not inflated to the
  \(t^3\) global target;
- the cyclotomic family tests exactly which positivity assumptions
  remain insufficient.

## 5. Reproduction

```bash
python3 verify_unit_switch_width_atlas.py
python3 -m unittest -v test_unit_switch_width_atlas.py
```

The verifier checks factor-occurrence counting, width additivity,
the height/distance identities, and a finite cyclotomic scalar-switch
family.  The all-parameter statements are proved above.
