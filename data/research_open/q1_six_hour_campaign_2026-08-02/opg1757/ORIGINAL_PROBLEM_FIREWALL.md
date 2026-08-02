# Exact implication firewall: layer theorem versus OPG-1757

Date: 2026-08-02

## 1. Original claim

The repository's frozen model contract for OPG-1757 is:

> For every finite simple graph (G), every two distinct edges (e,f),
> and a forest chosen uniformly from all forests of (G),
> \(\Pr(e\in F\mid f\in F)\le\Pr(e\in F)\).

Equivalently, if (\mathcal F,\mathcal F_e,\mathcal F_f,
\mathcal F_{ef}) denote the corresponding forest sets, the target is

\[
|\mathcal F_e|\,|\mathcal F_f|
-|\mathcal F|\,|\mathcal F_{ef}|\ge0
\tag{1}
\]

for every finite simple host and every distinct edge pair.

## 2. What the new theorem proves

The eighth-root theorem works in the complete-split host

\[
S_{s,t}=K_s\vee\overline{K_t},
\]

with two disjoint core edges (e=01,f=23).  After assigning one common
activity (\alpha) to core edges and one common activity (\beta) to
spokes, take the normalized Rayleigh difference

\[
\Delta=Z_eZ_f-ZZ_{ef}.
\]

It controls only the coefficient of (\alpha^2), expanded further in
the pooled page-Newton basis

\[
P_s^{(2)}(\beta,t)=\sum_n\binom tn B_n(s,\beta).
\]

For deficits (q=2s-5-n\) satisfying

\[
0\le q\le s^{1/8}/2^{24},
\]

every coefficient in the natural beta support of that particular
(B_n) is strictly positive.

Thus the proved implication is

\[
\text{complete-split + disjoint core pair + alpha-squared + deep pooled
window}
\Longrightarrow
\text{coefficientwise-positive contribution}.
\tag{2}
\]

## 3. What does not follow

Equation (2) does **not** imply (1), for four independent reasons.

1. **Host gap:** OPG-1757 quantifies over every finite simple graph;
   (2) uses only complete-split graphs.
2. **Edge-orbit gap:** a complete-split graph has seven relevant edge-pair
   orbits for (s\ge4); (2) uses only two disjoint core edges.
3. **Core-degree gap:** the full Rayleigh difference contains all
   powers of (\alpha); (2) controls only the (\alpha^2) coefficient.
4. **Pooled-depth gap:** even inside that coefficient, (2) covers only
   (2s-5-n\le s^{1/8}/2^{24}), not all (2\le n\le2s-5).

In particular, summing the proved positive sector cannot establish the
sign of the omitted sectors.  The new result is a rigorous unbounded
subtheorem and a plausible paper component, but the original arbitrary-
host negative-association conjecture remains `OPEN`.

## 4. Exact next closure targets

Within the current route, successively stronger sufficient milestones
are:

1. prove all active base-four Newton coefficients of every
   (C_{q,r}), which would close every pooled depth of this one
   alpha-squared/disjoint-core layer;
2. close the remaining alpha-degrees and six edge-pair orbits for the
   complete-split family;
3. prove a host operation or structural reduction carrying the Rayleigh
   inequality from controlled cores to arbitrary finite graphs.

Only completion of all required host and edge-pair quantifiers would
settle OPG-1757 itself.
