# OPG-1757: uniform endpoint polynomiality and denominator cancellation

Date: 2026-07-31

Status: `PROVED__ALL_ENDPOINTS__ALL_FIXED_DEFICIT_DENOMINATORS_CANCEL`

## 1. The theorem

For \(h\in\{0,1,2\}\), excess \(e\ge0\), and component count \(c\ge1\),
recall
\[
Q_{h,e,c}(s)
=\frac{H_{h,e,c}(s)}{2^h s^{s-h-2c-e}}.
\tag{1}
\]
Then
\[
\boxed{Q_{h,e,c}(s)\in\mathbb Q[s]}
\tag{2}
\]
for every endpoint parameter.  Combining (2) with the inherited degree
bound and the nonzero leading term gives
\[
\boxed{
\deg Q_{h,e,c}=2c+2e-2.
}
\tag{3}
\]

Consequently, in every fixed-deficit normalization
\[
C_{q,r}(s)=\frac{R_{q,r}(s)}{s^r},
\]
the denominator cancels:
\[
\boxed{
C_{q,r}(s)\in\mathbb Q[s],
\qquad
s^r\mid R_{q,r}(s).
}
\tag{4}
\]
Together with the positive leading-symbol theorem,
\[
\boxed{
\deg C_{q,r}=2q,
\qquad
[s^{2q}]C_{q,r}
=\frac4{q!}[z^r](1+2z+2z^2)^q>0.
}
\tag{5}
\]
Polynomiality here refers to the exact algebraic continuation of the
normalized endpoint: on every admissible integer \(s\) it equals the
combinatorial count (1), and the coefficient formulas below supply its
unique polynomial expression.

## 2. Three exact coefficient formulas

Use
\[
\Phi(t,u)=\frac{e^{ut}-1}{u},
\qquad
T=z e^{\Phi(T,u)},
\]
and the unrooted hypertree series \(V\).  The unmarked Lagrange formula is
\[
H_{0,e,c}
=\frac{(s-1)!}{(c-1)!}[t^{s-1}u^e]
V(t,u)^{c-1}(1-te^{ut})e^{s\Phi(t,u)}.
\tag{6}
\]

For one block of weight \(a\), put \(N=s-a\).  The direct Jacobian form
of Lagrange inversion gives
\[
\boxed{
H^{(a)}_{e,c}
=\frac{N!}{(c-1)!}[t^Nu^e]
(1-te^{ut})V(t,u)^{c-1}e^{s\Phi(t,u)}.
}
\tag{7}
\]

For two labelled blocks of weights \(a,b\), put \(N=s-a-b\).  The
two-marked path EGF gives a same-component factor
\[
ab e^{(a+b)\Phi}\frac{e^{uT}}{1-Te^{uT}}.
\]
The denominator is exactly the Lagrange Jacobian and therefore cancels.
Adding the different-component case yields
\[
\boxed{
\begin{aligned}
H^{(a,b)}_{e,c}
=N![t^Nu^e]e^{s\Phi(t,u)}\bigg[&
ab e^{ut}\frac{V(t,u)^{c-1}}{(c-1)!}\\
&+\mathbf1_{c\ge2}(1-te^{ut})
\frac{V(t,u)^{c-2}}{(c-2)!}
\bigg].
\end{aligned}
}
\tag{8}
\]
The required endpoints are (6), (7) with \(a=2\), and (8) with
\(a=b=2\).

### Formal-power-series legitimacy

All three identities are formal.  Work in \(\mathbb Q[s][[t,u]]\) with
the \(t\)-adic topology.  The apparent quotients by \(u\) are removable:
\(\Phi=t+ut^2/2+\cdots\), and the displayed \(V\) is likewise a member of
\(\mathbb Q[[t,u]]\).  Since
\(T=z\exp(\Phi(T,u))\) and the multiplier has constant term one, there is
a unique \(T\in z\mathbb Q[[z,u]]\), so formal Lagrange inversion applies.
The path factor \((1-Te^{uT})^{-1}\) is legitimate because its denominator
has constant term one.  In (8) this inverse is cancelled algebraically by
the exact Lagrange Jacobian \(1-te^{ut}\), before coefficient extraction.

For fixed \([u^e]\), (9)--(11) truncate to finite sums: only finitely many
positive-\(u\) factors and excess compositions can contribute.  Separating
\(e^{st}\) is therefore a formal coefficient identity, and (14) converts
each term into a falling factorial.  No analytic convergence, interchange
of infinite numerical sums, or negative factorial is used.  The \(N=0\)
case of (8) is covered directly by constant-term Lagrange inversion; the
different-component summand is simply absent when \(c=1\).

## 3. Termwise nonnegative \(s\)-valuation

Separate \(e^{st}\) and use the exact expansions
\[
\Phi(t,u)-t
=\sum_{j\ge1}\frac{u^jt^{j+1}}{(j+1)!},
\tag{9}
\]
\[
V(t,u)
=t-\frac{t^2}{2}
-\sum_{j\ge1}\frac{(j+1)u^jt^{j+2}}{(j+2)!},
\tag{10}
\]
and
\[
1-te^{ut}
=1-t-\sum_{j\ge1}\frac{u^jt^{j+1}}{j!}.
\tag{11}
\]
Fix a monomial contributing to \([u^e]\).  Suppose the exponential in
(9) supplies \(m\) positive-excess factors.  If their total excess is
\(e_E\), they contribute
\[
s^m t^{e_E+m}.
\tag{12}
\]
In a product of \(k\) copies of \(V\), suppose \(p\) copies use a
positive-excess term, and among the remaining copies \(j\) use the
quadratic rather than linear term of \(t-t^2/2\).  If their total excess
is \(e_V\), their total \(t\)-degree is
\[
e_V+k+p+j.
\tag{13}
\]

Coefficient extraction against \(e^{st}\) is exact:
\[
M![t^M]e^{st}t^d=(M)_d s^{M-d}.
\tag{14}
\]
Thus it suffices to check that the residual exponent of \(s\), after the
normalization (1), is nonnegative for each monomial.

### Unmarked endpoint

Use (6), so \(k=c-1\).  If (11) supplies its constant/linear part, let
\(b\in\{0,1\}\) be its \(t\)-degree.  Equations (12)--(14) leave
\[
c-p-j-b\ge0.
\tag{15}
\]
If (11) supplies positive excess, the residual exponent is
\[
c-1-p-j\ge0.
\tag{16}
\]

### One marked block

Use (7), again with \(k=c-1\).  The same two cases leave exactly the
nonnegative exponents (15)--(16).  Division by the fixed constant \(a\)
does not affect polynomiality in \(s\).

### Two marked blocks

For the same-component term in (8), \(e^{ut}\) supplies excess \(e_P\)
and the equal \(t\)-degree \(e_P\).  With \(k=c-1\), the residual exponent
is
\[
c-1-p-j\ge0.
\tag{17}
\]
For the different-component term, \(k=c-2\), and the two alternatives in
(11) leave
\[
c-p-j-b\ge0
\qquad\text{or}\qquad
c-1-p-j\ge0.
\tag{18}
\]

In every case, the normalized monomial is a rational constant times
\[
s^v(M)_d,
\qquad v\ge0,
\]
and hence is a polynomial in \(s\).  For fixed \(e,c\), only finitely many
monomials occur.  This proves (2).

The denominator-aware endpoint theorem already gives
\(Q_{h,e,c}=N_{h,e,c}/s^e\) with
\(\deg N_{h,e,c}\le2c+3e-2\).  Polynomiality therefore gives the upper
bound in (3), while the proved leading coefficient
\(A_{e,c}>0\) gives equality.

Finally, the fixed-deficit master formula is a finite sum of products of
the \(Q_{h,e,c}\), falling factorials, and rational constants.  It is
therefore polynomial term by term, proving (4).  Equation (5) follows
from the positive leading-symbol theorem.

## 4. Scope

This theorem removes the former arbitrary-\(q\) denominator caveat.  It
does not prove that the lower coefficients of \(C_{q,r}(s)\) are positive,
give a uniform threshold in \(q\), or settle bulk pooled depths or
arbitrary-host OPG-1757.
