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

The balanced theorem `ParametricLarge.parametric_frontier_wide` states this
for `9/23 < theta < 1`; it is retained, together with the older
`2/5 < theta < 3/5` theorem, as a compatibility result.  The adaptive theorem
below is now the widest compiled result.  All three depend only on Lean's
standard classical/propositional axioms, not on the fixed `bhp` axiom.

The file now also contains a kernel-checked **complete adaptive unbalanced
builder** on the full natural window

```text
0 < theta < 1,    0 < c < (1-theta)/3.
```

The actual scale is defined in Lean by

```text
U_r = k^(r+1) log(k)^(-Q(2r-1)),
V_r = k^(r+theta) log(k)^(Q(r-1)),
Z_r = max(n r!,V_r),
lambda_r = (Z_r/(n r!))^(1/r).
```

Lean proves `lambda_r^r=Z_r/(n r!)`, `lambda_r>=1`, constructs the least
stopping order with `n r!<=U_r`, and transports its preceding-order failure
to the exact logarithmic lower bound.  `adaptive_actual_selection_budget`
then proves

```text
log V_r <= log U_r,
log T1 <= -Q loglog(k),
log T2 <= -Q loglog(k),
log lambda <= (theta/r) log(k) + 3Q loglog(k).
```

The unified `r>=2` third-term bound and the additive-term estimate are proved
eventually, with no bounded-order gap.  The selected scale is substituted
exactly into the upstream arbitrary-real-`lambda` Konyagin theorem, yielding
`adaptive_bad_set_asymptotic_of_budgets`.  The resulting
`parametricRangeBuilder_adaptive` constructs all four ranges, and
`parametric_frontier_adaptive` proves under `PrimeIntervalInput theta`:

```text
0 < theta < 1,  0 < c < (1-theta)/3
----------------------------------------------------------
eventually every 2k<n<=exp(c log^2(k)/loglog(k)) has
a prime divisor p of Pprod(k,n) with k<p<2k.
```

Thus `9/23` is confirmed as an artifact of the balanced scale, not a lower
endpoint of the larger adaptive old-proof architecture.  This does not
increase the unconditional BHP value: `theta=21/40` still gives exactly every
`c<19/120`.

The file also kernel-checks the decisive obstruction for the explicitly
delimited **location-blind, termwise-nonnegative** certificate class.  For a
single block with arbitrary unbalanced scale and denominator parameter
`W>=1`, it proves the exact logarithmic product invariant

```text
(2r-1) log(T1)+(r-1) log(T2)=log(delta)+4log(W),
```

so increasing `W` cannot help.  It derives the finite safe-tail budget and
the endpoint excess bound `(3r-2)q<=(3D+3)loglog(k)+C`, then proves the exact
leading linear-program equivalence

```text
LocationBlindTermwiseLeadingCertificate(theta,c)
  iff c<(1-theta)/3                         (c>0).
```

Hence `locationBlindTermwiseLeadingCertificate_no_go` rules out the endpoint
inside that named leading parameter class, and its BHP specialization rules
out `c>=19/120` there.  This scoped result is not a no-go for Erdős 451 or for
methods using cross-block cancellation, prime-location-adaptive covers, or
stronger analytic/prime input.

The finite/growing subdivision bridge is now also kernel-checked.  Lean proves
the exact PI cardinality tail, telescoping of arbitrary finite interval
partitions, and positive weighted extraction for the structure
`LocationBlindTermwiseSubdivisionAt`.  The theorem
`locationBlindTermwiseSubdivision_endpoint_no_go` rules out any such finite
family when

```text
((3D+3)M+C)M < (3cK-(3D+2)M)q
```

at `c>=(1-theta)/3`.  It is uniform in the finite index set, so the block
count may grow arbitrarily with an outer parameter.  The remaining
natural-proof boundary is the source-geometric derivation of fixed uniform
losses `C,D` and the eventual instantiation from `q_k->infinity` and
`log(k)/loglog(k)^2->infinity`; see
`evidence/location_blind_subdivision_bridge.md`.

`balancedFourRangeParameters_iff` proves the exact feasibility certificate
for this delimited balanced four-range method (assuming `c>0`): its parameter
system exists if and only if
`9/23 < theta`, `theta < 1`, and `c < (1-theta)/3`.  Thus neither changing
`a,b,q₁,q₃` nor merely moving the existing split points crosses either
endpoint; a different estimate for the `r=3` additive remainder would be
needed below `9/23`.

The wrapper enters the shared OpenMath slice with a 30 GiB high watermark,
34 GiB hard memory limit, 4 GiB swap limit, and 512-task limit before Lake or
Lean starts.  The final full replay passed in unit
`openmath-task-20260826-204654-272766.scope` with zero swap and whole-replay
peak RSS `6,575,412 KiB`; the fresh range build of the same source passed in
unit `openmath-task-20260826-203707-264733.scope` in `107.22s` with peak RSS
`7,052,716 KiB`.  The checked `ParametricRanges.lean` SHA-256 is
`d5a039d2fb7a30f4302bb0c04b42ce73cebbd46ad29db5e6b57bdf8bdf48dfe2`.
