# Red-team audit: Euclidean interface of the identical-spectrum models

Date: 2026-07-31

Audited claims: Proposition 4 and Theorem 5 of
BREAKTHROUGH_ATTACK.md.

## 1. Verdict

| Claim | Verdict |
|---|---|
| The three-row model is an actual positive-radius reverse-circle bundle | **PASS** |
| Its three row circles have distinct heights and are pairwise nonaligned | **PASS** |
| All target points are off-axis and lie in nonperpendicular axial planes | **PASS** |
| The base-three construction gives the same properties for every finite \(k\) | **PASS** |
| The common anchor spectra and row maps are exact and injective | **PASS** |
| The construction realizes the polynomial \(2/9\) endpoint block | **NO / NOT CLAIMED** |
| It is a global few-distance counterexample to Erdős #1083 | **NO / NOT CLAIMED** |

The finite counterexamples are genuinely Euclidean, not merely formal
sumsets.  Their correct logical force is narrower: nonalignment,
positive radius, and reuse of one tangent-square universe do not by
themselves forbid arbitrarily many identical row spectra.

## 2. One coordinate chart checks every interface condition

Take the source axial plane to be \(y=0\), fix \(A=2\) and
\(\rho=1\), and use

\[
 X=\{0,1\},\qquad
 (\cos\phi_x,\sin\phi_x)=(1,0),(0,1).
\]

The anchor source points are

\[
 p_x=(A+\cos\phi_x,0,\sin\phi_x).
\tag{1}
\]

For a row indexed by a nonzero height difference \(z\), put

\[
 C_z:\quad (u-A)^2+(h+z)^2=1
\tag{2}
\]

in the source plane, and include the translated incidence points

\[
 p_{z,x}=(A+\cos\phi_x,0,-z+\sin\phi_x).
\tag{3}
\]

For every \(\tau\in T_z\), take the actual target point and selected
squared-distance label

\[
 q_{z,\tau}=(A,\sqrt{\tau},-z),\qquad
 d_\tau=1+\tau.
\tag{4}
\]

All square roots in (4) are real because every construction has
\(\tau>0\).

### Reverse-circle equation

The target point has unsigned radial coordinate
\(v=\sqrt{A^2+\tau}\) and target-plane cosine

\[
 c=\frac{A}{\sqrt{A^2+\tau}}>0.
\]

Thus \(cv=A\), so the induced reverse circle has centre
\((A,-z)\).  Its squared radius is

\[
 d_\tau-(1-c^2)v^2=(1+\tau)-\tau=1.
\tag{5}
\]

Equivalently, direct Cartesian calculation gives, for both
\(x\in X\),

\[
 \|p_{z,x}-q_{z,\tau}\|^2
 =\cos^2\phi_x+\tau+\sin^2\phi_x
 =1+\tau=d_\tau.
\tag{6}
\]

Hence every target triple in row \(z\) produces exactly the normalized
positive-radius circle \(C_z\), and \(C_z\) has both translated source
points as genuine incidences.

### Anchor spectrum

For the fixed anchor points (1),

\[
\begin{aligned}
\|p_x-q_{z,\tau}\|^2
&=\cos^2\phi_x+\tau+(z+\sin\phi_x)^2\\
&=1+z^2+\tau+2zx.
\end{aligned}
\tag{7}
\]

This is exactly the spectrum formula used in both constructions.
Thus equality of the formal spectra is equality of actual squared
distances between points in the one global configuration.

## 3. Positivity, distinctness, and nonalignment

The following checks are exact.

1. **Positive tangent squares.**  Proposition 4 uses
   \(T_*\subset\{10,\ldots,14\}\).  Theorem 5 chooses
   \(C>\max_i a_i^2/4\), so every element of
   \(C+\mathcal A_i-a_i^2/4\) is positive.
2. **Off-axis targets.**  Every target has horizontal coordinate
   \((A,\sqrt\tau)\ne(0,0)\).
3. **Nonperpendicular target planes.**  Their angle \(\beta\) from
   \(y=0\) has
   \(\cos\beta=A/\sqrt{A^2+\tau}>0\).
4. **Distinct targets.**  Equality of two targets forces equality of
   their heights, hence \(z=z'\), and equality of their positive
   transverse coordinates, hence \(\tau=\tau'\).
5. **Fixed-plane injectivity.**  For fixed \(z\) and a fixed target
   plane, positive transverse coordinates force a unique \(\tau\),
   hence a unique target and label producing \(C_z\).
6. **Distinct source incidences.**  For a fixed sine, distinct
   \(z\)'s give distinct heights; the two sine choices have different
   radial coordinates \(A+1\) and \(A\).  No translated source point
   is a target because every target has positive \(y\)-coordinate.
7. **Distinct circles.**  All constructed \(z\)'s are nonzero and
   pairwise distinct, so no row circle equals the anchor circle or
   another row circle.
8. **Nonalignment.**  The perpendicular axis of \(C_z\) is

   \[
   L_z=\{(A,s,-z):s\in\mathbb R\}.
   \]

   Distinct \(z\)'s give distinct parallel axes.  Hence the circles
   are nonaligned in the Mathialagan--Sheffer sense used upstream.

Repeated tangent squares across different rows merely put distinct
height points in the same axial target plane; this is allowed and is
the intended global-plane reuse.

## 4. Exact cardinality interface

For Proposition 4,

\[
 (S,U,H,R,|V|)
 =(2,2,3,5,4).
\]

There are six distinct target points, six translated source
incidences, five target planes, and five selected producer labels.

For Theorem 5,

\[
 S=2,\qquad H=k,\qquad U=2^{k-1},\qquad
 |V|=2^k=2U,
\]

\[
 R=\left|\bigcup_iT_{z_i}\right|\le kU.
\tag{8}
\]

There are exactly \(kU\) distinct target points and \(2k\) distinct
translated source incidences.  Because \(\tau\mapsto1+\tau\) is
injective, the selected-label count equals \(R\).  The target-plane
count also equals \(R\), since the positive transverse coordinate is
fixed by \(\tau\).

The construction is actually economical in tangent planes:
\(R/U\le k\).  Its endpoint failure is elsewhere.  With
\(U=t^{5/6+o(1)}\), it supplies only

\[
 H=k=O(\log U)=t^{o(1)}
\]

rows and keeps \(S=2\), whereas one exact endpoint spectral block
would require \(S=t^{7/9+o(1)}\) and
\(q=t^{13/18+o(1)}\) rows.  It therefore cannot be presented as a
realization of the endpoint block model.

## 5. Global-distance boundary

The common set \(V\) counts only distances from the two anchor points
to the target rows.  To make every reverse circle incidence-active,
the construction also adds the translated points (3).  Distances

- among translated source points,
- between different translated circles,
- among target points, and
- between a translated source point and a nonproducing target row

are not bounded by \(|V|=2U\) in the argument.

Consequently neither Proposition 4 nor Theorem 5 is a global
few-distance construction, and neither refutes Erdős #1083.  Any
claim that the abstract \(t^3\) block design itself has been
Euclidean-realized would also be false.  What is proved is the exact
local reverse-circle interface and the failure of bounded-exception
spectral separation.

## 6. Machine audit

verify_spectral_block_breakthrough.py now checks, for both models:

- positivity of every \(\tau\);
- radius squared exactly one;
- nonzero target-plane cosine;
- distinct rows, targets, and translated source points;
- pairwise nonalignment of the row axes;
- exact producer distances (6);
- exact anchor distances (7);
- equality of target-plane and selected-label universe sizes; and
- all spectrum and injectivity claims.

The corresponding regression assertions are in
test_verify_spectral_block_breakthrough.py.
