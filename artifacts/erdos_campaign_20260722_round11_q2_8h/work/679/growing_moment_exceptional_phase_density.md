# #679: growing-moment exceptional-phase density

Date: 2026-07-22

The growing moment also strengthens round 10's almost-all CRT-phase
statement from a fixed power of \(X\) to an exponential in \(HL\). This
is unconditional but still does not locate the actual dyadic start.

## 1. Point density

Let \(A\) be uniform modulo

\[
 Q=\prod_{H<p\le z}p.
\]

CRT independence and the exact first moment give

\[
 \mathbb E_A W(A)^q=\mu_q=e^{-(1+o(1))HL}.          \tag{1}
\]

If the selected-prime incidence count satisfies \(T(A)\le R\), then

\[
 W(A)^q=t^{qT(A)}\ge t^{qR},
 \qquad t^{-qR}=e^{o(HL)}.
\]

Markov's inequality therefore proves

\[
 {1\over Q}\#\{A\bmod Q:T(A)\le R\}
 \le t^{-qR}\mu_q
 =e^{-(1-o(1))HL}.                                 \tag{2}
\]

This is a local necessary-condition density, not a count of original
candidates in the self-consistent range.

## 2. Interval-start density

For an interval length \(N\asymp X\), define

\[
 S_N(A)=\sum_{1\le m\le N}W(A+m)^q.
\]

Translation invariance modulo \(Q\) gives exactly

\[
 \mathbb E_A S_N(A)=N\mu_q=e^{-(1+o(1))HL},         \tag{3}
\]

because \(\log N=o(HL)\). If the interval contains even one point with
\(T\le R\), then \(S_N(A)\ge t^{qR}\). A second application of Markov
therefore gives

\[
 {1\over Q}\#\{A\bmod Q:S_N(A)\ge t^{qR}\}
 \le Nt^{-qR}\mu_q
 =e^{-(1-o(1))HL}.                                 \tag{4}
\]

Thus all but an \(e^{-(1-o(1))HL}\) fraction of complete-period starts
have no local candidate.

## 3. Why (4) does not transfer to the actual start

The period has

\[
 \log Q=(1+o(1))z\gg HL.
\]

Hence the absolute number
\(Qe^{-(1-o(1))HL}\) of starts allowed by (4) is still enormous.
Moreover a CRT point \(n_0\) with \(W(n_0)^q=1\) makes every one of the
roughly \(N\) interval starts whose interval contains \(n_0\) exceptional.
So exceptional starts can cluster on the full physical interval scale
even while obeying (4).

The CRT representative is generally at scale \(Q\), not at the
self-consistent location \(A\asymp X\). Therefore (4) is a strict
almost-all-phase theorem but cannot be promoted to the original problem
without a location-sensitive input.

Strict status: **exceptional CRT-start density
\(e^{-(1-o(1))HL}\); actual dyadic start and Erdős #679 remain open**.
