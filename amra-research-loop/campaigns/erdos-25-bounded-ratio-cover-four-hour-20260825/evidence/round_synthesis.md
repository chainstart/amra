# Four-hour synthesis

## Outcome

The public Erdős 25 statement is **not closed**.  The campaign produced exact
subclass theorems, exact obstructions to several tempting proof mechanisms,
and one sharper theorem route, but neither an all-sequence logarithmic-density
proof nor a fixed infinite counterexample with a proved nonzero oscillation.

The four guarded search segments used

    5400.040083444997
  + 5432.586512609007
  + 2701.3790698619996
  +  865.0288517640001
  = 14399.03451768 seconds.

This is 0.96548232 seconds below the four-hour budget.  Analysis and exact
replay commands also used the guard but are verification overhead rather than
search-budget segments.

## Exact progress

1. If `sum 1/d_j` converges, bounded ratio makes `sum 1/r_j` converge and the
   infinite union is upper-log approximable by finite periodic unions.  It has
   natural, hence logarithmic, density.
2. Finite offset families `s_j=d_j-r_j`, pairwise-coprime modulus families,
   finite-colourable gcd-dependency families, and summably controlled affine
   chart families have logarithmic density.
3. The affine lift

       R_j = a + g r_j,    D_j = g d_j

   preserves admissibility and the bounded-ratio constant, has union exactly
   `a+gU`, and scales lower and upper logarithmic densities by `1/g`.  Thus a
   counterexample exists if and only if one can be confined to any prescribed
   positive-capacity arithmetic cell.  This lift does not repair the odd-
   modulus condition in the earlier binary embedding.
4. The Gilboa--Pinchasi finite progression-union theorem gives a valid finite
   almost-packing lower bound of order

       c(epsilon) min(n^(1-epsilon), ell)/(C R)

   in harmonic mass at target scale `R`.  No scale-uniform control of
   `c(epsilon)` or summable infinite scheduling was obtained.

See `tractable_tail_criteria.md`, `confinement_equivalence.md`, and
`finite_almost_packing_corollary.md`.

## Exact failed mechanisms

Uniform linear packing, a uniform pairwise-gcd second-moment constant, a
linear first-representative charge, full-history endpoint range, and bounded
echo collision multiplicity all fail.

The sharpest obstruction is the annular fixed-offset batch `r=d-1`,
`N<d<=2N`: targets are irredundant, yet the first `N` echoes lie in a
multiplication-table set of size `o(N^2)`.  Its fixed offset also explains why
this obstruction does not itself threaten density existence.  The prime
family `d=p,r=p-1` independently gives divergent target charge while its union
is all positive integers.  Arbitrarily many target-irredundant progressions
can also share one later echo via the `lcm(1,...,2H)-1` construction.

## Frozen-rule counterexample pressure test

Training used 5400.040083 seconds, 139851 trials, 85267 simulations, and
45842641967 exact rare indices.  Blind extension froze 24 rules and used
5432.586513 seconds, 368 simulations, and 24784557769 additional exact rare
indices, with cutoffs as large as 595898349.

Sixteen of 24 schedules generated at least two rises and two drops between
endpoints lying strictly beyond the training cutoff.  However, 15 of these 16
had negative log-log slopes of post-training step amplitude (median
`-0.15017`).  Among the four schedules whose training and blind strict floors
were both nonzero, the median blind/training floor ratio was only `0.06148`.

Therefore fixed finite-rule oscillation remains a finite counterexample
hypothesis, but the required positive asymptotic amplitude lower bound is not
supported.  The older overlapping-window persistence count is retained only
as a legacy diagnostic and is not treated as independent cycles.

## Non-affine near-extremizer pressure test

The primary seed used 2701.379070 seconds, 14322 trials, 12875 exact
target-irredundant batches, and 5708472281 progression incidences.  Its
champion had `N=525`, 27 offsets, non-affine union fraction `0.754032`, and a
same-moduli fixed-offset fraction `0.613634`, for ratio `1.22880`.

The 865.028852-second confirmation seed used 4727 trials, 4249 exact batches,
and 1842754879 incidences.  Its champion had `N=507`, 23 offsets, non-affine
union fraction `0.739832`, and fixed-offset fraction `0.567942`, for ratio
`1.30265`.

Both exact champion replays passed.  The search found no diffuse-chart batch
with multiplication-table-scale `o(N^2)` union.  This finite separation
supports, but does not prove, the following inverse route:

> multiplication-table-scale collision forces almost all compatible gcd
> weight into finitely or summably many affine offset charts.

The affine theorem would handle the structured charts, and the finite almost-
packing lemma would handle a quantitatively summable remainder.

## Freeze reason and next work

The mechanism-falsification gate requires killing at least 80% of
non-surviving mechanisms.  Only five of seventeen mechanisms have exact kill
certificates, so advancing would be bookkeeping rather than mathematics.

Freeze this campaign at mechanism falsification.  If Erdős 25 is revisited,
the next bounded task should be a proof-or-counterexample attempt for the
weighted affine-chart inverse lemma, with an explicit summable remainder.
Do not spend another long round extending the same random fixed-rule grammar.
