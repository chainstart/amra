# Endpoint audit for the theta-parametric four-range method

## Result

The original formal window `2/5 < theta < 3/5` was not maximal.  The exact
window supported by the balanced van Doorn--Tang/Konyagin four-range replay is

```text
9/23 < theta < 1,
0 < c < (1-theta)/3.
```

This expansion is kernel checked by
`ParametricLarge.parametric_frontier_wide`.  In particular:

- `theta=2/5` is admitted;
- all `3/5 <= theta < 1` are admitted;
- the old `theta<3/5` restriction was only an interface artifact used to
  infer `theta<1`;
- `theta=9/23` and `theta=1` are genuine strict endpoints for the precisely
  defined method-parameter class below.

## Range-by-range requirements

| Range/component | Theta requirements | Endpoint effect |
|---|---|---|
| Small | `0<theta<1` | None inside the final window. |
| Medium | `0<theta<1` | None inside the final window. |
| Medium-large, `r=2` | `0<theta<1` | Its balanced scale has `lambda>=1` only through the existing upper split `(1/2)k^(2+theta)`. |
| Raw large Konyagin bound | `0<theta<1`, `r>=3` | No `2/5` or `3/5` restriction. |
| First logarithmic term | `3 q1 b < 1-theta` | Forces `theta<1` when `b>c>0`; otherwise handled by choosing strict slack. |
| Third logarithmic term | `4 q3 b < 1` | Requires only `b<1/4`; this follows from the frontier construction once `theta>1/4`. |
| Additive `2 r lambda` term | `sharpAddExp(theta)<theta` | Exact lower endpoint `theta>9/23`. |
| Final interval shrink | `theta<1` | Gives `3k^theta<=k` eventually. |

The small, medium, and medium-large Lean theorems already work throughout
`0<theta<1`.  Thus both former endpoint restrictions came solely from the
large/package layer.

## Lower endpoint

Minimality of the large-range order gives

```text
a(theta,r)
 = (2-theta-E1(theta,r))/r
 = ((4-theta)r+theta-3)/(r(3r-2)).
```

For `r>=3`, this is maximized at `r=3`:

```text
a(theta,r) <= (9-2theta)/21.
```

Lean proves

```text
sharpAddExp(theta) < theta  iff  9/23 < theta.
```

At `theta=9/23`, the additive raw-bound envelope is of size
`k^theta log(k)`, while the available prime-count scale is
`k^theta/log(k)`; the ratio is `log^2(k)`, so no positive constant can absorb
it.  Below `9/23` there is already a positive power loss.

Changing `a,b,q1,q3` cannot repair this: those variables control the two
growing-order logarithmic terms, whereas the obstruction is the minimal order
`r=3`.  Merely moving the existing split cannot repair it either.  The
medium-large `r=2` choice reaches exactly the scale
`(1/2)k^(2+theta)` where its required `lambda>=1` is certified; moving the
large boundary upward leaves an uncovered interval, while moving it downward
does not remove the `r=3` worst case.  Crossing `9/23` therefore requires a
new treatment of the additive remainder or a genuinely different range
estimate, not parameter reselection.

This no-go is deliberately limited to the balanced four-range method class;
it is not a no-go theorem for Erdős #451 or for all Konyagin refinements.

## Upper endpoint

The `3/5` upper cutoff is removable.  The wide parameter construction uses
only

```text
f=(1-theta)/3 > 0,
f<theta,
4f<1.
```

Within the final lower range `theta>9/23`, the latter two are automatic, and
the first is exactly `theta<1`.  At or above `theta=1`, the strict first-term
margin `3 q1 b < 1-theta` is impossible for `q1>1` and `b>c>0`; also the
frontier `(1-theta)/3` admits no positive `c`.

## Exact method-class certificate

Lean defines `BalancedFourRangeParameters(theta,c)` to mean:

1. the sharp minimal-order additive exponent has a strict gap below `theta`;
2. there exist `a,b,q1,q3` with
   `0<a`, `c<a<b<theta`, `q1,q3>1`,
   `3q1b<1-theta`, and `4q3b<1`.

For every `c>0`, Lean proves the equivalence

```text
BalancedFourRangeParameters(theta,c)
  iff 9/23 < theta and theta < 1 and c < (1-theta)/3.
```

The corollaries `balancedFourRange_no_go_low` and
`balancedFourRange_no_go_high` certify infeasibility at the two closed
endpoints.  All these declarations use only
`[propext, Classical.choice, Quot.sound]`.
