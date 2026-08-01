# Erdős #809 — repeated-zero graph vertex-cover defect theorem

Date: 2026-08-01

Status: `PROVED__EXACT_VERTEX_COVER_BOUND__LINEAR_MATCHING_HARDNESS`

## 1. Setup

Use the maximum-degree witness
\[
 A=N[v],\qquad m=|A|,\qquad B=V(G)\setminus A,
 \qquad r=|B|,
\]
and the outer endpoint sets \(Y_\gamma\subseteq B\). Put
\[
 D_B=\sum_\gamma(|Y_\gamma|-1)_+.
\]

Define the **repeated-zero graph** \(Z_+\) on vertex set \(B\): a pair
\(bc\) is an edge of \(Z_+\) exactly when it is zero-shore and belongs
to \(\binom{Y_\gamma}{2}\) for at least two colours \(\gamma\). Thus
every edge of \(Z_+\) carries genuine excess multiplicity.

Let \(L\subseteq B\) be any vertex cover of \(Z_+\). Write
\[
 l=|L|,\qquad
 u_\gamma=|Y_\gamma\setminus L|,
 \qquad
 w_\gamma=|Y_\gamma\cap L|.
\tag{1}
\]
Let \(M_B[L]\) denote the number of missing \(B\)-edges internal to
\(L\), and put
\[
 g=m-r.
\tag{2}
\]
Finally, let
\[
 N_0(L)=
 |\{\gamma:|Y_\gamma|\ge1, u_\gamma=0\}|
\tag{3}
\]
and
\[
 P_{\ge3}(L)=
 \sum_{\gamma:\,u_\gamma\ge3}
 \binom{u_\gamma-1}{2}.
\tag{4}
\]

## 2. Exact theorem

### Theorem 2.1 (vertex-cover defect bound)

For every vertex cover \(L\) of the repeated-zero graph,
\[
\boxed{
 D_B-M_B
 \le
 M_B[L]+g|L|-N_0(L)-P_{\ge3}(L).
}
\tag{5}
\]
Consequently,
\[
\boxed{
 D_B-M_B
 \le
 \binom{|L|}{2}+g|L|-N_0(L)-P_{\ge3}(L).
}
\tag{6}
\]

#### Proof

Every active pair contained in \(B\setminus L\) occurs in at most one
colour. Indeed, a nonempty-shore pair has this property by the
fixed-pair theorem, while a zero-shore pair occurring twice would be an
edge of \(Z_+\) not met by \(L\). Hence the
\[
 P_L=\sum_\gamma\binom{u_\gamma}{2}
\tag{7}
\]
pairs generated outside \(L\) are distinct missing edges of \(G[B-L]\).

The following identity is immediate colour by colour. If
\(u_\gamma=0\), then
\((|Y_\gamma|-1)_+=w_\gamma-1\) for a nonempty colour. If
\(u_\gamma\ge1\), then
\[
 (|Y_\gamma|-1)-\binom{u_\gamma}{2}
 =w_\gamma-\binom{u_\gamma-1}{2}.
\]
Therefore
\[
 D_B-P_L
 =\sum_\gamma w_\gamma-N_0(L)-P_{\ge3}(L).
\tag{8}
\]

For \(x\in L\), the number of colours whose endpoint set contains
\(x\) is exactly \(d_A(x)\): every \(A\)--\(B\) edge has forced outer
endpoint \(x\), and same-colour good edges form a matching. Thus
\[
 \sum_\gamma w_\gamma=\sum_{x\in L}d_A(x).
\tag{9}
\]
Since \(v\) has maximum degree \(m-1\),
\[
 d_A(x)+d_B(x)\le m-1.
\]
Writing \(\overline d_B(x)=r-1-d_B(x)\), this gives
\[
 d_A(x)\le\overline d_B(x)+g.
\tag{10}
\]

Let \(I_B(L)\) count missing \(B\)-edges incident to \(L\). Since an
internal missing edge is counted twice in the missing-degree sum,
\[
 \sum_{x\in L}\overline d_B(x)=I_B(L)+M_B[L].
\tag{11}
\]
Combining (8)--(11),
\[
 D_B
 \le P_L+I_B(L)+M_B[L]+g|L|-N_0(L)-P_{\ge3}(L).
\]
The first two terms count disjoint sets of missing edges, so
\(P_L+I_B(L)\le M_B\). This proves (5), and
\(M_B[L]\le\binom{|L|}{2}\) proves (6). \(\square\)

## 3. Asymptotic hardness consequence

Let \(\tau(Z_+)\) be the vertex-cover number of the repeated-zero graph.
Choosing a minimum cover in (6) and discarding the nonnegative credits
gives the explicit universal bound
\[
\boxed{
 D_B\le M_B+\binom{\tau(Z_+)}2+g\tau(Z_+).
}
\tag{12}
\]
Since \(|g|\le n\), this immediately gives
\[
 \tau(Z_+)=o(n)
 \quad\Longrightarrow\quad
 \boxed{D_B\le M_B+o(n^2)}.
\tag{13}
\]

Thus any sequence for which
\[
 D_B-M_B=\Omega(n^2)
\tag{14}
\]
must have
\[
 \boxed{\tau(Z_+)=\Omega(n).}
\tag{15}
\]
If \(\nu(Z_+)\) is the matching number, the endpoints of a maximal
matching form a vertex cover, so \(\tau(Z_+)\le2\nu(Z_+)\). Consequently
every sequence satisfying (14) contains
\[
 \boxed{\nu(Z_+)=\Omega(n)}
\tag{16}
\]
pairwise vertex-disjoint repeated zero-shore pairs.

The constants are explicit. If
\[
 E=D_B-M_B>0
\]
and \(L\) is a minimum vertex cover, (6) after discarding the two
nonnegative credits gives
\[
 E\le\frac{l(l-1)}2+gl.
\]
Hence
\[
\boxed{
 \tau(Z_+)=l\ge
 \frac{-(2g-1)+\sqrt{(2g-1)^2+8E}}2,
 \qquad
 \nu(Z_+)\ge\frac{l}{2}.
}
\tag{17}
\]
At the minimal fixed-\(s\) scale \(g/n\to2s\), a gap
\(E\ge\varepsilon n^2\) therefore forces
\[
 \frac{\tau(Z_+)}n
 \ge\sqrt{4s^2+2\varepsilon}-2s-o(1),
 \qquad
 \frac{\nu(Z_+)}n
 \ge\frac{\sqrt{4s^2+2\varepsilon}-2s}{2}-o(1).
\tag{18}
\]

This is the desired synchronization threshold: concentrated exceptional
stars are asymptotically harmless for the \(B\)-defect, and a genuinely
quadratic failure must instead provide a linear matching of disjoint
zero-shore decompositions. The next structural task is to align the
R003 two-block decompositions associated with that matching.

## 4. Exact closure interfaces

The theorem also gives finite sufficient conditions. For any cover
\(L\), either of
\[
 M_B[L]+g|L|\le N_0(L)+P_{\ge3}(L)
\tag{19}
\]
or the stronger readily checked condition
\[
 \binom{|L|}{2}+g|L|\le N_0(L)+P_{\ge3}(L)
\tag{20}
\]
implies \(D_B\le M_B\).

Together with \(R_A\le S_m\), either condition closes the full
maximum-degree defect inequality
\[
 D_A=R_A+D_B\le S_m+M_B.
\]

More generally, suppose the full target fails by a positive amount
\[
 \Xi=D_A-(M_B+S_m)>0.
\]
Since
\[
 \Xi=(R_A-S_m)+(D_B-M_B),
\]
at least one of the following holds:

1. \(R_A-S_m>\Xi/2\);
2. \(D_B-M_B\ge\Xi/2\), in which case (17) supplies a matching of at
   least
   \[
   \boxed{
   \frac{-(2g-1)+\sqrt{(2g-1)^2+4\Xi}}4
   }
   \tag{21}
   \]
   pairwise vertex-disjoint repeated zero-shore pairs.

Thus a macroscopic counterexample to the maximum-degree defect bound is
forced into a precise two-way normal form: a macroscopic outer-\(A\)
residue, or a linear synchronized family of disjoint repeated
zero-shore pairs.

## 5. Scope firewall

Theorem 2.1 controls the outer-\(B\) defect for every repeated-zero
vertex cover. It does not prove that \(\tau(Z_+)=o(n)\), align a linear matching
of zero-shore decompositions, or control the outer-\(A\) residue
\(R_A\). The maximum-degree branch and Erdős #809 remain open.

As a falsification guard, `verify_global_reserve_union.py` enumerates
every vertex cover in each of its 4,045 accepted deterministic/seeded
\(B\)-side models, instantiates the maximum-degree inequality, and
checks (5) exactly. The models audit the algebra but are not asserted to
extend to full BCM witnesses.
