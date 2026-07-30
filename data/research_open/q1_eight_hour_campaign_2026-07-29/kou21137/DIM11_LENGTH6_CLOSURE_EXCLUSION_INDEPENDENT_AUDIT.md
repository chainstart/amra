# Dimension eleven: independent closure exclusion of the length-six profile

Date: 2026-07-30

## Theorem

Let \(J\) be an 11-dimensional nilpotent associative
\(\mathbb F_3\)-algebra with \(J^7=0\) and filtration profile

\[
(2,2,2,2,2,1).
\]

If the raw cube set \(C=\{x^3:x\in J\}\) is closed under the circle law,
then all raw cubes commute.  Hence this profile cannot give a Wilson
counterexample.

## Proof

Put \(A_i=J^i/J^{i+1}\), and let

\[
q:A_1\to A_3,\qquad q(\bar x)=\overline{x^3}.
\]

The projection of the circle subgroup \(C\) to additive \(A_3\) has image
\(q(A_1)\).  If this image were at most one-dimensional, the alternating
commutator form \(A_3\times A_3\to A_6\) would vanish on it.  Since
\(J^7=0\), all cubes would then commute.  In the noncommuting case the image
therefore has dimension two.  Both \(A_1\) and \(A_3\) have nine points, so
\(q\) is bijective.

Let
\[
K=C\cap J^4
\]
be the kernel of the projection to \(A_3\).  If \(r^3\in J^4\), then
\(q(\bar r)=0\); bijectivity gives \(r\in J^2\), and hence
\(r^3\in J^6\).  Thus \(K\subseteq J^6\).  On the other hand, if two cubes
do not commute, their group commutator is a nonzero member of
\(C\cap J^6\).  Since \(A_6=J^6\) is a line,

\[
K=J^6.                                                   \tag{1}
\]

The fibres of a subgroup homomorphism are cosets of its kernel.  Moreover,
\(J^3J^6=J^9=0\), so circle cosets by \(J^6\) are ordinary additive cosets.
Consequently any two raw cubes having the same \(A_3\) component differ by
an element of \(J^6\).

Take arbitrary \(v\in J\) and \(z\in J^3\).  The roots \(v\) and \(v+z\)
have the same \(A_1\) component, so their cubes have the same \(A_3\)
component.  By (1),

\[
D:=(v+z)^3-v^3\in J^6.                                  \tag{2}
\]

Because \(J^7=0\), every term with at least two occurrences of \(z\)
vanishes, and the noncommutative expansion is exactly

\[
D=v^2z+vzv+zv^2.                                        \tag{3}
\]

Equation (2) gives \(vD=Dv=0\).  Multiplying (3) on the two sides and
subtracting yields

\[
\begin{aligned}
0=vD-Dv
 &=\left(v^3z+v^2zv+vzv^2\right)\\
 &\quad-\left(v^2zv+vzv^2+zv^3\right)\\
 &=v^3z-zv^3.
\end{aligned}
\]

Finally set \(z=x^3\), which lies in \(J^3\), for arbitrary \(x\in J\).
Then

\[
v^3x^3=x^3v^3
\]

for all \(v,x\in J\).  All raw cubes commute, as claimed. \(\square\)

## Audit notes

- Closure is used twice and cannot be deleted: to make \(q(A_1)\) a
  subspace, and to make equal-leading fibres cosets of one kernel.
- The one-dimensionality of \(A_6\) is used to upgrade one nonzero
  commutator in \(K\) to \(K=J^6\).
- The equality \(J^7=0\) removes every two-\(z\) term and annihilates
  \(vD,Dv\).
- No solver result, raw-cube enumeration or assumption about associated
  graded filtered corrections is used.

At this stage, combining this theorem with
`search_dim11_algebra_profiles.py` left only

\[
(2,2,2,2,1,1,1),\qquad(2,2,3,1,1,1,1)
\]

as profiles not excluded by the lemmas in this independent audit.  The
later quadratic bound removes the second, and the two branch theorems in
`DIM11_CLOSURE_AWARE_STATUS.md` remove the first.  Thus this historical
intermediate status is now superseded by the full dimension-eleven
exclusion.
