# Complete variable-theta range builder

## Compiled theorem

`formal/ParametricRanges.lean` now proves the stronger
`ParametricLarge.parametric_frontier_adaptive`:

```text
0 < theta < 1
0 < c < (1-theta)/3
PrimeIntervalInput(theta)
----------------------------------------------------------
eventually, for every 2k < n <= exp(c log^2(k)/loglog(k)),
some prime p with k < p < 2k divides Pprod(k,n).
```

The companion theorem `parametricRangeBuilder_adaptive` constructs the exact
four-field `ParametricRangePackage theta c`.  Thus the conditional
`PI(theta)` theorem previously exposed only as an interface is now fully
formalized.

The adaptive proof is an actual real-scale construction, not only a
logarithmic parameter core.  For every

```text
0 < theta < 1,  0 < c < (1-theta)/3.
```

`adaptiveAnalyticParameters_of_wide` selects `c<a<b<(1-theta)/3`, `Q>1`,
and `q>1` with `3Qb<1-theta` and `2qb<1-theta/2`.  Lean defines

```text
U_r=k^(r+1)log(k)^(-Q(2r-1)),
V_r=k^(r+theta)log(k)^(Q(r-1)),
Z_r=max(nr!,V_r),
lambda_r=(Z_r/(nr!))^(1/r).
```

It proves `lambda_r^r=Z_r/(nr!)`, `lambda_r>=1`, constructs the least
stopping order with `nr!<=U_r`, and derives

```text
log(lambda) <= (theta/r) K + 3 Q M.
```

`adaptiveT3At_eventual` handles the third term uniformly for every `r>=2`,
while `adaptive_additive_term_eventual` proves the additive term is
`o(k^theta/log k)`.  `large_card_raw_adaptive_selected_at` performs the exact
substitution into the pinned upstream estimate, and
`adaptive_bad_set_asymptotic_of_budgets` closes the analytic count.  The final
large case, range package, builder, and divisor theorem are respectively
`case_large_adaptive_at`, `adaptiveRangePackage_of_parameters`,
`parametricRangeBuilder_adaptive`, and `parametric_frontier_adaptive`.

## Four range fields

1. `ParametricSmall.case_small`:
   `2k < n <= (1/2) k^(2-theta)`;
2. `ParametricMed.case_medium`:
   `(1/2) k^(2-theta) < n <= k^2/log^2(k)`;
3. `ParametricML.case_mediumlarge`:
   `k^2/log^2(k) < n <= (1/2) k^(2+theta)`;
4. `ParametricLarge.case_large_adaptive_at`:
   `(1/2) k^(2+theta) < n <= exp(c log^2(k)/loglog(k))`.

Each field first produces a prime in the actual source interval
`(k,k+3k^theta)`.  Common range composition then uses
`3 k^theta <= k` eventually to obtain `(k,2k)`.

## Sharp large-range exponent

The replay parameterizes `E1exp`, `lamLarge`, the balanced
`large_card_raw`, logarithmic margins, `r0Param`, factorial admissibility,
and the least admissible order.  It retains the positive balancing exponent:

```text
E1(theta,r) = (1-theta)(2r-1)/(3r-2),
a(theta,r)  = (2-theta-E1(theta,r))/r
            = ((4-theta)r+theta-3)/(r(3r-2)).
```

Lean proves, for `r>=3` and `0<theta<1`,

```text
a(theta,r) <= a(theta,3) = (9-2theta)/21.
```

The cleared-denominator difference is

```text
(r-3) * (r(27-6theta)+7theta-21) >= 0.
```

It also proves the exact equivalence
`(9-2theta)/21 < theta` iff `theta>9/23`, allowing

```text
2 k^((9-2theta)/21) log(k) = o(k^theta/log(k)).
```

The coarse `(2-theta)/3` bound is derived only for the third non-additive
Konyagin term; it is never used for the additive term controlling the lower
theta boundary.

## Parameter frontier

`exists_frontier_parameters_at` supplies `c<a<b`, `q1>1`, `q3>1` with

```text
3 q1 b < 1-theta,
4 q3 b < 1.
```

The least-order construction transfers these margins from
`r0=ceil(a log(k)/loglog(k))` to the minimal admissible `r`.  The condition
`c<(1-theta)/3` is the strict frontier used by this method class.  Endpoint
auditing proves the exact feasibility equivalence, for `c>0`:

```text
BalancedFourRangeParameters(theta,c)
  iff 9/23 < theta < 1 and c < (1-theta)/3.
```

This equivalence audits only the explicitly defined older **balanced**
parameter subclass.  It is not a no-go for the adaptive architecture:
`parametricRangeBuilder_adaptive` removes the `9/23` lower endpoint while
retaining the same leading `c<(1-theta)/3` frontier.

## Scoped location-blind obstruction

The kernel result now goes beyond merely repeating
`adaptiveFrontierParameters_iff`.  It defines abstract logarithmic first-two
terms for one subdivided Konyagin block and proves, for every `r>=2`,

```text
(2r-1) log(T1)+(r-1) log(T2)=log(delta)+4log(W).
```

Both the derivative factor and arbitrary unbalanced `lambda` cancel, while
`W>=1` can only increase the right side.  The theorem
`locationBlind_termwise_block_budget_obstruction` combines this identity
with the cardinality-tail safe threshold

```text
log(delta W^4)>=-(1-theta)K-M-C
```

to obtain the exact finite inequality

```text
((2r-1)alpha+(r-1)beta)M <= (1-theta)K+M+C.
```

The actual adaptive definitions satisfy the sharper equality with right side
`(theta-1)K`, checked by `adaptive_first_two_log_invariant` and
`adaptive_first_two_budget_obstruction`.

At the endpoint, Lean does not assume fixed decay exponents separated from
`1`.  If both block logs are at most `-M-q`, the order lower bound is
`rM>=cK-DM`, and `c>=(1-theta)/3`, then
`locationBlind_endpoint_excess_budget` proves

```text
(3r-2)q <= (3D+3)M+C.
```

`locationBlind_endpoint_termwise_no_go_of_excess` packages the strict reverse
inequality as a contradiction.  This finite form is used with the natural
proof's `q_k->infinity` and covers little-`o` budgets whose effective
log-power tends down to `1`.

Finally `LocationBlindTermwiseLeadingCertificate` is the precise LP image
with `rho>=c`, `alpha>1`, `beta>1`, and
`(2alpha+beta)rho<=1-theta`.  Lean proves its feasibility iff
`c<(1-theta)/3` for `c>0`, then kernel-refutes `c>=(1-theta)/3` in this named
class, including `c>=19/120` at `theta=21/40`.

This does **not** formalize arbitrary growing block families as Lean objects.
The PI cardinality-tail reduction and the weighted extraction of a good block
from a total `o(k^theta/log k)` nonnegative sum remain natural-proof steps in
`adaptive_unbalanced_partition_frontier.md`.  The kernel theorem is therefore
scoped to the block algebra and leading LP image and is not a no-go for all
methods or for Erdős 451.

At the
unconditional BHP input `theta=21/40`, it specializes to `c<19/120`.

## Axiom and resource audit

All parameterized large lemmas, the complete adaptive builder, and the final
abstract theorem report exactly

```text
[propext, Classical.choice, Quot.sound]
```

They contain no `bhp`, `sorryAx`, `admit`, or new axiom.  `bhp` is needed only
when separately instantiating `PrimeIntervalInput(21/40)`.

Run `cd formal && bash verify_guarded.sh`.  It performs the complete replay
inside the shared OpenMath memory slice, verifies exact axiom lists, rejects
`sorryAx`, and writes SHA-256 hashes to `formal/logs/final-sha256.txt`.

Final full replay: guard unit
`openmath-task-20260826-201020-239491.scope`, exit status `0`; the cached
range-build took `3.27s` with peak RSS `921,676 KiB`, while the whole replay
peaked at `6,597,940 KiB`, with zero swap.  The immediately preceding fresh
range build of the same source ran in guard unit
`openmath-task-20260826-200821-237917.scope`, took `109.97s`, peaked at
`7,009,816 KiB`, used zero swap, and is saved as
`formal/logs/location-blind-attempt03.log`.  The verified
`ParametricRanges.lean` SHA-256 is
`ab6bfdcc85dec37b7489a2f2f615e7976136e9a9a3c40cd9ccde8324b064a0e5`.
