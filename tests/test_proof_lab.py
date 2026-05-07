from __future__ import annotations

from pathlib import Path

from ara_math.proof_lab import AIProofLabRunner, cluster_route_attempts, parse_labeled_fields, route_signature


def test_parse_clean_attempt_fields_multiline() -> None:
    text = """
Route title: density increment route
Claim status: partial
Key lemma: Every dense subset has a structured subprogression.
Dependency graph:
main theorem -> density increment -> structured subprogression
Proof sketch: The increment step follows by Fourier concentration.
Dependencies: Parseval, regularity lemma
Failure mode: The structured subprogression lemma is not proved.
Formalization target: theorem dense_subset_has_subprogression
Self-audit: continue, because the missing lemma is precise.
"""

    fields = parse_labeled_fields(text)

    assert fields["route_title"] == "density increment route"
    assert fields["claim_status"] == "partial"
    assert "structured subprogression" in fields["key_lemma"]
    assert "density increment" in fields["dependency_graph"]
    assert fields["formalization_target"] == "theorem dense_subset_has_subprogression"


def test_route_clustering_groups_by_key_lemma() -> None:
    attempts = [
        {
            "attempt": 1,
            "parsed_fields": {
                "claim_status": "partial",
                "route_title": "Fourier route",
                "key_lemma": "Large spectrum gives a density increment",
            },
        },
        {
            "attempt": 2,
            "parsed_fields": {
                "claim_status": "proof_candidate",
                "route_title": "Different prose",
                "key_lemma": "Large spectrum gives a density increment",
            },
        },
        {
            "attempt": 3,
            "parsed_fields": {
                "claim_status": "fatal_gap",
                "route_title": "Compactness route",
                "key_lemma": "A compactness reduction closes the finite case",
            },
        },
    ]

    clusters = cluster_route_attempts(attempts)

    assert clusters[0]["signature"] == route_signature(attempts[0]["parsed_fields"])
    assert clusters[0]["count"] == 2
    assert clusters[0]["best_status"] == "proof_candidate"
    assert clusters[0]["representative_attempt"] == 2


def test_zero_audits_selects_no_candidates(tmp_path: Path) -> None:
    runner = AIProofLabRunner(repo_root=tmp_path)

    candidates = runner._select_audit_candidates(
        attempts=[{"attempt": 1, "parsed_fields": {"claim_status": "partial"}}],
        clusters=[{"representative_attempt": 1}],
        audits=0,
    )

    assert candidates == []


def test_clean_prompt_encodes_clean_room_doctrine(tmp_path: Path) -> None:
    runner = AIProofLabRunner(repo_root=tmp_path)

    prompt = runner._build_clean_attempt_prompt(
        statement="For every n, prove P(n).",
        context_bundle_path=tmp_path / "context.md",
        grounding_path=None,
        attempt=1,
        attempts=3,
    )

    assert "clean-room" in prompt
    assert "Do not edit files" in prompt
    assert "do not assume it is open" in prompt
    assert "Cluster attempts by key lemma" in prompt
    assert "Route title:" in prompt
    assert "Formalization target:" in prompt


def test_source_grounding_prompt_extracts_existing_assets(tmp_path: Path) -> None:
    runner = AIProofLabRunner(repo_root=tmp_path)

    prompt = runner._build_source_grounding_prompt(
        statement="Prove theorem T using the provided Lean file.",
        context_bundle_path=tmp_path / "context.md",
    )

    assert "source-first grounding stage" in prompt
    assert "Existing formal assets:" in prompt
    assert "Do not redo:" in prompt
    assert "Open continuation target:" in prompt
    assert "Recommended attack target:" in prompt


def test_clean_prompt_requires_grounding_when_present(tmp_path: Path) -> None:
    runner = AIProofLabRunner(repo_root=tmp_path)

    prompt = runner._build_clean_attempt_prompt(
        statement="For every n, prove P(n).",
        context_bundle_path=tmp_path / "context.md",
        grounding_path=tmp_path / "grounding.md",
        attempt=1,
        attempts=2,
    )

    assert "Mandatory source-grounding artifact:" in prompt
    assert "Do not redo existing formal assets" in prompt
    assert str(tmp_path / "grounding.md") in prompt


def test_backend_none_run_writes_report(tmp_path: Path) -> None:
    runner = AIProofLabRunner(repo_root=tmp_path)

    report = runner.run(
        statement="For every n, prove P(n).",
        backend="none",
        attempts=2,
        audits=1,
        time_budget_sec=60,
        output_root=tmp_path / "proof_lab",
        run_name="smoke",
    )

    assert report["status"] == "completed"
    assert report["attempts_completed"] == 2
    assert report["audits_completed"] == 1
    assert Path(report["run_dir"]).joinpath("report.json").exists()
    assert Path(report["summary_path"]).exists()
    assert report["clusters"][0]["signature"] == "unavailable-without-backend"


def test_source_first_backend_none_writes_grounding_report(tmp_path: Path) -> None:
    runner = AIProofLabRunner(repo_root=tmp_path)

    report = runner.run(
        statement="For every n, prove P(n).",
        backend="none",
        attempts=1,
        audits=0,
        time_budget_sec=60,
        source_first=True,
        output_root=tmp_path / "proof_lab",
        run_name="source-first-smoke",
    )

    grounding = report["grounding"]
    assert grounding["parsed_fields"]["recommended_attack_target"] == "run source-first grounding with backend=codex"
    assert Path(grounding["artifacts"]["output"]).exists()
    assert report["audits_completed"] == 0
    attempt_prompt = Path(report["attempts"][0]["artifacts"]["prompt"]).read_text(encoding="utf-8")
    assert "Mandatory source-grounding artifact:" in attempt_prompt


def test_source_first_can_run_grounding_only(tmp_path: Path) -> None:
    runner = AIProofLabRunner(repo_root=tmp_path)

    report = runner.run(
        statement="For every n, prove P(n).",
        backend="none",
        attempts=0,
        audits=0,
        time_budget_sec=60,
        source_first=True,
        output_root=tmp_path / "proof_lab",
        run_name="grounding-only",
    )

    assert report["status"] == "completed"
    assert report["grounding"] is not None
    assert report["attempts_completed"] == 0
    assert report["audits_completed"] == 0
