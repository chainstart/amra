# A sharp dimension-eleven witness for noncommuting cubes

Date: 2026-07-30

## Scope

This construction is **not** a Wilson/KOU-21.137 counterexample: its raw
cube-value set is not closed.  It shows that the human lower bound
\(\dim J\ge 11\), once the dimension-ten profile audit is completed, is
sharp for the weaker property “two raw cubes do not commute.”  Any further
dimension improvement must use raw-cube closure or additional structure,
not filtration dimensions alone.

## The algebra

Over \(\mathbb F_3\), take the monomial algebra
\[
 J=\langle A_i,B_i:1\le i\le5\rangle
   \oplus\langle B_6\rangle,
\]
where
\[
 A_i=a^i,\qquad B_i=a^{i-1}b.
\]
The nonzero products of basis elements are exactly
\[
 A_iA_j=A_{i+j}\quad(i+j\le5),\qquad
 A_iB_j=B_{i+j}\quad(i+j\le6).
\]
Every product with a \(B_i\) on the left is zero.  Equivalently, this is
the truncated algebra with
\[
 ba=b^2=0,\qquad a^6=0,
\]
while \(a^5b=B_6\ne0\), and every word of degree at least seven is zero.
The multiplication table is associative by direct word reduction; the
independent verifier also checks all \(11^3\) triples of basis elements.

Its power-filtration profile is
\[
 \left(\dim J^i/J^{i+1}\right)_{i=1}^6
 =(2,2,2,2,2,1),
\]
so \(\dim J=11\) and \(J^7=0\).

## Two noncommuting cubes

In characteristic three,
\[
 a^3=A_3,\qquad (a+b)^3=A_3+B_3.
\]
The second identity follows from \(ba=b^2=0\).  Their products are
\[
 A_3(A_3+B_3)=B_6,\qquad
 (A_3+B_3)A_3=0,
\]
because \(A_6=0\) but \(A_3B_3=B_6\ne0\).  Hence the corresponding cubes
in \(1+J\) do not commute.

## Exact raw-cube image and failure of closure

Write an arbitrary element as
\[
 x=p(a)+q(a)b.
\]
Then
\[
 x^3=p(a)^3+p(a)^2q(a)b.                         \tag{1}
\]
If the coefficient of \(a\) in \(p\) is nonzero, (1) ranges over one of
the two cosets
\[
 \pm A_3+\langle B_3,B_4,B_5,B_6\rangle.
\]
If that coefficient is zero, its image is exactly
\[
 \langle B_5,B_6\rangle.
\]
Thus the raw cube set has
\[
 2\cdot3^4+3^2=171
\]
elements.

The closure-aware projection obstruction is already visible in degree
three.  The leading image in
\(A_3=\langle A_3,B_3\rangle\) has seven points, not an additive subspace:
the zero leading value has 9 raw-cube lifts, while each of the other six
leading values has 27.  A subgroup projection must have a linear image and
equal nonempty fibre sizes.  The exhaustive verifier checks the exact list
\([9,27,27,27,27,27,27]\).

Closure already fails on two displayed cubes.  Both
\[
 A_3+B_3=(a+b)^3,\qquad -A_3=(-a)^3
\]
are raw cube values, but their circle product is
\[
 (A_3+B_3)+(-A_3)+(A_3+B_3)(-A_3)=B_3.
\]
The element \(B_3\) is not a cube, since a cube with zero \(A_3\)
coordinate lies in \(\langle B_5,B_6\rangle\).

## Reproduction

```bash
python3 verify_dim11_sharp_noncommuting_cubes.py
pytest -q test_verify_dim11_sharp_noncommuting_cubes.py
```

The verifier exhausts all \(3^{11}=177147\) algebra elements, confirms the
171-element image, checks the nonzero commutator and the missing circle
product, and separately checks associativity on the basis multiplication
table.
