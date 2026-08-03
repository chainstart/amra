# Independent audit: prism triangle-edge `z=1` component theorem

Date: 2026-08-03

Verdict: **the local theorem is correct and may be marked proved after one
explicit proof repair concerning the discriminant of `D`**.

## Reconstruction and algebra

The independent verifier reconstructs `P` and `xi` directly from all forests
of the eight-edge graph obtained by marking prism edge `01`.  It does not
import the candidate verifier or its displayed polynomials.  It again obtains
190 forests and 66 forests connecting the marked endpoints.

After coarsening the two size-two triangle orbits, the two singleton orbits,
and the size-two vertical orbit, shifting by `x=p+1,y=t+1,z=v+1`, and setting
`z=1`, the audit reproduces

```text
P=(x-1)C,
xi=(x-1)D,
```

with exactly the displayed quadratics `C` and `D`.  It also reproduces

```text
disc_y(C) = 8(x-1)^3(x+1),
Res_y(C,D) = -2(x-1)^7(x+1)(x+3)^2.
```

Both are respectively positive and nonzero for `x>1` as claimed.

## Component classification

For `x>1`, the leading coefficient `(x+1)(x^2+1)` of `C` is positive and
the discriminant is strictly positive.  Hence `C>0` is the disjoint union

```text
y < r_C^-(x)  or  y > r_C^+(x).
```

The functions `r_C^-` and `r_C^+` are continuous on `(1,infinity)`.  Each
of the corresponding hypo/epigraph regions is connected; for example the
upper region is homeomorphic to `(1,infinity) x (0,infinity)` via
`(x,y) -> (x,y-r_C^+(x))`.  The wall `x=1` lies in `P=0`, so a path from the
anchor cannot leave `x>1`.  Since `(2,2)` lies above `r_C^+(2)`, its complete
component in the `z=1` plane is exactly

```text
x>1,  y>r_C^+(x).
```

This verifies both connectedness and maximality, rather than merely showing
that the epigraph is contained in the component.

## Strict root order and the `D` double-root issue

The candidate proof needs one additional calculation:

```text
disc_y(D)=(x-1)^3(x^3+5x^2+11x-1).
```

For `x>1`,

```text
x^3+5x^2+11x-1
  = (x-1)(x^2+6x+17)+16 > 0.
```

Thus `D` has two distinct real roots throughout the entire interval `x>1`.
Its ordered roots are continuous there; no double-root fibre occurs in the
domain.  Since the resultant is nonzero, neither root of `D` can meet either
root of `C`.  At `x=2`,

```text
r_D^+=1/2 < 2/5+sqrt(6)/15=r_C^+.
```

Continuity and the nonzero resultant therefore give the strict order
`r_D^+<r_C^+` for every `x>1`.  Because `D` is upward-opening, it follows
strictly that `D>0` whenever `y>r_C^+(x)`, and hence

```text
xi=(x-1)D>0
```

on the complete distinguished `z=1` component.

The original parenthetical statement that a `D` double root would make the
conclusion “stronger” is not by itself sufficient: an upward quadratic at a
double root is nonnegative but vanishes at the root, so strict positivity
would still require proving that the double root lies outside the epigraph.
The discriminant calculation above repairs the proof more cleanly by showing
that the hypothetical case never occurs for `x>1`.

## Negative point and scope

At `x=3/2`, the lower root is

```text
r_C^-=8/13-2sqrt(10)/65 > 1/2;
```

the last inequality follows, for example, from `15>4sqrt(10)`.  Therefore
the point `(3/2,1/2,1)` belongs to the lower `C>0` component and is rigorously
separated from the anchor component inside the `z=1` plane.

This proves only the complete two-variable component obtained by imposing
`z=1` in the three-variable coarsening.  It says nothing about paths with
`z!=1`, the full five stabilizer variables, G201, or OPG-1757.

## Status recommendation

After adding the displayed `disc_y(D)` positivity argument, the appropriate
status is:

> `proved` for `xi>0` on the complete distinguished `z=1` component of the
> three-variable triangle-edge coarsening.

No broader promotion is supported.
