# Hub cross-fibre energy and the required collective saving

Date: 2026-07-30

## Purpose

The hub concentration audit leaves the abstract capacity
\[
 {\cal D}_{\rm low,low}\lesssim U^2L^2.
\]
This note organizes it as a four-endpoint cross-fibre energy and asks
whether geometry saves a power of \(U\).

Three conclusions are rigorous.

1. A bound \(U^{2-c}L^{2+o(1)}\) closes the target only for
   \[
   c\geq\frac{2+30\eta}{5+12\eta};
   \]
   at \(\eta=0\), this requires \(c\geq2/5\).
2. No positive saving holds for one fixed hub pair.  An explicit real
   construction with the exact radial offsets has \(\Theta(L)\) product
   fibres and linear overlap in each, hence energy \(\Theta(L^2)\).
3. Over odd finite fields the complete \(U^2L^2\) capacity is attainable
   with globally shared height sets and geometric radii.  A successful real
   proof must therefore use order/nonperiodicity and collective competition
   among many hub pairs for the same height coordinates.

No collective real saving or complete real counterexample was found.  No
exponent improvement is claimed.

## 1. Four-endpoint energy

Fix hub indices \(u,x\).  For every valid \(v\), put
\[
 y=u+v-x,
\]
so \(u+v=x+y\).  Define
\[
 E_{u,x}
 =
 \sum_v
 |(C_{uv}+A_{uv})\cap(C_{xy}+A_{xy})|, \tag{1}
\]
where \(|A_{ab}|=k=\Theta(L)\).

One common value, after choosing point representations, satisfies
\[
 (z_u-z_v)^2-(z_x-z_y)^2=C_{xy}-C_{uv}, \tag{2}
\]
or
\[
 (z_u+z_y-z_v-z_x)
 (z_u+z_x-z_v-z_y)=C_{xy}-C_{uv}. \tag{3}
\]
Thus (1) is a four-part energy repeated across product fibres, reusing the
same two hub sets \(Z_u,Z_x\).

After orienting every low block toward a hub endpoint,
\[
 {\cal D}_{\rm low,low}
\lesssim\sum_{u,x\in U}E_{u,x}. \tag{4}
\]
The trivial \(E_{u,x}\leq Lk=O(L^2)\) recovers \(U^2L^2\).

## 2. Exact saving required

Suppose
\[
 \sum_{u,x\in U}E_{u,x}
\lesssim U^{2-c}L^{2+o(1)}. \tag{5}
\]
Comparison with
\[
 {\cal D}_{\rm low,low}
\gtrsim L^{10/3-\eta-o(1)}
\]
gives
\[
 U\gtrsim
 L^{(4/3-\eta)/(2-c)-o(1)}. \tag{6}
\]
The previous audit needs
\[
 U\gtrsim L^{5/6+2\eta-o(1)}. \tag{7}
\]
Equating (6)--(7) yields
\[
\begin{aligned}
 c
 &\geq
 2-\frac{4/3-\eta}{5/6+2\eta}\\
 &=\frac{2+30\eta}{5+12\eta}. \tag{8}
\end{aligned}
\]
In particular \(c\geq2/5\) at \(\eta=0\).  A logarithmic or arbitrarily
small power saving is insufficient.

## 3. Why point incidences are on the wrong scale

For one block pair, represented point quadruples are counted by
\[
 \sum_{s^2-t^2=\Delta}
 r_{Z_u-Z_v}(s)r_{Z_x-Z_y}(t). \tag{9}
\]
Splitting \(t=\pm\sqrt{s^2-\Delta}\) gives incidences between \(m^2\) points
and \(m^2\) translates of finitely many strictly convex/concave graph
branches.  A pseudoline argument gives at best \(O(m^{8/3})\) point
solutions.  To see this directly on one branch, write its graph as
\[
 c=d+\sigma f(a-b),
 \qquad f(s)=\sqrt{s^2-\Delta}.
\]
The curves are indexed by \((a,d)\), and the points are
\((b,c)\in Z_v\times Z_x\).  On each real domain branch \(f'\) is strictly
monotone.  Hence the difference of two distinct horizontal translates of
\(f\) is strictly monotone on their common branch, so two curves meet at
most once.  The same derivative argument, with the two point abscissae
fixed, shows that two points lie on at most one curve.  Splitting into the
constant number of sign/domain branches and applying the pseudoline
Szemerédi--Trotter proof gives
\[
 O((m^2)^{2/3}(m^2)^{2/3}+m^2)=O(m^{8/3}).
\]

This does not control (1): one common selected value can have one
representation, while its value-overlap cap is only \(k=\Theta(m)\).
Since \(m<m^{8/3}\), the incidence estimate is too large.  BSG encounters
the same multiplicity-one obstruction.

## 4. A real one-hub-pair saturation

### Theorem 1 (no pairwise power saving)

Fix \(u\ne x\) with \(h=x-u=O(1)\).  For all sufficiently large \(L,m\),
there are shared \(m\)-point real sets \(Z_0,\ldots,Z_{L-1}\) such that for
\(\Theta(L)\) valid \(v\), with \(y=v-h\),
\[
 |S_{uv}\cap S_{xy}|\geq\lfloor(m-1)/2\rfloor. \tag{10}
\]
Consequently \(E_{u,x}=\Theta(Lm)=\Theta(L^2)\) in the balanced regime.
The construction uses the exact offsets
\[
 C_{ab}=T^2(q^a-q^b)^2.
\]

### Proof

Put zero in both hub sets and let \(r=\lfloor(m-1)/2\rfloor\).  For each
valid \(v\), excluding the \(O(1)\) indices meeting the hubs, set \(y=v-h\)
and
\[
 \Delta_v=C_{xy}-C_{uv}.
\]
Choose distinct large rational parameters \(s_{v,j}\) and put
\[
\alpha_{v,j}
=\frac{s_{v,j}+\Delta_v/s_{v,j}}2,\qquad
\beta_{v,j}
=\frac{\Delta_v/s_{v,j}-s_{v,j}}2. \tag{11}
\]
Then \(\alpha_{v,j}^2-\beta_{v,j}^2=\Delta_v\).

Place the \(\alpha_{v,j}\)'s in \(Z_v\) and the \(\beta_{v,j}\)'s in
\(Z_y\).  A nonhub set receives at most two channels, of total size
\(2r\leq m-1\); choose parameters generically and pad to \(m\) points.
For
\[
 t_{v,j}=C_{uv}+\alpha_{v,j}^2
\]
one has
\[
 t_{v,j}=C_{xy}+\beta_{v,j}^2.
\]
The zero anchors realize all \(r\) common values. \(\square\)

Generic padding can make full difference blocks incident to the hubs
quadratic in size.  Thus the example also fits the local low-link regime.
It rules out any proof based on a pairwise bound
\(E_{u,x}\leq L^{2-c}\).

## 5. The genuinely collective issue

If the construction is independently repeated on a graph of hub pairs of
maximum degree \(\Delta_H\), every nonhub height set receives
\(\Theta(\Delta_Hr)\) channels.  Its \(m\)-point capacity forces
\[
 r\lesssim m/\Delta_H.
\]
The total independently allocated energy is then only
\[
 O(UL^2), \tag{12}
\]
not \(U^2L^2\).

Saturating the abstract bound requires the same height coordinates to serve
many hub-pair correlations.  This is the only remaining opportunity for a
collective saving, and it is also where triangle compatibility re-enters.

A useful but **unproved conditional statement** is:

> One height-coordinate channel serves at most
> \(U^{1-c+o(1)}\) independent hub-pair systems, for a \(c\) satisfying
> (8).

Theorem 1 shows that “independent” must encode simultaneous multi-hub
compatibility, not the number of product fibres.

## 6. A complete odd finite-field saturation

### Proposition 2 (field-uniform saving is false)

Let \(\mathbb F_Q\) be an odd finite field, let \(\gamma\) generate its
multiplicative group, and take
\[
 L<(Q-1)/2,\qquad \rho_u=\gamma^u,\qquad Z_u=\mathbb F_Q.
\]
Put \(C_{uv}=(\rho_u-\rho_v)^2\).  Then every squared-difference block is
the quadratic-residue set
\[
 {\cal Q}=\{z^2:z\in\mathbb F_Q\}.
\]
Every shifted block has \(\Theta(Q)\) elements, two translates intersect in
\(Q/4+O(1)\), and every product-fibre union has at most \(Q\) elements.
For \(Q\asymp L\),
\[
 M=O(L^2),\qquad {\cal D}=\Theta(L^4). \tag{13}
\]

### Proof

Since \(Z_u-Z_v=\mathbb F_Q\), its squares are \({\cal Q}\).  Translation
by \(C_{uv}\) preserves size.  The standard quadratic-character sum gives
\[
 |({\cal Q}+a)\cap({\cal Q}+b)|=Q/4+O(1)
\]
for \(a\ne b\); equal translates have \((Q+1)/2\) values.  Restricting
integer exponents to \(2L<Q-1\) avoids product wraparound.  There are
\(\Theta(L)\) product fibres and \(\Theta(L^3)\) same-fibre block pairs,
which gives (13). \(\square\)

This respects the product-fibre matching and radial-offset formula, but does
not embed in the ordered reals.  It rules out a field-uniform polynomial
incidence, rank, spectral or positivity proof of (5).  The model has
abundant triangle links, so it does not refute the joint-moment alternative.

## 7. Status of the proposed approaches

- **Sum-product:** Theorem 1 realizes \(L^2\) energy by assigning independent
  hyperbola parameters along one hub-pair chain.  A sum-product theorem
  needs a common factor set across many hub pairs; none is yet extracted.
- **Spectral norm:** One fibre's overlap matrix is a Gram matrix and can have
  off-diagonal mass \(U^2k\).  Theorem 1 defeats pairwise cross-fibre
  savings; Proposition 2 defeats field-uniform collective savings.
- **Real incidence:** Pseudoline bounds count point representations and are
  too weak at multiplicity one.  A useful theorem must charge simultaneous
  use of one real height coordinate by many hub pairs.

## 8. Exact remaining alternative

The following remains **conditional and unproved**:

> For real height sets and geometric-progression radii, either (5) holds for
> a \(c\) satisfying (8), or the coordinate reuse violating (5) forces
> \({\cal J}\geq L^{11/3+\eta-o(1)}\).

Theorem 1 rules out a pairwise proof.  Proposition 2 rules out a
field-uniform proof.  What remains is a collective, real-order,
shared-coordinate theorem.  No complete real model satisfying small \(M\)
and saturating \(U^2L^2\) was found.

## 9. Verification

`verify_hub_cross_fibre_energy.py` checks the required \(c\), constructs the
exact rational one-hub-pair model, and verifies the odd-prime finite-field
saturation.
