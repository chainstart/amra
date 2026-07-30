# Arbitrary-height energy dichotomy for synchronized equal-radius fibres

Date: 2026-07-30.

## 1. Statement

Let \(m\) distinct coaxial circles have one common radius \(\rho>0\)
and heights
\[
z_0<z_1<\cdots<z_{m-1}.
\]
Put the same set of \(S\) distinct angular positions on every circle.
No progression or short-arc hypothesis is imposed.  After choosing one
of the common positions as angle zero, define
\[
A=\{(z_i-z_0)^2:0\leq i<m\}
\tag{1}
\]
and
\[
X=\{2\rho^2(1-\cos(k\theta)):0\leq k<S\}.
\tag{2}
\]
The set \(A+X\) is contained in the squared-distance set (including
zero).  Hence the number \(D\) of nonzero distances is at least
\(|A+X|-1\); this harmless subtraction is understood in all asymptotic
consequences below.

For a finite real set \(A\), define its largest nonzero difference
multiplicity by
\[
\lambda(A)=
\max_{t\ne0}|\{(a,b)\in A^2:a-b=t\}|
=\max_{t\ne0}|A\cap(A+t)|.
\tag{3}
\]

### Theorem 1 (arbitrary-height energy dichotomy)

Under the setup above,
\[
\boxed{
|A+X|
\ge
\frac{m^2S^2}{2mS+\lambda(A)S^2}.
}
\tag{4}
\]
Equivalently,
\[
|A+X|\gg
\min\left\{mS,\frac{m^2}{\lambda(A)}\right\}.
\tag{5}
\]

Thus one does not need consecutive heights.  Either the synchronized
equal-radius slice already expands, or the anchored squared heights
have a nonzero translate overlapping in many points.

At \(m=S\), (4) reads
\[
|A+X|\ge\frac{m^2}{\lambda(A)+2}.
\tag{6}
\]
In particular, if
\[
\lambda(A)\le m^{1/2-\delta},
\]
then
\[
|A+X|\ge m^{3/2+\delta-o(1)}.
\tag{7}
\]
For the critical parametrization \(m=S=t^2\), \(N=t^5\), this becomes
\[
D\ge N^{3/5+(2/5)\delta-o(1)}.
\tag{8}
\]

The theorem is unconditional inside the synchronized slice.  It is
not an unconditional estimate for arbitrary \(N\)-point sets, because
the inherited proof tree has not yet supplied a sufficiently reused
common angular set on a large equal-radius class.

## 2. Proof

Although \(X\) is written as a set, retain the \(S\) indexed layers
\[
x_k=2\rho^2(1-\cos\beta_k).
\]
Distinct angular points imply that each cosine, and hence each \(x\)
value, occurs at most twice.

Let
\[
r(y)=|\{(a,k)\in A\times\{0,\ldots,S-1\}:a+x_k=y\}|.
\]
Then
\[
\sum_y r(y)=mS.
\tag{9}
\]
The energy \(\sum_y r(y)^2\) counts
\[
a+x_k=b+x_l.
\tag{10}
\]
The \(k=l\) terms contribute \(mS\).  Ordered off-diagonal pairs with
\(x_k=x_l\) contribute at most another \(mS\), because every layer
value has multiplicity at most two.

If \(x_k\ne x_l\), the number of solutions of (10) for this fixed
ordered layer pair is
\[
|A\cap(A+x_l-x_k)|\le\lambda(A).
\]
There are fewer than \(S^2\) ordered layer pairs.  Therefore
\[
\sum_y r(y)^2\le2mS+\lambda(A)S^2.
\tag{11}
\]
Cauchy--Schwarz applied to (9) gives (4).

## 3. Polynomial-range lattice heights

The consecutive-height result in `SUMSET_EXPANSION_ATTACK.md` is a
special case of a much broader corollary.

### Corollary 2 (lattice-height escape)

Suppose
\[
z_i=z_0+h u_i,\qquad
0=u_0<u_1<\cdots<u_{m-1}\le H,
\]
where \(h>0\) and the \(u_i\) are integers.  Then
\[
\lambda(A)\le
\max_{1\le n\le H^2}\tau(n),
\tag{12}
\]
and consequently
\[
|A+X|
\ge
\frac{m^2S^2}
{2mS+S^2\max_{n\le H^2}\tau(n)}.
\tag{13}
\]
If \(H\le m^C\) for a fixed \(C\), the divisor bound gives
\[
|A+X|\gg
\min\{mS,m^{2-o(1)}\}.
\tag{14}
\]
In particular, \(m=S=t^2\) gives \(D\ge N^{4/5-o(1)}\) inside the
critical full construction \(N=t^5\).

To prove (12), divide differences in \(A\) by \(h^2\).  Every
representation of a nonzero difference is
\[
u_i^2-u_j^2=(u_i-u_j)(u_i+u_j)=n,
\qquad0<|n|\le H^2.
\]
After swapping \(i,j\) if needed, a positive divisor of \(|n|\)
determines the two factors and hence \(u_i,u_j\).  There are at most
\(\tau(|n|)\) possibilities.

The coordinate bound matters.  Merely knowing that the heights lie in
some lattice, with exponentially or arbitrarily large \(H\), does not
turn the standard estimate \(\tau(n)=n^{o(1)}\) into \(m^{o(1)}\).

## 4. Quantitative inverse statement

Let \(U=|A+X|\).  Rearranging the lower energy bound
\((mS)^2/U\) against (11) gives
\[
\boxed{
\lambda(A)\ge \frac{m^2}{U}-\frac{2m}{S}.
}
\tag{15}
\]
At \(m=S\), a hypothetical bound
\[
U\le m^{3/2+\eta}
\]
forces
\[
\lambda(A)\ge m^{1/2-\eta}-2.
\tag{16}
\]
Thus the remaining height obstruction is explicit: there must be a
nonzero \(t\) and at least \(m^{1/2-\eta}-2\) pairs satisfying
\[
(z_i-z_0)^2-(z_j-z_0)^2=t.
\tag{17}
\]

This is a genuine narrowing, but not by itself a contradiction.  Over
arbitrary real heights, large \(\lambda(A)\) is possible: one may put
many pairs \(u_j,\sqrt{u_j^2+t}\) into the height-offset set.  The next
bridge must therefore use either:

1. several popular shifts with compatibility across radius classes;
2. arithmetic/height complexity inherited from the original point set;
3. or the simultaneous angular collision relations, not only one
   popular height shift.

## 5. Relation to the earlier proof tree

The old equal-radius semiconvex estimate
\[
D\gg S\sqrt m
\]
uses only \(|A|=m\).  Theorem 1 replaces it by
\[
D\gg
\min\{mS,m^2/\lambda(A)\}.
\]
It is stronger whenever the squared-height difference multiplicity is
small enough.  At the critical \(m=S\) scale:

- \(\lambda(A)\le m^{1/2-\delta}\) gives a fixed exponent gain;
- polynomial-range lattice heights give the near-product \(N^{4/5-o(1)}\);
- only the high-correlation branch
  \(\lambda(A)\ge m^{1/2-o(1)}\) remains.

This changes the extraction target from “find consecutive heights and
an angular progression” to the weaker dichotomy “find a heavy radius
class with sufficient angular-column reuse and either low
square-difference multiplicity or a compatible high-correlation
network.”  Even complete angular synchronization can be weakened
further to the sparse incidence condition in
`SPARSE_ANGLE_INCIDENCE_EXPANSION.md`.

## 6. Claim status

- Theorem 1, Corollary 2, and (15) are human proofs.
- The verifier checks arbitrary rational height sets, repeated angular
  layers, lattice subsets, and deliberately high-\(\lambda\) examples.
- No finite test is used as a premise.
- No unconditional improvement of \(f_3(N)\) is claimed.
