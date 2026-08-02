# Independent audit of the zero-star colour-defect mass ledger

Date: 2026-08-02

Status: PASS

Audited source:
`../erdos1083/ERDOS809_ZERO_STAR_DEFECT_MASS_LEDGER.md`.

## 1. Independent reconstruction

Fix a zero-star with centre \(b\), distinct leaves \(L\), and outer
endpoint sets \(Y_\gamma\).  For each colour put

\[
 t_\gamma=|Y_\gamma|,
 \qquad
 k_\gamma=
 |\{c\in L:b,c\in Y_\gamma\}|.
\]

If \(k_\gamma>0\), the \(k_\gamma+1\) distinct vertices consisting of
\(b\) and its supported leaves all lie in \(Y_\gamma\).  Hence

\[
 (t_\gamma-1)_+\ge k_\gamma.
\]

The same inequality is trivial when \(k_\gamma=0\).  Summing directly
from the definition \(D_B=\sum_\gamma(t_\gamma-1)_+\), and then
double-counting supported leaf--colour incidences, gives

\[
 D_B\ge\sum_\gamma k_\gamma
 =\sum_{c\in L}|\{\gamma:b,c\in Y_\gamma\}|
 =H.
\]

No disjointness of different leaf supports was used.  The exact slack
is independently recovered as

\[
 D_B-H=
 \sum_{k_\gamma>0}(t_\gamma-1-k_\gamma)
 +\sum_{k_\gamma=0}(t_\gamma-1)_+\ge0.
\]

For a star selected from an inclusion-maximal repeated-zero matching,
each selected pair has multiplicity \(h_c\ge2\), so \(H\ge2\ell\).
The inherited concentration inequality

\[
 \frac{E_0}{4f}\le H-\ell
\]

and \(H\le D_B\) then give

\[
 2\ell\le H\le D_B,
 \qquad
 E_0\le4f(D_B-\ell).
\]

The quantifiers are valid for both same- and opposite-neighbourhood
selected stars.  The only matching-specific statements are the last
two consequences; \(H\le D_B\) itself holds for every zero-star.

## 2. Computational guard

The separate verifier passed all 129,510 enumerated support systems,
including 6,232 equality systems, and all 4 focused regression tests
passed.  This finite check tests overlap, unused colours, and extra
outer endpoints.  It is only a guard; the argument above is
all-parameter.

## 3. Verdict and boundary

Verdict: PASS.  The theorem is an exact new global coupling between
selected-star mass and the already present defect \(D_B\).  It does not
bound \(fD_B\), eliminate either coherent-star type, close the
maximum-witness feasibility region, or solve Erdős #809.
