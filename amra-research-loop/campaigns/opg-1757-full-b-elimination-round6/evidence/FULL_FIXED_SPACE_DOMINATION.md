# Full five-variable fixed-space domination theorem

## Theorem

Let `P(a,b,c,d,e)` and `xi(a,b,c,d,e)` be the exact stabilizer-orbit
polynomials for `K5-34` with marked edge `03`, as reconstructed from the 128
forests and 58 endpoint-connected forests in the verifier.  On the
distinguished Gårding component `C_P`,

```text
xi(a,b,c,d,e) > 0.
```

This proves the complete five-variable stabilizer-fixed marked-host lemma.
It does not restore the three transverse edge directions and therefore does
not prove the eight-variable host theorem, the global moving-edge lemma, or
OPG-1757.

## 1. Component coordinates supplied by derivative nesting

Put

```text
x=a+1,  w=c+1,  y=d+1,  z=e+1.
```

The deletion graph is obtained from `K4` by a parallel extension and a series
subdivision.  Fang--Ma's Theorem 13.13, duality, Proposition 13.12, and the
strictly positive orbit pullback make `P` Gårding.  Theorem 1.1 then nests
`C_P` in every nonzero partial-derivative component.  The exact derivative
factorizations in `GARDING_PRT_COMPONENT_FIREWALL.md` give, throughout
`C_P`,

```text
x,w,y,z>0,
xy>1,  xz>1,  yz>1,
A=partial_b P>0,
L=partial_c A>0.
```

No convexity assertion is used.

Write

```text
P=A b+C,       xi=D b+E,       Delta=A E-D C=2a^2 R.
```

As a polynomial in `w`, write `A=Lw+K` and let `w0=-K/L`.  Since `A>0`,
every component point has `w>w0`.

## 2. The xi slope is positive

Exact expansion gives

```text
partial_w D = 2M,
M=xyz^2+xy-2x-2y-z^2+3,
L=(xy+1)M-(x-1)^2(y-1)^2.
```

Thus `L>0` and `xy>1` imply `M>0`.  At the `A=0` boundary,

```text
L D(w0)=Res_w(A,D)
 =2(x-1)^2(y-1)^2(z-1)^2(z+1)^2(xy-1)>=0.
```

Since `D` has strictly positive `w`-slope and `w>w0`, it follows that

```text
D>0                                             (2.1)
```

on all of `C_P`.

## 3. Quadratic reduction for R

Write

```text
R(w)=r2 w^2+r1 w+r0,
T=xyz-x-y-z+2.
```

The leading coefficient is

```text
r2=(yz+1)T^2>=0.
```

Define `H` and `F` by

```text
disc_w(R)=(x-1)^2(y-1)^4(z-1)^4 H,
L R'(w0)=(x-1)(y-1)^2(z-1)^2 F.
```

The verifier checks their explicit coefficient lists and the master identity

```text
F^2-HL^2
 =8(y+1)^2(z+1)^2(xy-1)(xz-1)(yz+1)T^2.       (3.1)
```

Hence, whenever `H>0`, the conditions `L>0`, `xy>1`, and `xz>1` imply
`F!=0`.

## 4. Exact orientation lemma

We claim

```text
H>0  implies  (x-1)F>=0                         (4.1)
```

under the component inequalities.  The cases `x=1`, `y=1`, or `z=1` are
immediate from the displayed factor in `L R'(w0)`.  Otherwise use `x` as the
fibre variable.  The exact formulas are

```text
L=(y^2z^2-1)x^2-(y^2+z^2-2),

Res_x(L,F)
 =16(y-1)^3(y+1)^3(z-1)^3(z+1)^3
    (yz-1)^2(yz+1)^2.                           (4.2)
```

The positive root `ell(y,z)` of `L` is continuous in each of the connected
parameter chambers below, and (4.2) says `F(ell,y,z)` never vanishes there.
Its sign is fixed by two exact samples:

```text
y=z=2:
  ell=sqrt(2/5),
  F(ell)=36(-35+11sqrt(10))/5 <0
  because 1210<1225;

y=1/2, z=3:
  ell=sqrt(145)/5,
  F(ell)=6(-125+11sqrt(145))/5 >0
  because 17545>15625.
```

There are now only two chamber types.

1. If `y,z>1`, then `ell<1`, while `H` is an upward quadratic in `x` and
   `H(1)=-4(y^2-1)(z^2-1)<0`.  Thus its positive set consists of a possible
   lower interval below `1` and an unbounded upper interval above `1`.
   At the lower admissible boundary, `F<0`: this is the first sample and
   continuity if the boundary is `L=0`; if a pair boundary comes later, the
   exact identities

   ```text
   F(1/y,y,z)=-(y-1)^3(y+1)^2(yz+2y+1)/y^3,
   F(1/z,y,z)=-(z-1)^3(z+1)^2(yz+2z+1)/z^3
   ```

   give the same sign.  On the upper interval `F>0` from its positive leading
   coefficient.  Identity (3.1) prevents a zero of `F` inside either
   `H>0,L>0` interval.  Therefore `(x-1)F>0` on both.

2. If `0<y<1<z` and `yz>1` (or symmetrically with `y,z` exchanged), the pair
   condition forces `x>1/y>1`.  Here `L(1/y)<0`, so the admissible ray starts
   above its positive root `ell`.  The second sample, (4.2), and connectedness
   of `{0<y<1, z>1/y}` give `F(ell)>0`.  Any bounded `H>0` interval starts
   there with positive sign, while the unbounded interval has `F>0` at
   infinity.  Again (3.1) forbids a sign change.  Thus `(x-1)F>0`.

Both `y,z<1` are impossible because `yz>1`.  This proves (4.1).

## 5. Determinant sign

At `w=w0`, exact elimination gives

```text
L^2 R(w0)=Res_w(A,R)
 =2(x-1)^2(y-1)^4(y+1)^2(z-1)^4(z+1)^2
    (xy-1)(xz-1)>=0.                            (5.1)
```

If `H<=0`, then `disc_w(R)<=0`; with `r2>=0`, the quadratic is nonnegative
everywhere.  In the degenerate case `r2=0`, the discriminant forces the
linear coefficient to vanish and (5.1) supplies the same conclusion.

If `H>0`, (4.1) gives `L R'(w0)>=0`.  Since `L>0` and `R` is convex,
`R(w)>=R(w0)>=0` for every `w>w0`.  Hence in all cases

```text
R>=0,  and therefore Delta=2a^2R>=0             (5.2)
```

on `C_P`.

## 6. Return to the b fibre

Let `b0=-C/A`.  Because `A>0`, `P>0` is exactly `b>b0`.  At the boundary,

```text
xi(b0)=Delta/A>=0.
```

Using (2.1), for every component point

```text
xi(b)=xi(b0)+D(b-b0)>0.
```

This proves the theorem.

## Evidence and scope

Reproduce all forest counts, derivative identities, resultants, coefficient
lists, and master identities using only Python's standard library:

```sh
cd amra-research-loop/campaigns/opg-1757-full-b-elimination-round6
ulimit -v 524288
timeout 120s python3 evidence/verify_fixed_space_domination.py
```

Mathematical status: author-verified proof with an exact symbolic verifier
and a named primary-source Gårding dependency.  Independent reconstruction,
transverse lifting, and novelty review are still required.  The original
public problem and global interface remain open.
