# Double-negative activity Gram certificates for nonshared negative pages

## 1. Nested-odds chart

Let page `3` be the sole negative diagonal route and suppose both of its
activities are negative.  With the other positive route quantities
`c,q0,q4`, put

```text
P=c*q0*q4,
C=c*q0+c*q4+q0*q4.
```

The nested-odds square chart of
`NEGATIVE_Q0_DOUBLE_NEGATIVE_GRAM.md` applies verbatim after moving the
negative page:

```text
x3L=-s3*P/(C+s3*P),
x3R=-t*(1-s3)*P/(C+P*(s3+t-s3*t)).                    (1.1)
```

Its exact route-determinant numerator is

```text
P*C*(1-s3)*(1-t).                                     (1.2)
```

The verifier checks the effective page quantity and (1.2) directly.

## 2. Two q3 representatives

For `LNL` and `RNR`, clear every positive denominator squared and divide
the manifest positive factor

```text
c^2*q4*(1-s4)*(C+s3*P).                               (2.1)
```

The residuals have 1,234 and 1,239 terms and are quadratic in `s4`.

For `LNL`, the two endpoint ledgers contain 485 and 1,206 positive
Bernstein coefficients, both with minimum `1/36`.  Its 10,539-term Gram
determinant has common monomial `s0^2*q4`; after division, all 15,900
Bernstein coefficients are positive, with minimum `1/1200`.

For `RNR`, the endpoint counts are 410 and 1,053 with minima `1/18` and
`1/36`.  The 10,374-term determinant has the same common monomial, and all
13,562 residual Bernstein coefficients are positive, with minimum
`1/1350`.

## 3. Page-swap closure and scope

The exact page-`3`/page-`4` invariance of the original 178-term polynomial
maps

```text
q3:LNL -> q4:LLN,
q3:RNR -> q4:RRN.                                     (3.1)
```

The verifier constructs both target chart polynomials and checks (3.1)
coefficient by coefficient.

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 300s python3 evidence/verify_negative_nonshared_double_negative_gram.py
```

Its output must match `negative_nonshared_double_negative_gram.json`
exactly.  These four chambers raise negative-page coverage to 59 of 81;
22 orientations remain open.  The generic theorem and OPG-1757 are not
claimed, and the campaign remains in `survivor_deepening`.
