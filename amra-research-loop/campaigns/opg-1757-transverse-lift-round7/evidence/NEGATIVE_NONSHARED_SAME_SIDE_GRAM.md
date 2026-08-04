# Same-side Gram certificates for negative nonshared pages

## 1. Scope and symmetry

This note treats the cases in which page `3` or page `4` is the sole
negative diagonal route.  For a negative page quantity `-a`, retain the
Schur coordinate

```text
a=tau*P/B,                 0<=tau<=1,
```

where `P` is the product of the other three positive route quantities and
`B` is their product plus their three pairwise products.  Positive pages
use the uniform `q,s` charts, and the negative page uses its `L/R` chart.

The original 178-term polynomial is exactly invariant under swapping pages
`3` and `4`; the verifier checks that sparse identity and also checks the
corresponding cleared-chart identities.  Global hub exchange supplies the
second word in each row:

```text
q3: LLL <-> RRR,          q4: LLL <-> RRR,
q3: RLL <-> LRR,          q4: RLL <-> LRR.             (1.1)
```

Thus two representatives certify eight route/chamber pairs.

## 2. The `LLL` representative

After all positive denominators and `B^2` are cleared, exact division
removes

```text
c*(1-s3)*(1-s4).
```

The remaining 935-term polynomial is quadratic in `s4`.  Its two endpoint
ledgers have 477 and 971 strictly positive Bernstein coefficients, both
with minimum `1/12`.  The 7,740-term Gram determinant has common monomial
`s0^2*q4`; after division, all 13,667 tensor Bernstein coefficients are
positive, with minimum `1/270`.  Hence this representative and its three
images in (1.1) are nonnegative.

## 3. The `RLL` representative

The same positive factor leaves a 786-term polynomial, now quadratic in
`s3`.  Its endpoint ledgers contain 363 and 796 positive coefficients with
minima `1/12` and `1/6`.  The 5,802-term Gram determinant has common
monomial `c*s0^2*q4`; its residual has 11,551 positive Bernstein
coefficients, with minimum `1/270`.  This proves the other four cases in
(1.1).

## 4. Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 300s python3 evidence/verify_negative_nonshared_same_side_gram.py
```

The standard-library verifier reconstructs the forest polynomials, checks
both page charts and both exact symmetries, performs the manifest divisions,
and verifies every endpoint and determinant coefficient.  Its output must
match `negative_nonshared_same_side_gram.json` exactly.

Mathematical status: eight further negative-page route/chamber pairs are
closed.  Combined negative-page coverage is now 55 of 81, leaving 26
orientations.  The generic theorem and OPG-1757 are not claimed; the
campaign remains in `survivor_deepening`.
