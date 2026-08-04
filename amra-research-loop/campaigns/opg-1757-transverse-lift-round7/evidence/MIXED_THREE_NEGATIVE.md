# Mixed three-negative chamber certificate

## 1. Two representatives, one determinant

The six mixed three-negative chambers form two graph-symmetry orbits with
representatives `LLR` and `LRR`.  In the usual route charts, let the slots be

```text
(c,q0,t0,q3,t3,q4,t4),  0<=t0,t3,t4<1.
```

After clearing all square denominators, both representatives have an exact
`(1-t3)(1-t4)` factor.  The remaining polynomials have degrees `(4,2,2)` in
`(t0,t3,t4)` and respectively 212 and 199 terms.

Write either quotient as a quadratic in `t3`.  The remarkable exact
simplification is that the two resulting Gram determinants are identical.
It is therefore enough to prove one common determinant inequality, while
handling the endpoint entries of the two representatives separately.

## 2. Endpoint entries

For `LLR`, both `t3` endpoint entries are quadratics in `t4`.  Their
Bernstein term counts are

```text
27,33,42  and  42,53,67.
```

The two Gram determinants have 224 and 543 terms, all coefficientwise
strictly positive.  The only mixed-sign endpoint in each quadratic has the
form

```text
positive factors * (explicit square + positive residual),
```

where the positive residuals have 21 and 18 terms.  Thus both outer endpoint
entries are nonnegative.

For `LRR`, the `t3=0` endpoint is exactly the `x23=0` specialization of the
already certified `LPR` theorem in `NESTED_SHARED_DISCRIMINANT.md`, after
removing its positive `(1-t4)` factor.  Once the common determinant below is
nonnegative, the other endpoint follows on the strict interior and then by
continuity.

## 3. First discriminant collapse

The common 1378-term outer Gram determinant factors as

```text
t0^2*(q0+t0)^2*H,                              (3.1)
```

where `H` has 729 terms and is quadratic in `q0`.  Its discriminant has the
exact form

```text
disc_q0(H)
=-4*c^2*t4^2*(q4+t4)^2*(1-t0)^2*(q3+1)
  *(c*q3*q4+c*q3+c*q4+q3*q4)*K^2,             (3.2)
```

with a 28-term polynomial `K`.  The verifier recovers `K` by an exact sparse
polynomial square-root algorithm; its own coefficient signs are irrelevant
because only `K^2` occurs.  Equation (3.2) makes the discriminant
nonpositive.

It remains to determine the sign of `H` at one real test value.  At
`q0=-t0`, exact division gives

```text
H(-t0)=c^2*t4^2*(1-t0)^2*J,                   (3.3)
```

where `J` has 73 terms.

## 4. A finite implication certificate for `J`

Regard `J` as a quadratic in `c`:

```text
J=C2*c^2+C1*c+C0.
```

Here `C0` is a seven-term positive-coefficient polynomial and

```text
C2=(q3*q4+q3+q4)*S^2
```

for an explicit six-term signed linear polynomial `S`.  Hence `C0>0` and
`C2>=0` on the strict parameter domain.

Write

```text
C1=q3*t0*L,
disc_c(J)=q3^4*t0^2*t4^2*(q4+1)^2*(q3+1)*R,
```

where `L` and `R` have 23 and 16 terms.  Set

```text
T=q3*q4+q3+q4+t4,
B=t0*T-q3*(q4+t4),
A=B-q3*(q4+t4).
```

The verifier checks the exact identity

```text
t0*L-q3*R=2*q4*A*B.                           (4.1)
```

Suppose `L<0` but `R>=0`.  Then the left side of (4.1) is negative, so
`A*B<0`.  Since `A<B`, necessarily

```text
0<B<q3*(q4+t4).
```

Introduce `z=B`.  Direct substitution gives

```text
T*L=P(q3,q4,t4,z),                             (4.2)
```

where `P` has 28 terms and every coefficient is strictly positive.  The
right side of (4.2) is positive for `z=B>0`, contradicting `L<0`.
Therefore `L<0` implies `R<0`.

If `C1>=0`, the signs of `C0,C2` give `J>0` directly.  If `C1<0`, then
`L<0`, hence `R<0`, so the `c`-discriminant is negative and again `J>0`.
Equations (3.2)--(3.3) now give `H>=0`, and (3.1) proves the common outer
Gram determinant nonnegative.  Both representative quotients, and hence
their original `Delta_b`, are nonnegative.

## 5. Coverage, reproduction, and scope

Page exchange and global hub exchange transport the representatives to

```text
LLR, LRL, LRR, RLL, RLR, RRL.
```

The verifier checks these relabelings on the exact cleared polynomials.
Together with the five earlier sign certificates, all 27 activity-sign
chambers are now certified whenever `q0,q3,q4,c>=0` and edge floors are
positive.

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 300s python3 evidence/verify_mixed_three_negative.py
```

The verifier uses Python's standard library only and redoes every forest
reconstruction, denominator division, Gram determinant, factor division,
perfect-square recovery, implication identity, specialization, and graph
symmetry exactly.

This completes the nonnegative-effective-route sign partition only.  The
four matrix chambers with one negative diagonal route quantity, generic
contact classification, the full marked-host theorem, and OPG-1757 remain
open.
