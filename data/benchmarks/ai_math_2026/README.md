# AI Math Benchmark 2026

Generated: 2026-05-14

This benchmark suite collects public 2025-2026 AI mathematics cases that are useful for testing whether `AMRA` can independently discover, prove, and formalize known results.

The source problem bank is:

`data/banks/ai_math_benchmark_2026.yaml`

## Benchmark Tiers

| Tier | Meaning | Expected AMRA outcome |
| --- | --- | --- |
| `tier_1_reproduce_public_formal_result` | Publicly reported Lean/formal proof exists. | Recover a theorem header and produce a fresh no-sorry Lean proof without looking at proof scripts during the independence run. |
| `tier_2_research_level_informal_to_formal` | Research-level statement with expert-reviewed or AI-assisted informal proof evidence. | Produce an auditable proof plan, dependency graph, and at least one verified formal slice. |
| `tier_3_human_ai_workflow_reproduction` | Result needed multi-agent or human-AI orchestration. | Reproduce a small lemma slice and record where autonomous proof search fails. |
| `tier_4_large_scale_formalization_slice` | Industrial-scale formalization. | Select one named theorem slice and measure formalization/dependency recovery, not full project completion. |

## Independence Protocol

1. Use only the public problem statement and bibliographic metadata at first.
2. Do not expose released Lean scripts, Aletheia transcripts, Gauss-generated source files, or author solutions to the proving agent during the first attempt.
3. Require a fixed success contract before proof search:
   - target theorem statement,
   - allowed imports,
   - forbidden assumptions,
   - timeout and token budget,
   - verification command.
4. Accept success only when:
   - the target theorem exists,
   - `lake build` passes,
   - no `sorry`, `admit`, `axiom`, `constant`, `opaque`, or placeholder is introduced,
   - the proof log records all external facts used.
5. After a failed independence attempt, run a source-assisted pass and compare:
   - whether the system selected the same decomposition,
   - which library gaps blocked it,
   - whether it produced true but non-progress lemmas.

## Recommended First Runs

Start with these entries:

1. `ai-erdos-1026-weighted-erdos-szekeres`
2. `ai-erdos-728-factorial-divisibility`
3. `ai-firstproof-06-light-subset`
4. `ai-seed-prover-imo-2025-formal-suite`

Avoid starting with `ai-gauss-strong-pnt` or `ai-gauss-sphere-packing-slice`; those are scale tests, not current AMRA capability tests.

## Local Commands

List registered banks:

```bash
python3 run.py list-banks
```

List this benchmark bank:

```bash
python3 run.py list-problems --bank-name ai_math_benchmark_2026
```

Create a project for one benchmark case:

```bash
python3 run.py new-project \
  --bank-name ai_math_benchmark_2026 \
  --problem ai-erdos-1026-weighted-erdos-szekeres
```

Run proof search after project creation:

```bash
python3 run.py run-proof-search \
  --project <created-project-dir> \
  --backend codex \
  --timeout 900
```

Use the current project CLI help for exact backend and timeout flags if they change.

## Research Summary

### Mature Components

Lean, Rocq/Coq, Isabelle/HOL, HOL Light, Mizar, Metamath, SMT solvers, and SAT/ATP systems are mature verification technologies in the sense that they can check proofs or discharge specific formal fragments reliably. They are not by themselves autonomous research mathematicians.

### AI System Pattern

The strongest public AI mathematics results share the same structure:

1. A model proposes proof ideas or formal proof steps.
2. A proof assistant or formal checker supplies objective feedback.
3. Human experts often provide statement formalization, scaffolding, library design, or post-hoc mathematical review.
4. Large-scale systems run many agents in parallel and keep only proofs that compile.

This means the current frontier is not "one model solves arbitrary math." It is "tool-using proof pipelines can solve selected problems when the statement, search space, and verification loop are engineered carefully."

### Systems Survey

- Google DeepMind AlphaProof and AlphaGeometry2: AlphaProof searches Lean proofs after expert formalization; AlphaGeometry2 is specialized for synthetic geometry. The combined system solved four IMO 2024 problems.
- Google Gemini Deep Think / Aletheia: Deep Think reached official IMO 2025 gold-level natural-language performance. Aletheia extends this into research-agent workflows with web/search/tool use and reports 6/10 FirstProof solutions by majority expert assessment.
- Harmonic Aristotle: Proprietary Lean-centered theorem prover combining formal search, informal lemma generation, and geometry support. Public materials and papers report IMO-level and Erdős-problem Lean successes, but many details remain closed.
- Math Inc. Gauss: Autoformalization agent for large Lean projects. Strong evidence exists through public repositories for the strong PNT formalization; Math Inc. also reports major sphere-packing formalization contributions.
- ByteDance Seed-Prover: Formal Lean theorem-proving system with agentic RL, tool use, and verifier feedback; public repo includes IMO 2025 and Putnam formal proof artifacts.
- OpenAI GPT models and Claude Code: Strong as human-in-loop collaborators. They can propose strategies and write Lean/code, but the reliable pattern still requires formal verification and expert steering.
- Open-source theorem provers such as Goedel-Prover, DeepSeek-Prover, Kimina-style models, LeanDojo-based agents, and related systems are useful for formal proof generation benchmarks, especially when theorem statements are already formalized.

### Representative Proved or Formalized Problems

- AlphaProof / AlphaGeometry2: IMO 2024 P1, P2, P4, and P6; P1, P2, and P6 are Lean-oriented AlphaProof targets, while P4 is specialized geometry.
- Gemini Deep Think: official IMO 2025 gold-medal-standard natural-language solutions, not a public end-to-end Lean proof suite.
- Aletheia: FirstProof Problems 2, 5, 7, 8, 9, and 10 by majority expert assessment; also several Erdős-problem results or follow-up collaborations reported in public materials.
- Aristotle plus GPT workflows: Erdős Problem 728 is the cleanest public example of a Lean-verified AI workflow with a later informal writeup.
- Gauss: strong Prime Number Theorem formalization and sphere-packing formalization slices; these are large-scale formalization achievements rather than small autonomous theorem-discovery tasks.
- Seed-Prover: compilable Lean proofs for selected IMO 2025 and Putnam 2025 problems, with a public repository for proof artifacts.
- Claude Code / GPT / Aristotle workflows: the Vlasov-Maxwell-Landau equilibrium formalization is a documented example where Gemini produced a proof plan, Claude Code translated and organized Lean code, Aristotle closed many lemmas, and Lean verified the final project.
- Erdős AI contribution tracking: many 2025-2026 entries now list GPT, Claude, Gemini, Aristotle, AlphaEvolve, Aletheia, or other systems, but outcomes range from full Lean solutions to partial results and incorrect proofs; benchmark labels must preserve that distinction.

### Practical Conclusion for AMRA

`AMRA` should be evaluated as an orchestration and proof-engineering system, not as a standalone genius prover. The benchmark should measure:

- statement recovery,
- theorem-header formalization,
- proof route selection,
- lemma decomposition quality,
- Lean repair ability,
- whether generated lemmas close the target or merely accumulate.

The BMO campaign failure mode we observed is exactly what this benchmark should catch: a build-clean helper trail can still be mathematically irrelevant or routed through a false intermediate claim.

## Primary Sources

- Google DeepMind AlphaProof/AlphaGeometry IMO 2024: https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/
- AlphaProof Nature paper: https://www.nature.com/articles/s41586-025-09833-y
- Gemini Deep Think IMO 2025: https://deepmind.google/discover/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/
- Aletheia paper: https://arxiv.org/abs/2602.10177
- Aletheia FirstProof paper: https://arxiv.org/abs/2602.21201
- Aletheia transcripts/project: https://github.com/google-deepmind/superhuman/tree/main/aletheia
- Aristotle paper: https://arxiv.org/abs/2510.01346
- Math Inc. Gauss: https://www.math.inc/gauss
- Strong PNT repository: https://github.com/math-inc/strongpnt
- Sphere packing announcement: https://www.math.inc/sphere-packing
- Seed-Prover 1.5 announcement: https://seed.bytedance.com/en/blog/seed-prover-1-5-advanced-mathematical-reasoning-through-a-novel-agentic-architecture
- Seed-Prover repository: https://github.com/ByteDance-Seed/Seed-Prover
- FirstProof: https://1stproof.org/first-batch.html
- OpenAI FirstProof submissions: https://openai.com/index/first-proof-submissions/
- Erdos AI contributions wiki: https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems
- VML semi-autonomous formalization: https://arxiv.org/abs/2603.15929
- Automatic textbook formalization: https://arxiv.org/abs/2604.03071
