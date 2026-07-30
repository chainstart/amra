# First active base-four Newton layer: an exact theorem

Date: 2026-07-30

## 1. Statement

Let \(K_s\) have two fixed disjoint edges \(e,f\).  For
\(h=0,1,2\), let
\[
\Phi_h(x)=\sum_{j\ge0}\phi_{h,j}(s)x^j
\]
be the forest polynomial after contracting \(h\) of the fixed matching
edges and deleting their forced edge factors.  Equivalently,
\(\phi_{h,j}(s)\) counts forests of \(K_s\) which contain the prescribed
\(h\)-edge matching and have \(j+h\) edges in total.

Put
\[
C_k(s)=[x^k]\bigl(\Phi_1(x)^2-\Phi_0(x)\Phi_2(x)\bigr)
\]
and use the normalization inherited from the complete-split reduction,
\[
c_k(s)=\frac{k!}{2k(k-1)}C_k(s),\qquad k\ge2.
\]
Expand in the natural base-four Newton basis:
\[
c_k(s)=\sum_{q=0}^{2k-4}a_{k,q}\binom{s-4}{q}.
\]

Set
\[
q_0=\left\lfloor\frac{k-2}{2}\right\rfloor.
\]
Then
\[
a_{k,q}=0\qquad(0\le q<q_0),
\]
and the first possible coefficient is always strictly positive.  More
precisely:
\[
\boxed{
a_{k,q_0}=
\begin{cases}
2(k-2)!\left(\dfrac{k+5}{2}\right)^{k-3},
   &k\ \text{odd},\\[8pt]
\dfrac{(k-2)!}{2}(k^2+20k-12)
\left(\dfrac{k+6}{2}\right)^{k-4},
   &k\ \text{even}.
\end{cases}}
\tag{1}
\]
The even formula includes \(k=2\), where it evaluates to \(1\).

Thus the finite observation
\[
\min\{q:a_{k,q}\ne0\}
=\left\lfloor\frac{k-2}{2}\right\rfloor
\]
is now proved for every \(k\ge2\).

There is also an exact all-\(k\) result for the next layer.  If
\(q_1=q_0+1\), then
\[
a_{k,q_1}>0\qquad(k\ge3).
\tag{1a}
\]
More explicitly, put
\[
n=
\begin{cases}
(k+7)/2,&k\ \text{odd},\\
(k+8)/2,&k\ \text{even}.
\end{cases}
\]
For odd \(k\ge3\),
\[
\boxed{
a_{k,q_1}=(k-2)!(n-4)
\left[
(n^3+12n^2+20n-225)n^{2n-12}
-2(n-1)^{2n-10}
\right].
}
\tag{1b}
\]
For even \(k\ge4\), define
\[
Q(n)=n^5+16n^4+52n^3-587n^2-3063n+12240,
\quad R(n)=n^2+2n-27.
\]
Then
\[
\boxed{
a_{k,q_1}=(k-2)!(n-4)
\left[
\frac13Q(n)n^{2n-14}
-2R(n)(n-1)^{2n-12}
\right].
}
\tag{1c}
\]
For \(k=2\), \(c_2(s)=1\), so there is no second active layer.

## 2. The required one-, two-, and three-component counts

Write \(W_{h,c}(n)\) for the number of \(c\)-component spanning forests
of \(K_n\) containing a prescribed matching of size \(h\).  Contraction
identifies each prescribed edge to a vertex of weight \(2\), so
\[
\Phi_h(x)=\sum_{c\ge1}W_{h,c}(n)x^{n-h-c}.
\tag{2}
\]

For \(h=0,1,2\) and \(c=1,2,3\), the needed values are
\[
\begin{array}{c|ccc}
&c=1&c=2&c=3\\ \hline
h=0&
n^{n-2}&
\dfrac{(n-1)(n+6)}2n^{n-4}&
\dfrac{(n-2)(n-1)(n^2+13n+60)}8n^{n-6}\\[7pt]
h=1&
2n^{n-3}&
(n-2)(n+6)n^{n-5}&
\dfrac{(n-3)(n-2)(n^2+13n+60)}4n^{n-7}\\[7pt]
h=2&
4n^{n-4}&
2(n^2+3n-20)n^{n-6}&
\dfrac{(n-4)(n^3+10n^2+17n-210)}2n^{n-8}.
\end{array}
\tag{3}
\]

Here is a short derivation which also fixes the orbit and normalization
conventions.

The Liu--Chow complete-graph forest formula gives
\[
W_{0,c}(n)=n^{n-c-1}(n-1)!
\sum_{r=0}^{\min(c-1,n-c)}
\frac{(-1/(2n))^r(c+r)}
 {r!(c-r-1)!(n-c-r)!}.
\tag{4}
\]
Substitution of \(c=1,2,3\) gives the first row of (3).

Every \(c\)-component forest has exactly \(n-c\) edges.  Edge
transitivity therefore gives
\[
W_{1,c}(n)
=\frac{n-c}{\binom n2}W_{0,c}(n),
\tag{5}
\]
which is the second row.

For completeness, let \(A_c(n)\) count \(c\)-component forests
containing a prescribed adjacent edge pair.  Applying the same
Liu--Chow contraction formula to the resulting weight-\(3\) vertex
gives
\[
\begin{aligned}
A_1(n)&=3n^{n-4},\\
A_2(n)&=\frac{(n-3)(3n+20)}2n^{n-6},\\
A_3(n)&=\frac{(n-4)(n-3)(3n^2+43n+210)}8n^{n-8}.
\end{aligned}
\tag{6}
\]
There are
\[
N_{\rm adj}=\frac{n(n-1)(n-2)}2,\qquad
N_{\rm dis}=\frac{n(n-1)(n-2)(n-3)}8
\]
unordered adjacent and disjoint edge pairs in \(K_n\), respectively.
Double-counting a forest together with an unordered pair of its
\(n-c\) edges gives
\[
N_{\rm adj}A_c(n)+N_{\rm dis}W_{2,c}(n)
=\binom{n-c}{2}W_{0,c}(n).
\tag{7}
\]
Substituting (3), (6) into (7) gives the third row of (3).
This proves every enumeration used below.

## 3. Odd \(k\)

Let \(k=2m+3\), so \(q_0=m\) and
\[
n_0=4+q_0=m+4,\qquad k=2n_0-5.
\]
In a term of (2), the exponent of \(x\) is \(n-h-c\).
Consequently, a product contributing to \(C_k(n_0)\) must have total
component count
\[
c_1+c_2=2n_0-2-k=3.
\]
Only the pairs \((1,2)\) and \((2,1)\) occur.  Hence
\[
\begin{aligned}
C_k(n_0)
={}&2W_{1,1}(n_0)W_{1,2}(n_0)\\
&-W_{0,1}(n_0)W_{2,2}(n_0)
-W_{0,2}(n_0)W_{2,1}(n_0).
\end{aligned}
\]
Using (3) and simplifying,
\[
\boxed{C_k(n_0)=4n_0^{\,2n_0-8}.}
\tag{8}
\]

## 4. Even \(k\)

Let \(k=2m+2\), so \(q_0=m\) and
\[
n_0=4+q_0=m+4,\qquad k=2n_0-6.
\]
Now the total component count is
\[
c_1+c_2=2n_0-2-k=4.
\]
The possible pairs are \((1,3),(2,2),(3,1)\), so
\[
\begin{aligned}
C_k(n_0)
={}&2W_{1,1}(n_0)W_{1,3}(n_0)+W_{1,2}(n_0)^2\\
&-W_{0,1}(n_0)W_{2,3}(n_0)
-W_{0,2}(n_0)W_{2,2}(n_0)
-W_{0,3}(n_0)W_{2,1}(n_0).
\end{aligned}
\]
Substitution of (3) yields
\[
\boxed{
C_k(n_0)=
4n_0^{\,2n_0-10}(n_0^2+4n_0-24).
}
\tag{9}
\]
Since \(n_0\ge4\), the last factor is positive.

## 5. Passage to the Newton coefficient

The already proved capacity cancellation gives
\[
c_k(4)=c_k(5)=\cdots=c_k(3+q_0)=0.
\tag{10}
\]
Therefore the \(q_0\)-th forward difference has only its final term:
\[
a_{k,q_0}=\Delta^{q_0}c_k(4)=c_k(4+q_0)=c_k(n_0).
\tag{11}
\]
Multiplying (8) or (9) by \(k!/(2k(k-1))=(k-2)!/2\), and replacing
\(n_0\) by \((k+5)/2\) or \((k+6)/2\), gives (1).

## 6. Scope

This is a human theorem, with the Liu--Chow enumeration formula as its
only external counting input.  The companion verifier independently
reconstructs (3) by recursively selecting the component of the first
weighted vertex and checks (8)--(11) over a finite regression range.
The finite regression is not a premise of the proof.

The result closes the first-support/strict-positivity node.  It does
**not** prove \(a_{k,q}\ge0\) for all \(q>q_1\), and therefore does not
yet prove the complete first-coefficient theorem or OPG-1757.

## 7. The second active layer

The same method goes one step further without a new combinatorial
ansatz.  Formula (4), edge transitivity (5), the adjacent-pair
contraction
\[
A_c(n)=
\sum_{r=0}^{c-1}
\frac{(-1)^r(c+r+2)(n-3)!n^{n-c-r-3}}
 {2^rr!(c-r-1)!(n-c-r-2)!},
\tag{12}
\]
and the pair-orbit identity (7) determine \(W_{h,c}\) for every fixed
\(c\).  Terms outside the factorial range are interpreted as zero.
Substitution through \(c=5\) gives the two exact determinant layers
\[
\begin{aligned}
\mathcal C_5(n)
&:=\sum_{c=1}^{4}
\bigl(W_{1,c}W_{1,5-c}-W_{0,c}W_{2,5-c}\bigr)\\
&=2(n-4)(n^3+12n^2+20n-225)n^{2n-12},
\tag{13}\\
\mathcal C_6(n)
&:=\sum_{c=1}^{5}
\bigl(W_{1,c}W_{1,6-c}-W_{0,c}W_{2,6-c}\bigr)\\
&=\frac23(n-4)Q(n)n^{2n-14}.
\tag{14}
\end{aligned}
\]

At \(s=n_0+1\), the total component count has increased by two.
The forward-difference formula and the vanishing below \(q_0\) give
\[
a_{k,q_0+1}
=\frac{k!}{2k(k-1)}
\left(C_k(n_0+1)-(q_0+1)C_k(n_0)\right).
\tag{15}
\]
For odd \(k\), insert (8) and (13) into (15); for even \(k\), insert
(9) and (14).  This is exactly (1b)--(1c).

It remains to prove the signs without appealing to numerical
evaluation.  In the odd case \(k=3\) gives \(a_{3,1}=10\) directly.
For \(n\ge6\),
\[
\left(1-\frac1n\right)^{2n-12}\le1
\]
and
\[
n^3+12n^2+20n-225-2(n-1)^2
=n^3+10n^2+24n-227>0.
\tag{16}
\]
This proves (1b) is positive.

In the even case \(k=4\) gives \(a_{4,2}=294\) directly.  For \(n\ge7\),
\[
\left(1-\frac1n\right)^{2n-14}\le1,
\]
while, on writing \(n=m+5\),
\[
\begin{aligned}
Q(n)-6(n-1)^2R(n)
={}&m^5+35m^4+502m^3\\
&+3123m^2+4556m+1107>0.
\end{aligned}
\tag{17}
\]
This proves (1c) is positive.  Thus (1a) is a human all-parameter
theorem; the finite checks in the verifier are again only regressions.
