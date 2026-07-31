# Three-hour Q1 theorem campaign

Date: 2026-07-31

## Clock contract

- The user reset the clock to a new full interval at
  2026-07-31 17:05:46 HKT.
- Hard midpoint: 2026-07-31 18:35:46 HKT.
- Earliest permitted close: 2026-07-31 20:05:46 HKT.
- This is a literal wall-clock contract. Parallel agent time does not permit
  early completion.
- Work continues through the full interval even if a promising lemma appears
  early; remaining time is then spent on independent proof audit, falsification,
  priority checking, and manuscript-level closure.

## Primary targets

1. **Erdős #809:** prove the Case-1 linkage-defect estimate
   \[
   \sum_\gamma (|M_\gamma|-1)_+=o(n^2),
   \]
   or find the precise obstruction and the strongest correct replacement.
2. **Erdős #776:** prove the all-parameter rank-16 residual gate, preferably
   through the sharp complementary gap \(G_2(V)\ge V+1\), or isolate a strictly
   smaller noncircular lemma.
3. **OPG-1757:** replace fixed-rank positivity by an all-depth pooled-kernel,
   tail-sign, or finite-reduction theorem for the complete-split family.

Erdős #1083 remains frozen unless one of the three primary routes is
mathematically terminated before the midpoint. Its previous structural
theorems are not a reason to spend more time on local endpoint counting.

## Final outcome of the renewed interval

- **OPG-1757 complete-split model:** the fixed-deficit layers \(q=3,4,5,6\)
  are now proved coefficientwise positive in their stated ranges.  The new
  all-\(q\) endpoint top-two theorem gives
  \(\deg R_{q,r}\le2q+r\), and the all-\(q\) boundary-factor theorem gives
  \(\prod_{j=4}^{\lfloor(q+6)/2\rfloor}(s-j)\mid R_{q,r}\).  These do not
  solve arbitrary-host OPG-1757 or arbitrary-\(q\) positivity.
- **Erdős #776:** a quotient--remainder Macaulay certificate pushes the
  entry range to 233 and proves the closing reduction
  \(D_{248}<H_{248}\Rightarrow D_{18}<P_{18}\).  The premise is still open;
  finite scans are recorded only as falsification evidence.
- **Erdős #809:** an exact opposite-pair core theorem and weighted
  degree-support criterion are proved.  A full-contract graph family refutes
  the tempting implication from absorption-certificate failure to a small
  residual moment, but its exact defect budget closes, so it is not a
  counterexample to #809.

See `FINAL_REPORT.md` for the audited handoff and `CLAIM_LEDGER.md` for the
public claim boundary.

## Acceptance hierarchy

1. A proved unbounded headline theorem with every public quantifier closed.
2. A proved unbounded theorem that closes a major named-problem branch.
3. A proved structural theorem plus an exact one-lemma reduction.
4. A rigorous no-go theorem or counterexample family that kills a tempting
   route.
5. Finite exact evidence, clearly labelled as falsification/regression only.

No finite scan, interpolation without a degree theorem, asymptotic heuristic,
or conditional equivalence may be reported as a proof of a named problem.

## Parallel ownership

- `erdos809/`: linkage certificates, congestion charging, and Case-1 closure.
- `erdos776/`: residual gaps, Macaulay/colex carries, and all-\(V\) gates.
- `opg1757/`: pooled inversion and infinite-depth positivity mechanisms.
- Root files: clock, cross-audit, unified claim ledger, and final triage.
