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
exist.  This point is **not** yet a counterexample to the distinguished-
component statement: component membership remains open.

## Topology firewall

A coarse path search appeared to connect the anchor to `z`, but exact replay
found the transition segment

```text
(2,-1/2,0,1,1-6t)
```

on which `P=12(6t-1)^2`; it touches `P=0` at `t=1/6`.  A second apparent
detour likewise contained two exact roots missed by sampling.  This is direct
evidence that floating path sampling is unsafe at the narrow component neck.

No claim about `z` belonging to the anchor component is made.  No public
OPG-1757 conclusion changes.
