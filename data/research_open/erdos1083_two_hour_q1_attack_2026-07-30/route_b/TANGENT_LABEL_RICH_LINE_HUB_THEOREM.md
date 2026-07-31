# Erdős #1083: tangent--label rich-line elimination of the moderate hub

Date: 2026-07-30

## 0. Outcome

Fix the source axial plane \(\Pi_\alpha\) in the Euclidean hub branch.
The repeated reverse-circle chart has a second, previously unused,
two-dimensional incidence encoding:
\[
\boxed{d=\rho(C)^2+A(C)^2\tan^2(\alpha-\beta).}
\tag{1}
\]
Here \(C\subset\Pi_\alpha\) is a positive-radius reverse circle,
\((A(C),w(C))\) is its centre in signed radial--height coordinates,
\(\rho(C)\) is its radius, and \(\Pi_\beta\) is a retained target
plane that produces \(C\).

Thus every repetition of \(C\) is an incidence of the parameter line
\[
\ell_C:\quad y=\rho(C)^2+A(C)^2x
\tag{2}
\]
with the Cartesian product
\[
\mathcal P_{\tan,\mathcal D}
=
\mathcal T_\alpha\times\mathcal D_0,\qquad
\mathcal T_\alpha
=
\{\tan^2(\alpha-\beta):\beta\text{ retained}\}.
\tag{3}
\]
The other new input is transverse to (1): all source circles that
produce one fixed line (2) have total source incidence at most \(4Q\).

Combining these two facts with the real Szemerédi--Trotter theorem and
the existing weighted point--circle bound first gives
\[
\boxed{
\kappa<\frac3{14}
\quad\Longrightarrow\quad
\text{the Euclidean hub branch is impossible}.
}
\tag{4}
\]
There is a further Euclidean gain.  For one fixed sign of \(A\), all
target points belonging to all circles over one parameter line lie
in the same ordinary plane \(x=A\).  Applying the planar
distinct-distance theorem only to this explicit target subset is
legitimate because every distance inside the subset belongs to the
original configuration's global distance set \(\mathcal D\).  It
bounds the subset size in terms of the global budget \(D=|\mathcal D|\)
without identifying the subset size with the global point count.  This
strengthens (4) to
\[
\boxed{
\kappa<\frac9{41}
\quad\Longrightarrow\quad
\text{the Euclidean hub branch is impossible}.
}
\tag{5}
\]
This strictly improves the previous hub-elimination range
\(\kappa<1/5\), since
\[
\frac9{41}-\frac15=\frac4{205}.
\]

Consequently, for every fixed \(\varepsilon>0\), the critical
cross-plane codegree forces at least \(t^{1-o(1)}\) distance labels,
each supported on a matching of
\[
\boxed{t^{\,9/41-\varepsilon-o(1)}}
\]
pairwise disjoint rich axial-plane pairs, with
\(t^{3-o(1)}\) representations in every matched cell.

This is an unconditional improvement of the **structural matching
exponent**, from \(1/5\) to \(9/41\).  It is not yet an improvement of
the \(3/5\) distinct-distance exponent in Erdős #1083.

## 1. Setup and exact quantifiers

Use the hub setup and all removals from
`EUCLIDEAN_HUB_INCIDENCE_EXPANSION_THEOREM.md`.  Thus:

- \(\Pi_\alpha\) is one fixed source plane;
- \(P_\alpha\subset\Pi_\alpha\), with \(|P_\alpha|\le Q\);
- there are at most \(M\) retained nonperpendicular target planes;
- every target-plane point set has size at most \(Q\);
- all retained source and target points are off the common
  \(z\)-axis; in particular every target signed radial coordinate
  \(v\), and hence \(A=cv\), is nonzero;
- \(\mathcal D_0\) is a selected set of \(L\) squared-distance labels;
- the full point configuration determines at most \(D\) squared
  distances;
- empty and zero-radius reverse circles are removed;
- equal normalized positive-radius reverse circles are merged.

The off-axis condition is not a new deletion made inside this note.
It is part of the inherited critical node: the common-axis
contribution was removed before the active axial-plane sets and the
cross-plane codegree were defined.  In the upstream ledger this costs
only the already recorded \(o(Q)\) and \(o(R_0)\) contributions.
Thus the hub mass used here is a hub mass on the disjoint off-axis
sets \(P_\gamma\); no axial point is silently charged to (8).

For a merged circle \(C\), put
\[
s(C)=|P_\alpha\cap C|,
\qquad
\mu(C)
=
\#\{(\beta,q,d):\Gamma_{\beta,q,d}=C,\ d\in\mathcal D_0\}.
\tag{6}
\]
Fixed-plane injectivity gives
\[
\mu(C)\le M.
\tag{7}
\]
The retained weighted incidence mass is
\[
W=\sum_Cs(C)\mu(C).
\tag{8}
\]
The total triple weight satisfies
\[
\mathsf T:=\sum_C\mu(C)\le MQL.
\tag{9}
\]

All statements below are finite and hold with absolute implied
constants.  The power-scale consequence assumes
\[
\begin{aligned}
M&=t^{1+o(1)},&
Q&=t^{3+o(1)},\\
L&=t^{2-2\kappa+o(1)},&
D&\le t^{3+o(1)},\\
W&\ge t^{7-3\kappa-o(1)}
\end{aligned}
\tag{10}
\]
for one fixed \(0<\kappa<1\).

Here is the mass bookkeeping behind the last line.  Empty circle
equations contribute no incidences.  The perpendicular plane was
removed before the matching-or-hub extraction.  Every zero-radius
triple contributes at most one source incidence, and the number of
all triples is at most
\[
\mathsf T\le MQL=t^{6-2\kappa+o(1)}.
\tag{11}
\]
The original hub mass is
\[
LH=t^{7-3\kappa-o(1)}.
\]
For every fixed \(\kappa<1\), the exponent gap is \(1-\kappa>0\).
Thus deleting all empty and zero-radius triples leaves
\[
W\ge LH-\mathsf T=t^{7-3\kappa-o(1)}.
\tag{12}
\]

## 2. The tangent--label line identity

Rotate \(\Pi_\alpha\) to the \(xz\)-plane.  In the signed coordinates
used by the reverse-circle theorem, write
\[
c_{\alpha,\beta}=\cos(\alpha-\beta),
\qquad q=(v,w)\in P_\beta.
\]
The reverse circle is
\[
u^2+z^2-2c_{\alpha,\beta}v\,u-2wz
+v^2+w^2-d=0.
\tag{13}
\]
Its centre and squared radius are
\[
(A,w)=(c_{\alpha,\beta}v,w),
\tag{14}
\]
\[
\begin{aligned}
\rho^2
&=A^2+w^2-(v^2+w^2-d)\\
&=d-(1-c_{\alpha,\beta}^2)v^2.
\end{aligned}
\tag{15}
\]
Since the perpendicular plane was removed, \(c_{\alpha,\beta}\ne0\).
Using \(A=c_{\alpha,\beta}v\), (15) becomes
\[
d
=
\rho^2+A^2
\frac{1-c_{\alpha,\beta}^2}{c_{\alpha,\beta}^2}
=
\rho^2+A^2\tan^2(\alpha-\beta),
\tag{16}
\]
which proves (1).

Angles of axial planes are taken modulo \(\pi\).  On any such
representative interval, a value of \(\tan^2(\alpha-\beta)\) has at
most two preimages.  Hence, with
\[
r(\ell)
=
|\ell\cap(\mathcal T_\alpha\times\mathcal D_0)|,
\tag{17}
\]
every merged circle obeys
\[
\boxed{\mu(C)\le2r(\ell_C).}
\tag{18}
\]
Indeed, fixed-plane injectivity says explicitly that for one fixed
\(\beta\) there is at most one pair \((q,d)\) with
\(\Gamma_{\beta,q,d}=C\).  Axial planes are indexed modulo \(\pi\);
tangent is injective on this quotient, while squaring identifies only
the two values \(x\) and \(-x\).  Hence a point
\((\tau,d)\in\ell_C\cap(\mathcal T_\alpha\times\mathcal D_0)\) lifts
to at most two target planes and therefore at most two triples.
This proves (18).  It remains valid when \(A=0\).

## 3. The parameter-line fibre cap

### Lemma 1

For every line
\[
\ell:y=b+ax,\qquad a\ge0,\quad b>0,
\tag{19}
\]
one has
\[
\boxed{
\sum_{\ell_C=\ell}s(C)\le4Q.
}
\tag{20}
\]

### Proof

The equality \(\ell_C=\ell\) fixes
\[
A(C)^2=a,\qquad \rho(C)^2=b.
\]
There are at most two choices \(A=\pm\sqrt a\).  Fix one of them and
one source point \(p=(u,z)\in P_\alpha\).  A circle in this fibre has
centre \((A,w)\), radius \(\sqrt b\), and contains \(p\) only if
\[
(u-A)^2+(z-w)^2=b.
\tag{21}
\]
Equation (21) has at most two real solutions for \(w\).  Therefore
one source point is incident to at most four circles in the complete
fibre over \(\ell\).  Summing over the at most \(Q\) source points
proves (20). \(\square\)

The positivity \(b>0\) is exactly the retained positive-radius
condition.  The same \(4Q\) bound would remain true for \(b=0\).

### Lemma 2 (planar target-fibre cap)

Fix a parameter line \(\ell:y=b+ax\), one choice
\(A\in\{\sqrt a,-\sqrt a\}\), and any collection \(\mathcal F\) of
merged reverse circles satisfying
\[
\ell_C=\ell,\qquad A(C)=A.
\]
Then
\[
\boxed{
\sum_{C\in\mathcal F}\mu(C)\ll D\log(2D).
}
\tag{22}
\]

#### Proof

Write the centre of \(C\) as \((A,w_C)\).  Distinct circles in this
fixed-\(A\), fixed-radius fibre have distinct \(w_C\)'s.  Every triple
\((\beta,q,d)\) producing \(C\) has, in ordinary Cartesian
coordinates,
\[
q=(A,A\tan(\beta-\alpha),w_C).
\tag{23}
\]
Fixed-plane injectivity implies that the \(\mu(C)\) triples use
\(\mu(C)\) distinct target planes.  Since \(A\ne0\) in the retained
off-axis, nonperpendicular branch, their tangent coordinates, and
hence their target points, are distinct.  Target points belonging to
different circles have different heights \(w_C\), so they are also
distinct across \(C\).

Consequently the original point configuration contains a planar
subset
\[
X_{\ell,A}\subset\{(A,y,z):y,z\in\mathbb R\}
\]
of exact size
\[
|X_{\ell,A}|=\sum_{C\in\mathcal F}\mu(C).
\tag{24}
\]
The Guth--Katz planar distinct-distance theorem gives
\[
|\Delta^2(X_{\ell,A})|
\gg\frac{|X_{\ell,A}|}{\log(2|X_{\ell,A}|)}.
\]
All these are distances of the original configuration, whose global
budget is \(D\).  Rearranging proves (22). \(\square\)

The cited input is Guth--Katz,
[*On the Erdős distinct distances problem in the plane*,
Annals of Mathematics 181 (2015)](https://arxiv.org/abs/1011.4105).
Squared distances and distances have equal cardinality.

## 4. Dyadic tangent--label capacity theorems

For dyadic \(s,u\ge1\), let
\[
\mathcal C_{s,u}
=
\{C:s\le s(C)<2s,\ u\le\mu(C)<2u\},
\tag{25}
\]
and put
\[
W_{s,u}=\sum_{C\in\mathcal C_{s,u}}s(C)\mu(C).
\tag{26}
\]

### Theorem 2

For every dyadic layer with \(u\ge4\),
\[
\boxed{
W_{s,u}
\ll
Q\left\{
\frac{(ML)^2}{u^2}+ML
\right\}.
}
\tag{27}
\]

### Proof

Let \(\Lambda_{s,u}\) be the set of distinct parameter lines
\(\ell_C\) represented in the layer.  By (18), every such line is
incident to at least \(u/2\) points of
\(\mathcal P_{\tan,\mathcal D}\).  This point set has size at most
\[
|\mathcal T_\alpha|\,|\mathcal D_0|\le ML.
\tag{28}
\]
The standard rich-line consequence of the real
Szemerédi--Trotter theorem gives
\[
|\Lambda_{s,u}|
\ll
\frac{(ML)^2}{u^3}+\frac{ML}{u}.
\tag{29}
\]
By Lemma 1,
\[
\sum_{\substack{C\in\mathcal C_{s,u}\\\ell_C=\ell}}s(C)
\le4Q.
\]
Since \(\mu(C)<2u\), summing first over every parameter-line fibre
and then using (29) gives
\[
W_{s,u}
<2u\sum_{\ell\in\Lambda_{s,u}}
\sum_{\substack{C\in\mathcal C_{s,u}\\\ell_C=\ell}}s(C)
\le8Qu|\Lambda_{s,u}|,
\]
which is (27). \(\square\)

### Theorem 3 (refined dyadic capacity)

Every dyadic layer with \(u\ge4\) also satisfies
\[
\boxed{
W_{s,u}
\ll
\left\{
\frac{(ML)^2}{u^3}+\frac{ML}{u}
\right\}
\min\{Qu,\;Ds\log(2D)\}.
}
\tag{30}
\]

#### Proof

The \(Qu\) fibre bound is the proof of Theorem 2.  For the other
bound, split the circles over one parameter line into the at most two
signs of \(A\).  In either sign class, Lemma 2 and \(s(C)<2s\) give
\[
\sum_Cs(C)\mu(C)
<2s\sum_C\mu(C)
\ll Ds\log(2D).
\]
The two signs change only the absolute constant.  Multiply the better
of these two fibre bounds by the rich-line count (29). \(\square\)

This bound is independent of the general point--circle theorem.  It
uses the global common label set \(\mathcal D_0\), the angular
coefficient, and the one-dimensional centre fibre simultaneously.

## 5. First exclusion: the \(4Q\) cap gives \(3/14\)

There are only
\[
O(\log Q\log M)=t^{o(1)}
\tag{31}
\]
nonempty dyadic \((s,u)\)-layers.  Therefore (10) supplies one layer
with
\[
W_{s,u}\ge t^{7-3\kappa-o(1)}.
\tag{32}
\]
Write
\[
u=t^{m+o(1)},\qquad 0\le m\le1.
\tag{33}
\]

### 5.1 The existing circle incidence inequality forces \(m\) up

Let \(N=|\mathcal C_{s,u}|\).  Since \(N u\le\mathsf T\), applying
the planar point--circle theorem to the \(N\) distinct merged circles
and multiplying by the upper dyadic weight gives
\[
\begin{aligned}
W_{s,u}\ll{}&
Q^{2/3}\mathsf T^{2/3}u^{1/3}\\
&+Q^{6/11}\mathsf T^{9/11}u^{2/11}t^{o(1)}
+Qu+\mathsf Tt^{o(1)}.
\end{aligned}
\tag{34}
\]
At (10), \(\mathsf T\le t^{6-2\kappa+o(1)}\).  The four exponents on
the right of (34) are
\[
6-\frac{4\kappa}{3}+\frac m3,\qquad
\frac{72}{11}-\frac{18\kappa}{11}+\frac{2m}{11},
\qquad3+m,\qquad6-2\kappa.
\tag{35}
\]
For \(0<\kappa<1/3\), comparison with (32) shows
\[
\boxed{
m\ge\frac{5-15\kappa}{2}-o(1).
}
\tag{36}
\]
Indeed, the first term would require the stronger
\(m\ge3-5\kappa-o(1)\); the third cannot reach (32) because
\(m\le1\); and the fourth misses by \(1-\kappa\).

### 5.2 The tangent--label inequality forces \(m\) down

For \(\kappa<3/14\), (36) gives
\[
m\ge\frac{25}{28}-o(1)>0.
\]
Thus the mass-carrying layer has \(u=t^{m+o(1)}\to\infty\), and in
particular \(u\ge4\) for all sufficiently large \(t\).  This is the
point at which Theorem 2 becomes applicable.  No rich-line estimate
is asserted for the bounded-\(u\) layers.

The two terms in Theorem 2 have critical exponents
\[
9-4\kappa-2m,\qquad6-2\kappa.
\tag{37}
\]
The second again misses (32) by \(1-\kappa\).  Therefore the first
must reach (32), which forces
\[
\boxed{
m\le1-\frac\kappa2+o(1).
}
\tag{38}
\]

Equations (36) and (38) are incompatible whenever
\[
\frac{5-15\kappa}{2}
>
1-\frac\kappa2,
\]
or equivalently
\[
\boxed{\kappa<\frac3{14}.}
\tag{39}
\]
This proves (4).

## 6. Refined exclusion: the planar fibre gives \(9/41\)

Continue with the mass-carrying layer (32), and write
\[
s=t^{a+o(1)},\qquad N=|\mathcal C_{s,u}|=t^{b+o(1)}.
\tag{40}
\]

For \(\kappa<9/41\), (36) gives
\[
m\ge\frac{35}{41}-o(1)>0.
\]
Hence again \(u\to\infty\), so both Theorems 2 and 3 apply to this
selected layer for all sufficiently large \(t\).

For \(\kappa<9/41\), the \(Q^{2/3}N^{2/3}\), \(+Q\), and \(+N\)
terms of the point--circle theorem cannot carry (32).  Indeed, after
dyadic weighting and the capacity \(Nu\le\mathsf T\), they would
respectively require
\[
m\ge3-5\kappa>1,\qquad
3+m\ge7-3\kappa,\qquad
6-2\kappa\ge7-3\kappa,
\]
all impossible.  Therefore the \(6/11,9/11\) term must carry the
layer.  Before substituting \(N\le\mathsf T/u\), its exponent
inequality is
\[
a+b
\le
\frac{18}{11}+\frac9{11}b+o(1),
\]
or
\[
11a+2b\le18+o(1).
\tag{41}
\]
The layer mass gives
\[
b\ge7-3\kappa-a-m-o(1).
\tag{42}
\]
Combining (41)--(42) yields
\[
\boxed{
a\le\frac{4+6\kappa+2m}{9}+o(1).
}
\tag{43}
\]

Now use the \(Ds\) branch of Theorem 3.  Since
\[
ML=t^{3-2\kappa+o(1)},\qquad D=t^{3+o(1)},
\]
its two exponents are
\[
9+a-4\kappa-3m,\qquad
6+a-2\kappa-m.
\tag{44}
\]
Their difference is
\[
3-2\kappa-2m>0
\]
throughout \(m\le1,\ \kappa<9/41\).  Thus the first is the larger,
and comparison with (32) forces
\[
\boxed{
a\ge3m-2+\kappa-o(1).
}
\tag{45}
\]
Equations (43) and (45) imply
\[
\boxed{
m\le\frac{22-3\kappa}{25}+o(1).
}
\tag{46}
\]
The point--circle lower bound (36) is still valid, so a surviving hub
would require
\[
\frac{5-15\kappa}{2}
\le
\frac{22-3\kappa}{25}+o(1).
\tag{47}
\]
The two sides cross exactly at
\[
\boxed{\kappa=\frac9{41}.}
\tag{48}
\]
For every fixed \(\kappa<9/41\), (47) fails by a fixed power of \(t\).
This proves (5).

## 7. Matching corollary

Apply the parameterized matching-or-hub theorem with
\[
\kappa=\frac9{41}-\varepsilon
\]
for any fixed \(\varepsilon>0\).  The hub alternative is impossible
by (48).  Hence the matching alternative is unconditional:

> At least \(t^{1-o(1)}\) labels have a matching of
> \(t^{9/41-\varepsilon-o(1)}\) pairwise disjoint rich plane pairs,
> and every matched cell has \(t^{3-o(1)}\) representations of that
> label.

No arrow from this matching conclusion to an improved global
distinct-distance exponent has been proved.

## 8. Exact method boundary

At
\[
\kappa=\frac9{41},
\tag{49}
\]
the exponent ledger
\[
\boxed{
\begin{aligned}
a&=\frac{32}{41}
&&\text{for }s=t^a,\\
b&=\frac{193}{41}
&&\text{for }N=t^b,\\
m&=\frac{35}{41}
&&\text{for }u=t^m,\\
p&=\frac{105}{41}
&&\text{for }|\mathcal T_\alpha\times\mathcal D_0|=t^p,\\
c&=\frac{105}{41}
&&\text{for the number of parameter lines}
\end{aligned}}
\tag{50}
\]
simultaneously saturates every exponent used above:
\[
\begin{aligned}
a+b+m&=7-3\kappa=\frac{260}{41},\\
b+m&=6-2\kappa=\frac{228}{41},\\
a+b&=\frac{18}{11}+\frac9{11}b,\\
c&=2p-3m=p,\\
c+3+a&=7-3\kappa,\\
\frac{5-15\kappa}{2}
&=m=\frac{22-3\kappa}{25}.
\end{aligned}
\tag{51}
\]
There are \(t^{b-c}=t^{88/41}\) circles over a typical parameter
line.  Their target points have exponent
\[
(b-c)+m=\frac{123}{41}=3,
\]
exactly saturating the planar distinct-distance cap, while their
source incidence exponent is
\[
(b-c)+a=\frac{120}{41}<3.
\]
Thus the new planar target-fibre cap, rather than the old \(4Q\)
source cap, is the active endpoint constraint.

This is an abstract exponent ledger, not a Euclidean realization.
It shows that the present combination of:

1. the general point--circle bound;
2. total triple capacity;
3. tangent--label Szemerédi--Trotter; and
4. the \(4Q\) source-fibre cap;
5. the planar target-fibre distinct-distance cap

cannot cross \(9/41\) at power scale without an additional inequality.
The next genuine target is an inverse theorem for simultaneous
near-equality in the point--circle incidence and tangent--label
point--line incidence problems, together with near-minimal planar
distinct distances in every large target fibre.

The Cartesian-product point--line estimate of Stevens--de Zeeuw does
not improve the threshold in the relevant range: here the forced rich-line
parameter satisfies \(u\le M\), precisely where the ordinary real
Szemerédi--Trotter rich-line bound is at least as strong at exponent
scale.

## 9. Claim boundary

### Proved

- the exact tangent--label identity (16);
- the repetition-to-rich-line inequality (18);
- the \(4Q\) parameter-line fibre cap (20);
- the dyadic capacity bound (27) for every \(u\ge4\);
- the planar target-fibre cap (22);
- the refined dyadic bound (30);
- exclusion of the hub for every fixed \(\kappa<9/41\);
- the unconditional matching exponent \(9/41-\varepsilon\).

### Not proved

- exclusion at the endpoint \(\kappa=9/41\);
- a Euclidean realization of the equality ledger (50);
- an inverse theorem for simultaneous near-equality;
- conversion of the structural matching result into an exponent above
  \(3/5\) for Erdős #1083;
- a standalone Q1-level paper from this theorem alone.

## 10. Reproduction

```bash
cd data/research_open/erdos1083_two_hour_q1_attack_2026-07-30/route_b
python3 verify_tangent_label_rich_line_hub.py
pytest -q test_verify_tangent_label_rich_line_hub.py
```
