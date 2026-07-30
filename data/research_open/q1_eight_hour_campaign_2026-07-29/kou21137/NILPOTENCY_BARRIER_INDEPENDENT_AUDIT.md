# Independent audit of the odd-\(p\) nilpotency barrier

Date: 2026-07-29

## Verdict

The class-at-most-\(p\) conclusion in
`ODD_KOU_NILPOTENCY_BARRIER.md` is valid, provided the standard Hall
polynomial lemma is stated precisely.  The purpose of this note is to make
the divisibility step independent of the informal “choose positions”
description.

Let \(F=\langle x,y\rangle\) be the free nilpotent group of class \(c\).
For a fixed Hall basis, collect
\[
 [x^m,y^n]=\prod_d d^{E_d(m,n)}.
\]
If the basic commutator \(d\) has bidegree \((r,s)\), then:

1. \(E_d(m,n)\) is integer-valued on
   \(\mathbb Z_{\geq0}^2\);
2. its degree in \(m\) is at most \(r\), and its degree in \(n\) is at most
   \(s\);
3. \(E_d(0,n)=E_d(m,0)=0\).

These are the standard weighted-degree properties of Hall collection.
They can also be proved by induction on Hall weight: multiplication by one
more \(x\) or \(y\) takes a finite difference in the corresponding
variable, and forming a commutator adds bidegrees.

Every integer-valued polynomial on
\(\mathbb Z_{\geq0}^2\) has a unique Newton expansion
\[
 E_d(m,n)=
 \sum_{i=0}^{r}\sum_{j=0}^{s}
 a_{ij}\binom mi\binom nj,\qquad a_{ij}\in\mathbb Z.
 \tag{1}
\]
Indeed,
\[
 a_{ij}=(\Delta_m^i\Delta_n^jE_d)(0,0).
\]
The two vanishing identities force \(a_{0j}=a_{i0}=0\).  Hence (1) reduces
to
\[
 E_d(m,n)=
 \sum_{i=1}^{r}\sum_{j=1}^{s}
 a_{ij}\binom mi\binom nj.                         \tag{2}
\]

Now assume \(c\leq p\) and put \(m=n=p\).  Every commutator occurring in
the collected word contains both letters, so \(r,s\geq1\).  Its weight is
\(r+s\leq p\), whence \(r,s\leq p-1\).  Every summand in (2) is divisible
by \(p^2\), because
\[
 p\mid\binom pi\quad(1\leq i\leq p-1).
\]
Thus \(p^2\mid E_d(p,p)\) for every Hall factor.  In every quotient of
exponent dividing \(p^2\), all these factors vanish, proving
\[
 [x^p,y^p]=1.
\]

## Scope correction

The unitriangular example at class \(2p\) proves only that two raw
\(p\)-th powers can fail to commute.  It does not prove closure of the
complete raw value set.  Accordingly, the interval
\[
 p+1\leq c_{\rm nc}(p)\leq2p
\]
is now explicitly attached to the noncommutativity-only threshold
\(c_{\rm nc}(p)\).  For an actual odd-prime KOU counterexample, the work
establishes the lower bound \(p+1\) but no finite upper bound.

## Remaining citation obligation

Before submission, the Hall-polynomial weighted-degree lemma above should
be cited to an exact theorem/lemma number in Hall or Struik, or included as
a short formal induction.  The divisibility deduction itself is complete;
the remaining issue is bibliographic precision, not a computational gap.
