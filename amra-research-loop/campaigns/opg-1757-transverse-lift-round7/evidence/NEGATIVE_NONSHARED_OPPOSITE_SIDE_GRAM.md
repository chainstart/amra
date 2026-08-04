# Four opposite-side negative-nonshared chambers

## 1. Chamber and exact chart

Assume that `q3<0` is the sole negative diagonal route quantity in

```text
K=diag(q0,q3,q4,c)+1*1^T > 0.
```

Put

```text
P=c*q0*q4,
B=c*q0*q4+c*q0+c*q4+q0*q4.
```

The Schur coordinate is `q3=-tau*P/B`, with `0<=tau<=1`.  For the `L`
chart on the negative page, the two activity numerators and positive
denominators are

```text
-(tau*P+(B-tau*P)*s3) / B,       s3/(1-s3).
```

The other two pages use the same uniform positive-route charts as the
preceding nonshared-page certificates.  In the representative word `RLR`,
the negative activities on the negative page and the other nonshared page
lie on opposite hub sides.  Direct substitution and clearing the positive
squared denominators gives

```text
cleared Delta_b = c*(1-s3)*(1-s4)*Q,
```

where `Q` has 766 terms and is quadratic in `s3` and `s4`.

## 2. Nested Gram reduction

Write `Q` in the quadratic Bernstein Gram basis for `s3`.  Its two endpoint
forms are quadratic in `s4`.  Exact second-level Gram certificates give:

| `s3` endpoint | endpoint Bernstein rows | endpoint minima | determinant Bernstein rows | minimum |
|---|---:|---:|---:|---:|
| `0` | `68, 145` | `1/6, 1/12` | `933` | `1/8` |
| `1` | `127, 299` | `1/6, 1/6` | `2397` | `1/30` |

The remaining outer Gram determinant factors exactly as

```text
c*q0^2*q4*(q0+s0)^2*B*H1971.
```

Thus only the sign of the 1,971-term core remains.  It is cubic in `tau`.
Its four exact Bernstein rows factor as

```text
beta0 = B^3*K30,
beta1 = c*B^2*(M0+c*M1)/3,
beta2 = c^2*B*J9*H23/3,
beta3 = q4*(c+q4)*c^3*J9^2.                 (2.1)
```

`K30` has 130 strictly positive tensor Bernstein coefficients in `(s0,s4)`,
with minimum `1/18`.

## 3. Exact square certificates for the exceptional rows

For compactness set

```text
a=q0,  b=q4,  x=s0,  y=s4,  U=x+y-x*y=x+y*(1-x).
```

The nine-term kernel in (2.1) is the manifestly nonnegative polynomial

```text
J9 = (a*y-b*x)^2
   + a^2*b*y^2 + a*b^2*x^2
   + 2*a*b*x^2*y + 2*a*b*x*y^2
   + (a+b)*x^2*y^2.                          (3.1)
```

The 88-term middle core splits as `M0+c*M1`.  Exact sparse subtraction gives

```text
M0/b =
    a^3*y^2*(x*b-y)^2
  + a^3*y^2*(x*y-b)^2
  + 2*a*x*b*(a*y-x*b)^2
  + 2*a*b*y^3*(a-x^2)^2
  + 2*x^2*b*(a*y-x*b)^2
  + 2*x^2*y^2*(a*y-x*b)^2
  + R23,                                      (3.2)
```

where all 23 coefficients of `R23` are positive integers.  The other part
factors as `M1=A*K`, with

```text
A = a*b*U + a*y^2 + b*x^2 + x^2*y^2,
K = 2*(a*y-b*x)^2 + a*b^2*U + R8,             (3.3)
```

and all eight coefficients of `R8` are positive integers.  Since
`0<=x,y<=1`, `U>=0`; hence (3.2)--(3.3) prove `M0,M1>=0`.

Finally split `H23=H0+c*H1`.  The verifier checks the exact identities

```text
H0 = b*(a*y-b*x)^2 + R0,
H1 = (a*y-b*x)^2
   + a*b^2*(x-y)^2
   + a*b^2*y*(2-y) + R1,                      (3.4)
```

where `R0` and `R1` each have eight strictly positive coefficients.  Since
`2-y>=1`, (3.4) proves `H23>=0`.  Every Bernstein row in (2.1) is therefore
nonnegative, the outer Gram matrix is positive semidefinite, and
`Delta_b>=0` in the representative chamber.

## 4. Symmetry closure and scope

The verifier reconstructs all four cleared polynomials.  Global hub exchange
makes `q3:LRL` literally equal to `q3:RLR`, and page-3/page-4 exchange gives
the exact parameter permutations `q4:LLR` and `q4:RRL`.  Hence this certificate
closes

```text
q3:LRL, q3:RLR, q4:LLR, q4:RRL.
```

Together with the preceding certificates, 63 of the 81 negative-page
activity chambers are now exact; 18 remain open.

Reproduce the certificate with

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 240s python3 evidence/verify_negative_nonshared_opposite_side_gram.py
```

The verifier uses only Python's standard library, rebuilds the original 128
deletion forests and 58 marked-connection forests, checks every factor and
square identity over exact rationals, and hashes all decisive polynomials.
This result does not yet prove the generic sign of `Delta_b`, the full local
marked-host theorem, or OPG-1757; the campaign remains in
`survivor_deepening`.
