# Blind audit: full four-variable W4 rim distinguished component

Verdict: **PASS**, for the four-variable rim-orbit specialization only.

## 1. Independent reconstruction

Take the wheel with centre `0`, rim `1,2,3,4`, and marked rim edge `12`.
After deleting `12`, assign activities

```text
a: 01,02    b: 03,04    c: 23,14    d: 34.
```

I independently enumerated every acyclic subset `I` of these seven edges and
formed the complement monomial.  Summing all such monomials reconstructs
`P=C_delete`.  Summing only over forests in which vertices `1` and `2` are
already connected reconstructs `Q=xi`: adjoining the marked edge creates a
cycle exactly for these forests.

There are 82 deletion forests and 30 endpoint-connected forests, so
`P(1,1,1,1)=82` and `Q(1,1,1,1)=30`.  The audit script imports no saved author
polynomial.

## 2. Variable shift and exact identities

The affine substitution

\[
 x=a+1,\quad y=b+1,\quad z=c+1,\quad w=d+1
\]

is globally invertible.  Direct expansion of the independently reconstructed
polynomials gives, with

\[
 T=xyz-1,\quad L=xz+y-2,\quad K=x+yz-2,
\]

the identities

\[
 P=wT^2-L^2,
 \qquad Q=wK^2+Q_0(x,y,z).
\]

No division or sign assumption is used in these identities.

## 3. Distinguished positive component

If `P>0`, then `T` cannot vanish: at `T=0`, `P=-L^2<=0`.  Dividing only after
this observation gives

\[
 w>{L^2\over T^2}\ge0,
\]

so `w>0`, and the sign of `T` is constant on every positivity component.

The anchor `(a,b,c,d)=(1,1,1,1)` becomes `(x,y,z,w)=(2,2,2,2)` and has
`T=7>0`.  On the `T>0` branch, `xyz>1`, hence none of `x,y,z` vanishes and
their sign pattern is constant.  The anchor therefore lies in

\[
 \mathcal D=\left\{x,y,z>0, xyz>1,
 w>{(xz+y-2)^2\over(xyz-1)^2}\right\}.
\]

This set is open and path connected.  Its base is the half-space
`log x+log y+log z>0`; along any base path one may lift above the continuous
boundary function `L^2/T^2`, and each vertical fibre is an interval.  The
preceding sign invariants show that no path in `P>0` can leave `D` while
remaining in the anchor component.  Thus `D` is exactly that component.

The original positive activity orthant lies in the same component: there
`a,b,c,d>0`, the forest sum has strictly positive terms, and the positive
orthant connects to the anchor.  Hence `D` is the distinguished component,
not merely a convenient connected subset.

## 4. Boundary compression and denominators

Let `u=T>0`.  Since `x,y>0`, the substitution

\[
 z={u+1\over xy}
\]

has nonzero positive denominator and is equivalent to `u=xyz-1` on `D`.
At the lower boundary `w_0=L^2/T^2`—which lies in `P=0`, not in the open
component—the independently checked identity is

\[
 T^2Q(w_0)=T^2Q_0+K^2L^2
 ={(x-1)^2(y-1)^2\over x^2y^2}B,
\]

where

\[
 B=2u^3+A(x,y)u^2
 +2u\big((x-1)^2+(y-1)^2\big)
 +(x-1)^2(y-1)^2.
\]

All divisions used here are legitimate: `T`, `x`, and `y` are strictly
positive on `D`.  The boundary value is used only for comparison with the
open fibre; it is not asserted to belong to the positivity component.

## 5. Positivity of A and B

As a quadratic in `x`,

\[
 A=(y+1)^2x^2+(2y^2-4y-2)x+(y^2-2y+5)
\]

has leading coefficient `(y+1)^2>0` and discriminant

\[
 -16(y^3+y+1)<0
\]

for `y>0`.  Therefore `A>0` for every real `x` when `y>0`.  With `u>0`, all
terms in `B` are nonnegative and `2u^3` is strictly positive, so `B>0`.
Consequently the boundary value of `Q` is nonnegative.

## 6. Equality and strict interior positivity

The boundary value can vanish only when `x=1` or `y=1`, because `B>0` and
`x^2y^2>0`.  Moving to an interior point gives exactly

\[
 Q(w)=Q(w_0)+(w-w_0)K^2,qquad w-w_0>0.
\]

In the two possible equality cases, `K` is nonzero:

- if `x=1`, then `K=yz-1=T>0`;
- if `y=1`, then `T=xz-1>0`.  If `K=x+z-2` vanished, positive `x,z`
  with sum two would satisfy `xz<=1`, contradicting `xz>1`.

Thus the increase is strict whenever the boundary value is zero.  When the
boundary value is already positive, nonnegativity of the increase suffices.
Therefore `Q>0` everywhere in the full open component `D`.

## 7. Negative endpoint and scope

The previously sampled negative-`Q` endpoint has `P>0` but
`T=-679/250`, whereas the anchor has `T=7`.  Since `P>0` forbids `T=0`, these
points lie in different positivity components.  It is not a rim counterexample.

The proof establishes only domination for the W4 rim orbit after the stated
four stabilizer-variable identifications.  It does not prove the spoke orbit,
a globally valid moving edge, all graphic matroids, or OPG-1757.  No priority
or novelty conclusion was audited.

The independent checker ran under 2 GiB and a 120-second timeout in 0.6
seconds, without Lean.  SHA-256:
`6afb6f7597495e1aaef67b16c012b8fe2c6e98c18a34818e852849cc89a7c54d`.
