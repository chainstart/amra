# Adversarial self-audit (not independent reconstruction)

## Checks survived

- **Factorial scale:** `log(R!)=O(L)`, not `O(L^2/l)`, for
  `R=O(L/l)`.  This is the source of the factor-two improvement in the
  frontier and is uniform for fixed `c,epsilon`.
- **Integer stopping rule:** the large-range lower endpoint makes `r>=3`, and
  the sharpened upper bound makes `r<=k^(1-theta)/2` for large `k`.
- **Lambda admissibility:** the balanced numerator exponent uses
  `u_r>theta`; hence the least-order inequality implies `lambda>=1`.
- **Non-balanced lambda:** the exact product identity is independent of
  `lambda`; unequal balancing cannot improve the leading exponent.
- **Bounded r:** the third term was split at `r<=5` rather than incorrectly
  forcing a logarithmic envelope onto `r=3`.
- **Growing r:** the third term is controlled uniformly with
  `T3<=k^(-1/(4r))`; the active frontier is below `1/5`, so this is more than
  enough.
- **Additive term:** its exact exponent is decreasing and has a positive gap
  below `theta` throughout the frozen theta range.
- **Range coverage:** Sections 2, 3, and 5 are reused with their original
  boundaries; only Section 6 changes.
- **Output interval:** the theorem first produces `(k,k+3k^theta)` and only
  then uses `theta<1` to embed it into `(k,2k)`.
- **Endpoint semantics:** `19/120` is a supremum.  The attaining theorem is
  stated for every fixed `c<19/120`, not at equality.
- **No-go semantics:** the barrier is explicitly about the nonnegative
  Theorem 4.1 upper-bound certificate.  It is not asserted for the true bad set
  or for correlated multiblock methods.

## Adversarial attempts that failed

1. Choosing `lambda` away from balance cannot reduce both `A` and `B` because
   their powered product is fixed.
2. Choosing larger `r` improves `T3` but strictly worsens the active A--B
   envelope.
3. Adding independent comparable blocks multiplies both sides of the final
   comparison and preserves the normalized obstruction.
4. Taking a longer `k^beta` block makes `(1-beta)/3` smaller.
5. Subdividing PI(theta) into shorter blocks assumes prime-distribution
   information not contained in PI(theta).

## Unresolved checks reserved for an independent reviewer

- Reconstruct the `r<=(c+epsilon)L/l` uniformity without relying on this
  document's notation.
- Check every inequality sign in the third-term bounded/growing-r split.
- Verify that the source's Theorem 4.1 constant is uniform in growing `r` from
  the paper/formal source.
- Replay the unchanged Sections 2, 3, and 5 dependency chain and the precise
  integer-base form of PI(theta).
- Stress-test the equality endpoint in Theorem B and the word "comparable" in
  the multiblock definition.

Because this audit is by the proof author, it does not satisfy AMRA's
independent reconstruction gate.
