# Independent audit: spectral blocks and torsion-free tiling rank

Date: 2026-07-31

Audited source: `BREAKTHROUGH_ATTACK.md`

## 1. Verdict

| Item | Verdict |
|---|---|
| Parabolic lift | **PASS** |
| Near-direct-row deduction | **PASS** |
| Exact abstract block equality classification | **PASS** |
| Endpoint block exponents | **PASS** |
| Three-row Euclidean counterexample | **PASS** |
| Arbitrary-(k) hypercube construction | **PASS** |
| Full Euclidean interface of both finite constructions | **PASS** |
| Torsion-free direct-tiling rank theorem | **PASS** |
| Exact parabolic-resolution/fixed-difference theorem | **PASS** |
| Stability of the rank theorem | **NOT PROVED** |
| Euclidean realization of the endpoint block | **NOT PROVED** |
| Improvement above (3/5) | **NOT PROVED** |

The main new positive result is exact: if one common finite real set
has many *direct* decompositions by dilates of one tile (X), then a
pairwise rationally transverse subfamily has size at most
(log_{|X|}|V|).  The endpoint value is below three.  The proof does
not apply after even a sparse set of representation errors without a
new stability argument.

## 2. Parabolic lift reconstruction

For one target incidence ((z,\tau)), put

\[
 b=\rho^2+z^2+\tau.
\]

The row distance with source sine (x) is

\[
 d=b+2\rho zx.
\]

This is equivalent to incidence with

\[
 b=d-2\rho xz.
\]

There are (HU) parameter points and exactly (S) input incidences
per point, so the multiplicity count (HSU) is correct.  This is a
reformulation, not an incidence upper bound.

## 3. Near-direct-row audit

The inherited support inequality is

\[
 \sum_z|V_z|\ge\frac{HB}{1+\epsilon},
 \qquad B=SU,
 \qquad \epsilon=R^2S/(HU).
\]

Since (|V_z|\le B),

\[
 \sum_z(B-|V_z|)
 \le HB\frac{\epsilon}{1+\epsilon}
 \le HB\epsilon.
\]

At the endpoint (epsilon=t^{-1/6+o(1)}).  If a row has deficiency
at least (t^{-c}B), Markov's inequality bounds the number of such
rows by

\[
 t^{c-1/6+o(1)}H.
\]

Thus the quantifier (0<c<1/6) and the direction of (1.5) are valid.
Nothing in this step upgrades near injectivity to exact injectivity.

## 4. Block equality reconstruction

Let (r_d) be the label degree.  Then

\[
 \sum_{i\ne j}|V_i\cap V_j|
 =\sum_dr_d^2-\sum_dr_d.
\]

The second term is (HB), while Cauchy--Schwarz gives the first at
least (H^2B^2/D).  Equality requires all (r_d=HB/D).

If every pair intersection is zero or (B), positive intersection is
equality of the two (B)-sets.  Equal rows form equivalence classes,
different classes are disjoint, and the common label degree equals
the class size.  Therefore every class has size (q=HB/D).  No
unstated regularity assumption is used.

The exact endpoint arithmetic is

\[
\begin{aligned}
B&=t^{29/18},\\
q=HB/D&=t^{13/18},\\
G=D/B&=t^{25/18},\\
Gq^2&=t^{17/6},\\
Gq^2B&=t^{40/9}.
\end{aligned}
\]

All five values agree with the independent rational verifier.

The two proposed stability defects are also exact.  Writing
\(q=HB/D\) and \(a_{ij}=|V_i\cap V_j|\),

\[
 \sum_d(r_d-q)^2
 =\sum_{i,j}a_{ij}-H^2B^2/D.
\]

For an intermediate pair
\(\eta B\le a_{ij}\le(1-\eta)B\), the summand
\(a_{ij}(B-a_{ij})\) is at least
\(\eta(1-\eta)B^2\).  Hence the claimed bound on the number of
intermediate pairs follows.  Vanishing of both defects is equivalent
to label regularity plus zero/full pair intersections and therefore
to the exact block model.  This is a certificate for what a future
stability proof must control, not itself a proof that the inherited
endpoint estimates make both defects small.

## 5. Euclidean counterexample audit

For \(\rho=1\), the row formula is

\[
 1+z^2+\tau+2zx.
\]

Substitution of the three rows gives:

\[
\begin{array}{c|c|c}
z&T_z&V_z\\ \hline
-3/2&\{11,12\}&\{45,49,57,61\}/4\\
-1/2&\{11,14\}&\{45,49,57,61\}/4\\
 1/2&\{10,13\}&\{45,49,57,61\}/4.
\end{array}
\]

Each row has four inputs and four outputs.  With (A>1), the target
point ((A,\sqrt\tau,-z)) is off the common axis.  Its axial-plane
cosine is

\[
 \frac{A}{\sqrt{A^2+\tau}}\ne0,
\]

and selected label (1+\tau) gives reverse-circle radius one and
centre ((A,-z)).  Thus this is actual Euclidean geometry, not just a
formal sumset.

For the arbitrary-(k) construction, base-three uniqueness proves

\[
 \mathcal A_i\oplus\{0,3^i\}=\mathcal A.
\]

The shift (C>3^{2(k-1)}/4) makes every tangent square positive.
There are (2^{k-1}) values in each row and at most
(k2^{k-1}) in their union.  The construction is valid for every
finite (k), but its (k=O(\log U)) row count is far below the
polynomial endpoint block size.

The separate geometric-interface audit reconstructs the actual point
configuration.  With \(A=2\), each target
\((A,\sqrt\tau,-z)\) and label \(1+\tau\) induces the radius-one
circle centred at \((A,-z)\), because its transverse square is
\(\tau\).  The translated points
\((A+\cos\phi_x,0,-z+\sin\phi_x)\) are genuine incidences.  Positive
\(\tau\) makes the target real and off-axis, while
\(A/\sqrt{A^2+\tau}>0\) excludes perpendicular target planes.
Distinct \(z\)'s give distinct parallel circle axes and hence
nonaligned circles.  The construction still does not control all
distances created after the translated incidence points are added.

## 6. Group-ring theorem reconstruction

For a fixed finite transverse subfamily \(J\), only finitely many real
numbers occur, so the subgroup \(\Gamma\) they generate is a finitely
generated torsion-free abelian group.  Hence

\[
 \Gamma\simeq\mathbb Z^r
\]

and \(\mathbb Z[\Gamma]\) is a Laurent polynomial UFD.

The direct decomposition

\[
 V=A_i\oplus\lambda_iX
\]

is equivalent to

\[
 P_V=P_{A_i}P_{\lambda_iX};
\]

without directness the product coefficients would be representation
multiplicities and this identity would fail.

Suppose a nonunit polynomial divided two tile masks.  The Newton
polytope of a factor is a Minkowski summand of the Newton polytope of
each mask.  Its direction space is consequently contained in both

\[
 \operatorname{span}_{\mathbb Q}(\lambda_i(X-X))\otimes\mathbb R
\]

and the analogous space for (j).  Scalar extension from
\(\mathbb Q\) to \(\mathbb R\) preserves the zero intersection in the
hypothesis.  The factor's Newton polytope is therefore a point, so the
factor is a constant times a Laurent monomial.  Mask polynomials have
content one, making this a unit.  Pairwise coprimality follows.

In a UFD, the product of pairwise coprime divisors divides (P_V).
Under augmentation, every monomial becomes one, giving

\[
 |V|=Q(1)|X|^{|J|}.
\]

Here (Q(1)) is a positive integer because the left side and tile
cardinalities are positive.  Hence

\[
 |X|^{|J|}\le|V|.
\]

At the exact endpoint,

\[
 \log_S|V|=\log_S(SU)\to29/14<3,
\]

so three pairwise transverse rational dilation spaces are impossible
for all sufficiently large endpoint instances.

The inequality is sharp: \(k\) rationally independent weights and
their \(2^k\) subset sums give \(k\) pairwise transverse two-point
tile factors.  The same parabolic shift used in the arbitrary-row
construction makes all tangent squares positive.  Thus the audit does
not authorize a better universal exponent than (5.9).

## 7. Parabolic-resolution reconstruction

For one exact block, directness makes the cells

\[
 C_{z,\tau}=\rho^2+z^2+\tau+2\rho zX
\]

a partition of the common spectrum \(V\) for every row \(z\).  Thus
each \(v\in V\) is represented once in each of the \(q\) rows.
Counting ordered triples \((v,z,z')\), \(z\ne z'\), gives exactly
\(q(q-1)SU\) cross-row cell-intersection witnesses.

For every witness, uniqueness supplies \(x,x'\in X\), and subtraction
gives

\[
 z^2-z'^2+2\rho(zx-z'x')=\tau'-\tau.
\]

There are at most \(|T_*-T_*|\le R^2\) right-hand sides.  Therefore
one fixed difference supports at least \(q(q-1)SU/R^2\) witnesses.
The endpoint exponent is

\[
 2(13/18)+29/18-2=19/18.
\]

Separately, if \(r_\tau\) is the number of block rows containing
\(\tau\), then \(\sum_\tau r_\tau=qU\).  Averaging and
Cauchy--Schwarz give

\[
 \max_\tau r_\tau\ge qU/R,\qquad
 \sum_\tau r_\tau(r_\tau-1)\ge q^2U^2/R-qU.
\]

Their endpoint exponents are \(5/9\) and \(19/9\).  These identities
are exact.  They do not prove that the fixed-difference solutions are
nondegenerate or yield an affine-height chart.

## 8. Hard boundary

Three upgrades are not licensed by the proof.

1. A near-direct sum does not give exact mask-polynomial divisibility.
2. Pairwise intersections of the rational dilation spaces need not be
   transitive when
   \(\operatorname{rank}_{\mathbb Q}(X-X)>1\).
   The result gives two representative neighbourhoods, not two
   equivalence classes in general.
3. Commensurate heights do not automatically give consecutive integer
   vertical columns.  A separate stability/denominator-control bridge
   is required before invoking the ruled-column escape theorem.

Accordingly, the audit authorizes an exact block classification and a
new stability target, but rejects a claim that the (2/9) hub, the
matching branch, or Erdős #1083 has been closed.
