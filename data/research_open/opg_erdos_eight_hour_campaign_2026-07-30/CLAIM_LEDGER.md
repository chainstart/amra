# Claim ledger

Date: 2026-07-30

This ledger separates proved statements, conditional reductions, finite
certificates, and open targets.  `PASS` means that the human proof has an
independent reconstruction or red-team audit; it does not mean that a
journal has established priority or accepted the work.

## 1. OPG-1757

| Claim | Status | Scope and evidence |
|---|---|---|
| Explicit positive top Newton window \(0\le d\le k^{1/8}\) | **PROVED / PASS** | Unbounded theorem with author and independent exact-profile verifiers; it does not cover the linear-width middle. |
| Explicit bottom window \(0\le r\le2^{-28}\sqrt{k}\) for \(k\ge9\cdot2^{58}\) | **PROVED / PASS** | Uniform quantitative theorem with independent red-team audit. |
| Every fixed top depth is eventually positive | **PROVED / PASS** | Exact Lagrange-profile asymptotics; separate from the explicit growing window. |
| Every fixed ordinary-symbol rank is computable by a finite symbolic recurrence | **PROVED / PASS** | Starts from the exact Lagrange profiles and computes all depths at once; no interpolation in depth. |
| Explicit ordinary symbols \(\beta_{d,r}\) through \(r=8\) | **PROVED / PASS** | Ranks \(0,\ldots,8\) have exact all-\(d\) polynomial formulas.  Ranks seven and eight are uniquely reconstructed from the proved degree bounds using respectively 22 and 25 exact profile values plus four unused depths.  Independent reconstructions use different depth nodes, primitive finite profiles, and no author coefficient tables. |
| Alternating signs and normalized Newton inequalities through rank eight | **PROVED / PASS** | In particular \(\beta_{d,8}>0\) and \(a_{d,7}^2>a_{d,6}a_{d,8}\) for every \(d\ge8\); the independent shifted certificates have respectively 25 and 44 positive coefficients. |
| Uniform \(C=3\) weighted-symbol bound through rank eight | **PROVED / PASS** | Exact all-depth consequence of the eight explicit nontrivial ranks; not a bound at arbitrary rank. |
| First eight long-recurrence bands \(\gamma_0,\ldots,\gamma_7\) | **PROVED / PASS** | Exact positive polynomials on every admissible depth.  The eighth band \(\gamma_{d,7}>0\) for \(d\ge15\) is independently reconstructed by a separate Faulhaber/Newton triangle; all 24 coefficients after \(d=u+15\) are positive. |
| Raw all-rank pole bound and four-layer marked second-difference cancellation | **PROVED / PASS** | Eleven Bell configurations, the \(\Gamma_1\) correction, and the exceptional-profile cancellation are symbolic identities in the rank. |
| Complementary \(x=1\) endpoint localization | **PROVED / PASS** | A genuine complement-length hypergeometric identity and separate exceptional formula replace the invalid trial reindexing.  Two independent red teams checked the exact normalization, saddle selection, rational-branch continuation, and endpoint regularity. |
| \(B_r(t)=N_r(t)/(1-t)^{3r+1}\), \(\deg N_r\le4r\), hence \(\deg_d\beta_{d,r}\le3r\) | **PROVED / PASS** | The endpoint, marked low ranks, all-rank Bell cancellation, central propagation, infinity growth, and removable \(t^4\) have all passed audit. |
| Exact degree \(\deg_d\beta_{d,r}=3r\) and alternating leading sign | **PROVED / PASS** | A defect-four symbolic identity gives the first surviving marked Laurent layer; a strict log-convex convolution bound proves the sign.  The complete Bell support, low-rank boundary, convolution direction, and constants pass independent audit. |
| Falling-triangle factors for all ranks | **PROVED / PASS** | For every \(j\), \(\deg\mathfrak h_j=3j\), its leading sign is \((-1)^j\), and \(\prod_{m=j}^{2j-1}(d-m)\mid\mathfrak h_j(d)\); the residual has exact degree \(2j\).  The degree separation and every use of the polynomial extension pass independent audit. |
| Long-recurrence exact degree and positive leading layer | **PROVED / PASS** | For every \(q\), \(\deg\mathfrak g_q=3q+2\) and its leading coefficient is positive; for \(q\ge1\), division by the forced factor \(d-2q\) leaves exact degree \(3q+1\) with positive leading coefficient.  The proof combines the exact logarithmic reduction with a dominant-positive-zero/Jensen argument; two independent audits checked every constant and the finite/analytic seam. |
| Full-domain positivity of every fixed long-recurrence band is finitely decidable | **PROVED / PASS** | For an input \(q\), exact finite-profile arithmetic constructs \(\gamma_{d,q}\); the all-rank degree/positive-leading theorem and an exact Cauchy root bound reduce its sign on every integer \(d\ge2q+1\) to finitely many rational evaluations.  A negative result returns an exact counterexample.  This is an effective per-\(q\) decision theorem, not a proof that the answer is positive for every \(q\). |
| Ordinary-symbol real-rootedness | **FINITE EVIDENCE ONLY** | Exact roots/interlacing have been certified through the recorded finite range; no all-depth real-root theorem is claimed. |
| OPG-1757 for all graphs | **OPEN** | Neither the complete-split middle Newton region nor the general graph conjecture has been closed. |

Core files are in
`opg1757/top_newton_tail_2026-07-30/`, especially
`ORDINARY_RANK_SIX_SYMBOL_AND_NEWTON_THEOREM.md`,
`ORDINARY_SIXTH_LONG_RECURRENCE_BAND_THEOREM.md`,
`ORDINARY_RANK_SEVEN_AND_SEVENTH_BAND_THEOREM.md`,
`ORDINARY_RANK_EIGHT_AND_EIGHTH_BAND_THEOREM.md`,
`ALL_RANK_SADDLE_POLE_VALUATION_ATTACK_2026-07-30.md`,
`COMPLEMENTARY_ENDPOINT_LOCALIZATION_LEMMA.md`, and
`ALL_RANK_ORDINARY_SYMBOL_DEGREE_THEOREM.md`, together with
`ALL_FIXED_BAND_POSITIVITY_DECIDABILITY_COROLLARY.md`.

## 2. Erdős #1083

| Claim | Status | Scope and evidence |
|---|---|---|
| Forced cross-plane distance codegree \(\mathfrak C_{\rm plane}\ge N^{13/5-o(1)}\) at the critical branch | **PROVED / PASS** | Uses global distance energy and a two-degree-of-freedom circle-incidence bound. |
| High-codegree matching-or-hub extraction | **PROVED / PASS** | For every fixed \(0<\kappa<1\), the critical ledger forces either \(t^{1-o(1)}\) labels with \(t^{\kappa-o(1)}\) disjoint rich plane pairs per label, or one plane carrying \(t^{5-\kappa-o(1)}\) rich mass for each of \(t^{2-2\kappa-o(1)}\) labels.  A quadratic finite-field tensor saturates the ledger yet has no \(K_{3,2}\). |
| Euclidean hub incidence expansion | **PROVED / PASS** | Reverse-circle injectivity and the planar point--circle incidence bound exclude the hub alternative for every fixed \(\kappa<1/5\).  Hence, for every fixed \(\varepsilon>0\), at least \(t^{1-o(1)}\) labels support a \(t^{1/5-\varepsilon-o(1)}\) matching of rich plane pairs.  A weighted dyadic decomposition of merged circle multiplicities strengthens the surviving-hub conclusion to \(\mu\ge t^{(5-15\kappa)/2-o(1)}\) for \(\kappa<1/3\); the former \(/11\) exponent was only the coarse maximum-weight bound.  Independent red-team and exact exponent audits pass; this is a structure theorem, not a \(3/5\)-exponent improvement. |
| One repeated circle-axis chart alone forces superlinear distance expansion | **FALSE / PASS** | The chart has an exact orthogonal circle--axis normal form.  It forces \(\mu\) target planes, at least \(\lceil\mu/2\rceil\) labels, and \(\mu-1\) target--target distances, but, for every even \(\mu\), a regular \(n\)-gon plus a symmetric arithmetic progression of \(\mu\) axis points has \(n\mu\) cross representations and only \(O(n+\mu)\) total distances.  Independent symbolic and full-coordinate audits pass. |
| Two concentric repeated circle-axis charts with different radii alone force superlinear distance expansion | **FALSE / PASS** | For \(\mu=2m\), two aligned regular \(n\)-gons of different radii and one common odd arithmetic progression on their perpendicular axis realize \(4mn\) repeated-circle representations but at most \(3\lfloor n/2\rfloor+4m\) total squared distances.  For \(K\) concentric radii the corresponding bound is \(O(K^2n+Km+m)\).  Independent checks cover all four general cross formulas, every distance block, and the fixed-\(K\) ledger.  This excludes radius diversity alone and gives no \(3/5\)-exponent gain. |
| Two nonaligned retained active circles force bipartite expansion | **KNOWN THEOREM BRIDGE / PASS** | Mathialagan--Sheffer's two-circle theorem gives \(\Omega(\min\{s_1^{2/3}s_2^{2/3},s_1^2,s_2^2\})\) distances.  In axial-chart coordinates, aligned means \(s=0,\Delta w=0,A_1-A_2\cos\theta=0\).  Their other exception, perpendicular circles, would require \(A_1=A_2=0\), impossible for retained off-axis, nonperpendicular reverse circles.  The open campaign step is to extract two sufficiently incidence-rich nonaligned classes; the distance theorem itself is prior work. |
| Critical high-rich active-circle concentration | **PROVED / PASS** | For every fixed \(\eta>0\), all retained active circles in one hub plane with source incidence at least \(t^{9/4+\eta}\) are concentric.  Per-plane reverse-circle injectivity gives multiplicity at most \(M\), while distinct concentric circles have disjoint source sets, so their total weighted mass is at most \(MQ=t^{4+o(1)}=o(t^{7-3\kappa-o(1)})\) for every fixed \(\kappa<1\).  Zero-radius mass is also negligible.  Thus the principal hub mass lies on circles below the \(t^{9/4+\eta}\) richness threshold; this gives no exponent gain by itself. |
| Current moderate-rich constraints force a contradiction for \(1/5\le\kappa<1/3\) | **FALSE / PASS (ABSTRACT LEDGER BARRIER)** | The exact assignment \(a=1-\kappa\), \(b=(7+11\kappa)/2\), \(m=(5-15\kappa)/2\) simultaneously saturates \(N\mu=MQL\), \(N\mu t^a=LH\), and the weighted \(6/11,9/11\) incidence term, while satisfying \(\mu\le M\), the high-rich cutoff, every pairwise Mathialagan--Sheffer exponent constraint, and fixed-plane slot capacity.  This is not a Euclidean realization; it proves that the saved aggregate inequalities alone cannot close the hub branch. |
| Weighted ruled-column and rational-chord layer-cake terminals | **PROVED / PASS** | Convert a sufficiently large arithmetic chart into distinct-distance expansion; the required chart extraction is not inherited automatically. |
| Fixed and slowly growing number-field two-square terminals | **PROVED / PASS** | Exact divisor/unit bounds with all hypotheses recorded; they do not cover unrestricted growing cyclotomic degree. |
| Complete prime-cyclotomic tensor escape | **PROVED / PASS** | Radius-dependent height sets are allowed; complete \(p\)-gons force a linear number of distances. |
| Partial prime-cyclotomic fibre escape | **PROVED / PASS** | Angular support may vary arbitrarily at every height.  If all fibres have size \(S\le(p+1)/2\), then \(|\Delta^2(P)|\ge(1-1/S)|P|\). |
| Base-field extension of partial fibre escape | **PROVED / PASS** | Rational data may be replaced by a real field \(K\) over which \(\Phi_p\) is irreducible.  For each fixed number field this holds for all but finitely many \(p\). |
| Composite-order version with the same constant | **FALSE** | A square inside \(\mathbb Z/8\mathbb Z\) and a triangle inside \(\mathbb Z/9\mathbb Z\) are explicit counterexamples; a valid extension needs both a Kneser stabilizer term and chord-character independence. |
| Abstract growing-cyclotomic tensor excluded by energy/Galois ledgers alone | **FALSE** | An abstract tensor saturates the critical aggregate ledger.  The partial-fibre theorem excludes a large natural Euclidean realization, not every realization. |
| Unconditional improvement \(f_3(N)\ge N^{3/5+\varepsilon-o(1)}\) | **OPEN** | The missing step remains a Euclidean coefficient/extraction theorem turning cross-plane label reuse into an expandable chart or direct distance growth. |

Core files are in `erdos1083/geometric/`, especially
`ANGULAR_STARVATION_BRANCH_ATTACK.md`,
`EUCLIDEAN_HUB_INCIDENCE_EXPANSION_THEOREM.md`,
`COSINE_RADIAL_REPEATED_CIRCLE_BARRIER.md`,
`TWO_CIRCLE_AXIS_CHART_BARRIER.md`,
`MATHIALAGAN_SHEFFER_CIRCLE_CLASSIFICATION_BRIDGE.md`,
`HIGH_RICH_CIRCLE_CONCENTRATION_COROLLARY.md`,
`WEIGHTED_REVERSE_CIRCLE_DYADIC_REFINEMENT.md`,
`MODERATE_RICH_AGGREGATION_BARRIER.md`,
`WEIGHTED_RULED_COLUMN_LAYER_CAKE_THEOREM.md`,
`CROSS_PLANE_GALOIS_ORBIT_TRICHOTOMY.md`, and
`PARTIAL_CYCLOTOMIC_FIBRE_ESCAPE_THEOREM.md`.

## 3. Publication boundary

The OPG ordinary-symbol package is a genuine manuscript nucleus: it has
several unbounded theorems, explicit rank-eight structure, independent
certificates, an audited all-rank exact-degree/leading-sign theorem, and
an all-rank exact-degree/positive-leading theorem for the long
recurrence.
A strong-journal submission is now materially credible if the work is
recast as one conceptual theorem rather than a sequence of computations
and the remaining priority audit finds no overlap.  This still does not
solve OPG-1757.

The Erdős package contains useful structural and exclusion theorems, but
it has not improved the \(3/5\) exponent.  It should not presently be
marketed as a stand-alone solution paper.  Its strongest role is a
rigorous proof-tree reduction identifying and excluding broad candidate
obstructions.

No quartile claim follows from this ledger.  Priority remains subject to
the source audit in `LITERATURE_AND_NOVELTY_AUDIT.md`, a complete author
comparison, and conventional peer review.
