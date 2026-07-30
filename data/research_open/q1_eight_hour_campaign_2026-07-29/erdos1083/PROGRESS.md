# Erdos #1083: exponent campaign

## Exact target

For fixed `d >= 3`, let `f_d(n)` be the minimum number of nonzero Euclidean
distances determined by an `n`-point subset of `R^d`.  The original target is

```text
f_d(n) = n^(2/d-o(1)).
```

For `d=3`, the recognized inherited lower bound is
`f_3(n) >= n^(3/5-o(1))`.  A campaign success must either improve the `3/5`
exponent unconditionally and reconnect the argument to all branches, or prove
a natural structural theorem whose scope is independently publishable.

## Inherited high-Q interface

At the critical scale, the previous rounds produce approximately

```text
D = n^(3/5+o(1))
K = n^(4/5-o(1)) Q-rich reflection planes
Q = n^(3/5+o(1))
R = n^(1-o(1)) reflection-success points per plane.
```

The high-order branch further produces many triples
`g = s_c s_b s_a` with a common orientation-reversing isometry `g`.  Writing
`h_a = g s_a`, the surviving geometry splits into:

1. coplanar axes when `g` is a plane reflection;
2. parallel axes when `g` is a glide reflection;
3. concurrent axes when `g` has a unique fixed point.

The last two branches force `n^(9/20-o(1))` structured source planes; the first
forces a balanced `n^(1/5-o(1))` pencil/axis alternative.  Bare incidence
capacity remains `n^(3/5+o(1))`, so the missing lemma must use simultaneously

```text
q_a = |P intersect a| about Q,
|P intersect s_a(P)| at least R,
|P intersect (g s_a)(P)| at least R.
```

## First-stage pressure test

The following tempting shortcuts do not cross the exponent threshold.

- Counting only rich planes recovers the weighted Szemeredi--Trotter capacity
  `m <= n^2 ell / Q^3 = n^(3/5+o(1))`.
- Counting only rich rotations gives at best the inherited rich-rigid-motion
  bound `n^(9/5+o(1))`.
- For a fixed common axis, summing rotation correlations gives
  `|H_L| R <= O(nD)`, hence only `|H_L| <= n^(3/5+o(1))`.
- A first-moment count of triples
  `(z,x,y)` with `z in a`, `y = g s_a x` has lower bound `mQR`, but the sphere
  capacity upper bound is `O(n^2 D log n)` and remains too large.

Thus the next attack is a genuinely joint source-correlation estimate, not a
renaming of a standard incidence theorem.  Candidate weighted second moments
and extremal product configurations are being tested before any lemma is
promoted to a claim.

## Literature status

Primary references checked so far include Solymosi--Vu's higher-dimensional
bound, the Bardwell-Evans--Sheffer Lie-group reduction, Elekes--Sharir rich
rigid motions, Guth--Katz planar distances, and the incidence inputs already
listed in the round-12 source manifest.  No priority claim is made at this
stage.

## Fixed-axis circular interface audit

`CIRCLE_INTERFACE_NO_GO.md` now gives two complementary rigorous results.

1. An exact abstract-interface extremizer at the critical parameters
   `N=t^5`, `D_0=Q=t^3`, `M=t`, `R=N(1-2/t)` satisfies every previously used
   single-axis and single-fibre capacity, while its active joint moment is
   `(t-1-1/t)ND_0`.  Hence (4.37j) cannot be closed without cross-fibre
   distance information.
2. If the extremal angular progressions occur coherently on `F` equal-radius
   fibres with distinct heights, the convex-sumset bound gives
   `D >= c S sqrt(F)`.  At `S=t^2`, `F=t^3` this is `N^(7/10)`, excluding the
   coherent rectangular model by a fixed power.

The precise remaining gap is a robust extraction theorem: the aggregate
near-invariance and source-incidence hypotheses must produce many fibres with
a sufficiently common convex angular pattern.  Mere averaging does not yet
give that synchronization.

### Interface with the inherited proof tree

This audit applies specifically after Theorem 4.11 has entered its
plane-reflection/common-axis obstruction.  At that node the inherited
parameters are

```text
M >= n^(1/5-o(1)) active angles,
q_alpha >= Q = n^(3/5+o(1)),
r_alpha >= R = n^(1-o(1)),
D = n^(3/5+o(1)),
ell = |P intersect L| <= n^(2/5+o(1)).
```

Subtracting the harmless axis contribution, put

```text
q_alpha^o=q_alpha-ell,
r_alpha^o=r_alpha-ell.
```

The forced joint mass is then

```text
sum_active q_alpha^o r_alpha^o
    >= M (Q-ell)(R-ell)
    = n^(9/5-o(1)).
```

Theorem 1 rules out any attempted contradiction that uses only:

1. the formulas (4.37j) for `q_alpha` and `r_alpha`;
2. total angular mass `n`;
3. `|A_C|<=2D+1` or the number of within-fibre chord labels;
4. `sum q_alpha<=n+M ell`;
5. `sum r_alpha<=O(nD)`.

Those data admit the critical-scale abstract extremizer with joint mass
`n^(9/5-o(1))`.  In particular, separate Cauchy--Schwarz estimates for the
source and rotation sides, or any weighted interpolation of only those five
capacities, cannot close this proof-tree node.

This does **not** disprove a genuinely Euclidean estimate such as

```text
sum_active q_alpha^o r_alpha^o
    <= n D n^o(1).                              (target J)
```

If (target J) held, its right side would be `n^(8/5+o(1))`, contradicting the
forced `n^(9/5-o(1))` mass by a full `n^(1/5-o(1))` factor.  Proposition 2
explains why the local model cannot refute (target J): its simplest Euclidean
realization has `D=n-1`, and then the proposed right side is of quadratic
order.

Theorem 3 supplies a verified mechanism for global distance growth.  If an
extraction step produces `F` equal-radius fibres with distinct heights and a
common short-arc angular progression of length `S`, then

```text
D >= c S sqrt(F).
```

Thus the exact quantitative certificate needed from such an extraction is

```text
S sqrt(F) >= D n^epsilon                         (target E)
```

for some fixed `epsilon>0`.  A useful critical-scale benchmark is

```text
F >= Q n^-o(1)=n^(3/5-o(1)),
S >= n^(3/10+epsilon),
```

which gives (target E).  Neither common radius nor a common progression has
yet been derived from the aggregate correlations; they are the hypotheses of
the verified coherent subcase, not conclusions of the current proof.

Accordingly the next proof step has two honest alternatives:

1. prove the direct global joint estimate (target J), using cross-fibre
   Euclidean distances; or
2. prove a robust synchronization/inverse theorem that yields a certificate
   of type (target E), possibly after splitting into radius/height regimes.

Until one of these is established, the exponent `3/5` has not improved.

## Arbitrary-radius synchronized fibres

`COAXIAL_SYNCHRONIZATION_DICHOTOMY.md` removes the equal-radius assumption
from part of the coherent-subcase analysis.  If `F` arbitrary coaxial circles
share a short-arc angular progression of length `S`, and if `L` is the number
of distinct radii while `m` is the largest radius multiplicity, then

```text
D >= c S max(sqrt(L),sqrt(m)) >= c S F^(1/4).
```

The `sqrt(L)` term follows by taking logarithms of the within-circle chord
sets and applying the semiconvex sumset theorem to the distinct squared
radii.  The `sqrt(m)` term is the equal-radius height argument.  A common
angular slice also supplies `F` planar points, hence

```text
D >= c F/log(F).
```

At `S=N^(2/5)` and `F=N^(3/5)`, these become `N^(11/20)` and
`N^(3/5-o(1))`, respectively.  Therefore arbitrary-radius angular
synchronization alone, through these separate estimates, only recovers the
critical exponent.  The sharpened target is now radius concentration,
near-maximal radial diversity, or a genuinely joint expansion theorem for
the balanced regime `L about m about sqrt(F)`.

## Joint affine-copy audit

`AFFINE_COPY_REDUCTION_AND_BARRIER.md` gives two exact joint formulations.
Fixing the lowest reference circle produces `F` distinct affine copies

```text
a_i + b_i X_theta,
a_i=(rho_i-rho_0)^2+(z_i-z_0)^2,
b_i=rho_i rho_0>0.
```

Using all circle pairs produces `M` distinct parameter lines

```text
A_ij + B_ij X_theta,
A_ij=(rho_i-rho_j)^2+(z_i-z_j)^2,
B_ij=2 rho_i rho_j.
```

Ordinary Szemeredi--Trotter gives `D >= c min(M,sqrt(SM))`.  At the critical
scale it improves `N^(3/5)` only if `M > F^(4/3+epsilon)`; the attractive
target `M >= F^(3/2-o(1))` would yield `N^(13/20-o(1))`.  Only `M>=F` is
currently proved in full generality.  The equivalent open task is to bound
the energy of coincident `(A_ij,B_ij)` parameters, or show that high energy
forces another distance expansion.

One nontrivial branch is now isolated by the radius energy.  If `E_x(R)`
counts pairs of radius pairs with equal product and `m` is the largest radius
multiplicity, then the exact height-equation count gives

```text
parameter_energy <= 2 m^3 E_x(R),
M >= c F^4/(m^3 E_x(R)).
```

For balanced `L about m about sqrt(F)`, this beats `F^(4/3)` whenever
`E_x(R) <= L^(7/3-delta)` and gives `F^(3/2)` for multiplicatively Sidon
radii.  The remaining all-pairs obstruction is therefore confined to the
high multiplicative-energy radius regime; converting that structure into
extra intercept or distance expansion is open.

An exact high-energy benchmark shows what that conversion should exploit:
geometric radii `rho_u=m 2^u` have radius-product energy of order `L^3`, but
their radial-offset blocks are disjoint from the common height-difference
blocks and still give `M=m binom(L+1,2)`.  Thus high product energy is not a
counterexample; the missing lemma must couple product repetition to radial
offset and height-difference overlap.

`GEOMETRIC_RADIUS_HIGH_ENERGY.md` now proves a nontrivial structured subcase
with arbitrary, unequal height sets.  For radii `rho_u=T q^u`, integer
`q>=2`, if every height lies in one interval of length `H<T`, then radial
offset blocks belonging to the same radius product are disjoint and

```text
M >= (L+1)F/4.
```

Thus balanced `L about sqrt(F)` gives `M >> F^(3/2)` and, conditionally on
this thin-slab extraction, the all-pairs route gives
`D >> N^(13/20-o(1))`.  The unrestricted-height case remains open.

A second high-energy theorem removes the slab condition when every radius
carries the same arbitrary height set.  For a fixed radius product, the
geometric-progression radial offsets form a Sidon set: their consecutive
gaps are superincreasing.  An additive-energy calculation then gives

```text
M >= sum_p t_p^2 m/(t_p+m),
```

where `t_p` is the number of radius pairs with product exponent `p`.  In the
balanced case `m about L`, this is `M >> L^3 about F^(3/2)`, again yielding
the conditional `13/20` exponent.  The remaining open case now requires
height sets that vary independently across radii and are not confined to a
common thin slab.

The identical-height proof extends verbatim to any radius set whose
fixed-product radial-offset sets have distinct positive differences.  This
`Sidon-offset criterion` is the current plausible bridge from exact geometric
progressions to broader low-multiplicative-doubling radius sets.

## Independent wide height sets: second-order stability

`HIGH_ENERGY_OVERLAP_STABILITY.md` treats the only remaining geometric-radius
case at an elementary energy level.  With blocks

```text
S_e = C_e + (Z_u-Z_v)^2
```

and total block mass `I`, let `Kcorr` be the ordered sum of intersections of
blocks having the same radius product.  The exact second-moment identity and
Cauchy--Schwarz give

```text
M >= I^2/(I+Kcorr),
I >= (L+1)F/4.
```

Hence `M <= I/K` forces `Kcorr >= (K-1)I`: any asymptotic failure of
`M about FL` requires quantitatively diverging shifted correlations between
the squared height-difference sets.  If every pair correlation is
`F^o(1)`, the balanced branch already has `M >= F^(3/2-o(1))`.

For integer radii and heights, a block intersection solves
`a^2-b^2=delta`, so it is at most the divisor count `tau(|delta|)`.  This
closes lattice instances where the relevant divisor maximum is `F^o(1)`,
but coordinate size must be controlled; the generic `tau(n)=n^o(1)` statement
alone is not enough for exponentially large coordinates.

The missing inverse step is now explicit rather than heuristic: convert large
total shifted square-difference correlation into common translations or
reflections of several height sets, or into an independent distance
expansion.  No BSG-type conclusion is currently claimed.

A one-pair no-go prevents overclaiming this inverse step: the height sets
`{cosh(t_j)}` and `{sinh(t_j)}` against a singleton anchor have arbitrarily
many squared differences shifted by exactly one, but are not translates or
reflected translates.  Any successful inverse theorem must therefore use the
network of correlations across many radius pairs, not one popular block pair.

## Network inverse audit

`NETWORK_INVERSE_AUDIT.md` proves a dyadic graph-extraction lemma: from
weighted block correlation `W`, one obtains a threshold graph with
`r |E_r| >= W/O(log m)`, a high-minimum-degree core, and a 4-cycle once the
minimum degree exceeds `sqrt(t)+1`.

This graph information still does not close the branch.  An exact Hadamard
block design has `t=2^r-1` blocks of size `k=2^(r-1)`, every pair intersects
in `k/2`, the correlation graph is complete with all possible 4-cycles, but
the total union has only `2k` elements and every pair of blocks differs on
`k` elements.  After compensating arbitrary radial offsets, the sets remain
nonnegative.  Embedding the design universe as powers of three makes its
ordinary additive energy minimal of order `U^2`, so BSG on the ambient union
also has no useful input.  These blocks are not asserted to be
squared-difference sets.

Therefore graph extraction or BSG applied only to abstract shifted blocks is
insufficient.  The minimum viable inverse lemma must use the labelled
realizability `Y_uv=(Z_u-Z_v)^2` across many products.  A quantitative
conditional target is recorded: either independent expansion already gives
`L^3/F^o(1)` lines, or `L/F^o(1)` height sets share one common
`m/F^o(1)`-sized core.  Individual vertex-dependent translations or
reflections are not enough without an additional cocycle-consistency step.
The common-core target would reconnect to the Sidon-offset theorem, but it
remains unproved.

## Squared-difference realizability audit

`SQUARED_DIFFERENCE_REALIZABILITY.md` shows that realizability does not fix a
single product fibre.  Such a fibre is a matching on radius indices, so
arbitrary nonnegative blocks are exactly realizable if one endpoint per pair
is a singleton.  More strongly, every positive two-value set is
`(A-B)^2` for two two-point sets.  This gives an exact `q=2`, product
exponent `p=5` realization of the three-block Hadamard gadget with two
heights at every one of the six radii: pair intersections are one and the
union has only four values.

The first genuine constraint occurs across different product fibres.  For
three original radius vertices and height sets `A,B,C`, every represented
value triple

```text
a=(x-y)^2, b=(y-z)^2, c=(x-z)^2
```

lies on `(c-a-b)^2=4ab`.  If all three height sets have size `m`, at least
`m^2/4` distinct value triples in
`(A-B)^2 x (B-C)^2 x (A-C)^2` lie on this surface.  This follows from
representation multiplicity at most `2m`, not from a set-level coincidence.

Thus within-product triangles and 4-cycles in the abstract correlation graph
carry no height consistency; a successful inverse theorem must combine
correlations from different products with the degenerate-triangle surface
and coherent square-root signs around original-radius cycles.

## Triangle and K4 compatibility audit

`TRIANGLE_K4_COMPATIBILITY.md` shows that the triangle surface is itself
group-like:

```text
a=x^2, b=y^2, c=(x+y)^2.
```

Sets of sizes `n,n,2n-1` support exactly `n^2` such parameterized triples, so
no generic Elekes--Szabo-style incidence saving is available.

Four radius vertices do impose one genuinely new sign-cocycle identity.  With
`g_ij=(a_0i+a_0j-a_ij)/2`, actual line heights satisfy

```text
g_12 g_13 g_23 = a_01 a_02 a_03.
```

The four-cycle metric with opposite distances two and adjacent distances one
satisfies every triangle surface equation but violates this K4 identity.
Thus triangle magnitudes alone do not ensure globally coherent square-root
signs.

However, K4 compatibility is also group-like, parameterized by three signed
anchor differences.  Four `m`-point height sets determine between
`m^3/8` and `O(m^3)` compatible six-tuples in the common-progression model.
The exact triangle/K4 exponent ledger is therefore saturated: compatibility
alone gives no fixed-power gain.  The remaining lemma must combine the K4
sign cocycle with the independently established high shifted-correlation
mass; neither input alone is sufficient.

## Joint correlation--K4 threshold audit

`CORRELATION_K4_JOINT_AUDIT.md` combines the two inputs quantitatively after
truncating every balanced squared-difference block to size `k about m`.  If

```text
M <= L^(8/3+eta),
```

then dyadic extraction gives the rigorous dichotomy

```text
either r >= L^(5/6-eta-o(1)),
or the active graph on original radius indices contains a 4-cycle.
```

For the desired `F^(4/3+epsilon)` line bound, `eta=2 epsilon`.  The proof uses
forced correlation exponent `10/3-eta`, at most `L` same-product partners per
block, and the elementary `O(L^(3/2))` edge bound for a `C4`-free graph.

An active radius cycle still need not lift to a coherent quadruple of height
points.  A four-partite parity construction gives density `1/2` on each
representation graph but zero transversal cycles.  The coarse uncoloured
route would already require average representation multiplicity
`L^(2/3+eta+o(1))`, versus the automatic lower bound one, and even that would
not ensure four distinct radius parts.

Thus the exact missing input is a cycle-consistent representation-density
statement linking shifted-correlation labels to square-root signs.  A
labelled parity barrier satisfies all current marginal edge and compatibility
capacities while frustrating every candidate point cycle; it is not asserted
to arise from actual height sets.

## Realizable cycle-lifting barrier

`CYCLE_LIFTING_PARITY_BARRIER.md` upgrades the abstract parity warning to
actual real height sets and genuine squared differences.  Take four copies of
`{0,...,m-1}`.  On three consecutive cycle edges select even squared
differences and on the fourth select odd squared differences.  Every
representation graph has exactly `m^2/2` edges and average multiplicity `m`
per selected value, but there is no transversal point cycle.

The four selected value sets can simultaneously be embedded into genuine
same-product shifted correlations.  With cycle radius indices
`(0,7,1,16)` and disjoint external pairs
`(3,4),(2,6),(8,9),(5,11)`, the sums match edge by edge and every external
radial offset is smaller.  Singleton-anchor realization followed by padding
to `m` heights makes each shifted overlap have size `m/2`.

Thus even linear-sized block overlap, maximum-order representation
multiplicity, an active original-radius `C4`, and the K4 Gram identity do not
force a lift: the Gram cocycle can only test a point quadruple after one
exists.  The remaining possible theorem must impose cross-edge sign
coherence directly or derive it from a genuinely global property not present
in the current correlation energy.  This is a local lifting barrier, not a
global small-line construction.

There is a conditional network-level repair for exact parity models.  If
every active representation graph is given by one common two-class parity
rule with an edge label, any active `K_(2,3)` contains a zero-label-sum
4-cycle and hence a transversal point cycle.  With parity classes of size
at least `alpha m`, it gives at least `2(alpha m)^4` point cycles.
Since `K_(2,3)`-free graphs have `O(L^(3/2))` edges, a fixed-power excess
over the active-edge threshold closes this exact parity subcase.  General
squared-difference representation graphs need not have a common two-class
description, so the unconditional lifting problem remains open.

## Signed-difference and finite-quotient audit

`SIGNED_DIFFERENCE_FINITE_QUOTIENT_AUDIT.md` rewrites a point-level lift as
the signed equation

```text
d_01+d_12+d_23+d_30=0.
```

Parity is not exceptional.  For `m` divisible by seven, take four copies of
`{0,...,m-1}` and allow differences congruent to `+-1 mod 7` on three cycle
edges and `+-2 mod 7` on the fourth.  Each selected squared-value set has
exactly `2m/7` elements, its representation graph has exactly `2m^2/7`
edges, and its average multiplicity is exactly `m`; nevertheless the signed
sum is one of `+-1,+-3,+-5 mod 7`, so there is no transversal point cycle.
The same disjoint external radius pairs as in the parity construction realize
all four selections as genuine shifted correlations of size `2m/7`.

The balanced exponent ledger is therefore

```text
r=Theta(L), representation mass=Theta(L^2), lambda=Theta(L),
transversal cycles=0.
```

This rigorously blocks a local inverse lemma even above the strong-pair
threshold.  A Fourier calculation does give a weaker positive statement:
if four subsets of a finite abelian group, each of density at least `delta`,
have a fixed proportional deficit of zero-sum quadruples, then some set has
a nontrivial normalized Fourier coefficient of size
`Omega(delta^(3/2))`.  In a fixed group of order `q`, one common character
has a fourfold Fourier product bounded below by a constant depending on
`delta,q`.  Arithmetic removal only deletes a small exceptional set; it does
not turn this into a bounded-order common character model.

A coherent fixed quotient *is* globally repairable.  If every active edge
uses one of the `(q-1)/2` symmetric nonzero colours in a common
`Z/qZ` coordinate, an active `K_(2,((q-1)/2)^2+1)` forces a lift by repeated
ordered colour pairs.  For the exact mod-seven model, exhaustive
classification sharpens this to `K_(2,3)`.  Thus a fixed-power active-edge
excess over `L^(3/2)` excludes fixed coherent quotient barriers in the
diffuse branch.  The unique missing synchronization input is to extract the
same bounded quotient and compatible vertex coordinates on a dense active
subgraph; the current correlation energy and arithmetic removal do not do
this, and the strong-pair branch has no dense network on which to apply it.

## Edge-character synchronization audit

`EDGE_CHARACTER_SYNCHRONIZATION_AUDIT.md` proves a quantitative abstract
agreement lemma.  Label every edge of `K_N` by a character colour and an
oriented phase in a finite abelian group.  If at least a `1-epsilon`
fraction of the `K4`s are monochromatic and satisfy all four triangular
phase-zero equations, then one character `c_*` and vertex potentials `p_v`
agree with all but

```text
(4 epsilon + O(1/N)) binom(N,2)
```

edges.  The proof first samples disjoint edge pairs to concentrate the
character colour, then chooses a root with few failed triangle tests and
sets `p_v=ell_(v,r)`.  Thus an actual dense complex of nonvacuous labelled
`K4` tests would solve the synchronization step.

The squared-difference Gram identity does not provide those tests.  It
contains neither edge-character equality nor triangular phase equations,
and it is evaluable only after six squared values already arise from one
height quadruple.  A new explicit geometric certificate makes this mismatch
strict.  The original radius indices `(0,4,8,19)` have six mutually disjoint
same-sum external pairs.  Assign the six original edges the finite quotients

```text
7, 14, 21, 28, 5, 9
```

with the four cycle colours reducing modulo seven to
`+-1,+-1,+-1,+-2`.  For `m` divisible by `1260`, every edge has exactly
`2m/q_e` selected squared values, `2m^2/q_e` representations, and average
multiplicity `m`; all six selected sets are simultaneously realized as
genuine shifted correlations by the external pairs.  The moduli have gcd
one, yet the displayed cycle has no transversal point cycle.  The Gram
identity remains universally true for actual quadruples but supplies no
constraint on the selected edge labels.

The balanced ledger remains `r=Theta(L)`, representation mass
`Theta(L^2)`, and `lambda=Theta(L)` on every edge, with zero nonvacuous
selected `K4` tests.  Therefore the precise missing input is stronger than
edge-label synchronization: the geometry must first produce a dense test
complex comparing labels across edges.  Without that, the abstract
agreement lemma cannot be invoked.

## Strong-pair BSG audit

`STRONG_PAIR_BSG_AUDIT.md` stops the local-cycle route and audits the other
side of the correlation dichotomy,

```text
r >= L^(5/6-eta-o(1)).
```

A common shifted value from two distinct same-product blocks gives

```text
((a-b)-(c-d)) ((a-b)+(c-d)) = Delta,
```

where `Delta` is nonzero.  This is a fixed-product hyperbola between two
four-variable linear forms, not additive difference energy.  Dyadically
pigeonholing the two representation multiplicities yields a class of at
least `r/log^2(m)` common values with multiplicities
`lambda_1,lambda_2`, but the current hypotheses allow both lambdas to equal
one.

Even replacing the hyperbola by the fictitious zero-shift equation gives an
exact capacity barrier.  The cross energy is at most `4m^2 r`, so at
`m about L` the BSG parameter necessarily satisfies

```text
K >= L^(1/6+eta-o(1)).
```

For the target `F^(4/3+epsilon)`, `eta=2epsilon`.  Achieving
subpolynomial BSG loss would require
`lambda_1 lambda_2 >= m^(13/6+eta-o(1))`, exceeding the universal
`4m^2` representation capacity by exactly `m^(1/6+eta-o(1))`.
Intervals saturate this maximum-energy ledger in the zero-shift model.

The actual nonzero-shift situation can attain only one selected
representation on each side.  An explicit rational hyperbola

```text
x=(s+Delta/s)/2, y=(Delta/s-s)/2, x^2-y^2=Delta
```

followed by forbidden-difference-avoiding padding gives `m`-point real
height sets with `r` shifted coincidences and exact selected multiplicity
one.  The verifier uses the genuine radial-offset difference
`16129-64=16065`.  Thus dyadic decomposition cannot manufacture BSG energy.

Finally, perfect structure on the four height sets in one strong block pair
has only `O(m^2)=O(L^2)` internal parameter capacity, whereas the global
target is `L^(8/3+eta)`.  A further propagation factor
`L^(2/3+eta)` is missing.  Standard BSG/Plunnecke therefore cannot close the
strong-pair branch: a replacement must exploit the nonzero hyperbola and
propagate across many radius pairs, or the dichotomy must force a network of
strong pairs rather than one isolated pair.

## Global hyperbola-network audit

`GLOBAL_HYPERBOLA_NETWORK_AUDIT.md` treats all block correlations
simultaneously.  With `Theta(L^2)` truncated blocks of size `Theta(L)`,
total incidence is `I=Theta(L^3)`.  If

```text
M <= L^(8/3+eta),
```

then the unordered overlap mass is at least
`L^(10/3-eta-o(1))`.  A weighted double count proves the strongest general
reuse statement available from this mass: if a strong-edge graph has total
overlap `W_G`, some one parameter value is common to at least

```text
1 + 2 W_G/I
```

blocks in one product fibre.  At the forced correlation scale this is
`L^(1/3-eta-o(1))` blocks.

This falls short of the `L^(2/3+eta)` propagation factor needed to lift one
local four-height-set conclusion to the global line target, by exactly
`L^(1/3+2eta)`.  The shortfall is sharp for abstract blocks.  An affine-line
tensor over `F_q^d`, with `eta=1/3-1/d`, gives block size `L`, strong overlap
`L^(5/6-eta)`, strong degree `L^(1/2)`, union
`L^(8/3+eta)`, correlation `L^(10/3-eta)`, and maximum common-value
multiplicity only `L^(1/3-eta)`.  Thus the Cauchy, dyadic-network and reuse
bounds all saturate simultaneously.

Inside a single product fibre this tensor is genuinely realizable by
squared-difference blocks: the radius pairs form a matching, so singleton
anchors realize every prescribed truncated block independently.  Repeating
the tensor independently across all fibres is not known to be geometric,
because the same original height set `Z_u` must be reused in one block in
each of `Theta(L)` fibres.  The tensor instead assigns independent data to
each occurrence.

This identifies the sole remaining compatibility input: a theorem exploiting
the repeated appearance of each `Z_u` across different product fibres.
Generic Elekes--Szabo does not apply to the separable four-variable surface
`t=C+(a-b)^2`; point-line incidence sees only parallel additive incidences;
sum-product has no common factor set because the factors vary edgewise.
Any further global gain must first convert shared endpoints across fibres
into one common additive or multiplicative coordinate system.  No exponent
improvement is claimed.

## Cross-fibre shared-endpoint audit

`CROSS_FIBRE_ENDPOINT_REUSE_AUDIT.md` writes the repeated use of every
height set `Z_u` as a triangle tensor across three different product fibres.
For every radius triangle and every point triple, the squared values obey

```text
(a+b-c)^2 = 4ab.
```

A fixed value triple has at most `4m` point preimages, so every radius
triangle has at least `m^2/4` distinct compatible triples and the complete
system has `Omega(L^5)` scoped tests.  This is the minimal polynomial
obstruction preventing a generic independent-fibre affine tensor from being
globally realized by one shared family `(Z_u)`.

There is a quantitative simultaneous-retention lemma.  First,
`M >= I_full/L`; hence under `M<=L^(8/3+eta)`, the total full block mass is
at most `L^(11/3+eta)`.  Apart from `L^(2-delta)` exceptional blocks, all
block sizes are at most `L^(5/3+eta+delta)`.  Independent uniform
`Theta(L)`-value truncations then retain in expectation

```text
L^(3-3eta-3delta)
```

cross-fibre compatible triples.  Every truncation still has total incidence
`Theta(L^3)` and union at most `M`, so it deterministically retains the
forced within-fibre correlation `L^(10/3-eta-o(1))`.  Thus one truncation
simultaneously carries both marginals.

This still does not supply the missing propagation.  The compatible-test
count divided by the `Theta(L^3)` selected incidences is only
`L^(-3eta-o(1))`, and there is no lower bound forcing the highly reused
within-fibre values to be the values participating in compatible triangles.
A direct-sum tensor can place the two marginals on disjoint halves.
Moreover, with all shared height sets equal to `{0,...,m-1}`, selecting
differences `+-1 mod 7` on every edge gives `2m/7` values and `2m^2/7`
representations per edge but zero selected compatible value triples.  Hence shared
endpoints plus marginal density do not align the tensors.

The sole remaining input is now a joint overlap--triangle moment: the same
block--value incidences must simultaneously have high within-fibre reuse and
participate in the cross-fibre polynomial equation.  Any statement that this
moment supplies the missing `L^(1/3+2eta)` remains conditional and unproved.
No exponent improvement is claimed.

## Joint overlap--triangle moment

`JOINT_OVERLAP_TRIANGLE_MOMENT.md` finally puts the two tensors on the same
incidence.  For selected `a` in block `e`, let `d(e,a)` be its number of
same-product-fibre shifted reuses and let `tau(e,a)` count compatible
selected value pairs on radius triangles containing `e`.  Define

```text
J = sum_(e,a) d(e,a) tau(e,a).
```

Random truncation plus shared endpoints gives a new unconditional bound.
Condition on one reused shifted value in blocks `e=uv` and `f`.  Fix a point
representation of its value in `e`.  For each of `Theta(L)` third radius
classes `w`, its `m` heights generate at least `m/2` distinct compatible
pairs in blocks `uw,vw`.  Since each full block has at most `m^2` values and
the truncation retains `Theta(m)`, the conditional expected surviving
triangle degree is `Omega(1)`.  Therefore one common truncation satisfies

```text
D = sum d >= L^(10/3-eta-o(1)),
J >= L^(10/3-eta-o(1)).
```

A double dyadic extraction yields a class `X` with
`|X| lambda mu >= J/log^2 L`, where `d about lambda` and
`tau about mu`; in particular some incidence has
`d*tau >= L^(1/3-eta-o(1))`.

This is still below the useful benchmark.  To supply the propagation factor,
the overlap-weighted mean `J/D` must be at least
`L^(1/3+2eta-o(1))`, equivalently

```text
J_target >= L^(11/3+eta-o(1)).
```

The proved mean is only constant, leaving exactly the same
`L^(1/3+2eta)` gap.  Marginal Hölder/Cauchy cannot improve it because the
minimum supports of `d` and `tau` fit disjointly inside the `L^3`
incidences.

Keeping exact full-block sizes gives a reciprocal link weight, but overlap
may concentrate on a realizable high-complexity hub.  Take
`|U|=L^(2/3+eta)`, generic height sets on `U`, and one common arithmetic
progression outside.  Blocks incident to `U` have `Theta(m^2)` values,
outside blocks `Theta(m)`, and total full incidence is exactly
`L^(11/3+eta)`.  The `L^(4/3+2eta)` hub pairs can contain the required
`L^(4/3-eta)` maximally reused block support while their guaranteed random
triangle survival remains constant.  This is a genuine block-size
landscape, but not a globally small-`M`, high-overlap construction.

The mod-seven selection still makes `J=0`, but is not known to meet the
forced geometric overlap mass.  No global saturation construction satisfying
shared endpoints, geometric offsets, small `M`, and low `J` was found.  The
remaining conditional statement is precisely that strong overlap cannot
concentrate on the high-complexity hub without either increasing `M` or
raising `J/D` by `L^(1/3+2eta)`.  No exponent improvement is claimed.

## Hub concentration partial dichotomy

`HUB_CONCENTRATION_DICHOTOMY.md` attacks that last concentration directly.
Keeping exact full-block sizes gives the conditional random triangle-link
weight

```text
R_uv about m k^2 sum_w 1/(|Y_uw| |Y_vw|).
```

At the target `G=L^(1/3+2eta)`, set the large-block threshold
`S=L^(11/6-eta-o(1))`.  If `R_uv<G`, then one endpoint of `uv` must be
incident to a linear number of `S`-large blocks; otherwise linearly many
third vertices have both adjacent blocks below `S` and already contribute
`L^4/S^2=G` to `R_uv`.  Thus all low-link blocks are covered by a hub set
`U`.

If a positive fraction of overlap has a high-link orientation, the joint
moment reaches the benchmark

```text
J >= G D = L^(11/3+eta-o(1)).
```

Otherwise a positive fraction is between two low-link blocks.  Product
fibres are matchings, so each contains at most `|U|` low blocks; across all
fibres there are at most `O(|U|L)`.  Their total ordered overlap capacity is
`O(|U|^2 L^2)`.  Comparing with
`D=L^(10/3-eta-o(1))` forces

```text
|U| >= L^(2/3-eta/2-o(1)).
```

Every hub has linearly many `S`-large incident blocks, so
`M>=I_full/L>=|U|S`, giving the proved second alternative

```text
M >= L^(5/2-3eta/2-o(1)).
```

This is a rigorous partial dichotomy, not the desired exponent.  It misses
`L^(8/3+eta)` by exactly `L^(1/6+5eta/2)`.  Reaching the target with this
threshold would require `|U|>=L^(5/6+2eta)`, while overlap capacity only
forces `L^(2/3-eta/2)`.

No complete geometric saturation example with small `M` was found.  The
remaining conditional statement is now exact: realizing near-maximal
`|U|^2L^2` overlap capacity with the same hub height sets across all product
fibres must either add the missing `L^(1/6+5eta/2)` line expansion or raise
the overlap-weighted triangle link to the target.  Local C4, single-pair BSG
and marginal endpoint estimates do not address this multi-fibre saturation.
No exponent breakthrough is claimed.

## Hub cross-fibre energy audit

`HUB_CROSS_FIBRE_ENERGY.md` organizes low--low overlap by hub pairs:

```text
E_(u,x) = sum_v |
  (C_(u,v)+A_(u,v)) intersect
  (C_(x,v+u-x)+A_(x,v+u-x)) |.
```

A collective bound `sum E_(u,x) <= U^(2-c)L^(2+o(1))` closes the hub branch
only if

```text
c >= (2+30eta)/(5+12eta).
```

At `eta=0` this already requires `c>=2/5`; a logarithmic or arbitrarily
small power saving is insufficient.

No pairwise saving is possible over the reals.  For one fixed hub pair
`u,x`, rational hyperbola parameters

```text
alpha=(s+Delta/s)/2,
beta =(Delta/s-s)/2
```

are allocated along `Theta(L)` neighbour fibres.  Each nonhub height set
receives at most two half-size channels, and
`alpha^2-beta^2=C_(x,y)-C_(u,v)` gives `Theta(m)` exact common shifted values
per fibre.  Thus `E_(u,x)=Theta(Lm)=Theta(L^2)` with the actual geometric
offsets and globally shared height sets.  Pairwise incidence, BSG or spectral
estimates cannot supply a positive `c`.

Independent channel allocation over many hub pairs gives only `O(UL^2)`
total energy because every nonhub set has `m`-point capacity.  Reaching the
abstract `U^2L^2` capacity requires the same height coordinates to serve many
hub-pair systems.  Bounding this simultaneous coordinate congestion is the
remaining possible collective saving.

The collective saving is false over odd finite fields.  With geometric
radii generated by a primitive element and every shared height set equal to
the full field, squared-difference blocks are the quadratic residues,
distinct translates intersect in `Q/4+O(1)`, and each product-fibre union
has at most `Q` values.  For `Q about L`, this gives `M=O(L^2)` and
`D=Theta(L^4)`, respecting product-fibre matchings and the radial-offset
formula.  The model has abundant triangle links and does not embed in the
ordered reals.  It rules out field-uniform polynomial incidence, rank or
positivity proofs; a successful theorem must exploit real order and
collective shared-coordinate nonperiodicity.

No collective real saving and no complete real small-`M` saturation were
obtained.  The remaining conditional alternative is that multi-hub
coordinate reuse either yields the required `U^(-c)` saving or forces the
joint moment above its target.  No exponent improvement is claimed.

## Real multi-hub coordinate reuse audit

`REAL_MULTI_HUB_REUSE.md` writes the condition that one nonhub coordinate
`z in Z_v` serves hub pair `u,x` as

```text
(a-c-z+d)(a+c-z-d) = C_(x,y)-C_(u,v),
y=u+v-x.
```

The direct pointwise reuse target is false.  Take hub indices
`0,...,U-1`, source radius `v=2U`, put zero in every hub height set, and
choose one sufficiently large real `z`.  For every hub pair `u<x`, put

```text
d_(u,x)^2 = z^2 + C_(u,v) - C_(x,v-(x-u))
```

in the receiving set with radius `v-(x-u)`.  Product sums and shifted values
match exactly.  Pairs with the same hub difference use the same receiving
set, which needs only `U-h<=U<=m` coordinates.  Thus one real coordinate
serves all `binom(U,2)=Theta(U^2)` hub pairs with the genuine geometric
offsets.  Any pointwise `r(z)<=U^(2-c)` bound with `c>0` is impossible.

A second-moment bound could still be collective: to imply the desired
capacity it would need

```text
sum_(v,z) r(v,z)^2 <= U^(4-2c)L^(2+o(1)).
```

The star shows such an estimate cannot be proved pointwise; it must charge
the `Theta(U^2)` partner coordinates consumed across the receiving sets and
prevent dense iteration in which those partners themselves serve many
stars.

Pseudoline/VC arguments do not presently do this.  For fixed hub indices and
hub heights the service equation is a translated rectangular hyperbola with
bounded pair intersections, but the full family has independent parameters
`u,x,a,c`.  Freezing enough parameters makes Pach--Sharir count point
representations on a scale much larger than the selected distinct values.
With zero hub anchors, squaring turns the curves into parallel lines
`d^2-z^2=Delta`; strict convexity of the geometric intercept sequence gives
no transverse incidence bound.  Subtracting two service equations either
determines `z` from many arbitrary partner variables or transfers the
constraint to those partners.

The best unconditional collective exponent from these methods remains
`c=0`.  The remaining real-order problem is an iterated partner-coordinate
second moment: many quadratic-service stars must not form a dense reuse
network without expanding `M` or the joint triangle moment.  No complete
real saturation and no exponent improvement were obtained.

## Iterated partner-coordinate network

`ITERATED_PARTNER_REUSE_NETWORK.md` solves the iteration problem for the
anchor-coherent subnetwork, where both hub witnesses use one common real
height `A`.  After translating `A` to zero, attach to a nonhub coordinate
`(v,z)` the state

```text
n(v,z) = (v,(z-A)^2+rho_v^2)
```

and to hub index `u` the state `h_u=(u,rho_u^2)`.  Product matching and
equality of shifted squared distances are then exactly

```text
n(v,z)+h_u = n(y,d)+h_x.
```

Thus the reuse network is the induced Cayley graph for
`D=(H-H)\\{0}`, where `H={(u,q^(2u))}`.  For integer `q>=2`, `H` is a
`B_4` set.  Its difference translates have the exact codegree dichotomy

```text
|D intersect (D+t)| = 2U-4  if t is in D,
|D intersect (D+t)| <= 4    otherwise.
```

Counting two-paths by their middle vertex and endpoint pair gives, for any
`n` coordinate states,

```text
sum d(v)^2 << U sum d(v) + n^2,
sum d(v)   << nU + n^(3/2).
```

With `n<=Lm` and `m about L`, the total anchor-coherent service count is
`O(L^2 U+L^3)`.  At `U=L^alpha`, `alpha>=5/6+2eta`, this supplies every
`c<=2-1/alpha`.  In particular it permits `c=4/5` at `eta=0`, exceeding
the required `2/5`; throughout `eta<1/3` its exponent margin remains
positive.

This global estimate coexists with the pointwise `U^2` star.  It proves that
the star cannot be densely iterated inside one common-anchor network.
Short-cycle exclusion is not the mechanism: for any product index `P` and
large energy `W`, coordinates with

```text
(z_u-A)^2 = W-rho_u^2-rho_(P-u)^2
```

form a complete `U`-node service clique.  Parallel choices of `W` fill every
receiving height set and realize exact real 4-, 6- and 8-cycles.  The saving
comes from the two-level intersection law for whole star neighbourhoods,
not from the absence of a minimum cycle.

The unrestricted four-height network remains open.  Its exact pair-state is

```text
(u+v, rho_u^2+rho_v^2+(a-z)^2),
```

and the bilinear term `-2az` prevents separation into a hub state plus a
coordinate state when hub anchors vary.  Splitting by the two anchors costs
up to `m^2`, so the coherent theorem cannot simply be summed.  The precise
remaining input is now an anchor-coherence extraction or a full hypergraph
codegree inequality whose mixing error is charged to the joint triangle
moment.  Therefore this round gives a rigorous positive exponent only for
the coherent submodel, not an unconditional improvement of `3/5`.

## Anchor-coherence extraction barrier

`ANCHOR_COHERENCE_EXTRACTION_AUDIT.md` computes the exact mass needed to use
the coherent-network theorem.  Its upper bound is `O(L^3)`, while the
low--low service mass is `S=L^(10/3-eta-o(1))`, so an extraction needs

```text
theta >= L^(-1/3+eta-o(1)).
```

At the minimal hub size `U=L^(2/3-eta/2)`, one hub-coordinate supports on
average `L^(5/3-eta/2)` services, while one ordered pair of hub coordinates
supports only one.  Selecting one anchor per hub retains `S/L^2`.  Selecting
`r` anchors per hub can cross `L^3` only when

```text
r >= L^(5/6+eta/2).
```

Equivalently, a bucket decomposition may use at most
`L^(1/6-eta/2)` buckets, leaving a polynomial-size bucket.  The exact
bilinear term `-2az` survives inside such a bucket; cardinality bounds give
no numerical separation with which to round approximate collisions.

A strict Latin-square marginal barrier makes these losses sharp.  Take

```text
U=L^(2/3-eta/2),  h=L^(1/3-eta).
```

In every product fibre let `U` hub blocks share `L` symbols, and partition
the remaining blocks into `h`-block common-symbol groups.  Then

```text
I = Theta(L^3),
M = Theta(L^(8/3+eta)),
D = Theta(L^(10/3-eta)).
```

Giving every incidence triangle degree one also gives
`J=Theta(L^(10/3-eta))`.  Over a prime label field assign occurrence
`(u,p,k)` the hub anchor

```text
alpha(u,p,k)=k+s_u p.
```

For each two hubs, `(p,k)` maps bijectively to all off-diagonal ordered
anchor pairs.  Every anchor pair has multiplicity one, all anchor degrees
are equal, and the anchor graph is complete bipartite minus a matching.
Thus DRC is maximally dense, yet different hubs may use disjoint numerical
anchor sets and have no common real anchor.  Dyadic pigeonhole, DRC and BSG
cannot extract coherence from the retained marginals.

The barrier is independently realizable inside each product fibre but is
not a global point-set construction: it assigns partner coordinates
independently across repeated nonhub radius classes.  The first identity
that detects this omission is the representation-level Gram rectangle

```text
Q(P,N)+Q(P',N')-Q(P,N')-Q(P',N)
    = 2(P-P') dot (N'-N).
```

The value-level joint moment does not force this rectangle because triangle
links may use different point representations of the same squared value.
The next necessary statistic is a point-conditioned triangle or rectangle
moment retaining actual endpoint indices.  It must gain the missing
`L^(1/3+2eta-o(1))`.  Until that is proved, the coherent `c=4/5`
subtheorem does not reconnect to the full problem.

## Gram rectangle moment

`GRAM_RECTANGLE_MOMENT.md` turns every represented service

```text
Q(P,N)=Q(P',N'),  u+v=x+y
```

into its two cross cells

```text
(u+y,Q(P,N')) and (x+v,Q(P',N)).
```

These are genuine parameter-line cells in two other product fibres, so the
entire cross image lies in the same global universe of size at most `M`.
If `S` point-represented services are selected and `r(xi)` is cross-cell
multiplicity, Cauchy gives the unconditional energy

```text
R_cell = sum_xi r(xi)^2 >= 4S^2/M.
```

At `S=L^(10/3-eta)` and `M<=L^(8/3+eta)`, this is

```text
R_cell >= L^(4-3eta-o(1)).
```

Its per-service gain `L^(2/3-2eta)` exceeds the required
`L^(1/3+2eta)` for `eta<1/12`.  At the campaign value `eta=1/30`,
the cell moment exponent is `39/10`, the target is `37/10`, and the
surplus is `1/5`.

The remaining refinement is exactly quantified.  Let `V` be the maximum
number of actual cross point pairs representing a visited cell.  Refining
cell collisions by their actual point pair gives

```text
R_pt >= 4S^2/(M V).
```

Therefore the full target point-conditioned moment
`L^(11/3+eta-o(1))` holds under the explicit cross-Sidon condition

```text
V <= L^(1/3-4eta+o(1)).
```

This is a rigorous nondegenerate Euclidean subcase.  The unconditional
bound `V<=2Lm=O(L^2)` is much too weak.

An exact real vertical-translation fan proves the representation loss is
genuine.  Choose constants with

```text
C_(u,v)+R^2=C_(x,y)+S0^2
```

and translate all four heights by arbitrary distinct `A_j`.  Every
quadruple remains a service, both cross values are constant, and every Gram
rectangle identity holds.  For `r` translations the cell moment is
`2r^2`, but all actual cross point pairs are distinct, so the
point-conditioned moment is only `2r`.  The four height sets use only `r`
coordinates each.

Thus this round gives a sharp dichotomy: either the cross-Sidon condition
holds and the required rectangle moment follows, or a visited
product-fibre distance cell has more than
`L^(1/3-4eta-o(1))` actual real point-pair representations.  Controlling
the latter representation-rich branch, or proving that many translation
fans expand the global parameter union, remains open.  No unconditional
distance-exponent improvement is claimed.

## Representation-rich cross cells

`REPRESENTATION_RICH_CROSS_CELL.md` gives the exact one-cell geometry.
For a fixed cell `(p,t)` and radius block `(i,p-i)`, every representation
has

```text
a-z = +/-sqrt(t-C_(i,p-i)).
```

Thus the cell is a union of at most two vertical-translation rulings per
active block.  If `B` blocks are active, their signed multiplicities
`r_(i,+/-)` satisfy

```text
sum r^2 >= V^2/(2B),
max r   >= V/(2B).
```

Cross blocks form a hub-covered product matching, so `B<=U`.  At the
representation-rich threshold `V=L^(1/3-4eta)`, however,

```text
V/U <= L^(-1/3-7eta/2+o(1)).
```

The inequalities do not force even two representations on one ruling.
A real one-cell universality theorem confirms sharpness: any signed
multiplicity profile with per-block total at most `m` is realized by generic
translations on the geometric radius matching.  Numerical heights can be
disjoint across radius classes.

The semialgebraic cell parameters obey

```text
X^2-H^2=T^2 q^p,
4H^2+D^2=t.
```

The difference vector lies on a circle, while segment midpoints move freely
on vertical lines.  A large translation ruling gives parallel distinct
perpendicular-bisector planes, not one rich plane, so the inherited
rich-plane count does not absorb this degeneracy.

There is a stronger global ledger.  If the target point-conditioned moment
fails, Cauchy forces at least

```text
E >= L^(3-3eta-o(1))
```

distinct cross point-pair edges.  These form a bipartite graph with at most
`Um=O(UL)` hub-coordinate vertices and `Lm=O(L^2)` partner-coordinate
vertices.  If it is `C4`-free, KST gives

```text
E <= O(U L^2),
```

so the failed-moment branch requires `U>=L^(1-3eta-o(1))`.  Comparing with
the established upper bound `U<=L^(5/6+2eta+o(1))` leaves exponent surplus

```text
1/6-5eta.
```

At the campaign endpoint `eta=1/30` this surplus is exactly zero:
`E=L^(29/10+o(1))` and `U=L^(9/10+o(1))` simultaneously saturate the
point-energy, hub and bipartite `C4` capacities.  For smaller `eta`, a
coordinate rectangle is forced.

An uncoloured coordinate rectangle is not enough.  Its four edges can
belong to four unrelated cells and need not put a partner point on a
hub-pair perpendicular bisector.  What is additionally true for real shared
height sets is the signed cross-cell cocycle

```text
sum_cycle +/-sqrt(t_e-C_e)=0.
```

Independent one-cell fans cannot be pasted globally without satisfying
these equations.  No global real small-`M` obstruction satisfying all such
cycles was found.  The remaining input is a labelled-cycle surplus theorem
that turns the near-extremal coordinate rectangles into repeated/equal
distance labels, common anchors or parameter-line expansion.  No
unconditional exponent improvement is claimed.

## Labelled-C4 algebra

`LABELLED_C4_ALGEBRA.md` freezes the four radius-pair labels around a
coordinate rectangle.  With adjusted cell values

```text
A=(a-z)^2, B=(c-z)^2, C=(c-d)^2, D=(a-d)^2,
```

the signed cocycle is `x-y+w-v=0`.  Continuous squaring gives the explicit
quartic

```text
X=A+B-C-D,
F=(4CD-X^2-4AB)^2-16X^2 AB=0.
```

For fixed nonnegative `A,B,C`, there are at most four compatible values of
`D`; on a fixed actual sign branch there is only one.  This is a rigorous
constant-degree label-completion lemma.

The paired-label loci have strong vertical geometry.  Adjacent equality
`A=B` either collapses the hub heights or makes `z` their midpoint.
Opposite equality `A=C` on the equal-sign branch gives the vertical
parallelogram relation `a+d=c+z`.  For a shared arithmetic progression
`Z={0,...,m-1}`, all `m^4` point quadruples satisfy the cocycle, while there
are at most `4m^3` compatible label quadruples.  The vertical
parallelograms number exactly

```text
E_+(Z)=(2m^3+m)/3.
```

This retains both representation multiplicity and the shared capacity
`|Z|=m`, and identifies additive/translation structure as the degenerate
obstruction.

The quartic bound alone is quantitatively insufficient.  At `eta=1/30`,
`M=L^(27/10)` gives `M^3=L^(81/10)`, whereas the trivial point-rectangle
capacity from `n_H<=UL=L^(19/10)` and `n_N<=L^2` is only `L^(78/10)`.
The algebraic bound is worse by `L^(3/10)`.  Simultaneously, the forced
edge exponent and the C4-free KST threshold both equal `29/10`, so there is
no power-sized rectangle surplus.  The next input must be a weighted
quartic-energy or near-KST stability theorem retaining the shared height
sets; no unconditional exponent improvement is claimed.

## Weighted labelled-C4 dichotomy

`WEIGHTED_LABELLED_C4_DICHOTOMY.md` installs the point-conditioned weight
missing from the quartic label count.  For each signed translation fibre
`sigma`, let `q_sigma` be its number of actual coordinate rectangles, and
put

```text
Q=sum q_sigma,  J=sum q_sigma^2,
P=number of occupied signed fibres.
```

If all four height sets have capacity `m`, fibre collisions inject into
fourfold common nonzero differences.  Hölder then gives the exact chain

```text
Q^2/P <= J
J-Q <= sum_(h!=0) product_i r_(Zi-Zi)(h)
    <= m^2 product_i E_+(Zi)^(1/4)
    <= m^2 max_i E_+(Zi).
```

Hence

```text
max_i E_+(Zi) >= (Q^2/P-Q)/m^2
```

when the numerator is positive.  For any `R`, either one signed label fibre
has at least `R` actual rectangles, giving a common translated selected
subset of size `R` across all four height classes, or `P>Q/R`.  If
`Q^2/P-Q>=m^5/K`, some height set has energy at least `m^3/K`, the
BSG/Freiman regime.

Three sharp pressure tests delimit the theorem.

1. Four complete shared AP blocks have `Q=m^4`, `P=Theta(m^3)`,
   `J-Q=Theta(m^5)` and `E_+(Z)=Theta(m^3)`; they saturate every power in
   the inequality.
2. A single common translation fibre over
   `X={1,2,4,...,2^(m-1)}` has `Q=m`, `P=1`, `J=m^2`, but only
   `E_+(X)=2m^2-m`.  Thus a large fibre gives endpoint reuse, not
   automatically high additive energy.
3. Multiplying the four marginal cell representation counts is invalid.
   The same translation model has marginal cocycle energy `m^4` but only
   `m` actual rectangles.

The exact C4-free KST stability identity was also extracted.  If the sides
have sizes `h,n`, edge count `E`, partner-degree variance `V`, and `Delta`
hub pairs with no common partner, then

```text
V+2 Delta = h(h-1)-E^2/n+E.
```

An explicit prime-field transversal/Latin construction shows this is a
real barrier.  With `U<=q`, hub vertices `(s,x)`, partner vertices `(p,b)`
and adjacency `x=ps+b mod q`, it has

```text
h=Uq, n=q^2, E=Uq^2=h sqrt(n), C4=0.
```

Assigning every radius class the real AP heights `{0,...,q-1}` and
geometric radii gives at most two genuine squared-distance cells per radius
block, hence at most `2Uq` cells total and at most `q` representations per
cell.  Thus coordinate capacities, shared real height sets, representation
multiplicity, a small cell universe and quartic compatibility do not beat
KST.  The missing theorem must use the paired Gram-service origin of the
cross edges or turn this AP/translation branch into global expansion.

At `eta=1/30`, `h=L^(19/10)`, `n=L^2` and both the forced edge count and
KST scale are `L^(29/10)`, so no C4 lower bound follows.  Even under the
optimistic extra assumptions that supersaturation supplied `Q=L^(19/5)`
and this count survived freezing four radius classes, endpoint reuse of
size `L^(1/5)` would require `P<=L^(18/5)`.  Current bounds are `P<=L^6`
after four blocks are frozen and `P<=M^3=L^(81/10)` globally, leaving
gaps `L^(12/5)` and `L^(9/2)`.  Near-maximal additive energy would require
the still stronger `P<=L^(13/5)`.  Naive radius-quartet freezing itself may
cost `U^2L^2=L^(19/5)`, so this is only a best-case gap ledger.  No
unconditional exponent improvement is claimed.

## Gram-service lift of the Latin obstruction

`GRAM_SERVICE_LATIN_LIFT_AUDIT.md` restores the information omitted by the
unpaired cross representation graph.  A service with cross edges

```text
(u,a)--(y,d),  (x,c)--(v,z)
```

must first satisfy the radius-diagonal constraint

```text
u-y=x-v.
```

Writing the two signed cross shifts as `lambda=a-d`, `mu=c-z` and the
partner displacement as `theta=d-z`, the original equal-distance condition
is exactly

```text
C_uv-C_xy+lambda^2-mu^2+2 theta(lambda+mu)=0.
```

For distinct same-product geometric radius blocks, `lambda+mu` cannot
vanish, so

```text
theta=(C_xy-C_uv-lambda^2+mu^2)/(2(lambda+mu))
```

is uniquely forced.  The hub displacement is simultaneously forced as
`c-a=mu-lambda-theta`.  Hence one fixed paired signed-cell/radius type
supports at most `m` actual services.  A two-block real translation fan
attains exactly `m`, so this cap has no local power saving.

This new condition excludes the explicit unshifted Latin construction from
the preceding round.  If all heights lie in an interval of diameter `H`,
two same-product blocks with radial-offset gap greater than `H^2` cannot
form a service.  For geometric radii and the Latin block pattern,

```text
C_(u,y+Delta)-C_(u+Delta,y)
  =(B^(2Delta)-1)(B^(2y)-B^(2u)).
```

With the shared heights `{0,...,q-1}` this exceeds `(q-1)^2` on every
nontrivial same-diagonal block pair.  At `q=7,U=4`, exhaustive verification
checks 196 cross edges, 32 eligible radius-block pairs and 1568 candidate
edge pairs, finding zero nontrivial Gram services.  Thus the previous Latin
graph is not a counterexample to the full service problem.

The remaining consistency is a pair of coupled coboundaries.  Every service
labels its partner projection by the forced `theta` and its hub projection
by `mu-lambda-theta`; both label sums must vanish around every corresponding
coordinate cycle.  This constraint is strictly stronger than the
unpaired labelled quartic.

At `eta=1/30`, a full translated-Latin lift would need

```text
S=L^(33/10) services,
E=L^(29/10) distinct cross edges,
average service degree per cross edge=L^(2/5).
```

Its Cauchy point moment would be exactly `S^2/E=L^(37/10)`, equal to the
target with zero power surplus.  The sharp `m` cap requires at least
`S/m=L^(23/10)` paired signed types, while same-diagonal radius-block pairs
have capacity `LU^2=L^(14/5)`, leaving `L^(1/2)` slack.  Arbitrary
radius-class translations can also defeat the global-diameter obstruction.
The unresolved object is therefore precise: a translated Latin service
design satisfying both forced-shift coboundaries with average compatibility
degree `L^(2/5)`.  No such full construction and no power-saving exclusion
is currently proved.

## Translated-Latin service complex

`TRANSLATED_LATIN_SERVICE_COMPLEX.md` places the two forced service
displacements in one coordinate complex.  Orient a service boundary as

```text
P -> P' -> N -> N' -> P.
```

The height-difference 1-cochain on its four sides is

```text
psi, -mu, theta, lambda,
```

so every service obeys the local four-cycle identity

```text
psi-mu+theta+lambda=0.
```

Every four- or six-cycle in the partner and hub projections has alternating
sum zero in the `theta` and `psi` labels.  Substituting

```text
theta=(Delta-lambda^2+mu^2)/(2(lambda+mu)),
Delta=C_xy-C_uv,
```

shows that if `(lambda,mu)` is synchronized on one even cycle, its radial
gaps satisfy the low-rank identity

```text
Delta_1-Delta_2+Delta_3-Delta_4=0
```

or the analogous six-term relation.  This is a valid conditional route to
geometric-radius rigidity, but repeated signed shifts have not been forced.

The smallest coupled translated-Latin enumeration is SAT.  For `q=3,U=2`,
ordinary integer radius diagonals leave two singleton boundary blocks.
The remaining two paired strips have `3!^2=36` matching choices.  One exact
choice is

```text
pi_0=(2,0,1), pi_1=(1,2,0).
```

With radii `rho_j=2^j`, partner indices `5,6,7`, and translated height APs
whose shifts are

```text
alpha_0=0,
alpha_1=(-1+sqrt(49149))/2,
beta_0=(-1+sqrt(49149)-sqrt(12285))/2,
beta_1=-1/2, beta_2=1/2,
```

all six Gram services hold exactly.  Their equations reduce to

```text
alpha_1^2+alpha_1=12287,
(alpha_1-beta_0)^2=12285/4.
```

The design uses all 12 cross edges of the maximal pairable core exactly
once and only six distinct cross cells.  Its partner projection is a
forest.  Its hub projection has three parallel two-cycles, and each pair
has identical `psi`, so the first coupled cochain tests all close.

This is a genuine finite real geometric service core, not merely an
abstract finite-field model.  It is not an asymptotic counterexample to the
original problem: it has fixed `q=3,U=2`, deletes two unavoidable boundary
blocks, has service degree one instead of `L^(2/5)`, and does not control
all unused distances or angular copies.  Its exact consequence is that
the double coboundary has no universal finite forbidden pattern.  A proof
must force a dense family of synchronized 4/6-cycles, while a counterexample
must extend this SAT core to average compatibility degree `L^(2/5)` with a
small global cell universe.

## SAT-core scalability audit

`SAT_CORE_SCALING_AUDIT.md` tests the two most direct amplifications of the
finite translated-Latin core.

Common translation copies on the same five-radius skeleton give

```text
m=3r, S=6r, E_cross=12r,
average cross-edge service occurrence=1.
```

The six visited cross cells remain fixed and the full cell count on the
fixed skeleton is `O(r)`, since all height differences lie in a constant
number of translates of `A-A`.  However, the construction has only
`Theta(r)` points and no compatibility-degree growth.  The unique partner
shift formula forces the two cross edges of a same-palette service to use
the same translation copy.

Retaining every cross-copy version improves the raw counts to

```text
m=3r, S=6r^2, E_cross=12r^2,
visited cells=O(r), average occurrence=1.
```

For a translation step transcendental over the SAT core's number field,
subtracting a base Gram equation shows that the unique compatible opposite
edge uses the swapped pair of translations.  Thus even the full
cross-copy amplification has degree one.  Resonant translation sets could
create additional partners, but this becomes a new additive-hyperbola
problem.

Separating `k` radius-skeleton layers and using `r` translations per layer
gives

```text
radius classes=5k, m=3r,
S=6kr^2, E_cross=12kr^2, average occurrence=1.
```

For separated geometric scales, every radius block contributes at least
`r` cells, so the full union is `Omega(k^2 r)`.  At `k~r~L`, this has
`S=L^3`, short of `L^(33/10)` by `L^(3/10)`, while its cell count is
`L^3`, exceeding `L^(27/10)` by `L^(3/10)`.  Thus direct layering fails on
both service mass and global distance capacity.

A quantitative synchronized-cycle capacity lemma is now available.  Colour
each simple partner or hub service-projection edge by its ordered signed
pair `(lambda,mu)`, with palette size `K`.  If no colour contains any
cycle, `S<=K(N-1)`.  Standard even-cycle capacities give

```text
no monochromatic C4:       S << K N^(3/2),
no monochromatic C4 or C6: S << K N^(4/3).
```

Every forced monochromatic even cycle yields an alternating additive
relation among its radial gaps.  At `eta=1/30`, the resulting palette
thresholds are

```text
                         partner N=L^2    hub N=L^(19/10)
some synchronized cycle     K<L^(13/10)     K<L^(7/5)
synchronized C4             K<L^(3/10)      K<L^(9/20)
synchronized C4 or C6       K<L^(19/30)     K<L^(23/30).
```

The required cross-edge compatibility degree `L^(2/5)` alone is below the
short-cycle threshold.  No current consequence of `M<=L^(27/10)` bounds
the numerical signed-shift-pair palette by `L^(19/30)` or `L^(23/30)`.
Thus the first rigorous synchronized-cycle threshold is identified, but it
has no present exponent surplus.  The SAT core remains a finite local
warning, not a counterexample to the original geometric statement.

Exact exhaustive searches over several small integer universes found no
anomalously small parameter-line configuration; the minima in those samples
used a common arithmetic height progression.  These computations are
falsification evidence only, not a proof of the unrestricted conjecture.

A geometric two-angular-slice construction with `F=binom(q,2)` distinct
anchored affine maps but only `q` endpoint values proves that two angles alone
are intrinsically limited to `sqrt(F)`.  For the full anchored union, a bound
`S F^(beta-o(1))` improves the inherited exponent iff `beta>1/3`; the strong
target `S sqrt(F)` would give `N^(7/10)`.  None of these missing multi-slice
or parameter-energy bounds has yet been proved.

### Round 27: resonant translation-hyperbola capacity

The same-base-service compatibility problem for an arbitrary translation
set is now exact.  With signed base gaps `X,Y`, put `u=s-beta` and
`v=gamma-delta`.  Compatibility is

```text
u^2-v^2+2Xu-2Yv=0,
(u+X)^2-(v+Y)^2=X^2-Y^2.
```

If `r_A` is the ordered difference representation function, the total
service count over all first cross edges is exactly

```text
H_X,Y(A)=sum_{F(u,v)=0} r_A(u)r_A(v).
```

For `X != +/-Y`, every coordinate has at most two partners.  Separating the
universal zero difference gives

```text
H_X,Y(A) <= 2 E_+(A),
H_X,Y(A) <= n^2 + 2 mu_* n^2 + mu_* n,
mu_* = max_{t != 0} r_A(t).
```

Thus average degree `n^(2/5)` forces
`E_+(A) >= (1/2)n^(12/5)` and a nonzero popular difference of multiplicity
`Omega(n^(2/5))`.

Fixed rational APs have only a constant number of supported difference
pairs by a fixed-integer divisor argument.  Difference-Sidon sets,
including GPs, have average degree below four.  The classical convex-energy
bound gives only `O(n^(1/2))` average degree and misses the desired
exclusion; exact square-sequence searches through size ten have maximum
degree two.

Pointwise bounded degree is false.  Hyperbola parametrization gives an
explicit set of size `2r+1` on which one edge has at least `r+1` partners.
This is certified over the actual `q=3` SAT base field with
`X=-3/2`, `Y=sqrt(12285)/2`, and `X^2-Y^2=-3069`.  It is a resonant star,
not a dense network, and adds only linearly many incidences to a quadratic
baseline.

The one-dimensional route is eliminated for AP/GP/low-energy sets but not
for every translation set.  The remaining case is a high-energy set with
a popular nonzero overlap supporting a dense shifted-hyperbola network.
See `TRANSLATION_HYPERBOLA_ENERGY.md` and
`verify_translation_hyperbola_energy.py`.

### Round 28: multistar optimization and logarithmic average growth

The single resonant star has now been separated from genuine average-degree
growth.  A subset-zeta optimizer assigns every compatible ordered quadruple
to its vertex-support mask and therefore evaluates `H` for every subset of
a finite universe exactly.

For the rational model `X=2,Y=1`, every integer set satisfies

```text
H=(n+r_A(2))(n+r_A(4)) <= (2n-1)(2n-2) < 4n^2,
```

with equality on a step-two AP.  All subsets of a 12-point lattice were
exhausted.  For the actual SAT parameters, all subsets through size 12 of
the 17-point universe generated by `t=+/-1,...,+/-4` were exhausted.  The
largest average was `95/81`, attained at size 9; the size-12 optimum was
`160/144`.

Actual SAT translations restricted to rationals have

```text
H=n^2+n r_A(3) <= 2n^2-n.
```

More generally, for a two-layer set `A=P union (Q-Y)`, coefficient
comparison leaves only four fixed exceptional solutions and the scalable
family

```text
u=a, v=c-Y, (a-3/2)^2-c^2=-3069.
```

This gives an exact multistar-overlap reduction: average growth requires
simultaneously popular same-layer differences `a` and cross-layer
differences `c` on this hyperbola.

Universal bounded average degree is nevertheless false.  With a
transcendental `T`, take the `2k` Laurent-independent generators

```text
u_j=(T^j-3069 T^-j)/2+3/2,
c_j=(T^j+3069 T^-j)/2,
```

form the side-`L` additive box `P` on these generators, and put
`A=P union (P-Y)`.  Both `(u_j,c_j-Y)` and `(u_j,-c_j-Y)` are compatible.
The resulting exact ledger is

```text
n=2 L^(2k),
H=n^2 [1+k(1-1/L)^2],
|A-A|=3(2L-1)^(2k).
```

For `L=2`, the average degree is exactly
`1+k/4 = 1+(1/4)log_4(n/2)`.  A Laurent-unit factorization proves there are
no other supported nonconstant hyperbola points.  Thus multistar merging
does produce genuine unbounded average degree, but only logarithmically.
Its service mass remains `n^(2+o(1))`, so it changes no global polynomial
exponent and misses the `33/10` target by `13/10`.

See `RESONANT_MULTISTAR_OPTIMIZATION.md` and
`verify_resonant_multistar_optimization.py`.

### Round 29: optimal lattice-multistar scale and no-go theorem

The resonant multistar ansatz has now been audited under variable side
lengths, generator repetitions, low-rank relations, additive tensors, and
generic/lattice-aligned unions.

For the independent-frequency box,

```text
n=2L^(2k),
average=1+k(1-1/L)^2.
```

Eliminating `k` shows that every choice `L=L(k)` remains `O(log n)`; among
integer side lengths the logarithmic coefficient is maximized at `L=4`.
Repeating generators only enlarges an effective side length after
properization and changes constants.

Low-rank relations give a genuine improvement.  At one Laurent frequency,
normalize a rank-three lattice so that each resonant parameter has integer
coordinates `x,y` satisfying

```text
x y = N.
```

Thus the number of supported resonances is at most the divisor count
`tau(N)`, with `|N|<=n`.  Conversely, selecting the densest dyadic bin of
divisors of a highly composite `N` gives a proper rank-three box with

```text
n <= 210 N,
average >= 1 + tau(N)/(28(1+log_2 N)).
```

Hence the optimal scale of the lattice-aligned Laurent ansatz is

```text
average =
exp(Theta(log n / loglog n)) = n^o(1),
upper maximal-order constant log 2.
```

Additive tensor/product gains add rather than multiply: Laurent-unit
factorization forces all but one algebraically independent frequency to
cancel.  The number of frequencies is `O(log n)`, which is absorbed in the
subpolynomial bound.  Generic unions obey a quadratic-mass weighted bound;
unions whose cross resonances stay lattice-aligned properize back to the
same divisor problem.

The reviewable scoped theorem is:

```text
H_X,Y(A)/|A|^2
 <= exp((log 2+o(1)) log|A|/loglog|A|)
 = |A|^o(1)
```

for proper Laurent-lattice boxes, properized repetitions, independent
additive tensors, and generic/lattice-aligned unions.  It misses the target
`|A|^(2/5)` by the explicit factor `|A|^(2/5-o(1))`.

The minimal dependencies are the two-layer reduction, Laurent-ring units,
proper-box overlap counts, quadratic-mass convexity, and the classical
maximal order of `tau`.  These are useful structural lemmas, but without an
extension to arbitrary high-energy translation sets or an application
closing an open case they are not yet a standalone high-impact resolution.

See `RESONANT_ANSATZ_CONVERGENCE_AUDIT.md` and
`verify_resonant_ansatz_no_go.py`.

### Round 30: final escape-route audit

The remaining non-lattice routes have been classified against the exact
weighted target

```text
sum_t r_A(u(t)) [r_A(c(t)-Y)+r_A(-c(t)-Y)] >= n^(12/5).
```

Fixed algebraic number fields reduce to ideal divisors times a fixed-rank
unit lattice and give `n^o(1)`.  A nonconstant polynomial parametrization
of the factor equation is impossible because polynomial-ring units are
constant; rational and Laurent parametrizations return to denominator
ideals or the Round 29 bound.

For the actual quadratic GAP

```text
A_L={i+jY: 0<=i,j<L},
```

only four coefficient-difference pairs survive and

```text
H=L^2(2L-3)(2L-2), average -> 4.
```

A generic rank-two GAP `A={i+j theta}` with `theta` transcendental or of
degree greater than two over `Q(Y)` has only `(u,v)=(0,0),(3,0)`, by
coefficient comparison.  Bounded algebraic degree returns to the
fixed-field argument.

Several different divisor layers cannot multiply the gain.  Generic unions
are weighted by `n_i^2`; independent tensors add their average-degree
gains; commensurable cross-coupling clears to one common divisor equation.
Fixed-rank multiplicative groups have only polylogarithmically many
bounded-height elements.  An exact rational S-unit experiment using all
divisors of primorials makes every shift popular, but still has
`|T|=tau(D)` and `n=D^O(1)`, hence divisor-scale growth only.

One genuinely uncovered candidate remains: a growing-degree,
growing-multiplicative-rank, noncommensurable set whose hyperbola image lies
in the popular difference set of one small-doubling `A`.  At fixed overlap
density it needs at least `n^(2/5)` parameters, and it must avoid any common
integer/ideal factor equation of norm `n^O(1)`.  No explicit family was
found; current finite experiments are negative evidence.

See `ESCAPE_ROUTE_AUDIT.md`, `NEXT_BREAKTHROUGH_TARGET.md`, and
`verify_escape_route_audit.py`.

### Round 31: exact growing-degree cyclic-unit search

Exact arithmetic in `Z[x]/(f)` now computes the coordinates of

```text
2u=theta^e-3069 theta^(-e)+3,
2c=theta^e+3069 theta^(-e).
```

Every field remains irreducible over `Q(sqrt(1365))`.  For each exponent
subset, the smallest doubled rectangular power-basis GAP is built and all
selected overlap contributions are computed exactly.

The sparse search covered 104 fields of degrees 3–8 and all 511 subsets of
`[-4,4]`: 53,144 evaluations.  The best average decreased from `7.34029`
in degree 3 to `4.85830` in degree 8, while box size grew from about
`10^16` to `10^35`.

The complete `|a_i|<=2` search covered 36 cubics and 122 quartics, or
80,738 further evaluations.  The best multi-parameter normalized target
ratio was `6.19e-4`, attained by

```text
f=x^4+x^2-1, exponents={-4,-2,0,2,4},
n=150810678, certified average=2.157...
```

No growing-degree seed was found in the exact range.

For a fixed non-torsion algebraic unit, expanding and contracting
archimedean embeddings prove that only `O_theta(log n)` powers fit in a
power-basis box of size `n`.  The remaining gap is nonuniform field growth
or several multiplicatively independent units coupled to a nonrectangular
additive container.

See `GROWING_DEGREE_UNIT_ORBIT_SEARCH.md` and
`verify_growing_degree_escape_search.py`.

### Round 32: two-unit quartic and nonrectangular sanity check

All 122 accepted quartic fields with `|a_i|<=2` were searched.  For each,
two small exact norm-`+/-1` elements were retained after excluding every
relation `theta^a epsilon^b=1` with `|a|,|b|<=6`.  This is bounded-word,
not global, independence.

The nine words with exponents in `[-1,1]^2` have 486 rank-two subsets.
Across 244 unit pairs, 118,584 subsets received exact rectangular scores.
For the leading 32 candidates per objective and pair, all 25 identity or
single-shear unimodular coordinate maps were evaluated.

The best target-normalized candidate is

```text
f=x^4+x^3-2x-1,
epsilon=-1-theta,
words={(-1,1),(0,0),(0,1)},
shear x0 -> x0-x3,
n=2035999422,
certified average=1.772...,
(average-1)/n^(2/5)=1.45903e-4.
```

The rectangular ratio was `1.45205e-4`, so the nonrectangular improvement
was about `0.48%`.  No two-unit finite seed was found.

For a fixed unit rank `r`, bounded-height unit words number
`O_K((log n)^r)`.  A necessary condition for the target is therefore

```text
r >= (2/5-o(1)) log n / loglog n.
```

Fixed quartic rank cannot escape asymptotically.  The remaining bottleneck
is additive compression of a genuinely growing-rank unit lattice, not
another fixed-field constant optimization.

See `TWO_UNIT_NONRECTANGULAR_SEARCH.md` and
`verify_two_unit_nonrectangular_search.py`.

### Round 33: unit-rank uniformity correction

The fixed-field count `O_K((log n)^r)` is not uniform when the field varies.
If `lambda_n` is the shortest vector of the relevant logarithmic unit
lattice and all parameters have radius at most `C_n log n`, direct packing
gives

```text
|T_n| <= (1+2 C_n log(n)/lambda_n)^r.
```

Target average `n^(2/5)` therefore forces exactly

```text
r >= ((2/5)log n+O(1)) /
     log(1+2 C_n log(n)/lambda_n).
```

The earlier `2/5` coefficient is valid only when
`log C_n+log(1/lambda_n)=o(loglog n)`.  For a full power-basis box with
`d<=log_2 n` and only the standard degree-dependent unit-height bound
`lambda_n>=d^(-1-o(1))`, the safe consequence is instead

```text
r >= (1/5-o(1)) log n / loglog n.
```

Without uniform height/container assumptions, no coefficient `2/5`
follows for growing fields.

The minimum full-coordinate cost `2^r` does not close the route: at rank
`Theta(log n/loglog n)` it is only `n^o(1)`.  The precise missing theorem
must link independent logarithmic unit directions to independent additive
side growth, or uniformly control height from container cardinality.

See `UNIT_RANK_UNIFORMITY_AUDIT.md` and
`verify_unit_rank_uniformity_audit.py`.

### Round 34: raw unit-side growth is false; symmetrized replacement

The proposed implication from independent logarithmic unit directions to
independent additive directions is false.  Let

```text
f(x)=product_{k=1}^5 (x+k)-1
```

and `f(theta)=0`.  The polynomial is irreducible and totally real.
Each `theta+k` is a norm-one unit and their product is one.  An interval
calculation built by dividing degenerate integer intervals entirely inside
a high-precision interval context places a `4x4` logarithmic minor for
`theta+1,...,theta+4` inside the rounded-out interval

```text
[6.31087583266352, 6.31087583266354],
```

so these four units are multiplicatively independent.  Yet all lie in the
two-dimensional additive span of `1,theta`.

The geometric compatibility uses `t+R/t` and `t-R/t`, not raw `t`.
For the exact family `product_{k=1}^d(x+k)-1`, `5<=d<=12`, the raw unit
vectors retain additive rank two, while the inverse-symmetrized vectors
have full rank `d`.  Their smallest doubled power-basis boxes grow from 27
to 120 decimal digits.

A general determinant-volume lemma is now isolated.  If `s` shift vectors
lie in a proper integral box and have coordinate minor `Delta`, then

```text
|P| >= |Delta|/s!.
```

Therefore the condition

```text
|Delta|/s! >= |T|^(5/2+eta)
```

would force `|T|<=|P|^(2/5-delta)` and close the box ansatz.  The proposed
inverse-symmetrized determinant statement is explicitly a **CONJECTURE**,
requiring bounded-index integral coordinates, height control, and removal
of subfield/norm-torus degeneracies.

See `SYMMETRIZED_UNIT_CONTAINER_AUDIT.md` and
`verify_symmetrized_unit_container.py`.

### Round 35: exact consecutive-unit determinant

The observed inverse-symmetrized full rank now has a symbolic explanation.
For

```text
q_k=product_{j!=k}(x+j),
U_k=2u(theta+k)=x+k-3069*q_k+3,
C_k=2c(theta+k)=x+k+3069*q_k,
```

the ascending-coefficient minor on

```text
U1,C1,U2,C2,U3,...,U_(d-2)
```

is exactly

```text
(-1)^d * 4 * 3069^(d-2) * product_{m=1}^{d-3} m!.
```

The proof uses the evaluations
`q_k(-j)=0` for `j!=k` and
`q_k(-k)=(-1)^(k-1)(k-1)!(d-k)!`.
Thus the `q_k` are a scaled Lagrange basis, with coefficient determinant
`product_{m=1}^{d-1}m!`.  Elementary row operations reduce the selected
symmetrized rows to two affine rows and `d-2` of the `q_k`.

The determinant satisfies

```text
D_(d+1)=3069*(d-2)!*D_d.
```

Its decimal digits for degrees 5 through 12 are
`12,16,21,27,33,40,48,57`; the exact doubled coordinate-box digits are
`27,36,46,57,71,85,102,120`.  Both box and forced determinant volume have
formal logarithm `Theta(d^2 log d)`.  Exact algebra verifies irreducibility
and total reality through degree 30.  The determinant identity itself holds
for every degree, but its interpretation as an asymptotic number-field
container theorem is conditional on irreducibility and a real degree-`d`
root along an unbounded sequence; that has not been proved.

The compatibility audit is negative for counterexample construction.
Whenever those number-field hypotheses hold, the half-scaled two-coset
rectangular set has additive doubling `n^o(1)` and the selected shifts have
overlap density at least `2^-d=n^-o(1)`, but there are only
`d-1=n^o(1)` parameters.  This is far below `n^(2/5)`, even with optimally
generous overlap.  The identity strengthens the obstruction program; it
does not produce the required geometric counterexample or an unconditional
infinite family.

The degree-five log-unit certificate was also hardened.  Exact rational
root endpoints no longer pass through ordinary `mp.mpf`; all endpoint
division and logarithms remain in `mp.iv`, every shifted interval is
asserted not to cross zero, and two precision levels are regression-tested.
