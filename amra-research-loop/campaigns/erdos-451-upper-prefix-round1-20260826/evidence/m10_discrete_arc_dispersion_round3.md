# Round-3 discrete arc-dispersion diagnostics

Date: 2026-08-27

Classification: **finite diagnostic only**.  The experiment tests the
decisive arc-dispersion lemma in
`work/m10_round1/discrete_time_fejer_bridge_round3.md`; it does not prove a
uniform `K` or an Erdos 451 bound.

## Reproducible object

The script
`work/m10_round1/discrete_arc_dispersion_scan.py` computes the integer
period `P`, density product, `h`, and minimum arc endpoint exactly.  It then
computes the balanced two-interval Dirichlet weights, their local `L1`
masses, and the centered joint CRT arc mass in double precision.  For a
width-one prime it separately tests the exact reduced system with the
specific dilation by `p_0=k+1`.

```text
script SHA-256:
6b59ad57bb0d230852b01043651e2c0ed655fedba856073c7c2b59d7c77ebcc1

complete minimum-arc batch:
unit openmath-task-20260827-020715-373846.scope
exit 0; maximum RSS 12800 KiB; swaps 0

complete dyadic-profile batch:
unit openmath-task-20260827-020909-374353.scope
exit 0; maximum RSS 13280 KiB; swaps 0
```

An exploratory continuation under
`openmath-task-20260827-020728-373924.scope` completed `k=35,...,39` before
the unfinished `k=40,...,49` tail was stopped; its observed memory peak was
13676544 bytes and swap remained zero.  No incomplete row is used below.

## Minimum arcs

For `C=3`, the completed full-system minimum arcs gave

```text
k   rank   X=ceil(P/h)   effective K
10    4             3      1.07734
16    5            17      0.93811
22    6           518      0.92393
27    7          4261      0.99645
30    7          5190      0.91363
34    8        158492      1.10116
35    8         63109      1.00448
36    9        207452      1.00459
37    9       3782480      1.03984
38    9       1664413      1.02163
39    9        610178      1.09689
```

Here `effective K=(M(X)P/(XL))^(1/m)`, matching the one-sided baseline in
the stated lemma; the centered arc has approximately `2X` points, so even a
perfectly uniform system naturally has `effective K` slightly above one at
small rank.

For the systems with `p_0=k+1`, exact removal followed by the required
dilation gave minimum-arc effective constants

```text
k=10: 0.85174
k=16: 1.06938
k=22: 0.92703
k=30: 0.98534
k=36: 0.98280
```

## Dyadic arcs

The complete second batch checked up to ten doubling scales, capped at two
million frequencies.  The maximum effective constants over all completed
scales were

```text
k       10       16       22       27       30       34
full  1.1952   1.1456   1.2050   1.2279   1.1235   1.1168

width-one reduced/dilated, when present:
k       10       16       22       30
K     1.2603   1.1863   1.3069   1.1509
```

No tested arc contradicts a fixed-exponential estimate.  The largest
observed effective constant is about `1.307`, in the reduced/dilated
`k=22` system.  This is evidence that the lemma is calibrated at a plausible
scale, not evidence that the same bound persists at unbounded rank.
