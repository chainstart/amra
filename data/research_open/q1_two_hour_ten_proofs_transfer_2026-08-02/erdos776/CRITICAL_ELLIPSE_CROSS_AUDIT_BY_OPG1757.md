# Independent audit of the critical-ellipse final scratch

Auditor: OPG-1757 lane  
Date: 2026-08-02  
Decision: **PROMOTE** as a fixed-`c=2` eventual theorem for the relaxed
no-borrow bridge.  
Public status: **Erdős #776 remains OPEN**.

## Exact reconstruction

I did not import either #776 verifier.  The independent script
`critical_ellipse_cross_audit_by_opg1757.py` reconstructs the rank-two
canonical words from the definition.

For `A_q(s)=sq-binomial(s+1,2)`, least-depth minimality gives exactly
`0<=rho<q-s`; hence the complement words in (1.4), including their strict
upper remainder bounds, are legal.  Substitution reproduces (1.6)--(1.8).
Since `R_E(h)>R_D(h)` at every positive trial correction, the first legal
correction for `E` is no later than that for `D`, so

```text
m=s_D-s_E=k+1+h_D-h_E>=k+1>=2.
```

For `m>=3`, the worst possible negative remainder is
`-binomial(v_D-1,2)`.  Therefore the exact cap gain is at least

```text
binomial(v_D+3,3)-binomial(v_D,3)-binomial(v_D-1,2)
=v_D(v_D+3).
```

Because `v_D/q->1`, subtracting `binomial(q-k,2)+1` leaves normalized
liminf `1/2`.  A nonpositive sequence must thus have `m=2`, which forces
exactly `k=1` and `h_D=h_E`.

## Equal-correction phases

For `k=1`, equality of the two minimal corrections is equivalent to
`R_D(h)>=0` and `R_E(h-1)<0`: the strict inequality (1.8) supplies the two
omitted companion inequalities.  Combining these conditions gives the
necessary bound (3.4).  If `h>=3`, division by `hq` leaves a left side at
least `2/3`, while every right-side term tends to zero because
`h<=s_D=o(q)` and `u=o(q)`.  Thus only `h=1,2` can occur eventually.

Independent symbolic expansion reproduces both exact surplus polynomials
(4.2) and (4.5).  In phase one, `x=u^2/q` lies in `[0,1]` and the limit

```text
1/2+x/2-3x^2/8
```

is at least `1/2`.  In phase two, the two cap inequalities force
`u^2/q->2`, and the normalized surplus tends to one.  Both phases therefore
contradict a nonpositive countersequence.

## Quantifiers and executable guard

Negating the proposed threshold produces a sequence `q->infinity` of bad
admissible fixed-`c=2` points.  The already audited localization and boundary
handoff apply to that sequence, and the exhaustive integer alternatives
above give the contradiction.  This proves

```text
exists Q_2, for all q>=Q_2, every admissible fixed-c=2 no-borrow point
has gamma_4>0.
```

It is not uniform for growing `c`, does not prove phase exhaustiveness for
the adaptive bridge, and has no direct public-problem consequence.

The independent executable guard checked the symbolic identities and 36,892
direct canonical rows:

```text
ERDOS776 CRITICAL-ELLIPSE INDEPENDENT AUDIT: PROMOTE
exact_rows: 36892
m_ge_3_rows: 35674
rigid_m_2_rows: 1218
fixed_c2_eventual_only: True
growing_c_open: True
original_problem_proved: False
```

Verdict: **PROMOTE**, with the scope above and no weakening or mathematical
repair required.
