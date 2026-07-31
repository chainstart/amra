# Final report: renewed three-hour theorem campaign

Date: 2026-07-31

Research interval: 17:05:46--20:05:46 HKT.  The interval was used in full;
work after the hard endpoint was restricted to reruns, quantifier repair,
and documentation.  No file in this campaign was committed or pushed during
the renewed interval.

## 1. Strongest result: OPG complete-split programme

The campaign proves the new fixed-deficit layer

\[
B_{2s-11}(s,\beta)=0\quad(s=6),
\qquad
B_{2s-11}(s,\beta)>_{\rm coeff}0\quad(s\ge7).
\]

Its certificate contains 13 offsets, 108 endpoints, and 1,368 exact
endpoint values.  A second implementation uses the previously existing
primitive page-transfer engine and checks exactly 208 values, the sharp
count supplied by the new degree and boundary theorems.  The main and
independent SHA-256 digests are

```text
73245de5eb600ffa7727ce130c362f76c71decc64236112aae496a4974d8c887
da7b0e5430ab29140cbf3847777a5790ce65fea1f3a161daecd35af706c45d25
```

Together with the newly certified \(q=3,4,5\) layers, this closes the seven
deepest complete-split pooled layers \(q=0,\ldots,6\).

The structural advance is more important than one additional layer.  For
all endpoint excesses and component counts, the rooted-hypertree EGF and
binary-edge moment argument prove the two highest Laurent coefficients.
Termwise leading cancellation and endpoint transposition then give

\[
\deg R_{q,r}\le2q+r.
\]

Independently, the factorial-free boundary argument proves

\[
\prod_{j=4}^{\lfloor(q+6)/2\rfloor}(s-j)\mid R_{q,r}(s).
\]

This is a credible paper nucleus for the complete-split pooled model.  It is
not yet arbitrary-\(q\) positivity, all \(B_n\), the full \(\alpha^2\) layer,
or arbitrary-host OPG-1757.

## 2. Erdős #776: a much weaker closing target

A quotient--remainder refinement of the Macaulay entry certificate proves,
uniformly for \(V\ge288\), that a first moving-block entry of residual rank
at most 233 forces the zero-slack target.  The fixed-rank form is

\[
\boxed{D_{248}<H_{248}\Longrightarrow D_{18}<P_{18}.}
\]

The exact certificate checks 230 transitions and all 288 residue classes at
each transition.  At its endpoint

\[
K_3=\frac{903709}{89},\qquad
\lceil288K_3\rceil=2{,}924{,}362<\binom{261}{3},
\]

with margin 4,928.  The same invariant first fails at residual rank 234;
that refutes only this proof route, not the desired inequality.

An independent rank-46 conditional gate was also proved:

\[
D_{46}\le J_{46}+458V+292894
\Longrightarrow
D_{44}\le J_{44}+7V-46.
\]

The all-\(V\) premise \(D_{248}<H_{248}\) remains open, as do
\(R_2(V)\le7V\) and Erdős #776.  The scan through \(V=20{,}000\) and sparse
checks to \(10^6\) found no \(7V\) counterexample, but are recorded only as
finite falsification evidence.

## 3. Erdős #809: false route removed, exact gap isolated

For an opposite zero-shore pair, the campaign proves an exact two-block
missing-energy identity and a quantitative aligned-core theorem.  With
weighted opposite incidence \(\omega(v)\), it also proves

\[
\mathcal R_{\rm opp}
=nE_0^{\rm opp}-\sum_v\omega(v)d(v)
=\sum_v\omega(v)\left(\frac n2-d(v)\right),
\]

and the low-degree-support bound

\[
\mathcal R_{\rm opp}
\le2\varepsilon nE_0^{\rm opp}+\kappa\Omega_\varepsilon.
\]

A full-contract three-clique-chain family shows that failure of the
high/low absorption certificate, even together with failure of
\(R_A+E_0\le S_m\), does not force a little-\(o\) residual moment.  The
family satisfies the density, minimum-degree, exact BCM witness,
\(L_4(2)\), and rainbow-\(C_7\) requirements.  Crucially,
\(D_A=D_B=M_B\), so its exact defect budget closes: it is not a
counterexample to #809.

The remaining meaningful question is now narrower: in a genuinely
exact-budget-hard sequence, prove small weighted low-degree support,
synchronize the same-neighbourhood branch, or construct the required
compatible-edge family directly.  Erdős #809 remains open.

## 4. Verification summary

- Across the root runs, all 70 distinct campaign unit-test cases were
  covered and passed.
- OPG top-two root audit: 84 endpoint rows, 119 rooted/unrooted EGF rows,
  and 496 transpose checks; digest
  `1c2c26adc83e310b6290817416ee8678560222c91c132d43d522d0c31725ac54`.
- OPG \(q=5\) root rerun: both certificate digests reproduced; its six tests
  and the three #809 seventh-stage tests passed together in 356.34 seconds.
- OPG \(q=6\) plus #809 eighth stage: 11 root-level tests passed in
  254.02 seconds.
- The remaining 53 campaign tests passed in a separate 104.60-second smoke
  regression.
- #776 quick symbolic regression and exact scan through \(V=1000\): PASS.
- #809 finite obstruction audit: 780 endpoint pairs, equivalent to 578,760
  deletion checks, and all 36 repeated-colour pairs checked.
- Repository whitespace and control-character checks: PASS at final audit.

## 5. Publication triage

The OPG package is the only result from this window that currently looks
like a self-contained manuscript nucleus: it combines an all-parameter
structural theorem, a general boundary theorem, and seven exact positive
layers with independent certificates.  A high-tier submission claim still
requires an external proof audit, a full database priority search, and a
manuscript that explains why the complete-split pooled model is important.

The #776 and #809 results are useful research advances and could become
sections of future papers, but they remain reductions/conditional structure
around open named problems.  They should not yet be advertised as solutions
or as standalone top-quartile results.
