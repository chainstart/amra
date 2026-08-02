# Blind cross-audit freeze

Date: 2026-08-02

Audit window: 15:35--16:15 HKT

Status: **ALL FOUR AUDITS PASSED; ALL FOUR PUBLIC PROBLEMS REMAIN OPEN**

This file is the admission decision for the concentrated-proof results.
Every admitted statement was reconstructed by an author who did not write
the source theorem, was checked by a separately written executable guard
where computation is relevant, and retains an explicit firewall to the
public problem.  A repair below changes a boundary or proof exposition; it
does not enlarge the theorem being admitted.

## Verdict table

| Lane | Verdict | Repair admitted by the audit | Public-problem firewall |
|---|---|---|---|
| OPG-1757 | **PASS AFTER REPAIR** | The interval `31 <= d < 241 log(s)` is explicitly only an eventual gap, for the same ineffective `s >= S` as the bulk theorem. | The transports are not proved inside that gap; the universal third-active row and arbitrary-host OPG-1757 remain open. |
| Erdős #1083 | **PASS AFTER THREE MINIMAL REPAIRS** | Restore prime `S` in the finite-shadow corollary; correct the final displayed digit of the entropy-gap decimal; identify the relevant transverse-`Phi_6` fibre row unambiguously. | Arbitrary aperiodic centres, arbitrary signed residual divisors, the common-`X` scalar-copy interface, and outer exact-block stability remain open. |
| Erdős #776 | **PASS** | None. | The dyadic family refutes a fixed rank-five bridge only.  It does not refute #776 or an adaptive-rank theorem. |
| Erdős #809 | **PASS AFTER ONE LOCAL EXPOSITORY REPAIR** | Expand the two possible endpoint pairings after deleting the repeated-colour edges from a putative `C_7`; both pairings are impossible by the stated anticompleteness geometry. | The theorem treats one maximum-witness B-opposite subbranch.  Branch A, B-same, the surviving square-root-spread region, and other BCM branches remain open. |

## Admitted strongest statements

### OPG-1757

The independently audited universal second-active coefficient theorem is
retained.  For each of the two third-active transports there is an
absolute, ineffective `S` such that, for every `s >= S`,

\[
  241\log s\le d\le2s-4
\]

implies strict positivity.  The first 31 coefficients hold throughout
their stated nonnegative-homogenization bulk ranges, and the fixed top
bands hold in their stated stable ranges.  Therefore, for `s >= S`, the
only unproved transport interval is

\[
  31\le d<241\log s.
\]

The audit independently reconstructed all four dominant-kernel
decompositions, shift legality, rational logarithmic margins, and both
splices.  It also reproduced the negative fixed-depth layer coefficient
in the analyzed odd `u_2`-layer architecture, which refutes that particular
termwise-positive tail architecture rather than other fixed-depth
recurrences or either transport.

### Erdős #1083

For `1 <= C < S`, the same-line cyclotomic signed-positive-multiple model
has at most

\[
  1+2\sum_{r=2}^{C}\varphi(r)\le C^2
\]

admissible scales.  At the frozen endpoint `C=t^(1/18+o(1))`, the last
quantity is `t^(1/9+o(1))`.  Finite-quotient centres admit exact-mass nonnegative
shadows, while a three-term aperiodic centre escapes every finite quotient.
Full independent transverse `Phi_6` cubes force mass at least `2^k` under
a nonnegative quotient projection.  In the stronger transverse binary-box
submodel, at the calibrated endpoint
`k=14 ell`, `C=2^ell`, `S=2^(14 ell)`, `t=2^(18 ell)`, Hamming control gives
exponent

\[
  0.460189938897\ldots<5/9,
\]

and the uniform `X -> 3X` switch forces `C >= S`.  The audit explicitly
rechecked the `C=0` vacuity firewall and did not transfer these model
barriers across the four open global interfaces.

### Erdős #776

Five one-promotion rank-five chambers have uniform positive deficit
theorems.  In the sixth chamber, on the actual dyadic lattice,

\[
 K=6,\quad r=10,\quad h=224\,2^s,\quad
 q=(448\,2^s-2)/5,\quad s\equiv2\pmod4,
\]

and every admissible `s >= 14` has

\[
  \gamma_5=4{,}302{,}695-6q<0.
\]

Every member recovers at rank six, with the stable formula

\[
  \gamma_6=9{,}256{,}181{,}220{,}279+104q>0.
\]

The independent audit rebuilt the congruence, Macaulay expansions,
promotion, caps, all four deficits, the nonstable `s=14` rank-six case,
and the stable tails.  This is a rigorous counterexample to the proposed
fixed-rank bridge, not to the public conjecture.

### Erdős #809

If a maximum-degree witness has a B-opposite pair satisfying the pure
opposite-neighbourhood hypotheses, and `g=Delta-delta`, then

\[
 n\le
 \begin{cases}
  2g^2-2g-6,& n\text{ even},\\
  2g^2-2g-3,& n\text{ odd}.
 \end{cases}
\]

The proof uses only pairwise missing-edge accounting, a fourth disjoint
maximum-degree-deficit charge, and concavity in the centre degree.  Cyclic
two-clique graphs attain both constants; for `g >= 5` they satisfy
`L_4(2)`.  They also admit the audited repeated-colour stress test with
zero-shore multiplicity and `D_B` both exactly `g`, while the available
missing-star reserve is at least `g`.  Hence these examples are
reserve-paid and are not counterexamples to the hard branch.

## Independent evidence

- OPG: 37,550,762 retained-shift rows, 133,705 high-endpoint rows, and
  7,985 exact splice rows; the independent test passed.  The full author
  lane passed 24 tests.
- #1083: 48 cyclotomic identities, 39,308 CRT states, 511 torsion orders,
  8,190 binary words, all rank-two masks, and the `X -> 3X` guard passed.
  The independent wrapper passed 2 tests; the five affected author modules
  passed 22 tests.
- #776: the independent verifier and its 3 tests passed; the complete
  post-audit lane passed 28 tests.
- #809: the independent verifier checked 16,932 fourth-charge graphs,
  1,130,499 parity-sign rows, 28,794 root rows, 18 sharp graphs, 18 exact
  repeated-class `C_7` searches, 85 reserve profiles, and all 1,227
  `L_4(2)` endpoint pairs.  The combined old and new suite passed 19 tests.

The final all-campaign regression is intentionally deferred to the
16:15--16:35 freeze window.  Its result belongs in `FINAL_REPORT.md`, not
in this pre-freeze admission record.

## Frozen audit sources

- `opg1757/THIRD_ACTIVE_TRANSPORT_LOG_BOUNDARY_BLIND_AUDIT.md`
  (`sha256 71fef43e049853c6a956232eb0d7506bac8a5da285f50423e5bab8b6168b64ef`)
- `erdos1083/SIGNED_SWITCH_BLIND_AUDIT_II.md`
  (`sha256 10bdeddb625c91e0206fd98b6d7c85dfc6393e21a480fdfd0510f3d3225b71e9`)
- `erdos776/FINAL_CHAMBER_COUNTERFAMILY_BLIND_AUDIT.md`
  (`sha256 388a61b6cd588161336a03e63241b6bab83d924d926f43296270d759cadda4dd`)
- `erdos809/MAXIMUM_WITNESS_SQRT_SPREAD_BLIND_AUDIT.md`
  (`sha256 8edb5b011a498ae6ed37e1d496b2d5241afb1467163b16d2ed149aeef5a1ddf3`)
