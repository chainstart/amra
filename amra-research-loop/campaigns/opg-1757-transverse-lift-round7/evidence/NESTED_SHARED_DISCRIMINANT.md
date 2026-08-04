# Nested shared/nonshared discriminant certificate

## 1. Representative chamber

Start from the shared-page quadratic

```text
Delta_b=A2*x01^2+A1*x01+A0,
A1^2-4*A2*A0=-4*c^2*x02^2*x13^2*x14^2*H.
```

Allow `x01` to be arbitrary and put the right activity on nonshared page 4
in its negative route chart:

```text
x24=-t,  x14=(q4+t)/(1-t),
0<=t<1, q4,c,x02,x13,x23>=0.                    (1.1)
```

This is the representative sign chamber `LPR` once `x01<0` and its page-0
effective activity is nonnegative.  The argument below is stronger: it does
not use that last effective-activity condition.

## 2. Two exact Bernstein--Gram certificates

After substituting (1.1) and clearing `(1-t)^2`, the leading coefficient
`A2` has an exact factor `(1-t)`.  Its remaining quadratic is

```text
beta0*(1-t)^2+2*beta1*t*(1-t)+beta2*t^2.
```

The three Bernstein entries contain `35,41,50` terms.  Although `beta1` has
10 negative terms, both endpoint entries have strictly positive
coefficients, and

```text
beta0*beta2-beta1^2
```

is a 367-term polynomial with every coefficient strictly positive.  Hence
the associated `2 x 2` Gram matrix is positive semidefinite and `A2>=0`.

The same calculation for the 215-term discriminant residual `H` has an exact
cleared factor `(1-t)^2`.  Its quadratic Bernstein entries contain
`17,28,57` terms; the middle entry has 19 negative terms, while the endpoints
and the 237-term Gram determinant have strictly positive coefficients.
Consequently `H>=0` as well.

On the strict parameter interior, `A2>0` and the discriminant of the
`x01`-quadratic is nonpositive, so `Delta_b>=0` for every real `x01`.
Boundary cases follow by continuity.

## 3. Four new chambers and exact symmetries

Hub exchange, nonshared-page exchange, and their composition transport the
representative to

```text
LPR, RPL, LRP, RLP.
```

The verifier checks all three transports on the exact denominator-cleared
polynomials.  Together with `NONNEGATIVE_ROUTE_CHAMBERS.md` and
`SHARED_PAGE_DISCRIMINANT.md`, this certifies 17 of the 27 activity-sign
chambers for nonnegative effective routes.

## 4. Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 524288
timeout 180s python3 evidence/verify_nested_shared_discriminant.py
```

The verifier uses Python's standard library only.  It reconstructs
`Delta_b` from forests, reconstructs `A2` and `H`, performs the rational
substitution and exact polynomial divisions, verifies both Gram
determinants coefficient by coefficient, and hashes every intermediate
record.

This is still a partial sign theorem.  The two chambers `PLR,PRL`, all eight
three-negative chambers, every chamber with a negative effective route, the
generic Fourier-matrix PSD statement, and OPG-1757 remain open.
