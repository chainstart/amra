import json
from pathlib import Path

from ara_math.coordinator import add_workstream, initialize_comath_project, load_project_state, select_next_workstreams
from ara_math.comath_specialists import SpecialistProviderResult, run_specialist
from ara_math.obligation_refiner import materialize_obligations_from_specialist_run
from ara_math.workstreams import WorkstreamKind, WorkstreamRecord
from ara_math.workspace import write_text


def test_obligation_refiner_materializes_bellman_next_actions(tmp_path: Path) -> None:
    project_dir = tmp_path / "bellman-obligations"
    initialize_comath_project(project_dir, project_name="Bellman", original_goal="Formalize the BMO Bellman theorem.")

    parsed_output = {
        "fields": {
            "next_actions": (
                "Write the full piecewise `frontierPhiMajorant`, including cup and right-side formula; "
                "Prove induced-convex domain coverage, local concavity, C1 gluing, and boundary domination; "
                "Add Lean declarations for the exact upper-bound chain."
            )
        },
        "blockers": [
            "BMO-BELLMAN-GLOBAL-PROOF-MISSING: no certified global majorant proof.",
            "CUP-RIGHT-GLUING-CONCAVITY-MISSING: no checked gluing lemma.",
        ],
    }

    payload = materialize_obligations_from_specialist_run(
        project_dir,
        parsed_output=parsed_output,
        source_role_id="proof_reviewer",
        source_run_id="review-bmo",
        source_workstream_id="global-review",
        output_path=str(project_dir / "review.md"),
    )
    state = load_project_state(project_dir)
    majorant = next(item for item in state.workstreams if "frontierphimajorant" in item.workstream_id)
    selected = select_next_workstreams(project_dir, limit=1)
    criteria_path = project_dir / "comath" / "workstreams" / majorant.workstream_id / "acceptance_criteria.md"
    messages = (project_dir / "comath" / "messages.jsonl").read_text(encoding="utf-8")

    assert len(payload["created"]) == 3
    assert majorant.kind == WorkstreamKind.PROOF
    assert majorant.owner == "theory_builder"
    assert majorant.metadata["role_id"] == "theory_builder"
    assert majorant.metadata["executor"] == "llm_specialist"
    assert majorant.metadata["generated_by"] == "obligation_refiner"
    assert majorant.metadata["scheduler_priority"] <= 3
    assert "BMO-BELLMAN-GLOBAL-PROOF-MISSING" in criteria_path.read_text(encoding="utf-8")
    assert selected[0].workstream_id == majorant.workstream_id
    assert '"type": "obligations_refined"' in messages


class _ReviewProvider:
    provider_name = "review-test"

    def run(self, bundle):
        write_text(
            bundle.output_path,
            "\n".join(
                [
                    "Status: completed",
                    "Summary: Reviewer rejects the current Bellman route.",
                    "Blockers: BMO-BELLMAN-GLOBAL-PROOF-MISSING: no certified global majorant proof.",
                    "Next actions: Write the full piecewise `frontierPhiMajorant`, including cup and right-side formula.",
                    "",
                ]
            ),
        )
        return SpecialistProviderResult(
            provider=self.provider_name,
            status="completed",
            output_path=str(bundle.output_path),
            returncode=0,
        )


def test_specialist_run_refines_review_blockers_into_workstream(tmp_path: Path) -> None:
    project_dir = tmp_path / "specialist-obligation"
    initialize_comath_project(project_dir, project_name="Specialist Obligation", original_goal="Prove the theorem.")
    add_workstream(
        project_dir,
        WorkstreamRecord(
            workstream_id="review-target",
            kind=WorkstreamKind.REVIEW,
            goal="Review the current proof route.",
            owner="proof_reviewer",
            metadata={"role_id": "proof_reviewer"},
        ),
    )

    payload = run_specialist(
        project_dir,
        role_id="proof_reviewer",
        workstream_id="review-target",
        provider=_ReviewProvider(),
        run_name="review-with-obligation",
    )
    result_path = Path(payload["run_dir"]) / "result.json"
    result_payload = json.loads(result_path.read_text(encoding="utf-8"))
    state = load_project_state(project_dir)
    generated = next(item for item in state.workstreams if "frontierphimajorant" in item.workstream_id)
    source = state.get_workstream("review-target")

    assert payload["result"]["obligation_refinement"]["created"] == [generated.workstream_id]
    assert result_payload["obligation_refinement"]["created"] == [generated.workstream_id]
    assert generated.status.value == "planned"
    assert generated.owner == "theory_builder"
    assert generated.metadata["executor"] == "llm_specialist"
    assert source is not None
    assert source.status.value == "revision"
