# Erdős #809 — matching rectangle transference

Date: 2026-08-01

Status: `PROVED__TWO_LEVEL_MISSING_RECTANGLE_AND_NONLINEAR_MATCHING_CAPACITY`

## 1. Outcome

The repeated-zero vertex-cover theorem forces a linear matching whenever
the outer-\(B\) defect has a genuinely quadratic excess.  This note proves
the first synchronization theorem for such a matching.

Let \(F=\{e_1,\ldots,e_f\}\) be a matching of active zero-shore pairs in
\(B\).  If the colour rectangle associated with several members of \(F\)
uses one common coordinate \(a\in A\), then the corresponding two sets of
matched endpoints form a complete missing rectangle in \(B\).  The same is
true when several colour rectangles contain one common missing \(A\)-pair.

Writing \(h_i\) for the colour multiplicity of \(e_i\), \(M_A\) for the
number of missing edges in \(G[A]\), and \(\mathcal Q\) for the global
reserve union, the result gives
\[
 \boxed{
  2\sum_{i=1}^f h_i\le |A|\sqrt{|\mathcal Q|},
  \qquad
  \sum_{i=1}^f h_i^2\le M_A\sqrt{|\mathcal Q|}.
 }
 \tag{1}
\]
In particular, under global reserve failure \(|\mathcal Q|<D_B\),
with
\[
 q=\left\lfloor\sqrt{D_B-1}\right\rfloor,
\]
one has
\[
 \boxed{
  2\sum_i h_i\le |A|q,
  \qquad
  \sum_i h_i^2\le M_Aq.
 }
 \tag{2}
\]
This is a genuine two-level transfer: overlap of missing rectangles in
\(A\) creates a quadratically large set of *actual missing edges in \(B\)*.
It improves the old per-rectangle estimate for vertex-disjoint zero pairs
and supplies an exact capacity constraint for the linear matching forced
by a quadratic defect gap.  It does not yet prove that the matching has
enough total weight to close the maximum-degree branch.

## 2. Setup

Retain the maximum-degree witness
\[
 A=N[v],\qquad B=V(G)\setminus A.
\]
Let
\[
 F=\{e_i=\{b_i,c_i\}:1\le i\le f\}
\tag{3}
\]
be a matching of active zero-shore pairs.  Thus all \(2f\) displayed
vertices are distinct, every \(b_ic_i\) is missing, and there is no simple
three-edge \(b_i\)-to-\(c_i\) path.

For each \(i\), orient \(e_i\) temporarily as \((b_i,c_i)\), let
\(\Gamma_i\) be the colours using that pair, and put
\[
 X_i=\{x_{i,\gamma}:\gamma\in\Gamma_i\},\qquad
 Y_i=\{y_{i,\gamma}:\gamma\in\Gamma_i\},
 \qquad h_i=|\Gamma_i|.
\tag{4}
\]
Here \(b_ix_{i,\gamma}\) and \(c_iy_{i,\gamma}\) have colour \(\gamma\).
The fifth-stage colour-rectangle lemma gives
\[
 |X_i|=|Y_i|=h_i,\qquad X_i\cap Y_i=\varnothing,
 \qquad X_i\times Y_i\subseteq\overline E(G[A]).
\tag{5}
\]
Swapping \(b_i,c_i\) swaps \(X_i,Y_i\), so all statements below are
independent of the initial orientations.

Let \(\mathcal Q\subseteq\overline E(G[B])\) be the global reserve union
from `GLOBAL_RESERVE_UNION_REDUCTION.md`.  In particular, every missing
\(B\)-edge incident with an endpoint of an active zero-shore pair belongs
to \(\mathcal Q\).

## 3. One-anchor transference

### Lemma 3.1 (common coordinate creates a missing \(B\)-rectangle)

Fix \(a\in A\), and let \(I\subseteq\{1,\ldots,f\}\) be a set of indices
such that
\[
 a\in X_i\cup Y_i\qquad(i\in I).
\tag{6}
\]
Then there are disjoint sets \(U_a,V_a\subseteq B\), each of size
\(|I|\), such that
\[
 U_a\times V_a\subseteq\overline E(G[B])\cap\mathcal Q.
\tag{7}
\]
Consequently
\[
 |I|^2\le |\mathcal Q|.
\tag{8}
\]

#### Proof

For every \(i\in I\), orient \(e_i=(b_i,c_i)\) so that \(a\in X_i\).
Then \(ab_i\in E(G)\).  Put
\[
 U_a=\{b_i:i\in I\},\qquad V_a=\{c_i:i\in I\}.
\]
The matching property makes these two sets disjoint and gives both sizes
equal to \(|I|\).

The diagonal pair \(b_ic_i\) is missing.  If \(i\ne j\) and \(b_jc_i\)
were an edge, then
\[
 b_i-a-b_j-c_i
\]
would be a simple three-edge path between the endpoints of the zero-shore
pair \(e_i\), a contradiction.  Hence every pair in \(U_a\times V_a\)
is missing.  Each such pair is incident with an endpoint of an active
zero-shore pair, so it belongs to \(\mathcal Q\).  There are exactly
\(|I|^2\) such pairs, proving (8). \(\square\)

For \(a\in A\), define
\[
 r(a)=|\{i:a\in X_i\cup Y_i\}|.
\tag{9}
\]
Lemma 3.1 gives
\[
 \boxed{r(a)^2\le|\mathcal Q|.}
\tag{10}
\]
Since every \(X_i\cup Y_i\) has size \(2h_i\), double counting gives
\[
 2\sum_i h_i=\sum_{a\in A}r(a)
 \le |A|\sqrt{|\mathcal Q|},
\tag{11}
\]
which is the first inequality in (1).

## 4. Two-anchor transference

For a missing edge \(z=aa'\in\overline E(G[A])\), define its overlap
with the matching rectangles by
\[
 \mu_F(z)
 =|\{i:z\text{ has one endpoint in }X_i
              \text{ and one endpoint in }Y_i\}|.
\tag{12}
\]

### Lemma 4.1 (common missing coordinate pair)

For every \(z\in\overline E(G[A])\),
\[
 \boxed{\mu_F(z)^2\le|\mathcal Q|.}
\tag{13}
\]

#### Proof

For every rectangle counted by \(\mu_F(aa')\), orient its zero pair so
that \(a\in X_i\) and \(a'\in Y_i\).  Now apply Lemma 3.1 using only the
common coordinate \(a\).  The resulting missing \(B\)-rectangle has side
length \(\mu_F(aa')\) and lies in \(\mathcal Q\). \(\square\)

Each rectangle \(X_i\times Y_i\) contains exactly \(h_i^2\) distinct
missing \(A\)-edges.  Therefore
\[
 \sum_{z\in\overline E(G[A])}\mu_F(z)
 =\sum_i h_i^2.
\tag{14}
\]
Combining (13)--(14) proves
\[
 \sum_i h_i^2
 \le M_A\sqrt{|\mathcal Q|},
\tag{15}
\]
the second inequality in (1).

### Corollary 4.2 (weighted matching capacity)

Put
\[
 H_F=\sum_i h_i,
 \qquad W_F=\sum_i(h_i-1)=H_F-f.
\tag{16}
\]
Then
\[
 \boxed{
 H_F\le
 \min\left\{
 \frac{|A|\sqrt{|\mathcal Q|}}2,
 \sqrt{fM_A\sqrt{|\mathcal Q|}}
 \right\},
 }
\tag{17}
\]
and hence
\[
 \boxed{
 W_F\le
 \min\left\{
 \frac{|A|\sqrt{|\mathcal Q|}}2-f,
 \sqrt{fM_A\sqrt{|\mathcal Q|}}-f
 \right\}.
 }
\tag{18}
\]

#### Proof

The first term in (17) is (11).  Cauchy--Schwarz and (15) give
\[
 H_F^2\le f\sum_i h_i^2
 \le fM_A\sqrt{|\mathcal Q|}.
\]
Subtract \(f\) to obtain (18). \(\square\)

Under global reserve failure, integrality gives
\[
 |\mathcal Q|\le D_B-1.
\]
Replacing \(\sqrt{|\mathcal Q|}\) by
\(q=\lfloor\sqrt{D_B-1}\rfloor\) in (11), (15), (17), and (18) proves
all claimed failure-regime bounds.

## 5. Structural alternative

The proof contains more information than the numerical inequalities.
For every \(a\in A\), it explicitly constructs an anticomplete ordered
pair of equally sized endpoint sets \(U_a,V_a\subseteq B\) of size
\(r(a)\).  For every missing \(A\)-edge \(z\), it constructs such a pair
of size \(\mu_F(z)\).  Thus, for any \(\eta>0\) and any nonempty \(F\), either
\[
 \sum_i h_i^2<\eta M_A n,
\tag{19}
\]
or one obtains two disjoint sets in \(B\), each of size at least
\(\eta n\), with no edges between them.  This is an exact aligned
two-block output, not merely a large rectangle-overlap count.

The remaining issue is weight capture.  The vertex-cover theorem forces
a large *unweighted* matching from a quadratic defect gap, whereas (17)
and (18) constrain the multiplicity captured by a specified matching.
A theorem converting total repeated-zero mass into a sufficiently heavy
matching, or exploiting the many low-weight disjoint pairs directly, is
still needed.

## 6. Verification and scope firewall

`verify_matching_rectangle_transference.py` independently constructs
abstract matching-rectangle systems, materializes the forced missing
\(B\)-rectangles, and checks (10), (14), (15), (17), and (18), including
both orientations of a shared missing \(A\)-edge.  These finite checks
guard the double counts and orientation handling; the proof above is the
universal argument.

This theorem does not show that a defect-forced matching has quadratic
captured weight, does not control the outer-\(A\) residue \(R_A\), and does
not prove the maximum-degree branch or Erdős #809.
