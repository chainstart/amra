# Independent audit: tropical endpoint-gap shape

Verdict: **PASS; freeze as a scoped local theorem without public promotion**.

The audit reconstructed the support identities and equality-wall argument
without importing the author verifier.

## Product and scalar laws

For positive masks, every coefficient at an attained sum is positive, so
the product support is exactly the Minkowski sum.  If
`A={a_0<a_1<...}` and `B={b_0<b_1<...}`, the least non-minimal sum is

```text
min(a_1+b_0,a_0+b_1).
```

Subtracting `a_0+b_0` proves the left min law.  Applying the same argument
to the reversed order proves the right min law, while the two extreme sums
give width additivity.  Collisions do not alter this because coefficients
are positive.

Positive scalar dilation multiplies both gaps and width by the scalar.
Negative dilation reverses the fixed natural order and swaps the two gaps;
after division by width the pair is constant on either sign class.  The
argument only uses distinct ordered support points and is unchanged when a
natural endpoint is zero.

## Simultaneous feasibility and one equality row

The actual positive common-spectrum product gives

```text
L=min(a_j^-,c_-|lambda_j|),
R=min(a_j^+,c_+|lambda_j|).
```

Thus every actual row has

```text
|lambda_j| >= max(L/c_-,R/c_+).
```

If the thresholds differ, equality at the smaller threshold is infeasible
at the other endpoint.  Equality can therefore occur only at the larger
threshold.  If the thresholds agree, both equalities select that same
magnitude.  Same-sign distinct scalars have distinct magnitudes, so the
union of the two equality sets has size at most one.

After deleting that row, both source gaps are strict.  Each min equation
then uniquely forces the corresponding complement gap to `L` or `R`.
Together with the constant normalized source pair, the combined profile has
range exactly one on at least `|J_sigma|-1` rows.  Removing one row preserves
the inherited `t^(5/9-o(1))` size.

## Dependency and scope audit

The proof requires actual positive masks; it does not apply to arbitrary
signed factors where cancellation can change support.  It controls only the
first interior support point at each endpoint.  The mixed sum `2+3=5` in
`{0,2,100}+{0,3,100}` confirms that deeper layers do not obey the same
coordinatewise-min law.

No map from these gaps to new target-target Euclidean distances is proved.
All-target occurrence, collision-fibre savings and outer stability remain
open.  Consequently the public dimension-three `3/5` exponent is unchanged.
External novelty and priority remain uncertain.

## Reproduction

```text
AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/erdos-1083-shape-profile-round10/audit/verify_tropical_endpoint_gaps_independent.py
```

The author verifier was separately rerun under the same bound and returned
`PASS`, with the recorded SHA-256 matching the evidence ledger.
