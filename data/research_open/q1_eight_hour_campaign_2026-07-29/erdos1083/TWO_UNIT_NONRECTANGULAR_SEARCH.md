# Quartic two-unit and nonrectangular-container search

## Model and exact scope

This round tests whether two unit directions and a tilted additive
container can beat the cyclic-unit sanity check.  It is a finite constant
experiment, not a new asymptotic escape: every fixed quartic field has
fixed unit rank and is already covered asymptotically by the unit-lattice
polylogarithmic bound.

The field family consists of all 122 accepted real irreducible quartics

\[
f=x^4+a_3x^3+a_2x^2+a_1x\pm1,\qquad |a_i|\le2,
\]

which remain irreducible over \(\mathbb Q(\sqrt{1365})\).  Every such field
has at least two real embeddings and unit rank at least two.

For each field, the first unit is \(\theta\).  The program enumerates
power-basis coefficient vectors in \([-1,1]^4\), computes their norm as
the exact determinant of the multiplication matrix, and retains two
norm-\(\pm1\) elements.  It rejects every pair having a multiplicative
relation

\[
\theta^a\varepsilon^b=1,\qquad |a|,|b|\le6.
\]

This is an exact bounded-word independence certificate.  It is not a
claim of global multiplicative independence.

The parameter pool is the nine words

\[
t_{a,b}=\theta^a\varepsilon^b,\qquad -1\le a,b\le1.
\]

All 486 subsets spanning exponent rank two are tested for every unit pair.
For each subset, exact quotient-ring arithmetic computes

\[
2u=t-3069t^{-1}+3,\qquad 2c=t+3069t^{-1}.
\]

There are 122 fields, 244 unit pairs, and 118,584 exact rank-two subset
evaluations.

## Nonrectangular container

The baseline container is the smallest doubled rectangular box in the
quartic power basis.  To test a non-axis-aligned parallelepiped, the search
uses the 25 exactly unimodular coordinate maps

\[
I,\qquad x_i\mapsto x_i\pm x_j\quad(i\ne j).
\]

For every unit pair, the best 32 rectangular candidates under each of the
average and normalized-target objectives are combined, and every one of
their 25 elementary shears is evaluated exactly.  Thus:

- all rank-two subsets have exact rectangular scores;
- the stated finalists have the exact minimum over the one-shear family;
- the search does not claim the global best shear over every discarded
  subset or over arbitrary \(GL_4(\mathbb Z)\).

For a transformed shift \(h\), representation counts remain the exact
product \(\prod_i(M_i-|h_i|)\).

## Best results

The best normalized nonbaseline gain occurs for

\[
f=x^4+x^3-2x-1,\qquad
\varepsilon=-1-\theta,
\]

with the word subset

\[
\{(-1,1),(0,0),(0,1)\}.
\]

The best elementary shear is \(x_0\mapsto x_0-x_3\).  Its exact ledger is

\[
\begin{aligned}
n&=2{,}035{,}999{,}422,\\
\overline d_{\rm cert}
&=\frac{
68{,}010{,}566{,}449{,}710{,}257
}{
38{,}382{,}348{,}577{,}632{,}723
}
=1.772\ldots,\\
\frac{\overline d_{\rm cert}-1}{n^{2/5}}
&=1.45903\times10^{-4}.
\end{aligned}
\]

The corresponding rectangular ratio is
\(1.45205\times10^{-4}\).  The tilt improves the target score by only
about \(0.48\%\).

The largest certified average, rather than target-normalized score, is
\(6.79251\).  It uses all nine words but a box of size
\(3.578\times10^{19}\); its normalized ratio is only
\(6.95\times10^{-8}\).

Two independent directions therefore produce no finite evidence for a
power law in this scope.  The best target ratio is below both the target
and the best single-unit finite sanity check.

## Fixed-rank theorem and conditional rank growth

Let a fixed number field have multiplicative unit rank \(r\).  Dirichlet's
logarithmic embedding sends its units to a rank-\(r\) lattice.  The number
of unit words of height at most \(n^{O(1)}\) is

\[
O_K((\log n)^r).                                          \tag{1}
\]

Since each hyperbola point contributes at most \(n^2\), a necessary
condition for average degree \(n^{2/5}\) is at least \(n^{2/5}\) relevant
unit words.  For one fixed field, combining with (1) forces

\[
r\log\log n\ge(2/5-o(1))\log n,
\]

or

\[
\boxed{
r\ge(2/5-o(1))\frac{\log n}{\log\log n}.
}                                                         \tag{2}
\]

Thus every one fixed quartic field is asymptotically incapable of escape,
regardless of its finite container constant.  In a varying-field family,
rank growth on the scale (2) is necessary only under the uniformity
hypotheses stated next; it must also come with an additive container whose
size does not erase the word count.

For varying fields, the constant in \(O_K\) is not uniform.  Formula (2)
requires uniform polynomial-height control and shortest logarithmic unit
\(\lambda_n=(\log n)^{-o(1)}\).  With only the standard degree-dependent
height bound in a full power-basis box, the safe coefficient is \(1/5\),
not \(2/5\).  See `UNIT_RANK_UNIFORMITY_AUDIT.md`.

## Honest limitations

The certified mass includes only selected two-unit curve points.  Extra
accidental compatible differences could increase the full \(H\).
Furthermore, the search does not cover:

- globally certified fundamental-unit bases;
- word radius larger than one;
- more than two candidate second units per field;
- arbitrary nonrectangular GAPs or general unimodular transformations;
- fields of growing degree and rank.

The next theoretical bottleneck is no longer whether two fixed units help.
It is whether a rank
\(\Omega(\log n/\log\log n)\) unit lattice can have its hyperbola image
compressed into one additive container of size \(n\).

## Reproducibility

```bash
python3 verify_two_unit_nonrectangular_search.py
pytest -q test_verify_two_unit_nonrectangular_search.py
```
