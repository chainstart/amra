# Blind cross-audit protocol

Date: 2026-08-02

Window: 15:35--16:15 HKT

Status: FROZEN BEFORE AUTHOR SWAP

## Verdict contract

Each auditor must return exactly one of `PASS`, `PASS AFTER REPAIR`,
`REPAIR`, or `FAIL` for every theorem family.  A passing verdict requires:

1. reconstruction from the stated definitions, not merely rerunning the
   author's verifier;
2. an independent arithmetic or symbolic guard for every decisive
   constant, threshold, parity boundary, or first counterexample;
3. explicit checks of integrality, support, endpoint, and strictness
   quantifiers;
4. a firewall saying exactly which implication to the public problem is
   proved and which interface remains open;
5. source hashes and reproducible commands.

A counterexample to an intermediate lemma must be labelled separately
from a counterexample to the public problem.  An existential asymptotic
threshold must not be reported as effective.  Finite computation may
guard an identity but may not replace an all-parameter argument.

## Author swap

### Root audits OPG-1757

- Rebuild the four common-base decompositions and confirm their exponents,
  kernel degrees, lower-base polynomial budgets, and dominant endpoint
  coefficients.
- Check legality of the retained low/high binomial shifts throughout the
  claimed bulk ranges and the uniformity of the ratio estimate.
- Recheck `241 log s` against both exponential gaps, then splice the bulk
  theorem to the exact low columns and reverse top bands without a missing
  degree or small-parameter claim.
- Independently verify the fixed-depth negative coefficient and preserve
  the distinction between failure of termwise merging and failure of the
  transport itself.

### OPG author audits Erdős #776

- Reconstruct the dyadic congruence, canonical expansions, chamber signs,
  one-promotion legality, and the formulas for `gamma_3,...,gamma_6`.
- Verify the first negative rank-five member and the entire stable
  rank-six recovery, including every residue-class and threshold
  quantifier.
- Check that the family refutes only the fixed rank-five bridge, not the
  original capacity proposition or an adaptive-rank theorem.

### Erdős #776 author audits Erdős #1083

- Reconstruct the cyclotomic ratio bound with signed/contaminated
  quotients, the finite-shadow theorem and aperiodic escape, the full
  independent `Phi_6` cube rigidity, and the binary-box Hamming/entropy
  bound.
- Check mass conventions, divisibility in the correct quotient, all gcd
  and transversality hypotheses, the decimal exponent, and the uniform
  `X -> 3X` conclusion.
- Reject any inference across the still-open arbitrary-aperiodic,
  signed-residual, common-`X`, or outer-stability interfaces.

### Erdős #1083 author audits Erdős #809

- Rebuild the four disjoint missing-pair charges, the one-leaf interval,
  endpoint concavity, and both parity factorizations.
- Reconstruct the cyclic sharp graphs: edge count, minimum/maximum degree,
  opposite pair, and the eight `L_4(2)` templates.
- Audit the defect-slack corollary and the new recolouring stress test:
  rainbow `C_7`, `D_B=g`, and reserve size
  `delta+2*kappa-g-5 >= g`.
- Keep local repeated-colour provenance separate from hard global
  reserve failure and from the full public #809 statement.

## Freeze rule

At 16:15 no new theorem is admitted unless its full proof and independent
audit are already complete.  Remaining time is reserved for regression,
claim-ledger reconciliation, rendering/static hygiene, and the final
all-four open/closed status report.
