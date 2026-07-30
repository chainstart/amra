# A nilpotency-class barrier for the odd-prime KOU problem

Date: 2026-07-29

## Main obstruction

Let \(p\) be an odd prime and let \(G\) be a group of exponent dividing
\(p^2\) and nilpotency class at most \(p\).  Then
\[
  [x^p,y^p]=1\qquad(x,y\in G).                     \tag{1}
\]
Consequently the raw value set
\[
  P_p(G)=\{g^p:g\in G\}
\]
is a commuting set.  If \(P_p(G)\) is a subgroup, then it is necessarily
abelian.

Thus any odd-prime counterexample to the KOU requirement must have
\[
  \operatorname{cl}(G)\geq p+1.                   \tag{2}
\]
For \(p=3\), every exponent-nine group of class at most three is ruled out.

The lower bound (2) is rigorous.  It is not yet proved to be the exact
minimum for a KOU counterexample.  The first Hall coefficients that are not
automatically divisible by \(p^2\) occur at weight \(p+1\), but exponent
relations may still force their values to vanish.

There is a separate, weaker threshold that does not impose closure of the
raw power-value set.  Let \(c_{\rm nc}(p)\) be the least nilpotency class of
an exponent-\(p^2\) group having two noncommuting \(p\)-th powers.  An
explicit unitriangular family below shows
\[
  p+1\ \leq\ c_{\rm nc}(p)\ \leq\ 2p.              \tag{3}
\]
Only the lower bound transfers to the KOU problem: the unitriangular witness
is not known to have a closed raw power-value set.

There is now a sharp refinement for metabelian groups.  If \(G''=1\), then
the conclusion \([x^p,y^p]=1\) holds throughout
\(\operatorname{cl}(G)<2p\).  The proof uses the
\(\mathbb Z[G/G']\)-module structure of \(G'\) and the exponent-\(p^2\)
relation to kill the Hall terms having only one factor of \(p\); see
`METABELIAN_2P_NILPOTENCY_BARRIER.md`.  This does not yet prove the same
bound for arbitrary groups.

## Hall-collection proof

Work first in the free nilpotent group on \(x,y\) of class \(p\), and collect
\([x^m,y^n]\) in Hall order.  Every factor is a basic commutator \(c\) that
contains at least one occurrence of \(x\) and at least one occurrence of
\(y\).  If \(c\) has \(r\) occurrences of \(x\) and \(s\) occurrences of
\(y\), then \(r+s\) is its weight.

The multivariable Hall-polynomial form of the collection process has the
following divisibility property: the exponent \(e_c(m,n)\) of \(c\) is an
integer linear combination of products
\[
  \binom{m}{i}\binom{n}{j},
  \qquad 1\leq i\leq r,\quad 1\leq j\leq s.        \tag{4}
\]
Terms of larger Hall weight may change the precise linear combination, but
not these bounds on \(i,j\).  This follows inductively because choosing an
\(i\)-fold \(x\)-position and a \(j\)-fold \(y\)-position is the only way a
commutator of bidegree at most \((r,s)\) is created during collection.

Now put \(m=n=p\).  If the weight satisfies
\[
  r+s\leq p,
\]
then \(1\leq r,s\leq p-1\), and every pair \(i,j\) occurring in (4) lies
between \(1\) and \(p-1\).  For prime \(p\),
\[
  p\mid\binom pk\qquad(1\leq k\leq p-1).
\]
Each product in (4), and therefore every \(e_c(p,p)\), is divisible by
\(p^2\).  In a group of exponent dividing \(p^2\), all collected factors are
trivial.  This proves (1).

The same calculation identifies the first place where this argument can
fail.  At weight \(p+1\), a commutator of bidegree \((p,1)\) can have a
coefficient involving
\[
  \binom pp\binom p1=p,
\]
and similarly for bidegree \((1,p)\).  These coefficients have
\(p\)-adic valuation one, not two.  Thus weight \(p+1\) is the first
collection-theoretic possibility, which proves the necessity of (2) but
does not by itself construct a group attaining equality.

An equivalent two-stage view starts by collecting
\[
 [x^p,y]
 \]
and then taking the commutator with \(y^p\).  All terms of total weight at
most \(p\) acquire two factors of \(p\): one from the \(x\)-collection and
one from the \(y\)-collection.  A term containing \(p\) copies of one
letter first loses one factor through \(\binom pp=1\), again at total
weight \(p+1\).

## Relation with regular \(p\)-groups

Every finite \(p\)-group of class strictly less than \(p\) is regular.
For normal subgroups of a regular \(p\)-group, the standard regular-power
identity gives
\[
 [G^p,G^p]=[G,G]^{p^2}.
\]
This is trivial when \(\exp(G)\mid p^2\), so regular-group theory already
proves (1) for class \(<p\).  The Hall-divisibility proof above includes the
borderline class \(p\), where regularity is no longer automatic.

The regularity comparison is supporting prior theory, not a novelty claim.
The class-\(p\) endpoint and its use as a KOU search filter are the relevant
refinement here.

## A universal class-\(2p\) witness

The lower bound is not vacuous.  Let
\[
  U=\operatorname{UT}_{2p+1}(\mathbb F_p).
\]
This group has nilpotency class \(2p\).  It has exponent \(p^2\): for every
strictly upper-triangular \(N\),
\[
  (I+N)^{p^2}=I+N^{p^2}=I,
\]
because \(N^{2p+1}=0\) and \(2p+1\leq p^2\) for odd \(p\); a Jordan block of
size \(p+1\) supplies an element of order \(p^2\).

Let
\[
 X=\sum_{i=1}^{p}E_{i,i+1},\qquad
 Y=\sum_{i=p+1}^{2p}E_{i,i+1},
\]
and put \(x=I+X\), \(y=I+Y\).  In characteristic \(p\),
\[
 x^p=I+X^p=I+E_{1,p+1},\qquad
 y^p=I+Y^p=I+E_{p+1,2p+1}.
\]
Their products differ by the nonzero matrix unit \(E_{1,2p+1}\):
\[
 x^py^p
 =I+E_{1,p+1}+E_{p+1,2p+1}+E_{1,2p+1},
\]
whereas
\[
 y^px^p
 =I+E_{1,p+1}+E_{p+1,2p+1}.
\]
Thus \([x^p,y^p]\ne1\).  This proves the upper bound in (3).

This witness only concerns noncommutativity of raw powers; it does not say
that the complete raw power-value set of \(U\) is a subgroup.  It is
therefore a sharp search-bound witness, not an odd-prime KOU counterexample.

## Exhaustive \(p=3\) evidence through order \(729\)

`validate_odd_kou_nilpotency_barrier.g` scans all 594 SmallGroups types of
orders
\[
  3,9,27,81,243,729.
\]
For every exponent-nine group it computes the complete cube-value set, the
subgroup it generates, whether that subgroup is abelian, whether the raw set
is closed, and the nilpotency class.  The exact rows are:

```text
ODD_KOU_CLASS|p=3|class=1|exp9=9|power_nonabelian=0|power_closed=9|closed_nonabelian=0|first_nonabelian=fail
ODD_KOU_CLASS|p=3|class=2|exp9=118|power_nonabelian=0|power_closed=118|closed_nonabelian=0|first_nonabelian=fail
ODD_KOU_CLASS|p=3|class=3|exp9=270|power_nonabelian=0|power_closed=155|closed_nonabelian=0|first_nonabelian=fail
ODD_KOU_CLASS|p=3|class=4|exp9=66|power_nonabelian=0|power_closed=30|closed_nonabelian=0|first_nonabelian=fail
ODD_KOU_SCAN|p=3|orders=3..729|groups=594|exp9=463|power_nonabelian=0|closed_nonabelian=0
DONE
```

The first three rows verify the theorem throughout the available range.
The class-four row goes one step beyond the theorem: all 66 available
class-\(p+1\) groups still have commuting cubes.  This disproves neither
the lower bound nor its possible sharpness, because larger class-four
groups are not covered.  It does show that simply moving to class \(p+1\)
is not enough at small order.

For \(p=3\), the unitriangular construction is
\(\operatorname{UT}_7(\mathbb F_3)\), of class six and exponent nine.
The displayed matrices give an exact symbolic witness of two noncommuting
cubes.

## Extended \(p=3\) evidence at order \(2187\)

An optional scan with the complete SmallGrp 1.5.4 order-\(3^7\) data checks
all 9,310 groups of order \(2187\).  Of these, 8,302 have exponent nine:
1,181 have class four, 26 have class five, and none has class six.  Every
one of their cube subgroups is abelian.  In all 26 class-five endpoint
cases the cube subgroup lies in \(Z_3(G)\).

This reaches the proposed endpoint \(2p-1=5\) for every group in that
bounded catalogue.  It remains finite evidence, not a general
class-five theorem.  The exact optional audit is
`validate_odd_kou_p3_order2187.g`.

## Search consequence

An odd-prime KOU search can safely discard every exponent-\(p^2\) candidate
of class at most \(p\), without enumerating its power values.  At \(p=3\),
the bounded catalogue also justifies deprioritizing class four at small
orders.  The mathematically unresolved range is:

- class \(p+1,\ldots,2p-1\), where no general obstruction or witness has
  yet been proved here outside the metabelian case;
- class at least \(2p\), where noncommuting raw powers exist, but closure of
  the full raw power set remains the decisive extra constraint.

This result narrows the search space.  It is not by itself a solution of the
odd-prime KOU problem and is not claimed to guarantee a Q1 publication.

## Literature dependency

The collection argument is based on P. Hall,
[“A contribution to the theory of groups of prime-power order”](https://doi.org/10.1112/plms/s2-36.1.29),
*Proceedings of the London Mathematical Society* (2) **36** (1934),
29--95, and the basic-commutator refinements in R. R. Struik,
[“On nilpotent products of cyclic groups”](https://doi.org/10.4153/CJM-1960-039-x),
*Canadian Journal of Mathematics* **12** (1960), 447--462.

For context at the regularity boundary, P. Moravec,
[“On the exponent semigroups of finite \(p\)-groups”](https://users.fmf.uni-lj.si/moravec/Papers/exprank3.pdf),
records that \(C_p\wr C_p\) has exponent \(p^2\) and class \(p\), and
discusses when power maps are endomorphisms in regular and maximal-class
groups.  These are prior power-structure results.  The present claim is the
specific pairwise-commutativity obstruction for raw \(p\)-th powers in
exponent-\(p^2\), class-at-most-\(p\) groups.
