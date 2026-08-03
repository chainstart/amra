# Survivor deepening: normalized quotient family and actual-pair ledger

## A legal quotient family, with its exact boundary

Work in the Laurent UFD and factor the fixed quotient host, with occurrences
listed separately,

`B = u_B product_(nu=1)^D H_nu`.

For each divisor quotient `Q_j | B`, choose a representative normalized up to
a Laurent unit.  Its factor multiset is a submultiset `I_j` of the displayed
occurrences.  Then

`mathcal Q(y)=product_nu ((1-y_nu)+y_nu H_nu)`

is a well-defined polynomial with Laurent-polynomial coefficients and

`mathcal Q(1_(I_j)) = Q_j^norm`.

The discarded associate unit (sign/monomial translation) must be recorded as
a separate row parameter before coefficient moments or positive products are
reconstructed.  Thus this is a legal host for normalized factor-labelled M01
data, not yet a family of the original `Q_j` with all carrier positions.

The host gives no useful complexity bound by itself.  With `D` independent
formal factor occurrences it has total degree `D` and all `2^D` Boolean
specializations, despite coordinate degree one.  Likewise a coefficientwise
family in the scalar parameter `T` always exists through `K` samples by
Lagrange interpolation, but a delta coefficient sequence on `K` equally
spaced nodes has minimum degree `K-1`.  The actual exact-block samples might
have smaller degree; proving that is new mathematics, not a consequence of
interpolation.

The exact divisor-width map remains the only currently proved scalar bridge:
on a same-sign class, the divisor occurrence vector determines `b_j` and
`lambda_j=sigma(a+b_j)/D_X`.  This recovers the reciprocal chart but no
additional distance multiplicity bound.  M1083R3-01 therefore remains open
only for a factor-labelled invariant using paired positivity/common-X data
beyond normalized subset recovery, units and width.

## Correct actual-point incidence ledger

The geometry contains one common source set of `S` points and at most `qU`
targets `q_(i,tau)`.  The selected reciprocal hub contains `K` rows and hence
at most `KU` targets.  Therefore the relevant point-pair capacities are:

- source--all-target pairs: exponent `S+q+U=7/3`;
- pairs of selected chart targets: `2(K+U)=25/9`;
- selected-chart-target to all-target pairs:
  `K+U+q+U=53/18<3`;
- all target--target pairs: `2(q+U)=28/9`.

The formal quantity `K+2S+U+q=11/3` is not a point-pair domain.  A pair with
one source point carries one `X` index, not two.  This kills M1083R3-08 as
formulated.

Consequently a repaired M10 theorem cannot close by direct counting on the
selected chart.  It must transfer structural control from those `K` rows to
the full `qU` target set and prove that the maximum fibre, or an
energy-equivalent average fibre, of the actual target--target squared-distance
map has exponent strictly below

`28/9 - (3+epsilon) = 1/9-epsilon`.

The common-spectrum cells themselves remain contained in `V`, with
`|V|=SU=t^(29/18+o(1))`.  The capacity `26/9` is neither used nor accepted as
an exponent improvement.

## Scope

These are exact algebraic typing and incidence-capacity results.  They do not
prove the M01 compression theorem, the repaired all-target M10 fibre theorem,
outer stability, or any improvement of the public `3/5` exponent.
