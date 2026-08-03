# Second independent review: actual aggregate unit realization

Date: 2026-08-03

Verdict: **passed with the representative/cocycle and aggregate/raw scopes
retained**.

## Representative and normalization cocycle

Compatible representatives can be chosen simultaneously by taking the
literal quotient representatives

```text
R_j=F_j/G, B=P_A0/G, Q_j=B/R_j,
```

with `F_0` fixed.  The common product identity then gives `P_Aj=F_0Q_j`,
so the quotient row has zero affine right side.

If each associate class is normalized independently, normalization is not
required to be multiplicative.  Writing its fixed two-factor cocycle as
`kappa(X,Y)`, the same coefficient rows acquire fixed affine constants.  For
one leaf the quotient-row constant must be

```text
kappa_j=alpha_0+phi_0-phi_j-alpha_j.
```

This follows from the literal identity `P_A0 F_0=P_Aj F_j`.  Thus the fifth
row is still the coefficient combination
`PA0+F0-Fj-PAj`; only its affine constant changes.  The homogeneous rank,
minor and kernel conclusions are representative-independent.  The theorem
does not claim that an independently canonical normalization has zero
cocycle.

## Explicit aggregate minor and source subsystem

For `m` leaves, retain the rows `F0,PA0,F_j,PAj` and delete the `g` column.
In columns `(f,b,r_1,...,r_m,q_1,...,q_m)`, row elimination subtracting `F0`
from each `PAj` leaves an identity matrix.  Hence this is an explicit
`(2m+2)`-minor of determinant `+/-1` for every `m`, not a finite-rank guess.
It proves rank `2m+2`, saturated image, and the primitive one-dimensional
gauge kernel.

For the source-identity subsystem retain exactly `F0`, every `Fj`, and every
quotient identity row.  In a linear relation, the `q_j` columns first force
all identity coefficients to zero, the `r_j` columns then force all `Fj`
coefficients to zero, and the `f` column forces the `F0` coefficient to zero.
Thus these `2m+1` rows are independent.  Their two-dimensional kernel is
spanned by the aggregate gauge and the common spectrum shift.  This confirms
that the row selection in the audited report matches its stated “source plus
identity, complements unfixed” interpretation.

## Raw occurrences and projection

For a one-leaf split of `k>=2` occurrences into nonempty sets `R,Q`, the four
raw product rows are

```text
g+sum_R h,  f,  f+sum_Q h,  g+sum_all h.
```

The fourth equals the first plus the third minus the second.  The first three
have a unit rank-three minor using columns `g,f,h_q` for any occurrence
`q in Q`; hence the raw kernel has dimension `k-1` for every `k`.

The occurrence projection records `(sum_all,sum_R,sum_Q)`.  Its first row is
the sum of the other two, while one `R` and one `Q` column give rank two.
Its kernel therefore has dimension `k-2`, with an explicit basis of
within-`R` and within-`Q` difference vectors.  These vectors also kill every
raw product row.  A remaining raw kernel vector, for example `g=1` and one
`R` occurrence equal to `-1`, projects to the aggregate common gauge.

Thus the dimensions and interpretation in the first audit are exact for all
`k`, not extrapolated from `k<=10`.  They establish aggregate completeness
only after quotienting associate-normalization freedoms; no complete
multi-leaf raw-occurrence incidence theorem is claimed.

## Scope verdict

The actual identities realize the formal all-leaf aggregate coefficient
matrix, and fixing all aggregate absolute product observables leaves the
primitive coordinatewise gauge over the torsion-free exponent lattice.
They do not fix a power-large joint absolute profile at subpower cost and do
not improve the distance exponent.  With the stored kill ratio `7/9<80%`,
the correct campaign decision is freeze without promotion.

