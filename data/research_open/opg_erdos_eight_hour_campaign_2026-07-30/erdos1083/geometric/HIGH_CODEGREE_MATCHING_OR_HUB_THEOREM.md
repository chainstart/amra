# Erdős #1083: high plane-codegree matching-or-hub theorem

Date: 2026-07-30

## 0. Outcome

The critical cross-plane codegree does force an unconditional
structure, although not yet a ruled Cartesian chart.  At the
normalization
\[
 |\mathcal A|=t^{1+o(1)},\qquad
 |\mathcal D|\leq t^{3+o(1)},\qquad
 W_{e,d}\in\mathbb Z_{\geq0},\qquad
 W_{e,d}\leq t^{4+o(1)},
\tag{1}
\]
where \(e\) is an unordered pair of axial planes and \(d\) is a
squared-distance label, assume
\[
 \mathfrak C_{\rm plane}
 =
 \sum_d\left\{
 \left(\sum_eW_{e,d}\right)^2-\sum_eW_{e,d}^2
 \right\}
 \geq t^{13-o(1)}.
\tag{2}
\]
More generally, for every fixed \(0<\kappa<1\), one of the following
alternatives holds:

\[
\boxed{
\begin{array}{ll}
{\rm(M_\kappa)}&
\text{at least }t^{1-o(1)}\text{ labels each contain a rich matching
of size }t^{\kappa-o(1)};\\[2mm]
{\rm(H_\kappa)}&
\text{one plane is a hub for at least }t^{2-2\kappa-o(1)}
\text{ labels, with rich mass }t^{5-\kappa-o(1)}
\text{ per label.}
\end{array}}
\tag{2a}
\]

The balanced choice \(\kappa=1/2\) gives the following especially
simple alternatives.

### Matching branch

There are at least \(t^{1-o(1)}\) labels \(d\) such that the rich
support graph of \(d\) contains a matching of size
\(t^{1/2-o(1)}\).  Every edge in the matching satisfies
\[
 W_{e,d}\geq t^{3-o(1)}.
\tag{3}
\]

### Hub branch

There is one axial plane \(\alpha\) and at least \(t^{1-o(1)}\)
labels \(d\) for which
\[
 \sum_{\substack{\beta\ne\alpha\\
                   W_{\{\alpha,\beta\},d}\geq t^{3-o(1)}}}
 W_{\{\alpha,\beta\},d}
 \geq t^{9/2-o(1)}.
\tag{4}
\]

Thus high codegree forces either many coefficient-separated
plane-pair representations or a genuinely low-dimensional
single-plane concentration.  This conclusion uses no Euclidean
inverse theorem.

The theorem is sharp at the abstract tensor level.  Section 4 gives a
deterministic finite-field tensor with the complete critical ledger,
with a linear-size matching for almost every label, but with no
\(K_{3,2}\) common-label rectangle.  Hence the matching alternative
alone cannot improve the \(3/5\) exponent without using the Euclidean
quadratic.

## 1. A finite weighted-graph extraction lemma

Let \(G\) be a simple graph on \(n\) vertices with nonnegative edge
weights \(w_e\leq U\), and let
\[
 T=\sum_e w_e.
\]
Call an edge rich when
\[
 w_e\geq \frac{T}{4n^2}.
\tag{5}
\]
The nonrich edges carry total weight less than \(T/4\), so rich edges
carry at least \(3T/4\).

Fix an integer \(k\geq1\).  Then either:

1. the rich graph contains a matching of size \(k\); or
2. some vertex has rich weighted degree at least
   \[
   \frac{3T}{8k}.
   \tag{6}
   \]

Indeed, take a maximal rich matching.  If it has fewer than \(k\)
edges, its fewer than \(2k\) endpoints cover every rich edge.  The sum
of the rich weighted degrees over that cover is at least the rich edge
mass, so one endpoint has weighted degree at least \(3T/(8k)\).

There is also an automatic matching bound.  If the maximum rich
matching has size \(m\), its \(2m\) endpoints cover every rich edge.
Since each vertex is incident to fewer than \(n\) edges,
\[
 \#E_{\rm rich}\leq2mn.
\]
On the other hand,
\[
 \#E_{\rm rich}\geq\frac{3T}{4U}.
\]
Consequently
\[
 \boxed{m\geq\frac{3T}{8Un}.}
\tag{7}
\]

## 2. Extracting a common label scale

Put
\[
 T_d=\sum_eW_{e,d}.
\tag{8}
\]
Equation (2) implies
\[
 \sum_dT_d^2\geq t^{13-o(1)}.
\tag{9}
\]
There are only \(O(\log t)\) dyadic ranges for \(T_d\), because
\[
 T_d\leq {|\mathcal A|\choose2}\max_eW_{e,d}
 \leq t^{6+o(1)}.
\tag{10}
\]
Hence some dyadic range contains \(L\) labels with
\[
 T\leq T_d<2T,\qquad
 LT^2\geq t^{13-o(1)}.
\tag{11}
\]
Write \(T=t^{\lambda+o(1)}\).  Since \(L\leq t^{3+o(1)}\),
(11) gives \(\lambda\geq5-o(1)\); equation (10) gives
\(\lambda\leq6+o(1)\).  Moreover,
\[
 L\geq t^{13-2\lambda-o(1)}.
\tag{12}
\]

For every label in this range, declare an edge rich using (5), with
\(n=|\mathcal A|=t^{1+o(1)}\).  Its threshold is
\[
 \frac{T_d}{4n^2}
 =t^{\lambda-2-o(1)}
 \geq t^{3-o(1)}.
\tag{13}
\]

## 3. Proof of the dichotomy

For the parameterized statement, take
\[
 k=t^{\kappa-o(1)}.
\tag{14}
\]

If \(\lambda\geq5+\kappa-o(1)\), (7) and (1) give, for every label in
the selected range,
\[
 m_d\geq
 \frac{T_d}{t^{5+o(1)}}
 \geq t^{\kappa-o(1)}.
\tag{15}
\]
Also (12), using \(\lambda\leq6+o(1)\), gives
\[
 L\geq t^{1-o(1)}.
\]
This is the matching branch.

Suppose now that \(\lambda<5+\kappa+o(1)\).  If at least half of the
selected labels satisfy the first alternative of the weighted-graph
lemma, then
\[
 L/2\geq t^{3-2\kappa-o(1)}
\]
such labels exist.  Since \(\kappa<1\), this is at least
\(t^{1-o(1)}\), and proves \({\rm(M_\kappa)}\).

Otherwise, more than \(L/2\) labels have a hub vertex whose rich
weighted degree is, by (6),
\[
 \gg \frac{T}{t^{\kappa+o(1)}}
 \geq t^{5-\kappa-o(1)}.
\tag{16}
\]
Choose one such hub for each label.  Pigeonholing over
\(|\mathcal A|=t^{1+o(1)}\) planes produces one plane that is the hub
for at least
\[
 \frac{L}{2|\mathcal A|}
 \geq
 t^{12-2\lambda-o(1)}
 \geq t^{2-2\kappa-o(1)}
\tag{17}
\]
labels.  Equations (13) and (16) prove
\({\rm(H_\kappa)}\), and hence (2a).

Specializing \(\kappa=1/2\) gives (3)--(4).

## 4. Deterministic tensor showing the remaining barrier

Let \(q\) be an odd prime.  Take two disjoint plane families
\[
 \mathcal L=\{L_u:u\in\mathbb F_q\},\qquad
 \mathcal R=\{R_v:v\in\mathbb F_q\}.
\tag{18}
\]
Use the \(q^2\) cross-family unordered plane pairs
\[
 e_{u,v}=\{L_u,R_v\}.
\]
The \(q^3\) labels are quadratic polynomials
\[
 f_{a,b,c}(u)=au^2+bu+c,
\qquad(a,b,c)\in\mathbb F_q^3.
\tag{19}
\]
Define
\[
 W_{e_{u,v},f_{a,b,c}}
 =
 \begin{cases}
 q^4,&v=f_{a,b,c}(u),\\
 0,&\text{otherwise}.
 \end{cases}
\tag{20}
\]
If ordered plane pairs are required, copy each row to the reverse
orientation.  This changes only absolute factors.

Every label supports exactly \(q\) plane pairs, and every plane pair
supports exactly \(q^2\) labels.  Therefore
\[
\begin{array}{c|c}
\text{quantity}&\text{exact value}\\ \hline
\text{support cells}&q^4\\
\text{cell weight}&q^4\\
\text{row mass}&q^6\\
\text{label mass}&q^5\\
\text{total mass}&q^8\\
\sum_{e,d}W_{e,d}^2&q^{12}\\
\sum_d(\sum_eW_{e,d})^2&q^{13}\\
\mathfrak C_{\rm plane}&q^{13}-q^{12}.
\end{array}
\tag{21}
\]

For every nonconstant \(f\), each value has at most two preimages.
The graph
\[
 \{e_{u,f(u)}:u\in\mathbb F_q\}
\]
therefore contains a matching of size at least
\(\lceil q/2\rceil\).  This holds for \(q^3-q\) of the \(q^3\)
labels, so the tensor strongly realizes the matching branch.

The common-neighbour ledger is also exact.  One row lies on \(q^2\)
labels.  Two compatible rows with distinct left coordinates lie on
exactly \(q\) labels, because two independent evaluations leave one
free quadratic coefficient.  Three compatible rows with distinct
left coordinates lie on exactly one label.

Nevertheless, three distinct plane-pair rows have at most one common
label.  If two rows use the same \(L_u\) but different \(R_v\), their
common support is empty.  Otherwise, three common rows give three
distinct interpolation nodes \(u\).  Two quadratic polynomials
agreeing at those nodes are identical.  Thus
\[
\boxed{\text{the support tensor contains no }K_{3,2}.}
\tag{22}
\]
In particular it contains no growing two-sided common-label
rectangle, despite exact saturation of every exponent in (21).

This is an abstract incidence tensor, not a Euclidean distance
configuration.  Its role is precise: the new matching-or-hub theorem
is the strongest conclusion available from high codegree plus the
cell cap alone.  Turning either branch into distance expansion still
requires the four-plane Euclidean quadratic.

## 5. Claim boundary

### Proved

- the all-weight finite extraction lemma (5)--(7);
- the unconditional critical matching-or-hub dichotomy (3)--(4);
- a deterministic, symmetric-after-copying tensor with exact critical
  mass and energy ledger;
- exact absence of \(K_{3,2}\) in that tensor.

### Not proved

- Euclidean realizability of the finite-field tensor;
- a ruled Cartesian chart in the matching branch;
- an unconditional exponent improvement for Erdős #1083.

The useful new geometric targets are now branch-specific:

1. show that \(t^{1/2-o(1)}\) coefficient-separated rich plane pairs
   for many common distance labels force expansion; or
2. show that the single-plane hub in (4) forces a common radial/height
   chart or already creates more than \(t^{3+o(1)}\) distances.

## 6. Reproduction

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/erdos1083/geometric
pytest -q test_verify_high_codegree_matching_or_hub.py
python3 verify_high_codegree_matching_or_hub.py
```
