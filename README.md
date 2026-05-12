# ARA Math

`ara-math` is a separate mathematics research automation system focused on:

- problem selection from structured math problem banks
- proof planning via claim and lemma decomposition
- Lean 4 project bootstrapping and build diagnostics
- workspace-first research execution with explicit artifacts

It is intentionally separate from the ML-oriented `auto-research-agent` repository. The long-term goal is to share only small infrastructure pieces such as status logging and project viewers, not to force math workflows into the ML pipeline.

## Initial Version

This repository currently implements:

- a normalized problem bank format
- a registry of local and imported problem banks
- an importer for the local Erdős problem metadata file
- synchronization of topic-specific banks from the local `formal-math` workspace
- bank scouting for candidate selection over large open-problem catalogs
- project workspace creation
- a math proof plan generator
- exact-statement tracking and context auditing
- local and optional remote literature harvesting with structured evidence extraction
- proof-path assessment and mathematical-idea ledger seeding
- Lean claim stub generation from the proof plan
- a Lean workspace template
- a Lean build executor with `sorry` auditing
- an autonomous proof-search / proof-repair loop with per-attempt state and optional `codex exec` backend
- a root-goal driven campaign loop that schedules dependent proof subgoals before returning to the original theorem
- CoMath specialist orchestration that turns review blockers and next actions into prioritized proof obligations
- batch open-problem campaigning over scout shortlists with timeout-based handoff to the next problem
- manuscript blueprint generation
- deliverable assessment that routes projects into `research_report`, `formalization_note`, or `paper_candidate`
- math-specific review gates for placeholder statements, `sorry`, `axiom`, and other unresolved proof gaps
- a CLI for creating and running projects

It does **not** yet implement:

- trusted academic literature acquisition with source-quality ranking
- strong theorem proving that can routinely close nontrivial open problems
- domain-specific search executors for each problem family
- polished paper writing from verified theorem statements

## Repository Layout

```text
ara-math/
├── data/
│   └── problem_bank.yaml
├── src/ara_math/
│   ├── cli.py
│   ├── context.py
│   ├── formalization.py
│   ├── goal_campaign.py
│   ├── lean.py
│   ├── models.py
│   ├── orchestrator.py
│   ├── planning.py
│   ├── problem_bank.py
│   ├── review.py
│   ├── workspace.py
│   ├── writing.py
│   └── templates/lean_project/
├── tests/
└── projects/                # generated locally, ignored by git
```

## Quick Start

```bash
cd /home/biostar/work/projects/ara-math
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Without installation, the repo-local wrapper also works:

```bash
python3 run.py list-problems
```

List bundled problems:

```bash
python3 run.py list-problems
```

List registered banks after syncing local sources:

```bash
python3 run.py list-banks
```

Generate the registry and topic banks from the local `formal-math` workspace:

```bash
python3 run.py sync-local-banks \
  --formal-math-root /home/biostar/work/projects/formal-math
```

Scout a large bank such as the imported Erdős open catalog:

```bash
python3 run.py scout-bank \
  --bank-name erdos_open_637 \
  --formal-math-root /home/biostar/work/projects/formal-math \
  --top-k 12 \
  --output /home/biostar/work/projects/ara-math/artifacts/erdos_open_scouting.json
```

Harvest local or remote reference material for a project before planning:

```bash
python3 run.py harvest-literature \
  --project /home/biostar/work/projects/ara-math/projects/erdos-1052-shortlist-20260421
```

Enable remote URL fetching when you want the system to inspect web references directly:

```bash
python3 run.py harvest-literature \
  --project /home/biostar/work/projects/ara-math/projects/erdos-1052-shortlist-20260421 \
  --bank-name unitary_perfect_track \
  --allow-network
```

Create a project:

```bash
python3 run.py new-project --problem erdos-1052
```

Create a project from a registered bank:

```bash
python3 run.py new-project --bank-name unitary_perfect_track --problem erdos-1052
```

Supply the exact mathematical statement before serious proof work:

```bash
python3 run.py set-statement \
  --project /home/biostar/work/projects/ara-math/projects/erdos-1052-20260421 \
  --statement-file /path/to/exact_statement.md \
  --source "manual curation"
```

Override the deliverable type when human judgment should take precedence over the heuristic classifier:

```bash
python3 run.py set-deliverable \
  --project /home/biostar/work/projects/ara-math/projects/erdos-1052-20260421 \
  --mode research_report \
  --reason "This result is useful, but it does not justify a paper workflow."
```

Generate a proof plan:

```bash
python3 run.py plan --project /home/biostar/work/projects/ara-math/projects/erdos-1052-20260421
```

Generate Lean claim stubs and formalization artifacts:

```bash
python3 run.py prepare-formal --project /home/biostar/work/projects/ara-math/projects/erdos-1052-20260421
```

Run the Lean build and audit:

```bash
python3 run.py build-lean --project /home/biostar/work/projects/ara-math/projects/erdos-1052-20260421
```

Run a root-goal driven proof campaign from a manifest:

```bash
python3 run.py init-goal-campaign \
  --output /tmp/goal_manifest.json \
  --root-statement-file /path/to/root_statement.md \
  --root-target-theorem original_theorem \
  --root-target-file MathProject/MainClaim.lean \
  --workspace /path/to/lean/workspace

python3 run.py run-goal-campaign \
  --manifest /tmp/goal_manifest.json \
  --workspace /path/to/lean/workspace \
  --backend codex \
  --rounds 20 \
  --time-budget 7200 \
  --search
```

The goal manifest is the durable state for this loop. Add subgoals under
`goals` with `id`, `statement`, `target_theorem`, `target_file`,
`dependencies`, and `priority`; the runner proves ready subgoals first, records
root-gap reviews after each phase, and only accepts completion when the root
Lean target verifies.

`ara-math` now runs Lean in guarded mode by default:
- it refuses cold-cache builds that would bootstrap `mathlib` from scratch
- it lowers process priority and applies CPU / memory / process-count limits
- it checks current system headroom before launching Lean or proof-search attempts

If you intentionally want a cold-cache build, opt in explicitly:

```bash
python3 run.py build-lean \
  --project /home/biostar/work/projects/ara-math/projects/erdos-1052-20260421 \
  --allow-cold-cache
```

The default guardrails can be tuned with environment variables:
- `ARA_MATH_LEAN_MAX_MEMORY_MB`
- `ARA_MATH_LEAN_MAX_CPU_SECONDS`
- `ARA_MATH_LEAN_MAX_PROCESSES`
- `ARA_MATH_LEAN_NICENESS`
- `ARA_MATH_MIN_AVAILABLE_MEMORY_MB`
- `ARA_MATH_MAX_LOAD_PER_CPU`
- `ARA_MATH_SYSTEM_WAIT_SECONDS`
- `ARA_MATH_SYSTEM_WAIT_POLL_SECONDS`
- `ARA_MATH_BACKEND_MAX_MEMORY_MB`
- `ARA_MATH_BACKEND_MAX_CPU_SECONDS`
- `ARA_MATH_BACKEND_MAX_PROCESSES`
- `ARA_MATH_BACKEND_NICENESS`
- `ARA_MATH_ALLOW_COLD_CACHE=1`

Generate a manuscript blueprint:

```bash
python3 run.py write-manuscript --project /home/biostar/work/projects/ara-math/projects/erdos-1052-20260421
```

Run the math-specific review gate:

```bash
python3 run.py review-project --project /home/biostar/work/projects/ara-math/projects/erdos-1052-20260421
```

Run the current end-to-end MVP pipeline:

```bash
python3 run.py run --project /home/biostar/work/projects/ara-math/projects/erdos-1052-20260421
```

Run a math-only single-target attack loop before Lean formalization:

```bash
python3 run.py run-math-attack \
  --project /home/biostar/work/projects/ara-math/projects/erdos-1052-shortlist-20260421 \
  --target "Attack the branch 3 does not divide N for Erdős #1052" \
  --context-file /home/biostar/work/projects/formal-math/docs/erdos_1052_math_proof_program_2026-04-26.md \
  --context-file /home/biostar/work/projects/formal-math/docs/erdos_1052_branch3_lemma_pack_2026-04-26.md \
  --evidence-command "python3 /home/biostar/work/projects/formal-math/erdos-1052-unitary-perfect/src/branch3_closure.py --limit 60" \
  --evidence-cwd /home/biostar/work/projects/formal-math/erdos-1052-unitary-perfect \
  --iterations 8 \
  --time-budget 28800 \
  --iteration-timeout 420 \
  --model gpt-5.4 \
  --reasoning-effort high
```

This stage writes `proof/math_attack/...` artifacts inside the `ara-math` project while allowing specialized local scripts from `formal-math` to serve as evidence providers. Use it when the current blocker is mathematical route discovery rather than Lean proof repair.

## Project Outputs

Each project stores explicit artifacts:

- `idea/problem_context.json`: structured problem metadata plus exact-statement status
- `idea/exact_statement.md`: authoritative mathematical statement to be proved or audited
- `idea/proof_path_assessment.json`: historical proof base, modern tools, blockers, and a current route hypothesis
- `idea/literature_foundations.json`: recovered older results, companion theorems, and source inventory
- `idea/reference_snapshots.json`: harvested local or remote source snapshots and statement candidates
- `idea/literature_evidence.json`: structured known results, proof ingredients, modern tool hints, open gaps, and source attribution
- `idea/statement_recovery.json`: best recovered exact-statement candidate and whether it was applied
- `idea/literature_digest.md`: human-readable literature harvest summary
- `idea/math_idea_ledger.json`: reusable mathematical ideas and route hypotheses worth carrying across projects
- `idea/deliverable_override.json`: human override for `auto | research_report | formalization_note | paper_candidate`
- `proof/proof_plan.json`: task DAG for definitions, lemmas, main claim, and computational obligations
- `proof/claim_registry.json`: machine-readable claim inventory and current status
- `proof/math_attack_status.json`: latest math-only single-target attack loop status
- `proof/math_attack/*/journal.md`: iteration journal for route discovery, obstruction searches, and local evidence feedback
- `comath/workstreams/*`: specialist workstreams, including generated proof obligations with acceptance criteria
- `formal/MathProject/*.lean`: generated Lean workspace and proof stubs
- `artifacts/lean_build_report.json`: structured build diagnostics and `sorry` count
- `writing/manuscript.md`: manuscript blueprint tied to the current claims and build state
- `writing/research_report.md` or `writing/formalization_note.md`: lower-tier outputs for results that do not justify a paper workflow
- `artifacts/review_report.json`: publishability/proof-gap review with blockers and recommendations
- `artifacts/deliverable_assessment.json`: automatic output classification and rationale
- `pipeline_events.jsonl`: append-only event stream across stages

## Problem Bank Strategy

The bundled `data/problem_bank.yaml` is small and curated. For larger local inventories, use the importer:

```bash
python3 run.py import-erdos-bank \
  --source /home/biostar/work/projects/formal-math/docs/open_problems.yaml \
  --output /home/biostar/work/projects/ara-math/data/erdos_problem_bank.yaml
```

Then point project creation at the imported bank:

```bash
python3 run.py new-project --bank /home/biostar/work/projects/ara-math/data/erdos_problem_bank.yaml --problem 1052
```

After `sync-local-banks`, the registry includes:

- `erdos_open_637`: imported open Erdős catalog
- `erdos_full_1120`: imported full Erdős catalog
- `amicable_track`
- `triangle_dissection_track`
- `weird_numbers_track`
- `unitary_perfect_track`
- `carmichael_track`

## Design Notes

- Projects are file-system workspaces, not database rows.
- Claims and tasks are explicit JSON artifacts.
- Large catalogs should be scouted before project creation so ara-math attacks shortlisted problems rather than random open statements.
- A serious proof attempt starts with historical proof ingredients and modern tool synthesis, not with immediate Lean theorem stubs.
- Local READMEs and optional remote URL snapshots are harvested before planning so placeholder statements can be replaced with exact targets when possible.
- Lean verification is a first-class stage, not a final afterthought.
- A build is not considered clean if `sorry` placeholders remain.
- Placeholder theorem statements and missing exact statements are treated as blockers, not as success.
- Lean builds automatically try to reuse compatible local `.lake/packages` caches before downloading dependencies from scratch.
