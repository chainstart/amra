# Independent audit: round-four locked carriers

## Verdict

The n=14 graph certificate and the locked-circuit external-carrier theorem
reconstruct independently.  Six of the claimed strict mechanism kills match
their literal decisive statements.  Two—M809R4-02 and M809R4-05—capture valid
route obstructions but need statement repairs before they qualify as strict
literal refutations.

The two surviving mechanisms remain conditional and unproved.  Nothing here
constructs an external carrier, closes the outer-A interface, or changes the
public `1/8` term.

The checker was written from the prose graph description.  It imports neither
the author checker nor its generated evidence.

## 1. Full graph reconstruction

Use

```text
A={v,x1,...,x4,y1,...,y4,r1,r2},  B={b,c,z}.
```

Inside `A`, take the complete graph except all `X--Y` pairs and
`x1x2,y1y2`.  Add `b--X`, `c--Y`, `bz`, and `z--X`.  The independent
enumeration obtains:

- `n=14`, `e=50=floor(14^2/4)+1`;
- minimum and maximum degrees 4 and 10;
- `A=N[v]`;
- all 7,189 endpoint/deletion cases required by `L4(2)` pass;
- exactly 11,136 undirected seven-cycles.

For each `i=1,...,4`, colour `bxi` and `cyi` alike and give every other edge
a fresh colour.  Exact cycle enumeration finds no repeated colour on any C7,
so every C7 is rainbow.  The four diagonals `xiyi` are distinct missing
A-edges.  The colouring uses 46 colours and is route-level evidence only,
not a public counterexample.

On `B`, only `bz` is present.  Hence all missing B-edges are exactly

```text
{bc,cz}.
```

Direct canonical-reserve reconstruction gives `K(bc)={bc,cz}`.

## 2. Locked realization

The four repeated colours give four demands with the same two-point outer
support `{b,c}`.  Choosing either endpoint as root always produces the same
unordered base `bc`; all `2^4=16` simultaneous root states therefore retain
the identical neighbourhood `K(bc)`.

The carrier incidence graph is `K_(4,2)`.  Independent matching DP and direct
Hall-cut enumeration give rank two and maximum deficiency two.  Its four
three-demand subsets are precisely the inclusion-minimal deficient cuts.
They cross, while every demand pair has codegree two, equal to each
individual degree.

There is no missing B-edge outside `K(bc)`.  Thus this graph supplies no free
external actual carrier and no root rotation can change that fact.

## 3. Locked-circuit theorem

Let `d` demands all have the same two-point support and give each its full
canonical-reserve neighbourhood `K(e)`, of size `k`.  Base determinism makes
the incidence graph the complete bipartite graph `K_(d,k)`.  Therefore

```text
rank = min(d,k),   deficiency = d-rank = max(0,d-k).
```

The audit checks this independently for every `0<=d,k<=8`; the natural proof
is immediate from injective pairing of the smaller shore.

Root reversal leaves `e` unchanged.  Alternating rematching changes only a
matching inside the same graph; cut uncrossing only renames demand subsets;
sampling existing arcs can only delete arcs.  None can increase the rank of
the underlying incidence graph.

If `d>k`, a saturating matching uses `d` distinct right vertices, at most `k`
of which lie in `K(e)`.  It consequently requires at least `d-k` distinct
right vertices outside `K(e)`.  To count as actual carriers, these must be
concrete missing B-edges in the original graph with graph-proved legal arcs.
After they are constructed, saturation is still equivalent to every
augmented Hall cut.  This is necessity, not a carrier-creation theorem.

## 4. Statement match for the eight claimed kills

The following six are strict literal matches:

- `M809R4-01`: a minimal deficient triple has no free actual sink, so the
  asserted universal path cannot exist.
- `M809R4-03`: four owned A diagonals exist, but there is no B-edge outside
  the occupied full reserve.
- `M809R4-06`: positive deficiency coexists with zero capacity to a free
  actual-carrier sink.
- `M809R4-07`: all 16 root states preserve rank and reserve.
- `M809R4-08`: crossing minimal circuits exist and no leaf rotation can
  release an external edge.
- `M809R4-09`: codegree two is greater than half of degree two.

Two require qualifications:

- `M809R4-02`: the graph proves that a root reversal revisits the identical
  carrier neighbourhood with a different **root state**.  The decisive claim
  says “different ownership state.”  This is a strict kill only after the
  representation explicitly defines the chosen root as part of ownership
  state.  The carrier-state visit-once heuristic is refuted, but the present
  wording does not itself establish a changed owner.
- `M809R4-05`: the graph does refute the intended inference that each A owner
  creates a new B ground element or raises B saturation rank.  Literally,
  however, matchable subsets of the two-element ground set `{bc,cz}` form the
  uniform matroid, and its nonmaximal independent sets can be extended by an
  existing B element.  The full two-element set is already maximal.  Since
  an A diagonal is not an element of the declared B-edge ground set, the
  proposed A-to-B basis extension map is ill-typed rather than literally
  falsified by “rank four versus rank two.”  The mechanism statement should
  name the claimed graph operation and the nonmaximal rank notion.

Accordingly the audit does not certify the summary phrase “eight strict
kills” as written: it certifies six strict kills and two intended-route
obstructions requiring repaired statements.

## 5. Survivor boundaries

`M809R4-04` is not killed by this graph because the graph contains no actual
absorber catalogue, so its catalogue-size antecedent is absent.  It is not
proved either.  Moreover, the decisive claim as written says only “twice as
many certificates”; count alone does not imply disjoint absorbers when
outputs or witness edges overlap.  A valid survivor theorem must state and
prove a bounded-degree/codegree hypothesis and then output external legal
edges.

`M809R4-10` is also not killed: this graph has two actual carriers for four
demands and misses its carrier-rich antecedent.  But total actual-carrier
count is not by itself a cut-expansion hypothesis; unrelated carriers can
leave a locked cut untouched.  The survivor must prove legal neighbourhood
expansion beyond every relevant `K(e)`, contraction of maximum Hall
deficiency, and deterministic cleanup.

Neither survivor currently creates even one carrier on the locked graph or
connects to every public hard branch.

## 6. Scope

This is an independently reconstructed local negative interface lemma.  It
does not prove a carrier-creation theorem, the outer-A gate, the full public
asymptotic, or any change to coefficient `1/8`.

No Lean was used.  Reproduction:

- `audit/verify_carrier_round4_independent.py`, SHA-256
  `e6e183ef73ef8ad4fa531bdf2b8a3845f69ab972b90707b0f9765678c5a6e5fb`
- `audit/CARRIER_ROUND4_INDEPENDENT_AUDIT.json`, SHA-256
  `0a8b55646fecb99131f732cf5ebabebfb49ca5fafd7be00b5e3076bd4c2da15e`

```sh
ulimit -v 2097152
timeout 120s python3 audit/verify_carrier_round4_independent.py
```
