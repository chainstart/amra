# Independent audit: moderate-rich aggregation ledger barrier

Date: 2026-07-30

Audited file:

- `MODERATE_RICH_AGGREGATION_BARRIER.md`

## Verdict

\[
\boxed{\mathrm{PASS}}
\]

The proposed exponent point is feasible for every
\(1/5\le\kappa<1/3\):
\[
a=1-\kappa,\qquad
b=\frac{7+11\kappa}{2},\qquad
m=\frac{5-15\kappa}{2}.
\]
Direct substitution gives
\[
b+m=6-2\kappa,\qquad
a+b+m=7-3\kappa,
\]
so total triple weight and hub incidence mass are both saturated.
Moreover,
\[
a+b=\frac92+\frac{9\kappa}{2}
=\frac{18}{11}+\frac{9b}{11},
\]
which is exact equality in the unweighted \(6/11,9/11\)
point--circle exponent.  Adding \(m\), or equivalently substituting
it into the weighted dyadic form, gives \(7-3\kappa\) again.

On the stated interval, \(0<m\le1\), so the fixed-plane cap
\(\mu\le M\) is respected.  The per-plane slot exponent is
\[
b+m-1=5-2\kappa,
\]
exactly \(QL\).  The model richness is \(a=1-\kappa<1\), well below
the \(9/4+\eta\) cutoff, and a nonaligned equal-richness pair only
forces exponent
\[
\frac{4a}{3}=\frac{4(1-\kappa)}3<3,
\]
so the pairwise two-circle theorem does not contradict the critical
distance budget.

For rational exponents, a cyclic biregular circle--plane ledger
realizes the degree and slot counts after taking a suitable perfect
power of \(t\); rounding gives the same exponent data for arbitrary
fixed \(\kappa\).  This validates the ledger obstruction.

The construction is deliberately abstract.  It does not assert that
an actual Euclidean reverse-circle family attains every equality.
Its conclusion is only that the currently recorded aggregate
inequalities cannot, by themselves, close the surviving hub branch.

Reproduction:

```bash
python3 verify_moderate_rich_aggregation_barrier.py
pytest -q test_verify_moderate_rich_aggregation_barrier.py
```
