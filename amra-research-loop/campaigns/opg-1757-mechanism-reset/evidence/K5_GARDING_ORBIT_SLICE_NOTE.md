# K5 moving-certificate orbit slice

This is a bounded routing probe, not a domination proof.

Fix the marked edge `e=01` of `K5`.  In the nine remaining edges, specialize
the six edges incident with `0` or `1` to `a`, and the three edges among
`{2,3,4}` to `b`.  Exact forest enumeration gives

```
C_{M\e} = a^2 b F(a,b)
xi_e    = 3 a^2 b X(a,b),
```

where

```
F = a^4b^2 + 3a^4b + 3a^4 + 6a^3b^2 + 18a^3b + 18a^3
  + 15a^2b^2 + 39a^2b + 27a^2 + 20ab^2 + 36ab + 12b^2,

X = a^2b^2 + 5a^2b + 9a^2 + 4ab^2 + 12ab + 4b^2.
```

Both residual polynomials are coefficientwise positive.  On the component of
this two-dimensional slice containing `a,b>0`, the factors `a^2 b` prevent a
path from crossing `a=0` or `b=0`; hence `xi_e>0` throughout the positive
quadrant portion of the slice.  On the diagonal,

```
C_{M\e}(t,t) = t^5 (t^4 + 9t^3 + 36t^2 + 77t + 75),
xi_e(t,t)    = 3t^5 (t^2 + 9t + 25),
```

and the distinguished diagonal interval is only `t>0`.

Thus the maximally symmetric K5 slice does not kill the moving-edge route,
but it also does not test the difficult negative-coordinate part of the full
positivity component.  The next probe must break more symmetry (or use W4)
and must certify component membership, not merely sample points where
`C_{M\e}>0`.

Exact data and generator are in `k5_garding_orbit_probe.json` and
`k5_garding_orbit_probe.py`.
