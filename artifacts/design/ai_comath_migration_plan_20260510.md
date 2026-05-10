# AI Co-Mathematician Architecture Migration Plan

Date: 2026-05-10

## Scope

This plan adapts the public AI Co-Mathematician architecture described in arXiv:2605.06651 to `ara-math`. It does not assume access to Google's internal implementation or Gemini-specific tooling. The goal is to implement the architecture pattern in ARA: a stateful, multi-workstream, review-gated mathematical research system whose outputs can become Lean-verified artifacts.

## Source Architecture

The public paper describes an asynchronous stateful workspace for open-ended mathematics. The important architectural elements are:

- A project coordinator that refines user intent, defines project goals, and delegates to parallel workstreams.
- Workstream coordinators that own a single route or subgoal and may spawn specialist agents.
- A shared filesystem and internal messaging layer.
- Native mathematical artifacts: reports, proof sketches, computational outputs, source notes, and formal artifacts.
- Persistent uncertainty tracking: unresolved claims, failed hypotheses, exhausted routes, and stalled workstreams remain visible.
- Review loops before completion: mathematical reviewers, source/citation checks, computational reproducibility checks, and proof/formalization checks.
- Progressive disclosure: the user normally sees the top-level coordinator dashboard, but can inspect workstream details.

The paper abstract also emphasizes holistic support for ideation, literature
search, computational exploration, theorem proving, and theory building, plus
benchmark-grade problem solving. This migration targets the architecture pattern
only; it does not claim access to Google's internal implementation, model stack,
or reported benchmark performance.

## Paper Gap Analysis

Status after the local Phase 5 follow-up:

| Paper capability | ARA status | Gap |
| --- | --- | --- |
| Asynchronous stateful workspace | Partial | Durable state, dashboard, messages, artifact graph, uncertainty ledger, bounded parallel worker pools, and resource-decision reports exist. The remaining gap is an interactive multi-user workbench and external agent orchestration beyond local runners. |
| Project coordinator refining user intent | Missing | Current coordinator schedules declared workstreams. It does not yet interview/refine intent, rewrite goals, or propose project decomposition from a loose user prompt. |
| Parallel workstreams and specialist agents | Partial | Independent workstreams can run in bounded parallel batches with same-Lean-target serialization. Specialist roles are still wrappers around existing tools rather than autonomous agents with role-specific contracts. |
| Shared filesystem and native mathematical artifacts | Partial | Reports, source notes, Lean declarations, run artifacts, and dependency graph nodes are persisted. Artifact schemas are still local and minimal. |
| Persistent uncertainty and failed hypotheses | Implemented baseline | Source debt, theorem debt, statement drift, computation debt, stalled workstreams, and failed routes are recorded and shown on the dashboard. |
| Ideation / route generation | Partial | `proof_lab` and `math_attack` can generate routes, but the CoMath layer does not yet run ideation as a first-class reviewed specialist loop. |
| Literature search | Partial | `literature.py` is wrapped as a source workstream. It is not yet a fully autonomous citation/source auditor with iterative query planning. |
| Computational exploration | Partial | Computation certificates are modeled and review-gated. There is no first-class computational exploration workstream with reproducible command manifests and seeded reruns. |
| Theorem proving / Lean formalization | Partial | Lean formalizer and closure runners are wrapped and review-gated. Promotion still depends on local runner quality and does not reproduce benchmark-grade theorem proving. |
| Theory building and new direction discovery | Missing | No dedicated theory-building memory, conjecture graph, concept inventory, or novelty review loop exists. |
| Progressive disclosure UI | Partial | Markdown dashboard and per-workstream files exist. There is no interactive workbench UI. |
| Benchmark-grade evaluation | Missing | No FrontierMath-style evaluation harness or performance claim exists. |

## Completion Backlog

The completion plan is intentionally broader than the current codebase. It is
the checklist that should be followed to get as close as possible to the public
AI Co-Mathematician architecture while staying honest about the limits of a
local open implementation. Each phase must leave durable files, tests, and
review-gate behavior behind; otherwise it is not considered implemented.

1. Parallel execution and resource guards. Completed baseline.
   - Add bounded worker pools for independent workstreams.
   - Limit concurrent LLM-backed runners and Lean builds separately.
   - Serialize workstreams targeting the same Lean file or workspace write set.
   - Persist a loop manifest showing queued/running/completed workstreams and resource decisions.

2. Intent refinement and project decomposition. Implemented local baseline.
   - Add an intake command that turns a loose mathematical goal into a project state, original theorem claim, initial uncertainty items, and candidate workstreams.
   - Persist `comath/intake_plan.json` and `comath/intake_plan.md`.
   - Record refined goal, assumptions, context files, generated claims, and generated workstream ids.
   - Keep this local/deterministic first, with optional LLM refinement later.

3. Specialist workstream roles. Implemented local baseline.
   - Promote ideation, source audit, computational exploration, Lean repair, global review, and theory-building into explicit role records.
   - Give each role input contracts, output artifact contracts, and review requirements.
   - Persist `comath/specialist_roles.json` and surface role count in the dashboard.

4. Computational exploration workstream. Implemented local baseline.
   - Add reproducible command manifests, seeds, input hashes, output certificate hashes, and rerun verification.
   - Block approval when a computation certificate cannot be reproduced.
   - Persist manifests and certificates under `comath/computation/<workstream>/`.
   - Record verified certificates in the artifact graph as `computation_certificate` nodes.

5. Literature/source autonomy. Partially implemented.
   - Add iterative query plans, source inventory, theorem statement extraction, assumption matching, and citation confidence scoring.
   - Convert unresolved source assumptions into named uncertainty items automatically.
   - Current baseline has source workstreams, source-debt gates, automatic query-plan generation, source-auditor specialist rounds, source inventory, and citation-confidence reports.
   - Remaining gap: stronger primary-source retrieval, theorem statement extraction, and assumption matching against source text.

6. Theory-building memory. Implemented local baseline.
   - Add conjecture graph, reusable lemma inventory, failed-hypothesis suppression, and novelty notes.
   - Surface "new direction" candidates separately from proof-route candidates.
   - Persist `comath/theory_memory.json` and `comath/theory_memory.md`.

7. Interactive/progressive UI. File-backed baseline implemented; interactive UI pending.
   - Keep Markdown files as the durable substrate.
   - Add a browsable local dashboard only after the file-backed contracts stabilize.

8. Evaluation harness. Implemented local baseline.
   - Add small local benchmark suites for scheduling, source-debt control, Lean-promotion safety, and reproducibility.
   - Do not make Google-level benchmark claims without independent evaluation.
   - Persist `comath/evaluation_report.json` and `comath/evaluation_report.md`.

9. External model orchestration. Implemented local Codex CLI baseline.
   - Add pluggable LLM providers for the project coordinator and specialist roles.
   - Require every LLM-backed specialist to write native artifacts and uncertainty updates, not just chat transcripts.
   - Preserve local deterministic paths for tests and offline use.
   - Local baseline now uses the existing Codex CLI ChatGPT login as a provider, plus a fake provider for tests.
   - Each specialist run persists prompt, context manifest, output, result JSON, artifact graph nodes, and workstream state.
   - Each specialist also maintains `conversation_state.json`, which is injected into later prompts for app-level resume/memory.

10. Interactive research workbench. Pending by design.
    - Build a local UI only after the contracts above are stable.
    - UI must expose progressive disclosure: top-level blocker first, then workstream state, artifacts, reviews, and failed routes.

11. Benchmark-grade evaluation. Pending independent evaluation.
   - Add benchmark fixtures for source-debt control, theorem-proving safety, reproducibility, and scheduler behavior.
   - Do not claim FrontierMath-style performance without an independent benchmark run and comparable model budget.
   - Local regression benchmark baseline now covers specialist memory/resume, source-audit loop persistence, and capability evaluation.

## End-to-End Implementation Recipe

To reproduce the public paper's architecture pattern in this repository, run
these stages in order for a target project:

1. `init-comath-project`: create state, dashboard, artifact graph, uncertainty ledger, failed-route log, and workstream directories.
2. `intake-comath-project`: refine the user goal, write `intake_plan`, create proof/source/compute/Lean/theory/global-review workstreams, seed source and computation uncertainty, and install specialist role contracts.
3. `run-comath-loop`: execute ready workstreams with bounded parallelism, LLM/Lean resource limits, same-file serialization, and durable loop reports.
4. `record-computation-certificate` or the `computation_repro` workstream executor: attach command, seed, input hashes, output hashes, stdout hash, certificate hash, and rerun verification.
5. `update-theory-memory`: record conjectures, reusable lemmas, failed hypotheses, novelty notes, and new directions; failed hypotheses must suppress duplicate reruns unless changed.
6. `review-workstream` / review gate: block approval for source debt, theorem debt, statement drift, Lean placeholders, missing original-theorem dependency paths, or unverified computation certificates.
7. `run-comath-evaluation`: write a capability report for the project against the public paper modules.
8. `run-comath-source-audit-loop`: generate source queries, run source-auditor rounds, persist source inventory and citation-confidence reports.
9. `run-comath-benchmarks`: run fake-provider local regressions for memory/resume, source-audit loop, and capability evaluation.
10. Only after all relevant checks are implemented/partial with no missing local capability should a project proceed to final assembly.

For Codex-backed specialists, use the existing ChatGPT login rather than an
OpenAI API key:

```bash
ara-math run-comath-specialist \
  --project projects/<project> \
  --role source_auditor \
  --workstream source-literature-audit \
  --backend codex

ara-math run-comath-specialist-loop \
  --project projects/<project> \
  --backend codex \
  --max-specialists 3 \
  --max-parallel-specialists 2

ara-math run-comath-source-audit-loop \
  --project projects/<project> \
  --backend codex \
  --rounds 3 \
  --max-parallel-rounds 2
```

If `--model` is omitted, `codex exec` uses `~/.codex/config.toml`; on this
machine that currently selects `gpt-5.5` with `xhigh` reasoning effort. Tests
must continue to use `--backend fake` or a fake provider so CI never consumes
real model quota.

This recipe gives local architecture parity, not Google-internal parity. The
remaining irreducible gaps are proprietary model quality, Google-specific
interactive workbench behavior, and externally verified benchmark performance.

## Current ARA Mapping

`ara-math` already has useful lower-level engines:

- `proof_lab.py`: clean-room route generation, route clustering, source-first mode, adversarial audit.
- `lean_formalizer.py`: downstream Lean write/verify loop.
- `campaign_loop.py`: repeated proof-lab/formalizer alternation with durable round artifacts.
- `review.py`: project-level proof and publication blockers.
- `workspace.py`: project filesystem, manifest, event log, JSON/Markdown artifact helpers.
- `orchestrator.py`: existing project-level CLI orchestration.
- `literature.py`, `math_scout.py`, `proof_search.py`, `closure.py`: specialist tools that can become workstream executors.

The missing layer is not another proof attempt loop. The missing layer is a durable coordinator that treats route discovery, source verification, Lean writing, computation, review, and freezing as first-class workstreams with explicit dependencies.

## Proposed ARA Architecture

Add a Co-Mathematician-style layer above the current runners:

```text
ProjectCoordinator
  -> WorkstreamCoordinator(source/literature route)
  -> WorkstreamCoordinator(proof strategy route)
  -> WorkstreamCoordinator(Lean formalization route)
  -> WorkstreamCoordinator(computational/certificate route)
  -> PersistentReviewer(logic/source/Lean/reproducibility/global strategy)
  -> ArtifactGraph + UncertaintyLedger
```

Existing `proof_lab`, `lean_formalizer`, `closure`, and `proof_search` should become workstream executors. `campaign_loop` should become a worker under the coordinator, not the top-level brain.

## Data Model

Add durable workstream records under each project:

```text
projects/<project>/
  comath/
    project_state.json
    project_dashboard.md
    artifact_graph.json
    uncertainty_ledger.json
    failed_routes.jsonl
    messages.jsonl
    workstreams/
      <workstream_id>/
        goal.md
        status.json
        report.md
        messages.jsonl
        blockers.md
        artifacts/
        reviews/
          round-001/
            logic_review.md
            source_review.md
            lean_review.md
            decision.json
```

Recommended state machines:

- Project: `intake -> goals_planned -> workstreams_running -> review_gate -> final_assembly -> verified | partial | frozen | escalated`.
- Workstream: `planned -> running -> needs_review -> revision -> approved | frozen | escalated`.
- Claim: `hypothesis -> route_candidate -> proof_candidate -> source_grounded -> lean_stubbed -> lean_verified -> assembled`.

## Core Modules

Implement these modules incrementally:

- `src/ara_math/workstreams.py`: dataclasses/enums for project, workstream, claim, review, dependency status.
- `src/ara_math/artifact_graph.py`: records claims, files, sources, Lean declarations, computational certificates, and dependency edges.
- `src/ara_math/uncertainty.py`: failed routes, unresolved assumptions, source debt, theorem debt, confidence, and owner workstream.
- `src/ara_math/coordinator.py`: selects next workstreams, assigns budgets, tracks dependencies, writes dashboard.
- `src/ara_math/review_gate.py`: multi-reviewer approval policy, stronger than the current single `MathReviewer`.
- `src/ara_math/comath_cli.py` or extend `cli.py`: commands for initializing, running, reviewing, and summarizing Co-Mathematician projects.

## CLI Surface

Initial commands:

- `init-comath-project --project <path>`: creates `comath/` state around an existing ARA project.
- `add-workstream --project <path> --kind <proof|lean|source|compute|review> --goal-file <file>`.
- `run-workstream --project <path> --workstream <id> --time-budget <seconds>`.
- `review-workstream --project <path> --workstream <id> --reviewers logic,source,lean`.
- `run-comath-loop --project <path> --time-budget <seconds> --max-workstreams <n>`.
- `project-dashboard --project <path>`.

## Review Gates

A workstream cannot be marked approved unless its type-specific gates pass:

- Proof route: exact statement alignment, dependency graph, adversarial proof review, no easier-variant drift.
- Source route: cited theorem exists, statement is transcribed, assumptions match, no hidden strengthening.
- Lean route: `lake build` passes, no `sorry`, no `admit`, no project-owned `axiom`, no invented source theorem classified as proved.
- Computational route: command, seed, input data, output certificate, and verifier are reproducible.
- Global route: the workstream moves a blocker on the original theorem, not only a local lemma with no dependency path.

## Source-Debt Control

The current long loops can produce Lean progress while silently moving the real burden into a new unproved source statement. The Co-Mathematician layer should explicitly classify this:

- `source_verified`: theorem is already in mathlib or a cited source and assumptions match.
- `source_formalization_needed`: theorem is known but not yet formalized.
- `external_theorem_needed`: theorem is plausible but not established by accepted literature.
- `research_gap`: theorem is itself the hard mathematical problem.

Final theorem assembly must fail if any dependency remains `external_theorem_needed` or `research_gap`.

## Migration Phases

Phase 1: schema and dashboard.

- Add workstream, artifact graph, uncertainty ledger models.
- Add `init-comath-project` and `project-dashboard`.
- No LLM calls required.

Phase 2: wrap existing runners.

- Wrap `proof_lab` as `ProofStrategyWorkstream`.
- Wrap `lean_formalizer` and `closure` as `LeanFormalizationWorkstream`.
- Wrap `literature` as `SourceWorkstream`.
- Persist every run as a workstream artifact with status and blockers.

Phase 3: review-gated completion.

- Add persistent reviewer records.
- Require logic/source/Lean review depending on workstream kind.
- Add tests that a workstream with `sorry`, `axiom`, hidden source debt, or statement drift cannot be approved.

Phase 4: coordinator scheduling.

- Implement dependency-aware scheduling.
- Allocate budgets by bottleneck class: source debt, Lean debt, proof gap, computation gap.
- Freeze branches after repeated non-decreasing blockers and preserve a freeze package.

Phase 5: parallel execution.

- Add worker pool limits: max concurrent LLM calls, max concurrent Lean builds, CPU/memory guard.
- Run independent workstreams in parallel, but serialize writes to the same Lean file.
- Persist resource decisions and skip/queue reasons in the loop report.
- Add tests proving independent workstreams overlap while same-file Lean workstreams serialize.

Phase 6: current theorem integration.

- Apply the system to the active CES75/Erdos866 project.
- Create separate workstreams for dense central block source proof, Lean repair, source audit, and global theorem assembly.
- Make the dashboard show that the blocker is the source-level dense central block theorem, not a generic final-target Lean error.

## Immediate CES75/Erdos866 Workstreams

For the current project, start with four workstreams:

- `source-dense-central-block`: prove or source-certify the dense central block theorem from the CES75 hypotheses.
- `lean-current-final-window`: preserve and clean the already engineered final-window/dyadic/six-witness Lean chain.
- `source-audit-ces75-theorem4`: align the paper's Theorem 4 and the formal target statement exactly.
- `global-review`: verify that the dependency graph closes the original 866 statement and does not merely prove a stronger conditional theorem.

This avoids another broad loop that spends time on already-engineered local lemmas while the real blocker remains source debt.

## Acceptance Criteria

The migration is useful only if it changes system behavior:

- Every long run must have a dashboard showing current original-theorem blocker, not only latest Lean error.
- Every generated theorem must have a claim status and dependency path to the original theorem.
- Failed routes must persist and suppress near-duplicate reruns unless the next run explains what changed.
- A Lean-passing file cannot be promoted if it assumes an unverified source theorem.
- A local lemma cannot be treated as progress unless it reduces a named blocker in the artifact graph.

## Current Implementation Snapshot

Implemented locally:

- Phase 1 schema/dashboard.
- Phase 2 runner wrappers.
- Phase 3 review gate.
- Phase 4 scheduler loop.
- Phase 5 parallel execution/resource guards.
- Phase 6 CES75/Erdos866 bootstrap template.
- Intent refinement and automatic deterministic workstream decomposition.
- First-class specialist role contracts.
- Reproducible computation manifests, certificates, and verification reports.
- Theory-building memory for conjectures, lemmas, failed hypotheses, novelty notes, and new directions.
- Local capability evaluation harness.
- Codex CLI specialist orchestration over the existing ChatGPT login, with fake-provider tests.
- Specialist app-level memory/resume through `conversation_state.json`.
- Automatic source-auditor query loop with source inventory and citation-confidence output.
- Local fake-provider regression benchmark suite.

Still pending:

- Stronger primary-source retrieval, theorem statement extraction, and assumption matching in the source-auditor loop.
- Interactive UI beyond the durable Markdown/file-backed dashboard.
- Independent benchmark-grade evaluation and any claim comparable to Google FrontierMath results.
