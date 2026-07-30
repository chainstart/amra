# Independent audit: finite seeds at every prime

Date: 2026-07-29

Status: proof-level reduction.  The independent branch-recognition scan is
complete for \(p=2,3,5\) through order \(128\); an upstream
original-source check of the quoted class-three Camina exponent lemma
remains pending.

## Candidate classification

Fix a prime \(p\), let \(A\) be finite, and put \(W=A\wr C_p\).  The general
prime-wreath criterion reduces
\[
  P_p(W)=\{w^p:w\in W\}
\]
being a subgroup to a finite classification.  The resulting disjoint list is:

1. \(p\nmid |A|\);
2. \(A\) is a nontrivial elementary abelian \(p\)-group;
3. \(A\) is a nonabelian semi-extraspecial \(p\)-group for which the raw
   \(p\)-power map is onto
   \[
     A'=Z(A);
   \]
4. \(A=K\rtimes C_p\) is a Frobenius group with nontrivial kernel \(K\);
5. \(p=2\) and \(A=K\rtimes Q_8\) is a Frobenius group with nontrivial
   kernel \(K\).

In class 3, the extra surjectivity condition is automatic for \(p=2\).  For
odd \(p\), the class-two power map
\[
  A/A'\longrightarrow A',\qquad xA'\longmapsto x^p
\]
is linear, and surjectivity is a genuine additional condition.  In class 4
the kernel need not be abelian when \(p\) is odd.  In class 5 the
fixed-point-free central involution forces \(K\) to be abelian of odd order.

For \(p=2\), this specializes exactly to the five classes in
`FINITE_SEED_CLASSIFICATION.md`: the kernel in class 4 is then abelian of
odd order and the complement acts by inversion.

## Necessity audit

Let
\[
  Q=P_p(A)=\{a^p:a\in A\}.
\]
The unrestricted criterion gives either \(Q=A\), or
\[
  Q=A'<A,\qquad x^A=xA'\quad(x\notin A').          \tag{1}
\]

For finite \(A\), \(Q=A\) is equivalent to \(p\nmid|A|\).  This is class 1:
coprimality gives roots using an inverse of \(p\) modulo \(\exp(A)\), while
if \(p\mid|A|\), Cauchy's theorem makes the power map noninjective and hence
nonsurjective.

Suppose (1) holds.  If \(A\) is abelian, then \(Q=A'=1\), so \(A\) has
exponent \(p\).  This is class 2.

Now suppose \(A\) is nonabelian.  Equation (1) says precisely that \(A\) is
a Camina group and that \(A/A'\) has exponent \(p\).  Apply the
Dark--Scoppola classification.

### Camina prime-power branch

If \(A\) is a \(q\)-group, then the nontrivial group \(A/A'\) is both a
\(q\)-group and has exponent \(p\), so \(q=p\).

A Camina \(p\)-group has class two or three.  In the class-three case, the
standard structure theorem gives
\[
  A/A_3\ \text{of exponent }p.
\]
Consequently every \(p\)-th power lies in \(A_3\), whereas
\(A_3<A'\), contradicting \(Q=A'\).  Hence \(A\) has class two.

In class two, \(A'\le Z(A)\).  A central element outside \(A'\) would have a
singleton conjugacy class, contradicting (1), so \(Z(A)=A'\).  Also
\[
  \Phi(A)=A^pA'=A',
\]
because all \(p\)-th powers lie in \(A'\).  Thus \(A\) is special; the
class-two Camina condition is equivalent to being semi-extraspecial.  The
remaining equality \(Q=A'\) is exactly the surjectivity condition in
class 3.

For odd \(p\), \(A'\) has exponent \(p\), and
\[
  (xy)^p=x^py^p[y,x]^{\binom p2}=x^py^p.
\]
Thus the power map factors as a linear map \(A/A'\to A'\).  For \(p=2\),
the square map is quadratic rather than linear, but the
semi-extraspecial derivative condition makes it perfect nonlinear.  The
Fourier argument in `THEOREM_DRAFT.md`, equivalently the established
perfect-nonlinear fiber bound, proves that it is onto.

### Cyclic-complement Frobenius branch

Write \(A=K\rtimes H\), where \(H\) is cyclic.  In a Camina Frobenius group
of this type, \(A'=K\).  Since \(A/A'\cong H\) has exponent \(p\), one has
\[
  H\cong C_p.
\]
This is class 4.

### Quaternion-complement Frobenius branch

Here \(A=K\rtimes Q_8\) and
\[
  A/A'\cong Q_8/Q_8'\cong C_2^2.
\]
Its exponent must divide \(p\), forcing \(p=2\).  The central involution of
\(Q_8\) acts fixed-point-freely on \(K\); the standard bijectivity argument
for \(x\mapsto x^{-1}\alpha(x)\) shows that it acts by inversion.  Hence
inversion is an automorphism of \(K\), so \(K\) is abelian, and it has odd
order.  This is class 5.

These are all branches in the finite Camina classification.

## Sufficiency audit

Classes 1 and 2 follow immediately from the prime-wreath criterion.

Class 3 has \(P_p(A)=A'\) by hypothesis and is Camina, so the same criterion
applies.

For class 4, the fixed-point-free \(C_p\)-action implies \(p\nmid|K|\).
Hence the \(p\)-power map is surjective on \(K\), even when \(K\) is
nonabelian: if \(pr\equiv1\pmod{\exp(K)}\), then
\[
  k=(k^r)^p.
\]
Every \(p\)-th power in \(A\) lies in \(K\), because \(A/K\cong C_p\).
Therefore
\[
  P_p(A)=K=A'.
\]
For \(1\ne h\in C_p\), the map
\[
  K\longrightarrow K,\qquad y\longmapsto y^{-1}h(y)
\]
is injective: equality would give a nontrivial fixed point of \(h\).
It is therefore bijective.  Thus every element of \(Kh\) is conjugate to
\(h\), and similarly for every nonidentity complement coset.  Hence
\[
  x^A=xK=xA'\qquad(x\notin K),
\]
which proves sufficiency.

Class 5 was checked directly in `FINITE_SEED_CLASSIFICATION.md`.  If \(z\)
is the central involution of \(Q_8\), then
\[
  A'=K\rtimes\langle z\rangle.
\]
Squares in \(K\) cover \(K\), while for every order-four \(h\in Q_8\),
\[
  (k,h)^2=((1+h)k,z).
\]
The identity
\[
  (1-h)(1+h)=1-h^2=1-z=2
\]
on the odd-order abelian group \(K\) makes \(1+h\) invertible.  Squares
therefore cover \(Kz\), so \(P_2(A)=A'\).  The same fixed-point-free
calculation gives the Camina coset condition off \(A'\).

## Proof-risk register

The unrestricted wreath criterion itself passed the following independent
checks:

- the exact value-set formula was tested by enumerating actual wreath
  products at \(p=3\) and \(p=5\);
- the generated-subgroup formula was checked via coordinate axes, without
  assuming that \(Q\) is already a subgroup;
- both directions of the closure criterion are purely algebraic and do not
  use finiteness or centrality.

The finite classification has one remaining source obligation and one
completed computational check:

1. inspect an original source for the statement that a class-three Camina
   \(p\)-group has \(A/A_3\) of exponent \(p\), rather than relying only on
   Lewis's later open exposition;
2. **completed:** the independent SmallGroups recognizer checks all five
   branches for \(p=2,3,5\) across all 3,596 catalogue groups of orders at
   most \(128\); see `validate_general_prime_finite_seeds.g` and
   `COMPUTATIONAL_AUDIT.md`.

Until those two checks and the broader citation-chain audit are complete,
this file records a candidate general classification rather than a priority
claim.
