# Long-run findings for Erdős #354

## Proved

1. Unit relations and every fixed-size interval seed can be delayed beyond an
   arbitrary parameter-independent binary depth, even with irrational α/β.
   See `arbitrary_delay_lemma.md`.
2. The disjoint residue-core bridge converts height-marked representatives and
   a disjoint interval of q-multiple subset sums into an explicit integer
   interval.  See `residue_core_bridge.md`.

## Exact finite pressure tests

The guarded search used exactly 4500.13 productive seconds across four
redirected segments and one completed depth-scaling segment.  The final segment
tested 48,619 sparse carry paths at depths 10 through 22, enumerating every
allowed prefix/tail split for the selected modulus.  At depth 22 it found a
path whose best split still had representative-height spread 524,292 and
zero-residue quotient core length 1, hence bridge margin -524,291.  Mechanical
replay is in `longrun_replay.json`.

These are finite no-go certificates, not an infinite counterexample.  They kill
the automatic single-modulus/single-split route, not the public conjecture.

## Remaining dependency

A proof must either construct a dynamic sequence of moduli and disjoint cores,
or show that multiple sparse carry obstructions are eventually paid by a
multi-block potential.  One residue-covering prefix followed by one arbitrary
tail is insufficient. The general γ ∈ (1,2) variant remains untouched.
