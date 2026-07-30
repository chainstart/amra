# Real multi-hub coordinate reuse

Date: 2026-07-30

## Purpose

`HUB_CROSS_FIBRE_ENERGY.md` shows that a collective saving
\[
 U^{2-c}L^{2+o(1)}
\]
needs \(c\geq2/5\) already at \(\eta=0\).  A pairwise argument cannot give
such a saving.  This note asks whether real order, VC dimension, pseudoline
intersection, or a second moment for the number of hub pairs served by one
height coordinate can do so collectively.

The most direct target is false.  There is an explicit real construction,
using the exact geometric radial offsets and globally shared height sets, in
which one nonhub height coordinate serves
\[
 \binom U2=\Theta(U^2)
\]
different hub pairs.  The required partner coordinates are distributed by
hub-index difference, and every receiving height set uses only \(O(U)\)
positions.

The translated hyperbola family also has too many effective parameters for
a useful Pach--Sharir estimate at the distinct-value scale.  Pairwise curve
intersection is bounded, but the point-incidence bound counts
representations and remains far larger than the selected value overlap.

No positive collective exponent \(c\) is proved.  The strongest
unconditional value remains \(c=0\).  A second-moment theorem that averages
over all coordinates is not disproved by the one-coordinate star, but it
must charge the total partner-coordinate capacity and simultaneous reuse
across many different hub-index differences.  This is a stricter target than
pointwise VC dimension or curve intersection.

No exponent improvement is claimed.

## 1. The service equation for one shared coordinate

Fix a nonhub radius class \(v\) and one coordinate \(z\in Z_v\).  A service
of \(z\) to a hub pair \(u,x\) uses
\[
 y=u+v-x
\]
and heights
\[
 a\in Z_u,\qquad c\in Z_x,\qquad d\in Z_y
\]
such that
\[
 C_{uv}+(a-z)^2=C_{xy}+(c-d)^2. \tag{1}
\]
Equivalently,
\[
 (a-c-z+d)(a+c-z-d)=\Delta_{u,x,v},
\qquad
\Delta_{u,x,v}=C_{xy}-C_{uv}. \tag{2}
\]

For fixed \(u,x,a,c\), equation (2) is a translated rectangular hyperbola
in the \((z,d)\)-plane.  Solving for \(d\) gives
\[
 d=c\pm\sqrt{(a-z)^2-\Delta_{u,x,v}}. \tag{3}
\]
The same \(z\) may be incident to many curves because \(u,x,a,c\) all vary.

For geometric radii \(\rho_j=Tq^j\), put \(h=x-u\), so \(y=v-h\).
The radial-offset difference is
\[
\begin{aligned}
\Delta_{u,u+h,v}
&=C_{u+h,v-h}-C_{u,v}\\
&=(q^{2h}-1)\rho_u^2
 +(q^{-2h}-1)\rho_v^2. \tag{4}
\end{aligned}
\]
For fixed \(h,v\), this is an affine geometric sequence in \(\rho_u^2\).
This strict convexity is real and exact, but the target set \(Z_{v-h}\)
varies with \(h\), and the hub heights \(a,c\) vary with \(u\).

## 2. A real \(U^2\)-service star

### Theorem 1 (pointwise reuse has no power saving)

For every \(U\leq m\) and \(L\geq3U+2\), there are:

- \(U\) hub radius classes;
- one nonhub radius class \(v\);
- shared real height sets of size at most \(m\); and
- one height \(z\in Z_v\)

such that \(z\) participates in an exact common shifted value for every
unordered hub pair.  Thus
\[
 r(v,z)\geq\binom U2. \tag{5}
\]
All block pairs have matching product indices and use
\[
 C_{ab}=T^2(q^a-q^b)^2.
\]

### Proof

Take the hub indices
\[
 0,1,\ldots,U-1
\]
and choose \(v=2U\).  Put zero in every hub height set.  Choose \(z>0\) so
large that
\[
 z^2+C_{uv}-C_{xy}>0
\]
for every hub pair \(u<x\), where
\[
 y=u+v-x=v-(x-u).
\]
Since \(1\leq x-u\leq U-1\), every \(y\) lies strictly between the hubs and
\(v\), and the four radius indices \(u,x,v,y\) are distinct.

For the pair \(u<x\), put
\[
 d_{u,x}
=\sqrt{z^2+C_{uv}-C_{xy}}
\quad\text{in }Z_y. \tag{6}
\]
Then
\[
 C_{uv}+z^2=C_{xy}+d_{u,x}^2, \tag{7}
\]
using the zero hub anchors.

Pairs with the same difference \(h=x-u\) use the same receiving class
\(y=v-h\).  There are exactly \(U-h\leq U\) such pairs, so every \(Z_y\)
receives at most \(U\leq m\) coordinates.  Different \(h\)'s use different
height sets.  Pad all sets to \(m\) elements.  Equation (7) proves (5).
\(\square\)

Theorem 1 explicitly handles the same \(Z_v\) coordinate across different
hub pairs.  It rules out every pointwise estimate
\[
 r(v,z)\lesssim U^{2-c}
\]
with fixed \(c>0\), even over the reals and even with the exact radial
offsets.

## 3. What a second moment would actually need

Let \(r(v,z)\) count selected overlap services assigned to a coordinate
\((v,z)\).  There are \(O(Lm)=O(L^2)\) such coordinates.  A bound
\[
 \sum_{v,z}r(v,z)^2
\lesssim U^{4-2c}L^{2+o(1)} \tag{8}
\]
would, by Cauchy--Schwarz, imply
\[
 \sum_{v,z}r(v,z)
\lesssim U^{2-c}L^{2+o(1)}, \tag{9}
\]
which has the desired capacity form.

Theorem 1 contributes \(U^4\) to the left side of (8) at one coordinate.
This does not by itself contradict (8), whose right side also contains
\(L^2\).  It proves that an argument for (8) cannot be pointwise.  It must
show that creating many \(U^2\)-service stars consumes enough coordinates in
the receiving sets \(Z_{v-h}\) to prevent replication over \(L^2\) source
coordinates.

The one-star construction consumes
\[
 \sum_{h=1}^{U-1}(U-h)=\binom U2
\]
partner positions across \(U-1\) receiving sets.  Independent replication
therefore recovers the \(O(UL^2)\) channel bound from the previous audit,
but this accounting fails when one partner coordinate itself serves many
source stars.  Bounding those iterated reuse chains is exactly the unresolved
second-moment problem.

## 4. Why pseudoline and VC arguments stop

### Bounded intersections are not enough

For fixed \((u,x,a,c)\), (2) is a degree-two curve in \((z,d)\).  Two
noncoincident curves meet in \(O(1)\) points by elimination or Bézout.
However, the family has the independent parameters
\[
 u,\ x,\ a,\ c.
\]
Even after fixing the hub-index difference \(h\), the two hub-height
parameters remain.  It is therefore not a two-degree-of-freedom pseudoline
family at the level needed for all hub pairs.

Applying a Pach--Sharir bound after freezing enough parameters counts point
representations.  The curve set then has at least \(U^2m^2\) members, while
the relevant Cartesian point sets have \(m^2\) points per neighbour pair.
The resulting incidence upper bound is much larger than the
\(\Theta(m)\) selected common values per block pair.  Multiplicity-one
overlaps again sit below the incidence scale.

### Anchor restriction becomes parallel incidence

If all hub witnesses use the zero anchor, square (1) becomes
\[
 d^2-z^2=C_{uv}-C_{xy}. \tag{10}
\]
In the \((z^2,d^2)\)-plane these are parallel lines of slope one.  The
geometric sequence (4) appears only in their intercepts.  Parallel lines do
not satisfy a transverse Szemerédi--Trotter situation; arbitrary finite
sets on the two axes can place points on any prescribed collection of these
lines subject only to coordinate capacity.  Theorem 1 is an exact example.

Consequently strict convexity of the intercept sequence, sign variation and
ordinary translate VC dimension do not control pointwise reuse.

## 5. Subtracting two services

Two services sharing \(z\) satisfy
\[
 (a_i-z)^2-(c_i-d_i)^2=\Delta_i,\qquad i=1,2.
\]
Subtracting gives
\[
 2z(a_2-a_1)
=a_2^2-a_1^2
 +(c_1-d_1)^2-(c_2-d_2)^2
 +\Delta_1-\Delta_2. \tag{11}
\]
If \(a_1\ne a_2\), the other variables determine \(z\) uniquely.  This is
not a saving: the other variables range over different arbitrary height
sets, and Theorem 1 realizes the special case \(a_1=a_2=0\) for all hub
pairs.  If \(a_1=a_2\), equation (11) merely moves the constraint to the
partner coordinates.

Repeated subtraction creates a chain of rational constraints, but without
a bound on partner-coordinate reuse it does not reduce the number of
services.  This is why a local sign-change or two-curve argument cannot
prove (8).

## 6. Best unconditional exponent from these methods

The real one-star example rules out a pointwise positive \(c\).  The
curve-family parameter count and multiplicity-one scale prevent a useful
Pach--Sharir bound.  The anchor subcase degenerates to parallel lines.
Accordingly the best unconditional collective estimate presently proved is
still
\[
 \sum_{u,x}E_{u,x}\lesssim U^2L^2, \tag{12}
\]
corresponding to
\[
 c=0.
\]

This does not prove that a collective \(c\geq2/5\) theorem is false.  It
proves that such a theorem must control iterated partner-coordinate reuse,
not individual source-coordinate reuse.

## 7. Relation to the finite-field saturation

The odd finite-field model from the previous audit allows every coordinate
to participate in a field-sized translation-invariant family, and saturates
\(U^2L^2\).  Theorem 1 shows that large pointwise stars also occur over the
reals.  The difference is global replication: finite fields recycle partner
coordinates periodically, while no analogous finite translation-invariant
real set is known.

Thus the remaining real-order statement is:

> Many \(U^2\)-service stars cannot be linked into a dense reuse network
> without either expanding the real height sets/parameter union or creating
> the high joint triangle moment.

This remains **conditional and unproved**.  No complete real construction
simultaneously saturating the second moment (8), keeping \(M\) small and
respecting all product fibres was found.

## 8. Verification

`verify_real_multi_hub_reuse.py` constructs the exact \(U^2\)-service star,
checks product sums, radial offsets, receiving-set capacities, equation
(11), and all exponent benchmarks.
