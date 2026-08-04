# Double Gram certificate when a nonshared page is positive

## 1. Representative and shared discriminant

Assume that `c` is the sole negative diagonal route quantity and set

```text
P=q0*q3*q4,
B=q0*q3*q4+q0*q3+q0*q4+q3*q4,
c=-tau*P/B,                    0<=tau<=1.
```

Use `LLP` as representative, with charts

```text
x01=-s0,  x02=(q0+s0)/(1-s0),
x13=-t3,  x23=(q3+t3)/(1-t3),
x14=q4*s4, x24=q4*(1-s4)/(1+q4*s4),

q0,q3,q4>0,                  0<=s0,t3<1, 0<=s4<=1.
```

As before, write

```text
Delta_b=A2*x01^2+A1*x01+A0
```

and reconstruct the exact identity

```text
A1^2-4*A2*A0=-4*c^2*x02^2*x13^2*x14^2*H.       (1.1)
```

It is enough to prove both `A2>=0` and `H>=0`.  In this chamber they admit
parallel Gram certificates in the same page orientation.

## 2. The `A2` Gram certificate

The exact rational-side denominator degrees for `A2`, in page order
`(0,3,4)`, are `(2,2,2)`.  After the page and Schur substitutions, its
cleared numerator has an exact factor `(1-t3)`.  The quotient is quadratic:

```text
A2_tilde=(1-t3)^2*alpha0
         +2*t3*(1-t3)*alpha1
         +t3^2*alpha2.                           (2.1)
```

Tensor Bernstein transforms in `(s0,s4,tau)` give

```text
alpha0:  529 nonzero coefficients, minimum 1/6,
alpha2: 1018 nonzero coefficients, minimum 1/6.
```

The determinant `alpha0*alpha2-alpha1^2` has common monomial

```text
(0,0,0,3,0,4,0,0)=q3^3*q4^4.
```

After removing it exactly, all 13655 nonzero tensor Bernstein coefficients
of the 6628-term determinant are strictly positive, with minimum `1/540`.
Thus the matrix in (2.1) is positive semidefinite and `A2>=0`.

## 3. The `H` Gram certificate

The reconstructed rational-side degrees for `H` are `(2,3,3)`.  The two
degree-three entries are essential: `H` is cubic in both `x23` and `x24`.
Its correctly cleared numerator again factors as

```text
raw_H=(1-t3)*H_tilde,

H_tilde=(1-t3)^2*gamma0
        +2*t3*(1-t3)*gamma1
        +t3^2*gamma2.                             (3.1)
```

The endpoint ledgers in `(s0,s4,tau)` are

```text
gamma0:  894 nonzero coefficients, minimum 1/6,
gamma2: 1887 nonzero coefficients, minimum 1/6.
```

The determinant has 14235 terms and common monomial

```text
(0,0,0,3,0,5,0,0)=q3^3*q4^5.
```

Every one of the 14489 nonzero tensor Bernstein coefficients of its exact
residual is strictly positive; the minimum is `1/90`.  Therefore (3.1)
proves `H>=0`.  Combining this with (2.1) and (1.1) proves
`Delta_b>=0` in `LLP`.

## 4. Symmetries, reproduction, and scope

The verifier checks the following transports on exact cleared `Delta_b`
polynomials in raw coordinates for the positive page:

```text
LLP --page exchange--> LPL,
LLP --hub exchange---> RRP,
LLP --both-----------> RPR.
```

Hence all four chambers are certified.  Reproduce with the Python standard
library only:

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 240s python3 evidence/verify_negative_c_positive_nonshared_gram.py
```

The output must match `negative_c_positive_nonshared_gram.json` exactly.
Together with the preceding negative-`c` certificates, this raises the
interior activity-chamber coverage from twenty to twenty-four of 27.  Only

```text
PPP, PLL, PRR
```

remain open in the sole-negative-`c` matrix chamber.  The three
negative-page cases, generic contact classification, the global marked-host
theorem, and OPG-1757 also remain open; the campaign stays in
`survivor_deepening`.
