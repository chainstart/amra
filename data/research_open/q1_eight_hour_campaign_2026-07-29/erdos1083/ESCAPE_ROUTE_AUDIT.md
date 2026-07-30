# Escape-route audit beyond Laurent lattice boxes

## 1. Exact target

For the actual SAT base service, put

\[
u(t)=\frac12(t-3069/t)+\frac32,\qquad
c(t)=\frac12(t+3069/t),\qquad Y=\frac{\sqrt{12285}}2.
\]

Both \((u(t),c(t)-Y)\) and \((u(t),-c(t)-Y)\) are compatible.  A genuine
escape from the Round 29 no-go theorem must produce

\[
\sum_{t\in T}r_A(u(t))
\bigl(r_A(c(t)-Y)+r_A(-c(t)-Y)\bigr)
\ge |A|^{12/5}.                                           \tag{1}
\]

If all displayed differences have multiplicity at least
\(\rho |A|\), this requires

\[
|T|\ge\frac{1}{2\rho^2}|A|^{2/5}.                         \tag{2}
\]

This weighted incidence condition is the standard used throughout this
audit.

## 2. Fixed algebraic number fields

Let all translation differences lie in a fixed number field \(K\), in a
fixed fractional-ideal lattice.  After clearing the fixed denominator,
the two factors of the hyperbola satisfy

\[
\mathfrak a\,\mathfrak b=(R)
\]

at the ideal level.  There are only the ideal divisors of the fixed ideal,
and elements generating the same ideal differ by a unit.  Dirichlet's unit
theorem puts the units in a lattice of rank
\(r_K=r_1+r_2-1\).  The number with coefficient or archimedean height at
most a polynomial in \(n\) is

\[
O_K((\log n)^{r_K}).
\]

If the cleared denominator varies, the ideal-divisor factor contributes
the same
\(\exp(O(\log n/\log\log n))\) scale as Round 29, provided the containing
box pays its norm.  Thus fixed-degree, bounded-complexity algebraic fields
remain \(n^{o(1)}\).

### Executable quadratic-field check

For

\[
A_L=\{i+jY:0\le i,j<L\},
\]

exact coefficient comparison leaves only

\[
(u,v)=(0,0),(0,-2Y),(3,0),(3,-2Y)
\]

once \(L\ge4\).  Hence

\[
H(A_L)=L^2(2L-3)(2L-2),\qquad
\frac{H(A_L)}{|A_L|^2}\longrightarrow4.                  \tag{3}
\]

The verifier checks (3) through \(L=14\).

The unit experiment in \(\mathbb Q(\sqrt2)\) counts powers of
\(3+2\sqrt2\) in coefficient boxes up to \(10^{16}\); the count grows
linearly in the logarithm of the box height, as predicted by the
rank-one unit lattice.

## 3. Polynomial and rational parametrizations

The factor form is \(p(z)q(z)=R\).  In a polynomial ring over a field, the
only units are nonzero constants.  Therefore a polynomial
parametrization with both factors polynomial is constant.  Every
nonconstant parametrization must be rational or Laurent:

- Laurent monomials are covered by Round 29;
- rational functions introduce denominator ideals;
- clearing those denominators returns to ideal-divisor counting.

Thus fixed-degree polynomial/rational parametrizations do not supply a
power-law escape.

There is also a sharp rank-two GAP check.  Let
\(A=\{i+j\theta\}\).  If \(\theta\) is transcendental or has degree greater
than two over \(\mathbb Q(Y)\), write

\[
u=x+y\theta,\qquad v=z+w\theta.
\]

The \(\theta^2\) coefficient gives \(w=\pm y\).  The \(\theta\) coefficient,
together with \(X\ne\pm Y\), forces \(y=w=0\).  The constant coefficient
then leaves only

\[
(u,v)=(0,0),(3,0).
\]

The average is below two.  If \(\theta\) has bounded algebraic degree, the
fixed-field ideal/unit argument applies instead.

## 4. Several different divisor layers

Suppose generic layers have sizes \(n_i\) and average degrees \(D_i\).  A
disjoint union has

\[
D_{\rm union}-1
=\frac{\sum_i n_i^2(D_i-1)}{(\sum_i n_i)^2}
\le\max_i(D_i-1).                                        \tag{4}
\]

An independent additive tensor has

\[
D_{\rm tensor}-1=\sum_i(D_i-1),\qquad
n_{\rm tensor}=\prod_i n_i.                               \tag{5}
\]

Thus different \(N_i\)'s dilute under union and add under tensor.  If the
layers are commensurable and deliberately cross-coupled, clearing a common
denominator replaces them by one factor equation \(xy=N_*\).  The size of
the common refinement pays for \(N_*\), and the divisor bound returns.

The executable mass ledger verifies (4)--(5) exactly for arbitrary
rational inputs.

## 5. Multiplicative subgroups

For a fixed finitely generated multiplicative group, exponent vectors form
a fixed-rank lattice.  Bounded-height elements are polylogarithmic in the
height bound.  Fixed-rank groups therefore fall under the unit or Laurent
obstruction.

The exact rational experiment takes all divisors of a primorial \(D\) as
parameters.  Relative to the lattice step \(1/(2D)\), the two parameter
coordinates are

\[
Dt-3069D/t+3D,\qquad Dt+3069D/t.
\]

A one-dimensional box twice the largest shift makes every corresponding
difference popular by a constant proportion.  It produces genuine growth,
but

\[
|T|=\tau(D),\qquad |A|=D^{O(1)},
\]

so the result is again
\(\exp(\Theta(\log n/\log\log n))\).  Exact experiments for the first two
through seven primes certify every overlap.

## 6. Low-dimensional GAPs

The evidence now separates three cases:

1. Generic generators: coefficient comparison leaves only fixed solutions.
2. Generators in a fixed number field: ideal divisors times units give
   \(n^{o(1)}\).
3. Commensurable rational or Laurent generators: integer divisors give
   \(n^{o(1)}\).

What is not proved is a uniform theorem for GAPs whose rank, generated
field degree, discriminant, and multiplicative rank all grow with \(n\).
Such a family may evade a single common lattice normalization.

## 7. The one genuine uncovered candidate

The remaining candidate is a growing-degree/growing-rank multiplicative
set \(\Gamma_n\), not commensurable inside one bounded-complexity
fractional ideal, together with a small-doubling set \(A_n\), such that a
set \(T_n\subset\Gamma_n\) satisfies (1).

This is quantitatively nontrivial only if:

- \(|T_n|\ge n^{2/5-o(1)}\);
- both images \(u(T_n)\) and \(c(T_n)\pm Y\) lie in popular difference
  sets of the *same* \(A_n\);
- the translations cannot be properized into \(O(\log n)\) independent
  Laurent frequencies or one integer/ideal factor equation of norm
  \(n^{O(1)}\).

No explicit family meeting these conditions was found.  The candidate is
genuinely outside the current no-go theorem, but the rational S-unit and
fixed-field experiments are negative evidence.

## 8. Final classification

| Route | Outcome |
|---|---|
| Fixed algebraic number field | ideal divisors × units, \(n^{o(1)}\) |
| Polynomial parametrization | constant; Laurent/rational returns to old bound |
| Several \(N\) layers | union dilutes, tensor adds, common refinement divides |
| Fixed-rank multiplicative subgroup | polylogarithmic height count |
| Rational high-rank subgroup | divisor scale, experimentally certified |
| Fixed-rank GAP, generic generator | constant solutions |
| Fixed-rank GAP in fixed field | \(n^{o(1)}\) |
| Growing-degree, noncommensurable hybrid | genuinely uncovered target (1) |

The next work should focus only on the last row.  Repeating searches in the
other rows cannot close a polynomial exponent gap.

## Reproducibility

```bash
python3 verify_escape_route_audit.py
pytest -q test_verify_escape_route_audit.py
```
