# Erdős #1083: block-vs-diffuse breakthrough attack

Date: 2026-07-31

## 0. Verdict

This attack does **not** prove a new exponent for \(f_3(N)\).  It does
identify and exactly realize the obstruction hidden by the July 30
many-row synchronization theorem.

The live hub parameters are

\[
S=t^{7/9+o(1)},\quad U=t^{5/6+o(1)},\quad
H=t^{19/9+o(1)},\quad R=t^{1+o(1)},\quad D=t^{3+o(1)}.
\tag{0.1}
\]

Put

\[
B=SU=t^{29/18+o(1)}.
\tag{0.2}
\]

There is an exact abstract equality model in which the \(H\) row
spectra split into

\[
 G=t^{25/18+o(1)}
\tag{0.3}
\]

disjoint spectral blocks, each block consists of

\[
 q=t^{13/18+o(1)}
\tag{0.4}
\]

identical rows of size \(B\), and different blocks have disjoint
spectra.  This model has union size exactly \(t^{3+o(1)}\), exact
Cauchy--Schwarz intersection mass \(t^{40/9+o(1)}\), and exactly
\(t^{17/6+o(1)}\) intersecting ordered row pairs.  Thus the exponents
of the existing aggregate-support and pair-abundance argument are
compatible with a block-diagonal obstruction; spectral expansion
alone cannot exclude it.

The obstruction is not purely formal.  Section 5 gives three distinct
nonaligned reverse-circle rows, with all tangent squares in one
five-element universe, whose four-element anchor spectra are
**identical and representation-injective**.  It then gives, for every
\(k\), a genuine \(k\)-row Euclidean family with the same property.
This refutes the bold hypothesis that distinct centre heights, or even
arbitrarily many distinct centre heights, automatically separate the
spectra.  The construction pays
\(R\le kU\); it does not realize the much stronger endpoint reuse.

There is also a sharp information threshold.  The guaranteed
two-row overlap has exponent \(2/9\), whereas one fixed source sine
can already serve \(U=t^{5/6}\) labels.  Even the number of abundant
partners of one row has exponent \(13/18\), below
\(S=t^{14/18}\).  Hence neither the pair theorem nor its abundance
form forces reuse of a source sine.  A pairwise affine-rigidity attack
cannot start from the presently guaranteed overlap.

The next high-leverage theorem is therefore not another pairwise
intersection estimate.  It is a **block-vs-diffuse inverse theorem**
for the parabolic affine-copy system in Section 2.  In the block
branch it must classify many near-direct multi-slope tilings of one
set; in the diffuse branch it must retain a nondegenerate labelled
cycle across several rows.  Either output must then be connected to
the existing ruled-column escape theorem.

## 1. Inherited finite-real setup

Fix one anchor circle and suppress its common centre/radius
parameters except for \(\rho>0\).  Let

\[
 X\subset[-1,1],\qquad |X|=S,
\]

be the retained sine set on the anchor.  Let \(Z\) be the nonzero
height-difference set, \(|Z|=H\).  For every \(z\in Z\), let

\[
 T_z\subseteq T_*,\qquad |T_z|=U,qquad |T_*|=R.
\]

The row spectrum is

\[
 V_z
 =
 \rho^2+z^2+T_z+2\rho zX
 \subseteq \Delta^2(P).
\tag{1.1}
\]

Every \(\tau\in T_z\) is the square of a transverse target
coordinate.  The selected service label for its own circle is
\(\rho^2+\tau\).  Thus the model retains the actual tangent-square
reuse and is not a free sum-product abstraction.

The July 30 distinct-dilate theorem gives

\[
 \sum_z|V_z|
 \ge
 \frac{HSU}{1+R^2S/(HU)}.
\tag{1.2}
\]

At (0.1),

\[
 \frac{R^2S}{HU}\le t^{-1/6+o(1)}.
\tag{1.3}
\]

Since every row has size at most \(B=SU\), (1.2)--(1.3) imply

\[
 \sum_z(B-|V_z|)
 \le t^{-1/6+o(1)}HB.
\tag{1.4}
\]

This is stronger than merely saying that the average row expands:
for every fixed \(0<c<1/6\), all but
\(t^{c-1/6+o(1)}H\) rows have

\[
 |V_z|\ge(1-t^{-c})B.
\tag{1.5}
\]

Thus a surviving endpoint is already a near-direct-sum system in
almost every row.  Its compression must occur between rows.

## 2. Exact parabolic lift

The quadratic translation in (1.1) becomes linear after lifting the
target incidences.

### Theorem 1 (parabolic affine-copy equivalence)

Define the parameter-point set

\[
 \mathcal P
 =
 \{(z,b_{z,\tau}):z\in Z,\ \tau\in T_z\},
 \qquad
 b_{z,\tau}=\rho^2+z^2+\tau.
\tag{2.1}
\]

For \(x\in X\) and a squared-distance label \(d\), define the line

\[
 \ell_{x,d}:\qquad b=d-2\rho xz.
\tag{2.2}
\]

Then

\[
 d\in \rho^2+z^2+\tau+2\rho zX
\]

with witness \(x\) if and only if

\[
 (z,b_{z,\tau})\in\ell_{x,d}.
\tag{2.3}
\]

Consequently every parameter point is incident to the \(S\) lines
obtained from its \(S\) source sines, and the total incidence count is
exactly

\[
 I(\mathcal P,\mathcal L)=HSU.
\tag{2.4}
\]

#### Proof

Equation (2.3) is precisely

\[
 \rho^2+z^2+\tau=d-2\rho xz,
\]

which rearranges to (1.1).  There are \(HU\) parameter points and
one incidence for every triple \((z,\tau,x)\), proving (2.4).
\(\square\)

This formulation is useful because it identifies the exceptional
object exactly: \(HU\) affine maps

\[
 x\longmapsto b_{z,\tau}+2\rho zx
\tag{2.5}
\]

send the whole set \(X\) into the same \(D\)-element distance
universe, and their parameter pairs lie on \(R\) vertical translates
of a parabola.

It also explains why a generic point--line estimate does not close
the endpoint.  The potential Cartesian line family has size

\[
 |X|D=t^{34/9+o(1)},
\]

whereas (2.4) has exponent (67/18); the line-count term is larger
by (1/18).  The missing information is not plain incidence
cardinality but simultaneous containment of whole affine copies and
the parabolic restriction (2.1).

## 3. Exact spectral block extremizer

The following finite lemma isolates the equality geometry discarded
by the previous Cauchy--Schwarz step.

### Theorem 2 (exact block equality and classification)

Let \(V_1,\ldots,V_H\) be \(B\)-element subsets of a \(D\)-element
universe.  Write

\[
 r_d=\#\{i:d\in V_i\}.
\]

Then

\[
 \sum_{i\ne j}|V_i\cap V_j|
 =\sum_dr_d(r_d-1)
 \ge \frac{H^2B^2}{D}-HB.
\tag{3.1}
\]

Assume \(q=HB/D\) is an integer.  Equality holds in (3.1) if and
only if every label has degree \(q\).

If, in addition,

\[
 |V_i\cap V_j|\in\{0,B\}
 \qquad(i\ne j),
\tag{3.2}
\]

then the rows partition into \(H/q\) classes of \(q\) identical
spectra, and the spectra belonging to different classes are
disjoint.  Conversely, this block system satisfies equality in
(3.1).

#### Proof

The identity in (3.1) is double counting.  Since
\(\sum_d r_d=HB\), Cauchy--Schwarz gives

\[
 \sum_dr_d^2\ge (HB)^2/D,
\]

with equality exactly when all \(r_d=HB/D=q\).  Subtracting \(HB\)
proves the first assertion.

Under (3.2), positive intersection means intersection \(B\), and two
\(B\)-element sets with \(B\)-element intersection are equal.
Equality is an equivalence relation on the rows.  Different classes
are disjoint.  Every label in the spectrum of a class has degree
equal to the size of that class.  The equality condition \(r_d=q\)
therefore makes every class have size \(q\).  The converse is
immediate. \(\square\)

### Lemma 2A (two-defect certificate for stability)

In the notation of Theorem 2, allow \(q=HB/D\) to be real and define

\[
 \mathfrak V
 :=\sum_d(r_d-q)^2,\qquad
 a_{ij}:=|V_i\cap V_j|,
\]

\[
 \mathfrak F
 :=\sum_{i\ne j}a_{ij}(B-a_{ij}).
\]

Then the label-degree defect is exactly

\[
 \boxed{\mathfrak V
 =\sum_{i,j}a_{ij}-\frac{H^2B^2}{D}.}
\tag{3.2a}
\]

For every \(0<\eta<1/2\), the number \(M_\eta\) of ordered pairs
whose intersection is genuinely intermediate,

\[
 \eta B\le a_{ij}\le(1-\eta)B,
\]

satisfies

\[
 \boxed{M_\eta\le
 \frac{\mathfrak F}{\eta(1-\eta)B^2}.}
\tag{3.2b}
\]

Moreover, \(\mathfrak V=\mathfrak F=0\) if and only if the exact
block classification of Theorem 2 holds.

#### Proof

Expanding the square and using \(\sum_d r_d=HB=Dq\) gives

\[
 \mathfrak V
 =\sum_dr_d^2-\frac{H^2B^2}{D}
 =\sum_{i,j}a_{ij}-\frac{H^2B^2}{D}.
\]

Every intermediate pair contributes at least
\(\eta(1-\eta)B^2\) to \(\mathfrak F\), proving (3.2b).  Finally,
\(\mathfrak V=0\) makes all label degrees equal, while
\(\mathfrak F=0\) forces every \(a_{ij}\) to be \(0\) or \(B\);
Theorem 2 applies.  The converse is immediate. \(\square\)

### Endpoint substitution

Take \(B=SU\).  The block size forced by equality is

\[
 q=\frac{HB}{D}
 =t^{19/9+29/18-3+o(1)}
 =\boxed{t^{13/18+o(1)}}.
\tag{3.3}
\]

The number of blocks is

\[
 G=\frac Hq=\frac D B
 =\boxed{t^{25/18+o(1)}}.
\tag{3.4}
\]

The number of ordered intersecting row pairs is

\[
 Gq(q-1)=t^{25/18+26/18+o(1)}
 =\boxed{t^{17/6+o(1)}},
\tag{3.5}
\]

and their total intersection mass is

\[
 Gq(q-1)B
 =t^{25/18+26/18+29/18+o(1)}
 =\boxed{t^{40/9+o(1)}}.
\tag{3.6}
\]

The union has size

\[
 GB=t^{25/18+29/18}=t^3.
\tag{3.7}
\]

Thus (3.3)--(3.7) simultaneously match the global distance budget,
the Cauchy--Schwarz collision exponent, and the (17/6) abundance
exponent.  This does not claim that the full asymptotic block design
has been realized by Euclidean rows.  It proves that the current
spectral inequalities alone cannot distinguish it from an endpoint
configuration.

## 4. The pairwise source-rigidity threshold is not reached

### Lemma 3 (source-witness threshold)

Fix two rows.  Let \(\Omega\subseteq V_z\cap V_{z'}\), and choose one
representation

\[
 d=\rho^2+z^2+\tau_d+2\rho zx_d
\]

in the first row for every \(d\in\Omega\).  If \(k\) different
source values \(x_d\) are used, then

\[
 |\Omega|\le kU.
\tag{4.1}
\]

In particular, forcing two distinct source sines requires
\(|\Omega|>U\), and forcing three requires \(|\Omega|>2U\).

#### Proof

For a fixed \(x\), varying \(\tau\in T_z\) produces at most \(U\)
labels.  Sum this bound over the \(k\) used values of \(x\).
\(\square\)

At the endpoint the guaranteed pair overlap is only

\[
 t^{2/9-o(1)}=t^{4/18-o(1)},
\]

whereas

\[
 U=t^{15/18-o(1)}.
\tag{4.2}
\]

The gap is \(11/18\).  Therefore no affine correspondence between
two or three source sine values follows from the pair theorem.

The abundance conclusion also stops immediately before a useful
pigeonhole.  In the concentrated block model, one row has

\[
 q=t^{13/18+o(1)}
\]

partners, while

\[
 S=t^{14/18+o(1)}.
\tag{4.3}
\]

The partner set can be assigned injectively to source sines.  The
gap is exactly \(1/18\).  Thus “many synchronized pairs” does not by
itself create a repeated source witness or a three-row holonomy.

## 5. A genuine three-row affine-quadratic exception

The strongest naive hypothesis was:

> three different nonaligned height rows cannot have identical
> anchor spectra once all tangent squares lie in one small universe.

It is false.

### Proposition 4 (three identical nonaligned spectra)

Take \(\rho=1\),

\[
 X=\{0,1\},\qquad
 T_*=\{10,11,12,13,14\},
\]

and three distinct height differences

\[
 z_1=-\frac32,\qquad z_2=-\frac12,\qquad z_3=\frac12.
\]

Set

\[
 T_{z_1}=\{11,12\},\qquad
 T_{z_2}=\{11,14\},\qquad
 T_{z_3}=\{10,13\}.
\tag{5.1}
\]

Then every row map \(X\times T_z\to V_z\) is injective and

\[
 \boxed{
 V_{z_1}=V_{z_2}=V_{z_3}
 =\left\{\frac{45}4,\frac{49}4,
          \frac{57}4,\frac{61}4\right\}.}
\tag{5.2}
\]

Moreover, the two labels

\[
 \left\{\frac{49}4,\frac{61}4\right\}
\]

are witnessed with the single source value \(x=0\) in the
\(z=-1/2\) row and the single source value \(x=1\) in the
\(z=1/2\) row.

#### Proof

Substitute (5.1) into

\[
 1+z^2+\tau+2zx.
\]

The four values in every row are exactly (5.2), without repetition.
The fixed-source statement follows from

\[
 1+\frac14+\{11,14\}
 =
 1+\frac14+\{10,13\}+1.
\]

This is a genuine Euclidean reverse-circle chart.  Choose any
\(A>1\), put the anchor circle in \(y=0\) with centre \((A,0)\) and
radius one, and take source sines \(0,1\).  The row of height
difference \(z\) has centre height \(-z\); for every
\(\tau\in T_z\), use the target point

\[
 (A,\sqrt\tau,-z)
\]

and selected label \(1+\tau\).  All targets are off the common axis
and lie in nonperpendicular axial planes.  Translating the two anchor
source points to each row circle makes every row a two-incidence,
two-producing-triple positive-radius reverse circle.  Direct
Cartesian expansion is precisely the formula above. \(\square\)

This example is small, not an asymptotic endpoint construction.  Its
logical role is exact: distinct/nonaligned heights and a common
tangent universe do not forbid a multirow spectral block.  Any
asymptotic exclusion has to use quantitative density across the
whole network.

The phenomenon is not bounded to three rows.

### Theorem 5 (arbitrarily large Euclidean identical-spectrum blocks)

For every integer \(k\ge1\), there is a genuine fixed-\((A,\rho)\)
reverse-circle bundle with:

- \(k\) distinct nonaligned height rows;
- the common two-element source sine set \(X=\{0,1\}\);
- \(U=2^{k-1}\) positive tangent squares per row;
- one tangent universe of size \(R\le k2^{k-1}=kU\); and
- one common \(2^k=2U\)-element anchor spectrum;

such that every row map is injective.

#### Proof

Take \(\rho=1\) and the superincreasing odd weights

\[
 a_i=3^i,\qquad 0\le i<k.
\]

Their subset-sum set

\[
 \mathcal A
 =\left\{\sum_{i=0}^{k-1}\varepsilon_i a_i:
 \varepsilon_i\in\{0,1\}\right\}
\tag{5.3}
\]

has exactly \(2^k\) elements.  Let \(\mathcal A_i\) be the
\(2^{k-1}\)-element subset with \(\varepsilon_i=0\), put

\[
 z_i=\frac{a_i}{2},
\]

and choose a constant \(C>\max_i a_i^2/4\).  Define

\[
 T_{z_i}
 =C+\mathcal A_i-\frac{a_i^2}{4}.
\tag{5.4}
\]

Every element of (5.4) is positive, and

\[
\begin{aligned}
1+z_i^2+T_{z_i}+2z_iX
&=1+C+\mathcal A_i+\{0,a_i\}\\
&=\boxed{1+C+\mathcal A}.
\end{aligned}
\tag{5.5}
\]

The base-three expansion makes the last sum direct, so every row map
is injective.  Taking

\[
 T_*=\bigcup_iT_{z_i}
\]

gives \(R\le kU\).  Realize the rows by the circle-axis coordinates
in Proposition 4, using target transverse coordinate
\(\sqrt\tau\) for every positive \(\tau\in T_{z_i}\).  This produces
actual positive-radius nonaligned reverse circles. \(\square\)

Theorem 5 is a decisive no-go for any bounded-exception
classification based only on nonalignment.  It is also quantitatively
honest about what remains: its tangent-universe ratio is

\[
 \frac RU\le k,
\]

whereas the endpoint asks for \(R/U=t^{1/6+o(1)}\) while potentially
supporting polynomially many rows.  The next theorem must exploit
this global reuse gap, not merely the existence of several equal
spectra.

There is nevertheless a strong exact classification of the dilation
parameters in any literal block.  It is the main positive theorem of
this attack.

### Theorem 6 (torsion-free direct-tiling rank theorem)

Let \(X,V\subset\mathbb R\) be finite with

\[
 |X|=S\ge2,
\]

and suppose that, for every \(i\in I\), there are a nonzero real
\(\lambda_i\) and a finite set \(A_i\subset\mathbb R\) such that

\[
 \boxed{V=A_i\oplus\lambda_iX.}
\tag{5.6}
\]

Here \(\oplus\) means that every element of \(V\) has a unique
representation.  Put

\[
 W_i
 =\operatorname{span}_{\mathbb Q}
   \bigl(\lambda_i(X-X)\bigr)
 \subset\mathbb R.
\tag{5.7}
\]

Then every finite subfamily \(J\subseteq I\) satisfying

\[
 W_i\cap W_j=\{0\}\qquad(i\ne j\in J)
\tag{5.8}
\]

obeys

\[
 \boxed{S^{|J|}\le |V|.}
\tag{5.9}
\]

Equivalently, the graph on the dilation indices in which \(i\sim j\)
when \(W_i\cap W_j\ne\{0\}\) has independence number at most

\[
 \boxed{\lfloor\log_S|V|\rfloor.}
\tag{5.10}
\]

#### Proof

Fix a finite \(J\) satisfying (5.8).  Let \(\Gamma\) be the additive
subgroup of \(\mathbb R\) generated by all elements occurring in
\(V,X,A_i,\lambda_iX\) for \(i\in J\).  It is finitely
generated and torsion free, hence

\[
 \Gamma\cong\mathbb Z^r
\]

for some \(r\).  Its integral group ring is the Laurent polynomial
UFD

\[
 \mathbb Z[\Gamma]
 \cong
 \mathbb Z[x_1^{\pm1},\ldots,x_r^{\pm1}].
\]

For a finite set \(Y\subset\Gamma\), write its mask polynomial as

\[
 P_Y=\sum_{y\in Y}X^y.
\]

Unique representation in (5.6) is exactly the coefficientwise
identity

\[
 P_V=P_{A_i}P_{\lambda_iX}.
\tag{5.11}
\]

Thus every \(P_{\lambda_iX}\) divides \(P_V\).

We claim that the factors belonging to a family satisfying (5.8) are
pairwise coprime.  If a nonunit \(F\) divided both
\(P_{\lambda_iX}\) and \(P_{\lambda_jX}\), the Newton polytope product
identity would put the direction space of \(\operatorname{Newt}(F)\)
inside both \(W_i\otimes_{\mathbb Q}\mathbb R\) and
\(W_j\otimes_{\mathbb Q}\mathbb R\).  Condition (5.8) makes this
direction space zero.  Hence \(F\) is a monomial times an integer
constant.  Mask polynomials have content one, so that constant is
\(\pm1\), making \(F\) a unit after all.  This proves the claim.

Because the Laurent polynomial ring is a UFD, the product of the
pairwise coprime factors divides \(P_V\):

\[
 P_V=Q\prod_{i\in J}P_{\lambda_iX}
\tag{5.12}
\]

for an integral Laurent polynomial \(Q\).  Apply the augmentation map
which sends every monomial to one.  It sends \(P_Y\) to \(|Y|\), so

\[
 |V|=Q(1)S^{|J|}.
\tag{5.13}
\]

The left side is positive, hence \(Q(1)\) is a positive integer.
Equation (5.9) follows. \(\square\)

### Endpoint consequence of Theorem 6

In an exact identical-spectrum block from Section 3, near-injectivity
upgraded to exact injectivity gives

\[
 V=(\rho^2+z^2+T_z)\oplus(2\rho zX),
 \qquad |V|=SU.
\tag{5.14}
\]

Therefore a family of pairwise transverse rational dilation spaces
has size at most

\[
 \left\lfloor\log_S(SU)\right\rfloor.
\tag{5.15}
\]

At the endpoint exponent ratios,

\[
 \log_S(SU)
 \longrightarrow
 \frac{7/9+5/6}{7/9}
 =\boxed{\frac{29}{14}<3}.
\tag{5.16}
\]

Thus an exact polynomial-size block has at most **two** pairwise
transverse dilation-space representatives.  A maximal transverse
subfamily has size at most two, so every remaining height dilation
space intersects one of those two representatives nontrivially.

Writing

\[
 W=\operatorname{span}_{\mathbb Q}(X-X),
\]

the intersection \(\lambda_iW\cap\lambda_jW\ne\{0\}\) explicitly
means

\[
 \frac{\lambda_i}{\lambda_j}
 \in
 \frac{W\setminus\{0\}}{W\setminus\{0\}}.
\tag{5.17}
\]

Thus all exact-block slopes lie in the union of at most two
multiplicative translates of this quotient set.

When \(X-X\) spans a one-dimensional vector space over
\(\mathbb Q\), this has the especially concrete form:

\[
\boxed{
\text{all height ratios lie in at most two rational
 commensurability clusters}.}
\tag{5.18}
\]

The base-three construction in Theorem 5 lies in one such cluster;
all of its slopes are rationally commensurate.  The theorem therefore
both explains that construction and proves that generic
incommensurate slopes cannot form an exact endpoint block.

Theorem 6 is exact rather than stable.  Passing from the near-direct,
near-common endpoint rows to the mask-polynomial factorization
(5.11) is now the precise stability gap.  This is a much narrower
problem than unrestricted cross-height energy.

The bound is sharp.  Take \(X=\{0,1\}\) and positive numbers
\(a_1,\ldots,a_k\) linearly independent over \(\mathbb Q\), for
example square roots of distinct primes.  Their \(2^k\) subset sums
form \(V_0\).  With \(\lambda_i=a_i\),

\[
 V_0=V_{0,i}\oplus\{0,a_i\},
\]

where \(V_{0,i}\) consists of the subset sums omitting \(a_i\).
The spaces \(a_i\mathbb Q\) are pairwise transverse and

\[
 |V_0|=2^k=|X|^k.
\]

Adding the parabolic translations exactly as in (5.4) realizes these
factorizations as genuine identical reverse-circle spectra.  Thus
(5.9) cannot be improved without using the small common tangent
universe or other endpoint geometry.

### Corollary 7 (classification of the literal endpoint equality model)

Suppose a finite reverse-circle row family has all of the following
exact properties:

1. every row map is injective and has size \(B=SU\);
2. equality holds in the label-degree Cauchy--Schwarz inequality;
3. every two row spectra are either disjoint or identical; and
4. the common union has size \(D\), with \(q=HB/D\) integral.

Then the rows partition into \(H/q\) disjoint spectral blocks of
size \(q\).  Inside every block, the graph whose vertices are heights
and whose edges join rationally intersecting dilation spaces has
independence number at most

\[
 \lfloor\log_S(SU)\rfloor.
\]

In particular, at the exact \(2/9\) exponent ledger, every block is
covered by the rational-intersection neighbourhoods of at most two
representative height dilations.

#### Proof

Theorem 2 supplies the block partition.  On one block, the common
spectrum and row injectivity give the direct decompositions (5.14).
Apply Theorem 6, then use (5.16). \(\square\)

Corollary 7 is not the desired stability theorem, but it is a closed
classification of the exact equality object.  It replaces the former
unspecified phrase “affine-quadratic exceptional family” with a
concrete two-representative rational-intersection structure.

### Theorem 8 (parabolic resolution and fixed-difference compression)

Let \(Z\) be one exact identical-spectrum block of \(q\) rows.  Assume
that, for every \(z\in Z\),

\[
 V=(\rho^2+z^2+T_z)\oplus(2\rho zX),
 \qquad |T_z|=U,\qquad T_z\subseteq T_*,
\tag{5.19}
\]

where \(|X|=S\), \(|T_*|=R\), and hence \(|V|=SU\).  For
\(\tau\in T_z\), put

\[
 C_{z,\tau}
 :=\rho^2+z^2+\tau+2\rho zX.
\tag{5.20}
\]

Then:

1. for every fixed \(z\), the \(U\) cells \(C_{z,\tau}\) partition
   \(V\);
2. every \(v\in V\) belongs to exactly one cell from each row, hence
   to exactly \(q\) cells in total;
3. the exact cross-row intersection identity is

   \[
   \boxed{
   \sum_{\substack{z,z'\in Z\\z\ne z'}}
   \ \sum_{\tau\in T_z,\ \tau'\in T_{z'}}
   |C_{z,\tau}\cap C_{z',\tau'}|
   =q(q-1)SU;}
   \tag{5.21}
   \]

4. some fixed difference \(\delta\in T_*-T_*\) supports at least

   \[
   \boxed{\frac{q(q-1)SU}{|T_*-T_*|}
   \ge \frac{q(q-1)SU}{R^2}}
   \tag{5.22}
   \]

   tuples \((z,z',x,x')\), with \(z\ne z'\), satisfying

   \[
   \boxed{
   z^2-z'^2+2\rho(zx-z'x')=\delta.}
   \tag{5.23}
   \]

Independently, if \(r_\tau:=|\{z:\tau\in T_z\}|\), then

\[
 \max_\tau r_\tau\ge\frac{qU}{R}
\tag{5.24}
\]

and

\[
 \boxed{
 \sum_{z\ne z'}|T_z\cap T_{z'}|
 =\sum_\tau r_\tau(r_\tau-1)
 \ge\frac{q^2U^2}{R}-qU.}
\tag{5.25}
\]

#### Proof

The direct decomposition (5.19) proves the first assertion.  It also
gives, for each pair \((z,v)\), unique \(\tau\in T_z\) and \(x\in X\)
with \(v\in C_{z,\tau}\), proving the second assertion.  Count ordered
triples \((v,z,z')\) with \(v\in V\) and \(z\ne z'\) in two ways to
obtain (5.21).

Every point counted on the left of (5.21) has unique witnesses
\(x,x'\) and obeys

\[
 \rho^2+z^2+\tau+2\rho zx
 =\rho^2+z'^2+\tau'+2\rho z'x'.
\]

Group these \(q(q-1)SU\) witnesses by
\(\delta=\tau'-\tau\in T_*-T_*\).  Pigeonholing proves (5.22) and
(5.23).  Finally, \(\sum_\tau r_\tau=qU\); the maximum-degree bound is
averaging, and Cauchy--Schwarz gives
\(\sum_\tau r_\tau^2\ge(qU)^2/R\), proving (5.25).
\(\square\)

At the endpoint, (5.22) guarantees a fixed quadratic difference with

\[
 \frac{q^2SU}{R^2}
 =t^{\,2(13/18)+29/18-2+o(1)}
 =\boxed{t^{19/18+o(1)}}
\tag{5.26}
\]

representations.  Equations (5.24)--(5.25) also give, respectively,

\[
 \max_\tau r_\tau\ge t^{5/9+o(1)},\qquad
 \sum_{z\ne z'}|T_z\cap T_{z'}|
 \ge t^{19/9+o(1)}.
\tag{5.27}
\]

This is a second synchronization law hidden inside the spectral
block.  It does **not** by itself close the endpoint: a single
tangent-label fibre contains only \(t^{5/9+o(1)}\) rows, and even
disjoint copies from that fibre contribute only
\(t^{4/3+o(1)}<|V|=t^{29/18+o(1)}\) values.  The actionable next
question is instead whether the fixed-difference energy (5.23) forces
one of the two rational-intersection representatives from Corollary 7
to become an affine-height chart.  This formulation retains all
block mass and removes both tangent variables.

## 6. Bold hypotheses tested

| Hypothesis | Verdict | Exact reason |
|---|---|---|
| Nonaligned heights force different spectra | **REFUTED** | Theorem 5 gives arbitrarily many identical, injective Euclidean spectra. |
| A (t^{2/9}) pair overlap forces affine source rigidity | **REFUTED AS AN INFERENCE** | Lemma 3 needs overlap (>U=t^{5/6}). |
| Pair abundance forces reuse of one source sine | **REFUTED AS AN INFERENCE** | Partner exponent (13/18) is below source exponent (14/18). |
| The spectral graph alone forces union (>t^3) | **REFUTED** | Theorem 2's block model has union exactly (t^3). |
| A generic point--line theorem on the parabolic lift closes the hub | **NO** | Its line-count term misses in the wrong direction by (1/18). |
| Generic incommensurate slopes can form an exact polynomial block | **REFUTED** | Theorem 6 permits at most two pairwise transverse dilation spaces at the endpoint ratio. |
| The literal equality endpoint has no usable classification | **REFUTED** | Corollary 7 gives blocks, then at most two rational-intersection representatives per block. |
| The parabolic block exception can occur asymptotically at the critical endpoint | **OPEN** | The arbitrary-row construction is commensurate and does not meet the endpoint reuse. |

## 7. New branch-changing target

The old target asked for an undifferentiated upper bound on

\[
 \sum_{z\ne z'}|V_z\cap V_{z'}|.
\]

The exact block model shows that this is too coarse.  The next theorem
should instead have the following form.

### Required block-vs-diffuse parabolic inverse theorem

For the regular rows satisfying (1.1), (1.3), and (1.5), one of the
following occurs with fixed-power quantitative losses.

1. **Diffuse branch.**  A positive proportion of the intersection
   mass lies on a bounded labelled row cycle whose canonical
   witnesses use at least three noncollinear pairs
   \((x,x')\). Subtracting two label equations then pins the two
   heights by a nonsingular \(2\times2\) system; compatibility around
   the cycle forces a polynomial-height/affine coefficient chart.
2. **Block branch.**  There are
   \(t^{13/18-o(1)}\) distinct slopes \(z\) for which one
   \(B=t^{29/18-o(1)}\)-element set is, up to
   \(o(B)\) errors, tiled directly as

   \[
   V\approx \bigsqcup_{\tau\in T_z}
   (\rho^2+z^2+\tau+2\rho zX),
   \tag{7.1}
   \]

   with every \(T_z\subseteq T_*\). These are parabolically
   constrained multi-slope tilings of one real set.  They must be
   stabilized to the exact factorization in Theorem 6.  That theorem
   then leaves at most two rationally intersecting dilation-space
   clusters; those clusters must be converted into affine-digit/GAP
   families and sent to the existing ruled-column escape theorem.

The theorem has to be network-level.  Lemma 3 proves that no argument
which first selects one synchronized pair and then asks that pair for
source diversity can reach either branch.

## 8. Relation to the matching branch

The matching branch and the hub block branch are two support-graph
extremes:

- the matching branch separates plane endpoints for one label but
  loses most of the global (t^{13}) energy;
- the block hub branch concentrates row spectra into almost identical
  classes and loses source-witness coherence by exactly (1/18).

A genuine unifying theorem must therefore be **mass preserving**, not
just cardinality preserving.  A sufficient formulation is:

> From the full weighted plane--label tensor, extract either a bounded
> properly labelled cycle whose endpoint point sets retain a fixed
> power of the original cell mass, or a parabolic multi-slope tiling
> of the form (7.1).  The first alternative supplies coefficient
> holonomy; the second supplies a ruled affine chart.

No such theorem is proved here.  The point of the present attack is
that its two outputs are now forced by exact equality models rather
than selected heuristically.

## 9. Claim boundary

### PROVED

- the parabolic point--line equivalence (2.1)--(2.5);
- the near-direct-row consequence (1.4)--(1.5);
- the exact abstract block equality/classification theorem;
- every endpoint exponent in (3.3)--(3.7);
- the source-witness threshold (4.1);
- the (1/18) partner/source threshold gap;
- the genuine three-row identical-spectrum reverse-circle model.
- the arbitrary-(k) hypercube identical-spectrum construction.
- the torsion-free direct-tiling rank theorem and its endpoint
  two-transverse-class consequence.
- the combined classification of the literal endpoint equality
  model.
- the parabolic-resolution identity, fixed-difference compression,
  and tangent-fibre degree bounds for an exact block.

### COMPUTATIONAL / EXACT FINITE CERTIFICATE

- the rational endpoint arithmetic;
- a (12)-row, four-block exact set-system instance;
- all twelve circle--axis formula records in Proposition 4;
- the parabolic lift on all six parameter points and twelve
  incidences.
- the endpoint \(19/18\), \(5/9\), \(19/9\), and \(4/3\)
  parabolic-resolution exponents.

### REFUTED

- pairwise nonalignment alone separates spectra;
- the current pair-overlap size forces two source sine witnesses;
- the existing abstract spectral ledger excludes block compression.

### CONDITIONAL / OPEN

- stability from a near-extremal spectral ledger to a near-block or
  diffuse-cycle alternative;
- stability of the group-ring divisibility theorem under
  (o(SU)) row errors;
- endpoint-scale exclusion/classification of the multi-slope tiling
  branch;
- a mass-preserving matching-cycle theorem;
- any fixed (delta>0) in
  (f_3(N)\gg N^{3/5+\delta});
- Erdős #1083.

### Priority boundary

Mask-polynomial factorizations of direct sumsets and Newton-polytope
factor arguments are standard tools in tiling theory.  No exhaustive
MathSciNet/zbMATH priority search was completed for the precise bound
in Theorem 6.  It is proved here and new to the AMRA proof tree, but it
must not yet be advertised as a globally novel standalone theorem.

## 10. Reproduction

```bash
cd data/research_open/q1_breakthrough_campaign_2026-07-31/erdos1083
python3 verify_spectral_block_breakthrough.py
pytest -q
```

The finite verifier corroborates exact arithmetic and supplies
falsification examples.  The all-parameter claims rest on the proofs
above.
