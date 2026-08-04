# Gram certificates for six negative-`q0` chambers with positive pages

## 1. Scope

Continue with the negative-page coordinates of
`NEGATIVE_PAGE_DIRECT_CHAMBERS.md`.  Thus

```text
q0=-a,  a=tau*c*q3*q4/B,
B=c*q3*q4+c*q3+c*q4+q3*q4,       0<=tau<=1.
```

This note certifies

```text
LPP RPP LPR LRP RPL RLP.                              (1.1)
```

Exact sparse substitutions reduce these to `LPP` and `LPR`.  Page exchange
maps `LPR` to `LRP`.  Global hub exchange, together with swapping the two
raw activities on every `P` page, maps `LPP` to `RPP`, `LPR` to `RPL`, and
`LRP` to `RLP`.  The verifier checks all four polynomial identities rather
than assuming them as graph symmetries.

## 2. Outer Gram form and the `tau=0` endpoint

After clearing the positive chart denominators and the exact factor `B^2`,
write the Schur numerator as

```text
F=(1-tau)^2*beta0+2*tau*(1-tau)*beta1+tau^2*beta2.      (2.1)
```

At `tau=0`, the negative `L` chart is exactly the ordinary nonnegative
`L` chart restricted to `q0=0`.  The verifier reconstructs both charts and
checks the exact identity

```text
beta0=B^2*Delta_chart(q0=0).                            (2.2)
```

Consequently `beta0>=0` follows from the already frozen complete
nonnegative-effective-route theorem.  This is an explicit verified
dependency, not a fresh claim about an unchecked endpoint.

For `LPP`, all 4,145 nonzero tensor Bernstein coefficients of `beta2` in
`s0` are strictly positive, with minimum `1/6`.  For `LPR`, exact division
gives

```text
beta2=(1-s4)*G1084.                                    (2.3)
```

Regard `G1084` as a quadratic in `s4`.  Its two endpoint ledgers contain
428 and 698 positive coefficients, both with minimum `1/6`.  Its Gram
determinant has 5,878 terms and a common `s0^2` factor; after removing that
factor, all 7,331 Bernstein coefficients are positive, with minimum `1/15`.
Thus both endpoints in (2.1) are nonnegative.

## 3. The outer determinants

For `LPP`, exact factorization gives

```text
beta0*beta2-beta1^2
 = c^4*s0^2*u3^2*u4^2
   *(1-s0)^2*q3^2*q4^2*B^2*H195.                      (3.1)
```

Here `q3=u3*v3+u3+v3` and `q4=u4*v4+u4+v4`.  All 215
nonzero Bernstein coefficients of `H195` in `s0` are positive, with
minimum `1`.

For `LPR`, with `q3=u3*v3+u3+v3`, exact factorization gives

```text
beta0*beta2-beta1^2
 = c^4*s0^2*u3^2*q4^2
   *(1-s0)^2*q3^2*(q4+s4)^2*(1-s4)^2*B^2*H87.         (3.2)
```

Treat `H87` as a quadratic in `s4`.  Its endpoint ledgers contain 17 and
57 positive coefficients, both with minimum `1`.  The 222-term inner Gram
determinant has a common `s0^2*v3^2` factor, and its 237 residual Bernstein
coefficients are all positive, again with minimum `1`.  Hence the outer
Gram matrices in (2.1) are positive semidefinite and `F>=0` throughout all
six chambers (1.1).

## 4. Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 300s python3 evidence/verify_negative_q0_positive_page_gram.py
```

The standard-library verifier reconstructs the 178-term boundary
polynomial from 128 deletion forests and 58 connected endpoint forests.  It
then checks the chart identities, Schur substitution, dependency (2.2),
every exact division, all endpoint and determinant Bernstein ledgers, and
the symmetry closure.  Its output must match
`negative_q0_positive_page_gram.json` byte-for-structure.

Mathematical status: these six chambers raise negative-`q0` coverage from
16 to 22 of 27 and total negative-page coverage from 36 to 42 of 81.  The
five negative-`q0` `N` chambers and unresolved negative-`q3/q4` orientations
remain open.  The generic theorem and OPG-1757 are not claimed; the campaign
remains in `survivor_deepening`.
