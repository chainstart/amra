# Adaptive unbalanced author audit (not independent)

## Scope and maturity

This is an adversarial audit by the author of
`evidence/adaptive_unbalanced_partition_frontier.md`.  It does not replace the
campaign's existing independent audit, which covered the earlier balanced
theorem, nor does it promote the new `0<theta<1` extension to kernel-checked
status.

## Attaining theorem checks

- **Source interface:** the pinned Konyagin theorem accepts every integer
  `r>=2` and every real `lambda>=1`.  The inequality
  `n r!<=k^(r+theta)` belongs to the old parameter selection and is not a
  theorem hypothesis.
- **Stopping-rule endpoint:** existence at
  `R=ceil(a log(k)/loglog(k))` spends only `O(log k)` on `log(R!)`, while the
  gap `a-c` contributes order `log(k)^2/loglog(k)`.
- **Lower order:** at `r=1`, the new upper threshold is
  `k^2(log k)^(-Q)`.  The retained large-range lower bound
  `n>k^(2+theta)/2` therefore forces `r>=2` for every fixed `theta>0`.
- **Interval nonemptiness:** `V_r<=U_r` is exactly
  `Q(3r-2)loglog(k)<=(1-theta)log(k)` and follows uniformly from
  `r<=ceil(a log(k)/loglog(k))` and `3Qa<1-theta`.
- **First terms:** with `Z=max(nr!,V_r)`, the bounds `V_r<=Z<=U_r` give both
  first terms at most `(log k)^(-Q)` without assuming that the maximum's
  second branch is active.
- **Minimality at r=2:** when `lambda>1`, failure of the stopping rule at
  `r-1` is valid even for `r=2`, because it is precisely the already checked
  failure at order one.
- **Additive term:** the uniform estimate
  `lambda<=k^(theta/r)(log k)^(3Q)` uses fixed `theta>0`; its conclusion is not
  uniform as `theta` tends to zero with `k`.
- **Third term:** bounded `r` gives a negative power of `k`; growing `r` is
  controlled by `r<=a log(k)/loglog(k)`, and
  `a<(1-theta)/3<(1-theta/3)/2` gives strictly more than one logarithmic
  power of decay.
- **Prime input:** the general theorem remains conditional on `PI(theta)`.
  Only `theta=21/40` is discharged by the pinned BHP input, and its constant
  remains every `c<19/120`.

## Enlarged barrier checks

- **No outer-half assumption:** `PI(theta)` is used only through a total
  lower bound `M_k`.  Since fewer than `M_k/2` integers are closer than
  `M_k/2` to `k`, at least `M_k/2` supplied primes are in the deterministic
  tail beginning at `k+M_k/2`.
- **Correct safe scale:** on that tail the full factor group requires
  `delta` at least a constant multiple of `k^(theta-1)/log k`; a shorter
  contiguous group cannot lower it.  The lost logarithm produces the single
  `+loglog(k)` term in the invariant ledger and does not change its leading
  face.
- **Weighted partitions:** the no-go assumes the whole deterministic tail is
  partitioned and that nonnegative block estimates are summed.  A weighted
  Markov argument then selects blocks carrying almost all tail length with
  `A_j+B_j=o(1/log k)`, even when the finite number of blocks grows with `k`.
- **Equality:** at `c=(1-theta)/3`, the cardinality-tail correction leaves
  only `O(loglog k)` slack, whereas `r_j q_k` is much larger for `r_j` of
  order `log(k)/loglog(k)` and `q_k->infinity`.
- **Explicit exclusions:** the barrier does not cover a sparse cover selected
  after enumerating actual prime locations, cross-block cancellation, a
  stronger local prime theorem, a stronger Konyagin estimate, or a direct
  estimate of the true bad set.  It is only a no-go for the location-blind,
  independent nonnegative, little-o certificate class defined in Section 5.

## Remaining verification gap

The new adaptive attaining theorem and the enlarged barrier require a fresh
independent reconstruction.  The compiled Lean theorem still has the window
`9/23<theta<1`; no new Lean theorem is claimed here.  The guarded finite replay
is a transcription check, not proof of either quantified statement.
