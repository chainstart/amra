# Erdős #1083: two-hour proof attack

Date: 2026-07-30

## Outcome

The campaign did **not** solve Erdős #1083 and did not improve the
recognized arbitrary-set bound
\[
f_3(N)\gg N^{3/5}.
\]

It did prove a stronger structural theorem under the repository's
audited critical-codegree setup; the hub exclusion is unconditional
once those explicit hypotheses are assumed.  In the normalization
\(N=t^5\), the previous Euclidean matching exponent moved through
\[
\frac15
\quad\longrightarrow\quad
\frac9{41}
\quad\longrightarrow\quad
\boxed{\frac29}.
\]
More precisely, for every fixed \(\varepsilon>0\), at least
\(t^{1-o(1)}\) selected distance labels support a matching of
\[
t^{2/9-\varepsilon-o(1)}
\]
pairwise disjoint rich axial-plane pairs, and every matched cell has
\(t^{3-o(1)}\) representations.  In \(N\)-notation these scales are
\[
N^{1/5-o(1)},\qquad
N^{2/45-\varepsilon/5-o(1)},\qquad
N^{3/5-o(1)}.
\]

The key new geometric observation is that all reverse circles with
one fixed signed centre coordinate \(A\) have collinear centres and
are converted to distinct lines by
\[
(u,z)\longmapsto
\left(z,(u-A)^2+z^2\right).
\]
The resulting fixed-column Szemerédi--Trotter estimate, combined with
a second dyadic decomposition by signed parameter-line fibres and a
global target-point capacity bound, excludes the hub alternative for
every fixed \(\kappa<2/9\).

Two independent reconstructions return **PASS**.  An exact exponent
ledger survives at \(\kappa=2/9\); consequently the endpoint itself
is not excluded.

## Main files

- `route_b/COLLINEAR_CENTER_LINEARIZATION_THEOREM.md` — strongest
  theorem and complete \(2/9\) proof.
- `route_b/COLLINEAR_CENTER_LINEARIZATION_INDEPENDENT_AUDIT.md` —
  first independent reconstruction.
- `route_d/TWO_NINTHS_INDEPENDENT_AUDIT.md` — second independent
  reconstruction, including a separate audit of all error terms.
- `route_d/CROSS_HEIGHT_ENERGY_AND_EUCLIDEAN_BARRIER.md` — exact
  cross-height localization at the live endpoint.
- `route_d/TWO_NINTHS_NEXT_TARGET.md` — the \(1/18\) cross-energy
  saving floor and exact saving-to-threshold conversions.
- `route_e/CONDITIONAL_JOINT_ENDPOINT_THEOREM.md` — a normalized
  joint ST/service saving and its exact \(\delta/18\) payoff.
- `route_f/PAPER_READINESS_RED_TEAM.md` — independent submission-risk
  review and a clean conditional main-theorem statement.
- `route_h/SELF_CONTAINED_CONDITIONAL_THEOREM.md` — one continuous
  proof with the critical pair-codegree and cell cap exposed as
  hypotheses, with no internal campaign terminology.
- `route_a/FOUR_PLANE_MATCHING_COEFFICIENT_AUDIT.md` — proof that the
  matching branch alone does not force numerical coefficient
  diversity.
- `route_c/SIX_COPRIME_CYCLOTOMIC_FIBRE_ESCAPE_THEOREM.md` — a clean
  arithmetic structured-family theorem with exact threshold
  \(\gcd(m,6)=1\).
- `CLAIM_LEDGER.md` — proved/open/false claim boundary.
- `LITERATURE_AND_PRIORITY_AUDIT.md` — current baseline and targeted
  novelty audit.
- `FINAL_REPORT.md` — campaign synthesis and publication assessment.

## Verification

Run

```bash
pytest -q data/research_open/erdos1083_two_hour_q1_attack_2026-07-30
git diff --check
```

The finite programs are exact falsification and exponent
certificates.  They do not replace the all-parameter written proofs.

## Publication boundary

The \(2/9\) theorem is the only result in this package with a credible
route to a substantial discrete-geometry paper.  It is not yet
defensible as a Chinese Academy Q1 result by itself: the global
distance exponent is unchanged, the conclusion is an intermediate
inverse-structure theorem, and priority has received only a targeted
rather than exhaustive audit.

The shortest plausible route to a high-tier result is a power-saving
incompatibility theorem for the simultaneous \(2/9\)-endpoint
near-extremizers.  Any fixed saving at that node would move the
matching exponent above \(2/9\); a further theorem converting the
richer matching into more than \(N^{3/5}\) distances would constitute
the desired global breakthrough.

The precise joint target is now
\[
RNu^4
\le
t^{-\delta+o(1)}MQ(ML)^2.
\]
If this holds uniformly for some fixed \(\delta>0\), the audited
structural threshold becomes \(2/9+\delta/18\).  Target service alone
cannot supply the saving: Route E gives an exact finite Euclidean
parameter model saturating that capacity inequality.
