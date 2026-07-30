# Growing-number-field complexity budget for weighted chord charts

Date: 2026-07-30

## 1. Explicit field complexity

Let \(K\) be a number field, \(F=K(i)\), and write
\[
D=[F:\mathbb Q],\qquad r=r_F,\qquad w=|\mu_F|.
\]
Use one **unweighted** coordinate \(\log|\sigma(\varepsilon)|\) for
every real place and every conjugate pair of complex places.  This is
an invertible diagonal rescaling of the usual weighted Dirichlet
embedding and is still a rank-\(r\) lattice in its product-formula
hyperplane.
Let
\[
\lambda_F
=\min_{\varepsilon\in\mathcal O_F^\times\setminus\mu_F}
\|\log|\varepsilon|\|_\infty,
\tag{1}
\]
with \(\lambda_F=+\infty\) when \(r=0\), and put
\[
\mathcal T(X)=\max_{1\le m\le\lfloor X\rfloor}\tau(m).
\tag{2}
\]

### Theorem 1 (explicit varying-field two-square fibre)

For \(B\ge2\) and \(0\ne n\in\mathcal O_K\),
\[
\boxed{
|\mathcal R_K(n;B)|
\le
w\left(
1+\frac{2D\log(2B)}{\lambda_F}
\right)^r
\mathcal T((2B^2)^D)^D.
}
\tag{3}
\]
When \(r=0\), the parenthesized factor is interpreted as one.

### Proof

The ideal argument in the fixed-field theorem is uniform:
\[
d_F((n))
\le\tau(|N_{F/\mathbb Q}n|)^D
\le\mathcal T((2B^2)^D)^D.
\tag{4}
\]
It remains only to replace the unspecified unit-lattice constant.

For two generators \(\alpha,\alpha_0\) of the same solution ideal,
the conjugate upper and lower bounds give
\[
|\log|\sigma(\alpha/\alpha_0)||\le D\log(2B)
\tag{5}
\]
at every archimedean place.  Set \(L=D\log(2B)\).  Distinct points of
the logarithmic unit lattice are separated by at least \(\lambda_F\)
in the restricted infinity norm.  The radius-\(\lambda_F/2\) balls
around lattice points in the radius-\(L\) ball are disjoint and lie in
the radius-\(L+\lambda_F/2\) ball.  Comparing \(r\)-dimensional
volumes gives at most
\[
\left(1+\frac{2L}{\lambda_F}\right)^r
\tag{6}
\]
logarithmic unit vectors.  Every vector has exactly \(w\) unit
preimages.  Multiplying (4) and (6) proves (3).
\(\square\)

For the weighted chart theorem the coordinate bound is \(2B\), because
\(y=q(z-z_0)\).  Thus its exact varying-field fibre is
\[
\boxed{
\mathfrak G_F(B)
=
w\left(
1+\frac{2D\log(4B)}{\lambda_F}
\right)^r
\mathcal T((8B^2)^D)^D.
}
\tag{7}
\]
The proof and all quantifiers of the weighted layer-cake argument are
unchanged after replacing \(\mathfrak F_K(2B)\) by
\(\mathfrak G_F(B)\).

## 2. Exact asymptotic budget

Let \(K=K_t\), \(F_t=K_t(i)\), and suppose \(B_t\le t^C\) for one
fixed \(C\).  The terminal fibre is \(t^{o(1)}\) whenever
\[
\boxed{
\begin{aligned}
\Xi_t:={}&
\log w_t
+r_t\log\left(
1+\frac{2D_t\log(4B_t)}{\lambda_{F_t}}
\right)\\
&+D_t\log\mathcal T((8B_t^2)^{D_t})
=o(\log t).
\end{aligned}
}
\tag{8}
\]
This is an exact sufficient condition, not asymptotic notation hidden
inside a field-dependent constant.

Consequently the weighted terminal theorem gives
\[
|\Delta^2(P)|
\ge
\frac{\Omega_{\rm cyl}}
{|\mathcal J|L_UK_{\rm chord}\exp(\Xi_t)}.
\tag{9}
\]
Thus every exponent calculation in the fixed-field theorem remains
valid precisely when \(\Xi_t=o(\log t)\).

## 3. A field-uniform degree criterion

The classical uniform divisor estimate gives
\[
\log\mathcal T(X)
=O\left(\frac{\log X}{\log\log X}\right).
\tag{10}
\]
Since \(\log X=O(D_t\log t)\), its contribution to (8) is
\[
O\left(
\frac{D_t^2\log t}{\log(D_t\log t)}
\right).
\tag{11}
\]

For a non-torsion algebraic unit of degree at most \(D\),
Dobrowolski's theorem gives, uniformly as \(D\to\infty\),
\[
h(\varepsilon)
\gg
\frac1D
\left(\frac{\log\log D}{\log D}\right)^3.
\tag{12}
\]
The maximum absolute unit-log coordinate is at least
\(h(\varepsilon)\).  Hence
\[
\lambda_F^{-1}
\ll
D\left(\frac{\log D}{\log\log D}\right)^3.
\tag{13}
\]
The number of roots of unity in a degree-\(D\) field satisfies
\[
w=O(D\log\log(D+2)),
\tag{14}
\]
and \(r\le D-1\).

Equations (11)--(14) prove:

### Corollary 2 (slowly growing degree)

Uniformly over arbitrary fields \(K_t\), if
\[
B_t\le t^C,\qquad
D_t=[K_t(i):\mathbb Q]
=o(\sqrt{\log\log t}),
\tag{15}
\]
then
\[
\boxed{\mathfrak G_{F_t}(B_t)=t^{o(1)}.}
\tag{16}
\]
No bound on \(|\operatorname{Disc}(F_t)|\) is needed.  In particular,
bounded degree is uniform over all fields, rather than merely over a
fixed finite family or bounded-discriminant family.

### Proof

Under (15), \(\log(D_t\log t)\sim\log\log t\), so (11) is
\[
o(\log t).
\]
The logarithm of the unit factor in (7) is
\[
O\bigl(D_t(\log\log t+\log(D_t+2))\bigr)
=o(\log t),
\]
and (14) is smaller still.  This proves (16).
\(\square\)

## 4. Role of the discriminant and method boundary

The discriminant does not enter (3): ideal divisors are bounded using
the rational norm, and unit generators are counted by packing plus a
degree-uniform height lower bound.  A slowly growing discriminant is
therefore optional, not a missing hypothesis.  Bounded degree and
bounded discriminant still give a finite family by Hermite, but that is
strictly weaker than Corollary 2.

The degree scale in (15) is the strongest conclusion supplied by the
generic envelope (4).  At
\[
D_t\asymp\sqrt{\log\log t},
\]
the upper bound (11) is already \(O(\log t)\), not \(o(\log t)\).
This is a no-go for the present ideal-divisor majorant, not a
counterexample to a sharper two-square theorem.  Passing that boundary
requires exploiting splitting, relative norms, or the restricted
principal-ideal support; merely assuming a slowly growing discriminant
or unit rank does not remove the displayed \(\tau(\cdot)^{D_t}\)
loss.
