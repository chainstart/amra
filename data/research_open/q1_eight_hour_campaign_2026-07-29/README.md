# Eight-hour Q1 mathematics campaign

Date: 2026-07-29 (Asia/Hong_Kong)

## Objective

Advance three recent AMRA research lines far enough to decide whether any one of
them supports a genuinely original, independently checkable theorem of the
scope normally expected from a top-quartile mathematics paper:

1. OPG1757: a whole-graph, all-edge-pairs preservation theorem for uniform
   forest negative correlation;
2. KOU-21.137: minimum-order and complete order-128 classification beyond the
   previously public \(D_8\wr C_2\) counterexample;
3. Erdos #1083: an improvement to the recognized distinct-distance exponent,
   or a natural structural theorem with independent value.

## Acceptance gate

A result is not counted as a breakthrough unless all of the following hold:

- the statement is precise and unconditional;
- every branch of the proof is closed, or a finite computation has a
  fail-closed completeness argument;
- an independent verifier or adversarial audit reproduces the conclusion;
- current primary literature does not already contain the same theorem;
- the result changes a recognized mathematical boundary, rather than merely
  increasing a search range or recording solver telemetry.

## Time budget

- 00:00--00:30: freeze repository/resource state and proof contracts;
- 00:30--03:00: independent first attack on all three lines;
- 03:00--03:30: adversarial mid-session audit and stop/go decision;
- 03:30--06:45: concentrate on surviving lemmas and independent verification;
- 06:45--07:30: novelty and priority audit;
- 07:30--08:00: final synthesis and publication assessment.

## Repository boundary

The worktree was already dirty at campaign start. Existing modified and
untracked files are treated as user-owned. New work is isolated below this
directory or in separately named scripts/tests; no branch, commit, push, or
destructive cleanup is authorized by this campaign.

## Interim outcome map

| line | strongest closed result | unresolved boundary |
|---|---|---|
| KOU-21.137 | unrestricted prime-wreath closure criterion; finite seed classification; exact order-128 minimum and ten types; \(p=3\) order-\(3^8\) exclusion; all dimension-ten and dimension-eleven \(J^9=0\) algebra profiles excluded under closure; 582 dimension-twelve profiles reduced to eight inputs, three then excluded | authorized priority audit; odd-prime KOU case; closure analysis of the five remaining dimension-twelve contracts |
| OPG-1757 | fixed-page positivity through seven pages; general low coefficients; rooted-tree/Lagrange formula; base-4 Newton support; a necessary-and-sufficient boundary-partition criterion for universal outside stability; outside-stable saturated-\(K_4\) repair; three-transition, 350-chain complete injection on \(q=1,k=5\); exact \(q=2,k\le7\) Hall/rule audit | component-refining or external-partition-aware repair grammar with a termination/recovery invariant, or a uniform Hall theorem, plus image separation for arbitrary \(q,k\) |
| Erdős #1083 | no-go theorems for Laurent/divisor/fixed-field or explicitly normalized constructions; exhaustive finite tests; an exact determinant obstruction for one growing-degree unit family | varying-field, noncommensurable constructions with explicit height/regulator and popular-difference control |

The final synthesis is in [`FINAL_REPORT.md`](FINAL_REPORT.md), the
claim-by-claim scope firewall is in [`CLAIM_LEDGER.md`](CLAIM_LEDGER.md), and
the exact publication judgement is maintained in
[`PUBLICATION_READINESS.md`](PUBLICATION_READINESS.md).  Its current verdict
is deliberately conservative: KOU is a likely specialist manuscript after
priority clearance; OPG is a high-upside but incomplete proof programme; the
Erdős line has not improved the \(3/5\) exponent.

## Trust boundary

- “Proved” means a complete human argument or a fail-closed finite
  enumeration with an independently checkable ledger.
- Numerical nonnegativity, SAT timeouts, bounded searches and proposed
  injections are labelled as evidence, not theorems.
- The public \(D_8\wr C_2\) Lean example is treated as prior art.
- No claim of Chinese Academy of Sciences Zone-1 readiness is made before
  proof, priority and manuscript-scope gates are all cleared.
