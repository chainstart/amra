# Six-hour technical campaign: final report

Date: 2026-08-02

Campaign window: 10:34:51--16:34:51 HKT

Repository baseline: `669bbad1908e7ab7d8382a8b508e67757006e90c`

Final status: **ALL FOUR ORIGINAL PROBLEMS REMAIN OPEN**

This campaign did not produce a proof or disproof of any of the four
public problems.  It did produce four independently audited theorem or
counter-theorem packages that materially narrow the live proof space and
are suitable as rigorous sections of a research manuscript.  In
particular, the word *counterfamily* below always refers to an intermediate
bridge, never to a public-problem counterexample.

## Executive disposition

| Lane | Strongest six-hour outcome | Independent disposition | Original problem |
|---|---|---|---|
| OPG-1757 | Universal second-active positivity; third-active positivity in 31 low coefficients in their bulk ranges, fixed top bands, and the eventual logarithmic bulk `241 log(s) <= d <= 2s-4` | **PASS AFTER QUANTIFIER REPAIR** | **OPEN** |
| Erdős #1083 | Four signed-switch barriers: cyclotomic `C^2`, finite shadows and aperiodic escape, transverse `Phi_6` fibre rigidity, and binary-box Hamming rigidity below exponent `5/9` | **PASS AFTER THREE MINIMAL REPAIRS** | **OPEN** |
| Erdős #776 | Five positive rank-five chambers; an actual dyadic infinite counterfamily to the sixth fixed-rank bridge; exact rank-six recovery on that family | **PASS** | **OPEN** |
| Erdős #809 | Parity-sharp square-root degree-spread theorem in maximum-witness B-opposite, sharp cyclic graphs with `L_4(2)`, and a reserve-paid repeated-colour stress test | **PASS AFTER ONE LOCAL EXPOSITORY REPAIR** | **OPEN** |

The exact audit decisions, repairs, source hashes, and independent counts
are frozen in `BLIND_AUDIT_RESULTS.md`.  The cross-lane summary vocabulary
is controlled by `FINAL_CLAIM_LEDGER.md`; the four detailed claim ledgers
remain authoritative for intermediate claims.

## 1. OPG-1757

### Admitted advance

The second-active Newton row is now universally positive for both
parities.  For the third-active row, the exact reduction to two transport
inequalities is independently audited.  Each transport is positive in its
first 31 coefficients throughout the stated nonnegative-homogenization
bulk range and in its fixed reverse top band.  Moreover, there is an
absolute ineffective `S` such that, for `s >= S`, both transports are
positive on

\[
  241\log s\le d\le2s-4.
\]

Thus the only eventual transport gap is

\[
  31\le d<241\log s.
\]

In the analyzed odd `u_2`-layer decomposition, an explicit negative layer
coefficient at every fixed merge depth rules out that termwise-positive
tail architecture; it does not rule out other fixed-depth recurrences.
That is a rigorous obstruction to one proof architecture, not to the
transport itself.

### Publication value and remaining gate

The universal second-active theorem, exact third-active reduction, and
logarithmic-boundary analysis form a coherent base-four Newton coefficient
paper section: exact identities, all-parameter positivity, asymptotic
localization, and a method obstruction are all present.  Closing the
logarithmic layer would prove the two third-active transports and hence the
third-active row.  A proof of OPG-1757 would still require control of later
active rows/the full coefficient mechanism and a transfer to arbitrary
hosts.

## 2. Erdős #1083

### Admitted advance

Four model-level barriers survived blind reconstruction.

1. For `1 <= C < S`, a signed regularizer cannot make a power-large
   same-line cyclotomic family positive: the admissible scale set has size
   at most `1+2 sum_(r=2)^C phi(r)<=C^2`.  At the frozen endpoint
   `C=t^(1/18+o(1))`, this is `t^(1/9+o(1))`.
2. Any finite-quotient tiling centre has an exact-mass nonnegative shadow
   preserving external divisibility, while `1+x+x^4` supplies an
   aperiodic escape.  This sharply identifies the scope of the shadow
   method.
3. A full independent transverse `Phi_6` switch cube with nonnegative
   quotient projection has fibre mass at least `2^k`.
4. Even with signed residuals, the calibrated transverse binary-box exact
   model `k=14 ell`, `C=2^ell`, `S=2^(14 ell)`, `t=2^(18 ell)` has endpoint
   exponent `(7/9)H_2(1/7)=0.460189938897...<5/9`; within that same model,
   a common `X -> 3X` switch forces `C >= S`.

The necessary `C>0` hypothesis is explicit: at `C=0`, the zero quotient
would make an arbitrary ratio family vacuous.

### Publication value and remaining gate

These results support two tightly scoped algebraic sections: positive
multiples/finite shadows and transverse switch-cube rigidity.  They rule
out several natural exact-block constructions at the target exponent.
They do not improve the inherited `N^(3/5-o(1))` public-problem distance
exponent.
They do not yet control arbitrary aperiodic centres, arbitrary signed
residual divisors, the common-`X` scalar-copy interface, or extraction of a
stable exact block from the original near-extremal geometry.

## 3. Erdős #776

### Admitted advance

Five of six conditional one-promotion rank-five chambers have uniform
positive deficit.  The last chamber is false on the actual dyadic lattice:

\[
 K=6,\quad r=10,\quad h=224\,2^s,\quad
 q=(448\,2^s-2)/5,\quad s\equiv2\pmod4,
\]

and for every such `s >= 14`,

\[
 \gamma_5=4{,}302{,}695-6q<0.
\]

The whole family becomes positive at rank six; after the nonstable first
case, its stable formula is

\[
 \gamma_6=9{,}256{,}181{,}220{,}279+104q>0.
\]

This simultaneously kills the proposed fixed rank-five bridge and shows
how a one-step adaptive repair succeeds on the same obstruction.  It must
not be confused with the separate inherited family that refutes a global
fixed-rank-six theorem.

### Publication value and remaining gate

The exact dyadic counterfamily, five complementary chamber theorems, and
rank-six self-repair form a strong corrective/methodological package: they
replace a plausible but false bridge by a precisely localized obstruction.
To reach #776 itself, one still needs an adaptive seed theorem on the
complementary no-borrow lattice and positive-side cap transitions, followed
by the rank-42 capacity implication.

## 4. Erdős #809

### Admitted advance

For a maximum-degree witness in the B-opposite branch, with
`g=Delta(G)-delta(G)`, pure pairwise missing-edge accounting proves

\[
 n\le
 \begin{cases}
  2g^2-2g-6,& n\text{ even},\\
  2g^2-2g-3,& n\text{ odd}.
 \end{cases}
\]

The constants are graph-level sharp: explicit cyclic two-clique graphs
attain both bounds and satisfy `L_4(2)` for every `g>=5`.  A second
constructional stress test recolours the sharp graphs so that a zero-shore
pair has multiplicity `g` and actual defect `D_B=g` while every `C_7`
remains rainbow.  Its missing-star reserve nevertheless has size at least `g`, so
the example lies in the reserve-paid branch rather than furnishing a hard
counterexample.

### Publication value and remaining gate

The parity-sharp extremal theorem, equality constructions, exact path
templates, and reserve stress test are the most self-contained manuscript
unit from this campaign.  They isolate a genuine square-root degree-spread
barrier.  The full #809 problem still contains Branch A, B-same, the
surviving large-spread B-opposite profiles, and other BCM witness branches.

## Audit integrity

The blind phase used an author swap:

- root independently reconstructed OPG-1757;
- the OPG author reconstructed #776;
- the #776 author reconstructed #1083;
- the #1083 author reconstructed #809.

The four outcomes were one unqualified pass and three passes after small,
fully documented repairs.  None of the repairs changes a principal
constant or enlarges a theorem.  The meta-audit found one stale cross-lane
sentence and synchronized it; it found no mathematical contradiction among
the four packages.  Every public-problem row remains `OPEN / NOT CLAIMED`.

At 16:14 the #1083 author supplied an additional full-Euclidean interval
multirow construction with an executable author check.  Because no
author-swapped blind audit could be completed before the 16:15 admission
deadline, it is retained only as `NEW / AUTHOR-VERIFIED / NOT
BLIND-AUDITED / NOT ADMITTED TO THE FINAL CLAIM LEDGER`.  It is not used in
any disposition or publication-readiness ranking in this report.

## Reproduction and repository hygiene

The final all-campaign regression ran from 16:15:53 to 16:26:21 HKT:

    PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
      data/research_open/q1_six_hour_campaign_2026-08-02

It returned `151 passed in 613.80s (0:10:13)`.  The total includes the four
author-verification tests for the explicitly unadmitted late #1083 note;
their success does not promote that note into the blind-audited ledger.

After regression, 120 generated `.pyc` files and four empty
`__pycache__` directories were removed.  Per-file no-index diff checks
reported no trailing whitespace.  All Markdown display delimiters were
balanced, and scans found no known malformed math escapes, conflict
markers, or nonprinting control characters.  The campaign freezes with
180 files (92 Markdown and 87 Python); repository status contains only the
new campaign directory.

The campaign directory is additive relative to baseline `669bbad`; no
pre-existing source file is modified.  No commit or push is part of this
campaign.

## Bottom line

The six-hour objective of proving or refuting the four public propositions
was not attained.  The phase objective was attained in the narrower and
honest sense of producing substantial, independently audited manuscript
components: two all-parameter/asymptotic coefficient theorems, four
algebraic rigidity barriers, one exact infinite bridge counterfamily with
adaptive recovery, and one parity-sharp extremal graph theorem with sharp
constructions.  A submission-ready top-quartile paper would still require
a unified narrative, external literature positioning, and closure of at
least one remaining global interface; the present material is rigorous
stage work rather than a claim of a complete solution paper.
