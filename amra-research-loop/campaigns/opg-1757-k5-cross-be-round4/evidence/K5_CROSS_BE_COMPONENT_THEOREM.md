# K5-e marked-cross-edge `(b,e)` component theorem

Work in the marked-edge-03 stabilizer coordinates for `K5-34`, and set
`a=c=d=1`.  The inherited exact forest enumeration gives

\[
 P=bA(e)+C(e),\qquad \xi/2=bD(e)+E(e),
\]

where

\[
\begin{aligned}
A&=24e^2+48e+9, &C&=24e^2+20e+3,\\
D&=5e^2+10e+2, &E&=5e^2+6e+1.
\end{aligned}
\]

Let `alpha=-1+sqrt(10)/4`.  Then the connected component of `P>0`
containing `(b,e)=(1,1)` is exactly

\[
 U=\{(b,e):e>\alpha,\ b>-C(e)/A(e)\}.
\]

Moreover `xi>0` everywhere on `U`.

## Complete component classification

The two roots of `A` are `-1 plus or minus sqrt(10)/4`.  At the upper root
`alpha`, the whole vertical line has

\[
 P(b,\alpha)=C(\alpha)=22-7\sqrt {10}<0
\]

because `22^2<49*10`.  Consequently no path in `P>0` from the anchor can
cross this line.  Above it, `A>0`, so `P>0` is precisely
`b>-C/A`.  The map

\[
 (e,b)\longmapsto(e,u=b+C(e)/A(e))
\]

is a homeomorphism from this set to `(alpha,infinity) x (0,infinity)`.
It is connected and contains the anchor (`P(1,1)=128>0`), proving the
claimed equality with the complete distinguished component.

## Strict sign certificate

Direct expansion gives

\[
 A(e)\,\xi/2=D(e)P+Q(e),\qquad
 Q=EA-DC=44e^3+94e^2+32e+3.
\]

On `e>alpha`, `A>0`.  The upper root of `D` is
`-1+sqrt(15)/5`, and it is below `alpha`: this is equivalent to
`sqrt(15)/5<sqrt(10)/4`, whose square is `15/25<10/16`.
Thus `D>0` on `U`.

The cubic discriminant is `-9552<0`, so `Q` has exactly one real root.
Its leading coefficient is positive, and

\[
 Q(\alpha)=(-22+7\sqrt {10})/8>0
\]

because `49*10>22^2`.  If its unique real root were at or above `alpha`,
the sign of a positive-leading cubic with one simple real root would make
`Q(alpha)<=0`; hence that root lies below `alpha`, and `Q>0` for all
`e>alpha`.

Finally, throughout `U`, `P,A,D,Q` are strictly positive, and the identity
forces `xi>0`.

## Scope

This is a complete theorem on the natural `a=c=d=1` two-variable slice.
It does not release `a,c,d`, restore the three transverse edge directions,
prove G201, or prove OPG-1757.
