# Erdős #1083: multidilate energy and nonaligned chart synchronization

Date: 2026-07-30

## 0. Outcome

This note proves a new all-parameter additive-energy theorem and
applies it to the live \(2/9\) reverse-circle endpoint.

The additive theorem is elementary but substantially sharper than the
previous multi-dilate estimate in the regime relevant here.  If
\(T_z\) are arbitrary subsets of one \(R\)-element real set, \(X\) is
an \(S\)-element real set, and the nonzero dilates \(\lambda_z\) are
distinct, then
\[
\boxed{
 \sum_z E^+(T_z,\lambda_zX)
 \le
 S\sum_z|T_z|+R(R-1)S(S-1).
}
\tag{0.1}
\]
The first term consists of the unavoidable diagonal solutions.  Every
nontrivial ordered quadruple from
\(T_\ast^2\times X^2\) determines at most one dilation, which gives
the second term.

For a fixed-\((A,\rho)\) reverse-circle bundle, (0.1) implies that the
individual cross-distance spectra are almost injective in aggregate
whenever
\[
 HU\gg R^2S.
\tag{0.2}
\]
If their union has size at most \(D\), two different-height spectra
must then overlap in
\[
\boxed{\gg S^2U^2/D}
\tag{0.3}
\]
distinct squared-distance labels.

At the live \(\kappa=2/9\) hub endpoint, the inherited and audited
scalar inequalities force a parameter-line bundle with
\[
 S\ge t^{7/9-o(1)},\qquad
 U\ge t^{5/6-o(1)},\qquad
 H\ge t^{19/9-o(1)},\qquad
 R\le t^{1+o(1)}.
\tag{0.4}
\]
Consequently (0.2) has a \(t^{1/6-o(1)}\) margin, and two
incidence-rich, multiplicity-rich, pairwise nonaligned congruent
reverse circles have anchor-to-axis spectra sharing
\[
\boxed{t^{2/9-o(1)}}
\tag{0.5}
\]
distinct labels.

The quadratic height translation gives an additional many-by-many
conclusion.  At least
\[
\boxed{t^{35/18-o(1)}}
\tag{0.6}
\]
global distance labels each occur in the anchor-to-axis spectra of
at least
\[
\boxed{t^{13/18-o(1)}}
\tag{0.7}
\]
different pairwise nonaligned rows.

Moreover, for every fixed \(\varepsilon>0\), at least
\[
\boxed{t^{17/6-o(1)}}
\tag{0.8}
\]
unordered pairs of nonaligned rows each share
\[
\boxed{t^{2/9-\varepsilon-o(1)}}
\tag{0.9}
\]
labels.  Thus the synchronized pair is abundant rather than
exceptional.

This is a genuine endpoint structural theorem.  It does **not** prove
an exponent above \(3/5\): a new upper bound for the overlap in (0.5),
or a theorem converting that overlap into new distances, is still
required.

## 1. A sharp multidilate energy budget

For finite real sets \(A,B\), write
\[
E^+(A,B)
=
\#\{(a,b,a',b')\in A\times B\times A\times B:
 a+b=a'+b'\}.
\tag{1.1}
\]

### Theorem 1 (distinct-dilate energy budget)

Let \(X,T_\ast\subset\mathbb R\) be finite, with
\[
|X|=S,\qquad |T_\ast|=R.
\tag{1.2}
\]
Let \(\Lambda\subset\mathbb R\setminus\{0\}\) be a finite set of
distinct dilates, and for every \(\lambda\in\Lambda\) let
\[
T_\lambda\subseteq T_\ast
\tag{1.3}
\]
be arbitrary, possibly empty.  Then
\[
\boxed{
\sum_{\lambda\in\Lambda}E^+(T_\lambda,\lambda X)
\le
S\sum_{\lambda\in\Lambda}|T_\lambda|
+R(R-1)S(S-1).
}
\tag{1.4}
\]

The assertion is finite, has no asymptotic notation, and needs no
additive structure hypothesis.

### Proof

Fix \(\lambda\).  An energy solution has
\[
\tau+\lambda x=\tau'+\lambda x',
\qquad
\tau,\tau'\in T_\lambda,\quad x,x'\in X.
\tag{1.5}
\]
If \(x=x'\), then \(\tau=\tau'\), giving exactly
\[
S|T_\lambda|
\tag{1.6}
\]
diagonal solutions.

Every other solution has \(x\ne x'\), and then necessarily
\(\tau\ne\tau'\).  Equation (1.5) determines the dilation uniquely:
\[
\lambda=\frac{\tau'-\tau}{x-x'}.
\tag{1.7}
\]
An ordered quadruple
\[
(\tau,\tau',x,x')
\in
T_\ast^2\times X^2,
\qquad
\tau\ne\tau',\quad x\ne x',
\tag{1.8}
\]
can therefore be counted for at most one member of the distinct set
\(\Lambda\).  There are exactly
\[
R(R-1)S(S-1)
\tag{1.9}
\]
quadruples in (1.8).  Summing (1.6) and (1.9) proves (1.4).
\(\square\)

### Exact scope

The two terms in (1.4) have different meanings.

* The diagonal term cannot be removed: every pair
  \((\tau,x)\in T_\lambda\times X\) contributes one solution.
* The second term is a global budget over all dilates, not a separate
  \(R^2S^2\) allowance for every \(\lambda\).
* Distinctness of the nonzero dilates is essential.  Repeating one
  dilation repeats its full energy.

## 2. Aggregate expansion and two-spectrum synchronization

Let \(c_\lambda\in\mathbb R\) be arbitrary translations, and put
\[
\mathcal V_\lambda
=
c_\lambda+T_\lambda+\lambda X.
\tag{2.1}
\]
Translations do not change the same-row energy.

### Theorem 2 (aggregate support)

In the setup of Theorem 1, put
\[
\mathcal N
=
S\sum_{\lambda\in\Lambda}|T_\lambda|,
\qquad
\mathcal B
=
R(R-1)S(S-1).
\tag{2.2}
\]
Then
\[
\boxed{
\sum_{\lambda\in\Lambda}|\mathcal V_\lambda|
\ge
\frac{\mathcal N^2}{\mathcal N+\mathcal B}.
}
\tag{2.3}
\]

#### Proof

For each \(\lambda\), let \(r_\lambda(v)\) count representations
\[
v=c_\lambda+\tau+\lambda x.
\]
Then
\[
\sum_vr_\lambda(v)=S|T_\lambda|,
\qquad
\sum_vr_\lambda(v)^2=E^+(T_\lambda,\lambda X).
\tag{2.4}
\]
Cauchy--Schwarz first within each row and then across the rows gives
\[
\left(\sum_\lambda S|T_\lambda|\right)^2
\le
\left(\sum_\lambda|\mathcal V_\lambda|\right)
\left(\sum_\lambda E^+(T_\lambda,\lambda X)\right).
\tag{2.5}
\]
Apply (1.4) to the second factor.  This proves (2.3).
\(\square\)

Suppose now that
\[
|\Lambda|=H,\qquad |T_\lambda|\ge U
\quad(\lambda\in\Lambda).
\tag{2.6}
\]
Equations (2.2)--(2.3) give the convenient uniform form
\[
\boxed{
\sum_\lambda|\mathcal V_\lambda|
\ge
\frac{HSU}{1+R^2S/(HU)}.
}
\tag{2.7}
\]
Here and below replacing \(R(R-1),S(S-1)\) by \(R^2,S^2\) only
weakens the estimate.

### Theorem 3 (two-spectrum synchronization)

Assume (2.6), \(H\ge2\), and
\[
HU\ge R^2S.
\tag{2.8}
\]
Let
\[
\mathcal V=\bigcup_{\lambda\in\Lambda}\mathcal V_\lambda,
\qquad |\mathcal V|\le D.
\tag{2.9}
\]
If
\[
HSU\ge4D,
\tag{2.10}
\]
then two distinct dilates \(\lambda,\lambda'\) satisfy
\[
\boxed{
|\mathcal V_\lambda\cap\mathcal V_{\lambda'}|
\ge
\frac{S^2U^2}{8D}.
}
\tag{2.11}
\]

#### Proof

Put
\[
\mathcal S=\sum_\lambda|\mathcal V_\lambda|.
\]
By (2.7)--(2.8),
\[
\mathcal S\ge\frac{HSU}{2}\ge2D.
\tag{2.12}
\]
For \(v\in\mathcal V\), let
\[
q_v=\#\{\lambda:v\in\mathcal V_\lambda\}.
\]
Then
\[
\sum_vq_v=\mathcal S
\tag{2.13}
\]
and
\[
\sum_{\lambda\ne\lambda'}
|\mathcal V_\lambda\cap\mathcal V_{\lambda'}|
=
\sum_vq_v(q_v-1).
\tag{2.14}
\]
Cauchy--Schwarz over the at most \(D\) values gives
\[
\sum_vq_v(q_v-1)
\ge
\frac{\mathcal S^2}{D}-\mathcal S
\ge
\frac{\mathcal S^2}{2D}.
\tag{2.15}
\]
There are \(H(H-1)\) ordered distinct pairs.  Hence one pair has
intersection at least
\[
\frac{\mathcal S^2}{2DH(H-1)}
\ge
\frac{H^2S^2U^2}{8DH(H-1)}
\ge
\frac{S^2U^2}{8D}.
\]
This proves (2.11).
\(\square\)

The use of set intersections in (2.11), rather than representation
energy, is important: the conclusion supplies genuinely distinct
shared labels.

There is also a useful abundance form.  Put
\[
\mathcal J
=
\sum_{\lambda\ne\lambda'}
|\mathcal V_\lambda\cap\mathcal V_{\lambda'}|.
\tag{2.16}
\]
The proof gives
\[
\mathcal J\ge\frac{\mathcal S^2}{D}-\mathcal S.
\tag{2.17}
\]
If in addition \(|T_\lambda|\le2U\), then
\[
|\mathcal V_\lambda\cap\mathcal V_{\lambda'}|
\le2SU.
\tag{2.18}
\]
Consequently, for any threshold \(\theta\ge0\), the number
\(\mathcal N_\theta\) of ordered distinct pairs with intersection at
least \(\theta\) satisfies
\[
\boxed{
\mathcal N_\theta
\ge
\frac{\mathcal J-H(H-1)\theta}{2SU}
}
\tag{2.19}
\]
whenever the numerator is positive.  This is just the decomposition
of (2.16) into pairs below and above \(\theta\), followed by (2.18).

## 3. Euclidean reverse-circle bundle

Rotate the fixed source axial plane to
\[
\Pi_\alpha=\{(u,0,z):u,z\in\mathbb R\}.
\]
Fix \(A\ne0\), \(\rho>0\), and distinct real centre heights
\[
w_0,w_1,\ldots,w_H.
\]
Consider the congruent source-plane circles
\[
C_i:\quad
(u-A)^2+(z-w_i)^2=\rho^2.
\tag{3.1}
\]
Their perpendicular axes are
\[
L_i=\{(A,y,w_i):y\in\mathbb R\}.
\tag{3.2}
\]
The lines \(L_i\) are parallel and distinct.  Thus all the circles
\(C_i\) are pairwise nonaligned in the
Mathialagan--Sheffer classification.  Since they lie in the same
source plane, they are not in the perpendicular-circle exception
either.

Let \(P_0\subseteq P\cap C_0\) have \(s_0\) points.  Parameterize
\[
p_\phi=(A+\rho\cos\phi,0,w_0+\rho\sin\phi).
\tag{3.3}
\]
The sine map has fibres of size at most two, so the sine set
\[
X=\{\sin\phi:p_\phi\in P_0\}
\tag{3.4}
\]
satisfies
\[
|X|\ge s_0/2.
\tag{3.5}
\]

For \(i\ge1\), let \(Y_i\) be a set of transverse coordinates of
target points
\[
q_{i,y}=(A,y,w_i)\in P\cap L_i
\tag{3.6}
\]
that produce \(C_i\) as a reverse circle.  Put
\[
T_i=\{y^2:y\in Y_i\},
\qquad
T_\ast=\bigcup_{i=1}^HT_i.
\tag{3.7}
\]
Squaring is at most two-to-one, and therefore
\[
|T_i|\ge |Y_i|/2.
\tag{3.8}
\]
All retained target planes supply one common tangent-square universe,
so in the critical axial setup
\[
|T_\ast|\le M.
\tag{3.9}
\]

Write
\[
z_i=w_0-w_i.
\tag{3.10}
\]
Direct expansion gives the exact cross-distance formula
\[
\begin{aligned}
|p_\phi-q_{i,y}|^2
&=\rho^2+y^2+z_i^2+2\rho z_i\sin\phi.
\end{aligned}
\tag{3.11}
\]
Thus
\[
\mathcal V_i
=
\rho^2+z_i^2+T_i+2\rho z_iX
\subseteq\Delta^2(P).
\tag{3.12}
\]
The nonzero \(z_i\)'s are distinct, so the dilates
\[
\lambda_i=2\rho z_i
\tag{3.13}
\]
are distinct and Theorems 1--3 apply.

### Corollary 4 (nonaligned chart synchronization)

Assume every \(C_i\), \(i\ge1\), is produced by at least \(u\)
distinct target triples, and \(C_0\) has at least \(s\) source
incidences.  Put
\[
S=\lfloor s/2\rfloor,\qquad U=\lfloor u/2\rfloor,
\qquad R=|T_\ast|.
\tag{3.14}
\]
If
\[
HU\ge R^2S,\qquad HSU\ge4D,\qquad
|\Delta^2(P)|\le D,
\tag{3.15}
\]
then two pairwise nonaligned incidence-active circles
\(C_i,C_j\) have cross-spectra from the common rich anchor \(C_0\)
obeying
\[
\boxed{
|\mathcal V_i\cap\mathcal V_j|
\ge\frac{S^2U^2}{8D}.
}
\tag{3.16}
\]

Every label in this intersection is realized both between
\(P_0\) and \(Y_i\) and between \(P_0\) and \(Y_j\).  No finite
experiment or generic-position assumption is used.

### Theorem 5 (many-label/many-row spectral graph)

Keep the Euclidean setup (3.1)--(3.13), assume
\[
|X|=S,\qquad |T_i|\ge U,\qquad |T_\ast|=R,
\qquad |\Delta^2(P)|\le D,
\tag{3.17}
\]
and suppose
\[
HU\ge R^2S.
\tag{3.18}
\]
For a squared-distance label \(d\), put
\[
q_d=\#\{i:d\in\mathcal V_i\}.
\tag{3.19}
\]
Then at least
\[
\boxed{\frac{HU}{8R}}
\tag{3.20}
\]
distinct labels satisfy
\[
\boxed{
q_d\ge\frac{HSU}{4D}.
}
\tag{3.21}
\]

#### Proof

The aggregate-support theorem and (3.18) give
\[
\sum_dq_d=\sum_i|\mathcal V_i|
\ge\frac{HSU}{2}.
\tag{3.22}
\]
Call a label spectrally rich when it satisfies (3.21).  All labels
that are not spectrally rich contribute less than
\[
D\frac{HSU}{4D}=\frac{HSU}{4}
\tag{3.23}
\]
to (3.22).  Thus the rich labels carry at least \(HSU/4\) row
memberships.

It remains to bound one \(q_d\).  If \(d\in\mathcal V_i\), some
\((x,\tau)\in X\times T_\ast\) satisfies
\[
d=\rho^2+\tau+z_i^2+2\rho z_ix.
\tag{3.24}
\]
For fixed \(d,x,\tau\), this is a quadratic equation in \(z_i\), so
it has at most two real roots.  Therefore
\[
q_d\le2SR.
\tag{3.25}
\]
Dividing the \(HSU/4\) rich membership mass by (3.25) proves
(3.20).
\(\square\)

This conclusion is a bipartite-graph statement between actual
distance labels and actual nonaligned circle rows.  It does not
count repeated representations within one row.

## 4. The live \(2/9\) endpoint

We now use only the scalar inequalities already proved and
independently audited in the preceding two-hour campaign.  This
section adds the new consequence of Theorems 1--3; it does not
silently strengthen their upstream hypotheses.

Assume the critical pair-codegree and cell-cap setup, and apply the
matching-or-hub theorem at the exact value
\[
\kappa=\frac29.
\tag{4.1}
\]
If the matching alternative holds, it already gives
\[
t^{1-o(1)}
\]
labels with rich plane-pair matchings of size
\[
t^{2/9-o(1)}.
\tag{4.2}
\]

Suppose instead that the hub alternative holds.  Perform the audited
dyadic decomposition by circle richness and multiplicity, followed
by the secondary decomposition by the number of circles on a signed
parameter line \((A,\rho^2)\).  Write
\[
s=t^{a+o(1)},\quad
u=t^{m+o(1)},\quad
N=t^{b+o(1)},\quad
K=t^{c+o(1)},\quad
H=t^{h+o(1)}.
\tag{4.3}
\]
Here \(H\) is the number of circles on each retained signed
parameter-line copy and
\[
b=c+h.
\tag{4.4}
\]

At \(\kappa=2/9\), the existing mass, capacity, point--circle, and
tangent--label estimates give
\[
\begin{aligned}
a+b+m&\ge\frac{19}{3}-o(1),\\
b+m&\le\frac{50}{9}+o(1),\\
11a+2b&\le18+o(1),\\
m&\ge\frac56-o(1),\qquad m\le1+o(1),\\
c&\le\frac{46}{9}-3m+o(1).
\end{aligned}
\tag{4.5}
\]
For completeness, these inequalities imply the bundle exponents
without assuming equality in the old endpoint ledger.

The first two lines give
\[
\boxed{a\ge\frac79-o(1).}
\tag{4.6}
\]
Combining the mass lower bound with \(11a+2b\le18\) gives
\[
\boxed{
a\le\frac{16}{27}+\frac{2m}{9}+o(1).
}
\tag{4.7}
\]
Finally, (4.4)--(4.5) yield
\[
\begin{aligned}
h
&\ge
\left(\frac{19}{3}-a-m\right)
-\left(\frac{46}{9}-3m\right)-o(1)\\
&=
\frac{11}{9}-a+2m-o(1)\\
&\ge
\frac{17}{27}+\frac{16m}{9}-o(1)
\ge
\boxed{\frac{19}{9}-o(1)}.
\end{aligned}
\tag{4.8}
\]

Choose one retained signed parameter line.  Its \(H\) circles have
the same \(A\) and positive radius \(\rho\), but distinct centre
heights.  They are therefore pairwise nonaligned, each has at least
\[
t^{7/9-o(1)}
\]
source incidences, and each is produced at least
\[
t^{5/6-o(1)}
\]
times.  This is already a forced many-circle extraction, not a
single-circle or concentric-circle statement.

The common tangent-square universe has
\[
R\le M=t^{1+o(1)}.
\tag{4.9}
\]
Equations (4.7)--(4.8) give the strict reuse margin
\[
\begin{aligned}
h+m-2-a
&\ge-\frac79-2a+3m-o(1)\\
&\ge-\frac{53}{27}+\frac{23m}{9}-o(1)\\
&\ge\boxed{\frac16-o(1)}.
\end{aligned}
\tag{4.10}
\]
Thus
\[
HU\ge t^{1/6-o(1)}R^2S,
\tag{4.11}
\]
so the first condition in Corollary 4 has a fixed power margin.
Moreover,
\[
h+a+m
\ge\frac{11}{9}+3m-o(1)
\ge\boxed{\frac{67}{18}-o(1)}>3,
\tag{4.12}
\]
so the aggregate row-spectrum mass dominates the global
\(D=t^{3+o(1)}\) distance budget by a fixed power.

Corollary 4 now forces two distinct rows with shared spectrum size
\[
\begin{aligned}
|\mathcal V_i\cap\mathcal V_j|
&\gg\frac{S^2U^2}{D}\\
&\ge
t^{2a+2m-3-o(1)}\\
&\ge
\boxed{t^{2/9-o(1)}}.
\end{aligned}
\tag{4.13}
\]

Theorem 5 gives a simultaneous spectral graph.  Its number of rich
labels is
\[
\frac{HU}{R}
\ge
t^{h+m-1-o(1)}
\ge
\boxed{t^{35/18-o(1)}},
\tag{4.14}
\]
and every such label has row degree at least
\[
\frac{HSU}{D}
\ge
t^{h+a+m-3-o(1)}
\ge
\boxed{t^{13/18-o(1)}}.
\tag{4.15}
\]

Finally, the overlap is abundant.  The total ordered row-pair
intersection has exponent
\[
\mathcal J
\ge
t^{2(h+a+m)-3-o(1)}
\ge
t^{40/9-o(1)}.
\tag{4.16}
\]
Fix \(\varepsilon>0\) and put
\[
\theta=t^{2a+2m-3-\varepsilon}.
\tag{4.17}
\]
All pairs below this threshold contribute at most
\[
H^2\theta
=
t^{2(h+a+m)-3-\varepsilon+o(1)}
=o(\mathcal J).
\tag{4.18}
\]
Every one pair contributes at most
\[
t^{a+m+o(1)}
\tag{4.19}
\]
labels.  Therefore the number of ordered, and hence also the number
of unordered up to an absolute factor, synchronized pairs is at
least
\[
\begin{aligned}
t^{2h+a+m-3-o(1)}
&\ge
t^{\,2(19/9)+7/9+5/6-3-o(1)}\\
&=
\boxed{t^{17/6-o(1)}}.
\end{aligned}
\tag{4.20}
\]
Every such pair has intersection at least
\[
\theta\ge t^{2/9-\varepsilon-o(1)}.
\tag{4.21}
\]

We have proved the following endpoint dichotomy.

### Theorem 6 (conditional \(2/9\) endpoint dichotomy)

Under the audited critical pair-codegree and cell-cap hypotheses, at
least one of the following holds:

1. at least \(t^{1-o(1)}\) distance labels support a matching of
   \(t^{2/9-o(1)}\) pairwise plane-disjoint rich cells; or
2. one fixed source plane contains a congruent bundle of
   \(t^{19/9-o(1)}\) pairwise nonaligned positive-radius reverse
   circles, every circle has at least \(t^{7/9-o(1)}\) source
   incidences and \(t^{5/6-o(1)}\) producing triples, and two circle
   rows have anchor-to-axis spectra sharing \(t^{2/9-o(1)}\)
   distinct squared-distance labels.  Moreover,
   \(t^{35/18-o(1)}\) global labels each occur in at least
   \(t^{13/18-o(1)}\) different row spectra, and for every fixed
   \(\varepsilon>0\), at least \(t^{17/6-o(1)}\) unordered row pairs
   share \(t^{2/9-\varepsilon-o(1)}\) labels each.

The second alternative is the new conclusion.

## 5. Why this still stops short of \(3/5+\delta\)

Equation (4.13) forces a polynomial spectral overlap, but no
all-parameter theorem in the current package gives an upper bound
smaller than \(t^{2/9-o(1)}\) for that overlap.  The equality relation
is
\[
\tau+z^2+2\rho zx
=
\tau'+z'^2+2\rho z'x',
\tag{5.1}
\]
with
\[
T_z,T_{z'}\subseteq T_\ast,\qquad |T_\ast|\le t^{1+o(1)}.
\tag{5.2}
\]
Theorem 1 controls the \(z=z'\) energy sharply.  It does not control
the shifted cross-dilate relation \(z\ne z'\), because the quadratic
translations \(z^2,z'^2\) vary with both rows.

Therefore the unique local gap exposed by this route is:

> Prove a fixed-power aggregate de-reuse saving for the synchronized
> nonaligned row network in (5.1), unless it lies in an explicitly
> classified Euclidean exceptional configuration; then show that
> every exceptional configuration either expands distances or
> violates the global selected-label service graph.

This is strictly narrower than the previous request for an
unspecified cross-height power saving: the required object is now a
quantified network of nonaligned, source-rich, multiplicity-rich
charts rather than an unspecified collection of cross-height
collisions.

Concretely, a sufficient **bundle de-reuse lemma** would save a fixed
power in
\[
\sum_{z\ne z'}|\mathcal V_z\cap\mathcal V_{z'}|
\]
relative to
\[
\frac{(\sum_z|\mathcal V_z|)^2}{D},
\]
uniformly over a small exponent neighbourhood of the endpoint, unless
an explicit affine-quadratic exceptional family itself expands
distances.  The exact quantifiers and exception discharge are
recorded in `QUANTIFIER_AND_GEOMETRIC_GAP_AUDIT.md`.

Mathialagan--Sheffer's known two-circle theorem applies to the
extracted circles because they are neither aligned nor perpendicular,
but at \(s=t^{7/9-o(1)}\) it yields only
\[
t^{28/27-o(1)}
\]
source--source distances for one pair.  It has no aggregate numerical
distance-reuse bound over the \(t^{17/6-o(1)}\) pairs and does not
involve the perpendicular-axis target rows.  The missing result is
therefore not another one-pair circle classification.

Even a successful bundle de-reuse lemma would discharge only the hub
branch.  A full \(3/5+\delta\) result also requires conversion of the
rich plane-pair matching branch into distance expansion.

## 6. Claim boundary

### Proved here

- the exact all-parameter energy budget (1.4);
- aggregate support expansion (2.3);
- the two-spectrum overlap theorem (2.11);
- its exact Euclidean circle--axis interpretation;
- extraction of \(t^{19/9-o(1)}\) pairwise nonaligned congruent
  circles in any surviving \(2/9\) endpoint hub;
- the fixed \(t^{1/6-o(1)}\) global-reuse margin;
- a pair of nonaligned rows with
  \(t^{2/9-o(1)}\) shared cross-spectrum labels;
- the \(t^{35/18}\)-by-\(t^{13/18}\) spectral graph;
- abundance of \(t^{17/6-o(1)}\) synchronized nonaligned row pairs;
- the conditional endpoint dichotomy in Theorem 6.

### Not proved

- an unconditional improvement
  \(f_3(N)\gg N^{3/5+\delta}\);
- the \(N^{2/3-o(1)}\) target in Erdős #1083;
- exclusion of the synchronized-pair alternative;
- the aggregate bundle de-reuse lemma;
- conversion of the separate matching branch into \(t^{3+\epsilon}\)
  distances;
- Euclidean realization of every scalar endpoint ledger;
- Q1 publication status for this theorem by itself.

The word “conditional” in Theorem 6 refers only to the explicit
critical pair-codegree and cell-cap hypotheses inherited from the
audited reduction.  Theorems 1--3 and Corollary 4 are unconditional
finite real statements.
