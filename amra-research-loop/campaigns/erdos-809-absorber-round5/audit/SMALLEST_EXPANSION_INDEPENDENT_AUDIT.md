# Independent audit: round-five smallest expansion

## Verdict

The finite `n=15` certificate reconstructs independently.  The named graph
has 57 edges, satisfies all 9,660 `L4(2)` endpoint/deletion checks, has
`K(bc)={bc,cw,cz}` and `K(cw)={bc,cw,cz,wz}`, and contains exactly 128
simple length-four and 608 simple length-five `w--z` paths.  Every one of
the 15 nonempty subsets of the four named switches has an explicit
non-rainbow C7 witness.  A streaming pass through all
`C(13,7)=1,716` threshold expansions finds no instance with two individually
rainbow natural switches to `K(cw)\K(bc)`.

This certifies the finite **natural-switch firewall**.  It does not certify
the mechanism ledger's nine entries as strict literal kills.  Their scoped
kill-test prose mostly records useful route obstructions, while their
decisive claims quantify over wider graph operations, actual absorbers,
conditional legal switches, or asymptotic exceptional sets.  The formal
kill-ratio gate therefore fails without repairing those claims or weakening
their statuses.

The checker was written from the public prose construction and imports no
author enumerator or generated author evidence.

## Exact reconstruction

Start with

```text
A={v,x1,...,x4,y1,...,y4,r1,r2}, B0={b,c,z}.
```

Inside `A`, retain every edge except all `X--Y` edges and `x1x2,y1y2`.
Add `b--X`, `c--Y`, `bz`, and `z--X`.  This gives the frozen 14-vertex,
50-edge graph.  Add `w` with

```text
N(w)={b,r1,r2,x1,x2,x3,x4}.
```

The resulting graph has 15 vertices and 57 edges, while `vw` remains absent,
so `A=N[v]`.  Independent enumeration gives 21,508 undirected C7s, all
rainbow under the original four repeated colours, and all 9,660 `L4(2)`
checks pass.

On `B={b,c,z,w}`, direct reserve reconstruction gives

```text
K(bc)={bc,cw,cz},
K(cw)={bc,cw,cz,wz}.
```

Thus `wz` is the unique new output.  Direct simple-path enumeration gives
128 length-four and 608 length-five paths between its endpoints: 736 path
witnesses project to one output.

The label “first expansion” depends on an unstated enumeration order.  The
audit verifies the claimed named expansion but does not treat “first” as a
mathematical invariant.  Under the checker's explicitly declared old-vertex
order, a different valid neighbourhood is encountered earlier.

## Switch firewall

For switch `i`, move colour `gamma_i` from `b-x_i` to `w-x_i`, retaining
`c-y_i`.  Exact C7 search supplies a non-rainbow witness for every nonempty
subset of the four switches.  For example, switch 1 creates

```text
w-x1-r1-y1-c-y2-r2-w,
```

which contains both `w-x1` and `c-y1` in colour `gamma_1`.  Hence none of
the 15 nonempty states is legal and the named catalogue has zero legal
absorbers.

For the exhaustive check, choose seven neighbours of `w` from the 13 old
vertices other than `v`.  The checker streams all 1,716 choices.  It finds
no target instance; indeed, after requiring the original colouring to be
rainbow and the new reserve difference to be nonempty, no expansion has even
one individually rainbow natural switch.  This absence holds before an
`L4(2)` filter, so imposing `L4(2)` cannot create a target.

## Mechanism-statement audit

The evidence-policy distinction between a strict counterexample and a
failed proposed construction is decisive here.

- `M809R5-01`: the test exhausts four natural replacements, not every
  one-demand graph operation asserted by the decisive claim.  Route
  obstruction, not strict kill.
- `M809R5-02`: the claim assumes individually legal switches.  The named
  graph has none, so the antecedent is absent.  Not a strict kill.
- `M809R5-03`: 736 finite paths over one output correctly refute an
  unqualified pre-projection count, but do not instantiate the stated
  asymptotic “power-large local switch witness” hypothesis.  Qualified
  route obstruction.
- `M809R5-05`: the decisive claim concerns an **actual absorber**
  hypergraph.  The tested paths and switches are explicitly not actual
  absorbers.  The test exposes a mandatory codegree interface but does not
  refute the literal claim.
- `M809R5-07`: likewise, no family of compatible graph-realizable absorber
  certificates is present, so the proposed matroid representation has not
  been instantiated.  Not a strict kill.
- `M809R5-08`: deleting the natural transitions proves that this specified
  network has no linkage.  It does not show that every complete legal-switch
  network allowed by the broad decisive wording has been enumerated.
  Qualified route obstruction.
- `M809R5-09`: deleting one vertex at `n=15` does not instantiate an
  asymptotic `o(n)` rank-preservation statement.  Not a strict kill.
- `M809R5-10`: only natural one-vertex links are exhausted; the decisive
  claim quantifies over all graph-legal exceptional links.  Qualified route
  obstruction.
- `M809R5-12`: the claim assumes a legal external first switch.  The example
  has none, so it cannot refute the conditional iteration statement.

Thus the campaign contains nine well-scoped negative tests but zero strict
literal refutations of the decisive claims as currently worded.  Since the
gate requires at least 80% of non-survivors to be strictly killed, the
reported `9 killed / 3 surviving` ledger is not audit-ready.  The three
survivors remain merely conditional and unproved.

## Scope

The result is finite exact evidence for one expansion model and one typed
switch.  It neither excludes larger or different gadgets nor constructs a
post-projection reservoir, proves a bounded-overlap matching theorem, closes
the public problem, or changes coefficient `1/8`.

No Lean was used.  Reproduction uses the campaign's 3 GiB / 180 second
bounded wrapper.

