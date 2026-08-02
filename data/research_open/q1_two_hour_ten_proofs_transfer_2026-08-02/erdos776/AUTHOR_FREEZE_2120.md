# Author freeze for the 21:25 independent audit

Frozen: 2026-08-02 21:10 HKT.

No author-side edits should be made to the files hashed below after this
freeze.  Audit findings should be recorded separately.

## Frozen new result: Proposition 5.3

For every admissible no-borrow sequence with fixed promotion count
\(c=2\) and \(q\to\infty\),

\[
 \liminf \frac{\gamma_4}{q^3}\ge0.
\]

If every member of an unbounded such sequence has \(\gamma_4\le0\), then

\[
 \frac rq\to1,\qquad \frac uq\to0.
\]

The proof fixes a convergent subsequence of the normalized tails
\(2\alpha/q^2\to P\), \(2\beta/q^2\to S\) and the integer cap gap
\(g=t-a\).  With \(D=2+U^2-R^2\), the exact displacement and comparator
give

\[
 g+S-P=D,
 \qquad
 \frac{\gamma_4}{q^3}\to
 \frac{g-1+S^{3/2}-P^{3/2}}6.
\]

Writing \(f(x)=x-x^{3/2}\), the limiting numerator is
\(D-1+f(P)-f(S)\).  It is strictly positive for \(D>1\): for
\(D\ge2\), use \(0\le f\le4/27\); for \(1<D<2\), the only integer phases
are \(g=1,2\), and monotonicity of \(x^{3/2}\) gives positivity directly.
Zero can occur only when \(D=1\), which forces \((R,U)=(1,0)\).

### Firewall

- Proposition 5.3 is an asymptotic localization, not positivity at the
  boundary \(r/q\to1,u/q\to0\).
- Theorem 5.1 closes only the explicitly stated shallow two-cap phase on
  that boundary; it is not a global \(c=2\) classification.
- Theorem 5.2 has quantifiers
  \(\forall c\ge3\;\exists Q_c\;\forall q\ge Q_c\); it gives no threshold
  uniform in \(c\) and does not control growing \(c=c(q)\).
- The 85,278-state atlas is an exact finite falsifier, not an unbounded
  proof.
- The earlier bridge counterexample is not a counterexample to Erdős #776.

## Frozen verification output

Command:

```bash
pytest -q data/research_open/q1_two_hour_ten_proofs_transfer_2026-08-02/erdos776
```

Output:

```text
..                                                                       [100%]
2 passed in 1.73s
```

The standalone verifier also completed with these headline values:

```text
finite atlas checked states           85278
gamma4 nonpositive states             0
minimum gamma4                        69
second-level bound positive           85276
second-level residual count           2
shallow two-cap q<90 base             20
shallow two-cap base minimum gamma4   186
```

## Frozen SHA-256 hashes

```text
f13e7a224ddd2e523331ea6fd61dd03da880a2d5a05b0e85e2828d2f35184af6  TEN_PROOFS_METHOD_TRANSFER.md
a75fda9f09cd9b31bf4146274b4a1f0ce69456c56abf8b13687a79e8e2aa2c86  MULTI_PROMOTION_NO_BORROW_ATLAS.md
ddc8ff6805c91abfcb11f6787629d849d8cb3c249f68ecf5d44e81c6a2ea4719  CLAIM_LEDGER.md
0cc2a3a26bf43a3d5b77d753b36b45052db37459c2f6e59b4fbe7e7d1ab1e367  verify_multi_promotion_no_borrow.py
f725e3f1a7172f2566eae867bb786e8afbc6c38710cd0269b10666825fd7ed62  test_verify_multi_promotion_no_borrow.py
```
