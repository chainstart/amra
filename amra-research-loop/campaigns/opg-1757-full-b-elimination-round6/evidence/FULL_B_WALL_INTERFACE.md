# Full-`b` wall interface

Write the fixed-space polynomials as

```text
P  = A b + C,
xi = D b + E.
```

Both `A` and `C` are affine in `c`.  Put `Ac=dA/dc`, and similarly for
`Cc,Dc`.  On the generic sheet `A=0` one has `c=-A0/Ac`, and exact
elimination gives

```text
Ac * C|A=0 = -2 a^2 d^2 e^2 (d+2)^2 (ae+a+e),
Ac * D|A=0 =  2 a^2 d^2 e^2 (e+2)^2 (ad+a+d).
```

Consequently an `A=0` base point is traversable by the open set `P>0`
exactly when `C>0`; on the generic sheet this is a low-degree sign test.
At such a wall `Delta=A E-D C=-D C`, so the direction of the determinant
sign change is controlled by the second displayed factorization.

This is a useful codimension-one interface, not a component theorem.  The
coordinate factors and the exceptional locus `Ac=0` still have to be glued.

## Exact topology firewall

On the rational ray from `(1,1,1,1)` to

```text
(-1983/100, -1973/100, -207/50, -479/25)
```

the interval `0 <= t <= 3/20` contains three simple `A=0` crossings.  Exact
root isolation gives the signs of `C` there as `(-,-,+)`.  A coarse sampler
sees only the third, comfortably positive crossing and falsely suggests a
route out of the anchor chamber.  The first two are narrow but genuine
barriers because at `A=0,C<0` no value of `b` can make `P>0`.

The verifier reconstructs all polynomials from the frozen enumeration and
checks the identities and root signs over `QQ`.  It makes no assertion that
the recorded negative-`xi` point is in the distinguished component.
