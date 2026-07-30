# Mathialagan--Sheffer two-circle classification in axial-chart coordinates

Date: 2026-07-30

## 0. Status and source

This note is a source-aware reduction to a known theorem, not a new
distinct-distance theorem.

The source is Mathialagan--Sheffer,
[*Distinct distances on non-ruled surfaces and between circles*,
arXiv:2011.08098v2](https://arxiv.org/abs/2011.08098), Theorem 1.4
on pp. 2--3.  For finite sets \(P_i\subset C_i\) of sizes \(s_i\),
their theorem states:

- aligned or perpendicular circle pairs admit examples with only
  \(\Theta(s_1+s_2)\) bipartite distances;
- every circle pair that is neither aligned nor perpendicular obeys
  \[
  D(P_1,P_2)
  =
  \Omega\!\left(
  \min\{s_1^{2/3}s_2^{2/3},s_1^2,s_2^2\}
  \right).
  \tag{MS}
  \]

Cardinalities of distance sets and squared-distance sets are equal,
so (MS) applies without changing the campaign's squared-distance
notation.

## 1. Axial-chart geometry

Use the notation of `TWO_CIRCLE_AXIS_CHART_BARRIER.md`:
\[
\begin{aligned}
e_i&=(\cos\alpha_i,\sin\alpha_i,0),\\
f_i&=(-\sin\alpha_i,\cos\alpha_i,0),\\
c_i&=A_i e_i+w_i e_z,\\
C_i&=\{c_i+r_i(\cos\phi\,e_i+\sin\phi\,e_z)\}.
\end{aligned}
\]
The containing plane and circle axis are
\[
H_i=\operatorname{span}(e_i,e_z),\qquad
L_i=c_i+\mathbb R f_i.
\tag{1}
\]
Put
\[
\theta=\alpha_2-\alpha_1,\qquad
c=\cos\theta,\qquad s=\sin\theta,\qquad
\Delta w=w_1-w_2,\qquad
\delta=A_1-A_2c.
\tag{2}
\]

### Aligned translation

The circles are aligned exactly when \(L_1=L_2\).  Equality of the
line directions first gives \(s=0\).  Then \(H_1=H_2\), while
\(c_1-c_2\in H_1\) and \(f_1\perp H_1\).  Thus the two axis lines can
be equal only when \(c_1=c_2\).  In the signed coordinates this is
equivalent to
\[
\boxed{
s=0,\qquad \Delta w=0,\qquad A_1-A_2c=0.
}
\tag{3}
\]
This includes both \(\theta=0\) and the sign-reversed
\(\theta=\pi\) parameterization.

For axial charts, aligned therefore means a common centre and common
perpendicular axis.  The different-radius construction in
`TWO_CIRCLE_AXIS_CHART_BARRIER.md` is precisely the aligned
Mathialagan--Sheffer exception.

### Perpendicular translation

The planes \(H_1,H_2\) are perpendicular exactly when
\[
c=f_1\cdot f_2=0.
\]
Under \(c=0\), the horizontal vector \(e_1\) is normal to \(H_2\),
and \(e_2\) is normal to \(H_1\).  Hence
\[
c_1\in H_2\iff A_1=0,\qquad
c_2\in H_1\iff A_2=0.
\]
The source definition of perpendicular circles therefore becomes
\[
\boxed{
c=0,\qquad A_1=0,\qquad A_2=0.
}
\tag{4}
\]
There is no restriction on \(w_1,w_2\), since the common \(z\)-axis
lies in both containing planes.

## 2. Why the perpendicular exception is absent here

An incidence-active reverse circle retained by the campaign comes
from a target point off the common \(z\)-axis and a nonperpendicular
source--target plane pair.  Its radial centre parameter is
\[
A_i=\cos(\alpha_i-\beta)\,v,
\tag{5}
\]
where \(v\ne0\) and the retained cosine is nonzero.  Therefore
\[
\boxed{A_i\ne0}
\tag{6}
\]
for every such repeated-circle chart.

Condition (4) is consequently impossible for two genuine retained
charts.  This is special to the campaign's axial-chart family; the
perpendicular exception is essential for arbitrary pairs of circles
in \(\mathbb R^3\).

Combining (3), (4), (6), and (MS) yields the exact bridge.

### Known-classification corollary

Let \(C_1,C_2\) be two distinct incidence-active reverse circles from
the campaign, and let \(P_i\subset C_i\) be their source incidence
sets, with \(|P_i|=s_i\).  If
\[
(s,\Delta w,A_1-A_2c)\ne(0,0,0),
\tag{7}
\]
then the circles are not aligned; they cannot be perpendicular by
(6).  Hence
\[
\boxed{
|\Delta^2(P_1,P_2)|
=
\Omega\!\left(
\min\{s_1^{2/3}s_2^{2/3},s_1^2,s_2^2\}
\right).
}
\tag{8}
\]

Equation (8) is a direct application of Mathialagan--Sheffer
Theorem 1.4(b), not a campaign novelty claim.

## 3. Critical-scale consequence and remaining extraction gap

On the critical Erdős branch the total squared-distance budget is
\[
|\mathcal D|\le t^{3+o(1)}.
\tag{9}
\]
If \(s_i=t^{a_i+o(1)}\), then (8) forces
\[
\min\left\{
\frac23(a_1+a_2),\,2a_1,\,2a_2
\right\}
\le3.
\tag{10}
\]
In particular, two nonaligned active circles with
\[
s_1,s_2\ge t^{3/2+\eta}
\]
must satisfy
\[
s_1s_2\le t^{9/2+o(1)}.
\tag{11}
\]
The balanced threshold is especially transparent:
\[
s_1,s_2\ge t^{9/4+\eta}
\quad\Longrightarrow\quad
|\Delta^2(P_1,P_2)|
\ge t^{3+4\eta/3-o(1)},
\tag{12}
\]
contradicting (9).

The current hub theorem does not produce two circles satisfying
these incidence-size hypotheses.  Its multiplicity
\(\mu\) counts repeated triples attached to one active normalized
circle; it supplies neither a second nonaligned class nor a lower
bound of \(t^{9/4+\eta}\) for two source incidence sets.

Thus the corrected next target is an extraction theorem of one of
the following forms:

1. two nonaligned active circles whose incidence sizes violate
   (10);
2. many nonaligned circle classes whose aggregate use of (8) beats
   the critical distance budget; or
3. a proof that essentially all large-incidence active circles must
   lie in one aligned family, followed by an attack on that aligned
   Lenz-type concentration.

The missing step is no longer a two-circle collision theorem:
Mathialagan--Sheffer already supplies it outside the exact aligned
exception.
