# OPG-1757 transfer result: author-swap audit handoff

## Claims to audit independently

1. Reconstruct the four common-base sums from the old fixed-page formulas,
   rather than trusting the new template functions.
2. Recompute effective height `deg_s-j` and verify the exact top templates
   (6)--(8) in `COMPLETE_LOG_LAYER_THEOREM.md`.
3. Recompute the two bivariate complete-channel identities and check that
   substituting `y=e^(2x)` gives strict coefficients from degrees 8 and 10.
4. Check the growing page decomposition
   `A_q(1+o(1))+A_p(1+o(1))`, especially that every third candidate is either
   `o(A_q)` or `o(A_p)` independently of the ratio `A_q/A_p`.
5. Audit the single-threshold quantifier: four certificate thresholds, finite
   pigeonhole, and the bounded/趋∞ integer-subsequence dichotomy.
6. Audit the old lower-bound implication and the three-way degree splice.

## Effective-bound audit

1. Verify the binomial product estimate (3)--(4) in
   `EFFECTIVE_GAP_BOUND.md`, including the definition
   `Q=r(|ell|+r)`.
2. Check that multiplication by `k!` in `fixed_index_threshold` produces
   `(2a)^(k-j)(k)_j`, and that its `E_k` majorizes every lower power.
3. Verify independently the four maxima for `k<1000`, especially the
   117-digit odd-page maximum at `k=999`.
4. Check shifted coefficientwise nonnegativity of the retained `p` kernels
   and page `q=p-1` kernels.
5. Re-derive the growing sufficient and page majorants, including the
   `j=2` binomial ratio and
   `s^(-delta)<(242/241)^(delta shift)(241/242)^(delta k)`.
6. Check exact `Fraction` sums and monotone consecutive ratios at `k=1000`.
7. Confirm that `s>=242^2` makes every required binomial denominator at
   least `s`.

## Firewall

The audit should reject any wording that promotes:

- the finite stress scan to a proof;
- the effective low-gap threshold to an effective complete-transport
  threshold (the old high-range threshold is still ineffective);
- eventual transport positivity to all stable finite `s`; or
- the transport result to the original OPG-1757 proposition.
