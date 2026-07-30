# Growing-degree unit-orbit search

## Exact finite model

Let \(f\in\mathbb Z[x]\) be monic, irreducible, of degree
\(3\le d\le8\), with constant coefficient \(\pm1\), and let
\(\theta\) be a real root.  The search verifies that \(f\) remains
irreducible over \(\mathbb Q(\sqrt{1365})\), so

\[
\mathbb Q(\theta)\cap\mathbb Q(Y)=\mathbb Q.
\]

All arithmetic is exact in \(\mathbb Z[x]/(f)\).  For
\(e\in[-4,4]\), take \(t=\theta^e\).  Relative to the half-power basis,
the integral shift coordinates are

\[
2u=t-3069t^{-1}+3,\qquad 2c=t+3069t^{-1}.                 \tag{1}
\]

For every nonempty exponent subset, the program forms the smallest
coordinatewise doubled rectangular GAP containing all selected \(u,c\)
as differences.  If this box is \(P\), put \(A=P\cup(P-Y)\).  Every
selected parameter certifies both \((u,c-Y)\) and \((u,-c-Y)\), with exact
representation counts obtained from products of \(M_i-|h_i|\).

The search records both the largest certified average and the largest
ratio of certified nonbaseline gain to \(n^{2/5}\).

## Exact scope and results

The sparse family

\[
f=x^d+a x^j\pm1,\qquad
j\in\{1,d-1\},\quad1\le|a|\le3
\]

leaves 20, 16, 16, 16, 20, and 16 accepted fields in degrees 3 through 8.
All \(511\) subsets were tested in each: 104 fields and 53,144 exact
evaluations.

| degree | best average | box size \(n\) |
|---:|---:|---:|
| 3 | 7.34029 | \(1.0141\times10^{16}\) |
| 4 | 6.66091 | \(1.6977\times10^{20}\) |
| 5 | 6.65670 | \(1.0292\times10^{24}\) |
| 6 | 5.94354 | \(6.3182\times10^{27}\) |
| 7 | 5.30198 | \(3.8790\times10^{31}\) |
| 8 | 4.85830 | \(2.3819\times10^{35}\) |

The best multi-parameter target ratio was \(2.45\times10^{-4}\).

A second search exhausts every cubic and quartic

\[
f=x^d+a_{d-1}x^{d-1}+\cdots+a_1x\pm1,\qquad |a_i|\le2.
\]

After exact filters this gives 36 cubics and 122 quartics, or 80,738
subset evaluations.  The largest averages were:

| degree | polynomial | average | \(n\) |
|---:|---|---:|---:|
| 3 | \(x^3+2x^2+2x-1\) | 7.33858 | \(1.5097\times10^{16}\) |
| 4 | \(x^4-2x^3+2x^2-2x-1\) | 7.36951 | \(5.6878\times10^{21}\) |

The best multi-parameter target ratio was
\(6.19\times10^{-4}\), attained by

\[
f=x^4+x^2-1,\qquad e\in\{-4,-2,0,2,4\}.
\]

Its certified average is \(2.157\ldots\), while
\(n=150{,}810{,}678\).  It remains over three orders of magnitude below
the finite \(n^{2/5}\) target.

## Fixed cyclic-unit lemma

**Cyclic-unit box lemma.**  Fix a non-torsion algebraic unit \(\theta\)
and a power-basis proper box \(P\).  If coordinate vectors of
\(\theta^e\) and \(\theta^{-e}\) fit in \(P-P\), then

\[
|e|=O_\theta(\log|P|).
\]

Kronecker's theorem supplies expanding and contracting archimedean
embeddings.  A vector fitting the box has every archimedean image bounded
by \(O_\theta(|P|)\).  Apply the expanding embedding for positive \(e\)
and the contracting embedding for negative \(e\).

Thus a fixed cyclic algebraic-unit orbit gives only
\(O_\theta(\log n)\) resonant parameters and cannot supply a fixed power.
The constant is not uniform when the field and unit vary with \(n\);
that is the honest remaining gap.

## Interpretation and limitations

No candidate approaches the required scaling, and increasing degree makes
the rectangular-container cost worse.  The result does not exclude:

- several multiplicatively independent units;
- nonrectangular GAPs or coupled unions;
- larger polynomial coefficients or exponent windows;
- accidental compatible differences outside the selected orbit;
- fields whose smallest unit height approaches one as degree grows.

The next search should abandon single cyclic orbits and test two-unit
exponent boxes with optimized nonrectangular additive containers.

## Reproducibility

```bash
python3 verify_growing_degree_escape_search.py
pytest -q test_verify_growing_degree_escape_search.py
```
