# Independent audit: actual aggregate unit realization

Date: 2026-08-03

Verdict: **pass with the aggregate/raw distinction retained**.

## Reconstruction

Starting only from

```text
F_j=G R_j,  P_A0=G B,  B=R_j Q_j,  P_Aj=F_0 Q_j,
```

the independent verifier rebuilds the coefficient rows on
`(g,f,b,r_j,q_j)`.  They are exactly the formal round-six rows.  The fifth
identity row is

```text
row(P_A0)+row(F_0)-row(F_j)-row(P_Aj),
```

With quotient-defined compatible associate representatives its right side
vanishes by `P_A0 F_0=P_Aj F_j`.  If the five factors are instead normalized
independently, fixed monomial cocycle constants can appear on that affine
right side; the coefficient-row dependence, rank and kernel are unchanged.
It is therefore not an extra linear observable.

For `m=1,...,12`, an independently generated all-leaf matrix has rank
`2m+2`, nullity one, a unit maximal minor, and primitive kernel

```text
(g,f,b,r_1,...,r_m,q_1,...,q_m)
=(1,0,-1,-1,...,-1,0,...,0).
```

Deleting all complement-product rows leaves rank `2m+1` and the additional
common spectrum-shift kernel.  Thus the special scalar right sides from the
old finite example are not forced by common `X`; arbitrary actual exponent
vectors remain subject only to their common-spectrum relation.

## Ambient units and occurrences

A finitely generated torsion-free abelian `Gamma` is free, so tensoring the
primitive split exact sequence with `Gamma` is coordinatewise and creates
no additional aggregate observable kernel or torsion.  Positive
augmentation fixes only the `+/-1` coordinate, as the report states; it
does not fix the monomial exponent.

The raw-occurrence qualification is essential.  If `B` has `k` occurrences
split nontrivially between `R_j` and `Q_j`, the four product rows on
`(g,f,h_1,...,h_k)` have rank three and nullity `k-1`.  For every split and
`2<=k<=10`, the audit reconstructs `k-2` internal directions in the kernel
of the aggregate projection, plus one direction projecting to the aggregate
gauge.  These are normalization freedoms, not new product observables.
Nothing in this calculation proves a complete multi-leaf raw-occurrence
matrix.

This normalization-cocycle distinction also prevents an unjustified claim
that a convenient zero affine right side is canonical.  The audited theorem
is about the coefficient matrix and its homogeneous kernel; actual absolute
product-unit profiles remain data to be conditioned.

## Scope decision

The actual identities do realize the all-`m` matrix **on aggregate associate
units after normalization**.  They do not provide a subpower bound for the
number of joint absolute product-unit profiles.  Consequently the
power-large spectrum-fixed fibre, all-target occurrence mass, distance-label
fibre, stability transfer, and any exponent improvement remain open.

Mechanism statuses are matched literally: the aggregate realization and
conditional primitive-gauge claims are proved; independent identity rank,
automatic special right sides, sign torsion, tensor-created kernel, raw
completeness, raw observability, and source-only gauge uniqueness are killed;
the conditioning claim survives and the public-exponent leap is frozen.
The stored kill ratio `7/9` remains below the 80% gate, so no advancement is
permitted.
