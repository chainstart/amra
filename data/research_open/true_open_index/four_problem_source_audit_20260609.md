# Four Problem Source Audit - 2026-06-09

Audit date: 2026-06-09

Scope:

- `formal-conjectures-conjecture198a`
- `formal-conjectures-conjecture200`
- `formal-conjectures-conjecture327`
- `formal-conjectures-crystals-components-unique`

Purpose: verify original sources and whether each target should still be treated as a genuinely open mathematical problem.

## Executive Result

Only three of the four targets should remain in the true-open working set.

| problem_id | original source | current verdict | action |
| --- | --- | --- | --- |
| `formal-conjectures-conjecture198a` | WOWII / Graffiti.pc Conjecture 198a | still open candidate | retain |
| `formal-conjectures-conjecture200` | WOWII / Graffiti.pc Conjecture 200 | still open candidate | retain |
| `formal-conjectures-conjecture327` | WOWII / Graffiti.pc Conjecture 327 | resolved false by counterexample | remove from true-open set |
| `formal-conjectures-crystals-components-unique` | Abrate-Barbero-Cerruti-Murru, "The Biharmonic mean", Conjecture 4.5 | still open candidate | retain |

`formal-conjectures-conjecture327` is the important correction. The old local index and the original WOWII open page still list it as open, but the current upstream Formal Conjectures source marks it as `research solved` with a 12-vertex counterexample and points to a Lean formal counterexample proof.

## Sources Checked

Primary/local source files:

- `data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean`
- `data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture200.lean`
- `data/research_open/raw/formal_conjectures/FormalConjectures/WrittenOnTheWallII/GraphConjecture327.lean`
- `data/research_open/raw/formal_conjectures/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean`

External primary sources:

- WOWII main site: `http://cms.dt.uh.edu/faculty/delavinae/research/wowII/`
- WOWII open list: `http://cms.dt.uh.edu/faculty/delavinae/research/wowII/open.html`
- WOWII all list: `http://cms.dt.uh.edu/faculty/delavinae/research/wowII/all.html`
- WOWII resolved list: `http://cms.dt.uh.edu/faculty/delavinae/research/wowII/resolved.htm`
- WOWII true resolved list: `http://cms.dt.uh.edu/faculty/delavinae/research/wowII/resolvedT.htm`
- WOWII status legend: `http://cms.dt.uh.edu/faculty/delavinae/research/wowII/comments.htm`
- Formal Conjectures current main:
  - `https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/WrittenOnTheWallII/GraphConjecture198a.lean`
  - `https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/WrittenOnTheWallII/GraphConjecture200.lean`
  - `https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/WrittenOnTheWallII/GraphConjecture327.lean`
  - `https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/Arxiv/1601.03081/UniqueCrystalComponents.lean`
- Formal Conjectures proof for Conjecture 327 counterexample:
  - `https://github.com/mo271/formal-conjectures/blob/6e85aabe821e6ddf718d050a5bd8f19a48e4f2d9/FormalConjectures/WrittenOnTheWallII/GraphConjecture327.lean#L233`
- Biharmonic mean paper:
  - `https://arxiv.org/abs/1601.03081`
  - `https://imar.ro/journals/Mathematical_Reports/Pdfs/2016/4/5.pdf`

Targeted web queries were also run for exact statement fragments, declaration names, and proof/counterexample terms. No proof/counterexample was found for 198a, 200, or crystal component uniqueness. A counterexample/formal-proof record was found for 327 in the current Formal Conjectures ecosystem.

## Problem Details

### `formal-conjectures-conjecture198a`

Original source:

- WOWII / Graffiti.pc, Conjecture 198a.
- Original statement on WOWII open/all pages: if `G` is a simple connected graph with `n > 1` and `b(G) <= 2 + ecc_avg(G)`, then `G` has a Hamiltonian path.

Open-status evidence:

- WOWII `open.html`: entry appears as `O 198a`.
- WOWII `all.html`: entry appears as `O 198a`.
- WOWII `resolved.htm` and `resolvedT.htm`: no `198a` match. Note: Conjecture 198, a different statement using `ecc_avg(M)` for maximum-degree vertices, is listed as true; this must not be confused with 198a.
- Current Formal Conjectures main still marks 198a as `@[category research open, AMS 5]` and leaves the theorem body as `sorry`.
- Targeted web searches found no proof or counterexample.

Verdict: retain as a true-open candidate. Confidence: high, subject to the usual limitation that absence of a proof in search results is not an absolute proof of openness.

### `formal-conjectures-conjecture200`

Original source:

- WOWII / Graffiti.pc, Conjecture 200.
- Original statement on WOWII open/all pages: if `G` is a simple connected graph with `n > 1` and `tree(G) = CEIL[1 + lambda_avg(G)]`, then `G` has a Hamiltonian path.

Open-status evidence:

- WOWII `open.html`: entry appears as `O 200`.
- WOWII `all.html`: entry appears as `O 200`.
- WOWII `resolved.htm` and `resolvedT.htm`: no matching resolved Conjecture 200 entry.
- Current Formal Conjectures main still marks 200 as `@[category research open, AMS 5]` and leaves the theorem body as `sorry`.
- Targeted web searches found no proof or counterexample.

Verdict: retain as a true-open candidate. Confidence: high, subject to the same absence-of-evidence caveat.

### `formal-conjectures-conjecture327`

Original source:

- WOWII / Graffiti.pc, Conjecture 327.
- Original statement on WOWII open/all pages: if `G` is a simple connected graph with `n > 1` and `3 * gamma(G) = gamma_i(G)`, then `G` is well total dominated.

Open-status evidence from old source:

- WOWII `open.html`: entry appears as `O 327`.
- WOWII `all.html`: entry appears as `O 327`.
- WOWII `resolved.htm` and `resolvedT.htm`: no matching resolved Conjecture 327 entry.

Current contrary evidence:

- Current Google DeepMind Formal Conjectures main marks it as `@[category research solved, AMS 5, formal_proof ...]`.
- The current source says the conjecture is false and gives a 12-vertex counterexample.
- The referenced formal proof file proves `conjecture327_is_false`, exhibiting a connected graph with `3 * dominationNumber = indepDominationNumber` and `not IsWellTotallyDominated`.

Verdict: remove from true-open set. This is not an open proof target; if kept in AMRA, it should be a counterexample/formalization or source-reconciliation task only.

### `formal-conjectures-crystals-components-unique`

Original source:

- Marco Abrate, Stefano Barbero, Umberto Cerruti, Nadir Murru, "The Biharmonic mean", Mathematical Reports 18(68), no. 4 (2016), pp. 483-495; arXiv:1601.03081.
- Original conjecture in the conclusion: if `n = ab` is a crystal, then there is no other pair `c,d > 1`, different from `a,b`, with `n = cd` and `B(c,d)` an integer; equivalently, crystal components are unique.

Open-status evidence:

- The paper explicitly presents this as a conjecture and says that proof or counterexample does not follow easily.
- Current Formal Conjectures main marks it as `@[category research open, AMS 11 26]` and leaves the theorem body as `sorry`.
- Targeted web searches found no proof or counterexample. Search hits only returned the original paper, repository mirrors, OEIS citations, and institutional copies.

Verdict: retain as a true-open candidate. Confidence: medium-high. The problem is niche enough that a final literature audit should check MathSciNet/Zentralblatt/arXiv/Google Scholar before a publication claim, but no current proof or disproof was found in this audit.

## Updated Working Index

Retain for next open-problem work:

1. `formal-conjectures-conjecture198a`
2. `formal-conjectures-conjecture200`
3. `formal-conjectures-crystals-components-unique`

Exclude from open-problem work:

1. `formal-conjectures-conjecture327` - resolved false by counterexample.

## Caveat

For 198a, 200, and crystal component uniqueness, this audit supports "still open candidate" rather than a mathematically absolute proof that no one has solved them. The evidence is strong enough for AMRA target selection, but any paper or public claim of first proof must repeat the search in bibliographic databases and ideally check with domain experts.
