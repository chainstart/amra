# Ruled-transfer stability: dyadic extraction and the exact tensor barrier

Date: 2026-07-30

## 1. Outcome

At the critical normalization
\[
M=t,\qquad Q=t^3,\qquad S=MQ=t^4,\qquad
D\le t^{3+o(1)},
\tag{1}
\]
the cross-plane distance codegree satisfies
\[
\mathfrak C_{\rm plane}\ge t^{13-o(1)}.
\tag{2}
\]

This note tests whether dyadic pigeonholing, Balog--Szemerédi--Gowers
(BSG), or dependent random choice (DRC) can by themselves turn (2)
into a common vertical Cartesian substructure.

The answer is negative at the level of the plane-pair/distance
representation tensor:

\[
\boxed{
\text{the tensor data permit a critical one-scale random model with }
D=t^3,\ \mathfrak C_{\rm plane}=t^{13+o(1)},
\text{ but no polynomial two-sided common-label rectangle}.
}
\tag{3}
\]

The obstruction remains after resolving each tensor cell into endpoint
pairs by a random balanced partition.  Rotation marginals can also be
realized on a disjoint abstract reservoir with the correct exponents.

This is an exact **methodological no-go**, not a Euclidean
counterexample.  The random tensor is not asserted to come from
distances in \(\mathbb R^3\).  Consequently, any successful stability
theorem must use the coefficients of the Euclidean four-plane
quadratic, not only dyadic multiplicities, equality of distance labels,
and the inherited rotation marginals.

## 2. The representation tensor

Let
\[
\mathcal P
=\{(\alpha,\beta):
\text{retained ordered source-plane pairs}\},
\qquad |\mathcal P|=t^{2+o(1)},
\]
and let \(\mathcal D\) be the set of squared-distance labels, with
\[
|\mathcal D|\le t^{3+o(1)}.
\]
Write
\[
W_{e,d}=R_{\alpha,\beta}(d),
\qquad e=(\alpha,\beta)\in\mathcal P.
\tag{4}
\]
Then, suppressing \(t^{o(1)}\) factors,
\[
\sum_dW_{e,d}=Q^2=t^6,\qquad
\sum_{e,d}W_{e,d}=M^2Q^2=t^8.
\tag{5}
\]
Lemma 2 of `ANGULAR_STARVATION_BRANCH_ATTACK.md` gives
\[
W_{e,d}\ll Q^{4/3}+Q=t^{4+o(1)}.
\tag{6}
\]
The two energies are
\[
\mathfrak E_{\rm all}
=\sum_d\left(\sum_eW_{e,d}\right)^2,
\qquad
\mathfrak E_{\rm diag}
=\sum_{e,d}W_{e,d}^2,
\tag{7}
\]
and
\[
\mathfrak C_{\rm plane}
=\mathfrak E_{\rm all}-\mathfrak E_{\rm diag}.
\tag{8}
\]

Notice what (4) forgets: the radial and height coordinates of the two
endpoints, the coefficient
\(\cos(\alpha-\beta)\), and which endpoint pairs realize two labels.
Those are precisely the data needed to recognize a ruled Cartesian
model.

## 3. Complete dyadic ledger

Split the nonzero entries of \(W\) into dyadic ranges
\[
W_{e,d}\asymp t^\omega.
\]
There are only \(O(\log t)\) ranges.  A range carrying
\(t^{8-o(1)}\) representation mass has
\[
3-o(1)\le\omega\le4+o(1).
\tag{9}
\]
The upper bound follows from (6).  For the lower bound, a range below
\(t^{3-o(1)}\) has at most
\(|\mathcal P||\mathcal D|=t^{5+o(1)}\) cells and therefore cannot
carry \(t^{8-o(1)}\) mass.

For a regularized level of weight \(t^\omega\), all exponent losses are:
\[
\begin{array}{c|c}
\text{quantity}&\text{\(t\)-exponent}\\ \hline
\text{support edges}&8-\omega\\
\text{average degree on plane-pair side}&6-\omega\\
\text{average degree on label side}&5-\omega\\
\text{total representation mass}&8\\
\text{aggregate energy under uniform label degrees}&13\\
\text{diagonal energy}&8+\omega.
\end{array}
\tag{10}
\]
Indeed,
\[
t^{8-\omega}\cdot t^\omega=t^8,
\]
and the average number of plane pairs supporting one label is
\[
t^{8-\omega}/t^3=t^{5-\omega}.
\]
Thus its total representation multiplicity is \(t^5\), independent of
\(\omega\), and
\[
t^3(t^5)^2=t^{13}.                                  \tag{11}
\]

At the most concentrated allowed scale \(\omega=4\),
\[
|E|=t^4,\quad
\deg_{\mathcal P}=t^2,\quad
\deg_{\mathcal D}=t,\quad
\mathfrak E_{\rm diag}=t^{12}.                      \tag{12}
\]
This single level already realizes every critical exponent.  Therefore
an extraction theorem must handle (12); distributing energy over
several dyadic levels cannot be assumed.

## 4. DRC stops at one-dimensional reuse

Model the support at scale \(t^\omega\) by a bipartite graph with
\[
|\mathcal P|=t^2,\qquad |\mathcal D|=t^3,
\qquad p=t^{3-\omega}.
\tag{13}
\]
For extraction purposes, \(\mathcal P\) in this section means the
independent unordered plane-pair types.  Copying a type to its reverse
orientation is compulsory but supplies no new plane coefficients.
The degrees in (10) are exactly the random-graph expectations.
For \(h\) distinct plane-pair vertices, the expected common label count
is
\[
t^3p^h=t^{\,3+h(3-\omega)}.                         \tag{14}
\]
At the critical concentrated scale \(\omega=4\), the ledger is
\[
\begin{array}{c|cccc}
h&1&2&3&4\\ \hline
\text{common-label exponent}&2&1&0&-1.
\end{array}
\tag{15}
\]

Thus DRC can force either:

- one distance label reused by about \(t\) plane pairs; or
- about \(t\) labels common to two plane pairs.

It cannot force both sides of a common-label rectangle to have positive
power size.  In particular, it cannot coordinate a growing family of
independent plane pairs on a growing common label set.

A plane pair and its reverse share their entire support of \(t^2\)
labels, but this tautological duplication still represents only one
independent unordered coefficient type and does not improve the
extraction.

This is not just a weakness of the expectation calculation.  To retain
the mandatory symmetry
\[
R_{\alpha,\beta}(d)=R_{\beta,\alpha}(d),
\]
first group reverse orientations into independent unordered plane-pair
types.  On these \(\Theta(t^2)\) types, take the bipartite random graph
with edge probability \(p=t^{-1}\), and copy each support row to its
reverse orientation.  Chernoff bounds give every unordered plane-pair
degree \(t^{2+o(1)}\) and every label degree \(t^{1+o(1)}\), up to the
irrelevant factor two from orientations.  For a fixed four-tuple of
independent unordered plane-pair types, its common-neighbour count has
mean \(t^{-1}\).  For any fixed \(K>8\),
\[
\Pr(\text{that four-tuple has at least \(K\) common labels})
\le t^{-K+o(1)}.
\]
There are at most \(t^8\) such four-tuples, so with positive probability
every four independent unordered plane-pair types have fewer than \(K\)
common labels.  A tuple containing a pair and its reverse is deliberately
excluded from this assertion because those two rows must coincide.

Assign weight \(t^4\) to every support edge.  Up to harmless
regularization and integer rounding,
\[
\begin{aligned}
\text{row mass}&=t^2t^4=t^6,\\
\text{total mass}&=t^2t^2t^4=t^8,\\
\mathfrak E_{\rm diag}&=t^4t^8=t^{12},\\
\sum_eW_{e,d}&=t\cdot t^4=t^5,\\
\mathfrak E_{\rm all}&=t^3(t^5)^2=t^{13}.
\end{aligned}                                       \tag{16}
\]
Consequently
\[
\mathfrak C_{\rm plane}=t^{13+o(1)}
\]
while the desired multi-plane common-label core is absent.

The verifier uses both an exact-left-degree exponent model and a
symmetrized finite version: every unordered plane pair chooses \(t^2\)
of \(t^3\) labels, and its reverse receives the identical support.
Every chosen cell receives weight \(t^4\).  The resulting ordered tensor
has row mass \(t^6\), total mass \(\Theta(t^8)\), diagonal energy
\(\Theta(t^{12})\), and aggregate energy \(\Omega(t^{13})\) by
Cauchy--Schwarz.

## 5. Resolving tensor cells does not recover endpoint rectangles

One could try DRC a second time inside a rich cell
\[
R_{\alpha,\beta}(d)\asymp t^4.
\]
The cell is a bipartite graph between two point sets of size
\[
Q=t^3
\]
and has density
\[
\frac{t^4}{Q^2}=t^{-2}.                             \tag{17}
\]
For \(h\) source endpoints, a random graph of this density has expected
common target count
\[
Q(t^{-2})^h=t^{3-2h}.                               \tag{18}
\]
Already at \(h=2\), the exponent is \(-1\).

There is a simultaneous balanced model.  For each supported unordered
plane pair, partition its \(Q^2=t^6\) ordered endpoint pairs randomly
into \(t^2\) supported labels, exactly \(t^4\) pairs per label, and use
the transposed partition for the reverse orientation.  A fixed label
class has the density (17).  A standard hypergeometric tail bound and a
union bound over
\[
t^2\ \text{plane pairs}\times
t^2\ \text{labels}\times
Q^2=t^{10}
\]
choices show that, for a sufficiently large absolute \(K\), no two
source endpoints have \(K\) common targets in one label class.

This endpoint model retains every entry \(W_{e,d}\) and hence all
energies in (16), while destroying monochromatic endpoint rectangles.
It still is not a Euclidean realization: independent balanced
partitions generally violate the quadratic distance equations.  Its
purpose is to prove that endpoint coherence cannot be reconstructed
from the multiplicity tensor.

## 6. Why label BSG does not cross the gap

BSG requires additive energy such as
\[
|\{a_1+a_2=a_3+a_4\}|.
\]
The statistic in (8) only counts equality of already formed labels:
\[
d(p,q)=d(r,s).
\tag{19}
\]
The label set has no inherited group law compatible with all plane
pairs.  Relabelling \(\mathcal D\) by an arbitrary permutation preserves
(4)--(8), the dyadic levels, and every DRC conclusion, while destroying
any artificial additive pattern among the labels.

Embedding the labels arbitrarily into an abelian group and applying BSG
therefore only rediscovers that the multiset is supported on \(D=t^3\)
values.  It cannot lift a structured label subset back to compatible
radial parameters and heights.  In the model (16), each typical label
has \(t^5\) endpoint-pair representations, but those representations are
independently partitioned across the plane pairs.  The lift loses all
coefficient alignment.

Thus a legitimate BSG step would first need a common decomposition
\[
d=A_{\alpha,\beta}(a,b)+H(z,w)
\tag{20}
\]
on many plane pairs, with the same \(H\) and quantitatively controlled
variation of \(A_{\alpha,\beta}\).  Establishing (20) is already the
ruled-stability theorem; it is not a consequence of label energy alone.

## 7. Rotation marginals do not repair tensor-only extraction

The split reservoir from `SYNC_EXTRACTION_DRC_ATTACK.md` has the exact
critical ledger
\[
N=t^5,\qquad M=t,\qquad q_\alpha=t^3.
\]
Take \(t^2(t-1)\) rotation fibres of size \(t^2\).  Together with the
\(t^4\) source points, their total mass is
\[
t^2(t-1)t^2+t^4=t^5.
\]
For active index \(1\le j\le t\),
\[
r_{\alpha_j}
=t^2(t-1)(t^2-2j)=t^{5-o(1)},
\tag{21}
\]
and the normalized rotation codegree has scale
\[
\frac{t^2(t-1)}{t^2}
\left(\sum_{j=1}^t(t^2-2j)\right)^2
=t^{7-o(1)}.                                       \tag{22}
\]

The source endpoint tensor in Sections 4--5 and this reservoir can be
made disjoint.  At the level of abstract distance labels, all remaining
pairs can also be coloured with \(t^3\) labels.  Hence the cardinality
\(D=t^3\), source tensor, and rotation marginals are mutually consistent
as combinatorial data.

They are not known to be simultaneously Euclidean.  Generic reservoir
coordinates would create many additional distances.  This is exactly
why the no-go is limited to arguments that do not use the Euclidean
coupling between source and reservoir.

## 8. Exact barrier and the missing geometric input

The attempted extraction stops at
\[
\boxed{
\begin{aligned}
&\text{one label on }t^{1+o(1)}\text{ plane pairs},\quad\text{or}\\
&t^{1+o(1)}\text{ labels on two plane pairs},\quad\text{but not}\\
&t^\eta\text{ labels on }t^\eta\text{ independent plane pairs}
\quad(\eta>0).
\end{aligned}}
\tag{23}
\]
Inside one rich tensor cell it stops even earlier: two source endpoints
need not have a common target.

Therefore a successful next lemma must be explicitly Euclidean.  A
minimal useful form is:

> **Quadratic coefficient stability lemma.**  Under (1)--(2), either
> \(D\ge t^{3+\eta}\), or there are \(t^\eta\) retained plane pairs and
> subsets containing \(t^{\eta}Q^{1-o(1)}\) endpoint incidences on which
> the distance equations admit a common decomposition
> \[
> (a-b)^2+(j a-k b)^2+(z-w)^2,
> \]
> after bounded-complexity affine changes of the signed radial
> coordinates.

The exact exponents in a future proof may differ, but both a positive
power of plane-pair coherence and a positive power of endpoint mass are
essential.  Once such a decomposition is obtained, the divisor argument
in equations (32a)--(32c) of
`CROSS_PLANE_TO_RADIUS_TRANSFER_ATTACK.md` supplies distance expansion.

Possible geometric inputs not seen by the tensor are:

1. polynomial partitioning for the four-plane quadratic with its ruled
   components retained rather than discarded;
2. an inverse theorem for simultaneous near-extremizers of the
   two-degree-of-freedom circle bound;
3. entropy decrement on the actual radial products
   \(xy\cos(\alpha-\beta)\) and squared-height differences; or
4. incompatibility of a recovered ruled coefficient family with the
   near-maximal rotation reservoir.

## 9. Exponent ledger

| quantity | \(t\)-exponent |
|---|---:|
| active planes \(M\) | \(1\) |
| source points per plane \(Q\) | \(3\) |
| source mass \(S\) | \(4\) |
| distance labels \(D\) | \(3\) |
| plane-pair vertices | \(2\) |
| critical cell weight | \(4\) |
| support edges | \(4\) |
| labels per plane pair | \(2\) |
| plane pairs per label | \(1\) |
| total representation mass | \(8\) |
| aggregate energy | \(13\) |
| diagonal energy | \(12\) |
| cross-plane codegree | \(13\) |
| common labels of two plane pairs | \(1\) |
| common labels of three plane pairs | \(0\) |
| common labels of four plane pairs | none at power scale |
| one-label endpoint density | \(-2\) |
| common targets of one source endpoint | \(1\) |
| common targets of two source endpoints | none at power scale |
| rotation count per angle | \(5\) |
| normalized rotation codegree | \(7\) |

## 10. Claim boundary

### Proved

- the complete dyadic exponent ledger (9)--(12);
- the DRC common-neighbour loss (14)--(15);
- existence, by the probabilistic method, of tensor supports satisfying
  all critical source-energy exponents but no polynomial two-sided
  common-label rectangle;
- existence of balanced endpoint partitions with the same tensor and no
  large monochromatic \(K_{2,s}\);
- compatibility of these abstract source data with all inherited
  rotation marginal exponents.

### Not proved

- Euclidean realizability of the random tensor;
- a Euclidean point configuration with
  \(D=t^{3+o(1)}\) and all critical rotation marginals;
- extraction of a ruled Cartesian submodel from the actual four-plane
  quadratic;
- an unconditional improvement for Erdős problem #1083.

The precise no-go is therefore:
\[
\boxed{
\text{dyadic pigeonhole + tensor DRC + label BSG cannot prove ruled
stability without an additional Euclidean coefficient lemma.}
}
\]

## 11. Reproduction

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/erdos1083/geometric
pytest -q test_verify_ruled_stability_extraction.py
python3 verify_ruled_stability_extraction.py
```
