# Erdős #952: finite families of rational asymptotic corridors

Date: 2026-07-22 (Asia/Hong_Kong)

Status: rigorous extension of the round-7 one-corridor theorem; the Gaussian
moat problem remains open and this result is not a Q2-level stopping result.

## Theorem

Fix a step bound `D`.  For `1<=j<=J`, let `v_j,u_j` be integer bases of
`Z^2`, let `z_j in Z^2`, and let

\[
 g_j(T)=o\left({\log T\over\log\log T}\right).
\]

Define the affine rational corridors

\[
 \mathcal C_j=z_j+{t v_j+s u_j:t,s\in\mathbb Z,
                    |s|\le g_j(|t|)\}.
\]

The graph whose vertices are the Gaussian primes in
`union_j C_j`, with edges between vertices at Euclidean distance at most `D`,
has no infinite simple path.

Thus a hypothetical bounded-step path to infinity cannot eventually be
covered by finitely many rational directions, each with transverse error
`o(log r/log log r)`.  In particular it must change effective asymptotic
direction infinitely often, or leave this transverse scale.

## Proof

First merge all parallel directions.  After replacing a primitive direction
by its negative if needed, finitely many affine corridors with the same
direction are contained in one corridor of that direction whose width is

\[
 g(T)=\max_j g_j(T+O(1))+O(1)
     =o(\log T/\log\log T).                       \tag{1}
\]

It therefore suffices to consider pairwise nonparallel primitive directions.

For two such directions, change from either integer basis to Euclidean
coordinates.  The distance between the two underlying affine lines grows
linearly along every ray after their unique intersection, whereas both
corridor widths are `o(T)`.  Consequently their intersection is bounded.
The same linear separation shows more: for the fixed number `D`, outside a
sufficiently large ball there is no distance-`D` edge between the two
corridors.  Taking the maximum radius over the finitely many pairs gives one
ball `B` outside which different direction classes have no cross-edge.

Suppose an infinite simple path existed in the union.  It visits the finite
vertex set `B cap Z[i]` only finitely many times.  After its last such visit,
the absence of cross-edges forces the entire remaining tail into one merged
rational corridor.  The round-7 CRT transverse-wall theorem applies to that
corridor, since (1) has exactly its required width, and says that its
Gaussian-prime distance-`D` graph has no infinite simple path.  This is a
contradiction.

## Why this still does not approach a full moat

The proof depends essentially on a *fixed finite* direction family.  It gives
no uniform control when the number or arithmetic height of rational
directions grows with radius.  A path can keep turning and can use rational
approximants of increasing denominator; neither behavior is confined by the
current CRT walls.

There is also a genuine construction-scale obstacle to a naive annular CRT
wall.  A closed thickness-`D` lattice wall at radius `R` has `Omega_D(R)`
sites.  Assigning an independent prime ideal congruence to every site makes
the product modulus exponential in `R log R`, while black-box CRT gives no
location control comparable to `R`.  This is a limitation of that proof
template, not an impossibility theorem: congruence reuse or exceptional small
representatives could evade the count, so it must not be cited as ruling out
all CRT annuli.
