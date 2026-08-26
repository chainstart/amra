# Final scope audit for the six-hour Erdos 451 continuation

Date: 2026-08-27

Verdict: **PASS for scope and internal consistency; decisive lemma open.**
This is an internal same-model audit, not the independent reconstruction
required for promotion.

## Claims reconstructed

1. The local convolution `tau_i` is a probability with positive support
   exactly the actual allowed residues `0,...,d_i-1`.
2. The integer triangular window has a nonnegative Fejer transform, and
   finite Fourier inversion gives the stated exact count with zero-word
   contribution `h/P`.
3. Strict domination of every nonzero frequency by the zero word gives a
   positive integer count for every center.  This implication is proved;
   the domination estimate is not.
4. For a width-one prime, Dirichlet-kernel factorization and shift Parseval
   eliminate its entire frequency fibre exactly.  Only the specific
   dilation by `p_0`, not arbitrary unit dilations, remains.
5. The AM-GM majorant has the stated nonnegative compact triangular dual,
   complete-period mean `1/L_G`, and sufficient factor-two prefix target.
6. The additive discrepancy `Q<=h/L_G+K^m` is sufficient after choosing a
   fixed window base `C>2K`; it is not asserted as a theorem.
7. The threshold `C>=2`, the undilated `O(log k)` prefix through `|ell|<k`,
   and the quotient-gap identities are proved with the stated scopes.
8. The continuous `d=1`, separated norm, subset-period, support-only sieve,
   and literal finite `B=0,C=2` failures are recorded only as scoped
   no-goes.  None is promoted to a counterexample to Erdos 451.

## Evidence classification

- Algebraic/Fourier identities and the small-prefix bounds are proved.
- Scanner rows and effective constants are finite diagnostics only.
- The decisive weighted joint tail is conditional/open.
- Same-model cross-agent reconstruction passed the bridge and its
  normalization, but `audit.json` correctly keeps independent reconstruction,
  statement match, dependency check, and novelty check unstarted/unchecked.
- No public-network novelty claim was made.

## Gate expectation

The campaign must remain in `survivor_deepening`.  Validation is expected to
fail only with `decisive lemma must identify what it closes`, because
`decisive_lemma.json` deliberately retains `closes=[]` until the weighted
joint-tail theorem is actually proved.  Weakening that gate would be a claim
inflation and is forbidden.

Final guarded validation unit
`openmath-task-20260827-030435-390265.scope` exited `1` with exactly that one
error and no others.  Guarded syntax checks parsed 36 Python files and 26
JSON files, and the five `amra-research-loop` package tests passed under
units `openmath-task-20260827-030429-390163.scope` and
`openmath-task-20260827-030429-390164.scope`.

Four final guarded replay checks also exited zero:

- M05 exact/ledger replay: `openmath-task-20260827-030701-391434.scope`;
- phase identities: `openmath-task-20260827-030701-391447.scope`, covering
  8,628 subset systems and 164,320 centered-threshold cases;
- finite Fejer identity: `openmath-task-20260827-030701-391466.scope`, with
  Parseval error below `1.8e-15`;
- M10 round-one witnesses: `openmath-task-20260827-030701-391486.scope`,
  checking 732 prime pairs and both recorded block counterexamples.

Final `g++ -std=c++20 -fsyntax-only` checks passed for all three GMP/C++
scanners under units `openmath-task-20260827-030818-392136.scope`,
`openmath-task-20260827-030818-392149.scope`, and
`openmath-task-20260827-030818-392135.scope`.
