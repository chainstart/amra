# Nested and conditional Gram certificates for six negative-`q0` chambers

## 1. Scope and outer Schur quadratic

Use the negative-page charts and exact Schur coordinate from
`NEGATIVE_PAGE_DIRECT_CHAMBERS.md` with `q0<0`.  This note treats the six
activity words

```text
LLR LRL LRR RLL RLR RRL.                              (1.1)
```

Thus the shared page `0` has exactly one negative activity, while pages `3`
and `4` also have exactly one negative activity.  Put

```text
q0=-tau*c*q3*q4/B,
B=c*q3*q4+c*q3+c*q4+q3*q4,       0<=tau<=1.
```

After clearing the positive chart denominators and `B^2`, write the numerator
as

```text
F=(1-tau)^2*beta0+2*tau*(1-tau)*beta1+tau^2*beta2.      (1.2)
```

Only two representatives are needed.  Exact sparse substitution verifies

```text
F_RRL=F_LLR,
F_RLL=F_LRR,
F_LRL=F_RLR=swap_(3,4)(F_LLR).                         (1.3)
```

These are checked polynomial identities, not assumed graph symmetries.

## 2. Both outer endpoints

For each representative, `beta0` factors into `s0^2`,
`(1-s3)(1-s4)`, `B^2`, and a quadratic core.  The cores have 66 terms for
`LLR` and 57 terms for `LRR`.  A second Gram certificate in respectively
`s4` and `s0` proves them nonnegative: every endpoint Bernstein coefficient
and every residual determinant Bernstein coefficient is strictly positive.
The determinant minima are both `1/18`.

At `tau=1`, `beta2` factors into `(1-s3)(1-s4)` and two page cores.  The
left-negative core in `LLR` has 28 terms and strictly positive tensor
Bernstein coefficients, with minimum `1/2`.  Each right-negative core has 22
terms.  As a quadratic in `s0`, its two endpoint ledgers and 21-term Gram
determinant have strictly positive Bernstein coefficients, all with minimum
`1`.  Hence

```text
beta0>=0, beta2>=0.                                    (2.1)
```

## 3. The 94-term nested Gram core

For `LLR`, exact division gives

```text
beta0*beta2-beta1^2
 = positive monomial
   *(1-s0)^2*(1-s3)^2*(q4+s4)^2*(1-s4)^2*B^2*H94.      (3.1)
```

The corresponding `LRL` core follows by swapping pages.  Treat `H94` as a
quadratic in `s4`.  Its two Bernstein endpoints contain 36 and 68 nonzero
coefficients with minima `1` and `1/2`.  Its inner determinant has a common
`s0^2` factor; after division, all 428 nonzero tensor Bernstein coefficients
are positive, with minimum `1/6`.  Thus `H94>=0`, proving the outer Gram
matrix positive semidefinite in the four chambers represented by `LLR`.

## 4. The 33-term conditional core

For `LRR` and `RLL`, the same outer determinant reduces to a 33-term core.
Set

```text
Q=q3*q4+q3+q4,
L=s0*(s3+s4)-s3*s4,
T=q3*s4^2+q4*s3^2+s3^2*s4^2,
W=s3+s4-s3*s4.                                         (4.1)
```

The verifier checks

```text
H33=Q*L^2*c^2+M*c+q3*q4*s0^2*T,
M=s0^2*F9+2*q3*q4*s0*W*L,                              (4.2)
```

where

```text
F9=(q3*s4-q4*s3)^2
   +q3^2*q4*s4^2+q3*q4^2*s3^2
   +2*q3*q4*s3^2*s4+2*q3*q4*s3*s4^2
   +(q3+q4)*s3^2*s4^2 >=0.                             (4.3)
```

If `M>=0`, all three coefficients of the nonnegative-`c` quadratic (4.2)
are nonnegative.  Suppose `M<0`.  Then `L<0`, and define

```text
F13=s0^2*F9+4*q3*q4*s3*s4*(1-s0)*L.                    (4.4)
```

The exact discriminant identity is

```text
M^2-4*(Q*L^2)*(q3*q4*s0^2*T)=s0^2*F13*F9.              (4.5)
```

Moreover

```text
-s0*W+2*s3*s4*(1-s0)=s3*s4*(1-s0)-L>0.                (4.6)
```

Using `M<0` in (4.4) therefore gives

```text
F13
 <2*q3*q4*L*(-s0*W+2*s3*s4*(1-s0))
 <=0.                                                   (4.7)
```

Equations (4.3), (4.5), and (4.7) make the discriminant nonpositive in the
only branch where the middle coefficient can matter.  Thus `H33>=0` for
`c>=0`.  Together with (2.1), this proves the outer matrix in (1.2) positive
semidefinite and hence `F>=0` in all six chambers (1.1).

## 5. Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 240s python3 evidence/verify_negative_q0_no_positive_gram.py
```

The standard-library verifier reconstructs the forest polynomials, performs
all chart and Schur substitutions, checks the endpoint factorizations, the
nested Gram ledgers, the symmetry identities, and every algebraic identity
in (4.1)--(4.6).  Its output must match
`negative_q0_no_positive_gram.json` exactly.

Mathematical status: six additional `q0<0` activity chambers are certified.
Together with the preceding direct ledger, 16 of the 27 `q0`-negative
activity chambers are now closed.  Eleven `q0` chambers and the unresolved
`q3/q4` orientations remain; the generic theorem and OPG-1757 are not
claimed, and the campaign remains in `survivor_deepening`.
