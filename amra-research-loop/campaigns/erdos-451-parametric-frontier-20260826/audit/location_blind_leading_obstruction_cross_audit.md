# Same-model cross-audit of the location-blind leading obstruction

## Verdict

**PASS.**  I reconstructed the location-blind block algebra, the finite
safe-tail inequality, the actual adaptive specialization, and the leading
linear-program certificate directly from `formal/ParametricRanges.lean`.
The stated iff and endpoint no-go are correct for the explicitly defined
`LocationBlindTermwiseLeadingCertificate` class.  The evidence also draws
the essential formalization boundary correctly: the reduction from every
growing nonuniform subdivision to that LP image is a natural-proof bridge,
not a Lean theorem.

This was a read-only, same-model cross-audit.  It is not an independent human
peer review and I did not rerun the already frozen full Lean replay.  No
author source, evidence, or structured artifact was modified.

## 1. Exact `T1/T2` invariant

Lean defines

\[
 \log T_1={\log D+r\log\lambda+2\log W\over 2r-1},
\]

\[
 \log T_2={\log\delta+2\log W-\log D-r\log\lambda\over r-1}.
\]

For `r>=2`, both denominators are nonzero.  Multiplying by `2r-1` and
`r-1` cancels `logD` and `r*logLam` exactly and leaves

\[
 (2r-1)\log T_1+(r-1)\log T_2
 =\log\delta+4\log W.
\]

This is precisely `locationBlind_first_two_log_invariant`; it makes no
balanced-lambda assumption.  The theorem statement and proof have matching
quantifiers and no hidden positivity premise is used beyond `r>=2` for the
denominators.

## 2. `W>=1` monotonicity

`locationBlind_first_two_invariant_ge_delta_of_W_ge_one` substitutes
`logW=log W` into the exact identity.  From `W>=1`, Lean obtains
`log W>=0`, hence

\[
 \log\delta\le\log\delta+4\log W.
\]

The direction is correct: increasing the denominator parameter cannot make
the weighted first-two-term invariant smaller.  The evidence does not claim
that either individual term is monotone in `W`.

## 3. Finite safe-tail budget

The finite theorem assumes the two separate block bounds

\[
 \log T_1\le-\alpha M,\qquad
 \log T_2\le-\beta M,
\]

and the genuine safe-tail input

\[
 -(1-\theta)K-M-C\le\log\delta+4\log W.
\]

Because `r>=2`, the weights `2r-1` and `r-1` are nonnegative.  Multiplying
the separate bounds by those weights, summing, and inserting the exact
invariant gives

\[
 ((2r-1)\alpha+(r-1)\beta)M
 \le(1-\theta)K+M+C.
\]

This exactly matches
`locationBlind_termwise_block_budget_obstruction`.  In particular, the
extra `+M` on the right is present; the evidence does not silently use a
stronger tail threshold without the `loglog(k)` loss.

The final source also proves `locationBlind_endpoint_excess_budget`.  From
the two bounds `log(Ti)<=-M-q`, the invariant and safe tail first give

\[
 (3r-2)(M+q)\le(1-\theta)K+M+C.
\]

The endpoint premise gives `1-theta<=3c`; multiplying by `K>=0` and using
`cK-DM<=rM` yields

\[
 (1-\theta)K\le3cK\le(3r+3D)M.
\]

Subtracting the `(3r-2)M` part proves exactly

\[
 (3r-2)q\le(3D+3)M+C.
\]

The companion `locationBlind_endpoint_termwise_no_go_of_excess` assumes the
strict reverse inequality and derives the advertised contradiction.  Both
the direction and the constant `3D+3` are correct.  Their comments also
correctly say that extracting a sequence with growing excess from arbitrary
subdivisions is not asserted by either Lean theorem.

## 4. Actual adaptive invariant

For the actual adaptive definitions,

\[
 \log T_1={\log Z-(r+1)K\over2r-1},\qquad
 \log T_2={(r+\theta)K-\log Z\over r-1}.
\]

The same weighted sum cancels `logZ` and equals `(theta-1)K`.  Therefore
`adaptive_first_two_log_invariant` is exact even though
`Z=max(logN,V_r)` and depends on the balancing parameter `Q`.  The follow-up
budget theorem correctly derives

\[
 ((2r-1)\alpha+(r-1)\beta)M\le(1-\theta)K.
\]

This is consistent with, but logically distinct from, the generic
location-blind safe-tail theorem.

## 5. Leading-certificate iff

The formal class is explicitly defined by the existence of real
`rho,alpha,beta` satisfying

\[
 \rho>0,\quad \rho\ge c,\quad \alpha>1,\quad\beta>1,
 \quad(2\alpha+\beta)\rho\le1-\theta.              \tag{1}
\]

For `c>0`, the forward implication is correct: `2alpha+beta>3`, positivity
of `rho`, and `rho>=c` imply `3c<1-theta`, hence
`c<(1-theta)/3`.

For the reverse implication, the proof chooses a common
`alpha=beta=q>1` strictly below `(1-theta)/(3c)` and takes `rho=c`.
Then `(2alpha+beta)rho=3qc<1-theta`, so every field of (1) is satisfied.
Thus

\[
 \operatorname{LocationBlindTermwiseLeadingCertificate}(\theta,c)
 \iff c<(1-\theta)/3
\]

is exact under the displayed hypothesis `c>0`.

`locationBlindTermwiseLeadingCertificate_no_go` is then a direct
contradiction for `c>=(1-theta)/3`.  It is scoped to the named LP class and
does not quantify over proofs, subdivisions, bad sets, or all methods.

## 6. Natural bridge versus Lean theorem

I specifically audited the potentially misleading handoff from arbitrary
growing subdivisions to (1).

The natural proof in `evidence/adaptive_unbalanced_partition_frontier.md`
uses three additional arguments:

1. the PI cardinality tail leaves at least half the supplied primes at
   deterministic distance at least `M_k/2` from `k`;
2. a location-blind partition of that whole tail, together with a
   nonnegative total `o(k^theta/log k)` bound, permits weighted Markov
   extraction of blocks carrying `1-o(1)` of the length and satisfying
   `A_j+B_j=o(1/log k)`; and
3. the endpoint size and `lambda_j,W_j>=1` give the lower order scale
   `r_j>=c log(k)/loglog(k)-O(1)`, producing the limiting variables in (1).

Those arguments are stated as a natural proof, including the weighted
selection calculation.  Lean does **not** define a sequence of partitions,
formalize the PI cardinality-tail reduction, or prove that every such
growing certificate maps to `LocationBlindTermwiseLeadingCertificate`.
Instead it defines the LP image directly and proves its algebraic frontier.

The boundary is stated honestly in `formal/README.md`,
`evidence/lean_parametric_ranges.md`,
`evidence/lean_parametric_ranges.json`, `decisive_lemma.json`, and
`decision.json`.  I found no claim that the arbitrary-subdivision-to-LP
bridge is kernel checked.  Accordingly, the enlarged architecture barrier
has natural-proof status, while the block invariant, finite budgets, and LP
iff/no-go have kernel-checked status.

## 7. BHP specialization and evidence boundary

At `theta=21/40`,

\[
 {1-21/40\over3}={19\over120}.
\]

The formal no-go theorem correctly excludes
`LocationBlindTermwiseLeadingCertificate(21/40,c)` for
`c>=19/120`.  Separately, the positive unconditional BHP theorem proves the
range for every fixed `0<c<19/120`.  Neither theorem includes the endpoint,
improves the unconditional constant, or closes Erdos 451.

The final guarded replay reports exit `0` and no `sorryAx`.  Its current
`ranges-build.log` records exactly
`[propext, Classical.choice, Quot.sound]` for both endpoint-excess lemmas,
the leading-certificate iff, and the two scoped no-go theorems.  The current
`ParametricRanges.lean` SHA-256 is
`ab6bfdcc85dec37b7489a2f2f615e7976136e9a9a3c40cd9ccde8324b064a0e5`;
I checked it directly against `formal/logs/final-sha256.txt`.

The verification statement above is a read-only audit of the final source,
recorded build output, and hash.  I did not independently rerun Lean, and it
does not promote the natural arbitrary-subdivision-to-LP bridge to a formal
theorem.

No correction is required.
