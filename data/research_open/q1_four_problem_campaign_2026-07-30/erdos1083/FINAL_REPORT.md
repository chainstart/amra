# Erdős #1083 eight-hour line: final report

Date: 2026-07-30

## 1. Executive verdict

The primary target was not reached:
\[
\boxed{\text{no fixed }\delta>0\text{ is proved in }
f_3(N)\gg N^{3/5+\delta}.}
\]

The secondary structural target was reached.  The live
\(\kappa=2/9\) hub has been reduced to an explicit two-chart
synchronization alternative.  This is strictly stronger than the
previous single repeated-circle and aligned/concentric no-go
statements.

The strongest new finite-real theorem is
\[
\sum_\lambda E^+(T_\lambda,\lambda X)
\le
S\sum_\lambda|T_\lambda|
+R(R-1)S(S-1).
\]
It uses the fact that every nontrivial difference quadruple determines
at most one distinct dilation.

## 2. Endpoint consequence

If the exact \(2/9\) matching branch holds, at least
\(t^{1-o(1)}\) labels support rich plane-pair matchings of size
\(t^{2/9-o(1)}\).

If the hub branch holds, the audited scalar ledger forces one
fixed-\((A,\rho)\) bundle with
\[
(S,U,H,R,D)
\succeq
t^{(7/9,\,5/6,\,19/9,\,1,\,3)-o(1)}.
\]
Its circles have distinct centre heights and are therefore pairwise
nonaligned.  The global tangent-square reuse has the strict margin
\[
\frac{HU}{R^2S}\ge t^{1/6-o(1)}.
\]
The new energy theorem then forces aggregate row spectra of size
\[
t^{67/18-o(1)},
\]
far above the \(t^{3+o(1)}\) global distance budget.  Double counting
the resulting set overlap extracts two different-height rows with
\[
\boxed{
|\mathcal V_i\cap\mathcal V_j|
\ge t^{2/9-o(1)}.
}
\]

These are distinct shared labels, not merely repeated
representations.

The quadratic dependence on the centre-height difference also bounds
one label's row degree by \(2SR\).  Removing labels below half the
average row degree therefore gives:
\[
\boxed{
\text{at least }t^{35/18-o(1)}\text{ labels, each on }
t^{13/18-o(1)}\text{ nonaligned rows}.
}
\]
This many-label/many-row spectral graph is stronger than the
existence of one synchronized pair.

The pair conclusion is also abundant.  For every fixed
\(\varepsilon>0\), at least
\[
\boxed{t^{17/6-o(1)}}
\]
nonaligned row pairs share
\[
\boxed{t^{2/9-\varepsilon-o(1)}}
\]
labels each.

## 3. Why this is useful

The previous endpoint target asked for a general cross-height energy
saving over all \(H^2\) row pairs.  The new theorem replaces that
broad request with one concrete object:

- two nonaligned congruent rich circles;
- source richness \(t^{7/9-o(1)}\);
- target multiplicity \(t^{5/6-o(1)}\);
- one common rich anchor circle;
- a shared cross-spectrum of size \(t^{2/9-o(1)}\); and
- a \(t^{35/18}\)-label spectral graph of minimum retained degree
  \(t^{13/18}\); and
- \(t^{17/6-o(1)}\) synchronized row pairs at every
  \(t^{2/9-\varepsilon}\) overlap threshold; and
- all tangent-square rows contained in one \(t^{1+o(1)}\)-element
  universe.

A theorem excluding or classifying this pair would remove the exact
hub endpoint.  It would still have to be connected to the matching
branch to improve the global \(3/5\) exponent.

## 4. Verification

The exact verifier reports:

```text
schema: amra.erdos1083.multidilate-nonaligned.v1
small rational instances: 56
geometric formula records: 6
parabolic spectral graph: PASS
endpoint fractions: PASS
status: PASS
```

The new local tests return:

```text
6 passed
```

The focused suite including all direct inherited dependencies returns:

```text
24 passed
```

An independent written reconstruction found no missing factor, sign,
or endpoint inequality.

## 5. Publication assessment

This result is not yet a defensible standalone Q1 paper:

- the recognized global exponent is unchanged;
- the endpoint alternative is not eliminated;
- the finite-real energy inequality is elementary and has not
  received an exhaustive priority search; and
- the global critical-codegree reduction is still an explicit
  hypothesis in the self-contained formulation.

It is, however, a meaningful theorem-level addition to the existing
\(2/9\) inverse-structure package.  In a paper containing the full
critical reduction, fixed-\(A\) linearization, \(2/9\) hub exclusion,
and this exact endpoint dichotomy, it supplies a substantially sharper
final structural theorem than the previous strict
\(2/9-\varepsilon\) matching statement.

## 6. Next attack

The next local hub target is now precise:

\[
\boxed{
\sum_{z\ne z'}|\mathcal V_z\cap\mathcal V_{z'}|
\ll
t^{-\eta}
\frac{(\sum_z|\mathcal V_z|)^2}{D}
}
\]
uniformly over a small exponent neighbourhood of the endpoint, for
the extracted nonaligned network, unless it lies in a classified
affine-quadratic exceptional family.

For the exceptional family one must prove one of:

1. it violates the common selected-label service graph;
2. it forces a polynomial-height ruled chart already covered by the
   ruled-column escape theorem; or
3. it directly creates \(t^{3+\epsilon}\) distinct distances.

No weaker target should be advertised as closing the endpoint.

Mathialagan--Sheffer already classify one pair: our circles are in
their nonaligned, nonperpendicular case, giving only
\(t^{28/27-o(1)}\) source--source distances per pair at the forced
richness.  Their theorem neither aggregates numerical labels across
many circle pairs nor uses the perpendicular-axis target rows, so it
does not supply the displayed de-reuse saving.

Finally, this lemma would close only the hub branch.  A strict global
\(3/5\) improvement still needs a separate Euclidean theorem
converting the rich plane-pair matching branch into more than
\(t^{3+o(1)}\) distances.
