# Erdős #1083 author freeze

Freeze prepared: 2026-08-02 20:59 HKT  
Required checkpoint: 21:20 HKT  
Status: **AUTHOR-FROZEN / NOT BLIND-AUDITED / NOT ADMITTED TO A ROOT FINAL CLAIM LEDGER**

## Frozen claims

1. The factorial-energy, edit-stability, autocorrelation, prime-shadow,
   reciprocal-frame, popular-difference, minimum-debt-cover, and stable-collision
   statements in `SIGNED_RESIDUAL_FACTORIAL_ENERGY.md` are claimed proved under
   their displayed quantifiers.
2. The irreducibility, non-torsion unit roots, off-circle roots, small-divisor
   estimates, exact signed quotient, exact factorization, and co-vanishing
   statements in `APERIODIC_SMALL_DIVISOR_NO_GO.md` are claimed proved under
   their displayed quantifiers.
3. Erdős #1083, the power-large reciprocal-frame upper bound, cross-row
   synchronization of cancellation alphabets, and the outer Euclidean extraction
   remain explicitly open.

## Quantifier checks completed

- Lemma 1.2 assumes an infinite ambient group; the trivial group under the full
  product hypotheses is handled separately.
- The prime \(p>S\) is chosen support-injective simultaneously for all
  \(A_j,q_j,M,N_j\).  The group-ring homomorphism preserves convolution; support
  injectivity preserves coefficients, masks, augmentations, and \(\ell^2\) norms.
- The popular-difference theorem assumes \(S\ge2\), signed integral finite-support
  \(q\) with \(q(1)=C>0\), and only coefficientwise nonnegativity of \(P_Aq\);
  output collisions are allowed.
- The minimum-debt cancellation alphabet is shared only between the centre and
  one leaf for a fixed \(q_j\); it may vary across rows.
- The aperiodic signed escape is one row.  It supplies neither a second scalar
  copy nor a power-large common-mask family.

## Exact signed factorization

\[
\begin{aligned}
P&=1+x+x^3+x^5+x^6,\\
Q&=1-x^5+x^8+x^{10}-x^{13}+x^{18}\\
 &= (1+x^8)(1-x+x^2)
 (x^8+x^7-x^5-x^4-x^3+x+1),\\
PQ&=1+x+x^3+x^9+x^{11}+x^{13}+x^{15}+x^{21}+x^{23}+x^{24}.
\end{aligned}
\]

The factor augmentations are \((2,1,1)\), \(Q(1)=2<5\), and
\(\delta(Q)=2\).

## Verification output

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  test_signed_residual_factorial_energy.py \
  test_aperiodic_small_divisor_nogo.py
```

Output summary:

```text
Ran 12 tests in 0.132s
OK
```

Both standalone verifiers also returned `pass: true`.  Their scope fields retain
`original_problem_proved: false`; the factorial verifier additionally retains
`outer_geometric_extraction_proved: false`, and the aperiodic verifier retains
`power_large_family_constructed: false`.

No `__pycache__` or `.pytest_cache` directory remained at freeze.

## Frozen hashes

```text
31e5b8d7e1eca94e14ee5a8fd283074ae5f64fbc660bc699bfbfbbdb3de5c5a5  METHOD_TRANSFER_PLAYBOOK.md
5fdf6c324a8604a252e7019354587c8d4354f72a4b9ec52014d8e2796f1d2838  SIGNED_RESIDUAL_FACTORIAL_ENERGY.md
1b2f8abcaac34f3922e7b0b2a9f308e8a6c03972c01407707ce6067791065892  APERIODIC_SMALL_DIVISOR_NO_GO.md
e8ceff649929ea0ab1477589ec6f94e3adf9a740128a18c20698bd94b13110d6  verify_signed_residual_factorial_energy.py
763b2f3a87fd08669f0345bde32f096e49966fecf23a04081cc06341ca142948  verify_aperiodic_small_divisor_nogo.py
```

