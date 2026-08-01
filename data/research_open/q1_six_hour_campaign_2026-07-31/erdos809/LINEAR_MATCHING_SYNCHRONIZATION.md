# Erdős #809 — linear zero-matching synchronization theorem

Date: 2026-08-01

Status: PROVED__LINEAR_ZERO_MATCHING_FORCES_LINEAR_ANTICOMPLETE_BLOCKS

## 1. Main theorem

Let \(G\) be an \(n\)-vertex graph of minimum degree \(\delta\), and let
\[
 F=\{\{b_i,c_i\}:1\le i\le f\}
\tag{1}
\]
be a matching of zero-shore missing pairs.  Thus all \(2f\) endpoints
are distinct and there is no simple three-edge path between \(b_i\)
and \(c_i\).  Let
\[
 \overline M=\binom n2-e(G)
\tag{2}
\]
be the total number of missing edges of \(G\).

### Theorem 1.1 (zero-matching synchronization)

If \(f>0\), then there are disjoint endpoint sets
\[
 U=\{b_i:i\in I\},\qquad V=\{c_i:i\in I\}
\tag{3}
\]
after independently orienting the pairs in a submatching, such that
\[
 E_G(U,V)=\varnothing
\tag{4}
\]
and
\[
 \boxed{
 |U|=|V|=|I|
 \ge
 \max\left\{
 0,\
 \left\lceil
 \frac{f\binom{\delta}{2}}{\overline M}
 \right\rceil
 \right\}.
 }
\tag{5}
\]
In particular, if \(\delta=\Omega(n)\) and \(f=\Omega(n)\), then
\(U,V\) both have linear size.

If every member of \(F\) is active in the maximum-witness colour
system, then every edge of the missing rectangle \(U\times V\) belongs
to the global reserve union \(\mathcal Q\).  Consequently
\[
 \boxed{
 |\mathcal Q|
 \ge
 \left(
 \max\left\{
 0,\
 \left\lceil
 \frac{f\binom{\delta}{2}}{\overline M}
 \right\rceil
 \right\}
 \right)^2.
 }
\tag{6}
\]

This removes the principal weakness left by
MATCHING_RECTANGLE_TRANSFERENCE.md: the matching need not carry large
colour multiplicities.  Linear minimum degree alone synchronizes a
linear unweighted zero matching.

## 2. Proof

For each \(i\), put
\[
 P_i=N(b_i),\qquad Q_i=N(c_i).
\tag{7}
\]
Let \(\mathcal C_i\) be the set of unordered pairs
\[
 \{x,y\},\qquad x\ne y,\quad x\in P_i,\quad y\in Q_i.
\tag{8}
\]
Every member of \(\mathcal C_i\) is a missing edge: otherwise
\(b_i-x-y-c_i\) is a simple three-edge path.  The usual overlapping-set
count gives
\[
 |\mathcal C_i|
 \ge
 \binom{\min\{|P_i|,|Q_i|\}}2
 \ge
 \binom{\delta}{2}.
\tag{9}
\]
For completeness, if \(p=|P_i|\), \(q=|Q_i|\), and
\(r=|P_i\cap Q_i|\), then
\[
 |\mathcal C_i|=pq-r-\binom r2.
\tag{10}
\]
At fixed \(p,q\), this is minimized by the largest possible
intersection; after assuming \(p\le q\), it is at least
\(\binom p2\), proving (9).

For a missing edge \(z\in\overline E(G)\), let
\[
 \mu(z)=|\{i:z\in\mathcal C_i\}|.
\tag{11}
\]
Double counting and (9) give
\[
 \sum_{z\in\overline E(G)}\mu(z)
 =\sum_i|\mathcal C_i|
 \ge f\binom{\delta}{2}.
\tag{12}
\]
Hence some missing edge \(z=\{x,y\}\) satisfies
\[
 \mu(z)
 \ge
 \left\lceil
 \frac{f\binom{\delta}{2}}{\overline M}
 \right\rceil.
\tag{13}
\]
The denominator is nonzero: the existence of a zero-shore missing pair
already implies \(\overline M>0\).

For every occurrence counted by \(\mu(xy)\), orient its pair so that
\[
 x\in N(b_i),\qquad y\in N(c_i).
\tag{14}
\]
This is possible by the definition of \(\mathcal C_i\).  Neither anchor
can be an endpoint of a pair that it supports.  Indeed, \(x=b_i\)
would be a loop in \(x\in N(b_i)\), while \(x=c_i\) would make the
missing pair \(b_ic_i\) an edge; the two possibilities for \(y\) are
identical.  Thus no exceptional index must be deleted.  Let \(I\) be
the full support in (13).  Then (5) holds exactly, and neither \(x\)
nor \(y\) is an endpoint of a pair indexed by \(I\).

For \(i,j\in I\), the diagonal pair \(b_ic_i\) is missing.  If
\(i\ne j\) and \(b_jc_i\) were an edge, then
\[
 b_i-x-b_j-c_i
\tag{15}
\]
would be a simple three-edge path between the endpoints of the
zero-shore pair \(\{b_i,c_i\}\), a contradiction.  Therefore every
pair in \(U\times V\) is missing, proving (4).

If the pairs are active, every vertex in \(U\cup V\) is an endpoint of
an active zero-shore pair.  The global reserve contains every missing
\(B\)-edge incident with such an endpoint.  Thus
\[
 U\times V\subseteq\mathcal Q,
\]
and its \(|I|^2\) pairs prove (6). \(\square\)

### Corollary 2.1 (common complementary hosts)

The sets in Theorem 1.1 can be chosen together with a missing anchor
pair \(xy\) such that
\[
 U\subseteq N(x),\qquad V\subseteq N(y),
\tag{15a}
\]
and
\[
 \boxed{
 N(v)\cap N(x)=\varnothing\quad(v\in V),
 \qquad
 N(u)\cap N(y)=\varnothing\quad(u\in U).
 }
\tag{15b}
\]
Put
\[
 C_x=V(G)\setminus N(x),\qquad
 C_y=V(G)\setminus N(y),\qquad
 \kappa=n-2\delta.
\tag{15c}
\]
Then every \(v\in V\) and \(u\in U\) satisfies
\[
 \boxed{
 N(v)\subseteq C_x,\quad |C_x\setminus N(v)|\le\kappa,
 \qquad
 N(u)\subseteq C_y,\quad |C_y\setminus N(u)|\le\kappa.
 }
\tag{15d}
\]
Equivalently, \(V\) is anticomplete to the entire common block \(N(x)\)
and every member of \(V\) is complete to all but at most \(\kappa\)
vertices of the common complementary host \(C_x\); the symmetric
statement holds for \(U,N(y),C_y\).

#### Proof

The anchor construction gives (15a).  If
\(z\in N(v_i)\cap N(x)\), then
\[
 u_i-x-z-v_i
\]
is a simple three-edge path.  Indeed \(z\ne x\), because open
neighbourhoods do not contain their centres, and none of the other
coincidences is possible in a simple graph.  This contradicts the
zero-shore property.  Hence \(N(v_i)\cap N(x)=\varnothing\);
the other identity is symmetric.

It follows that \(N(v)\subseteq C_x\), and therefore
\[
 |C_x\setminus N(v)|
 =n-d(x)-d(v)
 \le n-2\delta=\kappa.
\]
The \(U,C_y\) statement is identical. \(\square\)

### Corollary 2.2 (anchored missing-energy bound)

Let \(t=|U|=|V|\), and define
\[
 d_*=\max\{\delta,t\},
 \qquad
 r_*=\min\{t,d_*-t\}.
\tag{15e}
\]
Then the common-host conclusion forces
\[
 \boxed{
 \overline M
 \ge
 t d_*-r_*-\binom{r_*}{2}.
 }
\tag{15f}
\]
In the main range \(\delta\ge2t\), this is
\[
 \boxed{
 \overline M\ge t\delta-\frac{t(t+1)}2.
 }
\tag{15g}
\]

#### Proof

The sets \(V\) and \(N(x)\) are anticomplete.  Put
\[
 d_x=d(x),\qquad r_x=|V\cap N(x)|.
\]
The \(t\) vertices of \(U\) lie in \(N(x)\setminus V\), so
\[
 d_x\ge\max\{\delta,t\},
 \qquad
 r_x\le\min\{t,d_x-t\}.
\]
The exact number of distinct unordered pairs with one endpoint in
\(V\) and one in \(N(x)\) is
\[
 t d_x-r_x-\binom{r_x}{2}.
\]
It decreases with \(r_x\).  After taking the largest allowed
intersection, the resulting expression is nondecreasing in \(d_x\);
its minimum is attained at \(d_x=d_*\), \(r_x=r_*\).  All these pairs
are missing, proving (15f).  When \(\delta\ge2t\), one has
\(d_*=\delta\) and \(r_*=t\), giving (15g). \(\square\)

## 3. Exact obstruction inequality

Assume from now on that \(\delta\ge2\).  In the global
reserve-failure regime,
\[
 |\mathcal Q|\le D_B-1.
\tag{16}
\]
Put
\[
 q_B=\left\lfloor\sqrt{D_B-1}\right\rfloor.
\tag{17}
\]
Equations (6) and (16) imply
\[
 \left\lceil
 \frac{f\binom{\delta}{2}}{\overline M}
 \right\rceil
 \le q_B,
\]
and therefore every active zero-shore matching obeys
\[
 \boxed{
 f
 \le
 \frac{\overline M\,q_B}
      {\binom{\delta}{2}}.
 }
\tag{18}
\]
This is the first exact inequality coupling all four quantities:
zero-matching size, global missing-edge energy, minimum degree, and the
actual reserve-union obstruction.

### Theorem 3.1 (exact quadratic reserve cost)

Assume \(\delta\ge2\) and that \(F\) is nonempty, and put
\[
 \alpha=\frac{\binom{\delta}{2}}{\overline M},
 \qquad
 c_\alpha=\frac{\alpha}{2-\alpha}.
\tag{19}
\]
Then \(0<\alpha\le1\), and every matching \(F\) of \(f\) active
zero-shore pairs satisfies
\[
 \boxed{
 |\mathcal Q|\ge c_\alpha f^2.
 }
\tag{20}
\]

#### Proof

Apply Theorem 1.1 repeatedly to the remaining matching.  If its current
size is \(r>0\), select exactly
\[
 t=\lceil\alpha r\rceil
\tag{21}
\]
members from the synchronized submatching and remove them.  The theorem
guarantees that these \(t\) pairs span a missing \(t\)-by-\(t\)
rectangle in \(\mathcal Q\).  Rectangles selected in different rounds
are edge-disjoint, because their matching endpoints are disjoint.

Put \(c=c_\alpha\) and write \(t=\alpha r+\varepsilon\), where
\(0\le\varepsilon<1\).  The defining identity
\((1+c)\alpha=2c\) gives
\[
 \begin{aligned}
 t^2+c(r-t)^2-cr^2
 &=2cr\varepsilon+(1+c)\varepsilon^2\\
 &\ge0.
 \end{aligned}
\tag{22}
\]
Because \(t\ge1\), the process exhausts the matching.  Sum (22) over
all rounds and telescope the potential \(cr^2\), obtaining
\[
 \sum_jt_j^2\ge cf^2.
\tag{23}
\]
The selected rectangles are disjoint subsets of \(\mathcal Q\), so
\(|\mathcal Q|\ge\sum_jt_j^2\).  This proves (20). \(\square\)

### Corollary 3.2 (closed-form matching caps)

Write
\[
 d_0=\binom{\delta}{2}.
\]
Theorem 3.1 is equivalently
\[
 \boxed{
 |\mathcal Q|
 \ge
 \frac{d_0}{2\overline M-d_0}\,f^2.
 }
\tag{23a}
\]
Consequently every global reserve obstruction satisfies the stronger
matching cap
\[
 \boxed{
 f
 \le
 \sqrt{
 \frac{(D_B-1)(2\overline M-d_0)}{d_0}
 }.
 }
\tag{23b}
\]

There is also a colouring-free extremal consequence.  For a matching
of arbitrary zero-shore pairs, the same disjoint rectangles lie in the
global missing-edge set, even when the pairs are not active.  Replacing
\(\mathcal Q\) by that set in the proof gives
\[
 \overline M
 \ge
 \frac{d_0}{2\overline M-d_0}f^2.
\]
Equivalently,
\[
 \boxed{
 \overline M
 \ge
 \max\left\{
 d_0,\
 \frac{d_0+\sqrt{d_0^2+8d_0f^2}}4
 \right\}.
 }
\tag{23c}
\]
The first term records the sharper one-pair neighbourhood rectangle;
the quadratic root is stronger once \(f^2>d_0\).  Thus (23c) is a
standalone extremal bound on matchings of vertex-disjoint pairs having
no three-edge path.

Combine (18) with the repeated-zero vertex-cover theorem.  If
\[
 E=D_B-M_B>0,\qquad g=|A|-|B|,
\]
then a maximum matching of the repeated-zero graph has size at least
\[
 \frac14\left(
 -(2g-1)+\sqrt{(2g-1)^2+8E}
 \right).
\tag{26}
\]
Thus any global obstruction with positive \(B\)-defect gap must satisfy
the explicit necessary inequality obtained by substituting (26) into
the left side of (18).  Violation of that inequality closes the
\(B\)-defect budget.

## 4. Fixed-\(s\) consequence

Suppose
\[
 e(G)=\left(\frac14+s^2+o(1)\right)n^2,\qquad
 \delta(G)\ge\left(\frac12-s-o(1)\right)n,
\tag{27}
\]
where \(0<s<1/2\), and suppose \(f\ge\beta n\).  Since
\[
 \frac{\overline M}{n^2}
 =\frac14-s^2+o(1),
\]
Theorem 1.1 yields anticomplete \(U,V\subseteq B\) with
\[
 \boxed{
 \frac{|U|}{n}=\frac{|V|}{n}
 \ge
 \frac{\beta(1-2s)}{2(1+2s)}-o(1).
 }
\tag{28}
\]
The iterated form is stronger at the reserve level.  Here
\[
 \alpha
 =
 \frac{1-2s}{2(1+2s)}+o(1),
 \qquad
 c_\alpha
 =
 \frac{1-2s}{3+10s}+o(1).
\tag{29}
\]
Therefore the same matching forces
\[
 \boxed{
 \frac{|\mathcal Q|}{n^2}
 \ge
 \frac{(1-2s)\beta^2}{3+10s}-o(1).
 }
\tag{30}
\]
Therefore the quadratic \(B\)-defect alternative from
ZERO_GRAPH_VERTEX_COVER_THEOREM.md now has a concrete global structural
output: either the outer-\(A\) residue is macroscopic, or the graph
contains two linearly large, aligned, anticomplete endpoint blocks
arising from pairwise vertex-disjoint repeated zero-shore
decompositions.

What remains is no longer synchronization itself.  It is the embedding
step that converts the anticomplete endpoint blocks, together with the
full \(L_4(2)\) connector condition and edge-energy ledger, into either
a large \(C_7\)-compatible family or enough slack to pay the defect.

## 5. Verification and claim boundary

The script verify_linear_matching_synchronization.py independently
checks:

1. the exact overlapping-neighbourhood formula (10);
2. the lower bound (9) exhaustively for all set pairs on a
   six-element universe;
3. the incidence averaging and proof that no endpoint deletion occurs;
4. the forced \(|I|^2\) endpoint rectangle on 2,000 seeded systems;
5. the arithmetic passage from (6) to (18) and the closed forms
   (23a)--(23c);
6. the common complementary-host identities (15b)--(15d) and anchored
   missing-energy bound (15f);
7. the exact greedy recurrence and potential bound (20) on 5,000 rational
   parameter pairs.

The finite audit checks only identities and extremal counts.  The
universal result is the proof above.  The theorem does not yet perform
the final \(C_7\)-embedding/slack step, does not control \(R_A\), and
does not prove the maximum-degree branch or Erdős #809.
