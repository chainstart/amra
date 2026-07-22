# Erdős #679 round 9 attempt log

Time window: 2026-07-22 14:42:16--16:12:16 (Asia/Hong_Kong)
CPU rule: every finite computation is single-threaded.

## Starting target

With the round-8 large-band/small-tilt parameters, write

\[
 W(n)=\prod_{p\in\mathcal P}(m_p+d_p(n))
     =\sum_{S\subseteq\mathcal P}F_S(n),
 \qquad c(S)=\prod_{p\in S}p.
\]

For a fixed \(\kappa<2/3\), all \(c(S)\le X^\kappa\) layers are already
controlled.  The round starts from the unproved sufficient estimate

\[
 \sum_{n\in I}\sum_{c(S)>X^\kappa}F_S(n)
 \le N\mu X^{o(1)}.
\]

No statement below is a closure unless this estimate, or a logically weaker
estimate still sufficient for the original quantifiers, is proved.

## Reproducibility ledger

Commands and outputs are appended only for computations that materially test
a proposed inequality.  Pure symbolic derivations are recorded in the route
notes and REPORT.md.

### Stopping-line identity audit

Command:

```text
taskset -c 1 nice -n 10 python artifacts/erdos_campaign_20260722_round9_6h/work/679/verify_stopping_line.py
```

Parameters: \(H=2\), \(t=0.7\), primes \(3,5,7,11,13\),
\(Q=15015\), cutoffs \(5,20,100,500\), both prime orders, all \(Q\)
residues.  Result: PASS, maximum identity error
\(2.220\times10^{-16}\).  This checks only the algebraic stopping identity;
it is not asymptotic evidence for the missing tail bound.

### Signed low-conductor minimax LP

Command:

```text
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 taskset -c 1 nice -n 10 python artifacts/erdos_campaign_20260722_round9_6h/work/679/minimax_majorant_probe.py
```

Parameters: ten Bernoulli coordinates attached to primes
\(11,13,17,19,23,29,31,37,41,43\), \(H=5\), \(a=0.2\), all 1024 activation
patterns, and six conductor cutoffs.  Result: PASS; the optimum approaches
the exact mean monotonically in the tested cutoffs.  This is a finite
linear-programming probe only.

Two exploratory one-off heredoc commands also tested a symmetric binomial
LP in the basis \(\binom{T}{j}/\binom{M}{j}\), pinned with the same
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 taskset -c 1
nice -n 10` prefix.  Cases with \(aM q\le10\) were numerically stable through
degree six; cases \(aMq=40,100,200\) became ill-conditioned and produced
impossible negative objectives or unbounded statuses.  Per
`minimax_probe_analysis.md`, all unstable outputs are discarded.

### Polynomial-level sieve-denominator audit

`ultrasmall_selberg_level_barrier.md` gives a symbolic, computation-free
bound.  At level \(D=X^\theta\), every supported squarefree modulus has at
most \(J=(\theta+o(1))L_1/(BL_2)\) selected prime factors.  Even granting the
optimistic soft local ratio \(g_q(p)=bH/(p-bH)\), the resulting Selberg
denominator satisfies \(\log G_q(D)=o(qL_1)\), uniformly for every admissible
growing moment.  It is therefore exponentially too small relative to the
complete-period exponent \((qC+o(q))L_1\).  This excludes only conventional
polynomial-level denominator transfer, not signed phase cancellation.

The current arXiv record for the superficially relevant Ramaré preprint
2605.29470 was also checked.  It is withdrawn because of an important
miscalculation and is not used.

### Fixed-exponent parameter refinement

The symbolic audit in fixed_exponent_tilt_refinement.md shows that the
earlier auxiliary hypothesis \(B\to\infty\) is unnecessary. With
\(H=(\log X)^2\), the threshold loss is \(O(L_1/L_3)\), the zero exponent is
\(CL_1\), and the relative variance is \(O(1/L_2)\). The explicit moment
\(q=\lfloor L_3\rfloor\) gives complete-period density
\(X^{-CL_3(1-o(1))}\) while retaining relative nonzero Fourier energy
\(O(L_3^2/L_2)=o(1)\). This remains a complete-period theorem only.

### Quantitative stopping-line conditioning

For the fixed \(H=(\log X)^2\) window and
\(q=\lfloor L_3\rfloor\), stopping_line_conditional_suffix.md proves that
the normalized absolute frontier mass up to \(X^\kappa z\) is
\(\exp\{O(L_1L_3/L_2)\}=X^{o(1)}\). Conditioning on a frontier residue
turns the suffix exactly into another \(H\)-residue weight on an arithmetic
progression of length \(N/c\). The resulting conditional inequality (10)
isolates a uniform suffix-transfer theorem as the sole input. A direct
recursion remains circular and loses the exponent at its terminal scale.

The same local \(L^1\) ledger gives a strict truncated interval theorem.
For \(q=\lfloor L_3\rfloor\), the conductor mass through \(Xz\) has logarithm
at most \((1/2+o_C(1))L_1L_3/L_2\). Hence the explicit moving cutoff
\[
D=X\exp\{-2L_1L_3/L_2\}
\]
transfers with relative error \(O(\exp\{-L_1L_3/L_2\})\). The remaining
full-weight tail is still signed and uncontrolled.

A fully uniform suffix black box was also strictly refuted: CRT supplies an
all-inactive suffix class of weight one, forcing relative factor at least
\((M\mu_{\rm suf})^{-1}\) on an interval chosen to contain it. Any
continuation must retain the inherited start phase rather than take a
supremum over arbitrary interval starts.

### Final verification rerun and status check

Both recorded finite commands were rerun with the same single-core
environment. The stopping identity again returned PASS with maximum error
\(2.220\times10^{-16}\); the minimax LP again returned PASS and the six
reported objective ratios.

The live Erdős Problems #679 page was opened on 2026-07-22 and remained
marked OPEN. It states that no partial or complete solution to the first
question is claimed in the comments.
