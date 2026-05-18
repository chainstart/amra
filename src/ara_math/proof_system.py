from __future__ import annotations

from pathlib import Path
from typing import Any

from ara_math.workspace import utc_now_iso


REFERENCE_SYSTEMS: tuple[dict[str, Any], ...] = (
    {
        "system_id": "leandojo_reprover",
        "label": "LeanDojo / ReProver",
        "source_url": "https://leandojo.org/leandojo.html",
        "patterns": [
            "Trace repositories and theorem states explicitly.",
            "Retrieve premises against the current proof state instead of prompting against the whole repo.",
            "Use best-first proof search rather than a single monolithic draft.",
        ],
    },
    {
        "system_id": "leanagent",
        "label": "LeanAgent",
        "source_url": "https://github.com/lean-dojo/LeanAgent",
        "patterns": [
            "Maintain a dependency graph of accessible premises.",
            "Run best-first tree search and keep progress memory across attempts.",
            "Prefer theorems and states with strong retriever support.",
        ],
    },
    {
        "system_id": "deepseek_prover_v15",
        "label": "DeepSeek-Prover-V1.5",
        "source_url": "https://arxiv.org/abs/2408.08152",
        "patterns": [
            "Use verifier feedback as the main search signal.",
            "Keep a frontier of diverse branches instead of retrying the same trajectory blindly.",
            "Reward novel states and shift away from stalled branches.",
        ],
    },
    {
        "system_id": "ulamai",
        "label": "UlamAI",
        "source_url": "https://github.com/ulamai/ulamai",
        "patterns": [
            "Start with one deep whole-theorem attempt.",
            "Fall back to claim decomposition only after verification failure or clear stalling.",
            "Persist whiteboard-style run memory and resumable artifacts.",
        ],
    },
    {
        "system_id": "numina_lean_agent",
        "label": "Numina-Lean-Agent",
        "source_url": "https://arxiv.org/abs/2601.14027",
        "patterns": [
            "Treat the proving system as a general coding agent with explicit tools and retrieval.",
            "Make blueprint / dependency planning first-class, not just hidden chain-of-thought.",
            "Use auxiliary tools and theorem search as part of the proving loop.",
        ],
    },
)


class ProofSystemPlanner:
    """Benchmark AMRA against standard prover architectures and derive an execution policy."""

    def build_benchmark_report(
        self,
        *,
        manifest: dict[str, Any],
        proof_path_assessment: dict[str, Any],
        theorem_inventory: dict[str, Any],
        theorem_graph: dict[str, Any],
        proof_path_frameworks: dict[str, Any],
        route_scaffold: dict[str, Any],
        route_discovery_brief: dict[str, Any],
        checkpoint_contract: dict[str, Any],
    ) -> dict[str, Any]:
        problem = manifest.get("problem") or {}
        open_problem = bool(problem.get("open_problem", False))
        theorem_inventory_count = int(theorem_inventory.get("entry_count", 0) or 0)
        theorem_graph_edge_count = int(theorem_graph.get("edge_count", 0) or 0)
        framework_count = int(proof_path_frameworks.get("framework_count", 0) or 0)
        route_candidate_count = len(route_discovery_brief.get("route_candidates", []))
        checkpoint_statement = str(checkpoint_contract.get("checkpoint_statement", "")).strip()
        dependency_chain = list(checkpoint_contract.get("dependency_chain", []))
        theorem_scope = "checkpoint_theorem" if open_problem and checkpoint_statement else "main_theorem"
        whole_theorem_first = bool(checkpoint_statement or not open_problem)

        capabilities = [
            {
                "capability_id": "theorem_dependency_dag",
                "status": "implemented" if theorem_graph_edge_count > 0 else "missing",
                "artifact_paths": ["proof/theorem_graph.json", "proof/route_candidates.json"],
                "why_it_matters": "Standard provers do not search the whole repo blindly; they operate against an explicit dependency structure.",
            },
            {
                "capability_id": "checkpoint_contract",
                "status": "implemented" if checkpoint_statement else "partial",
                "artifact_paths": ["proof/checkpoint_contract.json", "proof/checkpoint_contract.md"],
                "why_it_matters": "Open-problem systems need a theorem-sized target before proof search becomes meaningful.",
            },
            {
                "capability_id": "whole_theorem_then_decompose",
                "status": "planned",
                "artifact_paths": ["proof/proof_search_agenda.json", "proof/current_focus.md"],
                "why_it_matters": "UlamAI-style systems attempt the current theorem target directly before decomposing into finer claims.",
            },
            {
                "capability_id": "best_first_frontier",
                "status": "planned",
                "artifact_paths": ["proof/proof_search_agenda.json", "proof/verifier_feedback.json"],
                "why_it_matters": "DeepSeek/LeanDojo-style systems search a frontier of candidate branches instead of reusing one fixed prompt.",
            },
            {
                "capability_id": "persistent_run_memory",
                "status": "implemented",
                "artifact_paths": ["proof/proof_search_attempts.jsonl", "proof/attempts/"],
                "why_it_matters": "Agentic provers preserve attempt history and use it to avoid repeating failed branches.",
            },
            {
                "capability_id": "retrieval_and_accessible_premises",
                "status": "planned",
                "artifact_paths": ["proof/premise_retrieval.json", "proof/accessible_premise_graph.json"],
                "why_it_matters": "LeanDojo/LeanAgent-style premise control is a bottleneck for serious Lean proving.",
            },
            {
                "capability_id": "evaluator_hooks",
                "status": "implemented" if "computational_search" in list(problem.get("tags", [])) else "planned",
                "artifact_paths": ["proof/evaluator_plan.json", "proof/evaluator_report.json"],
                "why_it_matters": "Search-friendly math should use executable evaluators or bounded certificates as first-class tools.",
            },
        ]

        execution_policy = {
            "search_policy": "best_first_frontier",
            "whole_theorem_first": whole_theorem_first,
            "theorem_scope": theorem_scope,
            "decomposition_fallback": "after_verifier_failure_or_frontier_stall",
            "frontier_width": 6,
            "novelty_bonus": True,
            "verifier_feedback_memory": True,
            "persistent_focus_file": "proof/current_focus.md",
        }

        phases = [
            {
                "phase_id": "architecture_alignment",
                "goal": "Keep proving behavior aligned with standard Lean-agent architectures.",
                "deliverables": [
                    "proof/proof_system_benchmark.json",
                    "proof/proof_system_benchmark.md",
                ],
            },
            {
                "phase_id": "search_frontier",
                "goal": "Select the next proving move from a scored frontier rather than a fixed loop.",
                "deliverables": [
                    "proof/proof_search_agenda.json",
                    "proof/verifier_feedback.json",
                ],
            },
            {
                "phase_id": "execution_memory",
                "goal": "Persist verifier feedback so future attempts can shift mode after stalls.",
                "deliverables": [
                    "proof/proof_search_attempts.jsonl",
                    "proof/attempts/",
                    "proof/current_focus.md",
                ],
            },
        ]

        adjustments: list[str] = []
        if theorem_inventory_count == 0:
            adjustments.append("Raise theorem inventory coverage before treating proof search as a real prover loop.")
        if route_candidate_count == 0:
            adjustments.append("Rebuild route discovery before long proof attempts; standard provers do not search without a route scaffold.")
        if not checkpoint_statement and open_problem:
            adjustments.append("Generate a checkpoint theorem before any whole-theorem proving attempt.")
        if not adjustments:
            adjustments.append("Use the benchmarked execution policy as the default proving loop for this project.")

        return {
            "generated_at": utc_now_iso(),
            "project_name": str(manifest.get("project_name", "")),
            "problem_id": str(problem.get("problem_id", "")),
            "open_problem": open_problem,
            "baseline_systems": list(REFERENCE_SYSTEMS),
            "current_snapshot": {
                "proof_path_status": str(proof_path_assessment.get("status", "")),
                "theorem_inventory_count": theorem_inventory_count,
                "theorem_graph_edge_count": theorem_graph_edge_count,
                "framework_count": framework_count,
                "route_candidate_count": route_candidate_count,
                "checkpoint_dependency_count": len(dependency_chain),
            },
            "execution_policy": execution_policy,
            "capabilities": capabilities,
            "recommended_adjustments": adjustments,
            "planned_phases": phases,
        }

    def render_benchmark_markdown(self, *, report: dict[str, Any]) -> str:
        lines = [
            "# Proof-System Benchmark",
            "",
            f"- Project: `{report.get('project_name', '')}`",
            f"- Problem: `{report.get('problem_id', '')}`",
            f"- Search policy: `{(report.get('execution_policy') or {}).get('search_policy', '')}`",
            f"- Whole-theorem first: `{(report.get('execution_policy') or {}).get('whole_theorem_first', False)}`",
            f"- Theorem scope: `{(report.get('execution_policy') or {}).get('theorem_scope', '')}`",
            "",
            "## Baseline Systems",
            "",
        ]
        for item in report.get("baseline_systems", [])[:5]:
            lines.append(f"- `{item.get('label', '')}`: {item.get('source_url', '')}")
            for pattern in item.get("patterns", [])[:3]:
                lines.append(f"  Pattern: {pattern}")
        lines.extend(["", "## Capabilities", ""])
        for capability in report.get("capabilities", []):
            lines.append(
                f"- `{capability.get('capability_id', '')}` [{capability.get('status', '')}]: {capability.get('why_it_matters', '')}"
            )
        lines.extend(["", "## Recommended Adjustments", ""])
        for item in report.get("recommended_adjustments", []):
            lines.append(f"- {item}")
        lines.append("")
        return "\n".join(lines) + "\n"


class ProofSearchAgendaPlanner:
    """Build a best-first frontier and verifier-feedback memory for proof search."""

    def _attempt_counts(self, previous_attempts: list[dict[str, Any]]) -> tuple[dict[str, int], dict[str, int]]:
        by_item: dict[str, int] = {}
        by_kind: dict[str, int] = {}
        for attempt in previous_attempts:
            item_id = str(attempt.get("selected_agenda_item_id", "")).strip()
            kind = str(attempt.get("selected_agenda_item_kind", "")).strip()
            if item_id:
                by_item[item_id] = by_item.get(item_id, 0) + 1
            if kind:
                by_kind[kind] = by_kind.get(kind, 0) + 1
        return by_item, by_kind

    def build_feedback(
        self,
        *,
        previous_attempts: list[dict[str, Any]],
        build_report: dict[str, Any],
        review_report: dict[str, Any],
        evaluator_report: dict[str, Any],
    ) -> dict[str, Any]:
        outcome_counts = {"converged": 0, "checkpoint": 0, "stalled": 0}
        for attempt in previous_attempts:
            outcome = str(attempt.get("outcome", "")).strip()
            if outcome in outcome_counts:
                outcome_counts[outcome] += 1
        by_item, by_kind = self._attempt_counts(previous_attempts)
        last_attempt = previous_attempts[-1] if previous_attempts else {}
        whole_theorem_stall_count = sum(
            1
            for attempt in previous_attempts
            if str(attempt.get("selected_agenda_item_kind", "")) == "whole_theorem_attempt"
            and str(attempt.get("outcome", "")) == "stalled"
        )
        if whole_theorem_stall_count > 0:
            recommended_mode = "decomposition_fallback"
            recommendation = "The whole-theorem branch has already stalled; move to checkpoint import or supporting-lemma decomposition."
        else:
            recommended_mode = "whole_theorem_first"
            recommendation = "Start from the current whole theorem target before decomposing into smaller obligations."
        if evaluator_report.get("status") == "completed" and outcome_counts["stalled"] > 0:
            recommendation = "Use evaluator-backed evidence to prioritize importable or checkpoint-strengthening branches."

        return {
            "generated_at": utc_now_iso(),
            "attempt_count": len(previous_attempts),
            "outcome_counts": outcome_counts,
            "attempts_by_item": by_item,
            "attempts_by_kind": by_kind,
            "last_attempt": {
                "attempt_index": last_attempt.get("attempt_index"),
                "outcome": last_attempt.get("outcome", ""),
                "selected_agenda_item_id": last_attempt.get("selected_agenda_item_id", ""),
                "selected_agenda_item_kind": last_attempt.get("selected_agenda_item_kind", ""),
            },
            "build_status": str(build_report.get("status", "not_run")),
            "review_status": str(review_report.get("status", "not_run")),
            "evaluator_status": str(evaluator_report.get("status", "")),
            "recommended_mode": recommended_mode,
            "recommendation": recommendation,
            "whole_theorem_stall_count": whole_theorem_stall_count,
        }

    def _priority(
        self,
        *,
        base: int,
        item_id: str,
        item_kind: str,
        feedback: dict[str, Any],
        support_score: int,
    ) -> int:
        attempts_by_item = feedback.get("attempts_by_item", {})
        attempts_by_kind = feedback.get("attempts_by_kind", {})
        item_attempts = int(attempts_by_item.get(item_id, 0))
        kind_attempts = int(attempts_by_kind.get(item_kind, 0))
        novelty_bonus = max(0, 18 - item_attempts * 6)
        repeated_penalty = item_attempts * 10 + max(0, kind_attempts - item_attempts) * 2
        if feedback.get("recommended_mode") == "decomposition_fallback" and item_kind == "whole_theorem_attempt":
            repeated_penalty += 18
        return max(0, base + support_score + novelty_bonus - repeated_penalty)

    def build_agenda(
        self,
        *,
        manifest: dict[str, Any],
        recovered_statement: str,
        route_scaffold: dict[str, Any],
        route_discovery_brief: dict[str, Any],
        checkpoint_contract: dict[str, Any],
        theorem_hints: list[dict[str, Any]],
        porting_candidates: list[dict[str, Any]],
        premise_retrieval: dict[str, Any],
        accessible_premise_graph: dict[str, Any],
        evaluator_plan: dict[str, Any],
        evaluator_report: dict[str, Any],
        feedback: dict[str, Any],
        benchmark_report: dict[str, Any],
    ) -> dict[str, Any]:
        problem = manifest.get("problem") or {}
        open_problem = bool(problem.get("open_problem", False))
        checkpoint_statement = str(checkpoint_contract.get("checkpoint_statement", "")).strip()
        first_edit_targets = [str(item) for item in route_scaffold.get("first_edit_targets", []) if str(item).strip()]
        dependency_chain = [str(item) for item in checkpoint_contract.get("dependency_chain", []) if str(item).strip()]
        accessible_count = len(accessible_premise_graph.get("accessible_premises", []))
        import_candidates = list(accessible_premise_graph.get("import_candidates", []))
        retrieved_premises = list(premise_retrieval.get("local_lean_premises", []))
        items: list[dict[str, Any]] = []

        target_statement = checkpoint_statement or recovered_statement or str(problem.get("statement", "")).strip()
        if target_statement:
            item_id = "whole-theorem-target"
            support_score = min(24, len(dependency_chain) * 4 + accessible_count)
            items.append(
                {
                    "item_id": item_id,
                    "kind": "whole_theorem_attempt",
                    "label": "Whole theorem checkpoint attempt",
                    "target_statement": target_statement,
                    "target_files": first_edit_targets[:2] or ["formal/MathProject/MainClaim.lean"],
                    "rationale": "Start with one deep theorem-sized attempt before decomposition, following UlamAI-style policy.",
                    "decomposition_level": "theorem",
                    "support_score": support_score,
                    "priority_score": self._priority(
                        base=88 if feedback.get("recommended_mode") == "whole_theorem_first" else 66,
                        item_id=item_id,
                        item_kind="whole_theorem_attempt",
                        feedback=feedback,
                        support_score=support_score,
                    ),
                    "exit_criteria": [
                        "Either the checkpoint theorem becomes Lean-verifiable or the verifier feedback shows the branch is stalled.",
                        "If it stalls, move to dependency import or evaluator-backed decomposition rather than retrying the same branch blindly.",
                    ],
                }
            )

        for index, dependency in enumerate(dependency_chain[:3], start=1):
            item_id = f"checkpoint-dependency-{index}"
            support_score = min(20, 8 + accessible_count + len(retrieved_premises[:2]))
            items.append(
                {
                    "item_id": item_id,
                    "kind": "checkpoint_dependency",
                    "label": f"Checkpoint dependency {index}",
                    "target_statement": dependency,
                    "target_files": first_edit_targets[:2] or ["formal/MathProject/GeneratedClaims.lean"],
                    "rationale": "Decompose the current theorem into one dependency-sized import or supporting lemma.",
                    "decomposition_level": "dependency",
                    "support_score": support_score,
                    "priority_score": self._priority(
                        base=78,
                        item_id=item_id,
                        item_kind="checkpoint_dependency",
                        feedback=feedback,
                        support_score=support_score,
                    ),
                    "exit_criteria": [
                        "Record or import one dependency theorem with explicit provenance.",
                    ],
                }
            )

        for index, item in enumerate(import_candidates[:2], start=1):
            import_hint = str(item.get("import_hint", "")).strip() or str(item.get("name", "")).strip()
            item_id = f"premise-import-{index}"
            support_score = 10
            if item.get("compiled"):
                support_score += 6
            if item.get("staged"):
                support_score += 4
            if item.get("import_ready"):
                support_score += 6
            items.append(
                {
                    "item_id": item_id,
                    "kind": "premise_import",
                    "label": f"Premise import {index}",
                    "target_statement": import_hint,
                    "target_files": first_edit_targets[:2] or ["formal/MathProject/GeneratedClaims.lean"],
                    "rationale": "Use accessible or nearly accessible premises before writing unsupported local shells.",
                    "decomposition_level": "premise",
                    "support_score": support_score,
                    "priority_score": self._priority(
                        base=74,
                        item_id=item_id,
                        item_kind="premise_import",
                        feedback=feedback,
                        support_score=support_score,
                    ),
                    "exit_criteria": [
                        "Import or restate one premise and keep its provenance explicit in the project files.",
                    ],
                }
            )

        if evaluator_plan.get("search_friendly", False):
            item_id = "evaluator-certificate"
            support_score = 12
            if evaluator_plan.get("ready_to_run"):
                support_score += 10
            if evaluator_report.get("status") == "completed":
                support_score += 6
            items.append(
                {
                    "item_id": item_id,
                    "kind": "evaluator_certificate",
                    "label": "Evaluator-backed checkpoint",
                    "target_statement": str(evaluator_plan.get("checkpoint_statement", "")).strip() or target_statement,
                    "target_files": ["proof/counterexample_search_contract.json", "proof/evaluator_report.json"],
                    "rationale": "Use executable bounded search or certificate checking as a first-class branch when available.",
                    "decomposition_level": "certificate",
                    "support_score": support_score,
                    "priority_score": self._priority(
                        base=82,
                        item_id=item_id,
                        item_kind="evaluator_certificate",
                        feedback=feedback,
                        support_score=support_score,
                    ),
                    "exit_criteria": [
                        "Either the evaluator produces a bounded certificate / rejection or the contract is tightened for the next run.",
                    ],
                }
            )

        if route_discovery_brief.get("route_candidates"):
            item_id = "route-refinement"
            items.append(
                {
                    "item_id": item_id,
                    "kind": "route_refinement",
                    "label": "Route refinement",
                    "target_statement": str(route_discovery_brief.get("objective", "")).strip() or target_statement,
                    "target_files": ["proof/selected_route.md", "proof/proof_gap_notes.md"],
                    "rationale": "If the frontier is weak, refine the theorem chain instead of polishing local Lean shells.",
                    "decomposition_level": "route",
                    "support_score": 8,
                    "priority_score": self._priority(
                        base=58,
                        item_id=item_id,
                        item_kind="route_refinement",
                        feedback=feedback,
                        support_score=8,
                    ),
                    "exit_criteria": [
                        "Leave a clearer theorem chain, blocker note, or route rejection for the next attempt.",
                    ],
                }
            )

        items.sort(key=lambda item: (-int(item["priority_score"]), str(item["item_id"])))
        selected_item = items[0] if items else {}
        execution_mode = (
            "whole_theorem_first"
            if selected_item.get("kind") == "whole_theorem_attempt"
            else "decomposition_fallback"
        )
        if not items:
            execution_mode = "route_only"

        return {
            "generated_at": utc_now_iso(),
            "project_name": str(manifest.get("project_name", "")),
            "problem_id": str(problem.get("problem_id", "")),
            "open_problem": open_problem,
            "search_policy": str((benchmark_report.get("execution_policy") or {}).get("search_policy", "best_first_frontier")),
            "execution_mode": execution_mode,
            "selected_item_id": str(selected_item.get("item_id", "")),
            "selected_item": selected_item,
            "frontier_width": int((benchmark_report.get("execution_policy") or {}).get("frontier_width", 6)),
            "frontier": items[: int((benchmark_report.get("execution_policy") or {}).get("frontier_width", 6))],
            "feedback_recommendation": str(feedback.get("recommendation", "")),
            "whole_theorem_scope": str((benchmark_report.get("execution_policy") or {}).get("theorem_scope", "")),
            "transposition_keys": [item.get("item_id", "") for item in items[:8]],
        }

    def render_current_focus_markdown(
        self,
        *,
        benchmark_report: dict[str, Any],
        feedback: dict[str, Any],
        agenda: dict[str, Any],
    ) -> str:
        selected = agenda.get("selected_item") or {}
        lines = [
            "# Current Focus",
            "",
            f"- Search policy: `{agenda.get('search_policy', '')}`",
            f"- Execution mode: `{agenda.get('execution_mode', '')}`",
            f"- Selected agenda item: `{selected.get('item_id', '')}` / `{selected.get('kind', '')}`",
            f"- Label: {selected.get('label', '')}",
            f"- Target statement: {selected.get('target_statement', '')}",
            f"- Feedback recommendation: {feedback.get('recommendation', '')}",
            "",
            "## Target Files",
            "",
        ]
        target_files = selected.get("target_files", [])
        if target_files:
            for item in target_files:
                lines.append(f"- {item}")
        else:
            lines.append("- None recorded yet.")
        lines.extend(
            [
                "",
                "## Exit Criteria",
                "",
            ]
        )
        exit_criteria = selected.get("exit_criteria", [])
        if exit_criteria:
            for item in exit_criteria:
                lines.append(f"- {item}")
        else:
            lines.append("- None recorded yet.")
        lines.extend(
            [
                "",
                "## Benchmark Alignment",
                "",
                f"- Whole-theorem first: `{(benchmark_report.get('execution_policy') or {}).get('whole_theorem_first', False)}`",
                f"- Theorem scope: `{agenda.get('whole_theorem_scope', '')}`",
                "",
            ]
        )
        manual_override = agenda.get("manual_focus_override") or {}
        if manual_override:
            lines.extend(
                [
                    "## Manual Focus Override",
                    "",
                    f"- Source: `{manual_override.get('path', '')}`",
                ]
            )
            reason = str(manual_override.get("reason", "")).strip()
            if reason:
                lines.append(f"- Reason: {reason}")
            for note in manual_override.get("notes", [])[:5]:
                lines.append(f"- Note: {note}")
            lines.append("")
        return "\n".join(lines) + "\n"
