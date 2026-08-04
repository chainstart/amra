# Complete negative-`c` Schur endpoint

## 1. Endpoint and uniform page coordinates

In the part of the route chamber where `c` is the sole negative diagonal
quantity, write

```text
P = q0*q3*q4,
B = q0*q3*q4+q0*q3+q0*q4+q3*q4,
c = -tau*P/B,                 0<tau<1.
```

The boundary endpoint `tau=1` is exactly `det(K)=0`.  All three page
quantities are positive there.  A page of effective activity `q>0` can be
parameterized by one orientation coordinate in the unit interval:

```text
P: xL=q*s,  xR=q*(1-s)/(1+q*s),
L: xL=-s,   xR=(q+s)/(1-s),
R: xR=-s,   xL=(q+s)/(1-s).                    (1.1)
```

The `P` formula covers both nonnegative activities because
`0<=xL<=q`; the `L/R` formulas cover the unique negative activity.  Every
denominator in (1.1) is positive on its stated domain.

Write the full b-fibre as before:

```text
P_graph=A*b+C,  xi_03=D*b+E,  Delta_b=A*E-D*C.
```

At the Schur endpoint `A=det(K)=0`, hence

```text
Delta_b = -D*C.                                  (1.2)
```

The connection Gram certificate proves `D>0` in `K>0`; continuity gives
`D>=0` on this boundary.  It is therefore enough to prove `-C>=0`.

## 2. Sixteen direct chambers

The verifier reconstructs the 47-term `C` from forests, applies (1.1),
substitutes `c=-P/B`, and clears `B^2` and the three positive squared page
denominators.  In sixteen activity chambers, every nonzero tensor Bernstein
coefficient in the three orientation variables is strictly positive:

```text
LLP LLR LPP LPR LRP LRR
PLL PLR PRL PRR
RLL RLP RPL RPP RRL RRP
```

This directly certifies `-C>=0` in those chambers.

## 3. Four nine-term kernels close the other eleven chambers

The remaining endpoint numerators factor exactly into positive monomials,
`B`, factors of the form `1+q*s`, squares or `1-s`, and one of four
nine-term kernels.  The verifier constructs the factors rather than calling
a symbolic factorizer.  Their nonnegative decompositions are

```text
H_A = q0*s0^2*(1-s4)^2
    + q4*s4^2*(1-s0)^2
    + (s0-s4)^2,

H_B = q0*s0^2*(q4+s4)^2
    + q4^2*s0^2
    + q4*s4^2*(1-s0)^2
    + 2*q4*s0*s4+s4^2,

H_C = q0*s0^2*s4^2*(q4+1)
    + q4^2*(1-s0)^2
    + q4*s4*(s0^2*s4+2*(1-s0))
    + s4^2,

H_D = (q0*s4-q4*s0)^2
    + q0^2*q4*s4^2 + q0*q4^2*s0^2
    + 2*q0*q4*s0^2*s4 + 2*q0*q4*s0*s4^2
    + q0*s0^2*s4^2 + q4*s0^2*s4^2.           (3.1)
```

All summands in (3.1) are nonnegative for positive `q0,q4` and unit-
interval `s0,s4`.  The exact chamber assignment is

| kernel | activity chambers |
|---|---|
| `H_A` | `PPP`, `PLP`, `PRP` |
| `H_B` | `PPL` |
| `H_C` | `PPR` |
| `H_D` | `LLL`, `RRR`, `LRL`, `RLR`, `LPL`, `RPR` |

Together with the sixteen direct chambers, these eleven factorizations form
an exact, disjoint partition of all 27 `P/L/R` states.  Thus

```text
-C >= 0  and  Delta_b >= 0                           (3.2)
```

on the complete `c<0`, `det(K)=0` Schur endpoint.

## 4. Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 180s python3 evidence/verify_negative_c_schur_endpoint.py
```

The verifier uses only the Python standard library.  It rebuilds the graph
polynomial from 128 forests, checks all rational page and Schur
substitutions, proves the sixteen Bernstein ledgers and eleven displayed
factorizations, and hashes every endpoint and kernel.  Its JSON output must
match `negative_c_schur_endpoint.json`.

Mathematical status: exact author-verified contact theorem on the full
negative-`c` Schur endpoint.  The interior `0<tau<1` outside the ten already
certified chambers, the three cases with a negative page quantity, generic
interior contact classification, and the full marked-host theorem remain
open.  This result stays within `survivor_deepening` and does not change the
public status of OPG-1757.
