# Same-model cross-audit of the adaptive actual builder

## Verdict

**PASS.**  I independently reconstructed the dependency chain from the
actual real scales in `formal/ParametricRanges.lean` to
`ParametricLarge.parametric_frontier_adaptive`.  The final theorem is not
merely the earlier logarithmic parameter certificate: it uses the actual
least stopping order, the actual positive real `lambda`, the pinned raw
Konyagin estimate, all four source ranges, and `main_of_rangePackage`.

This is a read-only, same-model cross-audit.  It is not an independent human
peer review, it does not establish novelty, and it does not independently
replay Lean.  I used the checked source plus the campaign's guarded build log,
axiom report, and recorded SHA-256.  I did not modify any author evidence or
formal source.

## 1. Actual-scale and stopping reconstruction

The relevant objects are genuinely defined on the real scales

\[
 U_r=k^{r+1}(\log k)^{-Q(2r-1)},\qquad
 V_r=k^{r+\theta}(\log k)^{Q(r-1)},
\]

\[
 Z_r=\max(nr!,V_r),\qquad
 \lambda_r=\left({Z_r\over nr!}\right)^{1/r}.
\]

The source proves the exact identities `lambda_r^r=Z_r/(nr!)`,
`lambda_r>=1`, and `nr!*lambda_r^r=Z_r`.  The logarithmic definitions are
then tied back to these real objects by explicit `log_adaptive*` lemmas.

`exists_min_adaptive_stopping_order` applies `Nat.find` to
`nr! <= U_r`.  Its hypotheses provide a reference order satisfying the
predicate and failure for orders `0,1`; hence the selected order satisfies
`2<=r<=R`, the upper stopping inequality at `r`, and strict failure at
`r-1`.  `adaptive_preceding_failure_log_lower` converts that strict failure
to the precise lower logarithmic inequality used later.  This checks the
existence, `r>=2`, `r<=R`, and minimality interface, including the boundary
case `r=2` where the predecessor is order one.

## 2. Selection-budget algebra

`adaptive_log_selection_budget` assumes

\[
 rM\le aK,\qquad 3Qa<1-\theta,
\]

plus the upper stopping inequality and the preceding lower inequality.  Its
conclusions have the correct directions:

* `V_r<=U_r` follows from
  `(1-theta)K-Q(3r-2)M>0`, bounded using `3Q rM`;
* `Z_r=max(logN,V_r)` lies between `V_r` and `U_r`;
* the two first raw terms have logarithms at most `-QM`;
* the selected scale satisfies
  `log(lambda)<=theta*K/r+3QM`.

`adaptive_actual_selection_budget` transports these statements back to the
real scales and retains both the exact mass equality and positivity of
`lambda`.  I found no reversal of a max inequality or loss of the strict
margin during that transport.

The remaining estimates are also connected to the selected actual order.
`adaptiveT3At_eventual` is uniform for every `r>=2` in the stated order and
logarithmic budgets.  `adaptive_additive_term_eventual` uses `r>=2` to
replace `theta/r` by `theta/2` and proves the additive `2r lambda` term is
`o(k^theta/log k)` for every fixed `theta>0`.  Thus the old special
`r=3` balanced-envelope obstruction is not silently reused.

## 3. Pinned raw estimate and actual large certificate

`large_card_raw_adaptive_at` is a direct specialization of the pinned
`konyagin_application`.  Its hypotheses are the actual ones needed here:
`lambda>=1`, `0<theta<1`, `k<n`, `r>=2`, and
`r<=k^(1-theta)/2`.  It does not assume a balanced lambda or
`nr!<=k^(r+theta)`.

`large_card_raw_adaptive_selected_at` substitutes
`adaptiveLambdaAt`; the exact mass identity turns the first two raw terms
into `adaptiveT1At` and `adaptiveT2At`.  The selected third and additive
budgets are then combined in `adaptive_bad_set_asymptotic_of_budgets`.

`hasAdaptiveLargeCertificateAt_of_parameters` supplies every hypothesis of
that raw estimate from:

1. reference-order admissibility;
2. exclusion of stopping orders zero and one;
3. least-order selection and predecessor failure;
4. actual selection budgets; and
5. uniform third-term and additive estimates.

`case_large_adaptive_at` compares the resulting bad-set count with the
abstract `PrimeIntervalInput(theta)` count and invokes the pinned finishing
lemma.  I found no missing handoff between the parameter core and the actual
large-range theorem.

## 4. Complete four-range builder

`adaptiveRangePackage_of_parameters` fills the exact four fields of
`ParametricRangePackage(theta,c)` with
`ParametricSmall.case_small`, `ParametricMed.case_medium`,
`ParametricML.case_mediumlarge`, and the new adaptive large case.
`adaptiveAnalyticParameters_of_wide` constructs the strict auxiliary
parameters for every

\[
 0<\theta<1,\qquad 0<c<(1-\theta)/3.
\]

The non-obvious second feasibility margin is sound: with
`b<(1-theta)/3`, one has
`2b<1-theta/2` exactly because `theta<1`, so a `q>1` can be chosen with
`2qb<1-theta/2`.

Consequently `parametricRangeBuilder_adaptive` is an actual
`PrimeIntervalInput(theta) -> ParametricRangePackage(theta,c)` builder.
`parametric_frontier_adaptive` passes that package to
`main_of_rangePackage`, which combines the four ranges and eventually embeds
the source interval `(k,k+3k^theta)` into `(k,2k)`.  The theorem statement is
therefore genuinely supported for the full conditional window
`0<theta<1`, not only by an abstract or uninstantiated parameter lemma.

## 5. Audit for leakage of the old `9/23` condition

**PASS.**  Occurrences of `9/23` in the file belong to the retained older
balanced-scale analysis.  The adaptive final chain does not invoke its
balanced large-case theorem.  The only reused reference-order lemma,
`r0Param_eventual_admissible_at`, requires positivity and `c<a<b`; the
adaptive wrapper adds its own `2Qb<=1-theta` margin and imports no
`theta>9/23` or `b<theta` premise.  The small, medium, and medium-large fields
used by the adaptive package assume only `0<theta<1` and the abstract prime
input.  Hence the formal conclusion that `9/23` was an artifact of the
specified balanced scale is supported.  This is not a no-go statement about
all other possible methods.

## 6. Unconditional specialization

**PASS, with a strict-endpoint qualification.**  The new general theorem is
conditional on `PrimeIntervalInput(theta)`.  The campaign's unconditional
input remains BHP at `theta=21/40`, and

\[
 {1-21/40\over3}={19\over120}.
\]

Thus the unconditional conclusion remains **every fixed
`0<c<19/120`**.  It neither includes the endpoint `c=19/120` nor improves
the unconditional constant.  The decision and decisive-lemma artifacts say
this correctly and do not claim that Erdos 451 is closed.

## 7. Evidence and axiom boundary

The evidence JSON and Markdown identify the actual final theorem and builder,
not only the parameter certificate.  Their recorded guarded replay is unit
`openmath-task-20260826-193041-222943.scope`, exit `0`, wall time `94.89s`,
peak RSS `7,106,780 KiB`, and swap `0`.  The recorded source SHA-256 is
`f53b140146ab60348880a0d6c15cd8dafe756e62bb1a6701a197ce6a5ff6ea1c`.
The axiom report for the adaptive builder and final theorem is exactly
`[propext, Classical.choice, Quot.sound]`, with no `bhp` or `sorryAx`;
`bhp` enters only when the abstract prime input is specialized
unconditionally.

No mathematical or artifact correction is required by this audit.
