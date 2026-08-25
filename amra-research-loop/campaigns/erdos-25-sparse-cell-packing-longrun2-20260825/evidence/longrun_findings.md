# Long-run findings: cross-scale sparse-cell packing

## Mathematical status

Erdős #25 remains open.  The official page was rechecked on 2026-08-25 and
still records the exact activated-residue statement as OPEN.  This campaign
does not claim a proof or counterexample.

## Proved in this round

1. **Positive-background aggregate amplifier.**  A binary old tower leaves
   all evens plus one odd class modulo `Q`, so its density is `1/2+1/Q`.
   The block `n_r=rQ-2`, residue `1`, `R<=r<2R`, has pairwise isolated
   targets and aggregate transient/eventual-density ratio asymptotic to
   `Q/(4 log Q)` when `R=Q`.  Thus even a positive background admits
   unbounded relative local overspend.

2. **Absolute bounded-window limit.**  The same block has absolute normalised
   mass tending to zero.  In general, all targets in `[X,cX]` have total
   normalised harmonic capacity `O(log(c)/log(X))`.  Relative amplification is
   not an oscillation certificate.

3. **Affine echo-to-multiples theorem.**  For fixed `c,b` with
   `gcd(b,c)=1`, every family

       union_r {r+h(cr+b):h>=0}

   has logarithmic density.  The identity

       k=r+h(cr+b)  iff  cr+b divides ck+b

   reduces it to the Davenport--Erdős theorem for sets of multiples.  The
   proof also gives finite-periodic approximation in upper logarithmic
   density, hence every finite union of coprime affine echo families has
   logarithmic density.  This universally closes every infinite continuation
   of the explicit binary amplifier, not merely the finite samples.

4. **Exact non-affine hard-core reduction.**  With `Q` fixed, choose increasing
   targets and odd increasing echo steps satisfying

       r_j < d_j <= (Q r_j-1)/2.

   Original moduli `2d_j` and residues targeting `Qr_j-1` reduce exactly to
   the least-representative union `union_j r_j (mod d_j)` in the rare cell.
   Imposing `r_j=a (mod g)` and `g|d_j` confines all attacks to one coarse cell,
   certifying rare-index survivor density at least `1-1/g` and original
   survivor density at least `1/2+(1-1/g)/Q` throughout the infinite
   continuation.

## Guarded execution

The four productive segments used 600.148, 600.047, 1800.243, and 3000.013
seconds.  Total guarded productive time before replay was 6000.450 seconds,
or 100.008 minutes.  They evaluated 197,502 comparable configurations and
49,792,994,323 exact rare-index positions.  Every segment ran in an OpenMath
scope with 30 GiB high, 34 GiB max, 4 GiB swap max, and 512 tasks max.  Peak
memory observed at the long-search checkpoints remained below 62 MiB and
observed swap use was zero.

Two redirects were mathematical rather than resource failures: affine search
stopped when the all-parameter theorem closed its whole family; unrestricted
non-affine search stopped when global density from the even reservoir was
recognised as insufficient to certify positive density inside the attacked
cell.  The final 3000 seconds excluded the already-proved max-step affine
policy.

## Signed finite stress test

The largest raw endpoint range in the final pure non-affine search was about
`0.015622`, but signed auditing showed that this champion was monotone on its
late endpoints.  A range is not an oscillation.

The best retained two-sided schedule had `Q=32`, `g=3`, a certified original
survivor-density lower bound `0.520833...`, and finite two-sided swing
`0.00012984` at rare-index cutoff 42,699.  Keeping every parameter fixed and
extending to 60,000,000 indices preserved alternating rises and drops, but the
window's largest recovery drop decreased to about `0.0000860`; the two most
recent displayed drops were about `0.0000711` and `0.0000590`.  This is finite
evidence consistent with decay, not a proof of decay, and not a counterexample.

Mechanical replays of the affine and final non-affine champions passed
byte-for-byte.  The affine algebraic map passed 5,760 exhaustive finite subset
checks.  None of these author-controlled replays is an independent audit.

## Remaining theorem-grade dependency

The precise next subproblem is:

> For every fixed `C`, must every union of progressions `r_j (mod d_j)` have
> logarithmic density when both sequences increase and
> `r_j < d_j <= C r_j`?

A positive answer closes the fixed positive-capacity non-affine echo
obstruction exposed here.  A negative answer becomes relevant to Erdős #25
only if one fixed infinite schedule has two-sided normalised swings bounded
away from zero while retaining a certified positive inner finite-stage
density.  More finite range champions or monotone endpoint drift are
insufficient.
