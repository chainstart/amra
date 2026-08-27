# Round-3 homogeneous weighted-prefix diagnostics

Date: 2026-08-27

Classification: **finite diagnostic only**.  This tests the sufficient
homogeneous weighted-prefix lemma in
`evidence/m10_discrete_spectral_norm_ledger_round3.md`.  It is not a proof
of a uniform factor-two bound.

## Exact scanner

`work/m10_round1/discrete_positive_prefix_scan.cpp` uses GMP integers for
`P`, `D`, the ceiling defining `h`, the one-period check, and every centered
local-support decision.  It accumulates the nonnegative triangular weights
and the final normalized ratio `Q_h L_G/h` in `long double`.

```text
source SHA-256:
715b6eb12fb0a7c134e988808a65d8c2a6a48a1e286fcc391afa8c2112a099a8

guarded compile:
unit openmath-task-20260827-021149-375032.scope
exit 0; maximum RSS 142500 KiB; swaps 0
```

The `C=3` batch ran under
`openmath-task-20260827-021159-375104.scope`.  Rows through `k=35` completed;
the unfinished `k>=36` tail was stopped because its raw prefix exceeded the
useful finite budget.  The observed scope peak was below 3 MiB with zero
swap.  No incomplete row is reported.

The complete `C=2` batch ran under
`openmath-task-20260827-021253-375429.scope` (exit 0, maximum RSS 4160 KiB,
swaps 0).

After the selected rows exposed the need for an unbiased sweep, unit
`openmath-task-20260827-021353-375760.scope` exhaustively tested all 38
systems with `10<=k<=50` and `h<=10^9` at `C=2` (exit 0, maximum RSS
4160 KiB, swaps 0).  A threshold follow-up ran under
`openmath-task-20260827-021413-375974.scope` (exit 0, maximum RSS 4160 KiB,
swaps 0).

Unit `openmath-task-20260827-021505-376384.scope` then exhaustively tested
all 33 systems with `10<=k<=50` and `h<=10^9` at `C=5/2` (exit 0, maximum
RSS 4160 KiB, swaps 0).

## Results

The sufficient finite condition is `Q_h L_G/h<2`.  Every row below uses
the polynomial exponent `B=0`; no conclusion is drawn about the same `C`
after multiplying `h` by `k^B`.

```text
k   rank   C=3 ratio   C=2 ratio
10    4      1.03691     1.14800
16    5      1.01155     1.14054
22    6      1.00294     1.30743
27    7      1.01676     1.48304
30    7      1.00484     1.19210
34    8      1.01480     1.57892
35    8      1.01344     1.35181
```

All rows in the selected table pass, including the samples
`k=10,16,22,30` for which `k+1` is prime.  This is a substantive contrast
with the reconstruction-safe continuous majorant, which is rigorously
forced to have `S>=2` in those cases.  Here the compact dual factor for
`d=1` simply restricts the prefix variable to multiples of `k+1`, matching
the exact fibre elimination.

At `C=3`, these ratios are already within about 1.7 percent of the complete-
period mean value one.  The exhaustive `C=2` sweep, however, found genuine
finite failures of this stronger sufficient majorant:

```text
k=23: ratio 2.14858948768642
k=25: ratio 2.04105841877185
k=26: ratio 2.15064975273248
k=31: ratio 2.16056052782429
```

Thus the `B=0, C=2` specialization is falsified as a uniform finite form of
the factor-two prefix lemma.  This does not kill `C=2` with an allowed
polynomial enlargement `k^B`.  The same rows pass at `B=0, C=5/2`, with
ratios respectively
`1.18303, 1.59945, 1.46561, 1.10027`; all tested threshold rows also pass at
`C=11/4` and `C=3`.  The unbiased `C=5/2` sweep found no failure; its largest
ratio was `1.59945` at `k=25`.  This shows that increasing the fixed window
constant can repair every observed coherent spike, but does not prove that
one fixed constant works at unbounded rank.

These diagnostics motivate the positive-prefix lemma as the narrowest
current survivor while correctly killing its over-strong `C=2` version.

## Location of the `B=0,C=2` spikes

The guarded witness extractor
`work/m10_round1/discrete_positive_prefix_witness.py` ran under
`openmath-task-20260827-022120-378238.scope` (exit 0, maximum RSS
12800 KiB, swaps 0; source SHA-256
`058db8ab42b97a2d53b0857757f80119835d7c9c0dae84bcc34df6b6c585dcc5`).

In three of the four failing systems, the largest nonprincipal contribution
is the universal low prefix `ell=1`, whose centered residue word is
`(1,...,1)`:

```text
k=23: paired triangular contribution 0.75907
k=25: paired triangular contribution 0.48353
k=26: paired triangular contribution 0.39282
k=31: paired triangular contribution 0.67731
```

At `k=26` a larger individual arithmetic resonance occurs at `ell=48546`
with centered word `(0,0,2,2,-1,-5)` and paired contribution `0.36695`, but
the low common-start word is still comparable.  The failures are therefore
not caused solely by the width-one prime or one exotic high-support CRT
lift.  At the critical `B=0,C=2` scale the complete-period expected mass is
only constant-sized, so the unavoidable first few common-start frequencies
can already break a factor-two relative estimate.  A polynomial factor
`k^B` or any fixed `C>2` makes the expected mass grow and can absorb these
fixed-prefix terms; controlling the moving high-prefix resonances remains
the asymptotic problem.
