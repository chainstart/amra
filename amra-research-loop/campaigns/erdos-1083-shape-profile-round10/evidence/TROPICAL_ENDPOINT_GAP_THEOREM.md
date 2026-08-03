# Tropical endpoint-gap shape theorem

## Scope and definitions

Work in the inherited actual power-large block

```text
P_V=P_Aj F_j,        F_j=P_(lambda_j X),
```

with actual finite positive masks in the fixed natural real order.  Every
source and complement here has at least two support points.  For a finite
support `E={e_0<...<e_k}`, `k>=1`, define

```text
w(E)=e_k-e_0,
g_-(E)=e_1-e_0,
g_+(E)=e_k-e_(k-1).
```

Both gaps are invariant under Laurent translation.  Unlike width, they
retain the first non-affine interior support layer.

## 1. Exact positive-product law

For nonempty positive masks with supports `A={a_0<a_1<...}` and
`B={b_0<b_1<...}`, the support of the product is exactly `A+B`; positivity
prevents cancellation.  The least sum is `a_0+b_0`.  Every other sum is at
least one of `a_1+b_0` and `a_0+b_1`, and both candidates occur.  Therefore

```text
g_-(A+B)=min(g_-(A),g_-(B)).
```

Applying the same argument in reverse order gives

```text
g_+(A+B)=min(g_+(A),g_+(B)),
w(A+B)=w(A)+w(B).
```

Thus `(w,g_-,g_+)` is an exact sum/min/min composable observable.  The rule
is for actual positive product masks.  It is not asserted for signed factors
where extreme support coefficients may cancel, nor for independently
translated endpoint pairs before taking translation-invariant differences.

## 2. Scalar-copy shape

Put `D=w(X)>0`, `ell=g_-(X)>0`, `r=g_+(X)>0`.  In the fixed natural order,

```text
lambda>0: (g_-,g_+)(lambda X)=lambda(ell,r),
lambda<0: (g_-,g_+)(lambda X)=|lambda|(r,ell).
```

Consequently the projective source shape

```text
eta(E)=(g_-(E)/w(E),g_+(E)/w(E))
```

is constant on each scalar-sign class: `(ell/D,r/D)` for positive scalars
and its swap for negative scalars.  This statement is independent of whether
`min X` or `max X` equals zero.  Zero-anchor and nonzero-anchor branches need
no separate normalization and no order reversal.

Raw source gaps remain injective on a same-sign class of distinct scalars;
normalization removes precisely that already-known scalar size.

## 3. Common-spectrum censoring

Write

```text
L=g_-(V), R=g_+(V),
f_j^-=g_-(lambda_j X), f_j^+=g_+(lambda_j X),
a_j^-=g_-(A_j),          a_j^+=g_+(A_j).
```

The exact product law applied to `P_V=P_Aj F_j` gives

```text
L=min(a_j^-,f_j^-),       R=min(a_j^+,f_j^+).                 (1)
```

Hence every actual row obeys `f_j^- >= L` and `f_j^+ >= R`.  More sharply,

```text
f_j^- > L  => a_j^-=L,    f_j^+ > R => a_j^+=R.              (2)
```

At equality the corresponding complement gap is only constrained to be at
least the common gap.  This is the exact tropical censor: it loses a value
only on the equality wall.

## 4. Power-large two-sided core

Restrict to the inherited same-sign class `J_sigma`, where the scalars are
distinct and `|J_sigma|>=ceil(K/2)`.  On that class

```text
f_j^-=c_- |lambda_j|,     f_j^+=c_+ |lambda_j|
```

for fixed positive constants `c_-,c_+` (swapped between signs).  Thus each
equality set

```text
E_-={j:f_j^-=L},          E_+={j:f_j^+=R}
```

has size at most one.  There is a further simultaneous restriction.  Put

```text
u_-=L/c_-,                 u_+=R/c_+.
```

Every actual row has `|lambda_j|>=max(u_-,u_+)`.  If `u_-<u_+`, the left
equality magnitude is infeasible at the right endpoint; if `u_+<u_-`, the
right equality magnitude is infeasible at the left endpoint; and if they
are equal, both equalities select the same scalar magnitude.  Hence
`|E_- union E_+|<=1`.  Delete this union and put

```text
J*=J_sigma-(E_- union E_+).
```

Then

```text
|J*|>=|J_sigma|-1=t^(5/9-o(1)),
(g_-(A_j),g_+(A_j))=(L,R) for every j in J*.
```

Together with the constant normalized source shape, the non-affine profile

```text
Theta_j=(eta(F_j),g_-(A_j),g_+(A_j))
```

has exact range one on `J*`.  The two formal equality thresholds can differ,
but the smaller one cannot occur in an actual row because it violates
feasibility at the other endpoint.  Therefore the unconditional deletion
bound is one.

This is genuine complement boundary rigidity, not raw source indexing.  It
uses the actual positive common-spectrum equation and retains a
power-large family after a constant loss.

## 5. Higher-layer firewall

The second-support layer is special.  Higher ordered support layers do not
compose coordinatewise by minimum.  For

```text
A={0,2,100}, B={0,3,100},
```

the beginning of `A+B` is `0,2,3,5,...`; the fourth product support point is
the mixed sum `2+3`, although neither input has a fourth point.  No complete
boundary-profile semiring is claimed from the two-gap proof.

## 6. Scope

Proved:

- a translation-gauge-invariant, non-affine, exactly composable positive-mask
  observable;
- a sign-exhaustive and anchor-exhaustive constant normalized source shape;
- exact tropical common-spectrum censoring;
- a power-large actual subfamily, losing at most one row, on which both
  complement endpoint gaps and the combined shape profile are constant.

Not proved:

- rigidity of third or deeper support layers;
- factor-level signed shape control;
- an injection from endpoint gaps to new target-target Euclidean distances;
- all-target occurrence, collision-fibre saving or outer stability;
- an improvement of the public dimension-three `3/5` exponent.

## 7. Bounded reproduction

```text
AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/erdos-1083-shape-profile-round10/evidence/verify_tropical_endpoint_gaps.py
```

The checker exhausts positive finite support pairs on a bounded rational
grid, tests both scalar signs and every anchor branch, and verifies the
one-exception censoring logic.  Universal claims follow from the proof above,
not finite extrapolation.
