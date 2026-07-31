# Erdős #1083 Route D: cross-height energy and the true Euclidean barrier

Date: 2026-07-30

## 0. Outcome

The cross-centre formula does not, by itself, exclude the \(9/41\)
endpoint.  There is an exact Euclidean reverse-circle fibre in which
every one of \(H\) radius-one circles has \(S\) source incidences and
\(U\) producing target triples, while \(S\) points on one additional
radius-one circle and the \(UH\) target points determine only
\[
\boxed{O(UH)}
\]
cross distances when \(S\le U\).  Thus no factor \(S^\delta\) can be
deduced from the formula and the three cardinalities alone.

The model deliberately uses \(UH\) different axial target planes and
selected labels.  It therefore does **not** realize the Route B
endpoint, where only \(M=t^{1+o(1)}\) target planes are available.
This locates the remaining usable resource exactly: the same small
global set of tangent-square coordinates must be reused over very
many centre heights.

That reuse gives a rigorous new structural conclusion.  In a genuine
fixed-\((A,\rho)\) parameter-line fibre, suppose:

- a chosen source circle contains \(S\) source points;
- there are \(H\) other centre heights;
- every height row contains at least \(U\) target points;
- all row tangent squares lie in one global set of size \(R\le M\);
- the resulting cross-distance set has size at most \(D\).

At the \(9/41\) endpoint,
\[
(S,U,H,R,D)
=
t^{(32,35,88,41,123)/41+o(1)}.
\]
Then Cauchy--Schwarz forces at least
\[
t^{187/41-o(1)}
\]
distance collisions.  A multi-dilate additive-energy theorem bounds
all collisions staying at one centre height by
\[
t^{161/41+o(1)}.
\]
Hence a \(1-t^{-26/41+o(1)}\) proportion at exponent scale must be
**cross-height collisions**.  Any endpoint exclusion must bound those
relations; same-height sum-product cannot do it.

There is also a sharp exact-saturation lemma.  If every height row has
the smallest possible sumset with the source sine set, then
\[
\boxed{H\le R(R-1).}
\]
The endpoint violates this by \(t^{6/41-o(1)}\).  This rules out
literal row-by-row equality, but not near equality, so it is not yet
an endpoint exclusion.

## 1. Exact Euclidean formula

Rotate the source axial plane to \(y=0\).  Fix a positive-radius
circle
\[
C:\quad (u-A)^2+(z-w)^2=\rho^2
\]
and write its retained source points as
\[
p_x=(A+\rho\cos\phi,0,w+\rho\sin\phi),
\qquad x=\sin\phi.
\]
For a target point in the same signed-slope fibre,
\[
q=(A,y,w'),
\]
put \(z=w-w'\) and \(\tau=y^2\).  Direct expansion gives
\[
\begin{aligned}
\|p_x-q\|^2
&=\rho^2\cos^2\phi+\tau+(z+\rho\sin\phi)^2\\
&=\boxed{\rho^2+\tau+z^2+2\rho zx}.
\end{aligned}
\tag{1}
\]

If \(C\) contains \(S\) distinct source points, their sine values form
a set \(X\) with
\[
|X|\ge S/2,
\tag{2}
\]
because a fixed sine has at most two preimages on a circle.  Constants
of two will be suppressed below.

For a fixed parameter-line fibre \((A,\rho^2)\), let \(Z\) be the set
of centre-height differences from \(C\).  At height \(z\), let
\[
T_z=\{y(q)^2:q\text{ is a retained target point at that height}\}.
\tag{3}
\]
Fixed-plane injectivity makes the target points in a row distinct.
Squaring can identify at most the two transverse coordinates \(y\)
and \(-y\), so \(|T_z|\ge\mu(C_z)/2\); this absolute factor is
absorbed when \(U\) denotes the row scale.
All \(T_z\)'s are contained in the global tangent-square set
\[
T_\ast
=
\{A^2\tan^2(\beta-\alpha):
  \beta\text{ is a retained target plane}\},
\qquad |T_\ast|=:R\le M.
\tag{4}
\]

The cross-distance set under discussion is therefore
\[
\mathcal V
=
\bigcup_{z\in Z}
\left(\rho^2+z^2+T_z+2\rho zX\right)
\subseteq\Delta^2(P).
\tag{5}
\]

## 2. The generic one-step bounds are far below the endpoint

Even in the stronger Cartesian-product situation \(T_z=T\), equation
(5) is the polynomial image
\[
T+Z^2+2\rho ZX.
\tag{6}
\]
Regarding \(v=t+z^2+2\rho zx\) as a point--line incidence gives the
standard bound
\[
|T+Z^2+2\rho ZX|
\gg (|T||X||Z|)^{1/2}
\tag{7}
\]
up to the usual lower-order alternatives.  At the endpoint its
exponent is only
\[
\frac12\frac{35+32+88}{41}
=\frac{155}{82}<3.
\tag{8}
\]

Likewise, the asymmetric Elekes--Rónyai bound applied to
\(z^2+2\rho zx\) is at most useful at the scale
\[
\min\{
|X|^{2/3}|Z|^{2/3},|X|^2,|Z|^2
\}.
\tag{9}
\]
At the endpoint the minimum is \(|X|^2=t^{64/41+o(1)}\).
Consequently, citing a generic polynomial-expansion theorem cannot
produce the required \(t^{3+\delta}\) distances in this range.

## 3. A real Euclidean cancellation model

### Proposition 1

For every integers
\[
2\le S\le U,\qquad H\ge2,
\]
there are:

- \(S\) distinct points on one positive-radius circle in \(y=0\);
- \(UH\) distinct target points in the ordinary plane \(x=A\);
- \(H\) distinct target heights, with \(U\) points at each height;

such that the number of squared distances from the source points to
the target points is at most
\[
\boxed{H(S+U-1)\le2UH.}
\tag{10}
\]
All source and target points can be chosen off the common axis, and
all target axial planes can be chosen nonperpendicular to the source
plane.  Moreover, after adding a translated \(S\)-point copy on each
of the \(H\) unit circles, every target row genuinely produces that
rich reverse circle with multiplicity \(U\).

### Proof

Take \(\rho=1\), \(w=0\), and \(A>1\).  Choose an integer
\[
K>2UH.
\]
For \(1\le i\le S\), choose the source point on the circle with
\[
\sin\phi_i=\frac iK,\qquad \cos\phi_i>0.
\tag{11}
\]
These are distinct off-axis points.

Put
\[
C_0=H^2+1.
\]
For \(1\le z\le H\) and \(1\le j\le U\), define
\[
\tau_{z,j}
=
C_0-z^2+\frac{2zj}{K}>0
\tag{12}
\]
and the target point
\[
q_{z,j}=(A,\sqrt{\tau_{z,j}},-z).
\tag{13}
\]
Every such point lies on \(x=A\), is off-axis, and determines a
nonperpendicular axial target plane because \(A\ne0\).

Equation (1) gives
\[
\|p_i-q_{z,j}\|^2
=
1+C_0+\frac{2z(i+j)}K.
\tag{14}
\]
For fixed \(z\), the integer \(i+j\) takes only
\(S+U-1\) values.  Summing this upper bound over \(H\) heights proves
(10).

Translate the same source angular set to every circle
\[
C_z:\quad (u-A)^2+(v+z)^2=1
\]
by putting
\[
p_{z,i}=(A+\cos\phi_i,0,-z+\sin\phi_i).
\tag{14a}
\]
Give \(q_{z,j}\) the selected squared label
\[
d_{z,j}=1+\tau_{z,j}.
\tag{14b}
\]
Then
\[
\|p_{z,i}-q_{z,j}\|^2
=
\cos^2\phi_i+\tau_{z,j}+\sin^2\phi_i
=d_{z,j}.
\tag{14c}
\]
The reverse circle of \((q_{z,j},d_{z,j})\) in the source plane is
exactly \(C_z\).  Hence \(C_z\) has \(S\) retained source incidences
and \(U\) producing triples after the translated points are included
in the source set.

It remains to check that the target points, and in fact their axial
planes, are distinct.  If
\(\tau_{z,j}=\tau_{z',j'}\), then
\[
K(z'^2-z^2)=2(z'j'-zj).
\tag{15}
\]
When \(z\ne z'\), the nonzero left side has absolute value at least
\(K\), while the right side has absolute value at most \(2UH<K\), a
contradiction.  When \(z=z'\), equation (15) gives \(j=j'\).
Thus all \(UH\) positive \(y\)-coordinates, hence all target axial
planes, are distinct. \(\square\)

### What the model does and does not show

This is a genuine Euclidean reverse-circle subconfiguration, not a
formal sum-product model.  It has a fixed signed centre coordinate
\(A\), \(H\) rich positive-radius circles on one signed parameter
line, \(U\) producing triples per circle, valid axial target planes,
and exact Cartesian squared distances.

It does **not** embed the full Route B endpoint.  It consumes
\[
UH
\tag{16}
\]
target planes, while Route B permits only \(M\).  At the endpoint,
\[
UH=t^{123/41+o(1)}
\quad\text{but}\quad
M=t^{41/41+o(1)}.
\tag{17}
\]
It also does not assert simultaneous source point--circle incidence
saturation across all signed \(A\)'s or the small selected-label
budget: it has \(UH\) distinct labels \(d_{z,j}=1+\tau_{z,j}\).
Therefore Proposition 1 refutes a formula-plus-cardinalities argument
even inside one genuine rich reverse-circle fibre.  It does not
refute a theorem that genuinely uses global target-plane and
selected-label reuse.

## 4. Same-height energy is negligible at \(9/41\)

For finite real sets \(A,B\), write
\[
E^+(A,B)
=
\#\{(a,b,a',b')\in A\times B\times A\times B:
  a+b=a'+b'\}.
\tag{18}
\]

We use the following real Szemerédi--Trotter consequence of Murphy,
Roche-Newton and Shkredov, *Variations on the sum-product problem*,
Lemma 2.3:
\[
\sum_{\lambda\in\Lambda}E^+(A,\lambda B)
\ll
|A|^{3/2}|B|^{3/2}|\Lambda|^{1/2},
\qquad |\Lambda|\le|A||B|.
\tag{19}
\]
The zero dilation, if present, is deleted and handled separately.

### Theorem 2 (cross-height collision forcing)

Use the genuine fibre setup (2)--(5).  Assume
\[
|X|=S,\quad |Z|=H,\quad |T_\ast|=R,\quad
|T_z|\ge U\quad(z\in Z),
\tag{20}
\]
and \(H\ge RS\).  Let \(\mathcal E\) count all ordered collisions
\[
\tau+z^2+2\rho zx
=
\tau'+z'^2+2\rho z'x',
\tag{21}
\]
where \(z,z'\in Z\), \(\tau\in T_z\), \(\tau'\in T_{z'}\), and
\(x,x'\in X\).  Let \(\mathcal E_{\rm same}\) be the subcount with
\(z=z'\).  Then
\[
\boxed{
\mathcal E\ge\frac{S^2U^2H^2}{|\mathcal V|},
\qquad
\mathcal E_{\rm same}\ll RSH.
}
\tag{22}
\]
Consequently, if \(|\mathcal V|\le K U H\), then
\[
\boxed{
\mathcal E-\mathcal E_{\rm same}
\ge
\frac{S^2UH}{K}-O(RSH).
}
\tag{23}
\]

### Proof

There are at least \(SUH\) tuples \((x,z,\tau)\) in (5).
Cauchy--Schwarz over their values proves the first inequality in
(22).

At one fixed nonzero height \(z\), deleting the common translation
\(\rho^2+z^2\) shows that its collision count is
\[
E^+(T_z,2\rho zX)
\le E^+(T_\ast,2\rho zX).
\tag{24}
\]
Partition the nonzero dilations \(2\rho Z\) into blocks of cardinality
at most \(RS\).  Apply (19) to every block with
\(A=T_\ast\), \(B=X\).  A full block contributes at most
\[
(RS)^{3/2}(RS)^{1/2}=(RS)^2.
\]
Since \(H\ge RS\), summing the blocks gives \(O(RSH)\).  A possible
zero-height row is handled directly: its value is independent of
\(x\), so it contributes at most \(R S^2\le RSH\).  This proves the
second inequality in (22), and (23) follows. \(\square\)

### Endpoint substitution

The enriched Route B equality ledger gives
\[
(S,U,H,R,D)
=
t^{(32,35,88,41,123)/41+o(1)}.
\tag{25}
\]
Here \(H\ge RS\) with a gap \(15/41\).  If
\(|\mathcal V|\le D=t^{123/41+o(1)}=UH\,t^{o(1)}\), then (22) forces
\[
\mathcal E
\ge
t^{187/41-o(1)}.
\tag{26}
\]
On the other hand,
\[
\mathcal E_{\rm same}
\ll
t^{(41+32+88)/41+o(1)}
=t^{161/41+o(1)}.
\tag{27}
\]
The exponent gap is
\[
\boxed{\frac{187-161}{41}=\frac{26}{41}.}
\tag{28}
\]
Thus essentially all endpoint compression must be carried by
different-height solutions of (21).  This is an unconditional
necessary condition on any uniform endpoint fibre.

### The new \(2/9\) live endpoint

The later fixed-centre linearization moves the scalar endpoint to
\(\kappa=2/9\), with
\[
(S,U,H,R,D)
=
t^{(7/9,\,5/6,\,19/9,\,1,\,3)+o(1)}.
\tag{28a}
\]
The fibre contains \(UH=t^{53/18+o(1)}\) target points and
\(SUH=t^{67/18+o(1)}\) source--target tuples.  If the distance budget
remains \(D=t^{3+o(1)}\), Cauchy--Schwarz requires collision exponent
\[
2\cdot\frac{67}{18}-3=\frac{40}{9}.
\tag{28b}
\]
The same-height energy bound has exponent only
\[
1+\frac79+\frac{19}{9}=\frac{35}{9}.
\tag{28c}
\]
Thus the live endpoint still forces a cross-height energy gap of
\[
\boxed{\frac59.}
\tag{28d}
\]
Literal row-minimality below also fails because
\[
\frac{19}{9}-2=\frac19.
\tag{28e}
\]
Accordingly, the localization survives the stronger \(2/9\)
argument; it does not itself move that endpoint.

## 5. Literal row-minimality is impossible

The elementary one-dimensional sumset inequality says
\[
|A+B|\ge|A|+|B|-1.
\tag{29}
\]
For two finite real sets of sizes at least two, equality holds only
when both are arithmetic progressions with the same common
difference, up to sign.

### Theorem 3 (exact minimal-row cap)

In the setup of Theorem 2, suppose \(S,U\ge2\), all height
differences are nonzero, and every row is exactly minimal:
\[
|T_z+2\rho zX|=U+S-1,
\qquad |T_z|=U.
\tag{30}
\]
Then
\[
\boxed{H\le R(R-1).}
\tag{31}
\]

### Proof

Equality in (29) implies first that \(X\) is an arithmetic
progression, say with positive gap \(\delta\), and then that every
\(T_z\) is an arithmetic progression whose endpoint difference is
\[
(U-1)\,2\rho |z|\delta.
\tag{32}
\]
The endpoints belong to \(T_\ast\).  Distinct absolute values
\(|z|\) give distinct unordered endpoint pairs in \(T_\ast\), of
which there are at most \(\binom R2\).  Each absolute value has at
most the two signed preimages \(z,-z\).  Hence
\[
H\le2\binom R2=R(R-1).
\]
\(\square\)

At the endpoint,
\[
H=t^{88/41+o(1)},\qquad R^2=t^{82/41+o(1)},
\tag{33}
\]
so (31) fails by the fixed power \(t^{6/41-o(1)}\).
This proves that exact row-by-row Cauchy--Davenport equality cannot
underlie the endpoint.

The statement is deliberately not upgraded to a near-equality claim.
Since \(U/S=t^{3/41+o(1)}\), a bound of the form
\(|T_z+2\rho zX|\le C U\) has much more slack than the exact minimum
\(U+S-1\).  A quantitative inverse theorem strong enough in this
unbalanced regime would be a genuinely new input.

## 6. Precise remaining target

Theorem 2 reduces the cross-centre continuation to the following
finite real problem.

> Bound the number of cross-height solutions of
> \[
> \tau-\tau'
> =
> z'^2-z^2+2\rho(z'x'-zx),
> \]
> where \(T_z,T_{z'}\subset T_\ast\), \(|T_\ast|=R\),
> \(|T_z|,|T_{z'}|\asymp U\), \(|X|=S\), and \(|Z|=H\).
> A bound \(o(S^2UH)\) by any fixed power at the exponents (25)
> excludes the \(9/41\) endpoint.

Proposition 1 shows why the global constraint
\(T_z\subset T_\ast\), \(|T_\ast|\le M\), cannot be discarded.
Theorem 3 shows that literal minimal sumsets cannot satisfy it.
Theorem 2 shows that all remaining compression has to manifest as a
large cross-height parabolic-affine energy.  No available generic
sum-product or Elekes--Rónyai estimate gives the required upper bound
in this highly unbalanced range.

## 7. Claim boundary

### Proved

- the exact Euclidean cross-centre identity (1);
- the sine-fibre loss of at most two (2);
- the genuine Euclidean \(O(UH)\) cancellation model;
- the model's exact failure of the Route B \(M\)-plane constraint;
- the cross-height collision-forcing theorem (22)--(23);
- the \(26/41\) same-height energy gap at the endpoint;
- the exact minimal-row cap \(H\le R(R-1)\);
- the resulting \(6/41\) endpoint contradiction under literal
  row-minimality.

### Not proved

- an upper bound with a power saving for the cross-height energy;
- a stability version of Theorem 3 in the required unbalanced range;
- Euclidean realizability or exclusion of the complete \(9/41\)
  endpoint ledger;
- any improvement of the global \(3/5\) distinct-distance exponent.

## 8. Reproduction

```bash
cd data/research_open/erdos1083_two_hour_q1_attack_2026-07-30/route_d
python3 verify_cross_height_energy.py
pytest -q test_verify_cross_height_energy.py
```
