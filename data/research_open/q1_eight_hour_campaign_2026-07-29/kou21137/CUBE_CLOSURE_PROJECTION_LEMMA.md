# Raw-cube closure: projection and fibre obstruction

Date: 2026-07-30

## General lemma

Let \(J\) be a nilpotent associative \(\mathbb F_3\)-algebra with
\(J^9=0\), and write

\[
C=\{x^3:x\in J\}\subseteq J^3.
\]

Equip \(J\) with the circle law \(a\circ b=a+b+ab\), corresponding to
multiplication in \(1+J\).  If \(C\) is a circle subgroup, then the
projection

\[
\pi:C\longrightarrow A_3=J^3/J^4
\]

is a group homomorphism into the additive group of \(A_3\), because
\(ab\in J^6\subseteq J^4\).  Consequently:

1. the leading-cube image
   \[
   Q=\{(x+J^2)^3:x\in J\}\subseteq A_3
   \]
   is an \(\mathbb F_3\)-linear subspace;
2. every nonempty fibre of \(\pi\) has the same cardinality
   \(|C\cap J^4|\);
3. in particular \(|C|\) is a power of three.

These are necessary conditions only.  They are inexpensive and can be
enforced before any full circle-closure CEGIS loop.

## Length-six consequence

Assume \(J^7=0\).  For cubes \(c,d\), their commutator belongs to \(J^6\),
and its image is determined only by the leading classes
\(\pi(c),\pi(d)\in A_3\).  If \(Q\) is a line, all leading classes are
proportional and the alternating commutator form vanishes on \(Q\times Q\).
Since there is no \(J^7\) correction, all raw cubes commute.

Therefore a closed, noncommuting raw-cube set in a length-six profile must
have

\[
\dim Q\ge2.
\]

For the dimension-eleven length-six candidate
\((2,2,2,2,2,1)\), both \(A_1\) and \(A_3\) have dimension two.  Closure and
noncommutativity hence force \(Q=A_3\).  The leading cubic map

\[
q:A_1\longrightarrow A_3,\qquad v\longmapsto v^3,
\]

must be a bijection on the nine \(\mathbb F_3\)-points.

This converts raw-cube closure into a finite, exact first-stage constraint:
before modelling all \(3^{11}\) roots, one may require the nine leading
cubes to be all of \(A_3\).

There is a second inexpensive necessary condition.  If raw cubes \(u,v\)
do not commute, then their group commutator is another member of the closed
raw-cube set.  Here \(u,v\in J^3\) and \(J^7=0\), so

\[
[1+u,1+v]=1+(uv-vu),
\]

with \(0\ne uv-vu\in A_6\).  Since \(q:A_1\to A_3\) is bijective, a root
whose cube has zero \(A_3\)-component must have zero \(A_1\)-component.
Thus closure forces

\[
\exists z\in J^2:\qquad z^3=uv-vu\ne0.            \tag{1}
\]

Condition (1) is stronger than leading-image closure but weaker than a full
raw-cube product constraint.  It gives a small symmetry-broken SMT/CEGIS
contract for the last length-six profile.

## Sharp witness diagnosis

In `DIM11_SHARP_NONCOMMUTING_CUBE_WITNESS.md`, the leading image contains
seven points rather than a subspace: one point with zero \(A_3\)-coordinate
and six with nonzero \(A_3\)-coordinate.  The complete raw-cube fibres also
have sizes 9 and 27 rather than one common size.  Either failure independently
rules out closure.  The witness does **not** fail condition (1):
\((A_2+B_2)^3=B_6\).  This is a useful warning that a commutator-root
constraint alone is strictly weaker than projection/fibre closure.

Thus the witness establishes sharpness of the commutativity bound but is
discarded at the first closure-aware projection test.

## Scope

For length-seven profiles, proportional leading \(A_3\) classes may still
have a commutator in \(J^7\) coming from filtered corrections.  The
length-six conclusion must not be applied there without an additional
argument.  The general subspace and equal-fibre statements remain valid in
all lengths.
