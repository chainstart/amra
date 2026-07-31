# Paper-readiness red team: Route B and the \(2/9\) theorem

Date: 2026-07-30
Audit stance: independent referee-style review; no existing artifact was edited.

## 0. Executive verdict

\[
\boxed{\text{The strict }\kappa<2/9\text{ hub-exclusion argument is mathematically credible.}}
\]

\[
\boxed{\text{The present Route B directory is not a self-contained paper or a Q1-ready submission.}}
\]

The distinction is essential:

| Question | Red-team answer |
|---|---|
| Is the fixed-\(A\) circle-to-line lemma correct? | **Yes.** It is an elementary two-to-one parabolic lift followed by Szemerédi--Trotter. |
| Does the recorded scalar argument exclude the Euclidean hub for every fixed \(\kappa<2/9\)? | **Yes, conditional on the inherited axial-plane, codegree, matching-or-hub, and point--circle inputs.** No new exponent gap was found. |
| Is the endpoint \(\kappa=2/9\) proved? | **No.** The endpoint ledger satisfies every scalar inequality used. |
| Does Route B improve \(f_3(N)\gg N^{3/5}\)? | **No.** It proves an intermediate rich-matching conclusion only. |
| Is the \(2/9\) result already a stand-alone theorem in the present directory? | **No.** Its main hypotheses and the matching implication are inherited from files outside this two-hour package. |
| Is there a potentially publishable theorem after consolidation? | **Yes.** The natural unit is a conditional axial-plane distance-energy inverse theorem, stated explicitly in Section 2 below. |
| Is that minimum unit, without a further application, defensibly Q1-level? | **No.** It is better viewed as a specialized structural note or as the main technical theorem inside a larger paper. |
| Is priority certified? | **No.** The current search is informative but not exhaustive, and the parabolic lift itself is not a plausible novelty claim. |

The strongest defensible present wording is:

> Under a critical axial-plane distance-codegree hypothesis, every
> sufficiently large real Euclidean configuration has many distance
> labels supported on rich plane-pair matchings of exponent
> \(2/9-\varepsilon\).

It is not defensible to describe the work as a solution of Erdős #1083,
an improvement of the \(3/5\) exponent, an endpoint \(2/9\) theorem, or
an already established Q1 result.

## 1. Scope and evidence boundary

The technical review covered:

- `route_b/TANGENT_LABEL_RICH_LINE_HUB_THEOREM.md`;
- `route_b/COLLINEAR_CENTER_LINEARIZATION_THEOREM.md`;
- the three Route B independent audits;
- `route_d/TWO_NINTHS_INDEPENDENT_AUDIT.md`;
- the exact verifiers and tests for the tangent--label and \(2/9\)
  ledgers;
- the upstream
  `HIGH_CODEGREE_MATCHING_OR_HUB_THEOREM.md`,
  `EUCLIDEAN_HUB_INCIDENCE_EXPANSION_THEOREM.md`, and their audits in
  `opg_erdos_eight_hour_campaign_2026-07-30/erdos1083/geometric/`;
- the upstream forced-codegree argument in
  `ANGULAR_STARVATION_BRANCH_ATTACK.md`;
- the package claim and literature ledgers.

A read-only run using
`PYTHONDONTWRITEBYTECODE=1` and with the pytest cache disabled returned

```text
14 passed
```

for the three directly relevant test files.  These certificates check
finite geometry and exponent arithmetic; they do not replace the
all-parameter proofs or certify literature priority.

## 2. Clear theorem statement for a paper

The current prose should not advertise “Route B, stage 4” as the main
theorem.  The following is the cleanest stand-alone mathematical claim
actually supported by the combined chain.

### Proposed main theorem (critical axial distance energy forces rich matchings)

Let \(t\to\infty\).  For every \(t\), let \(\mathcal A_t\) be a set of
axial planes through one fixed line in \(\mathbb R^3\), indexed modulo
\(\pi\), and let
\[
P_\alpha\subset \Pi_\alpha\setminus\mathfrak a
\qquad(\alpha\in\mathcal A_t)
\]
be finite off-axis point sets.  Assume
\[
|\mathcal A_t|=t^{1+o(1)},\qquad
|P_\alpha|\le t^{3+o(1)},\qquad
|\Delta^2(P)|\le t^{3+o(1)},
\]
where \(P=\bigcup_{\alpha\in\mathcal A_t}P_\alpha\).

For a non-equal, nonperpendicular unordered plane pair
\(e=\{\alpha,\beta\}\) and a squared-distance label
\(d\in\Delta^2(P)\), define
\[
W_{e,d}
=
\bigl|\{(p,q)\in P_\alpha\times P_\beta:
|p-q|^2=d\}\bigr|.
\]
Assume the cell cap
\[
W_{e,d}\le t^{4+o(1)}
\]
and the critical cross-plane distance codegree
\[
\sum_d
\left[
\left(\sum_e W_{e,d}\right)^2
-\sum_e W_{e,d}^2
\right]
\ge t^{13-o(1)}.
\tag{A}
\]

Then, for every fixed \(0<\varepsilon<2/9\), there is a set
\(\mathcal D'\subseteq\Delta^2(P)\) of
\[
|\mathcal D'|\ge t^{1-o(1)}
\]
labels such that, for every \(d\in\mathcal D'\), the graph on
\(\mathcal A_t\) whose rich edges satisfy
\[
W_{e,d}\ge t^{3-o(1)}
\]
contains a matching of size
\[
\boxed{t^{\,2/9-\varepsilon-o(1)}}.
\]

All \(o(1)\) terms are to be made uniform along the configuration
sequence, with their dependence on the fixed \(\varepsilon\) stated.

### Exact claim boundary

This theorem is strict below \(2/9\).  It neither excludes the endpoint
nor asserts that the endpoint exponent ledger is geometrically
realizable.  It also does not imply a lower bound
\(|\Delta(P)|\ge |P|^{3/5+\delta}\).

### Why this is the right statement

It removes internal language such as “critical node”, “Route B”, and
“the inherited hub”, and exposes the actual input and output.  It also
separates two possible papers:

1. a conditional inverse/structure theorem beginning with (A); and
2. a full Erdős #1083 reduction paper that additionally proves how a
   general near-extremal point set reaches the axial hypotheses and
   codegree (A).

The second paper has a substantially stronger claim, but its complete
reduction is not contained in the two-hour directory.

## 3. Technical red-team reconstruction

### 3.1 What survives

The fixed-\(A\) geometry is exact.  For
\[
\Phi_A(u,z)=\bigl(z,(u-A)^2+z^2\bigr),
\]
each image has at most two source preimages, and
\[
(u-A)^2+(z-w)^2=\rho^2
\]
is equivalent to
\[
Y=2wZ+(\rho^2-w^2).
\]
For fixed signed \(A\), distinct normalized positive-radius circles
give distinct lines.  Hence
\[
I(P_\alpha,\mathcal C_A)
\ll Q^{2/3}N_A^{2/3}+Q+N_A,
\]
and summing over \(R\) signed centre coordinates gives
\[
I(P_\alpha,\mathcal C)
\ll Q^{2/3}R^{1/3}N^{2/3}+RQ+N.
\tag{B}
\]
The signs \(A\) and \(-A\) are correctly separated in (B).

The secondary dyadic decomposition is also legitimate.  Once source
richness \(s(C)\) and producing multiplicity \(\mu(C)\) are dyadically
fixed, further dyadic selection by the number \(t^{h+o(1)}\) of circles
above a signed parameter fibre \((A,\rho^2)\) loses only a
subpolynomial factor.  If \(K=t^{c+o(1)}\) fibres and
\(N=t^{b+o(1)}\) circles survive, then
\[
b=c+h.
\]

The target-capacity step does not require the false auxiliary bound
\(R\le M\).  One signed fibre uses \(t^{h+m-o(1)}\) distinct target
points in the plane \(x=A\): within a circle the target is off-axis and
therefore determines its axial plane, while different circles have
different centre heights.  Choosing one fibre per active \(A\) gives
\[
r+h+m\le4+o(1).
\tag{C}
\]

The ordinary rich-line estimate gives
\[
c\le6-4\kappa-3m+o(1),
\tag{D}
\]
and the inherited arbitrary-circle incidence estimate, after excluding
its other three terms in the claimed range, gives
\[
11a+2b\le18+o(1),
\qquad
m\ge\frac{5-15\kappa}{2}-o(1).
\tag{E}
\]
Using (B)--(E), the only remaining fixed-\(A\) Szemerédi--Trotter
branch yields
\[
m\le\frac{1+3\kappa}{2}+o(1).
\tag{F}
\]
Equations (E) and (F) are incompatible for every fixed
\(\kappa<2/9\), and meet exactly at \(\kappa=2/9\).

### 3.2 What does not survive as a stronger claim

- The scalar proof does not exclude \(\kappa=2/9\).
- The endpoint table is an exponent-feasibility certificate, not a
  Euclidean example.
- The linearization lemma by itself is elementary and should not be
  presented as the novelty.
- The rich matching does not preserve enough endpoint compatibility to
  supply a new global distinct-distance exponent.
- Tests confirm the formulas used by the proof but cannot certify the
  upstream near-extremal reduction, priority, or journal significance.

### 3.3 No newly found fatal mathematical gap, but a fatal packaging gap

Within the explicit conditional setup, no new proof-breaking algebraic
or incidence-theoretic error was found.  The fatal issue for a referee
is instead that the present directory does not contain the complete
theorem chain it claims to apply.

| Required component | Location | Status in the two-hour package |
|---|---|---|
| Fixed-\(A\) lift and summed incidence bound | `route_b/COLLINEAR_CENTER_LINEARIZATION_THEOREM.md` | Present |
| Tangent--label identity and multiplicity-to-richness map | `route_b/TANGENT_LABEL_RICH_LINE_HUB_THEOREM.md` | Present, but begins from an inherited setup |
| General planar point--circle incidence theorem | External literature | Cited indirectly; original source chain should be repaired |
| Critical cross-plane codegree | Earlier eight-hour campaign | Not present |
| Cell cap and removal of exceptional plane pairs | Earlier eight-hour campaign | Not present |
| Parameterized matching-or-hub theorem | Earlier eight-hour campaign | Not present |
| Derivation of the axial critical node from a general #1083 configuration | Earlier proof tree, itself stated as inherited in places | Not closed in this directory |
| One unified statement with uniform loss parameters | Nowhere | Missing |

Therefore the local claim-ledger description “PROVED” is acceptable
only as a repository-wide status label.  It is not yet a
self-contained manuscript proof.

## 4. Three referee lenses

### Reviewer 1 — technical soundness

The conditional hub-exclusion argument is the strongest aspect of the
work.  The lift, line richness, secondary fibre decomposition, target
distinctness, and all three branches of (B) survive reconstruction.
The strictness of the \(2/9\) threshold is correctly stated.

The present submission form would nevertheless receive a major
technical objection: its main corollary calls external, internally
named theorems without restating or proving their exact hypotheses.
The author must supply one continuous proof with quantitative
\(\varepsilon\)-bookkeeping.  Until then, the manuscript is not
independently checkable from the submitted text.

### Reviewer 2 — originality and significance

The potentially original contribution is the integration of several
weighted incidence and capacity constraints to obtain the exponent
\(2/9\), not the circle-to-line lift.  The available literature search
did not locate the exact conclusion, but a negative keyword search is
not a priority proof.

Significance is currently limited.  The global \(3/5\) exponent is
unchanged, the result applies at an intermediate axial critical branch,
and the endpoint remains open to the scalar method.  A specialist may
find the inverse structure useful, but the current manuscript does not
yet show a consequence commensurate with a top-quartile claim.

### Reviewer 3 — readability and paper architecture

The repository narrative is not suitable manuscript exposition.
“Route B”, “stage 4”, “hub”, “selected labels”, \(t\), \(M\), \(Q\),
\(L\), \(W\), and multiple unrelated uses of \(b\) are understandable
only after reading several campaign logs.  A reader cannot tell from
the opening theorem which assumptions are geometric facts, which are
near-extremal hypotheses, and which were proved earlier.

The paper needs one notation table, one dependency diagram, the theorem
in Section 2, and a proof ordered by logical dependence rather than
chronology of discovery.

### Cross-review synthesis

All three lenses agree that the strict conditional mathematics is
credible and that the current artifact is not submission-ready.  The
main disagreement a real referee panel might have is only how much
value to assign to an intermediate inverse theorem with no improved
distance exponent.  That uncertainty must be resolved by a stronger
application or by broadening the inverse theorem beyond this one proof
tree.

## 5. Q1-critical gaps

The following are not cosmetic requests.  Items Q1-1 through Q1-4 are
submission blockers for any claim that this is already an independent
Q1 theorem.

### Q1-1. Close the theorem dependency chain

Include, in the submitted manuscript, full statements and proofs of:

1. the nonexceptional plane-pair cell cap;
2. the critical cross-plane codegree;
3. the weighted matching-or-hub extraction;
4. the tangent--label identity and circle merging;
5. the fixed-\(A\) hub exclusion;
6. the rich-matching corollary.

Alternatively, state the codegree (A) as an explicit hypothesis and
submit only a conditional inverse theorem.  The manuscript may not
refer to a missing `EUCLIDEAN_HUB_INCIDENCE_EXPANSION_THEOREM.md` or to
an undefined “critical node”.

### Q1-2. Add a consequence with genuine field-level significance

At least one of the following is needed for a credible Q1 case:

- a fixed \(\delta>0\) with
  \(f_3(N)\gg N^{3/5+\delta-o(1)}\);
- an endpoint or stability theorem that converts the rich matching into
  distance expansion;
- a natural inverse theorem applying to a substantially broader class
  of Euclidean incidence configurations, with at least one additional
  application;
- a classification of near-extremizers that rules out simultaneous
  near-equality in the point--circle, tangent--label, and target-capacity
  steps.

Absent one of these, the \(2/9\) theorem is a respectable structural
lemma or specialist note, not a demonstrated Q1-scale result.

### Q1-3. Certify novelty at theorem level

The priority audit must compare the complete proposed theorem, not just
the internal terms “reverse circle” or “tangent-label”.  Required search
lanes include:

- higher-dimensional and bipartite distinct distances;
- few-distance inverse theorems;
- points and circles with collinear centres;
- Cartesian-product point--line incidence structure;
- weighted rich-line and energy decompositions;
- coaxial, perpendicular-bisector, and axial-plane formulations.

MathSciNet and zbMATH formula/author searches and direct bibliography
chasing are still required.  The manuscript must say precisely which
step is new relative to each closest result.

### Q1-4. Replace \(o(1)\)-ledger prose by a journal theorem

Use either explicit \(\eta\)-losses or one declared family of error
functions.  State:

- the order of quantifiers in \(t,\varepsilon,\eta\);
- which constants depend on \(\varepsilon\);
- the exact richness threshold;
- ordered versus unordered plane-pair conventions;
- the treatment of equal and perpendicular pairs;
- the off-axis deletion and its loss;
- the range \(0<\varepsilon<2/9\).

The present calculations strongly suggest this can be done, but it has
not yet been written.

### Q1-5. Repair the source basis

The \(6/11,9/11\) planar point--circle estimate is currently cited via
a later paper that describes the older planar theorem.  Cite the
original incidence/cutting sources as well as the later statement used.
The 2024/2025 removal of a logarithmic loss must be acknowledged and
its effect on the ledger stated explicitly.  It appears to change only
subpolynomial factors here, not the \(2/9\) power threshold, but that
comparison belongs in the paper.

### Q1-6. Build a conventional manuscript and independent proof audit

Provide:

- abstract, introduction, related work, main theorem, and proof;
- a stable notation table and dependency diagram;
- a section explaining why \(2/9\), rather than the elementary lift, is
  the contribution;
- a clearly labelled endpoint obstruction;
- a human proof audit independent of the exponent scripts;
- archived source and exact version hashes for the submitted proof.

## 6. Minimum publishable unit

### Minimum specialist submission

The smallest coherent submission is **not**
`COLLINEAR_CENTER_LINEARIZATION_THEOREM.md` alone.  It is:

1. the critical axial codegree theorem, or assumption (A);
2. the finite weighted matching-or-hub lemma;
3. the tangent--label encoding;
4. the fixed-\(A\) linearization and target-capacity argument;
5. the strict \(2/9-\varepsilon\) rich-matching theorem;
6. the endpoint feasibility ledger;
7. a serious prior-art section.

This would make a focused paper on an inverse theorem for near-critical
three-dimensional distance energy.  Route C and the unrelated barrier
files should not be inserted unless they become applications of the
same main theorem.

### Minimum Q1 submission

The above specialist unit plus one of the significance upgrades in
Q1-2.  The cleanest route is a theorem that turns the resulting
matching cells into a fixed power saving over \(3/5\).  The next-best
route is a broadly stated stability/inverse theorem with multiple
applications and a complete near-equality analysis.

### Go/no-go rule

- **Go for a specialist preprint after consolidation and priority
  audit.**
- **No-go for a Q1 claim in the present form.**
- **No-go for any title or abstract implying that Erdős #1083 or the
  \(2/9\) endpoint has been solved.**

## 7. Primary-source literature check

This was a bounded web/arXiv check, not an exhaustive priority search.
No exact published theorem matching the statement in Section 2 was
located.  That negative result must not be represented as proof of
priority.

Primary sources that a submission must compare directly include:

1. Solymosi and Vu,
   [*Distinct distances in high dimensional homogeneous
   sets*](https://doi.org/10.1007/s00493-008-2099-1), for the
   higher-dimensional distance baseline and reduction context.
2. Guth and Katz,
   [*On the Erdős distinct distances problem in the
   plane*](https://arxiv.org/abs/1011.4105), for the planar
   distinct-distance input used elsewhere in the Route B chain.
3. Bardwell-Evans and Sheffer,
   [*A reduction for the distinct distances problem in
   \(\mathbb R^d\)*](https://arxiv.org/abs/1705.10963), for the closest
   general higher-dimensional reduction framework.
4. Sharir, Sheffer, and Zahl,
   [*Improved bounds for incidences between points and
   circles*](https://arxiv.org/abs/1208.0053), which explicitly records
   the planar \(m^{6/11}n^{9/11}\) incidence term used in the proof and
   identifies its earlier source chain.
5. Janzer, Janzer, Methuku, and Tardos,
   [*Tight bounds for intersection-reverse sequences, edge-ordered
   graphs, and applications*](https://arxiv.org/abs/2411.07188), for
   the recent removal of the logarithmic loss in the pseudo-circle
   cutting input and its point--circle incidence consequences.
6. Sheffer and Silier,
   [*A structural Szemerédi--Trotter theorem for Cartesian
   products*](https://arxiv.org/abs/2110.09692), for structural
   near-extremal point--line incidence phenomena, including
   additive/multiplicative structure.
7. Dasu, Sheffer, and Shen,
   [*Structural Szemerédi--Trotter for lattices and their
   generalizations*](https://arxiv.org/abs/2310.00191), for a closer
   comparison with lattice and Cartesian-product near-extremizers.
8. Mathialagan and Sheffer,
   [*Distinct distances on non-ruled surfaces and between
   circles*](https://arxiv.org/abs/2011.08098), for the classification
   of small-distance configurations between two circles and the
   corresponding bipartite expansion theorem.

The current evidence supports only the cautious sentence:

> The integrated weighted axial-plane argument and its
> \(2/9-\varepsilon\) matching exponent were not found in this bounded
> primary-source search; priority remains uncertified.

## 8. Final risk / unsupported-claim register

| Proposed claim | Safe? | Required correction |
|---|---|---|
| “The fixed-\(A\) parabolic lift is new.” | **No** | Present it as an elementary device unless a direct priority audit proves otherwise. |
| “The Euclidean hub is excluded at \(2/9\).” | **No** | Say “for every fixed \(\kappa<2/9\)”. |
| “A \(2/9-\varepsilon\) structural matching theorem follows from the full repository chain.” | **Yes, conditionally credible** | Publish one self-contained proof with explicit hypotheses and uniform losses. |
| “Route B is self-contained.” | **No** | Import or restate the upstream codegree and matching-or-hub chain. |
| “The work improves the three-dimensional distinct-distance exponent.” | **No** | State explicitly that \(3/5\) is unchanged. |
| “Priority is established.” | **No** | Complete database and formula-level comparison. |
| “The present result is Q1-ready.” | **No** | Close Q1-1 through Q1-4 and add a Q1-2 significance upgrade. |

The red-team bottom line is therefore:

\[
\boxed{
\begin{array}{c}
\text{conditional strict-range theorem: credible},\\
\text{stand-alone manuscript: not yet},\\
\text{Q1-ready result: no}.
\end{array}}
\]
