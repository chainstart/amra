# Independent audit — OPG-1757 breakthrough package

Date: 2026-07-31

Two agents independently audited the symbolic proof rather than merely
rerunning the certificates. Their common verdict follows.

## Claims that pass

- ENDPOINT_POLYNOMIALITY_THEOREM.md is proof-grade. The unique
  alternating-path decomposition gives the stated two-marked kernel, its
  path pole cancels the Lagrange Jacobian, and the remaining termwise
  \(s\)-valuations are nonnegative in every same/different-component and
  zero/positive-excess case, including the \(N=0\) boundary.
- ALL_FIXED_DEFICIT_EVENTUAL_POSITIVITY_THEOREM.md is proof-grade after
  interpreting strict positivity on the natural support. The endpoint
  curvature, symmetric determinant kernel, and four-profile EGF collapse
  independently recompute to

  \[
  [s^{2q+r}]R_{q,r}=\frac4{q!}[z^r](1+2z+2z^2)^q>0.
  \]

  Hence, for every fixed \(q\), all \(2q+1\) supported coefficients are
  eventually positive. Coefficients below \(\beta^{2n}\) are structurally
  zero, so literal ambient-degree strict positivity is not claimed.

## Initial objections and final disposition

- The first audit held the universal second symbol conditional because
  its all-\(q\) quantifier lacked a formal filtered-ring argument.
  LAURENT_DEGREE_LEMMA.md now proves that Laurent loss \(k\) implies joint
  \((e,\rho)\)-degree at most \(2k\), jointly tracking \(V^\rho\), marked
  \(V^{\rho-1}\), Euler operators, and normalized \([v^e]\) extraction.
  A second independent line-by-line audit passed its unified functional,
  shifts, marking constants, and Jacobian degree credit. A new exact
  three-marking symbolic firewall also passes. Root independently
  evaluated the unified functional against 54 exact endpoint-polynomial
  values (all markings, two sample sizes, \(e\le2,c\le3\)); all agreed.
  Final status: **PROVED**.
- The logarithmic-over-logarithmic growing window needs an explicit
  uniform coefficient-height majorant. The present ledger has the right
  scale but must jointly account for varying shifts, restricted
  compositions, endpoint products, normalization, and the absence of
  \(s\)-dependent denominators. Status: **CONDITIONAL**.

## Exact checks

- two-marked endpoints: 12/12, including \(N=0\);
- endpoint polynomiality: 108/108;
- leading-symbol extended audit: 36 endpoint curvatures, 8 profile
  collapses, and 49 exact-layer coefficients;
- second-symbol evidence: 216 endpoint Laurent coefficients, a 111-term
  degree-four kernel, Touchard collapse, exact \(q=1\) cancellation, and
  the three-marking filtered-functional firewall, plus 54 independent
  exact unified-functional comparisons;
- unit tests: 2/2.

No audit found a substantive defect in the endpoint-polynomiality or
arbitrary-fixed-deficit theorem.
