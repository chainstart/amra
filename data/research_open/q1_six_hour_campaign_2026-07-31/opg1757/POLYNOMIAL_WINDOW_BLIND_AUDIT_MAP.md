# Blind-audit map: OPG-1757 polynomial deficit window

Date: 2026-08-01
Candidate status: **PENDING INDEPENDENT CROSS-AUDIT**

## Target

For integers \(q\ge1\), \(0\le r\le2q\), prove

\[
 s\ge2(4096q)^{67}\quad\Longrightarrow\quad C_{q,r}(s)>0,
\]

and then deduce the simultaneous window

\[
 0\le q\le s^{1/67}/8192.
\]

The claim is only for the complete-split pooled disjoint-core
\(\alpha^2\) layer.  Do not infer arbitrary-host OPG-1757.

## Dependency graph

1. **Exact normalized master identity.**  Verify formula (18), the
   \(n!\) cancellation, the selected \(s\)-power, the four shifts, and
   \(m_1+m_2+\ell=q+1\) in
   `UNIFORM_HEIGHT_AND_GROWING_WINDOW_THEOREM.md`.
2. **Endpoint inputs.**  Verify the exact endpoint height (16) in the
   same file and the all-order statement
   \(\deg q_{h,k}(e,\rho)\le2k\) in the inherited
   `../../q1_breakthrough_campaign_2026-07-31/opg1757/LAURENT_DEGREE_LEMMA.md`.
3. **Pointwise endpoint loss.**  Independently reconstruct triangular
   Newton interpolation, equations (7)--(11), in
   `POLYNOMIAL_GROWING_DEFICIT_WINDOW.md`.  Confirm it bounds values at
   actual profiles, not merely monomial coefficients.
4. **Four-factor loss.**  Check the exact shifts
   \(m_1+2,m_2+2,m_1+1,m_2+3\), natural-support bound \(\ell\le q\),
   falling estimate (13), and convolution envelope (14).
5. **Absolute profile mass.**  Starting from the five-tuple sum (16a),
   independently derive
   \[
   S_{q,r}=\frac8{(q+1)!}[z^r](1+2z+2z^2)^{q+1}
   \]
   and compare it with
   \(L_{q,r}=4[z^r](1+2z+2z^2)^q/q!\).  Check \(r=0\) and \(r=2q\).
6. **Loss-index and root chain.**  Confirm apparent degree \(2q+2\),
   cancellation of its top two orders, hence \(K=k+2\).  Then audit
   equations (24)--(26) and the window implication.  A line-by-line
   endpoint audit is isolated in `QUANTIFIER_CHAIN_SELF_AUDIT.md`.

## Three independent reconstruction gates

The candidate should not be upgraded unless the auditor independently
obtains all three:

- the normalized all-\(k\) endpoint interface with the same \(Q_{h,e,c}\);
- the exact factor \(8/(q+1)!\) in the absolute profile EGF;
- the shift \(K=k+2\) and the exponent budget \(60+6+1=67\).

## Executable falsification only

Run from this directory:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
  test_uniform_height_envelope.py test_polynomial_window_bounds.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_polynomial_window_bounds.py \
  --extended-endpoints
```

Expected: 9 tests; 99 profile identities; 1,001 Newton
reconstructions; 7,440 constant checks; 881,548 falling-coefficient
checks; 1,008 exact \(q=6\) endpoint losses; and 156 exact \(q=6\)
layer losses.  These are falsification aids, not substitutes for the six
proof gates above.
