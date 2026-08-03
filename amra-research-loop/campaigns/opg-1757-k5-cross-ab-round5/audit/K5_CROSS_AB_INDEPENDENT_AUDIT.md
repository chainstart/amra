# Independent audit: K5-e marked-cross-edge `(a,b)` component

Auditor: root, author-swapped graph-definition reconstruction.

An independent disjoint-set enumeration of `K5-{34,03}` reproduces 128
forests, 58 endpoint-connected forests, the four displayed coefficient
polynomials, and anchor values `P=128`, `xi=58`.

At `beta=-1+sqrt(10)/4`, `A=0` and `C=22-7sqrt(10)<0`; hence the vertical
line is absent from `P>0`.  Above it, `A>0`, and the epigraph `b>-C/A` is
connected and contains the anchor, proving the complete component statement.
The independent identity

```text
A xi/2 = D P + a^2(120a^2+48a+5)
```

has `D>0` there because `-3/14<beta`.  The quadratic has discriminant `-96`
and positive leading coefficient.  Thus every term on the right is
nonnegative and `DP` is strict, proving `xi>0` throughout.

Statement and dependencies pass only for `c=d=e=1`.  The remaining fixed
variables, transverse directions, G201 and OPG-1757 remain open; priority is
uncertain.
