# K5-e marked-cross-edge orbit and forest ledger

## Exact group action

The host is `K5-34` and the marked edge is `03`.  Exact enumeration of all
120 vertex permutations leaves two marked-host automorphisms: the identity
and `1<->2`.  The eight deletion edges split as

```text
a={01,02}, b={04}, c={12}, d={13,23}, e={14,24}.
```

Thus the complete stabilizer-fixed activity space has dimension five, with
orbit sizes `2,1,1,2,2`.  Its inclusion in the eight-independent-edge space
has a three-dimensional transverse complement.

## Complete forest polynomials

There are 128 forests in the deletion graph and 58 in which vertices 0 and
3 are already connected.  Complement weighting gives the deletion forest
polynomial `P` and endpoint-connected polynomial `xi`.  Both are affine in
the singleton variables `b,c`:

```text
P  = bc P11 + b P10 + c P01 + P00,
xi = bc X11 + b X10 + c X01 + X00,
```

where

```text
P10 = a*d*e*(a+2)*(d+2)*(e+2),
P01 = (a*d*e+a*d+a*e+d*e)
      *(a*d*e+a*d+a*e+2*a+d*e+2*e),
P00 = a*d*e*(d+2)*(a*e+2*a+2*e),

X11 = 2*(a*d*e^2+2*a*d*e+2*a*d+a*e^2+2*a*e+d*e^2+2*d*e),
X10 = 4*a*d*e*(e+2),
X01 = 2*(a+e)*(a*d*e+a*d+a*e+d*e),
X00 = 4*a*d*e*(a+e).
```

The remaining `P11` coefficient is

```text
a^2*d^2*e^2+2*a^2*d^2*e+a^2*d^2
+2*a^2*d*e^2+4*a^2*d*e+2*a^2*d+a^2*e^2+2*a^2*e
+2*a*d^2*e^2+4*a*d^2*e+2*a*d^2+4*a*d*e^2+8*a*d*e
+4*a*d+2*a*e^2+4*a*e+d^2*e^2+2*d^2*e+2*d*e^2+4*d*e.
```

The exact expanded forms and coefficient multiplicities are preserved in
`k5_cross_orbit_probe.json`.  Their polynomial gcd over `Q` is one.  At the
all-one anchor `(a,b,c,d,e)=(1,1,1,1,1)`, `(P,xi)=(128,58)`.

This ledger is a complete statement only for the five-variable stabilizer
specialization.  It makes no claim in the three transverse directions.
