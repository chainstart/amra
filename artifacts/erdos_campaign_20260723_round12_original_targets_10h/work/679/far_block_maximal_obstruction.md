# #679: a rigorous obstruction to a low far cutoff

Date: 2026-07-23

This note tests whether the pointwise union bound in the far-shift argument
can be replaced by a dyadic/block maximal estimate at a much lower cutoff.
The obstruction is stronger than the initially proposed scale

\[
 K=\exp\{C\log_2X\log_3X\}.
\]

A published local law for \(\omega\) proves that almost every integer is
already *bad* somewhere in a block whose length is slightly smaller than
\(\log X\).

## 1. Goudout's local law

Let

\[
 \pi_j(y)=\#\{m\le y:\omega(m)=j\},\qquad
 \delta_j(X)=\lambda((j-1)/\log_2X)
 { (\log_2X)^{j-1}\over (\log X)(j-1)!}.
\]

Goudout's Theorem 1 (2017) says the following.  For fixed
\(0<a_-<a_+\), uniformly for

\[
 a_-\log_2X<j\le a_+\log_2X,
 \qquad \psi(X)\le \delta_j(X)h\le X,
\]

where \(\psi(X)\to\infty\), one has

\[
 \pi_j(x+h)-\pi_j(x)=(1+o(1))\delta_j(X)h             \tag{1}
\]

for almost every \(x\asymp X\).  Moreover, if
\(j/\log_2X\to a>0\), Stirling gives

\[
 \delta_j(X)=(\log X)^{-Q(a)+o(1)},
 \qquad Q(a)=a\log a-a+1.                            \tag{2}
\]

For the smaller values of \(j\) needed below, Goudout's Theorem 2 says
that, for every fixed \(\eta>0\), uniformly for \(5\le j\le\log_2X\),

\[
 F_j(X)(\log_3X)^{2+\eta}\le\delta_j(X)h\le X,       \tag{3}
\]

one has

\[
 \pi_j(x+h)-\pi_j(x)\gg {\delta_j(X)h\over F_j(X)}  \tag{4}
\]

for almost every \(x\asymp X\), where

\[
 F_j(X)={ (\log_2X)^2\over j^2}
 \left(1-\exp\left\{-{j\log_3X\over\log_2X}\right\}
 \right)^{-1}.                                      \tag{5}
\]

The official TeX of arXiv:1607.08666 was checked directly for both
theorems.  The density factor is

\[
 \lambda(\kappa)={1\over\Gamma(\kappa+1)}
 \prod_p\left(1+{\kappa\over p-1}\right)
       \left(1-{1\over p}\right)^\kappa.
\]

In particular \(\lambda(\kappa)\to1\) as \(\kappa\to0^+\).  Indeed, the
linear term in the logarithm of the \(p\)-factor is
\(\kappa\{(p-1)^{-1}+\log(1-1/p)\}=O(\kappa/p^2)\),
and the quadratic remainder is \(O(\kappa^2/p^2)\), uniformly for small
\(\kappa\); the prime sum converges, and \(\Gamma(1+\kappa)\to1\).

Primary source: E. Goudout, *Lois locales de la fonction omega dans
presque tous les petits intervalles*, Proc. LMS 115 (2017), Theorems 1--2,
https://arxiv.org/abs/1607.08666.

We also use the paper's stated two-shift corollary: for every fixed
\(b\ge1\) and fixed \(R>0\), uniformly for \(j_1,j_2\le R\log_2X\),

\[
 \#\{m\asymp X:\omega(m)=j_1,\ \omega(m+b)=j_2\}
 \ll_{b,R}\delta_{j_1}(X)\delta_{j_2}(X)X.          \tag{5a}
\]

## 2. Almost every endpoint is bad below \(\log X\)

Fix \(\varepsilon>0\), write

\[
A=1+\varepsilon,\qquad B=\log_2X,\qquad
L=\log_3X,\qquad M=\log_4X,
\]

Before optimising exact levels, it is important to separate two claims.
At every cutoff treated immediately below,

\[
 A{\log(2H)\over\log_2(2H)}=(A+o(1)){B\over L}=o(B).
\]

For the single deterministic shift \(k=\lfloor H\rfloor\), the classical
Hardy--Ramanujan normal-order theorem already says
\(\omega(n-k)=(1+o(1))B\) for all but \(o(X)\) endpoints
\(n\in[X,2X]\).  Hence the almost-all #679 violation at these near-
\(\log X\) cutoffs needs no short-interval theorem.  The fine calculations
below locate the boundary of the *stronger mechanism* ``the whole
length-\(H\) block contains an integer with exactly the threshold number
of prime factors.''  They are a method-threshold audit, not a stronger
original-problem theorem.

Goudout's Theorem 1 becomes genuinely useful at the larger scale
\(H=e^{CBL}\) when \(AC>1\): there the threshold exceeds the normal order
at a fixed shift, yet the block still contains a rare exact level for
almost every endpoint.

There is a sharper near-critical formulation.  Put

\[
 T=M+1-\log A,qquad
 s_0={AT\over L}-{A^2T(T-1)\over L^2}.              \tag{6a}
\]

The previously retained \(L^{-2}\) safety margin can in fact be set to
zero.  To see the sign, if \(s=O_A(M/L)\) and

\[
 \kappa={A(1-s)\over L+\log(1-s)},
\]

then expansion through the next order gives

\[
 \begin{aligned}
 \kappa\{\log(1/\kappa)+1\}
 ={AT\over L}-{A^2T(T-1)\over L^2}+{C_3(A,T)\over L^3}
 +O_A(T^4/L^4),                                    \tag{6b}\\
 C_3(A,T)
 ={A^2T\over2}\{2AT^2-5AT+2A+2T-2\}.
 \end{aligned}
\]

Here the substitution \(s=s_0+O_A(T^3/L^3)\) is understood in (6b).
The \(L^{-3}\) coefficient of \(s\) does not change the displayed
expansion of \(\kappa\{\log(1/\kappa)+1\}\) at that order; it enters
\(-s+\kappa\{\log(1/\kappa)+1\}\) with the opposite sign.  In particular

\[
 C_3(A,T)=(A^3+o_A(1))T^3>0.                       \tag{6c}
\]

Thus, already with

\[
 H_0=\lfloor\exp\{B(1-s_0)\}\rfloor,
 \qquad
 r_0=\left\lceil A{\log(2H_0)\over\log_2(2H_0)}\right\rceil,
\]

Stirling gives

\[
 \boxed{
 \log\{\delta_{r_0}(X)H_0\}
 =(A^3+o_A(1)){BT^3\over L^3}\longrightarrow+\infty.} \tag{6d}
\]

Flooring \(H_0\), ceiling \(r_0\), the factor \(\lambda((r_0-1)/B)\),
and Stirling's logarithmic remainder contribute only
\(o(BT^3/L^3)\).

One can move one order closer still.  For any fixed \(\gamma>0\), set

\[
 s_\gamma=s_0+{C_3(A,T)-\gamma\over L^3},
 \qquad H_\gamma=\lfloor\exp\{B(1-s_\gamma)\}\rfloor,
\]

and define \(r_\gamma\) by the same ceiling.  Then

\[
 \boxed{
 \log\{\delta_{r_\gamma}(X)H_\gamma\}
 =\{\gamma+o(1)\}{B\over L^3}\longrightarrow+\infty.} \tag{6e}
\]

Also \(r_\gamma=(A+o(1))B/L\) and
\(F_{r_\gamma}(X)\asymp L^2\), so Theorem 2 applies and proves that
almost every endpoint has a violation in
\([H_\gamma,2H_\gamma)\).  This is the closest-to-critical exact-level
cutoff proved here.

The new third-order boundary \(\gamma=0\) in (6e) can also be classified:
the next coefficient is

\[
 C_4(A,T)=-{A^3T\over6}
 \{6AT^3-26AT^2+27AT-6A+15T^2-33T+12\}
 =(-A^4+o_A(1))T^4<0.                              \tag{6f}
\]

Hence at that exact truncation
\(\log(\delta_rH)=(C_4+o(T^4))B/L^4\to-\infty\), so
Goudout's Theorem 2 does **not** apply.  This is only the boundary of the
``exactly \(r\) in the interval'' route.  It is not a transition for #679
itself: throughout these \(H=(\log X)^{1-o(1)}\) scales the target
threshold is \(o(\log_2X)\), so the normal order of \(\omega(n-H)\) at
even one fixed shift already makes almost every endpoint bad.

A simpler, slightly larger family makes the dominant term especially
transparent.  Fix \(0\le\theta<A\), and put

\[
 H=\left\lfloor
 \exp\left(B-\theta{BM\over L}\right)
 \right\rfloor,
 \qquad
 r_X=\left\lceil A{\log(2H)\over\log_2(2H)}\right\rceil. \tag{6}
\]

Thus \(H=\log X\) when \(\theta=0\), while every fixed
\(0<\theta<A\) gives a block shorter than \(\log X\).  Flooring and
ceiling change all logarithms below by \(o(1)\) or \(O(1)\).  Direct
expansion gives

\[
 r_X=(A+o(1)){B\over L},\qquad 5\le r_X\le B.       \tag{7}
\]

Let \(q=r_X-1\) and \(\kappa=q/B\).  Then
\(\kappa=(A+o(1))/L\to0\), so \(\log\lambda(\kappa)=o(1)\).  Stirling's
formula in the exact definition of \(\delta_{r_X}\) yields

\[
 \begin{aligned}
 \log\delta_{r_X}(X)
 &=-B+q\{\log(B/q)+1\}+O(\log B)\\
 &=-B+(A+o(1)){B\over L}(M+1-\log A).
 \end{aligned}                                      \tag{8}
\]

Since \(\log H=B-\theta BM/L+o(1)\), this becomes

\[
 \boxed{
 \log\{\delta_{r_X}(X)H\}
 =(A-\theta+o(1)){BM\over L}\longrightarrow+\infty.} \tag{9}
\]

Also (5) and (7) give

\[
 F_{r_X}(X)=\left({1\over A^2(1-e^{-A})}+o(1)\right)L^2. \tag{10}
\]

For any fixed \(\eta>0\), the logarithm of the left side of (3) is only
\(O(M)\), whereas (9) is \(\gg BM/L\).  Hence all hypotheses of
Goudout's Theorem 2 hold, including the upper bound
\(\delta_{r_X}H\le X\).  Formula (4) tends to infinity and in particular
is positive.  It follows that for all but \(o(X)\) integer endpoints
\(n\in[X,2X]\), the interval

\[
 (n-2H,n-H]
\]

contains an integer \(m\) with \(\omega(m)=r_X\).  The passage from the
almost-everywhere real statement to integer endpoints is harmless: with
integer \(H\), the count in \((x,x+H]\) is constant for
\(x\in(q,q+1)\), apart from measure-zero endpoints.
The translated starts lie in the required dyadic range after discarding
only \(O(H)=o(X)\) boundary endpoints.

Set \(k=n-m\).  Then \(H\le k<2H\).  Since
\(t\mapsto\log t/\log_2t\) is increasing for large \(t\), (6) gives

\[
 \omega(n-k)=r_X
 \ge (1+\varepsilon){\log(2H)\over\log_2(2H)}
 \ge (1+\varepsilon){\log k\over\log_2k}.          \tag{11}
\]

Thus (11) violates the desired strict inequality.  We have proved the
quantifier-correct statement

\[
 \boxed{
 \#\left\{n\in[X,2X]:
 \begin{array}{c}
 \text{some }H\le k<2H\text{ violates the first}\\
 \text{inequality of Erd\H{o}s \#679}
 \end{array}\right\}
 =(1-o(1))X.}                                       \tag{12}
\]

Consequently no block maximal estimate can make the bad set \(o(X)\) at
even the sub-\(\log X\) scale in (6): the opposite density statement
(12) is true.  This does **not** disprove #679, whose desired integers may
belong to the exceptional \(o(X)\) set; it proves that any construction
must be very sparse and cannot be obtained by an almost-all far theorem at
this cutoff.

Two useful larger-scale corollaries follow from the same source.

* If \(H=\lfloor(\log X)^C\rfloor\) with any fixed \(C\ge1\), then
  \(r_X=(AC+o(1))B/L\), \(F_{r_X}(X)\asymp L^2\), and
  \[
    \log(\delta_{r_X}H)
    =(C-1)B+(AC+o(1)){B\over L}(M+1-\log(AC))\to\infty.
  \]
  Theorem 2 again proves (12).  The \(C=1\) boundary is genuinely
  admissible; the positive term of order \(BM/L\) dominates every
  polylogarithmic requirement in (3).  No assertion is made for fixed
  \(C<1\).
* If \(H=\lfloor\exp(CBL)\rfloor\) with fixed \(C>0\), then
  \(r_X/B\to AC\), and Theorem 1 gives
  \(\log(\delta_{r_X}H)=CBL-Q(AC)B+o(B)\to\infty\).
  Thus the initially proposed cutoff is also almost-all bad.

There is also a rigorous but ineffective diagonal extension.  For each
integer \(m\ge1\), apply Theorem 1 with the fixed choice \(C_m=m/A\) and
choose a threshold \(X_m\) beyond which its exceptional proportion is at
most \(1/m\).  Enlarge the thresholds so that they are increasing and
\(m\le\sqrt{\log_2X}\) whenever \(X\ge X_m\).  If

\[
 m(X)=\max\{m:X\ge X_m\},\qquad G(X)={m(X)\over A},
\]

then \(G(X)\to\infty\), \(H(X)=\exp\{G(X)BL\}=X^{o(1)}\), and the same
block-bad conclusion holds for \((1-o(1))X\) endpoints.  This proves the
existence of some arbitrarily slowly growing coefficient beyond every
fixed \(C\).  It gives no explicit growth rate and must not be read as
uniformity of Goudout's theorem for an arbitrary prescribed
\(G(X)\to\infty\).

There is a simpler quantitative density corollary with the original order
of quantifiers.  Fix \(\varepsilon>0\) and a fixed integer \(K\), and let

\[
 \mathcal G_{\varepsilon,K}(X)=
 \left\{n\in[X,2X]:
 \omega(n-k)<(1+\varepsilon){\log k\over\log_2k}
 \text{ for every }K\le k<n\right\}.
\]

Take the adjacent shifts \(k_X=\lfloor\log X\rfloor\) and \(k_X+1\).
They lie in \([K,n)\) for every \(n\in[X,2X]\) once \(X\) is large.  Put

\[
 q_X=\left\lceil A{\log k_X\over\log_2k_X}\right\rceil-1
 =(A+o(1)){B\over L}.
\]

Increasing \(q_X\) by at most one absorbs the negligible threshold change
between these shifts.  Every \(n\in\mathcal G_{\varepsilon,K}(X)\) then
has

\[
 \omega(n-k_X)\le q_X,qquad
 \omega(n-k_X-1)\le q_X.
\]

The level densities increase geometrically for \(j\le q_X<B/2\), so

\[
 \sum_{j\le q_X}\delta_j(X)
 \le\exp\left\{-B+(A+o(1)){B\over L}
                   (M+1-\log A)\right\}.           \tag{16}
\]

Apply (5a) with \(b=1\) to \(m=n-k_X-1\), and sum over both exact
levels.  This gives

\[
 \begin{aligned}
 \#\mathcal G_{\varepsilon,K}(X)
 &\ll X\left(\sum_{j\le q_X}\delta_j(X)\right)^2\\
 &\le X\exp\left\{-2B+(2A+o(1)){B\over L}
                 (M+1-\log A)\right\}\\
 &= {X\over(\log X)^{2-o(1)}}.                     \tag{17}
 \end{aligned}
\]

In particular

\[
 \boxed{\#\mathcal G_{\varepsilon,K}(X)=o(X).}
\]

Thus any witness sequence for the original first question, if it exists,
has dyadic density zero, with the stronger two-shift bound (17).  This is
not a finiteness statement and does not exclude an infinite sparse
sequence.  Although Goudout remarks that its method can be extended to any
fixed number of translates, only the explicitly stated two-shift theorem
is used here; no unproved many-shift iteration is claimed.

## 3. Why the pointwise tail cannot pay for this block

At the initially proposed scale \(H=e^{CBL}\), one has
\(r_X=(AC+o(1))B\).  The global density in (2) is
only

\[
 (\log X)^{-Q(AC)+o(1)}=\exp\{-Q(AC)B+o(B)\},
\]

whereas

\[
 H=\exp\{CBL+o(BL)\}.                               \tag{9}
\]

Hence an interval of length \(H\) contains
\(H\delta_{r_X}(X)=\exp\{CBL-O(B)\}\to\infty\)
such integers for almost every endpoint, exactly as (1) asserts.  Merely
grouping the pointwise union bound cannot reverse this fact.

By contrast, to make the Hardy--Ramanujan pointwise exponent pay a factor
\(1/K\), one needs

\[
 r\log(r/B)\gtrsim\log K,
 \qquad r\sim(1+\varepsilon){\log K\over\log_2K}.
\]

If \(\log K=CB\log B\), then \(r\asymp B\) and the left side is only
\(O(B)\), while the right side is \(CB\log B\).  If instead
\(\log K=B^D\), the ratio of the two leading exponents tends to
\((1+\varepsilon)(D-1)/D\), which exceeds one once
\(D>(1+\varepsilon)/\varepsilon\).  This explains the power-of-\(B\)
cutoff in the far-shift theorem.

## 4. An explicit injective translation component

There is also a direct pair-count obstruction to any black-box claim that
dyadic grouping automatically removes the block-length loss.  For a large
abstract block length \(H\), let \(r\) be the integer in (6), with this
abstract \(H\), and let

\[
 Q=p_1p_2\cdots p_r.
\]

The prime number theorem gives

\[
 \log Q=(1+\varepsilon-o(1))\log H,
 \qquad Q=H^{1+\varepsilon-o(1)}>2H.                \tag{10}
\]

For each multiple \(m\) of \(Q\), every pair
\((m,k)\), \(H\le k<2H\), is bad, because
\(\omega(m)\ge r\).  Restrict to multiples
\(m\in[X,2X-2H]\).  The map

\[
 (m,k)\longmapsto n=m+k
\]

is injective on these pairs: for each \(m\) its image is an interval of
length \(H\), and (10) makes the intervals for distinct multiples
disjoint.  Provided \(Q=o(X)\), this gives the rigorous lower bound

\[
 \#\{\text{bad endpoints in the block}\}
 \ge H\left({X\over Q}-O(1)\right)
 =XH^{-\varepsilon+o(1)}.                           \tag{11}
\]

Thus the factor \(H\) in the elementary translation union bound is
attained exactly on a genuine subset of the bad pairs.  Formula (12) is the
stronger obstruction at the proposed low cutoff; (11) separately records
why no general set-theoretic maximal inequality can discard the
translation factor without using substantial arithmetic overlap.
