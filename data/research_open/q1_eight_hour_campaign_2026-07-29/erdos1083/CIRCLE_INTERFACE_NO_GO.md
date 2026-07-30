# Fixed-axis circular interface: a critical-scale no-go theorem

## Scope

This note isolates what can and cannot be proved from the circular-fibre
interface (4.37j) alone.  It is a falsification result for a class of proposed
intermediate lemmas, not a counterexample to Erdos #1083.

Fix an axis `L`.  On each orbit circle `C`, encode `P intersect C` by a finite
angular set `A_C` in `R/(2 pi Z)`.  With a reference plane of angle zero, set

```text
q_alpha = sum_C |A_C intersect {alpha, alpha+pi}| + |P intersect L|,
r_alpha = sum_C |A_C intersect (A_C+2 alpha)| + |P intersect L|.
```

These are exactly the source-plane population and the success count of the
associated axial rotation.

## Theorem 1 (critical local-interface extremizer)

For every integer `t >= 3` there is a finite family of circular angular fibres
and `M=t` distinct infinite-order rotation angles such that, with

```text
N = t^5,       D_0 = t^3,       Q = t^3,
M = t,         R = t^5(1-2/t),
```

all of the following hold:

1. the total number of angular points is `N`;
2. every fibre contains `t^2 <= D_0` points and determines only `t^2-1 < D_0`
   nonzero within-fibre chord labels;
3. every active angle has `q_alpha=Q` and `r_alpha>=R`;
4. the active source incidence sum is `M Q=t^4<=N`;
5. the active rotation-success sum is at most `M N=t^6<=N D_0=t^8`;
6. nevertheless

```text
sum_active q_alpha r_alpha
  = t^6 (t^3-t(t+1))
  = t^9-t^8-t^7
  = (t-1-1/t) N D_0.
```

In exponent notation,

```text
D_0=Q=N^(3/5),  M=N^(1/5),  R=N(1-o(1)),
sum_active q_alpha r_alpha = N^(9/5)(1-o(1)).
```

Consequently no argument using only the displayed circular formulas, total
mass, the per-fibre `O(D)` chord cap, the source incidence capacity, and the
fixed-axis rotation capacity can rule out the exact critical configuration.
Any successful lemma must spend information about distances *between
different fibres* (or an equivalent genuinely global constraint).

### Proof

Choose a real angle `theta` with `theta/pi` irrational.  Take `F=t^3` formal
circular fibres and put on every fibre the same angular progression

```text
A={0,theta,...,(S-1)theta},  S=t^2.
```

Thus `N=F S=t^5`.  For `j=1,...,t`, put `alpha_j=j theta`.  Irrationality
implies that `alpha_j+pi` is not in `A`, so the plane of angle `alpha_j`
contains exactly one point from each fibre:

```text
q_(alpha_j)=F=t^3.
```

The rotation through `2 alpha_j` translates the progression index by `2j`.
It therefore has exactly `S-2j` successful indices on every fibre:

```text
r_(alpha_j)=F(S-2j)>=F(S-2t)=N(1-2/t).
```

The same irrationality makes every nonzero `2 alpha_j` an infinite-order
circle rotation.  It also ensures that index differences
`1,...,S-1` give distinct unoriented chord lengths: equality of two such
chords would imply `(k-l)theta` or `(k+l)theta` is a multiple of `2 pi`.

Summing the exact formulas gives

```text
sum_j q_j r_j
 = F^2 sum_(j=1)^t (S-2j)
 = t^6(t^3-t(t+1)).
```

All remaining inequalities are immediate substitutions.  QED.

## Proposition 2 (an honest Euclidean realization has many distances)

The angular fibres in Theorem 1 have a literal Euclidean realization, but a
natural such realization has `N-1`, not `D_0`, nonzero distances.

Put all fibres on a circular cylinder of radius `0<rho<1/2`, at heights
`0,1,...,F-1`.  The squared-distance set is exactly

```text
{x_k+h^2: 0<=k<S, 0<=h<F} minus {0},
x_k=2 rho^2(1-cos(k theta)).
```

All displayed combinations occur, by taking angular-index difference `k` and
height-index difference `h`.  Irrationality of `theta/pi` makes the `S`
numbers `x_k` distinct.  They all lie in `[0,4 rho^2) subset [0,1)`;
therefore the blocks `h^2+{x_k}` are disjoint for different nonnegative
integers `h`.  The distance count is consequently exactly

```text
S F-1=N-1.
```

Thus Theorem 1 is deliberately an **abstract-interface counterexample**, not
an `N`-point Euclidean configuration with `D_0=N^(3/5)` distances.  Its force
is logical: the omitted cross-fibre distances are indispensable.  Assigning
`D_0=t^3` records only that every local capacity previously used is compatible
with the critical scale.

The exact integer verifier is `verify_circle_interface_no_go.py`, with tests in
`test_verify_circle_interface_no_go.py`.

## Theorem 3 (coherent equal-radius fibres are globally too expensive)

There is a rigorous positive exclusion for the most coherent realization.
Let `F` distinct coaxial circles have a common radius `rho` and distinct
heights.  Suppose that every circle contains the same angular progression

```text
A={0,theta,...,(S-1)theta},
```

where `theta/pi` is irrational and `0<theta<pi/(2S)`.  Then the configuration
determines at least

```text
c S sqrt(F)-1
```

nonzero distances, for an absolute constant `c>0`.

### Proof

Let

```text
X={x_k=2 rho^2(1-cos(k theta)):0<=k<S}
```

and let `Y` be the set of squared height differences.  Ordering the heights
as `z_1<...<z_F` shows that

```text
{(z_j-z_1)^2:1<=j<=F} subset Y,
```

so `|Y|>=F`.  Every element of `X+Y` is a squared distance: use the two
fibres producing the chosen height difference and points whose angular
indices differ by `k`.

The consecutive gaps of `X` are

```text
x_(k+1)-x_k
 =4 rho^2 sin(theta/2) sin((2k+1)theta/2).
```

They are strictly increasing because `S theta<pi/2`.  Thus `X` is a convex
set in the additive-combinatorial sense.  The convex-sumset theorem gives

```text
|X+Y| >= c |X| |Y|^(1/2) >= c S sqrt(F).
```

Removing the zero distance proves the claim.  The invoked bound is the
standard unequal-size form of the Elekes--Nathanson--Ruzsa convex-sumset
estimate; a direct crossing-number proof appears in I. Ruzsa and J. Solymosi,
*Sumsets of Semiconvex Sets*, Theorem 1, arXiv:2008.08021.

For the critical local parameters `S=t^2`, `F=t^3`, and `N=t^5`, this yields

```text
D >= c t^(7/2)=c N^(7/10),
```

which is a fixed-power contradiction to `D=N^(3/5+o(1))`.

## Exact remaining gap

Theorem 3 kills the full rectangular progression extremizer, but the original
correlation hypotheses do not yet supply that rectangle.  They only give
large aggregate quantities

```text
sum_C |A_C intersect (A_C+2 alpha)| >= R
```

for each of many `alpha`, while `q_alpha>=Q` says that the single angle
`alpha` occurs on many (not necessarily the same) fibres.  A proof must
extract, with only subpolynomial loss, many fibres that share a long convex
angular pattern or another cross-fibre structure to which a sumset estimate
applies.  Standard averaging alone does not make the participating fibre
sets identical.

A now sharply specified route is:

1. use the simultaneous near-full correlations to extract many fibres with a
   common long approximate progression;
2. pass to a short arc where the chord-square sequence is convex;
3. apply a robust convex-sumset bound to cross-fibre offsets.

The unresolved step is item 1 with sufficient quantitative uniformity.  The
local no-go theorem shows why omitting it cannot work, while Theorem 3 shows
that completing it at the critical exponents would give more than the needed
fixed-power saving.
