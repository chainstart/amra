# M809-11 graph-realizability attack

Date: 2026-08-02

Status: **the sharp empty-ownership pattern is impossible under the real
B-opposite definitions; a tight full-reserve circuit itself is exactly
graph-realizable.  No public closure claim.**

## 1. Translation of one repeated colour

Use the hard normal form with maximum witness `v`,

\[
A=N[v],\qquad B=V(G)\setminus A.
\]

For a repeated colour `gamma` with two good A--B edges, write them as

\[
x_\gamma b_\gamma,\qquad y_\gamma c_\gamma,
\quad x_\gamma,y_\gamma\in A,
\quad b_\gamma,c_\gamma\in B.
\tag{1.1}
\]

Its B base pair is

\[
e_\gamma=b_\gamma c_\gamma.
\]

In the zero-shore case the actual full B-reserve neighbourhood is
`K(e_gamma)`.  Two elementary properties are non-negotiable:

1. `e_gamma` belongs to `K(e_gamma)`;
2. colours having the same base pair have the same full reserve
   neighbourhood, because `K(e)` is a function of the graph and `e`, not of
   the colour.

The inner endpoint pair

\[
a_\gamma=x_\gamma y_\gamma
\tag{1.2}
\]

is the natural A-side ownership atom.

## 2. The path-shaped sharp pair cannot be a full reserve system

The previous abstract no-go used

\[
N(c_1)=\{q_1\},\qquad
N(c_2)=\{q_1,q_2\},\qquad
N(c_3)=\{q_2\}.
\tag{2.1}
\]

Suppose these are full reserves `K(e_i)`.  Since `e_1` belongs to its
singleton reserve, `e_1=q_1`; similarly `e_3=q_2`.  The middle base
`e_2` belongs to `{q_1,q_2}`.  If `e_2=q_1=e_1`, base determinism gives
`K(e_2)=K(e_1)`, contradicting (2.1).  If `e_2=q_2=e_3`, the symmetric
contradiction follows.  These are the only cases.

Thus (2.1) is a sharp obstruction to the ownership-blind *abstract ledger*,
but it is not graph-realizable when a colour sees its complete canonical
reserve.  It could arise only after an additional, presently undefined,
colour-dependent thinning of `K(e)`.

The bounded CSP and relaxed B-graph search in
`m809_11_graph_realizability_probe.py` independently confirms:

- no base assignment realizes (2.1);
- no exact path target occurs in any B-graph through six vertices;
- tight full-reserve circuits of another shape do occur.

## 3. Owned-inner-pair C7-exit lemma

**Lemma 3.1.**  Under `L_4(2)`, minimum degree at least three, and the
assumption that every `C7` is rainbow, the pair `a_gamma` in (1.2) is a
missing A-edge.

**Proof.**  The automatic induced-matching theorem applies to the two
same-colour edges in (1.1).  In particular, no endpoint of one is adjacent
to an endpoint of the other, so `x_gamma y_gamma` is missing.  Equivalently,
if `x_gamma y_gamma` were present, the two same-colour edges plus this cross
edge and the exact four-edge path supplied by `L_4(2)` after deleting the
other two endpoints would form a non-rainbow `C7`.  \(\square\)

For a coherent opposite star with fixed centre `b`, leaf `c`, and colour
set `Gamma_c`, write the edges as `b x_gamma` and `c y_gamma`.  The
`x_gamma` are pairwise distinct because the edges incident with `b` are
distinct; the `y_gamma` are pairwise distinct for the same reason at `c`.
Opposite geometry puts the two endpoint sets on disjoint rectangle sides.
Hence

\[
\gamma\longmapsto x_\gamma y_\gamma
\tag{3.1}
\]

is an injection from `Gamma_c` into actual missing A-edges.

This proves that the earlier Bad pattern with an A atom but empty circuit
ownership cannot represent a coherent hard B-opposite star.  If three
colours share one opposite base, each side has at least three distinct inner
endpoints, so the union rectangle has at least `3*3=9` missing A edges and
contains three distinct owned diagonal atoms.  A `1 by 1` rectangle ledger
for those three colours is impossible.

## 4. Tight circuits nevertheless have real hard-local models

The exact probe `m809_11_l4_candidate_probe.py` constructs a graph on
fourteen vertices.  Its maximum-witness partition has

```text
A = {v, x1..x4, y1..y4, r1, r2}
B = {b,c,z}.
```

Inside A, take the complete graph except all `X--Y` edges and the two
edges `x1x2,y1y2`.  Add all `b--X` edges, all `c--Y` edges, `bz`, and all
`z--X` edges.  Colour `bxi,cyi` alike for `i=1,2,3`; every other edge has
a fresh colour.

Exact exhaustive checks give:

```text
n=14, e=50=floor(n^2/4)+1
minimum degree 4, maximum degree 10
A=N[v]
bc is B-opposite and zero-shore
K(bc)={bc,cz}
three repeated colours / two full reserve tokens
L4(2): pass for every endpoint pair and every <=2 deleted non-endpoints
C7 cycles checked: 11,136
non-rainbow C7: 0
owned missing A atoms: x1y1,x2y2,x3y3
```

Thus three colours with the common full neighbourhood `{bc,cz}` form a
real inclusion-minimal tight circuit inside the exact edge threshold,
rainbow-C7, `L_4(2)`, maximum-witness B-opposite local contract.  This is
not the path pattern (2.1), and it has the forced A ownership from Lemma
3.1.

The construction is **not** claimed to be a genuine public-problem
counterexample or to violate the complete canonical hardness ledger: it
uses 47 colours, and no claim is made that the outer-A/`S_m` gate fails.
It proves only that local graph geometry and the C7 condition do not by
themselves eliminate a tight reserve circuit.

## 5. What remains of M809-11

The graph-realizability attack resolves the ownership question but not the
typed-budget question:

- every coherent repeated colour has a genuine owned missing A atom;
- a tight B-reserve circuit can still occur in a graph satisfying all the
  local hard conditions;
- missing A atoms are not fungible B-reserve tokens and do not appear as
  additive capacity in `D_A<=M_B+S_m`;
- the inherited use of the A rectangle is nonlinear and global.

Therefore the only remaining exact M809-11 target is a **typed conversion
lemma**: for a coherent tight circuit, use the injective diagonal A atoms
and the whole anticomplete rectangle to prove either the outer-A/`S_m` gate,
additional distinct B reserve, or a non-rainbow C7.  A conjecture that a
tight circuit alone forces a C7 is refuted by the fourteen-vertex model.

For several circuits, ownership of diagonal A atoms must also be shown
distinct across stars or handled by a submodular overlap rank.

## 6. Reproduction and evidence scope

```bash
env AMRA_MEMORY_KIB=524288 AMRA_TIMEOUT_SECONDS=120 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh \
  python3 amra-research-loop/campaigns/erdos-809-reserve-potential/evidence/m809_11_graph_realizability_probe.py

env AMRA_MEMORY_KIB=524288 AMRA_TIMEOUT_SECONDS=120 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh \
  python3 amra-research-loop/campaigns/erdos-809-reserve-potential/evidence/m809_11_l4_candidate_probe.py
```

Output hashes:

- necessary-condition probe:
  `fb376052e5fe887efafd5845f53e755e59be657422ed8dfb612fde451c247758`;
- exact fourteen-vertex graph:
  `00bd6c081ab9ed214b1b4ea1b807b2ba87fd43159ca66fb8022e8871abe8a42d`.

All computations are exact finite evidence.  Lemma 3.1 and the injection
(3.1) are the unbounded natural proofs.  Erdős #809 and the `1/8` main term
are unchanged.
