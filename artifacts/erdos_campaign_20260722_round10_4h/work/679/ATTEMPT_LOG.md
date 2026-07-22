# Erdős #679 round-10 phase-tail attempt log

Unified charged window: 2026-07-22 17:10:18--18:10:18 (Asia/Hong_Kong).

Resource rule: symbolic work by default; any finite computation is pinned to
one core with `taskset`/`nice` and single-threaded libraries.

## Frozen starting point

For the fixed window (H=(\log X)^2), (q=\lfloor L_3\rfloor), write

\[
 W^q(n)=\prod_{H<p\le z}(m_p+d_p(n)),
 \qquad d_p=-b(X_p-H/p).
\]

Round 9 transfers the signed ANOVA truncation through

\[
 D=X\exp\{-2\Phi\},\qquad
 \Phi={L_1L_3\over L_2},
\]

with relative error (O(e^{-\Phi})). The remaining task is the signed tail
above (D), retaining the actual interval start, suffix endpoint, and
inherited affine phase. No arbitrary-start uniform suffix estimate is used.

## Claim boundary

No phase recurrence, conditional interface, or finite experiment below is a
closure unless it proves a full one-sided interval bound sufficient for the
original quantifiers.

## Exact phase state and top-band stress test

inherited_phase_state_and_abs_barrier.md derives the exact transformed
suffix sets
\({\cal B}_{p,r,c}=c^{-1}({\cal A}_p-u_r)\), where \(u_r\) runs through the
single inherited block \((A-c,A]\). It then constructs degree
\(d=L_2-2L_3+O(1)\) frontiers in a narrow band below \(z\). Their absolute
frontier mass is only iterated-logarithmic, but division by the retained
suffix mean costs \(X^{qC(1-o(1))}\). Hence any route taking absolute values
separately in the frontier index before using the inherited phase is
strictly excluded.

## Fixed-power additive target

`fixed_power_additive_sufficiency.md` records a quantitative simplification.
For fixed moment \(q\), the Markov threshold loss is only \(X^{o(1)}\), while
the transferred low-conductor sum is \(X^{1-qC+o(1)}\). Therefore, once
\(qC>1\), any bound

\[
 \left|\sum_I {\cal H}_{D,q}\right|\le X^{-\delta}
\]

with fixed \(\delta>0\) would close the relevant interval; no relative
estimate at the complete-period mean is required. The special case
\(q=1,C>1\) already has this sufficiency. For
\(q=\lfloor\eta L_3\rfloor\), the precise threshold price is
\(X^{2\eta C(1+\varepsilon)+o(1)}\).

## Primitive inherited Fourier state

`primitive_phase_target.md` expands each stopping prefix but leaves its
positive suffix intact. The local mean-zero factors force every surviving
frequency \(u\bmod c(T)\) to be primitive, and the exact coefficient is

\[
 \widehat g_T(u)=\gamma_T{(-b)^{|T|}\over c(T)}
 e(-uK/c(T))\prod_{p\mid c(T)}D_H(h_p(u)/p).
\]

On \(I=(A,A+N]\), this couples to the interval through
\(e(u(A-K)/c(T))\) and to the terminal-prime suffix through the twisted sum
\(\sum_{m\le N}e(um/c(T))V_{p_*}(A+m)\). The fixed-power missing theorem is
an \(O(X^{-\delta})\) estimate only after the joint sum over both \(T\) and
primitive \(u\); individual-frontier absolute values are not admissible.

## Kloosterman input audit

`kloosterman_applicability_audit.md` checks Bettin--Chandee, Walker,
Fouvry--Radziwiłł, and Wright (2026) against the exact primitive phase sum.
Their inverse-modulus phases are relevant analogies, but none is a black-box
application: the #679 expansion has conductor level \(X^{1-o(1)}\) despite
prime endpoint \(X^{o(1)}\), a growing collection of shifted linear forms,
a frontier-dependent untruncated suffix, and an additive \(X^{-\delta}\)
target. The literature check therefore produces only a precise conditional
multilinear interface, not the missing theorem.

## Finite identity audit

The exact primitive coefficient and correlation identity were checked with

```text
taskset -c 7 nice -n 10 python artifacts/erdos_campaign_20260722_round10_4h/work/679/verify_primitive_phase.py
```

for \(H=2,q=2,c=5\cdot11\), one skipped prefix prime, one suffix prime, and
an interval longer than the conductor. The maximum coefficient error was
\(4.680\times10^{-17}\), and the direct/Fourier correlation error was
\(2.419\times10^{-15}\). This audits the finite algebra only; it supplies
no asymptotic cancellation.

## Almost-all inherited phases

`almost_all_inherited_phases.md` uses exact ANOVA orthogonality on the full
CRT period. Since a conductor above \(D=Xe^{-2\Phi}\) needs at least
\(L_2-2L_3+O(1)\) active energy primes while
\(\sum_p \mathbb E d_p^2/m_p^2=O_C(q^2/L_2)\), the high-tail energy is at
most

\[
 \mu_q^2\exp\{-(2+o(1))L_2L_3\}.
\]

Averaging the actual length-\(N\) interval correlation over its start
\(A\bmod Q\) then proves that, for fixed \(q,C,\delta\) with
\(qC>1+\delta\), the fraction of starts violating the desired
\(X^{-\delta}\) high-tail bound is at most
\(X^{-2(qC-1-\delta)+o(1)}\). This is an unconditional theorem, but it does
not exclude the particular deterministic dyadic starts; original closure
still needs an exceptional-phase theorem.

## Long exceptional-run consequence of one candidate

`exceptional_phase_run_reduction.md` uses the original quantifier over all
sufficiently large \(k\). With
\(Y=\exp\{L_2\sqrt{L_3}\}=X^{o(1)}\), slide the consecutive \(H\)-shift
block through all \(K\in[Y,2Y]\). Translation gives
\(W_K(n)=W_0(n-K)\), while the threshold price stays \(X^{o(1)}\). Hence a
single hypothetical candidate forces every one of the \(Y+1\) consecutive
starts in \([A-2Y,A-Y]\) to have canonical interval moment at least
\(X^{-o(1)}\). It therefore suffices to exclude such long exceptional
clusters, a strictly more structured target than pointwise uniformity but
one not implied by the complete-period density estimate.

## Uniform anti-clustering counterexample

`uniform_anticlustering_counterexample.md` shows that even the length-\(Y\)
interface cannot be made uniform over the full CRT period. For
\(p>Y+H\), choose a CRT phase whose entire run misses the forbidden block.
For \(H<p\le Y+H\), independent local phase choices and a Chernoff/union
bound give simultaneous load \(O(HL_4)\) at every one of the \(Y\) points.
CRT then produces a run on which every canonical weight is \(X^{-o(1)}\).
This does not place the run near size \(X\); it strictly shows that the
remaining anti-clustering theorem must exploit the actual dyadic start and
cannot be an arbitrary-start black box.

## Freeze

The proof window ended at the prescribed hard boundary
`2026-07-22T18:10:18+08:00`. No mathematical claim was added after that
instant. The workflow is charged exactly 3,600 seconds from the unified
start `17:10:18`; post-boundary actions are limited to terminal metadata,
QA freeze, checksums, and handoff.
