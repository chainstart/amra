# OPG-1757: leading coefficients of the long recurrence

Date: 2026-07-30

## 0. Status

This note gives the exact all-rank generating identity for the leading
coefficients of the long-recurrence bands.  It reduces their
positivity to a logarithmic-coefficient problem.  That problem is
subsequently solved in
`ORDINARY_ALL_RANK_RECURRENCE_LEADING_POSITIVITY_THEOREM.md`.

The exact finite search through bands \(0,\ldots,299\) remains a
redundant certificate; it is no longer the only sign evidence.

## 1. Leading triangle

Put
\[
L_j=[d^{3j}]\mathfrak h_j(d),\qquad L_0=1,
\tag{1}
\]
and, allowing the value zero if the degree bound is not sharp, put
\[
G_q=[d^{3q+2}]\mathfrak g_q(d).
\tag{2}
\]
The falling-triangle theorem proves
\[
(-1)^jL_j>0.
\tag{3}
\]

Take degree \(3q+2\) in the exact triangular recurrence
\[
\mathfrak g_q(d)
=\mathfrak h_{q+1}(d)-\mathfrak h_{q+1}(d+1)
-\sum_{i=0}^{q-1}
\mathfrak g_i(d)\mathfrak h_{q-i}(d-1-2i).
\]
The finite difference contributes
\[
-3(q+1)L_{q+1},
\]
and shifts in the product factors do not change their leading
coefficients.  Hence
\[
\boxed{
G_q+\sum_{i=0}^{q-1}G_iL_{q-i}
=-3(q+1)L_{q+1}.
}
\tag{4}
\]

Define formal power series
\[
H(z)=\sum_{j\ge0}L_jz^j,\qquad
\widetilde G(z)=\sum_{q\ge0}G_qz^{q+1}.
\tag{5}
\]
Taking the coefficient of \(z^{q+1}\) in the product gives the exact
all-rank identity
\[
\boxed{
\widetilde G(z)H(z)=-3zH'(z),
\qquad
\widetilde G(z)=-3z\frac{H'(z)}{H(z)}.
}
\tag{6}
\]

## 2. Exact positivity reduction

Since \(H(0)=1\), formal logarithms are valid.  Equation (6) gives
\[
\boxed{
G_{n-1}=-3n[z^n]\log H(z)
\quad(n\ge1).
}
\tag{7}
\]
Thus every long-band leading coefficient is positive if and only if
\[
[z^n]\log H(z)<0
\quad(n\ge1).
\tag{8}
\]

Equivalently, let
\[
F(z)=H(-z)=\sum_{j\ge0}\lambda_jz^j,
\qquad
\lambda_j=(-1)^jL_j>0.
\]
Then (8) is
\[
\boxed{
(-1)^{n+1}[z^n]\log F(z)>0
\quad(n\ge1).
}
\tag{9}
\]
Positivity of the coefficients \(\lambda_j\) alone does not imply
(9).  For example, \(F(z)=1+z+10z^2\) already has a positive
quadratic logarithmic coefficient instead of the required negative
one.  A new structural property of this particular \(F\) is needed.

A sufficient, but currently unproved, route would be a genus-zero
canonical product
\[
H(z)=\prod_k(1-z/\rho_k),\qquad \rho_k>0:
\]
then
\[
-zH'(z)/H(z)
\]
has positive Taylor coefficients as sums of reciprocal powers of
the zeros.  Establishing such a zero theorem is at least comparable
to the unresolved analytic compatibility/real-rootedness step and is
not supplied by the falling-triangle degree theorem.

## 3. Independent formula for \(L_j\)

The highest-Laurent-layer theorem makes the search independent of
finite falling-polynomial interpolation.  Put
\[
\begin{aligned}
c_0&=1,\\
c_r&=\frac{(-1)^{r+1}(6r-3)!!}{9^r(2r)!},\\
d_r&=-\frac{6r}{6r-5}c_r,\\
e_0&=e_1=0,\qquad e_r=-6(r-1)c_{r-1}\quad(r\ge2).
\end{aligned}
\tag{10}
\]
Then
\[
A_n=\sum_{a+b=n}(d_ad_b-c_ae_b),
\qquad
\boxed{
L_j=\frac{A_{j+2}}{2(3j)!}.
}
\tag{11}
\]
Equations (4) and (10)--(11) compute every \(G_q\) exactly.

The first values are
\[
\begin{aligned}
(G_0,G_1,G_2,G_3,G_4)
=\biggl(
\frac{11}{6},\
\frac{341}{432},\
\frac{74317}{186624},\
\frac{13629341}{67184640},\
\frac{175122877}{1693052928}
\biggr).
\end{aligned}
\tag{12}
\]
They agree with the independently derived first five full bands.

## 4. Finite counterexample search

`verify_long_recurrence_leading_reduction.py` uses exact rational
arithmetic and only (4), (10), and (11).  It finds
\[
G_q>0\qquad(0\le q\le299).
\tag{13}
\]
This is evidence, not proof of (8)--(9).  The script records a SHA-256
digest of all exact fractions so that the search is reproducible
without placing hundreds of large numerators in this note:

```bash
python3 verify_long_recurrence_leading_reduction.py \
  --maximum-band 299
pytest -q test_verify_long_recurrence_leading_reduction.py
```

The subsequent dominant-zero/Jensen proof establishes (9) in every
degree.  The verifier here remains useful as an independent finite
reconstruction of the coefficients.
