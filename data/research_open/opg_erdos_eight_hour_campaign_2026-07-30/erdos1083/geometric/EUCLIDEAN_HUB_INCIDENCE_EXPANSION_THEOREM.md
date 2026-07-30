# Erdős #1083: Euclidean hub incidence expansion

Date: 2026-07-30

## 0. Outcome

The hub branch of
`HIGH_CODEGREE_MATCHING_OR_HUB_THEOREM.md` can be partially eliminated
using the actual Euclidean distance equation.

At the critical scale
\[
 M=t^{1+o(1)},\qquad Q=t^{3+o(1)},
\tag{1}
\]
fix one axial source plane \(\Pi_\alpha\), and let
\(\mathcal D_0\) be \(L\) squared-distance labels.  Suppose every
\(d\in\mathcal D_0\) has hub mass
\[
 \sum_{\substack{\beta\ne\alpha\\
 \cos(\alpha-\beta)\ne0}}
 R_{\alpha,\beta}(d)\geq H.
\tag{2}
\]
Then
\[
\boxed{
 LH
 \ll
 M\left\{
 Q^{2/3}(QL)^{2/3}
 +Q^{6/11}(QL)^{9/11}t^{o(1)}
 +Q+QL
 \right\}.
}
\tag{3}
\]
This is exactly the retained nonperpendicular plane-pair graph on
which the cell cap and the matching-or-hub theorem are defined.

For the hub parameters
\[
 L=t^{2-2\kappa-o(1)},\qquad
 H=t^{5-\kappa-o(1)},
\tag{4}
\]
the left side of (3) has exponent \(7-3\kappa\), while the four terms
on the right have exponents
\[
 \frac{19}{3}-\frac{4\kappa}{3},\qquad
 \frac{74}{11}-\frac{18\kappa}{11},\qquad
 4,\qquad
 6-2\kappa.
\tag{5}
\]
For \(0<\kappa<1\), the second exponent in (5) is the largest.
Its differences from the first and fourth exponents are respectively
\((13-10\kappa)/33\) and \((8+4\kappa)/11\), and it is also larger
than \(4\).
Consequently
\[
\boxed{\kappa<\frac15\quad\Longrightarrow\quad
\text{the Euclidean hub branch is impossible}.}
\tag{6}
\]

Combining (6) with the parameterized matching-or-hub theorem gives a
new unconditional Euclidean structure theorem:

> For every fixed \(\varepsilon>0\), the critical cross-plane
> codegree forces at least \(t^{1-o(1)}\) distance labels, each
> supported on a matching of
> \(t^{1/5-\varepsilon-o(1)}\) pairwise disjoint rich axial-plane
> pairs.  Every matched plane-pair cell has
> \(t^{3-o(1)}\) representations of that label.

This does not yet improve the \(3/5\) distinct-distance exponent, but
it replaces the previous abstract matching-or-hub alternative by an
unconditional Euclidean coefficient-separated matching theorem.

## 1. The hub as planar point--circle incidence

Use signed radial--height coordinates.  A source point of
\(\Pi_\alpha\) is
\[
 p=(u,z),
\]
and a target point of \(\Pi_\beta\) is
\[
 q=(v,w).
\]
Put
\[
 c_{\alpha,\beta}=\cos(\alpha-\beta).
\]
The squared-distance equation is
\[
 |p-q|^2
 =
 u^2+v^2-2c_{\alpha,\beta}uv+(z-w)^2=d.
\tag{7}
\]
For fixed \(\beta,q,d\), equation (7), viewed in the source
\((u,z)\)-plane, is the circle
\[
\boxed{
 u^2+z^2-2c_{\alpha,\beta}v\,u-2wz
 +v^2+w^2-d=0.
}
\tag{8}
\]
An incidence of \(p\in P_\alpha\) with this circle is exactly a
representation of \(d\) by the ordered pair \((p,q)\).

### Lemma 1 (no repeated reverse circles)

If \(c_{\alpha,\beta}\ne0\), the map
\[
 (q,d)\longmapsto \Gamma_{\beta,q,d}
\tag{9}
\]
defined by (8) is injective.

Indeed, equality of two normalized equations first gives
\[
 c_{\alpha,\beta}v=c_{\alpha,\beta}v',
\qquad w=w',
\]
and hence \(v=v'\), \(w=w'\).  Equality of the constant terms then
gives \(d=d'\).

Thus, after deleting the perpendicular target plane, the circle
collection for each fixed \(\beta\) is a set of distinct circles, not
a multiset.  This injectivity is the Euclidean input absent from the
abstract plane-pair/distance tensor.

Equations with negative squared radius have no incidences and are
discarded.  A zero-radius equation contributes at most one incidence;
all such terms are absorbed by the \(+QL\) term below.  The remaining
curves are genuine distinct real circles.

## 2. Proof of the capacity bound

Fix a nonperpendicular target plane \(\Pi_\beta\).  Use
\[
 \mathcal P=P_\alpha,\qquad
 \mathcal C_\beta
 =
 \{\Gamma_{\beta,q,d}:
 q\in P_\beta,\ d\in\mathcal D_0\}.
\]
Then
\[
 |\mathcal P|\leq Q,\qquad
 |\mathcal C_\beta|\leq QL,
\tag{10}
\]
and Lemma 1 makes the circles distinct.

The standard planar point--circle incidence theorem gives
\[
\begin{aligned}
 I(\mathcal P,\mathcal C_\beta)
 \ll{}&
 Q^{2/3}(QL)^{2/3}\\
 &+Q^{6/11}(QL)^{9/11}
 \log^{2/11}\!\left(2+\frac{Q^3}{QL}\right)
 +Q+QL.
\end{aligned}
\tag{11}
\]
The logarithm is \(t^{o(1)}\).  Equation (11) is the classical
planar bound
\[
 I(m,n)
 =
 O\!\left(
 m^{2/3}n^{2/3}
 +m^{6/11}n^{9/11}\log^{2/11}(2+m^3/n)
 +m+n
 \right);
\]
see Sharir--Sheffer--Zahl,
[*Improved bounds for incidences between points and circles*,
arXiv:1208.0053](https://arxiv.org/abs/1208.0053), equation (1) and
the references there for the planar theorem.
The later Janzer--Janzer--Methuku--Tardos
[*Tight bounds for intersection-reverse sequences, edge-ordered
graphs, and applications*](https://doi.org/10.1112/jlms.70324)
removes the logarithm from the underlying pseudo-circle cutting
input.  Retaining the older logarithmic form in (11) is harmless here:
the factor is \(t^{o(1)}\), and neither version changes any exponent
in (5), (12), or (15).

Summing (11) over the retained nonperpendicular target planes proves
(3).  The perpendicular pair was deleted before the high-codegree
matching-or-hub extraction, exactly as in
`ANGULAR_STARVATION_BRANCH_ATTACK.md`; no incidence or cell-cap claim
is made for that exceptional pair.

Substitution of \(M=t\), \(Q=t^3\), and
\(L=t^{2-2\kappa}\) in (3) gives exactly (5).  The differences between
the lower exponent and the four upper exponents are
\[
 \frac{2-5\kappa}{3},\qquad
 \frac{3-15\kappa}{11},\qquad
 3-3\kappa,\qquad
 1-\kappa.
\tag{12}
\]
The second is the smallest on \(0<\kappa<1\).  It is positive exactly
when \(\kappa<1/5\), proving (6).

## 3. The exact remaining incidence gap

Dividing (3) by \(L=t^{2-2\kappa}\), the strongest standard incidence
term permits average hub mass
\[
 H\leq t^{52/11+4\kappa/11+o(1)}.
 \tag{13}
\]
The matching-or-hub theorem asks for
\[
 H\geq t^{5-\kappa-o(1)}.
 \tag{14}
\]
The signed saving furnished by the standard theorem is therefore
\[
 (5-\kappa)
 -\left(\frac{52}{11}+\frac{4\kappa}{11}\right)
 =
 \boxed{\frac{3-15\kappa}{11}}.
 \tag{15}
\]
At the balanced value \(\kappa=1/2\), the incidence theorem misses by
\[
 \boxed{\frac{9}{22}}
 \tag{16}
\]
of a power of \(t\): it permits \(H=t^{54/11+o(1)}\), whereas the hub
only requires \(H=t^{9/2-o(1)}\).

This is an exact method boundary, not a Euclidean counterexample.
The general planar point--circle bound need not be sharp for the
special circles (8).

## 4. Cross-plane repeated-circle refinement

There is a second rigorous consequence in the range where the
plane-by-plane bound no longer contradicts the hub.  First discard
every reverse circle having no incidence with \(P_\alpha\).  Let
\(\mu\) be the maximum multiplicity of one remaining normalized
circle equation (8) among triples
\[
 (\beta,q,d),\qquad
 \beta\ne\alpha,\quad
 \cos(\alpha-\beta)\ne0,\quad
 q\in P_\beta,\quad d\in\mathcal D_0.
\tag{21}
\]
Thus every circle counted by \(\mu\) is incidence-active, not merely
a formally repeated empty equation.  After merging equal active
circles, write \(w_C\le\mu\) for the weight of a distinct circle and
put
\[
 \mathsf T=\sum_Cw_C\le MQL.
\]
Apply the planar incidence theorem separately to the dyadic classes
\(u\le w_C<2u\).  Such a class contains at most
\(\mathsf T/u\) distinct circles.  Multiplication by its upper weight
\(2u\), followed by summation over dyadic \(u\le\mu\), gives
\[
\begin{aligned}
 LH\ll{}&
 Q^{2/3}\mathsf T^{2/3}\mu^{1/3}\\
 &+Q^{6/11}\mathsf T^{9/11}\mu^{2/11}t^{o(1)}
 +Q\mu+\mathsf Tt^{o(1)}.
\end{aligned}
\tag{22}
\]
The logarithmic number of weight layers is absorbed by \(t^{o(1)}\).
Empty circles contribute nothing, and all zero-radius triples
contribute at most \(\mathsf T\), which is smaller than \(LH\) by
\(t^{1-\kappa-o(1)}\) for fixed \(\kappa<1\).

Write \(\mu=t^{m+o(1)}\).  At the critical parameters, the four terms
in (22) have exponents
\[
 6-\frac{4\kappa}{3}+\frac m3,\qquad
 \frac{72}{11}-\frac{18\kappa}{11}+\frac{2m}{11},
 \qquad3+m,\qquad6-2\kappa.
\]
To reach \(LH=t^{7-3\kappa-o(1)}\), the first three terms respectively
require
\[
 m\ge3-5\kappa,\qquad
 m\ge\frac{5-15\kappa}{2},\qquad
 m\ge4-3\kappa.
\]
The middle threshold is the smallest for every \(\kappa>0\), while
the last term misses by \(1-\kappa\).  Therefore a surviving hub
forces the strengthened bound
\[
\boxed{
 \mu\geq t^{(5-15\kappa)/2-o(1)}
 \qquad(\kappa<1/3).
}
\tag{23}
\]
For \(\kappa<1/5\), this contradicts the fixed-plane injective cap
\(\mu\le M=t^{1+o(1)}\), consistently recovering (6).  Full details
of the layer-cake step and an exact exponent certificate are in
`WEIGHTED_REVERSE_CIRCLE_DYADIC_REFINEMENT.md`.

This multiplicity has an exact Euclidean meaning.  Equality of circles
coming from \((\beta,v,w,d)\) and
\((\beta',v',w',d')\) is equivalent to
\[
\boxed{
 \cos(\alpha-\beta)v
 =\cos(\alpha-\beta')v'=A,\qquad
 w=w'=w_0,\qquad
 v^2-d=v'^2-d'=C.
}
\tag{24}
\]
Thus, for \(1/5\leq\kappa<1/3\), a surviving hub necessarily yields a
polynomial-size family on one horizontal height, aligned on the
cosine-radial curve
\[
 v=\frac{A}{\cos(\alpha-\beta)},
 \qquad d=v^2-C.
\tag{25}
\]
This is a genuine Euclidean chart, not an abstract label
concentration.  It supplies the next object on which a divisor,
sum-product, or angular-energy argument can act.

The geometry is especially transparent after rotating
\(\Pi_\alpha\) to the \(xz\)-plane.  A target point in (24) has
\[
(x,y,z)
=
(v\cos\beta,v\sin\beta,w_0)
=
(A,A\tan\beta,w_0).
\]
Thus all \(\mu\) target points lie on the horizontal line
\[
\ell_{A,w_0}=\{(A,y,w_0):y\in\mathbb R\},
\tag{25a}
\]
which is perpendicular to \(\Pi_\alpha\), while their labels satisfy
\[
d=y^2+(A^2-C).
\tag{25b}
\]
The common active reverse circle lies in \(\Pi_\alpha\), centered at
\((A,w_0)\).  Hence the repeated-circle alternative is precisely an
incidence-active circle--axis chart; this reformulation adds no
extra hypothesis.

## 5. Conditional incidence-saving extension

Suppose the special reverse-circle family (8) admits a saving
\(t^{-\sigma}\) over the \(6/11,9/11\) term after summing over
\(\beta\):
\[
 \sum_\beta I(P_\alpha,\mathcal C_\beta)
 \ll
 t^{74/11-18\kappa/11-\sigma+o(1)}
 \tag{26}
\]
with the other terms as in (3).  Then (12) becomes
\[
 \frac{3-15\kappa}{11}+\sigma>0.
\]
Therefore the hub branch is excluded whenever
\[
\boxed{
\kappa<\frac{3+11\sigma}{15}.
}
 \tag{27}
\]
In particular, reaching the balanced value \(\kappa=1/2\) requires
\[
\boxed{\sigma>\frac9{22}.}
 \tag{28}
\]

This identifies a precise next Euclidean target: exploit the coupled
center/radius form
\[
 \operatorname{center}(\Gamma_{\beta,q,d})
 =(c_{\alpha,\beta}v,w),
\qquad
 r^2=d-(1-c_{\alpha,\beta}^2)v^2
 \tag{29}
\]
to save more than \(9/22\) at the balanced hub scale, or combine a
smaller incidence saving with additional radial/height regularity.

## 6. Claim boundary

### Proved

- the exact reverse-circle representation (8);
- injectivity of \((q,d)\mapsto\Gamma_{\beta,q,d}\) for every
  nonperpendicular target plane;
- the all-parameter Euclidean hub capacity bound (3);
- unconditional exclusion of the hub branch for every
  \(\kappa<1/5\);
- the \(t^{1/5-\varepsilon}\) Euclidean rich-matching corollary;
- the repeated-circle/cosine-radial extraction (23)--(25) for every
  surviving hub with \(\kappa<1/3\);
- the exact \(9/22\) incidence deficit at \(\kappa=1/2\).

### Not proved

- exclusion of the hub branch for \(\kappa\geq1/5\);
- a \(9/22\) saving for the special circle family;
- an improvement of the \(3/5\) distinct-distance exponent.

## 7. Reproduction

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/erdos1083/geometric
pytest -q test_verify_euclidean_hub_incidence.py
python3 verify_euclidean_hub_incidence.py
```
