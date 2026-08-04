# Thirty direct chambers with a negative page quantity

## 1. Exact Schur coordinate for any negative page

Assume

```text
K=diag(q0,q3,q4,c)+1*1^T > 0
```

and let one page quantity `qi` be negative.  Positive definiteness allows at
most one negative diagonal quantity, so the direct route and the other two
page quantities are positive.  Denote those three positive quantities by
`r1,r2,r3` and put

```text
P=r1*r2*r3,
B=r1*r2*r3+r1*r2+r1*r3+r2*r3.
```

Writing `qi=-a`, direct expansion of the diagonal-plus-ones determinant gives

```text
det(K)=P-a*B.
```

Consequently the complete open chamber has the exact parameterization

```text
a=tau*P/B,              0<tau<1,
det(K)=P*(1-tau).                                      (1.1)
```

Both `P` and `B` are positive.  In particular `0<a<1`, because `B>P`.
The verifier checks the determinant identity afresh for every retained page
chart rather than relying on a numerical matrix test.

## 2. Complete activity charts

For the negative page `q=-a`, positive edge floors split into exactly three
charts:

```text
N: xL=-a*s,               xR=-a*(1-s)/(1-a*s),  0<=s<=1,
L: xL=-(a+(1-a)*s),       xR=s/(1-s),            0<=s<1,
R: xR=-(a+(1-a)*s),       xL=s/(1-s),            0<=s<1.   (2.1)
```

`N` is the chamber in which both activities are nonpositive; `L/R` names the
unique negative activity when the other one is nonnegative.  The denominators
in (2.1) are positive because `a<1`.  Every positive page uses

```text
P: xL,xR>=0,
L: xL=-s, xR=(q+s)/(1-s),
R: xR=-s, xL=(q+s)/(1-s).                       (2.2)
```

The verifier proves algebraically in every chart that
`xL*xR+xL+xR` equals the prescribed `-a` or `q`.  Thus (2.1)--(2.2), with
their common walls included by continuity, lose no positive-edge-floor
orientations.

## 3. Thirty strict Bernstein ledgers

Reconstruct the 178-term `Delta_b`, apply (2.1)--(2.2), substitute (1.1),
and clear the positive squared page denominators and the exact positive power
of `B`.  Tensor Bernstein transformation in `tau` and every bounded page
coordinate gives strictly positive nonzero coefficients in the following
chambers:

| negative route | certified activity words |
|---|---|
| `q0` | `LLL LLP LPL NLL NLR NRL NRR RPR RRP RRR` |
| `q3` | `LLP LLR LNP LNR PLL PRR RNL RNP RRL RRP` |
| `q4` | `LPL LPN LRL LRN PLL PRR RLN RLR RPN RPR` |

There are ten direct certificates for each negative page, or thirty of the
eighty-one negative-page activity chambers.  Representative exact ledgers
are

| negative route and state | Schur terms | nonzero Bernstein coefficients | minimum |
|---|---:|---:|---:|
| `q0:NLL` | 1300 | 2037 | `1/324` |
| `q0:LLP` | 5158 | 6173 | `1/18` |
| `q3:LNP` | 11409 | 39872 | `1/108` |
| `q3:LLR` | 2323 | 2530 | `1/108` |
| `q4:RPN` | 12343 | 39724 | `1/72` |

All remaining variables occur as ordinary monomials in nonnegative
quantities.  Hence every displayed chamber satisfies

```text
Delta_b >= 0.                                           (3.1)
```

## 4. Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 240s python3 evidence/verify_negative_page_direct_chambers.py
```

The verifier uses only Python's standard library, rebuilds the 128 deletion
forests and 58 marked-connection forests, checks every chart and Schur
identity, and hashes all thirty cleared polynomials.  Its output must match
`negative_page_direct_chambers.json` exactly.

Mathematical status: exact certificates for 30 of 81 negative-page activity
chambers.  Every one of the three negative-page route cases still contains
unresolved orientations, so the generic sign of `Delta_b`, the full local
marked-host theorem, and OPG-1757 remain open.  The campaign stays in
`survivor_deepening`.
