# Same-side three-negative chamber certificate

## 1. The `LLL` representative

Assume `q0,q3,q4,c>=0` and use the left-negative chart on every page:

```text
x_iL=-t_i,  x_iR=(q_i+t_i)/(1-t_i),
0<=t_i<1,  i=0,3,4.                            (1.1)
```

After clearing the three square denominators, exact division gives

```text
product_i(1-t_i)^2*Delta_b=(1-t3)*(1-t4)*Q,    (1.2)
```

where `Q` has 223 terms and degrees `(4,2,2)` in `(t0,t3,t4)`.

## 2. Nested Bernstein--Gram certificate

Regard `Q` as a quadratic in `t3`:

```text
Q=f0*(1-t3)^2+2*f1*t3*(1-t3)+f2*t3^2.          (2.1)
```

The two endpoint entries are quadratics in `t4`.  Their Bernstein entry
counts are respectively

```text
f0: 33,39,51,
f2: 51,62,76.
```

For each endpoint quadratic, its two endpoint coefficients are
coefficientwise strictly positive.  The associated Gram determinants have
224 and 543 terms, again all with strictly positive coefficients.  Hence
`f0,f2>=0` on `0<=t4<=1`.

The remaining Gram determinant

```text
f0*f2-f1^2=t0^2*R(t4)                          (2.2)
```

has a residual quartic in `t4`.  Its five Bernstein coefficient
polynomials contain

```text
224,321,481,514,543
```

terms, and every coefficient is strictly positive.  Thus (2.2) is
nonnegative, the matrix in (2.1) is positive semidefinite, and `Q>=0`.
The positive factors in (1.2) prove `Delta_b>=0` in `LLL`.

Global hub exchange preserves the `(q_i,t_i)` slots and makes the `RRR`
cleared polynomial literally identical.  This adds both `LLL` and `RRR`,
bringing the nonnegative-effective-route coverage to 21 of 27 chambers.

## 3. Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 1048576
timeout 180s python3 evidence/verify_same_side_three_negative.py
```

The verifier uses Python's standard library only.  It reconstructs
`Delta_b` from forests, verifies every denominator division, performs both
Bernstein--Gram layers with exact rational arithmetic, checks all required
coefficient signs, verifies the hub-exchange identity, and hashes every
intermediate polynomial.

Six mixed three-negative chambers, every negative-effective-route case, the
generic Fourier-matrix theorem, the full marked-host theorem, and OPG-1757
remain open.
