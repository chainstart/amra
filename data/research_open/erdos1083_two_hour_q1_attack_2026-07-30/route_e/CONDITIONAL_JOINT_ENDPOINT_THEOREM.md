# Erdős #1083 Route E: joint ST/service sensitivity at \(2/9\)

Date: 2026-07-30

## 0. Outcome

This note audits the live \(2/9\) endpoint of the fixed-centre
linearization argument.  It does not prove an unconditional endpoint
power saving.

There is, however, a natural single inequality which measures exactly
the missing gain.  In a mass-carrying secondary dyadic layer, use the
notation
\[
\begin{aligned}
M&=t^{1+o(1)},&
Q&=t^{3+o(1)},&
L&=t^{2-2\kappa+o(1)},\\
u&=t^{m+o(1)},&
N&=t^{b+o(1)},&
R&=t^{r+o(1)}.
\end{aligned}
\tag{1}
\]
Here \(u\) is the circle repetition scale, \(N\) is the number of
retained circles, and \(R\) is the number of represented signed centre
coordinates \(A\).

The usual rich-line Szemerédi--Trotter estimate and target-service
capacity imply, without a power saving,
\[
RNu^4\le t^{o(1)}MQ(ML)^2.
\tag{2}
\]
The concrete missing input is the following joint strengthening:
\[
\boxed{
RNu^4
\le
t^{-\delta+o(1)}MQ(ML)^2.
}
\tag{\(\mathrm J_\delta\)}
\]

### Conditional theorem

Fix
\[
0<\delta<\frac{16}{5}.
\tag{3}
\]
Assume that every putative Euclidean hub in the inherited setup has a
mass-carrying secondary dyadic layer satisfying
\((\mathrm J_\delta)\).  Then the hub is impossible for every fixed
\[
\boxed{
\kappa<\frac{4+\delta}{18}
=\frac29+\frac{\delta}{18}.
}
\tag{4}
\]
Consequently, the inherited matching-or-hub theorem gives, for every
fixed \(\varepsilon>0\), at least \(t^{1-o(1)}\) labels supporting
plane-pair matchings of size
\[
\boxed{
t^{\,2/9+\delta/18-\varepsilon-o(1)}.
}
\tag{5}
\]

Thus a saving of \(t^{-\delta}\) in the explicitly normalized joint
inequality \((\mathrm J_\delta)\) improves the matching exponent by
exactly
\[
\boxed{\delta/18.}
\tag{6}
\]
The coefficient \(1/18\) is not heuristic; every branch and every
factor of three is audited below.

## 1. Why (2) is exactly the joint ST/service boundary

After the secondary dyadic decomposition, let

- \(K\) be the number of represented signed parameter-line copies
  \((A,\rho^2)\);
- \(H\) be the common dyadic number of circles over such a copy.

Then
\[
N=t^{o(1)}KH.
\tag{7}
\]
Every represented geometric tangent--label line is \(u/2\)-rich in a
point set of size at most \(ML\).  Signed copies cost only a constant
factor, so the rich-line consequence of Szemerédi--Trotter gives
\[
K
\ll
\frac{(ML)^2}{u^3}+\frac{ML}{u}.
\tag{8}
\]

Choose one represented signed parameter line for each represented
\(A\).  Its \(H\) different centre heights and \(u\) producing triples
use \(Hu\) different target points.  The \(R\) ordinary planes \(x=A\)
are disjoint, and the retained target union has at most \(MQ\) points.
Therefore
\[
RHu\le t^{o(1)}MQ.
\tag{9}
\]
Multiplying (7)--(9) gives the finite-scale baseline
\[
RNu^4
\ll
MQ\bigl((ML)^2+ML\,u^2\bigr)t^{o(1)}.
\tag{10}
\]

In the range \(\kappa<2/5\), the trivial bound \(u\le M\) gives
\[
\frac{ML}{u^2}
\ge
t^{1-2\kappa-o(1)}.
\tag{11}
\]
Hence the first term in (10) is power-dominant, proving (2).

At the \(2/9\) endpoint,
\[
(r,b,m)
=
\left(\frac{19}{18},\frac{85}{18},\frac56\right),
\qquad
ML=t^{23/9+o(1)}.
\tag{12}
\]
Both sides of (2) have exponent
\[
r+b+4m
=
\frac{82}{9}
=
4+2\cdot\frac{23}{9}.
\tag{13}
\]
Thus \((\mathrm J_\delta)\) targets the exact simultaneously saturated
ST/service constraint rather than inserting a saving into an inactive
term.

## 2. Target service alone cannot supply a saving

The target-service inequality itself has an exact Euclidean parameter
model.

### Proposition 1 (exact interval service saturation)

Let \(B,H,U\) be positive integers.  Fix \(A=1\), and put
\[
\begin{aligned}
\mathcal B&=\{1,\ldots,B\},\\
\mathcal W&=\{1,\ldots,H\},\\
\mathcal T&=\{1,\ldots,U\},\\
\mathcal D&=\mathcal B+\mathcal T
            =\{2,\ldots,B+U\}.
\end{aligned}
\tag{14}
\]
For every \((b,w)\in\mathcal B\times\mathcal W\), take the
positive-radius reverse circle with centre \((1,w)\) and squared radius
\(b\).  For every \((w,\tau)\in\mathcal W\times\mathcal T\), take the
target point
\[
q_{w,\tau}=(1,\sqrt{\tau},w).
\tag{15}
\]
For each \(b\), give this target point the selected squared label
\[
d=b+\tau\in\mathcal D.
\tag{16}
\]
The tangent--label identity
\[
d=b+A^2\tau
\tag{17}
\]
shows that \(q_{w,\tau}\) with label \(d\) produces exactly the circle
\((b,w)\).

Consequently:

- every one of the \(BH\) circles has exactly \(U\) producers;
- the target union has exactly \(HU\) points;
- every target point services all \(B\) represented radii;
- \(|\mathcal D|=B+U-1\ge B\); and
- the fixed-\(A\) service cap is an equality:
  \[
  \sum_C\mu(C)
  =BHU
  =\min\{|\mathcal D|,B\}\,HU.
  \tag{18}
  \]

All radii are positive, all target points are off the common axis, and
the target axial planes are nonperpendicular.  The construction does
not assert source-incidence saturation; it proves the narrower and
necessary point that target service, even with perfectly reused height
and tangent sets, has no standalone power saving.

This is also why the elementary sumset lower bound
\[
|\mathcal B+\mathcal T|\ge B+U-1
\tag{19}
\]
does not help at exponent scale when \(U\ll B\): intervals attain
equality and \(B+U-1=B\,t^{o(1)}\).

## 3. Inherited scalar inequalities

Write the source richness as \(s=t^{a+o(1)}\).  The layer mass and total
triple capacity give
\[
\begin{aligned}
a+b+m&\ge7-3\kappa-o(1),\\
b+m&\le6-2\kappa+o(1).
\end{aligned}
\tag{20}
\]
In particular,
\[
\boxed{a\ge1-\kappa-o(1).}
\tag{21}
\]

For \(\kappa<2/5\), the \(Q^{2/3}N^{2/3}\) term in the inherited
weighted point--circle bound could carry the mass only if
\[
m\ge3-5\kappa-o(1)>1,
\tag{22}
\]
contrary to \(u\le M=t^{1+o(1)}\).  The \(+Q\) and \(+N\) terms miss
respectively by the bounds \(m\le1+o(1)\) and (20).  Hence the
\(Q^{6/11}N^{9/11}\) term carries, giving
\[
\boxed{11a+2b\le18+o(1).}
\tag{23}
\]
Combining (20), (21), and (23) gives
\[
\boxed{
a\le\frac{4+6\kappa+2m}{9}+o(1),
\qquad
m\ge\frac{5-15\kappa}{2}-o(1).
}
\tag{24}
\]

The restriction (3) guarantees that the proposed threshold in (4) is
strictly below \(2/5\), so every use of (22)--(24) is within its audited
range.

## 4. Exponent form of the conditional input

Taking exponents in \((\mathrm J_\delta)\) gives
\[
\boxed{
r+b+4m
\le
10-4\kappa-\delta+o(1).
}
\tag{25}
\]
Indeed, \(MQ\) has exponent \(4\), while
\[
2\log_t(ML)=2(3-2\kappa)=6-4\kappa.
\]
The coefficient of \(\delta\) in (25) is exactly one.

The fixed-\(A\) parabolic lift gives
\[
I(P_\alpha,\mathcal C)
\ll
Q^{2/3}R^{1/3}N^{2/3}+RQ+N.
\tag{26}
\]
Since the source incidence of the layer is \(t^{a+b+o(1)}\), one of
the three terms in (26) must carry.

## 5. Audit of all fixed-\(A\) ST branches

### 5.1 The \(+N\) branch

If \(+N\) carried, then \(a+b\le b+o(1)\), contrary to (21).  This
branch is impossible.

### 5.2 The \(+RQ\) branch

If \(+RQ\) carried, then
\[
a+b\le3+r+o(1).
\tag{27}
\]
Using (25) to eliminate \(r\), followed by the mass inequality in
(20), gives
\[
\boxed{
a\ge1+2m-2\kappa+\delta-o(1).
}
\tag{28}
\]
Combining (28) with the upper bound for \(a\) in (24) yields
\[
\boxed{
m\le\frac{24\kappa-5-9\delta}{16}+o(1).
}
\tag{29}
\]
This and the lower bound for \(m\) in (24) can coexist only when
\[
\boxed{
\kappa\ge\frac{5+\delta}{16}-o(1).
}
\tag{30}
\]
The error-branch threshold lies strictly above the claimed main
threshold, since
\[
\frac{5+\delta}{16}
-
\frac{4+\delta}{18}
=
\boxed{\frac{13+\delta}{144}>0.}
\tag{31}
\]
Therefore the \(+RQ\) branch cannot carry anywhere in the range (4).

### 5.3 The main term

The main term of (26) must carry:
\[
3a+b\le6+r+o(1).
\tag{32}
\]
Adding \(b+4m\) and using (25) gives
\[
3a+2b+4m
\le
16-4\kappa-\delta+o(1).
\tag{33}
\]
Twice the mass inequality in (20) says
\[
2a+2b+2m
\ge
14-6\kappa-o(1).
\tag{34}
\]
Subtracting (34) from (33) gives
\[
\boxed{
a+2m\le2+2\kappa-\delta+o(1).
}
\tag{35}
\]
Using (21),
\[
\boxed{
m\le\frac{1+3\kappa-\delta}{2}+o(1).
}
\tag{36}
\]
Finally, compare (36) with the point--circle lower bound in (24):
\[
\frac{5-15\kappa}{2}
\le
\frac{1+3\kappa-\delta}{2}+o(1).
\tag{37}
\]
A surviving hub would therefore require
\[
18\kappa\ge4+\delta-o(1),
\tag{38}
\]
which is precisely
\[
\kappa\ge\frac{4+\delta}{18}-o(1).
\]
Every fixed \(\kappa\) below this value leaves a fixed exponent gap.
This proves the conditional theorem.

## 6. Coefficient ledger

The propagation of one unit of saving is:
\[
\begin{array}{c|c}
\text{stage}&\text{saved exponent}\\ \hline
(\mathrm J_\delta)&\delta\\
r+b+4m\text{ upper bound}&\delta\\
a+2m\text{ upper bound}&\delta\\
m\text{ upper bound}&\delta/2\\
\text{gap between the two }m\text{ bounds}&\delta/2\\
\kappa\text{ threshold}&\delta/18
\end{array}
\tag{39}
\]
The last denominator \(18\) comes from the difference between the
\(-15\kappa\) and \(+3\kappa\) coefficients in the two \(m\)-bounds.

For comparison only, a saving \(t^{-\sigma}\) directly in the main
term of (26) would become \(3\sigma\) after clearing the one-third
exponents, and would locally move the main threshold by
\(\sigma/6\).  That is a different hypothesis from
\((\mathrm J_\delta)\), and its error-branch range would need a
separate audit.  No such fixed-\(A\) incidence saving is asserted here.

## 7. Claim boundary

### Proved unconditionally in this note

- the finite joint baseline (10) from the already established
  rich-line and target-capacity inequalities;
- exact saturation of the \(2/9\) exponent ledger in (13);
- the exact interval target-service model in Proposition 1;
- the fact that target service alone cannot yield a uniform power
  saving;
- every coefficient and every error branch in the implication
  \[
  (\mathrm J_\delta)
  \Longrightarrow
  \kappa_{\rm match}
  \ge
  \frac29+\frac{\delta}{18}-\varepsilon.
  \]

### Not proved

- \((\mathrm J_\delta)\) for any fixed \(\delta>0\);
- an unconditional exclusion of the \(2/9\) endpoint;
- incompatibility of simultaneous near-equality in the special
  fixed-\(A\) incidence problem and the interval-like service model;
- a Euclidean realization of the complete endpoint ledger;
- any improvement of the global \(3/5\) distinct-distance exponent.

The remaining mathematical target is therefore precise: prove
\((\mathrm J_\delta)\), or an inequality with the same exponent
consequence, using compatibility between the fixed-\(A\) lifted
source incidences and the heavily reused target height--tangent grids.

## 8. Reproduction

```bash
cd data/research_open/erdos1083_two_hour_q1_attack_2026-07-30/route_e
python3 verify_joint_endpoint_saving.py
pytest -q test_verify_joint_endpoint_saving.py
```
