from __future__ import annotations

from pathlib import Path
from typing import Any

from amra.core.context import build_context_audit, read_exact_statement
from amra.deliverables import DeliverableAssessor
from amra.core.workspace import load_project_manifest, read_json, record_event, update_pipeline_status, utc_now_iso, write_json, write_text


class MathWriter:
    def __init__(self) -> None:
        self.assessor = DeliverableAssessor()

    def _mathematical_context(
        self,
        *,
        manifest: dict[str, Any],
        exact_statement: str,
        claims: list[dict[str, Any]],
        tasks: list[dict[str, Any]],
        idea_ledger: dict[str, Any],
    ) -> str:
        parts: list[str] = [
            str(manifest["problem"].get("title", "")),
            str(manifest["problem"].get("domain", "")),
            exact_statement,
            " ".join(str(tag) for tag in manifest["problem"].get("tags", [])),
            " ".join(str(item) for item in idea_ledger.get("themes", [])),
        ]
        parts.extend(str(claim.get("statement", "")) for claim in claims)
        parts.extend(str(task.get("description", "")) for task in tasks)
        return "\n".join(parts).lower()

    def _default_figure_plan(self, context: str) -> list[dict[str, str]]:
        figures: list[dict[str, str]] = []
        graph_markers = ("graph", "simplegraph", "vertex", "vertices", "neighbor", "neighbour", "dominat", "clique")
        if any(marker in context for marker in graph_markers):
            if ("neighbor" in context or "neighbour" in context) and ("indep" in context or "clique" in context):
                figures.append(
                    {
                        "label": "fig:local-neighborhood",
                        "title": "Local neighborhood obstruction",
                        "caption": (
                            "Two non-adjacent neighbors would form an independent pair inside an open "
                            "neighborhood, contradicting the local independence bound."
                        ),
                        "tikz": r"""\begin{tikzpicture}[scale=1.0, every node/.style={circle, draw, inner sep=1.8pt}]
\node (v) at (0,0) {$v$};
\node (x) at (-1.4,1.0) {$x$};
\node (y) at (1.4,1.0) {$y$};
\draw (v) -- (x);
\draw (v) -- (y);
\draw[dashed] (x) -- node[above,draw=none,fill=none] {$?$} (y);
\end{tikzpicture}""",
                    }
                )
            if "connected" in context or "path" in context or "shortest" in context:
                figures.append(
                    {
                        "label": "fig:shortest-path-chord",
                        "title": "Shortest path chord",
                        "caption": (
                            "A local clique at the second vertex of a shortest path creates a chord, "
                            "which shortens the path and forces completeness."
                        ),
                        "tikz": r"""\begin{tikzpicture}[scale=1.0, every node/.style={circle, draw, inner sep=1.8pt}]
\node (p0) at (0,0) {$p_0$};
\node (p1) at (1.5,0) {$p_1$};
\node (p2) at (3.0,0) {$p_2$};
\node (p3) at (4.5,0) {$\cdots$};
\draw (p0) -- (p1) -- (p2) -- (p3);
\draw[bend left=35, thick] (p0) to (p2);
\end{tikzpicture}""",
                    }
                )
            if "dominat" in context or "complete" in context or "top" in context:
                figures.append(
                    {
                        "label": "fig:complete-total-domination",
                        "title": "Minimal total domination in a complete graph",
                        "caption": (
                            "In a complete graph, one selected vertex cannot dominate itself, while any "
                            "two selected vertices totally dominate all vertices."
                        ),
                        "tikz": r"""\begin{tikzpicture}[scale=1.0, every node/.style={circle, draw, inner sep=1.8pt}]
\node[fill=black!15] (a) at (90:1.35) {$a$};
\node[fill=black!15] (b) at (210:1.35) {$b$};
\node (c) at (330:1.35) {$c$};
\node (d) at (0,0) {$d$};
\foreach \u/\v in {a/b,a/c,a/d,b/c,b/d,c/d}{\draw (\u)--(\v);}
\end{tikzpicture}""",
                    }
                )
        elif any(marker in context for marker in ("triangle", "geometry", "dissection", "equilateral")):
            figures.append(
                {
                    "label": "fig:geometric-configuration",
                    "title": "Geometric configuration",
                    "caption": "A schematic geometric decomposition can track the main incidence and congruence constraints.",
                    "tikz": r"""\begin{tikzpicture}[scale=1.1]
\coordinate (A) at (0,0);
\coordinate (B) at (4,0);
\coordinate (C) at (2,3.46);
\draw (A)--(B)--(C)--cycle;
\draw (2,0)--(C);
\draw (1,1.73)--(3,1.73);
\end{tikzpicture}""",
                }
            )
        elif any(marker in context for marker in ("prime", "divisor", "divides", "number theory", "integer")):
            figures.append(
                {
                    "label": "fig:divisibility-structure",
                    "title": "Divisibility structure",
                    "caption": "A divisibility diagram records the implication chain used by the arithmetic proof.",
                    "tikz": r"""\begin{tikzpicture}[node distance=1.5cm, every node/.style={draw, rounded corners=2pt, inner sep=4pt}]
\node (h) {hypotheses};
\node[right of=h, xshift=1.8cm] (d) {divisibility lemmas};
\node[right of=d, xshift=1.8cm] (c) {conclusion};
\draw[->] (h) -- (d);
\draw[->] (d) -- (c);
\end{tikzpicture}""",
                }
            )
        figures.append(
            {
                "label": "fig:proof-dependency",
                "title": "Proof dependency outline",
                "caption": "The main theorem is organized as a chain of reusable lemmas leading to the final claim.",
                "tikz": r"""\begin{tikzpicture}[node distance=1.4cm, every node/.style={draw, rounded corners=2pt, inner sep=4pt}]
\node (l1) {local lemma};
\node[right of=l1, xshift=1.7cm] (l2) {structural lemma};
\node[right of=l2, xshift=1.7cm] (m) {main theorem};
\draw[->] (l1) -- (l2);
\draw[->] (l2) -- (m);
\end{tikzpicture}""",
            }
        )
        return figures[:4]

    def _figure_plan(
        self,
        project_dir: Path,
        *,
        manifest: dict[str, Any],
        exact_statement: str,
        claims: list[dict[str, Any]],
        tasks: list[dict[str, Any]],
        idea_ledger: dict[str, Any],
    ) -> list[dict[str, str]]:
        for path in (project_dir / "writing" / "figure_plan.json", project_dir / "artifacts" / "figure_plan.json"):
            payload = read_json(path, default={})
            figures = payload.get("figures", []) if isinstance(payload, dict) else []
            if figures:
                return [dict(item) for item in figures if isinstance(item, dict)]
        context = self._mathematical_context(
            manifest=manifest,
            exact_statement=exact_statement,
            claims=claims,
            tasks=tasks,
            idea_ledger=idea_ledger,
        )
        return self._default_figure_plan(context)

    def _figure_lines(self, figures: list[dict[str, str]]) -> list[str]:
        if not figures:
            return []
        lines = ["## Figures and Intuition", ""]
        for index, figure in enumerate(figures, start=1):
            lines.extend(
                [
                    f"### Figure {index}. {figure.get('title', 'Mathematical figure')}",
                    "",
                    figure.get("caption", "").strip() or "Add a caption explaining the mathematical role of this figure.",
                    "",
                ]
            )
            tikz = str(figure.get("tikz", "")).strip()
            if tikz:
                lines.extend(["```latex", tikz, "```", ""])
            label = str(figure.get("label", "")).strip()
            if label:
                lines.extend([f"Label: `{label}`", ""])
        return lines

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
        figures = self._figure_plan(
            project_dir,
            manifest=manifest,
            exact_statement=exact_statement,
            claims=claims,
            tasks=tasks,
            idea_ledger=idea_ledger,
        )
        figure_lines = self._figure_lines(figures)
        write_json(
            project_dir / "artifacts" / "manuscript_figure_plan.json",
            {
                "generated_at": utc_now_iso(),
                "project_name": manifest["project_name"],
                "figure_count": len(figures),
                "figures": figures,
            },
        )

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
                *figure_lines,
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
                *figure_lines,
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
            "figure_count": len(figures),
            "figure_plan_path": str(project_dir / "artifacts" / "manuscript_figure_plan.json"),
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
