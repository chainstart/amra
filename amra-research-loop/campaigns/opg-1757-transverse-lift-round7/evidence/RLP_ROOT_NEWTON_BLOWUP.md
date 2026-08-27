# Root-curve and weighted Newton blow-up in the compact `q3:RLP` chart

## 1. Scope

The preceding `q3:RLP` certificates isolate a singular root box, but ordinary
Bernstein subdivision of its complement accumulates at a second internal
curve.  This note reconstructs that curve exactly in the `q0`-maximal
projective chart and proves both Newton principals that meet there
nonnegative.  It does not control the higher weighted orders and therefore
does not close the chamber.

Let `u` be the compactified total route scale, let `A=c/q0` and `B=q4/q0`
be the projective ratios, and retain the page parameters `s0,v=s4,tau`.
All six variables lie in the closed unit interval.

## 2. The internal square face

At `(B,s0)=(0,0)`, the Pareto support of the 4,366-term compact chart is

```text
(deg_B,deg_s0) = (0,2), (1,1), (2,0).
```

Set

```text
D=(1-tau)*(1-u),
E=B*u*(tau-v)*(1-v).
```

The exact sum of those three faces is

```text
A^4*u^2*(1-tau)*(1-u)^3*(D*s0+E)^2.             (2.1)
```

Thus the subdivision accumulation is an actual square-zero curve rather
than evidence for a negative asymptotic direction.  Introduce its root
coordinate

```text
w=D*s0+E.
```

Substitution `s0=(w-E)/D` and multiplication by `D^4` gives an exact
30,669-term quartic

```text
R(w)=r0+r1*w+r2*w^2+r3*w^3+r4*w^4.              (2.2)
```

Its five row sizes are `12128, 8858, 5725, 3034, 924`, and their common
monomials are respectively

```text
u^4*B^3, u^3*B^2, u^2, u, 1.
```

## 3. Exact top-row factorization and Gram kill test

Define the manifestly nonnegative factor

```text
C=A*B*(1-tau*u)+(A+B)*(1-tau)*(1-u).             (3.1)
```

Exact square-root recovery and sparse division construct a 23-term
polynomial `F23` and a 156-term polynomial `H156` for which

```text
r4=(A+B)*C*(1-u)^2*F23^2,
r3=-2*C*(1-u)^2*F23*H156.                        (3.2)
```

Consequently the lower `2 x 2` minor of the natural tridiagonal quartic
Gram factors through

```text
K=(A+B)*r2-C*(1-u)^2*H156^2.                     (3.3)
```

`K` has 6,633 terms and common monomial `u^2*B^2`.  This factorization is a
useful exact reduction, but the corresponding full tridiagonal Gram is not
positive semidefinite throughout the chart.  At

```text
(u,A,B,v,tau)=(11/16,7/8,7/8,7/16,1/16)
```

its lower minor is positive while its full determinant is negative.  This
is a kill test for that sufficient Gram ansatz only: it is not a negative
value of `R(w)` on the admissible interval for `w` and not a counterexample
to the chamber sign.

## 4. The weighted intersection face

The Newton support of (2.2) at `(B,w)=(0,0)` starts with

```text
(deg_B,deg_w)=(3,0), (0,2).
```

The primitive integral blow-up is therefore

```text
B=b^2,  w=b^3*y.
```

Every term is divisible by `b^6`.  After division, the degree-zero face in
`b` is exactly

```text
A^3*u^2*(1-tau)^5*(1-u)^7
  * (u^2*v^2*(1-tau)*(1-v)^2 + A*y^2).           (4.1)
```

All factors and both summands in (4.1) are nonnegative on the closed chart.
This proves the second Newton principal nonnegative and identifies the
correct `2:3` anisotropic scaling for any subsequent resolution tree.

## 5. Reproduction and consequence

Run from the campaign directory:

```sh
python3 evidence/verify_rlp_root_newton_blowup.py \
  | diff -u evidence/rlp_root_newton_blowup.json -
```

The verifier uses only the Python standard library.  It rebuilds the 128
deletion forests and 58 marked-connection forests, reconstructs `H1884`,
checks (2.1)--(4.1) by exact rational polynomial identities, fixes all
decisive hashes, and evaluates the Gram kill test exactly.

This removes the observed internal root curve and its first weighted
intersection as possible negative leading directions.  The higher
`b`-orders still need a finite positive certificate or an exact
counterexample.  Coverage remains 63 of 81 negative-page chambers; the
generic sign of `Delta_b`, the marked-host theorem, and OPG-1757 remain
open.
