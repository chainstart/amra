# OPG-1757: ten-proofs method transfer note

Date: 2026-08-02  
Snapshot read: `openai/ten-proofs@94bc0fe`  
Sources: `SpherePacking.lean`, `MetricCodes.lean`,
`EhrhartVolumeInequality.lean`, and Chapters 1, 2, 9 of the official
`reasoning-walkthroughs.pdf` (local text supplied by the campaign lead).

Status: **METHOD EXTRACTION ONLY; OPG-1757 REMAINS OPEN**.

## 1. Common proof architecture

The three proofs use different mathematics, but the reusable architecture is
the same.

1. **Relax the extremal statement into a sign/energy inequality.**  Do not try
   to optimize the original object directly.  Sphere packing passes to a
   Fourier linear program; codes pass to a trace/Gram kernel; Ehrhart passes
   to a filtered Bergman space and a scalar log-partition slope.
2. **Normalize so that the sought constant becomes a geometric or spectral
   threshold.**  In `SpherePacking.lean`, `balancingScale` equalizes the two
   origin values and converts a quotient into a sign radius.  In
   `MetricCodes.lean`, three distinct weights (dimension, recurrence, and
   isometric block amplitude) are kept separate until the coordinate maps are
   genuinely isometric.  In `EhrhartVolumeInequality.lean`,
   `BodyScale.canonicalScale` turns volume into the unique scale at which the
   jet lower slope and geometric upper slope can meet.
3. **Replace termwise optimism by a positive global certificate.**  Sphere
   packing has both a universal Mellin obstruction and a positive tempered
   dual witness.  Metric codes prove positivity from the *complete Gram
   remainder* of moving projections; an individual associated polynomial can
   have the wrong sign.  Ehrhart uses the genuine rank-one level-one Bergman
   kernel to prove convexity of the correct log partition; pointwise convexity
   of finite rays does not suffice.
4. **Separate the scale limit from endpoint control.**  Interior asymptotics
   identify the limiting constant/symbol.  Separate estimates treat the
   unbounded frequency tail, short-radius interval, escaping representation
   rows, weak-probability mass escape, or shrinking-ball endpoint.  None of
   the three proofs extrapolates from an interior limit to a boundary.
5. **Use an exact finite identity as the bridge back to the original
   problem.**  Examples are Poisson summation plus balancing, the trace Gram
   identity for moving projections, and the jet layer-cake identity.  The
   asymptotic argument is never allowed to replace this bridge.

## 2. Source-specific lessons

### 2.1 Sphere packing: primal relaxation, balancing, and dual witness

The formal file packages admissibility in `CohnElkies.Admissible`, defines the
quotient and normalized program, and proves that dilation by
`balancingScale` produces `balancedFunction`.  Its anti-Fourier part is an
`AntiFourierWitness`; the theorem `normalizedCost_ge_of_no_antiFourierWitness`
is the exact bridge from local sign exclusion to a universal primal lower
bound.  The eventual result is then stated uniformly over *every* admissible
function in `SharpCohnElkiesManuscriptConclusions.universal_nonnegative_delta`.

The walkthrough highlights two safeguards that matter for OPG:

- a global norm bound failed because it forgot where the negative mass lived;
  the successful Mellin argument preserved the sign location;
- pointwise decay on an interior Mellin line was not enough; an additional
  tail bound was required before Fourier inversion.

The matching construction also has a transferable repair pattern.  A local
near-optimal perturbation ruined global damping.  A tiny remote shell restored
the missing global sign while being asymptotically invisible at the target
saddle.  Thus a certificate may be assembled from a sharp local component
plus a small firewall component, provided both effects are quantified.

### 2.2 Metric codes: exact normalization and complete Gram remainder

The first associated recurrence was numerically attractive but false because
its edges were not induced by actual orthogonal coordinate maps.  The Lean
development therefore constructs the Boolean raising/lowering maps, primitive
harmonic embeddings, channel matrices, and projection Gram features before
stating the asymptotic rate theorem.  The end product
`MetricCodes.Johnson.main_binary_theorem` is strict against the optimized MRRW
rate, and `HigherHierarchy.strict_hierarchy` includes the boundary analysis
needed to compare optimized infima.

The decisive lesson is:

> Positivity should be certified after all cancelling channels are assembled,
> not demanded from every summand.

For the moving projections, positivity is the Hilbert--Schmidt Gram identity
for the full remainder.  The two mixed terms are both essential.  The
walkthrough explicitly warns that an associated Gegenbauer channel can have
a negative coefficient although the full weighted remainder is positive.

Endpoint stability is equally important.  Improving every fixed parameter
tuple does not improve an infimum if tuples can escape.  The proof compactifies
escaping interlacing pairs, obtains a lower-level configuration plus a scale
factor, and only then concludes strict hierarchy.  For the binary bound,
interior and endpoint minimizers require different constructions (Johnson
shells versus the whole cube).

### 2.3 Ehrhart: filtration dual certificate, truncation, and slope sandwich

The factorial missing from symmetrization is recovered as the leading
coefficient of an `n`-variable jet count.  The formal development starts with
the exact lattice-count limit
`monomial_count_div_pow_tendsto_volume`, constructs the jet filtration and an
adapted orthonormal basis, and truncates vanishing orders at the canonical
scale.  Truncation gives an exact uniform bound; this is what permits passage
to the limiting probability without controlling rare extreme jets.

The central proof is a two-sided slope certificate:

- jet codimension gives a sharp lower bound on an initial slope;
- rank-one Bergman positivity gives convexity of the *correct* scalar
  log-partition;
- a shrinking complex ball gives the linear upper growth and hence an upper
  bound on the initial slope.

The file culminates in
`momentBodySharpJetScale_le_dimension_of_weakProbability`, then converts the
scale inequality to volume in
`normalizedVolume_le_sharpConstant_of_momentBodyWeakProbability`, and finally
discharges weak convergence in
`momentBodyBergmanWeakProbabilityConvergence_unconditional`.

Two warnings transfer directly.  First, the easy averaged convex ray is not
the desired log partition; Jensen points in the wrong direction.  Second,
local Laplace convergence on a noncompact space is not enough: normalization,
no-mass-escape, and total-variation/weak convergence are separate obligations.

## 3. Translation to the OPG-1757 boundary layer

The old campaign has exact common-base decompositions

\[
 T_{s,k}=\sum_{a=2}^{p}[\beta^k](1+a\beta)^{L}C_{a,s}(\beta),
 \qquad p\in\{6,7\},
\]

for two sufficient kernels and two page remainders.  The existing proof keeps
one positive coefficient from the dominant `p`-base and bounds *all* lower
bases by absolute values.  This produces the coarse budgets `30` and `36`,
hence `d>=241 log s`.  The remaining layer is
`31 <= d < 241 log s`.

The three transferred principles suggest the following replacement.

### 3.1 Tropical/scale normalization

For `k = c log s + O(1)`, normalize each base contribution by

\[
 p^k\binom{L}{k}s^\kappa.
\]

A term with base `a`, polynomial `s`-degree `m`, and fixed beta shift `j`
has scale

\[
 s^{m-\kappa-c\log(p/a)}(\log s)^j
\]

up to an explicit positive constant.  Thus the logarithmic layer is governed
not by the single dominant base, but by a finite upper envelope of affine
functions

\[
 e_{a,m}(c)=m-\kappa-c\log(p/a).
\]

The breakpoints of this envelope are the exact analogue of escaped rows or
endpoint minimizers.  They must be classified before any uniform positivity
claim.

### 3.2 Complete channel certificate

At each open interval between breakpoints, collect **all** terms on the top
scale, including cancellations between lower bases and beta shifts.  The
certificate sought is the leading normalized profile, not positivity of each
`C_{a,s}`.  If that profile is positive, keep a quantitative margin and bound
only the genuinely lower scales.  If it vanishes, pass to the next asymptotic
order, as one does with a filtered slope.  This is the common-base analogue of
the complete Gram remainder.

### 3.3 Endpoint and finite-column splice

Three endpoints need independent treatment:

- `c=0`, where fixed-column positivity already proves `d<=30` and where any
  normalized logarithmic profile may have high-order vanishing;
- every tropical breakpoint, where two or more bases have equal scale;
- the old dominant-base threshold, where the new certificate should splice
  into the proved `d>=241 log s` theorem.

The intended output is therefore a finite certificate table:

1. exact `(base, s-degree, beta-shift, leading coefficient)` data;
2. exact isolating intervals for every scale breakpoint;
3. a sign certificate for every open chamber and every tied endpoint;
4. a computable remainder bound, plus an explicit fixed-`s` verification
   threshold if possible.

## 4. Immediate attack plan and firewall

The next computation will reconstruct the four exact common-base sums from
the frozen old-campaign formulas, extract the full scale spectrum, and test
the leading tied profiles.  It will not infer positivity from sampling.  A
negative leading profile would be recorded as a rigorous obstruction to this
sufficient-kernel route, not automatically as a negative coefficient of the
actual transport.

No statement in this note proves either complete transport, the universal
third-active row, or OPG-1757.  All remain **OPEN**.
