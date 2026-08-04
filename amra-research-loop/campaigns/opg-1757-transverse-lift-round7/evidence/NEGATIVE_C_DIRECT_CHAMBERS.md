# Ten direct chambers with a negative direct route

## 1. Exact Schur coordinate

Assume the route matrix

```text
K = diag(q0,q3,q4,c) + 1*1^T
```

is positive definite and that its sole negative diagonal quantity is `c`.
Then `q0,q3,q4>0`.  Put

```text
P = q0*q3*q4,
B = q0*q3*q4 + q0*q3 + q0*q4 + q3*q4.
```

The leading three-route block of `K` is positive definite, `B` is its
determinant, and direct expansion gives

```text
det(K) = P+c*B.
```

Consequently this part of the exact projected component has the unique
parameterization

```text
c = -tau*P/B,       0<tau<1,                 (1.1)
det(K) = P*(1-tau).
```

Conversely, positive `q0,q3,q4` and (1.1) make the leading block and the
Schur complement positive, hence make `K` positive definite.  Thus (1.1)
loses no component points and introduces no outer-cone surrogate.

## 2. Activity sign chambers

For each length-two page with nonnegative effective activity `q`, positive
edge floors allow exactly the familiar three sign types

```text
P: xL,xR>=0,
L: xL=-t, xR=(q+t)/(1-t),
R: xR=-t, xL=(q+t)/(1-t),       0<=t<1.       (2.1)
```

The verifier reconstructs the 178-term `Delta_b` from forests and applies
(2.1) to every page.  It then substitutes (1.1) and clears the positive
factor `B^2` and the positive squared denominators from (2.1).

In every chamber below, the resulting polynomial has strictly positive
nonzero tensor Bernstein coefficients in `tau` and all negative-activity
parameters, with ordinary nonnegative monomials in the remaining unbounded
variables:

```text
PLR PRL
LPP RPP
LPR LRP RPL RLP
LRR RLL
```

The four representative ledgers are

| representative | Schur terms | nonzero Bernstein coefficients | minimum |
|---|---:|---:|---:|
| `PLR` | 2239 | 1353 | `1/18` |
| `LPP` | 7445 | 9548 | `1/12` |
| `LPR` | 3391 | 4253 | `1/36` |
| `LRR` | 1426 | 1788 | `1/108` |

All arithmetic is rational.  Missing tensor coefficients are zero and all
Bernstein basis functions are nonnegative on the closed unit cube, so the
certificate proves

```text
Delta_b >= 0                                             (2.2)
```

in the ten listed chambers.  Interior positivity follows whenever a
strictly positive monomial supporting the certificate is present, but only
the nonnegative conclusion (2.2) is used.

## 3. Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 180s python3 evidence/verify_negative_c_direct_chambers.py
```

The standard-library verifier independently rebuilds the deletion and
connection forest polynomials, checks the 178-term boundary determinant,
performs all rational substitutions, and verifies every exact Bernstein
coefficient.  Its JSON output must match `negative_c_direct_chambers.json`.

Mathematical status: exact author-verified sign certificates for ten of the
27 activity chambers in the `c<0` part of `K>0`.  The other 17 `c<0`
chambers, the three cases with a negative page quantity, generic contact
classification, and the full marked-host theorem remain open.  This does
not advance the campaign past `survivor_deepening` or change the public
status of OPG-1757.
