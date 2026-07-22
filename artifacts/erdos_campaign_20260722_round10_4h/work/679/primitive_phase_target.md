# #679: primitive Fourier form of the inherited frontier phase

Date: 2026-07-22

This note Fourier-expands only a stopping-line prefix. The positive suffix is
left intact, so the actual interval start, terminal suffix prime, and the
frontier conductor remain coupled.

Write \(e(x)=e^{2\pi i x}\). The original forbidden set at every selected
prime is

\[
 {\cal A}_p=\{K,K+1,\ldots,K+H-1\}\pmod p,
\]

and, for \(W^q\),

\[
 d_p(x)=-b\{1_{{\cal A}_p}(x)-H/p\},
 \qquad b=1-(1-a)^q.                                  \tag{1}
\]

## 1. Exact coefficient of one frontier

Order the primes decreasingly. A stopping frontier consists of a terminal
prime \(p_*\), a selected set \(T\) among the processed primes with
\(p_*\in T\), and conductor

\[
 c=c(T)=\prod_{p\in T}p,
 \qquad D<c\le Dp_*.
\]

The processed but unselected primes contribute the positive scalar

\[
 \gamma_T=\prod_{\substack{p\ge p_*\\p\notin T}}m_p,
 \qquad m_p=1-bH/p,
\]

and the prefix is

\[
 g_T(x)=\gamma_T\prod_{p\in T}d_p(x).                 \tag{2}
\]

For a function modulo \(c\), use

\[
 \widehat g(u)={1\over c}\sum_{x\bmod c}g(x)e(-ux/c).
\]

For \(p\mid c\), let

\[
 h_p(u)\equiv u(c/p)^{-1}\pmod p,
 \qquad 0\le h_p(u)<p,
\]

and put \(D_H(\theta)=\sum_{j=0}^{H-1}e(-j\theta)\). CRT
factorization and the mean-zero identity \(\widehat d_p(0)=0\) give the
exact formula

\[
 \boxed{
 \widehat g_T(u)=
 \begin{cases}
 \displaystyle
 \gamma_T{(-b)^{|T|}\over c}
 e(-uK/c)\prod_{p\mid c}D_H\!\left({h_p(u)\over p}\right),
       &(u,c)=1,\\[6pt]
 0,    &(u,c)>1.
 \end{cases}}                                         \tag{3}
\]

Indeed, for \(h\ne0\pmod p\),

\[
 {1\over p}\sum_{x\bmod p}d_p(x)e(-hx/p)
 =-{b\over p}e(-hK/p)D_H(h/p),                        \tag{4}
\]

and the CRT product of the factors \(e(-h_pK/p)\) is
\(e(-uK/c)\). Thus every surviving prefix frequency is primitive. This is
stronger information than merely saying that the prefix has mean zero.

## 2. Exact joint phase sum

Let the interval be \(I=(A,A+N]\), and let

\[
 V_{p_*}(n)=\prod_{p<p_*}(m_p+d_p(n))                 \tag{5}
\]

be the unexpanded suffix attached to this frontier. Fourier inversion in
(2), with no absolute values, gives

\[
 \begin{aligned}
 \sum_{n\in I}g_T(n)V_{p_*}(n)
  ={}&\gamma_T{(-b)^{|T|}\over c}
  \sum_{\substack{u\bmod c\\(u,c)=1}}
  e\left({u(A-K)\over c}\right)
  \prod_{p\mid c}D_H\!\left({h_p(u)\over p}\right)\\
 &\hspace{35mm}\times
  \sum_{m=1}^{N}e(um/c)V_{p_*}(A+m).                 \tag{6}
 \end{aligned}
\]

Summing (6) over all crossing frontiers is an exact representation of the
signed high-conductor aggregate:

\[
 \boxed{
 \sum_{n\in I}{\cal H}_{D,q}(n)
 =\sum_{T\in{\cal F}_D}\text{the right side of (6)}.} \tag{7}
\]

Formula (6) exposes all three pieces of state required in round 10:

1. interval length \(N\), inside the final twisted suffix sum;
2. suffix endpoint \(p_*\), inside \(V_{p_*}\);
3. inherited start phase \(e(u(A-K)/c)\), coupled to the same \((T,u)\)
   that determines every local inverse \(h_p(u)\).

Replacing the inner suffix sum by its modulus, or summing the modulus of
(6) separately over \(T\), destroys precisely the cancellation excluded by
the top-band barrier.

## 3. Sufficient analytic target

The fixed-power reduction in `fixed_power_additive_sufficiency.md` shows
that, for any fixed \(q,C\) with \(qC>1\), it is enough to prove that the
entire right side of (7), after summing jointly in \(T\) and primitive
\(u\), is

\[
 O(X^{-\delta})                                       \tag{8}
\]

for some fixed \(\delta>0\). No estimate of an individual frontier in
isolation is requested.

The inverse residues in (3) are of Kloosterman-fraction type after the
prime factors of \(c\) are grouped. However, (8) also contains a
frontier-dependent positive suffix and approximately \(L_2\) prime factors
per top-band conductor. A theorem for a single bilinear or trilinear
Kloosterman fraction does not apply until these two structural features are
preserved in a compatible factorization.

Strict status: **exact Fourier identity and a sharply stated sufficient
target; estimate (8) and Erdős #679 remain open**.
