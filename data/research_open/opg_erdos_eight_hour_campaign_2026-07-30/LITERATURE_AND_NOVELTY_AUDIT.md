# Literature and novelty audit: OPG-1757 Newton layers and square–translate energy

Date of audit: 2026-07-30

Search cutoff: 2026-07-30
Status: strict priority audit, not a novelty claim

## 1. Scope, method, and labels

This audit covers two groups of claims from the current campaign.

1. **OPG-1757 / uniform forests**
   - the complete-graph determinant behind the complete-split reduction;
   - the first, second, and third active base-four Newton layers;
   - the theorem that every fixed Newton depth is eventually positive.
2. **Erdős #1083 / additive expansion**
   - the divisor-energy bound for translates of the first squares;
   - the arbitrary-height energy dichotomy;
   - comparison with convex and semiconvex sumset results.

The sources below were checked through arXiv, Crossref/OpenAlex metadata,
publisher pages, and available journal or author PDFs.  Search phrases included
combinations of

```text
uniform forest negative correlation complete graph fixed components
forest Rayleigh complete split graph
coefficientwise Rayleigh difference forest polynomial Newton/binomial basis
square translates arbitrary set additive energy divisor bound
convex/semiconvex sumset arbitrary summand
Sidon/B_2[g] set sumset arbitrary set
```

The audit uses four labels.

- **Known:** the campaign claim is already stated in a located source, or is
  only a reparameterization of it.
- **Direct consequence:** the claim follows immediately from a standard
  identity plus an elementary estimate; the exact wording may be unrecorded.
- **Possibly new refinement:** the exact statement was not located and is not
  a formal consequence of the cited theorem, but the proof ingredients or
  asymptotic regime substantially overlap prior work.
- **Priority unresolved:** no direct match was found, but a MathSciNet/zbMATH
  citation-chain search and author-level comparison have not yet been done.

Absence from this search is not evidence of novelty.

## 2. Executive verdict

### 2.0 Late-session update: claims added after the initial audit

The initial audit below predates the strongest results of this
eight-hour campaign.  The following additional claims were therefore
searched separately through the same 2026-07-30 cutoff:

- an explicit \(k^{1/8}\) positive top Newton window;
- all-\(d\) first and second subleading ordinary-power symbols;
- a finite symbolic algorithm for every fixed symbol rank;
- an explicit fixed-constant square-root bottom window;
- forced cross-plane distance codegree;
- dense and weighted ruled-column distance expansion;
- rational-chord and fixed-number-field weighted terminal theorems.

Targeted searches combined the exact phrases

```text
complete split graph forest negative correlation Newton coefficients
uniform forest complete graph near-diagonal Newton window
fixed component forest pairwise negative correlation complete graph
near-diagonal r-Stirling symbol asymptotics
weighted ruled columns distinct distances integer heights
cross-plane distance codegree axial planes
fixed number field x^2+y^2 bounded conjugate height divisor
```

No direct statement of the campaign's \(k^{1/8}\) window, its two
closed all-\(d\) lower symbols, its cross-component fixed-rank
algorithm, or its weighted ruled-column theorem was located.  This is
only a negative search result, not a priority proof.

#### End-of-session claims not covered by the initial search

The final proof phase added the following results:

- exact ordinary symbols through rank eight and the first seven strict
  normalized Newton inequalities for every admissible depth;
- eight exact positive long-recurrence bands;
- an effective finite exact decision procedure for the full-domain
  positivity of each individually fixed long-recurrence band;
- an all-rank four-layer marked saddle cancellation;
- a complementary Charlier/Lagrange coefficient identity which removes
  the \(x=1\) endpoint singularity from the all-rank saddle expansion;
- arbitrary, height-dependent partial prime-cyclotomic fibre escape; and
- the same cyclotomic escape over a fixed real number field for all but
  finitely many prime angular orders.

Additional searches used

```text
complete graph forest ordinary symbol cubic degree
forest Rayleigh Newton recurrence fixed rank
Charlier polynomial complementary saddle forest enumeration
partial regular polygon fibres distinct distances cyclotomic
```

No direct statement of the rank-eight cross-component symbols, the
all-rank \(3r+1\) denominator law, the forced falling triangle, the
eight long-recurrence bands, the fixed-band decision corollary, or the
partial cyclotomic-fibre theorem was located.  The decision corollary
is elementary once the campaign's exact polynomial construction and
positive-leading theorem are granted, so it should be presented as an
effective consequence rather than as the novelty centrepiece.  The
closest special-function literature is Dunster,
*Uniform Asymptotic Expansions for Charlier Polynomials*, J. Approx.
Theory 112 (2001), 93--133,
[DOI 10.1006/jath.2001.3595](https://doi.org/10.1006/jath.2001.3595).
It studies Charlier turning-point asymptotics, but the search did not
locate the campaign's normalized forest profiles, marked determinant,
or cubic ordinary-symbol degree theorem there.  Britikov's
[*Asymptotic number of forests from unrooted
trees*](https://m.mathnet.ru/eng/mzm4331) is relevant classical
forest-enumeration background.  Its full text was checked: it gives
leading asymptotic regimes for the number of labelled unrooted
forests as the component count varies, using local limit and
large-deviation methods.  No marked two-edge profile, cross-component
Rayleigh determinant, all-order ordinary-symbol expansion, or
\(3r+1\) denominator theorem was located in it.  It remains mandatory
background for the forest asymptotics, but is not a direct statement
of the campaign's main theorem.

The OPG package should therefore be described as a **strong
manuscript nucleus with priority still unresolved**, not as an
established first result.  The conceptual all-rank theorem is much
more important for publication than any fixed-rank computation by
itself.  Conversely, the cyclotomic theorem is a broad structured
exclusion but still does not supply the missing inverse extraction
from an arbitrary critical Euclidean configuration.

#### Final targeted search: recurrence-leading and extraction results

The last proof phase added two further all-rank structures:

- the exact falling-triangle degrees and factors, followed by an
  all-rank theorem that every long-recurrence band has exact degree
  \(3q+2\) and positive leading coefficient; and
- a parameterized matching-or-single-plane-hub extraction from the
  critical cross-plane codegree.

Targeted OpenAlex/Crossref/arXiv and web searches used

```text
forest polynomial falling basis long recurrence
complete graph forest recurrence leading coefficient
2F0 Airy logarithmic derivative coefficient positivity
Airy asymptotic coefficients total positivity
high codegree weighted matching hub distance labels
```

No direct match for either statement was located.  The recurrence
proof passes through a formal
\({}_2F_0(1/6,-1/6;;6z)\) symmetric-square equation and an entire
factorial transform; the closest result located by the Airy search was
the general computer-algebra paper *Symbolic Evaluation of
Coefficients in Airy-type Asymptotic Expansions*
([arXiv:math/0103184](https://arxiv.org/abs/math/0103184)), which does
not state the forest transform, its dominant-zero theorem, or the
long-band sign.  Classical Hadamard, Jensen, and Rouché theory are
standard proof inputs and must not themselves be presented as new.

The matching-or-hub lemma is a tailored weighted-graph extraction.
Its finite-field quadratic tensor sharply demonstrates why the
aggregate ledger alone cannot force a rectangle, but the extraction
argument is elementary once the weighted tensor has been isolated.
It is therefore a useful structural node inside an Erdős proof, not a
stand-alone high-impact theorem without a Euclidean consequence.

The subsequent Euclidean hub theorem uses the classical planar
point--circle incidence estimate
\[
I(m,n)=O^*\!\left(
m^{2/3}n^{2/3}+m^{6/11}n^{9/11}+m+n
\right).
\]
The primary comparison is Sharir--Sheffer--Zahl,
[*Improved bounds for incidences between points and circles*,
Combinatorics, Probability and Computing 24 (2015), 490--520](https://doi.org/10.1017/S0963548314000534);
their equation (1) records the precise logarithmic planar bound.
The \(6/11,9/11\) planar term ultimately uses the pseudo-circle
cutting machinery of Marcus--Tardos,
[*Intersection reverse sequences and geometric applications*,
JCTA 113 (2006), 675--691](https://doi.org/10.1016/j.jcta.2005.07.002).
Janzer--Janzer--Methuku--Tardos subsequently removed the logarithm
from the underlying intersection-reverse/pseudo-circle cutting bound
in [*Tight bounds for intersection-reverse sequences, edge-ordered
graphs, and applications*](https://doi.org/10.1112/jlms.70324).
That 2025 refinement improves polylogarithmic factors but does not
alter the power exponents used in the campaign ledger.
The incidence estimate is known.  The campaign's contribution is the
injective reverse-circle encoding of the fixed-plane hub and its
combination with the critical codegree exponents, which excludes
\(\kappa<1/5\) hubs and extracts a
\(t^{1/5-\varepsilon}\) rich matching.  No newer general planar
point--circle exponent improving the \(6/11,9/11\) term was located in
the targeted search through the audit cutoff.

The extracted repeated-circle chart was also tested against the
campaign's arithmetic terminals.  Its exact normal form is a circle
and its perpendicular axis, and a regular-polygon plus symmetric
arithmetic-progression model, defined for every even circle
multiplicity \(\mu\), has only linear total distance growth.
Accordingly, the chart itself is a sharp Lenz-type obstruction rather
than an independently expandable terminal.  No novelty is claimed for
the classical circle--axis construction; the useful campaign-specific
information is that it is exactly the obstruction produced by equality
of the reverse-circle equations in this proof tree.

The late two-chart audit also sharpens the prior-work boundary.  The
complete source-circle classification is already Theorem 1.4 of
Mathialagan--Sheffer,
[*Distinct distances on non-ruled surfaces and between
circles*](https://arxiv.org/abs/2011.08098): for point sets of sizes
\(m,n\) on two circles in \(\mathbb R^3\) that are neither aligned nor
perpendicular, the bipartite distance set has size
\[
\Omega\!\left(
\min\{m^{2/3}n^{2/3},m^2,n^2\}
\right).
\]
Both aligned and perpendicular circle pairs admit \(O(m+n)\)
constructions.  Thus the campaign's concentric multi-radius model is
an audited realization of the aligned obstruction inside the reverse-
circle proof tree, not a new two-circle classification.  Any positive
multi-chart lemma must force a pair outside the applicable exceptional
family and then quantify how often such a pair occurs in the hub
ledger.  In the campaign's retained off-axis chart class the
perpendicular exception would require \(A_1=A_2=0\), whereas
\(A_i=\cos(\alpha_i-\beta_i)v_i\ne0\).  Hence only the aligned family
survives there, and the missing result is an incidence-rich
nonaligned-pair extraction rather than a new two-circle theorem.

Combining that known theorem with the campaign's per-plane
reverse-circle injectivity gives one additional campaign-specific
corollary.  All active circles richer than
\(t^{9/4+\eta}\) in a fixed hub plane must be concentric; their
incidence sets are disjoint and each merged circle has weight at most
the number \(M\) of target planes.  Their total weighted incidence is
therefore at most \(MQ=t^{4+o(1)}\), negligible relative to the hub
mass \(t^{7-3\kappa-o(1)}\) for fixed \(\kappa<1\).  The two-circle
expansion input is known; the weighted concentration consequence is
specific to this proof-tree bookkeeping and is not an exponent
improvement.

A subsequent weighted dyadic decomposition improves the forced
merged-circle multiplicity from the earlier coarse exponent
\((5-15\kappa)/11\) to \((5-15\kappa)/2\).  This is a tailored
layer-cake use of the known planar point--circle theorem, not a new
incidence theorem.  The accompanying moderate-rich feasible ledger
shows why this sharper bookkeeping still cannot improve the
\(3/5\) exponent without an additional Euclidean compatibility input.

These were negative searches, not a priority proof.  MathSciNet,
zbMATH, and a direct author-to-author comparison with Tang--Zhang
remain mandatory before submission.

The closest OPG source remains Tang--Zhang's March 2026 preprint,
[Pairwise Negative Correlation for Uniform Spanning Subgraphs of the
Complete Graph](https://arxiv.org/abs/2603.10738).  It proves
pairwise negative correlation for a fixed component count on \(K_n\)
when \(n\) is sufficiently large.  It does not state the campaign's
cross-component convolution, base-four Newton transform, growing
top/bottom windows, or ordinary-symbol expansion.  Those campaign results
must nevertheless cite Tang--Zhang prominently because their exact
forest enumerations and fixed-component asymptotic setting are the
nearest prior machinery.

For Erdős #1083, the current curated problem record still lists
\(f_3(n)\gg n^{3/5}\) as the best general lower exponent, obtained by
combining the Solymosi--Vu method with the planar Guth--Katz input:
[Erdős Problems #1083](https://www.erdosproblems.com/1083).
The primary high-dimensional baseline is Solymosi--Vu,
[Combinatorica 28 (2008), 113--125,
DOI 10.1007/s00493-008-2099-1](https://doi.org/10.1007/s00493-008-2099-1).
The closest modern geometric comparison located is Mathialagan--Sheffer,
[Distinct distances on non-ruled surfaces and between
circles](https://arxiv.org/abs/2011.08098), which proves stronger
bounds away from ruled exceptions and classifies linear-distance
circle-pair configurations.  Pach--de Zeeuw's
[curve theorem](https://arxiv.org/abs/1308.0177) is also mandatory
background for the exceptional line/circle geometry.

#### Updated OPG assessment

The package is now materially stronger than the initial
fixed-depth-only assessment:

1. a proved, effective positive top window
   \[
   0\le d\le k^{1/8};
   \]
2. a proved explicit bottom window
   \[
   0\le r\le2^{-28}\sqrt{k}
   \quad(k\ge9\cdot2^{58});
   \]
3. proved all-\(d\) first and second subleading symbols; and
4. a proof that every fixed symbol rank is computable by one finite
   Cauchy--saddle/central-moment recurrence.

This is a plausible stand-alone research-paper nucleus on asymptotic
Newton positivity for the complete-split reduction, subject to a
full author/source comparison and conventional peer review.  It is
still not a proof of OPG-1757, does not control the middle Newton
region, and does not justify advertising a \(k^{1/3}\) window.  The
finite \(C=3\) weighted-symbol check is evidence only.

The honest journal assessment is therefore:

- **paper nucleus:** yes;
- **unconditional solution of OPG-1757:** no;
- **CAS 1 readiness:** unresolved, and not established by the present
  metadata search alone.

#### Updated Erdős assessment

The forced codegree theorem and the weighted ruled-column theorem are
genuine structural progress.  In a polynomial-height integer chart,
\[
|\Delta^2(P)|
\ge
\frac{\Omega}
{|\mathcal J|L_UT_\times T_2},
\]
and the rational/fixed-number-field variants remove alignment and
rationality artefacts.  However, the fixed-field two-square fibre is
ultimately an application of standard ideal-divisor counting and
Dirichlet's unit theorem; it should be presented as a tailored
terminal lemma, not as a new theorem of algebraic number theory.

The missing implication remains:
\[
\mathfrak C_{\rm plane}\ge t^{13-o(1)}
\quad\Longrightarrow\quad
\text{one large bounded-complexity weighted chart},
\]
or a direct distance expansion.  The current work has not proved this
extraction and therefore has not improved the exponent \(3/5\).

The honest journal assessment is:

- **useful structural/conditional package:** yes;
- **unconditional exponent improvement:** no;
- **stand-alone CAS 1 main theorem:** no at the current boundary.

### 2.1 OPG-1757

The general pairwise negative-correlation conjecture for uniform forests
remains open.  However, two complete-graph regimes relevant to the campaign
are already known:

- Stark proved the unconditioned uniform-forest inequality for \(K_n\) when
  \(n\) is sufficiently large.
- Tang and Zhang proved in March 2026 that, for every fixed number \(c\) of
  components, the uniform \(c\)-component forest on \(K_n\) is pairwise
  negatively correlated for all sufficiently large \(n\).

Tang--Zhang is the closest priority source.  Its proof uses the same
Liu--Chow formula, contraction of prescribed edges, complete-graph symmetry,
and the adjacent/disjoint two-edge orbit identity used in this campaign.  In
particular, the campaign's exact formulas for the number of fixed-component
forests containing no prescribed edge or a prescribed adjacent edge pair
must not be presented as new.

The campaign's actual determinant
\[
\mathcal C_t(n)=
\sum_{c+d=t}\left(
W_{1,c}(n)W_{1,d}(n)-W_{0,c}(n)W_{2,d}(n)
\right)
\]
is different from the single-component correlation determinant controlled
by Tang--Zhang: it convolves possibly unequal component counts \(c,d\).
Likewise, taking Newton differences in the vertex parameter is not a step
stated in that paper.  Therefore the first/second/third active-layer formulas
and the fixed-depth theorem are **not located as known theorems**, but they
are best classified as **possibly new, technically close refinements**, not
as a new solution of complete-graph negative correlation.

As presently scoped, three exact active layers plus eventual positivity at
each fixed depth are unlikely to support a CAS 1 journal claim on their own.
They leave depths growing with \(k\) uncontrolled and do not prove the
complete first coefficient, the full \(\alpha^2\) layer, all edge-pair orbits
of complete-split graphs, or OPG-1757.

### 2.2 Square translates and arbitrary heights

The main inequalities in
`SUMSET_EXPANSION_ATTACK.md` and
`ARBITRARY_HEIGHT_ENERGY_DICHOTOMY.md` are mathematically useful in the
geometric proof tree, but their additive-combinatorial core is elementary.
For finite \(A\) and indexed \(X\), Cauchy--Schwarz gives
\[
|A+X|\ge \frac{|A|^2|X|_{\rm index}^2}{E(A,X)}.
\]
Bounding every nonzero correlation
\[
r_{A-A}(t)=|A\cap(A+t)|
\]
by \(\lambda(A)\), and bounding the multiplicity of an indexed \(X\)-value
by two, directly gives the campaign's denominator
\[
2mS+\lambda(A)S^2.
\]
The inverse inequality is just its rearrangement.  For
\(A=\{0^2,\ldots,(m-1)^2\}\), the estimate
\(\lambda(A)\le\max_{n\le(m-1)^2}\tau(n)\) follows immediately from
\[
d^2-e^2=(d-e)(d+e).
\]

Thus:

- the arbitrary-height theorem is a **direct mixed-energy consequence**;
- the square divisor specialization is a **direct elementary consequence**;
- the exact bounded-multiplicity formulation may be unrecorded, but that is
  not paper-level novelty by itself.

The potentially publishable contribution is not this inequality alone.  It
would be an extraction theorem showing that the synchronized square-height
or low-\(\lambda\) slice is forced inside the inherited distinct-distance
proof, thereby producing an unconditional exponent gain for \(f_3(N)\).
That bridge is currently absent.

## 3. OPG-1757: exact source-to-claim table

| Primary source | Exact source claim relevant here | Relation to this campaign | Classification |
|---|---|---|---|
| Feder--Mihail, *Balanced matroids*, STOC 1992, [DOI](https://doi.org/10.1145/129712.129716) | Introduces balanced matroids; uniform bases of graphic/regular matroids have negative-correlation and expansion properties. | Applies to spanning trees/bases, not to all forests/independent sets. It is background, not a solution of OPG-1757. | Known background |
| Grimmett--Winkler, *Negative association in uniform forests and connected graphs*, RSA 24 (2004), [DOI](https://doi.org/10.1002/rsa.20012), [arXiv](https://arxiv.org/abs/math/0302185) | States/reviews uniform-forest edge negative correlation and verifies it computationally for all graphs on at most 8 vertices and 9-vertex graphs with at most 18 edges. | Establishes the conjectural and finite-computation baseline. The campaign's larger finite scans do not replace a general proof. | Known baseline |
| Semple--Welsh, *Negative Correlation in Graphs and Matroids*, CPC 17 (2008), [DOI](https://doi.org/10.1017/S0963548307008978), [author PDF](https://www.math.canterbury.ac.nz/~c.semple/papers/SW07.pdf) | Proves weighted independence/spanning correlation for an infinite class obtained from blocks \(K_4\) or minors by series/parallel extensions. | Any claimed new infinite graph class must be shown not to lie in this closure. Complete graphs \(K_n\), \(n>4\), are not covered merely by this block description. | Known infinite-class result |
| Wagner, *Negatively Correlated Random Variables and Mason's Conjecture for Independent Sets in Matroids*, Ann. Comb. 12 (2008), [DOI](https://doi.org/10.1007/s00026-008-0348-z), [arXiv](https://arxiv.org/abs/math/0602648) | Develops the independent-set Rayleigh condition, structural consequences, and two-sum closure results. | Supplies the correct weighted/matroidal framework. The campaign currently proves only selected univariate coefficients, not an I-Rayleigh theorem. | Known framework |
| Erickson, *Sums of squares and negative correlation for spanning forests of series parallel graphs*, AJC 52 (2012), [arXiv](https://arxiv.org/abs/1008.3660), [journal PDF](https://ajc.maths.uq.edu.au/pdf/52/ajc_v52_p075.pdf) | Gives a sum-of-squares expression for the forest Rayleigh difference of series-parallel graphs. | A new SOS or graph-operation theorem must be compared with this. The campaign's complete-graph convolution is not an instance of the stated series-parallel result for large \(K_n\). | Known special class |
| Liu--Chow, *Enumeration of Forests in a Graph*, Proc. AMS 83 (1981), [DOI](https://doi.org/10.1090/S0002-9939-1981-0627715-2) | Gives the general \(k\)-component forest enumeration formula used by the campaign. | Formula (and applications obtained only by substituting a contracted complete graph) is prior art. | Known counting input |
| Myrvold, *Counting \(k\)-component forests of a graph*, Networks 22 (1992), [DOI](https://doi.org/10.1002/net.3230220704) | Gives a simpler graph-theoretic proof of Liu--Chow and a fixed-\(k\) polynomial-time algorithm. | Reinforces that fixed-component enumeration itself is not novel. | Known counting input |
| Stark, *The Edge Correlation of Random Forests*, Ann. Comb. 15 (2011), [DOI](https://doi.org/10.1007/s00026-011-0104-7) | Proves uniform-forest edge negative correlation on \(K_n\) for all sufficiently large \(n\), using enumerative/asymptotic methods. | The campaign cannot claim the unconditioned large-\(n\) complete-graph result. Its Newton coefficient refinement is a different question. | Known complete-graph theorem |
| Brändén--Huh, *Lorentzian polynomials*, Ann. Math. 192 (2020), [DOI](https://doi.org/10.4007/annals.2020.192.3.4), [arXiv](https://arxiv.org/abs/1902.03719) | Establishes Lorentzianity for the homogenized multivariate Tutte polynomial for \(0<q\le1\) and general negative-dependence consequences; Tang--Zhang record the resulting factor-2 forest correlation inequality for every graph. | This is a strong universal approximate benchmark, but not the conjectured factor \(1\). Selected coefficient positivity should be positioned against this theory. | Known approximate/general framework |
| Brändén--Krasikov--Shapiro, *Elements of Pólya--Schur theory in finite difference setting*, Proc. AMS 144 (2016), [DOI](https://doi.org/10.1090/proc/13115), [arXiv](https://arxiv.org/abs/1204.2963) | Develops finite-difference hyperbolicity preservers and mesh-\(\ge1\) real-rootedness tools. | Mandatory background for the campaign's Poisson/falling-basis real-root route.  It does not state real-rootedness of the marked forest determinant or the ordinary-symbol degree theorem. | Known analytic framework; no direct overlap located |
| Tang--Zhang, *Pairwise Negative Correlation for Uniform Spanning Subgraphs of the Complete Graph*, submitted 11 March 2026, [arXiv](https://arxiv.org/abs/2603.10738) | For each fixed component count \(c\ge2\), proves pairwise negative correlation for the uniform \(c\)-component forest on \(K_n\) for sufficiently large \(n\). Section 3 reviews Liu--Chow, counts adjacent prescribed edge pairs by contraction, and derives the disjoint orbit through moments. | Closest overlap. Its \(W_{0,c}\) and adjacent-pair formulas coincide with the campaign's counting engine. It does not state the cross-component convolution \(\mathcal C_t\) or base-four Newton positivity. | Known nearby theorem; mandatory citation |
| Ge--Liao--Zhang, *Resistance distances and the Moon-type formula of a vertex-weighted complete split graph*, DAM 359 (2024), [DOI](https://doi.org/10.1016/j.dam.2024.07.040) | Counts weighted spanning trees of a complete-split graph containing a fixed spanning forest. | Same graph family and prescribed-forest language, but only spanning trees, not the all-forest Rayleigh determinant or Newton layers. | Nearby enumeration, not a direct overlap |
| Yang--Tian, *Counting spanning trees of multiple complete split-like graph containing a given spanning forest*, Discrete Math. 348 (2025), [DOI](https://doi.org/10.1016/j.disc.2024.114300) | Gives formulas for spanning trees containing a fixed forest in complete-split and related graphs. | Must be cited if the complete-split reduction is published, but it does not establish forest negative correlation. | Nearby enumeration, not a direct overlap |

## 4. OPG campaign claim-by-claim assessment

### 4.1 Complete-graph determinant behind the complete-split reduction

Campaign claim:
\[
c_k(s)=\frac{(k-2)!}{2}[x^k]
\left(\Phi_1(x)^2-\Phi_0(x)\Phi_2(x)\right),
\]
where \(\Phi_h\) counts complete-graph forests containing a prescribed
matching of size \(h\).

Assessment:

- The interpretation as a coefficient of a forest Rayleigh difference is
  standard once the complete-split reduction is accepted.
- The enumerations of \(W_{0,c}\), \(W_{1,c}\), an adjacent prescribed
  pair, and the recovery of a disjoint pair by orbit double counting are
  all within the Liu--Chow/Tang--Zhang toolkit.
- The specific complete-split-to-complete-graph coefficient extraction was
  not located in the searched sources.  Its priority depends on the earlier
  internal reduction and a dedicated complete-split citation search.

Verdict: **possibly new reduction/packaging; priority unresolved.**  It is
not by itself a negative-correlation theorem.

### 4.2 First active Newton layer

Campaign claim:
\[
a_{k,q}=0\quad(q<q_0),\qquad
a_{k,q_0}>0,\qquad q_0=\left\lfloor\frac{k-2}{2}\right\rfloor,
\]
with exact parity-dependent formulas for all \(k\ge2\).

Assessment:

- The support vanishing is a capacity statement specific to the campaign's
  base-four Newton transform.
- The final formulas use component totals \(3\) and \(4\) and fixed-component
  complete-graph counts.  They were not found verbatim.
- They are not implied merely by Tang--Zhang's same-component p-NC theorem,
  because the campaign determinant contains cross terms with different
  component counts.

Verdict: **possibly new exact refinement**, but presently a boundary strip
of a larger coefficient array.  Insufficient alone for a strong journal
novelty claim.

### 4.3 Second and third active Newton layers

Campaign claims:
\[
a_{k,q_0+1}>0\quad(k\ge3),\qquad
a_{k,q_0+2}>0\quad(k\ge3),
\]
with explicit parity-dependent formulas.

Assessment:

- No exact match was found for these Newton differences.
- The generating mechanism
  \(F_0,F_1,A,F_2\), rooted-tree EGF, Lagrange inversion, and adjacent/disjoint
  orbit identity are classical or already present in nearby complete-graph
  work.
- The exact cancellation and sign checks appear to be campaign-specific,
  but they remain finitely many fixed depths.

Verdict: **possibly new calculations/lemmas, priority unresolved**.  The
publication value is cumulative, not three separate theorem claims.

### 4.4 Fixed-depth eventual positivity

Campaign claim: for every fixed \(r\),
\[
a_{k,q_0+r}
=\frac{2(k-2)!}{(t_r-3)!}n_r^{2n_r-8}
+O_r\!\left((k-2)!n_r^{2n_r-9}\right)>0
\]
for all sufficiently large \(k\).

Its engine is
\[
\mathcal C_t(n)=\frac{4}{(t-3)!}n^{2n-8}
+O_t(n^{2n-9})
\]
for fixed total component count \(t\).

Comparison with Tang--Zhang:

- Tang--Zhang fix one component count and let \(n\to\infty\).
- The campaign fixes the **sum** \(c+d=t\), expands each finite
  fixed-component term to the cancellation order, then convolves and applies
  a Newton difference.
- Tang--Zhang therefore does not formally imply this displayed constant.
  Nevertheless, it supplies essentially the same exact formulas and
  asymptotic setting from which the campaign calculation starts.

Verdict: **possibly unrecorded asymptotic refinement, but methodologically
close to prior work.**  Without control for \(r=r(k)\), it does not close all
Newton coefficients and is unlikely to be a CAS 1 main theorem.

### 4.5 What would clear a serious publication threshold?

At least one of the following should be obtained.

1. Prove all base-four Newton coefficients nonnegative, including depths
   growing with \(k\), and identify the precise complete-split consequence.
2. Prove the entire \(\alpha^2\) layer for all parameters and all relevant
   edge-pair orbits of complete-split graphs.
3. Give a conceptual operation, injection, SOS identity, or Lorentzian-type
   principle that proves forest Rayleigh inequalities for a genuinely new
   infinite graph class not covered by Semple--Welsh/Erickson/Stark/Tang--Zhang.
4. Obtain a multivariate theorem rather than isolated coefficients of a
   univariate specialization.

Even then, journal quartile depends on the final theorem and the journal's
current CAS classification; it cannot be inferred from correctness alone.

## 5. Additive combinatorics: exact source-to-claim table

| Primary source | Exact source claim relevant here | Relation to this campaign | Classification |
|---|---|---|---|
| Elekes--Nathanson--Ruzsa, *Convexity and Sumsets*, JNT 83 (2000), [DOI](https://doi.org/10.1006/jnth.1999.2386), [author PDF](https://www.theoryofnumbers.com/melnathanson/pdfs/nath1999-95.pdf) | Establishes incidence-based expansion for strictly convex images and sumsets. | The first squares are a convex sequence; this is the classical source of the generic \(3/2\)-type scale. | Known baseline |
| Ruzsa--Shakan--Solymosi--Szemerédi, *On distinct consecutive differences*, [arXiv](https://arxiv.org/abs/1910.02159) | If a real sequence has distinct consecutive differences, then its sum with an arbitrary finite set has the corresponding \( |A||B|^{1/2}\)-scale lower bound (up to swapping the paper's parameter names); the bound is tight up to constants. | Applied to \(A_m=\{0^2,\ldots,(m-1)^2\}\), this gives the generic \(m\sqrt S\) benchmark. | Known direct baseline |
| Ruzsa--Solymosi, *Sumsets of Semiconvex Sets*, CMB 65 (2022), [DOI](https://doi.org/10.4153/S0008439521000096), [arXiv](https://arxiv.org/abs/2008.08021) | Gives a new proof of the distinct-consecutive-difference bound and constructs semiconvex sets with subquadratic sumsets, showing the generic theorem cannot be upgraded to near-product expansion without extra structure. | Justifies using the arithmetic factorization of squares rather than convexity alone. | Known sharp generic boundary |
| Schoen--Shkredov, *On Sumsets of Convex Sets*, CPC 20 (2011), [DOI](https://doi.org/10.1017/S0963548311000277), [arXiv](https://arxiv.org/abs/1105.3542) | Improves self-sum/difference bounds for convex sets using additive-energy methods. | Relevant to convex self-sums, but it does not state the square-plus-arbitrary-layer divisor bound. | Known nearby result |
| Hanson, *Additive Correlation and the Inverse Problem for the Large Sieve*, MPCPS 168 (2020), [DOI](https://doi.org/10.1017/S0305004118000518), [arXiv](https://arxiv.org/abs/1706.06958) | Under large-sieve hypotheses, forces large mixed additive energy with the set of squares. | Shows that mixed energy with squares is established language, but its direction and hypotheses differ from the campaign's universal upper-energy argument. | Nearby, not a direct overlap |
| Hegyvári, *Note on the sumset of squares*, [arXiv](https://arxiv.org/abs/2504.13230) | Gives a lower bound for \(Q+Q\) for an arbitrary finite subset \(Q\) of square numbers. | Concerns arbitrary subsets and self-sums. It neither implies nor contradicts the stronger estimate for the initial-square set with an arbitrary translate set. | Nearby square-sumset work |
| Wigert's maximal-order theorem; modern statement in Elsholtz--Technau--Technau, *The maximal order of iterated multiplicative functions*, Mathematika 65 (2019), [DOI](https://doi.org/10.1112/S0025579319000214), [arXiv](https://arxiv.org/abs/1709.04799) | Records \(\max_{n\le x}\log\tau(n)=(\log2+o(1))\log x/\log\log x\). | Supplies \(\tau_*(m)=m^{o(1)}\). The asymptotic is classical, not a campaign contribution. | Known number-theory input |

## 6. Additive campaign claim-by-claim assessment

### 6.1 Arbitrary-height energy dichotomy

Campaign claim:
\[
|A+X|\ge
\frac{m^2S^2}{2mS+\lambda(A)S^2},
\qquad
\lambda(A)=\max_{t\ne0}|A\cap(A+t)|.
\]

This is an indexed mixed-energy estimate.  If \(x_k\) has multiplicity at
most two, then the collisions with \(x_k=x_l\) contribute at most \(2mS\).
Every other ordered layer pair contributes at most \(\lambda(A)\).  Applying
Cauchy--Schwarz gives the formula.

The inverse statement
\[
\lambda(A)\ge \frac{m^2}{|A+X|}-\frac{2m}{S}
\]
is an algebraic rearrangement of the same inequality.

Verdict: **direct consequence of standard mixed additive energy**.  The
precise indexed constant is useful bookkeeping but not a credible
stand-alone novelty claim.

### 6.2 Initial squares plus arbitrary indexed translates

Campaign claim:
\[
\left|\{0^2,\ldots,(m-1)^2\}+\{x_0,\ldots,x_{S-1}\}\right|
\ge
\frac{m^2S^2}{2mS+\tau_*(m)S^2}
\]
when each indexed \(x\)-value occurs at most twice.

For a fixed nonzero difference,
\[
d^2-e^2=n
\]
has at most \(\tau(|n|)\) solutions in the required range because a factor
pair \((d-e,d+e)\) determines \((d,e)\).  Substitution into the preceding
general energy lemma gives the result.

Verdict: **direct elementary specialization**.  The exact statement was not
located in the targeted search, but the proof is a one-step \(B_2[g]\)-type
energy argument.  It should be presented as a useful lemma, not as a major
new additive-combinatorics theorem.

### 6.3 Small-sumset relations and algebraic angle certificate

The lower bound on the number \(R\) of integer layer differences under
\(|A_m+X_S|\le Km\sqrt S\) is obtained by retaining only contributing
off-diagonal pairs in the same energy inequality.  The polynomial relation
\[
2m^2(T_k(c)-T_l(c))=n
\]
then directly implies algebraicity and a degree bound for \(c=\cos\theta\).

Verdict: **direct inverse bookkeeping plus an elementary algebraic
certificate**.  It becomes substantial only if many relations are converted
into a stronger classification, incompatibility theorem, or robust
Diophantine statement.

### 6.4 What is genuinely stronger than the convex baseline?

For the initial-square set, the factorization gives
\[
|A_m+X_S|\gg
\min\left\{mS,\frac{m^2}{\tau_*(m)}\right\}.
\]
At \(m=S\), this is \(m^{2-o(1)}\), stronger than the generic semiconvex
\(m^{3/2}\) scale.  The strengthening is mathematically correct because
the square-difference multiplicity is \(m^{o(1)}\); it does not contradict
the sharp semiconvex examples, whose difference multiplicities need not
obey this arithmetic bound.

This is a strong **structured-subcase obstruction** in the geometry
campaign.  It is not an unconditional lower bound for \(f_3(N)\), because
the inherited proof has not forced the common-radius, common-angular-pattern
slice (nor the required compatible height structure).

### 6.5 What would clear a serious publication threshold?

At least one of the following is needed.

1. An extraction theorem from an arbitrary \(N\)-point configuration that
   produces the synchronized slice with only subpolynomial losses and hence
   gives
   \[
   f_3(N)\ge N^{3/5+\varepsilon-o(1)}
   \]
   for an explicit \(\varepsilon>0\).
2. A genuinely stronger inverse theorem that classifies high
   square-difference multiplicity across several compatible shifts and can
   be reinserted into the geometric proof.
3. A robust approximate-collision/Diophantine theorem, with quantitative
   separation, that survives the non-exact geometry needed by the inherited
   argument.
4. A broader and sharp square-polynomial translate theorem whose conclusion
   is not already the standard energy inequality with
   \(\max_t r_{A-A}(t)\) inserted.

Without such a bridge, the additive results are supporting lemmas, not a
CAS 1 paper-level main result.

## 7. Required citation and claim language

Any manuscript based on the present campaign should:

1. cite Tang--Zhang prominently before presenting complete-graph
   fixed-component asymptotics;
2. state that Liu--Chow/Myrvold supply the counting formula and that
   adjacent-pair contraction plus orbit recovery is prior methodology;
3. describe the Newton results as cross-component coefficient refinements,
   not as the first complete-graph negative-correlation theorem;
4. describe the square-translate bound as an elementary mixed-energy lemma
   exploiting low difference multiplicity;
5. distinguish the structured \(N^{4/5-o(1)}\) slice conclusion from an
   unconditional bound for \(f_3(N)\);
6. avoid “new”, “first”, or “publication-grade” until MathSciNet/zbMATH
   priority searching and a source-by-source proof comparison are complete.

Safe current wording is:

> We prove exact positivity for the first several Newton layers and eventual
> positivity at every fixed depth in a cross-component complete-graph
> Rayleigh convolution.  These statements refine, but do not replace, prior
> complete-graph negative-correlation results of Stark and Tang--Zhang.

and:

> An elementary mixed-energy argument shows that the initial-square
> synchronized slice has near-product expansion; the unresolved issue is
> extracting such a slice from the general geometric configuration.

## 8. Final readiness decision

| Package | Correct present status | Stand-alone CAS 1 readiness |
|---|---|---|
| First/second/third active Newton layers | Possibly new exact coefficient refinements; priority unresolved | No |
| Every fixed Newton depth eventually positive | Possibly new asymptotic refinement, close to Tang--Zhang methodology | No |
| Full complete-split/OPG consequence | Not proved | No |
| Arbitrary-height energy dichotomy | Direct standard energy consequence | No |
| Square-translate divisor bound | Direct elementary specialization; useful structured lemma | No |
| Unconditional \(f_3(N)\) exponent gain | Not proved; extraction bridge missing | No |

The best current research direction is therefore not to add more fixed
Newton layers or more variants of the same energy estimate.  It is to close
one of the two uniformity gaps:

- Newton depth growing with \(k\), ideally the whole complete-split
  \(\alpha^2\) layer; or
- a synchronized-slice extraction/inverse theorem that turns the geometric
  energy lemma into an unconditional distinct-distance exponent gain.
