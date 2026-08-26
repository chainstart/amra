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
`2/5 < theta < 3/5`, `0 < c < (1-theta)/3`.  The remaining obligation for a
fully abstract theorem is explicitly represented by `ParametricRangeBuilder`;
it is not introduced as an axiom.  The existing `theta=21/40` theorem is also
reproved as `erdos451_bhp_frontier_via_interface`.

`ParametricRanges.lean` now constructs three of the four substantive fields of
that builder for a variable exponent.  Assuming `0 < theta < 1` and the
abstract `PrimeIntervalInput theta`, its theorems `ParametricSmall.case_small`,
`ParametricMed.case_medium`, and `ParametricML.case_mediumlarge` prove the
small, medium, and medium-large source intervals without `bhp` or any new
axiom.  The large range remains deliberately outside the compiled checkpoint:
the fixed upstream `E1exp`, `lamLarge`, `large_card_raw`, and minimal-order
machinery still have to be replayed with variable `theta`.  In particular the
replay must keep the exact additive exponent

```text
(2-theta-E1(theta,r))/r
  = ((4-theta)r+theta-3)/(r(3r-2))
  <= (9-2theta)/21 < theta       (r>=3, theta>2/5),
```

instead of the upstream coarse `(2-theta)/3`, which would unnecessarily
require `theta>1/2`.

The wrapper enters the shared OpenMath slice with a 30 GiB high watermark,
34 GiB hard memory limit, 4 GiB swap limit, and 512-task limit before Lake or
Lean starts.
