# Independent audit of the two-circle--axis chart barrier

Date: 2026-07-30

Audited file:

- `TWO_CIRCLE_AXIS_CHART_BARRIER.md`

## 0. Verdict

\[
\boxed{\text{PASS}}
\]

The four general cross-distance formulas, the complete distance
ledger for two concentric regular polygons of different radii, the
\(4mn\) representation count, and the fixed-\(K\) extension are
correct.  In particular, the displayed upper bound
\[
3\lfloor n/2\rfloor+4m
\]
does include the source--source distances between the two different
circles; it is not merely the sum of the two one-circle ledgers.

The construction is only a barrier for charts with a common centre
and common perpendicular axis.  Mathialagan--Sheffer Theorem 1.4
already supplies bipartite distance expansion for circle pairs that
are neither aligned nor perpendicular.  In the campaign's axial-chart
coordinates the perpendicular exception would require
\(A_1=A_2=0\), which is impossible for retained active reverse
circles.  The corrected manuscript records this known classification
and does not claim a distinct-distance exponent gain.

## 1. Reconstruction of the four general formulas

Put \(D=c_1-c_2\), and define
\[
X_1=\cos\phi\,e_1+\sin\phi\,e_z,\qquad
X_2=\cos\psi\,e_2+\sin\psi\,e_z.
\]
The required inner products are
\[
\begin{gathered}
e_1\cdot e_2=f_1\cdot f_2=c,\qquad
e_1\cdot f_2=-s,\qquad f_1\cdot e_2=s,\\
D\cdot f_1=-A_2s,\qquad
D\cdot f_2=-A_1s,\\
D\cdot X_1=(A_1-A_2c)\cos\phi+\Delta w\sin\phi,\\
D\cdot X_2=(A_1c-A_2)\cos\psi+\Delta w\sin\psi,\\
X_1\cdot X_2=c\cos\phi\cos\psi+\sin\phi\sin\psi.
\end{gathered}
\tag{A1}
\]

Now expand, respectively,
\[
\begin{aligned}
q_1(y)-q_2(z)&=D+yf_1-zf_2,\\
p_1(\phi)-q_2(z)&=D+r_1X_1-zf_2,\\
q_1(y)-p_2(\psi)&=D+yf_1-r_2X_2,\\
p_1(\phi)-p_2(\psi)&=D+r_1X_1-r_2X_2.
\end{aligned}
\tag{A2}
\]
Substitution of (A1) reproduces equations (3)--(6) of the audited
manuscript with the same signs.  Independent floating-point
coordinate evaluations also check these identities away from the
concentric specialization.

## 2. Repeated-circle and representation ledger

For an axis point \(q_j=(a,hj,0)\),
\[
v_j^2=a^2+h^2j^2,\qquad c_jv_j=a.
\]
With \(d_{i,j}=r_i^2+h^2j^2\), the normalized reverse-circle equation
has coefficients
\[
u^2+z^2-2au+(v_j^2-d_{i,j})
=u^2+z^2-2au+a^2-r_i^2=0.
\tag{A3}
\]
Thus all \(2m\) signed odd indices give the same circle
\[
(u-a)^2+z^2=r_i^2
\]
for fixed \(i\).  Since \(r_1\ne r_2\), the two reverse circles are
distinct.  Each has \(n\) source incidences and \(2m\) targets, hence
\[
n(2m)+n(2m)=4mn
\tag{A4}
\]
source--target representations.  The labels depend on \(j^2\), so
each chart uses exactly \(m\) cross labels.

## 3. Complete two-radius distance ledger

Let \(f=\lfloor n/2\rfloor\).  The source--source block splits into
three unordered radius pairs.

### Within \(S_1\)

The nonzero distances are
\[
2r_1^2\left(1-\cos\frac{2\pi s}{n}\right),
\qquad 1\le s\le f,
\]
so there are exactly \(f\) values.

### Within \(S_2\)

The same calculation with \(r_2\) again gives exactly \(f\) values.

### Between \(S_1\) and \(S_2\)

Here
\[
r_1^2+r_2^2-2r_1r_2\cos\frac{2\pi s}{n},
\qquad 0\le s\le f.
\]
These \(f+1\) values are distinct.  The \(s=0\) value is
\((r_2-r_1)^2>0\), so it belongs to the nonzero distance set and is
the extra \(+1\) in the manuscript.

Consequently all source--source pairs contribute at most
\[
f+f+(f+1)=3f+1
\tag{A5}
\]
values after taking their union.  Possible coincidences between the
three rows only decrease the count.

The target odd arithmetic progression has exactly
\[
2m-1
\tag{A6}
\]
nonzero distances.  For each \(i\), all \(S_i-T\) distances are
\[
r_i^2+h^2j^2,\qquad |j|\in\{1,3,\ldots,2m-1\},
\]
and therefore contribute exactly \(m\) values.  Adding the four
category bounds gives
\[
(3f+1)+(2m-1)+m+m
=3\lfloor n/2\rfloor+4m.
\tag{A7}
\]
This accounts for within-circle, between-circle, axis--axis, and
both circle--axis blocks.

## 4. Fixed-\(K\) extension

For \(K\) distinct concentric radii, there are \(K\) within-radius
source blocks and \(\binom K2\) between-radius source blocks.  The
same ledger gives the explicit bound
\[
\begin{aligned}
|\Delta^2|
&\le
Kf+\binom K2(f+1)+(2m-1)+Km\\
&=
\binom{K+1}{2}f+\binom K2+(K+2)m-1.
\end{aligned}
\tag{A8}
\]
Since \(n\ge3\), this is
\[
O(K^2n+Km+m).
\tag{A9}
\]
Thus equation (13) is correct.  Its stated fixed-\(K\) scope is more
conservative than necessary: (A8) supplies an absolute explicit
bound for every finite \(K\), provided \(K\) distinct positive radii
smaller than \(a\) are chosen.

The corresponding repeated-circle representation count is
\[
2Kmn.
\tag{A10}
\]

## 5. Final assessment

The two-chart example is a genuine sharp obstruction to any argument
using only:

- the number of repeated circle classes;
- their different radii;
- their source incidence counts; and
- their target multiplicities.

Outside the aligned exception, the needed two-circle collision
estimate is already known from Mathialagan--Sheffer.  The campaign's
actual unresolved step is an extraction theorem forcing two
nonaligned active circles with source incidence sizes large enough to
use that bound, or an aggregate version over many nonaligned classes.
