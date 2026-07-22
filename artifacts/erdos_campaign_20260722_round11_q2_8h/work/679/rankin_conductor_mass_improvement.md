# #679: fixed-moment Rankin conductor mass and a polynomial-in-z suffix

Date: 2026-07-22

Round 10 showed that a fixed Markov moment is sufficient. At fixed moment,
the conductor mass admits a substantially sharper Rankin bound than the
degree-only estimate used in round 9. This moves the deterministic transfer
cutoff to within a fixed power of the prime endpoint.

## 1. Rankin bound

Retain

\[
 H=\lfloor L_1^2\rfloor,\qquad z=e^{L_1/L_2},
 \qquad L=\sum_{H<p\le z}{1\over p}\sim L_2,
\]

and fix an integer \(q\ge1\) and \(C>1\). For \(W^q\), put

\[
 b=1-(1-a)^q,qquad a={CL_1\over HL},
 \qquad \rho_p={{\mathbb E}|d_p|\over m_p}.
\]

For all sufficiently large \(X\),

\[
 \rho_p\le {3bH\over p}.                              \tag{1}
\]

Define

\[
 {\cal F}(Y)=\sum_{\substack{T\subseteq{\cal P}\\c(T)\le Y}}
                  \prod_{p\in T}\rho_p,
 \qquad c(T)=\prod_{p\in T}p.                        \tag{2}
\]

For every \(s>0\), Rankin's trick gives

\[
 {\cal F}(Y)
 \le Y^s\prod_{H<p\le z}(1+\rho_pp^{-s})
 \le\exp\left\{s\log Y+3bH
                 \sum_{p>H}p^{-1-s}\right\}.         \tag{3}
\]

Take

\[
 s={1\over\log H}.                                    \tag{4}
\]

There is an absolute constant \(C_0\) such that

\[
 \sum_{p>H}p^{-1-1/\log H}\le C_0.                  \tag{5}
\]

For completeness, (5) follows from the Chebyshev upper bound
\(\pi(t)\ll t/\log t\) and partial summation:

\[
 \sum_{p>H}p^{-1-s}
 \ll\int_H^\infty {t^{-1-s}\over\log t}\,dt
 =\int_1^\infty {e^{-v}\over v}\,dv=O(1),            \tag{6}
\]

after \(t=H^v\). Since \(b\le qa\),

\[
 bH\le {qCL_1\over L}=O_{q,C}(L_1/L_2).              \tag{7}
\]

Equations (3)--(7), uniformly for \(Y\le Xz\), prove that a constant
\(K=K(q,C)>0\) exists with

\[
 \boxed{{\cal F}(Y)\le z^K\qquad(Y\le Xz).}          \tag{8}
\]

This replaces the earlier
\(\log{\cal F}\le(1/2+o_C(1))\Phi\), where
\(\Phi=L_1L_3/L_2\), by

\[
 \log{\cal F}(Xz)=O_{q,C}(L_1/L_2)=O_{q,C}(\log z).  \tag{9}
\]

The fixed-\(q\) hypothesis is essential to this improvement. With
\(q\asymp L_3\), the second term in (3) is again of order \(\Phi\).

## 2. Deterministic transfer to \(N/z^B\)

Let \(I=(A,A+N]\subset[X,3X]\), with \(N\asymp X\), and choose a fixed
constant

\[
 B>K+4,
 \qquad D=N z^{-B}.                                   \tag{10}
\]

Write \({\cal L}_{D,q}\) for the ANOVA sum over \(c(T)\le D\). Every
nonconstant term has mean zero and period \(c(T)\), so one incomplete period
and its exact period \(L^1\)-mean give

\[
 \left|\sum_{n\in I}F_T(n)\right|
 \le c(T)\mu_q\prod_{p\in T}\rho_p.                 \tag{11}
\]

Summing (11), then using (8) and (10), yields

\[
 \boxed{
 \sum_{n\in I}{\cal L}_{D,q}(n)
 =N\mu_q\{1+O(z^{-4})\}.}                            \tag{12}
\]

Here changing the harmless margin \(4\) changes the displayed power of
\(z\). Thus the rigorously transferred conductor range is

\[
 D={N\over z^{B(q,C)}},                               \tag{13}
\]

instead of \(N/z^{2L_3}\) in the round-10 starting point.

## 3. New stopping state

Order primes decreasingly and stop when the selected conductor first exceeds
\(D\). Every frontier conductor satisfies

\[
 D<c\le Dz<N.                                        \tag{14}
\]

After conditioning modulo \(c\), the exact inherited suffix interval has

\[
 {N\over c}+O(1)\in[z^{B-1}+O(1),z^B+O(1)].          \tag{15}
\]

Moreover the total absolute frontier mass is at most

\[
 {\cal F}(Dz)\le z^K.                                \tag{16}
\]

Consequently the unresolved deterministic object is now a joint inherited-
phase suffix correlation on an interval only a fixed power of its prime
endpoint. No arbitrary-start suffix supremum is introduced.

For \(q=1,C>1\), \(N\mu_1=X^{1-C+o(1)}\), so round 10's fixed-power
reduction still says that any \(O(X^{-\delta})\) estimate for the whole
signed frontier aggregate closes the candidate interval.

## 4. Boundary

Equations (8), (12), and (15) are unconditional deterministic improvements.
They do not bound the remaining signed frontier aggregate. In particular,
the suffix mean is still about \(X^{-qC}\), and the arbitrary-start CRT
spike and run counterexamples remain applicable if the inherited phase is
discarded.

Strict status: **changed conductor/suffix scale from a moving
\(z^{\Theta(L_3)}\) loss to a fixed \(z^{O_{q,C}(1)}\) loss; full signed
tail and Erdős #679 remain open**.
