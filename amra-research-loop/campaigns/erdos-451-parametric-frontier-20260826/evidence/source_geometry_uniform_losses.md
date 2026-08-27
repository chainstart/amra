# Finite source-geometry to uniform-loss interface

## Status and scope

This note records the kernel-checked finite map from explicit source-scale
inequalities to the common losses `C,D` used by the already proved
location-blind subdivision obstruction. It does not enlarge that obstruction
class or concern prime-location-adaptive covers, cross-block cancellation,
stronger analytic input, or the true bad-set cardinality.

Write `K=log k`, `M=log K`. The formal map takes fixed constants

```text
a>0,  En>=0,  ED>=0                                      (1)
```

outside the whole finite block family and returns

```text
C=-log a,  D=5/2+En+ED.                                  (2)
```

The earlier “uniform `C,D`” step is therefore kernel-checked from the raw
comparisons below. What remains conditional is whether a proposed broader
source subdivision supplies fixed `a,En,ED`; an unquantified
`D_r ≍ n r!/x^(r+1)` does not itself say that its constants are uniform.

## 1. Shifted-base loss

`sourceLogRatio_bounds_of_window` proves, for `0<k` and `r>=0`,

```text
k<=x<=k+w,  r*w<=B*k  ==>  0<=r log(x/k)<=B.              (3)
```

The upper bound is `log(1+t)<=t`. Its specialized form
`sourceRpowWindow_log_bounds` assumes

```text
1<=k, 0<=theta<=1, k<=x<=k+k^theta,
r<=(1/2)k^(1-theta),                                      (4)
```

and proves

```text
r log(x/k)<=1/2,
(r+1)(log x-log k)<=3/2.                                  (5)
```

No asymptotic `O(1)` occurs in these finite theorems.

## 2. Safe-tail loss

`sourceSafeTailLog_of_lower` starts from

```text
a*k^(theta-1)/log k <= delta,  a>0, k>1,                  (6)
```

and obtains

```text
-(1-theta)K-M-(-log a) <= log delta.                      (7)
```

`sourceSafeTailLog_with_W` adds `4 log W` for `W>=1`.
Thus the common safe loss is exactly `C=-log a`. The prior PI
cardinality-tail argument provides an eventual positive `a` for its full
deterministic tail; another source cover must prove its own (6).

## 3. Order loss

For each block the finite source interface assumes positive scales and

```text
exp(c*K^2/M-En) <= nScale,                                (8)
exp(-ED)*nScale*factorialScale/x^(r+1)
  <= derivativeScale.                                    (9)
```

It also assumes `factorialScale>=1`, `lambda>=1`, and `W>=1`. Lean takes
logs in `sourceEndpointLogLower_of_exp` and
`sourceDerivativeLogLower_of_scale`. If the first Konyagin log term is
negative, `sourceLogD_neg_of_T1` proves
`log derivativeScale<0`. Dropping the nonnegative factorial log and using
`(r+1)(log x-K)<=B`, `sourceOrderLoss_of_log_comparisons` yields

```text
c*K-(1+En+ED+B)*M <= r*M.                                 (10)
```

With `B=3/2` from (5), this is

```text
c*K-(5/2+En+ED)*M <= r*M.                                 (11)
```

The `5/2` is exact: one unit replaces `r+1` by `r`, and `3/2` is the
shifted-base window loss.

## 4. Family map and finite endpoint wrapper

`SourceGeometrySubdivisionBlock` records each block's positive weight,
`x`, `delta`, endpoint scale, factorial scale, derivative scale, `lambda`,
`W`, and natural order. `SourceGeometrySubdivisionAt` requires a nonempty
finite family whose positive weights sum to `H`; (4), (6), (8), and (9)
with the same `a,En,ED`; order at least two; `lambda,W>=1`; and the existing
summed nonnegative first-two-term ledger.

`sourceGeometrySubdivision_to_locationBlind` maps the whole family to
`LocationBlindTermwiseSubdivisionAt` with exactly (2), without a family-size
bound.

`sourceGeometrySubdivision_endpoint_no_go_of_scale_bounds` is the explicit
finite endpoint wrapper. Besides `q>=1`, `cK>=0`, and
`c>=(1-theta)/3`, it assumes

```text
(3D+2)M <= cK,                                           (12)
((3D+3)M+C)M < 2cK.                                     (13)
```

`sourceFiniteSeparation_of_scale_bounds` converts (12)--(13) to the strict
separation required by the previous endpoint no-go. The wrapper deliberately
does not state the unformalized limit `K/M^2 -> infinity`.

## 5. Exact remaining source input

The mapping is complete once fixed `a,En,ED` are supplied. It does not prove
that every shifted or variable grouping has them. For example, lower
comparison factors `exp(-ED(k))` with `ED(k)->infinity` map to
`D(k)=5/2+En+ED(k)`, not a fixed `D`. The one-block counterexamples in
`location_blind_subdivision_bridge.md` show that uncontrolled losses really
can evade the endpoint argument.

Hence the precise conclusion is:

> The source-to-obstruction map is kernel-checked for the explicitly defined
> finite source class with fixed raw comparison constants. Instantiating it
> for the pinned unshifted source, or a separately proved uniformly shifted
> source, is valid after checking (6), (8), and (9). It is not a theorem about
> arbitrary regroupings with unspecified comparison factors.

The guarded replay checks the new theorems have only
`[propext, Classical.choice, Quot.sound]`, no `sorry`/`admit`, and no new
axiom. Exact resources and hashes are recorded in
`evidence/lean_parametric_ranges.json`.
