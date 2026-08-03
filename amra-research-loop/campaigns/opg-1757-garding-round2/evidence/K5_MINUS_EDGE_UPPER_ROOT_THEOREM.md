# K5-e high-triangle slice: upper-root component theorem

Date: 2026-08-03

Status: **complete proof for the three-variable stabilizer slice; no claim for
the eight independent variables or global G201**

## Statement

Use the notation of `K5_MINUS_EDGE_HIGH_TRIANGLE_STABILIZER.md`.  Thus
`P=bF`, `xi=bG`, and the positive anchor is `(a,b,c)=(1,1,1)`.  On the
connected component of `P>0` containing that anchor,

\[
 b>0\quad\hbox{and}\quad G>0.
\]

Consequently `xi>0` on the complete three-variable stabilizer component.

## 1. Hyperbolic normal form

Put `y=b+1` and `z=c+1`, and define

\[
 L=z(y+1)-2,\qquad M=z(y^2+1)-2,
\]
\[
 A=(y+1)\{z^2(y^2+1)-2\}.
\]

Direct expansion gives

\[
 F=Aa^2+2LMa+(y-1)L^2                                      \tag{1}
\]

and

\[
 F-G=a(y-1)L\{a(L+4)+2L\}.                                 \tag{2}
\]

Moreover

\[
 \operatorname{disc}_a(F)=8(y^2+1)(z-1)^2L^2.              \tag{3}
\]

At the anchor, `y=z=2`, `A>0`, and `a` lies strictly above the upper
root of (1).  More intrinsically, on `A>0,F>0` the two sheets are
distinguished by the strict sign of

\[
 S_F=\partial_aF=2Aa+2LM:
 \quad S_F>0\ \hbox{on the upper sheet},\quad S_F<0\ \hbox{on the lower}.
\]

They cannot interchange without meeting `F=0` (including at a double-root
fibre).  The anchor sheet cannot meet `A=0`: on its positive-`z`
boundary

\[
 z=\sqrt{2/(y^2+1)},\quad y>1,
\]

one has `L<0<M`.  As `A` decreases to zero from above, the upper root of
(1) tends to `+infinity`; a bounded continuous path on the upper sheet
therefore cannot cross this boundary without first meeting `F=0`.
The other `A=0` branch has `z<0` and is separated from the anchor by the
same positive-`z` boundary.  Hence the distinguished component is exactly
contained in

\[
 \mathcal R:\quad y>1,\quad z>\sqrt{2/(y^2+1)},\quad
 a>r_F^+(y,z),                                               \tag{4}
\]

where `r_F^+` is the upper root of `F` in `a`.  Conversely this epigraph is
connected and contains the anchor, so (4) describes the component.

The leading coefficient of `G` on this region is

\[
 2D=2\{(y+1)z^2+y-3\}>0,                                   \tag{5}
\]

because at the lower `z` boundary

\[
 (y+1)\frac{2}{y^2+1}+y-3=\frac{(y-1)^3}{y^2+1}>0.
\]

Thus every fibre of `G` is an upward quadratic.

## 2. Roots cannot be born above the F wall

The exact discriminant is

\[
 \operatorname{disc}_a(G)
 =-8(z-1)L^2N,
 \quad N=y^2z+y^2-4y-3z+5.                                 \tag{6}
\]

All possible double-root loci in `R` are harmless.

* At `z=1`,
  \[
  F=(y-1)\{a(y+1)+y-1\}^2,
  \quad G=(y-1)(2a+y-1)^2.
  \]
  The double root of `G`, `-(y-1)/2`, is strictly below the (double)
  `F` root `-(y-1)/(y+1)`.
* At `L=0`,
  \[
  F=G=2a^2(y-1)^2/(y+1),
  \]
  so the only double root is on the `F=0` wall.
* On `N=0`, positivity of `z` forces `1<y<sqrt(3)` and
  \[
  z=-\frac{y^2-4y+5}{y^2-3}.
  \]
  At the double root of `G`, exact substitution gives
  \[
  F=\frac{(y-1)^5(y^2-7)(y^2+1)^3}
  {4(y^2-3)^2(y^2-2y-1)^2}<0.
  \]
  It therefore lies strictly between the two `F` roots, not in the
  epigraph (4).

Hence a pair of real `G` roots cannot be created inside the upper-root
epigraph.

## 3. Roots cannot cross the upper F wall

The common-root resultant is

\[
 \operatorname{Res}_a(F,G)=L^6H
\]

up to the already positive powers removed in passing from `P,xi`, where

\[
 H=L^2+8(z-1).
\]

At `L=0` the preceding formula shows that the common point is on the
`F=0` wall only.  If `H=0` and `L!=0`, (2) forces the common root

\[
 a_0=-\frac{2L}{L+4}.                                      \tag{7}
\]

Parameterize this wall by `ell=L`.  Then

\[
 z=1-\ell^2/8,
 \quad y=-\frac{\ell^2+8\ell+8}{\ell^2-8},
 \quad y-1=-\frac{2\ell(\ell+4)}{\ell^2-8}.
\]

The conditions `z>0,y>1` force `0<ell<sqrt(8)`.  At (7),

\[
 \partial_aF(a_0)=
 \frac{\ell^3(\ell^2+4\ell+8)}{2(\ell^2-8)}<0.
\]

For an upward quadratic this is the lower, not the upper, root.  Thus no
root of `G` crosses `r_F^+` through the common-root locus.

## 4. Conclusion

On the anchor base fibre `(y,z)=(2,2)`,

\[
 \operatorname{disc}_a(G)=-384<0,
\]

so that fibre contains no real `G` root at any `a` (the single value
`G(1)=70` alone would not establish this).  Equations (5)--(7), together
with continuity of the ordered roots of an upward quadratic over the
connected base region in (4), show that no `G` root can be
born in, or cross into, the connected epigraph (4).  Therefore `G>0`
throughout it.  Since `b>0` on the distinguished component,

\[
 \boxed{\xi=bG>0.}
\]

This closes the full `2,4,2` orbit-equalized K5-e high-triangle slice.  It
does **not** control the five transverse directions of the eight-variable
host and therefore does not promote global G201.
