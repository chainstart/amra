# PNL fourth `q` chart: third dyadic annulus certificate

## Claim boundary

This note extends `PNL_A_BOUNDARY_THIRD_NEWTON.md` inside the still-open
below-root `v`-maximal chart.  It certifies the complete full-dimensional
annulus `1/8<=q<=1/4` of the fourth-Newton `q`-maximal chart.  Together with
the earlier three-box certificate for `q>=1/4`, this closes the full region
`q>=1/8` in that chart.

It does not close `q<1/8`, the companion `v`-maximal fourth chart, the PNL
chamber, or OPG-1757.  The machine-readable coverage change remains zero.

## Exact partition

Put `q=(1+t)/8`, `0<=t<=1`, and clear the positive denominator by `8^56`.
The annulus closes with three compact boxes:

| box | remaining parameterization | polynomial terms | nonzero controls | zero controls | control hash |
|---|---|---:|---:|---:|---|
| `y_upper` | `y=(1+s)/2` | 1,548,355 | 6,342,903 | 108,927 | `9defb225132dc7e996438824ee6457fa44ebaf3f3baee3c99b970d5b4689426e` |
| `y_lower_b_lower` | `y=s/2`, `b=u/2` | 1,534,984 | 6,451,830 | 0 | `05f42d9a1ee0b95dc90983356ccee942637232aee36b4189894d0e331ab1d815` |
| `y_lower_b_upper` | `y=s/2`, `b=(1+u)/2` | 1,546,459 | 6,412,728 | 39,102 | `ddf0e712b4b337902975fb26af4c4eb934d9b287e6c5b0ff082080a0c6ca38a3` |

Every stored nonzero control is an exact positive `Fraction`.  The three
boxes contain 19,207,461 strictly positive nonzero controls in total, and
their union is exactly `1/8<=q<=1/4`.

## Reproduction and remaining gap

Run from the campaign directory:

```sh
python3 evidence/verify_pnl_fourth_q_third_annulus.py \
  | diff -u evidence/pnl_fourth_q_third_annulus.json -
```

The verifier reconstructs the deletion-forest polynomial and every upstream
Newton coordinate over exact rationals before checking the three boxes.  The
remaining part of this maximum chart is `0<=q<=1/8`; the full companion
`v`-maximal fourth chart and the other transverse directions also remain
open.
