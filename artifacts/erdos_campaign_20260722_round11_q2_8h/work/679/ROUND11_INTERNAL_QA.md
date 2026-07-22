# Erdős #679 round-11 adversarial QA

Date: 2026-07-22

Verdict: **PASS_STRICT_REDUCTIONS / ORIGINAL OPEN / Q2 GATE NOT MET**.

The growing-moment conductor cutoff is the strongest new result. The checks
below reconstruct its normalization, signs, and quantifiers. The fixed-
moment Rankin and middle-range statements are checked afterward.

## 1. The growing moment really makes both deletion parameters tend to one

The base weight has local values \(1\) and \(t=1-a\), with

\[
 a={CL_1\over HL}\asymp{1\over L_1L_2}.
\]

For \(q=\lfloor s/a\rfloor\), \(s\to\infty\), \(s=o(L_3)\),

\[
 q\log(1-a)=-qa+O(qa^2)=-s+o(1).
\]

Therefore

\[
 b_1=1-t^q=1-e^{-s+o(1)}\to1,\qquad
 b_2=1-t^{2q}=1-e^{-2s+o(1)}\to1.
\]

The floor in \(q\) changes \(qa\) by at most \(a=o(1)\). There is no
unstated fixed-\(q\) assumption in this calculation.

## 2. Complete-moment asymptotics at the dangerous lower endpoint

It would be false to say uniformly that
\(1-b_iH/p=1-o(1)\) for all \(p>H\) when \(b_i\to1\). The proof avoids
that assertion.

For \(H<p<2H\),

\[
 1-b_iH/p\ge1-H/p\ge(2H)^{-1}.
\]

Chebyshev's prime upper bound gives \(O(H/\log H)\) primes there, so the
absolute logarithmic contribution is \(O(H)=o(HL)\).

For \(p\ge2H\), \(b_iH/p\le1/2\), hence

\[
 \log(1-b_iH/p)=-b_iH/p+O(H^2/p^2).
\]

The total quadratic error is \(O(H)\), even without using prime density,
and the discarded reciprocal mass below \(2H\) is \(O(1/\log H)\). Since
\(b_i=1-o(1)\),

\[
 \log\mu_q=\log M_{2,q}=-(1+o(1))HL.
\]

Also

\[
 HL=(1+o(1))L_1^2L_2,\qquad {HL\over\log X}
 =(1+o(1))L_1L_2.
\]

This validates the conversion
\[
 \exp\{(1-\eta)HL\}
 =X^{(1-\eta+o(1))L_1L_2}.
\]

## 3. Fourier normalization, low-energy deviation, and Farey large sieve

For
\[
 \widehat F_T(u)={1\over c(T)}
 \sum_{x\bmod c(T)}F_T(x)e(-ux/c(T)),
\]
Fourier inversion has no extra factor. Local mean zero implies
\(\widehat F_T(u)=0\) unless \((u,c(T))=1\). Because \(c(T)\) is the
squarefree product of the primes in \(T\), distinct \(T\)'s have distinct
conductors. Equality of two primitive fractions forces equal conductors
and numerators. Thus the coefficient list has no duplicated frequencies.

Parseval and ANOVA orthogonality give

\[
 \sum_T\sum_u|\widehat F_T(u)|^2
 =\sum_T\mathbb E|F_T|^2
 =\mathbb E W^{2q}=M_{2,q}.
\]

This total-energy identity alone gives only the old coefficient \(1/2\).
The improved coefficient \(1\) depends on an additional lower-tail
estimate, checked next.

Write \(x_p=H/p\), \(\sigma_p^2=\mathbb E d_p^2\), and normalize each
ANOVA energy by \(M_{2,q}\). The resulting subset \(T\) has independent
Bernoulli coordinates with

\[
 \theta_p={\sigma_p^2\over m_p^2+\sigma_p^2}
 ={b_1^2x_p(1-x_p)\over1-(2b_1-b_1^2)x_p}.
\]

Indeed the exact normalized mass is
\[
 {1\over M_{2,q}}\mathbb E|F_T|^2
 =\prod_{p\notin T}(1-\theta_p)\prod_{p\in T}\theta_p,
\]
because \(m_p^2+\sigma_p^2=\mathbb E(1-b_1X_p)^2\).
There is no iid assumption. The inequality \(\theta_p\le x_p\) follows
because, after cancelling \(x_p\), the denominator minus the required
numerator is
\[
 1-(2b_1-b_1^2)x_p-b_1^2(1-x_p)
 =(1-b_1)(1+b_1-2b_1x_p)\ge0.
\]
Uniformly for \(p\ge2H\),

\[
 {\theta_p\over x_p}
 ={b_1^2(1-x_p)\over1-x_p+(1-b_1)^2x_p}
 =1+O(1-b_1)=1+o(1),
\]

because \(x_p\le1/2\). The lower endpoint \(H<p<2H\) contributes at most
\(O(H/\log H)=o(HL)\). Thus

\[
 \Lambda:=\sum_p\theta_p=(1+o(1))HL.
\]

For fixed \(\alpha>0\), \(c(T)\le e^{\alpha HL}\) and \(p>H\) imply

\[
 |T|\le r_\alpha={\alpha HL\over\log H}
 =(\alpha/2+o(1))H,
\]

since \(\log H=2L_2+o(1)\) and \(L\sim L_2\). Hence
\(\Lambda/r_\alpha\asymp L_2\) and

\[
 r_\alpha\log(\Lambda/r_\alpha)
 =O_\alpha(HL_3)=o(HL).
\]

For \(0<y<1\), the exact non-iid generating function obeys

\[
 \mathbb Ey^{|T|}
 =\prod_p(1-\theta_p+\theta_py)
 \le e^{-(1-y)\Lambda}.
\]

On \(|T|\le r_\alpha\), \(y^{|T|}\ge y^{r_\alpha}\). Choosing
\(y=r_\alpha/\Lambda\) proves

\[
 \mathbb P(c(T)\le e^{\alpha HL})
 \le\exp\{-\Lambda+r_\alpha+
                 r_\alpha\log(\Lambda/r_\alpha)\}
 =e^{-(1-o(1))HL}.
\]

Multiplication by \(M_{2,q}=e^{-(1+o(1))HL}\) gives the actual coefficient
energy bound

\[
 {\cal V}_{\le e^{\alpha HL}}
 :=\sum_{c(T)\le e^{\alpha HL}}\sum_u^*
       |\widehat F_T(u)|^2
 \le e^{-(2-o(1))HL}.
\]

The exponent \(2\) is not an artefact of including the empty set.
Uniformly for \(p\ge2H\),
\[
 v_p={\mathbb E d_p^2\over m_p^2}
 ={H/p\over1-H/p}(1+o(1)),
\qquad
 \sum_{p\ge2H}v_p=(1+o(1))HL.
\]
All these one-prime conductors lie below \(e^{\alpha HL}\), and their
energy is
\(\mu_q^2\sum_{p\ge2H}v_p=e^{-(2+o(1))HL}\).
Thus the nonconstant low energy itself has logarithmic exponent exactly
\(-2HL\).

Now fix \(0<\eta<1\), then set \(\alpha=1-\eta\), and only then let
\(X\to\infty\). For

\[
 {\cal C}_X=e^{(1-\eta)HL},
\]

reduced Farey fractions are circularly separated by at least
\({\cal C}_X^{-2}\). Primitive support and unique squarefree full
conductors ensure that no frequency or coefficient energy is counted
twice. The large sieve therefore gives

\[
 \sum_{n\in I}|{\cal E}_{\le{\cal C}}(n)|^2
 \le(N-1+{\cal C}_X^2)e^{-(2-o(1))HL}.
\]

After one physical-space Cauchy inequality, its logarithm is at most

\[
 {1\over2}\log N+\log{\cal C}_X
 -(1-o(1))HL
 =-(\eta-o(1))HL.
\]

The large sieve is applied directly on the prescribed physical interval;
no complete CRT-period average over its actual start is used.

The proof is also stable under \(H=\lfloor L_1^d\rfloor\) for any fixed
\(d\ge1\). Indeed \(\log H=dL_2+o(1)\), \(L\sim L_2\), and the only
changed small-deviation parameter is
\(r_\alpha=(\alpha/d+o(1))H\); its entropy correction remains
\(O_d(HL_3)=o(HL)\). Since \(HL\gg L_1\), the large-sieve interval term
and zero mode remain negligible. The candidate coefficient becomes \(d\),
and its moment cost is still \(o(HL)\).

## 4. Candidate threshold and sign direction

For a candidate, the number \(T(n)\) of active prime/shift incidences in
the selected band is at most

\[
 R\le(2+o_\varepsilon(1))(1+\varepsilon)
             {HL_2\over L_3}.
\]

The original admissibility threshold \(K_\varepsilon\) is fixed once
\(\varepsilon\) is fixed. Our block start \(K\asymp H\to\infty\), while
\(K+H=o(X)\); hence for all large \(X\), every shift used here lies in the
original quantified range. No \(X\)-dependent replacement of
\(K_\varepsilon\) is being assumed.

Since \(0<t<1\), \(T(n)\le R\) implies

\[
 W(n)^q=t^{qT(n)}\ge t^{qR}.
\]

The direction is important: a candidate has a **large**, not small, value
of the decreasing Chernoff weight. Moreover

\[
 q\log(1/t)=s+o(1),
\qquad
 \log t^{-qR}=O_\varepsilon(sHL_2/L_3)=o(HL).
\]

If one candidate lies in \(I\), then

\[
 \sum_IW^q\ge t^{qR}.
\]

Writing this exact sum as zero mode plus the low and high signed conductor
aggregates, the zero mode and the absolute low aggregate are
\(\exp(-\Omega_\eta(HL))=o(t^{qR})\), with \(\eta\) fixed before
\(X\to\infty\). Hence

\[
 \sum_I{\cal E}_{>{\cal C}}\ge\tfrac12t^{qR}>0.
\]

Both the sign and the factor \(1/2\) are therefore valid for large \(X\).
The left side is the exact **signed aggregate over all primitive full
conductors \(c(T)>{\cal C}_X\)**; it is not an absolute coefficient sum.
This is a necessary condition for a candidate, not an upper bound on the
tail and not a contradiction.

## 5. Fixed-moment Rankin check

For fixed \(q,C\),

\[
 {\cal F}(Y)\le
 \exp\left\{s_0\log Y+3bH\sum_{p>H}p^{-1-s_0}\right\},
 \qquad s_0=1/\log H.
\]

Chebyshev plus partial summation gives
\(\sum_{p>H}p^{-1-s_0}=O(1)\), while
\(bH=O_{q,C}(L_1/L_2)\). Thus
\({\cal F}(Y)\le z^{K(q,C)}\) for \(Y\le Xz\).
With \(D=Nz^{-B}\), \(B>K+4\), the incomplete-period error is

\[
 D\mu_q{\cal F}(D)\le N\mu_qz^{-4}.
\]

The inequality direction in Rankin's trick is correct because
\(c\le Y\) implies \(1\le(Y/c)^{s_0}\).

## 6. Fixed-moment primitive middle range

For fixed \(q,C\), the normalized variance parameters obey
\(\sum v_p=O(1/L_2)\). Since \(c(T)>Nz^{-B}\) forces
\(|T|\ge L_2-O(1)\), their total variance mass is

\[
 \exp\{-(2+o(1))L_2L_3\}.
\]

The same primitive large-sieve normalization gives, for prescribed fixed
\(A\),

\[
 \left|\sum_I\sum_{D<c(T)\le X^A}F_T\right|
 \le X^{A+1/2-qC+o(1)}
       e^{-(1+o(1))L_2L_3}.
\]

The quantifiers are:

1. prescribe fixed \(A\);
2. choose fixed \(q\) with \(qC>A+1/2+\delta\);
3. let \(X\to\infty\).

It is not one fixed moment controlling all \(A\).

## 7. Recent consecutive-factor and high-dimensional sieve input

For \(Y=\exp(L_2\sqrt{L_3})\), the van Doorn--Tang 2026 endpoint is only
\(\exp(\Theta(L_2^2))\), whereas the actual endpoint is
\(X=\exp(L_1)\). Solving their applicability condition for \(k\) requires
\(\log k\gg\sqrt{L_1L_2}\), at which point the #679 threshold is much too
large. No theorem from that paper is imported beyond its stated range.

Tao--Teräväinen arXiv:2512.01739v2 was checked in the rendered primary
text rather than inferred from an abstract. Its Theorem 1.1 gives the
weaker #248 conclusion \(\Omega(n+k)\le Ck\), while Remark 1.2 states the
exact #679 logarithmic target and assesses it as beyond their method. The
paper's product Selberg-sieve measure treats
\(K=O(\log_2X)\) simultaneous shifts. It asserts no estimate for the
\(H=(\log X)^2\)-shift, ultra-high-conductor signed aggregate at the
self-consistent dyadic start. Importing it as a closure or as the missing
upper bound would therefore be invalid.

The forward-citation audit also checked Lau arXiv:2604.15042v2, dated
2026-06-24. Its Theorem 1.3 is the directly matching minus-shift result
\(\omega(n-k)\le\Omega(n-k)\le C\log k\) for every \(1<k<n\), for
infinitely many \(n\). The paper explicitly records the remaining
\(\log\log k\) factor to #679. Its optimality conjecture and the theorem in
Section 7 implying a negative answer both have unproved conjectural
premises. Therefore it is a strong partial result and heuristic direction,
not a closure and not the missing signed-tail estimate.

The parameter comparison is consistent: our \(H=(\log X)^2\) block is
the \(d=2\) short-interval scale, and the candidate ceiling there is
\((2+o_\varepsilon(1))(1+\varepsilon)L_2/L_3\) per shift. A uniform
short-interval lower bound above this constant would close the negative
direction, but no such unconditional theorem has been imported.

## 8. Energy ceiling and arbitrary-start falsification

The one-prime computation in Section 3 shows that the **nonconstant
cumulative** low energy itself has exact logarithmic exponent \(-2HL\); the empty
component has the same scale. Thus an argument using only low-frequency
pooled energy, the global worst-case Farey separation, and physical
Cauchy cannot improve the displayed calculation. At cutoff
\(e^{\alpha HL}\) its output is

\[
 e^{(\alpha-1+o(1))HL}.
\]

Thus fixed \(\alpha<1\) is the strict useful range of this architecture.

This statement has deliberately limited scope. The one-prime witnesses
have conductors at most \(z\), not near the upper cutoff. They prove that
the cumulative energy exponent is sharp, but do not prove that multiplying
all energy by the largest Farey-spacing loss is sharp. A conductor-layered
energy estimate or structured cancellation inside a layer remains a
legitimate possible continuation.

There is also a direct quantifier test. CRT supplies \(n_0\bmod Q\)
avoiding all local forbidden classes, so \(W(n_0)^q=1\). Put \(n_0\)
inside any interval \(I\) of length \(N\asymp X\). Positivity gives
\(\sum_IW^q\ge1\), whereas the zero mode and the entire low aggregate are
exponentially small uniformly in the start. Therefore

\[
 \sum_I{\cal E}_{>{\cal C}}\ge1-o(1).
\]

So an arbitrary-start interval bound for the high tail is false, not just
unproved. This does not touch the self-consistent target
\(A\asymp X\), because the CRT representative can be of size comparable
to \(Q\gg X^B\) for every fixed \(B\).

This is consistent with the strengthened almost-all statement. For
\(A\) uniform modulo \(Q\),

\[
 \mathbb E_A\sum_{m\le N}W(A+m)^q=N\mu_q,
\]

so Markov gives exceptional-start proportion
\[
 Nt^{-qR}\mu_q=e^{-(1-o(1))HL}.
\]
But \(\log Q\sim z\gg HL\), and one CRT spike creates roughly \(N\)
consecutive exceptional starts. Density and clustering quantifiers
therefore do not contradict each other.

## 9. Status and publication gate

The growing-moment result changes the internal deterministic conductor
boundary from \(X/z^{O(1)}\), and then fixed \(X^A\), to

\[
 X^{(1-\eta+o(1))L_1L_2}.
\]

This is a genuine main-scale improvement **inside the reduction**.
Nevertheless:

* no upper bound for the complementary signed aggregate is proved;
* no original candidate is excluded or constructed;
* no recognized core conjecture is closed;
* the result is presently a structural lemma/reduction, not a standalone
  SCI Q2 theorem.

Therefore **closure count \(=0\)**, **Q2 early-stop \(=\) false**, and
Erdős #679 remains open.

## 10. Boundary freeze

The unified hard boundary was 2026-07-23 00:15:18 HKT (7,200 charged
seconds). No proof or source search was added after it. The existing
finite verifier was rerun once at 00:15:43, pinned to core 7 at low
priority; comparison with verify_growing_moment.out was byte-identical.
The terminal verdict remains unchanged.
