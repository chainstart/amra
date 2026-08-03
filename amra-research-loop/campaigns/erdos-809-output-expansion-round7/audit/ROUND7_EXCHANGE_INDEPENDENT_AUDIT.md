# Independent audit: Erdos-809 output-expansion round 7

Date: 2026-08-03

Verdict: **finite no-go passed; campaign must freeze without promotion**.

The audited statement is limited to the displayed locked `n=16,e=65`
natural-switch model.  It does not address four old deletions, nineteen
replacements, non-natural switches, other extensions, or the asymptotic
one-eighth problem.

## 1. Independent domain reconstruction

The verifier does not import `evidence/exchange_search.py`.  It reconstructs
the locked graph, the new-edge universe, the old deletion domain, all bad
`C7` traces, and every mode-2/mode-3 assignment.

There are 27 possible new edges incident with `w` or `u` after excluding
incidence with frozen `v`: thirteen from each new vertex to `V0-{v}`, plus
`wu`.  Two switch edges `wx1,ux2` are required.  The frozen typed model omits
`cw,cu,wz,uz`; switch legality together with `L4(2)` forces omission of
`wy1,uy2`.  Hence 19 optional edges remain.

The latter cross-edge exclusion is exact within the stated model.  If `wy1`
were present, the path `x1-w-y1-c`, together with the length-four `c`--`x1`
path guaranteed by `L4(2)` after deleting `w,y1`, would form a bad `C7`
containing the repeated pair `wx1,cy1`.  The `uy2` case is identical.

The old graph has 50 edges.  The ten edges incident with `v` are frozen by
`A=N[v]`; the eight old repeated-colour edges are frozen and disjoint from
them.  Their exact complement has 32 edges.  Thus the deletable-edge domain
is complete for this frozen interface, though not for a model that permits
changing `A` or the four old colour classes.

Consequently:

```text
mode 2: C(19,15)=3876 assignments, C(32,2)=496 deletion pairs;
mode 3: C(19,16)= 969 assignments, C(32,3)=4960 deletion triples.
```

## 2. Hitting-mask equivalence

For a bad cycle `C`, let `T(C)=C intersect D`, where `D` is the 32-edge
deletable-old domain.  A deletion set `S subset D` destroys every bad cycle
if and only if

```text
S intersects T(C) for every bad C7 C.                         (1)
```

The forward and reverse implications are exact because deleting edges
cannot create a cycle, and every bad cycle surviving after deletion was
already present before deletion.  A trace is empty precisely when its cycle
is protected from every allowed deletion.

In the author bitset implementation, the mask for one edge is the set of
deletion sets containing it.  OR over the edges of `T(C)` is therefore the
set of deletion sets meeting that trace; AND over all cycles is exactly (1).
This proves the mask equivalence, rather than treating it as a heuristic.

The independent verifier does not use those masks.  It builds the trace
hypergraph directly, exhausts every deletion set on all unprotected
assignments, and performs deterministic deleted-graph cycle replays as an
implementation cross-check.

## 3. Exhaustive results

Under the 3 GiB / 180 s cap, the independent implementation obtains:

```text
mode 2: 3876 x 496,  protected assignments 3860, candidates 0;
mode 3:  969 x 4960, protected assignments  968, candidates 0.
```

Thus no deletion pair or triple hits all bad-cycle traces in the respective
finite domains.  Later counters (`L4`, reserve, output, rank) are zero because
no candidate reaches them; they are not independent failures of those tests.

The sole unprotected mode-3 assignment omits exactly

```text
bu, bw, uw.
```

Its independently reconstructed hypergraph has 93 distinct traces, with
size distribution

```text
21 singleton traces, 72 three-edge traces.
```

Every transversal must contain the 21 different singleton edges, giving
`tau>=21`.  Those same 21 edges meet all 93 traces, giving `tau<=21`.
Therefore `tau=21` exactly.

## 4. Statement and dependency match

The decisive lemma is correct as a finite firewall for this fixed model.
The following broader readings are rejected:

* it does not rule out all threshold-preserving exchanges;
* it does not rule out four-deletion or non-natural-switch witnesses;
* it supplies no every-cut expansion or finite-to-asymptotic bridge;
* it does not change the public `F_3(n) ~ n^2/8` question.

There are six killed mechanisms and three selected survivors among the nine
non-survivor-denominator mechanisms used by the campaign gate.  Hence

```text
kill ratio = 6/(12-3) = 6/9 = 2/3 < 0.8.
```

The mechanism-falsification gate therefore fails exactly as designed.
The correct decision is `frozen`, supported by this finite no-go, with no
phase advance and no theorem promotion.

