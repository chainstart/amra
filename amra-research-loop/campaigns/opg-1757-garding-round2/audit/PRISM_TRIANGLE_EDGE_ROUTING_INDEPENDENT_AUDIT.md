# Independent audit: prism triangle-edge stabilizer routing

Date: 2026-08-03

Verdict: **exact algebra passed; two narrative scope repairs required; no
component counterexample**.

## Independent reconstruction

The audit verifier does not import the candidate verifier.  It reconstructs
the triangular-prism graph, enumerates all `6!` vertex permutations, derives
the automorphism group and marked-edge stabilizer, enumerates all 256 subsets
of the eight unmarked edges using the component-count forest criterion, and
builds coefficient dictionaries before invoking symbolic elimination.

The prism automorphism group has order 12.  The setwise stabilizer of `01`
has order 2 and has the following five orbits on unmarked edges:

```text
{25}, {34}, {02,12}, {03,14}, {35,45}.
```

Thus the orbit-size multiset is `{1,1,2,2,2}`, agreeing with the reported
ordered sizes `2,1,2,2,1` up to orbit ordering.

Independent subset enumeration gives exactly 190 forests and 66 forests in
which vertices 0 and 1 are connected.  Coalescing monomials by the five
stabilizer orbits gives 79 terms for `P` and 35 for `xi`.

The audit then identifies orbit types intrinsically: the two size-two
triangle orbits receive `x-1`, the two singleton orbits receive `y-1`, and
the size-two vertical orbit receives `z-1`.  Direct expansion reproduces
both displayed three-variable polynomials coefficient by coefficient.

## Resultant

Exact elimination of `x` reproduces a bivariate resultant of total degree 28
with 166 terms.  Division by

```text
y^2 (y-1)^4 (z-1)^2 (yz+y-2)^2
```

has zero remainder.  The residual has total degree 16 and 52 terms.  Exact
factorization over the rationals returns one degree-16 factor with exponent
one, so the residual is not a polynomial square up to a nonzero constant.

These facts refute the literal **single low-degree resultant-collapse
ansatz**: after removing the displayed boundary factors, a non-square
degree-16 residual remains.  They do **not** by themselves kill every
“simple square-wall routing” mechanism.  A factor controlling the
distinguished component need not equal the full elimination resultant, and
resultants may include branches irrelevant to that component.  Until
“simple square wall” is defined as the literal collapse ansatz, the evidence
sentence “strictly falsifies” and JSON value `killed_on_this_slice` are too
broad.  The audit-approved wording is:

> The single-factor low-degree resultant-collapse ansatz fails on this
> three-variable coarsening; component-level square-wall routing remains
> open.

## Negative point and component scope

At `(x,y,z)=(3/2,1/2,1)`, exact substitution gives

```text
P=1/64,  xi=-3/32.
```

On `z=1`, both polynomials are divisible by `x-1`, and at `y=1/2`,

```text
P=(x-1)(x^3+x^2-15x+17)/4.
```

Moreover `P(2,1/2,1)<0`, verifying the obstruction along that direct
positive-`x` segment.  None of this determines whether the negative point is
in the distinguished component of `{P>0}`.  Accordingly it is not a
component counterexample and cannot be enlarged into a counterexample for a
full prism variable component, G201, G214, or OPG-1757.  The phrase “in other
positivity islands” should be replaced by “at a P-positive point whose
component is undetermined.”

The report's mesh-`1/4` and mesh-`1/8` Bernstein path-absence sentence is not
implemented by the supplied candidate verifier, and the report does not
specify a finite search box or complete adjacency convention.  It is
therefore not independently reproducible from the supplied artifact.  Since
the report already classifies it as finite routing evidence, this gap does
not affect the exact algebra above, but that sentence should not be used as
audited support for component separation.

## Reproduction

From the repository root:

```text
ulimit -v 3145728; timeout 180s python3 \
  amra-research-loop/campaigns/opg-1757-garding-round2/evidence/verify_prism_triangle_edge_routing.py

ulimit -v 3145728; timeout 180s python3 \
  amra-research-loop/campaigns/opg-1757-garding-round2/audit/verify_prism_triangle_edge_routing_independent.py
```

Both commands pass.  The mathematical status is an exact finite
representation plus an exact obstruction to one literal elimination ansatz;
the component theorem remains open.
