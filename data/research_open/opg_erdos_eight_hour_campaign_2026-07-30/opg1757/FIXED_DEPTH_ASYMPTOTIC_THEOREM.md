# Every fixed Newton depth is eventually positive

Date: 2026-07-30

## 1. Result

Use the notation of `FIRST_ACTIVE_NEWTON_THEOREM.md`.  Thus
\[
C_k(n)=[x^k](\Phi _1(x)^2-\Phi _0(x)\Phi _2(x)),\qquad
c_k(n)=\frac{(k-2)!}{2}C_k(n),
\]
and
\[
c_k(n)=\sum_q a_{k,q}\binom{n-4}{q}.
\]
Put
\[
q_0=\left\lfloor\frac{k-2}{2}\right\rfloor .
\]

### Theorem 1 (fixed-depth positivity)

For every fixed integer \(r\geq0\), there is \(K_r\) such that
\[
\boxed{a_{k,q_0+r}>0\qquad(k\geq K_r).}
\tag{1}
\]
More precisely, set
\[
n_0=q_0+4,\qquad n_r=n_0+r,
\]
and
\[
t_r=
\begin{cases}
3+2r,&k\ \mathrm{odd},\\
4+2r,&k\ \mathrm{even}.
\end{cases}
\]
Then, as \(k\to\infty\) through either parity class,
\[
\boxed{
a_{k,q_0+r}
=\frac{2(k-2)!}{(t_r-3)!}\,
n_r^{\,2n_r-8}
+\;O_r\!\left((k-2)!\,n_r^{\,2n_r-9}\right).
}
\tag{2}
\]

Thus every fixed-width strip above the capacity boundary is eventually
strictly positive.  The case \(r=0\) strengthens to every \(k\ge2\),
and \(r=1\) strengthens to every \(k\ge3\), by the exact formulas in
`FIRST_ACTIVE_NEWTON_THEOREM.md`; \(k=2\) has no second active layer.

The theorem is not the full coefficientwise result: \(r\) is fixed
before \(k\) tends to infinity, and the proof does not control depths
growing with \(k\).

## 2. A uniform determinant asymptotic

Let \(W_{h,c}(n)\) count \(c\)-component forests of \(K_n\) containing
a prescribed matching of size \(h\), for \(h=0,1,2\).  For fixed
\(t\geq3\), define
\[
\mathcal C_t(n)=
\sum_{\substack{c,d\geq1\\c+d=t}}
\left(W_{1,c}(n)W_{1,d}(n)
-W_{0,c}(n)W_{2,d}(n)\right).
\tag{3}
\]

### Lemma 2 (positive leading term)

For every fixed \(t\geq3\),
\[
\boxed{
\mathcal C_t(n)
=\frac{4}{(t-3)!}\,n^{\,2n-8}
+O_t(n^{\,2n-9}).
}
\tag{4}
\]

The positivity in (4) is the mechanism behind Theorem 1.

There is a useful uniform-in-\(t\) formula for the next fixed-\(t\)
term:
\[
\boxed{
\mathcal C_t(n)
=\frac4{(t-3)!}n^{2n-8}
+\frac{16}{(t-4)!}n^{2n-9}
+O_t(n^{2n-10}),
}
\tag{4a}
\]
where the middle term is interpreted as zero for \(t=3\).  Equivalently,
\[
\mathcal C_t(n)
=\frac4{(t-3)!}n^{2n-8}
\left(1+\frac{4(t-3)}n+O_t(n^{-2})\right).
\tag{4b}
\]

## 3. Fixed-component expansions

Write \(u=1/n\), put \(\rho=c-1\), and set
\[
g_\rho=\frac1{2^\rho\rho!}.
\]
The Liu--Chow formula, in a form with all powers of \(n\) removed, is
\[
\frac{W_{0,c}(n)}{n^{n-2}}
=
\sum_{j=0}^{c-1}
\frac{(-1/2)^j(c+j)}{j!(c-j-1)!}
\prod_{\ell=1}^{c+j-1}(1-\ell u).
\tag{5}
\]
For an adjacent prescribed edge pair, write its count as \(A_c(n)\).
The corresponding contraction formula is
\[
\frac{A_c(n)}{n^{n-4}}
=
\sum_{j=0}^{c-1}
\frac{(-1/2)^j(c+j+2)}{j!(c-j-1)!}
\prod_{\ell=3}^{c+j+1}(1-\ell u).
\tag{6}
\]
Terms outside the factorial range vanish.  Expanding the finite
products in (5)--(6) gives
\[
\begin{aligned}
\frac{W_{0,c}(n)}{n^{n-2}}
&=g_\rho\left[
1+5\rho u
+\frac{\rho(35\rho-47)}2u^2+O_c(u^3)
\right],\\
\frac{A_c(n)}{n^{n-4}}
&=g_\rho\left[
3+11\rho u
+\frac{5\rho(13\rho-37)}2u^2+O_c(u^3)
\right].
\end{aligned}
\tag{7}
\]

For clarity, (7) involves no analytic approximation inside an
unbounded sum: for fixed \(c\), (5)--(6) are finite polynomials in
\(u\).  One direct verification of the displayed coefficients is to
use
\[
\prod_{\ell=a}^{b}(1-\ell u)
=1-\left(\sum_{\ell=a}^{b}\ell\right)u
+\frac12\left[
\left(\sum_{\ell=a}^{b}\ell\right)^2
-\sum_{\ell=a}^{b}\ell^2
\right]u^2+O_c(u^3),
\tag{8}
\]
and evaluate the remaining binomial moments from
\[
\sum_j\binom{\rho}{j}z^j=(1+z)^\rho
\tag{9}
\]
after applying \(z\,d/dz\) as needed and setting \(z=-1/2\).
This yields exactly (7).

Edge transitivity gives
\[
W_{1,c}(n)=\frac{2(n-c)}{n(n-1)}W_{0,c}(n).
\tag{10}
\]
There are
\[
N_{\rm adj}=\frac{n(n-1)(n-2)}2,\qquad
N_{\rm dis}=\frac{n(n-1)(n-2)(n-3)}8
\]
unordered adjacent and disjoint edge pairs.  Double-counting a forest
and two of its \(n-c\) edges gives
\[
N_{\rm adj}A_c+N_{\rm dis}W_{2,c}
=\binom{n-c}{2}W_{0,c}.
\tag{11}
\]
Substitution of (7) into (10)--(11) yields
\[
\begin{aligned}
\frac{W_{1,c}(n)}{n^{n-3}}
&=g_\rho\left[
2+8\rho u+\rho(25\rho-49)u^2+O_c(u^3)
\right],\\
\frac{W_{2,c}(n)}{n^{n-4}}
&=g_\rho\left[
4+12\rho u+2\rho(17\rho-57)u^2+O_c(u^3)
\right].
\end{aligned}
\tag{12}
\]

Keeping one further term in the same finite-product calculation gives
\[
\begin{aligned}
\frac{W_{0,c}}{g_\rho n^{n-2}}
&=\cdots+
\frac{\rho(\rho-1)(105\rho-364)}2u^3+O_c(u^4),\\
\frac{A_c}{g_\rho n^{n-4}}
&=\cdots+
\frac{\rho(\rho-1)(175\rho-1304)}2u^3+O_c(u^4),\\
\frac{W_{1,c}}{g_\rho n^{n-3}}
&=\cdots+
2\rho(\rho-1)(35\rho-181)u^3+O_c(u^4),\\
\frac{W_{2,c}}{g_\rho n^{n-4}}
&=\cdots+
2\rho(\rho-1)(45\rho-368)u^3+O_c(u^4).
\end{aligned}
\tag{12a}
\]
Here each ellipsis denotes exactly the three terms displayed for that
quantity in (7) or (12).

## 4. Proof of Lemma 2

In a summand of (3), put
\[
\rho=c-1,\qquad \sigma=d-1,\qquad
R=\rho+\sigma=t-2.
\]
The constant terms in (7), (12) cancel.  The coefficient of \(u\) in
the ordered summand, after removing
\(g_\rho g_\sigma n^{2n-6}\), is
\[
-4(\rho-\sigma).
\tag{13}
\]
It cancels after summing the two orders \((\rho,\sigma)\) and
\((\sigma,\rho)\).  The symmetrized coefficient of \(u^2\) is
\[
2\left(3R-(\rho-\sigma)^2\right).
\tag{14}
\]
Consequently the coefficient of \(n^{2n-8}\) in (3) is
\[
2\sum_{\rho+\sigma=R}
\frac{3R-(\rho-\sigma)^2}
{2^R\rho!\sigma!}.
\tag{15}
\]

Under the normalized weights
\[
\frac{\binom R\rho}{2^R},
\]
the variable \(\rho\) is binomial \(\operatorname{Bin}(R,1/2)\).
Hence
\[
\sum_{\rho+\sigma=R}g_\rho g_\sigma=\frac1{R!},
\qquad
\sum_{\rho+\sigma=R}g_\rho g_\sigma(\rho-\sigma)^2
=\frac R{R!}.
\tag{16}
\]
Equation (15) is therefore
\[
\frac{2(3R-R)}{R!}
=\frac4{(R-1)!}
=\frac4{(t-3)!}.
\]
The unrecorded terms in the finitely many summands are
\(O_t(n^{-3})\) after the common factor \(n^{2n-6}\) is removed.
This proves (4).

For (4a), the symmetrized \(u^3\) coefficient obtained from (12a) is
\[
-2\left[
5R^3-9R^2+4R-(20R+16)\rho\sigma
\right].
\tag{16a}
\]
Under the same binomial weights,
\[
\mathbb E(\rho\sigma)=\frac{R(R-1)}4.
\]
The weighted mean of (16a) is consequently
\[
16R(R-1).
\]
After multiplication by the total mass \(1/R!\), the coefficient of
\(n^{2n-9}\) is
\[
\frac{16R(R-1)}{R!}=\frac{16}{(t-4)!}.
\]
This proves (4a)--(4b).

## 5. Proof of Theorem 1

For a fixed \(k\), a product contributing to \(C_k(n)\) has total
component count
\[
t=2n-2-k.
\tag{17}
\]
The support cancellation gives \(C_k(4+i)=0\) for \(i<q_0\).
For odd \(k\) this is the capacity boundary.  In the sole even
borderline term it additionally uses the exact tree identity
\[
W_{1,1}^2-W_{0,1}W_{2,1}=0.
\]
Newton inversion at
\(q=q_0+r\) therefore says
\[
\frac{2a_{k,q_0+r}}{(k-2)!}
=\sum_{j=0}^{r}
(-1)^{r-j}
\binom{q_0+r}{r-j}
\mathcal C_{t_0+2j}(n_0+j),
\tag{18}
\]
where \(t_0=3\) for odd \(k\) and \(t_0=4\) for even \(k\).

The \(j=r\) term in (18), by Lemma 2, is
\[
\frac4{(t_r-3)!}n_r^{2n_r-8}
+O_r(n_r^{2n_r-9}).
\tag{19}
\]
For \(j=r-\ell\), where \(1\leq\ell\leq r\), its binomial
coefficient is \(O_r(n_r^\ell)\), while
\[
(n_r-\ell)^{2(n_r-\ell)-8}
=O_r\!\left(n_r^{2n_r-8-2\ell}\right).
\tag{20}
\]
More precisely, its ratio to
\(n_r^{2n_r-8-2\ell}\) is
\[
e^{-2\ell}
\,\left(1+\frac{\ell^2+8\ell}{n_r}
+O_r(n_r^{-2})\right),
\]
so the constant suppressed in (20) is harmless but nontrivial.
Thus every earlier term is
\(O_r(n_r^{2n_r-9})\), and their finite sum has the same bound.
Equations (18)--(20) give (2).  Its leading constant is positive, so
(1) follows.

## 6. Claim status and remaining gap

- Lemma 2 and Theorem 1 are human proofs.
- The companion verifier checks the finite-product expansions, the
  binomial-variance constant, and exact Newton coefficients using
  integer forest counts.  Those checks are regressions, not premises.
- The result is an unbounded theorem for every prescribed finite depth.
- It does not give a \(K_r\) uniform in \(r\), and therefore does not
  establish all Newton coefficients or OPG-1757.
