# Finite seeds for prime-power values in cyclic wreath products

Date: 2026-07-29

## Main theorem

Fix a prime \(p\), let \(A\) be a finite group, and put
\[
  P_p(X)=\{x^p:x\in X\}.
\]
Then \(P_p(A\wr C_p)\) is a subgroup if and only if exactly one of the
following mutually disjoint conditions holds.

1. \(p\nmid |A|\).
2. \(A\) is a nontrivial elementary abelian \(p\)-group.
3. \(A\) is a nonabelian semi-extraspecial \(p\)-group and
   \(P_p(A)=A'\).
4. \(A=K\rtimes C_p\) is a Frobenius group with nontrivial kernel \(K\).
5. \(p=2\) and \(A=K\rtimes Q_8\) is a Frobenius group with nontrivial
   kernel \(K\).

In condition 3 the power-surjectivity requirement is automatic when \(p=2\).
When \(p\) is odd, the map
\[
  A/A'\longrightarrow A',\qquad xA'\longmapsto x^p
\]
is linear, and condition 3 requires it to be onto.  In condition 4 the
kernel need not be abelian for odd \(p\).

## Reduction to finite Camina groups

The unrestricted prime-wreath theorem in
`GENERAL_PRIME_WREATH_CRITERION.md` says that, for any group \(A\),
\(P_p(A\wr C_p)\) is a subgroup exactly when either
\[
  P_p(A)=A,                                      \tag{1}
\]
or
\[
  P_p(A)=A'<A,\qquad x^A=xA'
  \quad\text{for every }x\notin A'.             \tag{2}
\]

For finite \(A\), (1) is equivalent to \(p\nmid|A|\).  Indeed, when
\((p,|A|)=1\), choose \(r\) with \(pr\equiv1\pmod{\exp(A)}\), so
\((a^r)^p=a\).  Conversely, if \(p\mid|A|\), Cauchy's theorem gives a
nonidentity element of order \(p\); the power map is not injective and,
on a finite set, is not surjective.  This proves condition 1.

Suppose (2) holds.  If \(A\) is abelian, then \(A'=1=P_p(A)\), so \(A\)
has exponent \(p\).  This gives condition 2, with the trivial group already
belonging to condition 1.

Now suppose \(A\) is nonabelian.  The conjugacy equality in (2) is the
Camina condition.  Moreover \(P_p(A)=A'\) implies that \(A/A'\) has
exponent \(p\).  The Dark--Scoppola classification of finite Camina groups,
with the corrected Lewis and Isaacs--Lewis argument, has three branches:
a Camina group of prime-power order, a Frobenius group with cyclic
complement, or a Frobenius group with quaternion complement.  We analyze
them in turn.

### Prime-power branch

If \(A\) is a \(q\)-group, then the nontrivial abelianization \(A/A'\) is
both a \(q\)-group and of exponent \(p\), so \(q=p\).

A Camina \(p\)-group has nilpotency class two or three.  In the class-three
case the established structure theorem gives
\[
  \exp(A/A_3)=p.
\]
It follows that \(P_p(A)\subseteq A_3<A'\), contrary to (2).  Thus \(A\)
has class two.

Now \(A'\leq Z(A)\).  If \(z\in Z(A)\setminus A'\), then
\(|z^A|=1\), whereas (2) gives \(|z^A|=|A'|>1\), a contradiction.
Consequently \(Z(A)=A'\).  Also
\[
  \Phi(A)=A^pA'=A',
\]
because every \(p\)-th power lies in \(A'\).  Thus \(A\) is special, and
the class-two Camina condition is equivalent to being semi-extraspecial.
The remaining equality \(P_p(A)=A'\) is precisely condition 3.

For odd \(p\), \(A'\) has exponent \(p\), and the class-two collection
formula gives
\[
  (xy)^p=x^py^p[y,x]^{\binom p2}=x^py^p.
\]
The power map therefore factors through a linear map \(A/A'\to A'\).
For \(p=2\), the square map \(A/Z(A)\to Z(A)\) is perfect nonlinear:
each nonzero derivative is an affine translate of a surjective commutator
map.  The standard perfect-nonlinear fiber bound, together with the
semi-extraspecial dimension bound, makes the square map surjective.

### Cyclic Frobenius-complement branch

Write \(A=K\rtimes H\), with \(H\) cyclic.  The fixed-point-free action
gives \([K,H]=K\), so \(A'=K\).  Since \(A/A'\cong H\) has exponent \(p\),
one has \(H\cong C_p\), giving condition 4.

Conversely, let \(A=K\rtimes C_p\) be any Frobenius group with nontrivial
kernel.  The kernel and complement have coprime orders, so the \(p\)-power
map is onto \(K\).  Every \(p\)-th power in \(A\) maps trivially to
\(A/K\cong C_p\), hence
\[
  P_p(A)=K=A'.                                   \tag{3}
\]
For a nonidentity \(h\in C_p\), the map
\[
  L_h:K\longrightarrow K,\qquad
  y\longmapsto y^{-1}h(y)
\]
is bijective.  Indeed, if \(L_h(y)=L_h(z)\), then
\(zy^{-1}=h(zy^{-1})\); fixed-point-freeness gives \(z=y\).
Thus conjugation by elements of \(K\) carries \(h\) through its entire
coset \(Kh\).  The same holds in every nonidentity complement coset, so
\[
  x^A=xK=xA'\qquad(x\notin K).
\]
Together with (3), this proves (2) and the sufficiency of condition 4.

### Quaternion Frobenius-complement branch

Here \(A=K\rtimes Q_8\), and
\[
  A/A'\cong Q_8/Q_8'\cong C_2^2.
\]
Its exponent divides \(p\), forcing \(p=2\).  This gives the only possible
fifth branch.

Let \(z\) be the central involution of \(Q_8\).  It acts fixed-point-freely
on \(K\).  The bijection \(y\mapsto y^{-1}z(y)\) shows that every element
of \(K\) has the form \(y^{-1}z(y)\); applying \(z\) shows that \(z\) acts
as inversion.  Inversion is an automorphism only when \(K\) is abelian.
Also \(K\) has odd order.  Hence
\[
  A'=K\rtimes\langle z\rangle.
\]

Squares in \(K\) cover \(K\).  If \(h\in Q_8\) has order four, then, in
additive notation for the abelian group \(K\),
\[
  (k,h)^2=((1+h)k,z).
\]
Since
\[
  (1-h)(1+h)=1-h^2=1-z=2
\]
and multiplication by two is invertible on \(K\), the map \(1+h\) is
invertible.  The squares with complement component \(h\) therefore cover
\(Kz\), and
\[
  P_2(A)=K\rtimes\langle z\rangle=A'.            \tag{4}
\]

For \(h\notin\langle z\rangle\), its \(K\)-conjugates cover \(Kh\).
Conjugation inside \(Q_8\) interchanges \(h\) and \(hz=h^{-1}\), so its
full \(A\)-class is
\[
  Kh\cup Khz=hA'.
\]
Thus (2) follows from (4), proving sufficiency of condition 5 and completing
the main theorem.

## Two infinite nontrivial families for odd primes

The odd-prime branches are not merely formal possibilities.

### Nonabelian kernels in the Frobenius branch

Let \(p\) be odd, let \(q\) be a prime power with \(q\equiv1\pmod p\), and
choose \(\lambda\in\mathbb F_q^\times\) of order \(p\).  Write
\[
 K=\operatorname{UT}_3(\mathbb F_q)
   =\{(a,b,c):a,b,c\in\mathbb F_q\},
\]
with multiplication
\[
 (a,b,c)(a',b',c')
 =(a+a',\,b+b',\,c+c'+ab').
\]
Then \(K\) is nonabelian because
\[
 [(1,0,0),(0,1,0)]=(0,0,1).
\]
Define
\[
 \alpha(a,b,c)=(\lambda a,\lambda b,\lambda^2c).
\]
The displayed group law shows directly that \(\alpha\) is an automorphism,
and \(\alpha\) has order \(p\).  For \(1\leq i<p\), neither
\(\lambda^i\) nor \(\lambda^{2i}\) equals one, since \(p\) is odd.
Therefore
\[
 C_K(\alpha^i)=1\qquad(1\leq i<p).
\]
It follows that
\[
  A_{p,q}=K\rtimes\langle\alpha\rangle
\]
is a Frobenius group with complement \(C_p\) and nonabelian kernel.  By
condition 4,
\[
 P_p(A_{p,q}\wr C_p)
\]
is a subgroup; it is nonabelian because it contains the diagonal copy of
\(A_{p,q}\).  Varying \(q\), and also taking suitable extension fields,
gives infinitely many examples for every odd \(p\).

### Power-surjective semi-extraspecial seeds

For every odd prime \(p\) and every \(n\geq1\), define \(E_{p,n}\) by
generators
\[
 x_1,y_1,\ldots,x_n,y_n,z
\]
and relations
\[
\begin{gathered}
 z^p=1,\qquad z\ \text{central},\\
 [x_i,y_i]=z,\qquad
 [x_i,x_j]=[y_i,y_j]=[x_i,y_j]=1\quad(i\ne j),\\
 x_1^p=z,\qquad y_1^p=1,\qquad
 x_i^p=y_i^p=1\quad(i\geq2).
\end{gathered}                                    \tag{5}
\]
These are the central products of one extraspecial group of order \(p^3\)
and exponent \(p^2\) with \(n-1\) extraspecial groups of order \(p^3\) and
exponent \(p\).  Hence
\[
 |E_{p,n}|=p^{2n+1},\qquad
 E_{p,n}'=Z(E_{p,n})=\Phi(E_{p,n})=\langle z\rangle,
\]
so \(E_{p,n}\) is extraspecial, and therefore semi-extraspecial and
nonabelian.

Every element has a unique normal form
\[
 z^c\prod_{i=1}^n x_i^{a_i}y_i^{b_i}.
\]
Because \(p\) is odd and the commutator subgroup has exponent \(p\), the
class-two collection formula and (5) give
\[
 \left(z^c\prod_{i=1}^n x_i^{a_i}y_i^{b_i}\right)^p=z^{a_1}.
\]
Thus
\[
  P_p(E_{p,n})=\langle z\rangle=E_{p,n}'.
\]
These groups satisfy condition 3, have exponent \(p^2\), and give a second
infinite family for which \(P_p(E_{p,n}\wr C_p)\) is a nonabelian subgroup.

## The square case as a corollary

Putting \(p=2\) in the main theorem gives the following complete
classification.  For finite \(A\), \(P_2(A\wr C_2)\) is a subgroup if and
only if \(A\) is exactly one of:

1. a group of odd order;
2. a nontrivial elementary abelian \(2\)-group;
3. a nonabelian semi-extraspecial \(2\)-group;
4. a generalized dihedral group
   \(K\rtimes C_2\), where \(K\ne1\) is abelian of odd order and the
   involution acts by inversion;
5. a Frobenius group \(K\rtimes Q_8\), where \(K\ne1\) is abelian of odd
   order.

For condition 4, a fixed-point-free involution acts by inversion by the same
bijection argument used above, and the existence of that inversion
automorphism forces \(K\) to be abelian.  Condition 3 has no additional
square-surjectivity hypothesis because it follows from the
perfect-nonlinear square map and the semi-extraspecial dimension bound.

## Dependency and novelty boundary

The proof uses prior structure theorems: the Dark--Scoppola classification,
its corrected Lewis/Isaacs--Lewis treatment, the class-three fact
\(\exp(A/A_3)=p\), and the perfect-nonlinear value-distribution bound.
The candidate contribution is their synthesis with the unrestricted
prime-wreath closure criterion, together with the exact five-branch
classification.  Priority is provisional pending the citation-chain checks
listed in `LITERATURE_AUDIT.md`.
