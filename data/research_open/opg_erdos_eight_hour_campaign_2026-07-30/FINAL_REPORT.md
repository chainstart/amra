# OPG-1757 and Erdős #1083: eight-hour research report

Date: 2026-07-30

## 1. Executive outcome

The campaign did not prove either original conjecture.  It did,
however, close a substantial all-rank theorem package on the
OPG side and replace the principal Erdős aggregate-energy gap by a
strict structural dichotomy with a sharp abstract obstruction.

The strongest OPG chain obtained in the campaign is
\[
\boxed{
\begin{gathered}
B_r(t)=\frac{N_r(t)}{(1-t)^{3r+1}},\qquad
\deg_d\beta_{d,r}=3r,\qquad
(-1)^r[d^{3r}]\beta_{d,r}>0,\\
\deg\mathfrak h_j=3j,\qquad
\prod_{m=j}^{2j-1}(d-m)\mid\mathfrak h_j(d),\\
\deg\mathfrak g_q=3q+2,\qquad
[d^{3q+2}]\mathfrak g_q(d)>0.
\end{gathered}}
\]
Every fixed long-recurrence band is therefore eventually positive.
These are unbounded theorems, not extrapolations from the computed
ranks.  Moreover, for each specified band, full positivity over all
admissible integer depths is decidable by a terminating exact-rational
algorithm.  This effectiveness statement does not prove that every
band passes the decision.

On the Erdős side, for every fixed \(0<\kappa<1\), the critical
plane-codegree ledger forces either
\[
t^{1-o(1)}
\text{ labels with a }t^{\kappa-o(1)}
\text{-matching of rich plane pairs},
\]
or one plane is a hub for
\[
t^{2-2\kappa-o(1)}
\text{ labels, with }t^{5-\kappa-o(1)}
\text{ rich mass per label}.
\]
A deterministic quadratic finite-field tensor saturates the critical
ledger while containing no \(K_{3,2}\).  Hence aggregate energy plus
matching extraction alone cannot improve the \(3/5\) exponent; a
genuinely Euclidean theorem is still needed.

The Euclidean reverse-circle incidence theorem now eliminates the hub
alternative throughout \(\kappa<1/5\).  Consequently, for every fixed
\(\varepsilon>0\), the critical codegree forces
\[
t^{1-o(1)}
\text{ labels, each with a }
t^{1/5-\varepsilon-o(1)}
\text{-matching of rich plane pairs}.
\]
For the wider range \(\kappa<1/3\), any surviving hub forces an
incidence-active repeated reverse circle of multiplicity
\[
\mu\ge t^{(5-15\kappa)/2-o(1)}.
\]
The strengthened exponent comes from a weighted dyadic decomposition
of the merged circle classes; the earlier \(/11\) exponent resulted
from multiplying the entire unweighted incidence bound by the maximum
circle weight.
The complete layer-cake proof and independent exponent audit are in
[`WEIGHTED_REVERSE_CIRCLE_DYADIC_REFINEMENT.md`](erdos1083/geometric/WEIGHTED_REVERSE_CIRCLE_DYADIC_REFINEMENT.md).
This is a genuine Euclidean structural refinement, but it does not
improve the \(3/5\) distinct-distance exponent.

The subsequent red-team attack identifies the exact limit of that
repeated-circle conclusion.  One repeated reverse circle is a circle
together with its perpendicular axis.  It forces \(\mu\) distinct
target planes, at least \(\lceil\mu/2\rceil\) labels, and
\(\mu-1\) target--target distances, but an explicit
regular-polygon/arithmetic-progression model has \(n\mu\) cross
representations and only \(O(n+\mu)\) total distances.  Thus one
circle-axis chart cannot be the missing exponent lemma.

The independently audited two-chart extension closes the next naive
escape.  Two concentric regular \(n\)-gons of different radii, with a
common odd arithmetic progression of \(2m\) axis points, realize
\(4mn\) repeated-circle representations but at most
\[
3\lfloor n/2\rfloor+4m
\]
total squared distances.  More generally, every fixed number \(K\)
of concentric radii has an \(O(K^2n+Km+m)\) model.  Thus neither the
number of charts nor radius diversity alone supplies expansion.  This
does not address the remaining exceptional geometries and is not an
exponent improvement.  In particular, nonconcentricity alone is not a
valid replacement hypothesis: the known two-circle classification has
a second linear-distance family consisting of perpendicular circles.
For the retained off-axis reverse circles that second family is
impossible, because every radial centre parameter
\(A=\cos(\alpha-\beta)v\) is nonzero.  Consequently the exact missing
step is to extract two sufficiently incidence-rich nonaligned circles,
not to prove another two-circle distance theorem.

This bridge also yields a new concentration corollary.  For every
fixed \(\eta>0\), all active circles in one hub plane with at least
\(t^{9/4+\eta}\) source incidences must be concentric.  Their source
sets are disjoint and each merged circle has triple multiplicity at
most \(M\), so their total weighted mass is at most
\[
MQ=t^{4+o(1)}=o\!\left(t^{7-3\kappa-o(1)}\right)
\qquad(\kappa<1).
\]
Thus the principal hub mass cannot hide on one or several
exceptionally rich circles; it is forced onto the much larger sector
of circles below this richness threshold.

## 2. OPG-1757 milestones

### 2.1 All-rank ordinary symbols

The central theorem is
[`ALL_RANK_ORDINARY_SYMBOL_DEGREE_THEOREM.md`](opg1757/top_newton_tail_2026-07-30/ALL_RANK_ORDINARY_SYMBOL_DEGREE_THEOREM.md).
Its endpoint gap is closed by the exact complement-length identity in
[`COMPLEMENTARY_ENDPOINT_LOCALIZATION_LEMMA.md`](opg1757/top_newton_tail_2026-07-30/COMPLEMENTARY_ENDPOINT_LOCALIZATION_LEMMA.md).
Independent audits check the endpoint normalization, saddle choice,
marked Laurent cancellation, low-rank boundary, and leading
convolution sign.

The theorem proves, uniformly in \(r\),
\[
B_r(t)=\frac{N_r(t)}{(1-t)^{3r+1}},\qquad
\deg N_r\le4r,\qquad t^r\mid N_r,
\]
and hence an exact degree-\(3r\) polynomial
\(\beta_{d,r}=P_r(d)\) for \(d\ge r\), with alternating nonzero
leading sign.

### 2.2 Falling triangle and long recurrence

[`ORDINARY_ALL_RANK_FALLING_TRIANGLE_COROLLARY.md`](opg1757/top_newton_tail_2026-07-30/ORDINARY_ALL_RANK_FALLING_TRIANGLE_COROLLARY.md)
turns the ordinary-symbol theorem into exact falling-basis degrees and
forced integer roots.  The independent audit verifies that every use
of \(P_r(d)\) lies in its valid range.

The leading long-recurrence coefficients satisfy the exact identity
\[
\sum_{q\ge0}G_qz^{q+1}
=-3z\frac{H'(z)}{H(z)}.
\]
The final theorem,
[`ORDINARY_ALL_RANK_RECURRENCE_LEADING_POSITIVITY_THEOREM.md`](opg1757/top_newton_tail_2026-07-30/ORDINARY_ALL_RANK_RECURRENCE_LEADING_POSITIVITY_THEOREM.md),
proves \(G_q>0\) at every rank.  Its proof has two independently
checkable pieces:

1. exact rational verification of the finite prefix; and
2. an unbounded complex-analytic tail argument.

The tail argument bounds the coefficients of \(H\), proves by
Rouché that \(H\) has one positive zero in \((0,2)\) and no other
zero of modulus at most \(2.1\), then uses genus-zero Hadamard
factorization and Jensen zero counting to show that the first zero
dominates every reciprocal zero power sum from order \(100\) onward.

The formal \({}_2F_0\), Airy/Bessel, and symmetric-square ODE behind
the highest layer are isolated in
[`HIGHEST_LAYER_HYPERGEOMETRIC_ODE_STRUCTURE_LEMMA.md`](opg1757/top_newton_tail_2026-07-30/HIGHEST_LAYER_HYPERGEOMETRIC_ODE_STRUCTURE_LEMMA.md).

At the finite end, the rank-six symbol now closes
[`ORDINARY_SIXTH_LONG_RECURRENCE_BAND_THEOREM.md`](opg1757/top_newton_tail_2026-07-30/ORDINARY_SIXTH_LONG_RECURRENCE_BAND_THEOREM.md):
\(\gamma_{d,5}>0\) for every \(d\ge11\).  Its independent
reconstruction uses Faulhaber power sums and Newton identities rather
than the author's signed-Stirling recurrence, and verifies all
eighteen positive coefficients after the shift \(d=u+11\).

The next independently audited application,
[`ORDINARY_RANK_SEVEN_AND_SEVENTH_BAND_THEOREM.md`](opg1757/top_newton_tail_2026-07-30/ORDINARY_RANK_SEVEN_AND_SEVENTH_BAND_THEOREM.md),
uses the all-rank degree theorem rather than an empirical degree guess.
Twenty-two exact depths uniquely determine the degree-\(21\) symbol
\(\beta_{d,7}\), and four depths are held out.  A second implementation
uses different interpolation nodes, rebuilds each fixed-depth ordinary
polynomial from the primitive finite profiles, and independently
reconstructs the Stirling/Newton triangles.  It proves
\[
\beta_{d,7}<0,\qquad
a_{d,6}^2>a_{d,5}a_{d,7},\qquad
0<a_{d,7}<(3d^2)^7
\quad(d\ge7),
\]
and the seventh full band
\[
\gamma_{d,6}>0\qquad(d\ge13).
\]
All 21 coefficients of its numerator after \(d=u+13\) are positive.

The same proof architecture now reaches
[`ORDINARY_RANK_EIGHT_AND_EIGHTH_BAND_THEOREM.md`](opg1757/top_newton_tail_2026-07-30/ORDINARY_RANK_EIGHT_AND_EIGHTH_BAND_THEOREM.md).
The author route uses depths \(8,\ldots,32\), while an independently
implemented primitive-profile route uses \(9,\ldots,33\); each keeps
four different exact holdouts.  Both reconstruct the same
degree-\(24\) symbol and prove
\[
\beta_{d,8}>0,\qquad
a_{d,7}^2>a_{d,6}a_{d,8},\qquad
0<a_{d,8}<(3d^2)^8
\quad(d\ge8).
\]
Their independently rebuilt triangles also give the eighth full band
\[
\gamma_{d,7}>0\qquad(d\ge15),
\]
with all 24 numerator coefficients positive after \(d=u+15\).

The all-rank leading theorem also has an effective consequence:
[`ALL_FIXED_BAND_POSITIVITY_DECIDABILITY_COROLLARY.md`](opg1757/top_newton_tail_2026-07-30/ALL_FIXED_BAND_POSITIVITY_DECIDABILITY_COROLLARY.md)
proves that, for every specified \(q\), positivity of
\(\gamma_{d,q}\) on all admissible integers \(d\ge2q+1\) is decidable
by a terminating exact rational computation.  The algorithm constructs
the band, applies an exact Cauchy root bound, checks the resulting
finite interval, and returns an exact counterexample when the answer is
negative.  It replays \(q=0,\ldots,7\) positively.  This is a
per-band decision theorem; it does not assert that all \(q\) return
positive.

### 2.3 Explicit ranks and windows

The campaign also retains:

- exact ordinary symbols through rank eight;
- strict normalized Newton inequalities through the first seven
  nontrivial ranks;
- exact positive long-recurrence bands \(\gamma_0,\ldots,\gamma_7\)
  on their full admissible domains;
- an explicit positive top window \(d\le k^{1/8}\); and
- an explicit bottom window
  \(r\le2^{-28}\sqrt{k}\) for the stated large-\(k\) range.

These results give substantial finite and growing-window support, but
the linear-width middle Newton region remains uncontrolled.

### 2.4 Boundary of the result

The campaign has not proved:

- the complete-split Rayleigh inequality over its whole coefficient
  range;
- compatibility of the long recurrence with real-rootedness at all
  depths; or
- OPG-1757 for arbitrary graphs.

## 3. Erdős #1083 milestones

### 3.1 Forced structure

The inherited critical branch forces
\(\mathfrak C_{\rm plane}\ge t^{13-o(1)}\).  The campaign's
[`HIGH_CODEGREE_MATCHING_OR_HUB_THEOREM.md`](erdos1083/geometric/HIGH_CODEGREE_MATCHING_OR_HUB_THEOREM.md)
converts this aggregate statement into the parameterized
matching-or-hub dichotomy above.  The proof is a dyadic label-mass
extraction followed by a weighted maximal-matching cover argument.

The same note gives a sharp abstract tensor:
quadratic polynomials over \(\mathbb F_q\) produce exact total,
diagonal, and aggregate exponents \(q^8,q^{12},q^{13}\), linear
matchings for almost every label, and no \(K_{3,2}\).

The independently audited
[`EUCLIDEAN_HUB_INCIDENCE_EXPANSION_THEOREM.md`](erdos1083/geometric/EUCLIDEAN_HUB_INCIDENCE_EXPANSION_THEOREM.md)
uses the actual distance equation after fixing the hub plane.  For
each nonperpendicular target plane, \((q,d)\) maps injectively to a
reverse circle in the source plane.  The planar point--circle
incidence bound then rules out the hub alternative for every fixed
\(\kappa<1/5\).  For \(0<\varepsilon<1/5\), apply the parameterized
dichotomy with \(\kappa=1/5-\varepsilon\); larger
\(\varepsilon\) give weaker conclusions and follow from any fixed
\(0<\kappa<1/5\).  Thus, for every fixed \(\varepsilon>0\), at least
\(t^{1-o(1)}\) labels support a matching of
\(t^{1/5-\varepsilon-o(1)}\) pairwise disjoint rich plane pairs; each
matched cell has \(t^{3-o(1)}\) representations.

If a hub survives with \(\kappa<1/3\), merging equal
incidence-active reverse circles and applying the weighted dyadic
incidence refinement gives the further exact alternative
\[
\mu\ge t^{(5-15\kappa)/2-o(1)}.
\]
Here empty and imaginary circles are discarded and zero-radius
circles are charged separately, so \(\mu\) records a real
circle-axis configuration rather than formal repetition.  Equality
of the repeated circle equations forces a common height and a common
cosine--radial parameter, providing a concrete Euclidean chart for
the next stage.

The independently audited
[`COSINE_RADIAL_REPEATED_CIRCLE_BARRIER.md`](erdos1083/geometric/COSINE_RADIAL_REPEATED_CIRCLE_BARRIER.md)
shows that this chart is exactly a circle with its perpendicular
axis.  Its sharp saturation model has a regular \(n\)-gon on the
circle and, for even \(\mu\), a symmetric arithmetic progression of
\(\mu\) axis points.  It realizes \(n\mu\) source--target
representations but at
most
\[
\lfloor n/2\rfloor+\frac32\mu-1
\]
distinct squared distances.  Therefore neither the present
rational-chord terminal nor the cyclotomic terminal can amplify one
repeated circle; a valid next lemma must synchronize many
arithmetically incompatible circle-axis charts.

The independently audited
[`TWO_CIRCLE_AXIS_CHART_BARRIER.md`](erdos1083/geometric/TWO_CIRCLE_AXIS_CHART_BARRIER.md)
extends the obstruction to any fixed number of concentric,
common-axis source circles with different radii.  The source-aware
bridge
[`MATHIALAGAN_SHEFFER_CIRCLE_CLASSIFICATION_BRIDGE.md`](erdos1083/geometric/MATHIALAGAN_SHEFFER_CIRCLE_CLASSIFICATION_BRIDGE.md)
then translates the known two-circle classification exactly into the
axial parameters.  For retained off-axis charts the perpendicular
exception is impossible; every nonaligned pair with incidence sizes
\(s_1,s_2\) therefore determines
\[
\Omega\!\left(
\min\{s_1^{2/3}s_2^{2/3},s_1^2,s_2^2\}
\right)
\]
distances.  This is a prior-work bridge, not a new distance theorem.
The new extraction target is now exact: force two nonaligned active
circles whose source-incidence sizes make this bound exceed the
critical \(t^{3+o(1)}\) budget.

The further
[`HIGH_RICH_CIRCLE_CONCENTRATION_COROLLARY.md`](erdos1083/geometric/HIGH_RICH_CIRCLE_CONCENTRATION_COROLLARY.md)
shows that the obvious way to meet this target does not occur:
circles above \(t^{9/4+\eta}\) richness are all concentric and carry
only \(t^{4+o(1)}\) weighted mass.  The next proof must therefore
aggregate the Mathialagan--Sheffer expansion over many moderately
rich nonaligned classes, or prove a stronger inverse theorem for the
remaining aligned concentration.

That first option has now been tested at the full exponent-ledger
level.  The exact feasible assignment
\[
(a,b,m)=\left(1-\kappa,\frac{7+11\kappa}{2},
\frac{5-15\kappa}{2}\right),
\qquad \frac15\le\kappa<\frac13,
\]
simultaneously saturates the hub mass, total triple capacity, weighted
point--circle term, and forced multiplicity threshold, while remaining
compatible with all current pairwise two-circle bounds and fixed-plane
capacity constraints.  See
[`MODERATE_RICH_AGGREGATION_BARRIER.md`](erdos1083/geometric/MODERATE_RICH_AGGREGATION_BARRIER.md).
This is an abstract ledger barrier rather than a Euclidean
construction.  It rules out a contradiction obtained merely by
recombining the saved aggregate inequalities and localizes the next
attack to reverse-circle algebra, cross-plane slot correlations, or a
special incidence saving for this family.

### 3.2 Structured terminal theorems

The campaign proves and audits:

- weighted ruled-column and rational-chord distance expansion;
- fixed and slowly growing number-field two-square terminals;
- complete prime-cyclotomic tensor escape;
- partial prime-cyclotomic fibre escape with arbitrary angular
  support at each height; and
- the same partial-fibre theorem over a fixed real number field for
  all but finitely many primes.

These theorems eliminate broad proposed extremizers.  They do not
show that an arbitrary critical Euclidean configuration contains one
of the required charts.

### 3.3 Boundary of the result

No \(\varepsilon>0\) has been proved in
\[
f_3(N)\ge N^{3/5+\varepsilon-o(1)}.
\]
The remaining target is now more specific: exploit the Euclidean
four-plane quadratic on the forced
\(t^{1/5-\varepsilon-o(1)}\) coefficient-separated matchings, or
force many mutually incompatible incidence-active circle-axis charts
inside a surviving hub.  The single-chart saturation model rules out
using multiplicity alone, while the finite-field tensor rules out
replacing the Euclidean step by another aggregate-energy argument.

## 4. Publication assessment

### OPG manuscript

There is now one strong manuscript nucleus, substantially broader
than any fixed-rank computation:

> all-rank ordinary-symbol rationality and cubic degree, exact
> falling-triangle factors, and all-rank positive leading
> long-recurrence coefficients, an effective fixed-band decision
> theorem, and explicit Newton applications.

This is a coherent conceptual paper if rewritten around the all-rank
mechanism, with computations presented as applications and
certificates.  A strong combinatorics/probability journal submission
is credible.  A Chinese Academy of Sciences Q1 placement is
plausible but not established: it depends on a complete priority
comparison, exposition, and peer review.  The paper must not be sold
as a proof of OPG-1757.

### Erdős manuscript

The Erdős material is presently a rigorous structural and
obstruction package, not a stand-alone exponent paper.  Without an
unconditional improvement beyond \(3/5\), it is unlikely by itself
to meet the stated Q1 target.  Its best current role is a major
section or companion preprint that makes the surviving Euclidean
inverse problem precise.

The search record and claim boundaries are in
[`LITERATURE_AND_NOVELTY_AUDIT.md`](LITERATURE_AND_NOVELTY_AUDIT.md)
and [`CLAIM_LEDGER.md`](CLAIM_LEDGER.md).  No direct match for the
all-rank forest-symbol/recurrence package was found in the targeted
search, but this negative result is not a priority proof.  The March
2026 Tang--Zhang preprint is the closest mandatory comparison.

## 5. Recommended next research sequence

1. Convert the OPG theorem chain into a single paper proof with one
   notation system and a source-to-lemma comparison against
   Tang--Zhang, Stark, Britikov, Dunster, and finite-difference
   Pólya--Schur theory.
2. Search for a compatibility theorem turning the positive long
   recurrence into interlacing or real-rootedness; this is the most
   direct route from the campaign recurrence result toward the missing
   Newton middle.
3. On Erdős #1083, attack the forced
   \(t^{1/5-\varepsilon-o(1)}\) rich matchings directly with the
   Euclidean four-plane quadratic.  In the surviving hub branch, seek
   a theorem producing two sufficiently incidence-rich nonaligned
   source circles, or otherwise incompatible circle-axis charts.  The
   known two-circle theorem then gives a
   \(\Omega(\min\{m^{2/3}n^{2/3},m^2,n^2\})\) bipartite distance
   bound.  One chart, and even any fixed number of concentric
   common-axis charts with different radii, is sharply saturated by
   the saved Lenz-type models.  Perpendicular circle pairs form the
   other general linear-distance exception, but the retained off-axis
   chart geometry rules them out.
   The moderate-rich ledger barrier proves that this extraction cannot
   follow from the current exponent inequalities alone; the next
   argument must exploit the special reverse-circle centre/radius
   equations, correlations of \((q,d)\) slots across target planes, or
   a genuine incidence saving for that restricted family.
   Every proposed lemma must still be tested against the finite-field
   tensor before it enters the proof tree.
4. Do not spend further time on aggregate Galois, energy, or
   rectangle extraction alone: the saved sharp models already show
   those ledgers are insufficient.

## 6. Final verification record

The final repository-level campaign checks were:

- OPG subtree: `125 passed in 818.32s`;
- Erdős subtree: `179 passed in 37.65s`;
- all 16 stored JSON files parsed successfully;
- 139 Markdown files were scanned, with all 22 explicit relative
  file links resolving;
- `git diff --check` reported no whitespace errors; and
- 13 test-generated `__pycache__` directories inside this campaign
  directory were removed after testing.

The rank-seven and rank-eight results each have two logically
separated exact certificates with different depth nodes and triangle
implementations.  The two-chart and high-rich results have independent
formula, coordinate, exponent, and multiplicity audits.  These checks
support the `PASS` labels in the claim ledger; they do not replace
external peer review or the unresolved priority audit.
