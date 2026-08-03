# General m-row formal unit-matrix theorem and actual-block firewall

## Formal theorem

Let `m>=1`, let the integer variables be

```text
(g,f,b,r_1,...,r_m,q_1,...,q_m),
```

and fix integers `s_i` and a scalar exponent `a`.  Impose

```text
g+r_i=s_i a                 (1<=i<=m),
f=2a,
f+q_i=-s_i a               (1<=i<=m),
g+b=-2a,
b-r_i-q_i=0                (1<=i<=m).
```

The full `(3m+2) x (2m+3)` coefficient matrix has rank `2m+2` over
`Q`.  Its integer kernel is the primitive line

```text
Z*(1,0,-1,-1,...,-1,0,...,0).
```

All nonzero Smith invariants equal one.  If the complement rows `f+q_i`
and `g+b` are deleted, leaving the source and identity subsystem, its rank
is `2m+1` and its integer kernel is

```text
Z*(1,0,-1,-1_i,0_i) direct-sum Z*(0,0,1,0_i,1_i).
```

The second generator is the common absolute-spectrum shift.

## Proof

For the full matrix, select the `m` source rows, the row `f`, the `m`
complement rows and the row `g+b`; delete the `g` column.  On columns

```text
(f,b,r_1,...,r_m,q_1,...,q_m)
```

elementary row subtraction makes the square matrix triangular with diagonal
entries `+/-1`.  Its determinant is `+/-1`.  Hence the rank is at least
`2m+2`.  The displayed nonzero gauge vector is annihilated by every row, so
the rank is exactly `2m+2`.  The unit maximal minor also makes the product
of the nonzero Smith invariants one; each invariant is positive and divides
the next, so all are one.  The rational kernel is one-dimensional and
contains a primitive integer vector, proving the integer-kernel statement.

For the source-identity subsystem, use all its `2m+1` rows and delete the
`g,b` columns.  On columns `(f,r_i,q_i)` the determinant is again `+/-1`.
Both displayed vectors lie in the kernel, so rank, Smith and kernel follow.

Substitution gives the same result directly.  In the full system,

```text
f=2a, q_i=-(s_i+2)a, b=-2a-g, r_i=s_i a-g,
```

and every identity row then vanishes.  Choosing `g=a` gives one particular
solution

```text
(a,2a,-3a,(s_i-1)a,-(s_i+2)a),
```

plus the gauge line.  Without complement rows, `g` and `b` are free and
`q_i=b+g-s_i a`, giving gauge plus spectrum shift.

The bounded Python guard verifies exact ranks, both explicit unit minors,
kernels and affine substitution for every `1<=m<=32`.  The proof for all m
is the unit-minor argument, not finite extrapolation.

## Mechanism falsification

The theorem proves `M1083U6-01` as a formal lemma.  It strictly refutes:

- `M1083U6-02`: a unit maximal minor leaves no Smith torsion;
- `M1083U6-03`: identity rows are consequences, not m extra ranks;
- `M1083U6-04`: every added row still annihilates the same gauge vector;
- `M1083U6-05`: the source-identity subsystem has the independent spectrum
  shift and rank `2m+1`, not `2m+2`;
- `M1083U6-07`: scalar primitivity alone says nothing about unrecorded
  coefficient units or extra ambient unit coordinates;
- `M1083U6-08`: the fixed-X shifts zero and `1/4` have different absolute
  label sets but both exactly 127 distinct target-target labels;
- `M1083U6-09`: source-identity data leave an arbitrary common spectrum
  shift, so the formal theorem does not make absolute-spectrum conditioning
  entropy-free.

`M1083U6-06` and `M1083U6-10` survive only as unproved actual-block and
all-target theorems.

## Actual-block audit

The archive does prove the formal simultaneous identities

```text
F_i=G R_i, P_A0=G B, B=R_i Q_i, P_Ai=F0 Q_i
```

for a selected exact-block normal form.  Coordinatewise valuation of those
identities explains the coefficient pattern above once all normalized
factors, scalar source units and absolute product units are fixed.

What is not present is a theorem that every power-large branch simultaneously
has:

1. one common Laurent unit lattice and exactly these variables, with no
   additional factor or coefficient units;
2. all absolute complement spectra fixed on a power-large fibre at subpower
   cost;
3. a complete row set indexed by every relevant target occurrence rather
   than only a selected reciprocal chart;
4. propagation to all `qU` targets with `t^(28/9-o(1))` pair occurrences;
5. distance-label fibre below `t^(1/9-epsilon)` and outer stability.

Thus the formal matrix accurately describes the conditional unit incidence
of the normalized identities, but it has not been proved to be the complete
matrix of an actual power-large block.  Extra equations would only reduce a
kernel, while extra variables, absent absolute rows or changing unit rings
can enlarge the observable quotient; the formal theorem decides none of
those alternatives.

## Scope

This is a standalone elementary integer-matrix lemma inside the research
loop, but the campaign contract permits promotion only for a main exponent
improvement.  No actual power-large realization, spectrum-range bound,
all-target fibre estimate or stability bridge is proved.  The public `3/5`
exponent is unchanged.

