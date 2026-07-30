# Complete finite-seed classification for \(A\wr C_p\)

Date: 2026-07-29

Fix a prime \(p\).  For a finite group \(A\), the set
\(P_p(A\wr C_p)\) is a subgroup if and only if \(A\) belongs to one of:

1. \(p\nmid|A|\);
2. a nontrivial elementary abelian \(p\)-group;
3. a nonabelian semi-extraspecial \(p\)-group for which
   \(P_p(A)=A'\);
4. a Frobenius group \(K\rtimes C_p\) with nontrivial Frobenius kernel
   \(K\);
5. when \(p=2\), a Frobenius group \(K\rtimes Q_8\) with nontrivial kernel
   \(K\).

In class 3, the extra power-surjectivity condition is automatic for \(p=2\).
For odd \(p\), the class-two power map \(A/A'\to A'\) is linear and must be
onto.  In class 4 the kernel need not be abelian when \(p\) is odd.  When
\(p=2\), a fixed-point-free involution forces \(K\) to be abelian of odd
order and to be inverted, recovering the generalized-dihedral branch.
In class 5, \(K\) is likewise abelian of odd order.

The nonabelian-kernel warning in class 4 is substantive.  For example, let
\(K=\operatorname{UT}_3(\mathbb F_7)\), written as triples
\((a,b,c)\), and define
\[
  \alpha(a,b,c)=(2a,2b,4c).
\]
This is an automorphism of order three.  Neither \(\alpha\) nor
\(\alpha^2\) fixes a nonidentity element, so
\(K\rtimes\langle\alpha\rangle\) is a Frobenius group with complement
\(C_3\) and nonabelian kernel \(K\).  Thus imposing abelianity on the kernel
would incorrectly delete valid odd-prime seeds.

## Proof

The general prime-wreath criterion gives either \(P_p(A)=A\), equivalent in
the finite case to \(p\nmid|A|\), or
\[
  P_p(A)=A',\qquad x^A=xA'\quad(x\notin A').       \tag{1}
\]
The abelian case of (1) is exactly class 2.

Suppose \(A\) is nonabelian.  Then (1) makes it a Camina group and makes
\(A/A'\) elementary abelian of exponent \(p\).  Apply the
Dark--Scoppola classification with the corrected Lewis/Isaacs--Lewis proof.

If \(A\) is a Camina \(q\)-group, its nontrivial abelianization forces
\(q=p\).  A class-three Camina \(p\)-group cannot occur: the known result
\(\exp(A/A_3)=p\) puts every \(p\)-th power in
\(A_3<A'\), contradicting \(P_p(A)=A'\).  Hence \(A\) has class two and is
semi-extraspecial; the remaining condition is exactly the surjectivity in
class 3.

If \(A=K\rtimes H\) is Frobenius with cyclic complement, then \(K=A'\), and
\(A/A'\cong H\) has exponent \(p\).  Thus \(H=C_p\).  The Frobenius action
has \((|K|,p)=1\), so every element of \(K\) is a \(p\)-th power.  Every
\(p\)-th power in \(A\) lies in \(K\) after passage to \(A/K\cong C_p\).
Therefore \(P_p(A)=K=A'\), giving class 4.

If the Frobenius complement is \(Q_8\), then
\(A/A'\cong Q_8/Q_8'\cong C_2^2\), forcing \(p=2\).  The calculation in
`FINITE_SEED_CLASSIFICATION.md` gives
\[
  A'=K\rtimes\langle z\rangle=P_2(A),
\]
so class 5 is both necessary and sufficient.

Conversely, every listed group satisfies (1) or the surjective-power case.
For class 4, the centralizer of a nonidentity complement element is the
complement, so each class outside \(K=A'\) is its full \(K\)-coset.  The
other branches were checked above.  The general criterion completes the
proof.

## Literature dependency

The class-three exclusion uses the established fact that
\(G/G_3\) has exponent \(p\) for a Camina \(p\)-group of class three; it is
recorded explicitly near the end of Section 5 of M. L. Lewis,
[“Centralizers of Camina \(p\)-groups of nilpotence class 3”](https://arxiv.org/abs/1510.06293),
*Journal of Group Theory* **21** (2018), 319--335,
[doi:10.1515/jgth-2017-0034](https://doi.org/10.1515/jgth-2017-0034).
Lewis attributes that exponent fact to an earlier 1990 source, which should
also be checked before submission.
The Camina classification and its correction are cited in
`FINITE_SEED_CLASSIFICATION.md`.  The candidate new contribution is the
synthesis with the exact prime-wreath criterion, not those structure
theorems.
