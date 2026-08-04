# Nested Gram and square certificate for the positive shared page

## 1. Representative and the `x02` discriminant

Assume that `c` is the sole negative diagonal route quantity and write

```text
P=q0*q3*q4,
B=q0*q3*q4+q0*q3+q0*q4+q3*q4,
c=-tau*P/B,                    0<=tau<=1.
```

Use `PLL` as representative, with the uniform page charts

```text
x01=q0*s0,  x02=q0*(1-s0)/(1+q0*s0),
x13=-t3,    x23=(q3+t3)/(1-t3),
x14=-t4,    x24=(q4+t4)/(1-t4),

q0,q3,q4>0,                    0<=s0<=1, 0<=t3,t4<1.
```

The earlier certificates used the quadratic in `x01`.  Here the useful
choice is the hub-conjugate quadratic

```text
Delta_b=B2*x02^2+B1*x02+B0.
```

Fresh reconstruction from the 128 forests and 58 marked-connected forests
gives the exact identity

```text
B1^2-4*B2*B0=-4*c^2*x01^2*x23^2*x24^2*H2.      (1.1)
```

It is therefore enough to prove `B2>=0` and `H2>=0`.  Both polynomials have
exact rational-side degrees `(0,2,2)` in page order `(0,3,4)`.

## 2. Outer Gram for `B2`

After the page and Schur substitutions, the cleared `B2` numerator has 448
terms and factors exactly as

```text
raw_B2=(1-t3)*(1-t4)*B2_tilde.
```

The 144-term quotient is quadratic in `t3`:

```text
B2_tilde=(1-t3)^2*alpha0
         +2*t3*(1-t3)*alpha1
         +t3^2*alpha2.                           (2.1)
```

Tensor Bernstein transforms in `(s0,t4,tau)`, with ordinary nonnegative
monomials in `q0,q3,q4`, give

```text
alpha0:  62 nonzero coefficients, minimum 1/2,
alpha2: 135 nonzero coefficients, minimum 1/2.
```

The determinant `alpha0*alpha2-alpha1^2` has 885 terms and common monomial

```text
q0^4*s0^2*q3^3*q4^2.
```

After removing this monomial, exact sparse division gives

```text
det_outer/common
 = ((1-tau)*q0*(q3*q4+q3+q4)+q3*q4)*S.          (2.2)
```

The first factor is nonnegative throughout the closed chart and strictly
positive in its interior.  It remains to prove `S>=0`.

## 3. Inner Gram and the endpoint square

The 346-term factor `S` is quadratic in `s0`:

```text
S=(1-s0)^2*eta0
  +2*s0*(1-s0)*eta1
  +s0^2*eta2.                                    (3.1)
```

The `eta0` transform in `(t4,tau)` has 57 nonzero coefficients, all
strictly positive, with minimum `1/18`.  The other endpoint `eta2` has 481
nonzero coefficients, only three of which are negative.  Those three terms
are not independent obstructions: they are the three cross terms of one
exact square.  Set

```text
L = q3*t4^2*tau
    -q3*q4^2*(1-t4)^2*tau
    -q0*q3*q4*(1-t4)^2*(1-tau)
    -q0*q4^2*(1-t4)^2*(1-tau).
```

Exact subtraction gives

```text
eta2=q0*q4*tau*L^2+R.                            (3.2)
```

All 471 nonzero tensor Bernstein coefficients of `R` in `(t4,tau)` are
strictly positive, with minimum `1/18`.  Thus `eta2>=0` without interval
subdivision or a floating-point positivity claim.

Finally, `eta0*eta2-eta1^2` has 1252 terms and common monomial

```text
q3*q4*t4^2*tau^2.
```

After exact removal, all 1842 nonzero tensor Bernstein coefficients are
strictly positive, with minimum `1/45`.  Hence the matrix in (3.1) is
positive semidefinite, so `S>=0`.  Equations (2.1)--(2.2) then prove
`B2>=0` (and `B2>0` in the open activity chamber).

## 4. Gram certificate for `H2`

The correctly cleared 667-term numerator factors as

```text
raw_H2=(1-t3)^2*(1-t4)^2*H2_tilde.
```

Its 111-term quotient is again quadratic in `t3`:

```text
H2_tilde=(1-t3)^2*gamma0
         +2*t3*(1-t3)*gamma1
         +t3^2*gamma2.                            (4.1)
```

The exact endpoint ledgers in `(s0,t4,tau)` are

```text
gamma0:  22 nonzero coefficients, minimum 1/2,
gamma2: 119 nonzero coefficients, minimum 1/4.
```

The 441-term determinant has common monomial

```text
q0^4*s0^2*q3^3*q4^2*t4^2.
```

Every one of the 433 nonzero tensor Bernstein coefficients of its exact
residual is strictly positive, with minimum `1/6`.  Therefore (4.1) proves
`H2>=0`.  Together with (1.1) and `B2>=0`, this gives `Delta_b>=0` in
`PLL`; boundary points follow by continuity.

## 5. Symmetry, reproduction, and scope

Hub exchange maps `PLL` to `PRR`.  The verifier checks this on the exact
cleared `Delta_b` polynomials, in addition to checking the graph-level hub
symmetry.  Thus both chambers are certified.

Reproduce using the Python standard library only:

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 240s python3 evidence/verify_negative_c_positive_shared_gram.py
```

The output must match `negative_c_positive_shared_gram.json` exactly.
Together with the preceding negative-`c` certificates, this raises the
interior activity-chamber coverage from twenty-four to twenty-six of 27.
Only `PPP` remains open in the sole-negative-`c` matrix chamber.  The three
negative-page cases, generic contact classification, the global marked-host
theorem, and OPG-1757 also remain open; the campaign stays in
`survivor_deepening`.
