# Triangular-prism triangle edge: complete z=1 component

Date: 2026-08-03

Status: **proved for the complete two-variable component inside the
three-variable routing slice; no five-variable or global promotion**

Use the shifted three-variable polynomials in
`PRISM_TRIANGLE_EDGE_STABILIZER_ROUTING.md`.  On `z=1`, exact factorization
gives

\[
 P=(x-1)C(x,y),\qquad \xi=(x-1)D(x,y),
\]

where

\[
C=(x+1)(x^2+1)y^2-4(x+1)y+6-2x
\]

and

\[
D=2(x+1)y^2+(x^3+x^2-x-9)y+10-6x.
\]

At the positive anchor `(x,y)=(2,2)`, `x>1`.  The wall `x=1` is contained
in `P=0`, so its distinguished component stays in `x>1`.  There

\[
\operatorname{disc}_y(C)=8(x-1)^3(x+1)>0
\]

and the coefficient of `y^2` is positive.  Hence the anchor component is
the connected epigraph

\[
x>1,\qquad y>r_C^+(x),
\]

where `r_C^+` is the upper root of `C`.

The polynomial `D` is also an upward quadratic in `y`, and

\[
\operatorname{disc}_y(D)
=(x-1)^3(x^3+5x^2+11x-1)>0\qquad(x>1),
\]

since the second factor equals
`(x-1)(x^2+6x+17)+16`.  Thus its two ordered real roots are distinct and
continuous throughout `x>1`.  They cannot cross either root of `C`, because

\[
\operatorname{Res}_y(C,D)
=-2(x-1)^7(x+1)(x+3)^2\ne0.
\]

At `x=2`, the upper root of `D` is `1/2`, whereas

\[
r_C^+(2)=\frac25+\frac{\sqrt6}{15}>\frac12.
\]

The root order is therefore `r_D^+<r_C^+` throughout `x>1`.  Strict equality
inside the epigraph is impossible by the nonzero resultant.  Thus

\[
y>r_C^+(x)\quad\Longrightarrow\quad D(x,y)>0,
\]

and finally

\[
\boxed{\xi=(x-1)D>0}
\]

on the entire distinguished `z=1` component.

The exact negative point `(3/2,1/2,1)` lies below the lower `C` root:

\[
r_C^-(3/2)=\frac8{13}-\frac{2\sqrt{10}}{65}>\frac12.
\]

It is therefore rigorously firewalled from this component within the
`z=1` plane.  Connectivity through `z!=1`, and the five-variable
stabilizer problem, remain open.
