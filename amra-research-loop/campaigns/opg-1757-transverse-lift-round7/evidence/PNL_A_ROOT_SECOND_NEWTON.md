# PNL negative-root `a`-chart: second Newton certificate

## Claim boundary

This note closes eight complete subcharts inside the `a`-maximal radial chart of
the negative moving-root branch constructed in
`PNL_DOUBLE_CORNER_BLOWUP.md`.  It does not close the full `a`-maximal chart,
the full PNL chamber, or OPG-1757.  The machine-readable coverage change is
therefore zero.

The exact reconstruction and all Bernstein controls are reproduced by
`verify_pnl_a_root_second_newton.py`; its canonical output is
`pnl_a_root_second_newton.json`.

## First radial chart and the accumulation point

In the h-dominant, c-maximal compact chart, write the six nonnegative boundary
deviations as

\[
  (a,\delta_1,H,\delta_2,e,s).
\]

On the negative moving-root branch, the first radial order is seven.  In the
`a`-maximal chart set

\[
  a=r,\qquad
  (\delta_1,H,\delta_2,e,s)
    =r(D_1,\bar H,D_2,E,S),
\]

where all six displayed chart coordinates lie in `[0,1]`.  After removing
`r^7`, the exact polynomial has 59,892 terms and hash
`e33459bb90c297dac3f44fd334293345f96a776d708d77f937be315383490876`.

Adaptive Bernstein discovery does not produce a negative witness.  Its only
persistent queue converges to the exact rational point

\[
 r=\zeta=\bar H=0,\qquad
 D_1=D_2=E=1,\qquad S=\frac23,
\]

where `zeta` is the negative-root interval coordinate.  This location is then
handled exactly; no floating-point sign is used in the certificate.

## Centering and the second Newton fan

Put

\[
 A=1-D_1,\qquad B=1-D_2,\qquad C=1-E.
\]

Split the interval for `S` at `2/3`:

\[
 S=\frac{2(1-d)}3\quad(0\le S\le 2/3),
 \qquad
 S=\frac{2+d}3\quad(2/3\le S\le1),
\]

with `0<=d<=1` on both sides.  Denominator clearing is by the positive
constant `3^6`.  In either centered chart the ideal

\[
 (r,\zeta,A,\bar H,B,C,d)
\]

has exact vanishing order two, and its entire degree-two face is the single
positive square

\[
 352836\,\zeta^2.
\]

Consequently, blow up this seven-variable ideal and split it into its seven
maximum-direction charts.  After removing the common radial square, all seven
compact coordinates again lie in `[0,1]`.

## Exact Bernstein controls

The following counts include implicit zero controls.  Every stored nonzero
control was computed as a Python `Fraction` and is strictly positive.

| side of `S=2/3` | maximal direction | total | nonzero | zero | minimum nonzero | maximum | control hash |
|---|---|---:|---:|---:|---:|---:|---|
| `0<=S<=2/3` | `zeta` | 4,167,450 | 4,114,824 | 52,626 | `729/2444464` | `1843968` | `0ce856b96face2e42a3f430b431caee76f0c14d6bdb772191d54dc4dd3d4ddfe` |
| `0<=S<=2/3` | `r` | 992,250 | 943,110 | 49,140 | `13122/4790071` | `1382976` | `0850b4040dd3320c04c76b350859d94d4bf0a3d5400991507b78cafee0525fd9` |
| `0<=S<=2/3` | `Hbar` | 2,976,750 | 2,857,800 | 118,950 | `81/152779` | `1843968` | `1b446d96360c21e68a43cf1a4b6832d6d44cf23949d266317f8f20ac1b427169` |
| `2/3<=S<=1` | `zeta` | 4,167,450 | 4,154,514 | 12,936 | `2662/12341` | `5467500` | `5fd44a4695d86b6d71ddca050087a153e6d58dc4ee418d69cfacbd9c4415bb38` |
| `2/3<=S<=1` | `r` | 992,250 | 952,560 | 39,690 | `1782/12341` | `4100625` | `48e0c9d4819a446da1246f0e8482409d32ba0493f89c8695fd048c8a96533aa9` |
| `2/3<=S<=1` | `Hbar` | 2,976,750 | 2,885,610 | 91,140 | `616/1763` | `5467500` | `12d42b142c5c793bea0eecfcd86dac4a1781edc04880db8d85848e5bc20d2f50` |
| `2/3<=S<=1` | `B` | 3,472,875 | 3,363,080 | 109,795 | `6561/44935` | `5467500` | `10f4ea92306c02bbb3b6b9af0ddaf75f3ca1708caf5c2870131559244dcf84bc` |
| `2/3<=S<=1` | `d` | 2,976,750 | 2,877,600 | 99,150 | `6561/44935` | `5467500` | `8d0f3f1b1eadcbfcac24456e937b51c31ca84afeadc0bda3772eb80839794654` |

These eight pieces are full compact-subdomain certificates, not merely
nonnegative leading faces.  The lower half closes the `zeta`, `r`, and
`Hbar` maximum directions; the upper half additionally closes the `B` and
`d` directions.

## Remaining gap

Six maximum-direction charts remain: `A`, `B`, `C`, and `d` on the lower
side, and `A` and `C` on the upper side.  Those charts, the rest of the first
`a`-maximal chart, the first-level `ratio1`, `ratio2`, and `e` directions, and
the positive-root branch remain outside this certificate.  No chamber count
or global theorem status changes here.
