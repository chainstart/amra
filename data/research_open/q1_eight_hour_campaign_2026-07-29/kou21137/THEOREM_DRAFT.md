# KOU-21.137 theorem draft: prime-wreath criteria, families, and minimum order

Date: 2026-07-29

## Scope and headline

KOU-21.137, proposed by L. Wilson, asks in particular whether the square
values in a finite 2-group of exponent \(8\), when they form a subgroup, must
form an abelian subgroup.  The answer to this 2-primary subquestion is no.

The individual counterexample
\[
  D_8\wr C_2
\]
is prior art: a public Lean development created by Elias Judin on 2026-04-14
already gives this group.  The potentially publishable content developed here
is therefore not the rediscovery of that example, but the following package:

1. an exact if-and-only-if criterion for \(p\)-th-power values in
   \(A\wr C_p\) to form a subgroup, for every prime \(p\), with no finiteness
   assumption on the seed;
2. its identification with the derived subgroup when the seed's square set is
   proper, and with the Frattini subgroup when the seed is a finite 2-group;
3. a uniform theorem that **every** finite semi-extraspecial 2-group is a
   valid seed, subsuming all extraspecial 2-groups and the groups
   \(\operatorname{UT}_3(\mathbb F_{2^m})\);
4. a complete classification of **all finite seeds for every prime** into at
   most five structural classes, using the Dark--Scoppola--Lewis Camina
   classification;
5. a complete, independently cross-checked SmallGroups classification through
   order \(128\): no example below \(128\), and ten isomorphism types at order
   \(128\);
6. an all-quotients obstruction showing that an exponent-\(p\)
   semi-extraspecial wreath seed can never be repaired into an odd-prime
   counterexample by factoring.

This does **not** settle the odd-prime part of KOU-21.137 or every possible
instance of the broader powerful-subgroup question.

## 1. Exact wreath-square formula

Let \(A\) be an arbitrary group, let
\[
  P=P_2(A):=\{a^2:a\in A\}
\]
be the set (not initially assumed to be a subgroup) of square values, and put
\[
  W=A\wr C_2=(A\times A)\rtimes\langle t\rangle,
  \qquad t(x,y)t=(y,x).
\]
Because the top group acts on only two coordinates, the restricted and
unrestricted wreath products coincide here.  No finiteness hypothesis is
used in Lemma 1, Theorem 2, or the derived-subgroup part of Corollary 3.
Write
\[
  \mathcal C_A:=\{(x,y)\in A^2:x\text{ and }y\text{ are conjugate in }A\}.
\]

### Lemma 1 (all square values)

\[
  P_2(W)=(P\times P)\cup\mathcal C_A.
\]

Indeed,
\[
  (a,b)^2=(a^2,b^2),\qquad ((a,b)t)^2=(ab,ba).
\]
The elements \(ab\) and \(ba\) are conjugate.  Conversely, if
\(y=a^{-1}xa\), then with \(b=a^{-1}x\) one has \(ab=x\) and \(ba=y\).

This elementary specialization is compatible with the general
characterization of powers in \(G\wr S_n\) by Kundu and Mondal.  It should not
be advertised as though the computation of powers in wreath products were
new.

## 2. Exact subgroup criterion

### Theorem 2 (square-subgroup criterion)

The set \(P_2(W)\) is a subgroup of \(W\) if and only if both conditions hold:

1. \(P\) is a subgroup of \(A\);
2. for every \(x\notin P\),
   \[
     x^A=xP.
   \]

When these conditions hold,
\[
  P_2(W)
  =A\times_{A/P}A
  =\{(x,y)\in A^2:xP=yP\}.
\]

### Proof

Suppose \(H=P_2(W)\) is a subgroup.  Lemma 1 shows that \(H\leq A^2\) and
that \(H\) contains the diagonal subgroup
\(\Delta A=\{(x,x):x\in A\}\).

Every subgroup of \(A^2\) containing \(\Delta A\) has the following elementary
fiber-product form.  Define
\[
  N=\{n\in A:(1,n)\in H\}.
\]
Then \(N\trianglelefteq A\), and multiplying an arbitrary \((x,y)\in H\) by a
diagonal element shows
\[
  H=\{(x,y):xN=yN\}.
\]
By Lemma 1, \((1,n)\) is a square value exactly when \(n\in P\): the only
element conjugate to \(1\) is \(1\), and \(1\in P\).  Hence \(N=P\).  In
particular, \(P\) is a normal subgroup.

The quotient \(A/P\) has exponent at most two and is therefore abelian.  Thus
conjugate elements of \(A\) lie in the same \(P\)-coset.  For
\(x\notin P\) and \(p\in P\), the pair \((x,xp)\) belongs to the fiber product
\(H\).  It cannot belong to \(P\times P\), so Lemma 1 forces \(x\) and \(xp\)
to be conjugate.  Consequently \(xP\subseteq x^A\); the reverse containment
was just proved.  This gives condition 2.

Conversely, assume conditions 1 and 2.  The square-value set is invariant
under conjugation, so once \(P\) is a subgroup it is automatically normal.
The set \(P\times P\) is exactly the fiber over the identity coset.  Since
conjugates have the same image in the elementary abelian quotient \(A/P\),
and since each nonidentity fiber is a single conjugacy class by condition 2,
\(\mathcal C_A\) supplies all other fibers.  Lemma 1 now gives
\[
  P_2(W)=A\times_{A/P}A,
\]
which is a subgroup. \(\square\)

## 3. Derived and Frattini identification

There are two useful boundary observations:

- for every group, \(P=1\) exactly when \(A\) is elementary abelian of
  exponent at most two;
- for finite \(A\), \(P=A\) exactly when \(A\) has odd order.  If \(|A|\) is
  odd, choose \(2r\equiv1\pmod{\exp(A)}\), so \(g=(g^r)^2\) for every \(g\).
  Conversely, surjectivity of the square map on a finite group makes it
  injective, which rules out an involution and hence rules out even order.
  For infinite \(A\), \(P=A\) simply means that the square map is
  surjective, and the finite odd-order characterization is not asserted.

If the criterion holds and \(P<A\), then
\[
  P=A'.
\]
The inclusion \(A'\leq P\) follows because \(A/P\) is abelian.  If
\(1\ne p\in P\), choose \(x\notin P\).  Since \(xp\in x^A\), the element \(p\)
is a commutator, so \(P\leq A'\).  (The case \(P=1\) also gives \(A'=1\).)
Thus a nonabelian seed satisfying the theorem is a Camina group:
\[
  x^A=xA'\quad(x\notin A').
\]

### Corollary 3

For an arbitrary group \(A\), assume \(P_2(W)\) is a subgroup and \(P<A\).
Then
\[
  P_2(W)=W'.
\]
If, in addition, \(A\) is a finite 2-group, then
\[
  P_2(W)=W'=\Phi(W).
\]

For completeness, define the surjective homomorphism
\[
  \psi:W\longrightarrow A_{\mathrm{ab}}\times C_2
\]
by sending \((x,y)\) to \(xyA'\) and recording the top
\(C_2\)-coordinate.  Its target is abelian, so \(W'\leq\ker\psi\).  Conversely,
commutators inside the two base factors give
\(A'\times A'\leq W'\), while
\([t,(a,1)]\) identifies the two copies of \(aA'\) in the quotient.  Modulo
\(A'\times A'\), these latter commutators generate the kernel of the
multiplication map
\[
  A_{\mathrm{ab}}\times A_{\mathrm{ab}}\longrightarrow A_{\mathrm{ab}}.
\]
It follows that \(\ker\psi\leq W'\), so \(\psi\) really is the
abelianization map and
\[
  W'=\{(x,y)\in A^2:xy\in A'\}.
\]
Since
\(A/A'=A/P\) has exponent two, this is precisely the condition
\(xP=yP\).  Theorem 2 therefore identifies the kernel \(W'\) with
\(P_2(W)\).

If \(A\) is a finite 2-group, then so is \(W\), and
\(\Phi(W)=W^2W'\).  Here the set of squares is already a subgroup
\(H=P_2(W)\), so \(W^2=H\), while the preceding paragraph gives \(W'=H\).
Hence \(\Phi(W)=H\).  The finite 2-group hypothesis is essential for this last
equality; it is not a statement about arbitrary seeds.  For example,
\(A=S_3\) satisfies the wreath criterion with \(P=A_3=A'\), and
\(P_2(S_3\wr C_2)=W'\) has order 18, whereas
\(\Phi(S_3\wr C_2)=1\).

### Corollary 3.1 (complete classification of finite seeds)

For a finite group \(A\), the square values of \(A\wr C_2\) form a subgroup
if and only if \(A\) is one of:

1. a group of odd order;
2. an elementary abelian 2-group;
3. a nonabelian semi-extraspecial 2-group;
4. a generalized dihedral group \(K\rtimes C_2\), with \(K\ne1\) finite
   abelian of odd order and the involution acting by inversion;
5. a Frobenius group \(K\rtimes Q_8\), with \(K\ne1\) finite abelian of odd
   order and \(Q_8\) acting fixed-point-freely.

Indeed, outside the surjective-square case Theorem 2 makes \(A\) a Camina
group with \(A/A'\) of exponent two.  The corrected
Dark--Scoppola--Lewis classification reduces the nonabelian cases to a
Camina \(p\)-group or a Frobenius group with cyclic or quaternion complement.
These become respectively classes 3, 4, and 5; the abelian proper case is
class 2.  Conversely, each class satisfies Theorem 2.  In the quaternion
case, if \(z\) is the central involution of \(Q_8\), then
\[
 A'=K\rtimes\langle z\rangle,\qquad
 (k,h)^2=((1+h)k,z)
\]
for \(h\) of order four.  Since
\((1-h)(1+h)=1-h^2=1-z=2\) on the odd-order abelian group \(K\),
\(1+h\) is invertible and the squares cover \(Kz\), proving
\(P_2(A)=A'\).

The complete proof, exact literature dependencies, and the exhaustive
SmallGroups check of all 3,596 types through order 128 are in
`FINITE_SEED_CLASSIFICATION.md`.

## 4. A structural source of counterexamples

### Corollary 4 (central Camina-special seeds)

Suppose \(A\) is a finite nonabelian 2-group with a central subgroup \(N\) such
that
\[
  P_2(A)=N,\qquad x^A=xN\quad(x\notin N).
\]
Then
\[
  P_2(A\wr C_2)
  =A\times_{A/N}A
  =(A\wr C_2)'
  =\Phi(A\wr C_2).
\]
Moreover \(N=A'=Z(A)=\Phi(A)\), and the square subgroup is explicitly
\[
  A\times_{A/N}A\cong A\times N,
  \qquad (a,n)\longmapsto(a,an).
\]

Here are the structural deductions.  A nontrivial finite 2-group cannot have
a surjective square map, so \(N=P_2(A)<A\).  Theorem 2 then gives \(N=A'\).
Also \(N\ne1\), since otherwise \(A\) would have exponent two and be abelian.
If \(z\in Z(A)\setminus N\), the hypothesis would give
\(z^A=zN\), contradicting \(z^A=\{z\}\).  Thus \(Z(A)=N\).  Finally, for a
finite 2-group,
\[
  \Phi(A)=A^2A'=N,
\]
because both the subgroup generated by squares and the derived subgroup are
\(N\).

If \(A\) has exponent \(4\), then \(A\wr C_2\) has exponent exactly \(8\).
Its square subgroup \(A\times N\) has exponent at most \(4\) and is
nonabelian.  For a finite 2-group \(H\), powerfulness requires
\(H'\leq H^4\); here \(H^4=1\) but \(H'\ne1\).  Thus the square subgroup is
not powerful, and in particular is not abelian.

## 5. All semi-extraspecial 2-groups are seeds

The two explicit families below belong to a much larger class.  Recall that a
finite 2-group \(A\) is semi-extraspecial when it is special and
\(A/N\) is extraspecial for every maximal subgroup \(N<Z(A)\).

### Theorem 5 (the square map is vectorial bent)

Let \(A\) be a finite semi-extraspecial 2-group, and write
\[
  |A:Z(A)|=2^{2n},\qquad |Z(A)|=2^m.
\]
Then \(m\leq n\), \(A\) has exponent \(4\), and
\[
  P_2(A)=Z(A).
\]
More precisely, for every \(z\in Z(A)\), the number of cosets
\(xZ(A)\) satisfying \(x^2=z\) is at least
\[
  2^{n-m}\bigl(2^n-2^m+1\bigr).
\]
Consequently, every \(A\wr C_2\) is an exponent-eight counterexample to the
2-primary part of KOU-21.137, with
\[
\begin{aligned}
  |A\wr C_2|&=2^{4n+2m+1},\\
  P_2(A\wr C_2)
    &=(A\wr C_2)'=\Phi(A\wr C_2)
      \cong A\times Z(A),\\
  |P_2(A\wr C_2)|&=2^{2n+2m}.
\end{aligned}
\]

The value-distribution part of this theorem is not claimed as new.
The map below is a vectorial Boolean bent, equivalently perfect nonlinear,
function.  Nyberg's bound already gives \(m\leq n\), while
Kölsch--Polujan, Theorem 2.4 and Corollary 2.7, give the displayed fiber
bound and surjectivity in this generality.  The contribution relevant here is
the identification of the semi-extraspecial square map with that established
theory and its use in the wreath-product criterion.

#### Proof

Put \(V=A/Z(A)\) and \(Z=Z(A)\), viewed as vector spaces over
\(\mathbb F_2\).  The square map
\[
  q:V\longrightarrow Z,\qquad q(xZ)=x^2
\]
is well defined and quadratic.  Its polar form is the commutator bimap
\[
  b(v,w)=q(v+w)+q(v)+q(w).
\]
For each nonzero \(\lambda\in Z^\vee=\operatorname{Hom}(Z,\mathbb F_2)\),
the scalar alternating form
\[
  b_\lambda=\lambda\circ b
\]
is nondegenerate: its radical is the center of the extraspecial quotient
\(A/\ker\lambda\), modulo \(Z/\ker\lambda\).

Equivalently, for every \(0\ne a\in V\), the derivative
\[
  D_aq(v)=q(v+a)+q(v)=q(a)+b(v,a)
\]
is balanced on \(Z\), because \(b(a,V)=Z\).  Thus \(q\) is perfect nonlinear,
or in the elementary abelian terminology, vectorial Boolean bent.

We first record the dimension bound.  In a basis of \(V\), the matrix of
\(b_\lambda\) is an alternating \(2n\times2n\) matrix whose entries are
linear forms in the \(m\) coordinates of \(\lambda\).  Its Pfaffian
\(f(\lambda)\) is homogeneous of degree \(n\), satisfies
\(\det b_\lambda=f(\lambda)^2\), and has zero set exactly
\(\{0\}\).  If \(n<m\), the Chevalley--Warning theorem would make the number
of zeros of \(f\) in \(\mathbb F_2^m\) divisible by \(2\), contradicting
that it is exactly \(1\).  Hence \(m\leq n\).  This recovers the classical
center bound attributed to Beisiegel; the Pfaffian argument is included to
keep the present proof self-contained.  It is also the group-theoretic
specialization of Nyberg's parameter bound.

Now fix \(0\ne\lambda\in Z^\vee\) and set \(Q_\lambda=\lambda\circ q\).
Because its polar form is nondegenerate, its quadratic Gauss sum satisfies
\[
  S_\lambda:=\sum_{v\in V}(-1)^{Q_\lambda(v)}=\pm2^n.
\]
For completeness, squaring the sum and substituting \(w=v+u\) gives
\[
\begin{aligned}
  S_\lambda^2
   &=\sum_{u\in V}(-1)^{Q_\lambda(u)}
       \sum_{v\in V}(-1)^{b_\lambda(v,u)}
     =2^{2n},
\end{aligned}
\]
because the inner character sum vanishes unless \(u=0\).

Fourier inversion on the additive group of \(Z\) therefore gives, for every
\(z\in Z\),
\[
\begin{aligned}
  |\{v\in V:q(v)=z\}|
   &=2^{-m}\sum_{\lambda\in Z^\vee}
       (-1)^{\lambda(z)}
       \sum_{v\in V}(-1)^{\lambda(q(v))}\\
   &\geq
     2^{-m}\left(2^{2n}-(2^m-1)2^n\right)\\
   &=2^{n-m}\bigl(2^n-2^m+1\bigr)>0.
\end{aligned}
\]
Thus \(q\) is onto and \(P_2(A)=Z\).  Semi-extraspecial groups are Camina
special, so \(x^A=xZ\) for \(x\notin Z\).  Corollary 4 now applies.  Finally,
surjectivity supplies an element of order four in \(A\); the corresponding
switched element in \(A\wr C_2\) has order eight.  The square subgroup
\(A\times Z\) is nonabelian and, having exponent four, is not powerful.
\(\square\)

The last Fourier calculation is retained as a short self-contained
special-case proof.  Its numerical lower bound is exactly the
Kölsch--Polujan perfect-nonlinear lower bound
\[
  |V|/|Z|-\sqrt{|V|}+\sqrt{|V|}/|Z|.
\]

### Corollary 5.1 (complete classification of finite nonabelian 2-group seeds)

For a finite nonabelian 2-group \(A\),
\[
  P_2(A\wr C_2)\text{ is a subgroup}
  \quad\Longleftrightarrow\quad
  A\text{ is semi-extraspecial}.
\]

The reverse implication is Theorem 5 together with the wreath criterion.
For the forward implication, Theorem 2 gives
\[
  P_2(A)=A',
  \qquad
  x^A=xA'\quad(x\notin A'),
\]
so \(A\) is a Camina 2-group.  Macdonald's theorem that every Camina
2-group has nilpotency class two now applies.  Since \(A'\ne1\), a central
element \(z\notin A'\) would have both \(z^A=\{z\}\) and
\(z^A=zA'\), which is impossible.  Thus \(Z(A)=A'\).  Also
\[
  \Phi(A)=A^2A'=A',
\]
because the square values themselves equal \(A'\).  Hence \(A\) is special.
For a maximal subgroup \(N<Z(A)\), if \(xN\) were central in \(A/N\) with
\(x\notin Z(A)\), the Camina property in class two would give
\([x,A]=Z(A)\nleq N\), a contradiction.  Therefore
\[
  Z(A/N)=(A/N)'=\Phi(A/N)=Z(A)/N\cong C_2,
\]
so \(A/N\) is extraspecial.  This proves directly that \(A\) is
semi-extraspecial, in agreement with Verardi's known equivalence between
class-two Camina \(p\)-groups and semi-extraspecial \(p\)-groups.

The Macdonald and Verardi results are prior structure theorems; the candidate
new content here is their combination with the wreath criterion and the
identification of the semi-extraspecial square map with the established
perfect-nonlinear framework.

### 5.2 Extraspecial seeds as a subfamily

Let \(A\) be any nontrivial extraspecial 2-group.  Then
\[
  Z(A)=A'=\Phi(A)\cong C_2,\qquad A/Z(A)\text{ is elementary abelian}.
\]
Every such \(A\) has exponent \(4\): its squares lie in its center, and a
nonabelian group cannot have exponent \(2\).  Hence
\[
  P_2(A)=Z(A).
\]
For \(x\notin Z(A)\), the map \(a\mapsto[x,a]\) is a nontrivial homomorphism
from \(A\) onto the order-two center, so \(x^A=xZ(A)\).

Consequently every \(A\wr C_2\) is a counterexample.  If
\[
  |A|=2^{2n+1},
\]
then
\[
  |A\wr C_2|=2^{4n+3},\qquad
  |P_2(A\wr C_2)|=2^{2n+2},
\]
and
\[
  P_2(A\wr C_2)\cong A\times C_2.
\]
The two extraspecial types give two infinite subfamilies.  At \(n=1\), the
seeds are \(D_8\) and \(Q_8\).

### 5.3 Unitriangular seeds as a subfamily

Let \(q=2^m\) and
\[
  A=\operatorname{UT}_3(\mathbb F_q)
  =\left\{
  u(a,b,c)=
  \begin{pmatrix}
  1&a&c\\0&1&b\\0&0&1
  \end{pmatrix}:a,b,c\in\mathbb F_q
  \right\}.
\]
The multiplication and square formulas are
\[
  u(a,b,c)u(a',b',c')
  =u(a+a',\,b+b',\,c+c'+ab'),
\]
\[
  u(a,b,c)^2=u(0,0,ab).
\]
Thus
\[
  P_2(A)=Z(A)=
  N=\{u(0,0,c):c\in\mathbb F_q\}.
\]
Indeed every \(c\) occurs as \(1\cdot c\).  The square formula also shows that
\(\exp(A)\leq4\), while \(u(1,1,0)\) has square \(u(0,0,1)\ne1\), so
\(\exp(A)=4\).  The commutator has central coordinate
\[
  ab'+a'b.
\]
For fixed \((a,b)\ne(0,0)\), this is a nonzero
\(\mathbb F_q\)-linear functional of \((a',b')\), hence is surjective.  It
follows that \(x^A=xN\) for every \(x\notin N\).

Therefore \(W=A\wr C_2\) has
\[
  |W|=2q^6=2^{6m+1},\qquad \exp(W)=8,
\]
and
\[
  P_2(W)=W'=\Phi(W)\cong A\times N,\qquad
  |P_2(W)|=q^4=2^{4m}.
\]
This subgroup is nonabelian and not powerful.  The case \(m=1\) recovers
\(D_8\wr C_2\), while \(m>1\) supplies a family not covered merely by
increasing the order of an extraspecial seed.

## 6. The direct odd-prime analogue fails at \(p=3\)

The tempting odd-prime replacement is
\[
  A=\operatorname{UT}_3(\mathbb F_3),\qquad W=A\wr C_3.
\]
Here \(|A|=27\), \(\exp(A)=3\),
\[
  |W|=3^{10}=59049,\qquad \exp(W)=9,
\]
so the ambient hypotheses of the odd part of KOU-21.137 are exactly right.
Nevertheless, exhaustive evaluation of all 59049 elements gives
\[
  |\{w^3:w\in W\}|=219,
\]
while the subgroup generated by those cube values has order \(243\).
It is nonabelian, but the cube-value set is not closed.

The deterministic first closure failure in the pc basis chosen by GAP is:
\[
\begin{aligned}
r_1&=(1,1,0,0,0,0,0,0,0,0),\\
r_2&=(1,2,0,0,2,1,0,0,0,0),\\
r_1^3&=(0,1,1,1,0,0,0,0,0,0),\\
r_2^3&=(0,2,2,2,2,0,0,0,0,1),\\
r_1^3r_2^3&=(0,0,0,0,2,0,0,0,0,1),
\end{aligned}
\]
and the last vector is not a cube value.  These coordinates are intended as
a machine-reproducible witness; `validate_odd_wreath_p3.g` constructs the pc
basis and verifies the claim from scratch.

The same 219 count has a structural explanation.  Writing \(Z=Z(A)\),
\[
  H:=\langle P_3(W)\rangle=\Delta A\,Z^3,\qquad
  Z(H)=Z^3,\qquad H'=\Delta Z.
\]
The value set fills the \(Z^3\)-coset over each of the eight nonzero elements
of \(A/Z\), but its central sector is only \(\Delta Z\).  Hence
\(219=8\cdot27+3\), with all 24 missing elements central in \(H\).
The cyclic-permutation module \(Z^3\) in characteristic three has the chain
\[
  0<\Delta Z<\ker(z_1+z_2+z_3)<Z^3.
\]
Adjoining these modules to the value set gives sizes \(219,219,225,243\).
Thus only all of \(Z^3\) repairs closure, and that module contains
\(H'=\Delta Z\), so the repaired quotient has abelian cube subgroup.

This failure cannot be repaired by quotienting this particular \(W\) while
retaining nonabelian cubes.  The computation gives
\[
  |Z(W)|=3,\qquad
  \langle w^3:w\in W\rangle'=Z(W).
\]
Every nontrivial normal subgroup of a finite \(p\)-group meets its center
nontrivially, so every nontrivial normal subgroup of this \(W\) contains
\(Z(W)\).  Hence the image of the generated cube group in every proper
nontrivial quotient is abelian.  Directly, \(W/Z(W)\) still has 73 cube values
generating a group of order 81, so even the smallest central quotient does not
make the values closed.

A second targeted repair begins with the extraspecial group of order 27 and
exponent 9 and quotients its \(C_3\)-wreath product by the diagonal center.
The resulting group has order 19683, exponent 9, and nilpotency class 5.  Its
81 cube values do form a subgroup of order 81, but that subgroup is abelian.
Thus this nearby modification satisfies closure without violating the
conjectured conclusion.

This is a useful boundary result, not a solution of the odd-prime branch.  It
shows that the successful \(C_2\)-wreath mechanism does not transfer formally
to \(C_p\).

### A general odd-prime no-go for the diagonal-power quotient repair

The preceding failed repair is the \(p=3\) instance of a general obstruction.
Let \(p\) be an odd prime and \(A\) a finite \(p\)-group.  Assume that
\[
  U=P_p(A)
\]
is a central subgroup, and put \(W=A\wr C_p\).  If \(\mathcal C(A)\) denotes
the conjugacy classes of \(A\), then
\[
  P_p(W)=U^p\cup\bigcup_{C\in\mathcal C(A)}C^p
  \tag{6.1}
\]
and, with \(M=UA'\),
\[
  \langle P_p(W)\rangle=\Delta A\,M^p.
  \tag{6.2}
\]
Thus
\[
\begin{aligned}
 |P_p(W)|
   &=|U|^p+\sum_C|C|^p-|U|,\\
 |\langle P_p(W)\rangle|
   &=|A|\,|M|^{p-1}.
\end{aligned}
\tag{6.3}
\]

For completeness, fix a generator \(t\) of the top \(C_p\).  In every
nontrivial coset \(A^pt^k\), the \(p\)-th-power coordinates are the cyclic
rotations of the base-coordinate product read with step \(k\).  Since
\(k\ne0\pmod p\), this visits all positions.  Conversely, choosing successive
prefixes realizes independently any ordered \(p\)-tuple in one conjugacy
class.  This proves (6.1), including all \(p-1\) nontrivial top cosets.
Comparing such tuples with diagonal tuples independently in each coordinate
generates \((A')^p\); together with the base powers this proves (6.2).

In fact, the closure criterion needs neither centrality nor finiteness.
For an arbitrary group \(A\), put \(Q=P_p(A)\) as a raw set and
\(V=\langle Q\rangle A'\).  The same calculation gives
\[
 P_p(A\wr C_p)=Q^p\cup\bigcup_C C^p,\qquad
 \langle P_p(A\wr C_p)\rangle=\Delta A\,V^p.
\]
Intersecting these two sets with a coordinate axis gives respectively
\(Q\) and \(V\).  Closure therefore forces \(Q=V\), so the raw value set
automatically becomes a subgroup containing \(A'\).  If \(Q<A\), the tuples
\((x,xq_1,\ldots,xq_{p-1})\) force \(x^A=xQ\), and then \(Q\le A'\).
Conversely these conditions give the fiber product over \(A/A'\).  Hence
\[
\boxed{
 P_p(A\wr C_p)\text{ is closed}
 \iff
 \begin{cases}
 Q=A,\quad\text{or}\\
 Q=A'\text{ and }x^A=xA'\ (x\notin A').
 \end{cases}}
\tag{6.4}
\]
For a nontrivial finite \(p\)-group the first case cannot occur.  In
particular, an exponent-\(p\) seed has \(Q=1\), so its wreath \(p\)-th
powers can be closed only when the seed is
abelian; the resulting diagonal subgroup is abelian.  Although such a wreath
has exponent \(p^2\), it cannot answer the odd KOU problem negatively.
The full unrestricted proof is in `GENERAL_PRIME_WREATH_CRITERION.md`.

### Every quotient of an exponent-\(p\) semi-extraspecial wreath seed

There is a stronger obstruction for the most direct odd-prime construction.
Let \(p\) be odd, let \(A\) be a nonabelian exponent-\(p\)
semi-extraspecial group, and write
\[
 U=A'=Z(A),\qquad W=A\wr C_p,\qquad
 S=P_p(W),\qquad H=\langle S\rangle,\qquad K=U^p.
\]
Then, for every \(N\trianglelefteq W\),
\[
 \boxed{
 P_p(W/N)\text{ is a subgroup}\quad\Longrightarrow\quad
 \Delta U\leq N.}
\]
Consequently the resulting \(p\)-power subgroup in \(W/N\) is abelian.

Indeed, the exponent-\(p\) hypothesis gives \(P_p(A)=\{1\}\).
Semi-extraspecial groups are Camina: their central conjugacy classes are
singletons and every noncentral class is a full coset \(aU\).  The exact
wreath value formula therefore reduces to
\[
 S=(H\setminus K)\cup\Delta U,\qquad
 H=\Delta A\,K,\qquad H'=\Delta U.                \tag{6.5}
\]
Put \(L=N\cap H\).  If the image of \(S\) is a subgroup, it equals all of
\(H/L\), because \(S\) generates \(H\).

If \(L\not\leq K\), choose \(h=\Delta a\,k\in L\setminus K\), where
\(a\notin U\) and \(k\in K\).  For \(g\in A\),
\[
 [h,\Delta g]=\Delta[a,g].
\]
The semi-extraspecial commutator map \(g\mapsto[a,g]\) is onto \(U\).
Normality of \(N\) therefore gives \(\Delta U\leq N\).

If \(L\leq K\), the noncentral part \(H\setminus K\) covers no element of
\(K/L\), so closure forces
\[
 K=L+\Delta U.
\]
As an \(\mathbb F_p[C_p]\)-module,
\[
 K\cong U\otimes_{\mathbb F_p}\mathbb F_p[z]/(z^p),
 \qquad z=t-1,\qquad \Delta U=z^{p-1}K.
\]
The equality \(K=L+\Delta U\) says that \(K/L\) is generated by fixed
points, so \(zK\leq L\).  Hence
\(\Delta U=z^{p-1}K\leq L\), proving the assertion in the second case.
Finally, (6.5) gives
\[
 (HN/N)'=\Delta U\,N/N=1.
\]

This result is strictly stronger than the earlier observation using the
order-three center of the smallest \(p=3\) wreath product: it applies to all
normal quotients and all exponent-\(p\) semi-extraspecial seeds.  GAP
enumerates all \(101\) normal subgroups of
\(\operatorname{UT}_3(\mathbb F_3)\wr C_3\); exactly \(98\) quotient images
have closed cube values, and all \(98\) kill \(\Delta U\).  The full proof
and exact regression certificate are in
`EXPONENT_P_WREATH_ALL_QUOTIENTS_NO_GO.md`.

Combining (6.4) with the corrected finite Camina classification gives a
complete finite-seed theorem for every prime.  The valid \(A\) are exactly:

1. \(p\nmid|A|\);
2. nontrivial elementary abelian \(p\)-groups;
3. nonabelian semi-extraspecial \(p\)-groups with \(P_p(A)=A'\);
4. Frobenius groups \(K\rtimes C_p\);
5. when \(p=2\), Frobenius groups \(K\rtimes Q_8\).

The class-three Camina \(p\)-groups are excluded because
\(\exp(A/A_3)=p\), so all \(p\)-th powers lie in \(A_3<A'\).
For odd \(p\), the kernel \(K\) in the cyclic-complement branch need not be
abelian.  For instance,
\(\operatorname{UT}_3(\mathbb F_7)\rtimes C_3\), with the complement acting
by \((a,b,c)\mapsto(2a,2b,4c)\), is a valid nonabelian-kernel seed.  The
complete proof, a \(p=2,3,5\) SmallGroups audit, and an exact regression for
this order-1029 example are in `GENERAL_PRIME_FINITE_SEEDS.md` and
`test_general_prime_nonabelian_kernel.py`.

The positive proper case also has an exact structural position.  Put
\(B=A/A'\), \(W=A\wr C_p\), and \(H=P_p(W)\).  In the coordinate quotient
\(A^p\to B^p\),
\[
 H/(A')^p=\Delta B,\qquad
 W'/(A')^p=\ker\!\left(\Sigma:B^p\to B\right).
\]
Since \(B\) has exponent \(p\), \(\Delta B\leq\ker\Sigma\), and therefore
\[
 H\leq W',\qquad [W':H]=|B|^{p-2}.                \tag{6.6}
\]
If \(A\) is a finite \(p\)-group, then
\(W/W'\cong B\times C_p\) has exponent \(p\), so
\[
 \Phi(W)=W'.
\]
Thus \(p=2\) is exactly the case \(H=W'=\Phi(W)\); for odd \(p\), \(H\) is
proper in both, with the precise index in (6.6).  A standalone proof and
two \(p=3\) exact checks are in
`STRUCTURAL_POSITION_OF_POWER_SUBGROUP.md`.

There is a complementary nilpotency-class barrier for the odd KOU problem.
If \(p\) is odd, \(\exp(G)\mid p^2\), and
\(\operatorname{cl}(G)\le p\), Hall collection of
\([x^p,y^p]\) has every basic-commutator coefficient divisible by \(p^2\):
at total weight at most \(p\), each coefficient contains one proper
binomial coefficient from the \(x\)-copies and one from the \(y\)-copies.
Hence
\[
 [x^p,y^p]=1\qquad(x,y\in G).                     \tag{6.7}
\]
The raw \(p\)-th powers therefore commute, and if they form a subgroup it
must be abelian.  A counterexample must have class at least \(p+1\).
The first potentially surviving Hall terms occur at weight \(p+1\);
an explicit \(\operatorname{UT}_{2p+1}(\mathbb F_p)\) family has exponent
\(p^2\), class \(2p\), and two noncommuting \(p\)-th powers.  Thus the
currently proved window for the least class \(c_{\rm nc}(p)\) at which
noncommuting raw \(p\)-th powers can occur is
\[
 p+1\le c_{\rm nc}(p)\le2p.
\]
The unitriangular family is not known to have a closed power-value set, so
the upper bound does not apply to the least class of a KOU counterexample;
only the lower bound \(p+1\) does.
For \(p=3\), all 463 exponent-nine SmallGroups through order 729 still have
commuting cubes, including all 66 class-four cases.  The proof, exact scan,
and unitriangular witness are in `ODD_KOU_NILPOTENCY_BARRIER.md`.

For metabelian groups the gap closes completely.  If \(G''=1\),
\(\exp(G)\mid p^2\), and \(\operatorname{cl}(G)<2p\), then
\[
 [x^p,y^p]=1\qquad(x,y\in G).                    \tag{6.8}
\]
To see this, write \(A=G'\) as a module over
\(\mathbb Z[G/G']\), let \(\Delta\) be the augmentation ideal, and put
\(X=\bar x-1\).  The class bound gives
\(A\Delta^{2p-2}=0\).  Expanding
\((ax)^{p^2}=1\) for \(a\in A\) shows
\[
 0=a\sum_{k\ge0}\binom{p^2}{k+1}X^k.
\]
Below augmentation degree \(2p-2\), the only coefficient not divisible by
\(p^2\) is
\(\binom{p^2}{p}=pu\), \(p\nmid u\).  Hence
\(paX^{p-1}=0\).  Metabelian collection represents
\([x^p,y^p]\), up to an invertible conjugation monomial, by
\[
 [x,y]\,
 \sigma_p(1+X)\sigma_p(1+Y),\qquad
 \sigma_p(1+X)=\sum_{i=0}^{p-1}\binom p{i+1}X^i.
\]
The terms below bidegree \((p-1,p-1)\) vanish by \(p^2A=0\) or the
preceding one-\(p\) relation, and the top term lies in
\(A\Delta^{2p-2}=0\).  This proves (6.8).

The bound is sharp even within the metabelian category.  For the two
length-\(p\) strings in \(\operatorname{UT}_{2p+1}(\mathbb F_p)\), the
subgroup generated by the two string matrices is metabelian: its derived
subgroup lies in one plus the square-zero mixed ideal spanned by
\(A^iB^j\).  It has class \(2p\) and the displayed \(p\)-th powers do not
commute.

The unrestricted analogue of (6.8) remains open in this package.  The
metabelian proof applied modulo \(G''\) yields only
\([G^p,G^p]\leq G''\).  The full order-\(2187\) SmallGroups audit gives
strong endpoint evidence at \(p=3\): among 8,302 exponent-nine groups,
including all 26 class-five cases, every cube subgroup is abelian and the
class-five cube subgroups lie in \(Z_3(G)\).  These refinements and the
fail-closed status are recorded in
`METABELIAN_2P_NILPOTENCY_BARRIER.md` and
`SHARP_2P_BARRIER_STATUS.md`.

### The genuine odd-prime target and two directed \(p=3\) exclusions

The preceding noncommutativity tests are sufficient only in the
exponent-\(p^2\) range.  In general, if \(H=P_p(G)\) is a subgroup, then
\[
 P_p(H)=P_{p^2}(G),
\]
so Wilson's non-powerfulness target is
\[
 H'\nleq H^p=\langle P_{p^2}(G)\rangle.           \tag{6.9}
\]
This distinction eliminates the positive odd-prime cyclic-wreath families:
for every finite \(p\)-group seed in the nonabelian branch,
\[
 H'=H^p=P_p(H)=\Delta A'.
\]
Thus \(H\) is powerful.  The short proof and its precise scope are in
`ODD_PRIME_WREATH_POWERFULNESS_NO_GO.md`.

For \(p=3\), let \(G\) be generated inside
\(\operatorname{UT}_7(\mathbb F_3)\) by the two length-three strings
\[
 1+E_{12}+E_{23}+E_{34},\qquad
 1+E_{45}+E_{56}+E_{67}.
\]
Then \(|G|=3^{13}\), \(\operatorname{cl}(G)=6\), and \(\exp(G)=9\).
Its 649 raw cubes generate a class-two, exponent-three, non-powerful
subgroup \(K\) of order \(3^{10}\), but are not closed.  More strongly,
\[
 Z(G)=K'=\langle[X^3,Y^3]\rangle\cong C_3.
\]
Every nontrivial normal subgroup of \(G\) contains this centre, so every
nontrivial quotient has abelian cube-generated subgroup.  Each of the four
maximal subgroups also has abelian cube-generated subgroup.  Exact
enumeration therefore excludes every section of this candidate; see
`UT7_TWO_STRING_SUBQUOTIENT_NO_GO.md`.

There is a complementary algebra-group barrier.  If \(J\) is a nilpotent
associative \(\mathbb F_3\)-algebra with \(J^9=0\), then
\[
 (1+a)^3=1+a^3.
\]
If \(P_3(1+J)\) is a non-powerful subgroup, two cubes do not commute, so
\([J^3,J^3]\ne0\).  Filtration dimensions then give
\[
 \dim_{\mathbb F_3}J\ge8.                         \tag{6.10}
\]
There are only seven possible dimension-eight filtration profiles.  Five
force \(J^3\) to commute by degree, one is ruled out by the associativity
inequality \(\dim\operatorname{gr}_2J=1\Rightarrow
\dim\operatorname{gr}_3J\le1\), and the final profile is
\((2,1,1,1,1,1,1)\).  In the final profile, either every cube lies in
\(J^4\), so cube products vanish in \(J^8\), or some
\(a^3\notin J^4\).  Then \(A_3A_3=A_6\) forces
\(a^6\notin J^7\), hence \(a^4\notin J^5\); the possible degree-seven
commutator is therefore a multiple of \([a^3,a^4]=0\).  This gives the
human strengthening \(\dim J\ge9\).  The older 34-variable SMT
certificate remains an independent check.

At dimension nine there are exactly 29 power-filtration profiles.  Degree
arguments remove 20 of the 21 profiles with \(J^7=0\).  For the sole
survivor \((2,2,2,1,1,1)\), a closure-aware QF_BV model additionally
requires the projected cube map \(A_1\to A_3\) to be bijective and requires
a cube root for the circle product of two noncommuting basis cubes.  The
resulting necessary-condition system is unsatisfiable.  A hand argument
now supersedes it without using closure.  If \(f_k\) denotes the
\(k\)-fold multiplication tensor on \(A_1\), associativity and the
one-dimensional layers \(A_4,A_5,A_6\) force
\[
f_5=f_4\otimes r=\ell\otimes f_4,
\qquad
f_6=f_5\otimes s=t\otimes f_5.
\]
The shift-tensor identity makes \(f_6\) a pure sixth tensor power, hence
symmetric.  Therefore \(x^3y^3=y^3x^3\) in \(A_6\), and \(J^7=0\)
kills the commutator of arbitrary filtered cubes.

Of the eight deeper profiles, one violates
\(\dim A_2=1\Rightarrow\dim A_3\le1\), four violate the layer inequality
\(d_{i+j}\le d_i d_j\), and the last three are removed by the human
cube-commutativity lemmas of
`DIM9_HUMAN_CUBE_COMMUTATIVITY.md`.  The two length-seven profiles use
the \(J^8=0\) argument above.  In the length-eight profile, either cubes
lie in \(J^4\), or one element's powers form a filtration basis of
\(J^2\), which is then commutative.  Hence the human-checkable bound is
\[
 \dim_{\mathbb F_3}J\ge10.                        \tag{6.11}
\]
See `DIM9_ALGEBRA_PROFILE_STATUS.md`.

At dimension ten, the stronger nilpotency hypothesis \(J^9=0\), which
implies exponent dividing nine for \(1+J\), permits 92, not 93,
positive power-filtration profiles: the formerly included
length-nine composition has \(A_9\ne0\) and lies outside the scope.
The human inequalities
\[
 d_{i+j}\le d_i d_j,\qquad
 d_i=1\Rightarrow d_{i+1}\le1\quad(i\ge2)
\]
and the earlier degree arguments first reduce the list.  The
consecutive-tail tensor lemma removes the remaining length-six
rank-one tails.  The length-seven cyclic-\(J^3\) lemma controls the
filtered correction explicitly: for a tail basis
\(t^4,\ldots,t^7\), a complementary \(u\in J^3\) has
\(ut,tu\in J^5\), and \((tu)t=t(ut)\) implies
\(ut^3=t^3u\).  The length-eight cyclic-basis lemma makes
\(t^3,\ldots,t^8\) a basis of \(J^3\).  These arguments remove every
dimension-ten profile.  Therefore the human-checkable bound strengthens
to
\[
 \dim_{\mathbb F_3}J\ge11.                       \tag{6.11a}
\]
The complete profile ledger is in
`DIM10_ALGEBRA_PROFILE_STATUS.md`.

This bound is sharp for noncommuting raw cubes alone.
`DIM11_SHARP_NONCOMMUTING_CUBE_WITNESS.md` constructs an associative
algebra with profile \((2,2,2,2,2,1)\) and cubes
\(A_3,A_3+B_3\) whose commutator is \(B_6\ne0\).  Its 171-element raw
cube set is not closed: a displayed circle product equals \(B_3\), which
is not a cube.  Thus further Wilson progress must use closure.

At dimension eleven, exact positive-composition enumeration gives 246
in-scope profiles.  A quadratic normal-word lemma gives
\[
d_2=2\Longrightarrow d_3\le2,
\]
and the remaining human tensor and cyclic-tail lemmas leave two profiles.
Closure excludes the sharp length-six profile
\((2,2,2,2,2,1)\): the leading cube map must be bijective, the kernel
of the projection of the closed cube subgroup to \(A_3\) is \(1+J^6\),
and comparison of \(v^3\) with \((v+z)^3\), \(z\in J^3\), forces
\(v^3z=zv^3\).  The profile-level pass leaves
\[
(2,2,2,2,1,1,1).
\]
It satisfies a further dichotomy: either its leading cube image in
\(A_3\) is one-dimensional,
or the kernel of the leading projection is \(1+J^6\), the closed
cube subgroup has order 81, and cubes of roots in \(J^2\) cover
\(J^6\).  The pure \(A_5,A_6,A_7\) tail makes the apparent
\(A_3\)-direction correction vanish, so the cube descends to a
nine-point bijection \(P:A_2\to J^6\).
Comparing roots \(v\) and \(v+w\), with
\(v\in A_1,w\in A_2\), also gives
\[
\operatorname{ad}_v^2(w)=0\text{ in }A_4,
\qquad \operatorname{ad}_w^2(v)=0\text{ in }A_5.
\]
The exact row reduction of the 12 q-bijective quadratic relation
planes then makes the associated graded algebra commutative in every
dimension-compatible case.  Writing its quadratic part as
\(\mathbb F_3[x,y]/(f)\), bijectivity excludes \(f=\ell^2\);
irreducibility of \(f\) would make the degree-five relation kill all of
degree six.  Hence \(f=xy\), and \(d_6=1\) forces one of the two pure
degree-five chains to stop.  For its generator \(b\), one has
\([b^2]\ne0\) but \(b^6=0\), contradicting
\(P([b^2])=(b^2)^3\) and bijectivity of \(P\).

In the one-dimensional branch, the pure degree-seven tensor makes the
products \(A_3A_4\to A_7\) and \(A_4A_3\to A_7\) equal.  Thus
\([J^3,J^4]\subseteq J^8=0\).  The kernel is central and the quotient
is cyclic, so the closed cube subgroup is abelian.  Both branches are
impossible.  Therefore every nilpotent associative
\(\mathbb F_3\)-algebra \(J\) with \(J^9=0\) whose raw cube set is a
nonabelian subgroup satisfies
\[
\dim_{\mathbb F_3}J\ge12.                        \tag{6.11b}
\]
See `DIM11_CLOSURE_AWARE_STATUS.md`.

At dimension twelve, exact positive-composition enumeration gives 582
in-scope profiles.  Applying only the proved structural and closure filters
used above leaves eight explicit branch inputs.  The length-six fibre lemma
extends without an \(A_6\)-rank hypothesis and excludes
\((2,2,2,2,2,2)\).  A filtered cross-relation commutator argument excludes
\((2,2,2,2,2,1,1)\), and the exact quadratic closure lemma excludes
\((2,2,2,3,1,1,1)\).  The other five obey the stricter necessary contracts
in `DIM12_CLOSURE_TRIAGE.md`.  One of those five is further reduced to 48
necessary graded cases, all of whose strict homogeneous quotients have
commuting cubes; only filtered terminal deformations remain.  This does not
exclude dimension twelve or establish realizability; the initial ledger is
in `DIM12_NEXT_FRONTIER.md`.

For the 15-dimensional two-string algebra with \(A^4=B^4=BA=0\), all
ideal quotients are excluded: if \(A^3B^3\) is killed, all cubes commute;
if it survives, the two cubes \(1+A^3\) and \(1+B^3\) do not commute but
their product is not a cube.  The proof, including the coefficient
obstruction and an exhaustive \(3^{15}\)-element audit, is in
`ALGEBRA_GROUP_P3_BARRIERS.md`.

These results do not settle the odd-prime question.  Within the
\(J^9=0\) algebra-group model, they prove that
subgroup/quotient repairs of the most natural class-six witness and its
associated algebra model are exhausted, exclude dimensions through ten
by cube commutativity, and exclude dimension eleven once raw-cube
closure is imposed.

The finite \(p=3\) order boundary was also pushed one full catalogue layer.
All \(1{,}396{,}077\) groups of order \(3^8\) were scanned.  Exactly 221
have nonabelian cube-generated subgroup and 63 have non-powerful
cube-generated subgroup, but all 63 have strictly fewer raw cubes than the
order \(243\) subgroup they generate.  Thus no order-\(3^8\) group is a
Wilson counterexample, and the complete smaller-order scans give the
computer-assisted implication
\[
 G\text{ a finite \(3\)-group counterexample}
 \quad\Longrightarrow\quad |G|\ge3^9.             \tag{6.12}
\]
This is only a \(p=3\) finite-order lower bound.  The exact three-shard
certificate and independent direct check of \(H'\nleq H^3\) are in
`ORDER6561_COMPLETE_WILSON_AUDIT.md`.

Now suppose \(U\le Z(A)\cap A'\) and \(U<A'\).  Write \(u=|U|\),
\(d=|A'|\), and \(z=|Z(A)|\).  Closure in (6.3) would require
\[
  |A|d^{p-1}-\sum_C|C|^p=u^p-u.
\]
But every class has size at most \(d\), while the \(z\) central singleton
classes alone give
\[
\begin{aligned}
 |A|d^{p-1}-\sum_C|C|^p
   &\ge z(d^{p-1}-1)
    \ge u(d^{p-1}-1)\\
   &\ge p^{p-1}u^p-u
    >u^p-u,
\end{aligned}
\]
because a proper subgroup of the \(p\)-group \(A'\) has index at least \(p\).
This contradiction proves
\[
  U=P_p(A)\le Z(A)\cap A',\quad U<A'
  \quad\Longrightarrow\quad
  P_p(A\wr C_p)\text{ is not closed}.
\]

Moreover, (6.1) is invariant under multiplication by the central diagonal
\(\Delta U\).  Both the \(p\)-th-power-value count and the order of its generated
subgroup are divided by \(|U|\) in the quotient.  Therefore
\[
 P_p(W/\Delta U)\text{ is closed}
 \quad\Longleftrightarrow\quad
 P_p(W)\text{ is closed}.
\]
If \(A\) has exponent \(p^2\), the diagonal quotient has exponent \(p^2\)
but can never repair closure.  If \(A\) has class two and \(U=A'\), the
resulting \(p\)-th-power subgroup is abelian because its derived subgroup
before quotienting is \(\Delta A'\).  The full proof and the \(p=3\)
exhaustive orders-\(27\)-through-\(729\) audit are in
`ODD_DIAGONAL_QUOTIENT_NO_GO.md`.

More strongly, assume the positive case of (6.4), with
\(\exp(A)=p^2\).  Then
\[
 H=P_p(W)\cong A\times U^{p-1},\qquad
 H'=\Delta U,\qquad \exp(W)=p^3.
\]
For any \(N\trianglelefteq W\) with \(\exp(W/N)\le p^2\), choose
\(a\in A\) for each \(u=a^p\in U\).  Since
\[
 ((a,1,\ldots,1)t)^{p^2}=\Delta u,
\]
one has \(\Delta U\le N\).  Power values commute with quotient maps, so
\[
 P_p(W/N)=HN/N
\]
is a subgroup whose derived subgroup is \(H'N/N=1\).  Thus no quotient that
lowers this closed wreath family into the exponent-\(p^2\) regime can retain
a nonabelian \(p\)-th-power subgroup.  A standalone proof is in
`CENTRAL_POWER_WREATH_CRITERION.md`.

## 7. Complete SmallGroups result through order 128

The independent table audit traverses every GAP SmallGroups isomorphism type
at orders
\[
  1,2,4,8,16,32,64,128,
\]
whose catalogue counts are respectively
\[
  1,1,2,5,14,51,267,2328.
\]
For every one of the \(2669\) Cayley tables, Python/NumPy independently
reconstructs the identity, inverses, element orders, exponent, square values,
closure, noncommutativity, derived subgroup, and Frattini subgroup, and checks
all \(n^3\) associativity triples.  GAP separately evaluates the semantic
predicates.  The two routes must agree or the run fails closed.

The completed result is:

- no hit at any order below \(128\);
- exactly ten hits of order \(128\):
  \[
    \operatorname{SmallGroup}(128,i),\qquad 928\leq i\leq937.
  \]

Thus \(128\) is the minimum possible order of a finite 2-group of exponent
exactly \(8\) whose square values form a nonabelian subgroup.

All ten groups have
\[
  P_2(G)=G'=\Phi(G),\quad |P_2(G)|=16,\quad
  G/G'\cong C_2^3,
\]
nilpotency class \(4\), generator rank \(3\), and center of order \(2\).
Their square subgroups split into two types:

- IDs \(928,\ldots,933\): \(P_2(G)\cong C_2\times D_8\);
- IDs \(934,\ldots,937\): \(P_2(G)\cong C_2\times Q_8\).

Their automorphism-group orders are
\[
\begin{array}{c|r|r|r|r}
i&\#|x|=2&\#|x|=4&\#|x|=8&|\operatorname{Aut}(G_i)|\\\hline
928&43&68&16&512\\
929&27&84&16&256\\
930&27&84&16&512\\
931&35&76&16&512\\
932&35&76&16&256\\
933&19&92&16&512\\
934&35&44&48&1536\\
935&19&60&48&512\\
936&27&52&48&512\\
937&11&68&48&1536
\end{array}
\]
For every type the lower-central-series orders are
\[
  128,16,4,2,1,
\]
and the derived-series orders are
\[
  128,16,2,1.
\]
The wreath-product endpoints are
\[
  G_{928}\cong D_8\wr C_2,\qquad
  G_{937}\cong Q_8\wr C_2.
\]

### A common central quotient

The ten catalogue entries admit a much cleaner common description.  Define
\[
\begin{aligned}
Q=\langle q_1,\ldots,q_6\mid\;&q_i^2=1\ (1\leq i\leq6),\\
 &[q_2,q_1]=q_4,\quad [q_3,q_1]=q_5,\\
 &[q_4,q_3]=q_6,\quad [q_5,q_2]=q_6,\\
 &[q_i,q_j]=1\text{ for every other }i>j\rangle .
\end{aligned}
\]
Collection in this presentation gives
\[
  |Q|=64,\quad \exp(Q)=4,\quad \operatorname{cl}(Q)=3,\quad
  |Z(Q)|=2,\quad |Q'|=8.
\]
For reference only, its SmallGroups label is \([64,138]\); the presentation,
not that label, defines \(Q\).

The exhaustive order-\(128\) result has the following structural
reformulation:
\[
\boxed{
\begin{array}{c}
|G|=128,\ \exp(G)=8,\ P_2(G)\text{ a nonabelian subgroup}
\\[2mm]\Longleftrightarrow\\[2mm]
|Z(G)|=2,\quad G/Z(G)\cong Q.
\end{array}}
\]
There are exactly ten such central extensions.  In each one
\[
  Z(G)\leq G',
\]
so it is a stem central extension of \(Q\) by \(C_2\), and
\[
  G/\gamma_3(G)\cong\operatorname{SmallGroup}(32,27).
\]
This equivalence is a catalogue-assisted classification theorem: the
explicit presentation makes the shared quotient conceptual, while the
assertion that these are all extensions with the stated order and center is
certified by the complete scan in `validate_order128_structure.g`.

Only the two endpoints are ordinary wreath products.  Indeed a group
\(A\wr C_2\) of order \(128\) forces \(|A|=8\).  Running over the five
isomorphism types of order-eight seeds gives SmallGroups IDs
\[
  67,\ 628,\ 928,\ 937,\ 1578,
\]
so the intersection with the ten counterexamples is exactly
\(\{928,937\}\).  The other eight groups are central relator twists of the
same quotient rather than additional ordinary wreath products.

There is also a common wreath-like internal skeleton.  Every one of the ten
groups has a unique nilpotency-class-two maximal subgroup \(B\) and an
outside involution \(t\) such that
\[
\begin{gathered}
  G=B\rtimes\langle t\rangle,\qquad
  Z(B)=B'=\Phi(B)\cong C_2^2,\qquad
  B/Z(B)\cong C_2^4,\\
  B/Z(G)\cong E_+:=D_8\mathbin{\circ}D_8,\qquad
  Z(G)=G''=\gamma_4(G)\cong C_2,\qquad
  [B,t]=G'.
\end{gathered}
\]
Here \(E_+\) is the extraspecial plus-type group of order \(32\).  The eight
outside involutions form one conjugacy class.  Their fixed subgroup in \(B\)
is \(D_8\) for IDs \(928,\ldots,933\) and \(Q_8\) for IDs
\(934,\ldots,937\), matching
\[
  G'\cong C_2\times D_8
  \quad\text{or}\quad
  G'\cong C_2\times Q_8.
\]
Only the endpoint bases split directly:
\[
  B_{928}\cong D_8\times D_8,\qquad
  B_{937}\cong Q_8\times Q_8;
\]
the other eight distinguished bases are directly indecomposable.

### Central-lift presentation classification

Let \(g_1,\ldots,g_7\) be the GAP pc generators and use
\([x,y]=x^{-1}y^{-1}xy\).  Put \(z=g_7\).  Omitted commutators are
trivial.  In every presentation below, quotienting by \(\langle z\rangle\)
gives the displayed presentation of \(Q\).

For IDs \(928,\ldots,933\), the common relations are
\[
\begin{aligned}
&g_1^2=g_4^2=g_5^2=g_6^2=g_7^2=1,\quad
g_2^2=g_7^a,\quad g_3^2=g_7^b,\\
&[g_2,g_1]=g_4,\quad[g_3,g_1]=g_5,\quad[g_6,g_1]=g_7,\\
&[g_5,g_2]=g_6g_7,\quad[g_4,g_3]=g_6,\quad[g_5,g_4]=g_7,\\
&[g_3,g_2]=g_7^c.
\end{aligned}
\]
The parameters \((a,b,c)\) for IDs \(928,\ldots,933\) are, in order,
\[
  000,\ 100,\ 110,\ 001,\ 101,\ 111.
\]

For IDs \(934,\ldots,937\), the common relations are
\[
\begin{aligned}
&g_1^2=g_6^2=g_7^2=1,\quad g_4^2=g_5^2=g_7,\quad
g_2^2=g_7^a,\quad g_3^2=g_7^b,\\
&[g_2,g_1]=g_4,\quad[g_3,g_1]=g_5,\\
&[g_4,g_1]=[g_5,g_1]=[g_6,g_1]=g_7,\\
&[g_4,g_2]=g_7,\quad[g_5,g_2]=g_6g_7,\\
&[g_4,g_3]=g_6,\quad[g_5,g_3]=g_7,\quad[g_5,g_4]=g_7,\\
&[g_3,g_2]=g_7^c.
\end{aligned}
\]
The parameters for IDs \(934,\ldots,937\) are
\[
  000,\ 100,\ 001,\ 111.
\]
All eight binary triples give valid groups in each lift pattern, but several
triples are isomorphic.  In lexicographic order
\[
  000,001,010,011,100,101,110,111,
\]
the resulting catalogue IDs are
\[
\begin{array}{c|cccccccc}
\text{\(D\)-pattern}&928&931&929&932&929&932&930&933\\
\text{\(Q\)-pattern}&934&936&935&936&935&936&935&937.
\end{array}
\]
Consequently the two relation patterns produce exactly six and four
isomorphism types, respectively, and together exhaust all ten central
extensions above.  This is more than a list of catalogue pc presentations:
it is a constructive classification as two central-lift patterns with three
binary relator twists.  It is not being claimed here that these three bits
are a full coordinate system for a cohomology group.

The \(6+4\) collapse itself has a finite generator-orbit explanation.  Write
\(\varepsilon=0\) for the \(D\)-pattern and \(\varepsilon=1\) for the
\(Q\)-pattern.

- For \(\varepsilon=0\), normalized generator changes fix \(c\) and act on
  \((a,b)\) by the transposition \(a\leftrightarrow b\).  For each value of
  \(c\), the weights \(0,1,2\) give three orbits, hence \(2\cdot3=6\).
- For \(\varepsilon=1\), put
  \[
    w=(a+c,b+c)\in\mathbb F_2^2.
  \]
  Normalized generator changes realize all of
  \(\operatorname{GL}(2,2)\) on \(w\), while fixing \(c\).  For each \(c\)
  there are the two orbits \(w=0\) and \(w\ne0\), hence \(2\cdot2=4\).

`validate_order128_parameter_orbits.g` exhausts the six ordered bases of
\(\mathbb F_2^2\), permits all derived-factor corrections, verifies every
defining relation after the change, and asserts exactly these orbit
partitions.  This is a finite relation-level orbit proof; a cohomological
interpretation via an explicit automorphism action on \(H^2(Q,C_2)\) remains
open.

The same relation calculation gives a further structural split.  The special
maximal subgroup \(B\) is Camina,
\[
  x^B=xB'\qquad(x\notin B'),
\]
exactly when \(c+\varepsilon=1\).  This selects precisely IDs
\(931,\ldots,935\).

### The order-64 boundary and power-closure hierarchy

Among all 2-groups below order \(128\), the only exponent-eight groups with
nonabelian Frattini subgroup are
\[
  \operatorname{SmallGroup}(64,i),\qquad i=32,33,36,37.
\]
For each, the set of squares has 12 elements and generates the nonabelian
Frattini subgroup of order 16, but is not itself closed.  The first two have
\(\Phi(G)\cong C_2\times D_8\), and the last two have
\(\Phi(G)\cong C_2\times Q_8\).

Every one of the ten order-\(128\) groups contains these boundary failures as
maximal subgroups: the \(D\)-pattern groups have two maximal subgroups of type
32 or 33, and the \(Q\)-pattern groups have three of type 36 or 37.  On the
other hand, inside each order-\(128\) group itself,
\[
  |V_2(G)|=|\langle V_2(G)\rangle|=16,\qquad
  |V_4(G)|=|\langle V_4(G)\rangle|=2,
\]
and higher \(2^k\)-power sets are trivial.  Thus each of the ten groups is
weakly power closed in the single-group sense, but none is section-wise power
closed.  This supplies a concrete firewall between the KOU property and the
stronger historical terminology.

## 8. Reproducibility

From the repository root:

```bash
python3 data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/verify_smallgroups_classification.py

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_wreath_criterion_smallgroups.g

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_wreath_families.g

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_semiextraspecial_square_surjectivity.g

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_odd_wreath_p3.g

python3 -m unittest -v \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/test_exponent_p_all_quotients_p3.py

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_order128_structure.g

/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap \
  -l /home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap -q \
  data/research_open/q1_eight_hour_campaign_2026-07-29/kou21137/validate_order128_parameter_orbits.g
```

The first command creates a canonical JSON certificate, a compressed raw
Cayley-table stream, and an independent GAP predicate transcript under
`kou21137/artifacts/`.  Software versions, script hashes, raw-stream hashes,
per-order counts, all group outcomes, and the ten positive records are stored
in the certificate.

## 9. Publication assessment

The mathematical package is materially stronger than a one-off computational
counterexample and is suitable for conversion into a focused group-theory
preprint.  A defensible paper would center the unrestricted prime-wreath
criterion, the at-most-five-class classification of all finite seeds for
every prime, the all-quotients exponent-\(p\) semi-extraspecial no-go, and
the central-power exponent-lowering quotient no-go.
The semi-extraspecial 2-group classification, perfect-nonlinear square-map
bridge, explicit families, and the order-\(128\) certified minimum-order
classification would support that centerpiece.

“CAS 1区” cannot be guaranteed from the present work.  Before submission the
following are still essential:

1. an expert, theorem-by-theorem proof audit;
2. authorized full-text checks of Mann (2005), Theorem 16, Bennett's 2012
   thesis, Macdonald (1986), and Verardi (1987), plus a broader
   MathSciNet/zbMATH novelty search, especially for square maps on
   semi-extraspecial groups and square values in \(A\wr C_2\);
3. a clean manuscript that explicitly separates the April 2026 prior
   counterexample from the new structural results;
4. ideally, a cohomological derivation of the finite \(6+4\) generator-orbit
   calculation, and a dedicated priority search for the central-power
   criterion and quotient obstruction.
