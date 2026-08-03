# Eleven certified nonnegative-effective-route chambers

## 1. Finite sign partition

Assume

```text
q0,q3,q4,c >= 0
```

and all edge floors are positive.  On each length-two page, at most one edge
activity can be negative.  Encode its sign type by

```text
P = both activities are nonnegative,
L = the left activity is negative,
R = the right activity is negative.
```

For a negative activity, use the exact parameterization

```text
xL=-t,  xR=(q+t)/(1-t),  0<=t<1                 (L)
```

or its left/right reversal.  A square power of `1-t` clears every
denominator because `Delta_b` has degree at most two in each edge.

## 2. Seven direct Bernstein chambers

Exact multivariate power-to-Bernstein conversion in every bounded `t`
coordinate gives strictly positive coefficient polynomials in the remaining
unbounded nonnegative variables for

```text
PPP,
PLL, PRR,
LPL, RPR,
LLP, RRP.                                      (2.1)
```

Thus (2.1) certifies the all-nonnegative activity chamber and every chamber
with exactly two negative activities lying on the same hub side.  The
verifier records between 178 and 874 nonzero Bernstein coefficients; their
smallest exact coefficient is positive.

## 3. One negative activity on a nonshared page

The raw Bernstein test is inconclusive when only page `3` or `4` has a
negative activity.  It nevertheless has a small exact certificate.  For the
representative `PPL`, put

```text
a=x01, b=x02, r=x13, z=x23 >=0,
x14=-t, x24=(q4+t)/(1-t), 0<=t<1.
```

The 214-term cleared cubic has the exact factorization

```text
(1-t)^2*Delta_b
 =(1-t)*[beta0*(1-t)^2+2*beta1*t*(1-t)+beta2*t^2]. (3.1)
```

The three Bernstein entries satisfy

```text
beta0 = a^2*H0,

beta2 = (q4+1)*[c^2*(a*z-b*r)^2+H2],

beta0*beta2-beta1^2 = a^2*b^2*Hdet,             (3.2)
```

where `H0`, `H2`, and `Hdet` have respectively `47,42,628` monomials and
every coefficient is strictly positive.  Hence

```text
[ beta0 beta1 ]
[ beta1 beta2 ] >= 0,
```

and the bracket in (3.1) is nonnegative on `[0,1]`.  Since `1-t>0`, this
proves `Delta_b>=0` in `PPL`.  The verifier checks the exact graph
relabelings giving the three other copies

```text
PPR, PLP, PRP.                                  (3.3)
```

## 4. Coverage and boundary

Together, (2.1) and (3.3) prove 11 of the 27 activity-sign chambers under
`q0,q3,q4,c>=0`:

```text
LLP, LPL, PLL, PLP, PPL, PPP,
PPR, PRP, PRR, RPR, RRP.
```

This is a strict partial theorem.  The 16 remaining nonnegative-route sign
chambers include a lone negative activity on the shared page `0`, opposite-
side two-negative patterns, and all three-negative patterns.  The exact
matrix chamber also permits one negative effective route, which is outside
the scope of this ledger.

## 5. Reproduction

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 524288
timeout 120s python3 evidence/verify_nonnegative_route_chambers.py
```

The verifier uses only Python's standard library.  It reconstructs
`Delta_b` from all forests, performs every rational substitution and
Bernstein transform, verifies the four relabelings, and checks (3.1)--(3.2)
by exact sparse arithmetic.  No generic sign, full marked-host theorem, or
OPG-1757 closure is claimed.
