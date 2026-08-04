# Exact root-Gram certificate for the `q3:RLP` singular box

## 1. Scope and coordinates

This note completes the quartic Gram questions left by
`RLP_PROJECTIVE_CORNER_REDUCTION.md` on one exact local box.  It does not
certify the complementary compact projective region and therefore does not
close the full `q3:RLP` activity chamber.

In the `q0`-maximal small-direction chart, put

```text
x=B*v*t*y,
0<=y<=1, 0<=a<=1/128, 0<=B<=1, 0<=v<=1/128, 0<=t<=1/32.
```

Thus the certificate covers the complete direction interval `0<=B<=1`, not
only the exploratory half-box `B<=1/2`.  With

```text
D=(1+t*y)*(1+t*v*y),
N=t^2*v*y^2+2*t*v*y+v^2*y-2*v*y+v+y,
w=D*z-N,
```

the normalized polynomial is the quartic

```text
R(w)=r0+r1*w+r2*w^2+r3*w^3+r4*w^4
```

with tridiagonal Gram matrix

```text
G = [[r0,r1/2,0],
     [r1/2,r2,r3/2],
     [0,r3/2,r4]].                                      (1.1)
```

## 2. Three exact kernels

Retain the factors from the projective reduction,

```text
C1=1-a+B,
C2=(1-a)*(1+t*v*y)+B*v*y*(1-a+a*t).
```

Exact polynomial division gives

```text
r0=B*R0,
r1=B*R1,
K24=B*Kbar,

4*r2*r4-r3^2
  =4*y^2*B^3*v^2*C2*F4^2*Kbar.                         (2.1)
```

The full Gram determinant reduces without remainder to

```text
4*det(G)=y^2*B^4*v^2*C2*F4^2*D4,
D4=4*R0*Kbar-C1*R1^2.                                  (2.2)
```

The reconstructed kernels have 16,469, 11,141, and 8,599 terms for
`R0,R1,Kbar`, respectively.  Their canonical hashes are fixed by the
verifier before the large convolution begins.

## 3. Exact Bernstein ledgers

On the box in Section 1, the direct tensor Bernstein ledgers give

| kernel | all controls | positive | zero | negative | minimum nonzero |
|---|---:|---:|---:|---:|---:|
| `R0` | 184,320 | 182,400 | 1,920 | 0 | `2048383/4672924418048` |
| `Kbar` | 108,864 | 108,864 | 0 | 0 | `4195872914689/4398046511104` |
| `D4` | 3,615,840 | 3,602,880 | 12,960 | 0 | positive when nonzero |

For `D4`, the tensor shape in `(y,a,v,t,B)` is

```text
(27,10,31,27,16).
```

The 16 `B` rows each contain exactly 810 structural zeros and no negative
control.  Their individual hashes and the combined hash

```text
a67b71d9eb45d916cd832016834eaffe30b9bb3b46bb3142a245769fb1d57e52
```

are recorded in `rlp_root_gram_certificate.json`.

## 4. Why this proves positive semidefiniteness

On the stated box, `C1>0` and `C2>0`.  The first Bernstein ledger gives
`r0=B*R0>=0`; the factorization of `r4` gives `r4>=0`; and the strict
`Kbar` ledger makes the lower principal minor in (2.1) nonnegative.  The
`D4` ledger and (2.2) make the full determinant nonnegative.

Where `r4>0`,

```text
det(G)=r4*(r0*r2-r1^2/4)-r0*r3^2/4
```

therefore also gives the upper `2 x 2` principal minor nonnegative.  The
lower minor similarly gives `r2>=0`.  The same inequalities extend to the
zero-factor strata by continuity, since points with `r4>0` are dense.  All
principal minors of the symmetric matrix (1.1) are therefore nonnegative,
so `G` is positive semidefinite and `R(w)>=0` for every real `w`.

## 5. Exact convolution and reproduction

The large products use Kronecker substitution in base `2^64`.  Positive and
negative parts are multiplied separately.  Their rigorous coefficient
carry bounds use only 39 bits for `R0*Kbar` and 41 bits for `R1^2`, so no
base digit can carry into an adjacent tensor entry.  Four standard-library
worker processes perform the independent integer products; all subsequent
transforms are exact integer operations whose signs equal the rational
Bernstein signs.

Run from the campaign directory:

```sh
timeout 900s python3 evidence/verify_rlp_root_gram_certificate.py \
  | diff -u evidence/rlp_root_gram_certificate.json -
```

No per-process virtual-memory ceiling is required; execution uses the WSL
total-memory limit.  The verifier reconstructs the original forest
polynomials before checking every identity and ledger.

Mathematical status: this removes the square-zero root stratum as an
obstruction throughout the exact local box.  Coverage remains 63 of 81
negative-page chambers, with 18 open.  The complementary projective region,
the generic sign of `Delta_b`, the full marked-host theorem, and OPG-1757
remain open.
