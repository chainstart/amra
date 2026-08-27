# Exact reduction of a non-affine positive-background family

Fix `Q=2^k >= 4`.  The old binary tower from
`positive_background_amplifier.md` leaves, up to finite onset exceptions,

    S_Q = {even integers} union {Qm-1:m>=1}.

Choose any increasing target indices `r_j` and any strictly increasing odd
steps `d_j` satisfying

    Q/2 < d_j,
    r_j < d_j <= (Q r_j - 1)/2.

Set the new original modulus and residue to

    n_j = 2 d_j,
    a_j = Q r_j - 1 (mod n_j).

Then the `n_j` are strictly increasing and exceed `Q`.  The residue `a_j` is
odd, so every new full class is odd and every even integer continues to
survive.  The upper bound on `d_j` says `n_j <= Qr_j-1`, so the distinguished
target is active.

Because `gcd(Q,2d_j)=2`, the intersection of this class with the rare cell is
one progression of period

    lcm(Q,2d_j)/Q = d_j

in rare-index coordinates.  It contains `r_j`; hence it is exactly

    {r_j + h d_j : h in Z}.

Since `0<r_j<d_j`, its positive part begins at `r_j`.  Thus the delayed
original class deletes from the old survivor precisely

    {Q(r_j+h d_j)-1 : h>=0}.

Let

    U = union_j {r_j+h d_j:h>=0}.

Apart from finitely many old-tower onset exceptions, the final survivor is

    {even integers} union {Qm-1:m not in U}.

Consequently the original survivor has logarithmic density if and only if
`U` does; if `delta_log(U)=eta`, its density is

    1/2 + (1-eta)/Q.

The affine theorem covers `d_j=c r_j+b` with fixed coprime `(c,b)`.  The exact
remaining structured question is whether a union of least-representative
progressions `r_j (mod d_j)` must have logarithmic density when both sequences
increase and `1 < d_j/r_j <= Q/2`.  This is still only a restricted subproblem
of Erdős #25, but either a proof or a counterexample here would materially move
the positive-density resume gate.

`work/search_nonaffine_echoes.py` samples this reduction exactly.  It chooses a
new class only when a requested target has not already been deleted, preserves
strict increase of `d_j`, and marks the entire positive progression through
the finite cutoff.

## Certified positive inner density

Global density `1/2` from the even reservoir is not by itself a useful stress
test: if the full progressions cover asymptotically all rare indices, the
rare-index survivor has density zero and the final original set converges to
the evens.  To remain inside the genuine positive-limit obstruction, fix an
odd `g>=3`, require

    r_j = a (mod g),       d_j = 0 (mod g)

for one fixed `a`.  Every progression `r_j (mod d_j)` then lies entirely in
the coarse cell `a (mod g)`.  The other `g-1` index cells survive every finite
stage and the infinite continuation.  Hence

    rare-index survivor density >= 1-1/g,

and the original survivor has the exact uniform lower bound

    1/2 + (1-1/g)/Q.

`work/search_confined_nonaffine_echoes.py` enforces these divisibility
conditions pointwise.  Its finite oscillations therefore cannot be dismissed
as a zero-inner-density route, although they still cannot establish an
infinite failure of logarithmic density.
