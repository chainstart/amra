# Translated-Latin service-incidence complex

Date: 2026-07-30

## Outcome

The preceding audit extracted two forced displacements from every paired
Gram service:
\[
 \theta=d-z,\qquad
 \psi=c-a=\mu-\lambda-\theta,
\]
where
\[
 \lambda=a-d,\qquad \mu=c-z.
\]
This note places both in one finite service-incidence complex, derives its
four- and six-cycle identities, and enumerates the smallest translated
Latin case.

The smallest meaningful case is **satisfiable**, not inconsistent.  For
\(q=3,U=2\), the ordinary radius diagonals leave two singleton boundary
blocks which can never participate in a distinct-block service.  On the
maximal pairable core, consisting of two pairs of Latin blocks, there are
exact real class translations for which:

* all six proposed Gram services hold;
* all twelve core cross edges are used exactly once;
* every local service four-cycle closes;
* the partner projection is a forest;
* the hub projection has three parallel two-cycles, all with equal
  cochain values.

This is the first genuine translated-Latin service design found in the
campaign.  It is a finite real geometric service instance with geometric
radii, not merely an abstract finite-field model.

It is **not** an asymptotic counterexample to the original distance
problem.  It has \(q=3,U=2\), omits unavoidable boundary blocks, and does
not realize the critical \(L^{33/10}\) service mass, all product fibres,
the angular layers, or a globally small distance set.  Its rigorous
consequence is narrower but important: no universal local contradiction
can follow from the double-coboundary equations alone.

No unconditional distance-exponent improvement is claimed.

## 1. One unified cochain

A service has coordinate vertices
\[
 P=(u,a),\quad P'=(x,c),\quad
 N=(v,z),\quad N'=(y,d).
\]
Its two observed cross edges have signed shifts
\[
 \lambda=a-d,\qquad \mu=c-z,
\]
and its two projection edges have shifts
\[
 \theta=d-z,\qquad \psi=c-a.
\]
Orient the four sides as
\[
 P\longrightarrow P'\longrightarrow N
 \longrightarrow N'\longrightarrow P.       \tag{1}
\]
Give them the height-difference labels
\[
 \psi,\quad-\mu,\quad\theta,\quad\lambda.     \tag{2}
\]
These labels are one 1-cochain
\[
 \omega(e)=h(\operatorname{head}e)
           -h(\operatorname{tail}e)
\]
on the finite coordinate complex.  It is the coboundary of the actual
height potential \(h\).

### Four-cycle identity

The boundary of every service 2-cell satisfies
\[
 \boxed{\quad
 \psi-\mu+\theta+\lambda=0.
 \quad}                                      \tag{3}
\]
Equivalently,
\[
 \psi+\theta=\mu-\lambda.                    \tag{4}
\]
This is the local compatibility tying the partner and hub cochains
together.  It is stronger than retaining either projection separately.

The Gram equation additionally gives
\[
 \theta
 =
 \frac{\Delta-\lambda^2+\mu^2}
      {2(\lambda+\mu)},\qquad
 \Delta=C_{xy}-C_{uv},                       \tag{5}
\]
for every distinct-block service.

## 2. Projection four- and six-cycles

Project each service to the directed partner arc
\[
 (v,z)\longrightarrow(y,d)
\]
with label \(\theta\), and to the directed hub arc
\[
 (u,a)\longrightarrow(x,c)
\]
with label \(\psi\).  Since both are restrictions of the same exact
cochain, every directed cycle has zero sum.

For a four-cycle this is
\[
\begin{aligned}
 \theta_1-\theta_2+\theta_3-\theta_4&=0,\\
 \psi_1-\psi_2+\psi_3-\psi_4&=0.             \tag{6}
\end{aligned}
\]
For a six-cycle,
\[
\begin{aligned}
 \theta_1-\theta_2+\theta_3-\theta_4
          +\theta_5-\theta_6&=0,\\
 \psi_1-\psi_2+\psi_3-\psi_4
          +\psi_5-\psi_6&=0.                 \tag{7}
\end{aligned}
\]
Parallel arcs form the still smaller two-cycle test: their labels must be
equal.

Substitution of (5) turns (6)--(7) into explicit rational identities among
radial gaps and signed cross shifts:
\[
 \sum_i(-1)^{i+1}
 \frac{\Delta_i-\lambda_i^2+\mu_i^2}
      {2(\lambda_i+\mu_i)}
 =0.                                         \tag{8}
\]

### Lemma 1 (equal-shift radial low rank)

If all services on one even projection cycle have the same ordered pair
\((\lambda,\mu)\), then its cochain identity is equivalent to
\[
 \sum_i(-1)^{i+1}\Delta_i=0.                 \tag{9}
\]

### Proof

The denominator in (8) is common.  The constant contribution
\(-\lambda^2+\mu^2\) cancels because an even alternating sum has equally
many positive and negative terms. \(\square\)

Thus a four-cycle with synchronized shifts forces
\[
 \Delta_1-\Delta_2+\Delta_3-\Delta_4=0,       \tag{10}
\]
and a six-cycle forces the analogous six-term relation.  This is the
desired low-rank/additive-separation mechanism for the radial offsets.

It is conditional on shift synchronization.  In the general
translated-Latin problem the denominators and square terms vary, and (8)
has enough freedom to be solvable.  The SAT core below is an explicit
example.

## 3. Why \(q=3,U=2\) is the first meaningful core

Latin cross blocks are indexed by
\[
 (s,p),\qquad 0\le s<U,\quad0\le p<q,
\]
and a service can pair only blocks with equal ordinary integer diagonal
\[
 s-p.                                        \tag{11}
\]
The word “ordinary” matters: radius indices do not live modulo \(q\).

For \(q=2,U=2\), only one two-block diagonal exists and the other two
blocks are singletons.  It is just one isolated translation strip, already
covered by the sharp fan of the preceding round.

For \(q=3,U=2\), the six blocks split as
\[
\begin{array}{c|c}
\text{diagonal}&\text{blocks}\\ \hline
0&(0,0),(1,1)\\
-1&(0,1),(1,2)\\
-2&(0,2)\\
1&(1,0).
\end{array}                                  \tag{12}
\]
The first two rows form a coupled pairable core; the last two are
unavoidable boundary blocks.  Coupling occurs because the two strips share
the hub translations and the middle partner class.

Each block contains the three Latin edges
\[
 x=ps+b\pmod3.
\]
There are \(3!^2=36\) possible pairs of edge matchings between the two
block pairs.  Exact polynomial enumeration produces the satisfiable choice
\[
 \pi_0=(2,0,1),\qquad
 \pi_1=(1,2,0).                              \tag{13}
\]

## 4. Exact real SAT certificate

Use geometric radii
\[
 \rho_j=2^j
\]
and put the three partner radius indices at \(5,6,7\).  Translate the
height progressions \(\{0,1,2\}\) by
\[
\begin{aligned}
 \alpha_0&=0,\\
 \alpha_1&=A=\frac{-1+\sqrt{49149}}2,\\
 \beta_0&=\frac{-1+\sqrt{49149}-\sqrt{12285}}2,\\
 \beta_1&=-\frac12,\qquad
 \beta_2=\frac12.                            \tag{14}
\end{aligned}
\]
Thus hub class \(s\) has heights
\(\alpha_s+\{0,1,2\}\), and partner class \(p\) has heights
\(\beta_p+\{0,1,2\}\).

For the first strip, pair edge \(b\) of block \((0,0)\) with edge
\(\pi_0(b)\) of block \((1,1)\).  For the second, pair edge \(b\) of
\((0,1)\) with edge \(\pi_1(b)\) of \((1,2)\).

The six Gram equations reduce exactly to two scalar relations:
\[
 A^2+A=12287,\qquad
 (A-\beta_0)^2=\frac{12285}{4}.              \tag{15}
\]
Both follow immediately from (14).  Hence all six services are exact over
the reals.

The design has
\[
\begin{array}{c|c}
\text{quantity}&\text{value}\\ \hline
\text{services}&6\\
\text{used cross edges}&12\\
\text{cross edges in pairable core}&12\\
\text{distinct cross cells}&6\\
\text{two-cell-per-block upper bound}&8.
\end{array}                                  \tag{16}
\]
Every pairable-core edge is used exactly once.

## 5. The first cochain cycles also close

The partner projection has nine vertices and six edges.  Under (13) it is
a disjoint union of three paths, so its cycle rank is zero.

The hub projection has six vertices and six service arcs.  Each strip
induces the same matching
\[
 (0,x)\longrightarrow(1,x),\qquad x=0,1,2.
\]
Thus it consists of three pairs of parallel arcs and has cycle rank three.
For each pair, both labels equal
\[
 \psi=\alpha_1-\alpha_0=A.
\]
All three parallel two-cycles therefore close.  Every local four-cycle
(3) also closes by direct symbolic verification.

The construction deliberately avoids nontrivial four- and six-cycles in
the partner projection.  It shows why local cycle testing alone does not
force radial low rank: a sparse projection complex can absorb the first
coupled strips while the repeated hub arcs agree exactly.

## 6. Abstract model versus the original geometry

The SAT certificate is stronger than an abstract service model in several
ways:

* its radius indices satisfy the actual integer product constraint;
* its radii are the genuine geometric sequence \(2^j\);
* its height sets are shared real translated arithmetic progressions;
* every service satisfies the original equality of squared Euclidean
  distances;
* both cross edges and their true cell values are retained.

It is nevertheless not a counterexample to the original asymptotic
theorem:

1. it is a fixed \(q=3,U=2\) configuration;
2. two boundary blocks are deleted;
3. every cross edge has service degree one rather than
   \(L^{2/5-o(1)}\);
4. it does not control the distance cells created by all unused radius
   pairs or angular copies;
5. it does not realize the inherited service mass or point count.

The valid negative conclusion is:

> The Gram equation, radius-diagonal pairing and simultaneous partner/hub
> coboundaries admit a nontrivial real translated-Latin core.  Therefore
> they cannot imply a universal finite forbidden pattern.

## 7. Updated gap at \(\eta=1/30\)

An asymptotic obstruction still needs
\[
 S=L^{33/10-o(1)},\qquad
 E=L^{29/10+o(1)}
\]
and therefore average compatibility degree
\[
 S/E=L^{2/5-o(1)}.                           \tag{17}
\]
The finite SAT core has degree one and supplies no power-scale
construction.

Conversely, the equal-shift Lemma 1 gives no unconditional saving because
shift synchronization has not been derived.  The exact missing theorem is
now one of:

1. a density theorem forcing many four- or six-cycles whose
   \((\lambda,\mu)\) pairs repeat, so (9) imposes additive radial-gap
   relations; or
2. an asymptotic construction extending the SAT core so every cross edge
   has \(L^{2/5-o(1)}\) compatible partners while the global cell universe
   remains small.

The first route must gain from density, not from a universal local
inconsistency.  The second must solve a growing coupled polynomial/cocycle
system, not merely paste independent two-block fans.
