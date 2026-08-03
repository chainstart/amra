# Independent audit: fixed-X relative units

## Verdict

The exact two-stage rank lemma reconstructs independently.  Fixed `X` and
the normalized source/identity equations give rank five with a two-dimensional
kernel.  Adding the three absolute complement-spectrum equations gives rank
six with exactly the primitive gauge line.  On that line `u(G)=a` selects one
representative and all six product units stay fixed.

The result is local to the displayed three-row block.  It does not improve
the public `3/5` exponent.  One mechanism verdict, `M1083U5-08`, needs a
scope downgrade because its literal statement concerns every power-large
block, whereas the counterevidence is finite.

## Independent linear reconstruction

Using variables `(g,f,b,r1,r3,q1,q3)`, I reconstructed the matrix directly
from the eight displayed equations rather than importing the author checker.
For the source and identity subsystem the rank is five.  Direct multiplication
annihilates both

```text
v_g=(1,0,-1,-1,-1,0,0),
v_s=(0,0,1,0,0,1,1).
```

Since the nullity is two, these independent vectors span its rational kernel.
The full matrix has rank six.  It annihilates `v_g`, while

```text
A v_s=(0,0,0,1,1,1,0,0),
```

so fixing all three absolute complement products removes `v_s`.  The gcd of
all nonzero rank-six minors is one; hence the remaining integer kernel is
primitive in this exact system.

Substitution independently gives

```text
(a,2a,-3a,0,2a,-3a,-5a)+delta*v_g.
```

Its first coordinate is `a+delta`, so `u(G)=a` is equivalent to `delta=0`.
This proves uniqueness of the displayed gauge slice, not a uniform theorem
for other incidence matrices.

## Independent geometry reconstruction

I rebuilt the 18 targets at literal common source `X={0,1}` and canonicalized
all 153 target-pair squared distances over rational coefficients and
squarefree radicals.

For common-spectrum shifts zero and `1/4`:

- both configurations have exactly 127 distinct labels;
- the absolute label sets differ;
- the indexed collision partitions are identical;
- in both cases 102 labels occur once, 24 occur twice, and one occurs three
  times.

Therefore `127/127` means precisely that this finite observable spectrum
translation changes label values but produces no label-count gain.  It is not
an asymptotic lower bound and cannot change an exponent.

## Mechanism and statement scope

The gauge line strictly supports the kills of raw-coordinate claims
`M1083U5-01` through `06`, `09`, and `10`.  `M1083U5-07` passes exactly for
this block.

`M1083U5-08` is not literally refuted as written.  Its decisive claim begins
“in every actual power-large ... block,” while the exhibited positive
observable rank occurs in one finite three-row block.  The example correctly
refutes automatic rank-zero inference from this local normal form, but it
does not prove that a power-large legal block realizes the same direction.
The audit therefore records it as an inconclusive finite route obstruction,
not a strict kill and not a survivor theorem.

## Promotion boundary

No complete matrix theorem for general blocks, bound on observable spectrum
range or torsion, all-target occurrence mass, fibre estimate below
`1/9-epsilon`, or outer stability transfer is supplied.  The sole campaign
success condition `main_exponent_improved` is unmet.  Promotion is rejected,
and the public `3/5` exponent is unchanged.

The independent checker used 3 GiB/180 seconds and no Lean.
