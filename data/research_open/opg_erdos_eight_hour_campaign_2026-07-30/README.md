# OPG-1757 and Erdős #1083 eight-hour proof campaign

Date: 2026-07-30

This campaign has two proof targets:

1. **OPG-1757.**  Prove pairwise negative correlation for the uniform
   forest measure, with the immediate technical target being a uniform
   Hall/injection theorem for the first unresolved complete-split
   coefficient layer.
2. **Erdős #1083.**  Improve the three-dimensional lower bound
   \(f_3(n)\ge n^{3/5-o(1)}\), with the immediate technical target being
   a genuinely joint correlation or synchronization theorem that gives a
   fixed positive exponent gain.

The work is proof-first.  Finite searches are used to falsify proposed
lemmas, identify minimal obstructions, and produce reproducible
certificates; they are never treated as proofs of unbounded statements.

The main end-of-session milestones are:

- ordinary OPG symbols and strict normalized Newton inequalities through
  rank eight, together with an independently audited all-rank theorem
  \(\deg_d\beta_{d,r}=3r\) and an alternating leading sign;
- exact all-rank falling-triangle degrees and forced factors, plus an
  independently audited proof that every long-recurrence band has exact
  degree \(3q+2\) and positive leading coefficient;
- exact positivity of the first eight complete long-recurrence bands
  \(\gamma_0,\ldots,\gamma_7\) on all admissible depths;
- a finite exact decision procedure for the full admissible-domain
  positivity of every individually fixed long-recurrence band (without
  claiming that every band returns a positive answer);
- explicit positive Newton windows at both ends of the support;
- a forced cross-plane distance-codegree theorem and a subsequent
  matching-or-single-plane-hub dichotomy for Erdős #1083;
- a Euclidean reverse-circle incidence theorem excluding the hub for
  every \(\kappa<1/5\), hence forcing
  \(t^{1/5-\varepsilon-o(1)}\) rich matchings for every fixed
  \(\varepsilon>0\); surviving hubs with \(\kappa<1/3\) have
  incidence-active circle-axis multiplicity, after a weighted dyadic
  circle-incidence refinement,
  \(\mu\ge t^{(5-15\kappa)/2-o(1)}\);
- an independently audited sharp barrier showing that one such
  circle-axis chart is a Lenz-type degeneracy: its exact saturation
  family, for arbitrarily large even \(\mu\), may carry
  \(n\mu\) cross representations while the whole chart has only
  \(O(n+\mu)\) distances, so any further hub attack must synchronize
  many incompatible charts;
- an independently audited two-chart barrier showing that even any
  fixed number of concentric common-axis charts with different radii
  can retain only linear distance growth; the known two-circle
  classification then gives expansion for every nonaligned pair,
  because the other general exception (perpendicular circles) is
  excluded by the retained off-axis chart geometry;
- a high-rich concentration corollary: for every fixed \(\eta>0\),
  all retained active circles with at least \(t^{9/4+\eta}\) source
  incidences are concentric, and their total weighted mass is at most
  \(MQ=t^{4+o(1)}=o(LH)\) for every fixed \(\kappa<1\); hence the
  critical hub mass is forced onto many less-rich circles;
- an exact moderate-rich exponent-ledger barrier: throughout
  \(1/5\le\kappa<1/3\), the assignment
  \[
  (a,b,m)=\left(1-\kappa,\frac{7+11\kappa}{2},
  \frac{5-15\kappa}{2}\right)
  \]
  simultaneously saturates the hub mass, triple capacity, weighted
  point--circle term, and multiplicity threshold while respecting all
  current pairwise two-circle and plane-capacity constraints.  Thus a
  further proof needs genuinely Euclidean compatibility information,
  not another recombination of the saved exponent inequalities;
- weighted ruled/number-field terminal theorems; and
- prime-cyclotomic escape even for height-dependent partial angular
  fibres, extended from rational data to almost every prime over a fixed
  real number field.

The full OPG conjecture and an unconditional improvement of the
three-dimensional \(3/5\) distinct-distance exponent remain open.
In particular, the campaign's Euclidean matching and circle-axis conclusions
are structural refinements and do not themselves improve that exponent.

Navigation:

- [`PLAN.md`](PLAN.md): time budget, kill criteria, and milestone contracts;
- `opg1757/`: partition-aware Hall/injection line;
- `erdos1083/geometric/`: joint-correlation and synchronization line;
- `erdos1083/algebraic/`: varying-field inverse-symmetrized container line;
- [`LITERATURE_AND_NOVELTY_AUDIT.md`](LITERATURE_AND_NOVELTY_AUDIT.md):
  primary-source scope and priority audit;
- `CLAIM_LEDGER.md`: final theorem/evidence/open-gap classification;
- `FINAL_REPORT.md`: final synthesis and publication assessment.

The directory is intentionally separate from the 2026-07-29 campaign so
that new claims can be audited without rewriting the earlier record.
