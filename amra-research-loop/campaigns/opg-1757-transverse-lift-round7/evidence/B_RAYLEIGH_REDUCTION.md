# Full `b=w04` Rayleigh reduction

## Exact reduction

Use the eight original deletion-edge activities

```text
x01,x02,b=x04,c=x12,x13,x14,x23,x24
```

and write

```text
P=A*b+C,  xi_03=D*b+E.
```

A fresh forest enumeration gives term counts

```text
       A   C   D   E   Delta_b=A*E-D*C
terms 81  47  34  24             178
```

where `Delta_b` has total degree 12.  Thus the full eight-variable local
theorem reduces to the sign of a 178-term seven-variable polynomial, rather
than the 7063-term all-base q-resultant.  The two reductions are compatible;
they expose different boundary coordinates.

## 1. The xi b-slope is positive on the whole component

Let `M` be the cycle matroid of `K5` minus edge `34`, with marked edge
`h=03`.  Then

```text
P=C_(M\h),  xi_h=C_(M\h)-C_(M/h).
```

Differentiating in `b=04` gives

```text
A=C_(M\{h,b}),  D=xi_h(M\b).
```

The graph `M\b` is exactly `K4` on vertices `{0,1,2,3}`, together with the
path `1-4-2` parallel to edge `12`: add a parallel copy of `12`, then
subdivide that copy.  Fang--Ma's at-most-six-element theorem, minor closure,
and series/parallel closure therefore make `M\b` C-Gårding.

Apply the proof of Fang--Ma Proposition 13.9 to the fixed edge `h`.  Its two
polynomials are precisely `A` and `D`; the alternative proper-position branch
is excluded by the nonnegative coefficients of `D`.  Hence

```text
D triangleleft A,
```

so `D>0` on the distinguished component of `A`.  The inherited Gårding
derivative nesting for `P` gives

```text
C_P subset C_A,
```

and therefore

```text
A>0 and D>0 throughout C_P.                    (1.1)
```

This is a genuine all-eight-variable sign; it is not inferred from positive
coefficients or a stabilizer restriction.

## 2. Boundary determinant equivalence

For any fixed values of the other seven variables, put `b0=-C/A`.  By (1.1),
the P-positive b-section containing a component point is `b>b0`, and

```text
xi_03(b0)=E-D*C/A=Delta_b/A.
```

Consequently

```text
Delta_b>=0  implies
xi_03(b)=Delta_b/A+D*(b-b0)>0                  (2.1)
```

for every component point.  Conversely, a negative `Delta_b` would make
`xi_03` negative immediately inside the P-boundary.  The remaining local
theorem is therefore exactly the sign problem

```text
Delta_b>=0 on the projection of C_P.           (2.2)
```

The 178 coefficients of `Delta_b` in the original activities are all
strictly positive.  This proves (2.2) in the nonnegative orthant but not on
the full real distinguished component.

## 3. Two-terminal book compression

After deleting `b`, the remaining graph is four parallel routes between
hubs `1` and `2`: the edge `c` and the length-two routes through vertices
`0,3,4`.  Put

```text
q0=x01*x02+x01+x02,
q3=x13*x23+x13+x23,
q4=x14*x24+x14+x24,

p=x01+x02,
r=x13+x23,
s=x01*x13+x02*x23.
```

An exact connected/disconnected state sum compresses the 81- and 34-term
polynomials to

```text
A=q0*q3*q4+c*(q0*q3+q0*q4+q3*q4+q0*q3*q4),

D=c*q4*(p+r+s)+(c+q4)*p*r.                    (3.1)
```

The external C-Gårding argument proves the sign of `D`; (3.1) records the
small state space that a direct algebraic audit can reconstruct.

## 4. Three-terminal partition compression

Delete both marked edges `h=03` and `b=04`, and classify each of the 81
forests by the connectivity partition it induces on terminals `{0,3,4}`.
Write

```text
t = 0|3|4,  x = 03|4,  y = 04|3,  z = 34|0,  u = 034.
```

The five state polynomials have respectively `23,12,12,12,22` terms.  A
fresh graph enumeration, independent of the formulas in (3.1), proves

```text
A   = t+x+y+z+u,       A-D = t+y+z,
C   = t+x+z,           C-E = t.
```

Consequently the entire 178-term obstruction is exactly

```text
Delta_b=(x+z)(y+z)+t(z-u).                    (4.1)
```

Thus the only explicitly subtractive channel is `-t*u`.  Formula (4.1) is
an exact compression, not yet a sign proof: the five state polynomials need
not be termwise positive at real component points.

## 5. Three closed coordinate walls

The verifier checks the exact factorizations

```text
Delta_b|c=0
 =x01^2*x02^2*(x13+x23)*(x14+x24)*q3*q4,

Delta_b|x01=0
 =c^2*x02^2*x13^2*x14^2*(1+x23)*(1+x24),

Delta_b|x02=0
 =c^2*x01^2*x23^2*x24^2*(1+x13)*(1+x14).
```

The edge-floor identities give every `1+xij>0`.  On `c=0`, the three fifth
derivatives proved in `C_ZERO_FIBRE_THEOREM.md` give `q3,q4>0` and
`x13+x23=2d>0`, `x14+x24=2e>0`.  Hence `Delta_b>=0` on all three walls.
Equation (2.1) proves the full b-section domination there.  In particular,
the two strata `a=+/-u`, which are `x02=0` and `x01=0`, are now classified
without also assuming `c=0`.

## Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 524288
timeout 120s python3 evidence/verify_b_rayleigh_reduction.py
```

The verifier uses only Python's standard library, reconstructs all 128/58
forests in the original edge variables, independently partitions the 81
`{03,04}`-deleted forests, verifies both book compressions and (4.1), and
checks the three wall factorizations without calling a symbolic factorizer.

The subsequent `ROUTE_MATRIX_CHAMBER.md` removes the remaining ambiguity in
the phrase “projection of `C_P`”: it proves that this projection is exactly
the positive-edge-floor preimage of

```text
K=diag(R0,R3,R4,Rc) with every off-diagonal entry 1 > 0.
```

It also clears the positive orientation denominators in `Delta_b`, leaving 45
orientation channels of multidegree `(4,2,2)`, and proves that both outer
coefficients of the resulting `h0` quartic are strictly positive on this
matrix chamber.

Mathematical status: author-verified exact reduction with the named Fang--Ma
C-Gårding dependency.  The generic sign of `Delta_b`, independent
reconstruction, and novelty review remain open.  Neither the full local host
theorem nor OPG-1757 is claimed.
