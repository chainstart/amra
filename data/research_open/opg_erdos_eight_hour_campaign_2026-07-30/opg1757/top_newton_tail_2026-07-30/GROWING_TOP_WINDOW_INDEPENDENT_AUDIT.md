# Independent red-team audit of the growing top-window theorem

Date: 2026-07-30

## Verdict after the Lemma 2 repair

\[
\boxed{\text{PASS}}
\]

The revised proof closes the two gaps identified in the first audit:

1. it gives a bivariate coefficient-norm estimate for a falling
   product whose length and initial point both vary; and
2. it imports the marked total-degree assertion explicitly, states
   the two required finite-difference bounds, and displays both levels
   of determinant cancellation.

I found no remaining mathematical gap in the growing-window argument.
In particular:

- the normalizations in (9a) and (9b) are exact;
- the Faulhaber--Newton--Stirling bookkeeping yields one absolute,
  \(\ell\)- and \(k\)-independent constant \(C\);
- the mixed binomial moment preserves the required degree and stays
  within the same coefficient-norm allowance;
- the \(4\)-Stirling bounds, equation (17), and the final growth
  estimate remain correct.

Two optional notation clarifications are recorded in Section 7.  They
do not affect the PASS verdict.

## 1. Independent check of (9a)

Let
\[
E_{\beta,r}(s):=E(s,s-\beta-r,r)
\]
denote the finite sum in (7), and set
\[
\widehat E_{\beta,r}(s)
=\frac{2^rr!}{s^r}E_{\beta,r}(s).
\]
The second term in the consecutive difference has degree \(r-1\) but
retains component parameter \(s-\beta-r\).  To express it as a hatted
profile of degree \(r-1\), its shift must satisfy
\[
s-\gamma-(r-1)=s-\beta-r,
\]
and therefore
\[
\gamma=\beta+1.
\]
Moreover,
\[
\frac{2^rr!}{s^r}
\bigl(E(s,s-\beta-r,r-1)\bigr)
=\frac{2r}{s}\widehat E_{\beta+1,r-1}(s).
\]
Consequently
\[
\boxed{
\widehat D_{\beta,r}(s)
=\widehat E_{\beta,r}(s)
-\frac{2r}{s}\widehat E_{\beta+1,r-1}(s)
}
\]
is exact.  The factor \(2r\), the one-unit loss, and the
\(\beta\mapsto\beta+1\) shift are all correct.

An independent symbolic implementation of the defining finite sums
checked this identity for
\[
0\le\beta\le4,\qquad 1\le r\le8,
\]
giving 40 exact polynomial identities.  This finite check supports
but is not needed for the algebraic derivation above.

## 2. Independent check of (9b)

Define
\[
\widehat F_{4,r-1}(s)
=s^{-(r-1)}(s-4)_{\underline{r-1}}.
\]
In the exceptional profile,
\[
E(s,s-3-r,r-1)
=E(s,s-4-(r-1),r-1)
=\frac{s^{r-1}}{2^{r-1}(r-1)!}
\widehat E_{4,r-1}(s).
\]
It follows directly that
\[
\begin{aligned}
&\frac{2^rr!}{s^{2r}}\,
4(s-4)_{\underline{r-1}}E(s,s-3-r,r-1)\\
&\qquad =
\frac{2^rr!\,4}{s^{2r}}\,
s^{r-1}\widehat F_{4,r-1}
\frac{s^{r-1}}{2^{r-1}(r-1)!}\widehat E_{4,r-1}\\
&\qquad =
\boxed{
\frac{8r}{s^2}\,
\widehat F_{4,r-1}(s)\widehat E_{4,r-1}(s)
}.
\end{aligned}
\]
Thus the exceptional term begins at loss two, and neither its factor
of \(8\) nor its power of \(s\) is missing.

The same independent implementation checked this identity exactly
for \(1\le r\le8\).

## 3. The effective coefficient-norm ledger

For
\[
P_{\beta,u}(t,r)
=[s^{t-u}](s-\beta-r)_{\underline t}
=(-1)^ue_u(\beta+r,\ldots,\beta+r+t-1),
\]
Newton's identities express \(P_{\beta,u}\) through
\[
S_v(t,r):=
\sum_{a=0}^{t-1}(\beta+r+a)^v,
\qquad 1\le v\le u.
\]

### Degree

The binomial theorem and Faulhaber's formula give
\[
\deg_{t,r}S_v\le v+1.
\]
A term of the partition expansion of \(e_u\), indexed by a partition
\(\lambda\vdash u\), is a product of \(\ell(\lambda)\) power sums.
Its degree is at most
\[
\sum_i(\lambda_i+1)
=u+\ell(\lambda)
\le2u.
\]
Hence
\[
\deg_{t,r}P_{\beta,u}\le2u.
\]

### Coefficient norm of each power sum

For \(0\le\beta\le5\), expanding
\((\beta+r+a)^v\) costs at most an exponential factor in \(v\).
Faulhaber's coefficients involve binomial coefficients and Bernoulli
numbers of order at most \(v\).  The uniform estimate
\[
|B_m|\le\frac{4m!}{(2\pi)^m}
\]
therefore gives an absolute \(c>0\) such that
\[
\|S_v\|_{\mathbb Q[t,r],1}
\le
\exp\!\bigl(c(v+1)\log(v+2)\bigr)
\tag{A}
\]
for every \(v\ge1\) and every allowed \(\beta\).

### Newton partition products

Coefficient \(\ell^1\)-norm is submultiplicative.  A partition product
therefore has norm at most
\[
\exp\!\left(
c\sum_i(\lambda_i+1)\log(\lambda_i+2)
\right)
\le
\exp\!\bigl(O(u^2\log(u+2))\bigr).
\]
The number of partitions and all rational combinatorial coefficients
in Newton's identities fit into another
\(\exp(O(u\log(u+2)))\) factor.  Thus, with one absolute \(C_0\),
\[
\boxed{
\|P_{\beta,u}\|_{\mathbb Q[t,r],1}
\le
\exp\!\bigl(C_0(u+1)^2\log(u+2)\bigr).
}
\]
The same argument, or the specialization \(t=r\) with fixed initial
point, covers the normalized outer falling product.

### The two Stirling basis changes

At loss \(u\), all \(t\)- and \(r\)-degrees are at most \(2u\).
Both kinds of Stirling numbers occurring in
\[
t^a\longleftrightarrow(t)_{\underline v},
\qquad
(r)_{\underline v}\longleftrightarrow r^q
\]
are bounded in absolute value by
\[
(2u)^{2u}.
\]
There are only \(O(u^2)\) relevant coefficients.  Hence both basis
changes together cost
\[
\exp(O(u\log(u+2))),
\]
which is smaller than, and therefore absorbed by, the square-exponent
allowance above.

Applying
\[
\sum_{t=0}^r
\binom rt2^{r-t}(-1)^t(t)_{\underline v}
=(-1)^v(r)_{\underline v}
\]
introduces no \(r\)- or \(k\)-dependent constant.  This proves the
claimed uniform norm bound for every normalized \(E\)-profile.

### Consecutive difference, exceptional term, and convolution

In (9a), multiplication by \(2r\) changes coefficient norm by at most
a factor two and shifts loss by one.  In (9b), multiplication by
\(8r\) changes it by at most a factor eight and shifts loss by two.
The bounded shifts \(0\le\beta\le5\) have already been included in
(A).

At total loss \(\ell\), the outer product, consecutive difference,
and exceptional product generate only \(O(\ell^2)\) truncated
convolution terms.  Since
\[
u^2\log(u+2)+(\ell-u)^2\log(\ell-u+2)
\le O(\ell^2\log(\ell+2)),
\]
all products, sums, fixed factors, and shifts are bounded by
\[
\boxed{
\|R_{\ell,h}\|_1
\le
\exp\!\bigl(C_1(\ell+1)^2\log(\ell+2)\bigr)
}
\]
with a single absolute \(C_1\), uniformly for \(h=0,1,2\).

This is now a sufficient proof of the effective coefficient norm; it
does not rely on testing finitely many losses.

## 4. Marked degree and the two cancellations

The revised manuscript explicitly imports the marked
cycle-inclusion--exclusion result
\[
\deg_r[h^v]R_{\ell,h}(r)\le\ell-v.
\]
For the three profiles used in the determinant this gives
\[
\deg_r(R_{\ell,1}-R_{\ell,0})\le\ell-1,
\]
\[
\deg_r(R_{\ell,2}-2R_{\ell,1}+R_{\ell,0})
\le\ell-2.
\]
Finite differences increase the specialized coefficient norm by at
most four.

Consequently, through \(r\)-degree \(\ell-1\),
\[
R_{\ell,h}=A_\ell+C_\ell+hB_\ell,
\]
where the degree-\(\ell\) part \(A_\ell\) and the \(h\)-independent
degree-\((\ell-1)\) part \(C_\ell\) do not depend on \(h\), while
\(\deg B_\ell\le\ell-1\).

At total profile loss \(L\):

1. the degree-\(L\) \(AA\) terms cancel pointwise;
2. the degree-\((L-1)\) \(AC\) and \(CA\) terms cancel pointwise;
3. the remaining degree-\((L-1)\) kernel is
   \[
   \sum_{\ell=0}^L
   \left(
   B_\ell(J)A_{L-\ell}(k-J)
   -
   A_\ell(J)B_{L-\ell}(k-J)
   \right),
   \]
   which is antisymmetric under
   \((J,\ell)\mapsto(k-J,L-\ell)\).

Since \(J\) and \(k-J\) have the same binomial distribution, the last
kernel has expectation zero.  The expected numerator therefore has
degree at most \(L-2\).

The mixed identity
\[
\mathbb E\!\left[
(J)_{\underline a}(k-J)_{\underline b}
\right]
=\frac{(k)_{\underline{a+b}}}{2^{a+b}}
\]
is exact.  The required ordinary/falling basis changes have order at
most \(L\), so their coefficient-norm cost is
\(\exp(O(L\log L))\), safely inside
\(\exp(O(L^2\log L))\).

With \(L=j+4\), division by \(2k(k-1)\) turns degree at most
\(L-2=j+2\) into the asserted
\[
|b_{k,j}|
\le
\exp(C(j+5)^2\log(j+5))k^j.
\]
No hidden constant depends on \(j\) or \(k\).

## 5. Downstream estimates

The first audit's positive findings remain unchanged.

### \(4\)-Stirling bounds

For \(T_{n,r}={n\brace n-r}_4\), selecting \(r\) disjoint pairs among
the \(n\) ordinary elements gives
\[
T_{n,r}\ge
\frac{(n)_{\underline{2r}}}{2^rr!}
\ge\frac{n^{2r}}{8^rr!}
\qquad(n\ge4r).
\]
Replacing every nonsingleton block by the star from its least element
injects the partitions into \(r\)-edge graphs on \(n+4\) vertices, so
\[
T_{n,r}\le
\binom{\binom{n+4}{2}}r
\le\frac{(n+4)^{2r}}{2^rr!}.
\]

### Ratio (17)

For \(1\le j\le d\),
\[
\begin{aligned}
\frac{T_{m-j,d-j}}{T_{m,d}}
&\le
\frac{(m-j+4)^{2(d-j)}}{2^{d-j}(d-j)!}
\frac{8^dd!}{m^{2d}}\\
&\le
2^{4d-j}\frac{(d)_{\underline j}}{k^{2j}}\\
&\le
16^d\frac{(d)_{\underline j}}{k^{2j}}.
\end{aligned}
\]
All powers of \(2\), \(d\), and \(k\) are correct.

### Relative error

Combining the ratio with the repaired Lemma 2 gives
\[
\left|\frac{p_{k,d}}{T_{m,d}}-1\right|
\le
16^dd\,
\exp(C(d+5)^2\log(d+5))\frac d k.
\]
Its logarithm is
\[
-\log k
+C(d+5)^2\log(d+5)
+d\log16
+O(\log(d+1)).
\]
Under the theorem's hypothesis this is
\(-(1-o(1))\log k\to-\infty\).  Thus the relative error tends to zero,
and the explicit window \(d\le(\log k)^{1/3}\) follows.

## 6. Verification record

No main theorem, verifier, or test file was modified during either
audit.

The following checks were run:

- 40 independent exact checks of (9a);
- 8 independent exact checks of (9b);
- 4,000 weighted-Cayley cycle-union stress checks;
- 765 exact mixed-binomial-moment checks;
- exact refined cancellation checks at total losses \(4,5,6\);
- 2,145 \(4\)-Stirling recurrence checks and 561 checks of its two
  comparison inequalities through \(n=64\);
- monomial-to-Newton checks through \(k=11\);
- the repository's growing-window and independent fixed-depth tests.

These finite computations are regression evidence only.  The PASS
verdict rests on the uniform analytic argument in Sections 1--5.

## 7. Optional editorial clarifications

Before publication, two small clarifications would improve
self-containment:

1. define \(E(s,z,r)\) explicitly immediately before (9a), or say
   that it denotes the finite sum in (7);
2. in (5a), say explicitly that \([h^v]R_{\ell,h}\) refers to the
   general marked-matching profile before specialization to
   \(h=0,1,2\).

Neither issue changes a formula, estimate, or inference.  The revised
growing top-window theorem passes this independent audit.
