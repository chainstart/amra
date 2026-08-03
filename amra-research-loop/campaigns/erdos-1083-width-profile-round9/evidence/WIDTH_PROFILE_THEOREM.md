# Gauge-invariant width profile theorem

## Scope

Work in the actual power-large simultaneous-switch block

```text
P_V=P_A0 F_0=P_Aj F_j,        F_j=P_{lambda_j X},
```

where all four displayed product masks are actual finite positive masks in
the fixed natural real order.  Put

```text
D=max X-min X,       W=wd(V),       d_j=wd(lambda_j X).
```

The selected same-sign class `J_sigma` has distinct nonzero scalars and
`|J_sigma|>=ceil(K/2)=t^(5/9-o(1))`.  Since the inherited endpoint has
`|X|=S>1`, one has `D>0`.

## 1. Endpoint gauge and positive products

For an ordered endpoint pair `(l,r)`, Laurent translation by `c` acts by
`(l,r)->(l+c,r+c)`.  Its orbit is completely classified by `r-l`: equality
of widths gives the translating scalar `c=l'-l`, and conversely translation
preserves width.  Thus support width is exactly the quotient of the two
natural endpoints by diagonal monomial gauge, not merely one invariant of
that quotient.

For nonempty finite positive masks, natural endpoints add under product:

```text
min(A+B)=min A+min B,       max(A+B)=max A+max B.
```

Consequently width is additive.  Positivity is essential for interpreting
the product as the actual support sum; independently normalized factor
endpoints are not canonical before taking the width quotient.

## 2. Exact four-width profile

Scalar dilation gives

```text
d_j=|lambda_j|D.
```

Taking widths in the two actual common-spectrum factorizations gives the
complete four-product profile

```text
Psi_j=(wd(F_j),wd(F_0),wd(P_Aj),wd(P_A0))
     =(|lambda_j|D, |lambda_0|D,
       W-|lambda_j|D, W-|lambda_0|D).
```

Hence only the first coordinate varies; the third is forced by the common
total, and the centre coordinates are fixed.  On `J_sigma`, distinct
scalars have distinct absolute values.  Since `D>0`, projection to the first
coordinate proves

```text
|Psi(J_sigma)|=|J_sigma|,
max_p |Psi^{-1}(p)|=1.
```

This conclusion is exhaustive: it does not depend on which natural endpoint
of `X` is zero.

## 3. Exact comparison with the round-eight profile

Write `x_-=min X`, `x_+=max X` and
`phi_j=min(lambda_j X)`.  In the fixed natural order,

```text
lambda_j>0:  phi_j=lambda_j x_-,   d_j=lambda_j D;
lambda_j<0:  phi_j=lambda_j x_+,   d_j=-lambda_j D.
```

There are exactly two information regimes on a fixed-sign class.

1. If the relevant endpoint (`x_-` for positive scalars, `x_+` for negative
   scalars) is zero, `phi_j` is constant but `d_j` and `Psi_j` are injective.
   Width therefore genuinely recovers information lost by the least-endpoint
   projection.
2. If the relevant endpoint is nonzero, width is a fixed nonzero multiple of
   `phi`: `d_j=(D/x_-)phi_j` in the positive class and
   `d_j=(-D/x_+)phi_j` in the negative class.  Width then adds no range or
   fibre information beyond `phi`.

Thus the joint pair `(phi_j,d_j)` is injective in both branches, and the width
coordinate is precisely what resolves the zero-anchor fibre.

## 4. Literal range versus residual information

The literal width profile costs the whole selected-row exponent under
constant-profile conditioning: every fibre on `J_sigma` is a singleton.
This is compatible with every simultaneous-switch identity; different rows
are allowed to carry different source widths.

It is not new complement entropy.  The row already contains `lambda_j` and
the common source `X`, so `d_j=|lambda_j|D` is known source data.  After
subtracting the predicted source coordinate, the exact residual equations are

```text
wd(F_j)-d_j=0,
wd(P_Aj)+d_j-W=0,
wd(F_0)-d_0=0,
wd(P_A0)+d_0-W=0.
```

Their joint residual range is one.  Literal conditioning and solving after
subtracting known row data are therefore opposite descriptions of the same
one-dimensional affine graph.

## 5. Divisor-atlas comparison

The inherited common-factor chart writes `F_j=G R_j` and proves

```text
wd(G)+wd(R_j)=a+b_j=|lambda_j|D.
```

Accordingly the distinct same-sign `b_j` atlas and the injective first width
coordinate are the same varying scalar up to the fixed shift `a`; they are
not two independent rigidity coordinates.

## 6. Exact scope

Proved:

- width is the complete two-endpoint translation-gauge quotient;
- the exact four-product width graph;
- unconditional same-sign injectivity in both zero-anchor and nonzero-anchor
  branches;
- width recovers exactly the information lost by `phi` in the zero-anchor
  branch and is redundant in the other branch;
- the known-source residual width profile is identically zero;
- the width injection is the inherited divisor-width atlas in different
  coordinates.

Not proved:

- a large constant literal-profile fibre;
- new complement entropy or cross-row rigidity;
- an injection from width values to new target-target Euclidean distances;
- all-target occurrence mass, distance-collision fibre savings or outer
  stability;
- any improvement of the public dimension-three `3/5` exponent.

## 7. Bounded reproduction

```text
AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/erdos-1083-width-profile-round9/evidence/verify_width_profile.py
```

The checker verifies the orbit quotient, product endpoint identities, both
scalar signs, both anchor branches, exact profile fibres and zero residuals.
The universal statements follow from the proof above, not finite
extrapolation.
