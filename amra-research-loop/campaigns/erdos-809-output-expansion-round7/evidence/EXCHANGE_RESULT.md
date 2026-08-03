# Exact two- and three-edge natural-switch exchange firewall

## Frozen model

The locked fourteen-vertex graph is extended by `w,u` in `B`.  The named
switch edges are `w-x1` and `u-x2`; the intended missing outputs are `w-z`
and `u-z`.  Edges `c-w,c-u,w-z,u-z` are absent by the typed reserve/output
model.  Edges `w-y1,u-y2` are absent necessarily: either one, together with
the corresponding switched repeated pair and an `L4(2)` path avoiding its
two internal vertices, creates a non-rainbow C7.

Old edges incident with `v` are not deletable because `A=N[v]` is frozen.
The eight old repeated-colour edges are not deletable because the four named
base colour classes are frozen.  Exactly thirty-two old edges remain
admissible.

## Exact transversal filter

For every bad C7, the program records its subset of admissible old edges.
For deletion-set size `d`, every `d`-subset of the thirty-two old edges is a
bit.  The mask for one bad C7 contains exactly the deletion sets meeting that
cycle.  Intersecting these masks over every bad C7 therefore returns exactly
the deletion sets that destroy every bad C7; it is neither a relaxation nor
a heuristic.

The implementation additionally searches all bad cycles needed to decide
whether a protected bad C7, containing no admissible old edge, exists.  Any
retained deletion set is independently replayed through the six repeated
pairs, the base and three switch states, full `L4(2)`, `K(bc),K(cw),K(cu)`,
the two canonical outputs, and matching rank.

## Binary reproduction

With seventeen new edges and two old deletions, there are
`C(19,15)=3876` new-edge assignments and `C(32,2)=496` deletion pairs per
assignment.  The result reproduces the earlier post-freeze calculation:
all 3,876 exact pair intersections are empty.  3,860 assignments contain a
protected bad C7; each remaining assignment has transversal number at least
three.

## New triple result

With eighteen new edges and three old deletions, there are
`C(19,16)=969` new-edge assignments and `C(32,3)=4960` deletion triples per
assignment, totaling 4,806,240 raw combinations.  All 969 exact triple
intersections are empty.  Of these, 968 contain a protected bad C7.  The
unique unprotected assignment omits `bu,bw,uw`; its bad-C7 hypergraph has
93 distinct traces, consisting of twenty-one singleton traces and seventy-two
three-edge traces.  The singleton traces force twenty-one distinct edges and
those edges hit every trace, so its transversal number is exactly 21.

No deletion triple reaches the later replay stages because no triple passes
their exact necessary C7 condition.  The zero replay counters must not be
read as failures caused by `L4(2)`, reserves, outputs, or matching.

For any fixed graph, hitting every bad C7 for the six displayed repeated
pairs is exactly equivalent to legality of the base and both singleton
states.  The joint state adds no extra obstruction because the two switches
use disjoint colour classes: a repeated colour in a bad joint C7 would
already be repeated in its singleton state, or in the base state for an
untouched colour.

Conditionally, if the two legal outputs were obtained, the locked four-demand
carrier neighbourhoods would be `{bc,cz,wz}`, `{bc,cz,uz}`, `{bc,cz}` and
`{bc,cz}`.  The explicit matching `wz,uz,bc,cz` has rank four.  This allocation
lemma does not construct either legal output.

## Reproduction and scope

From this campaign directory, run:

```text
ulimit -v 3145728; timeout 180s python3 evidence/exchange_search.py 2
ulimit -v 3145728; timeout 180s python3 evidence/exchange_search.py 3
ulimit -v 3145728; timeout 180s python3 evidence/verify_transversal_masks.py
```

The full searches completed in about 23 seconds and 6 seconds respectively.
The verifier fully replays all 496 pairs on three binary configurations and
64 deterministic triples on the unique unprotected triple configuration;
it is an implementation check, not the source of completeness.

This is a finite no-go for the displayed natural-switch model only.  It does
not exclude four old deletions with nineteen replacements, non-natural
switches, other extensions, or a scalable output-expansion theorem.  It does
not change the public `1/8` question.
