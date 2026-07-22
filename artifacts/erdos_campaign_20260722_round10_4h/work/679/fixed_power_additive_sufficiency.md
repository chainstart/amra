# #679: a fixed-power additive estimate is enough

Date: 2026-07-22

This note changes the quantitative target for the unresolved high-conductor
tail. Relative transfer down to the complete-period mean is sufficient but
is much stronger than necessary. A fixed negative power on the *signed
aggregate tail* already closes the relevant dyadic interval.

## 1. Markov reduction with an arbitrary moment

Fix the first-question parameter \(\varepsilon>0\). As in round 9, put

\[
 H=\lfloor(\log X)^2\rfloor,\qquad
 z=\exp(L_1/L_2),\qquad
 L=\sum_{H<p\le z}{1\over p},
\]

\[
 a={C L_1\over HL},\qquad t=1-a,
 \qquad W(n)=\prod_{H<p\le z}\{1-aX_p(n)\},          \tag{1}
\]

where \(C>1\) is fixed. For the block of \(H\) consecutive shifts used in
the construction, let

\[
 r(k)=\left\lceil(1+\varepsilon){\log k\over\log\log k}
      \right\rceil-1,
 \qquad R=\sum_{j<H}r(K+j).
\]

Every candidate in the good event obeys \(W(n)\ge t^R\). Consequently, for
every integer \(q\ge1\),

\[
 \#\{n\in I:n\hbox{ is good}\}
 \le t^{-qR}\sum_{n\in I}W(n)^q.                    \tag{2}
\]

For the fixed quadratic-logarithmic block,

\[
 r(K+j)\le (2+o_\varepsilon(1))(1+\varepsilon)
                 {L_2\over L_3},
\]

and \(L\sim L_2\). Hence, uniformly for \(qa=o(1)\),

\[
 qR\log(1/t)
 \le (2C(1+\varepsilon)+o_\varepsilon(1))
          {qL_1\over L_3}.                           \tag{3}
\]

There are two useful consequences.

* If \(q\) is fixed, then \(t^{-qR}=X^{o(1)}\). Thus an estimate
  \[
       \sum_{n\in I}W(n)^q\le X^{-\delta}             \tag{4}
  \]
  for any fixed \(\delta>0\) makes the integer on the left of (2) zero for
  all sufficiently large \(X\).
* If \(q=\lfloor\eta L_3\rfloor\), with \(\eta>0\) fixed, then
  \[
       t^{-qR}\le X^{2\eta C(1+\varepsilon)+o_\varepsilon(1)}. \tag{5}
  \]
  In that regime (4) still closes the interval whenever
  \(2\eta C(1+\varepsilon)<\delta\).

The fixed-\(q\) version is the quantitatively weaker required input. The
growing moment remains available only if it improves the estimate used to
prove (4).

## 2. The exact additive high-tail target

For \(W^q\), write

\[
 b=1-t^q,\qquad m_p=1-{bH\over p},\qquad
 d_p(n)=-b\{X_p(n)-H/p\}.
\]

Let \({\cal L}_{D,q}\) and \({\cal H}_{D,q}\) be respectively the ANOVA
terms of conductor at most \(D\) and the complementary signed aggregate,
where

\[
 D=X\exp(-2\Phi),\qquad \Phi={L_1L_3\over L_2}.
\]

The round-9 moving-cutoff theorem, whose proof is valid for fixed \(q\) as
well, gives

\[
 \sum_{n\in I}{\cal L}_{D,q}(n)
 =N\mu_q\{1+O(e^{-\Phi})\}.                           \tag{6}
\]

For fixed \(q\), the local mean satisfies

\[
 \mu_q=\prod_p m_p=X^{-qC+o(1)}.                     \tag{7}
\]

It follows that if \(qC>1\) and, for some fixed \(\delta>0\),

\[
 \boxed{
 \left|\sum_{n\in I}{\cal H}_{D,q}(n)\right|
 \le X^{-\delta},                                    \tag{8}
 }
\]

then

\[
 \sum_{n\in I}W(n)^q
 \le X^{-\min(qC-1,\delta)+o(1)}.                    \tag{9}
\]

Combining (2), (3), and (9) closes the interval. In particular, the
minimal formulation may take \(q=1\) and any fixed \(C>1\): one only needs
some fixed-power additive bound for the *joint signed high tail*. It need
not be relative to the much smaller quantity \(N\mu_1\).

For comparison, with \(q=\lfloor\eta L_3\rfloor\), (7) becomes
\(N\mu_q=X^{1-\eta C L_3+o(L_3)}\); then (8) and (5) close the interval
provided \(\delta>2\eta C(1+\varepsilon)\).

## 3. What has and has not changed

This reduction is unconditional once (8) is supplied. It strictly lowers
the missing quantitative target from relative transfer

\[
 \sum_I W^q=N\mu_q X^{o(1)}
\]

to a fixed-power additive estimate on one signed aggregate. It does not
prove (8). The top-band calculation in
`inherited_phase_state_and_abs_barrier.md` shows that (8) cannot be obtained
by taking absolute values separately over crossing frontiers; the inherited
residue/frontier phase must still be used before absolute values.

Strict status: **rigorous sufficient reduction; the fixed-power signed
high-tail estimate and Erdős #679 remain open**.
