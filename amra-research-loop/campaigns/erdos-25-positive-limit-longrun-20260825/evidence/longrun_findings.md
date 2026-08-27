# Long-run findings for Erdős #25

## Proved

1. The actual new delayed layer is exactly D_i = U_i ∩ [n_i, ∞), and the
   eventual densities of the disjoint full increments telescope.
2. The nested power-of-two construction has unbounded individual transient
   amplification asymptotic to Q/(2 log Q). See
   `conditional_layers_and_transient_amplifier.md`.

## Exact positive-density certificates

The guarded search used 2623.47 seconds before replay.  Over a previous
complement of density about 0.155 it found a two-layer finite block whose
normalised harmonic target mass is at least 1.309 times the sum of the two
eventual densities.  Thus even a positive-density background permits local
budget overshoot.

At candidate-modulus offsets 10,000 and 100,000, the best density-at-least-0.1
certificates had amplification lower bounds 0.946 and 0.908 respectively.  The
hard examples used only gcd 2 or 3 with the old period: the real obstruction is
that the old survivor can be extremely uneven among low-order congruence cells.
These are finite trends, not universal upper bounds.  Exact mechanical replay
is in `longrun_replay.json`.

## Remaining dependency

The positive-limit case now reduces to controlling repeated packing into the
same low-density congruence cell across many scales.  A viable proof needs an
aggregate potential that permits finite local overshoot but prevents it from
recurring with nonvanishing normalised harmonic mass.  No such bound was proved,
and no infinite oscillating construction was obtained.
