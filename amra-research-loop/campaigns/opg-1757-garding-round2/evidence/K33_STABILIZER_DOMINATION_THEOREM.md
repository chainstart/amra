# K3,3 marked-edge stabilizer domination

Fix a marked edge `03` of `K3,3`.  Its stabilizer has two orbits on the
eight unmarked edges: four edges incident with one marked endpoint have
activity `a`, and the remaining four have activity `b`.  This is the full
two-variable stabilizer specialization, not the full eight-variable edge
space.

Independent forest enumeration gives 194 deletion forests and 60 forests
connecting the marked endpoints.  After `x=a+1,y=b+1`, exact factorization is

`P=(y-1)F`,  `xi=4(y-1)G`,

where

`F=x^4(y^3+y^2+y+1)-4x^2(y+1)-2y+6`,

`G=x^2(y^2+y+2)-2xy-6x-y+5`.

The distinguished component contains `(x,y)=(2,2)`.  Since `P=0` on
`y=1`, every point in this component has `y>1`; since `P>0`, it also has
`F>0`.

Pseudo-division of `F` by `G` in `y` yields the exact remainder

`prem_y(F,G)=-x^4(x-1)^4(y-1)`.

Equivalently there is an exact polynomial quotient `S` with

`x^4 F = S G - x^4(x-1)^4(y-1)`.

If `G=0` and `x!=0`, then

`F=-(x-1)^4(y-1)<=0`,

which contradicts `F>0`.  If `x=0`, then `G=5-y`; its only zero has `y=5`
and `F=-4`, again outside the component.  Thus `G` has no zero on the
distinguished component.  It is positive at the anchor (`G(2,2)=15`), so
by connectedness it is positive throughout.  Therefore `xi>0` there.

This closes the exact marked-edge stabilizer-variable instance for `K3,3`,
which has only one edge orbit.  It does not prove domination when all eight
unmarked activities vary independently, the global moving-edge lemma, or
OPG-1757.
