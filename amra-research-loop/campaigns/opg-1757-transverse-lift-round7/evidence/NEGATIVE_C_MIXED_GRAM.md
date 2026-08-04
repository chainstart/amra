# Nested Gram certificate for four mixed negative-`c` chambers

## 1. Shared-coordinate reduction

Assume that `c` is the sole negative diagonal route quantity and use

```text
P = q0*q3*q4,
B = q0*q3*q4+q0*q3+q0*q4+q3*q4,
c = -tau*P/B,                 0<=tau<=1.
```

Take `LLR` as representative.  Its bounded page charts are

```text
x01=-s0,  x02=(q0+s0)/(1-s0),
x13=-t3,  x23=(q3+t3)/(1-t3),
x24=-t4,  x14=(q4+t4)/(1-t4),

q0,q3,q4>0,                  0<=s0,t3,t4<1.
```

Write the 178-term boundary determinant as a quadratic in `x01`:

```text
Delta_b=A2*x01^2+A1*x01+A0.
```

The exact shared-page identity is

```text
A1^2-4*A2*A0=-4*c^2*x02^2*x13^2*x14^2*H,       (1.1)
```

where `H` has 215 terms.  The verifier reconstructs both graph
polynomials and derives (1.1), so neither the coefficients nor the
factorization are imported as assumptions.

## 2. Exact denominator ledger and the leading coefficient

For `A2`, the rational-side activity degrees in page order `(0,3,4)` are
exactly `(2,2,2)`.  After clearing these page denominators and the positive
Schur denominator, all 1463 nonzero tensor Bernstein coefficients in
`(s0,t3,t4,tau)` are strictly positive; the minimum is `1/18`.  Thus
`A2>0` throughout the strict chart.

For `H`, the exact page degrees are `(2,3,2)`: the page-3 rational activity
`x23` occurs cubically.  The verifier derives the three degrees from `H`,
checks the declared ledger term by term, and rejects any insufficient
clearing degree.

## 3. A quadratic Gram certificate in `t3`

The correctly cleared Schur numerator of `H` has the exact factorization

```text
raw_H=(1-t3)*H_tilde.
```

The quotient is quadratic in `t3`.  Write it in Bernstein form as

```text
H_tilde=(1-t3)^2*gamma0
       +2*t3*(1-t3)*gamma1
       +t3^2*gamma2.                              (3.1)
```

Exact tensor Bernstein transforms in `(s0,t4,tau)` give

```text
gamma0: 489 nonzero coefficients, minimum 1/12,
gamma2: 888 nonzero coefficients, minimum 1/12.
```

The sign of `gamma1` is not assumed.  Instead form

```text
G=gamma0*gamma2-gamma1^2.
```

Its common monomial in verifier slot order is

```text
(0,0,0,3,0,2,2,0)=q3^3*q4^2*t4^2.
```

After exact removal of this nonnegative factor, all 5730 nonzero tensor
Bernstein coefficients of the 9987-term determinant are strictly positive;
the minimum is `1/270`.  Therefore the `2 x 2` matrix with diagonal entries
`gamma0,gamma2` and off-diagonal entry `gamma1` is positive semidefinite.
Equation (3.1) proves `H_tilde>=0`, hence `H>=0`.  Equation (1.1) now has
nonpositive discriminant and positive leading coefficient, proving
`Delta_b>=0` throughout `LLR`.

## 4. Symmetry images, reproduction, and scope

The exact cleared `Delta_b` polynomials verify the transports

```text
LLR --page exchange--> LRL,
LLR --hub exchange---> RRL,
LLR --both-----------> RLR.
```

Thus the same theorem closes all four chambers

```text
LLR, LRL, RRL, RLR.
```

Reproduce the certificate using only the Python standard library:

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 180s python3 evidence/verify_negative_c_mixed_gram.py
```

The output must match `negative_c_mixed_gram.json` exactly.  Together with
the direct, nonshared, and all-negative Gram certificates, this raises the
certified interior negative-`c` coverage from sixteen to twenty of the 27
activity chambers.  The seven chambers

```text
PPP, PLL, PRR, LLP, LPL, RRP, RPR
```

remain open, as do the three negative-page cases, generic contact
classification, the global marked-host theorem, and OPG-1757.  The campaign
therefore remains in `survivor_deepening`.
