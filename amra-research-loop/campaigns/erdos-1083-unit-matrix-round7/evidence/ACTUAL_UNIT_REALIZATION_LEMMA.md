# Actual common-X aggregate unit realization and raw-occurrence firewall

## Minimal actual block

Work in the actual power-large simultaneous normal form from
`POWER_LARGE_SIMULTANEOUS_SWITCH_CORE.md`:

```text
F_j=G R_j,   P_A0=G B,   B=R_j Q_j,   P_Aj=F_0 Q_j.
```

Choose one leaf `j`.  This centre-leaf restriction is the smallest actual
paired-positive common-X block: both `P_A0=G R_j Q_j` and
`P_Aj=F_0 Q_j` are honest positive `0/1` masks in the same Laurent UFD
`Z[Gamma]`.

Use aggregate associate-unit variables

```text
(g,f,b,r_j,q_j).
```

The actual product and identity rows, in that column order, are

```text
unit(F_j)  :  (1,0,0, 1,0)
unit(F_0)  :  (0,1,0, 0,0)
unit(P_Aj) :  (0,1,0, 0,1)
unit(P_A0) :  (1,0,1, 0,0)
B=R_j Q_j :  (0,0,1,-1,-1).
```

This is exactly the formal `m=1` coefficient matrix.  The identity row is
the linear combination

```text
row(P_A0)+row(F_0)-row(F_j)-row(P_Aj),
```

including its right side, because the exact block has the common total
spectrum identity `P_A0 F_0=P_Aj F_j`.

The associate representatives may be chosen compatibly with the literal
factorizations, as when `R_j=F_j/G`, `B=P_A0/G` and `Q_j=B/R_j` are defined.
If every associate class is instead normalized independently, fixed monomial
normalization cocycles appear on some right sides.  They change neither the
coefficient rows nor their rank and kernel, but they must not be silently set
to zero in the affine system.

Stacking these rows for every `j` in any selected actual family gives the
formal all-`m` coefficient pattern on aggregate variables
`(g,f,b,r_1,...,r_m,q_1,...,q_m)`.  Thus the round-six matrix is genuinely
realized as an **aggregate incidence matrix** by the actual simultaneous
normal form.

## What is and is not fixed

The actual affine right sides are

```text
phi_j=unit(F_j), phi_0=unit(F_0),
alpha_j=unit(P_Aj), alpha_0=unit(P_A0),
```

subject to

```text
alpha_0+phi_0=phi_j+alpha_j.
```

Common X and paired positivity do not force the special values
`s_j a,2a,-s_j a,-2a` used by the old finite normalized example.  Those are
one absolute observable profile.  For arbitrary actual blocks the coefficient
matrix is the same, but the right sides are actual exponent vectors in
`Gamma`.

If all four product-unit observables are fixed, the minimal matrix has rank
four, a determinant-minus-one maximal minor, and primitive kernel

```text
(1,0,-1,-1,0).
```

For all `m`, the round-six proof gives the corresponding common gauge.  If
the complement rows are not fixed, the source-identity subsystem retains the
independent spectrum-shift direction `(0,0,1,0,1)` already visible for one
leaf.  Matrix realization therefore does not make absolute-spectrum
conditioning free.

## Full Laurent unit lattice and signs

The ambient exponent group `Gamma` is finitely generated and torsion-free,
so it is isomorphic to `Z^r`.  The primitive scalar incidence sequence
therefore tensors coordinatewise: after fixing the aggregate product
observables, its exponent kernel is one copy of `Gamma` along the gauge and
there is no new observable torsion or kernel caused by ambient rank.

The sign coordinate is also harmless at the aggregate level.  The actual
normal form has

```text
G(1)>=2, R_j(1)=S/g>0, B(1)=U/g>0,
Q_j(1)=U/S>0, F_0(1)=S>0.
```

Choosing each aggregate associate representative with positive augmentation
fixes its `+/-1` unit.  This does not control unrelated coefficient-ring
extensions, but none occurs in the stated ring `Z[Gamma]`.

## Raw factor-occurrence refinement

The aggregate realization is not literally the complete **raw occurrence**
matrix.  Suppose normalized `B` has `k` irreducible occurrences and one leaf
uses a nonempty submultiset for `R_j`, with the complement used for `Q_j`.
On raw occurrence-unit variables `(g,f,h_1,...,h_k)`, the four product rows
have rank three.  Their kernel has dimension `k-1`:

- one direction projects to the aggregate `G/R_j/B` gauge;
- `k-2` directions redistribute associate units with zero total separately
  inside the `R_j` and `Q_j` occurrence groups.

The latter directions vanish under projection to `(b,r_j,q_j)` and change no
actual product mask.  They are internal normalization gauges, not additional
geometric observables.  A canonical choice of normalized irreducible
occurrences quotients them out.  Across many leaves the shared divisor
incidence may add further cross-row normalization relations; the archive does
not derive a power-large factor-occurrence matrix and should not call the
aggregate variables the complete raw list.

## Exact conclusion and remaining gap

The actual-block realization lemma is therefore:

> Every selected power-large simultaneous normal-form block realizes the
> formal all-`m` coefficient matrix on aggregate Laurent associate units.
> Coordinatewise over the actual exponent lattice, fixing every absolute
> source and complement product unit leaves only the primitive common gauge.

It does not prove that the joint absolute product-unit profile is constant on
a power-large fibre at subpower cost.  It also does not control all-target
occurrence mass, distance-label fibres, or outer stability.  No public
distance exponent changes.

## Reproduction

```text
ulimit -v 3145728; timeout 180s python3 evidence/verify_actual_unit_realization.py
```

The bounded verifier reconstructs the minimal aggregate rows, primitive
minor, gauge and spectrum shift, and checks occurrence refinements with two
through eight factor occurrences.  The all-`m` statement follows from
stacking the actual identities and the symbolic round-six unit-minor proof,
not from finite extrapolation.
