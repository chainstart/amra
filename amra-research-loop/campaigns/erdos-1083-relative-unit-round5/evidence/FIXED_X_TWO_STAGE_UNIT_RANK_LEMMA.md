# Fixed-X two-stage unit-rank lemma

For the exact normalized three-row paired-positive block, let

```text
u=(g,f,b,r1,r3,q1,q3)
```

be the seven Laurent exponents.

## Stage one: fixed X and normalized data

Fix `X_a={a,a+1}`, the normalized factors and quotients, the identities
`B=R1Q1=R3Q3`, and the three scalar source copies.  The resulting integer
linear system has rank five.  Its affine solution space is the particular
solution plus the two primitive directions

```text
v_gauge=(1,0,-1,-1,-1,0,0),
v_spectrum=(0,0,1,0,0,1,1).
```

The first direction annihilates every actual source and complement product
unit.  It is therefore a monomial refactorization gauge.  The second direction
translates all three complement product units equally.  It is observable: at
fixed `X={0,1}`, shifts `0` and `1/4` give different exact absolute
target-distance label sets, although both have 127 distinct target-target
labels.  Thus normalized data at fixed X do not have a rank-zero unit quotient
and this exact observable variation alone gives no collision-count gain.

## Stage two: fix the absolute row spectrum

If all three absolute 12-label source--target spectra are also fixed, the
three complement equations raise the matrix rank to six.  The remaining
solution space is exactly

```text
(a,2a,-3a,0,2a,-3a,-5a)+delta*v_gauge.
```

A rank-six minor has determinant `-1`, so the kernel is primitive and there
is no torsion in this exact quotient.  Imposing the projective gauge
`u(G)=a` forces `delta=0`; this gives one unique representative and loses no
source, complement, tangent or target-target distance datum.

## Proof boundary

Both statements are elementary consequences of exact rational row reduction,
the primitive minor, and substitution into all six product units.  The
checker additionally replays 65 integer gauge representatives and exact
squarefree-radical labels, but the all-rational conclusions follow from the
displayed kernels, not from finite sampling.

The lemma is local to this incidence matrix.  A general theorem must form the
complete matrix for every actual power-large block, identify all gauge
directions, control the remaining observable spectrum translations, and
derive either subpower range or a uniform distance-count gain.  No such
theorem, all-target propagation, `1/9-epsilon` fibre estimate or stability
bridge is proved here.  The public `3/5` exponent is unchanged.

