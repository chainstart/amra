# Independent audit: triangular-prism vertical stabilizer

## Verdict

PASS for the complete three-variable stabilizer specialization of a marked
vertical edge of the triangular prism.

Independent complement-of-forest enumeration gives 180 deletion forests and
46 endpoint-connected forests.  All three polynomial identities reconstruct
exactly.  The distinguished-component equality, strict AM-GM step for `V`,
and the exceptional case `A=0` are logically sound.

The result closes only the vertical-edge orbit after identifying the eight
unmarked activities into the marked-edge stabilizer's three orbits.  It does
not treat the triangle-edge orbit, eight independent activities, G201, the
global moving-edge lemma, or OPG-1757.

The checker imports neither the author verifier nor its result.

## 1. Independent graph and forest sums

Use triangular faces `012` and `345` and vertical matching
`03,14,25`.  Delete the marked vertical edge `03`.  Its stabilizer orbits on
the remaining edges are

```text
a: 14,25                         (size 2),
b: 01,02,34,35                   (size 4),
c: 12,45                         (size 2).
```

For every acyclic selected edge set, the deletion polynomial receives the
monomial formed by the complementary edge activities.  Restricting to
forests that already connect `0` and `3` gives `xi`.

The blind disjoint-set enumeration obtains:

| selected edges | all forests | endpoint-connected |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 8 | 0 |
| 2 | 28 | 0 |
| 3 | 54 | 2 |
| 4 | 59 | 14 |
| 5 | 30 | 30 |
| total | 180 | 46 |

Thus the anchor values at `a=b=c=1` are exactly 180 and 46.

## 2. Polynomial identities

After `x=a+1,y=b+1,z=c+1`, direct expansion of the reconstructed sums gives

```text
T=y^2 z-1,          V=y^2+z-2,
A=y(z+1)-2,         B=2y+z-3,

P=(xT)^2-V^2,
xi=2(xA^2-B^2).
```

Independent symbolic expansion also gives the exact barrier

```text
V A^2-T B^2=(y-1)^4(z-1)^2.
```

At `(x,y,z)=(2,2,2)`, the audit finds

```text
T=7, V=4, P=180, xi=46.
```

## 3. Distinguished component

Let `C` be the component of `{P>0}` containing `(2,2,2)`.  Since

```text
P>0 iff |xT|>|V|,
```

the anchor lies in the open branch `xT>|V|`.  This strict branch cannot
change inside a connected component without reaching `P=0`.  Consequently
`xT>0` throughout `C`.  Neither factor can cross zero, and both are positive
at the anchor, so `x>0,T>0` on `C`.

Now `T=y^2z-1>0` implies `y^2z>1`; hence `z>0` and `y` is nonzero.  Its sign
cannot change on `C`, so the positive anchor gives `y>0`.

Conversely, on the base

```text
y>0, z>0, y^2z>1,
```

the logarithmic coordinates satisfy the open linear inequality

```text
2 log y+log z>0.
```

The base is therefore path connected.  AM-GM gives

```text
y^2+z >= 2y sqrt(z).
```

Because `y^2z>1` and all factors are positive, `y sqrt(z)>1`; hence the
inequality is strict after subtracting two:

```text
V=y^2+z-2>0.
```

With `T>0`, the anchor branch is exactly

```text
x>V/T.
```

This is the open epigraph of a continuous function over the log-convex base.
It is path connected: lift any base path above the maximum of `V/T` along
its compact image, traverse it, and lower vertically.  It contains the
anchor and every point of `C`; conversely every point in it has `P>0` and
connects to the anchor.  Thus it is exactly the distinguished component.

## 4. Barrier and the A=0 exception

Divide the barrier identity by positive `T` on `C`:

```text
(V/T)A^2-B^2 >= 0.
```

It remains essential to know `A!=0`, since otherwise the strict inequality
`x>V/T` would not become strict after multiplication by `A^2`.

If `A=0`, the undivided identity reads

```text
-T B^2=(y-1)^4(z-1)^2.
```

The left side is nonpositive and the right side nonnegative.  Equality
forces `B=0` and `y=1` or `z=1`.  If `y=1`, then
`A=z-1=0`, so `z=1`.  If `z=1`, then `A=2(y-1)=0`, so again `y=1`.
But `(y,z)=(1,1)` gives `T=0`, contradicting the component condition.
Therefore `A!=0`.

Finally,

```text
xA^2>(V/T)A^2>=B^2,
```

so `xi=2(xA^2-B^2)>0` throughout `C`.

## 5. Scope

The prism has two graph-edge orbits: vertical and triangle.  Edge symmetry
transfers this certificate among the three vertical edges only.  No claim is
made for a marked triangle edge.  Moreover the polynomial proof relies on
the three stabilizer identifications `2+4+2`; it is not an eight-variable
domination theorem.

No G201 or public status was changed.  No Lean was used.  Reproduction was
bounded by 2 GiB and 120 seconds.

