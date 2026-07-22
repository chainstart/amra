# #679: a growing-moment reduction to ultra-high conductors

Date: 2026-07-22

The fixed-moment middle-range theorem can be strengthened substantially by
letting the Markov moment grow. The clean formulation below avoids
normalizing by small local means near the lower prime endpoint and works
directly with the exact first and second moments.

It is a deterministic reduction at the actual interval start. It does not
bound the final signed ultra-high-conductor aggregate.

## 1. Growing moment and exact complete moments

Retain

\[
 H=\lfloor L_1^2\rfloor,\qquad
 z=\exp(L_1/L_2),\qquad
 L=\sum_{H<p\le z}{1\over p}\sim L_2,
\]

\[
 a={CL_1\over HL},\qquad t=1-a,
\]

where \(C>0\) is fixed. Choose a function

\[
 s=s(X)\longrightarrow\infty,\qquad s=o(L_3),
\]

and the integer moment

\[
 q=\left\lfloor{s\over a}\right\rfloor.              \tag{1}
\]

Then \(qa=s+o(1)\). Put

\[
 b_1=1-t^q,\qquad b_2=1-t^{2q}.
\]

Since \(q\log(1-a)=-s+o(1)\),

\[
 b_1=1-e^{-s+o(1)}=1-o(1),\qquad b_2=1-o(1).         \tag{2}
\]

For the collision-free local indicator \(X_p\), the exact first and second
complete-period means are

\[
 \mu_q=\prod_{H<p\le z}\left(1-{b_1H\over p}\right),
 \qquad
 M_{2,q}=\prod_{H<p\le z}\left(1-{b_2H\over p}\right). \tag{3}
\]

Both satisfy

\[
 \boxed{
 \log\mu_q=-(1+o(1))HL,\qquad
 \log M_{2,q}=-(1+o(1))HL.}                          \tag{4}
\]

Here one must not use a uniform Taylor expansion at primes immediately
above \(H\). Split instead at \(2H\). For \(p\ge2H\), Taylor expansion gives
the main term \(-b_iH/p\) and total quadratic error

\[
 O\left(H^2\sum_{p\ge2H}p^{-2}\right)
 =O(H/\log H)=o(HL).
\]

The whole interval \(H<p<2H\) contains \(O(H/\log H)\) primes. Its
contribution is \(O((s+\log H)H/\log H)=o(HL)\): the local factor is at
least \(e^{-2s+o(1)}(1-H/p)\), and \(s=o(L_3)\). Finally, replacing \(b_i\)
by one above \(2H\) costs \(o(HL)\) by (2). This proves (4) without a false
claim that every local mean is \(1-o(1)\).

## 2. Primitive large sieve at a moving conductor level

Expand

\[
 W(n)^q=\sum_{T\subseteq{\cal P}}F_T(n),\qquad
 F_T(n)=\prod_{p\notin T}m_p\prod_{p\in T}d_p(n),
\]

where \(m_p=1-b_1H/p\) and \(d_p\) has local mean zero. Every nonconstant
\(F_T\) has full conductor \(c(T)=\prod_{p\in T}p\), and its Fourier
support consists only of primitive fractions \(u/c(T)\). Distinct full
conductors therefore give distinct reduced fractions.

Parseval and ANOVA orthogonality give

\[
 \sum_T\sum_{u\bmod c(T)}^*
       |\widehat F_T(u)|^2=M_{2,q},                  \tag{5}
\]

where the zero-frequency term is understood separately for
\(T=\varnothing\). There is an additional full exponential gain for low
conductors which is lost if one merely bounds a subcollection by
\(M_{2,q}\).

Put

\[
 \sigma_p^2=\mathbb E d_p^2,\qquad
 \theta_p={\sigma_p^2\over m_p^2+\sigma_p^2}.
\]

After dividing every ANOVA energy by \(M_{2,q}\), membership \(p\in T\)
is an independent, not necessarily identically distributed, Bernoulli
variable of parameter \(\theta_p\). If \(x=H/p\), then exactly

\[
 \theta_p={b_1^2x(1-x)\over
                  1-(2b_1-b_1^2)x}\le x.            \tag{5a}
\]

For \(p\ge2H\), \(x\le1/2\), and hence, uniformly in this whole range,

\[
 {\theta_p\over x}
 ={b_1^2(1-x)\over1-x+(1-b_1)^2x}
 =1+O(1-b_1)=1+o(1).
\]

The omitted range \(H<p<2H\) contributes only
\(O(H/\log H)=o(HL)\). Therefore

\[
 \Lambda:=\sum_p\theta_p=(1+o(1))HL.                \tag{5b}
\]

Fix a constant \(\alpha>0\). Since every selected prime is \(>H\),
\(c(T)\le\exp(\alpha HL)\) implies

\[
 |T|\le r_\alpha:={\alpha HL\over\log H}
 =\left({\alpha\over2}+o(1)\right)H.                \tag{5c}
\]

Here \(\log H=2L_2+o(1)\) and \(L\sim L_2\). In particular,
\(\Lambda/r_\alpha\asymp L_2\), so
\[
 r_\alpha\log(\Lambda/r_\alpha)=O_\alpha(HL_3)=o(HL).
\]

For completeness, this lower-tail estimate does not use an iid
assumption. If \(S=\sum_p1_{p\in T}\) and \(0<y<1\), independence gives

\[
 \mathbb Ey^S
 =\prod_p(1-\theta_p+\theta_py)
 \le\exp\{-(1-y)\Lambda\}.
\]

On \(S\le r_\alpha\), \(y^S\ge y^{r_\alpha}\). Taking
\(y=r_\alpha/\Lambda\) (and harmlessly rounding \(r_\alpha\)) yields

\[
 \mathbb P(c(T)\le e^{\alpha HL})
 \le\mathbb P(S\le r_\alpha)
 \le\exp\{-\Lambda+r_\alpha+
                 r_\alpha\log(\Lambda/r_\alpha)\}
 =\exp\{-(1-o(1))HL\}.                              \tag{5d}
\]

Combining (4), (5), and (5d), the total Fourier energy, including the
empty set if desired, below any fixed exponential level is

\[
 \sum_{\substack{T:\ c(T)\le e^{\alpha HL}}}
 \ \sum_{u\bmod c(T)}^*|\widehat F_T(u)|^2
 \le \exp\{-(2-o(1))HL\}.                           \tag{5e}
\]

The exponent \(2\) remains sharp even after removing the empty set. Indeed,
for \(p\ge2H\),
\[
 v_p:={\sigma_p^2\over m_p^2}
 ={H/p\over1-H/p}(1+o(1))
\]
uniformly, and
\[
 \sum_{p\ge2H}v_p=(1+o(1))HL.
\]
All one-prime conductors satisfy \(p\le z<e^{\alpha HL}\), so their total
energy is
\[
 \mu_q^2\sum_{p\ge2H}v_p=\exp\{-(2+o(1))HL\}.
\]
Together with (5e), the nonconstant low-conductor energy has logarithmic
asymptotic \(-(2+o(1))HL\). The empty-set energy has the same exponential
scale but is not responsible for this endpoint.

Now fix \(0<\eta<1\), set \(\alpha=1-\eta\), and only afterward let
\(X\to\infty\). Define

\[
 {\cal A}_X=(1-\eta){HL\over L_1},
 \qquad
 {\cal C}_X=X^{{\cal A}_X}
            =\exp\{(1-\eta)HL\}.                    \tag{6}
\]

Let

\[
 {\cal E}_{\le{\cal C}}(n)
 =\sum_{1<c(T)\le{\cal C}_X}F_T(n).                  \tag{7}
\]

All frequencies in (7) are primitive and are separated by at least
\({\cal C}_X^{-2}\). Distinct \(T\)'s have distinct squarefree full
conductors, so there is no multiplicity hidden in the coefficient norm.
The additive large sieve and (5e) give, for every interval \(I\) of
\(N\asymp X\) consecutive integers, uniformly in its integer start,

\[
 \begin{aligned}
 \sum_{n\in I}|{\cal E}_{\le{\cal C}}(n)|^2
 &\le (N-1+{\cal C}_X^2)\exp\{-(2-o(1))HL\},\\
 \left|\sum_{n\in I}{\cal E}_{\le{\cal C}}(n)\right|
 &\le \exp\{-(\eta-o(1))HL\}.                        \tag{8}
 \end{aligned}
\]

The zero mode separately satisfies

\[
 N\mu_q\le\exp\{-(1+o(1))HL\}.                       \tag{9}
\]

Since \(H=L_1^2\) and \(L\sim L_2\), the cutoff exponent is

\[
 \boxed{
 {\cal A}_X=\left(1-\eta+o(1)\right)L_1L_2.}         \tag{10}
\]

Thus (8) controls conductors vastly beyond \(X^A\) for every fixed \(A\).

## 3. What a candidate would force

For a candidate and the block of \(H\) shifts beginning at
\(K\asymp H\), round 10's threshold ledger gives

\[
 R=\sum_{j<H}r(K+j)
 \le (2+o_\varepsilon(1))(1+\varepsilon){HL_2\over L_3}. \tag{11}
\]

Every candidate contributes at least \(t^{qR}\) to \(W^q\). By (1),

\[
 t^{-qR}
 \le\exp\left\{(2+o_\varepsilon(1))(1+\varepsilon)
                    {sHL_2\over L_3}\right\}
 =\exp\{o(HL)\},                                     \tag{12}
\]

because \(L\sim L_2\) and \(s=o(L_3)\).

Define the remaining signed aggregate

\[
 {\cal E}_{>{\cal C}}(n)
 =\sum_{c(T)>{\cal C}_X}F_T(n).                      \tag{13}
\]

If a candidate occurs in \(I\), then positivity of its contribution and
(8)--(12) force

\[
 \boxed{
 \sum_{n\in I}{\cal E}_{>{\cal C}}(n)
 \ge {1\over2}\,t^{qR}
 =\exp\{-o(HL)\}}                                    \tag{14}
\]

for all sufficiently large \(X\). Indeed, the zero mode plus the absolute
value of the whole conductor range in (7) is
\(\exp\{-(\eta+o(1))HL\}=o(t^{qR})\).

Consequently, it is enough to prove any deterministic upper bound

\[
 \sum_{n\in I}{\cal E}_{>{\cal C}}(n)
 \le\exp\{-\delta HL\}                               \tag{15}
\]

with fixed \(\delta>0\), or even any bound that is
\(o(t^{qR})\), at the actual dyadic start.

## 4. Boundary

This changes the location and scale of the unresolved tail:

* fixed-moment Rankin transfer reached \(X/z^{O(1)}\);
* fixed-moment primitive large sieve reached any prescribed \(X^A\);
* the growing moment reaches
  \[
  X^{(1-\eta+o(1))L_1L_2}.
  \]

The last range is obtained from the exact \(L^2\) mass together with a
Poisson-binomial small-deviation estimate for the low-conductor energy,
not from a complete-period density assertion, and is uniform in the
actual interval start.

It does not control (13). Indeed, choose by CRT one point avoiding every
local forbidden block and put it inside an arbitrary-start interval of
length \(N\asymp X\). Positivity gives total \(W^q\)-mass at least one,
while (8)--(9) remain exponentially small uniformly in that start; hence
the high signed aggregate on this interval is at least \(1-o(1)\).
Therefore a phase-uniform interval theorem is false, not merely missing.
The CRT representative is not constrained to the self-consistent scale
\(A\asymp X\). A successful final step must use that actual location or
cancellation inside its joint ultra-high primitive spectrum.

Strict status: **deterministic moving-conductor reduction; the final signed
aggregate (13) and Erdős #679 remain open**.

## 5. Fixed-power block robustness

The exponent \(2\) in \(H=\lfloor L_1^2\rfloor\) is not essential to the
reduction. Fix any constant \(d\ge1\) and instead take
\[
 H=\lfloor L_1^d\rfloor .
\]
Then \(H=o(z)\), \(\log H=dL_2+o(1)\), and the same prime band still has
\(L\sim L_2\). The lower-end complete-moment error is \(O(H)=o(HL)\);
(5b) remains \(\Lambda=(1+o(1))HL\); and (5c) becomes
\[
 r_\alpha=(\alpha/d+o(1))H,
\qquad
 r_\alpha\log(\Lambda/r_\alpha)=O_d(HL_3)=o(HL).
\]
Thus (5e)--(8) hold verbatim with cutoff
\[
 \exp\{(1-\eta)HL\}
 =X^{(1-\eta+o(1))L_1^{d-1}L_2}.
\]
Also \(HL\gg L_1\), including at \(d=1\), so the interval-length and zero
mode terms remain negligible. At shifts \(k\asymp H\), the candidate
threshold in (11) changes from coefficient \(2\) to \(d\), and (12) still
follows from \(s=o(L_3)\). Hence the whole signed-tail reduction is valid
for every fixed \(d\ge1\). This robustness does not prove any
short-interval high-\(\omega\) assertion.
