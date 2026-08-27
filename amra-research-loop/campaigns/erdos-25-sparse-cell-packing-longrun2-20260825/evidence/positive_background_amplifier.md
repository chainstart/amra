# A positive-background aggregate amplifier and its absolute-capacity limit

This note is author-verified mathematics.  The accompanying verifier checks
the finite identities and numerical asymptotics, but it is not an independent
audit.

## Construction

Let `Q = 2^k` with `Q >= 4`.  For each power of two `q` with
`4 <= q <= Q`, first forbid

    q/2 - 1 (mod q).

The full complement of these old classes is exactly

    S_Q = {even integers} union {-1 (mod Q)}.

Indeed, the class `1 (mod 4)` removes one half of the odd integers, the
class `3 (mod 8)` removes one half of the remaining odd integers, and so on.
Thus `S_Q` has periodic density `1/2 + 1/Q`, uniformly bounded away from
zero.

Fix an integer `R >= 2`.  For every integer `r` in `[R, 2R-1]`, add

    n_r = rQ - 2,        a_r = 1 (mod n_r),

and call

    t_r = rQ - 1 = n_r + 1

its distinguished target.  The new moduli are strictly increasing and larger
than `Q` when `R >= 2`.

## Exact target isolation

Every `t_r` is odd and is `-1 (mod Q)`, so it belongs to `S_Q`.  It is the
first member of `1 (mod n_r)` at or after the onset `n_r`.

If `r < s`, then `t_r < n_s`, so the later class is not active at `t_r`.
The earlier class contains `t_s` exactly when

    n_r divides t_s - 1 = n_s.

All the `n_r` lie in one half-open multiplicative interval: for
`R <= r < s <= 2R-1`,

    n_r < n_s < 2 n_r.

Consequently no `n_r` divides another `n_s`, and every target is deleted by
its own delayed class but by no other selected class.

## Eventual-density budget

The class `1 (mod n_r)` is odd, so among the old survivor residues modulo
`Q` it is compatible only with `-1 (mod Q)`.  Since

    gcd(Q, n_r) = gcd(Q, 2) = 2,

the intersection has one residue modulo `lcm(Q,n_r)=Q n_r/2`.  Its density
before accounting for overlaps among the new classes is therefore

    e_r = 2 / (Q n_r).

The density of the union of all new full increments is at most

    E(Q,R) = sum_{r=R}^{2R-1} 2 / (Q(rQ-2)).

At the cutoff `X=(2R-1)Q-1`, target isolation gives the rigorous lower bound

    A(Q,R) = [sum_{r=R}^{2R-1} 1/(rQ-1)] / log X

for normalised harmonic deletion mass.  Taking `R=Q` gives

    A(Q,Q) / E(Q,Q) ~ Q / (4 log Q),

so aggregate relative amplification is unbounded even though the old
complement density tends to `1/2` rather than to zero.  This kills every
unconditioned local charging inequality of the form `A <= C E`.

## Why this does not answer Erdős #25

For `R=Q`,

    A(Q,Q) ~ log(2) / (Q log(2Q^2)) -> 0.

The relative ratio diverges only because the eventual-density budget is even
smaller.  More generally, every set of targets contained in `[X,cX]` has

    (1/log(cX)) sum_{X <= m <= cX} 1/m
      <= (log c + O(1/X)) / log(cX) -> 0.

Thus a bounded-ratio block cannot by itself produce nonvanishing logarithmic
oscillation, regardless of its congruence structure.  A counterexample would
need deletion and recovery windows whose logarithmic span is comparable with
the full logarithmic age of their endpoint.  The outstanding issue is whether
the unavoidable future CRT repetitions (the "echoes" of each selected class)
permit such recovery while the finite-stage complement retains positive
density.
