# OPG-1757: final \(q=2\) layer \(k=8\)

Date: 2026-07-30

## 0. Status

- **FINITE EVIDENCE:** the complete reserve-expanded \(q=2,k=8\) graph
  has a matching of all 124416 negative objects.
- **FINITE COVERAGE:** together with the saved \(k=1,\ldots,7\)
  certificates, every possible nonempty \(q=2\) layer in the current
  six-vertex active model is computationally certified.
- **OPEN GAP:** this exhaustive fixed-model result is not a symbolic
  all-\(k\) Hall proof and does not prove OPG-1757.

## 1. Why this is the final parameter

Both colours are forests on six vertices, so each contains at most five
edges.  A layer-\(k\) pair contains \(k+2\) coloured edge copies.  Hence
\[
k+2\le10,\qquad k\le8.                              \tag{1}
\]
The \(k=0\) layer is empty under the exact \(q=2\) active definition:
its two available copies are already the required blue edges \(E=01\) and
\(F=23\), leaving active vertices \(4,5\) absent.

Therefore \(k=1,\ldots,8\) are all possible nonempty layers in this model.

## 2. Preconstruction resource bound

Before generating adjacency, the following deliberately loose bound was
used.  At \(k=8\), the deterministic target has ten edge copies.  Protecting
red \(E\) and blue \(F\) leaves at most eight outgoing reserve choices.
Each tests all 15 incoming \(K_6\) edges, and there are at most six
direct/single targets.  Thus
\[
\deg_{\rm candidate}(s)\le8\cdot15+6=126.           \tag{2}
\]

For 124416 sources, uint64 CSR offsets and uint32 target indices give the
preconstruction expanded-CSR bound
\[
63\,701\,000\ {\rm bytes}.                          \tag{3}
\]
This was safely below available memory, so no disk-blocked augmentation was
needed.

## 3. Exact graph and matching

Enumeration gives equal side counts:
\[
|\mathcal N_8|=|\mathcal P_8|=124416.
\]

| graph | edges | maximum matching | deficiency |
|---|---:|---:|---:|
| direct/single | 138816 | 115324 | 9092 |
| reserve-expanded | 5114592 | 124416 | 0 |

The base alternating Hall witness has
\[
|S|=18216,\qquad |N(S)|=9124,\qquad
|S|-|N(S)|=9092.                                    \tag{4}
\]

Starting from the base maximum matching, the compact matcher finds 9092
augmenting paths:

| length | paths |
|---:|---:|
| 1 | 19 |
| 2 | 6545 |
| 3 | 2272 |
| 4 | 225 |
| 5 | 30 |
| 6 | 1 |

After flipping these paths:
\[
\boxed{\nu(G^{\rm reserve}_{q=2,k=8})=124416.}       \tag{5}
\]

Because the two sides have equal size, this is a perfect matching of the
finite graph.

## 4. Actual resources

The compact representation used:

| object | bytes |
|---|---:|
| base CSR | 1550600 |
| expanded CSR | 21453704 |
| combined CSR | 23004304 |

One timed run on the current host reported:

```text
wall time       26.33 s
maximum RSS     98772 KiB
swaps           0
```

The runtime observations are environment-specific and are not hashed
certificate fields.

## 5. Complete finite \(q=2\) coverage

The currently saved results are:

| \(k\) | negative objects | matching used | unmatched |
|---:|---:|---:|---:|
| 1 | 2 | direct/single | 0 |
| 2 | 115 | direct/single | 0 |
| 3 | 1585 | direct/single | 0 |
| 4 | 10730 | direct/single | 0 |
| 5 | 43648 | reserve-expanded | 0 |
| 6 | 112200 | reserve-expanded | 0 |
| 7 | 172800 | reserve-expanded | 0 |
| 8 | 124416 | reserve-expanded | 0 |

Thus every possible nonempty \(q=2\) layer has a computed matching under
the current enumeration and active-set definition.  This is a finite
exhaustive result about eight explicit graphs.  It is not a formula,
canonical map, or structural proof of the fibre-excess lemma.

The \(k=8\) verifier also reads the saved \(k=1,\ldots,7\) certificates,
checks that each recorded matching covers its negative side, and embeds
their payload hashes in the new certificate.  This links the coverage table
to the actual saved artifacts rather than treating it as an unverified
summary.

## 6. Reproducibility hashes

```text
base adjacency:
58d13df3354384968e9e8ae3f8a5c84d5425e7cd8a74860f7a73ef1a9f501cca

expanded adjacency:
045859f074e247db653f04bd19836d3fb59742fbadba55680d0e31cb64d3e630

expanded matching:
bfb87985e70fd68f4fb8e22b99e0c233eab1f079dded05b11670e2550509f0ee

9092 augmenting paths:
7cfbaac4688df69a30abaa6e2e5d6d009dcf3e7fef345dcd3f1714002d6e737c

certificate payload:
8796c075e147ff20bc9290919310ff7160f653fbb1000bee136587e8927057a1
```

## 7. Reproduction

```bash
python3 verify_q2_k8_reserve.py
pytest -q test_verify_q2_k8_reserve.py
```

The saved certificate is `q2_k8_extension_certificate.json`.
