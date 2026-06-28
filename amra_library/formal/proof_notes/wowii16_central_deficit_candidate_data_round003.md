# WOWII16 central deficit candidate data, round 003

Target checked:
`central_deficit_diametral_safe_candidate_data`.

No external web or literature sources were used. The run artifact directory was
read-only in this sandbox, so this workspace note records the nontrivial tool
check required by the round.

## First blocker

The exact requested theorem is not merely absent from the Lean file. A finite
search found a small obstruction to the predicate
`centralDeficitDiametralSafeCandidateData G b A`.

## Finite obstruction

Use the 6-cycle on vertices `0,1,2,3,4,5` with edges

```text
0-4, 0-5, 1-3, 1-5, 2-3, 2-4
```

Equivalently, the cyclic order is `0,4,2,3,1,5,0`.

Take:

```text
b = 0
A = {4, 5}
diametral path p = 1,3,2,4
e = 3
r = radius = 3
D = Icc (e - r + 2) (r - 1) = Icc 2 2
```

Checks:

```text
G is connected
G.radius.toNat = 3
G.diam = 3
2 < r
¬ 2*r ≤ diam + 1, since 6 ≤ 4 is false
A is an independent subset of neighborSet b
A.card = maxIndepNeighborsCard G = 2
p is a diametral path of length 3
D.card = 1 = 2*r - 2 - e
```

The candidate-data predicate requires `Q0/Q1` off the path support. The path
support is `{1,2,3,4}`, so the only off-path vertices are `{0,5}`. Their
distances from `b = 0` are:

```text
dist 0 0 = 0
dist 0 5 = 1
```

Thus no off-path vertex can be in `Q0`, because `Q0` requires distance at least
`2` from `b`, and no off-path vertex can be in `Q1`, because `Q1` requires
distance at least `3` from `b`. Therefore `Q0 = Q1 = ∅`, but `D.card = 1`,
contradicting the required cardinal bound

```text
D.card ≤ ((Q0.image fun x => (x, false)) ∪
          (Q1.image fun x => (x, true))).card
```

This obstruction is independent of the choice of `P0/P1`: the `Q0/Q1` off-path
distance constraints alone fail for the displayed diametral path.

## Tool check

Python finite search decoded this obstruction while checking all hard-branch
graphs up to six vertices. Output summary:

```text
n 3 hard graphs checked 0
n 4 hard graphs checked 0
n 5 hard graphs checked 0
COUNTER ('bad_path', 6, 1880, 3, 3, 0, {4, 5}, (1, 3, 2, 4), 1, 4)
```

The mask `1880` over lexicographic pairs of `Fin 6` decodes to the six edges
listed above.

## Consequence

The theorem
`central_deficit_diametral_safe_candidate_data` should not be the next Lean
target as stated. The next target should either weaken the candidate-data
predicate to allow path endpoints or near-base off-path vertices in the central
demand repair, or replace the route with a candidate package that is not
quantified over every diametral path.

## Round 003 follow-up: semi-strong existential package

External/source material relied on: supplied local proof-lab context, supplied
local AMRA math tools report, local Lean source, local proof notes, and local
verifier output only. No web or literature source was used in this iteration.

Lean edit made:

```text
centralDeficitExistsDiametralSafeCandidateDataDisjoint
central_deficit_decoupled_assigned_radius_tail_component_safe_hall_of_exists_disjoint_candidate_data
```

The new predicate binds the same witnesses
`u w p e D P0 P1 Q0 Q1` to all existential candidate-data clauses and adds
the semi-strong disjointness condition

```text
Disjoint (Q0 ∪ Q1) ((A ∪ P1) ∪ insert b P0)
```

The wrapper packages any such existential witnesses through the existing
`central_deficit_decoupled_assigned_radius_tail_component_safe_hall_of_safe_candidates`.

Remaining mathematical blocker: prove the global compatible safe-capacity
selection theorem, i.e. construct these witnesses under the hard-branch
hypotheses of `central_deficit_exists_diametral_safe_candidate_data_disjoint`.
The proof-lab route identifies this as the blocker-to-augmentation dichotomy:
insufficient disjoint off-path safe capacity should force either a larger
fixed-color extension or an independent neighborhood larger than `A`.

## Iteration 2 follow-up: C6 compatibility validation

External/source material relied on: supplied local proof-lab context, supplied
local AMRA math tools report, local Lean source, local proof notes, and local
verifier output only. No web or literature source was used in this iteration.

Finite search check: a Python brute-force search of all connected hard-branch
graphs through 7 vertices found no counterexample to the strengthened
existential-disjoint predicate. Summary output:

```text
n 3 hard graphs 0
n 4 hard graphs 0
n 5 hard graphs 0
n 6 hard graphs 60
n 7 hard graphs 7920
True
```

Lean edit made:

```text
centralDeficitC6CompatiblePath
central_deficit_c6_exists_diametral_safe_candidate_data_disjoint
```

The new C6 theorem proves that the old obstruction is repaired by the
existential-compatible route: for the same graph, base `0`, and
`A = {4, 5}`, the compatible diametral path `0-4-2-3` admits
`P0 = {2}`, `P1 = {3}`, `Q0 = {1}`, and `Q1 = ∅`, satisfying the added
disjointness clause.

Remaining mathematical blocker unchanged: the exact general theorem
`central_deficit_exists_diametral_safe_candidate_data_disjoint` is still not
proved. The next proof step should formalize the global compatible
safe-capacity selection/dichotomy, using the C6-compatible witness as a sanity
test for the intended construction.

## Iteration 3 follow-up: cardinal packaging and Fin9 sanity check

External/source material relied on: supplied local proof-lab context, supplied
local AMRA math tools report, local Lean source, local proof notes, and local
verifier output only. No web or literature source was used in this iteration.

Lean edit made:

```text
central_deficit_exists_diametral_safe_candidate_data_disjoint_of_untagged
```

This constructor packages future witness data into
`centralDeficitExistsDiametralSafeCandidateDataDisjoint` from the more natural
untagged capacity inequality

```text
D.card ≤ (Q0 ∪ Q1).card
```

using `Disjoint Q0 Q1` to convert the tagged Boolean-image cardinality in the
definition. This does not solve the global existence theorem, but removes one
Lean-side bookkeeping step from the remaining safe-capacity selection proof.

Finite search check: the existing 9-vertex base-compatible obstruction graph in
the Lean file is not an immediate counterexample to the strengthened
existential-disjoint predicate. For its unique maximum-local base `b = 5` and
`A = {2, 6, 7}`, a Python brute-force search found the compatible witnesses:

```text
path = (0, 7, 5, 2, 1, 3)
P0 = {0, 1}
P1 = {8, 3}
Q0 = {4}
Q1 = ∅
radius = 4
diameter = 5
D.card = 1
```

Remaining mathematical blocker unchanged: prove the global compatible
safe-capacity selection/dichotomy under the hard-branch hypotheses. The exact
target theorem `central_deficit_exists_diametral_safe_candidate_data_disjoint`
is still absent.

## Iteration 4 follow-up: selector reduction

External/source material relied on: supplied local proof-lab context bundle,
supplied local AMRA math tools report, local Lean source, local proof notes,
and local verifier output only. No web or literature source was used in this
iteration.

Lean edit made:

```text
central_deficit_exists_diametral_safe_candidate_data_disjoint_of_diametral_selector
```

This reduction packages the existing
`central_deficit_diametral_path_radius_tail_demand` witness with a future
compatible selector for `P0/P1/Q0/Q1`. The selector obligation is now the exact
remaining mathematical core:

```text
for the diametral demand D, construct P0 P1 Q0 Q1 satisfying independence,
left/right disjointness, path-cardinality, off-pathness, Q0/Q1 safety,
D.card <= (Q0 union Q1).card, and disjointness from the fixed sides.
```

The exact target theorem
`central_deficit_exists_diametral_safe_candidate_data_disjoint` is still absent;
proving the selector under the hard-branch hypotheses will close it via the new
reduction lemma.

## Iteration 5 follow-up: universal selector demoted

External/source material relied on: supplied local proof-lab context bundle,
supplied local AMRA math tools report, local Lean source, local proof notes,
and local verifier output only. No web or literature source was used in this
iteration.

Lean edit made:

```text
central_deficit_diametral_disjoint_selector_universal_refuted
```

This theorem formally rules out the tempting strengthening used by the previous
selector reduction: a selector quantified over every diametral path, even with
the new disjointness clause and untagged `D.card <= (Q0 union Q1).card`
capacity. The proof specializes the alleged universal selector to the same C6
bad diametral path `1-3-2-4`; off-path vertices are only `0` and `5`, both too
close to base `0`, so `Q0 = Q1 = empty` contradicts `D.card = 1`.

Tool checks:

```text
random n 8 hard 27 no counter
random n 9 hard 47 no counter
random n 10 hard 68 no counter
random search ok
```

A temporary Lean probe also tested uncommenting the older fixed-color padding
block. It failed at the claimed arithmetic step deriving
`2 * (G.radius.toNat - 1) <= p.length - 2` from
`G.radius.toNat <= p.length`; that implication is false in the relevant
small-radius/diametral regime, so that commented route should not be restored
as a shortcut to the candidate-data theorem.

Verifier:

```text
env LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1 lake env lean AmraLibrary/OpenProblemBatches/Attack1680866_20260608/Wowii16CentralCore.lean
```

Result: pass, with only existing `simpa` style warnings and one additional
style warning on the new refutation theorem.

Remaining mathematical blocker: the exact theorem
`central_deficit_exists_diametral_safe_candidate_data_disjoint` is still not
declared. The next proof target must be an existential compatible diametral
path selector, not a selector over all diametral paths.

## Iteration 6 follow-up: existential selector packaging isolated

External/source material relied on: supplied local proof-lab context bundle,
supplied local AMRA math tools report, local Lean source, local proof notes,
and local verifier output only. No web or literature source was used in this
iteration.

Lean edit made:

```text
central_deficit_exists_diametral_safe_candidate_data_disjoint_of_exists_untagged
```

This lemma removes the last Lean-side packaging issue from the compatible
selector route.  If proof-lab supplies the natural existential witnesses
`u w p e D P0 P1 Q0 Q1` with the untagged capacity bound

```text
D.card <= (Q0 union Q1).card
```

and the fixed-side disjointness clause, the lemma converts that data into
`centralDeficitExistsDiametralSafeCandidateDataDisjoint` using the previously
proved tagged-card conversion.

Remaining mathematical blocker unchanged: the exact target theorem
`central_deficit_exists_diametral_safe_candidate_data_disjoint` is still not
declared/proved.  What remains is a genuine graph-theoretic selector theorem:
under the hard-branch hypotheses, choose a compatible diametral path and safe
pools with enough off-path capacity.  The earlier universal selector route is
formally refuted by the C6 bad path, so the next target must be existential.
