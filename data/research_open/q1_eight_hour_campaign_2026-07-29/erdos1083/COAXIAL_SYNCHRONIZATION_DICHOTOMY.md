# Coaxial synchronization: a radius--height dichotomy

Date: 2026-07-29

## Purpose

`CIRCLE_INTERFACE_NO_GO.md` proves a strong distance lower bound after making
the very special assumption that all synchronized circular fibres have the
same radius.  This note removes that assumption as far as two separate
mechanisms allow, and records the exact remaining loss.

The conclusion is deliberately not advertised as an improvement to the
\(3/5\) exponent in Erdős problem 1083.  At the critical parameters it
recovers, but does not beat, the inherited scale.

## Setup

Let \(S\geq2\), and let \(C_1,\ldots,C_F\) be distinct circles with a common axis in
\(\mathbb R^3\).  Write their radii and axial heights as
\[
  \rho_i>0,\qquad z_i\in\mathbb R.
\]
Assume that every circle contains the same angular progression
\[
  A=\{0,\theta,\ldots,(S-1)\theta\},
  \qquad 0<\theta<\frac{\pi}{2S}.
\]
Let \(D\) be the number of nonzero distances determined by the union of these
\(FS\) points.  Let
\[
  L=\bigl|\{\rho_1,\ldots,\rho_F\}\bigr|,
  \qquad
  m=\max_{\rho>0}|\{i:\rho_i=\rho\}|.
\]
Since a coaxial circle is determined by its radius and height, circles counted
in one radius class have distinct heights, and
\[
  F\leq Lm.
\]

## Theorem 1 (radius--height dichotomy)

There is an absolute constant \(c>0\) such that
\[
  D\geq
  c(S-1)\max\{\sqrt L,\sqrt m\}.
\]
Consequently,
\[
  D\geq c(S-1)F^{1/4}.
\]

### Proof: distinct radii

Put
\[
  X=\{2(1-\cos(k\theta)):1\leq k<S\}.
\]
The nonzero squared chord lengths on the circle of radius \(\rho_i\) include
\[
  \rho_i^2X.
\]
Choose one circle for each distinct radius and put
\[
  R=\{\rho^2:\rho\text{ is one of those radii}\}.
\]
The global squared-distance set therefore contains \(RX\).

The sequence
\[
  \log\!\bigl(2(1-\cos(k\theta))\bigr)
  =\log4+2\log\sin(k\theta/2),
  \qquad 1\leq k<S,
\]
is strictly increasing and strictly concave.  Indeed,
\[
  \frac{d^2}{dx^2}\,2\log\sin(x\theta/2)
  =-\frac{\theta^2}{2}\csc^2(x\theta/2)<0.
\]
Its consecutive differences are therefore all distinct.  The
Ruzsa--Solymosi semiconvex sumset theorem, applied after taking logarithms,
gives
\[
  |RX|
  =|\log R+\log X|
  \geq c(S-1)\sqrt L.
\]
Taking logarithms is legitimate because all members of \(R\) and \(X\) are
positive, and it preserves cardinality.

### Proof: a repeated radius

Choose a radius occurring on \(m\) circles and let
\[
  Y=\{(z_i-z_j)^2:\rho_i=\rho_j=\rho\}.
\]
Ordering the \(m\) distinct heights and fixing the smallest one shows
\(|Y|\geq m\): its \(m\) nonnegative differences are distinct before
squaring.
For
\[
  X_\rho=\{2\rho^2(1-\cos(k\theta)):0\leq k<S\},
\]
every member of \(X_\rho+Y\) is a squared distance between two points on
circles in this radius class.

The consecutive gaps of \(X_\rho\) are
\[
  4\rho^2\sin(\theta/2)\sin((2k+1)\theta/2).
\]
They are strictly increasing under \(S\theta<\pi/2\).  A second application
of the same semiconvex sumset theorem yields
\[
  |X_\rho+Y|\geq cS\sqrt m.
\]
Removing the possible zero distance changes the bound only by one and can be
absorbed into the absolute constant.

Combining the two estimates proves the first assertion.  Since \(F\leq Lm\),
\[
  \max\{\sqrt L,\sqrt m\}\geq F^{1/4},
\]
which proves the second. \(\square\)

## Proposition 2 (the common-angle planar slice)

Under the same assumptions,
\[
  D\geq c\,\frac{F}{\log F}
\]
for an absolute constant \(c>0\) and all sufficiently large \(F\).

### Proof

Take from each circle its point of angle zero.  These \(F\) distinct points
all lie in the meridian half-plane through the common axis and have planar
coordinates \((\rho_i,z_i)\).  Their planar distances are distances in the
original three-dimensional configuration.  The Guth--Katz planar distinct
distance theorem gives the displayed bound. \(\square\)

Combining the two conclusions gives the unconditional synchronized-fibre
bound
\[
  D\geq
  c\max\left\{\frac{F}{\log F},
               (S-1)\sqrt L,
               (S-1)\sqrt m\right\}.
\]

### Collision and hypothesis audit

The two semiconvex applications do not assume that their displayed distance
subsets are disjoint from any other distances.  They use only the inclusions
\[
 RX\subseteq\Delta^2(P),\qquad
 X_\rho+Y\subseteq\Delta^2(P),
\]
where \(\Delta^2(P)\) denotes the set of squared distances.  Collisions with
distances outside a displayed subset therefore cannot weaken its lower
bound.  Inside \(RX\), taking logarithms is injective because both factors
are positive.  Inside \(X_\rho+Y\), the semiconvex theorem already counts
all additive collisions.

The short-arc hypothesis is used only to make the relevant consecutive gaps
strictly monotone.  Irrationality of \(\theta/\pi\) is not needed here:
\(0<k\theta<\pi/2\) already makes all chord values in the proof distinct.
Positivity of the radii is needed for the logarithmic argument.  Finally,
choosing the smallest height in a repeated-radius class makes the \(m\)
fixed-base squared height differences distinct.

## Critical-scale diagnosis

For the full rectangular local-interface model from
`CIRCLE_INTERFACE_NO_GO.md`,
\[
  S=N^{2/5},\qquad F=N^{3/5}.
\]
The new arbitrary-radius estimates give
\[
  (S-1)F^{1/4}=N^{11/20-o(1)}
\]
and
\[
  \frac{F}{\log F}=N^{3/5-o(1)}.
\]
Thus the planar slice reaches exactly the inherited critical exponent, while
the radius--height dichotomy is weaker.  In particular, merely extracting a
common angular progression on many otherwise arbitrary coaxial circles does
not, through these separate mechanisms, yield a fixed-power improvement.

The earlier equal-radius theorem corresponds to \(m=F\) and gives
\[
  D\geq cS\sqrt F=N^{7/10},
\]
which is much stronger.  The loss occurs precisely when the fibres split
between many radii and many heights per radius.

## Refined remaining target

A successful continuation must provide at least one of the following.

1. **Radius concentration:** extract a synchronized subfamily with
   \(m\geq F^{1-o(1)}\), so that the equal-radius mechanism survives with
   only subpolynomial loss.
2. **Radial expansion:** extract \(L\geq F^{1-o(1)}\), which likewise lets
   the multiplicative semiconvex estimate give \(S\sqrt F\).
3. **Genuinely joint expansion:** prove a bound using the full two-parameter
   quantities
   \[
     (\rho_i-\rho_j)^2+(z_i-z_j)^2
     +2\rho_i\rho_j(1-\cos(k\theta)),
   \]
   rather than taking the maximum of a radius-only and a height-only bound.

The balanced regime \(L\asymp m\asymp F^{1/2}\) is the precise obstruction
left by Theorem 1.  Any proposed synchronization lemma that does not address
that regime cannot by itself improve the \(3/5\) exponent.

The exact joint affine-copy reductions, including the all-pairs parameter-line
target, are recorded in `AFFINE_COPY_REDUCTION_AND_BARRIER.md`.

## Source

The sumset input is I. Ruzsa and J. Solymosi, *Sumsets of Semiconvex Sets*,
Canadian Mathematical Bulletin 65 (2022), 230--237,
doi:10.4153/S0008439521000096, Theorem 1.  It states that a monotone real set
with pairwise distinct consecutive differences satisfies
\[
  |A+B|\geq c|A||B|^{1/2}
\]
for every finite real set \(B\).

The planar input is L. Guth and N. H. Katz, *On the Erdős distinct distances
problem in the plane*, Annals of Mathematics 181 (2015), 155--190.
