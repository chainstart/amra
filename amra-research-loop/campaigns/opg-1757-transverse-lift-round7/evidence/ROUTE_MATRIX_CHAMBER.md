# Exact route-matrix chamber and orientation compression

## 1. The projected component is a `4 x 4` positive-definite cone

After deleting `b=04`, put edge floors `y_e=1+x_e` and route products

```text
R0=y01*y02,  R3=y13*y23,  R4=y14*y24,  Rc=1+c.
```

Equivalently, the four effective route activities are

```text
q0=R0-1,  q3=R3-1,  q4=R4-1,  qc=c=Rc-1.
```

The 81-term polynomial `A=partial_b P` from
`B_RAYLEIGH_REDUCTION.md` loses every internal route orientation.  Exact
substitution gives

```text
A = R0*R3*R4*Rc
    - sum_(i<j) Ri*Rj
    + 2*sum_i Ri - 3
  = det K,

K = diag(q0,q3,q4,qc) + 1*1^T
  = [ R0  1   1   1  ]
    [ 1   R3  1   1  ]
    [ 1   1   R4  1  ]
    [ 1   1   1   Rc ].
```

This identifies the distinguished component of `A>0` exactly:

```text
C_A = {all seven edge floors are positive and K is positive definite}. (1.1)
```

Indeed, along an `A`-positive path from the positive anchor the symmetric
matrix `K` stays nonsingular, so its inertia stays positive definite.  Its
positive diagonal entries force all four route products to be positive; an
individual edge floor cannot change sign without making its route product
zero.  Conversely, the affine set `K>0` is convex in `(R0,R3,R4,Rc)`, and
each positive-product orientation fibre is connected to its balanced point.
This proves both inclusions in (1.1), rather than using a derivative outer
cone as a surrogate for the component.

The full b-projection is the same set:

```text
projection(C_P) = C_A.                                      (1.2)
```

For the forward inclusion, use the already audited C-Gårding derivative
nesting `C_P subset C_(partial_b P)`.  For the reverse inclusion, follow a
compact path in `C_A` and choose `b` uniformly large in
`P=A*b+C`; since `A>0`, this lifts the entire path into `P>0`.  The b-line at
the positive anchor then joins that lift to the original anchor.

Thus the exact residual statement from the b-Rayleigh reduction is now

```text
Delta_b >= 0 for positive edge floors with K>0.              (1.3)
```

There is no longer an unspecified projected semialgebraic set in (1.3).

## 2. Every route derivative is a principal minor

For every nonempty subset `S` of the four routes, the verifier checks

```text
det K[S,S] = partial_(routes outside S) A.
```

The `4,6,4,1` principal minors of orders `1,2,3,4` are therefore exactly

```text
Ri,
Mij = Ri*Rj-1,
Bi  = product_(j!=i) Rj - sum_(j!=i) Rj + 2,
A.
```

All are strictly positive on `C_A`.  In particular, for any two routes
`i,j`, `Ri,Rj>0` and `Ri*Rj>1`, so

```text
Sij=Ri+Rj-2 > 0.                                             (2.1)
```

This matrix identity supplies an exact component-complete meaning for the
route inequalities that earlier searches used only as necessary tests.

## 3. Forty-five orientation channels

Choose the positive left-edge floors as orientation coordinates and eliminate
their partners:

```text
y01=h0,  y02=R0/h0,
y13=h3,  y23=R3/h3,
y14=h4,  y24=R4/h4,
```

where `h0,h3,h4>0`.  The sign of `Delta_b` is the sign of

```text
N = h0^2*h3*h4*Delta_b.
```

Exact sparse substitution gives 577 fully expanded monomials but only 45
orientation monomials, with orientation multidegree

```text
deg_(h0,h3,h4) N = (4,2,2).                                 (3.1)
```

This is a much smaller exact object than either the 178-term original-activity
form or the 7063-term q-resultant.

## 4. Both outer h0 slices are strictly positive

Write

```text
S4c=R4+Rc-2, M4c=R4*Rc-1,
S3c=R3+Rc-2, M3c=R3*Rc-1,
B0 =R3*R4*Rc-R3-R4-Rc+2.
```

Here `M4c,M3c,B0>0` are principal minors of `K`, while `S4c,S3c>0`
follows from (2.1).  The leading `h0^4` slice factors exactly as

```text
[M4c*h3^2 - 2*S4c*h3 + R3*S4c]
[M3c*h4^2 - 2*S3c*h4 + R4*S3c].             (4.1)
```

The constant `h0^0` slice is `R0^2` times

```text
[S4c*h3^2 - 2*S4c*h3 + R3*M4c]
[S3c*h4^2 - 2*S3c*h4 + R4*M3c].             (4.2)
```

Each quadratic has positive leading coefficient, and the verifier checks that
its discriminant is respectively

```text
-4*S4c*B0  or  -4*S3c*B0.
```

Consequently all four quadratics, and hence both outer slices, are strictly
positive for every real `h3,h4` on `K>0`.  On the closure they are
nonnegative.  Thus the `h0` quartic is coercively positive at both ends
`h0 -> 0+` and `h0 -> +infinity`; any negative orientation island would have
to be bounded by at least two positive roots.  These outer limits are edge-
floor limits, not the activity walls `x01=0` and `x02=0` already classified
in the preceding ledger.

## 5. Reproduction and boundary

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 524288
timeout 120s python3 evidence/verify_route_matrix_chamber.py
```

The verifier uses only Python's standard library.  It reconstructs the graph
polynomials from forests, proves the determinant and every principal-minor
identity, rebuilds the 45-channel orientation numerator, and verifies (4.1),
(4.2), and all four discriminants without a symbolic factorizer.

Mathematical status: exact author-verified chamber classification and
orientation reduction.  The three middle `h0` coefficients, an equivalent
Gram/Schur certificate, and the generic sign of `Delta_b` remain open.
Nothing here advances the campaign past `survivor_deepening`, proves the full
local marked-host theorem, or changes the public status of OPG-1757.
