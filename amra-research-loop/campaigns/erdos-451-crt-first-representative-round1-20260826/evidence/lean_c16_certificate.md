# Lean certificate for the `1/16` lower-bound constant

## Exact result

At upstream commit `92a033fa99f0a53a3c16257c47e3d9e04dfc3f55`, the public
formalization proves the denominator-`20` theorem.  The replayable patch in
`formal/erdos451-c16.patch` strengthens its large-`n` branch and proves:

> For all sufficiently large natural numbers `k` and every integer `n` with
> `2k < n` and
> `n <= exp((log k)^2 / (16 log(log k)))`, there is a natural prime `p` with
> `k < p < 2k` such that `p` divides `Pprod k n`.

Here `Pprod k n` is the upstream definition of
`(n-k)(n-k+1)...(n-1)`.  Thus the formal statement matches the forbidden-prime
interval in Erdős #451 and gives the lower-bound constant `1/16`, subject to
the same short-prime-interval input as the published proof.

This changes the explicit constant in the lower-bound exponent from `1/20` to
`1/16`.  It does not determine the main term, prove an upper bound of the
conjectured scale, or close the public estimation problem.

## The non-cosmetic repair

Simply replacing `20` by `16` is not valid.  The old large-range proof uses one
uniform envelope for the third Konyagin term.  With the larger reference order

```text
r0 = ceil(log k / (8 log(log k))),
```

that envelope no longer proves `log(k)^(-10/9)` at the boundary `r=3`.  Lean
rejected this exact step.  The repaired proof splits the cases:

- at `r=3`, it retains the stronger power saving `k^(-1/18)`;
- at `r>=4`, the original `log(k)^(-10/9)` estimate remains valid;
- the first large-range term uses `log(k)^(-38/35)`, still strictly smaller
  than `log(k)^(-1)`;
- the extra power-saving term is absorbed by the existing `poly_log_lt`
  asymptotic lemma.

Finally, `main_theorem_c16_two_k` formalizes
`k + 3 k^(21/40) <= 2k` for sufficiently large `k`, so the theorem does not
leave the passage to the public interval `(k,2k)` implicit.

## Reproduction and axiom audit

Run:

```bash
cd amra-research-loop/campaigns/erdos-451-crt-first-representative-round1-20260826/formal
./verify_guarded.sh
```

The script downloads the pinned upstream source, verifies its SHA-256, replays
the upstream theorem, applies the saved patch, verifies the patched SHA-256,
and replays both strengthened theorems.  It always starts Lake and Lean through
the OpenMath aggregate guard.

The final clean replay reported:

- upstream: 159.15 seconds, maximum RSS 7,830,580 KiB, zero swaps, exit 0;
- patched: 162.80 seconds, maximum RSS 7,856,592 KiB, zero swaps, exit 0;
- patched source SHA-256:
  `501b105cd48a6dfe24e4cb061b54c1a7c24f5cb1ec41d9a1ab95c619c3bc57a4`;
- patch SHA-256:
  `65bb2d1eccb534bf7318009d49553b76582de5612da5c2bdb20be51a4a2592ec`.

Lean printed the same dependency set for both strengthened theorems:

```text
[bhp, propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`.  The named `bhp` axiom is the same Baker--Harman--Pintz
short-prime-interval input used by the upstream formalization.  Konyagin's
estimate is proved inside the upstream Lean file rather than added as an axiom.

## Maturity and priority

This is evidence-strength level 1 under the AMRA policy: an exact
kernel-checked formal proof.  It is not, however, an independent reconstruction
in the phase-gate sense, because this same research session authored and
replayed the patch.  A different reviewer must still reconstruct the decisive
large-range argument before promotion.

The current arXiv paper, Erdős Problems page/discussion, and public source
repository found in the priority scan all state the denominator-`20` result;
the scan found no public `1/16` statement.  That negative search is not a
priority proof, so novelty remains `priority_uncertain`.
