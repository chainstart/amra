# Independent audit: distinct-output expansion round six

## Verdict

The fixed-graph joint-legality lemma, conditional rank-four matching lemma,
and all three finite no-go searches reconstruct independently.  The
`w-y1,u-y2` exclusions are complete for colour-preserving one-old-edge
exchanges by the inherited `L4(2)` property.

There are two wording qualifications:

1. `M809O6-02` asserts existence in the general 15-new-edge model, while its
   6,435-case evidence exhausts only the symmetric subfamily containing all
   `w-X,u-X`.  The symmetric claim is strictly killed; the broader decisive
   wording is not.
2. `M809O6-12` is proved only after base and singleton rainbow legality are
   assumed.  Distinct output edges and owners alone are not sufficient, as
   the failed finite candidates themselves show.  It is correct if “switch”
   is explicitly defined to mean an individually legal switch in a legal
   base state.

The operational ledger has four killed mechanisms among nine non-survivors,
`4/9=44.4%`, already below the 80% gate.  Under literal statement matching,
only three kills are unqualified, so the strict audited ratio is at most
`3/9=33.3%`.  Either reading requires freeze.  No legal two-output witness,
all-branch output theorem, or public `1/8` progress is obtained.

The checker was written from the graph and prose model and imports no author
search functions or result files.

## 1. Locked graph and colour tests

The audit reconstructs the 14-vertex, 50-edge locked graph:

```text
A={v,x1,...,x4,y1,...,y4,r1,r2}
```

is complete except all `X-Y` edges and `x1x2,y1y2`; add `b-X`, `c-Y`,
`bz`, and `z-X`.  The four original repeated pairs are

```text
(b-x_i,c-y_i), i=1,...,4.
```

After adding `w,u`, the two switched pairs are

```text
(w-x1,c-y1), (u-x2,c-y2).
```

Since every other edge colour is unique, a state is non-rainbow exactly when
a C7 contains both edges of one active repeated pair.  Thus checking the
four base pairs and two switched pairs is equivalent to checking the base
state and both singleton states.  The joint state then follows from the
joint-legality lemma.

## 2. Joint-legality lemma

Consider one fixed graph and recolour disjoint repeated-colour classes.  If a
joint-state C7 is non-rainbow, it repeats some colour.  For a colour untouched
by both switches, the identical edge pair occurs in the base state.  For a
colour changed by switch `i`, disjointness means its joint-state edge pair is
identical to its pair in singleton state `i`.  The bad C7 would therefore
already be bad in one of the assumed rainbow states.

This proves `M809O6-01`.  It does not cover graph-changing switches, shared
colour classes, or a switch whose singleton state has not been proved legal.

## 3. Independent finite searches

The independent checker first lists all C7s containing each repeated edge
pair in the maximal graph.  Each cycle is stored only as its optional-new-edge
mask and old-edge mask.  A subset zeta transform then computes, for every
assignment, whether any bad cycle exists and the intersection of the old
edges across all bad cycles.  This is a different implementation from
candidate-by-candidate graph replay.

### Symmetric no-deletion model

Require all eight edges `w-X,u-X`; forbid

```text
vw,vu,cw,cu,wz,uz.
```

Exactly 15 allowed new edges remain optional.  Choosing seven gives

```text
C(15,7)=6435
```

65-edge graphs.  No assignment makes all six repeated pairs C7-safe.  This
strictly kills the symmetric no-deletion family.

It does not exhaust nonsymmetric 15-edge additions requiring only
`w-x1,u-x2`; this is the scope mismatch in `M809O6-02`.

### Symmetric one-exchange model

Choose eight of the same 15 optional edges, giving 16 new edges before one
old deletion.  For each of all

```text
C(15,8)=6435
```

assignments, intersect the old-edge sets of every bad C7.  The intersection
is empty in every case.  Therefore no old edge at all—not merely no
admissible edge—hits every bad C7.

### General natural one-exchange model

Require only `w-x1,u-x2` and forbid

```text
vw,vu,cw,cu,wz,uz,w-y1,u-y2.
```

There are 19 optional new edges.  Choosing 14 yields

```text
C(19,14)=11628
```

assignments with 16 new edges before deletion.  Again the common old-edge
intersection of all bad C7s is empty for every assignment.  Hence no one-old
edge exchange in this complete natural-switch model can make the base and
both singleton colourings rainbow.  L4(2), reserve and matching filters
cannot restore a candidate already failing this necessary colour condition.

This validates the finite core of `M809O6-03`, `M809O6-05` and
`M809O6-11` in the stated general natural-switch one-exchange model.  For
`M809O6-03`, its conditional wording is a literal refutation only when “the
pure model” means the preceding audited symmetric model; its consequent is
nevertheless independently false throughout the general one-exchange model.

No result here excludes two old deletions, 17 replacement edges, another
switch type, or a larger extension.

## 4. Why w-y1 and u-y2 are safely excluded

An admissible exchange must preserve the original repeated-colour edges;
otherwise the stated base and singleton colour models no longer exist.  Fix
such an old deletion `e` and suppose `w-y1` is added.

Choose an endpoint of `e` different from the desired endpoints `x1,c`.
The `L4(2)` property of the old graph, after deleting this vertex and `y1`,
supplies a four-edge `x1-c` path avoiding both `e` and `y1`.  Together with

```text
x1-w-y1-c
```

it forms a C7 containing the two switched `gamma1` edges `w-x1,c-y1`.
Thus the singleton is non-rainbow after every colour-preserving one-edge
deletion.  The `u-y2` argument is identical.

As an implementation-independent guard, the checker explicitly finds such a
four-path for each of the 42 old edges outside the eight protected repeated
pairs, for both switches.  Deleting `c-y1` or `c-y2` is not an exception to
the model; it is inadmissible because it destroys a required colour pair.

## 5. Conditional carrier matching

The frozen old carrier graph has four identical rows `{bc,cz}`, matching
rank two and maximum Hall deficiency two.  Conditional on legal arcs for two
different demands to distinct new outputs, the rows become

```text
{bc,cz,wz}, {bc,cz,uz}, {bc,cz}, {bc,cz}.
```

The explicit matching

```text
wz, uz, bc, cz
```

has size four.  Exact cut enumeration gives maximum deficiency zero.  This
proves `M809O6-06` and `M809O6-09` as conditional matching statements.  It
is an augmentation of the frozen n=14 `K_(4,2)` carrier graph; it does not
claim that merely adding vertices automatically leaves the canonical reserve
unchanged, and it constructs no legal arc.

## 6. Mechanism statement audit

- `M809O6-01`: **proved**, with fixed graph, legal base/singletons and
  disjoint recoloured classes explicit.
- `M809O6-02`: **symmetric subfamily strictly killed; decisive wording too
  broad**.  General nonsymmetric 15-edge addition was not enumerated.
- `M809O6-03`: **general one-exchange consequent strictly impossible**.
  The implication is a strict kill under the intended preceding symmetric
  no-go antecedent; its wording should name that antecedent.
- `M809O6-04`: **surviving**.  Finite traces exist, but no scalable or
  old-graph-independent obstruction-core theorem is proved.
- `M809O6-05`: **strictly killed** by complete unsatisfiability of the exact
  general one-exchange Boolean model.
- `M809O6-06`: **proved conditionally**; two distinct demand-output arcs give
  matching rank at least two, and the full ledger gives rank four.
- `M809O6-07`: **correctly frozen** because no first witness exists from
  which to extract an actual resource tensor.
- `M809O6-08`: **surviving**; the scalable overlap quantifier is outside all
  three finite searches.
- `M809O6-09`: **proved conditionally** by the explicit four-edge matching
  and all-cut enumeration.
- `M809O6-10`: **surviving**.  A general minimal-deficient-cut composition
  theorem is neither proved nor refuted by `K_(4,2)`.
- `M809O6-11`: **strictly killed** within the complete natural one-exchange
  model: every assignment has empty common old-edge intersection.
- `M809O6-12`: **proved only with an implicit legality hypothesis**.  After
  base and singleton legality, no extra consumable witness is needed.  As
  literally written, distinct owners and outputs alone are insufficient.

The three selected survivors are therefore genuine unclosed interfaces, but
none supplies a legal output in a public hard branch.

## 7. Gate and promotion

The stored operational statuses count four kills among the nine mechanisms
outside the three survivor slots, only `44.4%`.  The required ratio is 80%.
Moreover literal auditing qualifies `M02`, reducing the unqualified strict
kill count to three; `M12` also needs a hypothesis repair on the proved side.

The campaign must freeze at mechanism falsification.  Finite absence and
conditional allocation satisfy no frozen success condition.  The public
problem and coefficient `1/8` are unchanged.

No Lean was used.  Reproduction was bounded by 3 GiB and 180 seconds.

