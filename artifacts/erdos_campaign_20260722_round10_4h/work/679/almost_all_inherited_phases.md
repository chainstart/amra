# #679: the high tail is small for almost all interval phases

Date: 2026-07-22

This note proves a full-CRT phase-average theorem for the unresolved
high-conductor tail. It does not control the particular deterministic phase
required by the original problem, but it shows that the exceptional-phase
set has polynomially small density.

## 1. Exact high-tail energy

For \(W^q\), write

\[
 W(n)^q=\prod_{H<p\le z}(m_p+d_p(n)),
 \qquad \mu_q=\prod_pm_p,
\]

where

\[
 b=1-(1-a)^q,\quad m_p=1-bH/p,\quad
 d_p=-b(X_p-H/p).
\]

Let

\[
 F_T(n)=\prod_{p\notin T}m_p\prod_{p\in T}d_p(n),
 \qquad c(T)=\prod_{p\in T}p,
\]

and define the complete high-conductor ANOVA tail

\[
 {\cal H}_{D,q}(n)=\sum_{c(T)>D}F_T(n).               \tag{1}
\]

The \(F_T\)'s are mutually orthogonal on the complete CRT period
\(Q=\prod_{H<p\le z}p\). Therefore

\[
 {1\over Q}\sum_{n\bmod Q}|{\cal H}_{D,q}(n)|^2
 =\mu_q^2\sum_{c(T)>D}\prod_{p\in T}v_p,             \tag{2}
\]

with

\[
 v_p={{\mathbb E}_p d_p^2\over m_p^2}
 ={b^2(H/p)(1-H/p)\over(1-bH/p)^2}.                  \tag{3}
\]

For fixed \(q\) (and, more generally, \(q=o(\sqrt{L_2})\)),

\[
 V:=\sum_pv_p=O_C(q^2/L_2).                           \tag{4}
\]

Take the moving cutoff

\[
 D=Xe^{-2\Phi},\qquad \Phi={L_1L_3\over L_2},
 \qquad z=e^{L_1/L_2}.
\]

Since every selected prime is at most \(z\), \(c(T)>D\) forces

\[
 |T|\ge d_0:=\left\lceil{\log D\over\log z}\right\rceil
 =L_2-2L_3+O(1).                                     \tag{5}
\]

Dropping the product constraint after retaining (5),

\[
 \sum_{c(T)>D}\prod_{p\in T}v_p
 \le\sum_{j\ge d_0}{V^j\over j!}
 \le 2\left({eV\over d_0}\right)^{d_0}.             \tag{6}
\]

For fixed \(q\), this gives

\[
 \boxed{
 {1\over Q}\sum_{n\bmod Q}|{\cal H}_{D,q}(n)|^2
 \le \mu_q^2\exp\{-(2+o(1))L_2L_3\}.}              \tag{7}
\]

The same \(2+o(1)\) exponent holds for
\(q=\lfloor\eta L_3\rfloor\), because then
\(d_0/V=L_2^{2-o(1)}\).

## 2. Averaging the actual interval start

For \(1\le N\le X\), define

\[
 S_D(A)=\sum_{m=1}^{N}{\cal H}_{D,q}(A+m).
\]

Cauchy's inequality followed by translation invariance modulo \(Q\) yields

\[
 \begin{aligned}
 {1\over Q}\sum_{A\bmod Q}|S_D(A)|^2
 &\le {1\over Q}\sum_{A\bmod Q}
       N\sum_{m=1}^{N}|{\cal H}_{D,q}(A+m)|^2\\
 &=N^2{1\over Q}\sum_{n\bmod Q}|{\cal H}_{D,q}(n)|^2. \tag{8}
 \end{aligned}
\]

Combining (7)--(8), for every \(Y>0\),

\[
 {1\over Q}\#\{A\bmod Q:|S_D(A)|>Y\}
 \le {N^2\mu_q^2\over Y^2}
       \exp\{-(2+o(1))L_2L_3\}.                      \tag{9}
\]

In particular, fix \(q,C,\delta\) with \(qC>1+\delta\). Since
\(\mu_q=X^{-qC+o(1)}\), taking \(N\le X\) and \(Y=X^{-\delta}\) gives

\[
 \boxed{
 {1\over Q}\#\left\{A\bmod Q:
 \left|\sum_{m\le N}{\cal H}_{D,q}(A+m)\right|>
 X^{-\delta}\right\}
 \le X^{-2(qC-1-\delta)+o(1)}.}                      \tag{10}
\]

Thus the fixed-power additive estimate required in round 10 holds for all
but a polynomially sparse set of complete-CRT starting phases.

When \(N\asymp X\), as in the candidate-counting application, the
moving-cutoff theorem controls the low part uniformly in \(A\):

\[
 \sum_{m\le N}{\cal L}_{D,q}(A+m)
 =N\mu_q\{1+O(e^{-\Phi})\}.
\]

If \(qC>1+\delta\), this is \(o(X^{-\delta})\). Hence every start outside
the exceptional set in (10) satisfies

\[
 \sum_{m\le N}W(A+m)^q\le (1+o(1))X^{-\delta}.        \tag{11}
\]

For fixed \(q\), the Markov threshold factor is \(X^{o(1)}\), so (11)
contains no good integer once \(X\) is sufficiently large. Thus (10) is
also an almost-all-start **zero-candidate theorem**, not merely an energy
statement.

## 3. Distance from the original quantifier

Equation (10) averages \(A\) over the enormous period \(Q\). The original
problem requires the particular dyadic interval phases arising from the
integers under study; no randomness or averaging in \(A\) is available.
A set of density \(X^{-\sigma}\) modulo \(Q\) may still contain every one
of those deterministic starts. Therefore (10) is not an interval-uniform
bound and does not close #679.

The theorem does sharpen the obstruction: complete-period energy and the
entire high-degree tail are already more than sufficient for almost every
inherited phase. What remains is a deterministic exceptional-phase
exclusion theorem, not a typical-phase estimate.

Strict status: **unconditional almost-all-phase theorem; deterministic
phase and Erdős #679 remain open**.
