# Conditional copositive certificate for the all-positive activity chamber

## 1. The last sole-negative-`c` chamber

Write

```text
P=q0*q3*q4,
B=q0*q3*q4+q0*q3+q0*q4+q3*q4,
c=-tau*P/B,                    0<=tau<=1,
```

and use the positive-page chart on all three pages:

```text
x_iL=qi*si,
x_iR=qi*(1-si)/(1+qi*si),      qi>0, 0<=si<=1.
```

After clearing the three positive denominators and `B^2`, let the resulting
`PPP` numerator be `F`.  It is quadratic in `tau`.  In Bernstein form,

```text
F=(1-tau)^2*beta0
  +2*tau*(1-tau)*beta1
  +tau^2*beta2.                                  (1.1)
```

The verifier reconstructs the 178-term `Delta_b`, its 628-term cleared
`PPP` chart, and the 1395-term Schur numerator before checking every identity
below.

Put `u=1-s0` and, for `j=3,4`, set

```text
Xj=1+qj*sj,
Yj=1+qj*sj^2,
Hj=q0*s0^2*(1-sj)^2
   +qj*sj^2*u^2
   +(s0-sj)^2.                                   (1.2)
```

Exact sparse factorization gives

```text
beta0=q0^4*q3^2*q4^2*s0^2*u^2
      *X3*Y3*X4*Y4*B^2,

beta2=q0^4*q3^4*q4^4*X3*X4*H3*H4.              (1.3)
```

Thus both endpoints are nonnegative; each `Hj` is explicitly a sum of three
weighted squares.  The middle coefficient factors as

```text
2*beta1=-M*K,
M=q0^4*q3^3*q4^3*s0*u*X3*X4*B >=0,             (1.4)
```

where `K` has only 35 terms.  Its sign determines which of two elementary
certificates applies.

## 2. Conditional Gram reduction

Define

```text
Aj=q0*s0^2*(1-sj)^2+(s0-sj)^2,
Ej=Yj*Hj.                                        (2.1)
```

The 12276-term Gram determinant in (1.1) satisfies the exact identity

```text
4*(beta0*beta2-beta1^2)
 =M^2*(4*E3*E4-K^2).                            (2.2)
```

If `K<=0`, then (1.4) gives `beta1>=0`, so all three Bernstein coefficients
in (1.1) are nonnegative and there is nothing more to prove.

Suppose instead that `K>0`.  It is enough by (2.2) to prove

```text
K/2 <= sqrt(E3*E4).                              (2.3)
```

Only this one-sided bound is needed.  The unconditional two-sided Gram
bound is false when `K<0`, which is why the sign split is essential.

## 3. Exact one-sided bound for `K`

Set

```text
Jj=q0*s0*(1-sj)^2+2*(s0-sj),

L=q0*s0^2*(1-s3)*(1-s4)
  +(s0-s3)*(s0-s4).                              (3.1)
```

Expansion of the 35-term kernel gives the short identity

```text
K/2=L-u*q0*s0*(s3-s4)^2/2
    -q3*u*s3^2*J4/2
    -q4*u*s4^2*J3/2
    +q3*q4*u^2*s3^2*s4^2.                       (3.2)
```

First, the exact two-vector Cauchy remainder is

```text
A3*A4-L^2=q0*s0^2*u^2*(s3-s4)^2 >=0,            (3.3)
```

so `L<=sqrt(A3*A4)`.

Second, each scalar `Jj` obeys

```text
-Jj/2 <= sqrt(Aj).                               (3.4)
```

Indeed, (3.4) is immediate when `Jj>=0`.  If `Jj<0`, then `sj>s0` and

```text
q0*s0*(1-sj)^2 < 2*(sj-s0) <= 2*sj.
```

The verifier checks the exact identity

```text
4*Aj-Jj^2
 =q0*s0*(1-sj)^2*(4*sj-q0*s0*(1-sj)^2),         (3.5)
```

whose right side is therefore nonnegative.  This proves (3.4) in the only
case where it is not automatic.

Dropping the nonpositive square term in (3.2) and using (3.3)--(3.4) now
gives

```text
K/2 <= (sqrt(A3)+q3*u*s3^2)
       *(sqrt(A4)+q4*u*s4^2).                    (3.6)
```

Finally,

```text
Ej=(1+qj*sj^2)*(Aj+qj*sj^2*u^2),

Ej-(sqrt(Aj)+qj*u*sj^2)^2
  =qj*sj^2*(sqrt(Aj)-u)^2 >=0.                  (3.7)
```

Equations (3.6)--(3.7) prove (2.3).  Because this branch assumes `K>0`, it
is legitimate to square (2.3); (2.2) then makes the matrix in (1.1)
positive semidefinite.  Thus `F>=0` for every `tau` in the unit interval.
Positive clearing factors recover `Delta_b>=0` in `PPP`, with activity walls
following by continuity.

## 4. Reproduction and scope

Reproduce using the Python standard library only:

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 240s python3 evidence/verify_negative_c_all_positive_copositive.py
```

The output must match `negative_c_all_positive_copositive.json` exactly.
Together with the preceding exact chamber certificates, this completes all
27 activity-sign chambers in the region where `c` is the sole negative
diagonal route quantity.  It does not settle the three K-positive cases in
which a page quantity is negative.  Those cases, generic contact
classification, the global marked-host theorem, and OPG-1757 remain open;
the campaign stays in `survivor_deepening`.
