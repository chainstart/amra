# Erdős #679: conductor truncation transfers the critical CRT weight past one period

Date: 2026-07-22 (Asia/Hong_Kong)

Status: new strict partial theorem.  It repairs the *incomplete-period transfer*
step for the collision-free critical band when the modulus is chosen as the
first prime-prefix modulus exceeding the interval length.  The zero-frequency
large-deviation exponent is still \(o(\log X)\), so this does not make the
candidate count less than one and does not settle the first question in #679.

## 1. Statement

Let \(X\to\infty\), let \(N\asymp X\), and suppose

\[
 H=(\log X)^{o(1)},\qquad H\longrightarrow\infty.
\]

Starting with the primes larger than \(H\), stop at the first prime \(z\) for
which

\[
 Q=\prod_{H<p\le z}p>N.                                      \tag{1}
\]

For consecutive, pairwise distinct shifts \(k_j=K+j\), \(0\le j<H\), and
\(1/2\le t<1\), put

\[
 W(a)=t^{\sum_{j<H}\#\{p:H<p\le z,\ p\mid a-k_j\}}.
\]

Let

\[
 \mu={1\over Q}\sum_{a\bmod Q}W(a),\qquad
 M_2={1\over Q}\sum_{a\bmod Q}W(a)^2.
\]

Then, uniformly for every interval \({\cal I}\) of \(N\) consecutive
integers,

\[
 \boxed{\sum_{a\in{\cal I}}W(a)=N\mu\{1+o(1)\}.}             \tag{2}
\]

More explicitly, the proof below gives a relative error
\(O(X^{-3/16+o(1)}+X^{-1/4+o(1)})\).  The exponents are not
optimised.

The critical parameters of the round-5 construction satisfy
\(H=(\log X)^{o(1)}\) and \(t=\rho\to1\), so they fall within this theorem.
Thus the passage from a complete CRT period to an interval of length
\(\asymp X\) is no longer the obstruction if one stops the modulus at the
first prefix exceeding that length.

## 2. Size of the first overrun modulus

The prime number theorem gives

\[
 \log\prod_{H<p\le y}p=\vartheta(y)-\vartheta(H).
\]

Since \(H=(\log X)^{o(1)}=o(\log X)\), the first endpoint in (1) satisfies

\[
 z=(1+o(1))\log N\ll\log X.                                \tag{3}
\]

Removing the final prime makes the product at most \(N\).  Consequently

\[
 \boxed{N<Q\le Nz\ll N\log X.}                             \tag{4}
\]

The logarithmic overshoot in (4), rather than the full value of \(Q\), is
what the conductor argument exploits.

## 3. Exact Fourier energy and the conductor random variable

Use the normalisation

\[
 \widehat W(h)={1\over Q}\sum_{a\bmod Q}W(a)e(-ha/Q).
\]

The round-7 CRT factorisation gives

\[
 \sum_{h\bmod Q}|\widehat W(h)|^2=M_2.                     \tag{5}
\]

Under the probability measure

\[
 \mathbb P_2(h)={|\widehat W(h)|^2\over M_2},
\]

the reduced conductor

\[
 C(h)={Q\over\gcd(h,Q)}
\]

is the product of independent local activations.  The activation
probability at \(p\mid Q\) is

\[
 \beta_p=
 {\frac{H(1-t)^2}{p}(1-H/p)
  \over 1-\frac{H(1-t^2)}p}.                               \tag{6}
\]

Because \(p>H\) and \(t\ge1/2\), the denominator in (6) is at least
\(t^2\ge1/4\).  Hence

\[
 \beta_p\le {4H\over p}.                                  \tag{7}
\]

For every fixed \(0<\theta<1\), equations (6)--(7) imply

\[
 \begin{aligned}
 \mathbb E_2 C(h)^\theta
 &=\prod_{p\mid Q}(1-\beta_p+\beta_pp^\theta)\\
 &\le \exp\!\left(\sum_{p\mid Q}\beta_pp^\theta\right)\\
 &\le \exp\{O_\theta(Hz^\theta)\}
  =\exp\{o(\log X)\}.                                    \tag{8}
 \end{aligned}
\]

The deliberately crude last bound sums over all integers up to \(z\); no
prime-density saving is needed.  Markov's inequality therefore yields, for
every fixed \(\eta>0\),

\[
 \boxed{
 \mathbb P_2(C(h)>X^\eta)
 \le X^{-\theta\eta+o(1)}.
 }                                                         \tag{9}
\]

Thus almost all Fourier \(L^2\)-energy lives on conductors much smaller
than \(X\), even though the full CRT modulus is larger than \(X\).

We shall also use

\[
 \boxed{{M_2\over\mu^2}=X^{o(1)}.}                         \tag{10}
\]

Indeed, the exact local variance identity gives

\[
 {1-H(1-t^2)/p\over(1-H(1-t)/p)^2}
 =1+{\frac{H(1-t)^2}{p}(1-H/p)
       \over(1-H(1-t)/p)^2}.
\]

The denominator is at least \(t^2\ge1/4\), and hence the logarithm of
(10) is

\[
 O\!\left(H\sum_{H<p\le z}{1\over p}\right)
 \le O(H\log\log z)=(\log X)^{o(1)}=o(\log X).
\]

## 4. Low conductors: complete periods cancel exactly

For an interval \({\cal I}\), write

\[
 G_N(h)=\sum_{a\in{\cal I}}e(ha/Q).
\]

If \(C(h)=c\), then \(h=(Q/c)u\), where \((u,c)=1\).  The character has
period \(c\).  Complete \(c\)-periods inside \({\cal I}\) cancel; if
\(r=N\bmod c\), finite Parseval on \(\mathbb Z/c\mathbb Z\) gives

\[
 \sum_{u\bmod c}\left|\sum_{v<r}e(uv/c)\right|^2=cr\le c^2. \tag{11}
\]

Let \(D=X^\eta\).  Summing (11) only over primitive \(u\), and then over
the divisors \(c\mid Q\) with \(c\le D\), gives the elementary bound

\[
 \sum_{\substack{h\bmod Q\\C(h)\le D,\ h\ne0}}|G_N(h)|^2
 \le\sum_{c\le D}c^2\le D^3.                             \tag{12}
\]

Cauchy's inequality, (5), and (10) now show that the low-conductor error,
relative to \(N\mu\), is at most

\[
 {M_2^{1/2}D^{3/2}\over N\mu}
 \le X^{-1+3\eta/2+o(1)}.                                \tag{13}
\]

## 5. High conductors: their energy tail beats the modulus overrun

Because \(N<Q\), Parseval for the interval indicator in
\(\mathbb Z/Q\mathbb Z\) is

\[
 \sum_{h\bmod Q}|G_N(h)|^2=QN.                            \tag{14}
\]

Equations (5), (9), (10), (14), and Cauchy's inequality bound the relative
high-conductor error by

\[
 \begin{aligned}
 &\left({M_2\over\mu^2}\right)^{1/2}
  \left({Q\over N}\right)^{1/2}
  \mathbb P_2(C(h)>D)^{1/2}\\
 &\hspace{25mm}\le
 X^{-\theta\eta/2+o(1)},                                \tag{15}
 \end{aligned}
\]

where (4) absorbs the factor \(Q/N\ll\log X\).

Choose, for instance,

\[
 \eta={1\over2},\qquad \theta={3\over4}.
\]

Then (13) is \(X^{-1/4+o(1)}\), while (15) is
\(X^{-3/16+o(1)}\).  Fourier inversion proves (2).

## 6. What this changes, and what it does not

The round-7 raw Cauchy estimate used the full factor
\(\sqrt{Q/N-1}\sqrt{M_2/\mu^2-1}\) and therefore lost the complete-period
saving as soon as \(Q>N\).  That was a genuine barrier to *undifferentiated*
\(L^2\), but not to the Fourier route itself.  The present conductor split
shows that:

* low-conductor characters cancel over their many complete short periods;
* high conductors contain only a polynomially small fraction of Fourier
  energy;
* the first-prime overshoot is only logarithmic, so that small energy tail
  absorbs it.

This is a successful phase/conductor continuation of the old route, rather
than a repetition of the raw \(L^2\) bound.

It still does **not** close #679.  For the round-5 critical choice, the
complete-period Chernoff exponent is

\[
 H L(1-t)^2=(\log X)^{o(1)}=o(\log X).
\]

Consequently \(N\) times the resulting zero-frequency density still tends
to infinity.  Formula (2) faithfully transfers that density, but cannot
turn it into an empty interval.  A successful proof of the first question
still needs a stronger multi-band zero-frequency gain, a structural
argument beyond finite band conditions, or the short-interval high-
\(\omega\) input represented by Lau's Conjecture 8.

## 7. A saddle-point single-band conductor-budget barrier

The preceding failure is not peculiar to the round-5 numerical choice.
There is a general tradeoff inside this single collision-free-band
paradigm.

Let \(t=R/(HL)\) be the usual Chernoff saddle for the aggregate threshold,
and let

\[
 L=\sum_{H<p\le z}{1\over p},\qquad a=1-t.
\]

The zero-mode Chernoff exponent has scale

\[
 E_0=HL\,I(t),\qquad I(t)=1-t+t\log t.
\]

For all \(0<t<1\),

\[
 I(t)\le4(1-t)^2=4a^2.                                \tag{16}
\]

For \(t\ge1/2\) this follows directly from Taylor expansion or convexity;
for \(t<1/2\), use \(I(t)\le1\le4(1-t)^2\).

On the other hand, the logarithmic size of an energy-typical reduced
conductor is governed by

\[
 B_C:=Ha^2\sum_{H<p\le z}{\log p\over p}.             \tag{17}
\]

Suppose one stays in the natural conductor-transfer budget

\[
 B_C\ll\log X.                                        \tag{18}
\]

This includes the regime in which most Fourier energy has conductor at
most a fixed power of \(X\).  Since every selected prime is larger than
\(H\), equations (16)--(18) give

\[
 {E_0\over\log X}
 \ll {B_C\over\log X\,\log H}
 \ll {1\over\log H}
 =o(1).                                               \tag{19}
\]

Therefore a **saddle-point** collision-free band whose energy-bearing
conductors remain within the transferable \(X^{O(1)}\) range cannot produce
the \(\asymp\log X\) zero-mode exponent needed to force an interval empty.
Taking \(z\) much larger increases \(L\), but increases typical conductor
size faster; keeping conductors transferable restores (19).

This is a proved optimisation barrier under the explicit budget (18) and
the saddle relation, not an impossibility result for nonsaddle small tilts,
multiband constructions, cancellation beyond energy concentration, or a
non-Fourier structural argument.  The separate large-band note exploits
exactly the nonsaddle loophole.

## 8. Old-route autopsy

* **Correct but weak:** the round-7 CRT factorisation, Parseval identity,
  Bernoulli conductor ledger, and raw-Cauchy calculation are correct.
* **Proved method barrier:** treating all nonzero frequencies with one raw
  \(L^2\) norm necessarily exposes the full modulus \(Q\) and variance
  inflation.
* **Not a barrier to phase analysis:** the present theorem uses the same
  exact coefficients but preserves reduced conductors and removes that
  loss at the first overrun modulus.
* **Remaining decisive boundary:** even deleting all nonzero frequencies
  leaves a zero mode with exponent \(o(\log X)\).  This is independent of
  the incomplete-period issue.

No assertion of literature novelty or of closure of the original problem
is made.
