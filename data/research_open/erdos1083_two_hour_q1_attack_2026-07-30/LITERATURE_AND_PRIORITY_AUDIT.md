# Erdős #1083: literature and priority audit

Audit date: 2026-07-30.

## 1. Baseline that must not be overstated

The current [Erdős Problems #1083 page](https://www.erdosproblems.com/1083)
still marks the problem open.  It records
\[
f_3(N)\gg N^{3/5}
\]
as the recognized three-dimensional lower bound, obtained by combining
the method of Solymosi--Vu with the planar Guth--Katz theorem, and asks
whether
\[
f_d(N)=N^{2/d-o(1)}
\]
for every fixed \(d\ge3\).

Relevant primary sources are:

1. J. Solymosi and V. H. Vu,
   [*Distinct distances in high dimensional homogeneous sets*](https://doi.org/10.1007/s00493-008-2099-1),
   Combinatorica 28 (2008), 113--125.
2. L. Guth and N. H. Katz,
   [*On the Erdős distinct distances problem in the plane*](https://doi.org/10.4007/annals.2015.181.1.2),
   Annals of Mathematics 181 (2015), 155--190.
3. S. Bardwell-Evans and A. Sheffer,
   [*A reduction for the distinct distances problem in
   \(\mathbb R^d\)*](https://arxiv.org/abs/1705.10963),
   Journal of Combinatorial Theory, Series A 166 (2019), 64--93.

No result in the present two-hour package improves the exponent \(3/5\).
The correct baseline label is therefore **new structural progress inside
a critical branch**, not a solution or numerical improvement of #1083.
Targeted 2025--2026 searches for a later general \(\mathbb R^3\) bound
located new results for points restricted to curves or surfaces, but no
replacement for the \(3/5\) arbitrary-point-set baseline.

## 2. Route B: tangent--label and rich-plane matching

### Exact new-looking claim

The package first reached \(9/41\) through the tangent--label
parameter-line and planar target-fibre bounds.  A later fixed-centre
parabolic linearization strengthens the final result: subject to the
inherited and explicitly restated critical-branch hypotheses, the
Euclidean hub alternative is impossible for every fixed
\[
\kappa<\frac29.
\]
Combined with the inherited matching-or-hub extraction, this forces
\(t^{1-o(1)}\) distance labels with rich plane-pair matchings of size
\[
t^{2/9-\varepsilon-o(1)}.
\]
The proof uses the exact parameter-line identity
\[
d=\rho(C)^2+A(C)^2\tan^2(\alpha-\beta),
\]
the real Szemerédi--Trotter theorem, a source-circle fibre cap, and a
planar target-fibre distance cap.  Its final extra input is that, for
fixed signed \(A\), the map
\[
(u,z)\longmapsto\bigl(z,(u-A)^2+z^2\bigr)
\]
turns every reverse circle centred on \(x=A\) into a distinct line,
with point-map multiplicity at most two.

### Closest literature located

The closest general structural input found was A. Sheffer and O. Silier,
[*A structural Szemerédi--Trotter theorem for Cartesian
products*](https://arxiv.org/abs/2110.09692).  That paper explicitly
studies Cartesian-product point-line configurations with extremal
\(\Theta(n^{4/3})\) incidence count, proves parallel/concurrent and
additive/multiplicative structure, and constructs infinite extremal
families.  It therefore supports the present manuscript's caution:
ordinary Cartesian-product structure alone does not yield a universal
power saving at the \(9/41\) endpoint.

A second close current input is G. Currier, J. Solymosi and H.-H. H. Yu,
[*On the structure of extremal point-line
arrangements*](https://arxiv.org/abs/2409.06115),
Computational Geometry 132 (2026), 102227,
[doi:10.1016/j.comgeo.2025.102227](https://doi.org/10.1016/j.comgeo.2025.102227).
Their theorem says that a positive-density near-extremal
Szemerédi--Trotter arrangement contains a linear-size point
subconfiguration with only \(O(1)\) rigidity degrees of freedom.
This makes a simultaneous-near-equality attack at the \(2/9\) endpoint
more plausible, but it does not provide a power saving and does not
couple the different signed \(A\)-fibres, target service sets, or
distance labels required here.

Targeted searches using combinations of

```text
reverse circle, tangent-label, rich plane pair, matching-or-hub,
three-dimensional distinct distances, signed radial coordinate
```

did not locate the exact parameter identity or fixed-centre
linearization packaged as a hub-elimination theorem, nor the \(2/9\)
matching exponent.  This is not a proof of priority: the terminology
“reverse circle” is internal, and the same calculation could appear
under perpendicular-bisector, coaxial-plane, or distance-energy
language.  The parabolic circle-to-line map itself is elementary and
should not be advertised as a new incidence theorem; the potentially
new content is its integration with the weighted hub, rich-parameter-line,
and target-capacity ledgers to obtain the exponent \(2/9\).

### Publication assessment

Route B is the strongest candidate in this package.  It is a rigorous
inverse-structure theorem with a nontrivial rational exponent, and the
final \(2/9\) argument has two independent proof reconstructions.
Nevertheless, on the evidence currently available it is **not yet a
defensible Q1 submission by itself**:

- it does not improve \(f_3(N)\);
- its main conclusion lives at an intermediate node of a long inherited
  proof tree;
- the endpoint is compatible with every inequality currently used;
- a referee would reasonably ask what global distance consequence follows
  from the richer matchings.

It becomes a serious high-tier paper candidate if one adds either:

1. a fixed-power improvement above \(3/5\); or
2. a natural, stand-alone inverse theorem excluding simultaneous
   near-equality in the Cartesian-product incidence and planar-distance
   components, with applications beyond this one proof tree.

## 3. Route C: six-coprime cyclotomic fibre escape

### Exact new-looking claim

For angular order \(m>1\) with
\[
\gcd(m,6)=1,
\]
the package proves selected-distance-label injection across arbitrary
coaxial angular fibres whose squared radii and anchored height squares
lie in \(\mathbb Q\).  The threshold is exact for this universal injection
mechanism: orders divisible by \(2\) or \(3\) admit explicit collisions.
Kneser's theorem then gives the sharp equal-fibre bound
\[
|\Delta^2(P)|
\ge
\frac{\ell-1}{2\ell}|P|,
\]
where \(\ell\) is the least prime divisor of \(m\).  The argument extends
to every real characteristic-zero field \(K\) over which \(\Phi_m\)
remains irreducible.

### Closest literature located

The arithmetic input is H. B. Mann,
[*On linear relations between roots of
unity*](https://doi.org/10.1112/S0025579300005210),
Mathematika 12 (1965), 107--117.  Mann's theorem is already used in
discrete-geometry distance questions; for example, S. Kurz and V. Mishkin,
[*Open sets avoiding integral
distances*](https://doi.org/10.1007/s00454-013-9508-y),
Discrete & Computational Geometry 50 (2013), 99--123, uses it in a
different excluded-distance setting.  Thus “Mann plus regular polygons”
cannot itself carry a novelty claim.

Targeted searches using combinations of

```text
roots of unity, Mann theorem, distinct distances, concentric circles,
coaxial fibres, rational squared radii, five-term signed relation
```

did not locate the exact six-coprime injection classification or the
Kneser aggregate theorem.  Again, this is only a targeted negative search.
A full priority audit would need MathSciNet/Zentralblatt searches and
formula-level reading of work on rational distances, regular polygons,
vanishing sums of roots of unity, and distance sets on concentric circles.

### Publication assessment

Route C is clean and plausibly suitable as a lemma or a short specialized
note, but it is not presently Q1-scale:

- the signed five-term rigidity is a short consequence of Mann's theorem;
- the geometric family is arithmetic and highly structured;
- no extraction theorem forces such a fibre inside an arbitrary critical
  #1083 configuration;
- generic real parameters usually have much stronger distance
  separation, while the difficult configurations need not satisfy the
  field hypothesis.

The result becomes substantially stronger if paired with a robust
extraction/stability theorem that produces a large six-coprime fibre from
the matching branch, or with a classification over substantially broader
coefficient fields.

## 4. Priority decision

The defensible claim hierarchy after this audit is:

| Claim | Decision |
|---|---|
| #1083 solved | **No** |
| Exponent \(3/5\) improved | **No** |
| New intermediate structural exponent \(2/9\) | **Proved, priority not yet certified** |
| Exact six-coprime selected-label injection | **Proved, priority not yet certified** |
| Ready for a Chinese Academy Q1 journal | **Not yet** |
| Worth developing into a paper | **Yes: Route B first; Route C as a supporting or separate short theorem** |

Before any public priority claim, the next literature pass must include
MathSciNet/Zentralblatt and direct comparison with the closest
higher-dimensional distance and Cartesian-product incidence papers.
