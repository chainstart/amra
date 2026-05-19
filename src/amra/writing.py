from __future__ import annotations

from pathlib import Path
from typing import Any

from amra.core.context import build_context_audit, read_exact_statement
from amra.deliverables import DeliverableAssessor
from amra.core.workspace import load_project_manifest, read_json, record_event, update_pipeline_status, utc_now_iso, write_json, write_text


class MathWriter:
    def __init__(self) -> None:
        self.assessor = DeliverableAssessor()

    def write_manuscript(self, project_dir: Path) -> dict[str, Any]:
        manifest = load_project_manifest(project_dir)
        plan = read_json(project_dir / "proof" / "proof_plan.json", default={"tasks": [], "notes": []})
        registry = read_json(project_dir / "proof" / "claim_registry.json", default={"claims": []})
        build_report = read_json(project_dir / "artifacts" / "lean_build_report.json", default={})
        assessment = self.assessor.assess(project_dir)
        context_audit = build_context_audit(project_dir)
        proof_path = read_json(project_dir / "idea" / "proof_path_assessment.json", default={})
        idea_ledger = read_json(project_dir / "idea" / "math_idea_ledger.json", default={})
        literature_evidence = read_json(project_dir / "idea" / "literature_evidence.json", default={})
        convergence_plan = read_json(project_dir / "artifacts" / "convergence_plan.json", default={})
        external_requirements = read_json(project_dir / "artifacts" / "external_requirements.json", default={})
        exact_statement = read_exact_statement(project_dir).strip() or manifest["problem"]["statement"]
        claims = registry.get("claims", [])
        tasks = plan.get("tasks", [])

        claim_lines = ["## Claim Registry", ""]
        if claims:
            for claim in claims:
                claim_lines.extend(
                    [
                        f"### {claim['title']}",
                        "",
                        f"- Claim ID: `{claim['claim_id']}`",
                        f"- Status: `{claim['status']}`",
                        f"- Validation mode: `{claim['validation_mode']}`",
                        f"- Statement: {claim['statement']}",
                        "",
                    ]
                )
        else:
            claim_lines.extend(["No claims have been registered yet.", ""])

        task_lines = ["## Proof Strategy", ""]
        for task in tasks:
            task_lines.extend(
                [
                    f"### {task['title']}",
                    "",
                    f"- Task type: `{task['task_type']}`",
                    f"- Validation mode: `{task['validation_mode']}`",
                    f"- Success contract: {task['success_contract']}",
                    f"- Description: {task['description']}",
                    "",
                ]
            )

        references = read_json(project_dir / "idea" / "references.json", default={"references": []}).get("references", [])
        reference_lines = ["## References", ""]
        if references:
            reference_lines.extend([f"- {item}" for item in references])
            reference_lines.append("")
        else:
            reference_lines.extend(["- Add references here.", ""])

        evidence_lines = ["## Literature Evidence", ""]
        if literature_evidence:
            counts = literature_evidence.get("counts", {})
            evidence_lines.extend(
                [
                    f"- Known results recovered: `{counts.get('known_results', 0)}`",
                    f"- Proof ingredients recovered: `{counts.get('proof_ingredients', 0)}`",
                    f"- Modern tool hints recovered: `{counts.get('modern_tools', 0)}`",
                    f"- Open gaps recovered: `{counts.get('open_gaps', 0)}`",
                    "",
                ]
            )
            for heading, key in (
                ("### Known Results", "known_results"),
                ("### Proof Ingredients", "proof_ingredients"),
                ("### Modern Tools", "modern_tools"),
                ("### Open Gaps", "open_gaps"),
            ):
                items = literature_evidence.get(key, [])
                if not items:
                    continue
                evidence_lines.extend([heading, ""])
                for item in items[:4]:
                    evidence_lines.append(f"- {item['statement']}  Source: {item['source']}")
                evidence_lines.append("")
        else:
            evidence_lines.extend(["- No structured literature evidence has been generated yet.", ""])

        proof_path_lines = ["## Proof Path Assessment", ""]
        if proof_path:
            proof_path_lines.extend([f"- Readiness tier: `{proof_path.get('readiness_tier', 'unknown')}`"])
            proof_path_lines.extend([f"- {item}" for item in proof_path.get("historical_foundations", [])[:3]])
            proof_path_lines.extend([f"- {item}" for item in proof_path.get("modern_toolkit", [])[:4]])
            proof_path_lines.extend([f"- Blocker: {item}" for item in proof_path.get("blockers", [])[:3]])
            proof_path_lines.append("")
        else:
            proof_path_lines.extend(["- No proof-path assessment has been generated yet.", ""])

        idea_lines = ["## Mathematical Ideas", ""]
        themes = idea_ledger.get("themes", [])
        if themes:
            idea_lines.extend([f"- {item}" for item in themes[:8]])
            idea_lines.append("")
        else:
            idea_lines.extend(["- No reusable idea seeds have been recorded yet.", ""])

        convergence_lines = ["## Convergence Plan", ""]
        if convergence_plan:
            convergence_lines.extend(
                [
                    f"- Current phase: `{convergence_plan.get('phase', 'unknown')}`",
                    f"- Ready for long run: `{convergence_plan.get('ready_for_long_run', False)}`",
                    f"- Current milestone: {convergence_plan.get('current_milestone', 'unknown')}",
                    "",
                ]
            )
            convergence_lines.extend([f"- Next objective: {item}" for item in convergence_plan.get("next_formal_objectives", [])[:5]])
            convergence_lines.append("")
        else:
            convergence_lines.extend(["- No convergence plan has been generated yet.", ""])

        external_lines = ["## External Requirements", ""]
        requirements = external_requirements.get("requirements", []) if isinstance(external_requirements, dict) else []
        if requirements:
            for item in requirements:
                external_lines.extend(
                    [
                        f"- `{item.get('kind', 'unknown')}`: {item.get('title', '')}",
                        f"  Status: `{item.get('status', 'unknown')}`",
                        f"  Reason: {item.get('reason', '')}",
                    ]
                )
            external_lines.append("")
        else:
            external_lines.extend(["- No external papers, data, or cache setup have been flagged yet.", ""])

        header_lines = [
            f"# {manifest['problem']['title']}",
            "",
            f"Deliverable type: `{assessment['deliverable_type']}`",
            "",
        ]
        if assessment["deliverable_type"] == "research_report":
            body_lines = [
                "## Summary",
                "",
                "This output is a research report rather than a paper draft. It records verified progress, proof assets, and next steps without claiming standalone publishability.",
                "",
                "## Exact Statement",
                "",
                exact_statement,
                "",
                "## Verified Progress",
                "",
                *claim_lines,
                "## Formalization Status",
                "",
                f"- Exact statement available: `{context_audit['has_exact_statement']}`",
                f"- Lean build status: `{build_report.get('status', 'not_run')}`",
                f"- Sorry count: `{build_report.get('sorry_count', 'unknown')}`",
                "",
                "## Project Notes",
                "",
                *task_lines,
                *evidence_lines,
                *proof_path_lines,
                *idea_lines,
                *convergence_lines,
                *external_lines,
                "## Assessment",
                "",
                *[f"- {item}" for item in assessment["rationale"]],
                "",
                *reference_lines,
            ]
        elif assessment["deliverable_type"] == "formalization_note":
            body_lines = [
                "## Abstract",
                "",
                "This draft is a short formalization note intended for a modest theorem or a compact Lean verification result.",
                "",
                "## Statement",
                "",
                exact_statement,
                "",
                "## Formalization",
                "",
                "Summarize the Lean development, imported definitions, and the structure of the formal proof here.",
                "",
                *claim_lines,
                "## Verification Status",
                "",
                f"- Lean build status: `{build_report.get('status', 'not_run')}`",
                f"- Sorry count: `{build_report.get('sorry_count', 'unknown')}`",
                "",
                *evidence_lines,
                *proof_path_lines,
                *idea_lines,
                *convergence_lines,
                *external_lines,
                "## Scope",
                "",
                *[f"- {item}" for item in assessment["rationale"]],
                "",
                *reference_lines,
            ]
        else:
            body_lines = [
                "## Abstract",
                "",
                "This draft is generated by AMRA as a working manuscript blueprint. It is not publication-ready.",
                "",
                "## Introduction",
                "",
                f"This project studies `{manifest['problem']['problem_id']}` from `{manifest['problem']['source']}`.",
                "",
                "## Exact Statement",
                "",
                exact_statement,
                "",
                "## Preliminaries",
                "",
                "Document the definitions, imported Mathlib components, and normalization choices here.",
                "",
                "## Main Results",
                "",
                "Only Lean-verified statements without `sorry`, `admit`, or placeholder propositions should remain in the final manuscript.",
                "",
                *claim_lines,
                "## Formalization Status",
                "",
                f"- Exact statement available: `{context_audit['has_exact_statement']}`",
                f"- Lean build status: `{build_report.get('status', 'not_run')}`",
                f"- Sorry count: `{build_report.get('sorry_count', 'unknown')}`",
                "",
                *evidence_lines,
                *proof_path_lines,
                *idea_lines,
                *convergence_lines,
                *external_lines,
                *task_lines,
                "## Discussion",
                "",
                "Summarize mathematical progress, current proof gaps, and which claims remain conjectural.",
                "",
                *reference_lines,
            ]

        document_path = project_dir / "writing" / assessment["document_name"]
        manuscript = "\n".join([*header_lines, *body_lines]).strip() + "\n"
        write_text(document_path, manuscript)
        report = {
            "generated_at": utc_now_iso(),
            "project_name": manifest["project_name"],
            "claim_count": len(claims),
            "task_count": len(tasks),
            "has_exact_statement": context_audit["has_exact_statement"],
            "lean_status": build_report.get("status", "not_run"),
            "deliverable_type": assessment["deliverable_type"],
            "auto_deliverable_type": assessment["auto_deliverable_type"],
            "deliverable_override_active": assessment["override"]["active"],
            "deliverable_override_mode": assessment["override"]["mode"],
            "paper_workflow_recommended": assessment["paper_workflow_recommended"],
            "manuscript_path": str(document_path),
        }
        write_json(project_dir / "artifacts" / "manuscript_report.json", report)
        update_pipeline_status(
            project_dir,
            stage="writing",
            status="completed",
            details={
                "claim_count": len(claims),
                "task_count": len(tasks),
                "deliverable_type": assessment["deliverable_type"],
            },
        )
        record_event(
            project_dir,
            stage="writing",
            event="manuscript_generated",
            details={
                "claim_count": len(claims),
                "task_count": len(tasks),
                "deliverable_type": assessment["deliverable_type"],
            },
        )
        return report
