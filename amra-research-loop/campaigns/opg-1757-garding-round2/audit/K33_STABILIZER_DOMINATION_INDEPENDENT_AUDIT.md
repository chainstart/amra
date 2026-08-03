# Independent audit: K3,3 marked-edge stabilizer domination

## Verdict

PASS for the complete two-dimensional stabilizer specialization of a marked
edge of `K3,3`.

Blind complement-of-forest enumeration reconstructs 194 deletion forests
and 60 forests connecting the marked endpoints.  It gives exactly the stated
shifted polynomials `P` and `xi`, the pseudo-remainder identity is correct,
and the distinguished-component sign argument handles both the `y=1` wall
and the exceptional line `x=0`.

The conclusion is only

```text
xi_03>0 on the P-positive component containing (x,y)=(2,2)
in the full two-orbit stabilizer specialization.
```

It is not a theorem for eight independently varying unmarked-edge
activities, does not establish G201, does not prove the global moving-edge
lemma, and does not close OPG-1757.  No G201 status was changed.

The verifier was written from the graph and theorem statement.  It imports
neither the author verifier nor its generated result.

## 1. Forest reconstruction

Use the bipartition

```text
{0,1,2} | {3,4,5}
```

and delete the marked edge `03`.  The marked-edge stabilizer has two orbits:

- `04,05,13,23`, labelled `a`;
- `14,15,24,25`, labelled `b`.

For every acyclic subset `I` of these eight edges, add the monomial formed
by the labels of the complementary edges.  Summing over all forests gives
the deletion polynomial.  Restricting to forests in which `0` and `3` are
already connected gives `xi`, because adjoining the marked edge then creates
a cycle.

The independent disjoint-set enumeration obtains:

| selected edges | all forests | endpoint-connected |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 8 | 0 |
| 2 | 28 | 0 |
| 3 | 56 | 4 |
| 4 | 65 | 20 |
| 5 | 36 | 36 |
| total | 194 | 60 |

At `a=b=1` the two complement-monomial sums are therefore exactly 194 and
60.  This independently validates both the forest interpretation and the
anchor values.

## 2. Shifted polynomials

Substitute

```text
x=a+1, y=b+1.
```

Direct expansion and factorization of the reconstructed sums gives

```text
P=(y-1)F,
xi=4(y-1)G,
```

where

```text
F=x^4(y^3+y^2+y+1)-4x^2(y+1)-2y+6,
G=x^2(y^2+y+2)-2xy-6x-y+5.
```

At `(2,2)`, the audit obtains

```text
P=194, xi=60, G=15.
```

Thus the stated anchor lies in `{P>0}` and `G` is positive there.

## 3. Pseudo-remainder

Independent pseudo-division in `y` gives

```text
prem_y(F,G)=-x^4(x-1)^4(y-1).
```

Exact division also reconstructs the quotient

```text
S=x^4(x^2 y+2x+1)
```

and verifies the polynomial identity

```text
x^4 F = S G - x^4(x-1)^4(y-1).
```

No numerical root approximation enters this calculation.

## 4. Distinguished-component logic

Let `C` be the connected component of `{P>0}` containing `(2,2)`.

First, `P(x,1)=0` for every real `x`.  The entire line `y=1` is therefore
absent from `{P>0}` and separates its `y>1` and `y<1` parts.  Since the
anchor has `y=2`, every point of `C` has `y>1`.  On `C`,

```text
P=(y-1)F>0
```

then implies `F>0`.

Suppose `G=0` at a point of `C` with `x!=0`.  The exact quotient identity
forces

```text
F=-(x-1)^4(y-1)<=0,
```

contradicting `F>0`.  Division by `x^4` is not used on the exceptional line
`x=0`: there one computes separately

```text
G(0,y)=5-y.
```

Its sole zero is `y=5`, where `F(0,5)=-4`, again outside `C`.  Hence `G`
has no zero anywhere on `C`.

As a polynomial, `G` is continuous.  Its image on connected `C` cannot
change sign without containing zero; since `G(2,2)=15`, it is positive
throughout `C`.  Together with `y>1`, this gives

```text
xi=4(y-1)G>0
```

on the whole distinguished component.

This argument uses connectedness only after all possible zeros, including
`x=0`, have been excluded.  It does not assume path connectedness or infer a
sign from sampling.

## 5. Scope

The specialization identifies four edges with `a` and four with `b`; it is
the full fixed-edge stabilizer space, which is two-dimensional.  The same
graph nevertheless has eight unmarked edges, and this proof supplies no
control when their activities vary independently.  Edge transitivity of
`K3,3` transfers the same two-variable statement to another choice of marked
edge, but does not remove the stabilizer identifications.

Accordingly the certificate is a correct host-and-specialization theorem,
not G201 or a global graphic-matroid result.

No Lean was used.  Reproduction was bounded by 2 GiB and 120 seconds.

