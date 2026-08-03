# Independent audit: K5-e upper-root component theorem

Date: 2026-08-03

Verdict: **passed after two explicit continuity clarifications**.

Scope: the complete `2,4,2` orbit-equalized high-triangle marked-edge slice
of `K5-e`.  This audit makes no claim about the five transverse edge
directions, global `G201`, or OPG-1757.

## Independent reconstruction

The verifier does not import the author script.  It independently enumerates
all `2^8` subsets of the eight unmarked edges.  A subset is certified as a
forest by the rank of its oriented incidence matrix; endpoint connectivity is
checked by a separate graph traversal.  It recovers 134 forests and 70
forests connecting the marked endpoints, and reconstructs `P=bF`, `xi=bG`.

After the change of variables `y=b+1,z=c+1`, it independently verifies

```text
F=Aa^2+2LMa+(y-1)L^2,
A=(y+1)((y^2+1)z^2-2),
L=(y+1)z-2,
M=(y^2+1)z-2,
disc_a(F)=8(y^2+1)(z-1)^2L^2.
```

It also reconstructs `G`, its leading coefficient `2D`, its discriminant,
and the `F,G` resultant used by the theorem.

## Component equality audit

On `A>0,F>0`, define

```text
S_F=partial_a F=2Aa+2LM.
```

The identity

```text
S_F^2-disc_a(F)=4AF>0
```

shows that `S_F` cannot vanish.  Its positive and negative signs distinguish
the upper and lower `F` sheets even on a fibre where the two roots coalesce.
At the anchor `S_F=172>0`.

The first possible `A=0` wall is
`z=j=sqrt(2/(y^2+1))`.  For `y>1`, exact squared inequalities give

```text
j<2/(y+1),  L(j)<0,  M(j)=sqrt(2(y^2+1))-2>0.
```

The upper-root numerator tends to `-2LM>0` while `A -> 0+`, so the upper
root tends to `+infinity`.  A continuous path on a compact parameter
interval is bounded and cannot cross this wall.  The base
`{y>1,z>j(y)}` is connected and the upper root is continuous; its epigraph
is therefore connected.  This confirms that it is exactly the anchor
component, rather than merely a subset.

## G-root continuity audit

On the upper-root base,

```text
D>(y-1)^3/(y^2+1)>0,
```

so `G` remains an upward quadratic.  A necessary starting fact, made
explicit during audit, is

```text
disc_a(G) at (y,z)=(2,2) is -384<0.
```

Thus the anchor base fibre has no real `G` roots at any `a`; the value
`G(1)=70` alone would not have been sufficient.

The complete double-root locus is `z=1`, `L=0`, or `N=0`, where

```text
N=(y^2-3)z+(y-2)^2+1.
```

The first two double roots are on or below the `F` wall.  On `N=0`, positivity
of `z` is equivalent to `1<y<sqrt(3)`.  At the double root,

```text
F=(y-1)^5(y^2-7)(y^2+1)^3 /
  (4(y^2-3)^2(y^2-2y-1)^2) < 0,
```

so the root lies strictly below the upper `F` root.

The only common-root walls are `L=0` and `H=L^2+8(z-1)=0`.  The former is
on `F=0`.  Parameterizing the latter by `ell=L`, the conditions `y>1,z>0`
give `0<ell<sqrt(8)`, and at the common root

```text
partial_a F = ell^3(ell^2+4ell+8)/(2(ell^2-8)) < 0.
```

It is therefore the lower `F` root.  No `G` root can be born in, or cross
into, the upper-root epigraph.  Along any finite path in the connected base,
`D` has a positive minimum, so roots also cannot enter from infinity.

## Verdict and mechanism recommendation

The theorem `G>0`, hence `xi=bG>0`, on the complete three-variable
distinguished component is correct.

Recommended mechanism record:

```text
G215 status: proved
```

with the strict statement match “K5-e high-triangle `2,4,2` stabilizer slice
only.”  `G201` must remain unchanged and surviving; the global closure
contract is unaffected.

