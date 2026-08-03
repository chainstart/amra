# G201: exact two-coordinate falsification test

## Result

No fixed-edge-quantifier falsifier was found on the bounded exact test.
For both `K4` and `W4`, every accepted point had every edge strictly good.
Thus the strict-good profile never shrank, and no two profiles had empty
intersection.

This is a finite absence result.  G201 remains surviving and unproved.

## Exact setup

For each host, each marked edge `e`, and each pair of globally varied edges
`f,g`, forest enumeration is performed once.  It produces exact biaffine
integer polynomials

```text
P_e(x,y)=a00+a10*x+a01*y+a11*x*y,
Q_e(x,y)=b00+b10*x+b01*y+b11*x*y.
```

No symbolic algebra package is used during the grid search.  The grid is

```text
x,y in {-20,-159/8,...,79/8,10}.
```

For an endpoint `(x,y)`, consider the simultaneous straight path from the
all-ones point:

```text
x(t)=1+t(x-1), y(t)=1+t(y-1), 0<=t<=1.
```

Every `P_e(x(t),y(t))` has degree at most two.  The script computes its three
degree-two Bernstein coefficients exactly as integers after multiplying by
the common positive factor `2*8^2`.  A point is admitted only when all three
coefficients are strictly positive for every marked edge.  Since Bernstein
basis functions are nonnegative and sum to one, this proves `P_e>0` on the
complete path to the positive anchor for every edge separately.  Therefore
each restriction lies in its distinguished deletion component.

Only after this simultaneous component certificate is established does the
script evaluate every `Q_e` and form the strict-good edge set.

## K4

All 15 varied-edge pairs and 58,081 rational endpoints per pair were tested.
There were 109,800 endpoints with a simultaneous Bernstein-positive path.
After good-set deduplication there was exactly one profile: all six edges.
Consequently the minimum intersection of any two observed profiles is six.

A genuinely two-coordinate representative varies edges `01,02` to

```text
(-5/8,3/2).
```

Across all marked edges its smallest scaled Bernstein coefficient is 16 and
its smallest scaled `Q_e` value is 40, both strictly positive.

Negative `Q` values do occur away from certified paths.  For example at
`(x,y)=(-20,-20)`, edges `01,02,03` have nonpositive `Q`; however the marked
edge `01` has scaled `P`-path Bernstein coefficients

```text
[3072,-15744,-34560].
```

This exact barrier rejects the point as a component-valid counterexample.

## W4

All 28 varied-edge pairs and the same 58,081 endpoints per pair were tested.
There were 205,518 simultaneously certified endpoints and again exactly one
strict-good profile: all eight edges.  The minimum observed two-profile
intersection is eight.

For the representative varying `01,02` to

```text
(-5/8,21/8),
```

the smallest scaled Bernstein coefficient is 18 and the smallest scaled
`Q_e` value is 230.

At the rejected point `(-20,-20)`, `Q_01,Q_02` are nonpositive, but the
`P_01` path has exact scaled Bernstein coefficients

```text
[11008,-58880,-128768].
```

It therefore leaves `{P_01>0}` and supplies no G201 kill.

## Scope

Bernstein positivity is a sufficient path certificate, not a complete
description of the distinguished component.  Rejected grid points might be
reachable by nonlinear paths, and points outside this finite denominator-eight
box were not tested.  Hence the calculation does not prove G201 for either
host and cannot be extrapolated to arbitrary graphs.

The campaign remains in `mechanism_falsification`.  No Lean was used and no
public OPG conclusion changes.

Reproduction:

- `evidence/g201_multicoordinate_exact.py`, SHA-256
  `0748bf11ee1cafe982c6856d5de6a727f245235ce42657bc619d1c8b63c1de37`
- `evidence/G201_MULTICOORDINATE_EXACT.json`, SHA-256
  `dcf165949bb88a8082866c7916d89063b5aa6a8d2afc89d226c153681986e213`

```sh
AMRA_MEMORY_KIB=2097152 AMRA_TIMEOUT_SECONDS=120 LEAN_NUM_THREADS=1 \
  ../../scripts/run_bounded.sh python3 evidence/g201_multicoordinate_exact.py
```
