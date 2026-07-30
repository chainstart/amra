# Dimension-ten human boundary: independent audit

Date: 2026-07-30

## Audited claim

Let \(J\) be a finite-dimensional nilpotent associative algebra over
\(\mathbb F_3\), with \(J^9=0\).  If two raw cubes in \(J\) do not
commute, then

\[
\dim_{\mathbb F_3}J\ge 11.
\]

This is a statement about noncommuting algebra cubes.  It does not assume
that the raw cube set is closed, and it does not by itself construct or
exclude every Wilson counterexample.

## Scope correction

For \(\dim J=10\), noncommuting cubes require \(J^6\ne0\) and
\(\dim J/J^2\ge2\).  The condition \(J^9=0\) allows filtration lengths
only \(6,7,8\).  Their positive-composition counts are respectively

\[
56,\quad28,\quad8,
\]

for a total of 92.  A length-nine tuple has
\(J^9/J^{10}\ne0\) and is outside the stated exponent-nine scope.  The
former count 93 therefore contained one inadmissible profile.

## Proof-dependency audit

The complete exclusion uses only the following implications.

1. \(A_iA_j=A_{i+j}\), hence \(d_{i+j}\le d_i d_j\).
2. If \(d_i=1\) for \(i\ge2\), then \(d_{i+1}\le1\).  With
   \(V=A_1\), associativity gives
   \(f_i\otimes R=L\otimes f_i\).  Applying two independent coordinate
   forms on \(A_{i+1}\) would make the same nonzero tensor \(f_i\) a pure
   power of two independent linear forms.  This contradicts injectivity
   of the dual of the surjection \(R:V\to A_{i+1}\).
3. For length six, \(d_3=1\) forces cube commutativity by degree; and
   \(d_5=d_6=1\) makes the sixfold word tensor a symmetric pure power.
4. For length seven, the power lemma with
   \(d_3=d_4=d_6=1\) removes three profiles.
5. The only remaining profile with \(d_3=2\) has
   \(d_4=\cdots=d_7=1\).  Choosing \(t\) along the common pure tensor and
   \(u\) in the kernel of multiplication \(A_3A_1\to A_4\) gives
   \(ut,tu\in J^5\).  The identity \((tu)t=t(ut)\) matches their
   \(t^5,t^6\) coefficients, and consequently
   \(ut^3=t^3u\).  Also \(uJ^4=J^4u=0\), because the exceptional
   filtration gain puts these products in \(J^8=0\).  Thus \(J^3\) is
   commutative.
6. For length eight, the final two profiles have
   \(d_3=\cdots=d_8=1\).  Then \(t^3,\ldots,t^8\) are a
   filtration-adapted basis of \(J^3\), so \(J^3\) is commutative.

The potentially dangerous point in item 5 is the filtered
\(A_3A_3\to A_7\) correction.  The proof does not delete it: it permits
different \(t^7\) coefficients in \(ut\) and \(tu\), then observes that
two further multiplications annihilate their difference.

## Independent executable ledger

`audit_dim10_boundary_independent.py` does not import the campaign's
original profile search.  It uses a Cartesian-product enumeration and
assigns every admissible tuple to its first applicable human lemma.  Its
partition is

| first exclusion | count |
|---|---:|
| layer rank | 63 |
| \(d_2=1\Rightarrow d_3\le1\) | 6 |
| length-six degree bound | 9 |
| general line propagation | 4 |
| sixfold tail tensor | 4 |
| seven-layer power lemma | 3 |
| cyclic \(J^3\) lemma | 1 |
| cyclic-basis lemma | 2 |
| survivors | **0** |

Run:

```bash
python3 audit_dim10_boundary_independent.py
pytest -q test_audit_dim10_boundary_independent.py
```

## Sharpness and remaining Wilson gap

`verify_dim11_sharp_noncommuting_cubes.py` checks an 11-dimensional
associative algebra with two noncommuting cubes, so the dimension bound is
sharp if one uses only cube commutativity.  It also enumerates the raw
cube set and finds 171 values, with an explicit missing circle product.
Thus that algebra is **not** a Wilson counterexample.

Any further improvement must use the closure of the raw cube set.  The
publication-safe boundary is therefore:

> The exponent-nine algebra-group route has no noncommuting-cube
> candidate below algebra dimension 11; dimension 11 is sharp before
> imposing raw-cube closure.
