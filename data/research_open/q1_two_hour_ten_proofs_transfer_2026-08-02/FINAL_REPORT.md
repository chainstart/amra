# Final report — learning from `openai/ten-proofs` and transferring the methods

Research window: 2026-08-02 20:09:56--22:09:56 HKT  
AMRA baseline: `669bbad1908e7ab7d8382a8b508e67757006e90c`  
ten-proofs snapshot: `94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6`

## Executive conclusion

The requested transfer was productive, but it did **not** prove or disprove
any of the four original problems.  It produced four independently audited
packages and three particularly strong late-stage upgrades:

1. OPG-1757: a complete same-height generating-function aggregation closes
   the entire third-active logarithmic gap, and a second audit makes the
   resulting eventual theorem fully effective with one explicit 117-digit
   threshold for both transports.
2. Erdős #1083: a Galois pair-flip argument proves an unbounded coprimality
   theorem for the fixed five-point source at every pair of distinct scales,
   ruling out a genuine second row for the current signed escape.
3. Erdős #776: exact cap-depth analysis closes the last fixed-`c=2` region;
   combined with the earlier compactness theorem, every fixed promotion count
   `c>=2` is eventually positive (with a threshold depending on `c`).
4. Erdős #809: the naive imported colour-label invariant is proved vacuous,
   while the retained exact parity remainder yields a quantitative stability
   theorem and identifies the missing reserve-aware endpoint invariant.

These are substantial stage results with reusable proof infrastructure.
They are not yet a standalone solution paper to any original problem, and
“Q1 publishable” would require closing at least one firewall identified
below, polishing exposition, and external expert review.

## What was learned from ten-proofs

The useful lesson was not a single trick.  Across the ten result packages,
the successful pattern was:

- make the informal bridge into a literal finite or algebraic interface;
- attack that bridge with small exact countermodels before investing in it;
- replace the target property by a stronger conserved invariant;
- aggregate all same-scale terms before estimating their sign;
- separate a locally sharp core from the small device that repairs global
  tails or quantifiers;
- retain discarded positive remainders and convert small gains into a
  bounded-potential contradiction;
- treat interpolation, padding, legality, and model assumptions as proof
  obligations rather than prose;
- formalize the interfaces and independently reconstruct decisive constants.

That interpretation comes from the official [announcement](https://openai.com/index/ten-advances-in-mathematics/), the [collected paper](https://cdn.openai.com/pdf/ten-proofs-oai.pdf), the [reasoning walkthroughs](https://cdn.openai.com/pdf/reasoning-walkthroughs.pdf), and the [Lean repository](https://github.com/openai/ten-proofs/tree/main).  The local repository snapshot compiled in full (`lake build All`, 8666 jobs).  This confirms compatibility of the published formal artifacts with their pinned toolchain; it is not a substitute for independent journal peer review of every informal claim.

## Direct method transfer

| ten-proofs mechanism | Literal AMRA translation | Outcome in this round |
|---|---|---|
| Local sharp core plus remote correction | Separate 31 low columns, logarithmic gap, inherited high range, and top bands in OPG | Complete effective eventual third-active transports |
| Moving projection / aggregate before sign | Sum every equal-height OPG base, then substitute `y=e^(2x)` | Positive core `e^(2x)-(1+x)^2`; avoids false basewise positivity |
| Signed reconstruction with several invariants | Factorial energy, autocorrelation debt, prime shadows, valuations and common-scale algebra in #1083 | Exact stable ledger plus a sharp conditioning no-go |
| Identify an invariant's blind coordinate | Ask whether a fixed signed escape can hide a second scalar row | Galois pair-flips prove fixed-source coprimality at all distinct absolute scales |
| Finite falsification followed by parametric lifting | Search exact Macaulay states, retain the next remainder, then use scale limits and exact cap depths in #776 | Eventual positivity for every fixed `c>=2` |
| Stronger recursive labels plus a precommitted certificate | Seek endpoint agreement and reserve-Hall provenance for #809 colour labels | Bare label proposal refuted; candidate strengthened target isolated but remains open |
| Equality-core stability | Keep parity and concavity remainders near sharp #809 graphs | Explicit quantitative localization and reserve-paid sharp family |

## Lane results and next gates

### OPG-1757

The decisive repair was to stop estimating different bases separately.  The
complete top-height sums factor through

```text
e^(2x) - (1+x)^2 = x^2 + sum_(n>=3) 2^n x^n/n!,
```

so every relevant coefficient is positive.  Fixed and growing logarithmic
indices are then exhaustive, including the two-scale transition in the page
remainder.  The gap certificate and the independently effectivized old high
range splice with the universal low columns and top bands.  The final
117-digit threshold is therefore an effective bound for both complete
candidate transports.

Next gate: replace eventual complete-split positivity by universal finite
`s` control, then transfer beyond the third-active row and beyond the special
host family.

### Erdős #1083

The factorial energy

```text
delta(q) = (||q||_2^2 - q(1))/2
```

is a nonnegative integer which bounds edit distance to a mask and gives the
exact ordered autocorrelation debt of a mask product, with an exact
factorial-defect correction for general integral outputs.  This survived
hostile reconstruction after two necessary quantifier repairs.

The five-point mask `P=1+x+x^3+x^5+x^6` then serves two opposite purposes.
It refutes the shortcut from “no torsion zeros” to uniform conditioning, but
its reciprocal cubic has enough Galois symmetry to prove
`gcd(P(x^r),P(x^s))=1` for all `r!=s`.  Thus the explicit one-row signed
escape cannot be promoted to a different-scale two-row escape within the
stated augmentation range.

Next gate: move from this single source to a power-large common-mask theorem,
then establish the missing outer geometric stability that supplies a small
factorial defect.

### Erdős #776

Retaining one more canonical Macaulay remainder converted a finite atlas into
an unbounded multi-cap inequality.  Compactness at fixed promotion count
first proves eventual positivity for every `c>=3`.  For `c=2`, any bad
sequence is initially forced to satisfy

```text
k = O(q^(1/3)),  u = O(q^(2/3)),
limsup(2k/q^(1/3) + (u/q^(2/3))^2) <= 3^(2/3).
```

Exact least-cap depths then force the discrete phase `k=1` with equal depth
correction `h`; minimality leaves only `h=1,2`, and both exact surplus
polynomials have positive normalized limits.  Thus every fixed `c>=2` is
eventually positive in the relaxed no-borrow model.

Next gate: construct a potential uniform when the promotion count grows with
`q`, and prove the bridge from relaxed no-borrow positivity to the adaptive
seed statement required by Erdős #776.

### Erdős #809

The Ramsey-style proposal exposed its own missing interface.  Under the
current normal form every colour class is already an induced matching and
therefore two-colourable; moreover each matching has an independent edge-flip
gauge.  A label selected after seeing a Hall obstruction carries no content.
The viable invariant must precommit endpoint choices and pair them with
actual reserve tokens.

Keeping the full parity/concavity remainder nevertheless gives exact
near-sharp parameter localization and shows that the sharp repeated-colour
family pays all its defect from genuine reserve.

Next gate: prove the fixed-endpoint label-reserve Hall condition in the hard
B-opposite branch, then connect it to the untreated B-same and A branches.

## Quality control

- The frozen ten-proofs Lean aggregate compiled: 8666 jobs, no failure.
- The campaign suite passed 25 tests.
- Each lane's decisive identities were recomputed by a non-author program.
- The independent scans covered 85,278 Macaulay states, 13,313,069 #809
  scalar profiles, 26,165,382 feasible #809 instances, and exact OPG source
  spectra; these counts are finite evidence only where explicitly labelled.
- Two main audits required mathematical wording/association repairs; both
  hostile counterexamples remain regression guards.
- No commit or push was made; the work is an untracked research package in
  the AMRA working tree.

The exact theorem statuses and firewalls are frozen in `FINAL_CLAIM_LEDGER.md`;
machine results and hashes are frozen in `REGRESSION_REPORT.md`.
