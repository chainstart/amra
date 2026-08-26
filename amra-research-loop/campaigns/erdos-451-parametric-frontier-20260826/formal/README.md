# Lean package for the Erdős #451 parametric frontier

This package pins the public upstream formalization at commit
`92a033fa99f0a53a3c16257c47e3d9e04dfc3f55` and SHA-256
`44e478bed8d756f271aaffd45af5fa4797fbee857aa780f7412275a521b84004`.

`FrontierLemmas.lean` parameterizes the active large-range inequalities by
strict logarithmic margins and proves `erdos451_bhp_frontier`: for every real
`0 < c < 19/120`, all sufficiently large `k` and all integers
`2k < n <= exp(c log^2(k) / loglog(k))` have a prime divisor of `Pprod k n`
strictly between `k` and `2k`.  No `sorry`, `admit`, or new axiom is allowed.
Run the replay only through:

```bash
./verify_guarded.sh
```

`ParametricInterface.lean` additionally extracts the general exponent
interfaces that do not rely on the numerical BHP exponent: abstract
`PrimeIntervalInput`, the bad-count-to-divisor bridge, exact four-range
composition, and strict-margin parameter feasibility for
`2/5 < theta < 3/5`, `0 < c < (1-theta)/3`.  It exposes the then-remaining
obligation as `ParametricRangeBuilder` without introducing it as an axiom;
`ParametricRanges.lean` now discharges that obligation.  The existing
`theta=21/40` theorem is also reproved as
`erdos451_bhp_frontier_via_interface`.

`ParametricRanges.lean` now constructs all four substantive fields of the
builder for a variable exponent.  The small, medium, and medium-large fields
hold for `0 < theta < 1`; endpoint auditing expands the complete large field
to the sharp method interval `9/23 < theta < 1`.  Its parameterized
`E1expAt`, `lamLargeAt`,
`large_card_raw_at`, logarithmic-margin estimates, and least-admissible-order
construction use only the abstract `PrimeIntervalInput theta`.  The crucial
additive exponent is retained exactly as

```text
(2-theta-E1(theta,r))/r
  = ((4-theta)r+theta-3)/(r(3r-2))
  <= (9-2theta)/21 < theta       (r>=3, theta>9/23),
```

instead of the upstream coarse `(2-theta)/3`, which would unnecessarily
require `theta>1/2`.

The widest compiled theorem `ParametricLarge.parametric_frontier_wide` states:
for every `9/23 < theta < 1`, every `0 < c < (1-theta)/3`, and every
`PrimeIntervalInput theta`, all sufficiently large `k` and all integers
`2k < n <= exp(c log^2(k)/loglog(k))` admit a prime divisor of `Pprod k n`
strictly between `k` and `2k`.  It and the complete builder depend only on
Lean's standard classical/propositional axioms, not on the fixed `bhp` axiom.
The older `2/5 < theta < 3/5` theorem is retained as a compatibility
corollary.

The file now also contains a kernel-checked **adaptive unbalanced parameter
core** on the full natural window

```text
0 < theta < 1,    0 < c < (1-theta)/3.
```

`AdaptiveFrontierParameters` proves exact feasibility of fixed `Q,a` with
`1<Q`, `c<a`, and `3Qa<1-theta`.  The definitions `adaptiveLogU`,
`adaptiveLogV`, and `adaptiveLogZ` encode the logarithms of the natural-proof
scales `U_r`, `V_r`, and `max(nr!,V_r)`.  The theorem
`adaptive_log_selection_budget` proves from the stopping and minimality
inequalities that

```text
log V_r <= log U_r,
log T1 <= -Q loglog(k),
log T2 <= -Q loglog(k),
log lambda <= (theta/r) log(k) + 3Q loglog(k).
```

This removes `theta>9/23` from the kernel-checked parameter algebra.  It does
not yet change the widest compiled final divisor theorem: the existing
balanced wrapper hardcodes `lamLargeAt`, but
`large_card_raw_adaptive_at` now separately exposes the upstream Konyagin
estimate for arbitrary real `lambda>=1` and every `r>=2`.  Completing the
adaptive final builder still requires lifting the logarithmic max selection
to an actual positive real `lambda`, constructing the least stopping order,
and proving the analytic third/additive-term asymptotics.

`balancedFourRangeParameters_iff` proves the exact feasibility certificate
for this delimited balanced four-range method (assuming `c>0`): its parameter
system exists if and only if
`9/23 < theta`, `theta < 1`, and `c < (1-theta)/3`.  Thus neither changing
`a,b,q₁,q₃` nor merely moving the existing split points crosses either
endpoint; a different estimate for the `r=3` additive remainder would be
needed below `9/23`.

The wrapper enters the shared OpenMath slice with a 30 GiB high watermark,
34 GiB hard memory limit, 4 GiB swap limit, and 512-task limit before Lake or
Lean starts.
