# Independent-audit protocol for the `1/16` certificate

## Separation requirement

The auditor must not be the session that authored `formal/erdos451-c16.patch`.
The first reconstruction pass should use only the public paper, the pinned
upstream Lean theorem, and the exact target statement below.  Do not inspect the
candidate patch or `evidence/lean_c16_certificate.md` until after recording the
reconstructed inequalities and any failure point.

## Frozen target

With `theta=21/40` and the same short-prime-interval input as the public proof,
show that for all sufficiently large `k` and every integer `n` satisfying

```text
2k < n <= exp((log k)^2 / (16 log(log k))),
```

the product `(n-k)...(n-1)` has a prime divisor in `(k,2k)`.

## Required checks

1. Reconstruct the large-range choice of `r0` and every exponent margin without
   copying the candidate patch.
2. Treat `r=3` explicitly; state whether a uniform logarithmic envelope is
   valid there.
3. Check the first two Konyagin terms, the third term, and the additive
   `2 r lambda` term separately.
4. Verify the passage from `(k,k+3k^theta)` to `(k,2k)` and all sufficiently
   large thresholds.
5. After freezing the natural reconstruction, inspect and replay
   `formal/erdos451-c16.patch` with `formal/verify_guarded.sh`.
6. Compare theorem quantifiers and definitions with Erdős #451, list every Lean
   axiom, and report any hidden dependence or mismatch.
7. Repeat the primary-source priority search.  Failure to find `1/16` must be
   recorded as `priority_uncertain`, not as a novelty proof.

## Promotion gate

Promotion remains forbidden unless the reconstruction, statement match,
dependency check, and promotion decision all pass.  A successful kernel replay
alone does not satisfy the independent-reconstruction field because the patch
has already been author-replayed in this campaign.
