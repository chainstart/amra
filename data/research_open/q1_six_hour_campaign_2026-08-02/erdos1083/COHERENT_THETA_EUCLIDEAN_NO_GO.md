# Erdős #1083: a sharp Euclidean no-go model for coherent-theta closure

Date: 2026-08-02

## 0. Result and firewall

The coherent theta output of the frozen exact-block argument has no
standalone distance-budget contradiction, even after strengthening all
of its selected-record interfaces.

For every \(S\ge2\) and every \(1\le K\le S-1\), there is a genuine
finite point set in \(\mathbb R^3\) whose row-record graph contains
\(K\) internally vertex-disjoint coherent paths of length two with:

- the same two lifted endpoints;
- one fixed orientation word \((+,-)\);
- one fixed nonzero tangent difference \(\delta=1\);
- the same endpoint tangent square on every arm;
- the same internal tangent square on every arm;
- one common squared-distance label on all \(2K\) edges;
- rationally transverse row spaces on every edge; and
- positive tangents, off-axis targets, and distinct nonzero heights.

The complete local point set, including the entire \(S\)-point source
set and every selected target, has at most

\[
 2S^2+S
\tag{0.1}
\]

distinct nonzero distances.  At the frozen substitution
\(S=t^{7/9+o(1)}\), this is

\[
 t^{14/9+o(1)}=o(t^3).
\tag{0.2}
\]

In particular, the inherited \(t^{1/20+o(1)}\)-arm theta output is
far below a genuine local obstruction: the construction allows
\(K=S-1=t^{7/9+o(1)}\) arms.

This is a sharp no-go theorem for a **local closure lemma**, not a
counterexample to Erdős #1083.  The model has one selected tangent
cell per row; it does not give \(U=t^{5/6}\) tangent cells per row,
does not tile one common \(SU\)-element spectrum, and has far fewer
than the \(N=t^5\) points of the public problem.  Consequently a
valid positive closure theorem must use the full exact partitions
\(T_i\) (or information of equivalent strength), not merely the
theta graph and its selected records.

## 1. The source circle and the rows

Fix \(S\ge2\), \(1\le K\le S-1\), and put

\[
 X=X_S=\left\{\frac{j}{S-1}:0\le j<S\right\}
 \subset[0,1].
\tag{1.1}
\]

Use \(\rho=1\).  For \(1\le i\le K\), set

\[
 x_i=\frac{i}{S-1},
 \qquad
 z_i=-x_i+\sqrt{1+x_i^2}.
\tag{1.2}
\]

The two endpoint heights are

\[
 z_+=\sqrt2,
 \qquad z_-=-\sqrt2,
\tag{1.3}
\]

and their selected source label is \(x_0=0\).  Define the parabolic
potential

\[
 F(z,x)=z^2+2zx.
\tag{1.4}
\]

Equations (1.2)--(1.3) give the exact two-level chart

\[
 F(z_+,0)=F(z_-,0)=2,
 \qquad F(z_i,x_i)=1.
\tag{1.5}
\]

All heights are nonzero and distinct.  Indeed, every \(z_i\) is in
\((0,1)\), and the function
\(-x+\sqrt{1+x^2}\) is strictly decreasing for \(x>0\).

## 2. Exact transversality

All elements of \(X-X\) are rational and \(1/(S-1)\in X-X\), so

\[
 \operatorname{span}_{\mathbb Q}(X-X)=\mathbb Q.
\tag{2.1}
\]

The row space at height \(z\) is therefore

\[
 W_z=\operatorname{span}_{\mathbb Q}(2z(X-X))=z\mathbb Q.
\tag{2.2}
\]

For every \(i\), the ratio \(z_i/\sqrt2\) is irrational.  Otherwise
write \(z_i=r\sqrt2\) with \(r\in\mathbb Q\).  Substitution in
\(z_i^2+2x_iz_i=1\) gives

\[
 2r^2+2x_ir\sqrt2=1.
\tag{2.3}
\]

Here \(r\ne0\) and \(x_i>0\), so the coefficient of \(\sqrt2\) is
nonzero, contradicting (2.3).  Hence

\[
 W_{z_+}\cap W_{z_i}=W_{z_-}\cap W_{z_i}=\{0\}.
\tag{2.4}
\]

These are exactly the \(2K\) adjacencies used below.  No claim of
pairwise transversality among all internal rows is needed.

## 3. One fixed difference, tangent pair, and distance label

Fix any \(a>0\); the verifier uses \(a=10\).  Give both endpoint
rows the selected tangent square \(a\), and every internal row the
selected tangent square \(a+1\).  Direct both graph edges

\[
 z_+\longrightarrow z_i,
 \qquad z_-\longrightarrow z_i.
\tag{3.1}
\]

By (1.5), every directed edge obeys

\[
 F(z_\pm,0)-F(z_i,x_i)=1
 =(a+1)-a=:\delta.
\tag{3.2}
\]

Equivalently, it is an exact fixed-difference record:

\[
 z_\pm^2-z_i^2+2(z_\pm\cdot0-z_ix_i)=\delta.
\tag{3.3}
\]

The two corresponding tangent cells share the same label

\[
 d=1+F(z_\pm,0)+a
  =1+F(z_i,x_i)+(a+1)
  =a+3.
\tag{3.4}
\]

Thus tangent reuse has already been maximized: all endpoint
incidences use \(a\), all internal incidences use \(a+1\), and all
edges use the one label \(a+3\).  There is no latent pigeonhole gain
left to take from these selected records.

Traverse the path

\[
 z_+,z_i,z_-.
\]

The first directed edge agrees with the traversal and the second is
opposite to it, so every arm has word \((+,-)\).  At the internal row
both incident records use \(x_i\), and both endpoints use \(0\).
Every path is therefore coherent.  Its interior is the single row
\(z_i\), so the \(K\) interiors are pairwise vertex-disjoint.

## 4. Genuine Euclidean realization

Choose \(A>1\).  For every \(x\in X\), take the actual source point

\[
 p_x=(A+\sqrt{1-x^2},0,x).
\tag{4.1}
\]

These are \(S\) distinct points on the unit circle centred at
\((A,0,0)\) in the plane \(y=0\).  For a row \((z,\tau)\), take the
actual target

\[
 q_{z,\tau}=(A,\sqrt\tau,-z).
\tag{4.2}
\]

The Cartesian distance identity is

\[
\begin{aligned}
 \|p_x-q_{z,\tau}\|^2
 &= (1-x^2)+\tau+(x+z)^2\\
 &=1+z^2+\tau+2zx.
\end{aligned}
\tag{4.3}
\]

Consequently (3.4) is an equality between actual Euclidean squared
distances:

\[
 \|p_0-q_{z_+,a}\|^2
 =\|p_{x_i}-q_{z_i,a+1}\|^2
 =\|p_0-q_{z_-,a}\|^2
 =a+3.
\tag{4.4}
\]

Every tangent square is positive.  The target transverse coordinate
\(\sqrt\tau\) is nonzero, and \(A>1\) puts the chart in the genuine
nonperpendicular/off-axis regime used by the inherited reverse-circle
interface.  Distinct heights give distinct target rows.  For every
row, (4.3) is injective as a function of \(x\in X\), since \(z\ne0\).
Thus the construction realizes the whole selected \(S\)-element
tangent cell, not only the one highlighted incidence.

## 5. Complete local distance audit

Let

\[
 P_{S,K}
 =\{p_x:x\in X\}
 \cup\{q_{z_+,a},q_{z_-,a}\}
 \cup\{q_{z_i,a+1}:1\le i\le K\}.
\tag{5.1}
\]

All these points are distinct and

\[
 |P_{S,K}|=S+K+2\le2S+1.
\tag{5.2}
\]

This is a genuine point set, so its *entire* nonzero distance set,
including source--source, source--target, and target--target
distances, satisfies the unconditional bound

\[
 |\Delta(P_{S,K})|
 \le\binom{S+K+2}{2}
 \le\binom{2S+1}{2}
 =2S^2+S.
\tag{5.3}
\]

No uncontrolled cross-distance class is omitted from (5.3).  This is
why the construction is a full Euclidean audit of the *local theta
interface*, rather than merely a formal solution of the edge
equations.

At \(S=t^{7/9+o(1)}\), (5.3) is \(t^{14/9+o(1)}\), which is smaller
than the assumed global budget \(t^{3+o(1)}\) by

\[
 3-\frac{14}{9}=\frac{13}{9}.
\tag{5.4}
\]

## 6. Sharp meaning and remaining positive target

On one fixed potential level \(F=C\), a prescribed source label
\(x\) allows at most two heights because

\[
 z^2+2xz=C
\tag{6.1}
\]

is quadratic.  Hence a fixed-level family has at most \(2S\) rows.
The construction supplies \(S-1\), showing that the natural local
capacity is \(\Theta(S)\).  The inherited theta width
\(t^{1/20+o(1)}\) is far below this sharp scale
\(S=t^{7/9+o(1)}\).

The no-go result rules out each proposed closure step that uses only:

1. fixed \(\delta\);
2. coherent bounded paths;
3. common lifted endpoints and orientation word;
4. endpoint/internal tangent repetition;
5. adjacent rational transversality; and
6. the fact that all selected records are actual Euclidean distances.

It does **not** rule out a theorem that also uses the exact identities

\[
 V=(1+z^2+T_z)\oplus(2zX),\qquad |T_z|=U,
\tag{6.2}
\]

for all \(q\) rows.  Equation (6.2), and especially compatibility of
the unused \(U-1\) tangent cells across all arms, is now the first
unproved interface.  Any continued positive attack must charge those
unused cells or prove that completing the local model to (6.2)
creates a ruled/commensurate subsystem.

## 7. Reproduction

Run:

```bash
python3 verify_coherent_theta_euclidean_nogo.py
python3 -m unittest -v test_coherent_theta_euclidean_nogo.py
```

The verifier checks exact radical identities, row-cell injectivity,
minimal-polynomial transversality for finite falsifier instances, all
selected Euclidean distance equalities, point distinctness, and the
complete pair-count bound.  The all-parameter assertions are proved
above; enumeration is not used as their proof.
