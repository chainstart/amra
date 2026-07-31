# Erdős #1083 Route B, stage 2: signed-slope aggregation at \(9/41\)

Date: 2026-07-30

## 0. Outcome

The tangent--label argument admits a genuine aggregation over all
parallel parameter lines with one fixed signed slope \(A\).

Let \(X_A\) be the set of target points used by circles whose centre
has signed radial coordinate \(A\).  Then
\[
\boxed{
\sum_{C:A(C)=A}\mu(C)\le L|X_A|.
}
\tag{1}
\]
Indeed, a fixed target point \(q=(A,y,w)\) and a fixed selected label
\(d\) determine the unique parameter-line intercept
\[
b=d-y^2.
\tag{2}
\]
Thus one target point participates in at most \(L\) parallel
parameter lines.

Since \(X_A\) is contained in the plane \(x=A\), and distances in
that plane are distances of the original configuration,
\[
|X_A|\ll D\log(2D).
\tag{3}
\]
Different signed \(A\)'s give disjoint planes, so also
\[
\sum_A|X_A|\le MQ.
\tag{4}
\]

For a dyadic circle layer with \(s(C)<2s\), if \(R\) signed slopes
occur, (1)--(4) yield
\[
\boxed{
W_{s,u}
\ll
sL\min\{RD\log(2D),\,MQ\}.
}
\tag{5}
\]

This is the strongest unconditional slope-aggregate inequality
obtained in this attack.  It does **not** move the strict threshold
beyond \(9/41\).  At \(\kappa=9/41\), there is a simultaneous equality
assignment for the exponents in (5), the parameter-line
Szemerédi--Trotter bound, the planar target-fibre cap, the
point--circle bound, and total target capacity.

The stage therefore ends with a sharp **method barrier**, not a new
distinct-distance exponent:

> Any improvement beyond \(9/41\) must use compatibility absent from
> the present ledgers—most plausibly a quantitative incompatibility
> between near-extremal Cartesian-product point--line incidence,
> near-minimal planar distances in the \(x=A\) fibres, and the same
> target points serving many selected labels.

The aggregate label constraint alone has no power saving.  A finite
interval model in Section 6 loses only a vanishing fraction
\(O(U/J)\) while using \(U\) different tangent-square values.

## 1. Setup

Use the notation and all inherited removals in
`TANGENT_LABEL_RICH_LINE_HUB_THEOREM.md`.

In particular:

- \(\Pi_\alpha\) is the fixed source plane;
- all retained points are off the common axis;
- the perpendicular target plane is absent;
- \(C\subset\Pi_\alpha\) is a merged positive-radius reverse circle;
- \(A(C)\ne0\) is the signed radial coordinate of its centre;
- \(\rho(C)>0\) is its radius;
- \(s(C)=|P_\alpha\cap C|\);
- \(\mu(C)\) counts producing triples
  \((\beta,q,d)\), \(d\in\mathcal D_0\);
- \(|\mathcal D_0|=L\);
- the full squared-distance budget is \(D\);
- there are at most \(M\) target planes, each with at most \(Q\)
  target points.

For a triple producing \(C\), rotate \(\Pi_\alpha\) to the \(xz\)-plane.
The target point and label have the exact form
\[
q=(A,A\tan(\beta-\alpha),w_C),
\qquad
d=\rho(C)^2+A^2\tan^2(\beta-\alpha).
\tag{6}
\]
Put
\[
y(q)=A\tan(\beta-\alpha).
\]
The associated parameter line is
\[
\ell_C:\quad d=b+A^2\tau,
\qquad b=\rho(C)^2,\quad
\tau=\tan^2(\beta-\alpha),
\tag{7}
\]
and equivalently
\[
d=b+y(q)^2.
\tag{8}
\]

## 2. The signed-slope aggregate cap

Fix one signed value \(A\ne0\).  Let \(\mathcal C_A\) be any collection
of merged circles with \(A(C)=A\), and define
\[
X_A
=
\{q:\text{\(q\) occurs in a triple producing some }
C\in\mathcal C_A\}.
\tag{9}
\]

### Theorem 1 (label service cap on one signed slope)

\[
\boxed{
\sum_{C\in\mathcal C_A}\mu(C)\le L|X_A|.
}
\tag{10}
\]

### Proof

Fix \(q=(A,y,w)\in X_A\).  For each \(d\in\mathcal D_0\), equation
(8) fixes
\[
b=d-y^2.
\tag{11}
\]
The signed centre coordinate \(A\), centre height \(w\), and squared
radius \(b\) determine at most one normalized circle in
\(\Pi_\alpha\).  Therefore \((q,d)\) contributes to at most one
circle of \(\mathcal C_A\).

There are \(L\) possible labels \(d\).  Hence \(q\) is counted at most
\(L\) times in \(\sum_C\mu(C)\).  Sum over \(q\in X_A\). \(\square\)

### Corollary 2 (planar and global forms)

Every \(X_A\) lies in the ordinary plane
\[
H_A=\{(A,y,z):y,z\in\mathbb R\}.
\tag{12}
\]
The planar distinct-distance theorem and the global distance budget
give
\[
|X_A|\ll D\log(2D).
\tag{13}
\]
Moreover, the planes \(H_A\) are disjoint for distinct signed \(A\),
and their target points belong to the retained union of at most \(M\)
sets of size \(Q\).  Thus
\[
\sum_A|X_A|\le MQ.
\tag{14}
\]

For a dyadic layer \(s\le s(C)<2s\), Theorem 1 gives
\[
\sum_{C\in\mathcal C_A}s(C)\mu(C)
<2sL|X_A|.
\]
If \(R\) signed values of \(A\) occur, summing and applying
(13)--(14) proves (5).

## 3. Parallel-line bookkeeping

For one signed slope \(A\), let \(\mathcal B_A\) be the set of squared
radii \(b\) of parameter lines represented in a layer.  Put
\[
K_A=|\mathcal B_A|.
\tag{15}
\]
The geometric parameter line depends on \(A^2\), so the two signed
values \(A,-A\) can give the same line.  Treating \((A,b)\) as a
signed line copy changes every total by at most a factor two.  This
has no effect on any exponent below; when invoking
Szemerédi--Trotter, equal geometric copies are merged.
All parameter lines with this signed slope are parallel.  If each is
\(u/2\)-rich in
\[
\mathcal T_\alpha\times\mathcal D_0,
\qquad
|\mathcal T_\alpha\times\mathcal D_0|\le ML,
\]
then their parameter-point incidence sets are disjoint.  Consequently
\[
\boxed{
K_Au\ll ML.
}
\tag{16}
\]
This is compatible with the endpoint ledger below; it has a strict
\(t^{6/41}\) slack there.

There is also an exact service interpretation.  For
\[
q=(A,y,w)\in X_A,
\]
the parallel intercepts used by \(q\) are contained in
\[
\mathcal D_0-y^2
=
\{d-y^2:d\in\mathcal D_0\}.
\tag{17}
\]
The actual service relation also requires that the circle with centre
\((A,w)\) and squared radius \(b\) belongs to the layer.  Dropping
that condition gives the three-set incidence envelope
\[
\#\{(b,q,d):b\in\mathcal B_A,\ q=(A,y,w)\in X_A,\
d\in\mathcal D_0,\ b+y^2=d\}.
\tag{18}
\]
A power saving for this envelope would suffice for an improvement,
but the next sections show that cardinality and exact
finite-translation arguments alone do not give one.  A successful
attack may instead have to retain the omitted \((b,w)\)-circle
compatibility.

## 4. The enriched \(9/41\) endpoint ledger

Write all exponents relative to \(t\).  At
\[
\kappa=\frac9{41},
\]
put
\[
\boxed{
\begin{array}{c|c|l}
\text{symbol}&\text{exponent}&\text{meaning}\\ \hline
\ell&64/41&L=t^\ell\\
a&32/41&s=t^a\\
b&193/41&N=t^b\text{ circle classes}\\
m&35/41&u=t^m\\
p&105/41&|\mathcal T_\alpha\times\mathcal D_0|=t^p\\
c&105/41&K=t^c\text{ parameter lines}\\
r&41/41&R=t^r\text{ signed slopes}\\
j&64/41&K_A=t^j\text{ lines per signed slope}\\
h&88/41&t^h\text{ circles per parameter line}\\
x&123/41&|X_A|=t^x\text{ target points per slope}
\end{array}}
\tag{19}
\]

The original Route B equalities remain:
\[
\begin{aligned}
a+b+m&=\frac{260}{41}=7-3\kappa,\\
b+m&=\frac{228}{41}=6-2\kappa,\\
a+b&=\frac{18}{11}+\frac9{11}b,\\
c&=2p-3m=p.
\end{aligned}
\tag{20}
\]
The new aggregation equalities are
\[
\boxed{
\begin{aligned}
c&=r+j,\\
b&=r+j+h,\\
x&=h+m=3,\\
r+x&=4,\\
j&=\ell,\\
r+\ell+x+a&=\frac{260}{41},\\
r+j+h+m&=\frac{228}{41}.
\end{aligned}}
\tag{21}
\]

They have a direct interpretation inside this uniform equality
ledger.  More precisely, the interpretation below assumes that the
relevant dyadic and signed-slope classes are simultaneously uniform
at exponent scale.  No claim of exact finite equality, nor a general
regularization theorem for every endpoint near-extremizer, is being
made.

1. A parameter line contains \(t^h\) different centre heights and
   each circle has \(t^m\) target triples.  Those target points are
   distinct, so the uniform ledger requires
   \(x\ge h+m=3\).  On the other hand, (13) gives \(x\le3\) at
   exponent scale.  Therefore \(x=3\), and one line uses
   \[
   t^{h+m}=t^3
   \]
   points in \(H_A\).
2. Distinct signed \(A\)'s give disjoint \(H_A\)'s, while the retained
   target union has at most \(MQ=t^4\) points.  Hence \(r+x\le4\).
3. The slope-aggregate mass bound (5) forces
   \(r+\ell+x+a\ge260/41\).
4. The last two constraints force \(r+x=4\).  Together with
   \(x=3\), this gives
   \[
   \boxed{x=3,\qquad r=1.}
   \tag{22}
   \]
5. Since \(K=t^{105/41}\), this leaves
   \(t^{64/41}=L\) parameter lines per signed slope.
6. The triple mass per slope is
   \[
   t^{j+h+m}=t^{187/41}
   =t^{\ell+x}.
   \]
   Thus the label-service cap (10) is also exactly saturated at
   exponent scale: on average, every point of \(X_A\) serves
   \(t^\ell=L\) parallel lines.

The parallel-line point capacity (16) is respected:
\[
j+m=\frac{99}{41}<\frac{105}{41}=p.
\tag{23}
\]
The old source fibre cap also has slack:
\[
h+a=\frac{120}{41}<3.
\tag{24}
\]

Hence slope aggregation adds no inconsistent exponent to the endpoint.

## 5. Exact equality is impossible, but this gives no power saving

Suppose, at one fixed signed slope, that:

- the represented intercept set \(\mathcal B_A\) has cardinality
  \(L\);
- every \(q=(A,y,w)\in X_A\) serves all \(L\) intercepts; and
- two points of \(X_A\) have distinct values \(y_1^2\ne y_2^2\).

Then (17) forces
\[
\mathcal B_A
=
\mathcal D_0-y_1^2
=
\mathcal D_0-y_2^2.
\tag{25}
\]
Thus the finite set \(\mathcal D_0\) is invariant under the nonzero
translation \(y_1^2-y_2^2\), which is impossible over \(\mathbb R\).

This rules out literal finite equality.  It does not produce a fixed
power saving.  When the number \(U\) of tangent-square values is
substantially smaller than \(L\), intervals lose only \(O(U)\) of
their \(L\) translates.  At the endpoint,
\[
U=t^{35/41},\qquad L=t^{64/41},
\qquad \frac UL=t^{-29/41}.
\tag{26}
\]
The loss is invisible at exponent scale.

## 6. Finite interval model for the label-service barrier

Let \(J,U,H\) be positive integers with \(J\gg U\).  Use one signed
slope \(A=1\), tangent-square set
\[
\mathcal T=\{1,2,\ldots,U\},
\tag{27}
\]
intercepts
\[
\mathcal B=\{1,2,\ldots,J\},
\tag{28}
\]
and labels
\[
\mathcal D_0=\{2,3,\ldots,J+U\}.
\tag{29}
\]
Every parameter line
\[
d=b+\tau,\qquad b\in\mathcal B,
\tag{30}
\]
contains all \(U\) parameter points
\[
(\tau,b+\tau),\qquad \tau\in\mathcal T.
\]

Take \(H\) formal centre heights.  For every pair \((b,w)\), make one
circle class, and for every \(\tau\in\mathcal T\), attach the target
point
\[
q_{\tau,w}=(1,\sqrt{\tau},w).
\tag{31}
\]
Then:
\[
\begin{array}{c|c}
\text{quantity}&\text{exact value}\\ \hline
\text{parameter lines}&J\\
\text{target points}&UH\\
\text{circle classes}&JH\\
\text{multiplicity per circle}&U\\
\text{lines served per target point}&J\\
\text{total triples}&JUH\\
\text{selected labels}&J+U-1.
\end{array}
\tag{32}
\]

When \(J/U\to\infty\),
\[
|\mathcal D_0|=J(1+o(1)),
\]
so (32) saturates the label-service cap at power scale while using
\(U\to\infty\) different tangent squares.  This is an exact finite
model of the slope/label incidence ledger.

It is **not** asserted to realize the complete Euclidean endpoint:
in particular, it does not certify the global planar distance budget,
the point--circle incidence saturation, or simultaneous compatibility
of \(t\) different signed slopes.  Its role is narrower and rigorous:
no power improvement follows from (1), (17), finite translation
non-invariance, and label cardinality alone.

## 7. Why current structural incidence theory does not close the gap

At exponent scale, the endpoint parameter configuration has
\[
|\mathcal P_{\tan,\mathcal D}|
=
|\mathcal L|
=
t^{105/41+o(1)},
\]
and
\[
I(\mathcal P_{\tan,\mathcal D},\mathcal L)
=
t^{140/41+o(1)}
=
|\mathcal P_{\tan,\mathcal D}|^{4/3+o(1)}.
\tag{33}
\]
It is therefore a Szemerédi--Trotter near-extremal problem at exponent
scale on the Cartesian product
\[
|\mathcal T_\alpha|=t^{1+o(1)},\qquad
|\mathcal D_0|=t^{64/41+o(1)}.
\]
The aspect exponent is
\[
\frac{\log|\mathcal T_\alpha|}
{\log|\mathcal P_{\tan,\mathcal D}|}
=
\frac{41}{105}+o(1),
\qquad \frac{41}{105}\in(1/3,1/2).
\tag{34}
\]

Sheffer--Silier,
[*A structural Szemerédi--Trotter Theorem for Cartesian Products*]
(https://arxiv.org/abs/2110.09692), Theorem 1.3, treats every
\(1/3<\alpha<1/2\) and constructs an infinite family of
Cartesian-product configurations with \(\Theta(n^{4/3})\)
incidences.  Theorem 1.4 gives parallel/concurrent alternatives and,
in the parallel case, additive-energy and multiplicative-energy
structure.  These results do not provide a universal negative power
saving for (33); indeed, Theorem 1.3 rules out such a saving for
arbitrary Cartesian products in this aspect range.

Accordingly, citing that theorem does not exclude the endpoint.  A
successful continuation must prove a new incompatibility specific to
the reverse-circle geometry, for example:

1. a power loss when the endpoint parameter-line configuration also
   has only \(t\) signed slopes and \(L\) parallel lines per slope;
2. a power loss when every signed-slope target fibre is simultaneously
   a near-minimal planar distinct-distance set;
3. a power loss from serving almost all labels at almost all target
   points across many slopes; or
4. a direct distance expansion from the cross-centre formula
   \[
   \rho^2+y^2+(w-w')^2
   +2\rho(w-w')\sin\phi.
   \]

None of these four statements is proved here.

There is nevertheless a precise quantitative target.  Suppose that,
uniformly for the mass-carrying layers in the desired interval above
\(9/41\), one could prove for some fixed
\(0<\delta<37/125\) the compatibility-sensitive strengthening
\[
W_{s,u}\ll t^{-\delta}sLMQ.
\tag{35}
\]
Since \(L=t^{2-2\kappa+o(1)}\), comparison with the hub mass would give
\[
a\ge1-\kappa+\delta-o(1).
\tag{36}
\]
Combining (36) with the point--circle inequality (43) gives
\[
m\ge\frac{5-15\kappa+9\delta}{2}-o(1).
\]
The existing upper bound (46) would then force
\[
\kappa\ge\frac{9+25\delta}{41}-o(1).
\tag{37}
\]
Thus (35) would rigorously move the exclusion threshold from
\(9/41\) to \((9+25\delta)/41\), in the same dyadic regime.  The
restriction on \(\delta\) keeps this threshold below \(2/5\), the
range in which the argument behind (43) rules out the other
point--circle terms.  Without that restriction, the calculation
certifies only the smaller of \((9+25\delta)/41\) and \(2/5\).
The interval model proves that (35) cannot follow from label
cardinality and the envelope (18) alone; it must use the omitted
circle compatibility, simultaneous multi-slope structure, or
additional distance expansion.

## 8. Claim boundary

### Proved

- the fixed-signed-slope label service cap (10);
- its planar and global aggregate forms (13)--(14);
- the dyadic aggregate mass bound (5);
- the parallel-line capacity (16);
- exact impossibility of literal full service for two different
  tangent squares;
- the finite interval model showing no power saving from that
  impossibility;
- the enriched endpoint exponent ledger (19)--(24).

### Not proved

- exclusion of \(\kappa=9/41\) or any larger strict interval;
- Euclidean realization of the enriched endpoint ledger;
- a power-saving structural Szemerédi--Trotter theorem in the required
  subclass;
- an improvement of the \(3/5\) distinct-distance exponent.

## 9. Reproduction

```bash
cd data/research_open/erdos1083_two_hour_q1_attack_2026-07-30/route_b
python3 verify_nine_forty_one_next_attack.py
pytest -q test_verify_nine_forty_one_next_attack.py
```
