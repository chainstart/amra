# A self-contained conditional axial-plane matching theorem

Date: 2026-07-30

## 1. Scope and asymptotic convention

This note proves a conditional inverse theorem for a finite Euclidean
configuration.  Its only problem-specific upstream assumption is the
pair-codegree hypothesis stated in Theorem 1 below.  The proof uses two
standard incidence theorems, both stated explicitly in Section 4.  No
other reduction, branch, or inherited theorem is invoked.

All asymptotics are along a sequence \(t\to\infty\).  The notation
\(X=t^{x+o(1)}\) means that
\[
 t^{x-\omega(t)}\le X\le t^{x+\omega(t)}
\]
for a function \(\omega(t)\to0\).  A one-sided version has the
corresponding meaning.  The error functions in the hypotheses are
uniform over all planes, plane pairs, and labels in the configuration.
Errors created in the proof may depend on a fixed parameter
\(\varepsilon\), but still tend to zero with \(t\).

## 2. Geometry and notation

After a rigid motion, fix the common axis
\[
 \mathfrak a=\{(0,0,z):z\in\mathbb R\}.
\]
For \(\alpha\in\mathbb R/\pi\mathbb Z\), choose its representative in
\([0,\pi)\), put
\[
 e_\alpha=(\cos\alpha,\sin\alpha,0),
\]
and define the **axial plane**
\[
 \Pi_\alpha
 =
 \{u e_\alpha+z(0,0,1):u,z\in\mathbb R\}.
\tag{2.1}
\]
The angle is taken modulo \(\pi\) because
\(\Pi_{\alpha+\pi}=\Pi_\alpha\).  The radial coordinate \(u\) in
(2.1) is signed.

Let \(\mathcal A_t\subset\mathbb R/\pi\mathbb Z\) be a finite set of
distinct axial-plane angles.  For each \(\alpha\in\mathcal A_t\), let
\[
 P_\alpha\subset\Pi_\alpha\setminus\mathfrak a
\]
be finite, and put
\[
 P=\bigcup_{\alpha\in\mathcal A_t}P_\alpha,\qquad
 \Delta^2(P)=\{|p-q|^2:p,q\in P,\ p\ne q\}.
\tag{2.2}
\]
The sets \(P_\alpha\) are disjoint because distinct axial planes meet
only on \(\mathfrak a\).

An unordered pair \(e=\{\alpha,\beta\}\subset\mathcal A_t\) is
**admissible** when
\[
 \alpha\ne\beta
 \quad\text{and}\quad
 \cos(\alpha-\beta)\ne0.
\tag{2.3}
\]
Thus equal and perpendicular axial-plane pairs are excluded.  Fix any
total order on \(\mathcal A_t\).  If \(\alpha<\beta\), define the
**plane-pair/label cell weight**
\[
 W_{e,d}
 =
 \bigl|\{(p,q)\in P_\alpha\times P_\beta:
                  |p-q|^2=d\}\bigr|,
\qquad d\in\Delta^2(P).
\tag{2.4}
\]
The total order only selects an orientation for the Cartesian product;
the value is independent of that choice by symmetry of distance.

For a label \(d\), a graph on \(\mathcal A_t\) has **rich support** if
its edges are admissible pairs \(e\) whose weights exceed a stated
threshold.  A **matching of size \(m\)** is a set
\[
 \{\{\alpha_i,\beta_i\}:1\le i\le m\}
\tag{2.5}
\]
of rich edges for which the \(2m\) angles
\(\alpha_1,\beta_1,\ldots,\alpha_m,\beta_m\) are all distinct.

## 3. Conditional main theorem

### Theorem 1 (critical pair-codegree forces rich axial-plane matchings)

Assume
\[
 |\mathcal A_t|=t^{1+o(1)},\qquad
 \max_{\alpha\in\mathcal A_t}|P_\alpha|\le t^{3+o(1)},\qquad
 |\Delta^2(P)|\le t^{3+o(1)}.
\tag{3.1}
\]
Assume also the **cell cap**
\[
 W_{e,d}\le t^{4+o(1)}
\tag{3.2}
\]
for every admissible \(e\) and every \(d\), and the **critical
pair-codegree hypothesis**
\[
 \boxed{
 \sum_{d\in\Delta^2(P)}
 \left[
 \left(\sum_{\substack{e\ {\rm admissible}}}W_{e,d}\right)^2
 -
 \sum_{\substack{e\ {\rm admissible}}}W_{e,d}^2
 \right]
 \ge t^{13-o(1)}.
 }
\tag{3.3}
\]

Then, for every fixed
\[
 0<\varepsilon<\frac29,
\tag{3.4}
\]
there is a set \(\mathcal D'\subseteq\Delta^2(P)\) with
\[
 |\mathcal D'|\ge t^{1-o_\varepsilon(1)}
\tag{3.5}
\]
such that, for every \(d\in\mathcal D'\), the graph whose edges satisfy
\[
 W_{e,d}\ge t^{3-o_\varepsilon(1)}
\tag{3.6}
\]
contains a matching of size at least
\[
 \boxed{t^{\,2/9-\varepsilon-o_\varepsilon(1)}}.
\tag{3.7}
\]

In particular, for all sufficiently large \(t\), each such matching
contains two edges and hence four distinct axial planes supporting the
same squared-distance label.  The conclusion is stronger than merely
finding four planes: it gives a polynomial-size family of pairwise
plane-disjoint cells, each with the representation lower bound (3.6).

## 4. Standard incidence inputs

The proof uses the following two classical planar results.

### Incidence input I: Szemerédi--Trotter

For a finite point set \(\mathcal P\subset\mathbb R^2\) and a finite
set \(\mathcal L\) of distinct lines,
\[
 I(\mathcal P,\mathcal L)
 \ll
 |\mathcal P|^{2/3}|\mathcal L|^{2/3}
 +|\mathcal P|+|\mathcal L|.
\tag{4.1}
\]
Consequently, if every line of \(\mathcal L\) contains at least
\(u\ge2\) points of \(\mathcal P\), then
\[
 |\mathcal L|
 \ll
 \frac{|\mathcal P|^2}{u^3}
 +\frac{|\mathcal P|}{u}.
\tag{4.2}
\]

### Incidence input II: points and circles

For \(q\) points and \(n\) distinct circles in \(\mathbb R^2\),
\[
 I(q,n)
 \ll
 q^{2/3}n^{2/3}
 +q^{6/11}n^{9/11}
   \log^{2/11}\!\left(2+\frac{q^3}{n}\right)
 +q+n.
\tag{4.3}
\]
Only its exponent form is used below; the logarithm is \(t^{o(1)}\).
The argument is unchanged if one uses the later logarithm-free
pseudo-circle cutting input.

## 5. The finite matching-or-hub mechanism

We first isolate the complete combinatorial step.

### Lemma 2 (finite weighted matching or hub)

Let \(G\) be a simple graph on \(n\) vertices with nonnegative edge
weights \(w_e\le U\), and set
\[
 T=\sum_{e\in E(G)}w_e.
\tag{5.1}
\]
Call an edge rich when
\[
 w_e\ge\frac{T}{4n^2}.
\tag{5.2}
\]
For every integer \(k\ge1\), at least one of the following holds:

1. the rich graph contains a matching of size \(k\);
2. some vertex has rich weighted degree at least
   \[
   \frac{3T}{8k}.
   \tag{5.3}
   \]

Moreover, if \(m\) is the maximum rich matching size, then
\[
 m\ge\frac{3T}{8Un}.
\tag{5.4}
\]

#### Proof

All nonrich edges together have weight less than
\[
 n^2\frac{T}{4n^2}=\frac T4.
\]
Thus rich edges carry at least \(3T/4\).

Take a maximal rich matching.  If it has fewer than \(k\) edges, its
fewer than \(2k\) endpoints form a vertex cover of the rich graph.
The sum of rich weighted degrees over this cover is at least the total
rich edge weight.  One cover vertex therefore has rich weighted degree
at least \((3T/4)/(2k)=3T/(8k)\).  This proves the dichotomy.

For the last assertion, the \(2m\) endpoints of a maximum matching
cover all rich edges, so there are at most \(2mn\) rich edges.  On the
other hand, at least \(3T/4\) rich weight and the cap \(U\) require at
least \(3T/(4U)\) rich edges.  Comparing the two counts proves (5.4).
\(\square\)

### Proposition 3 (codegree-scale matching or a common Euclidean hub)

Under (3.1)--(3.3), fix \(0<\kappa<1\).  At least one of the following
holds:

* **matching alternative:** at least \(t^{1-o(1)}\) labels \(d\) have
  a matching of size \(t^{\kappa-o(1)}\), and every matched edge has
  \[
  W_{e,d}\ge t^{3-o(1)};
  \tag{5.5}
  \]
* **hub alternative:** there are one angle
  \(\alpha\in\mathcal A_t\) and a label set
  \(\mathcal D_0\) such that
  \[
  L:=|\mathcal D_0|=t^{2-2\kappa+o(1)}
  \tag{5.6}
  \]
  and, for every \(d\in\mathcal D_0\),
  \[
  \sum_{\substack{\beta:
       \{\alpha,\beta\}\ {\rm admissible}\\
       W_{\{\alpha,\beta\},d}\ge t^{3-o(1)}}}
  W_{\{\alpha,\beta\},d}
  \ge t^{5-\kappa-o(1)}.
  \tag{5.7}
  \]

#### Proof

Put
\[
 T_d=\sum_{e\ {\rm admissible}}W_{e,d}.
\tag{5.8}
\]
The nonnegative second term inside (3.3) can be discarded, giving
\[
 \sum_dT_d^2\ge t^{13-o(1)}.
\tag{5.9}
\]
There are at most \(t^{3+o(1)}\) labels.  Also, (3.1)--(3.2) give
\[
 T_d\le|\mathcal A_t|^2\max_eW_{e,d}\le t^{6+o(1)}.
\tag{5.10}
\]
Since the weights are integers, the positive \(T_d\)'s occupy only
\(O(\log t)\) dyadic ranges.  Hence one range contains \(L_1\) labels
with
\[
 T\le T_d<2T,\qquad L_1T^2\ge t^{13-o(1)}.
\tag{5.11}
\]
Write \(T=t^{\lambda+o(1)}\).  From the label cap and (5.10),
\[
 5\le\lambda\le6,\qquad
 L_1\ge t^{13-2\lambda-o(1)}.
\tag{5.12}
\]

Apply Lemma 2 to the plane graph for each selected label, using
\[
 n=|\mathcal A_t|=t^{1+o(1)},\qquad
 U=t^{4+o(1)},\qquad
 k=t^{\kappa-o(1)}.
\]
Its rich threshold is
\[
 \frac{T_d}{4n^2}\ge t^{3-o(1)},
\tag{5.13}
\]
which proves the asserted cell richness.

If \(\lambda\ge5+\kappa-o(1)\), (5.4) gives a matching of size
\(t^{\kappa-o(1)}\) for every label in the range.  Equation (5.12) and
\(\lambda\le6+o(1)\) give \(L_1\ge t^{1-o(1)}\), so the matching
alternative holds.

Suppose instead that \(\lambda<5+\kappa+o(1)\).  If at least half the
labels take the matching side of Lemma 2, then (5.12) gives at least
\[
 \frac{L_1}{2}
 \ge t^{3-2\kappa-o(1)}
 \ge t^{1-o(1)}
\tag{5.14}
\]
matching labels.  Otherwise, more than half the labels have a hub
vertex with rich weighted degree
\[
 \gg\frac{T}{t^\kappa}
 \ge t^{5-\kappa-o(1)}.
\tag{5.15}
\]
Choose one hub vertex for each such label and pigeonhole over the
\(t^{1+o(1)}\) planes.  One plane is the chosen hub for at least
\[
 \frac{L_1}{2|\mathcal A_t|}
 \ge t^{12-2\lambda-o(1)}
 \ge t^{2-2\kappa-o(1)}
\tag{5.16}
\]
labels.  Discarding surplus labels gives (5.6), while (5.15) gives
(5.7). \(\square\)

## 6. Euclidean interpretation of a putative hub

We now prove that the hub alternative is impossible for each fixed
\[
 0<\kappa<\frac29.
\tag{6.1}
\]
Fix its source angle \(\alpha\) and rotate coordinates so that
\(\Pi_\alpha\) is the \(xz\)-plane.  Write
\[
 p=(u,z)\in P_\alpha,\qquad
 q=(v,w)\in P_\beta
\tag{6.2}
\]
in signed radial-height coordinates, and put
\[
 c_{\alpha,\beta}=\cos(\alpha-\beta).
\]
The distance equation is
\[
 u^2+v^2-2c_{\alpha,\beta}uv+(z-w)^2=d.
\tag{6.3}
\]

### Lemma 4 (reverse circles and fixed-plane injectivity)

For a target triple \((\beta,q,d)\), equation (6.3), viewed in the
source coordinates \((u,z)\), is the reverse circle
\[
 \Gamma_{\beta,q,d}:\quad
 (u-A)^2+(z-w)^2=\rho^2,
\tag{6.4}
\]
where
\[
 A=c_{\alpha,\beta}v,\qquad
 \rho^2=d-(1-c_{\alpha,\beta}^2)v^2.
\tag{6.5}
\]
For fixed admissible \(\beta\), the map
\[
 (q,d)\longmapsto\Gamma_{\beta,q,d}
\tag{6.6}
\]
is injective among normalized circle equations.

#### Proof

Completing the square in (6.3) gives (6.4)--(6.5).  For fixed
\(\beta\), admissibility gives \(c_{\alpha,\beta}\ne0\).  A normalized
circle determines its centre \((A,w)\) and \(\rho^2\), hence it
determines \(v=A/c_{\alpha,\beta}\), the point \(q=(v,w)\), and then
\[
 d=\rho^2+(1-c_{\alpha,\beta}^2)v^2.
\]
Thus (6.6) is injective. \(\square\)

Discard reverse equations with negative \(\rho^2\), since they have no
source incidences.  A zero-radius equation has at most one source
incidence.  The total number of target triples is at most
\[
 |\mathcal A_t|\,\max_\beta|P_\beta|\,L
 \le t^{6-2\kappa+o(1)}.
\tag{6.7}
\]
The hub incidence mass in (5.7), summed over the \(L\) labels, is at
least
\[
 t^{7-3\kappa-o(1)}.
\tag{6.8}
\]
Because \(\kappa<1\), (6.7) is smaller by a fixed power.  Deleting all
zero-radius equations therefore preserves the lower bound (6.8).

Merge equal normalized positive-radius circles.  For a merged circle
\(C\), define its source richness and production multiplicity by
\[
 s(C)=|P_\alpha\cap C|,
\tag{6.9}
\]
\[
 \mu(C)
 =
 \#\{(\beta,q,d):
       d\in\mathcal D_0,
       \{\alpha,\beta\}\text{ is a rich admissible cell},\
       \Gamma_{\beta,q,d}=C\}.
\tag{6.10}
\]
Lemma 4 gives at most one producing triple for each \(\beta\), so
\[
 \mu(C)\le|\mathcal A_t|=t^{1+o(1)}.
\tag{6.11}
\]
The retained positive-radius mass is
\[
 \sum_Cs(C)\mu(C)\ge t^{7-3\kappa-o(1)},
\tag{6.12}
\]
and the total production multiplicity satisfies
\[
 \sum_C\mu(C)\le t^{6-2\kappa+o(1)}.
\tag{6.13}
\]

### Lemma 5 (tangent-label line reduction)

For a retained circle \(C\), let its centre be \((A(C),w(C))\) and
its squared radius be \(\rho(C)^2>0\).  Put
\[
 \mathcal T_\alpha
 =
 \{\tan^2(\alpha-\beta):
   \{\alpha,\beta\}\text{ occurs in }(6.10)\}.
\tag{6.14}
\]
Then \(|\mathcal T_\alpha|\le t^{1+o(1)}\), and each producer of \(C\)
satisfies
\[
 \boxed{
 d=\rho(C)^2+A(C)^2\tan^2(\alpha-\beta).
 }
\tag{6.15}
\]
Thus \(C\) defines the line
\[
 \ell_C:\quad y=\rho(C)^2+A(C)^2x
\tag{6.16}
\]
in the parameter plane, and
\[
 \mu(C)
 \le
 2\bigl|\ell_C\cap
       (\mathcal T_\alpha\times\mathcal D_0)\bigr|.
\tag{6.17}
\]

#### Proof

Equation (6.5) gives
\[
 d=\rho^2+(1-c_{\alpha,\beta}^2)v^2.
\]
Since \(A=c_{\alpha,\beta}v\) and \(c_{\alpha,\beta}\ne0\),
\[
 (1-c_{\alpha,\beta}^2)v^2
 =A^2\tan^2(\alpha-\beta),
\]
which proves (6.15).  On angles modulo \(\pi\), a value of
\(\tan^2(\alpha-\beta)\) has at most two preimages \(\beta\).
For fixed \(\beta\), Lemma 4 supplies at most one target triple.
Therefore each point of the intersection in (6.17) accounts for at
most two producers. \(\square\)

The off-axis hypothesis and admissibility also give
\[
 A(C)=c_{\alpha,\beta}v\ne0.
\tag{6.18}
\]
In ordinary three-dimensional coordinates, a producing target point
has the useful form
\[
 q=(A,A\tan(\beta-\alpha),w)
\tag{6.19}
\]
after the rotation fixing \(\Pi_\alpha\) as the \(xz\)-plane.

## 7. Dyadic regularization and the fixed-\(A\) lift

Choose a dyadic circle subfamily on which
\[
 s\le s(C)<2s,\qquad
 u\le\mu(C)<2u,
\tag{7.1}
\]
and which retains \(t^{-o(1)}\) of (6.12).  Such a choice exists
because (6.11), \(|P_\alpha|\le t^{3+o(1)}\), and (6.13) allow only
\(O((\log t)^2)\) nonempty dyadic classes.  Write
\[
 s=t^{a+o(1)},\qquad
 u=t^{m+o(1)},\qquad
 N=t^{b+o(1)}
\tag{7.2}
\]
where \(N\) is the number of circles in the selected class.  Then
\[
 a+b+m\ge7-3\kappa-o(1),
\qquad
 b+m\le6-2\kappa+o(1),
\qquad
 m\le1+o(1).
\tag{7.3}
\]
The first two inequalities immediately give
\[
 a\ge1-\kappa-o(1).
\tag{7.4}
\]

Apply the point-circle bound (4.3) to \(P_\alpha\) and these \(N\)
distinct circles.  The source incidence count is
\[
 I(P_\alpha,\mathcal C)=t^{a+b+o(1)}.
\tag{7.5}
\]
The \(q^{2/3}n^{2/3}\) term could carry only if
\[
 m\ge3-5\kappa-o(1),
\tag{7.6}
\]
as follows by multiplying that term by the circle multiplicity \(u\),
using \(q\le t^{3+o(1)}\), and substituting
\(b+m\le6-2\kappa+o(1)\).  For \(\kappa<2/9\), (7.6) contradicts
\(m\le1+o(1)\).  The \(+q\) and \(+n\) terms, after multiplication by
\(u\), have exponents at most \(4+o(1)\) and
\(6-2\kappa+o(1)\), respectively, both below (6.12).  Hence the
\(q^{6/11}n^{9/11}\) term must carry:
\[
 \boxed{11a+2b\le18+o(1).}
\tag{7.7}
\]
Combining (7.3), (7.4), and (7.7) yields
\[
 \boxed{
 a\le\frac{4+6\kappa+2m}{9}+o(1),
 \qquad
 m\ge\frac{5-15\kappa}{2}-o(1).
 }
\tag{7.8}
\]

We now regularize the signed centre fibres.  For a signed pair
\((A,\sigma)\), where \(\sigma>0\), put
\[
 \nu(A,\sigma)
 =
 \#\{C:A(C)=A,\ \rho(C)^2=\sigma\}.
\tag{7.9}
\]
A further dyadic selection retains \(t^{-o(1)}\) of the mass and makes
\[
 \nu(A,\sigma)=t^{h+o(1)}
\tag{7.10}
\]
on every represented signed fibre.  Let
\[
 K=t^{c+o(1)}
\quad\text{and}\quad
 R=t^{r+o(1)}
\tag{7.11}
\]
be, respectively, the number of represented signed fibres
\((A,\sigma)\) and the number of represented signed values of \(A\).
Since each fibre has \(t^{h+o(1)}\) circles,
\[
 b=c+h.
\tag{7.12}
\]

The signed fibres \((A,\sigma)\) map at most two-to-one to the
geometric parameter lines
\[
 y=\sigma+A^2x.
\]
By (6.17), every represented line is \(u/2\)-rich in the point set
\(\mathcal T_\alpha\times\mathcal D_0\), whose size is at most
\[
 t^{1+o(1)}t^{2-2\kappa+o(1)}
 =t^{3-2\kappa+o(1)}.
\tag{7.13}
\]
The lower bound in (7.8) gives \(u\to\infty\).  Applying the rich-line
bound (4.2) and using \(m\le1+o(1)\), the cubic term dominates the
linear term by the fixed exponent
\[
 (6-4\kappa-3m)-(3-2\kappa-m)
 =3-2\kappa-2m
 \ge1-2\kappa-o(1)>0.
\]
Therefore
\[
 \boxed{c\le6-4\kappa-3m+o(1).}
\tag{7.14}
\]

There is also a global target-capacity inequality.  Fix one represented
fibre \((A,\sigma)\).  Its \(t^{h+o(1)}\) distinct circles have
different centre heights \(w\).  Each circle has \(t^{m+o(1)}\)
producers.  Within one circle these producers use distinct target
points, because an off-axis point belongs to a unique axial plane and
Lemma 4 permits only one triple from that plane.  Producers of
different circles have different heights.  By (6.19), all these
target points lie in the ordinary plane \(x=A\).  Thus one fibre uses
\[
 t^{h+m-o(1)}
\tag{7.15}
\]
distinct target points in \(x=A\).

Choose one fibre for every represented \(A\).  The ordinary planes
\(x=A\) are disjoint, while the full target union has at most
\[
 |\mathcal A_t|\max_\beta|P_\beta|\le t^{4+o(1)}
\]
points.  Consequently,
\[
 \boxed{r+h+m\le4+o(1).}
\tag{7.16}
\]
Using (7.12) and (7.14) in (7.16) gives
\[
 \boxed{
 r\le10-4\kappa-b-4m+o(1).
 }
\tag{7.17}
\]

It remains to exploit the fact that circles with one signed \(A\)
have collinear centres.

### Lemma 6 (fixed-\(A\) parabolic lift)

Fix \(A\in\mathbb R\) and define
\[
 \Phi_A(u,z)
 =
 (Z,Y)
 =
 \bigl(z,(u-A)^2+z^2\bigr).
\tag{7.18}
\]
Every fibre of \(\Phi_A\) has size at most two.  A circle
\[
 C:\quad (u-A)^2+(z-w)^2=\rho^2,\qquad \rho>0,
\tag{7.19}
\]
maps to the line
\[
 \lambda_C:\quad
 Y=2wZ+(\rho^2-w^2).
\tag{7.20}
\]
Distinct normalized positive-radius circles with the same signed
\(A\) give distinct lines.  Hence, for any such circle set
\(\mathcal C_A\),
\[
 I(P_\alpha,\mathcal C_A)
 \ll
 |P_\alpha|^{2/3}|\mathcal C_A|^{2/3}
 +|P_\alpha|+|\mathcal C_A|.
\tag{7.21}
\]

#### Proof

Equality of two images under \(\Phi_A\) fixes \(z\) and
\((u-A)^2\), leaving at most two choices for \(u\).  Expanding (7.19)
gives
\[
 (u-A)^2+z^2=2wz+(\rho^2-w^2),
\]
which is (7.20).  Equal lines have equal slopes, hence equal \(w\),
and then equal intercepts, hence equal \(\rho^2\).  Positivity of the
radii makes the circles equal.  Thus
\[
 I(P_\alpha,\mathcal C_A)
 \le2I(\Phi_A(P_\alpha),\{\lambda_C:C\in\mathcal C_A\}),
\]
and (7.21) follows from (4.1). \(\square\)

Let \(N_A=|\mathcal C_A|\).  Summing (7.21) over the \(R\) represented
signed values of \(A\), and applying Hölder to
\(\sum_A N_A^{2/3}\), gives
\[
 \boxed{
 I(P_\alpha,\mathcal C)
 \ll
 t^{2+o(1)}R^{1/3}N^{2/3}
 +t^{3+o(1)}R+N.
 }
\tag{7.22}
\]
The signs \(A\) and \(-A\) are kept separate because their lifts are
different.

## 8. The \(2/9\) scalar closure

The left side of (7.22) has exponent \(a+b+o(1)\).  Therefore at least
one of the following three terms must carry:
\[
 2+\frac r3+\frac{2b}{3},\qquad
 3+r,\qquad
 b.
\tag{8.1}
\]
The \(+N\) branch is impossible by \(a\ge1-\kappa-o(1)>0\).

Suppose the \(+t^3R\) branch carries.  Then
\[
 a+b\le3+r+o(1).
\tag{8.2}
\]
Using (7.17), (7.3), and then (7.8), successively, gives
\[
 a\ge2m+1-2\kappa-o(1),
\tag{8.3}
\]
\[
 m\le\frac{24\kappa-5}{16}+o(1).
\tag{8.4}
\]
For \(\kappa<2/9\), (8.4) gives \(m<1/48+o(1)\), whereas (7.8) gives
\[
 m>\frac56-o(1).
\]
Thus the \(+t^3R\) branch is impossible.

The main term in (7.22) must carry, so
\[
 3a+b\le6+r+o(1).
\tag{8.5}
\]
Substitute (7.17):
\[
 3a+2b+4m\le16-4\kappa+o(1).
\tag{8.6}
\]
Twice the mass inequality in (7.3) is
\[
 2a+2b+2m\ge14-6\kappa-o(1).
\tag{8.7}
\]
Subtracting (8.7) from (8.6) yields
\[
 a+2m\le2+2\kappa+o(1).
\tag{8.8}
\]
Together with (7.4), this gives the upper bound
\[
 \boxed{
 m\le\frac{1+3\kappa}{2}+o(1).
 }
\tag{8.9}
\]
But (7.8) gives the lower bound
\[
 \boxed{
 m\ge\frac{5-15\kappa}{2}-o(1).
 }
\tag{8.10}
\]
The fixed parts of (8.9)--(8.10) are compatible only if
\[
 5-15\kappa\le1+3\kappa,
\]
or
\[
 \kappa\ge\frac29.
\tag{8.11}
\]
This contradicts (6.1).  Hence the hub alternative in Proposition 3
cannot occur for any fixed \(\kappa<2/9\).

To finish Theorem 1, take
\[
 \kappa=\frac29-\varepsilon.
\]
Proposition 3 must take its matching alternative, which is exactly
(3.5)--(3.7). \(\square\)

## 9. Why the endpoint is not included

The strictness in Theorem 1 is intrinsic to the scalar inequalities
just used.  At \(\kappa=2/9\), the following exponent assignment
satisfies every capacity and incidence inequality in Sections 7--8:
\[
 \begin{array}{c|c|l}
 \text{symbol}&\text{exponent}&\text{quantity}\\ \hline
 a&7/9&s=t^a\\
 b&85/18&N=t^b\\
 m&5/6&u=t^m\\
 c&47/18&K=t^c\\
 h&19/9&\text{circles per signed fibre}\\
 r&19/18&R=t^r\\
 \ell&14/9&L=t^\ell.
 \end{array}
\tag{9.1}
\]
Indeed,
\[
 \begin{aligned}
 a+b+m&=7-3\kappa,\\
 b+m&=6-2\kappa,\\
 11a+2b&=18,\\
 b&=c+h,\\
 c&=6-4\kappa-3m,\\
 r+h+m&=4,\\
 3a+b&=6+r,\\
 \frac{5-15\kappa}{2}
 &=m=\frac{1+3\kappa}{2}.
 \end{aligned}
\tag{9.2}
\]
This is an exponent-feasibility ledger, not a Euclidean
configuration.  It proves only that the present scalar closure cannot
exclude the hub at the endpoint.

## 10. Exact claim boundary

### Proved here

* Under the explicit geometric size assumptions, cell cap, and
  pair-codegree hypothesis (3.1)--(3.3), every fixed exponent strictly
  below \(2/9\) occurs as a rich axial-plane matching exponent for at
  least \(t^{1-o(1)}\) labels.
* The matching uses pairwise disjoint plane pairs; consequently its
  first two edges give four distinct axial planes.
* Equal and perpendicular plane pairs are absent by definition, and
  all point sets are off the common axis.
* The finite weighted matching-or-hub lemma, reverse-circle
  construction, tangent-label reduction, target-capacity step, and
  fixed-\(A\) lift are proved in this note.

### Assumed, not proved here

* The critical pair-codegree lower bound (3.3).
* The nonexceptional cell cap (3.2).
* Any reduction from a general three-dimensional few-distance
  configuration to the axial hypotheses (3.1)--(3.3).
* The two standard planar incidence theorems in Section 4.

### Not claimed

* Hub exclusion at \(\kappa=2/9\), or a matching exponent with no
  fixed loss below \(2/9\).
* Euclidean realizability of the endpoint ledger (9.1).
* An improvement of the known \(3/5\) lower-bound exponent for the
  three-dimensional distinct-distance problem.
* A solution of Erdős problem #1083, a classification of
  near-extremizers, a priority claim, or a claim of journal-level
  significance.

The theorem is therefore a **conditional structural matching
theorem**, with its condition and its conclusion both fully exposed.
