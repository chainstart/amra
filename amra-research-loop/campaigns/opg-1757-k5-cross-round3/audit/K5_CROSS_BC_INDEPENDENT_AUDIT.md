# Independent audit: K5-e marked-cross-edge `(b,c)` component

Auditor: root, author-swapped from `erdos776_lane`.

The audit checker was written from the graph definition and imports no author
checker or generated data.  It independently enumerates every subset of the
eight unmarked edges of `K5-{34,03}`, rejects cycles with a disjoint-set
calculation, and tests endpoint connectivity of `0,3` directly.

It reproduces 128 forests and 58 endpoint-connected forests, then reconstructs
on `a=d=e=1`

```text
P  = 54bc+27b+32c+15,
xi = 22bc+12b+16c+8.
```

Under `x=54b+32`, `y=c+1/2`, it independently obtains
`P=xy-1` and `54xi=22xy+x+160y-32`.  Since the positive anchor maps into
`x>0,y>0,xy>1`, and the two components of `xy>1` are distinguished by the
signs of `x,y`, this is exactly the anchor component.  There
`y>1/x`, so

```text
54xi > x+160/x-10 = (x-5)^2/x+135/x > 0.
```

The statement therefore passes exactly for the two-variable stabilizer slice.
It gives no control over the other three fixed-space variables or the three
transverse edge directions, and does not prove G201 or OPG-1757.  Priority is
not checked.
