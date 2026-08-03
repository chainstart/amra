# Triangular-prism vertical-edge stabilizer domination

Mark one of the three matching (vertical) edges of the triangular prism.
Its stabilizer has three orbits on the eight remaining edges, of sizes
`2,4,2`; write their activities as `a,b,c` and shift
`x=a+1,y=b+1,z=c+1`.

Exact complement-of-forest enumeration gives 180 deletion forests and 46
forests connecting the marked endpoints.  Put

`T=y^2*z-1`, `V=y^2+z-2`,

`A=y(z+1)-2`, `B=2y+z-3`.

The reconstructed polynomials satisfy

`P=(xT)^2-V^2`,

`xi=2(xA^2-B^2)`,

and the exact barrier identity

`V A^2-T B^2=(y-1)^4(z-1)^2`.                         (1)

At the shifted positive anchor `(2,2,2)`, `xT>|V|`.  On its component of
`P>0`, continuity therefore preserves `xT>|V|`, hence `xT>0`.  Neither `x`
nor `T` can change sign without making `xT=0`; starting from the anchor they
remain positive.  Since `T=y^2z-1>0`, also `z>0` and `y` cannot cross zero,
so `x,y,z>0`.

Conversely, the base `y,z>0`, `T>0` is a half-space in
`(log y,log z)`.  Moreover

`V=y^2+z-2 > 2y*sqrt(z)-2 > 0`.

Thus the region `x>V/T` is a connected epigraph containing the anchor and
is exactly the distinguished component.

On this component `x>V/T`.  Identity (1) gives

`(V/T)A^2-B^2>=0`.

Here `A` cannot vanish: if it did, (1) would force `B=0` and either `y=1`
or `z=1`; then `A=0` forces `y=z=1`, contradicting `T>0`.  The strict
inequality for `x` therefore yields

`xA^2-B^2>0`,

so `xi>0` on the full three-variable marked-vertical-edge stabilizer
component.

This does not treat the prism's six-edge triangle orbit, eight independent
unmarked-edge activities, G201, or OPG-1757.  It is an exact scoped host
certificate pending independent audit.
