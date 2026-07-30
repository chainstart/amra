# Independent red-team audit of the angular-starvation branch

Date: 2026-07-30

Audited file: `ANGULAR_STARVATION_BRANCH_ATTACK.md`

## Verdict

\[
\boxed{\text{PASS}}
\]

The revised document passes the strict proof audit.  The central
unconditional conclusion
\[
\mathfrak C_{\rm plane}\ge N^{13/5-o(1)}
\]
is correct.  Lemma 2 now gives the accurate coordinate classification:
equal planes are harmless, while perpendicular planes with same-height
antipodal targets are the genuine positive-dimensional exception.
Proposition 4 now binds the energy-selected radius \(\rho_*\), occupied
anchor height \(z_0\), deleted anchor circle, and
\(\lambda(\rho_*,z_0)\) in the correct quantifier order.

## 1. Coordinate audit of Lemma 2

Rotate coordinates so that the target plane \(\Pi_\beta\) is the
\((v,w)\)-plane and the common axis is the \(w\)-axis.  Write a source
point of \(\Pi_\alpha\) as \((u,z)\), where \(u\ne0\) is signed radial
coordinate, and put
\[
c=\cos(\alpha-\beta).
\]
For a target point \((v,w)\), the fixed squared-distance equation is
\[
u^2+v^2-2cuv+(z-w)^2=d.                              \tag{A}
\]

### 1.1 Repeated circles

For fixed source \((u,z)\), equation (A), viewed in \((v,w)\), is
\[
v^2+w^2-2cu\,v-2z\,w+u^2+z^2-d=0.                  \tag{B}
\]
Thus the target circle has center \((cu,z)\) and squared radius
\[
d-(1-c^2)u^2.
\]
Two normalized circle equations arising from \((u_1,z_1)\) and
\((u_2,z_2)\) coincide exactly when
\[
c(u_1-u_2)=0,\qquad z_1=z_2,\qquad u_1^2=u_2^2.
\tag{C}
\]
If the planes are not perpendicular, then \(c\ne0\), and (C) forces
\((u_1,z_1)=(u_2,z_2)\).  Hence the nonexceptional family has no
repeated circles at all; the claimed “absolute multiplicity” can be
taken to be one.

When \(c=0\), the two opposite source points \((u,z)\) and \((-u,z)\)
produce the same circle.  Their multiplicity is two, but this is not
the only perpendicular-plane problem.

### 1.2 Number of circles through two target points

Let \(y_i=(v_i,w_i)\), \(i=1,2\), be distinct target points.  Subtracting
their two equations (A) gives the affine line
\[
-2c(v_1-v_2)u-2(w_1-w_2)z
+v_1^2+w_1^2-v_2^2-w_2^2=0.                        \tag{D}
\]
If (D) is not the zero polynomial, its intersection with either source
circle (A) contains at most two real points.  Therefore at most two
members of the source-indexed family pass through \(y_1,y_2\).

For distinct \(y_1,y_2\), equation (D) is identically zero exactly in
the following case:
\[
c=0,\qquad w_1=w_2,\qquad v_2=-v_1\ne0.             \tag{E}
\]
That is, the planes are perpendicular and the target points are
same-height antipodes.  Then their two distance equations coincide,
and an arbitrary number of selected source points can lie on that
source circle.  This is the positive-dimensional degeneracy that
invalidates the two-degree-of-freedom condition.

For equal planes \(c=1\) (or \(c=-1\) under the opposite orientation),
(D) cannot vanish for distinct target points.  Equal planes are
therefore not degenerate.  The revised text states this explicitly;
removing their \(M\) ordered pairs is permitted but unnecessary.

Point and empty intersections cause no difficulty: empty curves
contribute nothing, and point circles contribute at most one incidence
each.  All remaining curves have bounded algebraic complexity, distinct
curves meet in at most two points, and any two target points belong to
at most two curves.  The standard two-degrees-of-freedom circle
incidence bound consequently yields
\[
R_{\alpha,\beta}(d)\ll Q^{4/3}+Q
\]
for every retained nonperpendicular pair.  Equations (14a)--(14b) in
the revision now contain precisely this classification, so Lemma 2
passes as written.

## 2. Audit of Theorem 3

There are \(M^2\) ordered plane pairs.  Equal pairs number \(M\), and
each plane has at most one perpendicular partner modulo \(\pi\), so
discarding both classes removes only \(O(M)\) pairs.  Since every source
plane has \(Q=N^{3/5-o(1)}\) points,
\[
\sum_{(\alpha,\beta)\in\mathcal G}\sum_d
R_{\alpha,\beta}(d)
=(M^2-O(M))Q^2
=(1-o(1))M^2Q^2.                                    \tag{F}
\]
The off-axis sets are disjoint because an off-axis point determines its
axial plane modulo \(\pi\).  Every label in (F) belongs to the global
set of at most \(D+1\) squared distances.  Hence
\[
\mathfrak E_{\rm all}
\ge \frac{(1-o(1))M^4Q^4}{D+1}
=N^{13/5-o(1)}.                                     \tag{G}
\]

For every retained pair,
\[
\sum_dR_{\alpha,\beta}(d)^2
\le (Q^{4/3}+Q)Q^2
\ll Q^{10/3}+Q^3.
\]
Summing over \(O(M^2)\) plane pairs gives
\[
\mathfrak E_{\rm diag}
\ll M^2Q^{10/3}
=N^{12/5+o(1)}.                                     \tag{H}
\]
The exponents are independently:
\[
4\cdot\frac15+4\cdot\frac35-\frac35=\frac{13}{5},
\qquad
2\cdot\frac15+\frac{10}{3}\cdot\frac35=\frac{12}{5}.
\]
Thus (H) is smaller than (G) by \(N^{1/5-o(1)}\), and subtraction proves
Theorem 3.  No source-plane mass or ordered/unordered factor changes an
exponent.  This portion passes.

## 3. Quantifier audit of the revised Proposition 4

The energy inequality gives existence of a radius \(\rho_*\) satisfying
\[
I_{\rho_*}
\ge\frac{\mathfrak E_{\rho\angle}}{\sum_\rho I_\rho}
=\frac{\mathfrak E_{\rho\angle}}{MQ}
\ge N^{3/5+\delta-o(1)}.                            \tag{I}
\]
To apply the sparse Xi theorem at that radius, one must also choose an
occupied anchor height \(z_0\) on \(\rho_*\), delete its circle, and
define
\[
A_{\rho_*,z_0}
=\{(z-z_0)^2:
\text{an undeleted source point of radius }\rho_*
\text{ occurs at height }z\},
\]
\[
\lambda(\rho_*,z_0)
=\max_{t\ne0}
|A_{\rho_*,z_0}\cap(A_{\rho_*,z_0}+t)|.
\tag{J}
\]

The revision now performs exactly this choice in (25a), then assumes an
occupied \(z_0\) on this same \(\rho_*\), defines the post-deletion set
\(A_{\rho_*,z_0}\), and imposes (25b) on
\(\lambda(\rho_*,z_0)\).  Thus the high-\(I\) witness and the
small-\(\lambda\) witness can no longer be different radii.

The remaining calculation is valid.  Deleting one anchor circle loses
at most \(2M\) incidences
because there are at most \(2M\) actual angular columns.  Since
\(I_{\rho_*}=N^{3/5+\delta-o(1)}\), this loss is negligible.  With
\(J\le2M=N^{1/5+o(1)}\) and
\(\lambda(\rho_*,z_0)\le N^{o(1)}\),
\[
\frac{I_{\rho_*}^2}
 {2I_{\rho_*}+\lambda(\rho_*,z_0)J^2}
\ge N^{3/5+\delta-o(1)}.
\tag{K}
\]
Indeed the two candidate quotient exponents are
\[
\frac35+\delta,\qquad \frac45+2\delta,
\]
so the first controls.

For hypothesis (25), the proof first uses
\(\mathfrak E_{\rho\angle}\ge\mathfrak C_{\rho\angle}\) and then makes
the same bound choice.  Proposition 4 therefore passes.

## 4. Independent verifier

`verify_angular_starvation_independent_audit.py`:

- derives the normalized target-circle coefficients from (A);
- verifies injectivity for \(c\ne0\) and the perpendicular
  opposite-source repetition;
- detects precisely the perpendicular same-height antipodal
  two-target degeneracy;
- checks by resultants that nondegenerate two-target systems are at
  most quadratic;
- recomputes the \(13/5\), \(12/5\), and \(1/5\) exponents; and
- supplies an abstract two-radius counterexample to the unbound
  small-\(\lambda\) reading.

Run:

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/erdos1083/geometric
pytest -q test_verify_angular_starvation_independent_audit.py
python3 verify_angular_starvation_independent_audit.py
```

The verifier is a finite algebra check and does not replace the
incidence theorem.  Its role is to certify the coordinate identities,
exception classification, and exponent arithmetic used in this audit.

## 5. Separate verdict on `CROSS_PLANE_TO_RADIUS_TRANSFER_ATTACK.md`

### Audited claim

The new equations (32a)--(32c) claim that the ruled family
\[
P_t=\{(a,ja,z):
j\in\mathcal J_t,\ 1\le a\le t,\ 0\le z<t^2\}
\]
determines
\[
|\Delta^2(P_t)|=t^{4-o(1)}.
\]

### Verdict

\[
\boxed{\text{PASS FOR (32a)--(32c)}}
\]

Let \(k_0=\min\mathcal J_t\) and
\(\mathcal L=\{j-k_0:j\in\mathcal J_t,\ j>k_0\}\).  Because translation
by \(k_0\) is injective,
\[
|\mathcal L|=|\mathcal J_t|-1=t^{1-o(1)},
\qquad \mathcal L\subseteq\{1,\ldots,t-1\}.
\]
The fact that \(k_0\) may depend on \(t\) is irrelevant; only these two
properties are used.

For
\[
\mathcal X=\{a\ell:1\le a\le t,\ \ell\in\mathcal L\},
\]
the fibre over a positive integer \(n\le t^2\) contains at most one
pair for each positive divisor \(a\mid n\).  Hence
\[
|\mathcal X|
\ge
\frac{t|\mathcal L|}
{\max_{n\le t^2}\tau(n)}
=t^{2-o(1)}.                                        \tag{L}
\]
This is valid for an arbitrary set \(\mathcal L\); no interval or
equidistribution assumption is hidden in (L).

For each \(x=a(j-k_0)\in\mathcal X\) and every
\(0\le u<t^2\), choose the actual pair
\[
(a,ja,u),\qquad (a,k_0a,0)
\]
from \(P_t\).  Its squared distance is exactly
\[
x^2+u^2.
\]
Thus all \(|\mathcal X|t^2=t^{4-o(1)}\) input pairs used in the
counting argument are genuinely realized.

Every resulting label is a positive integer \(n<2t^4\).  The number of
input pairs \((x,u)\), with \(x>0\) and \(u\ge0\), mapping to a fixed
\(n\) is at most the full two-square representation number
\[
r_2(n)\le4\tau(n)
\le \max_{m<2t^4}4\tau(m)
=t^{o(1)}.                                          \tag{M}
\]
Dividing the input count by this maximum fibre gives
\[
|\Delta^2(P_t)|\ge t^{4-o(1)}.
\]
The coordinate range in (25) gives the matching
\(|\Delta^2(P_t)|=O(t^4)\), proving (32a).

The independent verifier now also enumerates the two successive maps
\[
(a,\ell)\mapsto a\ell,\qquad
(x,u)\mapsto x^2+u^2,
\]
checks their fibres against \(\tau(n)\) and \(4\tau(n)\), verifies that
the labels stay below \(2t^4\), and confirms the two quotient lower
bounds for finite \(t\).  These checks corroborate the all-orders
divisor arguments (L)--(M).
