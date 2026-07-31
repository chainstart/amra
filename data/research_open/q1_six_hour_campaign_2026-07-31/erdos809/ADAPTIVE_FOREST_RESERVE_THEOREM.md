# Erdős #809 — adaptive forest-reserve theorem

Date: 2026-08-01

Status: PROVED__EXACT_MATROID_INTERSECTION_DICHOTOMY

## 1. Motivation

The preceding reserve-Hall attack first chooses one root in each outer
endpoint set \(Y_\gamma\), represents its \(t_\gamma-1\) defect units by
the resulting star, and only then asks for distinct missing-edge charges.
That order is unnecessarily rigid. The numerical defect
\(t_\gamma-1\) is the rank of a spanning tree on \(Y_\gamma\), so the
tree and the missing-edge charges should be selected simultaneously.

This note gives the exact min-max theorem for that simultaneous choice.
It strictly contains every fixed-root Hall test and replaces an arbitrary
deficient token set by a canonical family of partitions of the colour
endpoint sets.

## 2. Frozen setup and reserves

Retain the centered maximum-degree setup of the ninth attack. For every
colour \(\gamma\), let \(Y_\gamma\subseteq B\) be its outer endpoint set.
Edges of one colour form an induced matching, hence every pair
\[
e\in\binom{Y_\gamma}{2}
\]
is a missing edge of \(G[B]\).

For a missing pair \(e=\{b,c\}\subseteq B\), define its charge reserve
\(\mathcal R(e)\subseteq\overline E(G[B])\) by
\[
\mathcal R(e)=
\begin{cases}
\{e\},&\text{if the shore graph of \(e\) is nonempty},\\[2mm]
\mathcal K(e),&\text{if the shore graph of \(e\) is empty},
\end{cases}
\tag{1}
\]
where \(\mathcal K(e)\) is the star-plus-neighbourhood reserve from the
ninth attack. Reserve validity proves
\[
\mathcal R(e)\subseteq\overline E(G[B])
\tag{2}
\]
in both cases.

Put
\[
D_B=\sum_\gamma (|Y_\gamma|-1)_+.
\tag{3}
\]

## 3. Exact partition criterion

For each \(\gamma\), let \(\Pi_\gamma\) be a partition of \(Y_\gamma\).
Write
\[
\operatorname{Cross}(\Pi_\gamma)
=\{\{b,c\}\subseteq Y_\gamma:
b,c\text{ lie in distinct blocks of }\Pi_\gamma\}.
\tag{4}
\]
The partition debt is
\[
d(\Pi)=\sum_\gamma(|\Pi_\gamma|-1).
\tag{5}
\]
Empty and singleton endpoint sets contribute zero.

### Theorem 3.1 (adaptive forest-reserve min-max theorem)

The following are equivalent.

1. For every colour \(\gamma\), one can choose a spanning tree
   \(T_\gamma\) on \(Y_\gamma\), and for every
   \(e\in E(T_\gamma)\) one can choose a charge
   \(f_{\gamma,e}\in\mathcal R(e)\), so that all chosen charge edges are
   pairwise distinct.
2. For every family of partitions \(\Pi=(\Pi_\gamma)_\gamma\),
   \[
   \boxed{
   \left|
   \bigcup_\gamma
   \bigcup_{e\in\operatorname{Cross}(\Pi_\gamma)}
   \mathcal R(e)
   \right|
   \ge
   \sum_\gamma(|\Pi_\gamma|-1).
   }
   \tag{6}
   \]

Consequently, if (6) holds then
\[
\boxed{D_B\le M_B.}
\tag{7}
\]
If (6) fails, the violating partitions give the exact canonical
obstruction
\[
\boxed{
\left|
\bigcup_\gamma
\bigcup_{e\in\operatorname{Cross}(\Pi_\gamma)}
\mathcal R(e)
\right|
<
d(\Pi).
}
\tag{8}
\]

#### Proof

Form a ground set of labelled charge triples
\[
\Omega=
\{(\gamma,e,f):
e\in\binom{Y_\gamma}{2},\ f\in\mathcal R(e)\}.
\tag{9}
\]

Let \(\mathsf M\) be the direct sum, over colours \(\gamma\), of the
graphic matroid on the complete graph with vertex set \(Y_\gamma\).
The triples with the same pair \((\gamma,e)\) are parallel copies of
the graphic edge \(e\). Thus a set is independent in \(\mathsf M\)
exactly when, for every colour, its projected base pairs form a forest.

Let \(\mathsf P\) be the partition matroid in which triples with the same
charge coordinate \(f\) form one class of capacity one. Independence in
\(\mathsf P\) means that no missing edge is charged twice.

The total rank of \(\mathsf M\) is \(D_B\). By the matroid-intersection
min-max theorem, a common independent set of size \(D_B\) exists if and
only if, for every \(Z\subseteq\Omega\),
\[
r_{\mathsf M}(Z)+r_{\mathsf P}(\Omega\setminus Z)\ge D_B.
\tag{10}
\]

For fixed \(Z\), let \(\Pi_\gamma(Z)\) be the component partition of the
graph on \(Y_\gamma\) whose edges are those \(e\) for which
\((\gamma,e,f)\in Z\) for at least one \(f\). Then
\[
r_{\mathsf M}(Z)
=\sum_\gamma\bigl(|Y_\gamma|-|\Pi_\gamma(Z)|\bigr).
\tag{11}
\]

Enlarge \(Z\) to \(Z^\star\) by adding every triple
\((\gamma,e,f)\) whose endpoints lie in one block of
\(\Pi_\gamma(Z)\). This does not change (11), while it can only decrease
\(r_{\mathsf P}(\Omega\setminus Z)\). Therefore it is enough in (10) to
consider these saturated sets. For the saturated set determined by a
partition family \(\Pi\),
\[
r_{\mathsf P}(\Omega\setminus Z^\star)
=
\left|
\bigcup_\gamma
\bigcup_{e\in\operatorname{Cross}(\Pi_\gamma)}
\mathcal R(e)
\right|.
\tag{12}
\]

Finally,
\[
D_B-r_{\mathsf M}(Z^\star)
=\sum_\gamma(|\Pi_\gamma|-1)=d(\Pi).
\tag{13}
\]
Substituting (12)--(13) into (10) gives exactly (6).

A common independent set of size \(D_B\) projects, for every colour, to
an acyclic graph with \(|Y_\gamma|-1\) edges, hence a spanning tree.
The partition-matroid condition makes all charge coordinates distinct.
By (2), these are distinct missing edges of \(G[B]\), proving (7).
\(\square\)

## 4. Relation to the fixed-root theorem

Choosing a root \(r_\gamma\in Y_\gamma\) in advance restricts
\(T_\gamma\) to one particular star. The ninth-stage Hall graph asks only
whether charges can be assigned after this restriction. Theorem 3.1
allows every tree and every charge to be chosen together. Hence:

- any successful fixed-root Hall matching is a feasible adaptive
  forest-reserve solution;
- failure for one or even every fixed root is not yet a failure of (6);
- genuine failure is witnessed by the partition obstruction (8), which
  is independent of arbitrary root choices.

For the base-only reserve \(\mathcal R(e)=\{e\}\), (6) is the exact
edge-disjoint spanning-tree packing criterion for the family
\((Y_\gamma)_\gamma\). The enlarged zero-shore reserves can only make the
left side larger.

The improvement over fixed roots is strict already for one abstract
four-vertex colour. Give the six pairs the reserves
\[
 R_{12}=\{a\},\quad R_{13}=\{b\},\quad R_{14}=\{a\},
 \qquad
 R_{23}=\{b\},\quad R_{24}=\{a\},\quad R_{34}=\{c\}.
\tag{16}
\]
Every rooted star has two edges whose reserve is the same singleton, so
none has a system of distinct representatives. The path
\(12,23,34\), however, has the distinct charges \(a,b,c\). Thus an
adaptive tree can succeed even when every possible fixed-root test
fails. This example certifies strictness for the abstract reserve
selection theorem; it is not asserted to arise from a BCM witness.

## 5. Maximum-witness interface

If (6) holds and the outer-\(A\) residue satisfies
\[
R_A\le S_m,
\tag{14}
\]
then
\[
D_A=R_A+D_B\le S_m+M_B,
\tag{15}
\]
so the maximum-degree BCM branch closes. In particular it closes whenever
all repeated good colours are outer-\(B\) supported.

If the branch remains hard after this theorem, it supplies partitions
\(\Pi_\gamma\) whose many cross-block zero-shore pairs have an overlapping
union of star-plus-neighbourhood reserves smaller than their total
component debt. This is strictly more structured than the arbitrary
token subfamily in the fixed-root Hall certificate.

## 6. Scope firewall

The adaptive forest-reserve theorem is an exact all-parameter
combinatorial theorem. It does not prove that condition (6) always holds
under the full BCM contract, and it does not control \(R_A\) without
additional input. Erdős #809 remains open.

## 7. Independent finite guard

`verify_adaptive_forest_reserve.py` directly enumerates spanning trees,
charge matchings, and all partition families. It confirms the min--max
equivalence on 100 exhaustive tiny reserve systems and 1,000
deterministically generated systems, checks the strict example (16),
and recovers the base-only packing thresholds for two versus three
spanning trees of \(K_4\) and \(K_5\). These computations audit the
formalization; they are not used as a proof of Theorem 3.1.
