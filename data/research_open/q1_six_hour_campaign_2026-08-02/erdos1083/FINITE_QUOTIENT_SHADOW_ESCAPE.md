# Erdős #1083: finite-quotient shadows and the first aperiodic escape

Date: 2026-08-02

Status: **PROVED — INDEPENDENT CROSS-AUDIT PASSED AFTER SCOPE REPAIR**

## 0. Outcome

The cyclic-shadow argument in
CYCLOTOMIC_SIMULTANEOUS_POSITIVE_MULTIPLE_BOUND.md does not fundamentally
require an interval source. It requires the centre mask to tile a finite
quotient.

Let \(\Gamma=\Gamma_0\oplus\Gamma_1\), let
\(F_0\in\mathbb Z[\Gamma_0]\) be an \(S\)-term mask, and suppose that
there are a finite abelian quotient

\[
 \pi:\Gamma_0\longrightarrow G
\tag{0.1}
\]

and a mask \(Y\subseteq G\) such that

\[
 \boxed{\pi(F_0)P_Y=P_G:=\sum_{g\in G}[g]}
\tag{0.2}
\]

coefficientwise. Thus \(\pi(\operatorname{supp}F_0)\oplus Y=G\) is an
exact finite tiling.

If \(R\in\mathbb Z[\Gamma]\) may be signed but

\[
 B=F_0R
\tag{0.3}
\]

is a nonzero \(0/1\) mask with \(R(1)=C>0\), then finite-quotient compression
produces a nonnegative integral shadow \(K\in\mathbb Z[\Gamma_1]\) with

\[
 \boxed{K(1)=C.}
\tag{0.4}
\]

Every factor \(H\in\mathbb Z[\Gamma_1]\) of \(B\) remains a factor of
\(K\). Consequently, for prime \(S\) and the same-line cyclotomic leaf
family below, the quadratic bound

\[
 |{\cal D}|\le 1+2\sum_{r=2}^C\varphi(r)\le C^2
\tag{0.5}
\]

continues to hold whenever the common centre mask has such a
finite-quotient tiling.

This extension has a sharp boundary. Put

\[
 \boxed{
 F_0=1+x+x^4,\qquad
 R=1-x^4+x^5+x^7.}
\tag{0.6}
\]

Then

\[
 \boxed{
 F_0R=1+x+x^6+x^7+x^9+x^{11}}
\tag{0.7}
\]

is a \(0/1\) mask, although \(R\) is signed and

\[
 R(1)=2<3=F_0(1).
\tag{0.8}
\]

But \(1+x+x^4\) has no root-of-unity zero. Hence
\(X=\{0,1,4\}\) tiles no finite cyclic quotient, and indeed no finite
abelian quotient of \(\mathbb Z\). Thus no theorem based only on a finite
tiling shadow can handle every contaminated quotient. This three-term,
two-augmentation identity is the first exact aperiodic escape.

## 1. Finite-quotient shadow theorem

### Theorem 1.1

Under (0.1)--(0.3), extend \(\pi\) as the identity on \(\Gamma_1\).
There is a nonnegative integral \(K\in\mathbb Z[\Gamma_1]\) such that

\[
 \boxed{
 P_Y\pi(B)=P_GK,\qquad K(1)=C.}
\tag{1.1}
\]

If \(H\in\mathbb Z[\Gamma_1]\) and \(H\mid B\), then

\[
 \boxed{H\mid K.}
\tag{1.2}
\]

#### Proof

By (0.2),

\[
 P_Y\pi(B)
 =P_Y\pi(F_0)\pi(R)
 =P_G\pi(R).
\tag{1.3}
\]

The left side has nonnegative integer coefficients: projection can only
merge coefficients of the \(0/1\) mask \(B\), and multiplication by
\(P_Y\) preserves nonnegativity. In a finite group ring, multiplication
by \(P_G\) makes the coefficient of every \(g\in G\) equal. Therefore
the right side of (1.3) has the unique form \(P_GK\), where \(K\) is
nonnegative integral.

Because \(|G|=S|Y|\), augmentation in (1.1) gives

\[
 |Y|SC=|G|K(1),
\]

and hence \(K(1)=C\).

If \(B=HT\), then

\[
 P_GK=P_Y\pi(B)=H\,P_Y\pi(T).
\tag{1.4}
\]

The factor \(H\) is independent of the \(G\)-coordinate. Compare the
coefficient of any one \(g\in G\) in (1.4); it gives \(K=H K'\) for an
integral Laurent polynomial \(K'\). This proves (1.2). QED.

The prime cyclic shadow is the special case

\[
 G=\mathbb Z/S\mathbb Z,\qquad
 \pi(F_0)=P_G,\qquad Y=\{0\}.
\tag{1.5}
\]

Theorem 1.1 also works for composite \(S\), noncyclic \(G\), and a
nontrivial finite tiling complement \(Y\).

## 2. Cyclotomic consequence

Assume now that \(S\) is prime, and retain the same-line leaf masks

\[
 F_m=P_S(y^m),\qquad m\mid M,\qquad S\nmid M,
\tag{2.1}
\]

but replace the interval centre \(P_S(x)\) by any \(S\)-term centre
\(F_0\) satisfying (0.2). Let

\[
 R_m=\frac{F_M}{F_m}Q
\tag{2.2}
\]

and suppose every \(F_0R_m\) is a mask with \(1\le R_m(1)=C<S\).

For \(m,n\), put \(g=(m,n)\), \(a=m/g\), and \(b=n/g\). Exactly as in
the cyclotomic quadratic-bound theorem,

\[
 H_{S,a}(y^g)\mid R_n,\qquad
 H_{S,b}(y^g)\mid R_m.
\tag{2.3}
\]

Theorem 1.1 extracts from \(F_0R_n\) a nonnegative \(C\)-mass shadow
still divisible by \(H_{S,a}(y^g)\). The sharp positive-multiple mass
lemma gives

\[
 C\ge\min\{S,a\}.
\tag{2.4}
\]

Thus \(a,b\le C\), and the Farey count proves (0.5). Signed and
direction-contaminated \(R_m\)'s are allowed throughout.

## 3. The aperiodic signed escape

Expanding (0.6) gives

\[
\begin{aligned}
 (1+x+x^4)(1-x^4+x^5+x^7)
 &=1+x+x^4-x^4-x^5-x^8\\
 &\quad+x^5+x^6+x^9+x^7+x^8+x^{11}\\
 &=1+x+x^6+x^7+x^9+x^{11},
\end{aligned}
\tag{3.1}
\]

so (0.7)--(0.8) are exact.

It remains to prove that \(F_0\) has no torsion zero. Suppose
\(\zeta\) is a root of unity and

\[
 1+\zeta+\zeta^4=0.
\tag{3.2}
\]

Three unit complex numbers sum to zero only when they are the vertices of
a centred equilateral triangle. Since one of them is \(1\), the set
\(\{1,\zeta,\zeta^4\}\) would have to be
\(\{1,\omega,\omega^2\}\), where \(\omega\) is a primitive cube root.
In particular \(\zeta\) would be a primitive cube root. But then
\(\zeta^4=\zeta\), contradicting the required three distinct vertices.
Thus (3.2) is impossible.

Now suppose \(X=\{0,1,4\}\) tiled a finite cyclic group
\(\mathbb Z/N\mathbb Z\) with complement \(Y\). At every nontrivial
\(N\)-th root \(\xi\), Fourier transform of the tiling identity gives

\[
 F_0(\xi)P_Y(\xi)=0.
\tag{3.3}
\]

The first factor never vanishes, so every nontrivial Fourier coefficient
of \(1_Y\) vanishes. Fourier inversion makes \(1_Y\) constant, equal to
\(|Y|/N=1/3\), impossible for a \(0/1\) function.

Finally, the image of \(\mathbb Z\) in any finite abelian quotient is
cyclic. If \(X\) tiled the whole quotient, restriction to any coset of
that cyclic image would make \(X\) tile the cyclic image itself. This
reduces the general finite-abelian case to the contradiction above.

The source size \(S=3\) is minimal for this obstruction. Every two-point
set \(\{u,u+d\}\) in a torsion-free finitely generated abelian group has
a finite cyclic quotient in which its image tiles: choose an integer
homomorphism nonzero on \(d\), and reduce modulo twice the resulting
nonzero difference.

## 4. Exact boundary

Theorem 1.1 closes every same-line cyclotomic family whose centre is a
finite-quotient translational tile. Identity (0.6) proves that this
hypothesis cannot be deleted: even an aperiodic three-term centre can
hide a signed quotient of augmentation \(2<3\) inside a positive mask.

The escape is one row, not a power-large simultaneous family and not a
counterexample to Erdős #1083. It identifies the next minimal algebraic
gate precisely:

> control simultaneous signed positive multiples for aperiodic centre
> masks which have no finite-quotient tiling shadow.

Such a theorem must use interactions among many quotients, or a different
positive functional; torsion-character compression alone is insufficient.

## 5. Reproduction

~~~bash
python3 verify_finite_quotient_shadow_escape.py
python3 -m unittest -v test_finite_quotient_shadow_escape.py
~~~

The verifier checks a nontrivial finite-quotient tiling shadow with factor
preservation, the exact signed escape, 256 torsion orders, the two-point
minimality models, and the endpoint quadratic gap. The all-parameter
statements are proved above.
