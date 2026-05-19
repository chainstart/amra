from __future__ import annotations

from pathlib import Path
from typing import Any

from amra.core.context import build_context_audit
from amra.lean.executor import LeanExecutor
from amra.core.workspace import load_deliverable_override, load_project_manifest, read_json, utc_now_iso, write_json


class DeliverableAssessor:
    """Classify the appropriate output form for a project.

    This avoids routing every verified theorem into a paper workflow.
    """

    DOCUMENT_NAMES = {
        "research_report": "research_report.md",
        "formalization_note": "formalization_note.md",
        "paper_candidate": "manuscript.md",
    }

    SUMMARY_LABELS = {
        "research_report": "Research report",
        "formalization_note": "Formalization note",
        "paper_candidate": "Paper candidate",
    }

    def assess(self, project_dir: Path) -> dict[str, Any]:
        manifest = load_project_manifest(project_dir)
        context_audit = build_context_audit(project_dir)
        registry = read_json(project_dir / "proof" / "claim_registry.json", default={"claims": []})
        build_report = read_json(project_dir / "artifacts" / "lean_build_report.json", default={})
        review_report = read_json(project_dir / "artifacts" / "review_report.json", default={})
        override = load_deliverable_override(project_dir)

        problem = manifest["problem"]
        tags = set(problem.get("tags", []))
        formalized = str(problem.get("formalized", "no"))
        open_problem = bool(problem.get("open_problem", True))
        claims = registry.get("claims", [])
        lean_claim_count = sum(1 for claim in claims if claim.get("validation_mode") == "lean")
        lean_verified_count = sum(1 for claim in claims if claim.get("status") == "lean_verified")
        claim_count = len(claims)
        reference_count = int(context_audit.get("reference_count", 0))
        build_passed = build_report.get("status") == "passed"
        blocker_count = len(review_report.get("blockers", []))
        formal_root = project_dir / "formal"
        lean_executor = LeanExecutor()
        placeholder_count = lean_executor.count_pattern(formal_root, LeanExecutor.PLACEHOLDER_PATTERN) if formal_root.exists() else 0
        sorry_count = lean_executor.count_sorries(formal_root) if formal_root.exists() else 0
        axiom_count = (
            lean_executor.count_pattern(formal_root, LeanExecutor.AXIOM_PATTERN, strip_comments=True)
            if formal_root.exists()
            else 0
        )
        admit_count = (
            lean_executor.count_pattern(formal_root, LeanExecutor.ADMIT_PATTERN, strip_comments=True)
            if formal_root.exists()
            else 0
        )
        effective_lean_verified_count = lean_verified_count
        if (
            effective_lean_verified_count == 0
            and build_passed
            and placeholder_count == 0
            and sorry_count == 0
            and axiom_count == 0
            and admit_count == 0
        ):
            effective_lean_verified_count = lean_claim_count

        auto_rationale: list[str] = []

        if not context_audit["has_exact_statement"]:
            auto_deliverable_type = "research_report"
            auto_rationale.append("The exact mathematical statement is not finalized yet.")
        elif not build_passed:
            auto_deliverable_type = "research_report"
            auto_rationale.append("Lean verification has not passed, so the output should remain a report.")
        elif blocker_count > 0:
            auto_deliverable_type = "research_report"
            auto_rationale.append("The review stage still reports blockers.")
        elif open_problem:
            if reference_count >= 6 and effective_lean_verified_count >= 4 and "starter_theorem" not in tags:
                auto_deliverable_type = "paper_candidate"
                auto_rationale.append(
                    "This is an open problem with a nontrivial verified core and enough references to consider paper scoping."
                )
            else:
                auto_deliverable_type = "research_report"
                auto_rationale.append(
                    "Open-problem progress is present, but the current scope is not yet strong enough for a paper workflow."
                )
        else:
            if "starter_theorem" in tags:
                auto_deliverable_type = "research_report"
                auto_rationale.append("This is explicitly marked as a starter theorem, so a report is the default output.")
            elif formalized in {"yes", "partial"}:
                auto_deliverable_type = "research_report"
                auto_rationale.append(
                    "This looks like a simple or incremental formalization of known mathematics rather than a standalone paper."
                )
            elif reference_count >= 2 and effective_lean_verified_count >= 3 and claim_count >= 3:
                auto_deliverable_type = "formalization_note"
                auto_rationale.append("The theorem appears complete enough for a short formalization note.")
            else:
                auto_deliverable_type = "research_report"
                auto_rationale.append("The verified content is still best treated as a technical report.")

        override_active = override["mode"] != "auto"
        if override_active:
            deliverable_type = override["mode"]
            rationale = [
                f"Manual override selected `{deliverable_type}` output.",
                f"Automatic assessment would have produced `{auto_deliverable_type}`.",
            ]
            if override["reason"]:
                rationale.append(f"Override reason: {override['reason']}")
        else:
            deliverable_type = auto_deliverable_type
            rationale = list(auto_rationale)

        document_name = self.DOCUMENT_NAMES[deliverable_type]

        assessment = {
            "generated_at": utc_now_iso(),
            "project_name": manifest["project_name"],
            "problem_id": problem["problem_id"],
            "deliverable_type": deliverable_type,
            "auto_deliverable_type": auto_deliverable_type,
            "document_name": document_name,
            "paper_workflow_recommended": deliverable_type == "paper_candidate",
            "summary_label": self.SUMMARY_LABELS[deliverable_type],
            "rationale": rationale,
            "auto_rationale": auto_rationale,
            "override": {
                "active": override_active,
                "mode": override["mode"],
                "reason": override["reason"],
                "updated_at": override["updated_at"],
            },
            "signals": {
                "open_problem": open_problem,
                "formalized": formalized,
                "reference_count": reference_count,
                "claim_count": claim_count,
                "lean_verified_count": lean_verified_count,
                "effective_lean_verified_count": effective_lean_verified_count,
                "lean_claim_count": lean_claim_count,
                "build_passed": build_passed,
                "review_blocker_count": blocker_count,
                "placeholder_count": placeholder_count,
                "sorry_count": sorry_count,
                "axiom_count": axiom_count,
                "admit_count": admit_count,
            },
        }
        write_json(project_dir / "artifacts" / "deliverable_assessment.json", assessment)
        return assessment
