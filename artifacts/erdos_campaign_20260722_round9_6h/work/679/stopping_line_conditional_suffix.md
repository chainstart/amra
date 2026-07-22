# #679: quantitative conditional-suffix form of the stopping line

Date: 2026-07-22

This note sharpens the exact stopping identity into a quantitative recursive
interface. It shows that, in the fixed \(H=(\log X)^2\) window and with the
growing moment \(q=\lfloor L_3\rfloor\), the entire absolute frontier costs
only \(X^{o(1)}\). The unresolved input is now a uniform relative estimate
for the positive suffix on arithmetic progressions. A naive induction does
not yet supply that input.

## 1. Local absolute ratios

Work directly with \(W^q\). Put

\[
 b=1-(1-a)^q,\qquad x_p=H/p,\qquad
 m_p=1-bx_p,\qquad d_p(n)=-b\{X_p(n)-x_p\},
\]

where \(X_p\) is the indicator of the \(H\) forbidden residues modulo \(p\).
The same argument includes \(q=1\); the displayed strongest conductor-mass
ledger uses \(q=\lfloor L_3\rfloor\).
Then

\[
 u_p:=\mathbb E_p|d_p|
      =2b x_p(1-x_p),\qquad
 \rho_p:={u_p\over m_p}\le {3bH\over p}                \tag{1}
\]

for all sufficiently large \(X\). Moreover

\[
 S:=\sum_p\rho_p\le (3+o(1))bHL=O_C(qL_1).             \tag{2}
\]

For \(Y\ge1\), define the conductor mass

\[
 {\cal F}(Y)=
 \sum_{\substack{T\subseteq{\cal P}\\c(T)\le Y}}
 \prod_{p\in T}\rho_p.                                \tag{3}
\]

Since every selected prime exceeds \(H=(\log X)^2\), every term with
\(c(T)\le X^\kappa z\) has

\[
 |T|\le J=(\kappa+o(1)){L_1\over2L_2}.
\]

The elementary-symmetric bound and (2) therefore give, for
\(q=\lfloor L_3\rfloor\),

\[
 \log{\cal F}(X^\kappa z)
 \le \log(J+1)+J\log{eS\over J}
 \le \left({1\over2}+o_C(1)\right)
       {L_1L_3\over L_2}=o(L_1).                       \tag{4}
\]

Here \(S/J\to\infty\), so the summands \(S^j/j!\) increase through
\(j=J\), and
\(\sum_{j\le J}S^j/j!\le(J+1)(eS/J)^J\). This records the constant
\(1/2\) needed by the moving-cutoff corollary.

Thus the stopping frontier has subpower absolute mass even though the
unrestricted absolute ANOVA expansion is enormous.

### A strict low-conductor transfer improvement

Let

\[
 W_{\le D}(n)=\sum_{c(T)\le D}F_T(n),\qquad D=X^\kappa.
\]

Every nonempty \(F_T\) has mean zero and period \(c(T)\). An incomplete
period therefore contributes at most

\[
 c(T)\,\mu\prod_{p\in T}\rho_p
\]

in absolute value. Summing and using (3)--(4) proves, for every fixed
\(\kappa<1\),

\[
 \boxed{
 \sum_{n\in I}W_{\le X^\kappa}(n)
 =N\mu\{1+O(X^{-1+\kappa+o(1)})\}.
 }                                                     \tag{4a}
\]

This raises the rigorously transferred conductor range from the earlier
\(\kappa<2/3\) Cauchy range to every fixed \(\kappa<1\) in this small-tilt
window. It is an actual interval theorem for the truncated ANOVA expansion,
not for the positive full weight.

The proof of (4) is uniform for every \(Y\le Xz\), since it only replaces
\(J\) by at most \((1+o(1))L_1/(2L_2)\). Hence it permits a moving cutoff.
Put

\[
 \Phi(X)={L_1L_3\over L_2}.
\]

With the explicit choice

\[
 D=X\exp\{-2\Phi(X)\}
   =X^{1-2L_3/L_2},
\]

one has \(Dz<X\) and

\[
 \boxed{
 \sum_{n\in I}W_{\le D}(n)
 =N\mu\{1+O(\exp(-\Phi(X)))\}.
 }                                                     \tag{4b}
\]

Indeed, (4) is uniform with constant \(1/2+o_C(1)\), so
\((D/N){\cal F}(D)\le\exp\{-(3/2-o_C(1))\Phi(X)\}\).
Thus only conductors within
an \(X^{O(L_3/L_2)}\) factor of the interval length remain untreated.

## 2. Exact conditioning on a frontier conductor

Order the primes decreasingly and stop when the selected conductor first
exceeds \(D=X^\kappa\), \(0<\kappa<1\), or at the moving cutoff in (4b).
A frontier term has the form

\[
 g_T(n)W_{\rm suf}(n),\qquad
 D<c(T)\le Dz=X^{\kappa+o(1)},                         \tag{5}
\]

where \(g_T\) is periodic modulo \(c=c(T)\), has mean zero, and
\(W_{\rm suf}\) uses only primes not dividing \(c\).

Fix a residue \(r\bmod c\) and write \(n=r+c\ell\). Multiplication by \(c\)
permutes the residues modulo every suffix prime. Hence
\(W_{\rm suf}(r+c\ell)\) is exactly another collision-free \(H\)-residue
weight, now on an ordinary interval of

\[
 M_r=N/c+O(1)                                         \tag{6}
\]

consecutive \(\ell\)'s. No equidistribution assertion is used in this
reparametrization.

Suppose that, uniformly in \(r,c\) and in the resulting arbitrary
\(H\)-element forbidden sets, one had

\[
 \sum_{\ell\in J_r}W_{\rm suf}(r+c\ell)
 \le M_r\mu_{\rm suf}A(M_r),\qquad A(M_r)\ge1.         \tag{7}
\]

Positivity also gives an absolute discrepancy at most
\(M_r\mu_{\rm suf}A(M_r)\). Splitting by \(r\bmod c\), and using

\[
 {1\over c}\sum_{r\bmod c}|g_T(r)|
 =\left(\prod_{p\ {\rm in\ prefix}}m_p\right)
  \prod_{p\in T}\rho_p,
\]

one obtains

\[
 \left|\sum_{n\in I}g_T(n)W_{\rm suf}(n)
       -\mu_{\rm suf}\sum_{n\in I}g_T(n)\right|
 \le 2N\mu\,A(N/c)\prod_{p\in T}\rho_p.                \tag{8}
\]

The main term in (8) has the elementary periodic bound

\[
 \left|\mu_{\rm suf}\sum_{n\in I}g_T(n)\right|
 \le c\,\mu\prod_{p\in T}\rho_p.                       \tag{9}
\]

Summing (8)--(9) over the frontier and applying (4) gives the rigorous
conditional estimate

\[
 {|\text{high tail on }I|\over N\mu}
 \le X^{-1+\kappa+o(1)}
    +X^{o(1)}
      \sup_{X^{1-\kappa-o(1)}\le M\le X^{1-\kappa}}
       A(M).                                           \tag{10}
\]

The same absolute-ratio calculation bounds all nonconstant
\(c(T)\le D\) terms by \(X^{-1+\kappa+o(1)}\).

With the moving cutoff (4b), the identical proof gives

\[
 {|\text{high tail on }I|\over N\mu}
 \le e^{-\Phi(X)}
 +e^{(1/2+o_C(1))\Phi(X)}
  \sup_{M=\exp\{(2+o(1))\Phi(X)\}}A(M).                \tag{10a}
\]

This is the sharpest form reached here: the untreated suffix interval is
subpower in \(X\), but still vastly longer than its prime endpoint, since
\(\log z=o(\Phi(X))\).

## 3. What (10) achieves and what it does not

Equation (10) removes two previously suspected losses:

* the number of frontier subsets costs only
  \(\exp\{O(L_1L_3/L_2)\}=X^{o(1)}\);
* conditioning on a crossing conductor preserves exactly \(H\) forbidden
  residues at every suffix prime.

Therefore a uniform \(A(M)=M^{o(1)}\) theorem for these transformed suffix
weights would close the required interval transfer, and the growing-moment
bound would then close #679.

There is a strict warning: such a theorem is false if “uniform” is enlarged
to all starting points and all arbitrary \(H\)-sets. For any finite suffix,
choose one allowed residue at each prime. CRT gives an all-inactive class
\(\ell_0\) with \(W_{\rm suf}(\ell_0)=1\). An interval of length \(M\)
containing \(\ell_0\) then forces

\[
 A(M)\ge {1\over M\mu_{\rm suf}}.                      \tag{11}
\]

At the first recursive scale \(M=X^{1-\kappa+o(1)}\), the enlarged family
contains top-endpoint suffixes with
\(\mu_{\rm suf}=X^{-qC+o(q)}\). For
\(q=\lfloor L_3\rfloor\), (11) is vastly larger than \(M^{o(1)}\).
Consequently the missing theorem must retain the inherited starting phase
and its correlation with the frontier residue; an arbitrary-shift black
box cannot work.

Using (10) itself as a theorem for the restricted inherited family is also
circular. Repeated recursion
shortens the interval much faster than it exhausts the suffix's reciprocal
prime mass. Eventually the endpoint primes need not be subpower relative to
the recursively shortened interval, and the trivial terminal estimate
\(A\le\mu_{\rm suf}^{-1}\) can return the entire lost exponent. The
subpower frontier factor in (10) is not a polynomial contraction, so this
terminal loss is not absorbed.

Strict status: **new quantitative frontier-to-suffix reduction; a
fully-uniform suffix theorem is impossible and the inherited-phase theorem
is unproved; no interval transfer or original closure**.
