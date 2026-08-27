# Echo mapping, absolute capacity, and the remaining fixed-cell obstruction

All statements in Sections 1--3 are author-verified elementary lemmas.  They
are scoped to the binary-reservoir family and do not close Erdős #25.

## 1. Exact rescaling of one attack

Fix `Q=2^k >= 4` and write the rare old survivor cell as

    C_Q = {Q r - 1 : r >= 1}.

For a selected index `r >= 2`, use modulus `n_r=Qr-2` and residue `1`.
A point `Qk-1` of `C_Q` belongs to this full class exactly when

    Qk - 2 is divisible by Qr - 2.

Since `gcd(Q,Qr-2)=2`, the compatible points in index coordinates form the
single progression

    k = r + h d_r,       d_r = Qr/2 - 1,       h >= 0.

The point `Qr-1=n_r+1` is the first compatible point at or after the onset.
Thus the simulator in `work/search_cross_scale_echoes.py` marks the delayed
class exactly by the slice `r, r+d_r, r+2d_r, ...`; it is not a probabilistic
approximation.

The first future echo occurs at

    r+d_r = (Q/2+1)r-1 < (Q/2+1)r.

So a target in this cell cannot be made free of its own future periodic echo
for more than the multiplicative factor `Q/2+1`.

## 2. Absolute capacity of the rare cell

For `N >= 2`,

    (H_N-1)/Q
      <= sum_{r=2}^N 1/(Qr-1)
      <= H_(N-1)/Q.

The lower bound uses `Qr-1 < Qr`; the upper bound uses
`Qr-1 >= Q(r-1)`.  Including `r=1` changes the sum by only `1/(Q-1)`.
Consequently the normalised harmonic capacity of the entire cell is

    lim_{N->infinity} [sum_{r<=N} 1/(Qr-1)] / log(QN) = 1/Q.

No attack schedule contained in `C_Q` can have asymptotic oscillation
amplitude larger than `1/Q`.  Therefore a proposed construction that obtains
longer echo-free spans by taking `Q -> infinity` automatically has amplitude
at most `1/Q -> 0`.

## 3. Fresh-cell compactness

Let `C_j` be pairwise disjoint periodic cells of densities `rho_j`, with
`sum_j rho_j <= 1`.  Suppose block `j` only changes membership inside its
fresh cell `C_j`.  At every cutoff its absolute normalised harmonic effect is
at most `rho_j+o_j(1)`.  Since a summable nonnegative sequence satisfies
`rho_j -> 0`, fresh disjoint cells cannot support infinitely many blocks of
nonvanishing amplitude.

The same observation applies to a strictly nested chain whose cell densities
tend to zero: activity below the `j`-th node is contained in that node and has
capacity tending to zero.  This is a dominated-capacity argument, independent
of any eventual-density charging inequality.

## 4. What is still open after these lemmas

The only unresolved sparse-cell scenario is repeated use of a fixed positive
capacity (or a nontrivial overlapping family) over unbounded logarithmic time.
For fixed `Q`, every selected target produces an echo within factor
`Q/2+1`, but the echo progressions can overlap and a schedule may select only
some targets.  The elementary echo bound alone does not prove that deletion
and recovery averages converge.

The guarded search alternates prescribed deletion and preservation windows,
adds a class only when a requested target has not already been deleted, and
then marks every echo exactly up to the cutoff.  It tests whether finite
fixed-`Q` schedules retain a late endpoint range after stratification by both
`Q` and cutoff scale.  Even a clean decay trend would remain finite evidence;
the next theorem-grade task is a fixed-cell echo-covering or Carleson bound.
