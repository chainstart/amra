# OPG-1757: partition-aware Hall and global cycle-opening attack

Date: 2026-07-30

## 0. Claim ledger

This note deliberately separates three levels.

- **HUMAN PROOF:** Theorems A--D below are valid for arbitrary finite
  boundary sets and arbitrary local/external forests.
- **FINITE EVIDENCE:** The partition tables are exhaustive through six
  boundary vertices.  The \(q=2,k=3\) Hall-kernel statements are exhaustive
  only for that finite layer and the explicitly stated rule graph.
- **OPEN GAP:** No injection for every \(q,k\), and hence no proof of the
  complete first coefficient, is claimed here.

The main outcome is partly negative but decisive.  Merely adding the external
component partition to a local rule does not close the induction.  There are
valid negative objects for which the same outside red forest is incompatible
with **every** positive object, because every positive object must contain
the marked red edge \(E\).  A successful proof must therefore be allowed to
open the external fundamental cycle, rather than leave the exterior fixed.

## 1. Exact partition state

Let \(F\) be a local forest, let \(H\) be an external forest, and suppose
their edge sets are disjoint and their vertex sets meet only in a finite
boundary \(B\).  Write

\[
\pi=\pi_B(F),\qquad \sigma=\pi_B(H).
\]

For two partitions \(\pi,\sigma\) of \(B\), let \(I(\pi,\sigma)\) be the
bipartite multigraph whose vertices are the blocks of the two partitions and
whose edge labelled \(b\) joins the \(\pi\)-block and \(\sigma\)-block
containing \(b\).

### Theorem A: fixed-context repair — HUMAN PROOF

\[
F\cup H\text{ is a forest}
\quad\Longleftrightarrow\quad
I(\pi,\sigma)\text{ is a forest}.                    \tag{A1}
\]

Consequently, if \(F'\) is another local forest with boundary partition
\(\tau\), then in the **fixed external state** \(\sigma\)

\[
F\mapsto F'\text{ is safe}
\quad\Longleftrightarrow\quad
I(\tau,\sigma)\text{ is a forest}.                   \tag{A2}
\]

Proof.  Contract every component of \(F\) and of \(H\).  Since both graphs
are forests and their edges are disjoint, contraction preserves cycle rank.
The resulting multigraph is exactly \(I(\pi,\sigma)\).  This proves (A1);
(A2) follows by applying it to \(F'\cup H\). \(\square\)

The universal outside-stability criterion from the preceding campaign is
the quantifier-eliminated special case

\[
\forall\sigma:\ I(\pi,\sigma)\text{ forest}
\Longrightarrow I(\tau,\sigma)\text{ forest}
\quad\Longleftrightarrow\quad
\tau\text{ refines }\pi.                             \tag{A3}
\]

For two colours, (A1)--(A3) apply independently to
\((\pi_R,\sigma_R)\) and \((\pi_B,\sigma_B)\).

## 2. Exact simultaneous-merge test

A tempting but false rule is:

> a collection of merges is safe whenever the blocks merged by each target
> block lie in different current incidence components.

Two individually safe merges can jointly close a cycle.  The exhaustive
audit found the smallest four-point example

\[
\begin{aligned}
\pi&=02|1|3,\\
\tau&=03|12,\\
\sigma&=01|23.
\end{aligned}
\]

Here \(I(\pi,\sigma)\) is the path
\[
1-01-02-23-3.
\]
Each target merge joins its two ends from different components after
splitting \(\pi\) into singletons, but the two merges together give the
four-cycle between the two \(\sigma\)-blocks and the two \(\tau\)-blocks.

### Theorem B: second incidence graph — HUMAN PROOF

Assume that \(\tau\) is a coarsening of \(\pi\) and that
\(G=I(\pi,\sigma)\) is a forest.  Construct \(J=J(\pi,\tau;\sigma)\):

- the left vertices are the connected components of \(G\);
- the right vertices are the blocks of \(\tau\);
- every block \(P\) of \(\pi\) contributes one edge from the component of
  \(G\) containing \(P\) to the unique \(\tau\)-block containing \(P\).

Then

\[
I(\tau,\sigma)\text{ is a forest}
\quad\Longleftrightarrow\quad
J(\pi,\tau;\sigma)\text{ is a forest}.               \tag{B1}
\]

Proof.  Start with \(G\), add one hub for each \(\tau\)-block, and join every
\(\pi\)-block vertex to its hub.  Contracting the added star edges produces
\(I(\tau,\sigma)\); contracting every tree component of \(G\) produces
\(J\).  Both operations contract only edges and preserve the cyclomatic
number, including parallel-edge two-cycles.  Thus the two results are
acyclic simultaneously. \(\square\)

For an arbitrary target partition \(\tau\), first split \(\pi\) to the common
refinement
\[
\rho=\pi\wedge\tau
\]
and then apply Theorem B to \(\rho\to\tau\).  Splitting cannot create a cycle,
so this is an exact split-then-merge normal form, not merely a sufficient
test.

## 3. Conditional Hall lifting

### Theorem C: partition-state Hall lifting — HUMAN PROOF

Fix a canonical decomposition of every global object into a local object
\(L\) and an exterior \(H\), with disjoint labelled edge sets.  For every
external coloured partition state
\[
\Sigma=(\sigma_R,\sigma_B),
\]
let \(\mathcal N_\Sigma\) and \(\mathcal P_\Sigma\) be the compatible
negative and positive local objects, using (A1) in each colour.  Suppose a
bipartite relation \(G_\Sigma\) has:

1. edges only from \(\mathcal N_\Sigma\) to \(\mathcal P_\Sigma\);
2. Hall expansion
   \[
   |N_{G_\Sigma}(S)|\ge |S|
   \quad\text{for every }S\subseteq\mathcal N_\Sigma;
   \]
3. a deterministic matching choice recoverable from \(\Sigma\) and the
   image.

Then the matching, applied while keeping \(H\) fixed, is an injection on all
global objects having that canonical decomposition.

Proof.  The actual exterior determines one state \(\Sigma\).  Hall gives a
matching saturating its compatible negative local objects.  Theorem A makes
each matched target compatible with the unchanged \(H\).  Images with the
same \(H\) are distinct by the matching; images with different labelled
exteriors remain distinct because \(H\) is unchanged and the decomposition
is canonical. \(\square\)

The theorem is useful as a reduction, but its hypotheses fail for the
outside-fixed OPG-1757 local model.

## 4. A general obstruction to every outside-fixed local injection

### Theorem D: forced-edge obstruction — HUMAN PROOF

Let \(E=uv\).  Suppose every positive local object must contain \(E\) in
red.  If the external red forest \(H_R\) already connects \(u\) to \(v\),
then no positive local red forest is compatible with the unchanged \(H_R\):
the edge \(E\) closes the unique \(u\)-\(v\) path in \(H_R\).

Therefore, whenever there is a compatible negative source with
\(E\notin F_R\), **no injection preserving this exterior can exist**, even
if every possible local rule and every partition tag is allowed.

This is stronger than failure of a particular merge signature.  It says the
outside path itself must sometimes be changed.

## 5. Exhaustive partition evidence

`verify_partition_aware_hall.py` exhausts all set partitions through
\(|B|=6\).  It verifies:

1. the universal implication (A3);
2. the second-incidence test (B1), via the split-then-merge normal form;
3. exact counts of context-safe but non-universal transitions.

The main rows are:

| \(|B|\) | partitions | compatible \((\pi,\sigma)\) | universal replacements | context-safe replacements | context-safe non-universal triples |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 | 0 |
| 2 | 2 | 3 | 3 | 5 | 1 |
| 3 | 5 | 15 | 12 | 53 | 25 |
| 4 | 15 | 107 | 60 | 965 | 675 |
| 5 | 52 | 1003 | 358 | 26515 | 22486 |
| 6 | 203 | 11735 | 2471 | 1020131 | 949303 |

**FINITE EVIDENCE ONLY.**  These rows audit the implementation and expose
small obstructions; the arbitrary-\(|B|\) statements rest on the human
proofs above.

## 6. The minimal \(q=2,k=3\) Hall core with partition state

The old three-rule graph has an exact \(8>6\) Hall core.  Its eight
active-active escape edges fall into three boundary-partition profiles:

- 2 keep the red partition and perform a mixed split/merge in blue;
- 2 keep the blue partition and perform a mixed split/merge in red;
- 4 perform mixed split/merge transitions in both colours.

Every escape is safe in some external partition states and unsafe in others.
Thus the external partition is genuinely relevant, but conditioning on it
does not solve Hall automatically.

The audit restricts this 8-source kernel separately in all
\[
B_6^2=203^2=41209
\]
coloured external partition states:

- 7394 states retain at least one of the eight sources;
- 4752 have a three-rule deficit;
- the active-active rule closes 3042 of these deficits;
- 1710 states still have a four-rule Hall deficit;
- the largest residual deficit is 6.

These are **finite \(q=2,k=3\) statements**.  A residual deficit is a valid
Hall witness against the full context-restricted four-rule graph because
all three/four-rule neighbors of the selected sources were included.
Conversely, closure of this one kernel does not certify a full graph.

The first saved residual context is

\[
\sigma_R=01234|5,\qquad
\sigma_B=02|1|3|4|5.
\]

It retains sources 1538 and 1546:

\[
\begin{aligned}
R_{1538}=R_{1546}&=\{45\},\\
B_{1538}&=\{01,04,15,23\},\\
B_{1546}&=\{01,05,14,23\}.
\end{aligned}
\]

This partition context has a literal forest realization: take a new red
vertex \(r\) and the red star
\[
H_R=\{0r,1r,2r,3r,4r\},
\]
and a new blue vertex \(b\) with
\[
H_B=\{0b,2b\}.
\]
Both displayed sources remain pairs of forests after adjoining
\((H_R,H_B)\).  Any positive red object contains \(01\), which closes the
triangle \(0r,1r,01\).

Neither source has an available four-rule neighbor.  More importantly, the
entire positive local class is empty in this context (0 compatible positives
versus 120 compatible negatives): \(\sigma_R\) connects 0 and 1, while every
positive red forest contains \(E=01\).  This is the finite realization of
Theorem D.

## 7. Revised all-parameter route: open the external cycle

The previous target, “find a context-dependent local replacement while
leaving \(H\) fixed,” is now ruled out.  The viable route is a global
fundamental-cycle exchange.

### Lemma E: single-colour cycle opening — HUMAN PROOF

If \(T\) is a forest and the endpoints of \(e\notin T\) are connected in
\(T\), let \(P_T(e)\) be their unique path.  For every \(x\in P_T(e)\),
\[
T+e-x
\]
is a forest and has the same connected-component partition as \(T\).

This elementary lemma supplies the first step: when inserting red \(E\)
would close an external cycle, remove a canonically selected red edge \(x\)
on the external \(E\)-path.  The removed coloured copy must then be routed
through the other forest.  If that insertion closes another cycle, repeat.
The state has to include at least

\[
(\text{current colour},\text{current edge},
\pi_R,\pi_B,\sigma_R,\sigma_B,\text{path/phase tag}).
\]

The finite q=1 and q=2 alternating-chain certificates support this shape,
but do not prove its termination.

### Deletion-contraction formulation — OPEN PROGRAM

Expose the first edge \(x\) on the current fundamental path.

- **Deletion branch:** keep \(x\) out of the receiving colour; the relevant
  external partition is unchanged.
- **Contraction/insertion branch:** insert \(x\); if its endpoints are
  already connected, Theorem B locates the precise incidence cycle and
  Lemma E opens it at the next tagged edge.

This gives an exact state transition, but three missing claims remain:

1. **bounded/canonical interface:** the active boundary must be chosen so
   that the state is recoverable without retaining an unbounded history;
2. **termination or Hall expansion:** the alternating cycle-opening graph
   needs a well-founded phase potential or a uniform Hall theorem;
3. **coefficient bookkeeping:** transitions may change the red/blue size
   split, and the resulting images must preserve the signed coefficient
   weights and remain mutually disjoint.

A plausible next invariant is not a source-only scalar.  It is the pair

\[
(\text{unresolved fundamental cycles},
 \text{BFS distance to a free positive state}),
\]

augmented by the ordered edge tag on the currently opened path.  The old
q=1 two-cycle already rules out a phase-free source potential.

## 8. Publication assessment

Theorems A--D and the second-incidence correction form a clean,
all-parameter forest-repair framework.  The forced-edge obstruction is
useful because it rules out an entire proof architecture, not just one
candidate rule.  On their own these results are elementary and are not
claimed to meet a top-quartile-paper threshold.

A paper-level result would require one of:

1. a uniform alternating cycle-opening/Hall theorem that closes the first
   coefficient for every \(q,k\); or
2. a broader partition-state exchange theorem for two graphic matroids,
   with a genuinely new termination or log-concavity consequence.

Current status: a rigorous change of route and a reproducible minimal
obstruction, **not** the OPG-1757 proof.

## 9. Reproduction

```bash
python3 verify_partition_aware_hall.py
pytest -q test_verify_partition_aware_hall.py
```

The certificate is `partition_aware_hall_certificate.json`; its claim labels
identify human proofs, finite evidence, and the open gap separately.
