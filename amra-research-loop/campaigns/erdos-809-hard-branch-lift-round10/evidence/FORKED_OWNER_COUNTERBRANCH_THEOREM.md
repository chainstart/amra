# Forked-owner counterbranch theorem

## Minimal owner counterbranch

Start with the parameterized round-9 vertex blocks for `m>=3,r>=0`, but
replace the two independent switches by two mutually exclusive alternatives
on the same owner.  The base state has repeated pairs

```text
(b-x_i,c-y_i), i=1,...,m.
```

The two singleton states replace `b-x1` by `w-x1` or by `u-x1`, retaining
the same owner `c-y1`.  Both switch vertices have the round-9 local
adjacency interface, except that both forbid their edge to `y1`; as before
`bu,bw,uw` are omitted.  The permitted state complex consists of the base
and the two singleton alternatives.  There is no joint state because the
two alternatives consume the same owner.

This is minimal in the relevant sense: with one candidate there is no
independence question; with two candidates, two distinct owners give the
round-9 Boolean square, whereas one shared owner gives the first possible
rank-one fork.

## Exact forked-owner kernel

Let `Q=X-{x1,x2}`, `U={y1,y2}`, and `W=Y-U`.  Use exactly the old-edge
deletion domain of round 9.  The bad-C7 trace hypergraph for legality of all
three permitted states has singleton kernel

```text
F_fork = R x ({x1} union Y)
       union {x1} x Q
       union U x W
       union K(W).
```

Every trace has size one or three, and every trace meets `F_fork`.  Since
every member of `F_fork` itself occurs as a singleton trace,

```text
tau(H_fork)
 = |F_fork|
 = r(m+1) + (m-2)(m+3)/2.
```

The round-9 independent-owner value exceeds this by exactly `r+m-2`.
Those missing edges are

```text
R x {x2}  union  {x2} x Q,
```

precisely the block controlled by the second independent owner.  Thus the
five-block round-9 kernel is not invariant under owner collision.

## Legality and complete support

Deleting `F_fork` makes the base state and both singleton states C7-legal:
the set hits every trace, and deletion creates no cycle.  This is exact
state-by-state legality, not a candidate count.

For completeness, a bad C7 contains the four endpoints of one displayed
repeated pair and only three further vertices.  After fixing the special
indices `1,2` and a generic repeated index, simultaneous relabelling uses
at most indices `1,...,6` and at most three residual `R` vertices.  Hence
any extra singleton, missing formula singleton, empty trace, or trace
disjoint from `F_fork` descends to one of

```text
3 <= m <= 6,  0 <= r <= 3.
```

Conversely every formula edge orbit has a witness on its support and embeds
in all larger instances.  The exact verifier reconstructs all simple C7s
on these sixteen representatives, checks equality of the singleton set and
the displayed formula, and checks the hitting property.  This is a complete
orbit-support proof for every `m>=3,r>=0`, not a fixed census.

## Failure of the global reduction

An owner- and state-preserving map cannot send this fork to the round-9
two-owner Boolean architecture: the fork's owner-incidence matching rank is
one and its two-candidate face is absent, while round 9 has matching rank
two and contains the joint face.  A map that merely preserves block sizes
would invent an owner and a permitted state, and is not trace preserving.

Therefore the inherited hard normal form cannot imply the round-9
architecture without a new **distinct-owner Booleanity lemma**.  The frozen
normal form contains scalar reserve and star coordinates but no clause that
constructs two distinct owners or their compatible joint switch.

## Scope firewall

The fork is an exact infinite legal switch-state family and a counterbranch
to universality of the round-9 labelled architecture.  It is not proved to
arise at `floor(n^2/4)+1` edges, nor to be forced by a genuine public hard
counterexample.  Consequently it does not refute or prove
`F_3(n)~n^2/8`.  It identifies the first missing structural hypothesis:
distinct owner rank plus Boolean joint compatibility must be derived before
the round-9 kernel can be composed with arbitrary hard branches.

## Reproduction

```text
AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/erdos-809-hard-branch-lift-round10/evidence/verify_forked_owner_kernel.py
```
