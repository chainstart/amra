# Nested-odds Gram certificate for the last five negative-`q0` chambers

## 1. A square chart adapted exactly to `K>0`

Suppose both activities on page `0` are negative and put

```text
P=c*q3*q4,
C=c*q3+c*q4+q3*q4,
Rmax=P/C.
```

For an activity `x` with `-1<x<=0`, its odds `y=-x/(1+x)` is
nonnegative.  If `R=y0L+y0R+y0L*y0R`, then the effective page quantity is
`q0=-R/(1+R)`.  The Schur condition `K>0` is exactly `R<Rmax`.

Fill this admissible interval successively with `0<=s0,t<=1`:

```text
y0L=s0*Rmax,
(1+y0L)*y0R=t*(Rmax-y0L).
```

After returning to the activities this gives

```text
x0L=-s0*P/(C+s0*P),
x0R=-t*(1-s0)*P/(C+P*(s0+t-s0*t)).                    (1.1)
```

The verifier checks both the effective-quantity identity and

```text
numerator(det K)=P*C*(1-s0)*(1-t).                    (1.2)
```

Thus the entire double-negative page chamber is a unit square, and its
interior is precisely `s0,t<1`.  Positive `P` pages use the uniform chart

```text
xL=q*s,  xR=q*(1-s)/(1+q*s),                          (1.3)
```

while `L/R` pages use the preceding one-negative-activity charts.  Page
exchange reduces the five open words to

```text
NPP, NPL, NPR;      NPL<->NLP, NPR<->NRP.              (1.4)
```

Both identities in (1.4) are verified on the exact cleared polynomials.

## 2. First Gram layer

After clearing every positive denominator squared, exact division removes
the following manifest positive factors:

```text
NPP: c^4*q3^4*q4^4*(1+q3*s3)*(1+q4*s4),
NPL/NPR: c^4*q3^4*q4^2*(1+q3*s3)*(1-s4).
```

The residuals have respectively 501, 501, and 474 terms and are quadratic
in `t`.  Their `t=0` endpoints have 25, 129, and 43 strictly positive
tensor Bernstein coefficients, all with minimum `1/6`.

Each `t=1` endpoint factors as `K3*K4`, where

```text
K3=q3^2*s3^2*(c+q4)*(1-s0)^2+B*(s0-s3)^2 >=0,
B=c*q3*q4+c*q3+c*q4+q3*q4.                            (2.1)
```

The three `K4` factors have 18, 18, and 24 terms.  As quadratics in `s0`,
their endpoints and 21-term Gram determinants have strictly positive
Bernstein ledgers.  Hence both endpoints of the outer `t` Gram matrices are
nonnegative.

Their determinants factor into positive monomials and squares times cores
of only 57, 57, and 163 terms.  Common square factors include
`(1-s0)^2`, `(1-s3)^2`, and

```text
(C+s0*P)^2,                                            (2.2)
```

with `(1-s4)^2` for `NPP`, `(q4+s4)^2` for `NPL`, and an
additional `s4^2` monomial for `NPR`.

## 3. Second and third Gram layers

Regard each small core as a quadratic in `s0`.  Every `s0=0` endpoint is
strictly Bernstein-positive.  The `NPP` endpoint at `s0=1` is directly
positive with minimum `1/2`.  For `NPL` and `NPR`, that endpoint is itself
a quadratic in `s3`; its two endpoint ledgers and residual Gram determinant
are strictly positive, with determinant ledgers of 87 and 147 terms.

The inner `s0` Gram determinants for `NPL` and `NPR`, after their common
monomials are removed, have 188 and 598 positive Bernstein coefficients
with minima `1/2` and `1/6`.

The apparent obstruction in `NPP` has an exact final factorization.  Its
123-term residual is

```text
B*C^2*H9,
H9=q3*s3^2*(1-s4)^2
   +q4*s4^2*(1-s3)^2
   +(s3-s4)^2 >=0.                                    (3.1)
```

This completes every Gram layer and proves the cleared numerator
nonnegative in all five chambers (1.4).

## 4. Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 300s python3 evidence/verify_negative_q0_double_negative_gram.py
```

The verifier uses only the Python standard library.  It reconstructs the
178-term boundary polynomial from 128 deletion forests and 58 connected
endpoint forests; checks (1.1)--(1.4); performs every exact division and
polynomial rebuild; verifies all Bernstein and Gram ledgers; and constructs
the sums of squares (2.1) and (3.1) explicitly.  Its output must match
`negative_q0_double_negative_gram.json` exactly.

Mathematical status: all 27 negative-`q0` activity chambers are now closed.
Together with the direct negative-`q3/q4` ledgers, 47 of the 81
negative-page chambers are certified.  The remaining 34 orientations have
negative `q3` or `q4`; the generic theorem and OPG-1757 are not claimed, and
the campaign remains in `survivor_deepening`.
