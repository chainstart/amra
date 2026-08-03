# M809-11 second-wave attack: ownership is the missing invariant

Date: 2026-08-02

Status: **proved abstract completion lemma plus sharp indistinguishability
no-go for the current ledger; no graph-realizability or public closure
claim.**

Graph-translation update: the path-shaped abstract pair and its empty
A-ownership branch are not realizable under the canonical full-reserve and
B-opposite definitions.  See `M809_11_GRAPH_REALIZABILITY.md`.  The abstract
pair remains a valid proof that the old scalar ledger omits ownership; it is
not a hard-graph counterexample.

## 1. Tight circuit input

Let `S` be an inclusion-minimal deficient colour set in the fixed-endpoint
colour--token incidence graph.  The independently audited lemma gives

\[
|N_B(S)|=|S|-1,
\]

and every proper subset `T` of `S` satisfies

\[
|N_B(T)|\ge|T|.
\tag{1.1}
\]

The subscript `B` emphasizes that these are actual root-free B-reserve
tokens.  A second algebraic occurrence of one missing leaf pair `mu` is not
a new token.

## 2. Minimal ownership-aware capacity

Let `R` be a set of actual capacity-one resource atoms, partitioned by
provenance into B-missing edges, A-rectangle edges, and any future owned
slack atoms.  Each atom `r` has a precommitted owner neighbourhood

\[
O(r)\subseteq S
\]

consisting of the circuit colours that can legally use it.  Define the
coverage rank

\[
\rho(T)=|\{r\in R:O(r)\cap T\ne\varnothing\}|.
\tag{2.1}
\]

This is monotone and submodular: each atom contributes the Boolean coverage
function `1[O(r) intersects T]`, and the submodular inequality holds atom by
atom.  Unlike an ordinary additive branch ledger, (2.1) prevents the same
`mu` edge from being spent twice and records whether an `E_A`-generated
rectangle edge is usable by a colour in this circuit.

The nonlinear rectangle theorem may generate many actual A-edge atoms, but
`E_A` itself is not an atom and the product cardinality does not determine
the owner sets `O(r)`.  Likewise, the scalar `S_m` is not a resource until
it is decomposed into owned atoms.

## 3. One-owned-atom completion lemma

**Lemma 3.1.**  Let `S` satisfy (1.1) and `|N_B(S)|=|S|-1`.  If there is one
new actual atom `a` outside `N_B(S)` with `O(a)` containing at least one
colour `c` of `S`, then adjoining `a` to the legal neighbourhood of `c`
makes the incidence system on `S` satisfy Hall.

**Proof.**  A subset not containing `c` is unchanged and satisfies (1.1).
A proper subset containing `c` already satisfied (1.1), even before the new
atom.  The full set gains the new atom, so its neighbourhood size rises from
`|S|-1` to `|S|`.  Hall's inequalities now hold for every subset.  \(\square\)

Thus a single tight circuit does not need a large additive budget: it needs
one genuinely new atom with nonempty ownership inside the circuit.  This is
the exact structural target for M809-11.

## 4. Sharp ownership-blind indistinguishable pair

Take three colours with B-neighbourhoods

\[
N_B(c_1)=\{q_1\},\qquad
N_B(c_2)=\{q_1,q_2\},\qquad
N_B(c_3)=\{q_2\}.
\tag{4.1}
\]

This is an inclusion-minimal tight circuit: the full set has two tokens for
three colours; every pair has two tokens; and both tokens have circuit
degree two.

Give both instances the same current scalar ledger:

```text
|S|=3, |Q|=2, deficiency=1
colour B-degrees [1,2,1], token S-degrees [2,2]
branch B-opposite
mu occurs algebraically twice but denotes one distinct B atom
E_A=1, rectangle side sizes (1,1), rectangle product 1
S_m=0
```

Both also contain one actual A-rectangle atom `a1`.

- **Chargeable instance:** `O(a1)={c2}`.  A matching is
  `c1-q1, c3-q2, c2-a1`.
- **Unchargeable instance:** `O(a1) cap S` is empty.  The atom exists and
  all displayed scalars are unchanged, but the maximum matching size on
  `S` remains two.

The coverage rank (2.1) is submodular in both instances and distinguishes
them on the full circuit: it is three in the first and two in the second.
The existing ledger cannot distinguish them because it records the number
of A atoms, not their colour ownership.

The bounded exact probe `m809_11_ownership_probe.py` verifies every Hall,
matching, minimality, and submodularity assertion in this pair.  This pair
is an abstract information-theoretic obstruction.  It is **not** claimed to
be graph-realizable under the full hard BCM hypotheses.

Reproduction:

```bash
env AMRA_MEMORY_KIB=262144 AMRA_TIMEOUT_SECONDS=60 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh \
  python3 amra-research-loop/campaigns/erdos-809-reserve-potential/evidence/m809_11_ownership_probe.py
```

Output SHA-256:
`380abb24cbe22e41837cd50854a55c818b4c5acdc9bdd06174d7d868d71d25ac`.

## 5. Consequence for M809-11

The tight-circuit lemma alone cannot imply geometric coherence or injection
into typed budgets.  A viable graph theorem must supply at least one of:

1. an ownership theorem: every hard tight circuit has an actual B/A atom
   outside its current neighbourhood whose owner set meets the circuit;
2. a C7-exit theorem: absence of such an owned atom forces two same-colour
   edges into a non-rainbow C7;
3. a graph-realizability exclusion: the unchargeable ownership pattern in
   Section 4 cannot arise from a common maximum witness.

For several simultaneous circuits, an additional distinctness/laminarity
theorem is required so the same owned atom is not charged twice.  The
submodular coverage rank is the minimal sound bookkeeping object, but its
owner neighbourhoods are new mathematical information, not consequences of
`mu`, `E_A`, rectangle product, or `S_m` scalars.

Therefore the current ledger instantiation of M809-11 is exhausted.  The
general graph-specific possibility remains open only after adjoining an
ownership or C7-compatibility theorem.  Erdős #809 and the `1/8` main term
are unchanged.
