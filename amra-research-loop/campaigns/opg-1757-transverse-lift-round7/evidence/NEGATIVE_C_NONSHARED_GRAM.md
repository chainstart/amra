# Four negative-`c` chambers from a shared-coordinate Gram matrix

## 1. Reuse the exact shared-page discriminant

Write the boundary determinant as a quadratic in the left activity of the
shared page:

```text
Delta_b = A2*x01^2+A1*x01+A0.
```

The previously verified graph identity is

```text
A1^2-4*A2*A0 = -4*c^2*x02^2*x13^2*x14^2*H,       (1.1)
```

where `H` is a 215-term polynomial.  Thus `A2>=0` and `H>=0` imply
`Delta_b>=0` for the given values of all other activities.

Use the exact negative-`c` Schur coordinate

```text
c = -tau*q0*q3*q4/B,
B = q0*q3*q4+q0*q3+q0*q4+q3*q4,
0<=tau<=1,
```

and the bounded page coordinates from `NEGATIVE_C_SCHUR_ENDPOINT.md`.
For each representative `PPR` and `PRP`, clearing the positive Schur and
page denominators turns `A2` into a polynomial whose 549 nonzero tensor
Bernstein coefficients are strictly positive; the minimum is `1/18`.

## 2. A second quadratic and a `2 x 2` Gram certificate

The substituted `H` is quadratic in the shared-page orientation `s0`.
Write it in Bernstein form as

```text
H = beta0*(1-s0)^2
  + 2*beta1*s0*(1-s0)
  + beta2*s0^2.                                  (2.1)
```

For both representatives, exact tensor Bernstein expansion in the other
two page orientations and `tau` gives

```text
beta0: 507 nonzero coefficients, minimum 1/72,
beta2:  33 nonzero coefficients, minimum 1/36.
```

The middle coefficient is not termwise positive.  Instead, the verifier
forms the Gram determinant

```text
G = beta0*beta2-beta1^2.                         (2.2)
```

After removing its explicit positive common monomial, `G` has 8155 ordinary
terms and 3205 nonzero tensor Bernstein coefficients.  Every coefficient is
strictly positive, with minimum `1/2100`.  Therefore

```text
[ beta0  beta1 ]
[ beta1  beta2 ] >= 0,
```

and (2.1) proves `H>=0`.  Equation (1.1) then proves `Delta_b>=0` in `PPR`
and `PRP` throughout the full closed Schur interval.

## 3. Exact hub images

The verifier independently checks that exchanging hubs `1` and `2`
preserves the 178-term `Delta_b` and all route quantities.  This exchange
swaps `L/R` on every page, hence

```text
PPR -> PPL,
PRP -> PLP.
```

The certificate therefore closes the four chambers

```text
PPL PPR PLP PRP.                                (3.1)
```

Together with `NEGATIVE_C_DIRECT_CHAMBERS.md`, (3.1) raises the certified
interior negative-`c` coverage from ten to fourteen of the 27 activity
chambers.  `NEGATIVE_C_SCHUR_ENDPOINT.md` separately covers all 27 at
`tau=1`.

## 4. Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 180s python3 evidence/verify_negative_c_nonshared_gram.py
```

The standard-library verifier reconstructs the graph polynomials, derives
(1.1), performs every rational substitution, checks all exact Bernstein and
Gram coefficients, verifies the hub symmetry, and hashes the residuals.  Its
JSON output must match `negative_c_nonshared_gram.json`.

Mathematical status: exact author-verified sign theorem for four additional
interior negative-`c` chambers.  Thirteen negative-`c` activity chambers,
the three cases with a negative page quantity, generic interior contact
classification, and the full marked-host theorem remain open.  The campaign
stays in `survivor_deepening`; no public OPG-1757 claim is changed.
