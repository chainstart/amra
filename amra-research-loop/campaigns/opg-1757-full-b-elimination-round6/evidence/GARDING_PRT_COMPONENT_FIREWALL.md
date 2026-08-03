# Gårding PRT firewall for the full-`b` fixed space

## Exact outcome

The previously recorded point

```text
z=(-7/5,-6,-5,-3,-5),  P(z)=65,  xi(z)=-1588/5
```

is rigorously **outside** the distinguished component of `P`.  This closes
the membership question for that point; it does not prove `xi>0` everywhere
on the component and does not change OPG-1757.

There are two independent exact exclusions.  Along the positive coordinate
ray from `z`,

```text
P(z+t e_a)=5(270t^2-248t+13),
P(z+(1/2)e_a)=-435/2.
```

A Gårding component passes the positive ray test, so a component point could
not have this positive-coordinate translate outside `{P>0}`.  Separately,

```text
partial_a P(z)=-1240,
```

whereas derivative-component nesting makes every nonzero partial derivative
strictly positive on the component of `P`.

## Why the Gårding dependency applies

After deleting the marked edge `03`, the eight-edge graph is exactly `K4` on
vertices `{0,1,2,4}` together with the path `1-3-2`, parallel to the existing
edge `12`.  Matroidally it is obtained from `M(K4)` by adding a parallel copy
of `12` and subdividing that copy.  Fang--Ma's at-most-six-elements theorem,
duality, and series/parallel closure therefore make its cospanning generating
polynomial `C_M` Gårding.

The polynomial `P` in this campaign is `C_M` after the strictly positive
linear substitution which repeats one variable on each stabilizer orbit.
It is consequently a Gårding polynomial.  The external dependencies are:

- Fang--Ma, *Gårding polynomials*, arXiv:2604.27755v2, Definition 4.9 and
  Theorem 1.1 (positive affine pullback, PRT, and derivative nesting);
- Proposition 13.12 (series/parallel closure); and
- Theorem 13.13 plus duality (the `M(K4)` base).

Primary source: <https://arxiv.org/html/2604.27755>.

No convexity is used.  In fact the same source's Example 11.7 explicitly
shows that an ordinary Gårding component need not be convex.  Thus older
component exclusions based only on “C-Gårding implies convex” require a
separate stable/ideal-Gårding proof or must be treated as unresolved.

## New component inequalities

Exact forest reconstruction gives `P(1,1,1,1,1)=128` and
`xi(1,1,1,1,1)=58`.  The verifier then checks the five identities

```text
partial^(1,1,1,2,2) P = 8(a+1),
partial^(2,0,1,2,2) P = 8(b+1),
partial^(2,1,0,2,2) P = 8(c+1),
partial^(2,1,1,1,2) P = 8(d+1),
partial^(2,1,1,2,1) P = 8(e+1).
```

Therefore every component point satisfies

```text
a,b,c,d,e > -1.
```

Three more derivative channels are

```text
partial^(0,1,1,0,2) P = 2 q_ad(q_ad+2),  q_ad=ad+a+d,
partial^(0,1,1,2,0) P = 2 q_ae(q_ae+2),  q_ae=ae+a+e,
partial^(2,1,1,0,0) P = 2 q_de(q_de+2),  q_de=de+d+e.
```

They are positive throughout the connected component, and each `q` equals
`3` at the anchor.  Continuity excludes the other positive-product branch,
so

```text
ad+a+d>0,  ae+a+e>0,  de+d+e>0.
```

Finally `A=partial_b P>0` throughout the component.  Hence the distinguished
component never meets the `A=0` wall; the old `A`-wall route is only a
projection/topology diagnostic, not an internal component crossing.

## Second elimination

For `Delta=2a^2R`, exact elimination of `c` now gives

```text
Res_c(A,R)
 =2a^2d^4e^4(d+2)^2(e+2)^2(ad+a+d)(ae+a+e).
```

This is nonnegative under the component inequalities and is strictly
positive away from the exceptional coordinate locus `ade=0`.  It proves that
on the generic component domain an `R=0` wall cannot meet `A=0`.  It does
**not** prove that `R` has no zero with `A>0`, which is the remaining exact
fixed-space issue.

## Reproduction and scope

Run:

```sh
ulimit -v 524288
timeout 120s python3 evidence/verify_garding_prt_firewall.py
```

The verifier uses only the Python standard library, reconstructs all forests
instead of importing the inherited polynomial, and checks the displayed
identities over exact integers/rationals.

Mathematical status: the point exclusion and derivative identities are
author-verified exact results with a named primary-source dependency.  Full
fixed-space domination, the eight-variable host statement, the global
moving-edge interface, and OPG-1757 remain open.
