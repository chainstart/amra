# Fixed-number-field weighted chart: independent red-team audit

Date: 2026-07-30

## Verdict

\[
\boxed{\mathrm{PASS\ with\ one\ wording\ repair}}
\]

The two-square fibre theorem and its weighted-chart substitution are
correct.  One statement was repaired: \(C_F\) depends on both the
logarithmic unit lattice and the finite torsion subgroup \(\mu_F\), not
on the logarithmic lattice alone.  The original proof already included
torsion in \(C_F\), so the bound and all downstream conclusions are
unchanged.

The independent verifier imports no author verifier and reconstructs
the tested arithmetic from definitions.

## 1. Ideal divisors

For \(\alpha=x+iy\), \(\beta=x-iy\),
\[
(\alpha)(\beta)=(n).
\]
Thus \((\alpha)\) is an integral ideal divisor of \((n)\).  If a
rational prime \(p\) has at most \(D\) primes above it and
\[
E=v_p(|N_{F/\mathbb Q}n|),
\]
then every prime-ideal exponent in \((n)\) is at most \(E\).  Hence its
local divisor count is at most \((E+1)^D\), and multiplication over
rational primes gives
\[
d_F((n))\le\tau(|Nn|)^D.
\]
This is deliberately loose but valid.  Principal solution ideals are a
subset of all divisors, so neither a class-number factor nor a choice of
class representatives is needed.

## 2. Generator and unit count

The map from a representation to \(\alpha\) is injective even when
\(i\in K\).  Indeed \(n\ne0\) gives
\[
\beta=n/\alpha,\quad
x=(\alpha+\beta)/2,\quad
y=(\alpha-\beta)/(2i).
\]

Every conjugate satisfies \(|\sigma\alpha|\le2B\).  Since its norm is a
nonzero integer, bounding the other \(D-1\) conjugates gives
\[
(2B)^{-(D-1)}\le|\sigma\alpha|\le2B.
\]
For two generators of the same ideal, their unit ratio therefore lies
in the log box
\[
|\log|\sigma\varepsilon||\le D\log(2B).
\]
A fixed rank-\(r_F\) lattice has \(O_F((1+\log B)^{r_F})\) points in
this box.  The torsion multiplicity \(|\mu_F|\) must be included; this
is the repaired wording.

## 3. Norm and zero boundary

For a representation,
\[
1\le|N_{F/\mathbb Q}n|\le(2B^2)^D.
\]
The lower bound fails at \(n=0\), and when \(i\in K\), every
\((iu,u)\) represents zero.  Excluding \(n=0\) is therefore necessary,
not cosmetic.

In the weighted application, \(x\) and \(y\) have real distinguished
values and \(x>0\).  Hence \(n=x^2+y^2>0\) at that embedding and cannot
be zero.

## 4. Weighted-chart quantifiers

The star and dyadic layer-cake choices occur before the fibre bound and
produce
\[
H|\mathcal E_H|
\ge\Omega_{\rm cyl}/(|\mathcal J|L_U).
\]
After quotienting by anchored chord multiplicity, one representative
is retained for each distinct algebraic \(x\).  For each retained
\(x\), the \(H\) chosen heights give distinct algebraic
\(y=q(z-z_0)\).  Thus the selected inputs inject into ordered
representations \((x,y)\).

The chord has conjugate bound \(B\), while the height difference has
bound \(2B\).  Applying the fibre theorem at coordinate bound \(2B\)
is therefore correct and gives norm range
\[
(2(2B)^2)^D=(8B^2)^D.
\]
This is exactly \(\mathfrak F_K(2B)\).  Equal real scaled distances
give equal algebraic labels because the distinguished embedding is
injective.  Multiplication by the common positive \(q^2\) preserves the
number of labels.

For fixed \(K,C\) and \(B\le t^C\), the unit factor is polylogarithmic
and
\[
\tau(m)^D
=\exp(O(\log t/\log\log t))
=t^{o(1)}.
\]
The \(o(1)\) is uniform over every nonzero label and every chart
satisfying the stated common \(K,q,B\); it is not uniform over
uncontrolled varying fields.

## 5. Growing fields

`GROWING_NUMBER_FIELD_WEIGHTED_CHART_THEOREM.md` removes the hidden
field constant.  With \(\lambda_F\) the shortest non-torsion unit-log
vector and \(w_F=|\mu_F|\), the exact weighted fibre is
\[
w_F\left(1+\frac{2D\log(4B)}{\lambda_F}\right)^{r_F}
\mathcal T((8B^2)^D)^D.
\]
This yields a complete explicit complexity budget.  Dobrowolski's
height bound and the uniform maximal-divisor estimate imply the
field-uniform sufficient condition
\[
D=o(\sqrt{\log\log t})
\]
for polynomial \(B\), without any discriminant restriction.

At \(D\asymp\sqrt{\log\log t}\), the generic
\(\tau(\cdot)^D\) envelope already has polynomial-size logarithmic
upper bound.  This is a rigorous limitation of the present proof
method, not a counterexample to a sharper representation theorem.
