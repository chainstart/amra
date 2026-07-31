# Independent red-team audit: collinear-centre linearization

Date: 2026-07-30

Audited artifact:
`COLLINEAR_CENTER_LINEARIZATION_THEOREM.md`

## 0. Verdict

\[
\boxed{\texttt{PASS}}
\]

The fixed-signed-centre parabolic lift, the summed
Szemerédi--Trotter estimate, the secondary signed-line dyadic
decomposition, the target-point distinctness argument, the
elimination of the \(RQ\) and \(N\) error terms, and the strict
\(2/9\) hub-exclusion threshold all survive an independent
reconstruction.

The precise proved conclusion is
\[
\boxed{
\kappa<\frac29
\quad\Longrightarrow\quad
\text{the retained Euclidean hub cannot occur}.
}
\]
The endpoint \(\kappa=2/9\) is not excluded.  The endpoint table is a
simultaneously feasible scalar exponent ledger, not a Euclidean
configuration.

This audit also checked a tempting but invalid shortcut.  One must
not freeze the old \(9/41\) endpoint value \(r=1\) after adding the
new source-incidence inequality.  Before the secondary line-fibre
constraint is used, the old endpoint can rebalance to
\(r=43/41\).  The actual gain to \(2/9\) comes from the new,
independently justified inequality
\[
r+h+m\le4+o(1),
\]
not from substituting \(r=1\) into the fixed-\(A\) incidence bound.

## 1. Fixed-\(A\) geometry

Fix a signed centre coordinate \(A\).  For a source point
\(p=(u,z)\), put
\[
\Phi_A(p)=(Z,Y)
=\bigl(z,(u-A)^2+z^2\bigr).
\]
If two source points have the same image, then their \(z\)-coordinates
are equal and
\[
(u_1-A)^2=(u_2-A)^2.
\]
Thus a fibre contains at most the two values
\[
u=A\pm\sqrt{Y-Z^2}.
\]
Consequently the lift has multiplicity at most two.

A circle with centre \((A,w)\) and positive radius \(\rho\) has
equation
\[
(u-A)^2+(z-w)^2=\rho^2.
\]
Expansion gives the exact equivalence
\[
p\in C
\quad\Longleftrightarrow\quad
Y=2wZ+(\rho^2-w^2).
\]
Hence \(C\) maps to the line
\[
\lambda_C:\quad Y=2wZ+(\rho^2-w^2).
\]

If two such lines agree, equality of slopes gives equality of the
centre heights \(w\), and equality of intercepts then gives equality
of \(\rho^2\).  Positive radii give equality of \(\rho\).  Therefore
distinct normalized circles with the same signed \(A\) map to
distinct lines.

Writing
\[
P'_A=\Phi_A(P_\alpha),
\qquad
\Lambda_A=\{\lambda_C:C\in\mathcal C_A\},
\]
the fibre bound gives
\[
I(P_\alpha,\mathcal C_A)
\le2I(P'_A,\Lambda_A).
\]
The ordinary real Szemerédi--Trotter theorem therefore yields
\[
\boxed{
I(P_\alpha,\mathcal C_A)
\ll Q^{2/3}N_A^{2/3}+Q+N_A.
}
\tag{1}
\]

### Signed \(A\) versus \(A^2\)

The lifts \(\Phi_A\) and \(\Phi_{-A}\) are generally different, so
the source-incidence proof must split the two signed values.  This
is done correctly in the manuscript.

Conversely, the tangent--label parameter line depends on \(A^2\).
A geometric parameter line consequently has at most the two signed
copies \(A\) and \(-A\).  Passing between geometric lines and signed
line copies therefore costs only an absolute factor two and no
power of \(t\).

## 2. Summing the fixed-\(A\) estimates

Let \(R\) be the number of represented signed values of \(A\), and
let
\[
\sum_A N_A=N.
\]
Summing (1) and applying concavity, equivalently Hölder, gives
\[
\sum_A N_A^{2/3}
\le R^{1/3}N^{2/3}.
\]
Thus
\[
\boxed{
I(P_\alpha,\mathcal C)
\ll
Q^{2/3}R^{1/3}N^{2/3}+RQ+N.
}
\tag{2}
\]
No disjointness of the lifted source point sets for different \(A\)
is needed; Szemerédi--Trotter is applied separately before summing.

## 3. The strengthened fixed-\(A\) service cap

Fix a target point
\[
q=(A,y,w).
\]
For a fixed selected label \(d\), the squared radius of its parameter
line is uniquely
\[
b=d-y^2.
\]
The data \(A,w,b\) determine at most one normalized positive-radius
circle.  Hence \(q\) contributes to at most \(L\) circles.

Independently, for a fixed represented intercept \(b\), the same
data \(A,w,b\) again determine at most one circle.  If \(K_A\) is the
number of represented intercepts at signed centre \(A\), then \(q\)
contributes to at most \(K_A\) circles.  Summing over the target
points gives
\[
\boxed{
\sum_{C\in\mathcal C_A}\mu(C)
\le\min\{L,K_A\}|X_A|.
}
\tag{3}
\]
This strengthening is valid.  The direct one-line target argument
below is enough for the \(2/9\) theorem; (3) records the same
constraint in service-cap language.

## 4. Secondary dyadic decomposition

Begin with a mass-carrying layer
\[
s\le s(C)<2s,\qquad
u\le\mu(C)<2u.
\]
Every circle in this layer has weight \(s(C)\mu(C)\) between
\(su\) and \(4su\).  For a signed tangent--label line copy
\((A,b)\), define
\[
\nu(A,b)
=
\#\{C:A(C)=A,\ \rho(C)^2=b\}.
\]
There are only \(O(\log N)=t^{o(1)}\) possible dyadic ranges for
\(\nu(A,b)\).  Partitioning the signed line copies by those ranges
and retaining a mass-maximizing range therefore loses only a
\(t^{o(1)}\) factor.

In the retained sublayer, write
\[
\begin{aligned}
s&=t^{a+o(1)},&
u&=t^{m+o(1)},\\
N&=t^{b+o(1)},&
K&=t^{c+o(1)},\\
R&=t^{r+o(1)},&
\nu(A,b)&=t^{h+o(1)}.
\end{aligned}
\]
Every retained circle belongs to exactly one signed copy.  Hence
\[
\boxed{b=c+h.}
\tag{4}
\]
The symbols \(b,c,h,r\) here refer to the retained secondary
sublayer; redefining them after the polylogarithmic loss is
essential.

Every represented geometric parameter line is \(u/2\)-rich in
\(\mathcal T_\alpha\times\mathcal D_0\), and the number of signed
copies is at most twice the number of geometric lines.  With
\[
|\mathcal T_\alpha\times\mathcal D_0|
\le ML=t^{3-2\kappa+o(1)},
\]
the rich-line consequence of Szemerédi--Trotter gives
\[
K
\ll
\frac{(ML)^2}{u^3}+\frac{ML}{u}.
\]
For \(\kappa<2/9\), the old point--circle lower bound proved below
gives \(m>5/6-o(1)\), while \(\mu(C)\le M\) gives \(m\le1+o(1)\).
The exponent difference between the first and second rich-line
terms is
\[
(3-2\kappa)-2m
\ge1-2\kappa-o(1)>0.
\]
Therefore
\[
\boxed{c\le6-4\kappa-3m+o(1).}
\tag{5}
\]

## 5. Target points on one signed line are distinct

Fix one retained signed line copy \((A,b)\).  Its
\(t^{h+o(1)}\) circles have the same signed centre coordinate \(A\)
and the same positive squared radius \(b\).  Since equal normalized
circles were merged, their centre heights \(w_C\) are distinct.

For one circle \(C\), its \(\mu(C)\) producing triples use distinct
target points.  More explicitly, fixed-plane injectivity gives at
most one producing pair \((q,d)\) for each target plane, and an
off-axis target point belongs to a unique axial plane.  Equivalently,
the exact target coordinates
\[
q=(A,A\tan(\beta-\alpha),w_C)
\]
show that the producing target points are distinct.  Across
different circles on the fixed signed line, the last coordinate
\(w_C\) is different.  Thus all target points counted over the
circles of this signed copy are distinct.

It follows that every retained signed line copy uses at least
\[
t^{h+m-o(1)}
\]
different target points in the plane \(H_A=\{x=A\}\).

For each of the \(R\) represented signed values of \(A\), choose one
retained signed line copy.  Distinct signed values of \(A\) give
disjoint planes \(H_A\), hence disjoint target subsets.  The whole
retained target union contains at most
\[
MQ=t^{4+o(1)}
\]
points.  Consequently
\[
\boxed{r+h+m\le4+o(1).}
\tag{6}
\]
Combining (4)--(6) yields
\[
\boxed{
r
\le10-4\kappa-b-4m+o(1).
}
\tag{7}
\]

This step does not require an unproved uniformity assertion about
the numbers of lines per signed \(A\).  The secondary dyadic
decomposition makes every retained signed line contain comparable
numbers of circles, and only one such line is selected from each
active signed \(A\).

## 6. Independent reconstruction of the old point--circle input

The retained sublayer still has hub-scale mass, so
\[
\boxed{
a+b+m\ge7-3\kappa-o(1).
}
\tag{8}
\]
Moreover,
\[
Nu\le\sum_C\mu(C)\le MQL
=t^{6-2\kappa+o(1)},
\]
and hence
\[
\boxed{b+m\le6-2\kappa+o(1).}
\tag{9}
\]
Since the layer mass is at most a constant times
\(s\sum_C\mu(C)\), (8)--(9) already imply
\[
\boxed{a\ge1-\kappa-o(1).}
\tag{10}
\]

Apply the ordinary planar point--circle incidence theorem to the
distinct merged circles of the retained sublayer.  In the range
\(\kappa<2/9\), the \(Q^{2/3}N^{2/3}\) term cannot carry the mass:
using (9), that alternative would force
\[
m\ge3-5\kappa-o(1)>1,
\]
contrary to \(\mu(C)\le M=t^{1+o(1)}\).  The \(+Q\) term would force
\[
m\ge4-3\kappa-o(1)>1,
\]
and the \(+N\) term contradicts (10).  Therefore the
\(Q^{6/11}N^{9/11}\) term must carry, giving
\[
\boxed{11a+2b\le18+o(1).}
\tag{11}
\]

Combining (8), (9), and (11) independently recovers
\[
\boxed{
a\le\frac{4+6\kappa+2m}{9}+o(1),
\qquad
m\ge\frac{5-15\kappa}{2}-o(1).
}
\tag{12}
\]
Thus equation (15) and all three inequalities in equation (17) of
the audited manuscript are valid after the secondary restriction.

## 7. Elimination of the source-incidence error terms

For the retained sublayer,
\[
I(P_\alpha,\mathcal C)=t^{a+b+o(1)}.
\]
Applying (2), one of the three exponent terms
\[
2+\frac r3+\frac{2b}{3},
\qquad
3+r,
\qquad
b
\tag{13}
\]
must carry.

The \(+N\) term cannot carry because it would give \(a\le o(1)\),
whereas (10) gives a fixed positive lower bound.

Suppose the \(RQ\) term carries.  Then
\[
a+b\le3+r+o(1).
\]
Inserting (7), and then using the mass lower bound (8), gives
\[
\begin{aligned}
a+2b+4m&\le13-4\kappa+o(1),\\
2m&\le a+2\kappa-1+o(1).
\end{aligned}
\tag{14}
\]
Use the upper bound for \(a\) in (12):
\[
2m
\le
\frac{4+6\kappa+2m}{9}
+2\kappa-1+o(1).
\]
Rearrangement gives
\[
\boxed{
m\le\frac{24\kappa-5}{16}+o(1).
}
\tag{15}
\]
Together with the lower bound in (12), compatibility of the
\(RQ\) alternative would in fact require
\[
\frac{5-15\kappa}{2}
\le
\frac{24\kappa-5}{16}+o(1),
\]
whose exact crossing is
\[
\kappa=\frac5{16}.
\]
Hence the \(RQ\) term is impossible throughout the much larger range
\(\kappa<5/16\), in particular throughout \(\kappa<2/9\).  This
confirms equations (22)--(23) of the manuscript.

The main term in (13) must therefore carry:
\[
\boxed{3a+b\le6+r+o(1).}
\tag{16}
\]
Combining (16) with (7) gives
\[
3a+2b+4m\le16-4\kappa+o(1).
\]
Using (8) now yields
\[
\boxed{a+2m\le2+2\kappa+o(1).}
\tag{17}
\]
Finally, (10), (12), and (17) imply
\[
\frac{5-15\kappa}{2}
\le m
\le\frac{1+3\kappa}{2}+o(1).
\]
The exact crossing is
\[
\boxed{\kappa=\frac29.}
\]
Every fixed \(\kappa<2/9\) leaves a fixed exponent gap, so all
polylogarithmic and \(t^{o(1)}\) losses are harmless.

## 8. Independent endpoint ledger check

At \(\kappa=2/9\), take
\[
\begin{array}{c|c}
\ell&14/9\\
p&23/9\\
a&7/9\\
b&85/18\\
m&5/6\\
c&47/18\\
h&19/9\\
r&19/18\\
j&14/9\\
x&53/18
\end{array}
\]
The following equalities hold exactly:
\[
\begin{aligned}
a+b+m&=7-3\kappa=\frac{19}{3},\\
b+m&=6-2\kappa=\frac{50}{9},\\
11a+2b&=18,\\
b&=c+h,\\
c&=2p-3m,\\
r+h+m&=4,\\
x&=h+m,\\
c&=r+j,\\
j&=\ell,\\
j+h+m&=\ell+x,\\
3a+b&=6+r,\\
a&=1-\kappa,\\
m&=\frac{5-15\kappa}{2}
=\frac{1+3\kappa}{2}.
\end{aligned}
\tag{18}
\]
The remaining relevant inequalities have strict slack:
\[
h+a=\frac{26}{9}<3,
\qquad
j+m=\frac{43}{18}<p=\frac{46}{18},
\qquad
x=\frac{53}{18}<3,
\qquad
a+r=\frac{11}{6}>2-\kappa=\frac{16}{9}.
\tag{19}
\]

Thus the scalar system is feasible at \(2/9\).  The proof correctly
uses a strict inequality \(\kappa<2/9\) and makes no endpoint claim.

## 9. Claim boundary

### Audited as proved

- the fixed-\(A\) lift and its two-to-one fibre bound;
- injectivity of the circle-to-line map for fixed signed \(A\);
- the summed incidence estimate (2);
- the strengthened service cap (3);
- retention of hub-scale mass under the secondary dyadic
  decomposition;
- distinctness of the \(t^{h+m-o(1)}\) target points on one signed
  line;
- the global target-capacity inequality (6);
- the old point--circle inequality after the secondary restriction;
- exclusion of both error terms in (13);
- hub exclusion for every fixed \(\kappa<2/9\);
- the resulting structural matching exponent
  \(2/9-\varepsilon\).

### Not proved

- hub exclusion at \(\kappa=2/9\);
- Euclidean realizability or non-realizability of the endpoint
  ledger;
- a power saving beyond the scalar endpoint;
- an improvement of the global \(3/5\) distinct-distance exponent;
- a standalone journal theorem at the claimed Q1 level.

The audit found no hidden identification of target subsets with the
whole configuration, no collision across the selected target
points, and no use of a rich-line estimate before \(u\to\infty\) is
established.
