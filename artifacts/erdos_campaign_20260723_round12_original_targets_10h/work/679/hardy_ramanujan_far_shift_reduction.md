# #679: an unconditional far-shift reduction

Date: 2026-07-23

This note removes all sufficiently far shifts for almost every integer at a
dyadic scale.  It is useful for locating the genuine difficulty, but it does
not supply an integer that is simultaneously good in the exceptional near
range and hence does not close Erdős #679.

## 1. Uniform Hardy--Ramanujan input

We use the classical uniform Hardy--Ramanujan inequality: there is an
absolute constant \(C_0\) such that, uniformly for \(x\ge3\) and integers
\(j\ge1\),

\[
 \#\{m\le x:\omega(m)=j\}
 \ll {x\over\log x}
      { (\log_2x+C_0)^{j-1}\over(j-1)!}.             \tag{1}
\]

The all-\(j\) uniformity in (1) matters here; a fixed-parameter
Sathe--Selberg asymptotic would not cover the required upper tail.

Fix \(\varepsilon>0\).  More generally, choose any fixed

\[
 D>{1+\varepsilon\over\varepsilon},
 \qquad
 \eta_D=(1+\varepsilon)\left(1-{1\over D}\right)-1>0,
\]

and set

\[
 K_X=\left\lceil
       \exp\{(\log_2X)^D\}\right\rceil.             \tag{2}
\]

This is still \(X^{o(1)}\).  For \(k\ge K_X\), write

\[
 u=\log k,\qquad v=\log_2k,
 \qquad r_k=\left\lceil
 (1+\varepsilon){u\over v}\right\rceil.             \tag{3}
\]

Put \(B_X=\log_2(2X)+C_0\).  Since \(v\ge
D\log_3X\), one has, uniformly for \(K_X\le k\le2X\),

\[
 r_k\ge2B_X                                                   \tag{4}
\]

and, for all sufficiently large \(X\),

\[
 (r_k-1)\log{r_k-1\over eB_X}
 \ge(1+\eta_D/2)\log k.                            \tag{5}
\]

For clarity, (5) is not an appeal to an unspecified large-deviation
asymptotic.  From (3), uniformly in the stated range,
\((r_k-1)v/u=1+\varepsilon-o(1)\), while

\[
 \log{r_k-1\over eB_X}
 \ge v-\log v-\log B_X+O_\varepsilon(1).
\]

The loss divided by \(v\) is maximal at the lower endpoint, up to an
\(o(1)\) term, and there it is

\[
 {\log B_X\over v}+{\log v+O_\varepsilon(1)\over v}
 ={1\over D}+o(1).
\]

Therefore the left side of (5), divided by \(u=\log k\), is at least

\[
 (1+\varepsilon)\left(1-{1\over D}\right)-o(1)
 =1+\eta_D-o(1),
\]

which proves (5).  The condition \(D>(1+\varepsilon)/\varepsilon\) is
the exact strict inequality needed by this pointwise-tail-plus-union
architecture.

## 2. Summing all far bad shifts

When \(r\ge2B_X\), the terms on the right of (1) have successive ratio at
most \(1/2\).  Stirling's elementary lower bound therefore gives

\[
 \begin{aligned}
 \#\{m\le2X:\omega(m)\ge r_k\}
 &\ll {X\over\log X}
       \left({eB_X\over r_k-1}\right)^{r_k-1}\\
 &\ll {X\over\log X}\,k^{-1-\eta_D/2}.             \tag{6}
 \end{aligned}
\]

For a fixed \(k\), the map \(n\mapsto m=n-k\) shows that (6) also bounds
the number of \(n\in[X,2X]\) with \(k<n\) and

\[
 \omega(n-k)\ge(1+\varepsilon){\log k\over\log_2k}.
\]

A union bound over every integer \(K_X\le k<2X\) now proves

\[
 \boxed{
 \#\left\{n\in[X,2X]:
 \begin{array}{c}
 \text{some }K_X\le k<n\text{ violates the}\cr
 \text{first inequality in Erd\H{o}s \#679}
 \end{array}\right\}
 \ll_{\varepsilon,D} {X\over\log X}\,K_X^{-\eta_D/2}.}       \tag{7}
\]

Equivalently, a proportion

\[
 1-O_{\varepsilon,D}\!\left(
 {K_X^{-\eta_D/2}\over\log X}\right)
\]

of \(n\in[X,2X]\) satisfies the desired strict inequality for every
\(K_X\le k<n\).

## 3. Exact remaining interface

Equation (7) shows that the original obstruction is confined to the
subpower but still very long range

\[
 K_\varepsilon\le k<K_X
 =\exp\{(\log_2X)^D\}.                               \tag{8}
\]

It would be enough to construct a near-good integer outside the exceptional
set in (7), or to prove the analogue of (7) under a probability weight that
constructs a near-good integer.  Neither follows from cardinality alone:
the exceptional set in (7), although of density \(o(1)\), can still have
\(X^{1-o(1)}\) elements, while known near-shift constructions only prove
existence under a highly nonuniform sieve weight.

Thus (7) cannot be intersected blindly with Lau's theorem or with the
moving-conductor reduction.  It is an unconditional and quantifier-correct
far-shift theorem, not a proof of the existence of even one full #679
candidate.  The original first question remains open.

A convenient explicit specialization is

\[
 D={2(1+\varepsilon)\over\varepsilon}.
\]

Then \(\eta_D=\varepsilon/2\), so (7) retains the saving
\(K_X^{-\varepsilon/4}\) while reducing the previously used safe exponent
\(16(1+\varepsilon)/\varepsilon\) by a factor of eight.

## 4. Critical-power refinement

The strict power loss \(D>(1+\varepsilon)/\varepsilon\) can itself be
removed by retaining the next logarithmic term.  Put

\[
 A=1+\varepsilon,\qquad
 D_0={A\over\varepsilon},qquad
 B=\log_2X,qquad L=\log_3X,
\]

choose a fixed constant

\[
 C_*>\left({e\over\varepsilon}\right)^{D_0},
 \qquad
 c_*:=\log C_*-D_0\log(e/\varepsilon)>0,            \tag{9}
\]

and define

\[
 K_X^*=\left\lceil
 \exp\{C_*B^{D_0}L^{D_0}\}\right\rceil,
 \qquad
 \xi_X={A c_*\over5D_0^2L}.                        \tag{10}
\]

At the lower endpoint, with \(u=\log K_X^*\) and \(v=\log u\),

\[
 v=D_0L+D_0\log L+\log C_*+o(1).
\]

The exact next-order excess over the unit exponent is controlled by

\[
 \begin{aligned}
 &v-D_0\{L+\log v-\log A+1\}\\
 &\qquad=\log C_*-D_0\log D_0+D_0\log A-D_0+o(1)\\
 &\qquad=c_*+o(1),                                  \tag{11}
 \end{aligned}
\]

where \(D_0/A=1/\varepsilon\).  Therefore the left side of (5), divided
by \(u\), is

\[
 A\left\{1-{L+\log v-\log A+1+o(1)\over v}\right\}
 \ge1+\xi_X                                          \tag{12}
\]

for all sufficiently large \(X\).  The expression is increasing with
\(v\) in the relevant range, so (12) holds uniformly for every
\(k\ge K_X^*\).  The geometric factorial-tail argument and summation now
give

\[
 \boxed{
 \#\{n\in[X,2X]:\text{some }K_X^*\le k<n
       \text{ violates #679}\}
 \ll_{\varepsilon,C_*} {X\over\log X}\,
 { (K_X^*)^{-\xi_X}\over\xi_X}.}                   \tag{13}
\]

Here \(\xi_X\asymp_\varepsilon1/\log_3X\), but

\[
 \xi_X\log K_X^*
 \asymp_\varepsilon B^{D_0}L^{D_0-1}\to\infty,
\]

so (13) is still a strong density-zero estimate.  This critical-power
cutoff is smaller than \(\exp(B^D)\) for every fixed \(D>D_0\).  The
constant boundary \(C_*=(e/\varepsilon)^{D_0}\) is resolved more finely
below.

## 5. The constant boundary and a tending-to-critical cutoff

Put \(M=\log_4X=\log L\),
\(c_0=\log(e/\varepsilon)=1-\log\varepsilon\), and
\(C_0=(e/\varepsilon)^{D_0}\).  At the literal constant boundary
\(C_*=C_0\), the cancellation in (11) has the exact next sign

\[
 \begin{aligned}
 v-D_0\{L+\log v-\log A+1\}
 &=-D_0\log\left(1+{M+c_0\over L}\right)+o(M/L)\\
 &=-{D_0M\over L}(1+o(1))<0.                         \tag{14}
 \end{aligned}
\]

Thus equality is actually on the wrong side for this pointwise
Hardy--Ramanujan union-bound architecture; merely replacing \(>\) by
\(=\) in (9) is invalid.

One can nevertheless let the coefficient tend to the boundary.  Define

\[
 C_X=C_0\exp\left({3D_0M\over L}\right),\qquad
 K_X^\dagger=\left\lceil
 \exp\{C_XB^{D_0}L^{D_0}\}\right\rceil,\qquad
 \xi_X^\dagger={AM\over5D_0L^2}.                     \tag{15}
\]

Now

\[
 v=D_0\{L+M+c_0+3M/L\}+o(1).
\]

Writing \(a=(M+c_0+3M/L)/L\), direct substitution gives

\[
 \begin{aligned}
 v-D_0\{L+\log v-\log A+1\}
 &=D_0\{3M/L-\log(1+a)\}+o(M/L)\\
 &={D_0(2M-c_0)\over L}
   +O_\varepsilon(D_0M^2/L^2)\\
 &\ge {D_0M\over L}                                  \tag{16}
 \end{aligned}
\]

eventually.  Since \(v\sim D_0L\), (16) makes the exponent in (12) at
least \(1+\xi_X^\dagger\).  Its derivative with respect to \(v\) is
positive in this range, so the estimate is again uniform for all larger
\(k\).  The same geometric-tail summation yields

\[
 \boxed{
 \#\{n\in[X,2X]:\text{some }K_X^\dagger\le k<n
       \text{ violates #679}\}
 \ll_\varepsilon {X\over\log X}\,
 { (K_X^\dagger)^{-\xi_X^\dagger}\over
   \xi_X^\dagger}.}                                  \tag{17}
\]

The quantifiers here are: first fix \(\varepsilon>0\), hence fix
\(D_0=1+1/\varepsilon\) and \(C_0\); then let \(X\to\infty\), allowing
only the displayed \(C_X\) and \(K_X^\dagger\) to vary.  In particular,

\[
 {C_X\over C_0}=1+O_\varepsilon(M/L)\to1,\qquad
 \xi_X^\dagger>0,
\]

and, term by term,

\[
 \xi_X^\dagger\log K_X^\dagger
 ={AC_X\over5D_0}\,
   B^{D_0}M L^{D_0-2}\longrightarrow\infty,           \tag{18}
\]

while \(\log K_X^\dagger=o(\log X)\).  Ceiling the cutoff, the integer
threshold for \(r_k\), replacing \(\log_2(2X)\) by \(B\), and the
\(O(1)\) in the uniform Hardy--Ramanujan inequality perturb the normalised
exponent by
\(O_\varepsilon(1/B+L^2/\log K_X^\dagger)=o(M/L^2)\);
they cannot reverse (16).

Hence (17) reaches the critical constant up to an explicit relative
\(O_\varepsilon(\log_4X/\log_3X)\) inflation.  The negative sign at
literal equality classifies only this Hardy--Ramanujan union-bound method;
it is not a boundary theorem for the original problem.  The result remains
an almost-all far-shift theorem with a growing cutoff, not a candidate
construction and not a closure of #679.

Primary modern statement of the uniform input: Steve Fan, *The
Hardy--Ramanujan inequality for sifted sets and its applications*,
arXiv:2508.06005 (the displayed classical inequality in its abstract and
introduction).
