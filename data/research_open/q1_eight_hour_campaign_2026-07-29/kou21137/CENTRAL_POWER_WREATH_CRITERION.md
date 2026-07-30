# Central power values in \(A\wr C_p\)

Date: 2026-07-29

## 1. Exact closure criterion

The closure statement below is a central-value corollary of the stronger
theorem in `GENERAL_PRIME_WREATH_CRITERION.md`, where no centrality or
finiteness assumption is needed.  Centrality is retained here because it is
essential for the direct-product description and quotient obstruction in
Section 3.

Let \(p\) be a prime, let \(A\) be finite, and suppose
\[
  U=P_p(A)=\{a^p:a\in A\}
\]
is a central subgroup of \(A\).  Put \(W=A\wr C_p\).  Then
\[
  P_p(W)\text{ is a subgroup}
\]
if and only if either

1. \(U=A\); or
2. \(U<A\), \(U=A'\), and
   \[
     x^A=xU\qquad(x\notin U).                     \tag{1}
   \]

In the second case \(A\) is a Camina group and
\[
  P_p(W)
  =
  \{(a_0,\ldots,a_{p-1})\in A^p:
    a_0U=\cdots=a_{p-1}U\}.                       \tag{2}
\]
Thus the value set is the inverse image of the diagonal subgroup of
\((A/U)^p\).

The first case is a necessary degenerate exception in the finite-group
statement.  For example, if \(p\nmid|A|\) and \(A\) is abelian, then
\(U=A\) and \(P_p(W)=A^p\).  For a nontrivial finite \(p\)-group, \(U<A\)
automatically, because the \(p\)-th-power map is not injective and hence
cannot be surjective.

### Proof

The exact value-set and generated-subgroup formulas are
\[
\begin{aligned}
  S:=P_p(W)&=U^p\cup\bigcup_{C\in\mathcal C(A)}C^p,\\
  H:=\langle S\rangle&=\Delta A\,(UA')^p.          \tag{3}
\end{aligned}
\]
Here set powers denote Cartesian powers.

Fix a coordinate \(i\) and let \(E_i(X)\) denote the copy of \(X\) on that
coordinate axis.  Formula (3) gives
\[
  S\cap E_i(A)=E_i(U).                             \tag{4}
\]
Indeed, \(U^p\) has exactly this intersection, while a tuple in \(C^p\)
with \(p-1\) identity coordinates must have \(C=\{1\}\).
Similarly,
\[
  H\cap E_i(A)=E_i(UA').                           \tag{5}
\]
The inclusion from right to left follows from \((UA')^p\leq H\).  Conversely,
if a product of a diagonal tuple with an \((UA')^p\)-tuple lies on one axis,
any other coordinate shows that its diagonal entry belongs to \(UA'\), and
then so does the remaining coordinate.

If \(S\) is a subgroup, then \(S=H\), so (4)--(5) imply
\[
  A'\leq U.                                        \tag{6}
\]
Assume \(U<A\), and choose \(x\notin U\).  Since \(H\) contains
\[
  (x,xu_1,\ldots,xu_{p-1})
\]
for arbitrary \(u_i\in U\), closure forces these tuples into the
conjugacy-class part of \(S\).  Their first coordinate is \(x\), so
\[
  xU\subseteq x^A.
\]
But every conjugate of \(x\) lies in \(xA'\), and (6) gives
\[
  x^A\subseteq xA'\subseteq xU.
\]
Thus \(x^A=xU\).  In particular \(xu\in x^A\) for every \(u\in U\), so
\(u=x^{-1}x^g\in A'\); hence \(U\leq A'\).  Together with (6), this proves
\(U=A'\) and (1).

Conversely, if \(U=A\), the first term \(U^p\) in (3) is all of \(A^p\).
If the second condition holds, the terms in (3) are exactly the Cartesian
powers of all \(U\)-cosets, which is the fiber product (2), hence a subgroup.

## 2. Exponent-\(p\) seed obstruction

Let \(A\ne1\) be a finite \(p\)-group of exponent \(p\).  Then \(U=1<A\).
The criterion shows
\[
  P_p(A\wr C_p)\text{ is a subgroup}
  \quad\Longleftrightarrow\quad
  A\text{ is abelian}.                             \tag{7}
\]
In the positive case the power subgroup is the diagonal copy \(\Delta A\),
so it is abelian.

Moreover,
\[
  \exp(A\wr C_p)=p\,\exp(A)=p^2.
\]
The upper bound follows from the wreath power formula; equality follows
because \((a,1,\ldots,1)t\) has \(p\)-th power \(\Delta a\).
Consequently, an unquotiented regular wreath product built from an
exponent-\(p\) seed can never produce the exponent-\(p^2\) KOU target with a
nonabelian subgroup of \(p\)-th powers.

## 3. Quotient no-go for exponent-\(p^2\) Camina seeds

There is a stronger obstruction that covers every quotient used to lower the
exponent, not only the diagonal quotient.

Let \(A\) be a finite \(p\)-group of exponent \(p^2\) such that
\[
  U=P_p(A)=A'\leq Z(A),
  \qquad
  x^A=xU\quad(x\notin U).                          \tag{8}
\]
For \(W=A\wr C_p\), the criterion gives a subgroup
\[
  H=P_p(W)=\Delta A\,U^p.
\]
The map
\[
  A\times U^{p-1}\longrightarrow H,\qquad
  (a,u_1,\ldots,u_{p-1})
  \longmapsto(a,au_1,\ldots,au_{p-1})
\]
is an isomorphism because \(U\) is central.  Hence
\[
  H'=\Delta A'=\Delta U.                           \tag{9}
\]
Also \(\exp(W)=p^3\): the general upper bound is
\(p\exp(A)\), and if \(a\) has order \(p^2\), then
\[
  x_a=(a,1,\ldots,1)t,\qquad x_a^p=\Delta a
\]
has order \(p^3\).

Now let \(N\trianglelefteq W\) and suppose
\[
  \exp(W/N)\leq p^2.                               \tag{10}
\]
For every \(u\in U\), choose \(a\in A\) with \(a^p=u\).  Then
\[
  x_a^{p^2}=\Delta(a^p)=\Delta u.
\]
Condition (10) therefore forces
\[
  \Delta U\leq N.                                  \tag{11}
\]
Word values commute with epimorphisms, so
\[
  P_p(W/N)=HN/N.
\]
This is a subgroup, but by (9)--(11) its derived subgroup is
\[
  (HN/N)'=H'N/N=1.
\]
We have proved:
\[
\boxed{
 \exp(W/N)\leq p^2
 \quad\Longrightarrow\quad
 P_p(W/N)\text{ is an abelian subgroup}.}
\]

Thus no quotient of this entire closed wreath family can reduce exponent
\(p^3\) to the exponent-\(p^2\) KOU regime while retaining a nonabelian
\(p\)-th-power subgroup.

## 4. Computational anchors

The general formula has an independent \(p=5\) exact-value regression in
`test_odd_power_value_formula.py`, which enumerates all 500,000 elements of
\(D_{10}\wr C_5\).

At \(p=3\), `validate_odd_diagonal_quotient_no_go.g` scans all SmallGroups
seeds of orders \(27,81,243,729\) satisfying the central-power hypotheses.
It finds no closure when \(P_3(A)<A'\), exactly as the criterion predicts.

Finally, `validate_odd_wreath_p3.g` checks the positive boundary seed: the
extraspecial group of order 27 and exponent 9.  Its wreath product has
exponent 27, its cube values form a nonabelian subgroup with derived subgroup
\(\Delta U\), and quotienting by \(\Delta U\) lowers the exponent to 9 while
making the cube subgroup abelian.
