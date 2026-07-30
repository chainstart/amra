# Angular-starvation branch: forced cross-plane codegree and the last transfer

Date: 2026-07-30

## 1. Outcome

This note attacks the fourth branch isolated in
`XI_EUCLIDEAN_DICHOTOMY_ATTACK.md`.  It obtains one genuinely new statistic
that is forced by the inherited proof tree:

\[
\boxed{
\mathfrak C_{\rm plane}
\ge N^{13/5-o(1)}.
}
\]

Here \(\mathfrak C_{\rm plane}\) counts equal-distance coincidences shared
by **different ordered pairs of active axial planes**.  This is stronger
than the old one-angle marginals and cannot be supplied by the diagonal
energy of individual plane pairs.

The proof has two parts:

1. global Cauchy--Schwarz, using \(D=N^{3/5+o(1)}\), forces total
   cross-plane distance energy \(N^{13/5-o(1)}\);
2. a two-degree-of-freedom circle-incidence bound limits the sum of the
   individual plane-pair energies to \(N^{12/5+o(1)}\).

Thus a full factor \(N^{1/5-o(1)}\) must come from reuse of the same
distance labels across different plane pairs.

This still does not prove an unconditional \(\varepsilon\)-improvement.
No established inverse theorem converts this distance-label codegree into
same-radius angular incidence concentration.  The exact sufficient transfer
is identified below.  A Euclidean construction saturates all old angular
marginals, the maximum possible normalized rotation codegree, and the
critical \(N^{7/5}\) radius–angle energy while keeping Xi at
\(N^{3/5+o(1)}\).  Its source part has \(\Theta(N)\) distances, so it
deliberately fails the newly forced cross-plane reuse.  This precisely
locates where the global distance hypothesis must enter.

## 2. Inherited data

Let \(\mathcal A\) be the selected active axial planes after removing the
common-axis contribution.  At the critical node,
\[
|\mathcal A|=M=N^{1/5-o(1)},\qquad
q_\alpha=Q=N^{3/5-o(1)},\qquad
r_\alpha=R=N^{1-o(1)},
\tag{1}
\]
and the total number of nonzero distances is
\[
D=N^{3/5+o(1)}.
\tag{2}
\]

For a circular fibre \(C\), write
\[
a_C=|A_C|,\qquad
s_{C,\alpha}=|A_C\cap\{\alpha,\alpha+\pi\}|,
\qquad
w_{C,\alpha}=|A_C\cap(A_C+2\alpha)|.
\tag{3}
\]
Then
\[
\sum_Cs_{C,\alpha}=q_\alpha,\qquad
\sum_Cw_{C,\alpha}=r_\alpha,\qquad
\sum_Ca_C=N.
\tag{4}
\]

## 3. The strongest forced rotation codegree

Define the normalized rotation codegree
\[
\mathfrak C_{\rm rot}
:=\sum_{\alpha,\beta\in\mathcal A}
\sum_C\frac{w_{C,\alpha}w_{C,\beta}}{a_C},
\tag{5}
\]
omitting empty fibres.

### Proposition 1 (forced second rotation moment)

\[
\boxed{
\mathfrak C_{\rm rot}
\ge \frac{(\sum_\alpha r_\alpha)^2}{N}
\ge \frac{M^2R^2}{N}.
}
\tag{6}
\]
Since \(w_{C,\alpha}\le a_C\),
\[
\mathfrak C_{\rm rot}\le M^2N.
\tag{7}
\]
At (1), both bounds have exponent
\[
\boxed{\mathfrak C_{\rm rot}=N^{7/5+o(1)}}.
\tag{8}
\]

### Proof

Put \(x_C=\sum_\alpha w_{C,\alpha}\).  Weighted Cauchy--Schwarz gives
\[
\sum_C\frac{x_C^2}{a_C}
\ge\frac{(\sum_Cx_C)^2}{\sum_Ca_C}
=\frac{(\sum_\alpha r_\alpha)^2}{N},
\]
which is (6).  The pointwise estimate
\[
\sum_{\alpha,\beta}
\frac{w_{C,\alpha}w_{C,\beta}}{a_C}
\le M^2a_C
\]
gives (7). \(\square\)

This is essentially the largest possible second-order rotation statistic.
Nevertheless it does not move Xi: it says the same fibres support many
**differences** \(2\alpha\), not that the source angles themselves occur
on a common radius class, nor that their phases align across heights.

## 4. A statistic that also spends the global distance bound

For \(\alpha\in\mathcal A\), let \(P_\alpha\) be the \(q_\alpha\) off-axis
source points in the axial plane \(\Pi_\alpha\).  Distinct active planes
modulo \(\pi\) have disjoint off-axis source sets.

For an ordered plane pair \(\boldsymbol\alpha=(\alpha,\beta)\), define
\[
R_{\alpha,\beta}(d)
=|\{(x,y)\in P_\alpha\times P_\beta:
|x-y|^2=d\}|.
\tag{9}
\]
Discard the \(O(M)\) ordered pairs for which the two planes are equal or
perpendicular.  Call the remaining set \(\mathcal G\).  Then
\[
|\mathcal G|=M^2-O(M).
\tag{10}
\]

Define the aggregate energy
\[
\mathfrak E_{\rm all}
=\sum_d
\left(\sum_{(\alpha,\beta)\in\mathcal G}
R_{\alpha,\beta}(d)\right)^2,
\tag{11}
\]
the individual-pair diagonal energy
\[
\mathfrak E_{\rm diag}
=\sum_{(\alpha,\beta)\in\mathcal G}\sum_d
R_{\alpha,\beta}(d)^2,
\tag{12}
\]
and the cross-plane-pair codegree
\[
\mathfrak C_{\rm plane}
=\mathfrak E_{\rm all}-\mathfrak E_{\rm diag}.
\tag{13}
\]
Thus \(\mathfrak C_{\rm plane}\) counts pairs of representations of one
distance whose ordered axial-plane pairs are different.

### Lemma 2 (one distance on two nonexceptional planes)

For fixed nonexceptional \((\alpha,\beta)\) and fixed \(d\),
\[
\boxed{
R_{\alpha,\beta}(d)
\ll Q^{4/3}+Q.
}
\tag{14}
\]

### Proof

For each \(x\in P_\alpha\), intersect the sphere
\[
|x-y|^2=d
\]
with \(\Pi_\beta\).  The result is a circle, a point, or the empty set in
\(\Pi_\beta\).  To check the degeneracies, rotate coordinates so that
\(\Pi_\beta\) has signed radial--height coordinates \((v,w)\), write a
source point in \(\Pi_\alpha\) as \((u,z)\), and put
\(c=\cos(\alpha-\beta)\).  The target-circle equation is
\[
v^2+w^2-2cu\,v-2z\,w+u^2+z^2-d=0.                 \tag{14a}
\]
For a retained pair \(c\ne0\).  Equality of two normalized equations
in (14a) forces \(u=u'\) and \(z=z'\), so there are no repeated
circles.  If two distinct target points \((v_i,w_i)\), \(i=1,2\),
lie on a source-indexed circle, subtracting their two equations gives
the affine line
\[
-2c(v_1-v_2)u-2(w_1-w_2)z
+v_1^2+w_1^2-v_2^2-w_2^2=0.                       \tag{14b}
\]
For \(c\ne0\), this is never the zero polynomial for two distinct
targets.  Its intersection with the source circle has at most two
points.  Hence these circles form a two-degree-of-freedom
pseudocircle family:

* two distinct circles meet in at most two points;
* two off-axis points of \(\Pi_\beta\) lie on at most two of the circles.

Equal planes are not degenerate, although deleting their \(M\) ordered
pairs is harmless.  The genuine positive-dimensional exception occurs
for perpendicular planes (\(c=0\)) and two target points that are
same-height antipodes; their two source equations then coincide.
Those plane pairs were also removed.  The standard crossing-lemma
incidence bound for two-degree-of-freedom pseudocircles gives
\[
I(P_\beta,\{\Gamma_x:x\in P_\alpha\})
\ll Q^{2/3}Q^{2/3}+Q+Q.
\]
This incidence count is exactly (14). \(\square\)

### Theorem 3 (forced cross-plane-pair distance codegree)

At the inherited critical node,
\[
\boxed{
\mathfrak C_{\rm plane}
\ge N^{13/5-o(1)}.
}
\tag{15}
\]

### Proof

The number of ordered point pairs represented in (11) is
\[
\sum_{(\alpha,\beta)\in\mathcal G}\sum_dR_{\alpha,\beta}(d)
=(1-o(1))M^2Q^2.
\]
All labels belong to the global squared-distance set, of size at most
\(D+1\).  Cauchy--Schwarz gives
\[
\mathfrak E_{\rm all}
\gg\frac{M^4Q^4}{D}.
\tag{16}
\]

For one plane pair, (14) and
\(\sum_dR_{\alpha,\beta}(d)=Q^2\) imply
\[
\sum_dR_{\alpha,\beta}(d)^2
\le\max_dR_{\alpha,\beta}(d)\sum_dR_{\alpha,\beta}(d)
\ll Q^{10/3}+Q^3.
\]
Therefore
\[
\mathfrak E_{\rm diag}
\ll M^2Q^{10/3}.
\tag{17}
\]
At
\[
M=N^{1/5-o(1)},\quad Q=N^{3/5-o(1)},\quad
D=N^{3/5+o(1)},
\]
the exponents in (16)--(17) are
\[
\frac{M^4Q^4}{D}=N^{13/5-o(1)},\qquad
M^2Q^{10/3}=N^{12/5+o(1)}.
\tag{18}
\]
The diagonal term is smaller by \(N^{1/5-o(1)}\).  Subtracting it in
(13) proves (15). \(\square\)

This is a genuinely global statement.  Proposition 1 survives even when
source and rotation fibres are disjoint; Theorem 3 additionally forces
distance-label reuse across different source-plane pairs.

## 5. The useful radius–angle statistic

For a radius \(\rho\), put
\[
q_{\rho,\alpha}
=|\{p\in P_\alpha:\operatorname{rad}(p)=\rho\}|,
\qquad
I_\rho=\sum_{\alpha\in\mathcal A}q_{\rho,\alpha}.
\tag{19}
\]
Define
\[
\mathfrak E_{\rho\angle}
=\sum_\rho I_\rho^2
\tag{20}
\]
and its genuine cross-angle part
\[
\mathfrak C_{\rho\angle}
=\sum_\rho\sum_{\alpha\ne\beta}
q_{\rho,\alpha}q_{\rho,\beta}.
\tag{21}
\]
The total source mass is
\[
\sum_\rho I_\rho=\sum_\alpha q_\alpha=MQ=N^{4/5-o(1)}.
\tag{22}
\]
Consequently
\[
\max_\rho I_\rho
\ge\frac{\mathfrak E_{\rho\angle}}{MQ}.
\tag{23}
\]

### Proposition 4 (conditional escape from angular starvation)

Suppose, for some fixed \(\delta>0\), that
\[
\boxed{
\mathfrak E_{\rho\angle}
\ge N^{7/5+\delta-o(1)}
}
\tag{24}
\]
or merely
\[
\mathfrak C_{\rho\angle}
\ge N^{7/5+\delta-o(1)},
\tag{25}
\]
respectively.  In the second case first use
\(\mathfrak E_{\rho\angle}\ge\mathfrak C_{\rho\angle}\).
Choose a radius \(\rho_*\) satisfying
\[
I_{\rho_*}
\ge\frac{\mathfrak E_{\rho\angle}}{MQ}.            \tag{25a}
\]
Assume further that there is an occupied anchor height \(z_0\) on
this same radius such that, after deleting the anchor circle, the set
\[
A_{\rho_*,z_0}
=\{(z-z_0)^2:
\text{an undeleted source point of radius }\rho_*
\text{ occurs at height }z\}
\]
has
\[
\lambda(\rho_*,z_0)
:=\max_{t\ne0}
|A_{\rho_*,z_0}\cap(A_{\rho_*,z_0}+t)|
\le N^{o(1)}.                                      \tag{25b}
\]
Then
\[
\boxed{
\Xi\ge N^{3/5+\delta-o(1)}.
}
\tag{26}
\]

### Proof

Equations (22), (24), and (25a) give
\[
I_{\rho_*}\ge N^{3/5+\delta-o(1)}.
\]
There are at most \(2M=N^{1/5+o(1)}\) actual source angular columns.
Delete one anchor circle, losing at most \(O(M)\) incidences.  Apply the
sparse Xi theorem on the remaining height–angle graph:
\[
\Xi\ge
\frac{I_{\rho_*}^2}
{2I_{\rho_*}+\lambda(\rho_*,z_0)(2M)^2}.
\]
Its two exponents are
\[
\frac35+\delta,\qquad
\frac45+2\delta-o(1).
\]
The first is smaller, proving (26). \(\square\)

The threshold \(N^{7/5}\) is exact.  At equality, (23) gives only
\(I_\rho=N^{3/5}\), reproducing the starvation branch.

## 6. The minimum missing transfer lemma

Theorem 3 forces
\[
\mathfrak C_{\rm plane}\ge N^{13/5-o(1)},
\]
whereas Proposition 4 needs
\[
\mathfrak E_{\rho\angle}\ge N^{7/5+\delta-o(1)}.
\]
Therefore the following transfer, for any fixed \(\eta>0\), would close
the branch:
\[
\boxed{
\mathfrak C_{\rm plane}
\ll
N^{6/5-\eta+o(1)}
\mathfrak E_{\rho\angle}.
}
\tag{27}
\]
Indeed, (15) and (27) imply
\[
\mathfrak E_{\rho\angle}
\ge N^{7/5+\eta-o(1)},
\]
and Proposition 4 gives
\[
\Xi\ge N^{3/5+\eta-o(1)}.
\]

Equation (27) is not currently proved.  It is an inverse theorem for
equal-distance coincidences across four axial planes: unless many source
angles reuse common radii, the cross-plane-pair distance codegree must lose
a fixed power relative to its trivial \(N^{6/5}\)-times-radius-energy
capacity.

An equivalent, more geometric formulation is:

> **Minimum missing lemma.**  An off-axis set consisting of
> \(Q=N^{3/5-o(1)}\) points on each of
> \(M=N^{1/5-o(1)}\) planes through one axis, and determining
> \(D=N^{3/5+o(1)}\) distances, must have
> \[
> \sum_\rho\left(\sum_\alpha q_{\rho,\alpha}\right)^2
> \ge N^{7/5+\eta-o(1)}
> \]
> for some absolute \(\eta>0\), unless the height-overlap branch has
> \(\lambda=N^{\Omega(1)}\).

This statement is strictly weaker than extracting a complete common
angular rectangle and exactly strong enough for Xi.

## 7. Euclidean sharp barrier for all old angular marginals

The following construction shows that neither Proposition 1 nor any old
\(q_\alpha,r_\alpha\) marginal can imply (24).

Fix \(t\ge3\) and set
\[
N=t^5,\quad D_0=Q=t^3,\quad M=t,\quad S=t^2.
\tag{28}
\]
Choose \(\theta/\pi\) irrational with \(0<M\theta<\pi/4\), and put
\(\alpha_j=j\theta\), \(1\le j\le M\).

### Rotation reservoir

Take
\[
F_0=t^2(t-1)
\]
coaxial circular fibres, each with \(S\) angular points in a generic
translate of
\[
\{K\theta,(K+1)\theta,\ldots,(K+S-1)\theta\},
\qquad K>2M.
\]
Choose the generic phases so that no source angle occurs.  Then
\[
w_{C,\alpha_j}=S-2j.
\tag{29}
\]

### Euclidean source columns

For each \(j\) and \(0\le h<Q\), take the actual point
\[
\boxed{
p_{j,h}=(1,\tan(j\theta),h).
}
\tag{30}
\]
It lies in the axial plane of angle \(j\theta\), on the coaxial circle
of radius
\[
\rho_j=\sec(j\theta)
\]
and height \(h\).  The radii \(\rho_j\) are distinct.  Put no other point
on these \(MQ=t^4\) source fibres.

The reservoir contains
\[
F_0S=t^5-t^4
\]
points, so the total is exactly \(N\).  For every active angle,
\[
q_{\alpha_j}=Q,\qquad
r_{\alpha_j}=F_0(S-2j)=N(1-o(1)).
\tag{31}
\]
The source and rotation fibre sets are disjoint, and hence every
same-fibre source–rotation coupling is zero.

The construction has
\[
\mathfrak C_{\rm rot}
=\frac{F_0}{S}
\left(\sum_{j=1}^M(S-2j)\right)^2
=N^{7/5+o(1)},
\tag{32}
\]
so it saturates the strongest forced rotation statistic.

Every source angle occupies one private radius with \(Q\) heights.  Thus
\[
\mathfrak E_{\rho\angle}=MQ^2=t^7=N^{7/5},
\qquad
\mathfrak C_{\rho\angle}=0.
\tag{33}
\]
On each source radius, there is only one angular column.  With the lowest
point as anchor, the squared-height set is
\[
\{1^2,\ldots,(Q-1)^2\}
\]
and has \(\lambda=Q^{o(1)}\).  Consequently
\[
\Xi=N^{3/5-o(1)}
\tag{34}
\]
at equality.

The construction is also sharp for every **individual** source-plane
pair.  From (30),
\[
|p_{j,h}-p_{k,\ell}|^2
=(\tan(j\theta)-\tan(k\theta))^2+(h-\ell)^2.
\tag{35}
\]
For fixed \(j,k\), there are exactly \(Q\) squared-distance labels and
their ordered representation energy is
\[
\boxed{
Q^2+4\sum_{r=1}^{Q-1}r^2=\Theta(Q^3),
}
\tag{36}
\]
the Cauchy--Schwarz scale \(Q^4/D_0\).

For a generic admissible \(\theta\), however, the translated square blocks
in (35) for different unordered \(j,k\) are disjoint.  The source part then
has
\[
\Theta(M^2Q)=\Theta(N)
\]
distances.  Its aggregate energy is only of order \(M^2Q^3=N^{11/5}\),
far below the forced \(N^{13/5}\) in Theorem 3.

Thus this is a literal Euclidean realization satisfying all old angular
marginals and their strongest rotation second moment.  It is not a
few-distance counterexample.  The global distance hypothesis rules it out
precisely through the cross-plane-pair reuse statistic (15).

## 8. Exponent ledger

| Statistic | Forced or barrier exponent |
|---|---:|
| active planes \(M\) | \(1/5\) |
| points per source plane \(Q\) | \(3/5\) |
| source mass \(MQ\) | \(4/5\) |
| normalized rotation codegree \(\mathfrak C_{\rm rot}\) | \(7/5\) |
| useful radius–angle threshold | \(7/5+\delta\) |
| barrier radius–angle energy | \(7/5\) |
| total cross-plane distance energy | \(13/5\) |
| individual-plane-pair diagonal upper bound | \(12/5\) |
| Euclidean barrier individual-pair energy sum | \(11/5\) |
| starvation Xi | \(3/5\) |

The forced rotation codegree is already maximal at exponent level and does
not help.  The new \(13/5\) cross-plane codegree is the first inherited
statistic that the sharp angular-marginal barrier cannot imitate.

## 9. Claim boundary

### Unconditional results

* Proposition 1: the inherited rotation marginals force
  \(\mathfrak C_{\rm rot}\ge N^{7/5-o(1)}\).
* Lemma 2 and Theorem 3: the global distance bound forces
  \(\mathfrak C_{\rm plane}\ge N^{13/5-o(1)}\).
* The Euclidean construction realizes every old angular marginal, maximal
  rotation codegree, radius–angle energy \(N^{7/5}\), and Xi at the
  \(N^{3/5}\) threshold.

### Conditional result

* Any fixed-power transfer (27), or directly (24), gives the corresponding
  fixed-power Xi improvement.

### Open

* No proof of (27) is known.
* Therefore no unconditional improvement of \(f_3(N)\) is claimed.
