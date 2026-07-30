# Independent attack: the cosine--radial repeated-circle chart

Date: 2026-07-30

Source audited:
`EUCLIDEAN_HUB_INCIDENCE_EXPANSION_THEOREM.md`, especially
equations (23)--(25).

## 0. Verdict

The repeated-circle extraction has a stronger elementary geometric
interpretation than is stated in the source:

* multiplicity \(\mu\) forces exactly \(\mu\) distinct target axial
  planes (and hence \(\mu\) distinct plane angles);
* it forces at least \(\lceil\mu/2\rceil\) distinct ordinary radii and
  at least \(\lceil\mu/2\rceil\) distinct distance labels;
* the \(\mu\) target points themselves determine at least
  \(\mu-1\) distinct distances.

These bounds are optimal.  They do **not** yield superlinear
expansion and do not activate either the cyclotomic-fibre theorem or
the weighted rational-chord theorem at useful density.  The exact
obstruction is a circle together with its perpendicular axis, a
three-dimensional Lenz-type configuration.

At the extracted exponent
\[
 \mu\geq t^{(5-15\kappa)/2-o(1)}
 \qquad(1/5\leq\kappa<1/3),
\tag{1}
\]
the direct label bound is much weaker than the already available
\[
 |\mathcal D_0|=L=t^{2-2\kappa-o(1)}.
\tag{2}
\]
Indeed
\[
 (2-2\kappa)-\frac{5-15\kappa}{2}
 =\frac{11\kappa-1}{2}>0.
\tag{3}
\]
Thus the repeated-circle chart is genuine structure, but by itself it
does not improve the distinct-distance exponent.

## 1. Strongest unconditional normal-form lemma

### Lemma (orthogonal circle--axis normal form)

Fix the source axial plane \(\Pi_\alpha\).  Suppose one normalized
reverse-circle equation occurs for \(\mu\) triples
\[
 (\beta_i,q_i,d_i),\qquad 1\leq i\leq\mu,
\]
where \(\beta_i\ne\alpha\), \(q_i\) is off the common axis, and
\(\cos(\alpha-\beta_i)\ne0\).

Choose horizontal Cartesian coordinates so that \(\Pi_\alpha\) is
the \(xz\)-plane, and write
\[
 q_i=(v_i\cos(\beta_i-\alpha),
      v_i\sin(\beta_i-\alpha),w_i).
\]
Then there are constants \(A\ne0,w_0,C\) and pairwise distinct real
numbers \(y_1,\ldots,y_\mu\) such that
\[
\boxed{
 q_i=(A,y_i,w_0),\qquad
 v_i^2=A^2+y_i^2,\qquad
 d_i=A^2+y_i^2-C.
}
\tag{4}
\]
The common normalized circle is
\[
\boxed{
 (u-A)^2+(z-w_0)^2=A^2-C
}
\tag{5}
\]
in \(\Pi_\alpha\).

Consequently:

\[
\boxed{
 \begin{aligned}
 &|\{\beta_i\}|=\mu,\\
 &|\{|v_i|\}|=|\{d_i\}|
   =|\{y_i^2\}|\geq\lceil\mu/2\rceil,\\
 &|\Delta^2(\{q_1,\ldots,q_\mu\})|\geq\mu-1.
 \end{aligned}}
\tag{6}
\]
In particular, every such repeated circle obeys the useful absolute
caps
\[
\boxed{
 \mu\leq |\mathcal A|-1,
 \qquad
 \mu\leq2|\mathcal D_0|.
}
\tag{6a}
\]

If the common circle has \(s\) source incidences, all \(s\mu\)
source--target pairs in the resulting complete bipartite block use
only \(|\{d_i\}|\) cross-distance labels.

### Proof

Equality of normalized reverse circles is exactly
\[
 c_i v_i=A,\qquad w_i=w_0,\qquad v_i^2-d_i=C,
\qquad c_i=\cos(\alpha-\beta_i).
\tag{7}
\]
In the chosen Cartesian coordinates, the first horizontal coordinate
of \(q_i\) is \(c_iv_i=A\).  Put
\[
 y_i=v_i\sin(\beta_i-\alpha).
\]
Then \(v_i^2=A^2+y_i^2\), and (7) gives (4).
Completing the two squares in the normalized equation gives (5).

Because \(q_i\) is off-axis and \(c_i\ne0\), (7) gives \(A\ne0\).
Lemma 1 of the source theorem says that, for fixed \(\beta\), the map
\((q,d)\mapsto\Gamma_{\beta,q,d}\) is injective.  Hence the \(\mu\)
triples use \(\mu\) distinct planes.  Since
\[
 \tan(\beta_i-\alpha)=y_i/A
\]
modulo the axial-plane period \(\pi\), their \(y_i\)'s are pairwise
distinct.

Each value of \(y_i^2\) has at most two preimages.  Formula (4) then
proves the radius and label bounds in (6).  Finally, order the
\(y_i\)'s.  The \(\mu-1\) distances from the leftmost target point to
the other target points have pairwise distinct lengths, proving the
last line of (6).

If \(p=(u,0,z)\) lies on (5), then
\[
 |p-q_i|^2
 =(u-A)^2+(z-w_0)^2+y_i^2
 =A^2-C+y_i^2=d_i.
\tag{8}
\]
Thus every incident source point pairs with every target point, while
the cross labels remain precisely the values \(d_i\). \(\square\)

## 2. Exact saturation model

Fix integers \(n\geq3\), \(m\geq1\), real numbers
\[
 a>r>0,\qquad h>0,
\]
and let \(\alpha\) be the \(xz\)-plane.  Put a regular \(n\)-gon on
the circle
\[
 S_n=
 \left\{
 \left(
 a+r\cos\frac{2\pi k}{n},\
 0,\
 r\sin\frac{2\pi k}{n}
 \right):0\leq k<n
 \right\}.
\tag{9}
\]
All these points are off the common \(z\)-axis because \(a>r\).

Let
\[
 J_m=\{\pm1,\pm3,\ldots,\pm(2m-1)\}
\tag{10}
\]
and place \(2m\) target points on the line perpendicular to
\(\Pi_\alpha\) through the circle centre:
\[
 T_m=\{q_j=(a,hj,0):j\in J_m\}.
\tag{11}
\]
The target point \(q_j\) lies in the distinct axial plane
\[
 \beta_j=\arctan(hj/a)\pmod\pi,
\]
and
\[
 v_j^2=a^2+h^2j^2,\qquad
 c_j=\frac a{v_j}\ne0.
\tag{12}
\]
Set
\[
 C=a^2-r^2,\qquad
 d_j=v_j^2-C=r^2+h^2j^2.
\tag{13}
\]
Take \(\mathcal D_0=\{d_j:j\in J_m\}\).  With one target point on
each plane \(\beta_j\), no other triple in this selected family can
produce (14).
Every one of the \(2m\) triples
\((\beta_j,q_j,d_j)\) produces the same normalized reverse circle
\[
 (u-a)^2+z^2=r^2.
\tag{14}
\]
Thus this circle has multiplicity
\[
 \boxed{\mu=2m}
\tag{15}
\]
and has all \(n\) source points as incidences.  It contributes exactly
\(2mn=n\mu\) source--target representations.

At the same time,
\[
 |\{d_j:j\in J_m\}|
 =|\{|v_j|:j\in J_m\}|
 =m=\mu/2.
\tag{16}
\]
The \(y\)-coordinates in (11) form an arithmetic progression of
length \(2m\), so their nonzero squared-distance set has exactly
\[
 2m-1=\mu-1
\tag{17}
\]
elements.  Hence every lower bound in (6) is attained.

The entire configuration \(S_n\cup T_m\) still has only linearly many
distinct squared distances:

* \(S_n-S_n\) contributes at most \(\lfloor n/2\rfloor\) regular-polygon
  chord values;
* \(T_m-T_m\) contributes exactly \(2m-1\) values;
* \(S_n-T_m\) contributes the \(m\) values in (13).

Therefore
\[
\boxed{
 |\Delta^2(S_n\cup T_m)|
 \leq
 \lfloor n/2\rfloor+3m-1
 =O(n+\mu).
}
\tag{18}
\]
This remains valid with arbitrarily large \(n\) and \(\mu\).  In
particular, even \(n\mu\) equal-circle incidences do not force
superlinear distance growth.

## 3. Why the existing arithmetic theorems do not amplify the chart

### 3.1 Weighted rational-chord theorem

The repeated-circle relation is a fixed **projection**
\[
 \rho_i\cos(\beta_i-\alpha)=A,
\tag{19}
\]
not a common-radius relation.  Equation (6) shows that a fixed
ordinary radius can occur on at most two target rays.

In the saturation model, every occupied target radius supports exactly
the symmetric pair \(\beta_j,\beta_{-j}\), with one height on each ray.
Hence its ordered radial overlap is
\[
 \Omega_{\rm cyl}=2m=\mu,
\]
while the target subsystem has \(2m=\mu\) occupied rays.  The full
configuration also contains the source ray \(\alpha\), so its total
ray count is \(2m+1\); under the radial-support separation imposed
below that extra ray adds no target radial overlap and only enlarges
the denominator in the rational-chord bound.
Even when all chord and height coordinates are rational and the chord
multiplicity is \(K=1\), the bound
\[
 \frac{\Omega_{\rm cyl}}
 {|\mathcal J|L_UKT_2}
\]
is only \(O(1)\).  No polynomial expansion follows.

If desired, choose \(h\) so large that
\[
 \sqrt{a^2+h^2}>a+r.
\]
Then the target radii are disjoint from every source radius in
\(S_n\), so the source circle supplies no missing same-radius overlap.

### 3.2 Cyclotomic-fibre theorem

The cosine--radial equation imposes no root-of-unity orbit, prime
cyclic angular group, or coefficient-field independence.  The
parameters
\[
 y_i=A\tan(\beta_i-\alpha)
\]
may be an arbitrary finite set of distinct real numbers.

Even if additional assumptions placed the angles in a prime
cyclotomic group, each ordinary radius supports at most two target
angles and only one height.  The partial-fibre theorem would therefore
return at most a constant per radius, hence only \(O(\mu)\) labels.
That is already sharp by (16)--(18).

### 3.3 Sum-product or rational-angle arguments

The chart reduces to an arbitrary real set \(Y=\{y_i\}\) on one line:
\[
 d_i=(A^2-C)+y_i^2,\qquad
 |q_i-q_j|^2=(y_i-y_j)^2.
\tag{20}
\]
Taking \(Y\) to be the arithmetic progression (10) simultaneously
makes \(|Y-Y|=O(|Y|)\), gives exactly \(|Y|/2\) values of \(Y^2\),
and realizes (18).  Therefore no sum-product statement using only
(20) can force a superlinear distance set.  The fixed-rational-angle
theorem is likewise inapplicable: the angles vary with \(i\), and no
common angular step is forced.

## 4. Precise remaining target

The repeated-circle chart can contribute to an exponent improvement
only after adding information that rules out the orthogonal
circle--axis saturation.  A sufficient next lemma would have to force
at least one of:

1. superlinear additive expansion of the transverse coordinates
   \(Y\);
2. polynomially many target rays on many common ordinary radii, not
   merely the two allowed by one repeated circle;
3. many distinct repeated circles whose transverse sets are
   arithmetically incompatible; or
4. a quantitative restriction preventing the incident source set
   from concentrating on a regular (or otherwise few-distance)
   circle.

None of these conclusions follows from multiplicity \(\mu\), equations
(24)--(25), or the current cyclotomic/rational-chord theorems alone.
