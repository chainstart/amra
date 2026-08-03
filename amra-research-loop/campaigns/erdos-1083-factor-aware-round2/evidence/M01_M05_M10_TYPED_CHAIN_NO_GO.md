# M01 -> M05 -> M10: typed-chain deepening

## Verdict

The proposed chain cannot currently be compressed into a valid decisive
lemma.  Its first bridge is ill-typed.  This is a scoped no-go for the chain
as written, not a counterexample to every possible factor-aware argument.

## Exact type audit

On the inherited almost-full exact hub, the simultaneous normal form is

\[
 F_j=GR_j,\qquad P_{A_0}=GB,\qquad B=R_jQ_j,
 \qquad P_{A_j}=F_0Q_j.
\]

The common-source scalar-copy identity is

\[
 F_j=P_{\lambda_jX}.
\]

Thus the two objects have different types and roles:

- `F_j` is the positive source mask obtained by scaling the one common set
  `X` by `lambda_j`;
- `Q_j` is a generally signed element of the ambient Laurent group ring,
  defined as a complementary quotient.

M01's proposed labelled moments concern the factor occurrences and
coefficients of `Q_j`.  M05 instead invokes coefficient maps
`Q_j(lambda_j X)` and their Jacobian.  The exact-block data provide neither a
one-parameter family `Q_j(T)` nor an evaluation/substitution operation taking
`T=lambda_j X`.  Consequently `Q_j(lambda_j X)` and its Jacobian are not
defined by the hypotheses.  A rank/codimension conclusion cannot be inferred
from M01 until an additional typed parametrization is constructed and proved
compatible with both positive products.

This is not merely missing notation.  Replacing `Q_j` by `F_j` repairs the
type, but then the inherited heavy-factor theorem already supplies the needed
geometric consequence directly: `G|F_j` gives a nonzero Newton direction `h`,
`h=lambda_j w_j`, and hence

\[
 z_j={h\over2\rho w_j},\qquad
 \rho^2+\tau_0+{h^2\over4\rho^2w_j^2}+{h\over w_j}X.
\]

So the repaired M01-to-M05 bridge is redundant rather than an unproved
Jacobian gain.  The surviving decisive problem is M10: turn this already
proved reciprocal chart into sufficiently many *actual distinct distance
labels*, with controlled collisions and exceptional loci.

## Exponent ledger

The inherited heavy-factor pigeonhole loses only `log_2 U=t^o(1)` and a
same-sign selection loses only a factor two.  Therefore

\[
 K=t^{5/9-o(1)}\longmapsto K/\log_2U
 \longmapsto K/(2\log_2U)=t^{5/9-o(1)}.
\]

Neither step supplies a positive power gain.  Distinct chart parameters yield
only `K-1=t^(5/9-o(1))` target--target labels by fixing one endpoint.  Reaching
more than `t^(3+epsilon)` labels therefore requires an amplification exponent
strictly exceeding `22/9`.  Even the formal product of all frozen native
counts has exponent

\[
 {5\over9}+{7\over9}+{5\over6}+{13\over18}={26\over9},
\]

leaving `1/9+epsilon` beyond that bookkeeping product.  This last comparison
is a ledger warning, not an incidence upper bound: it says M10 must prove real
label expansion/multiplicity control rather than rename available tuples.

## Exact scope

The no-go rules out only the implication

```text
factor-labelled moments of the signed Q_j
  -> Jacobian of Q_j(lambda_j X)
```

under the presently frozen normal form.  It does not rule out:

1. a newly defined algebraic family `Q(T)` with `Q(lambda_j)=Q_j` and
   controlled degree/fibres;
2. a Jacobian built from the correctly typed source masks `F_j`, provided it
   proves information beyond the already known Newton-direction chart; or
3. a direct M10 distance-label theorem on the inherited reciprocal chart.

No improvement of the public `3/5` exponent follows.
