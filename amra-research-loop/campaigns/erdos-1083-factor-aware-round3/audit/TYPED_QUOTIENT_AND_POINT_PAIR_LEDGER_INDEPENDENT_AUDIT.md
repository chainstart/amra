# Independent audit: typed quotient host and point-pair ledger

Verdict: **PASS with one dependency precision**.  The decisive lemma is valid
as a scoped algebraic and incidence firewall.  It is not an M01 positivity
theorem, an M10 fibre theorem, or a change to the public `3/5` exponent.

## 1. Normalized Boolean quotient host

Let the Laurent UFD be `R=Z[Gamma]`, with `Gamma` finitely generated and
torsion-free, and factor

\[
 B=u_B\prod_{\nu=1}^D H_\nu
\]

with irreducible occurrences listed separately.  If `Q_j|B`, unique
factorization shows that

\[
 Q_j=u_j\prod_{\nu\in I_j}H_\nu
\]

for a submultiset of occurrences and a Laurent unit `u_j`.  After choosing the
normalized associate with unit one,

\[
 \mathcal Q(y)=\prod_{\nu=1}^D\big((1-y_\nu)+y_\nu H_\nu\big)
\]

legally specializes at `y=1_(I_j)` to `Q_j^norm`.  This repairs the former
type error only at the level of normalized associate classes.

Each coordinate has degree one.  Because every `H_nu` is a nonunit,
`H_nu-1` is nonzero; the Laurent coefficient ring is a domain, so the top
`y_1...y_D` coefficient is nonzero and the total degree is `D`.

With independent formal factors the Boolean specializations are all distinct,
giving `2^D` products.  This is an existential worst-case obstruction, not a
claim that every actual factorization has `2^D` distinct normalized divisors.
Repeated occurrences of one irreducible can make different labelled Boolean
vectors specialize to the same product; the accurate universal count is at
most `2^D` and, by multiplicity types, at most `prod_i(m_i+1)` distinct
divisors.  The decisive lemma's wording “can realize `2^D`” is correct.

## 2. Why the unit and translation must be retained

Units of this Laurent ring are a sign times a monomial.  They are invisible
to the normalized divisor subset but not to the proposed downstream data.
For example,

\[
 H=1+X,\qquad X^3H=X^3+X^4
\]

have the same augmentation two, while their first exponent moments are one
and seven.  Multiplication by `-1` reverses every coefficient sign and hence
changes coefficientwise positivity.  Therefore an application to coefficient
moments or either positive product must restore the row unit `u_j`, including
its monomial translation.  The normalized host alone supplies neither the
original `Q_j` nor the paired-positivity hypotheses of M01.

## 3. K-node delta interpolation

Let `lambda_1,...,lambda_K` be distinct.  A scalar coefficient polynomial
which is zero at the first `K-1` nodes and one at the last has `K-1` distinct
roots, so every interpolant has degree at least `K-1`.  The Lagrange polynomial

\[
 {\prod_{i<K}(T-\lambda_i)\over
  \prod_{i<K}(\lambda_K-\lambda_i)}
\]

attains degree `K-1`.  Thus interpolation existence alone has sharp worst-case
degree `K-1`; it gives no `t^o(1)` complexity theorem.

This is a scoped force for arbitrary samples.  It does not show that actual
exact-block quotient samples realize a delta coefficient, nor does it refute
a future low-degree theorem derived from new positivity/common-X structure.

## 4. Independent point-pair exponent ledger

Using

\[
 K={5\over9},\quad S={7\over9},\quad
 U={5\over6},\quad q={13\over18},
\]

the named point sets have capacities

\[
 |X|=t^{S+o(1)},\quad
 |T_{\rm all}|\le t^{q+U+o(1)}=t^{14/9+o(1)},\quad
 |T_{\rm sel}|\le t^{K+U+o(1)}=t^{25/18+o(1)}.
\]

Consequently:

| Actual pair domain | Exponent |
|---|---:|
| source to all targets | `S+q+U = 7/3` |
| selected target pairs | `2(K+U) = 25/9` |
| selected targets to all targets | `K+U+q+U = 53/18` |
| all target pairs | `2(q+U) = 28/9` |

The first three exponents are below three.  Only the all-target occurrence
pair capacity exceeds three, by `1/9`.

The expression `K+2S+U+q=11/3` (`KS^2Uq`) is not a point-pair domain: it
contains a selected-row index, two source indices, and a target index.  A
source--target pair has one source index; a target--target pair has two target
indices.  Likewise `K+S+U+q=26/9` mixes an auxiliary selected row with a
source--target pair, is not an admissible pair domain, and is below three in
any case.  Neither quantity may be used as a label lower bound.

For one actual occurrence-pair domain of size `t^(28/9-o(1))`, the standard
fibre inequality

\[
 |\operatorname{labels}|\ge {|\mathcal I|\over
 \max_\ell|\mathcal I_\ell|}
\]

requires fibre exponent strictly below

\[
 {28\over9}-(3+\varepsilon)={1\over9}-\varepsilon
\]

to yield `t^(3+epsilon)` labels.  The same exponent applies to a correctly
normalized energy/average-fibre statement.

## 5. Decisive statement and dependencies

The decisive statement matches the proved material if “reaches `28/9`” is
read as an occurrence-pair **capacity**, not an established lower bound for
distinct physical pairs or labels.  Its dependency list correctly retains:

- restoration and control of Laurent units;
- an M01 theorem using information beyond Boolean subset recovery and width;
- propagation from the selected `K` rows to the full target family;
- an all-target distance-fibre theorem below `1/9-epsilon`;
- outer stability with subpower loss.

One precision must stay explicit: the fibre implication also needs the same
actual occurrence domain to retain size `t^(28/9-o(1))` (or an equivalent
weighted mass).  An upper capacity bound `|T_all|<=qU` plus a fibre bound alone
does not yield a label lower bound.  This requirement is naturally part of
the stated propagation dependency, but must be written into any future M10
theorem.

M1083R3-01 remains only an unproved survivor.  This audit supplies no paired
positivity compression theorem and no bridge to the public exponent.

The checker imported no author computations, used exact symbolic/rational
arithmetic, and ran under 2 GiB and 120 seconds in 2.4 seconds.  No Lean was
used.  SHA-256:
`243b460e0630bc3a988896f237fb31fcc887ebe1b86bedd24f98f5c902806a34`.
