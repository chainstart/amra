# Full marked-cross-edge `b`-elimination ledger

## Exact identities

For the five stabilizer orbit variables of `K5-34` with marked edge `03`,
both `P` and `xi` are affine in the singleton variable `b`:

```text
P=A b+C,  xi=D b+E.
```

The boundary determinant factors as

```text
Delta=A E-D C=2 a^2 R(a,c,d,e),
```

where `R` has total degree ten, 41 monomials, and all coefficients are
positive integers.  This proves `Delta>=0` only on the nonnegative orthant.
It is not a complete-component proof.

As a quadratic in `c`, `R=r2 c^2+r1 c+r0`, with

```text
r2=(de+d+e+2)(ade+ad+ae+de)^2,
r0=2a^2 d^2 e^2(d+2)(e+2),
```

and the exact `c`-discriminant recorded by the verifier.  These factors expose
the first genuine wall arrangement for the four-variable base.

## Strictly killed broad mechanisms

The complete anchor component is not contained in the nonnegative orthant.
Along

```text
(a,b,c,d,e)=(1-11t/10,1,1,1,1),  0<=t<=1,
```

one has

```text
P=2(726t^2-2255t+1600)/25>0,
```

while the endpoint has `a=-1/10` and `P=142/25`.  Thus coefficient-cone
containment is false.

The exact point

```text
z=(-7/5,-6,-5,-3,-5)
```

satisfies

```text
P(z)=65, xi(z)=-1588/5,
A=9/5, C=379/5, D=198, E=4352/5,
Delta=-336042/25.
```

Thus even the all-positive coefficient sign pattern `A,C,D,E>0` does not
force `Delta>=0`, and no global positive-factor decomposition of `Delta` can
exist.  The new PRT firewall now proves that this point is **outside** the
distinguished component, so it is not a counterexample to the component
statement.

## Topology firewall

A coarse path search appeared to connect the anchor to `z`, but exact replay
found the transition segment

```text
(2,-1/2,0,1,1-6t)
```

on which `P=12(6t-1)^2`; it touches `P=0` at `t=1/6`.  A second apparent
detour likewise contained two exact roots missed by sampling.  This is direct
evidence that floating path sampling is unsafe at the narrow component neck.

## Exact Gårding-component firewall

The deletion graph is `K4` on `{0,1,2,4}` with a parallel copy of edge `12`
subdivided through vertex `3`.  The Fang--Ma six-element base theorem and
series/parallel closure make its cospanning polynomial C-Gårding; orbit
equalization is a strictly positive linear pullback.  Consequently the
fixed-space component passes PRT and is nested in every nonzero derivative
component.

At the point `z` above,

```text
partial_a P(z)=-1240,
P(z+t e_a)=5(270t^2-248t+13),
P(z+(1/2)e_a)=-435/2.
```

Either derivative nesting or PRT therefore excludes `z` from the full
distinguished fixed-space component.  No convexity assumption is used.

The same derivative nesting gives the necessary component inequalities

```text
a,b,c,d,e>-1,
ad+a+d>0,  ae+a+e>0,  de+d+e>0,
A=partial_b P>0.
```

Thus the component itself never crosses `A=0`.  A further exact elimination
identity is

```text
Res_c(A,R)
 =2a^2d^4e^4(d+2)^2(e+2)^2(ad+a+d)(ae+a+e),
```

which is nonnegative on the component and positive outside `ade=0`.  The
subsequent orientation theorem in `FULL_FIXED_SPACE_DOMINATION.md` combines
this boundary value with the exact `w=c+1` discriminant and proves `R>=0`
throughout `A>0`.

See `GARDING_PRT_COMPONENT_FIREWALL.md` and
`FULL_FIXED_SPACE_DOMINATION.md`, with their standard-library verifiers.
Full five-variable fixed-space domination is now proved.  The transverse
eight-variable lift, global interface, and OPG-1757 remain open.
