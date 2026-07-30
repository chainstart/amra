# Independent audit of dense ruled-column stability

Date: 2026-07-30

Audited target: `DENSE_RULED_COLUMN_STABILITY.md`

Verdict:
\[
\boxed{\textsf{PASS WITH A FACTOR-TWO SHARPENING}.}
\]

The theorem as written is correct.  No hypothesis needed by its proof
is missing.  The one-sided reduction is also correct, but it is
unnecessary: keeping a signed horizontal product removes its factor
\(2\).  This audit proves and independently checks the stronger bound
\[
\boxed{
|\Delta^2(P)|
\ge
\frac{H\Psi(\mathcal E)}
{|\mathcal J|T_\times T_2}.
}\tag{A1}
\]
Consequently the Cauchy--Schwarz version can also be sharpened to
\[
\boxed{
|\Delta^2(P)|
\ge
\frac{H}
{|\mathcal J|T_\times T_2}
\left(
\frac{|\mathcal E|^2}{|\mathcal A|}-|\mathcal E|
\right).
}\tag{A2}
\]
The original displayed bounds, with an additional \(2\) in the
denominator, follow immediately.

## 1. Audit matrix

| Component | Verdict | Independent check |
|---|---:|---|
| Radial degree second moment | PASS | Explicitly enumerated all ordered triples \((k,j,a)\), \(k\ne j\), and compared with \(\sum_a d_a(d_a-1)\). |
| Base-star averaging | PASS | Verified \(\sum_k S_k=\Psi\), hence \(\max_kS_k\ge\Psi/|\mathcal J|\). |
| Left/right split | PASS, nonoptimal | The larger side has at least half the star.  Signed products retain both sides and remove this loss. |
| Multiplication fibre | PASS | For fixed signed \(x=a(j-k_0)\), a positive divisor \(a\mid |x|\) uniquely fixes \(j=k_0+x/a\). |
| Arbitrary sparse integer heights | PASS | Translation by one anchor is injective on every \(H\)-element height subset; no interval, alignment, or additive structure is used. |
| Two-square fibre | PASS | Selected inputs inject into signed integer pairs \((x,y)\); independently brute-counted \(r_2(n)\) and checked \(r_2(n)\le4\tau(n)\). |
| Actual Euclidean realization | PASS | Independently constructed all points and all pairwise squared distances; every selected label occurs in the genuine distance set. |
| Critical exponent | PASS | The radial moment is \(t^{3-o(1)}\), and \(H\Psi/|\mathcal J|=t^{4-o(1)}\); divisor maxima cost only \(t^{o(1)}\). |
| Common rational denominator | PASS in limited scope | A single polynomially bounded common denominator can be cleared; unrelated denominators are not covered. |

## 2. Radial second moment and star average

For each \(a\), let
\[
N(a)=\{j:(j,a)\in\mathcal E\},\qquad d_a=|N(a)|.
\]
The set
\[
\mathcal Q
=\{(k,j,a):k,j\in N(a),\ k\ne j\}
\]
has cardinality
\[
|\mathcal Q|=\sum_a d_a(d_a-1)=\Psi(\mathcal E).
\tag{A3}
\]
Partitioning \(\mathcal Q\) by its first slope gives
\[
\mathcal Q=\bigsqcup_{k\in\mathcal J}\mathcal Q_k,
\qquad |\mathcal Q_k|=S_k.
\]
Therefore
\[
\sum_kS_k=\Psi(\mathcal E)
\quad\Longrightarrow\quad
S_{k_0}\ge\frac{\Psi(\mathcal E)}{|\mathcal J|}
\tag{A4}
\]
for some \(k_0\).  This confirms that the ordered convention in
\(\Psi\) and the star convention in the manuscript agree exactly;
there is no hidden factor of two here.

Cauchy--Schwarz over all declared radial classes, including those of
degree zero, gives
\[
\Psi
=\sum_ad_a^2-|\mathcal E|
\ge\frac{|\mathcal E|^2}{|\mathcal A|}
-|\mathcal E|.
\tag{A5}
\]
If the right-hand side is negative, the resulting lower bound is merely
vacuous, as the manuscript states.

## 3. Left/right split and the stronger signed argument

The manuscript splits \(\mathcal Q_{k_0}\) into \(j<k_0\) and
\(j>k_0\), retains the larger part, and uses
\[
x=a|j-k_0|>0.
\]
This is valid: after the side is fixed, \(a\mid x\) determines both
\(|j-k_0|\) and its sign, hence \(j\).  The loss is at most two.

For the sharpening, do not split.  Put instead
\[
x=a(j-k_0)\in\mathbb Z\setminus\{0\}.
\tag{A6}
\]
For fixed signed \(x\), every representation chooses a positive divisor
\(a\mid |x|\), after which
\[
j=k_0+\frac{x}{a}
\]
is unique.  Thus every fibre of the map
\((j,a)\mapsto a(j-k_0)\) has size at most
\(\tau(|x|)\le T_\times\), and the signed product set
\(\mathcal X_\pm\) satisfies
\[
|\mathcal X_\pm|
\ge\frac{S_{k_0}}{T_\times}
\ge\frac{\Psi(\mathcal E)}
{|\mathcal J|T_\times}.
\tag{A7}
\]
There is no later penalty for allowing both signs: the classical
quantity \(r_2(n)\) already counts ordered signed pairs.

## 4. Sparse height fibres and two-square labels

For every \(x\in\mathcal X_\pm\), choose one representing
\((j_x,a_x)\), one anchor
\(z_x^0\in\mathcal Z_{k_0,a_x}\), and any \(H\) distinct elements
\(z\in\mathcal Z_{j_x,a_x}\).  The corresponding distance is
\[
x^2+(z-z_x^0)^2.
\tag{A8}
\]
For fixed \(x\), translation by \(-z_x^0\) is injective.  Distinct
\(x\)'s remain distinct as ordered inputs even if their squares agree.
Hence there are exactly \(|\mathcal X_\pm|H\) distinct signed integer
input pairs
\[
(x,z-z_x^0).
\tag{A9}
\]

For a positive label \(n\), at most
\[
r_2(n)
=4\sum_{d\mid n}\chi_4(d)
\le4\tau(n)
\le T_2
\tag{A10}
\]
such pairs map to \(n\).  The range assumptions give
\[
0<n\le(RL)^2+(2Z)^2.
\]
Dividing (A9) by (A10) and using (A7) proves (A1).

This step uses only:

- distinct integral heights;
- at least \(H\) heights in each occupied column; and
- one uniform absolute height bound \(Z\).

The sets may be sparse, different in every column, and have no common
translate.  Conversely, replacing integer heights by arbitrary real
heights would invalidate the divisor argument and is not covered.

## 5. Critical exponent

Under the corollary assumptions,
\[
|\mathcal A|\le O(t),\qquad
|\mathcal E|=t^{2-o(1)}.
\]
Therefore
\[
\frac{|\mathcal E|}{|\mathcal A|}
\ge t^{1-o(1)}\longrightarrow\infty
\]
and
\[
\frac{|\mathcal E|^2}{|\mathcal A|}
-|\mathcal E|
=t^{3-o(1)}.
\tag{A11}
\]
This is the only point where density of the occupied slope--radial
graph is used.  Since \(H=t^{2-o(1)}\) and
\(|\mathcal J|=O(t)\),
\[
\frac{H\Psi}{|\mathcal J|}
=t^{4-o(1)}.
\tag{A12}
\]
Also \(RL=O(t^2)\) and
\((RL)^2+(2Z)^2=O(t^4)\).  The standard maximal-divisor estimate on
fixed polynomial ranges yields
\[
T_\times T_2=t^{o(1)}.
\tag{A13}
\]
Equations (A12)--(A13) confirm the exponent \(4-o(1)\).  The signed
sharpening changes only an absolute factor, not the critical exponent.

## 6. Limited common-denominator extension

There is a safe rational extension, but its scope must be stated
explicitly.  Suppose one fixed integer \(q\ge1\) satisfies
\[
j=\frac{J}{q},\qquad a=\frac{A}{q},\qquad
z=\frac{Z'}q
\]
for integer numerators.  Then
\[
q^2(a,ja,z)=(qA,JA,qZ')\in\mathbb Z^3.
\tag{A14}
\]
All squared distances are multiplied by \(q^4\), so their cardinality
is unchanged.  On a common-radial slice, the scaled horizontal
difference is the integer product
\[
A(J-K),
\]
and the scaled vertical difference is \(q(Z'_1-Z'_0)\).  Thus the same
signed-product and two-square proof applies to the numerator ranges.

For the asymptotic \(t^{o(1)}\) divisor loss, \(q\) and all numerator
ranges must have fixed polynomial height in \(t\).  This observation
does **not** cover independently varying denominators whose least
common multiple may be superpolynomial.

## 7. Independent executable audit

`independent_verify_dense_ruled_columns.py` imports no existing AMRA
verifier.  It independently:

1. computes \(\Psi\) by enumerating ordered shared-radial triples;
2. reconstructs every base star and both sides;
3. verifies positive and signed multiplication fibres using a new
   trial-division implementation of \(\tau\);
4. uses nonlinear, gapped, independently translated height sets;
5. brute-counts signed two-square representations;
6. enumerates the full Euclidean point set and all actual squared
   distances;
7. proves both bounds by exact integer cross-multiplication;
8. exhausts all \(2^6=64\) occupancy patterns on a small column
   universe; and
9. checks the exponent ledger and one common-denominator scaling
   instance.

Run:
```bash
python3 independent_verify_dense_ruled_columns.py \
  > dense_ruled_columns_independent_certificate.json
pytest -q test_independent_verify_dense_ruled_columns.py
```

The saved audit returns `PASS_WITH_SHARPENING`.  The independent test
suite contains five tests.
