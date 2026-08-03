# W4 rim natural-slice component audit

Put `b=a` and `d=c`, and write the resulting deletion polynomial and
domination polynomial as `P(a,c)` and `Q(a,c)`.  Exact evaluation gives

```text
P(-1,c)=c-3,
Q(-1,c)=-c^2+10c-3.
```

Thus `(a,c)=(-1,10)` is a genuine sign candidate:

```text
P(-1,10)=7>0,        Q(-1,10)=-3<0.
```

It is not in the distinguished component.

## Exact fibre classification

As a cubic in `c`, `P` has leading coefficient `(a+1)^4`, and exact
elimination gives

```text
disc_c(P) = -a^6(a+1)^4(27a^2-32),
Res_c(P,dP/dc) = a^6(a+1)^8(27a^2-32).
```

Hence for

```text
-4sqrt(6)/9 < a < 0,       a != -1,
```

there are three distinct real roots

```text
rho1(a) < rho2(a) < rho3(a).
```

Sturm isolation on the regular fibre `a=-1/2` places one root in each of
`(0,1)`, `(2,3)`, and `(6,7)`.  Since the leading coefficient is positive,
the positive fibres are exactly

```text
(rho1,rho2)  union  (rho3,+infinity).
```

At the left critical value `a=-4sqrt(6)/9`, the two lower roots merge at

```text
c = 152/25 + 72sqrt(6)/25,
```

while exact division shows the remaining root is strictly larger.  Thus the
middle positive interval closes there.  At the right boundary,
`P(0,c)=c^3`, so all three roots collapse at zero; the middle interval again
closes on `P=0`.

The degree-drop fibre `a=-1` does not join the two components.  There
`P=c-3`; the finite interval `c>3` continues the middle branch, whereas the
upper branch escapes to `c=+infinity` as `a` approaches `-1`.  A continuous
path has compact image and cannot use infinity to pass between them.

The point `(-1,10)` therefore lies in the middle positive component.  The
component containing `(1,1)` crosses `a=0` through `c>0` and, immediately on
the negative side, lies above `rho3`.  The intervening root band is `P<0`.

This gives an exact Sturm/resultant proof that the natural-slice negative
`xi` island is disconnected.  It neither proves full four-variable rim
domination nor rules out a different full-variable component counterexample.

