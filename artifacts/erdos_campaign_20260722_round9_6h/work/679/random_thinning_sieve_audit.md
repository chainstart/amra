# #679: random thinning and the growing-dimension sieve boundary

Date: 2026-07-22

## Exact thinning identity

Let \(B_p\) be independent Bernoulli variables with
\(\mathbb P(B_p=1)=a\).  Since \(X_p(n)\in\{0,1\}\),

\[
 W(n)=\prod_p(1-aX_p(n))
 =\mathbb E_B,1_{\{X_p(n)=0\text{ for every }p\text{ with }B_p=1\}}. \tag{1}
\]

Thus the soft weight is an exact average of ordinary sifted-set indicators.
This makes a fundamental-lemma attack natural, but it also exposes the
parameter mismatch.

## Effective dimension versus available level

Averaging the local sifting factors in (1) gives

\[
 \prod_{w<p\le y}\left(1-{aH\over p}\right)^{-1}
 =\left({\log y\over\log w}\right)^{aH+o(aH)}.          \tag{2}
\]

Hence the soft/thinned sieve has effective dimension

\[
 \kappa_{\rm eff}=aH=C\sqrt H
 =(C+o(1)){L_1\over L_2}.                              \tag{3}
\]

At the round-8 endpoint \(z=X^{1/L_2}\), even a full level
\(D=X^{O(1)}\) supplies only

\[
 u={\log D\over\log z}=O(L_2),
 \qquad {u\over\kappa_{\rm eff}}ll {L_2^2\over L_1}=o(1). \tag{4}
\]

The classical fundamental lemma is useful when the inclusion--exclusion
level is long compared with the sieve dimension; (4) is the opposite
regime.  In the direct Bonferroni language the same mismatch is exact: the
natural order is

\[
 aHL=(C+o(1))L_1,                                      \tag{5}
\]

whereas a product of top-band primes already exceeds \(X^{O(1)}\) after only
\(O(L_2)\) selections.

## Literature-interface check

A targeted search found the standard fixed-dimension fundamental lemma and
Henriot's Nair--Tenenbaum bounds for polynomial values, including the 2014
erratum.  Those results do not state uniformity for a product of
\(H=(L_1/L_2)^2\) growing linear factors in the regime (4).  Friedlander--
Iwaniec's irregular-density Selberg sieve concerns thin prime sets, not this
growing effective dimension.  No theorem located in the targeted search
supplies the missing uniform estimate.

Primary references checked:

- K. Henriot, *Nair--Tenenbaum bounds uniform with respect to the
  discriminant*, arXiv:1102.1643, together with its published erratum;
- J. Friedlander and H. Iwaniec, *Selberg's sieve of irregular density*,
  arXiv:2206.03479.

Strict conclusion: (1) is useful, but applying an off-the-shelf fundamental
lemma without proving a new estimate uniform in (3)--(4) is invalid.  This
is a parameter audit, not an impossibility theorem for every signed or
weighted sieve.
