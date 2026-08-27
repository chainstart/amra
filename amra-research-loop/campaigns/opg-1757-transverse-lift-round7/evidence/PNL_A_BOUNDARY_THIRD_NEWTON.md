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

The complementary region `K<=0`, where no moving root is possible, is
covered by two compact boxes:

| patch | parameterization | total controls | nonzero | minimum nonzero | control hash |
|---|---|---:|---:|---:|---|
| `B>=1/7` | `B=(1+6b)/7`, `zeta=y` | 127,890 | 125,629 | `279936/7` | `c10c4f9d392e4b3b17b7d35c35e84b33ca2138ef751269dc8e8dccb48409c148` |
| `B<=1/7`, above threshold | `B=b/7`, `zeta=(7(1-b)+11by)/(7+4b)` | 213,150 | 208,747 | `246071287/18` | `5685efd042850a7c7e891f45ca8687b0a7ac4b5be0a508e5a55c0653c6e82f4f` |

All stored controls in both boxes are strictly positive, so the full
`K<=0` part of the transverse `R` chart is closed before introducing the
root split.

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

Together with the two `K<=0` boxes, these add 4,205,922 strictly positive
nonzero controls to the exact
PNL local certificate stack.

## Next face in the open below-`v` chart

The remaining below-root `v`-maximal polynomial has 145,406 terms, radial
degree vector `(28,0,6,0,6,10,29,6)`, and hash
`44e2a18c05eca1e00a198c271c773a91995a6305b8f6c4a9bfbe6059e41028e1`.
At its corner `(q,v)=(0,0)`, where `R=qv`, the fourth Newton order is one.
The complete 122-term face has hash
`97d4008cf2dc069d014f671c365942b1a2fa16918b4072d894bd770e68d61bda`
and factors exactly as

\[
\begin{aligned}
28&(1-b)^2(2b+7)^2(4b+7)(1-y)^2
 (14by-36b-14y-63)^2\\
&\quad\times\left[
 q(4b+21)(7by+4b-7y+7)^2
 +847b(4b+7)v
 \right]. \tag{3}
\end{aligned}
\]

Every factor in (3) is nonnegative for `0<=b,y,q,v<=1`.  Thus this corner
has no negative leading direction, even though the power-basis expansion of
the face has negative coefficients.  This is a leading-face certificate;
it is not a certificate for either complete fourth-Newton chart.

### Complete `b=1` and `y=1` endpoints of the `q`-maximal chart

One full degenerate boundary beyond (3) nevertheless closes exactly.  On
`b=1`, the fourth `q`-maximal polynomial has the common monomial `q^2*v` and,
after putting `z=q^2*v`, its 488-term primitive factors as

\[
\begin{aligned}
1771561&(1-z)(6z+1)(dz+2)^2
 (6\bar H z^3+\bar H z^2+12z+9)\\
&\times(\bar Hdz^3-\bar Hdz^2+2\bar Hz^2-5\bar Hz-9)^2
 Q(z,\bar H,d). \tag{4}
\end{aligned}
\]

The residual `Q` has 71 power-basis terms and degree `(10,3,2)` in
`(z,Hbar,d)`.  Its exact tensor-product Bernstein expansion has 132 controls:
126 are strictly positive, six vanish, the minimum nonzero control is
`6048/5`, and the maximum is `1097599/15`.  The control hash is
`20b19508a53ab9f4a6281626ef3e7a41168707ff68a6cf6244dc5d4f5523f1a5`.
All remaining factors in (4) are nonnegative on the unit cube (the unsquared
cubic is at least nine), so the complete `b=1` endpoint is nonnegative.

The adjacent `y=1` endpoint has the same common monomial and compression.
Writing

\[
 A=b(1-z)+7z,
 \qquad
 B=\bar Hbz^2(1-z)+7\bar Hz^3+2b(1-z)+14z+7,
\]

and

\[
\begin{aligned}
L={}&11\bar Hbdz^3-11\bar Hbdz^2+22\bar Hbz^2-34\bar Hbz\\
   &-21\bar Hz+7bdz-22b-7dz-77,
\end{aligned}
\]

its 4,290-term primitive has the exact form

\[
 121(dz+2)^2 A B L(z,\bar H,b,d)^2 Q_y(z,\bar H,b,d), \tag{5}
\]

Here `A>=0` and `B>=7`.  The 390-term residual `Q_y` has degree
`(11,3,5,2)` in `(z,Hbar,b,d)` and 864 exact Bernstein controls: 834 are
strictly positive, 30 vanish, and none is negative.  Their minimum nonzero
value is `133056/5`, their maximum is `11344725`, and their hash is
`e91fe7e7979e158e38eea0d9e0484f90db591d1facf25d411e126e075023a37a`.
Consequently the complete `y=1` endpoint is also nonnegative.

The opposite radial endpoint `q=1` closes directly, without a further
factorization.  Its five-variable tensor has 113,190 controls: 109,473 are
strictly positive and 3,717 vanish.  The minimum nonzero control is
`48229972252/225`, and the exact control hash is
`3d6a042e5f239678202bbfe9a088d3d41a218234de876b2a875c60640c526d48`.

### Full upper half of the `q`-maximal chart

The endpoint certificate extends to a full-dimensional compact subdomain.
Set `q=(1+t)/2`, `0<=t<=1`, and clear the positive denominator by `2^56`.
The resulting 1,534,976-term polynomial has 6,451,830 tensor-product
Bernstein controls over `(t,y,Hbar,b,v,d)`.  Exactly 6,340,859 controls are
strictly positive, 110,971 vanish, and none is negative.  The minimum nonzero
control is `3475335760995144988855631872/225`; the control hash is
`9cc319051d62babe66bebd99b95ff533d0ab5d3ade457631a12fc551e573b536`.
Therefore the entire `1/2<=q<=1` half of this fourth-Newton chart is closed.

The adjacent annulus `1/4<=q<=1/2` closes after one split at `y=1/2`.
Set `q=(1+t)/4`; on the lower box use `y=s/2`, and on the upper box use
`y=(1+s)/2`.  Positive denominator clearing uses `4^56*2^6` in each box.

| `y` box | polynomial terms | nonzero controls | zero controls | minimum nonzero | control hash |
|---|---:|---:|---:|---:|---|
| `[0,1/2]` | 1,534,972 | 6,412,728 | 39,102 | `1005733952911915343685415854644593778334105600` | `dbfe6b3101071ea3553ea9aaf695b2d15d001e74d7970a36760909c1371f5378` |
| `[1/2,1]` | 1,548,346 | 6,342,903 | 108,927 | `4006789334580504094394060823905169390092419072/225` | `5467d865f0d2447f68b945b35cbf2f047b69f16d7038447a87abb5eadd0b89d1` |

Thus 12,755,631 strictly positive nonzero controls close the complete second
dyadic annulus.  Together with the upper half, the full region `q>=1/4` of the
`q`-maximal fourth chart is certified.

`PNL_FOURTH_Q_THIRD_ANNULUS.md` continues the same construction.  Three
further exact boxes, containing 19,207,461 strictly positive nonzero controls,
close `1/8<=q<=1/4` and extend the certified region to `q>=1/8`.

`PNL_FOURTH_Q_FOURTH_ANNULUS.md` adds three more exact boxes with another
19,207,461 strictly positive nonzero controls. They close `1/16<=q<=1/8`
and extend the certified region to `q>=1/16`.

## Remaining gap

For `K>=0`, the lower region `0<=q<=1/16` of the `q`-maximal fourth chart and
the complete `v`-maximal fourth chart still have genuine negative Bernstein
controls away from the now-closed `b=1` and `y=1` endpoints, so their higher
orders need further subdivision or another identity.  The `Hbar`, `C`, and
`d` transverse maximum directions and the rest of the above-side `A`
second-Newton chart also remain open.  No chamber count or global theorem
status changes here.
