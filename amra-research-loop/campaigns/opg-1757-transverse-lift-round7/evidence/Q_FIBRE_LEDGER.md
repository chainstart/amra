# Exact all-base q-fibre ledger

## Quadratic reduction

Keep `(a,b,c,d,e,u,v)` arbitrary and regard both polynomials as quadratics in
`q`:

```text
P  = P2 q^2 + P1 q + P0,
xi = X2 q^2 + X1 q + X0.
```

Direct reconstruction of all 128 deletion forests and 58 endpoint-connected
forests gives coefficient term counts

```text
       constant  linear  quadratic
P          104       3         48
xi          25       3         10.
```

The sparse linear coefficients factor completely:

```text
P1 = 2 c u (v^2-d^2-2d),
X1 = 2 c (v(a^2-u^2)-2du).
```

The quadratic coefficients have a common `(b+1)` factor:

```text
P2 = -(b+1) H_P2,
X2 = -2(b+1)(acd+ac+2ad+cd+cuv),
```

where `H_P2` has 24 terms and is recorded by a canonical hash in the machine
ledger.  The sign of `P2` is geometrically natural: it is the negative mixed
edge derivative `-partial_14 partial_24 P`.  This derivative is a nonzero
polynomial and has value `48` at the positive anchor.  The C-Gårding and
derivative-component nesting dependency already checked in round 6 therefore
gives

```text
partial_14 partial_24 P > 0, hence P2 < 0,
```

throughout the open distinguished component.  Thus every nonempty component
`q`-fibre is a single interval between the two real `P` roots; no convexity of
the full Gårding component is being assumed.  The exact identities
`partial_(E\{e})P=1+w_e` also give `b+1>0`, so the displayed `b=-1` factor is
disjoint from the component.

## Common-wall equation

Define

```text
D0 = P2 X0 - X2 P0,
D1 = P2 X1 - X2 P1,
D2 = P1 X0 - X1 P0.
```

The exact quadratic resultant is

```text
Res_q(P,xi) = D0^2 - D1 D2.
```

The verifier checks this identity against the full Sylvester determinant.  The
three compressed polynomials have respectively 264, 118, and 242 terms; their
combination has 7063 terms and total degree 22.  The compact identity exposes
the only locations where a `P` wall and an `xi` wall can exchange order,
without pretending that the sign chambers have already been classified.

## The c=0 wall

On `c=0`, both `P1` and `X1` vanish, so the common-wall resultant is the square
of `D0`.  Exact restriction and factorization give

```text
D0 = 4 d e (a^2-u^2)^2 (b+1) (v^2-d^2-2d).
```

The subsequent independent forest ledger `C_ZERO_FIBRE_THEOREM.md` closes
this entire wall.  Three fifth derivatives give the pair polynomials

```text
x01*x02+x01+x02,  x13*x23+x13+x23,  x14*x24+x14+x24
```

as positive on the component.  Together with the edge floors, they imply
`a,d,e>0` and `d^2+2d-v^2>0`.  Hence the endpoint determinant has the correct
sign, while `X2=-4ad(b+1)<0` makes `xi` strictly concave between the two `P`
roots.  Therefore the complete component `q`-interval is contained in
`xi>0` on `c=0`, including `a=+/-u`.

## Candidate decisive lemma

For every base point in the projection of the distinguished component, the
connected `q`-interval cut out by `P>0` is contained in the `xi>0` interval.
This all-base statement would lift the fixed-space theorem to the full local
eight-variable marked host.  It remains conditional on:

1. sign classification of `D0^2-D1D2` on every projected distinguished
   chamber;
2. correct root order on the resultant-zero contact strata;
3. propagate from the now-closed `c=0` wall across `u=0` and the remaining
   displayed linear-factor walls.

No item is discharged merely by the coefficient ledger.

## Reproduction

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 524288
timeout 120s python3 evidence/verify_q_fibre_ledger.py
```
