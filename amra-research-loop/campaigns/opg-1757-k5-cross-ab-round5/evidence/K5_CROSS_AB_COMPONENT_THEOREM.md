# K5-minus-edge cross-edge `(a,b)` component theorem

On the marked-edge-`03` stabilizer slice `c=d=e=1`, put

\[
 P=A(a)b+C(a),\quad A=24a^2+48a+9,\quad C=24a^2+20a+3,
\]
\[
 \xi=2(D(a)b+E(a)),\quad D=14a+3,\quad E=5a^2+6a+1.
\]

Let
\[
 \beta=-1+\frac{\sqrt {10}}4.
\]
Then the complete connected component of `P>0` containing `(1,1)` is

\[
 \mathcal H=\{(a,b):a>\beta,\ b>-C(a)/A(a)\},
\]

and `xi>0` everywhere on `H`.

## Complete component classification

The roots of `A` are `-1-sqrt(10)/4` and `beta`.  Hence `A>0` for
`a>beta`.  At the upper wall,

\[
 P(\beta,b)=C(\beta)=22-7\sqrt {10}<0
\]

for every real `b` (square the positive quantities to check
`sqrt(10)>22/7`).  Thus the entire vertical line `a=beta` is absent from
`P>0`.  Every connected subset of `P>0` containing `(1,1)` therefore lies
in `a>beta`.

Within that half-plane `A>0`, so `P>0` is equivalent to
`b>-C/A`.  This epigraph is connected: `(a,t)` with `a>beta,t>0` maps
homeomorphically to `(a,-C(a)/A(a)+t)`.  It contains `(1,1)` because
`P(1,1)=128`.  It is consequently the whole anchor component.

## Strict sign certificate

Exact expansion gives

\[
 A\frac{\xi}{2}=DP+(EA-DC)
 =DP+a^2(120a^2+48a+5).
\]

The quadratic factor is strictly positive on the real line: its leading
coefficient is positive and its discriminant is `48^2-4*120*5=-96`.
Moreover the only root of `D` is `-3/14`, and
`-3/14<beta` (equivalently `22/7<sqrt(10)`).  Hence on `H`, `A,D,P` are
strictly positive and the remainder is nonnegative.  The displayed
identity yields `xi>0` everywhere on `H`, including `a=0`, where the
strict term is `DP`.

The `b`-resultant is
`Res_b(P,xi)=2a^2(120a^2+48a+5)`.  Its only real zero in the projection is
`a=0`; there `P(0,b)=3(3b+1)` and `xi(0,b)=2(3b+1)`, so the common zero
`b=-1/3` is on the excluded boundary and does not weaken strict interior
positivity.

## Scope

This closes the complete real distinguished-component question on the
specified two-variable slice only.  It does not release `c,d,e`, control
the three transverse directions, or close G201/OPG-1757.
