# Nested Gram certificate for the two all-negative activity chambers

## 1. Domain and the shared-coordinate reduction

Assume that `c` is the sole negative diagonal route quantity and use the
exact Schur coordinate

```text
P = q0*q3*q4,
B = q0*q3*q4+q0*q3+q0*q4+q3*q4,
c = -tau*P/B,                 0<=tau<=1.
```

On the representative chamber `RRR`, the right activity on every page is
negative.  The bounded page chart is

```text
xR = -s,
xL = (q+s)/(1-s),             q>0, 0<=s<1.
```

Write the 178-term boundary determinant as a quadratic in `x01`:

```text
Delta_b = A2*x01^2+A1*x01+A0.
```

The exact shared-page identity from `SHARED_PAGE_DISCRIMINANT.md` is

```text
A1^2-4*A2*A0 = -4*c^2*x02^2*x13^2*x14^2*H.       (1.1)
```

After the `RRR` chart and Schur substitution, all 265 nonzero tensor
Bernstein coefficients of the cleared `A2` are strictly positive; the
minimum is `1/108`.  It remains to prove `H>=0`.

## 2. The inner quadratic and its endpoint coefficient

The cleared Schur numerator of `H` contains an exact positive chart factor
`(1-s0)^2`.  Divide this factor exactly and call the remaining quadratic
`H_tilde`.  In the Bernstein basis of the shared-page coordinate,

```text
H_tilde = beta0*(1-s0)^2
        + 2*beta1*s0*(1-s0)
        + beta2*s0^2.                              (2.1)
```

An exact tensor Bernstein transform in `(t3,t4,tau)` gives three nonzero
coefficients for `beta0`, all strictly positive, with minimum `1/36`.
The middle entry `beta1` is not termwise positive, so it is retained for a
Gram determinant.

To certify `beta2`, abbreviate

```text
a=q3, b=q4, x=t3, y=t4, d=a*y-b*x.
```

The verifier checks the exact factorization

```text
beta2 = a*b*(1-x)^2*(1-y)^2*N(tau),

N(tau) = (1-tau)^2*N0
       + 2*tau*(1-tau)*N1
       + tau^2*N2,                                  (2.2)
```

where the three Bernstein coefficients are

```text
N0 = B^2*(a*y^2+b*x^2+x^2*y^2),

N1 = B/2 * [
      q0*d^2
    + q0*a^2*b*y^2 + q0*a*b^2*x^2
    + 2*q0*a*b*x^2*y^2
    + q0*a*x^2*y^2 + q0*b*x^2*y^2
    + 2*a^2*b*y^2 + 2*a*b^2*x^2 + 2*a*b*x^2*y^2
    ],

N2 = a*b * [
      q0*d^2
    + q0^2*a*b*x^2*y^2
    + q0^2*a*x^2*y^2 + q0^2*b*x^2*y^2
    + q0*a^2*b*y^2 + q0*a*b^2*x^2
    + 2*q0*a*b*x^2*y^2
    + q0*a*x^2*y^2 + q0*b*x^2*y^2
    + a^2*b*y^2 + a*b^2*x^2 + a*b*x^2*y^2
    ].                                                (2.3)
```

Every summand in (2.3) is nonnegative on the chart.  Therefore all three
Bernstein coefficients in (2.2) are nonnegative and `beta2>=0` on the
entire closed Schur interval.

## 3. Exact outer Gram determinant

Form

```text
G = beta0*beta2-beta1^2.
```

The common monomial of `G`, in verifier slot order, is

```text
(0,2,0,3,2,3,2,2),
```

or explicitly

```text
M = q0^2*a^3*x^2*b^3*y^2*tau^2.
```

After exact removal of this monomial and four copies of each chart factor,
the apparent 2003-term residual collapses to the identity

```text
G = M*(1-x)^4*(1-y)^4*B*D*Q,                       (3.1)

D = (1-tau)*q0*(a*b+a+b)+a*b,

Q = d^2
  + a^2*b*y^2 + a*b^2*x^2
  + 2*a*b*x^2*y + 2*a*b*x*y^2
  + a*x^2*y^2 + b*x^2*y^2.                         (3.2)
```

Here `B>0`, `D>0`, and `Q>=0`.  Hence `G>=0`; together with
`beta0,beta2>=0`, this proves that the `2 x 2` matrix with diagonal entries
`beta0,beta2` and off-diagonal entry `beta1` is positive semidefinite.
Equation (2.1) gives `H_tilde>=0`, the removed chart factors give `H>=0`,
and (1.1) finally gives `Delta_b>=0` in `RRR`.

## 4. Hub image, reproduction, and scope

The verifier independently reconstructs and checks the hub exchange

```text
x01 <-> x02,
x13 <-> x23,
x14 <-> x24.
```

It preserves `Delta_b` and sends `RRR` to `LLL`.  Thus the same certificate
closes both all-negative-activity chambers.

Reproduce the certificate with only the Python standard library:

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
python3 evidence/verify_negative_c_all_negative_gram.py
```

The output must match `negative_c_all_negative_gram.json` exactly.  Together
with the direct and nonshared Gram certificates, this raises the certified
interior negative-`c` coverage from fourteen to sixteen of the 27 activity
chambers.  Eleven negative-`c` chambers, the three negative-page cases,
generic contact classification, and the global marked-host theorem remain
open.  The campaign stays in `survivor_deepening`.
