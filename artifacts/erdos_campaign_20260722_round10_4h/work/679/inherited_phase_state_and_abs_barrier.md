# #679: exact inherited-phase state and a top-band absolute-value barrier

Date: 2026-07-22

This note keeps the interval start instead of replacing the suffix by an
arbitrary-shift supremum. It also proves that taking absolute values
frontier-by-frontier before using that phase is exponentially fatal.

## 1. Exact inherited phase

Let \(I=(A,A+N]\), let a stopping frontier have conductor \(c<N\), and let
\(g_c\) denote its prefix factor. For \(0\le r<c\), define

\[
 L_r=\left\lfloor{A-r\over c}\right\rfloor,\qquad
 M_r=\left\lfloor{A+N-r\over c}\right\rfloor-L_r.      \tag{1}
\]

Then the integers of \(I\) congruent to \(r\bmod c\) are exactly

\[
 n=r+c(L_r+s),\qquad 1\le s\le M_r.                   \tag{2}
\]

If the suffix prime \(p\nmid c\) has forbidden set
\({\cal A}_p\subset\mathbb Z/p\mathbb Z\), its transformed forbidden set in
the \(s\)-coordinate is

\[
 {\cal B}_{p,r,c}
 =c^{-1}({\cal A}_p-r)-L_r\pmod p.                    \tag{3}
\]

Put \(u_r=r+cL_r\). It is the unique representative of \(r\bmod c\) in
\((A-c,A]\), and (3) becomes

\[
 {\cal B}_{p,r,c}=c^{-1}({\cal A}_p-u_r)\pmod p.       \tag{4}
\]

As \(r\) runs through a complete residue system, \(u_r\) runs bijectively
through the \(c\) consecutive integers in \((A-c,A]\). Hence all suffix
phases share the same inherited base point \(u_r\); they are not independent
arbitrary \(H\)-sets.

The exact frontier correlation is therefore

\[
 \boxed{
 \sum_{n\in I}g_c(n)W_{\rm suf}(n)
 =\sum_{r\bmod c}g_c(r)
   \sum_{1\le s\le M_r}
   \prod_{p\ {\rm in\ suffix}}
   \{1-b\,1_{{\cal B}_{p,r,c}}(s)\}.
 }                                                     \tag{5}
\]

Only two adjacent values of \(L_r\), and only
\(\lfloor N/c\rfloor,\lceil N/c\rceil\) for \(M_r\), occur. Formula (5) is
the phase-preserving state to be estimated.

## 2. Why separate absolute values cannot exploit (5)

Continue with the round-9 parameters

\[
 H=L_1^2\{1+o(1)\},\qquad
 q=\lfloor L_3\rfloor,\qquad
 b=1-(1-a)^q,\qquad
 bH=(qC+o(q)){L_1\over L_2},
\]

and

\[
 D=Xe^{-2\Phi},\qquad \Phi={L_1L_3\over L_2},\qquad
 z=e^{L_1/L_2}.
\]

Let

\[
 d=\left\lceil{\log D\over\log z}\right\rceil+1
   =L_2-2L_3+O(1).                                    \tag{6}
\]

Choose a point \(y_0<z\) with
\[
 \log y_0={\log D\over d}+1.
\]
The extra \(+1\) in the definition of \(d\) guarantees \(y_0<z\)
uniformly, without making any assumption on the fractional part of
\(\log D/\log z\): indeed
\(d-\log D/\log z\ge1\), while \(\log z/d\to\infty\).
Then choose a very narrow prime band
\({\cal B}=(y_0,y_1]\) so that

\[
 S_{\cal B}:=\sum_{p\in{\cal B}}\rho_p=(1+o(1))d,
\qquad
 \rho_p={\mathbb E|d_p|\over m_p}.
                                                               \tag{7}
\]

Such a band exists: throughout this band,
\(\rho_p=(2+o(1))bH/p\), so its required reciprocal width is

\[
 w={d\over2bH}
   =(1+o(1)){L_2^2\over2qCL_1}=o(1),                  \tag{8}
\]

while the number of available primes tends to infinity much faster than
\(d\). The band is narrow enough that
\[
 d\log y_0>\log D,\qquad
 (d-1)\log y_1<\log D.
\]
Indeed, the margin in the second inequality has scale
\(\log D/d\asymp\log z\), whereas the band perturbation has only
iterated-logarithmic scale. Every \(d\)-set \(T\subset{\cal B}\) is
therefore a valid decreasing-order frontier:

\[
 c(T)>D,\qquad {c(T)\over\min T}\le y_1^{d-1}<D,
 \qquad c(T)\le D\min T<Dz.                            \tag{9}
\]

The individual \(\rho_p\)'s are \(o(1/d)\). Sampling \(d\) times from the
probability weights \(\rho_p/S_{\cal B}\), the collision probability is
\(o(1)\). Consequently

\[
 e_d((\rho_p)_{p\in{\cal B}})
 =(1-o(1)){S_{\cal B}^d\over d!}
 =\exp\{d+o(d)\}.                                     \tag{10}
\]

For all these terminal frontiers, the suffix contains every prime below
\(y_0\). Since
\[
 \log\log z-\log\log y_0=O(1/L_2)=o(L)
\]
(and the additional band width (8) is smaller still),

\[
 \mu_{\rm suf}^{-1}
 =\exp\{(1+o(1))bHL\}
 =X^{qC(1-o(1))}.                                     \tag{11}
\]

Thus the normalized coefficient produced by bounding each suffix by one
and then summing absolute frontier \(L^1\)-masses satisfies the strict lower
bound

\[
 \boxed{
 \sum_{\substack{T\ {\rm frontier}\\T\subset{\cal B}}}
 {1\over\mu_{\rm suf}}\prod_{p\in T}\rho_p
 \ge X^{qC(1-o(1))}\exp\{L_2+o(L_2)\}.
 }                                                     \tag{12}
\]

This is not a lower bound for the actual signed tail. It is a lower bound
for the cost of the architecture that takes absolute values before using
the joint \(r,T\) phase.

Although the displayed round-9 specialization took
\(q=\lfloor L_3\rfloor\), the same construction applies to every fixed
integer \(q\ge1\). Then
\(bH=(qC+o(1))L_1/L_2\), the required band width in (8) is still
\(o(1)\) and still fits inside the margin below \(z\), and (11)--(12)
become \(X^{qC(1-o(1))}\) with the same
\(\exp\{L_2+o(L_2)\}\) factor. Thus the barrier also covers the fixed-
moment target in `fixed_power_additive_sufficiency.md`.

## 3. Consequence

The round-9 subpower *unnormalized* frontier mass is compatible with (12):
the fatal factor is precisely the almost-full suffix zero mode. Therefore
the next estimate must preserve both of the following cancellations:

1. the mean-zero signs inside \(g_c(r)\) as \(r\) ranges over the inherited
   block \((A-c,A]\);
2. cancellation across distinct top-band frontier sets \(T\), whose CRT
   conductors and phases differ.

Keeping only the interval length and suffix endpoint is still insufficient
if the \(T\)-dependent inherited phase is replaced by absolute values.

Strict status: **exact phase state plus an architecture no-go; full signed
tail and Erdős #679 remain open**.
