# Prime-power values in \(A\wr C_p\): an exact criterion

Date: 2026-07-29

## Theorem

Let \(p\) be a prime and \(A\) an arbitrary group.  Put
\[
  Q=P_p(A)=\{a^p:a\in A\},\qquad W=A\wr C_p.
\]
Then \(P_p(W)\) is a subgroup if and only if exactly one of the following
conditions holds:

1. \(Q=A\);
2. \(Q<A\), \(Q=A'\), and
   \[
     x^A=xA'\qquad(x\notin A').                    \tag{1}
   \]

In the second case
\[
  P_p(W)
  =
  \{(a_0,\ldots,a_{p-1})\in A^p:
    a_0A'=\cdots=a_{p-1}A'\},                      \tag{2}
\]
the fiber product of \(p\) copies of \(A\) over \(A/A'\).

Condition (1) is the Camina condition when \(A\) is nonabelian.  The theorem
also includes the abelian exponent-\(p\) case: then \(Q=A'=1\), (1) holds,
and the power subgroup is the diagonal copy of \(A\).

No finiteness or centrality hypothesis is used.

## Proof

### Exact value set

Let \(\mathcal C(A)\) be the set of conjugacy classes of \(A\).  The
coordinate calculation for every nontrivial top coset gives
\[
  S:=P_p(W)
    =Q^p\cup\bigcup_{C\in\mathcal C(A)}C^p.        \tag{3}
\]
Set powers here are Cartesian powers.

To recall why all \(p-1\) nontrivial top cosets give the same set, fix a
generator \(t\) of \(C_p\).  In \(A^pt^k\), \(1\le k<p\), the \(p\)-th-power
coordinates are cyclic rotations of the product of the base entries read
with step \(k\).  Since \(k\) is invertible modulo \(p\), every position is
visited once.

For completeness, the converse has no hidden compatibility condition.
First take \(k=1\) and prescribe arbitrary conjugates
\(c_0,\ldots,c_{p-1}\) of one element.  Choose
\(a_0,\ldots,a_{p-2}\) successively so that
\[
 c_{i+1}=a_i^{-1}c_i a_i\qquad(0\le i<p-1),
\]
put \(a=a_0\cdots a_{p-2}\), and set
\[
 a_{p-1}=a^{-1}c_0.
\]
Then \(a_0\cdots a_{p-1}=c_0\), and the \(i\)-th cyclic rotation of this
product is \(c_i\), since consecutive rotations are related by conjugation
by \(a_i\).  Thus every ordered tuple in \(C^p\) occurs.  For general
\(k\ne0\), reindex the base coordinates by multiplication by
\(k\pmod p\).  This proves (3).

### Generated subgroup

Let
\[
  V=\langle Q\rangle A'.
\]
The power tuples include \(Q^p\), so they generate
\(\langle Q\rangle^p\).  The conjugacy-class tuples include \(\Delta A\);
comparing a tuple with its diagonal counterpart independently in one
coordinate generates \((A')^p\).  Conversely, every conjugate of \(x\)
belongs to \(xA'\).  Therefore
\[
  H:=\langle S\rangle=\Delta A\,V^p.               \tag{4}
\]
The product on the right is a subgroup because \(V\trianglelefteq A\).

### Coordinate-axis rigidity

For a fixed coordinate \(i\), let \(E_i(X)\) denote the copy of \(X\) on
that coordinate axis.  From (3),
\[
  S\cap E_i(A)=E_i(Q).                             \tag{5}
\]
Indeed, \(Q^p\) gives \(E_i(Q)\), while a tuple from \(C^p\) with every other
coordinate equal to \(1\) must have \(C=\{1\}\).

From (4),
\[
  H\cap E_i(A)=E_i(V).                             \tag{6}
\]
One inclusion is immediate from \(V^p\le H\).  For the reverse inclusion,
write an axis element as a diagonal tuple times a \(V^p\)-tuple.  Any one of
the \(p-1\) identity coordinates forces the diagonal entry into \(V\), and
then the remaining coordinate also lies in \(V\).

If \(S\) is a subgroup, then \(S=H\).  Equations (5)--(6) yield
\[
  Q=V.                                             \tag{7}
\]
Thus closure itself forces the raw power-value set \(Q\) to be a subgroup
containing \(A'\).

If \(Q=A\), condition 1 holds.  Suppose \(Q<A\), and fix \(x\notin Q\).
Since \(Q=V\), the generated group contains
\[
  (x,xq_1,\ldots,xq_{p-1})
\]
for arbitrary \(q_i\in Q\).  It equals \(S\), and the displayed tuple is not
in \(Q^p\), so (3) puts all its coordinates in the conjugacy class \(x^A\).
Consequently
\[
  xQ\subseteq x^A\subseteq xA'\subseteq xQ,
\]
where the last inclusion uses \(A'\le Q\).  Hence \(x^A=xQ\).  For every
\(q\in Q\), the conjugacy of \(xq\) and \(x\) gives
\(q=x^{-1}x^g\in A'\).  Therefore \(Q=A'\), proving necessity of condition
2.

Conversely, condition 1 makes the first term \(Q^p\) in (3) equal to all of
\(A^p\).  Under condition 2, \(Q^p=(A')^p\) is the identity fiber, while
each class \(x^A=xA'\) supplies the full Cartesian power of a nonidentity
\(A'\)-coset.  Formula (3) is therefore exactly (2), a subgroup.  This proves
the theorem.

## Finite consequences

For finite \(A\), condition \(Q=A\) is equivalent to \(p\nmid|A|\).  If
\(p\nmid|A|\), choose \(r\) with \(pr\equiv1\pmod{\exp(A)}\).  Conversely,
if \(p\mid|A|\), Cauchy's theorem gives a nonidentity element with \(p\)-th
power one, so the finite power map is not injective and hence not
surjective.

For a nontrivial finite \(p\)-group, only condition 2 can occur.  Thus
\[
\boxed{
 P_p(A\wr C_p)\text{ is a subgroup}
 \iff
 P_p(A)=A'\text{ as sets and }A\text{ satisfies the Camina condition}.}
\]

The square theorem in `THEOREM_DRAFT.md` is the case \(p=2\).  The central
criterion and the exponent-lowering quotient obstruction in
`CENTRAL_POWER_WREATH_CRITERION.md` are consequences with the additional
hypothesis \(P_p(A)\le Z(A)\), which is needed only for the later structural
and exponent calculations.
