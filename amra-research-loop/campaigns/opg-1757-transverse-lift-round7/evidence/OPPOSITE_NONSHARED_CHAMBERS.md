# Opposite nonshared-negative chamber certificate

## 1. The remaining two-negative pattern

Assume `q0,q3,q4,c>=0` and positive edge floors.  The only two-negative
pattern not covered by the earlier ledgers is represented by `PLR`.  Write

```text
x13=-u,  x23=(q3+u)/(1-u),
x14=(q4+s)/(1-s),  x24=-s,             (1.1)
0<=u,s<1,
```

and let `a=x01,b=x02>=0`.  Exact division after clearing the two square
denominators gives

```text
(1-u)^2*(1-s)^2*Delta_b=(1-u)*(1-s)*Q(u,s),    (1.2)
```

where `Q` has 91 terms and bidegree `(2,2)` in `(u,s)`.

## 2. First nested Bernstein--Gram layer

Write the quadratic in `u` in Bernstein form:

```text
Q=f0(s)*(1-u)^2+2*f1(s)*u*(1-u)+f2(s)*u^2.     (2.1)
```

Both endpoint entries are quadratics in `s`.  For `f0`, the three
Bernstein entries contain `9,11,14` terms; its two endpoint entries and its
53-term Gram determinant have strictly positive coefficients.  For `f2`,
the corresponding counts are `14,20,28`, and its 175-term Gram determinant
is likewise coefficientwise strictly positive.  Thus

```text
f0(s)>=0, f2(s)>=0 on 0<=s<=1.                 (2.2)
```

The mixed Bernstein entries need not be coefficientwise positive, so this
check does not discard the actual obstruction.

## 3. The quartic obstruction collapses to a quadratic discriminant

The remaining Gram determinant is

```text
D(s)=f0(s)*f2(s)-f1(s)^2=a^2*b^2*R.            (3.1)
```

Although `D` is quartic in `s`, the 465-term residual `R` is only quadratic
in the positive-page activity `b`:

```text
R=B2*b^2+B1*b+B0.                              (3.2)
```

The coefficient polynomials `B0,B1,B2` contain `73,151,241` terms.  Every
coefficient of `B0` is strictly positive.  More decisively,

```text
B1^2-4*B0*B2
```

has exactly 1247 nonzero terms and every coefficient is strictly negative.
On the strict nonnegative-parameter interior, (3.2) therefore has positive
constant term and negative discriminant; in particular its leading
coefficient is positive and `R>0` for every real `b`.  The full closed
parameter domain follows by continuity.  Hence `D>=0`, the matrix in (2.1)
is positive semidefinite, and `Q>=0`.  Equation (1.2) proves
`Delta_b>=0` in `PLR`.

Global hub exchange maps `PLR` exactly to `PRL`; the verifier checks this on
the denominator-cleared polynomials.  The combined nonnegative-effective-
route coverage is therefore 19 of 27 chambers.  Only the eight
three-negative sign patterns remain in that route domain.

## 4. Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 1048576
timeout 180s python3 evidence/verify_opposite_nonshared_chambers.py
```

The standard-library verifier reconstructs `Delta_b` from forests, performs
the two exact rational route substitutions, verifies both nested Gram
layers and all 1247 discriminant signs, checks the symmetry copy, and hashes
every intermediate polynomial.

This result does not cover the eight three-negative chambers, any chamber
with a negative effective route, the generic Fourier-matrix statement, the
full marked-host theorem, or OPG-1757.
