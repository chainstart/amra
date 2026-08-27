# Audit of the periodized-bridge LLL diagnostic

Date: 2026-08-27

File audited read-only:
`work/m10_round1/periodized_bridge_lll_scan.py`.

Verdict: **PASS for the lattice, scaling, exact target, and single-term
weight; PASS with finite-claim scope qualifications.**

1. The first basis row represents `H=1,a_i=1` and the `i`-th remaining row
   represents `H=0,a_i=-p_i`.  Their integer span is exactly

   \[
   \{(2bH,2ha_1,\ldots,2ha_q):a_i\equiv H\pmod {p_i}\}.
   \]

   No congruence or carry condition is omitted from the coefficient-side
   small-lift lattice.
2. The two coordinate scales are correct: after division by the common
   box radius `2bh`, the first coordinate is `H/h` and the other coordinates
   are `a_i/b`.  Thus `inside_bridge_box` is exactly
   `|H|<h, |a_i|<b`.
3. The script uses
   `2b=2 floor((Delta-1)/2)+1` and

   \[
   h=\left\lceil{k^B C^qP\over\prod_i(p_i-k)}\right\rceil,
   \]

   which is the density-scale target used in the proof note.  It rejects
   systems outside the proved Fejer alias range `2h<P`.
4. For an inside row, `log_single_S_term` is exactly the logarithm of that
   row's summand in (14d):

   \[
   \log(P/h)-q\log b+log(1-|H|/h)
      +\sum_i\log(1-|a_i|/b).
   \]
5. Every reported LLL row is checked by exact integer divisibility and
   congruence before the floating logarithm is evaluated.  LLL supplies
   candidates only: it is neither an enumeration of all inside vectors nor
   an upper or lower bound for their total weighted sum.

Two output-scope qualifications are mandatory.  The aggregate field
`systems_with_inside_lll_row` counts any inside reduced-basis row, including
one labelled `trivial_diagonal`; nontriviality must be checked from
`best_nontrivial_log_single_S_term` or the full rows.  Also the script
records ordinary local support but does not compute `r_epsilon`, so the
description “high-support row” requires a separate comparison with the
block's threshold.  Subject to those qualifications, the reported negative
single-row log weights are valid finite falsification evidence, but they do
not control `S` because exponentially many unreported rows may contribute.
