# Erdős #809 — rigidity of a minimal adaptive-reserve obstruction

Date: 2026-08-01

Status: `PROVED__EXACT_CRITICAL_OBSTRUCTION_AND_ZERO_SHORE_CONCENTRATION`

## 1. Setup

Use the reserve system and notation of
`ADAPTIVE_FOREST_RESERVE_THEOREM.md`.  For a family of partitions
\(\Pi=(\Pi_\gamma)_\gamma\), put
\[
 d(\Pi)=\sum_\gamma (|\Pi_\gamma|-1)
\]
and
\[
 U(\Pi)=
 \bigcup_\gamma
 \bigcup_{e\in\operatorname{Cross}(\Pi_\gamma)}
 \mathcal R(e).
\tag{1}
\]
Partitions of empty or singleton endpoint sets contribute zero.  A
partition family is an **obstruction** when
\[
 |U(\Pi)|<d(\Pi).
\tag{2}
\]

For two distinct blocks \(P,Q\in\Pi_\gamma\), let
\(\Pi^{\gamma;P,Q}\) be obtained by merging \(P,Q\), and define the
reserve layer removed by that merge:
\[
 L_\gamma(P,Q)=
 U(\Pi)\setminus U(\Pi^{\gamma;P,Q}).
\tag{3}
\]

## 2. Critical-obstruction theorem

### Theorem 2.1

If the adaptive partition criterion fails, choose an obstruction
\(\Pi\) with minimum positive debt. Then:

1. its deficiency is exactly one,
   \[
   \boxed{|U(\Pi)|=d(\Pi)-1};
   \tag{4}
   \]
2. every one-step block merge leaves the reserve union unchanged,
   \[
   \boxed{L_\gamma(P,Q)=\varnothing}
   \tag{5}
   \]
   for every \(\gamma\) and every two blocks \(P,Q\in\Pi_\gamma\);
3. consequently, every charge supplied by the pairs between \(P\) and
   \(Q\) is also supplied by an active pair not removed by their merge:
   \[
   \bigcup_{p\in P,\ q\in Q}\mathcal R(pq)
   \subseteq
   \bigcup_{\substack{(\eta,e):\\
             e\in\operatorname{Cross}(\Pi_\eta),\\
             (\eta,e)\notin\{(\gamma,pq):p\in P,q\in Q\}}}
             \mathcal R(e).
   \tag{6}
   \]

#### Proof

Write \(d=d(\Pi)\), \(u=|U(\Pi)|\).  Since \(\Pi\) is an
obstruction, \(u\le d-1\).  Merge any two blocks in any nontrivial
\(\Pi_\gamma\).  The new family has debt \(d-1\); by minimality of
\(d\), it is not an obstruction.  Hence, writing its union size as
\(u'\),
\[
 d-1\le u'\le u\le d-1.
\]
All three quantities are equal.  This proves (4), proves that the merge
loses no charge, and hence proves (5)--(6). \(\square\)

This says that a genuine failure may always be represented by a
unit-tight, completely merge-redundant object.  In particular, a
putative proof no longer has to control arbitrary deficient partition
families.

## 3. Repeated zero-shore mass

For the critical obstruction above, put
\[
 t_\gamma=|Y_\gamma|,\qquad k_\gamma=|\Pi_\gamma|,
\]
and let
\[
 X=\sum_\gamma
 |\operatorname{Cross}(\Pi_\gamma)|
\tag{7}
\]
be the number of active base-pair occurrences, counted with colour
multiplicity.  Let \(E_*\) be the set of distinct active base pairs and
let \(m_e\) be the number of active colour occurrences of \(e\).

The fixed-pair theorem says that \(m_e\le1\) whenever \(e\) has a
nonempty shore.  Therefore the entire repetition mass
\[
 \rho_0=\sum_{\substack{e\in E_*:\ e\text{ zero-shore}}}(m_e-1)
\tag{8}
\]
is supported on zero-shore pairs, and
\[
 \rho_0=X-|E_*|.
\tag{9}
\]

### Theorem 3.1 (quantitative zero-shore concentration)

Every critical obstruction satisfies
\[
\boxed{
 \rho_0\ge X-d(\Pi)+1
 \ge
 1+\sum_\gamma (k_\gamma-1)
 \left(t_\gamma-1-\frac{k_\gamma}{2}\right).
}
\tag{10}
\]
In particular, at least one active pair is zero-shore and is repeated
across colours.

#### Proof

Every reserve contains its base pair, so
\(E_*\subseteq U(\Pi)\).  Theorem 2.1 gives
\[
 |E_*|\le |U(\Pi)|=d(\Pi)-1.
\]
Together with (9), this proves the first inequality in (10).

For a partition of \(t\) points into \(k\) nonempty blocks, the number
of cross pairs is minimized by block sizes \(t-k+1,1,\ldots,1\), and
therefore is at least
\[
 \binom t2-\binom{t-k+1}{2}
 =(k-1)\left(t-\frac{k}{2}\right).
\tag{11}
\]
Sum (11) over the colours and subtract
\(d(\Pi)=\sum_\gamma(k_\gamma-1)\).  This gives the second inequality
in (10).  Its right side is at least one because \(t_\gamma\ge
k_\gamma\) for every active partition. \(\square\)

### Corollary 3.2 (one highly congested exceptional pair)

An obstruction cannot have \(d(\Pi)=1\): its unique nontrivial
two-block partition has a cross pair, whose nonempty reserve already
has size at least one. Hence \(d(\Pi)\ge2\). Let \(z\) be the number
of distinct active zero-shore pairs. Since
\(z\le |E_*|\le d(\Pi)-1\), some zero-shore pair occurs in at least
\[
\boxed{
 1+\left\lceil
 \frac{1+
 \sum_\gamma (k_\gamma-1)
 (t_\gamma-1-k_\gamma/2)}{d(\Pi)-1}
 \right\rceil
}
\tag{12}
\]
active colours.  If this number is \(h\), the quadratic colour-rectangle
lemma from the fifth attack gives
\[
\boxed{M_A\ge h^2.}
\tag{13}
\]

#### Proof

Pigeonhole (10) over the \(z\) zero-shore pairs and use
\(z\le d-1\).  A pair repeated with excess at least \(r\) has
multiplicity at least \(1+r\).  The bound (13) is exactly the proved
zero-shore colour-rectangle theorem. \(\square\)

## 4. Dependency consequence

Fix an active pair \(e=pq\) lying between blocks \(P,Q\) of colour
\(\gamma\).  Its base charge \(e\) belongs to \(\mathcal R(e)\).
Equation (6) shows that after the \(P,Q\) layer is deleted, \(e\) is
still supplied by another active occurrence.

If \(e\) has a nonempty shore, the same base pair cannot occur in a
second colour.  Also a different nonempty-shore pair has singleton
reserve and cannot supply \(e\).  Hence:

> Every active nonempty-shore pair in a critical obstruction belongs to
> the enlarged reserve \(\mathcal K(e')\) of some active zero-shore pair
> \(e'\ne e\).

Thus the exceptional zero-shore pairs do not merely carry the repeated
base-pair mass in (10); their enlarged reserves must cover every
ordinary active base pair as well.  This is an exact synchronization
condition suitable for the next structural attack.

## 5. Scope firewall

Theorems 2.1 and 3.1 are all-parameter consequences of failure of the
adaptive-reserve criterion.  They do not prove that such an obstruction
cannot occur under the BCM contract, and (13) need not by itself fit
inside the available slack.  The maximum-degree branch and Erdős #809
remain open.

The independent enumerator in `verify_adaptive_forest_reserve.py`
reconstructed and checked the unit-deficiency and merge-redundancy
conclusions on 164 seeded random obstructed reserve systems. This is a
finite guard only; the proof above is the universal justification.
