# Parameterized natural-switch block-kernel theorem

## Family

For integers `m>=3` and `r>=0`, put

```text
X={x1,...,xm},  Y={y1,...,ym},  R={r1,...,rr}.
```

Take the round-8 construction verbatim with these block sizes: `A` consists
of `v,X,Y,R`; its only missing same-shore edges are `x1x2,y1y2`, and all
`X-Y` edges are absent.  The old outside vertices are `b,c,z`, with `b-X`,
`c-Y`, `bz,z-X`.  The repeated-colour pairs are

```text
(bxi,cyi), i=1,...,m;  (wx1,cy1);  (ux2,cy2).
```

The two switch vertices see every old vertex except `v,c,z`, with `wy1`
and `uy2` also forbidden.  In the colour-legal branch delete `bu,bw,uw`.
As before, admissible old deletions exclude edges incident with `v` and all
displayed repeated-colour edges.  Let `H(m,r)` be the hypergraph of their
intersections with bad `C7`s.

## First necessary condition: the three missing switch edges are forced

If any one of `uw,bw,bu` is restored, a bad `C7` has empty admissible-old
trace.  Uniform witnesses (valid for every `m>=3,r>=0`) are

```text
uw: w-x1-v-y1-c-y3-u-w,
bw: b-x1-u-y1-c-y2-w-b,
bu: b-x1-v-y1-c-y3-u-b.
```

Each cycle contains the indicated repeated-colour pair and otherwise only
new, `v`-incident, or repeated-colour old edges.  Hence no admissible old
deletion can repair it.  Thus every colour-legal branch in this architecture
must omit all three edges; the round-7 “unique unprotected assignment” is
not an accident of `m=4,r=2`.

## Exact parameterized kernel

Write `P={x1,x2}`, `Q=X-P`, `U={y1,y2}`, and `W=Y-U`.  In the branch omitting
`bu,bw,uw`, the singleton traces are exactly

```text
F(m,r) = R x (P union U union W)
       union P x Q
       union U x W
       union K(W).
```

Moreover every trace of `H(m,r)` meets `F(m,r)`.  Since each member of `F`
itself occurs as a singleton trace,

```text
tau(H(m,r)) = |F(m,r)|
            = r(m+2) + (m-2)(m+5)/2.
```

This specializes to `2*6+2*9/2=21` at `(m,r)=(4,2)` and explains the
round-8 `12+4+4+1` decomposition as one point on an infinite formula.

## Completeness of the symbolic support reduction

A bad seven-cycle contains the four endpoints of one displayed
repeated-colour pair, leaving only three other vertices.  The graph is
invariant under relabelling `R` and under simultaneous relabelling of the
generic paired indices `i>=3`.  Therefore any proposed extra singleton,
missing formula singleton, or trace disjoint from `F` relabels into an
instance with

```text
3 <= m <= 6,  0 <= r <= 3.
```

Conversely witnesses in a support representative embed into every larger
instance with the same orbit data.  The verifier reconstructs all simple
seven-cycles for all sixteen support representatives and checks exact
singleton equality and the hitting property.  Thus the computation is a
complete finite orbit-support proof, not extrapolation from selected sizes.

## Scope

This theorem covers an infinite parameterized natural-switch architecture,
but the canonical hard normal form does not force an arbitrary hard graph
to realize this architecture.  In particular it neither proves the public
`F_3(n)~n^2/8` statement nor changes its leading constant.  What it closes
is the previously missing lift from the locked 16-vertex singleton kernel
to all block sizes inside the exact same labelled switch interface.
