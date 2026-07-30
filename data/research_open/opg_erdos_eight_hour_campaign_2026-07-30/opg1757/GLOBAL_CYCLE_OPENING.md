# OPG-1757: deterministic global cycle opening

Date: 2026-07-30

## 0. Status

- **HUMAN PROOF:** the one-step exchange, termination, preservation,
  tagged inverse, and finite-to-one bound below hold for arbitrary finite
  graphs and arbitrary pairs of forests.
- **FINITE EVIDENCE:** the collision statistics are exhaustive only for the
  old \(q=2,\ k=1,\ldots,7\) layers.
- **OPEN GAP:** forgetting the exchange tag is not injective.  This note
  does not prove the complete first coefficient.

This is the global replacement required by the forced-edge obstruction in
`PROOF_ATTACK.md`: an edge on the actual external fundamental path may move
between colours.

## 1. Deterministic transition

Let \(R,B\) be red and blue forests on a common ordered edge set.  Let
\[
E=uv\in B\setminus R.
\]
In the OPG-1757 reduced classes, \(E=01\), the other marked edge
\(F=23\) remains blue, and the goal is to move \(E\) from blue to red.

Put
\[
B_0=B-E.
\]
Because \(B\) is a forest containing \(E\), \(u\) and \(v\) lie in different
components of \(B_0\).

The deterministic map \(\Psi\) is:

1. If \(u,v\) are disconnected in \(R\), set
   \[
   \Psi(R,B)=(R+E,B-E),\qquad t=\bot.
   \]
2. Otherwise let
   \[
   P_R(E)=(e_1,\ldots,e_m)
   \]
   be the unique \(u\)-\(v\) path, oriented from \(u\) to \(v\).  Let \(x\)
   be the first \(e_i\) whose endpoints lie in different components of
   \(B_0\).  Set
   \[
   \Psi(R,B)=(R+E-x,\ B-E+x),\qquad t=x.              \tag{1}
   \]

The total order is used only to make path reconstruction deterministic;
the path itself is unique.

### Pseudocode

```text
GLOBAL-OPEN(R, B, E = uv):
    B0 := B - E
    P  := the unique u-v path in R
    if P does not exist:
        return (R + E, B0), DIRECT

    label every vertex by its component in B0
    scan P from u toward v
    x := first path edge whose endpoint labels differ
    return (R + E - x, B0 + x), EDGE(x)
```

This is a composite forest-to-forest move.  If implemented as microsteps,
the temporary graph \(R+E\) is unicyclic; after removing \(x\), both output
colours are forests.  No claim is made that the temporary microstate is a
pair of forests.

## 2. One-step cycle-opening theorem

### Theorem 1 — HUMAN PROOF

The edge \(x\) in step 2 always exists, and the output of \(\Psi\) is a pair
of forests.

Proof.  If every edge of the red \(u\)-\(v\) path had both endpoints in the
same \(B_0\)-component, transitivity along the path would put \(u,v\) in one
\(B_0\)-component.  This contradicts the fact that deleting \(E\) from the
blue forest separates its endpoints.  Hence \(x\) exists.

The graph \(R+E\) has the unique cycle \(P_R(E)+E\); deleting the path edge
\(x\) opens it.  Thus \(R+E-x\) is a forest.  The endpoints of \(x\) are in
different \(B_0\)-components, so \(B_0+x\) is a forest. \(\square\)

### Corollary 2: termination — HUMAN PROOF

The number of unresolved monochromatic cycles falls from at most one to
zero in one composite transition.  An alternating multi-step chain is not
needed for existence.

This termination uses the component partition of the *entire* blue forest
\(B-E\), not a bounded local partition.  That is why the outside-fixed local
rules missed it.

## 3. Preservation

### Theorem 3 — HUMAN PROOF

The transition preserves:

1. the total number \(|R|+|B|\) of coloured edge copies;
2. the uncoloured union \(R\cup B\), and hence every active-vertex label;
3. every blue marked edge other than \(E\), in particular \(F\);
4. the reduced sign class: \(E\) moves from blue-only to red-only.

Proof.  The direct case only changes the colour of \(E\).  In the exchange
case, \(x\notin B_0\), since its endpoints lie in different
\(B_0\)-components; also \(x\ne E\).  Thus \(x\in R\setminus B\), and (1)
exchanges the colours of the two distinct edge copies \(E,x\). \(\square\)

This is exactly the coefficient weight/support contract needed by the
first-coefficient signed forest-pair interpretation.

## 4. Tagged reversibility and finite fibres

### Theorem 4 — HUMAN PROOF

The tagged map
\[
(R,B)\longmapsto(\Psi(R,B),t)
\]
is injective.  If the target is \((R',B')\), the inverse is

\[
(R,B)=
\begin{cases}
(R'-E,\ B'+E),&t=\bot,\\
(R'-E+t,\ B'-t+E),&t\in E(G).
\end{cases}                                           \tag{2}
\]

Proof.  Formula (2) uniquely reconstructs the source; replaying the
deterministic rule verifies whether a proposed tag is valid. \(\square\)

### Theorem 5 — HUMAN PROOF

After forgetting the tag, every positive target has at most
\[
1+|B'\setminus R'|                                   \tag{3}
\]
preimages.  In a layer with \(k+2\) total coloured copies, this is at most
\(k+2\).

Proof.  There is at most one direct predecessor.  Every exchange predecessor
is specified by its tag \(x\), and (2) requires
\(x\in B'\setminus R'\). \(\square\)

Thus (1) is a general finite-to-one map and a reversible injection into
**edge-tagged** positives.  Bound (3) alone is not sufficient for the
unweighted coefficient inequality.

## 5. The tag cannot simply be erased

The first finite collision occurs already at \(q=2,k=3\).  Two negative
sources are

\[
\begin{aligned}
(R_1,B_1)
 &=\bigl(\{04,05,15\},\{01,23\}\bigr),&
t_1&=05,\\
(R_2,B_2)
 &=\bigl(\{04,15\},\{01,05,23\}\bigr),&
t_2&=\bot.
\end{aligned}
\]

Both map to
\[
(R',B')=\bigl(\{01,04,15\},\{05,23\}\bigr).          \tag{4}
\]

This collision is structurally unavoidable for this one-step recolouring
architecture:
the exhaustive audit below gives a \(q=2,k=5\) Hall set with 12 negative
sources but only 6 targets even after **all** valid direct moves and
\(E\leftrightarrow x\) exchanges preserving the uncoloured union are
allowed.  An injective extension of this architecture must leave the
direct/single-exchange neighborhood, for example by changing the uncoloured
union or encoding the tag through a multi-edge target feature.

The minimal extra state exposed by (4) is

\[
(\text{phase}\in\{\mathrm{direct},\mathrm{exchange}\},
 \text{exchanged path edge }x).
\]

The target alone cannot distinguish the direct source from the exchange
source.

## 6. Literal repair of the outside-path obstruction

Use vertices \(6,7\) as the external red/blue hubs from
`PROOF_ATTACK.md`:

\[
\begin{aligned}
R={}&\{06,16,26,36,46,45\},\\
B={}&\{01,04,15,23,07,27\}.
\end{aligned}
\]

The red \(0\)-\(1\) path is \(06,16\).  In \(B-E\), edge \(06\) crosses
components, so the deterministic tag is \(x=06\).  The image is

\[
\begin{aligned}
R'&=R+01-06,\\
B'&=B-01+06.
\end{aligned}
\]

Both are forests.  This demonstrates why a globally visible path edge,
rather than another local \(K_6\) edge, is the required repair.

## 7. Finite q=2 audit

`verify_global_cycle_opening.py` applies the deterministic map to every
negative object in the previous \(q=2,\ k=1,\ldots,7\) enumeration.
Before imposing the OPG layer conditions, it also exhausts every forest pair
with \(E\in B\setminus R\) on \(K_n\), \(2\le n\le5\).  The respective
source counts are \(1,12,336,18414\), and all tagged images are distinct.
This is a finite falsification audit of Theorems 1--4, not their proof.

| \(k\) | negatives | direct | exchange | deterministic untagged images | max fibre | all union-preserving matching | deficit |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 2 | 0 | 2 | 1 | 2 | 0 |
| 2 | 115 | 115 | 0 | 115 | 1 | 115 | 0 |
| 3 | 1585 | 1559 | 26 | 1559 | 2 | 1585 | 0 |
| 4 | 10730 | 9988 | 742 | 10050 | 3 | 10730 | 0 |
| 5 | 43648 | 35728 | 7920 | 37888 | 3 | 43642 | 6 |
| 6 | 112200 | 70848 | 41352 | 90552 | 4 | 111344 | 856 |
| 7 | 172800 | 62208 | 110592 | 138608 | 4 | 167488 | 5312 |

For every row:

- all images are in the correct positive layer;
- both colours remain forests;
- total weight and active labels are unchanged;
- the tagged image count equals the negative count;
- inverse replay recovers every source.

The last two columns use a larger graph than the deterministic map: each
source is joined to its direct image, when valid, and to every valid target
obtained by exchanging \(E\) with one of its red edges while preserving the
uncoloured union.  The first failure is the exact \(q=2,k=5\) Hall witness
\[
|S|=12,\qquad |N(S)|=6.                              \tag{5}
\]
Thus changing only the deterministic path order cannot solve the problem.
At least six sources in this finite kernel must leave the direct/single-edge
exchange neighborhood; the audit does not rule out more complicated
multi-edge recolourings that keep the same union.
The certificate records all 12 source indices, all 6 target indices, and
the first source
\[
R=\{02,03,12\},\qquad B=\{01,13,23,45\}.
\]

These are **FINITE EVIDENCE**, not an all-\(q,k\) injection.

## 8. Deletion–contraction interpretation

The transition is an exact deletion–contraction step around \(E\):

1. delete \(E\) from blue, exposing the component partition of \(B-E\);
2. insert \(E\) in red;
3. if insertion closes a cycle, delete the first red path edge crossing
   that blue partition and contract/insert its colour copy into blue.

Theorem 1 shows that the alternating process terminates immediately once
the entire component partition is available.  The remaining difficulty is
not termination; it is **tag absorption**.

A possible next Hall graph has:

- left vertices: negative forest pairs;
- primary right vertices: untagged positive pairs;
- secondary edges: union-changing repairs that encode
  \((\mathrm{direct}/\mathrm{exchange},x)\).

The old \(q=1,k=5\) and \(q=2,k\le7\) matchings are finite evidence that
such secondary images exist.  What remains open is a uniform reserve-image
or Hall theorem that absorbs every fibre in (3).

## 9. Reproduction

```bash
python3 verify_global_cycle_opening.py
pytest -q test_verify_global_cycle_opening.py
```

The generated certificate is `global_cycle_opening_certificate.json`.
