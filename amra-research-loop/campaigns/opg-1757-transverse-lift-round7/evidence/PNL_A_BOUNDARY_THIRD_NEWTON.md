# PNL above-`A` boundary: third Newton certificate

## Claim boundary

This note resolves a nested accumulation inside the still-open, above-side
`A`-maximal chart of `PNL_A_ROOT_SECOND_NEWTON.md`.  It closes three complete
third-Newton subcharts.  It does not close that second-Newton chart, the PNL
chamber, or OPG-1757, so the machine-readable coverage change remains zero.

`verify_pnl_a_boundary_third_newton.py` reconstructs the entire chain over
exact rationals and emits `pnl_a_boundary_third_newton.json`.

## The exact boundary zero face

The negative Bernstein controls of the above-side `A` chart accumulate only
at its radial boundary `rho=1`.  The exact restriction has 34,738 terms and
hash
`1a281747d0472ad41551d4004f3f73cbfc12ceec3b74fb69e0362b2c31cc6ace`.
It vanishes identically on

\[
 r=1,\qquad \bar H=0,\qquad C=1,\qquad d=0,
\]

with `zeta` and `B` free.  Put `R=1-r` and replace `C` by its deviation from
one.  The transverse ideal `(R,Hbar,C,d)` has order two, and its complete
50-term face factors as

\[
 4B(2B+1)^2(2\zeta+9)^2
 \left[11C+R\bigl((4B+1)\zeta+7B-1\bigr)\right]^2. \tag{1}
\]

Thus the apparent obstruction is another moving square, not a negative
witness.

## Rational root coordinates

Take the `R`-maximal transverse chart.  The square in (1) can have an
admissible root only when

\[
 K=1-7B-(4B+1)\zeta\ge0.
\]

The exact substitution

\[
 B=\frac b7,\qquad
 \zeta=\frac{7(1-b)y}{7+4b}
\]

maps the unit square in `(b,y)` onto this region and gives
`K=(1-b)(1-y)`.  Split the compact ratio `C/R` at `K/11` and let `v` measure
distance from that root on either side.  Positive denominator clearing uses
only powers of `7`, `7+4b`, and `11`.

On both sides the ideal `(R,v)` has order one.  Its common 77-term face is

\[
\begin{aligned}
 28R&(1-b)^2(2b+7)^2(4b+7)(4b+21)(1-y)^2\\
 &\times(7by+4b-7y+7)^2
 (14by-36b-14y-63)^2, \tag{2}
\end{aligned}
\]

which is manifestly nonnegative on the compact parameter square.

## Full compact-subdomain certificates

The following are full Bernstein certificates for the higher-order
polynomials after (2), not merely certificates for the leading face.  Every
stored nonzero control is an exact positive `Fraction`.

| root side | maximal direction | total controls | nonzero | zero | minimum nonzero | control hash |
|---|---|---:|---:|---:|---:|---|
| `0<=C/R<=K/11` | `R` | 339,570 | 328,419 | 11,151 | `48229972252/225` | `da59a931a468698dff2265f1a785524fe4ab86e05beead9b5f9ea4f1f3f63962` |
| `K/11<=C/R<=1` | `R` | 339,570 | 328,517 | 11,053 | `48229972252/225` | `97f465a71f712dba3b7bd99e13558765ff974a24c84db44d5faf27ffadf44ec5` |
| `K/11<=C/R<=1` | `v` | 3,282,510 | 3,214,610 | 67,900 | `1722499009/225` | `a086c26d760c093bff23755a786b1d12df660227177d75ff2addbfddd077286c` |

Together these add 3,871,546 strictly positive nonzero controls to the exact
PNL local certificate stack.

## Remaining gap

The below-root `v`-maximal chart has genuine negative Bernstein controls and
needs further subdivision or another identity.  The region `K<=0`, the
`Hbar`, `C`, and `d` transverse maximum directions, and the rest of the
above-side `A` second-Newton chart also remain open.  No chamber count or
global theorem status changes here.
