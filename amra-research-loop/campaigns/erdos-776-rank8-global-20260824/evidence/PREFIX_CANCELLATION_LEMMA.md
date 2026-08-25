# Exact canonical prefix cancellation

## Lemma

Fix integers `q>s>=1`.  Let

\[
 P=\sum_{i=s+1}^{q}{a_i\choose i},
 \qquad a_q>a_{q-1}>\cdots>a_{s+1}\ge s+1.
\]

Let `x` be a nonnegative integer whose `s`-canonical expansion has every
upper index strictly below `a_{s+1}`.  Then the `q`-canonical expansion of
`P+x` is the displayed prefix followed by the `s`-canonical expansion of
`x`, and therefore

\[
 \operatorname{KK}_q(P+x)
 =\sum_{i=s+1}^{q}{a_i\choose i-1}
  +\operatorname{KK}_s(x).                              \tag{1}
\]

Consequently, if both `x` and `y` obey the same separator condition, then

\[
 \operatorname{KK}_q(P+y)-\operatorname{KK}_q(P+x)
 =\operatorname{KK}_s(y)-\operatorname{KK}_s(x).        \tag{2}
\]

## Proof

The upper indices in the concatenated list are strictly decreasing: this is
true inside the prefix and inside the canonical suffix, and the separator
hypothesis supplies the one inequality across their join.  The list has the
required lower indices and its binomial sum is `P+x`.  Uniqueness of the
Macaulay canonical expansion makes it the canonical word of `P+x`.
Applying the lower-shadow operator term by term gives (1); subtracting two
instances gives (2).

The executable verifier checks 92,242 small separated concatenations, but
the proof above is the all-parameter justification.

## Exact scope and remaining gap

This lemma supplies genuine overlap credit: a common high prefix contributes
zero to the difference of two shadows.  It does **not** prove that the
adjacent shortened orbits for `V` and `V+1` share a prefix at every rank.  The
lemma may be used only after a separator has been proved independently of the
rank-six target.  In particular, imposing the separator directly on the new
rank-six residual can be equivalent to assuming the desired cap and is
circular.  Moreover, the actual `V=56 -> 57` rank-seven words have different
first terms, so a uniform adjacent-prefix assertion is false.  The refined
`M776G-01` route in `HIGH_RANK_ONE_SIDED_BRIDGE.md` instead asks for
independent separation only at ranks 7 through 14 and crosses all word walls
with the one-sided subadditive carry lemma.
