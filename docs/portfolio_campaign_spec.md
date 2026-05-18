# AMRA Portfolio Campaign Spec

Status: draft
Created: 2026-05-18
Owner: AMRA

## 1. Purpose

AMRA, short for Automated Mathematical Research Agents, should optimize for producing verified mathematical results and reusable proof assets across a broad problem portfolio, not for repeatedly exhausting resources on one hard problem.

The system should:

- run shallow probes over many problems;
- identify problems likely to yield complete proofs or Lean formalizations quickly;
- promote easy or high-value targets into focused attack;
- park hard, unclear, or counterexample-suspected targets without losing work;
- preserve all attempts, failures, partial lemmas, proof sketches, Lean artifacts, and review results as reusable memory;
- harvest completed Lean declarations into a shared local library.

This spec defines the architecture, data model, agent roles, scheduling policy, memory layout, and development phases for a portfolio-level campaign system.

## 2. Naming And Full Rename Mandate

The project name is AMRA.

During this refactor, the old `ara-math` naming must be fully replaced by AMRA naming across code, docs, CLI, tests, artifacts, and local library packaging.

Canonical names:

- Product/system name: `AMRA`.
- Full expansion: `Automated Mathematical Research Agents`.
- Repository name: `amra`.
- Python package: `amra`.
- Python source root: `src/amra`.
- CLI module: `python3 -m amra`.
- Optional console script: `amra`.
- Local reusable Lean library directory: `amra_library`.
- Local reusable Lean library module prefix: `AmraLibrary`.

Required rename map:

- `ara-math` -> `amra`.
- `ara_math` -> `amra`.
- `ARA Math` -> `AMRA`.
- `ara_library` -> `amra_library`.
- `AraLibrary` -> `AmraLibrary`.

Backward compatibility aliases may exist only as temporary migration shims, and must be marked deprecated. New implementation, tests, docs, and generated artifacts should use AMRA naming only.

## 3. Core Principle

The unit of optimization is the whole problem set, not a single problem.

Single-problem loops are still useful after a target is promoted, but the outer loop must continuously ask:

- Which problem is currently most likely to produce a verified result?
- Which problem is consuming time without measurable progress?
- Which partial result should be extracted and reused elsewhere?
- Which failed route should be recorded so future agents do not repeat it?

## 4. Existing Components To Reuse

The current repository already has several useful pieces:

- `src/amra/math_scout.py`: shallow problem probing and active readiness assessment.
- `src/amra/campaign_loop.py`: single-target iterative proof/formalization loop.
- `src/amra/focused_attack.py`: bounded Lean-focused attack on a named target.
- `src/amra/pure_agents.py`: Codex-style loop that can execute actions and observe results.
- `src/amra/artifact_graph.py`: durable artifact/dependency graph.
- `src/amra/amra_library.py`: local reusable Lean library manager.
- `src/amra/comath_capabilities.py`: existing theory memory and failed hypothesis support.
- `src/amra/review_gate.py`: independent review and gating concepts.
- `data/problem_bank.yaml` and `data/banks/*.yaml`: problem sources.

The portfolio system should extend these modules rather than replacing them.

## 5. Non-Goals

This system should not:

- assume every promoted problem must be solved;
- trust a proof because the proving agent claims it is complete;
- overwrite prior attempts or collapse history into one mutable summary;
- require every partial lemma to be globally promoted;
- let multiple workers write to the same Lean file concurrently;
- spend long budgets before a problem has passed independent feasibility review.

## 6. Problem Lifecycle

Every problem should have an explicit lifecycle state.

Allowed states:

- `unseen`: loaded from a bank but not actively probed.
- `scouted`: shallow probe completed.
- `promising`: evaluator recommends more work.
- `active_attack`: currently receiving focused proof/formalization resources.
- `formalization_ready`: natural-language proof or route is coherent enough for Lean work.
- `verified`: main target or accepted subtarget verifies in Lean without placeholders.
- `library_harvested`: reusable declarations have been promoted into `amra_library`.
- `parked`: not currently worth additional budget, but may be resumed.
- `frozen`: should not be resumed without human override.
- `counterexample_suspected`: current statement or route appears false.
- `needs_source`: exact statement or provenance is insufficient.

State transitions must be append-only in a history log.

Example:

```json
{
  "problem_id": "imo-2025-p6",
  "state": "counterexample_suspected",
  "previous_state": "active_attack",
  "changed_at": "2026-05-18T00:00:00+08:00",
  "reason": "Focused Lean attack found a diagonal uncovered-set counterexample candidate for the side-filter multiplicity lemma.",
  "evidence": [
    "projects/imo-2025-p6-formal-20260516/formal/focused_runs/p6-side-filter-multiplicity-2h-20260518/attack_note.md"
  ]
}
```

## 7. Directory Layout

### 6.1 Portfolio Run

Each portfolio campaign run should write an immutable run directory:

```text
artifacts/portfolio_campaigns/<campaign-id>/
  campaign_manifest.json
  campaign_state.json
  campaign_log.jsonl
  scout_report.json
  evaluator_report.json
  ranking.json
  promotion_queue.json
  parked_queue.json
  active_assignments.json
  final_report.md
  problems/
    <problem-id>/
      probe/
      evaluation/
      promotion/
      attack_runs/
      formalization_runs/
      review/
```

### 6.2 Problem Project

Each serious problem should have a durable project directory:

```text
projects/<problem-id>/
  problem.yaml
  state.json
  state_history.jsonl
  difficulty.json
  resume_pack.md
  memory/
    claim_ledger.json
    route_ledger.json
    failed_routes.json
    evidence_index.json
    reviewer_notes.jsonl
  proof/
    sketches/
    audits/
    blockers/
    current_focus.md
  formal/
    MathProject/
  runs/
    <run-id>/
      run_manifest.json
      prompt.txt
      output.md
      report.json
      observations.jsonl
      tool_logs/
```

### 6.3 Global Indexes

Portfolio-level memory should maintain global indexes:

```text
artifacts/global_memory/
  problem_index.json
  claim_index.json
  failed_route_index.json
  theorem_asset_index.json
  difficulty_history.jsonl
```

These indexes should not replace project-local memory. They are search and retrieval accelerators.

## 8. Memory Model

### 7.1 Claim Ledger

The claim ledger is the canonical record of mathematical assertions.

Each claim should include:

- stable `claim_id`;
- human statement;
- optional Lean declaration name;
- status;
- dependencies;
- proof evidence;
- counterexample evidence;
- source provenance;
- owning problem;
- whether it is reusable.

Example:

```json
{
  "claim_id": "imo2025-p6-side-filter-multiplicity",
  "kind": "lemma",
  "statement_nl": "The eight side-pair filters around a common increasing/decreasing chain cell have cardinality at least 2025 + incLen + decLen - 3.",
  "lean_name": "P6Tiling.sidePairFilterMultiplicityLowerBound2025",
  "status": "counterexample_suspected",
  "dependencies": [
    "imo2025-p6-longest-chain-arm-sum",
    "imo2025-p6-side-pair-covering"
  ],
  "evidence": [
    {
      "type": "counterexample_candidate",
      "path": "focused_runs/p6-side-filter-multiplicity-2h-20260518/attack_note.md"
    }
  ],
  "reusable": false,
  "updated_at": "2026-05-18T00:00:00+08:00"
}
```

Allowed claim statuses:

- `hypothesis`
- `sketch`
- `route_supported`
- `needs_review`
- `review_rejected`
- `lean_stubbed`
- `lean_partial`
- `lean_verified`
- `counterexample_suspected`
- `false`
- `obsolete`

### 7.2 Route Ledger

The route ledger records proof strategies, not just claims.

Each route should include:

- route name;
- target claim;
- core idea;
- required dependencies;
- current blocker;
- attempt history;
- evaluator verdict;
- continuation cost estimate.

Example statuses:

- `new`
- `promising`
- `blocked`
- `failed`
- `superseded`
- `completed`

### 7.3 Failed Route Memory

Failed routes must be first-class memory. This is essential for avoiding repeated P6-style loops.

Each failed route should include:

- exact failed assertion or approach;
- failure mode;
- evidence path;
- whether failure is logical, modeling, formalization, source, or resource related;
- future resume condition.

Example failure modes:

- `counterexample_candidate`
- `lean_statement_mismatch`
- `missing_mathlib_api`
- `proof_gap`
- `combinatorial_case_explosion`
- `modeling_too_weak`
- `resource_timeout`

## 9. Difficulty Assessment

Difficulty must be assessed independently from proof generation.

### 8.1 Scores

Each problem receives a `difficulty.json`:

```json
{
  "problem_id": "imo-2025-p1",
  "generated_at": "2026-05-18T00:00:00+08:00",
  "feasibility_score": 8.2,
  "formalization_score": 7.5,
  "expected_hours_to_result": 4.0,
  "confidence": 0.7,
  "recommendation": "promote",
  "primary_blocker": "formalization",
  "risk_flags": [],
  "evidence": [
    "artifacts/imo/2025/pure_proof_agent_runs/..."
  ]
}
```

### 8.2 Signals

The evaluator should consider:

- exact statement availability;
- known theorem or source availability;
- shallow proof success;
- number and depth of unresolved obligations;
- Lean build status;
- placeholder count;
- whether the formal statement matches the natural-language theorem;
- rate of progress per hour;
- number of repeated failed attempts;
- presence of counterexample candidates;
- dependency on large missing theory;
- reusability of intermediate lemmas.

### 8.3 Promotion Rules

Default promotion thresholds:

- Promote if `feasibility_score >= 7` and no severe risk flags.
- Promote if a known theorem/source exists and formalization appears bounded.
- Park if `feasibility_score < 5`.
- Park if two consecutive runs show no measurable progress.
- Freeze if a counterexample candidate is strong and unresolved.
- Send to source recovery if exact statement or provenance is missing.

### 8.4 Progress Velocity

Every active attack should update progress metrics:

```json
{
  "lean_verified_declarations_added": 3,
  "open_obligations_before": 12,
  "open_obligations_after": 7,
  "placeholder_count_before": 5,
  "placeholder_count_after": 2,
  "new_failed_routes": 1,
  "elapsed_seconds": 7200,
  "progress_velocity": 0.42
}
```

If velocity remains near zero for two rounds, the scheduler should park the problem unless a human override exists.

## 10. Agent Roles

### 9.1 ScoutAgent

Purpose: short-budget broad probing.

Inputs:

- problem statement;
- metadata;
- local assets;
- prior global memory hits.

Outputs:

- exact statement status;
- shallow proof attempt;
- possible known theorem;
- likely formalization target;
- feasibility score;
- blocker class.

Default budget: 5 to 20 minutes per problem.

ScoutAgent should be read-only by default.

### 9.2 ProofAgent

Purpose: produce or refine mathematical proof routes.

Inputs:

- promoted problem;
- claim ledger;
- route ledger;
- evaluator constraints;
- relevant library inventory.

Outputs:

- natural-language proof sketch;
- lemma decomposition;
- explicit dependency graph;
- candidate Lean theorem statements;
- counterexample checks.

ProofAgent may use tools such as Lean quick checks, search, computation, and local scripts. It should not be restricted to pure prose.

### 9.3 FormalizerAgent

Purpose: turn accepted proof routes into Lean.

Inputs:

- reviewed proof route;
- exact theorem statement;
- Lean workspace;
- existing local library;
- allowed edit scope.

Outputs:

- verified Lean declarations;
- updated proof gap notes;
- build report;
- list of promoted candidate declarations.

FormalizerAgent writes only inside its assigned workspace.

### 9.4 EvaluatorAgent

Purpose: independent assessment.

EvaluatorAgent should not share the ProofAgent's private working context. It should read only durable artifacts:

- proof sketches;
- Lean files;
- build reports;
- claim ledger;
- failed route ledger;
- run summaries.

Outputs:

- difficulty score;
- proof confidence;
- formalization confidence;
- recommendation: `promote`, `continue`, `park`, `freeze`, `source_recover`, `counterexample_review`;
- concrete reason.

### 9.5 CounterexampleAgent

Purpose: stress-test claims and proof routes.

Inputs:

- target claim;
- assumptions;
- model definitions;
- known boundary cases.

Outputs:

- counterexample candidate;
- formal counterexample if possible;
- recommendation to revise statement or route.

This agent should be invoked automatically when:

- a proof route depends on a strong combinatorial inequality;
- Lean attack reports `counterexample_suspected`;
- evaluator flags a modeling mismatch.

### 9.6 LibrarianAgent

Purpose: promote reusable verified Lean assets.

Inputs:

- verified Lean declarations;
- provenance metadata;
- project source path;
- candidate module.

Outputs:

- updated `amra_library/formal/AmraLibrary/...`;
- updated `amra_library/registry.json`;
- build report;
- import hints for future projects.

Only declarations that build without `sorry`, `axiom`, `admit`, `opaque`, or placeholder constants should be promoted.

### 9.7 Coordinator

Purpose: schedule work across the portfolio.

Responsibilities:

- maintain queues;
- assign budgets;
- avoid duplicate work;
- enforce write locks;
- trigger evaluation after each run;
- park low-value targets;
- launch focused attacks for high-value targets;
- trigger library harvesting.

## 11. Multi-Agent Execution Model

### 10.1 Parallelism

Safe parallel work:

- multiple ScoutAgents on different problems;
- multiple EvaluatorAgents in read-only mode;
- ProofAgent and CounterexampleAgent on copied artifacts;
- FormalizerAgents on separate Lean workspaces.

Unsafe parallel work:

- two writers editing the same Lean file;
- two LibrarianAgents modifying the same library module;
- one agent rewriting project state while another agent updates lifecycle state.

### 10.2 Locks

Use simple lock files:

```text
projects/<problem-id>/.locks/
  state.lock
  formal.lock
  library-promotion.lock
```

Lock records should include:

- owner agent;
- PID if local;
- started_at;
- intended action;
- timeout.

### 10.3 Workspace Isolation

Long formalization attempts should run in isolated workspaces:

```text
projects/<problem-id>/workspaces/<run-id>/formal/
```

Only successful, reviewed changes should be merged back into the canonical `formal/` workspace.

## 12. Scheduler Policy

### 11.1 Outer Loop

One portfolio round:

1. Load candidate problem bank.
2. Retrieve global memory matches.
3. Run short scouting probes.
4. Run independent evaluation.
5. Rank problems by expected result yield.
6. Promote top targets.
7. Assign bounded proof/formalization work.
8. Review outputs.
9. Update ledgers and global indexes.
10. Harvest verified reusable lemmas.
11. Park or freeze low-yield targets.

### 11.2 Ranking Formula

Initial ranking can use:

```text
priority =
  3.0 * feasibility_score
  + 2.0 * formalization_score
  + 1.5 * reusable_asset_score
  + 1.0 * source_quality_score
  - 2.0 * risk_score
  - 1.0 * estimated_hours_to_result
  - 1.5 * repeated_failure_count
```

The exact weights should be configurable.

### 11.3 Budget Classes

Default budgets:

- `scout`: 5 to 20 minutes.
- `micro_attack`: 20 to 45 minutes.
- `focused_attack`: 1 to 4 hours.
- `deep_attack`: requires explicit promotion and evaluator confidence.

No problem should receive `deep_attack` until it has:

- exact statement;
- at least one credible proof route or known theorem;
- independent evaluator score above threshold;
- no unresolved strong counterexample candidate.

## 13. Review Gates

A result is not complete until it passes gates appropriate to its level.

### 12.1 Natural-Language Proof Gate

Must include:

- exact statement;
- assumptions;
- lemma dependency chain;
- no unexplained "obvious" critical step;
- stress-test notes;
- evaluator verdict.

### 12.2 Lean Formalization Gate

Must include:

- successful `lake build`;
- no `sorry`, `admit`, `axiom`, `opaque`, or placeholder constants;
- theorem statement matches intended problem;
- review confirms no weakened or mismodeled target;
- build report stored.

### 12.3 Library Promotion Gate

Must include:

- reusable declaration names;
- source project and file;
- provenance note;
- `amra_library` build success;
- registry entry.

## 14. Retrieval And Reuse

Before any new serious attempt, the agent should retrieve:

- similar problem statements;
- prior failed routes with overlapping tags;
- verified Lean declarations from `amra_library`;
- partial lemmas from claim indexes;
- known source/literature records.

The prompt should explicitly include:

- "do not repeat failed route X unless you can address failure Y";
- "prefer using library declaration Z";
- "current exact blocker is B".

## 15. CLI Design

Proposed new commands:

```bash
python3 -m amra run-portfolio-campaign \
  --bank data/banks/imo_2025.yaml \
  --run-name imo-2025-portfolio-round-1 \
  --scout-limit 6 \
  --scout-timeout 600 \
  --promote-top 2 \
  --attack-budget 14400
```

```bash
python3 -m amra evaluate-problem \
  --project projects/imo-2025-p6-formal-20260516 \
  --run-name p6-independent-evaluation
```

```bash
python3 -m amra harvest-library-candidates \
  --project projects/imo-2025-p1 \
  --module AmraLibrary.Olympiad.IMO2025.P1
```

```bash
python3 -m amra summarize-portfolio-memory \
  --campaign artifacts/portfolio_campaigns/imo-2025-portfolio-round-1
```

## 16. Implementation Plan

### Phase 1: Portfolio Data Layer

Add:

- `src/amra/portfolio_campaign.py`
- `src/amra/portfolio_memory.py`
- `tests/test_portfolio_campaign.py`
- `tests/test_portfolio_memory.py`

Implement:

- campaign directory creation;
- problem state schema;
- claim ledger load/save/upsert;
- route ledger load/save/upsert;
- failed route load/save/upsert;
- global memory index update.

Acceptance criteria:

- can create a portfolio campaign over a small fake bank;
- writes stable JSON artifacts;
- can resume without overwriting prior entries.

### Phase 2: Broad Scouting Integration

Extend `MathScoutRunner` or wrap it from `PortfolioCampaignRunner`.

Implement:

- per-problem short probe;
- structured parsing;
- ranking report;
- promotion and parked queues.

Acceptance criteria:

- given 3 test problems, system ranks them and emits promotion queue;
- failed or timed-out scout runs still produce valid artifacts.

### Phase 3: Independent Evaluation

Add `EvaluatorAgentRunner`.

Implement:

- read-only evaluation prompt;
- standardized difficulty output;
- risk flags;
- promotion/park/freeze recommendation.

Acceptance criteria:

- evaluator can mark a counterexample-suspected route as `freeze` or `counterexample_review`;
- evaluator can promote an easy known theorem target.

### Phase 4: Attack Scheduling

Connect promoted targets to:

- `AIProofLabRunner`;
- `LeanFormalizerRunner`;
- `FocusedLeanAttackRunner`;
- pure Codex proof loops.

Implement:

- budget assignment;
- write locks;
- isolated workspaces;
- progress velocity metrics.

Acceptance criteria:

- only promoted problems receive focused attack budget;
- two formalizer workers cannot write the same canonical Lean workspace concurrently.

### Phase 5: Memory Consolidation

Implement automatic updates:

- claim ledger from proof outputs;
- failed route ledger from blockers;
- global memory index from project-local memory;
- resume pack generation.

Acceptance criteria:

- a failed route from one run appears in the next prompt as a route to avoid;
- a verified declaration appears in future retrieval results.

### Phase 6: Library Harvesting

Extend `AmraLibraryManager` workflow.

Implement:

- candidate detection from verified project declarations;
- provenance block;
- registry update;
- library build;
- import hint generation.

Acceptance criteria:

- verified declarations can be promoted into `amra_library`;
- future project prompts include relevant library inventory.

### Phase 7: Dashboard And Reports

Add portfolio summary reports:

- active queue;
- promoted targets;
- parked targets;
- completed proofs;
- library assets added;
- highest-value blockers;
- repeated failure clusters.

Acceptance criteria:

- one command produces `final_report.md`;
- user can see why each problem was promoted, parked, or frozen.

## 17. Testing Strategy

Unit tests:

- state transitions;
- claim ledger merge;
- failed route deduplication;
- ranking formula;
- lock behavior;
- evaluator parser;
- library candidate detection.

Integration tests:

- fake bank with easy, medium, and impossible targets;
- portfolio scout -> evaluate -> promote -> focused run;
- counterexample-suspected route gets parked;
- verified lemma gets harvested to library.

Regression tests:

- P6-style false main lemma should not be repeatedly attacked after a failed route is recorded.
- P1-style easier target should be promoted ahead of P6 if its expected time to verified result is lower.

## 18. P6 Lesson Applied

The P6 side-filter multiplicity episode should become a canonical failed-route example.

Record:

- target claim: `sidePairFilterMultiplicityLowerBound2025`;
- status: `counterexample_suspected`;
- suspected model: identity diagonal uncovered set;
- consequence: do not continue this exact route without revising the inequality;
- next allowed actions:
  - formalize the counterexample;
  - weaken or correct the side-filter bound;
  - switch to a different counting route.

The scheduler should not allocate long focused proof budget to this exact lemma again unless a new route explicitly addresses the recorded failure.

## 19. Success Metrics

The portfolio system should be evaluated by:

- number of verified Lean declarations per compute hour;
- number of completed problem-level proofs;
- number of reusable library declarations harvested;
- reduction in repeated failed-route attempts;
- average time from scouting to promotion decision;
- evaluator accuracy on easy vs hard targets;
- percentage of runs with complete durable artifacts.

## 20. Open Design Questions

- Should natural-language proof and Lean formalization be one unified agent loop or two staged loops with shared tools?
- How aggressive should automatic library promotion be?
- Should parked problems be periodically rescored as the library grows?
- What is the minimum evidence needed to freeze a route as false rather than merely blocked?
- Should portfolio ranking favor easy wins or high-value reusable lemmas when compute is scarce?

Default answer for now:

- use unified proof/formalization agents for active attack;
- keep evaluator separate and read-only;
- harvest only Lean-verified declarations;
- rescore parked problems after major library growth;
- optimize first for verified outputs and reusable assets.
