# Erdős Problem 1 Boolean Boundary Notes

Target: `boolean_half_downset_upperBoundary_card_ge_middle`.

External source relied on for theorem identification:

- Stephen Raty, "Harper's Theorem", arXiv:1806.11061, https://arxiv.org/abs/1806.11061.

The current Lean blocker is that mathlib in this workspace provides LYM,
Sperner, shadow, Harris-Kleitman, and Kruskal-Katona APIs, but not a packaged
Harper vertex-isoperimetric theorem for the Boolean cube. The target theorem is
the half-sized downset external vertex-boundary case of Harper.

Iteration 2 tool check:

- Python exhaustive check over all half-sized downsets for `n = 1,2,3,4`
  found minimum upper external boundary sizes `1,2,3,6`, matching
  `Nat.choose n (n / 2)`.
- Lean progress added rank-slice boundary support lemmas:
  `boolean_slice_succ_subset_upShadow_slice` and
  `boolean_upperBoundary_slice_eq_upShadow_slice_sdiff`.

Iteration 3 tool/proof notes:

- Re-ran the Python exhaustive check for `n = 1,2,3,4`; the half-downset
  counts/minimum boundary sizes were `(1,1)`, `(2,2)`, `(4,3)`, `(24,6)`,
  again matching the middle binomial coefficients.
- Searched the local mathlib/project for Harper, Boolean vertex-isoperimetry,
  and symmetric-chain-decomposition APIs. No packaged Harper/SCD theorem was
  found; the available local machinery remains LYM, Sperner,
  Harris-Kleitman, shadows, and Kruskal-Katona.
- Lean progress added basic setup lemmas:
  `boolean_downset_isLowerSet`, `boolean_half_downset_empty_mem`, and
  `boolean_half_downset_univ_not_mem`.

Iteration 4 Lean progress:

- Added and verified `boolean_upperBoundary_subset_of_not_mem`: if `∅ ∈ D`
  and `t ∉ D`, then some `u ⊆ t` lies in the one-step upper external
  boundary of `D`.
- This supports the next proof route: every maximal Boolean chain has a first
  exit through the upper external boundary. A Lubell/counting lemma for such
  chain cutsets would imply boundary size at least the middle binomial
  coefficient using `Nat.choose_le_middle`.
- Verifier command `lake env lean FormalConjectures/ErdosProblems/1.lean`
  passes with only the pre-existing `sorry` warnings in unrelated declarations.

Iteration 5 Lean/tool progress:

- Re-ran a Python finite check for all half-sized downsets through `n = 5`.
  The minimum upper external boundary sizes were `1, 2, 3, 6, 14`, while
  `Nat.choose n (n / 2)` is `1, 2, 3, 6, 10`.
- Added the exact Lean target
  `boolean_half_downset_upperBoundary_card_ge_middle` to
  `FormalConjectures/ErdosProblems/1.lean`.
- The proof body now verifies the previously formalized first-exit setup:
  `∅ ∈ D`, `univ ∉ D`, and the top set has a one-step boundary subset.
  The remaining Lean gap is precisely the Harper/symmetric-chain global
  lower bound for the half-downset boundary.

Iteration 6 Lean progress:

- Local search again found no packaged Harper vertex-isoperimetric or symmetric
  chain decomposition theorem in the local mathlib checkout. Available tools
  remain LYM/Sperner, shadow APIs, Harris-Kleitman, and Kruskal-Katona.
- Added and verified
  `boolean_slice_card_mul_succ_le_boundary_add_next_slice`, a rank-slice
  recurrence obtained from local LYM:
  `|D_k| (n-k) <= (|B_{k+1}| + |D_{k+1}|)(k+1)`.
- Added and verified `boolean_half_downset_upperBoundary_nonempty`, factoring
  the first-exit argument out of the target proof.
- Verifier command `lake env lean FormalConjectures/ErdosProblems/1.lean`
  passes with the target still warning because the final global
  Harper/SCD/Lubell-cutset lower bound is not yet formalized.
- No new external source was used in this iteration; the standing external
  provenance remains Raty, "Harper's Theorem", arXiv:1806.11061.

Iteration 7 Lean/tool progress:

- Ran a Z3 Optimize finite check for `n = 6`, with Boolean variables for all
  `64` subsets, downset implications, exact size `32`, and the exact
  one-step upper external boundary definition. Z3 returned an optimum model
  with boundary size `20`, matching `Nat.choose 6 3`.
- The extremal model had rank profile `D = [1, 6, 15, 10, 0, 0, 0]` and
  boundary rank profile `[0, 0, 0, 10, 10, 0, 0]`, reinforcing that the
  target is the half-cube Harper boundary case rather than a false local
  rank inequality.

Iteration 8 tool/proof notes:

- Re-ran an independent Python exhaustive downset generator through `n = 5`
  using the exact one-step upper external boundary. The half-downset counts
  and minimum boundary sizes were:
  `n=1: (1,1)`, `n=2: (2,2)`, `n=3: (4,3)`, `n=4: (24,6)`,
  `n=5: (621,10)`, matching `Nat.choose n (n / 2)` in each case.
  This corrects the earlier iteration-5 note that reported `14` for `n=5`;
  the exact minimum is `10`.
- Checked the tempting normalized-density route from the local LYM recurrence.
  It is insufficient by itself: as a relaxed rank-profile optimization it
  allows fractional monotone profiles, for example at `n=4` a profile with
  densities `[1, 1/2, 1/2, 1/2, 0]`, whose local-constraint boundary lower
  bound is below `Nat.choose 4 2`. Such profiles are not actual downsets, so
  the missing ingredient remains a structural Harper/SCD/Kruskal-Katona
  argument, not another adjacent-rank LYM rearrangement.
- Searched the local checkout again for Harper, Boolean vertex-isoperimetry,
  and symmetric-chain-decomposition APIs. No packaged theorem was found. No
  new external source was used beyond the standing Raty Harper provenance
  recorded above.

Round 008 `_harper` target notes:

- Re-ran an independent Python exhaustive downset generator through `n = 6`
  using the exact one-step upper external boundary in the Lean statement. The
  half-downset counts and minimum boundary sizes were:
  `n=1: (1,1)`, `n=2: (2,2)`, `n=3: (4,3)`, `n=4: (24,6)`,
  `n=5: (621,10)`, `n=6: (492288,20)`, matching
  `Nat.choose n (n / 2)` in each case.
- Added the exact requested declaration
  `boolean_half_downset_upperBoundary_card_ge_middle_harper`. It currently
  delegates to the existing
  `boolean_half_downset_upperBoundary_card_ge_middle`, so the Lean target is
  present and typechecks, but the real proof blocker remains the `sorry` in
  the underlying Harper/SCD half-downset boundary lemma.
- No new external web/literature source was used in this round.

Iteration 2 of round 008 Lean progress:

- Re-read the supplied context bundle and math-tools report, then searched the
  local mathlib checkout for Harper, Boolean vertex-isoperimetry,
  symmetric-chain, graded-poset Sperner, Ahlswede-Zhang, and Kleitman APIs.
  No packaged Harper/SCD boundary theorem was found. The external theorem
  provenance relied on remains Stephen Raty, "Harper's Theorem",
  arXiv:1806.11061, already recorded above.
- Added and verified
  `boolean_not_mem_subset_upperClosure_upperBoundary`: if `∅ ∈ D`, every set
  outside `D` lies in the upward closure of the one-step upper external
  boundary.
- Added and verified `boolean_half_downset_compl_card`: for positive `n`, the
  complement of a half-sized family also has cardinal `2 ^ (n - 1)`.
- Added and verified
  `boolean_half_downset_compl_subset_upperClosure_upperBoundary`, combining
  the previous two first-exit facts for half-sized downsets.
- The remaining Lean blocker is unchanged: convert the half-sized complement
  being covered by the upward closure of the boundary into the sharp Harper
  cardinal lower bound
  `Nat.choose n (n / 2) ≤ |∂⁺D \ D|`.

Iteration 3 of round 008 Lean progress:

- Re-read the supplied context bundle and math-tools report before editing.
  No new web/literature source was used; the standing external provenance
  remains Stephen Raty, "Harper's Theorem", arXiv:1806.11061.
- Re-searched the local mathlib/project checkout for Harper,
  vertex-isoperimetry, symmetric-chain decomposition, simplicial order, and
  hypercube boundary APIs. No packaged theorem stronger than the existing
  LYM/Kruskal-Katona/Harris-Kleitman/Ahlswede-Zhang tools was found.
- Added and verified
  `boolean_upperBoundary_card_eq_sum_slice_card`, rewriting the exact one-step
  upper external boundary cardinal as the sum of its rank-slice cardinalities
  via mathlib's `Finset.sum_card_slice`.
- The active Lean blocker is now explicitly the slice-sum Harper/SCD lower
  bound:
  `Nat.choose n (n / 2) ≤ ∑ k ∈ Finset.Iic n, |B # k|`, where `B` is the
  one-step upper external boundary of the half-sized downset.

Iteration 4 of round 008 Lean progress:

- Re-read the supplied context bundle and math-tools report before editing.
  No new web/literature source was used; the standing external provenance
  remains Stephen Raty, "Harper's Theorem", arXiv:1806.11061.
- Rechecked the local mathlib APIs around LYM, Harris-Kleitman,
  Ahlswede-Zhang, and Kruskal-Katona. These provide local shadow, correlation,
  and compression facts but still no packaged Harper/SCD vertex-isoperimetric
  theorem for the Boolean cube.
- Added and verified `boolean_upperBoundary_subset_compl`: the one-step upper
  external boundary is contained in the complement of `D`.
- Added and verified `boolean_half_downset_upperBoundary_card_le_half`: in the
  half-sized case the same boundary has cardinality at most `2 ^ (n - 1)`.
- The active blocker remains the sharp lower bound, not a set-definition issue:
  prove a Harper/SCD cutset theorem implying
  `Nat.choose n (n / 2) ≤ |B|` for the exact boundary `B`.

Iteration 5 of round 008 Lean/tool progress:

- Re-read the required context bundle and math-tools report before editing.
  No new web/literature source was used; the standing external provenance
  remains Stephen Raty, "Harper's Theorem", arXiv:1806.11061.
- Re-ran a Python exhaustive check over all half-sized downsets for
  `n = 1,2,3,4`. The minimum exact upper external boundary sizes were
  `1,2,3,6`, matching `Nat.choose n (n / 2)`.
- Searched the local mathlib checkout again for Harper, Boolean
  vertex-isoperimetry, symmetric-chain decomposition, and chain partition
  APIs. No packaged Harper/SCD theorem was found; available APIs remain
  LYM/Sperner, shadow, Kruskal-Katona, Harris-Kleitman, and Ahlswede-Zhang.
- Added and verified
  `boolean_half_downset_upperBoundary_card_ge_middle_of_upset_boundary`.
  This reduces the target to the equivalent upset-boundary form of Harper:
  if an upset `C` has cardinal `2 ^ (n - 1)`, then its lower one-step
  vertex boundary inside `C` has cardinal at least `Nat.choose n (n / 2)`.
  The complement of a downset is exactly such an upset, and its boundary
  rewrites to the target boundary.
- The remaining blocker is exactly this Harper/SCD upset-boundary theorem,
  not the boundary/complement reduction. A weaker arbitrary upper-closure
  cover principle would be false, e.g. a singleton generator can cover a
  dictator half-cube.

Iteration 6 of round 008 Lean progress:

- Re-read the required context bundle and math-tools report before editing.
  No new web/literature source was used; the standing external provenance
  remains Stephen Raty, "Harper's Theorem", arXiv:1806.11061.
- Added and verified
  `boolean_compl_upset_boundary_eq_upperBoundary`, extracting the definitional
  rewrite between the lower one-step boundary of the complement upset and the
  upper one-step external boundary of the original downset.
- The verifier
  `lake env lean FormalConjectures/ErdosProblems/1.lean` passes. The active
  target still depends on the unformalized Harper/SCD half-cube cutset lower
  bound, now isolated from complement/upset boundary bookkeeping.

Round 009 upset-boundary target notes:

- Re-read the supplied `context_bundle.md` and `math_tools_report.md` before
  editing. No new web/literature source was used; the standing external
  provenance remains Stephen Raty, "Harper's Theorem", arXiv:1806.11061.
- Ran a Python finite check for the exact current upset statement. Exhaustive
  enumeration over all half-sized upsets for `n = 1,2,3,4` found minimum
  lower one-step boundary sizes `1,2,3,6`, matching
  `Nat.choose n (n / 2)`. Dictator-style samples for `n = 5,6` had boundary
  sizes `16,32`, above the corresponding middle-layer sizes `10,20`.
- Re-searched local Mathlib/project APIs for Harper, Boolean
  vertex-isoperimetry, symmetric-chain decomposition, chain decompositions,
  Dilworth/Mirsky-style machinery, Menger/min-cut statements, and graded-poset
  cutset results. No packaged theorem was found. Available local tools remain
  LYM/Sperner, shadow APIs, Harris-Kleitman, Ahlswede-Zhang, and
  Kruskal-Katona.
- The current target is mathematically the lower-boundary form of the same
  Harper/SCD vertex-cut theorem: the one-step lower boundary of a half-sized
  upset is a vertex cut separating `∅` from `univ` in the directed Boolean
  lattice, and a symmetric-chain/min-cut theorem would give the
  central-binomial lower bound.

Iteration 8 round 009 Lean/tool progress:

- Re-read the required `context_bundle.md` and `math_tools_report.md` before
  editing. No new web/literature source was used; the standing external
  provenance remains Stephen Raty, "Harper's Theorem", arXiv:1806.11061.
- Finite-falsified a tempting abstraction: an arbitrary family `B` whose lower
  and upper closures each cover at least half the Boolean cube need not have
  middle-layer size. For `n = 2`, the singleton family `B = {{0}}` has both
  closure sizes `2 = 2^(2-1)` but `|B| = 1 < Nat.choose 2 1 = 2`.
  Therefore the remaining separator theorem must use the fact that `B` is the
  one-step boundary of a half-upset, not just a two-sided closure cover.
- Added and verified
  `boolean_half_upset_compl_subset_lowerClosure_boundary`, the complement-side
  first-entry lemma: every set outside a half-sized upset lies below a member
  of the same one-step lower boundary. This pairs with the existing upper
  closure lemma and isolates the remaining proof as a genuine Harper/SCD
  two-sided separator lower bound.

Round 009 upset-boundary target notes:

- Re-read the required context bundle and math-tools report before editing.
  No new web/literature source was used; the standing external provenance
  remains Stephen Raty, "Harper's Theorem", arXiv:1806.11061.
- Searched the local mathlib checkout again for Harper, Boolean
  vertex-isoperimetry, symmetric-chain decomposition, chain partition,
  Sperner/LYM, Kruskal-Katona, Harris-Kleitman, and Ahlswede-Zhang APIs. No
  packaged Harper/SCD cutset theorem was found.
- Ran a quick Python sanity probe for the exact upset boundary on standard
  extremal families (dictators and upper rank tails) for `n = 1..8`. Dictators
  have boundary size `2^(n-1)`, while balanced upper-half examples match the
  expected middle layer when they have exact half size. This did not reveal a
  counterexample and supports the existing diagnosis that the missing step is
  a genuine Harper/SCD theorem.
- Added and verified
  `boolean_half_upset_subset_upperClosure_boundary`: every member of a
  half-sized upset lies above a member of its one-step lower external
  boundary. This is the upset-side chain-crossing fact needed for a symmetric
  chain proof.

Iteration 6 of round 009 Lean progress:

- Re-read the required context bundle and math-tools report before editing.
  No new web/literature source was used; the standing external provenance
  remains Stephen Raty, "Harper's Theorem", arXiv:1806.11061.
- Rechecked local mathlib set-family APIs. The available imported tools still
  cover LYM/Sperner, shadows, Kruskal-Katona, Harris-Kleitman, and
  Ahlswede-Zhang, but no packaged Boolean-cube Harper/SCD cutset theorem was
  found.
- Added and verified `boolean_upset_boundary_card_eq_sum_slice_card`,
  rewriting the exact lower one-step boundary of an upset as the sum of its
  rank slices via `Finset.sum_card_slice`.
- Added and verified
  `boolean_half_upset_boundary_card_ge_middle_of_slice_sum`, reducing the
  current target to the sharp slice-sum lower bound
  `Nat.choose n (n / 2) <= ∑ k, |B # k|` for the upset boundary `B`.
- The remaining blocker is not boundary-definition bookkeeping: it is still
  the Harper/SCD/compression theorem proving that slice-sum lower bound for
  every half-sized upset.
- The remaining blocker is still the sharp SCD/Harper counting step: from
  each symmetric chain crossing the half-sized upset, choose one first-entry
  boundary point, and use the central-binomial number of chains to prove
  `Nat.choose n (n / 2) ≤ |B|`.

Round 009 iteration 3 Lean/tool progress:

- Re-read the required context bundle and math-tools report before editing.
  No new web/literature source was used; the standing external provenance
  remains Stephen Raty, "Harper's Theorem", arXiv:1806.11061.
- Rechecked the local Mathlib set-family APIs. Kruskal-Katona is available,
  including `Finset.kruskal_katona_lovasz_form`, but the available statement
  controls fixed-rank shadows and does not by itself supply the global
  half-upset vertex-boundary lower bound.
- Ran a small Python probe for `n = 1,2,3,4` on the equivalent half-upset
  boundary statement. The minimum lower-boundary sizes were `1,2,3,6`,
  matching `Nat.choose n (n / 2)`. The extremal rank profiles again confirm
  that the missing ingredient is a Harper/SCD/compression argument rather than
  a local rank-density rearrangement.
- Added and verified `boolean_upset_boundary_exists_between`: if `a ∉ C`,
  `b ∈ C`, and `a ⊆ b`, then some `t` with `a ⊆ t ⊆ b` lies in the exact
  one-step lower boundary used by
  `boolean_half_upset_boundary_card_ge_middle`. This formalizes the first-entry
  chain-crossing step needed by a future symmetric-chain decomposition proof.

Iteration 7 of round 008 Lean/tool progress:

- Re-read the required context bundle and math-tools report before editing.
  No new web/literature source was used; the standing external provenance
  remains Stephen Raty, "Harper's Theorem", arXiv:1806.11061.
- Rechecked local Mathlib for Harper, Boolean vertex-isoperimetry, symmetric
  chain decomposition, and simplicial-order APIs. No packaged theorem was
  found beyond LYM/Sperner, shadows, Kruskal-Katona, Harris-Kleitman, and
  Ahlswede-Zhang.
- Ran a finite Python obstruction check for the tempting Sperner shortcut:
  with `n = 3` and downset `D = {∅, {0}}`, the exact one-step upper external
  boundary is `{ {1}, {2}, {0,1}, {0,2} }`, which contains comparable pairs
  such as `{2} ⊂ {0,2}`. Thus the target boundary is not generally an
  antichain, and Sperner/LYM on the boundary alone cannot prove the middle
  binomial lower bound.
- Refactored the remaining `sorry` in
  `boolean_half_downset_upperBoundary_card_ge_middle` so it is precisely the
  equivalent half-sized upset lower-bound form:
  for every half-sized upset `C`, the set of `t ∈ C` with an immediate
  predecessor outside `C` has cardinal at least `Nat.choose n (n / 2)`.

Round 009 iteration 2 Lean/tool progress:

- Re-read the required context bundle and math-tools report before editing.
  No new web/literature source was used; the standing external provenance
  remains Stephen Raty, "Harper's Theorem", arXiv:1806.11061.
- Rechecked local Mathlib for Harper, Boolean vertex-isoperimetry,
  symmetric-chain decomposition, chain partition, LYM/shadow, and
  Kruskal-Katona APIs. No packaged Harper/SCD theorem was found.
- Ran a Python exhaustive check over all half-sized upsets for `n = 1,2,3,4`.
  The minimum exact lower one-step boundary sizes were `1,2,3,6`, matching
  `Nat.choose n (n / 2)` in each checked dimension.
- Added and verified upset-side setup lemmas:
  `boolean_half_upset_compl_card`, `boolean_half_upset_univ_mem`,
  `boolean_half_upset_empty_not_mem`,
  `boolean_half_upset_boundary_nonempty`, and
  `boolean_half_upset_boundary_card_pos`.
- The remaining blocker is the genuine sharp Harper/SCD cutset theorem for a
  half-sized upset. The local facts now prove nonemptiness and positivity of
  the target boundary, but not the central-binomial lower bound.

Iteration 8 of round 008 Lean/tool progress:

- Re-read the required context bundle and math-tools report before local work.
  No new web/literature source was used; the standing external provenance
  remains Stephen Raty, "Harper's Theorem", arXiv:1806.11061, as supplied by
  the proof-lab context.
- Re-ran the required verifier baseline:
  `lake env lean FormalConjectures/ErdosProblems/1.lean` passes, with the
  expected `sorry` warning at the isolated Harper/SCD cutset gap and the
  unrelated open-problem statements later in the file.
- Rechecked local Mathlib APIs around LYM, Ahlswede-Zhang,
  Kruskal-Katona, shadows, double-counting, and permutation cardinality. No
  packaged Boolean vertex-isoperimetric or symmetric-chain-decomposition
  theorem is available in the local checkout.
- Re-ran exhaustive Python enumeration of all half-sized downsets for
  `n = 1,2,3,4`. The minimum exact one-step upper external boundary sizes
  were again `1,2,3,6`, matching `Nat.choose n (n / 2)`.
- Tested the tempting maximal-chain/Lubell shortcut. It proves only that
  every maximal chain crosses the boundary; by itself this gives a weighted
  Lubell lower bound, but it does not imply the cardinal lower bound because
  boundary elements at different ranks have very different chain weights.
  Closing the target still requires a genuine Harper/SCD cutset theorem or a
  formal compression argument strong enough to recover the middle-binomial
  cardinal bound.

Round 009 iteration 5 Lean/tool progress:

- Re-read the required context bundle and math-tools report before editing.
  No new web lookup was used. External/source provenance relied on in this
  iteration is local Mathlib documentation for LYM/Kruskal-Katona/Ahlswede-
  Zhang and the already-recorded Harper source, Stephen Raty, "Harper's
  Theorem", arXiv:1806.11061.
- Rechecked local Mathlib set-family files. Available APIs include
  `Finset.local_lubell_yamamoto_meshalkin_inequality_mul`,
  `IsAntichain.sperner`, `Finset.kruskal_katona_lovasz_form`,
  Harris-Kleitman, and Ahlswede-Zhang identities. No packaged Boolean
  vertex-isoperimetric or symmetric-chain-decomposition cutset theorem was
  found.
- Ran a Python exhaustive/antichain enumeration check for all half-sized
  upsets through `n = 5`. The minimum exact lower one-step boundary sizes were
  `1, 2, 3, 6, 10`, matching `Nat.choose n (n / 2)`. This again supports the
  statement and leaves the formal blocker at the Harper/SCD counting theorem.
- Added the verified slice identity
  `boolean_upset_boundary_slice_eq_compl_upShadow_slice_inter`, identifying
  the rank `k + 1` part of the upset boundary as the upset slice intersected
  with the upper shadow of the complement's rank `k` slice.
