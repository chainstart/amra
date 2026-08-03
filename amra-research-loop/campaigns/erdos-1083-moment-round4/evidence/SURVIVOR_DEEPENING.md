# Survivor deepening: the unit-sensitive route

## Decisive finite lemma

There are two genuine reverse-circle configurations with the following data
identical after Laurent-associate normalization:

- the common-X scalar-copy pattern;
- the Boolean quotient vectors `y_1=(1,1,1)` and `y_3=(0,1,1)`;
- every normalized factor, root-multiplicity and logarithmic-derivative datum;
- paired positivity of all products used in the block;
- the same 12-element source--target squared-distance spectrum in every row.

Nevertheless their exact target--target squared-distance label counts differ:
the instance at source translation `t=0` has 127 labels and the instance at
`t=-1/4` has 145.  Both source sets lie in `[-1,1]`.  The identities and
distances are checked over rationals and canonical squarefree radicals by
`small_d_unit_translation_adversary.py`.

Consequently, no theorem whose sufficient statistic discards all Laurent
units can infer the target--target collision pattern from normalized Boolean,
factor/root and per-row spectrum data.  This is a precise information-loss
lemma.  It is finite and does not imply an asymptotic distance lower bound.

## M1083M4-01: Boolean Fourier/noise

The first Fourier levels do not compress the legal host.  On each even
middle layer of the Boolean cube, every degree-one Walsh moment vanishes,
while exact row counts for dimensions 2, 4, 6, 8 and 10 are 2, 6, 20, 70 and
252.  Conversely, retaining the full Fourier transform simply reconstructs
the complete Boolean distribution and can cost all `2^D` coordinates.

Thus a viable Fourier theorem must use an actual extra hypothesis: the same
common-X scalar copies, paired positivity, and unit compatibility must force
either concentration on `o(log t)` coordinates or a directly chargeable
Euclidean structure.  Neither ordinary low-degree cancellation nor generic
Boolean hypercontractivity supplies that interface.  This mechanism remains
conditional, not proved.

## M1083M4-07: Laurent-unit fibre

For the exact block the normalized quotient vectors are constant along the
translation orbit, but the Laurent exponents are

`u(G)=t`, `u(F_0)=2t`, `u(B)=-3t`, `u(R_3)=2t`,
`u(Q_1)=-3t`, and `u(Q_3)=-5t`.

The legal source interval contains the continuum `-1 <= t <= 0`; therefore
normalization alone supplies no finite unit count across configurations.
This does not kill M1083M4-07, because within one configuration the common
source is fixed and may constrain all row units jointly.  It sharpens the
required theorem: either prove a subpower bound for the *relative* row-unit
fibre after fixing the common source, or prove a uniform distance-label gain
over that fibre.  Counting normalized profiles is insufficient.

## M1083M4-10: propagation and fibre threshold

The selected reciprocal chart cannot close the exponent directly.  The full
target set has at most `qU` points, so its pair capacity is

`(qU)^2 = t^(28/9+o(1))`.

To force more than `t^(3-epsilon)` actual squared-distance labels by a fibre
argument, the maximum or average fibre must be at most

`t^(1/9-epsilon+o(1))`.

Information proved only on the selected `K` rows must also be propagated to
every one of the `qU` targets.  The exact translation pair shows why the
propagated profile must remain unit-aware.  No identity accomplishing this,
and no fibre estimate below `1/9`, is currently proved.

## Result of deepening

The strongest proved output is the unit-sensitivity firewall above.  It
closes the unit-blind normalized-moment route and focuses further work on a
three-link chain:

1. common-X/paired-positive Fourier structure beyond subset recovery;
2. control or exploitation of relative Laurent units;
3. unit-aware propagation to the complete target-pair graph with fibre
   exponent below `1/9-epsilon`.

Every link remains open.  The public `3/5` exponent is unchanged.
