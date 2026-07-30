# Complete classification of finite wreath seeds

Date: 2026-07-29

## Theorem

For a finite group \(A\), let
\[
  P_2(A)=\{a^2:a\in A\},\qquad W=A\wr C_2.
\]
Then \(P_2(W)\) is a subgroup if and only if \(A\) belongs to exactly one of
the following five classes:

1. \(A\) has odd order;
2. \(A\) is a nontrivial elementary abelian 2-group;
3. \(A\) is a nonabelian semi-extraspecial 2-group;
4. \(A=K\rtimes\langle t\rangle\) is generalized dihedral, where \(K\ne1\)
   is finite abelian of odd order, \(t^2=1\), and \(t\) acts on \(K\) by
   inversion;
5. \(A=K\rtimes Q_8\) is a Frobenius group, where \(K\ne1\) is finite
   abelian of odd order and \(Q_8\) acts fixed-point-freely on \(K\).

The trivial group is included in class 1.  The qualifications above make the
five classes disjoint.

## 1. Reduction to Camina groups

The wreath criterion proved in `THEOREM_DRAFT.md` says that \(P_2(W)\) is a
subgroup exactly when \(P=P_2(A)\) is a subgroup and
\[
  x^A=xP\qquad(x\notin P).                         \tag{1}
\]

If \(P=A\), finiteness gives precisely class 1.  Indeed, odd order makes
squaring surjective: choose \(r\) with
\(2r\equiv1\pmod{\exp(A)}\), so \(g=(g^r)^2\).  Conversely, if \(|A|\) is
even, the identity and an involution have the same square, so the square map
on the finite set \(A\) cannot be surjective.

Suppose \(P<A\).  The wreath criterion further gives
\[
  P=A',\qquad x^A=xA'\quad(x\notin A').             \tag{2}
\]
Thus \(A/A'\) is elementary abelian of exponent two, and, when \(A\) is
nonabelian, \(A\) is a Camina group.

We now apply the finite Camina classification: a nonabelian finite Camina
group is either a Camina \(p\)-group, a Frobenius group with cyclic
complement, or a Frobenius group with quaternion complement.  This is the
Dark--Scoppola theorem in the corrected proof framework of Lewis and
Isaacs--Lewis; see the references below.

## 2. Necessity in the three Camina branches

### The \(p\)-group branch

If \(A\) is abelian, (2) gives \(P=A'=1\), so every element has square one
and \(A\) is elementary abelian of order a power of two: class 2.

Now suppose \(A\) is nonabelian and a \(p\)-group.  The nontrivial
\(p\)-group \(A/A'\) has exponent two, so \(p=2\).  Macdonald's theorem says
that every Camina 2-group has class two; Verardi's equivalence then says that
it is semi-extraspecial.  This is class 3.

### The cyclic-complement branch

Write \(A=K\rtimes H\), with Frobenius kernel \(K\) and cyclic complement
\(H\).  Since \(A/K\cong H\) is abelian, \(A'\leq K\).  Conversely, for a
generator \(1\ne h\in H\), coprime action gives
\[
  K=[K,h]C_K(h)=[K,h],
\]
because the Frobenius action has \(C_K(h)=1\).  Hence \(K=A'\).
Now \(A/A'\cong H\) has exponent two, so \(H\cong C_2\).

Let \(t\) be its involution.  The Frobenius action makes \(t\) fixed-point-free
on \(K\).  The following standard argument is included to avoid hiding the
kernel structure behind a citation.  For an involutory fixed-point-free
automorphism \(\alpha\), the map
\[
  f(x)=x^{-1}\alpha(x)
\]
is injective: \(f(x)=f(y)\) implies \(yx^{-1}=\alpha(yx^{-1})\), hence
\(x=y\).  It is therefore surjective on finite \(K\).  Writing every
\(k=x^{-1}\alpha(x)\) gives
\[
  \alpha(k)=\alpha(x)^{-1}x=k^{-1}.
\]
Thus inversion is an automorphism of \(K\), so \(K\) is abelian.  It has odd
order, since an involution in \(K\) would be fixed by inversion.  We obtain
class 4.

### The quaternion-complement branch

Write \(A=K\rtimes Q_8\), and let \(z\) be the unique involution of \(Q_8\).
The same fixed-point-free-involution argument shows that \(K\) is abelian of
odd order and that
\[
  z(k)=k^{-1}\qquad(k\in K).                       \tag{3}
\]
This is class 5.  It also gives the useful derived-subgroup formula
\[
  A'=K\rtimes\langle z\rangle.                     \tag{4}
\]
Indeed, for every \(1\ne h\in Q_8\), the endomorphism \(1-h\) of \(K\) is
injective and hence onto, so \([K,Q_8]=K\); also \(Q_8'=\langle z\rangle\).

These arguments exhaust the Camina classification and prove necessity.

## 3. Sufficiency

Classes 1 and 2 satisfy (1) immediately.  In class 3, the square map is onto
\(Z(A)=A'\), and the semi-extraspecial/Camina condition gives
\(x^A=xA'\) off \(A'\).

For class 4, every element of \(K\) is a square because \(|K|\) is odd,
whereas
\[
  (kt)^2=k\,t(k)=1.
\]
Hence \(P_2(A)=K=A'\).  Also
\[
  (kt)^K=Kt,
\]
because conjugation varies the \(K\)-coordinate by a square and squaring is
bijective on \(K\).  Thus (1) holds.

It remains to check class 5 carefully.  Use additive notation for the
abelian group \(K\).  Equations (3)--(4) give
\[
  A'=K\rtimes\langle z\rangle.
\]
Squares of elements of \(K\) cover \(K\), and elements of \(Kz\) square to
one.  If \(h\in Q_8\) has order four, then
\[
  (k,h)^2=((1+h)k,z).                              \tag{5}
\]
The endomorphism \(1+h\) is invertible, because
\[
  (1-h)(1+h)=1-h^2=1-z=2,
\]
and multiplication by two is an automorphism of the odd-order group \(K\).
Consequently (5) covers all of \(Kz\), and
\[
  P_2(A)=K\cup Kz=A'.                              \tag{6}
\]

Finally, if \(h\in Q_8\) has order four, then \(1-h\) is invertible on \(K\);
therefore every \(kh\) is conjugate by an element of \(K\) to \(h\).
The Frobenius condition gives \(C_K(h)=1\), while
\(C_{Q_8}(h)=\langle h\rangle\), so
\[
  C_A(h)=\langle h\rangle,\qquad |h^A|=2|K|=|A'|.
\]
The class lies in its \(A'\)-coset because \(A/A'\) is abelian.  Therefore
\(x^A=xA'\) for every \(x\notin A'\), and (1) proves sufficiency.

## 4. Exhaustive SmallGroups cross-check

`validate_finite_seed_classification.g` independently scans every one of the
3,596 SmallGroups types of every order from 1 through 128.  For each group it
computes the square-value set and checks the exact wreath criterion.  A
separate route recognizes:

- odd order;
- elementary abelian 2-groups;
- semi-extraspecial 2-groups via special and conjugacy-class conditions;
- the generalized-dihedral and quaternion branches via the Fitting subgroup,
  quotient type, and fixed-point-free action.

The two decisions must agree or the script stops.  The successful certificate
is

```text
FINITE_SEEDS|orders=1..128|groups=3596|criterion=164|class_counts=[ 107, 7, 11, 38, 1 ]|q8_hits=[ [ 72, 41 ] ]
DONE
```

Thus the five classes contribute respectively \(107,7,11,38,1\) types in
this range.  The first quaternion-complement example is
\(\operatorname{SmallGroup}(72,41)\).

## 5. Literature status

- M. L. Lewis,
  [“Classifying Camina groups: a theorem of Dark and Scoppola”](https://arxiv.org/abs/0807.0167),
  records the three-branch classification and gives an alternate proof.
- R. Dark and C. M. Scoppola, “On Camina Groups of Prime Power Order,”
  *Journal of Algebra* **181** (1996), 787--802,
  [doi:10.1006/jabr.1996.0146](https://doi.org/10.1006/jabr.1996.0146).
- I. M. Isaacs and M. L. Lewis,
  [“Camina \(p\)-groups that are generalized Frobenius complements”](https://arxiv.org/abs/1411.3278),
  *Archiv der Mathematik* **104** (2015), 401--407,
  [doi:10.1007/s00013-015-0755-4](https://doi.org/10.1007/s00013-015-0755-4),
  supplies the corrected general argument forcing the quaternion case.
- J. D. Dixon and B. Mortimer, *Permutation Groups*, Graduate Texts in
  Mathematics 163, Springer, 1996, Theorem 3.4A, is a standard reference for
  the fact that a Frobenius group with even-order complement has abelian
  kernel.  The elementary fixed-point-free-involution proof needed here was
  given above.

The Camina classification, Macdonald class-two theorem, Verardi equivalence,
and Frobenius kernel facts are prior results.  The candidate contribution is
their exact synthesis with the wreath square-closure criterion.  A dedicated
citation-chain audit is still required before asserting priority.
