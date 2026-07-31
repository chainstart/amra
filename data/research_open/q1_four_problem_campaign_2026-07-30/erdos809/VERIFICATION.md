# Verification record

## Commands

From this directory:

```bash
python3 -m unittest -v test_809_near_dirac.py
python3 verify_809_near_dirac.py
```

Both commands passed on 2026-07-30.

## Unit tests

```text
test_dense_clique_compatibility ... ok
test_distance_two_splice ... ok
test_four_path_obstruction_identities ... ok
test_nonindependent_core_hub_union ... ok
test_rectangle_count ... ok

Ran 5 tests
OK
```

## Full guard counts

### Exact-four-path obstruction

- labelled graphs exhausted for \(3\le n\le6\): 33,864;
- obstructed graph/pair profiles: 212,888;
- property-(P) neighbourhood pairs checked: 384,432;
- complement-neighbourhood bounds checked: 110,448;
- type-product bounds checked: 128,616;
- exact two-clique and complete-bipartite models at \(n=20\): passed.

The exhaustive labelled-graph counts by order were:

| \(n\) | graphs | obstructed pairs |
|---:|---:|---:|
| 3 | 8 | 24 |
| 4 | 64 | 384 |
| 5 | 1,024 | 7,640 |
| 6 | 32,768 | 204,840 |

### Distance-two splice

- fixed-seed random graphs: 500;
- edge pairs at edge distance two inspected: 1,630;
- actual avoiding three-path splices checked as simple \(C_7\)'s: 728.

### Dense two-clique branch

- \(K_9\) minus a three-edge matching: all 528 pairs among 33 edges
  covered by a \(C_7\);
- \(K_{10}\) minus a spanning ten-cycle: all 595 pairs among 35 edges
  covered by a \(C_7\).

### Maximum-cut core/hub branch

The independent-side hypothesis was deliberately violated by adding three
edges to the \(B\)-side of a 14-vertex finite model.  The family contains
four hub rows and two genuine core rows.

- graph edges: 56;
- compatible-family edges: 32;
- family-edge pairs: 496;
- pairs covered by brute-force \(C_7\) enumeration: 496.

### Rectangle optimisation

On all 80,601 profiles
\[
0\le y\le x\le1,\qquad x,y\in\frac1{400}\mathbb Z,
\]
the normalized expression
\[
x+(1-x)\max(0,1-x-y)
\]
had minimum exactly \(1/2\), attained at \(x=y=1/2\).

## Guard boundary

The exhaustive and random checks verify finite identities, vertex
distinctness, displayed seven-cycle templates, and the elementary
optimization.  They do not:

- replace the asymptotic cleaning arguments;
- prove that a bounded sample implies Theorem A;
- close the linearly low-minimum-degree BCM26 Case 1;
- prove Erdős #809.
