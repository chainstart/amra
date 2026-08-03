# K5-e three-variable slice: exact D/L/T wall audit

Date: 2026-08-03

Superseded status: the ambient connectivity gap isolated below is closed by
`K5_MINUS_EDGE_UPPER_ROOT_THEOREM.md`.  This file remains as the exact wall
reduction record.

Scope: only the stabilizer specialization with orbit variables `(a,b,c)` from
`K5_MINUS_EDGE_HIGH_TRIANGLE_STABILIZER.md`.  This is not a statement about
the eight-independent-variable polynomial and does not close the campaign's
global interface.

Let `P=bF`, `xi=bG`.  Since `b=1` at the anchor and `P>0` on its distinguished
component, `b>0` there.  Put

```text
L = bc+b+2c,
D = bc^2+2bc+2b+2c^2+4c,
K = bc+b+c+2,
T = 4aK+L(L+4).
```

Exact pseudo-division in `a` gives

```text
prem_a(F,G) = -b^2 L^2 T,       lc_a(G)=2D.
```

Consequently, on `G=0`, away from `D L=0`,

```text
2 D F = -b^2 L^2 T.             (1)
```

At `(a,b,c)=(1,1,1)`, `(D,T,L)=(11,52,4)`.

## The D wall reduces to one connected candidate strip

Write `q=c+1`.  Then

```text
D=(b+2)q^2+b-2.
```

Thus `D=0,b>0` has the single rational parametrization

```text
b=2(1-q^2)/(1+q^2),  c=q-1,  -1<q<1.
```

On this wall the sign of `F` is the sign of

```text
S(a,q)=-(q+1)^3 a^2 +(q^4-2q^2-4q+1)a +(q-1)^2(q+1).
```

Its discriminant is

```text
(q^2+1)^2 ((q^2-1)^2+4) > 0.
```

Since the leading coefficient is negative, `F>0` is the connected open strip
between the two continuous roots of `S`.  It meets `b=1` at
`q=1/sqrt(3),a=0`; there

```text
F=7-4sqrt(3)>0,
u+v=(-4+2sqrt(3))/3<0,
uv=(7-4sqrt(3))/15>0.
```

Hence `u<0,v<0`.  The complete `b=1` classification places this trace point
in the non-anchor chamber of that slice.

This does **not** by itself prove ambient non-connectivity: the two chambers
of the `b=1` section could reconnect through `b != 1`.  What is proved is the
sharp reduction that all of `D=0,F>0,b>0` is one connected candidate strip;
one ambient connectivity decision settles the whole `D` wall.

## The L wall is harmless and is actually anchor-reachable

For `L=0`, namely `c=-b/(b+2)`, exact substitution gives

```text
F=G=2a^2 b^2/(b+2),
D=b^2/(b+2),
T=4a(3b+4)/(b+2).
```

Thus no point of `L=0,F>0` lies on `G=0`.  This is not a separating wall:
the path `a=b=1`, `c:1 -> -1/3` stays in `P>0` and reaches its `a>0`
sheet.  (On this path `P=2(27c^2+32c+8)` and its first root below `1`
is strictly less than `-1/3`.)

## The T wall reduces to three connected candidate sheets

For `K != 0`, solve `T=0` as `a=-L(L+4)/(4K)`.  Substitution gives

```text
G = L^2 D H/(8K^2),
F = (b+2)L^2 H J/(16K^2),
H = (b+2)^2 q^2-4bq-4,
J = (b^2+2b+2)q^2-2.
```

For `b>0`, `K=0` cannot occur together with `T=0`: it would require
`L=0` or `L=-4`, giving respectively `b=-4/3` or `b=0`.

Let

```text
j  = sqrt(2/(b^2+2b+2)),
h- = -2/(sqrt(2b^2+4b+4)+b),
h+ =  2(sqrt(2b^2+4b+4)+b)/(b+2)^2.
```

The exact root ordering is

```text
-j < h- < 0 < j < h+.
```

It follows that `T=0,F>0` consists of three connected sheets:

```text
q < -j,       h- < q < j,       q > h+.
```

The possible pole `K=0`, at `q=-1/(b+1)`, lies in the omitted gap
`(-j,h-)`; the zero `L=0`, at `q=2/(b+2)`, lies in the omitted gap
`(j,h+)`.  The inequalities follow by squaring positive quantities; the
checker records their reduced polynomial differences.

Every sheet meets `b=1`.  Representatives `(a,c)` are respectively

```text
(5/4,-2),  (1,-1),  (-5/12,0).
```

At these points the `b=1` wall coordinates are

```text
(-35+sqrt(10))/12, (-35-sqrt(10))/12;
-2/3-sqrt(10)/15, -2/3+sqrt(10)/15;
-1/12+sqrt(10)/60, -1/12-sqrt(10)/60.
```

Both entries in every pair are negative.  Thus every sheet has a trace in the
non-anchor chamber of the `b=1` section.  As for the `D` wall, this slice
trace is not an ambient separation proof.

The degenerate intersections are consistent with this classification:

* `L=T=0` forces `a=0`, hence `F=0`.
* Away from `D L=0`, `T=G=0` forces `H=0`, hence `F=0`.
* On `D=T=G=0`, the parametrization above gives
  `sign(F)=sign(C(q))`, where `C(q)=2q^3-q^2+2q+1`.  Its derivative is
  strictly positive and it has one root `rho` in `(-1,0)`.  Hence the
  `F>0` part is exactly `rho<q<1`.  It joins the `D` strip to the central
  `T` sheet (`h-<q<j`), so those are one candidate rather than two.

## Exact remaining connectivity problem

The attempted wall proof does not yet close, because a non-anchor trace in
the `b=1` section is not a certificate of non-connectivity in the full
three-variable `F>0` set.  No grid extension is needed: the unresolved set
has reduced to three explicit connected candidates:

1. the single `D=0,F>0` strip together with the central `T` sheet, joined
   along `rho<q<1` as above;
2. the left outer `T` sheet `q<-j`;
3. the right outer `T` sheet `q>h+`.

The `L` wall contributes no candidate zero and is anchor-reachable with
`G>0`.  If the three candidates can each be separated from the anchor
component, then (1) closes the slice theorem.  If any one is anchor-reachable,
an explicit path to that sheet is the minimal next object; its `G` sign then
decides whether it opens a route to the `DT<0` zero-locus cell.

This is only a local stabilizer-slice reduction and does not change the
campaign phase or its global closure contract.
