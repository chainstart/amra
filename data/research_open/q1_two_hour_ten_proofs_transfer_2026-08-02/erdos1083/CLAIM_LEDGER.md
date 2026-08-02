# Claim ledger

Date: 2026-08-02

| Claim | Status | Boundary / evidence |
|---|---|---|
| Erdős #1083 is proved or disproved | **OPEN / NOT CLAIMED** | No global distance exponent improvement and no few-distance counterexample is produced. |
| Ten-proofs methods were extracted from the requested paper, walkthroughs, and five Lean files | **DONE** | `METHOD_TRANSFER_PLAYBOOK.md`; Lean snapshot `94bc0fe`. |
| Factorial energy is a nonnegative integral signed-residual potential | **PROVED / INDEPENDENT CROSS-AUDIT PASSED AFTER QUANTIFIER REPAIR** | Lemma 1.1; the global product interface now states \(S\ge1\). |
| A residual lies within \(2\delta(q)\) in \(\ell^1\) of a \(C\)-term mask | **PROVED, WITH INFINITE-GROUP QUANTIFIER / AUDITED** | Lemma 1.2; under \(S\ge1\), the only trivial-group product case is \(S=C=1,q=1\). |
| A mask product has autocorrelation debt \(-2S\delta(q)\) | **PROVED** | Theorem 2.1, exact norm expansion. |
| A signed residual with any nonnegative product forces a difference of multiplicity at least \(S/(C+N_-)\) | **PROVED** | Theorem 2.2; output collisions are allowed. |
| A Sidon source forces \(\delta(q)\ge S-C\) | **PROVED AS COROLLARY** | Set \(\mu(X)=1\) in Theorem 2.2. |
| The collision ledger persists for non-mask outputs with factorial-defect error | **PROVED** | Theorem 2.3.  No Euclidean cleaning theorem supplying a small defect is claimed. |
| Every \(S\)-term mask is Fourier-invertible on \(\Gamma/p\Gamma\) for a sufficiently large prime \(p>S\) | **PROVED** | Lemma 3.1; support-injective choice of \(p\) is explicit. |
| Aperiodicity supplies a uniform lower Fourier bound on torsion characters | **REFUTED** | \(1+x+x^3+x^5+x^6\) is irreducible, has no torsion zero, has non-torsion unit-circle zeros, satisfies \(0<\sigma_n\le15\pi/n\), and even \(\sigma_n\le30\pi/n^2\) infinitely often. |
| The ill-conditioned five-term centre has an actual signed positive quotient | **PROVED / CONSTRUCTED** | Explicit augmentation-two quotient gives a ten-term mask and has \(\delta=2\).  It is one row, not a power-large family. |
| The fixed escape mask \(M\) contains a second nonassociate five-term mask divisor | **REFUTED FOR THIS FIXED \(M\) / INDEPENDENT ADDENDUM AUDIT PASSED** | Four augmentation-five normalized divisors, exactly one mask divisor \(P\); this is not an all-common-mask theorem. |
| Primitive rational scalar pairs through 100 are coprime and hence augmentation-obstructed for \(1\le C<5\) | **EXACT FINITE PRECURSOR / SUPERSEDED BY THE NEXT ROW** | 3,043 pairs in the scratch guard; the independent auditor separately checked all 127 pairs through 20.  These computations guard examples only; the next row supplies the unbounded proof. |
| For the fixed mask \(P=1+x+x^3+x^5+x^6\), scalar substitutions of distinct absolute scale are coprime; hence no integral common complement of augmentation \(5C\), \(1\le C<5\), supports both rows | **PROVED / INDEPENDENTLY PROMOTED — FIXED SOURCE ONLY** | `SECOND_SCALAR_FINAL_SCRATCH.md`; the unbounded step is the \(S_3\)/independent-square-class pair-flip proof followed by the Laurent-UFD augmentation obstruction, not finite extrapolation. `verify_second_scalar_global_structure.py` guards the structural identities and 1,101 additional gcd rows. Independent promotion is recorded in `CROSS_AUDIT_BY_OPG1757.md` at SHA `4b4038d68ab02b418797eb6f1ad497822f02809e72ca08eae904271baf3dcda8`. This classifies only the displayed fixed \(P\); Erdős #1083 remains **OPEN**. |
| A small denominator forces a large actual residual ratio in that escape | **FALSE** | Exact co-vanishing gives \(|M|^2/|P|^2=|Q|^2\le36\), with prime-shadow average exactly \(6\). |
| The common-mask reciprocal-frame excess equals \(2\sum_j\delta(q_j)\) | **PROVED** | Theorem 3.2 and Parseval. |
| Full geometric transversality forces a positive rowwise debt gap beyond \(\delta\ge1\) | **FALSE** | Existing Euclidean \(Q_S\) switch has \(\delta(Q_S)=1\) for every \(S\ge4\). |
| The reciprocal-frame excess is \(o(K)\) in the exact block | **OPEN / NOT CLAIMED** | This is the new sharp simultaneous algebraic target. |
| Outer near-extremal geometry yields small factorial output defect | **OPEN / NOT CLAIMED** | Theorem 2.3 only identifies the required error quantity. |
| Verification suites | **FINITE / 12 OF 12 AUTHOR TESTS PASS; INDEPENDENT CROSS-AUDIT PASS_AFTER_REPAIR** | Two local quantifier repairs were made: \(S\ge1\) globally and “signed” before the \(\delta=1\) normal form. |
