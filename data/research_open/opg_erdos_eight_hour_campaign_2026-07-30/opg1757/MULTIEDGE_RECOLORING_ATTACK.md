# OPG-1757: two-stage recolouring and the \(q=2,k=5\) Hall kernel

Date: 2026-07-30

## 0. Status

- **HUMAN PROOF:** after the deterministic global cycle opening, one
  protected basis exchange in either colour preserves both forest
  conditions.  With the opening edge and basis-exchange data retained, the
  two-stage move is reversible on every finite graph.
- **FINITE EVIDENCE:** on the complete \(q=2,k=5\) layer on \(K_6\), adding
  all such reserve moves to all direct/single-exchange moves raises the
  maximum matching from \(43642\) to \(43648\), equal to the number of
  negative objects.  The resulting finite injection uses no auxiliary tag
  in its target.
- **REFUTED:** allowing arbitrarily many recolourings while keeping the
  uncoloured union fixed cannot repair the first block of the minimal
  kernel: it has eight sources and only four positive objects on that
  union.
- **OPEN GAP:** there is no proved canonical injection for every \(q,k\),
  no uniform Hall expansion theorem for the reserve graph, and no
  application of bounded congestion to the unit-weight OPG coefficient.
  Complete first-coefficient positivity is not claimed.

Here “untagged” means that the image is an ordinary positive forest pair,
with no exchange edge stored beside it.  The finite matching uses the fixed
vertex/edge order of the enumerator; it is not a proof of an equivariant
unlabelled-graph rule.

## 1. The complete canonical 12-object kernel

As in `GLOBAL_CYCLE_OPENING.md`, let
\[
E=01,\qquad F=23.
\]
A negative object has \(E\) blue-only and \(F\) blue; a positive object has
\(E\) red-only and \(F\) blue.  At \(q=2,k=5\), every pair has seven
coloured edge copies and both active vertices \(4,5\) occur.

The direct/single-\(E\)-exchange graph has the following canonical Hall set
returned by alternating reachability from a maximum matching.  The edge
notation in the table lists the complete red and blue forests.

| source index | red | blue | only old neighbour |
|---:|---|---|---:|
| 433 | 02,03,12 | 01,13,23,45 | 9460 |
| 499 | 02,03,12,45 | 01,13,23 | 10102 |
| 518 | 02,03,13 | 01,12,23,45 | 3043 |
| 584 | 02,03,13,45 | 01,12,23 | 3670 |
| 3645 | 02,12,13 | 01,03,23,45 | 3043 |
| 3718 | 02,12,13,45 | 01,03,23 | 3670 |
| 11159 | 03,12,13 | 01,02,23,45 | 9460 |
| 11232 | 03,12,13,45 | 01,02,23 | 10102 |
| 16782 | 04,05,14 | 01,15,23,45 | 21736 |
| 16918 | 04,05,15 | 01,14,23,45 | 16754 |
| 19639 | 04,14,15 | 01,05,23,45 | 16754 |
| 25258 | 05,14,15 | 01,04,23,45 | 21736 |

Its complete old target set is:

| target index | red | blue |
|---:|---|---|
| 3043 | 01,02,13 | 03,12,23,45 |
| 3670 | 01,02,13,45 | 03,12,23 |
| 9460 | 01,03,12 | 02,13,23,45 |
| 10102 | 01,03,12,45 | 02,13,23 |
| 16754 | 01,04,15 | 05,14,23,45 |
| 21736 | 01,05,14 | 04,15,23,45 |

Thus the collision graph is exactly the union of six two-leaf stars:
\[
\begin{array}{c|c}
\text{target}&\text{sources}\\ \hline
3043&518,3645\\
3670&584,3718\\
9460&433,11159\\
10102&499,11232\\
16754&16918,19639\\
21736&16782,25258.
\end{array}
\tag{1}
\]
This is the full reported \(12\)-source, \(6\)-target witness, not a sample.
It is not inclusion-minimal: each row of (1) is itself an
inclusion-minimal \(2\)-source, \(1\)-target Hall obstruction.  The
12-object set is the disjoint union of these six minimal components.

## 2. Why more recolouring on the same union still fails

The first eight sources in the table have the common uncoloured union
\[
U_1=E(K_{\{0,1,2,3\}})\cup\{45\}.
\]
Exhausting every positive pair with this same union gives exactly targets
\[
\{3043,3670,9460,10102\}.
\]
Hence even an arbitrary-length recolouring sequence confined to \(U_1\)
has a Hall deficiency of four:
\[
8-4=4.                                               \tag{2}
\]

The last four sources have union
\[
U_2=\{01,04,05,14,15,23,45\}
\]
and six same-union positive objects, so that block alone is not deficient.
Equation (2) proves that a repair of the whole kernel must change the
uncoloured support of at least some sources.  Merely changing the order or
number of same-union colour swaps cannot work.

## 3. The protected reserve move

First apply the deterministic map \(\Psi\) from
`GLOBAL_CYCLE_OPENING.md`:
\[
(R,B)\xmapsto{\Psi}(R_0,B_0),
\]
retaining its opening tag \(x\in R\) or \(x=\bot\) only for the inverse
proof.

Choose one colour \(C\in\{R_0,B_0\}\), an edge \(a\in C\), and an edge
\(b\notin C\).  Replace
\[
C\longmapsto C-a+b.                                  \tag{3}
\]
The move is admissible when:

1. the endpoints of \(b\) lie in different components of \(C-a\);
2. \(E\) is not removed from red or inserted into blue;
3. \(F\) is not removed from blue;
4. if active labels are part of the layer, the active vertex set after
   (3) equals the active vertex set before it.

Conditions 2--3 are the protected-edge rule.  In the finite verifier,
membership in the enumerated positive layer independently rechecks all
marked-edge, weight and active-label conditions.

### Theorem 1: forest and support control — HUMAN PROOF

Every admissible two-stage move has two forest outputs, preserves the total
number of coloured edge copies, and changes the uncoloured union in at most
the two edges \(a,b\):
\[
\bigl((R_0\cup B_0)\mathbin{\triangle}
      (R_1\cup B_1)\bigr)\subseteq\{a,b\}.            \tag{4}
\]

Proof.  The cycle-opening theorem gives two forests \(R_0,B_0\).  Removing
\(a\) from \(C\) leaves a forest.  By condition 1, inserting \(b\) joins
two distinct components and cannot make a cycle.  The other colour is
unchanged.  One edge copy is removed and one inserted, proving weight
preservation.  All edges except \(a,b\) have unchanged membership in the
union, proving (4).  Conditions 2--4 preserve the sign class and active
labels. \(\square\)

The intermediate microstate is also always a pair of forests: unlike the
temporary \(R+E\) inside the composite opening map, (3) removes before it
inserts.

### Theorem 2: tagged reversibility — HUMAN PROOF

The map
\[
(R,B)\longmapsto
\bigl((R_1,B_1),(x,C,a,b)\bigr)                      \tag{5}
\]
is injective for every finite graph.

Proof.  From the target and \((C,a,b)\), replace \(b\) by \(a\) in colour
\(C\), recovering \((R_0,B_0)\).  Then use the inverse formula for
\(\Psi\) with opening tag \(x\).  This reconstructs the unique source.
Replaying the two steps verifies tag admissibility. \(\square\)

Theorem 2 is an all-parameter reversibility statement, but (5) is still
tagged.  The finite matching below is what absorbs the tags at \(q=2,k=5\).

## 4. A reserve matching on the 12-object kernel

Let a reserve edge join a source to every positive target obtained by one
admissible move (3) after its deterministic opening.  This reserve graph
has a matching of all 12 kernel sources.  One reproducible matching is:

| source | target | opening tag | reserve \(C:a\to b\) |
|---:|---:|---|---|
| 433 | 298 | 02 | red: 12→02 |
| 499 | 1155 | 02 | red: 12→02 |
| 518 | 323 | 03 | red: 13→03 |
| 584 | 1165 | 03 | red: 13→03 |
| 3645 | 1278 | 12 | red: 13→04 |
| 3718 | 2119 | 12 | red: 13→04 |
| 11159 | 7687 | 13 | red: 12→04 |
| 11232 | 8551 | 13 | red: 12→04 |
| 16782 | 2286 | 04 | red: 14→02 |
| 16918 | 1352 | 05 | red: 15→02 |
| 19639 | 4586 | 14 | red: 04→02 |
| 25258 | 3829 | 15 | red: 05→02 |

All target indices are distinct.  The certificate stores the complete
target forests and verifies the tagged inverse for every row.  This table
is a tag-free injection of this finite kernel: the tags displayed here
certify how the targets were found but are not attached to the image.

## 5. Six augmenting chains close the entire finite layer

Define \(G_1\) to contain every valid direct move and every valid single
\(E\leftrightarrow x\) exchange.  Define \(G_2\) by adjoining every
protected reserve move after deterministic opening.  Exact enumeration
gives:

| graph | edges | maximum matching | deficiency |
|---|---:|---:|---:|
| \(G_1\) | 112556 | 43642 | 6 |
| \(G_2\) | 1987196 | 43648 | 0 |

There are 43648 negative and 45620 positive objects.  Starting with the
deterministic Hopcroft--Karp maximum matching of \(G_1\), the verifier finds
six alternating paths, each with two source-to-target edges:

\[
\begin{aligned}
3645&-323-422-9485,\\
3718&-1165-495-8561,\\
11159&-298-507-3018,\\
11232&-1155-580-2109,\\
19639&-16608-16866-16607,\\
25258&-21612-25232-29723.
\end{aligned}                                       \tag{6}
\]

In each row, the first source is unmatched in \(G_1\), the middle target is
matched to the middle source, and the final target is free.  Flipping all
six paths produces a matching of every negative object.  The certificate
records the reserve exchange used on every new edge of (6).

Consequently:
\[
\boxed{\text{the expanded }q=2,k=5\text{ finite layer has an ordinary
untagged injection.}}                                \tag{7}
\]
Statement (7) is an exhaustive finite result, not a theorem for arbitrary
\(q,k\).

## 6. What bounded congestion can and cannot buy

The following bookkeeping lemma is valid at every layer.

### Lemma 3: weighted fibre compensation — HUMAN PROOF

Let \(\phi:\mathcal N\to\mathcal P\), with nonnegative source and target
weights \(w_-,w_+\).  If
\[
\sum_{n\in\phi^{-1}(p)}w_-(n)\le w_+(p)
\quad\text{for every }p\in\mathcal P,                \tag{8}
\]
then
\[
\sum_{n\in\mathcal N}w_-(n)
\le\sum_{p\in\mathcal P}w_+(p).
\]
In particular, a fibre bound \(|\phi^{-1}(p)|\le C\) suffices when every
mapped source satisfies \(w_-(n)\le w_+(\phi(n))/C\).

Proof.  Sum (8) over all targets. \(\square\)

This does not close OPG-1757.  In the reduced forest-pair coefficient every
object in the audited layer has unit weight.  Thus a congestion bound
\(C>1\) supplies no factor \(1/C\), and Lemma 3 reduces to genuine
injectivity.  Any successful all-\(k\) compensation argument must exhibit
real target capacity already present in the coefficient formula, or a
sign-reversing cancellation among the colliding sources.  Neither has been
proved.

## 7. Exact remaining gap

The reserve move resolves the first direct/single-exchange failure and the
entire finite \(q=2,k=5\) matching problem.  A complete proof still needs
one of:

1. a canonical reserve choice whose untagged image is injective for every
   \(q,k\);
2. a uniform Hall theorem for the graph generated by direct, single and
   protected reserve moves;
3. a coefficient-level capacity or cancellation mechanism satisfying
   (8) despite unit object weights.

The finite result does not establish any of these.  It therefore does not
prove the complete first coefficient or OPG-1757.

## 8. Reproduction

```bash
python3 verify_multiedge_recoloring_attack.py
pytest -q test_verify_multiedge_recoloring_attack.py
```

The generated certificate is
`multiedge_recoloring_attack_certificate.json`.  It contains all 12 source
objects, all six old targets, the exact collision graph, both same-union
blocks, the 12-target reserve matching, and the six full-layer augmenting
paths.
