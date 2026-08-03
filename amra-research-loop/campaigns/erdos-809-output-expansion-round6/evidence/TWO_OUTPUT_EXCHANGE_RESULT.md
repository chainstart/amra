# Two-output natural-switch and edge-exchange result

## Typed target

Start from the locked `n=14` graph and add two B vertices `w,u`.  The two
natural switches are

```text
gamma1: (b-x1,c-y1) -> (w-x1,c-y1),
gamma2: (b-x2,c-y2) -> (u-x2,c-y2).
```

The intended distinct outputs are `wz` and `uz`.  They are required to be
missing and outside the old `K(bc)`, while belonging to `K(cw)` and `K(cu)`
after the corresponding switch.

Every graph remains at the exact threshold: `n=16`, `e=65`.  Edges incident
with `v` are not changed, so `A=N[v]` is retained.  A candidate is accepted
only after exact C7, reserve, matching and full `L4(2)` replay.

## Joint legality lemma

For fixed-graph recolourings of disjoint colour classes, the base state and
the two singleton states being rainbow already imply joint legality.

Indeed, a non-rainbow joint C7 repeats some colour.  If it is `gamma1` or
`gamma2`, the same repeated edge pair appears in the corresponding singleton
state.  If it is an untouched colour, the same pair appears in the base
state.  Each possibility contradicts one of the hypotheses.

Thus joint replay remains an important implementation check, but it consumes
no extra graph resource in this precise recolouring model.  This statement
does not cover switches that add/delete graph edges or share a colour class.

## Exact finite searches

Three complete finite searches were run.

1. In the symmetric no-deletion family, add all eight edges `w-X,u-X` and
   choose seven of the fifteen remaining allowed incident edges.  None of the
   `C(15,7)=6435` assignments keeps all four base repeated pairs and the two
   switched pairs C7-safe.
2. In the same symmetric family with one exchange, choose eight optional
   edges and delete one admissible old edge.  For all 6,435 assignments, no
   single old edge meets every bad C7.
3. In the general natural-switch one-exchange family, require only `w-x1`
   and `u-x2`, choose fourteen of nineteen remaining allowed new edges, and
   delete one admissible old edge.  All 11,628 assignments again have no one
   old edge hitting every bad C7.
The edges `w-y1` and `u-y2` are soundly excluded from the last search.  For
example, if `w-y1` were present, `L4(2)` supplies a four-edge path from `x1`
to `c` after deleting `w,y1`; together with `x1-w-y1-c` this is a non-rainbow
C7 containing both switched `gamma1` edges.  The `u-y2` case is identical.

These are literal finite no-go results for the stated models.  They do not
exclude two or more old-edge deletions, a different graph operation, or a
larger extension.

## Conditional rank ledger

If two legal arcs to distinct outputs were constructed for two different
demands, the locked carrier graph would change from four identical
neighbourhoods `{bc,cz}` to

```text
{bc,cz,wz}, {bc,cz,uz}, {bc,cz}, {bc,cz}.
```

It has the explicit matching `wz,uz,bc,cz`, hence rank four and deficiency
zero.  This is exact allocation after construction; it constructs neither
switch.

## Status

No two-output legal witness was found.  The finite no-go and conditional
matching lemma do not change the public `1/8` statement.  Python searches
used 3 GiB/180 seconds; no Lean process was used.
