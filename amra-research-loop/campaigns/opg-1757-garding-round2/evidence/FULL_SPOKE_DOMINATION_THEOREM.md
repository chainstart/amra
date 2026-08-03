# Full four-variable W4 spoke domination

Let `P=C_(W4\01)` and `Q=xi_01` in the four stabilizer variables from G202,
and shift

```text
x=a+1,  y=b+1,  z=c+1,  w=d+1.
```

The Lorentz formula `w(xyz-1)^2-(xz+y-2)^2` belongs to the marked-rim
deletion, not to this spoke deletion.  Applying its successful strategy—an
exact fibre description plus a distinguished-component sign barrier—to the
correct spoke polynomial gives the following identities.

## Exact spoke fibre

Put

```text
A=(wx-1)(wxy+y-2),
H=w^2y+2wx-4w+x^2y-4x-2y+6,
C=2(w^2xy+wx^2-2wx-w+xy-2x-2y+4),
E=-2(w^2y+2wx-4w+x^2+2xy-6x-3y+7),
J=w^2y+2wx+2wy-4w+y-2.
```

Direct expansion gives

```text
P=A z^2-H,                 Q=C z+E,                      (1)
H C^2-A E^2=4(w-1)^2(x-1)^4(y-1)^2 J.                  (2)
```

## The distinguished component

Let `r=wx`.  Consider

```text
D={x,w,z>0, r>1, y(r+1)>2, z>sqrt(H/A)}.                (3)
```

On the base of (3), `A>0`.  Both `J` and `C/2` are affine increasing
functions of `y`.  At the lower base boundary `y=2/(r+1)`, exact reduction
gives

```text
J=2(r-w)^2/(r+1),
C/2=(r-1)(r-w)^2/(w(r+1)),
dJ/dy=(w+1)^2,
d(C/2)/dy=(r(w^2+1)-2w)/w>0.
```

Therefore `C,J>0` in the open base.  Equation (2) yields `H>=0`; equality
would require `(w-1)(x-1)(y-1)=0` and `E=0`.  In these three cases direct
substitution gives respectively `H=A>0`, `H=A>0`, or
`H=(w+x-2)^2>0` because `wx>1`.  Hence `H>0`.

The base is connected: in logarithmic coordinates `log x+log w>0`, and the
`y` fibre is the interval `y>2/(wx+1)`.  The `z` fibre in (3) is also an
interval above the continuous boundary `sqrt(H/A)`.  Thus `D` is connected,
lies in `P>0`, and contains the shifted positive anchor `(2,2,2,2)`.

It is the whole distinguished component.  A path starting in `D` cannot
cross any defining wall while keeping `P>0`:

- at `wx=1`, the preceding side has `y>=1` and
  `H=(x-1)^2(y(x+1)^2-4x)/x^2>=0`, so `P=-H<=0`;
- at `y(wx+1)=2`,
  `H=2(w-1)^2(x-1)^2/(wx+1)>=0`, so again `P<=0`;
- `x=0` or `w=0` cannot be reached before `wx=1`;
- at `z=0`, `P=-H<0`.

Hence no other portion of `{P>0}` can join the anchor component.

## Positivity of the spoke polynomial

For a point of `D`, (1) gives `z>sqrt(H/A)` and `C>0`.  If `E>=0`, then
`Q=Cz+E>0`.  If `E<0`, (2) gives

```text
H C^2 >= A E^2,
```

so

```text
C sqrt(H/A) >= -E.
```

The strict `z` inequality now gives `Q=Cz+E>0`.  Therefore

```text
xi_01>0 on the complete four-variable distinguished component of P.       (4)
```

This proves G202 for the W4 spoke stabilizer specialization.  It does not
prove the moving-edge lemma for arbitrary graphic matroids or OPG-1757.
