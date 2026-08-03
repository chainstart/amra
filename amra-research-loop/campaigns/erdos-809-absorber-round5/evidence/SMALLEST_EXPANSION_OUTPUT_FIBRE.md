# Smallest-expansion absorber/output-fibre test

## Exact model

Start with the frozen `n=14`, 50-edge locked graph.  Add one new B vertex
`w`, retain `v-w` as a nonedge so that `A=N[v]`, and add exactly seven edges
incident with `w`.  This is the smallest vertex expansion at the exact
threshold, since

`floor(15^2/4)+1 - (floor(14^2/4)+1) = 57-50 = 7`.

The first expansion passing the original colouring's rainbow-C7 condition,
`L4(2)`, and possessing a missing B-edge outside `K(bc)` has

`N(w)={b,r1,r2,x1,x2,x3,x4}`.

Its exact reserves are

`K(bc)={bc,cw,cz}` and `K(cw)={bc,cw,cz,wz}`.

Thus `wz` is a concrete missing B-edge outside the old reserve.  It has 128
simple length-four paths and 608 simple length-five paths in the same graph.
This is already a large graph-realizable path catalogue over one output.

## Legality firewall

For each repeated colour `gamma_i`, the natural smallest switch replaces
the edge `b-x_i` by `w-x_i` while retaining `c-y_i`.  The base would change
from `bc` to `cw`, making `wz` canonical in the new reserve.

Exact C7 enumeration rejects every nonempty subset of these four switches:
each switched colouring has a non-rainbow C7.  Therefore the four gadgets
are candidates, not legal arcs, and the 736 paths are witnesses, not
absorbers.  The legal-absorber count in this example is zero.

A second pass exhausts all `C(13,7)=1716` one-vertex threshold expansions
of this form.  None has two individually rainbow natural switches whose new
reserve `K(cw)` reaches an output in `K(cw)\K(bc)`.  This is complete only
for the stated one-vertex model and switch type.

## Consequence

The attempted stronger counterexample—many *legal* actual absorbers with
rank one—was not found at the smallest expansion.  What is proved is the
earlier firewall that must precede it:

1. existence of an external missing B-edge does not give a legal arc;
2. graph-path and candidate-gadget counts do not give absorber counts;
3. even after legality, certificate count must be projected to distinct
   outputs and all internal resources before a codegree or matching theorem.

This finite test neither constructs an absorber nor changes the public
`1/8` interface.

Reproduction uses 3 GiB and 180 seconds, with no Lean process:

```sh
AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/erdos-809-absorber-round5/evidence/small_expansion_search.py
```
