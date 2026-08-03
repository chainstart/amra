# Direct Gram certificates for the three page connections

## 1. Graph-native connection polynomials

Delete `b=04` and retain the four parallel routes between hubs `1,2`: the
direct edge `c` and the three pages through `0,3,4`.  For page `i`, write

```text
qi=li*ri+li+ri,   yiL=1+li,   yiR=1+ri.
```

Let `pij` be the complement polynomial of forests connecting the internal
vertices `i,j`.  Fresh enumeration gives 81 forests and 34 connecting
forests for each of `p03,p04,p34`.  If `k` is the remaining page, exact
state compression gives

```text
pij = c*qk*(pi+pj+sij) + (c+qk)*pi*pj,
pi  = li+ri,
sij = li*lj+ri*rj.                                      (1.1)
```

For `(i,j,k)=(0,3,4)`, `p03` is exactly the polynomial `D=partial_b xi_03`
in `B_RAYLEIGH_REDUCTION.md`.  The other two copies are reconstructed from
the graph rather than asserted by symmetry.

## 2. A three-dimensional Gram identity

Eliminate each right activity without choosing a square root:

```text
ri=(qi-li)/(1+li).
```

The edge-floor hypothesis makes every denominator `1+li` positive.  Put

```text
A = det(diag(q0,q3,q4,c)+1*1^T),
Tk=c+qk,
Lk=c*qk,
Mk=c+qk+c*qk,
Ej=c*qj+c*qk+qj*qk,
Ei=c*qi+c*qk+qi*qk,

Hk = [ Mk  Lk  Lk ]
     [ Lk  Ej  Lk ]
     [ Lk  Lk  Ei ],

zij=(li*lj,li,lj)^T.
```

Direct expansion of (1.1) proves the exact identity

```text
pij*(1+li)*(1+lj) = A + zij^T Hk zij.                    (2.1)
```

The verifier checks (2.1) for all three permutations.  Each cleared
connection numerator has only 17 terms.

## 3. Positivity on the exact route chamber

Let `Bi` denote the `3 x 3` principal minor of the route matrix complementary
to page `i`.  The three leading Sylvester minors of `Hk` factor as

```text
Mk,
Tk*Bi,
Tk^2*A.                                                  (3.1)
```

On the chamber from `ROUTE_MATRIX_CHAMBER.md`, `A`, `Mk`, and `Bi` are
strictly positive principal minors.  Moreover

```text
Tk=c+qk=Rc+Rk-2>0
```

because `Rc,Rk>0` and the corresponding `2 x 2` principal minor gives
`Rc*Rk>1`.  Hence (3.1) makes `Hk` positive definite.  Equation (2.1) and
the positive edge-floor denominator then give

```text
p03>0,  p04>0,  p34>0                                  (3.2)
```

throughout the projected component.

In particular, (3.2) supplies a direct graph-algebraic proof of `D>0`.  The
external C-Garding argument previously used for that sign is no longer a
logical dependency of the b-fibre reduction.

## 4. Reproduction and boundary

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 524288
timeout 120s python3 evidence/verify_connection_gram.py
```

The verifier uses only Python's standard library.  It independently
enumerates the three connection polynomials, checks their state
compressions, verifies all three Gram identities, and factors every
Sylvester minor by exact sparse-polynomial arithmetic.

Mathematical status: exact author-verified sign theorem for the three
single-connection polynomials.  A coupled Gram, Schur-complement, or
Binet--Cauchy identity is still needed to prove the generic sign of
`Delta_b`; neither the full marked-host theorem nor OPG-1757 is claimed.
