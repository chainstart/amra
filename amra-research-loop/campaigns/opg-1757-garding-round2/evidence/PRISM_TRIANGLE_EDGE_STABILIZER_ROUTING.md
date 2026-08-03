# Triangular-prism triangle-edge stabilizer routing

Date: 2026-08-03

Status: **exact representation and obstruction; component theorem open**

Mark the triangle edge `01` in the prism with top triangle `012`, bottom
triangle `345`, and vertical edges `03,14,25`.  Its setwise stabilizer has
five orbits on the eight unmarked edges, of sizes

\[
 2,1,2,2,1.
\]

Independent complement-of-forest enumeration gives 190 forests and 66 in
which the marked endpoints are connected.  Thus the all-ones values are
`P=190, xi=66`.  The complete five-variable polynomials have respectively
79 and 35 monomials and are reconstructed by the verifier.

## A three-variable routing slice

Equalize the two size-two triangle orbits, equalize the two singleton
orbits, and retain the size-two vertical orbit.  After shifting the three
values by `x=p+1,y=t+1,z=v+1`, exact expansion gives

\[
\begin{aligned}
P={}&x^4y^2z^2-x^2yz^2-2x^2yz-x^2y-2x^2z+4xz+4x\\
   &-y^2+4y-6,
\end{aligned}
\]

\[
\begin{aligned}
\xi={}&x^4y+x^2y^2z^2+x^2y^2+2x^2yz-4x^2y+2x^2z-8x^2\\
 &-4xyz-4xy-8xz+24x-2y^2-yz^2+10y+8z-18.
\end{aligned}
\]

Unlike the vertical-edge orbit, elimination in `x` does not collapse to a
single square barrier.  The resultant has the proved factors

\[
y^2(y-1)^4(z-1)^2(yz+y-2)^2R(y,z),
\]

where the full resultant has total degree 28 and 166 monomials, while the
residual factor `R` has total degree 16 and 52 monomials and is a nonsquare
irreducible factor over the rationals.  This falsifies only the literal
ansatz that elimination collapses to one low-degree square wall on this
coarsening.  A component-level square-wall routing with additional chamber
data remains open.

There are easy negative points in the `P`-positive locus.  For example

\[
(x,y,z)=(3/2,1/2,1),\qquad P=1/64,quad \xi=-3/32.
\]

The later audited `z=1` theorem places this point below the lower `C` root,
in a different component from the anchor within that plane.  It is not a
counterexample in the full three-variable coarsening.  On `z=1`, both
polynomials contain the wall factor `x-1`, and at `y=1/2`

\[
P=\frac{(x-1)(x^3+x^2-15x+17)}4,
\]

while the direct segment toward larger `x` hits `P<0`.  No component
membership is inferred from this one segment; the negative point remains
an explicitly unclassified positivity island.

The next valid task is a component classification around the four
resultant factors, not a broader random scan.  Nothing here changes G201 or
the already proved marked-vertical-edge result G214.
