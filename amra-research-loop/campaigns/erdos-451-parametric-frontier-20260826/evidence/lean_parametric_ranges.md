# Complete variable-theta range builder

## Compiled theorem

`formal/ParametricRanges.lean` proves
`ParametricLarge.parametric_frontier_wide`:

```text
9/23 < theta < 1
0 < c < (1-theta)/3
PrimeIntervalInput(theta)
----------------------------------------------------------
eventually, for every 2k < n <= exp(c log^2(k)/loglog(k)),
some prime p with k < p < 2k divides Pprod(k,n).
```

The companion theorem `parametricRangeBuilder_wide` constructs the exact
four-field `ParametricRangePackage theta c`.  Thus the conditional
`PI(theta)` theorem previously exposed only as an interface is now fully
formalized.

The same file now separately kernel-checks the adaptive unbalanced parameter
core for every

```text
0 < theta < 1,  0 < c < (1-theta)/3.
```

`adaptiveFrontierParameters_iff` proves exact feasibility of
`1<Q`, `0<a`, `c<a`, `3Qa<1-theta`.  With `K=log k`, `M=loglog k`, and
`logN=log(nr!)`, the definitions `adaptiveLogU`, `adaptiveLogV`, and
`adaptiveLogZ=max(logN,adaptiveLogV)` encode the adaptive stopping scales.
`adaptive_log_selection_budget` proves `V<=U`, both first-term logarithms at
most `-QM`, and

```text
log(lambda) <= (theta/r) K + 3 Q M.
```

This is a formal parameter theorem, not a new final divisor theorem.  The
widest compiled `ParametricRangeBuilder` remains the balanced
`9/23<theta<1` builder.  The new `large_card_raw_adaptive_at` does expose the
upstream theorem at arbitrary real `lambda>=1` and `r>=2`; the remaining glue
is the actual positive-real max scale, least stopping-order construction, and
uniform third/additive-term asymptotics.

## Four range fields

1. `ParametricSmall.case_small`:
   `2k < n <= (1/2) k^(2-theta)`;
2. `ParametricMed.case_medium`:
   `(1/2) k^(2-theta) < n <= k^2/log^2(k)`;
3. `ParametricML.case_mediumlarge`:
   `k^2/log^2(k) < n <= (1/2) k^(2+theta)`;
4. `ParametricLarge.case_large_of_margin_certificate_at`:
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

At the
unconditional BHP input `theta=21/40`, it specializes to `c<19/120`.

## Axiom and resource audit

All parameterized large lemmas, the adaptive parameter core, the complete
balanced builder, and the final abstract theorem report exactly

```text
[propext, Classical.choice, Quot.sound]
```

They contain no `bhp`, `sorryAx`, `admit`, or new axiom.  `bhp` is needed only
when separately instantiating `PrimeIntervalInput(21/40)`.

Run `cd formal && bash verify_guarded.sh`.  It performs the complete replay
inside the shared OpenMath memory slice, verifies exact axiom lists, rejects
`sorryAx`, and writes SHA-256 hashes to `formal/logs/final-sha256.txt`.
