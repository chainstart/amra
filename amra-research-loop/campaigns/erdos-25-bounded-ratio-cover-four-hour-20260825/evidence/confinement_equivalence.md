# Exact affine-confinement equivalence

This is an author-verified structural lemma for the bounded-ratio subproblem.
It shows that requiring a fixed positive-density reservoir does not make the
subproblem easier.

Let

    U = union_j {r_j+h d_j : h>=0},

with both sequences strictly increasing and

    0<r_j<d_j<=C r_j.

Fix any integer `g>=2` and residue `0<=a<g`, and define

    R_j = a+g r_j,    D_j = g d_j.

Then `R_j,D_j` are strictly increasing and

    0<R_j<D_j<=C R_j.

Indeed `R_j<D_j` follows from

    a+g r_j <= g-1+g r_j < g(r_j+1) <= g d_j,

and `D_j<=C g r_j<=C R_j`.  The lifted progression union is exactly

    V = union_j {R_j+hD_j:h>=0} = {a+g n:n in U}.

For logarithmic harmonic sums,

    1/(a+g n) = (1/g)(1/n) + O(1/n^2).

The accumulated error is bounded and
`log((X-a)/g)=log X+O(1)`.  Consequently the lower and upper logarithmic
densities transform as

    lower_delta_log(V) = lower_delta_log(U)/g,
    upper_delta_log(V) = upper_delta_log(U)/g.

Thus `V` has a logarithmic density if and only if `U` does.  At the same time,
`V` lies entirely in one residue cell modulo `g`, so its complement has lower
natural density at least `1-1/g` at every finite stage and in the limit.

## Consequences

1. If the bounded-ratio theorem is false, it already has a counterexample
   confined to one arbitrary coarse cell, with a certified positive-density
   complement.
2. The positive-inner-density constraint used by the guarded searches is not
   an extra mathematical restriction; it is a lossless affine lift.
3. A universal proof must be stable under quotienting and lifting periodic
   cells.  A global survivor-density lower bound alone cannot supply the
   missing tightness estimate.
4. Cell-relative signed amplitudes are the invariant quantity under this
   lift; absolute amplitudes are scaled by `1/g` but remain nonzero for every
   fixed `g`.

This lemma does not decide whether the base union `U` has logarithmic density.
It sharpens the interface between a bounded-ratio counterexample and the
positive-density version needed in the Erdos 25 reduction.  The particular
binary-reservoir embedding from the preceding campaign also imposed odd echo
steps; this lift preserves, rather than repairs, the parity of `d_j`.  Hence an
arbitrary counterexample would still need an odd-step realization or a
modified embedding before it directly refuted the public problem.
