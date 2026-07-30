# OPG-1757: all-rank falling-triangle factors and recurrence degrees

Date: 2026-07-30

## 0. Result

This note combines the cubic-degree theorem for the ordinary symbols
with the Poisson--Newton triangle.  It explains two patterns that were
previously visible only in the first five computed ranks:

1. the \(j\)-th falling-basis coefficient has exact degree \(3j\),
   alternating leading sign, and \(j\) consecutive forced zeros; and
2. the \(q\)-th long-recurrence band is a polynomial of degree at most
   \(3q+2\), with one forced zero for \(q\ge1\).

This note by itself asserts no full-band positivity beyond the first
five bands.  The subsequently derived and independently audited
`ORDINARY_SIXTH_LONG_RECURRENCE_BAND_THEOREM.md` proves the sixth band
on its whole admissible range, while
`ORDINARY_ALL_RANK_RECURRENCE_LEADING_POSITIVITY_THEOREM.md` proves
positive leading coefficients at every rank.

## 1. Falling-basis coefficients

Let
\[
P_d(k)=b_{k,d}
=\sum_{r=0}^{d}\beta_{d,r}k^{d-r}
\tag{1}
\]
and expand at \(k=n+2\):
\[
\boxed{
P_d(n+2)
=
\sum_{j=0}^{d}h_{d,j}(n)_{\underline{d-j}}.
}
\tag{2}
\]
Equivalently, if
\[
A_d(z)=e^{-z}\sum_{n\ge0}P_d(n+2)\frac{z^n}{n!},
\qquad
A_d(x^2)=x^dH_d(x),
\]
then
\[
H_d(x)=
\sum_{j=0}^{\lfloor d/2\rfloor}h_{d,j}x^{d-2j}.
\tag{3}
\]

The all-rank cubic-degree theorem gives polynomials
\[
\beta_{d,r}=P_r(d),
\qquad
\deg P_r=3r,
\qquad
(-1)^r[d^{3r}]P_r(d)>0
\quad(d\ge r).
\tag{4}
\]
For fixed \(j\), use (4) in the ordinary-to-falling triangular
identity to define the polynomial extension
\[
\mathfrak h_j(d)
\in\mathbb Q[d],
\qquad
\mathfrak h_j(d)=h_{d,j}\quad(d\ge j).
\tag{5}
\]

### Theorem 1 (all-rank forced falling factor)

For every \(j\ge1\),
\[
\boxed{
\deg\mathfrak h_j=3j,
\qquad
(-1)^j[d^{3j}]\mathfrak h_j(d)>0,
\qquad
\prod_{m=j}^{2j-1}(d-m)
\ \bigm|\ \mathfrak h_j(d).
}
\tag{6}
\]
Thus
\[
\boxed{
\mathfrak h_j(d)
=
\left(\prod_{m=j}^{2j-1}(d-m)\right)R_j(d),
\qquad
\deg R_j=2j,
\qquad
(-1)^j[d^{2j}]R_j(d)>0.
}
\tag{7}
\]

### Proof

Let \(s_\ell(n)=s(n,n-\ell)\) be a near-diagonal signed
Stirling polynomial of the first kind.  Comparing the coefficient of
\(n^{d-\ell}\) in (2) gives
\[
\mathfrak h_\ell(d)
=
\sum_{r=0}^{\ell}
P_r(d)\binom{d-r}{\ell-r}2^{\ell-r}
-
\sum_{j=0}^{\ell-1}
\mathfrak h_j(d)s_{\ell-j}(d-j).
\tag{8}
\]
The polynomial \(s_m(n)\) has degree \(2m\).  Induction in \(\ell\)
now gives
\[
\deg\mathfrak h_\ell
\le
\max_{0\le r\le\ell}\{3r+\ell-r\}
\le3\ell;
\]
the second sum has degree at most
\[
3j+2(\ell-j)=2\ell+j\le3\ell.
\]

The degree-\(3\ell\) contribution is unique.  In the first sum of
(8), the term \(r=\ell\) is exactly \(P_\ell(d)\).  Every term with
\(r\le\ell-1\) has degree at most
\[
3r+\ell-r=\ell+2r\le3\ell-2,
\]
whereas every term in the second sum has degree at most
\[
3j+2(\ell-j)=2\ell+j\le3\ell-1
\qquad(j\le\ell-1).
\]
Therefore
\[
[d^{3\ell}]\mathfrak h_\ell(d)
=[d^{3\ell}]P_\ell(d).
\tag{8a}
\]
The exact degree and alternating leading sign in (6) now follow from
the all-rank ordinary-symbol theorem.

For an integer \(d\) with
\[
j\le d\le2j-1,
\]
the coefficient in (2) is the Newton coefficient at falling degree
\[
d-j<\left\lceil\frac d2\right\rceil.
\]
The forced zero of \(A_d(z)\) at the origin therefore gives
\[
h_{d,j}=0.
\tag{9}
\]
All formulas \(P_r(d)\) used in (8) are valid because
\(d\ge j\ge r\).  Hence (9) consists of \(j\) genuine zeros of the
polynomial extension \(\mathfrak h_j\).  This proves the divisibility
in (6).  The forced product is monic of degree \(j\), so (8a) also
proves the exact quotient degree and leading sign in (7). \(\square\)

For \(j=1,\ldots,5\), the forced factors are
\[
(d-1),\quad
(d-2)(d-3),\quad
(d-3)(d-4)(d-5),\quad\ldots,
\]
exactly matching the independent finite formulas.

## 2. Long-recurrence bands

The monic parity basis has a unique expansion
\[
xH_d-H_{d+1}
=
\sum_{q=0}^{\lfloor(d-1)/2\rfloor}
\gamma_{d,q}H_{d-1-2q}.
\tag{10}
\]
For fixed \(q\), define its polynomial extension by the triangular
formula
\[
\boxed{
\mathfrak g_q(d)
=
\mathfrak h_{q+1}(d)-\mathfrak h_{q+1}(d+1)
-
\sum_{i=0}^{q-1}
\mathfrak g_i(d)
\mathfrak h_{q-i}(d-1-2i).
}
\tag{11}
\]
For \(d\ge2q+1\), all terms are actual coefficients and
\[
\mathfrak g_q(d)=\gamma_{d,q}.
\tag{12}
\]

### Theorem 2 (all-rank recurrence degree and forced boundary zero)

For every \(q\ge0\),
\[
\boxed{\deg\mathfrak g_q\le3q+2.}
\tag{13}
\]
For every \(q\ge1\),
\[
\boxed{
(d-2q)\mid\mathfrak g_q(d),
\qquad
\deg\frac{\mathfrak g_q(d)}{d-2q}\le3q+1.
}
\tag{14}
\]

### Proof

The finite difference of \(\mathfrak h_{q+1}\), whose degree is at
most \(3q+3\), has degree at most \(3q+2\).  Assuming (13) below
rank \(q\), each product in (11) has degree at most
\[
(3i+2)+3(q-i)=3q+2.
\]
This proves (13) by induction.

Now let \(q\ge1\) and put \(d=2q\).  The first two terms of (11) are
\[
\mathfrak h_{q+1}(2q),
\qquad
\mathfrak h_{q+1}(2q+1),
\]
and both vanish by Theorem 1 because
\[
q+1\le2q,2q+1\le2(q+1)-1.
\]
For \(0\le i<q\), put \(j=q-i\).  The remaining falling coefficient
is evaluated at
\[
d-1-2i=2j-1,
\]
which is again the last forced zero in (6).  Hence every summand in
(11) vanishes and
\[
\mathfrak g_q(2q)=0.
\]
Divisibility and the quotient-degree bound follow. \(\square\)

The case \(q=0\) is deliberately excluded from (14): its polynomial
extension is
\[
\mathfrak g_0(d)=\frac{(d+1)(11d+43)}6
\]
and need not agree with a nonexistent band at \(d=0\).

## 3. Relation to the positivity problem

Theorems 1--2 explain the boundary-factor pattern for every rank.  The
subsequent theorem
`ORDINARY_ALL_RANK_RECURRENCE_LEADING_POSITIVITY_THEOREM.md` upgrades
(13) to
\[
\deg\mathfrak g_q=3q+2,\qquad
[d^{3q+2}]\mathfrak g_q(d)>0
\quad(q\ge0).
\]
It does not prove positivity on the whole admissible domain.  The
independent theorem
`ORDINARY_FIRST_FIVE_LONG_RECURRENCE_BANDS_THEOREM.md` proves
\[
\mathfrak g_q(d)>0
\qquad
(0\le q\le4,\ d\ge2q+1).
\]
The remaining all-domain sign problem is
\[
\boxed{
\frac{\mathfrak g_q(d)}{d-2q}>0
\quad
(q\ge1,\ d\ge2q+1),
}
\tag{15}
\]
for residual polynomials now known to have exact degree \(3q+1\) and
positive leading coefficient.

There is a sharper exact reduction for just the highest coefficient.
If
\[
L_j=[d^{3j}]\mathfrak h_j(d),\qquad
G_q=[d^{3q+2}]\mathfrak g_q(d),
\]
and
\[
H(z)=\sum_{j\ge0}L_jz^j,\qquad
\widetilde G(z)=\sum_{q\ge0}G_qz^{q+1},
\]
then leading-term comparison in (11) gives
\[
\boxed{\widetilde G(z)H(z)=-3zH'(z).}
\tag{16}
\]
Thus \(G_q>0\) for every \(q\) is equivalent to strict negativity of
all nonconstant coefficients of \(\log H(z)\).  The exact derivation
and a rational search through \(q=299\) are recorded in
`ORDINARY_LONG_RECURRENCE_LEADING_REDUCTION_LEMMA.md`.  No
counterexample is found, but the logarithmic sign condition remains
unproved.

Even a proof of (15) would still require a compatibility theorem to
deduce real-rootedness from the long recurrence.  The algebraic
degree/factor theorem and the analytic interlacing step remain
logically distinct.

## 4. Verification

`verify_all_rank_falling_triangle_corollary.py` checks the degree
recurrences, forced-factor ranges, and the exact \(j\le5\),
\(q\le4\) instances.  Its finite checks audit the indexing; the
arbitrary-rank result is the proof above together with the all-rank
ordinary-symbol degree theorem.
