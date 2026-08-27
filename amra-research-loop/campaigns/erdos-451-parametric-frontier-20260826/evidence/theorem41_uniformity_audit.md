# Theorem 4.1 uniformity audit

The growing order `r=O(log(k)/loglog(k))` makes uniformity of the implied
constant essential.  A bound of the form `K <<_r ...` would not suffice without
controlling its growth.

The source paper states Theorem 4.1 with an unsubscripted `<<`.  More
decisively, its public Lean formalization proves the underlying theorem with a
single explicit constant independent of `r`:

```text
c9      = 256
K_const = max 4 c9
B_const = 16 K_const
C0      = 4 B_const
c6      = 4 C0
```

The theorem then concludes

```text
card S < c6 * N * (term1 + term2 + term3) + 2*r*lambda
```

for every natural `r>=2`.  None of `c9`, `K_const`, `B_const`, `C0`, or `c6`
depends on `r`.  This appears in
`ErdosProblem451.upstream.lean`, definitions around lines 2431--2436 and theorem
`konyagin_thm` around lines 3368--3407.  The audited upstream file has SHA-256

```text
44e478bed8d756f271aaffd45af5fa4797fbee857aa780f7412275a521b84004
```

This is read-only dependency evidence from the preceding campaign; no old file
was changed and no new Lean run was performed.  Independent audit must still
check that the pinned formal theorem matches the natural-language Theorem 4.1
used here, but the dangerous possibility of an unrecorded `r`-dependent
constant is not present in the pinned formal statement.
