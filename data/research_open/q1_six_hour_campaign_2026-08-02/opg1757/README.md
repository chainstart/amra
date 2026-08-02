# OPG-1757 six-hour technical campaign (2026-08-02)

This directory is the isolated OPG-1757 lane of the 2026-08-02
campaign.  Its primary target is to prove or refute the original
OPG-1757 statement.  The first mandatory gate is an independent audit of
the previous campaign's polynomial-width theorem candidate.  After that
gate, the lane attacks the full base-four Newton positivity conjecture or
extracts the strongest rigorous all-parameter subtheorem available.

Status vocabulary is literal:

- `PROVED`: a universal written argument has been checked dependency by
  dependency;
- `CONDITIONAL`: the implication is proved but a named input remains
  unproved;
- `FINITE`: exact computation on a stated finite range only;
- `OPEN`: neither proof nor counterexample is known.

Current files:

- `BASELINE_FREEZE.md`: immutable source hashes and replayed evidence;
- `CLAIM_LEDGER.md`: claim/status firewall;
- `RESEARCH_LOG.md`: chronological technical log;
- `POLYNOMIAL_WINDOW_INDEPENDENT_AUDIT.md`: six-gate independent audit;
- `POWER_EIGHTH_WINDOW_THEOREM.md`: new all-parameter eighth-root window;
- `ORIGINAL_PROBLEM_FIREWALL.md`: exact relation to OPG-1757;
- `verify_power_eighth_window.py`: independent falsification certificate.
- `ODD_SECOND_ACTIVE_INDEPENDENT_AUDIT.md`: universal odd second-row proof;
- `Q7_FULL_NEWTON_FINITE_THEOREM.md`: exact next full deficit layer;
- `EVEN_SECOND_ACTIVE_PARTIAL_THEOREM.md`: two uniform even-row boundary
  bands and an exact obstruction to fixed-depth layer induction
  (now superseded as the endpoint of the even attack);
- `EVEN_SECOND_ACTIVE_UNIVERSAL_THEOREM.md`: universal even-row proof and
  parity-free second-active corollary;
- `EVEN_SECOND_ACTIVE_UNIVERSAL_INDEPENDENT_AUDIT.md`: independent
  reconstruction of the moving top-degree induction and focused audit;
- `verify_even_second_active_partial.py`: exact symbolic certificate for
  31 low columns, six top columns, and the layer obstruction;
- `verify_even_second_active_universal.py`: four-layer recurrence and
  tail-induction certificate;
- `even_second_active_workbench.py`: finite recurrence route-selection
  probe, explicitly firewalled from proof status.
- `THIRD_ACTIVE_EXACT_REDUCTION.md`: exact parity-separated
  `B6/B4/B2` and `B7/B5/B3` reductions, with the first universal sign
  gate isolated;
- `third_active_workbench.py`: exact reconstruction and finite
  falsification of the candidate third-row transports.
- `THIRD_ACTIVE_TRANSPORT_TOP_BANDS.md`: all-parameter strict positivity
  of the complete eight-/ten-coefficient reverse boundary bands of the
  odd/even third-active transports;
- `third_active_transport_top_attack.py`: exact reverse-extraction and
  dominant-exponential ratio certificate for those transport bands.
- `THIRD_ACTIVE_TRANSPORT_LOW_COLUMNS.md`: all-parameter positivity of
  the first 31 coefficients of both transports in their bulk ranges;
- `third_active_transport_bulk_attack.py`: Bernoulli-scale lower kernels
  and fixed-column symbolic certificates for those low bands.
- `THIRD_ACTIVE_TRANSPORT_FIXED_LAYER_OBSTRUCTION.md`: exact obstruction
  to a fixed-depth termwise-positive `u_2`-layer proof of the odd bulk
  recurrence; the recurrence itself remains open.
- `THIRD_ACTIVE_TRANSPORT_INTERIOR_SYMBOL.md`: compact-uniform positivity
  for every macroscopic coefficient window `epsilon*s<=d<=(2-epsilon)*s`
  and the exact factored interior symbols.
- `THIRD_ACTIVE_TRANSPORT_LOG_BOUNDARY.md`: dominant-base theorem proving
  both transports above `d=241*log(s)` for all sufficiently large `s`;
  for those `s`, only the low layer `31<=d<241*log(s)` remains open.
- `THIRD_ACTIVE_TRANSPORT_LOG_BOUNDARY_BLIND_AUDIT.md`: author-swapped
  reconstruction of all four dominant sums, retained shifts, the constant
  241, both splices, and the fixed-layer obstruction; passed after making
  the eventual `s>=S` quantifier explicit.
- `ERDOS776_NEGATIVE_INITIAL_CHAMBERS_RED_TEAM.md`: independent hostile
  audit of the #776 no-borrow chart, legality gates, uniform asymptotics,
  and the then-open rank-five implication; the current #776 lane now
  refutes that implication while retaining the original problem as open.

Finite verification is used for falsification and transcription checks,
never as a replacement for an all-parameter proof.
