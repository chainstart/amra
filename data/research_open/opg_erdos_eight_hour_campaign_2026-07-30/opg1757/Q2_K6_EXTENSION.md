# OPG-1757: extension of the reserve move to \(q=2,k=6\)

Date: 2026-07-30

## 0. Status

- **HUMAN PROOF:** the protected basis-reserve move has the all-parameter
  forest-preservation and tagged-inverse properties audited in
  `INDEPENDENT_MULTIEDGE_AUDIT.md`.
- **FINITE EVIDENCE:** the complete \(q=2,k=6\) candidate graph on \(K_6\)
  has a matching covering all 112200 negative objects.
- **OPEN GAP:** this is not a canonical injection for arbitrary \(q,k\) and
  does not prove the complete first coefficient or OPG-1757.

## 1. Candidate graph

Let \(E=01\) and \(F=23\).  The left side consists of all active negative
forest pairs with \(E\) blue-only, \(F\) blue, and eight total coloured edge
copies.  The right side consists of the corresponding positive pairs with
\(E\) red-only.

The base graph contains every valid direct move and every valid exchange of
\(E\) with one red edge.  The expanded graph additionally does the
following for each source:

1. apply deterministic global cycle opening;
2. in either output colour, remove any non-protected edge \(a\);
3. insert any of the 15 \(K_6\) edges \(b\) that produces a forest;
4. retain the target exactly when its marked-edge class and active vertex
   set are unchanged.

This is the same move family used at \(k=5\).  The enumeration is exhaustive
for this definition, not for arbitrary multiedge recolouring.

## 2. Exact counts and maximum matchings

Independent bit-mask enumeration gives:

\[
|\mathcal N_6|=112200,\qquad
|\mathcal P_6|=117384.
\]

The graph results are:

| graph | candidate edges | maximum matching | deficiency |
|---|---:|---:|---:|
| direct/single | 257996 | 111344 | 856 |
| expanded reserve graph | 5470120 | 112200 | 0 |

For the base graph, alternating reachability from the 856 unmatched sources
gives a Hall set with
\[
|S|=4168,\qquad |N(S)|=3312,\qquad |S|-|N(S)|=856.
\]
This independently reproduces the previous base deficit.

Starting from that maximum matching, the reserve graph supplies exactly 856
augmenting paths:

| source-to-target path length | number |
|---:|---:|
| 1 | 169 |
| 2 | 687 |

Of these paths, 184 use one new reserve edge and 672 use two.  Flipping all
paths matches every negative source.  Since a matching cannot contain more
than 112200 left vertices, this is automatically a maximum matching.

Thus:
\[
\boxed{\nu(G^{\mathrm{reserve}}_{q=2,k=6})=112200.}
\tag{1}
\]

Equation (1) is a finite exhaustive statement.

## 3. Reproducibility hashes

The independent enumerator orders forest pairs by edge bit masks and hashes
the complete CSR adjacency:

```text
direct/single adjacency:
c652ecb052eb7aa73e69aa7058536f0d8cd64ecef1c69c81053e19a8b82c622e

expanded adjacency:
0088bf748db7c925d38b98d4adf2c356a7cace555a7c374b9724713f764a6b96

expanded source matching:
81318bd622364836c689cbb4feeb4d0f01de983ff0db0cc617b581bd0561cca6

856 augmenting paths:
9eedc3220276ced6f7415130f83a1ebdec85ee6d5c02873b3edc56be19d24b00
```

The certificate payload hash is:

```text
a46bf616725d5aed1a690afd4370c5f45defa8cab0e4ad2319e67b50a61be578
```

The certificate also records the first 12 augmenting paths and the complete
path-length/new-edge histograms.

## 4. What changed relative to \(k=5\)

The old move family has a much larger base obstruction at \(k=6\):
856 unmatched sources rather than six.  Nevertheless, no new type of
support change is needed in this finite layer.  A single protected basis
exchange after deterministic opening supplies enough reserve targets, and
every required augmentation has length at most two in the independently
constructed matching.

This is evidence that the useful object is the **reserve graph plus
alternating matching**, not a source-wise deterministic reserve rule.
The calculation does not show that the short-path phenomenon persists with
\(q\) or \(k\), nor that one reserve exchange always satisfies Hall's
condition.

## 5. Remaining theorem gap

A uniform result would need to prove for every Hall set \(S\) that
\[
|N_{\mathrm{direct/single+reserve}}(S)|\ge |S|.
\]
The finite computations for \(k=5,6\) verify this inequality only by full
enumeration.  The current human theorem controls validity and reversibility
of each edge, not expansion of the whole candidate graph.

In particular, bounded congestion of the tagged opening map still does not
compensate the unit weights of the signed forest-pair coefficient.  The
extension supplies a finite untagged matching, not a coefficient-level
capacity theorem.

## 6. Reproduction

```bash
python3 independent_verify_multiedge_and_k6.py
pytest -q test_independent_multiedge_and_k6.py
```

The saved finite certificate is `q2_k6_extension_certificate.json`.
