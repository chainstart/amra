# Fixed-common-X unit rank and gauge falsification

## Exact fixed-X system

Use the normalized three-row paired-positive block inherited only as an
algebraic test object, but hold the common source literally fixed:

```text
X_a={a,a+1}.
```

Write the raw Laurent exponents as

```text
(g,f,b,r1,r3,q1,q3)
= (u(G),u(F0),u(B),u(R1),u(R3),u(Q1),u(Q3)).
```

The three scalar-source products and two quotient identities first impose a
fixed-X normalized-data system of rank five.  Its kernel has two generators:

```text
(1,0,-1,-1,-1,0,0),
(0,0,1,0,0,1,1).
```

The first is gauge.  The second translates `B,Q1,Q3` together.  It preserves
the literal common X, all normalized quotient/factor/root data, identities and
positivity, but shifts all three complement masks by the same amount.  The
shifts `0` and `1/4` produce different absolute radical distance-label sets,
although each still has exactly 127 target-target labels.

If the same absolute 12-label row spectrum is also fixed, the three complement
product equations join the system and impose

```text
g+r1=a,             f=2a,              g+r3=3a,
f+q1=-a,            g+b=-2a,           f+q3=-3a,
b-r1-q1=0,          b-r3-q3=0.
```

Exact rational row reduction gives matrix rank six on seven variables.  Every
solution is

```text
(a,2a,-3a,0,2a,-3a,-5a)
  + delta (1,0,-1,-1,-1,0,0).
```

A rank-six minor has determinant `-1`, so the exact block has no hidden
integer torsion.  The sole kernel generator is primitive.

## Gauge versus observable units

Along the `delta` direction,

```text
u(G)      increases by delta,
u(B),u(R1),u(R3) decrease by delta,
u(F0),u(Q1),u(Q3) stay fixed.
```

All six geometry-bearing product units remain constant:

```text
u(GR1), u(F0), u(GR3), u(F0Q1), u(GB), u(F0Q3).
```

The factor and quotient identities also remain exact.  Hence this is an
internal monomial refactorization gauge, not an observable target translation.
Fixing `u(G)=a` sets `delta=0` and gives one canonical representative.

Thus fixed X plus normalized data alone has one observable common-spectrum
translation after quotienting gauge.  Fixing the absolute row spectrum removes
that direction; every remaining solution then lies on the one gauge orbit and
the observable quotient has rank zero.

## Exact geometry guard

At the literal fixed source `X={0,1}`, the independent checker reconstructs
18 targets.  Every scalar row has source--target spectrum `{100,...,111}` and
the target set has 127 exact target--target labels.  For all 65 integer gauge
representatives `-32<=delta<=32`, the source units, complement units, tangent
squares and complete radical collision profile are identical.

The bounded sample is only an implementation guard.  Constancy for every
rational `delta` follows from the exact kernel calculation, since all actual
product units are constant on the whole affine line.

## Mechanism results

The gauge line strictly kills eight raw-unit claims:

- raw torus characters need not have geometric meaning;
- the raw fixed-X fibre need not be finite or subpower;
- individual factor valuations are unbounded despite fixed product supports;
- nonzero raw displacement need not cross a Newton or target wall;
- infinitely many raw vectors can have one collision profile;
- high additive energy on a gauge progression has no collision consequence;
- raw conditional entropy consumes no carrier or label;
- representative count is unrelated to collision-chamber count.

One gauge-quotient mechanism survives:

- `M1083U5-07` is proved on this exact block: a projective gauge slice is
  unique and lossless.
- `M1083U5-08` is killed as stated: before absolute spectrum fixing, this exact
  fixed-X normalized-data quotient already has observable rank one.

## Scope

This is not the round-four translation pair: `X` does not move.  It finds
both a pure gauge line and a genuine common-spectrum translation.  The latter
changes absolute labels but not the 127-label count in the tested pair; after
fixing that spectrum only the geometrically identical gauge representatives
remain.

The exact lemma supplies no uniform theorem for general blocks, no all-target
propagation, no fibre bound below `1/9-epsilon`, and no stability theorem.  The
public `3/5` exponent is unchanged.

## Reproduction

```sh
env AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh \
  python3 amra-research-loop/campaigns/erdos-1083-relative-unit-round5/evidence/fixed_X_unit_rank_falsification.py
```

The run completed in under one second with no Lean. SHA-256:

- script: `ee87da519c620760ad477e0e89ffd52fc85defd59dfe9266faceb0b37ad93e9f`
- JSON: `329c4c41d0471e49828176ab9902dccbf818acfe703d2fc7779289469e2ae4e6`
