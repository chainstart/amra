# Shared-page coordinate discriminant theorem

## 1. A global quadratic in one shared-page activity

Keep the six activities

```text
x02,c,x13,x23,x14,x24
```

nonnegative, but allow `x01` to be any real number.  The exact 178-term
boundary determinant is quadratic in `x01`:

```text
Delta_b=A2*x01^2+A1*x01+A0.                    (1.1)
```

The three coefficient polynomials `A2,A1,A0` have respectively `149,25,4`
terms, and every coefficient is strictly positive.  More decisively, their
discriminant factors as

```text
A1^2-4*A2*A0
 =-4*c^2*x02^2*x13^2*x14^2*H,                 (1.2)
```

where `H` has 215 monomials, all positive, with integer coefficients between
1 and 12.

Thus the discriminant is nonpositive.  When the remaining activities are
strictly positive, `A2>0`, so (1.1) is nonnegative for every real `x01`.
The boundary cases follow directly from the nonnegative coefficients and by
continuity.  Hub exchange gives the identical theorem with `x01,x02`
interchanged.

## 2. New sign chambers

Under the nonnegative-effective-route hypotheses of
`NONNEGATIVE_ROUTE_CHAMBERS.md`, this proves the two previously open chambers

```text
LPP, RPP,
```

where the only negative activity lies on the shared page `0`.  Combined with
the earlier ledger, 13 of the 27 nonnegative-effective-route activity-sign
chambers are now certified.

The theorem is slightly stronger than that count: it does not require a
fixed effective activity `q0`, an edge-floor parameterization, or even a
lower bound on the free real value of `x01`; only the other six activities
are assumed nonnegative.

## 3. Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 524288
timeout 120s python3 evidence/verify_shared_page_discriminant.py
```

The standard-library verifier reconstructs `Delta_b` from forests, extracts
all three quadratic coefficients, checks the 215-term factorization without
a symbolic factorizer, verifies coefficient signs, and checks the hub-swap
copy exactly.

This is a coordinate-discriminant partial theorem.  It does not treat a
second negative activity, a negative effective route, the generic Fourier
matrix, the full marked-host theorem, or OPG-1757.
