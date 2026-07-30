# Sparse height–angle incidence expansion

Date: 2026-07-30.

## 1. Geometric setup

Fix an anchor point of angle zero on a coaxial circle of radius
\(\rho>0\) and height \(z_0\).  Let \(m\) further circles have the same
radius and distinct heights
\[
z_0<z_1<\cdots<z_m.
\]
Let \(B\) be a finite set of \(J\) distinct angular positions.  The
point set need not contain the complete height-by-angle rectangle.
Instead, record its incidences by
\[
E\subseteq\{1,\ldots,m\}\times B,\qquad I=|E|.
\]
For \((i,\beta)\in E\), the squared distance to the anchor is
\[
a_i+x_\beta,\qquad
a_i=(z_i-z_0)^2,\qquad
x_\beta=2\rho^2(1-\cos\beta).
\tag{1}
\]

Distinct angular positions give each chord value \(x_\beta\)
multiplicity at most two.  Put
\[
A=\{a_1,\ldots,a_m\},\qquad
\lambda(A)=\max_{t\ne0}|A\cap(A+t)|.
\tag{2}
\]

### Theorem 1 (sparse incidence expansion)

The number \(U\) of values in (1) satisfies
\[
\boxed{
U\ge\frac{I^2}{2I+\lambda(A)J^2}.
}
\tag{3}
\]
Therefore the original point configuration determines at least
\[
\frac{I^2}{2I+\lambda(A)J^2}-1
\tag{4}
\]
nonzero distances.

This theorem requires neither a common progression nor a complete
rectangle.  Its only synchronization input is reuse of a set of \(J\)
angular columns across \(I\) height-angle incidences.

## 2. Proof

For every real \(y\), let
\[
r(y)=|\{(i,\beta)\in E:a_i+x_\beta=y\}|.
\]
Then \(\sum_y r(y)=I\).  Its energy counts
\[
a_i+x_\beta=a_j+x_\gamma.
\tag{5}
\]

If \(x_\beta=x_\gamma\), then \(a_i=a_j\), so \(i=j\).  At a fixed
pair \((i,x)\), at most two angular positions have chord value \(x\).
Thus the contribution of all equal-chord pairs is at most
\[
\sum_{i,x}m_{i,x}^2\le2\sum_{i,x}m_{i,x}=2I.
\tag{6}
\]

If \(x_\beta\ne x_\gamma\), then for a fixed ordered pair of chord
values, (5) has at most \(\lambda(A)\) ordered height pairs.  There are
fewer than \(J^2\) ordered angular pairs, so these terms contribute at
most \(\lambda(A)J^2\).  Hence
\[
\sum_y r(y)^2\le2I+\lambda(A)J^2.
\]
Cauchy--Schwarz proves (3).

## 3. Consequences

### 3.1 Complete synchronization

If every angular column occurs on every height, then \(I=mJ\), and
(3) becomes
\[
U\ge\frac{m^2J^2}{2mJ+\lambda(A)J^2},
\]
exactly Theorem 1 of
`ARBITRARY_HEIGHT_ENERGY_DICHOTOMY.md`.

### 3.2 Minimum column degree

If each of the \(J\) angular columns occurs on at least \(Q\) heights,
then \(I\ge JQ\), and monotonicity of \(x^2/(2x+c)\) gives
\[
\boxed{
U\ge\frac{JQ^2}{2Q+\lambda(A)J}.
}
\tag{7}
\]
Thus:

- if \(Q\ge\lambda(A)J\), then \(U\gg JQ\);
- if \(Q<\lambda(A)J\), then \(U\gg Q^2/\lambda(A)\).

This is the exact source-incidence bridge to test against the old
common-axis quantities \(q_\alpha\).

### 3.3 Polynomial-range lattice heights

If \(z_i=z_0+h u_i\) with distinct integers
\(0<u_i\le H\), then
\[
\lambda(A)\le\max_{n\le H^2}\tau(n).
\tag{8}
\]
When \(H\le m^C\), this is \(m^{o(1)}\).  Consequently a reused sparse
angle graph already has
\[
U\gg
\min\{I,\ I^2/(m^{o(1)}J^2)\}.
\tag{9}
\]

## 4. Exact reconnection diagnosis

The old source statistic \(q_\alpha\) says that one angular plane
contains many points, but those points may be spread across many
radius classes.  Theorem 1 can be invoked only after choosing:

1. one radius class and an anchor circle in it;
2. a common set of angular columns \(B\);
3. enough incidences \(I\) within that one radius class;
4. either a small \(\lambda(A)\), or a separate argument for the
   high-\(\lambda\) height branch.

For the explicit anisotropic grid, restricting the \(M=N^{1/5}\)
active source angles to one radius class gives only
\(I=N^{3/5}\), reproducing the old threshold.  Its stronger
\(N^{4/5-o(1)}\) slice bound uses the full \(S=N^{2/5}\) angular set.
Therefore (3) is a genuine weakening of rectangular synchronization,
but source incidences alone still do not close the inherited branch:
one must convert the rotation-correlation mass into additional reused
angular columns.

This is a sharper open bridge than “extract identical fibres.”  The
quantitative target is now simply
\[
\frac{I^2}{2I+\lambda(A)J^2}>N^{3/5+\varepsilon}
\tag{10}
\]
on some repeated-radius class.

## 5. Claim status

- Theorem 1 and its corollaries are human proofs.
- The verifier exhausts arbitrary sparse rational incidence patterns
  and includes chord-value multiplicity two.
- No common-progression assumption is used.
- The inherited rotation correlations have not yet been proved to meet
  (10), so no unconditional improvement of \(f_3(N)\) is claimed.
