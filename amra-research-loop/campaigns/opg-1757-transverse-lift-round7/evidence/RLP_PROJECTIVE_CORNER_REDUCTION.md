# Projective corner reduction for the open `q3:RLP` chamber

## 1. Scope

This note records an exact structural reduction for one of the five remaining
negative-page representatives.  The companion
`RLP_ROOT_GRAM_CERTIFICATE.md` now certifies the singular local root box found
here, but the complementary compact region remains open.  Consequently this
note still does not close an activity chamber.

For `q3<0`, use the usual Schur parameter

```text
q3=-tau*c*q0*q4/(c*q0*q4+c*q0+c*q4+q0*q4),   0<=tau<=1.
```

Substitution in the `RLP` activity chart, removal of its manifest positive
factor, and a quadratic Bernstein Gram reduction in `s3` leave an outer Gram
determinant.  After its common monomial and the positive factor

```text
(q0+s0)^2*(c*q0*q4+c*q0+c*q4+q0*q4)
```

are divided out, the unresolved factor is a 1,884-term polynomial `H1884`.
The verifier reconstructs it from the original 128 deletion forests and 58
marked-connection forests and fixes its hash.

## 2. The two total-scale boundary faces

The total degree of `H1884` in `(c,q0,q4)` ranges from 7 through 14.  Its two
extreme homogeneous faces factor exactly as

```text
H[7] = s0^4*(c+q4)
       *(c*q0*(1-tau)+c*q4+q0*q4*(1-tau))^3,                 (2.1)

H[14] = c^3*q0^5*q4^5*s4^2*(1-tau)^3
        *(c*(s0+s4-1)^2+q4*s0^2*s4^2).                      (2.2)
```

Both are manifestly nonnegative on the parameter domain.  Thus neither the
zero-scale nor the infinite-total-scale face supplies a negative asymptotic
direction.

## 3. Projective compactification and common Newton face

Write `(c,q0,q4)=r*(C,Q0,Q4)` and cover the positive direction space by the
three charts in which `c`, `q0`, or `q4` is maximal.  In each chart divide
the common factor `r^7`, put `r=u/(1-u)`, and use local coordinates at the
only unresolved equal-direction corner:

```text
x=1-u,  a=1-A,  z=1-s0,  b=1-B,  v=s4,  t=1-tau.
```

Here `A,B` are the two projective direction ratios.  All three local
polynomials have the same seven-term Pareto face.  At `A=B=1` it is

```text
2*x^3 + t*(x+v^2*t)^2 + t*(x+v*t*(v-z))^2.                 (3.1)
```

More strongly, the verifier checks the following parameter-retaining exact
Newton principals:

```text
Pc = A^4*B^3 * (
       (1+B)*x^3
       + A*t*((x+B*v*t*(v-z))^2+B*(x+B*v^2*t)^2)),          (3.2)

Pq0 = A^3*B^3 * (
        (A+B)*x^3
        + t*(B*(x+B*v^2*t)^2+A*(x+B*v*t*(v-z))^2)),         (3.3)

Pq4 = A^3*B^4 * (
        (1+A)*x^3
        + B*t*((x+v^2*t)^2+A*(x+v*t*(v-z))^2)).             (3.4)
```

They contain respectively 235, 196, and 205 terms after expansion.  Each is
a sum of a nonnegative cubic and two weighted squares.  Their Pareto support
and all seven Pareto coefficients agree exactly with the corresponding local
form of `H1884`; after subtraction, every remainder starts in total local
degree four.  This proves the leading projective asymptotic sign, but not the
sign of the higher-order remainder.

## 4. The small-direction square faces

The remaining adaptive branch moves from `B` near one to the opposite
direction boundary `B=0` in the `c`-maximal and `q0`-maximal charts.  Reverse
the local coordinate `b=1-B`.  At `B=0`, the two exact faces are

```text
c chart:
A^3*x^5*t^3*(1-z)^2*(x*a-x*z-a+1)^2,

q0 chart:
A^4*x^5*t^3*(1-z)^2*(1-x*z)^2.                             (4.1)
```

At `x=0`, they are

```text
c chart:
A^5*B^5*v^2*t^3*((z-v)^2+B*v^2*(1-z)^2),

q0 chart:
A^3*B^5*v^2*t^3*(A*(z-v)^2+B*v^2*(1-z)^2).                (4.2)
```

Hence all four codimension-one faces are nonnegative.  On the subcone
`x<=B*v*t`, put `x=B*v*t*y` and remove the common monomial
`B^5*v^2*t^3`.  Define

```text
F = t^2*v*y^2*z-t^2*v*y^2+t*v*y*z-2*t*v*y+t*y*z
    -v^2*y+2*v*y-v-y+z.
```

The new `B=0` faces become the exact squares

```text
c chart:  A^5*(1+t*v*y)*F^2,
q0 chart: A^4*(1+t*v*y)*F^2.                               (4.3)
```

This explains why ordinary box Bernstein subdivision accumulates at this
boundary: the obstruction is a genuine square-zero stratum, not evidence of
a negative value.

## 5. Root coordinate and quartic Gram kernel

For the `q0` chart set

```text
D=(1+t*y)*(1+t*v*y),
N=t^2*v*y^2+2*t*v*y+v^2*y-2*v*y+v+y,
w=D*z-N=F.
```

After substituting `z=(N+w)/D` and clearing `D^4`, the 5,740-term normalized
form becomes an exact 37,709-term quartic

```text
R(w)=r0+r1*w+r2*w^2+r3*w^3+r4*w^4.
```

It has the tridiagonal Gram representation

```text
R(w) = [1,w,w^2]
       [[r0,r1/2,0],
        [r1/2,r2,r3/2],
        [0,r3/2,r4]]
       [1,w,w^2]^T.                                        (5.1)
```

The two bottom rows factor much further.  With

```text
C1=1+B-a,
C2=(1-a)*(1+t*v*y)+B*v*y*(1-a+a*t),
```

the verifier constructs exact 17-term and 260-term polynomials `F4,H260`
and checks

```text
r3 = -2*y*B*v*C2*F4*H260,
r4 =  y^2*B^2*v^2*C1*C2*F4^2.                             (5.2)
```

Consequently the lower `2 x 2` Gram minor is exactly

```text
4*r2*r4-r3^2
 = 4*y^2*B^2*v^2*C2*F4^2*K24,

K24 = C1*r2-C2*H260^2.                                    (5.3)
```

`K24` has 8,599 terms and a further common factor `B`.  Equations
(5.1)--(5.3) replace the unstructured singular corner by three explicit
Gram principal-minor questions.  The companion exact Bernstein certificate
proves all three on

```text
0<=y<=1, 0<=a<=1/128, 0<=B<=1, 0<=v<=1/128, 0<=t<=1/32.
```

The region outside this local box remains to be proved or falsified.

## 6. Reproduction and consequence

Run the standard-library verifier with

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
timeout 240s python3 evidence/verify_rlp_projective_corner_reduction.py
```

The result eliminates the artificial independent-infinity corner, proves
both total-scale faces and the common Newton principal nonnegative, and
identifies the exact compact kernels still blocking `q3:RLP`.  Coverage
therefore remains 63 of 81 negative-page chambers; 18 are open.  The generic
sign of `Delta_b`, the full marked-host theorem, and OPG-1757 are not claimed.
