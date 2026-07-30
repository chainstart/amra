# KOU-21.137 independent proof audit

Audit date: 2026-07-29

## Scope

An independent, read-only internal pass checked the mathematical arguments in
`THEOREM_DRAFT.md`, separately from the agents that developed the theorem and
the exhaustive enumeration.  The pass checked logical implications and
boundary hypotheses; it was not a journal referee report, a formal proof
assistant verification, or a novelty assessment.

## Result

After one substantive correction and several explicit justifications, the
core theorem package passed the audit:

1. the complete square-value formula in \(A\wr C_2\);
2. the if-and-only-if subgroup criterion and fiber-product description;
3. the identification with the derived subgroup for seeds with a proper
   square set;
4. the Frattini identification under the additional finite 2-group
   hypothesis;
5. the central Camina-special seed corollary;
6. the extraspecial and
   \(\operatorname{UT}_3(\mathbb F_{2^m})\) families.

The exhaustive minimum-order statement remains a computer-assisted result
supported by the separate certificate and computational audit.

## Substantive issue found and corrected

An earlier draft claimed
\[
  \operatorname{Sq}(A\wr C_2)=\Phi(A\wr C_2)
\]
for every finite seed satisfying the proper-square criterion.  This is false
outside finite 2-groups.  The audit supplied the test case \(A=S_3\):
\[
  P_2(S_3)=A_3=S_3',
\]
and the wreath criterion holds.  In \(W=S_3\wr C_2\),
\[
  |\operatorname{Sq}(W)|=|W'|=18,
  \qquad
  \Phi(W)=1.
\]

The draft now states the correct split:

- for arbitrary finite \(A\) with proper \(P_2(A)\),
  \(\operatorname{Sq}(W)=W'\);
- for finite 2-group seeds,
  \(\operatorname{Sq}(W)=W'=\Phi(W)\).

The GAP regression suite independently includes finite non-2-group seeds, so
the repaired statement is checked against the same boundary.

## Justifications made explicit

The audit requested, and the theorem draft now records, the following steps.

- A word-value set is conjugacy invariant.  Hence, once \(P_2(A)\) is known
  to be a subgroup, it is normal; this legitimizes the quotient \(A/P_2(A)\)
  in the converse direction of the wreath criterion.
- In the proper case the criterion forces \(A'=P_2(A)\): one inclusion comes
  from the elementary abelian quotient, and the reverse inclusion comes from
  \(xp\in x^A\) for \(x\notin P_2(A)\).
- Under the central seed assumptions, a central element outside \(N\) would
  have a singleton conjugacy class, contradicting \(z^A=zN\).  This proves
  \(Z(A)=N\); together with the proper-case theorem and
  \(\Phi(A)=A^2A'\), it gives
  \(N=A'=Z(A)=\Phi(A)\).
- For \(\operatorname{UT}_3(\mathbb F_{2^m})\), the upper exponent bound from
  the square formula is attained: \(u(1,1,0)^2=u(0,0,1)\ne1\).
- The degenerate assertion \(P_2(A)=A\) exactly for finite groups of odd
  order follows from bijectivity of the square map in odd order and, in the
  reverse direction, the absence of involutions.

## Post-audit hypothesis reduction

A subsequent dependency check found that the first three results do not use
finiteness.  For an arbitrary group \(A\), the base of \(A\wr C_2\) still has
exactly two factors, the fiber-product argument is purely algebraic,
\(A/P_2(A)\) has exponent two once \(P_2(A)\) is a subgroup, and the standard
abelianization calculation gives
\[
  (A\wr C_2)'=\{(x,y)\in A^2:xy\in A'\}.
\]
Thus Lemma 1, Theorem 2, \(P_2(A)=A'\) in the proper case, and
\(P_2(A\wr C_2)=(A\wr C_2)'\) are now stated for arbitrary groups.
Finiteness remains essential only in the odd-order characterization of a
surjective square map, the finite 2-group Frattini formula used here, and the
KOU/minimum-order applications.

## Remaining limits

This audit does not certify literature priority.  In particular, Mann (2005),
Theorem 16 remains inaccessible in authorized full text and is a documented
pre-submission blocker in `LITERATURE_AUDIT.md`.  The later
`validate_order128_structure.g` audit upgrades the catalogue list to a common
central quotient and central-lift classification, but that subsequent
computer-assisted classification was not part of this proof-only pass.

## Semi-extraspecial strengthening audit

A later pass audited the assertion that every finite
semi-extraspecial 2-group \(A\) satisfies
\[
  P_2(A)=Z(A).
\]
The proof passed the following checks.

1. Since \(A\) is special, \(Z(A)\) and \(A/Z(A)\) are elementary abelian,
   \(x^2\in Z(A)\), and \(q(xZ)=x^2\) is well defined.  Its polar form is the
   commutator bimap.
2. For every nonzero \(\lambda\in Z(A)^*\), the quotient
   \(A/\ker\lambda\) is extraspecial.  Hence the polar form of
   \(\lambda\circ q\) is nondegenerate.
3. If \(\dim A/Z(A)=2n\) and \(\dim Z(A)=m\), the Pfaffian of the scalar
   commutator pencil is a homogeneous polynomial of degree \(n\) whose only
   zero over \(\mathbb F_2^m\) is the origin.  Chevalley--Warning therefore
   rules out \(n<m\).  This is a self-contained recovery of the already known
   Beisiegel bound \(m\leq n\), not a novelty claim.
4. For a nondegenerate quadratic form \(Q\) on a \(2n\)-dimensional
   \(\mathbb F_2\)-space, the identity
   \[
     \left(\sum_v(-1)^{Q(v)}\right)^2=2^{2n}
   \]
   follows by a change of variables and orthogonality of the nontrivial
   linear characters.  Thus every nonzero Fourier coefficient of the
   vector-valued \(q\) has absolute value \(2^n\).
5. Fourier inversion then gives every fiber the uniform lower bound
   \[
     |q^{-1}(z)|
       \geq2^{n-m}(2^n-2^m+1)>0.
   \]
   No assumption on the signs of the individual Gauss sums is made.

The audit subsequently identified the correct prior framework.  The
derivative
\[
  D_aq(v)=q(v+a)+q(v)=q(a)+b(v,a)
\]
is balanced for every \(a\ne0\), so \(q\) is a perfect nonlinear/vectorial
Boolean bent function.  Nyberg's theorem already gives the dimension bound,
and Kölsch--Polujan, Theorem 2.4 and Corollary 2.7, already give precisely the
fiber bound and surjectivity above.  The five steps remain a valid
self-contained proof, but they do not support novelty claims for those
conclusions.  The potentially new point is the group-theory identification
and its application to the wreath criterion.

The converse classification was checked separately.  If \(A\) is a finite
nonabelian 2-group and \(P_2(A\wr C_2)\) is a subgroup, the wreath criterion
makes \(A\) a Camina group and gives \(P_2(A)=A'\).  Macdonald's prior theorem
that Camina 2-groups have class two then applies.  The Camina property forces
\(Z(A)=A'\), while \(P_2(A)=A'\) gives \(\Phi(A)=A'\).  Directly quotienting
by each maximal \(N<Z(A)\) shows that \(A/N\) is extraspecial.  Hence
\[
  P_2(A\wr C_2)\leq A\wr C_2
  \quad\Longleftrightarrow\quad
  A\text{ is semi-extraspecial}
\]
for finite nonabelian 2-group seeds.  Verardi's prior equivalence between
class-two Camina \(p\)-groups and semi-extraspecial \(p\)-groups provides an
independent literature cross-check of the last step.

The assertion-heavy GAP script
`validate_semiextraspecial_square_surjectivity.g` checks both definitions of
semi-extraspecial independently and scans all 2665 SmallGroups types of
orders \(8,16,32,64,128\).  It finds exactly eleven types:
\[
\begin{array}{c|c}
|A|&\text{SmallGroups IDs}\\\hline
8&3,4\\
32&49,50\\
64&241,242,243,244,245\\
128&2326,2327,
\end{array}
\]
and verifies square surjectivity and the Fourier lower bound in every case.
This finite scan is corroboration, not part of the proof.

## Odd-prime diagonal-quotient no-go audit

The later odd-prime obstruction was checked for an arbitrary odd prime
\(p\), not only for the computational case \(p=3\).

1. For each \(1\leq k<p\), the \(p\)-th power of an element of the
   \(A^pt^k\) coset has coordinate products read cyclically with step \(k\).
   Since \(k\) is invertible modulo \(p\), these are cyclic rotations using
   every base coordinate once.
2. Given \(x\in A\) and arbitrary conjugators
   \(g_1,\ldots,g_{p-1}\), the consecutive factors
   \(g_i^{-1}g_{i+1}\), followed by \(g_{p-1}^{-1}x\), recover the tuple
   \((x,g_1^{-1}xg_1,\ldots,g_{p-1}^{-1}xg_{p-1})\).
   Thus every nontrivial top coset contributes exactly
   \(\bigcup_C C^p\), with no hidden tuple constraint.
3. If \(U=P_p(A)\) is a central subgroup, the intersection of \(U^p\)
   with that union is precisely \(\Delta U\).  Comparing independently
   chosen conjugates with diagonal tuples generates \((A')^p\), proving
   \[
     |P_p(A\wr C_p)|=|U|^p+\sum_C|C|^p-|U|,
     \qquad
     |\langle P_p(A\wr C_p)\rangle|
       =|A|\,|UA'|^{p-1}.
   \]
4. Under \(U\leq Z(A)\cap A'\) and \(U<A'\), every class size is at most
   \(d=|A'|\), while the central singleton classes give the strict moment
   deficit
   \[
     |A|d^{p-1}-\sum_C|C|^p
       \geq |U|(d^{p-1}-1)
       \geq p^{p-1}|U|^p-|U|
       >|U|^p-|U|.
   \]
   This contradicts the equality forced by closure.
5. The value set is invariant under the free action of \(\Delta U\).
   Therefore both its size and its generated-subgroup order divide by
   \(|U|\) in the quotient, proving that the diagonal quotient preserves
   closure or nonclosure exactly.

The proof is algebraic apart from finiteness used in the counting and
\(p\)-group index bound.  The SmallGroups scan at \(p=3\) is a regression
check, not part of the theorem.

## Complete finite-seed classification audit

The five-class theorem was checked branch by branch.

- The proper-square wreath criterion gives \(P_2(A)=A'\), the Camina
  condition, and exponent two for \(A/A'\).
- In the Camina \(p\)-group branch, a nontrivial abelianization of exponent
  two forces \(p=2\); Macdonald and Verardi then give precisely the
  nonabelian semi-extraspecial branch.  The abelian proper case gives exactly
  the elementary abelian 2-groups.
- For a cyclic Frobenius complement, the kernel equals \(A'\): the quotient
  is abelian, while the fixed-point-free generator gives
  \(K=[K,h]\le A'\).  The exponent-two abelianization forces the complement
  to be \(C_2\).  Its involution inverts the kernel, which is therefore
  abelian of odd order.
- For a quaternion complement, the central involution similarly inverts the
  abelian odd-order kernel, and
  \(A'=K\rtimes\langle z\rangle\).  For every order-four \(h\),
  \((1-h)(1+h)=2\) on \(K\), so \(1+h\) is invertible and squares cover
  \(Kz\).  This proves \(P_2(A)=A'\).
- In the last branch, \(1-h\) also conjugates every \(kh\) to \(h\), and
  \(C_A(h)=\langle h\rangle\).  The resulting class size is
  \(2|K|=|A'|\), which proves the Camina coset condition directly.

The literature dependency was corrected to account for the erratum to
Lewis's 2014 proof and the corrected Isaacs--Lewis 2015 quaternion argument.
The theorem is a synthesis with prior Camina/Frobenius classification, not a
new classification of Camina groups.

## Central-power criterion and exponent-lowering quotient audit

The closure criterion was subsequently strengthened to remove both
centrality and finiteness.  For the raw set \(Q=P_p(A)\), put
\(V=\langle Q\rangle A'\).  The audit checked
\[
 P_p(A\wr C_p)=Q^p\cup\bigcup_C C^p,\qquad
 \langle P_p(A\wr C_p)\rangle=\Delta A\,V^p.
\]
Their coordinate-axis intersections are \(Q\) and \(V\), respectively.
Thus closure forces \(Q=V\), making the raw value set a subgroup containing
\(A'\).  In the proper case the mixed diagonal tuples force
\(Q=A'\) and the Camina condition.  The converse is exactly the fiber
product over \(A/A'\).  The degenerate \(Q=A\) case was retained; for finite
groups it is equivalent to \(p\nmid|A|\).

Under the additional central hypothesis, the exponent and quotient
obstruction passed the following checks.

1. The coordinate-axis intersection of the value set is \(U\), while that of
   its generated subgroup is \(UA'\).  Equality under closure gives
   \(A'\le U\).
2. When \(U<A\), independently variable tuples
   \((x,xu_1,\ldots,xu_{p-1})\) force \(x^A=xU\), and hence \(U\le A'\).
   The omitted \(U=A\) case was restored explicitly; without it the theorem
   would be false for finite abelian \(p'\)-groups.
3. Conversely, \(U=A'\) plus the Camina coset condition makes the value set
   exactly the fiber product over \(A/U\).
4. In the exponent-\(p^2\) positive case, centrality makes
   \(H\cong A\times U^{p-1}\), and a direct commutator calculation gives
   \(H'=\Delta U\).
5. If \(\exp(W/N)\le p^2\), the elements
   \(x_a=(a,1,\ldots,1)t\) satisfy
   \(x_a^{p^2}=\Delta(a^p)\), forcing \(\Delta U\le N\).
   Epimorphisms carry word-value sets onto word-value sets, so
   \(P_p(W/N)=HN/N\), whose derived subgroup is trivial.

This proves the quotient obstruction for every normal \(N\), not only for
the diagonal quotient.

## All-prime finite-seed classification audit

The unrestricted criterion permits the finite classification to be repeated
for an arbitrary fixed prime \(p\).  The branch audit found:

- \(P_p(A)=A\) is equivalent to \(p\nmid|A|\);
- the abelian proper case is exactly a nontrivial elementary abelian
  \(p\)-group;
- a Camina \(q\)-group branch forces \(q=p\);
- class-three Camina \(p\)-groups are impossible because the prior theorem
  \(\exp(A/A_3)=p\) puts all \(p\)-th powers in \(A_3<A'\);
- the remaining \(p\)-group branch is semi-extraspecial of class two, with
  the additional exact requirement \(P_p(A)=A'\);
- a cyclic Frobenius complement must be \(C_p\), and its kernel is exactly
  the \(p\)-power-value set because the kernel has order coprime to \(p\);
- the quaternion complement has abelianization of exponent two and therefore
  occurs only for \(p=2\).

The audit explicitly rejected the tempting but false assertion that the
kernel in \(K\rtimes C_p\) must be abelian for odd \(p\).  That conclusion is
special to the fixed-point-free involution at \(p=2\).

Two infinite-family checks make the odd branches concrete.

1. If \(q\equiv1\pmod p\), \(p\) is odd, and \(\lambda\in\mathbb F_q^*\)
   has order \(p\), then
   \[
     (a,b,c)\mapsto(\lambda a,\lambda b,\lambda^2c)
   \]
   is an order-\(p\) automorphism of
   \(\operatorname{UT}_3(\mathbb F_q)\).  For every \(1\le i<p\), both
   \(\lambda^i\) and \(\lambda^{2i}\) differ from one, so the action is
   fixed-point-free.  The kernel is nonabelian, and the resulting
   semidirect product lies in the cyclic Frobenius branch.  The case
   \((p,q)=(3,7)\) is additionally checked by complete enumeration in
   `test_general_prime_nonabelian_kernel.py`.
2. For odd \(p\), the central product of one extraspecial order-\(p^3\)
   group of exponent \(p^2\) with any number of extraspecial exponent-\(p\)
   factors is extraspecial of exponent \(p^2\).  In the presentation in
   `GENERAL_PRIME_FINITE_CLASSIFICATION.md`, every \(p\)-th power equals
   \(z^{a_1}\), so the raw power set is exactly the order-\(p\) derived
   subgroup.  This verifies the power-surjective semi-extraspecial branch
   for every odd \(p\) and every extraspecial rank.  Its first case
   \((p,n)=(3,1)\) is the exponent-nine seed already checked in
   `validate_odd_wreath_p3.g`.

## Structural-position audit

In the positive proper case, set \(B=A/A'\), \(W=A\wr C_p\), and
\(H=P_p(W)\).  The fiber-product formula identifies
\[
 H/(A')^p=\Delta B.
\]
An independent abelianization calculation sends
\[
 (a_0,\ldots,a_{p-1})t^j
 \longmapsto
 \left(\sum_i a_iA',t^j\right)\in B\times C_p.
\]
Its kernel is the inverse image of the augmentation subspace
\(\ker(\Sigma:B^p\to B)\).  Base commutators give \((A')^p\), while
base--top commutators give every cyclic difference tuple, and those tuples
fill \(\ker\Sigma\).  Thus the kernel is exactly \(W'\), not merely an
upper bound for it.

Since \(B\) has exponent \(p\), \(\Delta B\leq\ker\Sigma\), yielding
\[
 H\leq W',\qquad [W':H]=|B|^{p-2}.
\]
For a finite \(p\)-group seed, the raw power values already form \(H\), so
\(W^p=H\leq W'\) and the standard formula
\(\Phi(W)=W^pW'\) gives \(\Phi(W)=W'\).  At \(p=2\), the diagonal and
augmentation subspaces coincide; at odd \(p\), their quotient has order
\(|B|^{p-2}\).

The \(p=3\) GAP audit checks both \(A=C_3\) and the extraspecial order-27,
exponent-nine seed.  It obtains respectively
\[
 (|B|,|H|,|W'|,|\Phi(W)|)=(3,3,9,9)
\]
and
\[
 (9,243,2187,2187),
\]
exactly matching the index formula.

## Odd-\(p\) nilpotency-barrier audit

Let \(G\) have exponent dividing \(p^2\), with \(p\) odd.  In the Hall
collection of \([x^p,y^p]\), a basic commutator of bidegree \((r,s)\)
contains both letters.  If its total weight is at most \(p\), then
\(1\le r,s\le p-1\).  Its Hall-polynomial coefficient is an integer
combination of
\[
 \binom pi\binom pj,\qquad
 1\le i\le r,\quad1\le j\le s,
\]
and every such product is divisible by \(p^2\).  Thus class at most \(p\)
forces \([x^p,y^p]=1\).  This independently agrees with regular-\(p\)-group
theory for class \(<p\) and extends the conclusion to the non-automatically
regular endpoint class \(p\).

At weight \(p+1\), bidegrees \((p,1)\) and \((1,p)\) introduce the
coefficient \(\binom pp\binom p1=p\).  Hence the collection proof gives the
rigorous necessary bound \(\operatorname{cl}(G)\ge p+1\), but it does not
prove existence at equality.  This distinction is explicit in the theorem
file.

For the weaker problem of merely obtaining two noncommuting raw powers, the
opposite bound is witnessed by
\(\operatorname{UT}_{2p+1}(\mathbb F_p)\), of exponent \(p^2\) and class
\(2p\).  Two length-\(p\) Jordan strings meeting at one endpoint have
\(p\)-th powers \(I+E_{1,p+1}\) and \(I+E_{p+1,2p+1}\), whose products
differ by \(E_{1,2p+1}\).  Thus, if \(c_{\rm nc}(p)\) denotes the minimum
class for noncommuting raw \(p\)-th powers (without the KOU closure
condition), the current rigorous window is
\[
 p+1\le c_{\rm nc}(p)\le2p,
\]
not the unsupported assertion that the lower endpoint is attained.  This
upper bound is not an upper bound for the least class of a KOU
counterexample.

For \(p=3\), the all-SmallGroups scan through order 729 finds no
noncommuting cubes among 463 exponent-nine groups.  It covers 270 class-three
groups and 66 class-four groups; the latter are evidence beyond the theorem
but not a proof for all groups of class four.

The later metabelian refinement was separately checked at the level of its
three essential module claims.  With \(A=G'\) and
\(R=\mathbb Z[G/G']\), metabelianity makes \(A\) an \(R\)-module and gives
\(A\Delta^r\leq\gamma_{r+2}(G)\).  The norm identity
\((ag)^{p^2}=1\) yields
\(a\sigma_{p^2}(\bar g)=0\).  In degrees below \(2p-2\), Kummer/Lucas
valuation leaves only
\(\binom{p^2}{p}=pu\) modulo \(p^2\), proving
\(pa(\bar g-1)^{p-1}=0\).  Finally the metabelian formula for
\([x^p,y^p]\) is a product of the two norm operators.  Its lower terms have
two factors of \(p\), its two edge families are killed by the preceding
one-variable relation, and its corner has augmentation degree \(2p-2\).
This validates the class-\((2p-1)\) endpoint for metabelian groups.

No step in that proof kills a residual element of \(G''\) in an arbitrary
group.  Accordingly, the unrestricted class-\((2p-1)\) statement remains
labelled a candidate rather than a theorem.  The complete order-\(2187\)
scan (8,302 exponent-nine groups, including 26 of class five) is supporting
evidence only.

## Exponent-\(p\) wreath all-quotients audit

The later all-quotients theorem for a nonabelian exponent-\(p\)
semi-extraspecial seed \(A\) was checked independently.  With
\(U=A'=Z(A)\), \(W=A\wr C_p\), \(S=P_p(W)\),
\(H=\langle S\rangle\), and \(K=U^p\), the critical points are:

1. The exact conjugacy-class formula gives
   \[
   S=(H\setminus K)\cup\Delta U,\qquad
   H=\Delta A\,K,\qquad H'=\Delta U.
   \]
   This is equality of raw sets, not merely an equality after generation.
2. For \(N\trianglelefteq W\) and \(L=N\cap H\), closure of the image of
   \(S\) forces that image to be all of \(H/L\), because \(S\) generates
   \(H\).
3. If \(L\not\le K\), one element \(\Delta a\,k\in L\setminus K\) suffices:
   its commutators with \(\Delta A\) cover \(\Delta U\), by the defining
   semi-extraspecial commutator surjectivity.
4. If \(L\le K\), closure first gives \(K=L+\Delta U\).  No semisimple
   complement is used.  In the regular unipotent module
   \(K\cong U\otimes\mathbb F_p[z]/(z^p)\), this equality makes \(K/L\)
   top-fixed, hence \(zK\le L\), and therefore
   \(\Delta U=z^{p-1}K\le L\).
5. In both cases \(\Delta U\le N\), and
   \((HN/N)'=\Delta U N/N=1\).  Thus closure in a quotient implies an
   abelian power subgroup.

The implication is not a converse.  In the complete \(p=3\) normal-subgroup
enumeration, 100 of 101 normal subgroups contain \(\Delta U\), while only
98 quotient images have closed cubes.  All 98 closed images contain
\(\Delta U\), and none is nonabelian.

## Directed \(p=3\) two-string audit

The later search was audited against the actual odd-prime condition.  If
\(H=P_3(G)\) is closed, Wilson failure means \(H'\nleq H^3\), not merely
\(H'\ne1\).  For the two-string unitriangular group the ambient exponent is
nine, so \(H^3=1\) and noncommutativity is equivalent to
non-powerfulness.

The section no-go has two independent logical parts.

1. Exact calculation gives
   \[
   Z(G)=\langle P_3(G)\rangle'
       =\langle[X^3,Y^3]\rangle\cong C_3.
   \]
   Every nontrivial normal subgroup of a finite \(p\)-group meets its
   centre, hence contains this complete cube-derived subgroup.  Thus every
   nontrivial normal quotient has abelian cube-generated subgroup; the
   trivial quotient retains the raw closure defect.
2. The four maximal subgroups cover every proper subgroup.  Exact cube
   enumeration in each maximal subgroup gives an abelian cube-generated
   group.  Therefore every proper subgroup, and every quotient of it, also
   has abelian cube-generated group.

For the associated two-string algebra \(J\), the ideal-quotient proof was
checked symbolically.  Since \(J^6=\langle A^3B^3\rangle\), killing
\(A^3B^3\) makes all cubes commute.  If it survives, assuming that
\((1+A^3)(1+B^3)\) is a cube modulo an ideal first forces the linear
\(A,B\) coefficients of a putative cube root to be one.  Multiplication of
the residual relation by \(A^2\) and \(B\) then forces \(A^3B^3\) into the
ideal, a contradiction.  This argument covers every two-sided ideal, not
only homogeneous or enumerated ideals.

The first general algebra-dimension bound uses only the power filtration.
Under the standing \(J^9=0\) algebra-group hypothesis, a non-powerful
closed cube set forces
\([J^3,J^3]\ne0\), hence \(J^6\ne0\) and
\(\dim J/J^2\ge2\).  Dimension seven would force
\(\dim J^3/J^4=1\) and \(J^7=0\), which makes \(J^3\) commutative.  Thus
\(\dim J\ge8\).  The next paragraph strengthens this human argument to
\(\dim J\ge9\).  No nilpotency-class lower bound is inferred from either
filtration statement.

At dimension eight the seven possible power-filtration profiles were
separated explicitly.  Five have \(J^7=0\) and
\(\dim J^3/J^4=1\), hence commuting \(J^3\).  The only length-six profile
with a two-dimensional third layer is impossible: associativity of the
maps
\[
 V\otimes V\to A_2,\qquad V A_2+A_2V\to A_3
\]
forces \(\dim A_3\le1\) whenever \(\dim A_2=1\).  The sole remaining
profile is \((2,1,1,1,1,1,1)\).  Its exact graded constraint system is
consistent, but the additional requirement \(A_3A_4\ne A_4A_3\) is
unsatisfiable.  More importantly, a later hand argument removes the same
profile: if all cubes lie in \(J^4\), their products vanish in \(J^8\);
otherwise \(a^3\notin J^4\) forces \(a^4\notin J^5\) through the
nonzero map \(A_3A_3\to A_6\), and the possible degree-seven commutator
is a multiple of \([a^3,a^4]=0\).  Hence the human boundary is
\(\dim J\ge9\); the finite solver audit is now only a regression check.

At dimension nine, positive-composition counting gives 29 profiles:
21 of length six, seven of length seven, and one of length eight.  In the
length-six branch, 15 profiles have \(d_3=1\) and hence
\([J^3,J^3]\le J^7=0\).  Five more contradict
\(d_2=1\Rightarrow d_3\le1\).  This leaves only
\((2,2,2,1,1,1)\).

The original solver exclusion of this last profile was audited to use
genuine closure consequences.  In the length-six setting, noncommuting
cubes must have independent degree-one roots.  Raw closure makes the
projected cube image \(q(A_1)\subseteq A_3\) additively closed; since it
contains two independent elements and both spaces have order nine, \(q\)
is bijective.
A stronger hand argument does not need this bijectivity or closure.
Let \(f_k\) be the \(k\)-fold multiplication tensor on \(A_1\).
One-dimensional \(A_4,A_5,A_6\) and associativity yield
\[
f_5=f_4\otimes r=\ell\otimes f_4,\qquad
f_6=f_5\otimes s=t\otimes f_5.
\]
The elementary tensor implication
\(T\otimes r=\ell\otimes T\Rightarrow
T=c\ell^{\otimes m}\) makes \(f_6\) symmetric.  Thus
\(x^3y^3=y^3x^3\) in \(A_6\); for arbitrary filtered roots the
commutator lies in \(J^7=0\).  The former bijectivity and circle-product
root constraints are not needed.

The eight deeper profiles were then checked independently.  One violates
\(d_2=1\Rightarrow d_3\le1\).  Four violate the necessary rank inequality
\[
 d_{i+j}\le d_i d_j,
\]
which follows from the surjection
\((J^i/J^{i+1})\otimes(J^j/J^{j+1})
\twoheadrightarrow J^{i+j}/J^{i+j+1}\).
For the final three profiles, the complete filtered multiplication table
was constrained by every associativity coordinate and every ordered layer
surjection.  The witness variables are arbitrary algebra elements \(a,b\),
and the asserted condition is exactly
\(a^3b^3\ne b^3a^3\).  All three systems are UNSAT, but hand proofs now
supersede them.  The two length-seven cases follow from the preceding
\(J^8=0\) cube lemma.  In the length-eight case, either all cubes lie in
\(J^4\), or the powers of one element form a filtration basis of \(J^2\),
making it commutative.  Thus the intermediate dimension-nine boundary
\(\dim J\ge10\) is human-checkable.  All four dimension-nine
solver certificates remain useful independent regressions but are no
longer proof premises.

The dimension-ten follow-up is also human-checkable.  Exponent nine means
\(J^9=0\), so only lengths six through eight are in scope and positive
composition gives 92 profiles; the old length-nine row was a scope error.
Besides the layer-surjection inequality, associativity gives the stronger
propagation rule
\[
d_i=1\Longrightarrow d_{i+1}\le1\qquad(i\ge2).
\]
The consecutive-tail tensor lemma removes
\((2,2,2,2,1,1)\), \((2,2,3,1,1,1)\),
\((2,3,2,1,1,1)\), and \((3,2,2,1,1,1)\).
The remaining length-seven profile is handled without dropping filtered
higher terms: after choosing \(t^4,\ldots,t^7\) as a tail basis and a
complement \(u\in J^3\), one has \(ut,tu\in J^5\), while
\((tu)t=t(ut)\) forces \(ut^3=t^3u\).  The two length-eight profiles have
a filtration basis \(t^3,\ldots,t^8\) of \(J^3\).  Thus every
dimension-ten profile has commuting cubes and
\[
\dim J\ge11.
\]
The historical 240-second timeout is no longer a search boundary.
`DIM11_SHARP_NONCOMMUTING_CUBE_WITNESS.md` independently shows that this
commutativity bound is sharp: its dimension-eleven algebra has
noncommuting cubes, but its raw cube set is explicitly not closed.

The closure-aware dimension-eleven continuation enumerates 246 profiles.
The quadratic normal-word bound \(d_2=2\Rightarrow d_3\le2\) and the
existing hand lemmas leave two.  An exhaustive independent audit of all
130 planes in \(\operatorname{Gr}(2,4)(\mathbb F_3)\) confirms that the
cubic quotient dimensions are distributed as \(48,48,34\) in
dimensions \(0,1,2\), so \((2,2,3,1,1,1,1)\) is impossible.  For the
length-six profile
\((2,2,2,2,2,1)\), closure makes the leading cube map
\(A_1\to A_3\) bijective and makes the kernel of the cube subgroup's
projection equal to \(J^6\).  Comparing the cubes of \(v\) and
\(v+z\), \(z\in J^3\), then yields
\[
v^2z+vzv+zv^2\in J^6
\quad\Longrightarrow\quad
v^3z=zv^3.
\]
Thus this profile cannot support closed noncommuting raw cubes.  The
profile-level remainder \((2,2,2,2,1,1,1)\) obeys the fail-closed
contract
\[
\dim Q=1
\quad\text{or}\quad
\bigl(\dim Q=2,\ K=1+J^6,\ |H|=81\bigr).
\]
In the second branch, the pure tail proves
\(L_w(z)=w^2z+wzw+zw^2=0\), so the cube descends to a bijection
\(P:A_2\to J^6\).  Closure also
forces
\(\operatorname{ad}_v^2(A_2)=0\) in \(A_4\) and
\(\operatorname{ad}_{A_2}^2(A_1)=0\) in \(A_5\).  The exact quadratic
lemma makes the viable graded quotient commutative.  Its quadratic
relation is neither a square (cube bijectivity fails) nor irreducible
(a degree-five relation would kill \(A_6\)); hence it is \(xy\).
The one-dimensional \(A_6\) forces one pure fifth-power chain to stop.
For its generator \(b\), filtered multiplication gives
\([b^2]\ne0\) and \(b^6=0\), contradicting
\(P([b^2])=(b^2)^3\).

In the \(\dim Q=1\) branch, the pure degree-seven tensor makes
\(A_3A_4=A_4A_3\), so \([J^3,J^4]\subseteq J^8=0\).
The kernel of \(H\to Q\) is then central and the quotient is cyclic,
forcing \(H\) abelian.  Thus both branches are excluded and the
closure-aware bound is
\[
\dim J\ge12.
\]
The earlier graded SAT result tested only a subset of the necessary
conditions and is superseded by this proof.

The dimension-twelve follow-up is deliberately weaker: an independent
positive-composition ledger applies the same proved filters to all 582
in-scope profiles and leaves eight necessary branch inputs.  The generalized
length-six fibre lemma, the filtered cross-relation commutator argument, and
the exact quadratic \(d_4\)-bound then exclude three, while the other five
receive strict closure contracts.  It is not a dimension-twelve exclusion
or an existence statement.  The first two exclusions are solver-free; the
third is a fail-closed audit of all 130 quadratic relation planes.

For \((2,3,2,2,1,1,1)\), a second exact front-end enumerates all 40
quadratic relation lines, every cubic extension, all 13 projective
\(A_2\)-directions in the degree-five closure identity, and every
degree-five extension.  The ledger
\[
36\longrightarrow144\longrightarrow48
\]
leaves 48 necessary graded cases with digest
`80fd2b21a7b59d1b542b759b5f20a062f451cca9c6dcdf96191e4eef386183ef`.
It does not encode filtered lifts or full raw closure.  The strict
homogeneous quotients themselves have commuting cubes; any candidate in
this branch must use a terminal filtered \(A_3A_3\to A_7\) correction.

## Complete order-\(3^8\) Wilson scan audit

The production scan covers the three adjacent intervals
\[
[1,261686],\quad[261687,802107],\quad[802108,1396077],
\]
whose sizes sum to \(1{,}396{,}077\).  It finds 221 nonabelian cube-generated
subgroups, 63 non-powerful ones, and no closed non-powerful raw cube set.
The independent hard-candidate audit directly verifies
\(H'\nleq H^3\) for all 63 and then finds
\(|P_3(G)|<|H|=243\) in every case.  Therefore no group of order \(3^8\)
is a counterexample.  Combined with the smaller complete catalogues, this
is a computer-assisted lower bound \(|G|\ge3^9\) only for finite
\(3\)-groups; it makes no assertion for other primes or unbounded orders.
