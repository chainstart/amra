from __future__ import annotations

from pathlib import Path
from typing import Any

from amra.core.workspace import read_text, utc_now_iso


class OpenProblemStrategyPlanner:
    """Synthesize a case-study-driven execution profile for open math problems."""

    CASE_STUDIES: tuple[dict[str, Any], ...] = (
        {
            "case_id": "erdos_728_lean_pipeline",
            "title": "Erdos #728 Lean pipeline",
            "source_url": "https://arxiv.org/abs/2601.07421",
            "lessons": [
                "An informal proof route becomes much more trustworthy once it is translated into Lean and kernel-checked.",
                "Prime-by-prime or local-to-global decompositions are often the right first checkpoint for a hard number-theory claim.",
            ],
        },
        {
            "case_id": "erdos_650_chatgpt_strategy_aristotle_verification",
            "title": "Erdos #650 strategy then Lean verification",
            "source_url": "https://arxiv.org/abs/2603.28636",
            "lessons": [
                "A useful division of labor is: language model proposes the strategy, formal prover or Lean validates the final argument.",
                "The best progress often comes from a single strong combinatorial idea, not from polishing many local shell lemmas.",
            ],
        },
        {
            "case_id": "erdos_ai_wiki_variant_and_error_pressure",
            "title": "Erdos AI wiki error patterns",
            "source_url": "https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems",
            "lessons": [
                "Open-problem work needs explicit variant checks because many apparent successes are only for easier or earlier formulations.",
                "Incorrect but plausible AI proofs are common enough that statement-alignment and human review must remain first-class gates.",
            ],
        },
        {
            "case_id": "ryu_gpt5_human_guided_brainstorming",
            "title": "GPT-5 as a mathematical brainstorming partner",
            "source_url": "https://openai.com/index/gpt-5-mathematical-discovery/",
            "lessons": [
                "Researchers get value by quickly killing bad branches and drilling into the few suggestions with structural promise.",
                "The model adds breadth and speed, especially by surfacing ideas from adjacent literature, but the human still verifies the math.",
            ],
        },
        {
            "case_id": "funsearch_evaluator_backed_search",
            "title": "FunSearch evaluator-backed discovery",
            "source_url": "https://www.nature.com/articles/s41586-023-06924-6",
            "lessons": [
                "When a problem admits an executable score or verifier, search should be driven by that evaluator instead of free-form prose alone.",
                "Diversity and many bounded attempts outperform a single monolithic reasoning pass on search-heavy mathematical tasks.",
            ],
        },
        {
            "case_id": "vml_abstract_concrete_split",
            "title": "Semi-autonomous formalization lessons",
            "source_url": "https://arxiv.org/abs/2603.15929",
            "lessons": [
                "Keep the abstract proof plan separate from the concrete Lean encoding until the theorem statement and definitions stabilize.",
                "Adversarial self-review and explicit definition-alignment checks are necessary because hypothesis drift is a recurrent failure mode.",
            ],
        },
    )

    def _route_ready(self, *, theorem_inventory: dict[str, Any], route_discovery_brief: dict[str, Any], selected_route: str) -> bool:
        theorem_inventory_count = int(theorem_inventory.get("entry_count", 0) or 0)
        route_candidate_count = len(route_discovery_brief.get("route_candidates", []))
        has_theorem_chain = "## Theorem Chain" in selected_route
        return theorem_inventory_count > 0 and route_candidate_count > 0 and has_theorem_chain

    def _has_evaluator_hint(self, *, proof_path: dict[str, Any], literature_evidence: dict[str, Any]) -> bool:
        for item in proof_path.get("proof_path_hypothesis", []):
            text = str(item).lower()
            if any(token in text for token in ("search", "certificate", "finite", "bounded", "enumerat", "compute", "sat")):
                return True
        for bucket in ("proof_ingredients", "modern_tools"):
            for item in literature_evidence.get(bucket, []):
                text = " ".join(
                    [
                        str(item.get("statement", "")),
                        str(item.get("source", "")),
                        str(item.get("title", "")),
                    ]
                ).lower()
                if any(token in text for token in ("search", "certificate", "finite", "bounded", "encoding", "sat", "computation")):
                    return True
        return False

    def _selected_cases(
        self,
        *,
        open_problem: bool,
        route_ready: bool,
        has_evaluator_hint: bool,
        source_attribution_count: int,
    ) -> list[dict[str, Any]]:
        selected_ids = [
            "erdos_ai_wiki_variant_and_error_pressure",
            "ryu_gpt5_human_guided_brainstorming",
            "vml_abstract_concrete_split",
        ]
        if open_problem:
            selected_ids.append("erdos_728_lean_pipeline")
            selected_ids.append("erdos_650_chatgpt_strategy_aristotle_verification")
        if has_evaluator_hint:
            selected_ids.append("funsearch_evaluator_backed_search")
        if source_attribution_count == 0:
            selected_ids.append("erdos_ai_wiki_variant_and_error_pressure")
        case_map = {entry["case_id"]: entry for entry in self.CASE_STUDIES}
        deduped: list[dict[str, Any]] = []
        seen: set[str] = set()
        for case_id in selected_ids:
            if case_id in seen or case_id not in case_map:
                continue
            seen.add(case_id)
            deduped.append(case_map[case_id])
        if route_ready and "erdos_728_lean_pipeline" not in seen:
            deduped.append(case_map["erdos_728_lean_pipeline"])
        return deduped[:5]

    def analyze(
        self,
        *,
        project_dir: Path,
        manifest: dict[str, Any],
        context_audit: dict[str, Any],
        review_report: dict[str, Any],
        build_report: dict[str, Any],
        proof_path: dict[str, Any],
        literature_evidence: dict[str, Any],
        theorem_inventory: dict[str, Any],
        route_discovery_brief: dict[str, Any],
    ) -> dict[str, Any]:
        problem = manifest.get("problem") or {}
        open_problem = bool(problem.get("open_problem", False))
        review_status = str(review_report.get("status", "not_run")).strip() or "not_run"
        build_status = str(build_report.get("status", "not_run")).strip() or "not_run"
        source_attribution_count = int(literature_evidence.get("source_attribution_count", 0) or 0)
        theorem_inventory_count = int(theorem_inventory.get("entry_count", 0) or 0)
        route_candidate_count = len(route_discovery_brief.get("route_candidates", []))
        selected_route = read_text(project_dir / "proof" / "selected_route.md")
        route_ready = self._route_ready(
            theorem_inventory=theorem_inventory,
            route_discovery_brief=route_discovery_brief,
            selected_route=selected_route,
        )
        has_evaluator_hint = self._has_evaluator_hint(proof_path=proof_path, literature_evidence=literature_evidence)

        if not open_problem:
            strategy_profile_id = "closed_problem_formalization"
            recommended_focus_mode = "default"
        elif not route_ready:
            strategy_profile_id = "route_before_formalization"
            recommended_focus_mode = "route_discovery"
        elif build_status == "blocked":
            strategy_profile_id = "paper_first_until_build_ready"
            recommended_focus_mode = "paper_first"
        elif review_status in {"blocked", "checkpoint_verified"}:
            strategy_profile_id = "literature_checkpoint_then_formalize"
            recommended_focus_mode = "paper_first"
        else:
            strategy_profile_id = "formalize_verified_checkpoint"
            recommended_focus_mode = "default"

        required_checks = [
            "Variant check: confirm the claimed result matches the exact target statement and is not only an easier or historical formulation.",
            "Definition-alignment check: verify every quantifier, side condition, and notation choice against the source theorem statement.",
            "Adversarial self-review: write down the likeliest failure point before treating an attempt as real progress.",
            "Abstract/concrete split: keep theorem-chain notes separate from Lean implementation until one checkpoint theorem is stable.",
            "Checkpoint discipline: advance exactly one theorem import, one checkpoint lemma, or one blocked-route report per attempt.",
        ]
        if has_evaluator_hint:
            required_checks.append(
                "Evaluator-first check: if a bounded search, certificate, or executable score exists, use it to prune candidates before prose elaboration."
            )

        failure_modes = [
            "Solving a nearby variant or previous formulation instead of the intended open problem.",
            "Hypothesis creep, where assumptions silently change between natural-language notes and Lean statements.",
            "Spending most of the budget on local Lean shell edits before the theorem chain is explicit.",
            "Keeping eloquent but wrong branches alive instead of rejecting them quickly.",
        ]
        if source_attribution_count == 0:
            failure_modes.append("Treating uncited mathematical folklore as if it were a verified imported theorem.")

        next_moves: list[str] = []
        if not route_ready:
            next_moves.append(
                "Produce a selected route with one explicit checkpoint theorem and a theorem-to-theorem dependency chain before aggressive Lean repair."
            )
        if source_attribution_count == 0:
            next_moves.append("Raise source attribution by anchoring the next checkpoint to a named paper or theorem rather than an unattributed idea.")
        if build_status == "blocked":
            next_moves.append("Keep working in route notes and checkpoint statements while the verifier remains blocked; do not invent unsupported Lean shells.")
        if review_status == "checkpoint_verified":
            next_moves.append("Extend the current checkpoint by importing one literature-backed lemma instead of polishing surrounding boilerplate.")
        if has_evaluator_hint:
            next_moves.append("Prefer many bounded evaluator-backed attempts over one long unconstrained proof narrative.")
        if not next_moves:
            next_moves.append("Advance the strongest checkpoint theorem into Lean and keep provenance explicit.")

        principles = [
            "Use the model for breadth, structural rewrites, and literature connections; use Lean and explicit checks for truth.",
            "Treat open-problem progress as a sequence of verified checkpoints, not as a one-shot main-theorem leap.",
            "Kill dead ends quickly and preserve only branches with explicit mathematical structure or verifier support.",
        ]
        if route_ready:
            principles.append("Once a route is explicit, formalize the first checkpoint theorem before broadening the search again.")
        if has_evaluator_hint:
            principles.append("Objective evaluators should dominate selection whenever the problem family admits them.")

        case_studies = self._selected_cases(
            open_problem=open_problem,
            route_ready=route_ready,
            has_evaluator_hint=has_evaluator_hint,
            source_attribution_count=source_attribution_count,
        )
        highlighted_lessons = [lesson for case in case_studies for lesson in case.get("lessons", [])][:8]

        return {
            "generated_at": utc_now_iso(),
            "project_name": str(manifest.get("project_name", "")),
            "problem_id": str(problem.get("problem_id", "")),
            "open_problem": open_problem,
            "strategy_version": "case-study-v1",
            "strategy_profile_id": strategy_profile_id,
            "recommended_focus_mode": recommended_focus_mode,
            "principles": principles,
            "required_checks": required_checks,
            "failure_modes": failure_modes,
            "next_moves": next_moves,
            "highlighted_lessons": highlighted_lessons,
            "selected_case_studies": case_studies,
            "gates": {
                "has_exact_or_recovered_statement": bool(
                    context_audit.get("has_exact_statement", False) or context_audit.get("has_recovered_statement", False)
                ),
                "route_ready": route_ready,
                "source_attribution_count": source_attribution_count,
                "theorem_inventory_count": theorem_inventory_count,
                "route_candidate_count": route_candidate_count,
                "has_evaluator_hint": has_evaluator_hint,
            },
            "evidence_snapshot": {
                "review_status": review_status,
                "build_status": build_status,
                "literature_source_attribution_count": source_attribution_count,
                "theorem_inventory_count": theorem_inventory_count,
                "route_candidate_count": route_candidate_count,
            },
        }
