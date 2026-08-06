# PNL fourth `q` chart: fourth dyadic annulus certificate

## Claim boundary

This note extends `PNL_FOURTH_Q_THIRD_ANNULUS.md` inside the still-open
below-root `v`-maximal chart. It certifies the complete full-dimensional
annulus `1/16<=q<=1/8` of the fourth-Newton `q`-maximal chart. Together with
the earlier certificates, this closes the full region `q>=1/16` in that
chart.

It does not close `q<1/16`, the companion `v`-maximal fourth chart, the PNL
chamber, or OPG-1757. The machine-readable chamber coverage change remains
zero.

## Exact partition

Put `q=(1+t)/16`, `0<=t<=1`, and clear the positive denominator by `16^56`.
The annulus closes with the same three compact boxes used on the preceding
dyadic annulus:

| box | remaining parameterization | polynomial terms | nonzero controls | zero controls | control hash |
|---|---|---:|---:|---:|---|
| `y_upper` | `y=(1+s)/2` | 1,548,357 | 6,342,903 | 108,927 | `184943060ebdbd964d97f5b5f74ac01c6f3d3c7af151c2bf19e99c9e9a07c9ae` |
| `y_lower_b_lower` | `y=s/2`, `b=u/2` | 1,534,986 | 6,451,830 | 0 | `2414bc2ae62479d015ff94bbe0c89b1a5427d038bd5bccf694f0e37f415550b8` |
| `y_lower_b_upper` | `y=s/2`, `b=(1+u)/2` | 1,546,458 | 6,412,728 | 39,102 | `5e43dd00134a0cbde9728fdeacb27569f024a2da886ba7ba9d5b71775d9b0e96` |

Every stored nonzero control is an exact positive `Fraction`. The three
boxes contain 19,207,461 strictly positive nonzero controls in total, and
their union is exactly `1/16<=q<=1/8`.

## Reproduction and remaining gap

Run from the campaign directory:

```sh
python3 evidence/verify_pnl_fourth_q_fourth_annulus.py \
  | diff -u evidence/pnl_fourth_q_fourth_annulus.json -
```

The verifier reconstructs the deletion-forest polynomial and every upstream
Newton coordinate over exact rationals before checking the three boxes. The
remaining part of this maximum chart is `0<=q<=1/16`; the full companion
`v`-maximal fourth chart and the other transverse directions also remain
open.
