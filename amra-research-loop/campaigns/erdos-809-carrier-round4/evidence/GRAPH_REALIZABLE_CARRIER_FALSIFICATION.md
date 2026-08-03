# Round-four graph-realizable carrier falsification

## Boundary

Every strict kill below is replayed on one labelled original graph, not on an
arbitrary demand--carrier incidence table.  The graph has 14 vertices and 50
edges, exactly `floor(14^2/4)+1`; its maximum-witness partition is
`A=N[v]` and `B={b,c,z}`.  Exact enumeration verifies minimum degree four,
`L4(2)`, and all 11,136 seven-cycles rainbow.

The four repeated colours are `b-x_i` and `c-y_i`, `1<=i<=4`.  Their owned
A-diagonals `x_i-y_i` are four distinct actual missing A-edges.  Every demand
has outer endpoint set `{b,c}`, hence base pair `bc`.  The exact zero-shore
reserve is

```text
K(bc) = {bc, cz} = all missing edges of G[B].
```

Thus four graph-realized demands have matching rank two and Hall deficiency
two.  Reversing any of the four roots gives 16 simultaneous root states, but
the unordered base and reserve are unchanged in every state.  No universal
dummy carrier is introduced.

## Exact kills

- `M809R4-01`: the root-state alternating component is terminal and contains
  no free actual B-edge.
- `M809R4-02`: root reversal changes the root state while returning to the
  identical carrier neighbourhood, refuting the simple visit-once forest.
- `M809R4-03`: four distinct A owners do not produce any B-edge outside the
  occupied reserve.
- `M809R4-05`: A ownership rank four does not extend the common-ground B rank
  two; the asserted exchange axiom fails.
- `M809R4-06`: Hall deficiency two coexists with zero path capacity to a free
  actual carrier, killing the universal gammoid min-cut lower bound.
- `M809R4-07`: all 16 actual root rotations preserve `K(bc)`, so minimal
  reserve circuits need not have a rank-increasing rotation.
- `M809R4-08`: the four three-demand subsets are minimal deficient circuits;
  two cross, but no legal rotation releases an edge.  Set-theoretic
  uncrossing therefore supplies no graph exchange.
- `M809R4-09`: pair codegree is two, equal to the full individual degree two,
  contradicting the claimed half-degree premise.

The same exact graph strengthens the inherited three-demand circuit: adding
the fourth repeated colour preserves the edge threshold, `L4(2)`, and the
rainbow-C7 property.  This is route-level negative evidence, not a public
counterexample; the colouring uses far more than the target number of
colours.

## Survivors

`M809R4-04` survives narrowly.  The countergraph contains no actual absorber
certificate, so it cannot refute a future theorem which first derives many
bounded-overlap absorbers from additional hard-branch geometry.

`M809R4-10` also survives its first strict test.  Its antecedent requires at
least as many actual carriers as demands, while the exact graph has only two
for four.  Treating formal unrelated or universal carriers as satisfying the
antecedent would violate the campaign firewall.

Neither survivor creates one carrier, proves a rank gain, or changes the
public `1/8` interface.

## Bounded computation

The checker also enumerates all 33,866 labelled simple B-graphs through six
vertices and 78,008 zero-shore pairs (156,016 two-endpoint root states).  This
B-side scan is a discovery relaxation only; its finite outcomes cannot be
promoted.

```sh
env AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=120 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh \
  python3 amra-research-loop/campaigns/erdos-809-carrier-round4/evidence/graph_realizable_carrier_falsification.py
```

The run completed in 2.5 seconds with no Lean process.  SHA-256:

- script: `d9c616bf955d9ab9cd326a6d0fa851fb7c0b27184ef27eb9ab88ede839f06166`
- JSON: `05c3f88f64d0151a125d3df0bb165b4cc25d70e7d8eba3187705bfcd8422cc58`

