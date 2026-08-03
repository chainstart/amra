# Small-D normalized-moment falsification

## Exact paired-positive common-X block

Work in a one-variable Laurent group ring.  Let

`G=1+x`, `F_0=1+x^2`, `R_1=1`, and `R_3=1-x+x^2`.

Factor

`B=1+x^4+x^8=(x^2-x+1)(x^2+x+1)(x^4-x^2+1)`

and put `Q_1=B`, `Q_3=B/R_3`.  Direct multiplication gives

`G B = P_{ {0,1,4,5,8,9} }`,

`F_0 Q_1 = P_{ {0,2,4,6,8,10} }`,

`F_0 Q_3 = P_{ {0,1,2,6,7,8} }`,

as well as `B=R_jQ_j` and

`G R_1=1+x`, `G R_3=1+x^3`.

Thus the centre scalar is `2`, the two odd leaf scalars are `1,3`, all
positive products are masks, the odd leaves share `G`, and every row tiles
the same length-12 spectrum.

For a rational translation `t`, take the common source
`X_t={t,t+1}`.  The scalar masks acquire units `x^(lambda t)`, while the
complements acquire the inverse units.  In the simultaneous normal form,

`G_t=x^tG`, `F_(0,t)=x^(2t)F_0`,

`B_t=x^(-3t)B`, `R_(3,t)=x^(2t)R_3`,

`Q_(1,t)=x^(-3t)Q_1`, `Q_(3,t)=x^(-5t)Q_3`.

All mask and quotient identities remain exact.  After quotienting Laurent
associates, the Boolean vectors are unchanged:

`y_1=(1,1,1)`, `y_3=(0,1,1)`.

## Actual distance collision pair

Translate the common spectrum to `{100,...,111}` and take `rho=1`,
`z_lambda=lambda/2`.  For each row, subtract `lambda*t` from its complement
and then subtract `1+z_lambda^2` to obtain positive tangent squares.  For
`t=0,-1/4,-1/2`, every source coordinate lies in `[-1,1]`, so the standard
reverse-circle coordinates give genuine points in `R^3`.  Each row's
source--target squared-distance map is still a bijection onto the same
12-element spectrum.

Target--target distances were canonicalized exactly as

`tau+sigma+(z-w)^2-2 sqrt(tau*sigma)`,

with rational coefficients and squarefree radicals.  Among 18 targets the
exact distinct-label counts are:

- `t=0`: 127;
- `t=-1/4`: 145;
- `t=-1/2`: 138.

Hence `t=0` and `t=-1/4` have identical normalized Boolean quotient data,
normalized factor roots/log derivatives, paired positivity, common-X scalar
copies and the same per-row distance spectrum, but different target--target
collision behaviour.  This is an exact unit/translation adversarial pair.

It kills every claim that discards units and then asserts that normalized
moments determine target collision behaviour.  It does not refute a lower
bound uniform over the entire unit fibre, an asymptotic unit-aware theorem,
or the public problem.

## Other moment guards

On the uniform middle layer of `{0,1}^D`, every degree-one Walsh moment is
zero by coordinate complementation, while the row count is
`binom(D,D/2)`.  Exact enumeration for `D=2,4,6,8,10` gives row counts
`2,6,20,70,252`.  Low Fourier degree is therefore not row compression.

Unit-aware logarithmic derivatives satisfy the additive identity

`(Q_j'/Q_j)(chi) = unit_j(chi) + sum_nu y_(j,nu)(H_nu'/H_nu)(chi)`.

Once `y_j` and its unit are known, such jets are deterministic linear
readouts unless a new cross-row inverse theorem is proved.  Root multiplicity
and subset-poset statistics likewise do not acquire Euclidean meaning merely
by being computed exactly.

## Falsification result

The initial tests kill `M1083M4-02,03,04,05,06,08,09,11,12`.  The exact pair
directly kills `08,09`; the remaining kills are scoped representation or
missing-interface failures, not counterexamples satisfying every advertised
future hypothesis.

Three routes survive their first tests:

1. `M1083M4-01`: a genuinely common-X/paired-positive Fourier theorem beyond
   middle-layer statistics;
2. `M1083M4-07`: a theorem bounding or exploiting the Laurent-unit fibre;
3. `M1083M4-10`: an explicit propagation theorem from those unit-aware
   profiles to the all-target fibre threshold `1/9-epsilon`.

The exact checker ran under 3 GiB and 120 seconds.  No Lean process was used,
and the public `3/5` exponent did not change.
