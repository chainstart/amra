# Complete rational-angle escape in the critical coaxial subcase

Date: 2026-07-30

## 1. Result

Take \(m\) coaxial circles of common radius \(m\), at heights
\(0,\ldots,m-1\), and put the same angular progression
\[
\{0,\theta,\ldots,(S-1)\theta\}
\]
on every circle.  Squared distances with height difference \(d\) and
angular difference \(k\) are
\[
\delta_{d,k}=d^2+2m^2(1-\cos(k\theta)),
\qquad 0\le d<m,\quad 1\le k<S.
\tag{1}
\]

Suppose \(\cos\theta=a/b\in\mathbb Q\) is in lowest terms and
\(|a|<b\).

- If an odd prime \(p\mid b\), with \(e=v_p(b)\), then
  \[
  D\ge
  m\max\left\{0,S-1-
  \left\lfloor\frac{2v_p(m)}e\right\rfloor\right\}.
  \tag{2}
  \]
- If \(b=2^e\) with \(e\ge2\), then
  \[
  \boxed{
  D\ge
  m\max\left\{0,S-1-
  \left\lfloor\frac{2v_2(m)}{e-1}\right\rfloor\right\}.
  }
  \tag{3}
  \]

The first assertion is the odd-prime argument recorded in
`CRITICAL_ANISOTROPIC_GRID_BARRIER.md`.  The second assertion completes
the missing pure \(2\)-power denominator case.

Consequently every fixed rational cosine compatible with arbitrarily
long *distinct* angular progressions satisfies
\[
D\ge m(S-O(\log m)).
\tag{4}
\]
Indeed, the only reduced denominators not covered by (2)--(3) are
\(b=1,2\), which give
\(\cos\theta\in\{0,\pm\tfrac12\}\) under \(|a|<b\); their angular
orbits are periodic of bounded length.  At the critical specialization
\[
m=S=t^2,\qquad N=t^5
\]
inside the full anisotropic construction, (4) gives
\[
D\ge t^4-O(t^2\log t)=N^{4/5-o(1)}.
\tag{5}
\]

This classifies fixed rational cosines in the explicit critical
coaxial subcase.  It does **not** show that the inherited Erdős proof
tree produces a fixed rational angle, and hence is not an unconditional
improvement of \(f_3(N)\).

## 2. Exact \(2\)-adic denominator lemma

### Lemma

Let \(a\) be odd and \(e\ge2\).  For every \(k\ge1\),
\[
\boxed{
T_k\left(\frac{a}{2^e}\right)
=\frac{A_k}{2^{(e-1)k+1}},
\qquad A_k\ \text{odd}.
}
\tag{6}
\]

### Proof

Use the explicit Chebyshev expansion
\[
T_k(x)=
\frac{k}{2}\sum_{j=0}^{\lfloor k/2\rfloor}
\frac{(-1)^j}{k-j}\binom{k-j}{j}(2x)^{k-2j}.
\tag{7}
\]
The \(j=0\) term is \(2^{k-1}x^k\).  After substituting
\(x=a/2^e\) and multiplying by \(2^{(e-1)k+1}\), this term becomes
\(a^k\), which is odd.

For \(j\ge1\), put
\[
r_{k,j}=\frac{k}{k-j}\binom{k-j}{j}
=\binom{k-j}{j}+\binom{k-j-1}{j-1}\in\mathbb Z.
\tag{8}
\]
The corresponding contribution to the same common numerator is
\[
(-1)^j r_{k,j}a^{k-2j}2^{2j(e-1)},
\tag{9}
\]
which is even.  Thus the common numerator is odd, proving (6).
\(\square\)

It follows immediately that
\[
1-T_k(a/2^e)
=\frac{B_k}{2^{(e-1)k+1}},
\qquad B_k\ \text{odd}.
\tag{10}
\]

## 3. Proof of the distance bound

Multiplying (10) by \(2m^2\) gives
\[
v_2\!\left(2m^2(1-\cos(k\theta))\right)
=2v_2(m)-(e-1)k.
\tag{11}
\]
When
\[
k>\frac{2v_2(m)}{e-1},
\]
this valuation is negative.  Adding the integer \(d^2\) in (1)
does not change it.  Different usable values of \(k\) have different
valuations and hence give disjoint distance sets.  For a fixed \(k\),
the \(m\) values \(d^2\), \(0\le d<m\), are distinct.  Counting usable
\(k\)'s proves (3).

The same reasoning with an odd prime divisor of \(b\) proves (2):
the leading Chebyshev term is a \(p\)-adic unit after clearing \(b^k\),
while every lower term contains \(b^2\).  Thus
\[
v_p(1-T_k(a/b))=-kv_p(b),
\]
and (2) follows.

## 4. Scope and next target

The rational classification shows that the line-count extremizer is
not a distance extremizer for any fixed rational nonperiodic angle.
The remaining angular target is therefore genuinely irrational:

1. prove denominator/height growth for a Diophantine class of
   irrational cosines; or
2. show that failure of such growth forces an algebraic or
   approximate-resonance structure incompatible with the inherited
   joint-correlation hypotheses.

Neither implication is currently proved.
