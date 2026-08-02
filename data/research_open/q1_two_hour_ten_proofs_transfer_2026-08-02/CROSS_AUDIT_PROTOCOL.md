# Cross-audit protocol

Scheduled window: 2026-08-02 21:25--21:50 HKT.

No author-written test counts as an independent audit.  Each auditor must
reconstruct the central identity from the theorem statement, try the first
boundary cases and reversed inequalities, inspect the quantifier firewall,
and run or write a check which does not call the author's certificate logic.

## Assignments

| Auditor | Target | Mandatory hostile checks |
|---|---|---|
| OPG-1757 author | Erdős #1083 | integrality/nonnegativity of factorial energy; correlation sign and ordered-pair factor; finite-quotient support collisions; Fourier normalization; edit-distance quantifier; full-transverse `delta=1` model |
| Erdős #1083 author | Erdős #809 | both parity factorizations; conversion from minimum-degree deficit to vertex deficit; parity of `a`; admissible range of `h`; near-band constants; repeated-colour `C_7` path pairing; reserve cardinality and firewall |
| Erdős #776 author | OPG-1757 | exact top-height extraction; exponential-generating substitution; page transition has exactly two positive scales; uniformity of all `o(1)` terms for `k=O(log s)`; four-certificate pigeonhole; no integer splice gap |
| Root | Erdős #776 | Macaulay canonical conventions; tax cancellation; two exact normal forms; domains and direction of multi-cap transport; second-layer comparator; finite-box filters/counts; bridge-versus-public firewall |

## Verdict vocabulary

- `PASS`: statement and quantifiers survive reconstruction.
- `PASS_AFTER_REPAIR`: theorem survives but exposition, implementation, or
  a noncentral guard needed a concrete repair.
- `NARROW`: hypotheses or conclusion must be weakened.
- `FAIL`: a claimed theorem has a counterexample or invalid inference.

Every verdict must identify the public-problem status independently of the
stage theorem.
