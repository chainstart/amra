# Two incidence-active circle--axis charts: exact cross formulas and barrier

Date: 2026-07-30

## 0. Result

Two incidence-active repeated-circle charts do **not** by themselves
force superlinear distance expansion.  This remains false even when
their source circles have different radii.

The obstruction is an exact two-radius Lenz model: two concentric
regular polygons in one vertical plane, together with a common
arithmetic progression on their perpendicular axis.  Each circle is
a distinct repeated-circle chart with arbitrarily many source
incidences and arbitrarily large target multiplicity, while the union
has only linearly many distances.

Thus “two charts” or “two different radius families” is not a
sufficient next hypothesis.  The known Mathialagan--Sheffer
two-circle classification identifies aligned and perpendicular circle
pairs as the two exceptional geometries.  In the present axial-chart
family the perpendicular case is impossible for genuine retained
reverse circles, while aligned means a common centre and common
perpendicular axis.  The remaining campaign gap is therefore to
extract two nonaligned charts with sufficiently large source
incidence sets, not to prove a new two-circle collision theorem.

## 1. Exact distances between two general charts

For chart \(i=1,2\), let
\[
 e_i=(\cos\alpha_i,\sin\alpha_i,0),\qquad
 f_i=(-\sin\alpha_i,\cos\alpha_i,0),
\]
\[
 c_i=A_i e_i+w_i e_z,
\]
and parameterize its source circle and target axis by
\[
 p_i(\phi)
 =c_i+r_i(\cos\phi\,e_i+\sin\phi\,e_z),
\qquad
 q_i(y)=c_i+yf_i.
\tag{1}
\]
Put
\[
 \theta=\alpha_2-\alpha_1,\quad
 c=\cos\theta,\quad s=\sin\theta,\quad
 \Delta w=w_1-w_2,
\]
\[
 B=|c_1-c_2|^2
 =A_1^2+A_2^2-2cA_1A_2+\Delta w^2.
\tag{2}
\]
Direct expansion gives the four cross blocks:
\[
\boxed{
\begin{aligned}
|q_1(y)-q_2(z)|^2
={}&B+y^2+z^2-2cyz-2A_2sy+2A_1sz,
\end{aligned}}
\tag{3}
\]
\[
\boxed{
\begin{aligned}
|p_1(\phi)-q_2(z)|^2
={}&B+r_1^2+z^2\\
&+2r_1\{(A_1-A_2c)\cos\phi+\Delta w\sin\phi\}\\
&+2A_1sz+2r_1sz\cos\phi,
\end{aligned}}
\tag{4}
\]
\[
\boxed{
\begin{aligned}
|q_1(y)-p_2(\psi)|^2
={}&B+y^2+r_2^2-2A_2sy\\
&-2r_2\{(A_1c-A_2)\cos\psi+\Delta w\sin\psi\}\\
&-2r_2sy\cos\psi,
\end{aligned}}
\tag{5}
\]
and
\[
\boxed{
\begin{aligned}
|p_1(\phi)-p_2(\psi)|^2
={}&B+r_1^2+r_2^2\\
&+2r_1\{(A_1-A_2c)\cos\phi+\Delta w\sin\phi\}\\
&-2r_2\{(A_1c-A_2)\cos\psi+\Delta w\sin\psi\}\\
&-2r_1r_2\{c\cos\phi\cos\psi+\sin\phi\sin\psi\}.
\end{aligned}}
\tag{6}
\]
The mixed terms disappear completely for concentric, co-oriented
charts.  Outside the exact circle-pair exceptions their collision
behavior is already controlled by Mathialagan--Sheffer,
[*Distinct distances on non-ruled surfaces and between circles*,
arXiv:2011.08098v2](https://arxiv.org/abs/2011.08098), Theorem 1.4.
Section 3 translates that known classification into the parameters
above.

## 2. Exact two-chart saturation

Fix \(a>r_2>r_1>0\), an integer \(n\ge3\), and
\[
 J_m=\{\pm1,\pm3,\ldots,\pm(2m-1)\}.
\]
In the \(xz\)-plane take the two aligned regular polygons
\[
 S_i=
 \left\{
 \left(
 a+r_i\cos\frac{2\pi k}{n},\
 0,\
 r_i\sin\frac{2\pi k}{n}
 \right):0\le k<n
 \right\},
\qquad i=1,2,
\tag{7}
\]
and on their common perpendicular axis take
\[
 T=\{(a,hj,0):j\in J_m\}.
\tag{8}
\]

For every \(q_j=(a,hj,0)\), its axial plane is nonperpendicular to
the \(xz\)-plane and its signed radial data obey
\[
 c_jv_j=a,\qquad v_j^2=a^2+h^2j^2.
\]
For circle \(S_i\), assign the label
\[
 d_{i,j}=r_i^2+h^2j^2.
\tag{9}
\]
Then all \(2m\) triples for fixed \(i\) produce the normalized circle
\[
 (u-a)^2+z^2=r_i^2.
\tag{10}
\]
Hence there are two distinct incidence-active charts, each of
multiplicity \(2m\), each incident to all \(n\) points of its source
polygon.

The full distance ledger is nevertheless linear:

* within or between \(S_1,S_2\),
  \[
  |p_i(k)-p_j(\ell)|^2
  =
  r_i^2+r_j^2
  -2r_ir_j\cos\frac{2\pi(k-\ell)}n,
  \tag{11}
  \]
  so the three unordered radius pairs contribute at most
  \(3\lfloor n/2\rfloor+1\) labels;
* \(T-T\) contributes exactly \(2m-1\) labels;
* \(S_i-T\) contributes the \(m\) labels
  \(r_i^2+h^2j^2\), for each \(i\).

Therefore
\[
\boxed{
 |\Delta^2(S_1\cup S_2\cup T)|
 \le 3\lfloor n/2\rfloor+4m
 =O(n+m).
}
\tag{12}
\]
There are \(2n+2m\) points and \(4mn\) cross representations across
the two repeated circles.  Thus (12) is a genuine linear-distance
double-chart obstruction, not a low-incidence example.

The same construction works for every fixed number \(K\) of
concentric radii, with
\[
 |\Delta^2|
 =O(K^2n+Km+m).
\tag{13}
\]

## 3. Known classification and the actual unresolved extraction

Let \(H_i=\operatorname{span}(e_i,e_z)\) be the plane of the source
circle and
\[
 L_i=c_i+\mathbb R f_i
\]
its axis.  Mathialagan--Sheffer call the circles **aligned** when
\(L_1=L_2\).  In the parameters of Section 1 this is exactly
\[
\boxed{
 s=0,\qquad \Delta w=0,\qquad A_1-A_2c=0.
}
\tag{14}
\]
Indeed, equality of the line directions gives \(s=0\); then both
centres lie in the same plane perpendicular to \(f_1\), so equality
of the axis lines forces equality of the centres.

Their second exception consists of **perpendicular** circles: the
planes \(H_1,H_2\) are perpendicular and each circle centre lies in
the other plane.  Here this is exactly
\[
\boxed{
 c=0,\qquad A_1=A_2=0.
}
\tag{15}
\]
But every retained incidence-active reverse circle has
\[
 A_i=\cos(\alpha_i-\beta)v\ne0,
\]
because its target is off the common axis and the perpendicular
source--target plane was deleted.  Thus (15) cannot occur in the
campaign's chart family.

Let \(C_i\) be the source circle parameterized by \(p_i(\phi)\) in
(1), and let \(P_i\subset C_i\) be arbitrary source incidence sets of
sizes \(s_i\).  If (14) fails, Mathialagan--Sheffer Theorem 1.4(b)
therefore applies and gives the known bound
\[
\boxed{
 |\Delta^2(P_1,P_2)|
 =
 \Omega\!\left(
 \min\{s_1^{2/3}s_2^{2/3},s_1^2,s_2^2\}
 \right).
}
\tag{16}
\]
The source theorem is stated for distances rather than squared
distances, which does not change the cardinality.

At the critical budget \(|\mathcal D|\le t^{3+o(1)}\), writing
\(s_i=t^{a_i+o(1)}\), equation (16) forces
\[
 \min\left\{\frac23(a_1+a_2),2a_1,2a_2\right\}\le3.
\tag{17}
\]
For example, two nonaligned active circles each incident to
\(t^{9/4+\eta}\) source points would already contradict the critical
distance budget.

The present hub theorem does not force two such circles: its
multiplicity \(\mu\) may be concentrated on one aligned active circle,
and it gives no matching lower bounds for two source incidence sets.
The valid next lemma must therefore extract two nonaligned
incidence-rich circles, aggregate (16) over many nonaligned classes,
or prove that all large-incidence classes concentrate in one aligned
family and then attack that concentration.  A fuller source-aware
translation is recorded in
`MATHIALAGAN_SHEFFER_CIRCLE_CLASSIFICATION_BRIDGE.md`.

## 4. Verification

`verify_two_circle_axis_chart_barrier.py` constructs the regular
polygon/AP model in exact SymPy arithmetic, verifies both repeated
circle equations, checks multiplicity \(2m\) and \(m\) cross labels
per chart, and enumerates the full distance set.

```bash
python3 verify_two_circle_axis_chart_barrier.py
pytest -q test_verify_two_circle_axis_chart_barrier.py
```

The source-aware aligned/perpendicular parameter translation and the
critical \(9/4\) incidence threshold are checked separately by
`verify_mathialagan_sheffer_chart_bridge.py` and
`test_verify_mathialagan_sheffer_chart_bridge.py`.
