# Endpoint shape does not determine Euclidean row labels

## 1. Exact positive interval family

Fix an integer `L>=1` and put

```text
M=2(L!)^2,       S=M+1,       U=SM,       X={0,...,S-1}.
```

For every `e=1,...,L`, set `d_e=Se`.  Then `d_e|U`, because `e|M`, and
`U<S^2`.  Define

```text
A_d={r+dSk: 0<=r<d, 0<=k<U/d},
V={0,...,SU-1}.
```

Every `n in V` has a unique quotient/remainder representation

```text
n=r+d h,              0<=r<d,
h=x+Sk,               0<=x<S, 0<=k<U/d.
```

Therefore

```text
V=A_d direct-sum dX,       |A_d|=U, |X|=S,
```

for all `L` rows.  These are honest positive `0/1` masks with one common
spectrum and fixed source/complement cardinalities.

## 2. Constant shape profile

Both endpoints of `A_d` lie in a consecutive residue block of length `d`.
Since `d>=S>=3`, its first and last distinct-point gaps are both one.  The
same is true of `V`.  The scalar source `dX` has width `d(S-1)` and both
endpoint gaps `d`.  Hence every row has exactly the round-ten profile

```text
Theta_d=(g_-(dX)/w(dX),g_+(dX)/w(dX),g_-(A_d),g_+(A_d))
       =(1/(S-1),1/(S-1),1,1).
```

The complete interiors of `A_d` and the scalar `d` nevertheless vary.  Thus
two forced complement boundary layers do not reconstruct the complement
mask or the scalar-copy parameter.

## 3. Arbitrarily large family

Every `e=1,...,L` divides `M=2(L!)^2`, so the instance has `L` distinct
positive scalars `d_e=Se`.  This refutes any absolute bounded-fibre or
functional `Theta -> lambda` theorem while retaining `U<S^2`.

## 4. Common positive tangent

Take

```text
rho=1/2,       z_d=d,       R0>(SL)^2+rho^2,
A'_d=R0+A_d,   V'=R0+V,
T_d=A'_d-rho^2-z_d^2.
```

Because `d=Se` and `e^2<M`,

```text
d^2=dS e belongs to A_d
```

(the corresponding block index is `k=e<U/d=M/e`).  Thus every `T_d`
contains the same tangent

```text
tau0=R0-rho^2>0.
```

The choice of `R0` makes every element of every `T_d` positive.  Moreover

```text
(rho^2+z_d^2+T_d) direct-sum (2rho z_d X)
=A'_d direct-sum dX=V'.
```

So all rows are literal exact Euclidean rows with positive tangent sets and
one common tangent, not merely polynomial factorizations.

## 5. Exact interface no-go

On the common tangent, the inherited chart gives

```text
||q_(d,tau0)-q_(d',tau0)||^2
=(d-d')^2
```

because `lambda=d=2rho z_d` and `rho=1/2`.  For `d_e=Se`, the family has
`L` distinct target positions and exactly `L-1` positive squared-distance
values `S^2h^2`, `1<=h<L`, while its shape-profile range is one.

Consequently no functional map from the round-ten profile value to the
scalar position or to the common-tangent label set exists.  Any positive
bridge must retain additional interior tiling/factor incidence or prove a
new scalar-reconstruction lemma from hypotheses absent in this family.

## 6. Scale and selected-core firewall

The counterfamily is arbitrarily large but not power-large.  Since

```text
log U=Theta(L log L),
```

its row count is `L=U^o(1)`, far below the inherited
`t^(5/9-o(1))` selected family.  It also is not proved to satisfy the
centre-leaf transversality and heavy-factor-hub hypotheses of that selected
core.  Therefore it kills a direct profile-to-label functional bridge, but
does not refute a stronger theorem using those omitted hypotheses at
power-large scale.

## 7. Scope

Proved:

- an all-`L` positive direct common-spectrum family with `U<S^2`;
- identical normalized-source/raw-complement endpoint-gap profiles;
- a literal Euclidean realization with positive tangent sets and one common
  tangent;
- arbitrarily many distinct scalar positions and common-tangent labels in
  one shape fibre;
- failure of any direct functional shape-to-scalar or shape-to-label bridge.

Not proved:

- a power-large counterfamily;
- membership in the transverse heavy-factor selected core;
- failure of a bridge using deeper interior or factor-incidence data;
- any change to the public dimension-three exponent.

## 8. Bounded reproduction

```text
AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/erdos-1083-shape-distance-interface-round11/evidence/verify_shape_distance_no_go.py
```

The checker exhausts the `L=3` direct masks and symbolically checks the
all-`L` arithmetic through `L=12`.  The universal result is the quotient
proof above, not finite extrapolation.
