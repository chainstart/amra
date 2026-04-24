from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ara_math.context import build_context_audit
from ara_math.deliverables import DeliverableAssessor
from ara_math.lean import LeanExecutor
from ara_math.workspace import load_project_manifest, read_json, read_text, record_event, update_pipeline_status, utc_now_iso, write_json, write_text


class MathReviewer:
    def __init__(self) -> None:
        self.lean_executor = LeanExecutor()
        self.assessor = DeliverableAssessor()

    def _sync_claim_registry_statuses(
        self,
        project_dir: Path,
        status: str,
        registry: dict[str, Any],
        *,
        main_claim_partial: bool = False,
    ) -> None:
        claims = registry.get("claims", [])
        changed = False
        for claim in claims:
            if claim.get("validation_mode") != "lean":
                continue
            claim_id = str(claim.get("claim_id", ""))
            if status == "ready_for_human_review":
                desired = "lean_verified"
            elif status == "checkpoint_verified" and main_claim_partial and claim_id.endswith(":main"):
                desired = "formalization_in_progress"
            else:
                desired = claim.get("status", "candidate")
            if claim.get("status") != desired and (
                status == "ready_for_human_review" or (status == "checkpoint_verified" and main_claim_partial and claim_id.endswith(":main"))
            ):
                claim["status"] = desired
                changed = True
        if changed:
            registry["generated_at"] = utc_now_iso()
            write_json(project_dir / "proof" / "claim_registry.json", registry)

    def review(self, project_dir: Path) -> dict[str, Any]:
        manifest = load_project_manifest(project_dir)
        context_audit = build_context_audit(project_dir)
        plan = read_json(project_dir / "proof" / "proof_plan.json", default={"tasks": []})
        registry = read_json(project_dir / "proof" / "claim_registry.json", default={"claims": []})
        build_report = read_json(project_dir / "artifacts" / "lean_build_report.json", default={})
        formal_preparation = read_json(project_dir / "artifacts" / "formal_preparation.json", default={})
        proof_path_assessment = read_json(project_dir / "idea" / "proof_path_assessment.json", default={})
        idea_ledger = read_json(project_dir / "idea" / "math_idea_ledger.json", default={})
        literature_evidence = read_json(project_dir / "idea" / "literature_evidence.json", default={})
        assessment = self.assessor.assess(project_dir)
        manuscript_report = read_json(project_dir / "artifacts" / "manuscript_report.json", default={})
        manuscript_path = Path(manuscript_report.get("manuscript_path", project_dir / "writing" / assessment["document_name"]))
        manuscript = read_text(manuscript_path)
        formal_root = project_dir / "formal"
        main_claim_text = read_text(project_dir / "formal" / "MathProject" / "MainClaim.lean")

        placeholder_count = self.lean_executor.count_pattern(formal_root, LeanExecutor.PLACEHOLDER_PATTERN) if formal_root.exists() else 0
        axiom_count = (
            self.lean_executor.count_pattern(formal_root, LeanExecutor.AXIOM_PATTERN, strip_comments=True)
            if formal_root.exists()
            else 0
        )
        admit_count = (
            self.lean_executor.count_pattern(formal_root, LeanExecutor.ADMIT_PATTERN, strip_comments=True)
            if formal_root.exists()
            else 0
        )
        has_checkpoint_marker = "checkpoint" in main_claim_text.lower()
        has_benchmark_marker = "benchmark" in main_claim_text.lower() or "base case" in main_claim_text.lower()
        has_problem_shell = ": Prop :=" in main_claim_text or re.search(r"\bdef\s+\w*(problem|question)\w*\s*:\s*Prop\s*:=", main_claim_text)
        has_string_alignment_marker = "mainTargetStatement = targetStatement" in main_claim_text
        has_contract_marker = "proof contract" in main_claim_text.lower() or "future proof of" in main_claim_text.lower()
        has_reduction_marker = any(
            marker in main_claim_text.lower()
            for marker in (
                "reduction step for the main claim",
                "boundedness reduction for the main claim",
                "it is enough to show",
            )
        ) or bool(re.search(r"\btheorem\s+\w+_main_of_\w+", main_claim_text))
        main_claim_partial = any(
            (
                has_checkpoint_marker,
                has_benchmark_marker,
                bool(has_problem_shell),
                has_string_alignment_marker,
                has_contract_marker,
                has_reduction_marker,
            )
        )

        blockers: list[str] = []
        warnings: list[str] = []
        recommendations: list[str] = []

        if not context_audit["has_exact_statement"]:
            if context_audit.get("has_recovered_statement"):
                warnings.append("The project relies on a literature-recovered exact statement rather than a manually curated one.")
            else:
                blockers.append("The exact mathematical statement has not been supplied yet.")
        if not plan.get("tasks"):
            blockers.append("The proof plan is missing or empty.")
        if not formal_preparation:
            blockers.append("Formal preparation has not been run.")
        if not proof_path_assessment or proof_path_assessment.get("status") == "not_generated":
            warnings.append("A proof-path assessment has not been generated yet.")
        if not idea_ledger:
            warnings.append("The mathematical idea ledger is still empty.")
        evidence_counts = literature_evidence.get("counts", {}) if isinstance(literature_evidence, dict) else {}
        evidence_total = sum(int(value) for value in evidence_counts.values())
        if evidence_total == 0:
            warnings.append("No structured literature evidence has been recorded yet.")
        if manifest["problem"]["open_problem"] and int(literature_evidence.get("source_attribution_count", 0) or 0) == 0:
            warnings.append("Open-problem work should carry literature source attribution before publication claims are considered.")
        if not build_report:
            blockers.append("Lean build verification has not been run.")
        elif build_report.get("status") != "passed":
            blockers.append(f"Lean build status is `{build_report.get('status')}` instead of `passed`.")
        if build_report.get("sorry_count", 0) > 0:
            blockers.append("The Lean workspace still contains `sorry` placeholders.")
        if placeholder_count > 0 and not (
            build_report.get("sorry_count", 0) == 0
            and axiom_count == 0
            and admit_count == 0
            and main_claim_partial
        ):
            blockers.append("Generated placeholder claims are still present in the Lean sources.")
        elif placeholder_count > 0:
            warnings.append("The Lean workspace records a verified checkpoint, but the main claim remains an explicit partial-progress marker.")
        if build_report.get("status") == "passed" and main_claim_partial and placeholder_count == 0:
            warnings.append("The Lean workspace currently verifies only a benchmark/checkpoint shell around the main open problem, not a resolved main theorem.")
        if axiom_count > 0:
            blockers.append("The Lean workspace contains `axiom` declarations.")
        if admit_count > 0:
            blockers.append("The Lean workspace contains `admit` placeholders.")
        required_sections = {
            "research_report": ["## Summary", "## Exact Statement", "## Formalization Status"],
            "formalization_note": ["## Abstract", "## Statement", "## Verification Status"],
            "paper_candidate": ["## Abstract", "## Exact Statement", "## Formalization Status"],
        }[assessment["deliverable_type"]]
        missing_sections = [section for section in required_sections if section not in manuscript]
        if missing_sections:
            warnings.append(f"The generated document is missing required sections: {', '.join(missing_sections)}.")
        if context_audit["reference_count"] < 2:
            warnings.append("The project currently has fewer than two references recorded.")
        if manifest["problem"]["open_problem"]:
            warnings.append("This is an open problem. Any claimed main theorem still requires strong human validation even after Lean passes.")
        if assessment["deliverable_type"] != "paper_candidate":
            recommendations.append(
                f"Route this project to `{assessment['deliverable_type']}` output by default, not to a publication-grade paper workflow."
            )
        else:
            recommendations.append("This project may justify a paper workflow, but novelty and mathematical significance still need human confirmation.")

        if not blockers:
            if main_claim_partial and manifest["problem"]["open_problem"]:
                status = "checkpoint_verified"
                recommendations.append("Use this checkpoint as a bounded-progress milestone, not as a solved theorem claim.")
                recommendations.append("Next, replace the checkpoint marker by porting one literature-backed lemma or strengthening the formal definitions.")
            else:
                status = "ready_for_human_review"
                recommendations.append("Run a human mathematical audit of theorem statements and imported dependencies.")
                recommendations.append("Only promote claims to publishable results after checking they match the intended natural-language statement.")
        else:
            status = "blocked"
            recommendations.append("Resolve all blockers before treating the manuscript or theorem files as publishable progress.")

        report = {
            "generated_at": utc_now_iso(),
            "project_name": manifest["project_name"],
            "problem_id": manifest["problem"]["problem_id"],
            "status": status,
            "deliverable_type": assessment["deliverable_type"],
            "auto_deliverable_type": assessment["auto_deliverable_type"],
            "deliverable_override_active": assessment["override"]["active"],
            "deliverable_override_mode": assessment["override"]["mode"],
            "paper_workflow_recommended": assessment["paper_workflow_recommended"],
            "blockers": blockers,
            "warnings": warnings,
            "recommendations": recommendations,
            "checks": {
                "has_exact_statement": context_audit["has_exact_statement"],
                "has_recovered_statement": context_audit.get("has_recovered_statement", False),
                "reference_count": context_audit["reference_count"],
                "literature_evidence_count": evidence_total,
                "literature_source_attribution_count": int(literature_evidence.get("source_attribution_count", 0) or 0),
                "lean_status": build_report.get("status", "not_run"),
                "sorry_count": build_report.get("sorry_count", 0),
                "placeholder_count": placeholder_count,
                "axiom_count": axiom_count,
                "admit_count": admit_count,
                "claim_count": len(registry.get("claims", [])),
                "has_proof_path_assessment": bool(proof_path_assessment),
                "idea_seed_count": len(idea_ledger.get("themes", [])),
            },
        }
        self._sync_claim_registry_statuses(project_dir, status, registry, main_claim_partial=main_claim_partial)
        write_json(project_dir / "artifacts" / "review_report.json", report)
        write_text(
            project_dir / "writing" / "reviewer_notes.md",
            "\n".join(
                [
                    "# Reviewer Notes",
                    "",
                    f"- Status: `{status}`",
                    "",
                    "## Blockers",
                    "",
                    *([f"- {item}" for item in blockers] if blockers else ["- None"]),
                    "",
                    "## Warnings",
                    "",
                    *([f"- {item}" for item in warnings] if warnings else ["- None"]),
                    "",
                    "## Recommendations",
                    "",
                    *([f"- {item}" for item in recommendations] if recommendations else ["- None"]),
                    "",
                ]
            )
            + "\n",
        )
        update_pipeline_status(
            project_dir,
            stage="review",
            status=status,
            details={
                "blocker_count": len(blockers),
                "warning_count": len(warnings),
                "deliverable_type": assessment["deliverable_type"],
            },
        )
        record_event(
            project_dir,
            stage="review",
            event="review_completed",
            details={
                "status": status,
                "blocker_count": len(blockers),
                "deliverable_type": assessment["deliverable_type"],
            },
        )
        return report
