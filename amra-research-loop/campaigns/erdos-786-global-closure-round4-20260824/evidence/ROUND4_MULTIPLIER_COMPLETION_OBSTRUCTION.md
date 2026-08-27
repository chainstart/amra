# Round 4: multiplier-completion obstruction to guard-only coherence

## MC.1 (all-parameter completion theorem)

Let `P,Q` be disjoint nonempty finite sets of positive integers with
`|P|!=|Q|`.  Put

\[
X=\prod_{p\in P}p,\qquad Y=\prod_{q\in Q}q,
\qquad M=\max(X,Y).
\]

If `X=Y`, then `P,Q` are already a bad distinct-Finset relation.  Suppose
`X!=Y`.  For every sufficiently large integer `t`, the two shores

\[
P\cup\{tY\},\qquad Q\cup\{tX\}                              \tag{MC.1}
\]

are disjoint Finsets, have unequal cardinalities, and have equal products:

\[
X(tY)=Y(tX)=tXY.                                            \tag{MC.2}
\]

Only finitely many `t` can make `tX` or `tY` collide with a fixed member of
`P union Q`; `tX!=tY` follows from `X!=Y`.  This proves the claim.

Let `S` be any admissible infinite set containing `P union Q`, and let
`D=N\S`.  Relation (MC.1) forces

\[
\{tX,tY\}\cap D\ne\varnothing                              \tag{MC.3}
\]

for every sufficiently large `t`.  Among `1<=t<=T`, a fixed deleted integer
can occur as `tX` for at most one `t` and as `tY` for at most one `t`.
Consequently

\[
|D\cap[1,MT]|\ge {T\over2}-O_{P,Q}(1).                     \tag{MC.4}
\]

Thus, if `D` has a natural density,

\[
d(D)\ge {1\over2M}.                                        \tag{MC.5}
\]

The same proof gives upper density at least `1/(2M)` without assuming the
limit exists.

## Corollary MC.2 (small permanent seeds)

If an admissible set has natural density greater than `1-delta` and contains
three distinct integers `a,b,c<=R`, use `P={a,b}` and `Q={c}`.  If `ab=c`,
the three already form a forbidden relation.  Otherwise MC.1 gives

\[
\delta\ge {1\over2\max(ab,c)}\ge {1\over2R^2}.              \tag{MC.6}
\]

Hence for `delta<1/(2R^2)` the admitted part of `[1,R]` contains at most two
integers.

## Mechanism consequence

MC.1 refutes `M786G-12` in its frozen **guard-only** form.  Cross-block
relations are not confined to a sparse boundary: one permanently admitted
unequal-size seed produces the full matching family `{tX,tY}`, and hitting
that family only in future blocks costs positive density.  A successful
coherent construction must instead revise/delete at least one old seed
element and charge that recourse explicitly.  Once old-prefix recourse is
allowed, the route is `M786G-11`, not `M786G-12`.

This theorem does not refute the public problem.  Deleting finitely many old
seed elements has zero density, and MC.1 gives no lower bound uniform over
all possible seeds.
