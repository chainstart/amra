# Full four-variable W4 rim domination

Let `P=C_delete` and `Q=xi` for the W4 rim edge orbit.  Introduce shifted
variables

```text
x=a+1,  y=b+1,  z=c+1,  w=d+1.
```

Direct exact expansion gives the Lorentz identity

```text
P = w(xyz-1)^2-(xz+y-2)^2.                              (1)
```

Put `T=xyz-1` and `L=xz+y-2`.  Equation (1) shows that the component
containing `(x,y,z,w)=(2,2,2,2)` is exactly

```text
x,y,z>0,  T>0,  w>L^2/T^2.                              (2)
```

Indeed, `P>0` forces `w>0` and `T!=0`.  On the `T>0` side the sign pattern
of `x,y,z` cannot change, since `xyz>1`; the all-positive base becomes the
half-space `log x+log y+log z>0` in logarithmic coordinates, and every
`w`-fibre in (2) is an interval.  Hence (2) is connected and is precisely
the distinguished positivity component.

The domination polynomial has the second exact form

```text
Q = w(x+yz-2)^2+Q0(x,y,z).                               (3)
```

Set `K=x+yz-2` and `u=T>0`.  At the lower boundary `w=L^2/T^2`, exact
cancellation gives

```text
T^2 Q0+K^2 L^2 = (x-1)^2(y-1)^2 B/(x^2 y^2),             (4)
```

where, after `z=(u+1)/(xy)`,

```text
B = 2u^3+A(x,y)u^2
    +2u((x-1)^2+(y-1)^2)+(x-1)^2(y-1)^2,

A = x^2y^2+2x^2y+x^2+2xy^2-4xy-2x+y^2-2y+5.
```

As a quadratic in `x`, `A` has positive leading coefficient `(y+1)^2`
and discriminant

```text
-16(y^3+y+1)<0
```

for `y>0`.  Thus `A>0`, then `B>0`, and (4) is nonnegative.  Moving from
the boundary to the strict component increases `Q` by
`(w-L^2/T^2)K^2`.  If the boundary expression vanishes, then `x=1` or
`y=1`.  For `x=1`, `K=yz-1=T>0`; for `y=1`, `K=x+z-2` cannot vanish
when `xz>1`.  Therefore the increase is strict in every equality case.

Consequently

```text
Q>0 throughout the full four-variable distinguished component.          (5)
```

The coarse negative endpoint is also classified exactly.  It has
`T=-679/250`, whereas the positive anchor has `T=7`; since `P>0` forbids
`T=0`, the endpoint lies in a different positivity component.  This
explains the previously detected narrow straight-path failure without any
mesh or path guess.

Result (5) proves the W4 rim-orbit instance only.  It does not prove the
spoke orbit, the global moving-edge quantifier, or OPG-1757.

