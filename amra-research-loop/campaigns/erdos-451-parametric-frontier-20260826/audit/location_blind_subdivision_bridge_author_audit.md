# Author audit of the location-blind subdivision bridge

## Verdict and status

**PASS within the stated certificate class.**  This is an adversarial audit
by the author of the new bridge, not an independent audit and not human peer
review.  I checked the natural instantiation against the exact Lean theorem
and tried to remove every uniformity hypothesis.  The arbitrary finite and
growing block-count quantifier survives; fixed safe-tail and order-loss
constants are indispensable.

## Quantifier audit

- `theta,c,C,D` are fixed before `k` tends to infinity; `0<theta<1`, `c>0`,
  and `c>=(1-theta)/3`.
- At each `k` the index set may be any nonempty finite set.  Its cardinality,
  block positions, orders, scales, and positive lengths may all depend on
  `k`.
- The blocks cover the whole deterministic PI cardinality tail, and their
  positive lengths sum exactly to its length.  No comparable-size or
  polylogarithmic-cardinality premise was used.
- The losses `C,D` are common to every block and independent of `k`.  This is
  a substantive source-geometry hypothesis, not a consequence of weighted
  averaging.
- The ledger is termwise nonnegative and has total
  `o(H_k/log k)`.  Cancellation or a signed combined estimate is outside the
  theorem.

## Reconstruction of the finite proof

The weighted average bound selects one block with

```text
exp(logT1)+exp(logT2)<=exp(-M-q).
```

Because both exponentials are positive, each log is at most `-M-q`.  With
`M>0` and `q>=0`, the first log is negative, so the conditional order premise
is legally invoked.  The order lower bound gives

```text
3cK-(3D+2)M <= (3r-2)M.
```

Multiplication by `q>=0` preserves its direction.  The global separation
then implies the strict block excess

```text
(3D+3)M+C < (3r-2)q,
```

contradicting the previously checked endpoint-excess theorem.  No division
by a block length, `M`, or a possibly negative coefficient is hidden in the
Lean proof.

## Cardinality and geometric audit

For `m` distinct natural offsets, at most `floor(m/2)` offsets are below
`floor(m/2)`, so at least `floor(m/2)` remain in the deterministic tail.  The
Lean statement uses natural subtraction and was checked at the parity edge.
The partition-length identity is pure telescoping; positivity of lengths is
an explicit certificate premise rather than an inferred property of
arbitrary cut points.

The PI step guarantees only this total tail mass.  It does not justify
short-interval prime counts or a cover selected after observing the primes.
Those stronger operations remain excluded.

## Little-o and endpoint audit

The normalized average is strictly positive, so
`q_k=-M-log(e_k)` is defined.  The relation
`e_k=o(exp(-M))` is exactly `q_k->infinity`.  For fixed losses,
the left side of the finite separation is `O(M^2)`, while the positive
coefficient on its right is eventually at least `2cK`; since
`K/M^2->infinity`, even `q_k>=1` suffices.  This closes the equality endpoint
without pretending that there are fixed `alpha,beta>1` limits.

I also checked that the leading LP theorem is not used as the endpoint
extraction theorem.  The new bridge goes through the exact finite excess
bound, which permits effective exponents tending down to one.

## Counterexample audit

The one-block examples in
`evidence/location_blind_subdivision_bridge.md` satisfy the two log equations
exactly.  Allowing `D_k` to grow like `K/M` admits a fake fixed-order family;
allowing `C_k` to absorb `(3r_k-2)q_k` admits an arbitrary-order fake family.
They are correctly labeled abstract counterexamples to weakened assumptions,
not Konyagin constructions and not counterexamples to the prime theorem.

## Formal boundary and residual risk

The finite extraction/no-go, cardinality tail, and partition identity are
kernel checked.  The source formulas that yield uniform `C,D`, and the
standard asymptotic passage `K/M^2->infinity`, remain natural mathematics in
the evidence note rather than a single Lean sequence theorem.  A future
independent audit should inspect that source-to-uniform-loss mapping.  This
author audit does not amend the campaign's older independent-audit verdict.
