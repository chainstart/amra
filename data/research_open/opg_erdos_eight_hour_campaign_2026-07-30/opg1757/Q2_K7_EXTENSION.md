# OPG-1757: reserve-expanded \(q=2,k=7\) layer

Date: 2026-07-30

## 0. Status

- **FINITE EVIDENCE:** exhaustive enumeration of the stated move family on
  \(K_6\) gives a matching of all 172800 negative objects.
- **HUMAN PROOF:** every candidate reserve edge is a valid protected forest
  basis exchange and has the tagged inverse already proved in
  `MULTIEDGE_RECOLORING_ATTACK.md`.
- **OPEN GAP:** neither the matching nor the observed short augmenting paths
  constitute a uniform Hall theorem.

## 1. Complete finite graph

The source and target definitions are unchanged.  At \(k=7\), a pair has
nine coloured edge copies.  The base candidate graph contains all valid
direct moves and all valid exchanges of \(E=01\) with one red edge.  The
expanded graph additionally contains every protected one-edge forest basis
exchange after deterministic global opening, subject to preserving the
active vertex set and the marked blue edge \(F=23\).

Exact counts are:

\[
|\mathcal N_7|=172800,\qquad
|\mathcal P_7|=177984.
\]

| graph | edges | maximum matching | deficiency |
|---|---:|---:|---:|
| direct/single | 306408 | 167488 | 5312 |
| reserve-expanded | 8160144 | 172800 | 0 |

The base maximum matching has the alternating Hall witness
\[
|S|=17656,\qquad |N(S)|=12344,\qquad
|S|-|N(S)|=5312.                                    \tag{1}
\]

Starting from that matching, all 5312 defects are removed:

| augmenting path length | count |
|---:|---:|
| 1 | 667 |
| 2 | 4557 |
| 3 | 88 |

The new-reserve-edge counts per path are:

| new edges used | paths |
|---:|---:|
| 1 | 715 |
| 2 | 4510 |
| 3 | 87 |

The final matching has one distinct ordinary positive target for every
negative source.  Thus
\[
\boxed{\nu(G^{\rm reserve}_{q=2,k=7})=172800.}       \tag{2}
\]
Equation (2) is an exhaustive finite statement, not a general injection
formula.

## 2. Compact construction and resources

The verifier does not store millions of Python integer objects in nested
adjacency lists.  It streams each generated row into compact CSR arrays:

- unsigned 64-bit row offsets;
- unsigned 32-bit target indices.

The deterministic allocation is:

| object | bytes |
|---|---:|
| base CSR | 2608040 |
| expanded CSR | 34022984 |
| combined CSR | 36631024 |

One timed reproduction on the current host used:

```text
wall time       26.06 s
maximum RSS     130424 KiB
swaps           0
```

These runtime numbers are environmental observations.  Only the exact CSR
byte counts are certificate fields.

## 3. Reproducibility hashes

```text
base adjacency:
76050fe93551c56957defe1902d636002de5fec4503f6eb229ded3517eb498b7

expanded adjacency:
fc8eeaeb6ef1a362fd5a7c808f5c732c2483932f73a52c9b1a067721a4567611

expanded matching:
1609b01783f1d5760375e37404836006d9f2b9509d7cca0d14bff3ea1913a69c

5312 augmenting paths:
998d82b5c3eca4323c7790fa54d551856e89398ca351e54e1d47d777037b9322

certificate payload:
d43580171d6336c9f8095d8848b40f0a7937faea601f2650862eedd15d81818f
```

The expanded graph has left degrees between 38 and 60, but right degrees
between 6 and 142.  Therefore the crude sufficient condition
“minimum left degree at least maximum right degree” does not explain Hall:
\[
38<142.
\]
The proof must exploit exchange geometry or fibre structure rather than
only extremal degrees.

## 4. Interpretation

The same one-reserve move family now closes three consecutive difficult
layers \(k=5,6,7\).  The required paths remain of bounded observed length,
but the bound has increased from two to three.  This supports an
alternating-channel strategy; it does not prove that a fixed bound persists
for other layers or larger active sets.

The structural reduction and exact pending lemma are stated in
`Q2_UNIFORM_HALL_ATTACK.md`.

## 5. Reproduction

```bash
python3 verify_q2_k7_reserve.py
pytest -q test_verify_q2_k7_reserve.py
```

The saved certificate is `q2_k7_extension_certificate.json`.
