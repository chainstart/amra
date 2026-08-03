# Independent audit: K5-e cross-edge `(b,e)` component

## Verdict

The theorem reconstructs from the four displayed polynomials without using
the author verifier.  On `a=c=d=1`, the complete connected component of
`P>0` containing `(b,e)=(1,1)` is exactly

```text
e>alpha,  b>-C(e)/A(e),   alpha=-1+sqrt(10)/4,
```

and `xi>0` throughout it.  The result is confined to this two-variable
slice and does not change OPG-1757 or the public `1/8` target.

## 1. Reconstruction and anchor

Starting only from

```text
A=24e^2+48e+9,   C=24e^2+20e+3,
D=5e^2+10e+2,    E=5e^2+6e+1,
P=bA+C,           xi=2(bD+E),
```

direct substitution gives

```text
P(1,1)=81+47=128,  xi(1,1)=2(17+12)=58.
```

Thus the stated anchor is strictly inside both positive loci.

## 2. The alpha wall and complete component topology

Exact factorization gives

```text
A=24(e-alpha)(e-beta),
alpha=-1+sqrt(10)/4, beta=-1-sqrt(10)/4.
```

At the upper wall,

```text
P(b,alpha)=C(alpha)=22-7sqrt(10)<0,
```

because `22^2=484<490=49*10`.  Hence the entire vertical line
`e=alpha` is absent from `{P>0}`.  A continuous path from the anchor cannot
reach `e<alpha` without meeting that line.

For `e>alpha`, `A>0`, so the complete fibre condition is precisely

```text
b>-C/A.
```

The change of coordinates

```text
(e,b) -> (e,u=b+C/A)
```

is a homeomorphism from this epigraph onto
`(alpha,infinity) x (0,infinity)`.  It is connected and contains the anchor,
where `u=128/81`.  The wall argument gives the reverse containment for the
anchor component.  Therefore this epigraph is the complete distinguished
component, not merely a local chamber.

## 3. Strict xi certificate

Independent expansion gives

```text
A*xi/2 = D*P+Q,
Q=EA-DC=44e^3+94e^2+32e+3.
```

The upper root of `D` is `-1+sqrt(15)/5`.  It is strictly below `alpha`
because `15/25<10/16`; therefore `D>0` whenever `e>alpha`.

The exact cubic discriminant is

```text
disc(Q)=-9552<0,
```

so `Q` has exactly one real, simple root.  Independently, rational root
isolation places that root below `-1/4`, while `alpha>-1/4`.  Also

```text
Q(alpha)=(-22+7sqrt(10))/8>0
```

because `490>484`.  With positive leading coefficient and one real root,
`Q` is therefore positive on every `e>alpha`.

On the distinguished component, `A,D,P,Q` are all strictly positive.  The
identity forces `xi>0`, including arbitrarily close to the open P wall.

## 4. Mechanism and scope audit

The nine killed shortcut mechanisms agree with the exact wall and root
data.  With three retained mechanisms among twelve total, all nine
non-survivors are killed; the configured kill gate is exceeded.  The proved
M410 statement matches exactly the two-variable component theorem.  M411
and M412 remain research routes only: releasing `c` or the other stabilizer
variables can create new walls not controlled here.

No claim is established for the full five-variable stabilizer component,
the three transverse independent-edge directions, G201, or arbitrary finite
graphs.  Consequently there is no public `1/8` improvement and no global
promotion.

The blind checker ran under a 3 GiB virtual-memory limit and 180-second
timeout.  It does not import the author script or JSON.  Lean was not needed.
