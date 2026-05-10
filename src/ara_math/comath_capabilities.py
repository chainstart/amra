from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ara_math.artifact_graph import (
    DependencyRelation,
    load_artifact_graph,
    save_artifact_graph,
)
from ara_math.coordinator import (
    add_workstream,
    comath_paths,
    initialize_comath_project,
    load_project_state,
    render_project_dashboard,
    save_project_state,
)
from ara_math.uncertainty import (
    SourceDebtStatus,
    UncertaintyItem,
    UncertaintyKind,
    append_failed_route_jsonl,
    load_uncertainty_ledger,
    save_uncertainty_ledger,
)
from ara_math.workspace import append_jsonl, read_json, slugify, write_json, write_text
from ara_math.workstreams import (
    ClaimRecord,
    ClaimStatus,
    DependencyStatus,
    ProjectStatus,
    WorkstreamKind,
    WorkstreamRecord,
    WorkstreamStatus,
    utc_now_iso,
)


REQUIRED_PAPER_CAPABILITIES = (
    "intent_refinement",
    "asynchronous_stateful_workspace",
    "parallel_workstreams",
    "specialist_agents",
    "llm_specialist_orchestration",
    "uncertainty_tracking",
    "failed_hypothesis_memory",
    "native_mathematical_artifacts",
    "literature_search",
    "computational_exploration",
    "theorem_proving",
    "theory_building",
    "review_gates",
    "progressive_disclosure",
    "evaluation_harness",
)


SPECIALIST_ROLE_DEFINITIONS: tuple[dict[str, Any], ...] = (
    {
        "role_id": "project_coordinator",
        "title": "Project Coordinator",
        "paper_capability": "Refines user intent, maintains project goals, delegates workstreams.",
        "input_contract": ["original_goal", "context_files", "uncertainty_ledger", "artifact_graph"],
        "output_contract": ["intake_plan", "workstream_plan", "top_blocker", "loop_report"],
        "review_requirements": ["global"],
    },
    {
        "role_id": "ideation_specialist",
        "title": "Ideation Specialist",
        "paper_capability": "Generates proof routes, alternative formulations, and new direction candidates.",
        "input_contract": ["refined_goal", "failed_routes", "known_claims"],
        "output_contract": ["route_candidates", "failed_route_updates", "new_direction_candidates"],
        "review_requirements": ["logic", "global"],
    },
    {
        "role_id": "source_auditor",
        "title": "Source Auditor",
        "paper_capability": "Searches literature, extracts theorem statements, and checks assumptions.",
        "input_contract": ["refined_goal", "context_files", "source_inventory"],
        "output_contract": ["source_inventory", "statement_alignment", "source_debt_items"],
        "review_requirements": ["source", "global"],
    },
    {
        "role_id": "computational_explorer",
        "title": "Computational Explorer",
        "paper_capability": "Runs reproducible computations and records command/input/output certificates.",
        "input_contract": ["question", "command_manifest", "seed", "input_hashes"],
        "output_contract": ["computation_manifest", "computation_certificate", "verification_report"],
        "review_requirements": ["computation", "global"],
    },
    {
        "role_id": "lean_formalizer",
        "title": "Lean Formalizer",
        "paper_capability": "Turns proof candidates into Lean artifacts and repairs verifier failures.",
        "input_contract": ["claim", "proof_sketch", "source_dependencies", "target_file"],
        "output_contract": ["lean_declaration", "build_report", "placeholder_audit"],
        "review_requirements": ["lean", "logic", "global"],
    },
    {
        "role_id": "proof_reviewer",
        "title": "Proof Reviewer",
        "paper_capability": "Reviews mathematical validity, statement drift, and hidden assumptions.",
        "input_contract": ["claim", "proof_sketch", "dependency_path", "source_status"],
        "output_contract": ["logic_review", "blockers", "approval_decision"],
        "review_requirements": ["logic", "source", "global"],
    },
    {
        "role_id": "theory_builder",
        "title": "Theory Builder",
        "paper_capability": "Maintains conjecture graph, reusable lemmas, failed hypotheses, and novelty notes.",
        "input_contract": ["artifact_graph", "failed_routes", "route_candidates"],
        "output_contract": ["theory_memory", "lemma_inventory", "new_direction_candidates"],
        "review_requirements": ["logic", "global"],
    },
)


def _json_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _resolve_project_path(project_dir: Path, value: str | Path, *, cwd: Path | None = None) -> Path:
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    base = cwd or project_dir
    return (base / path).resolve()


def _path_record(project_dir: Path, path: Path) -> dict[str, Any]:
    exists = path.exists()
    try:
        display_path = str(path.relative_to(project_dir))
    except ValueError:
        display_path = str(path)
    return {
        "path": display_path,
        "absolute_path": str(path),
        "exists": exists,
        "sha256": _file_sha256(path) if exists and path.is_file() else "",
        "size_bytes": path.stat().st_size if exists and path.is_file() else 0,
    }


def _upsert_claim(state: Any, claim: ClaimRecord) -> None:
    for index, existing in enumerate(state.claims):
        if existing.claim_id == claim.claim_id:
            claim.created_at = existing.created_at
            state.claims[index] = claim
            state.updated_at = utc_now_iso()
            return
    state.add_claim(claim)


def _read_context_files(context_files: list[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in context_files:
        records.append(
            {
                "path": str(path),
                "exists": path.exists(),
                "size_bytes": path.stat().st_size if path.exists() and path.is_file() else 0,
            }
        )
    return records


def install_specialist_role_contracts(project_dir: Path) -> dict[str, Any]:
    project_dir = Path(project_dir)
    initialize_comath_project(project_dir)
    paths = comath_paths(project_dir)
    payload = {
        "generated_at": utc_now_iso(),
        "paper_mapping": "arXiv:2605.06651 public architecture role contracts",
        "roles": [dict(role) for role in SPECIALIST_ROLE_DEFINITIONS],
    }
    write_json(paths.root / "specialist_roles.json", payload)
    write_text(
        paths.root / "specialist_roles.md",
        "\n".join(
            [
                "# CoMath Specialist Role Contracts",
                "",
                *[
                    "\n".join(
                        [
                            f"## {role['title']}",
                            "",
                            f"- Role id: `{role['role_id']}`",
                            f"- Paper capability: {role['paper_capability']}",
                            f"- Reviews: {', '.join(role['review_requirements'])}",
                            "",
                        ]
                    )
                    for role in SPECIALIST_ROLE_DEFINITIONS
                ],
            ]
        ),
    )
    append_jsonl(
        paths.messages,
        {"ts": utc_now_iso(), "type": "specialist_roles_installed", "role_count": len(SPECIALIST_ROLE_DEFINITIONS)},
    )
    render_project_dashboard(project_dir)
    return payload


def refine_intake_project(
    project_dir: Path,
    *,
    goal: str = "",
    project_name: str | None = None,
    domain: str = "",
    context_files: list[Path] | None = None,
) -> dict[str, Any]:
    project_dir = Path(project_dir)
    context_files = [Path(path).expanduser() for path in context_files or []]
    state = initialize_comath_project(project_dir, project_name=project_name, original_goal=goal or None)
    original_goal = (goal or state.original_goal or "").strip()
    refined_goal = original_goal
    if original_goal and not original_goal.lower().startswith(("prove", "classify", "construct", "decide", "source")):
        refined_goal = f"Resolve the mathematical objective: {original_goal}"
    elif not original_goal:
        refined_goal = "Resolve the mathematical objective supplied by the project context."

    assumptions = [
        "Every promoted claim must keep a dependency path to original-theorem.",
        "Source, computation, and Lean evidence must pass their type-specific review gates before final assembly.",
    ]
    if not context_files:
        assumptions.append("No context files were supplied; source audit must discover or certify all external theorem dependencies.")
    if domain:
        assumptions.append(f"Domain hint: {domain}.")

    workstreams = [
        WorkstreamRecord(
            workstream_id="ideation-route-discovery",
            kind=WorkstreamKind.PROOF,
            goal="Generate independent proof routes and record failed hypotheses for the refined goal.",
            owner="ideation_specialist",
            claim_ids=["route-space"],
            metadata={"role_id": "ideation_specialist", "executor": "proof_strategy", "paper_capability": "ideation"},
        ),
        WorkstreamRecord(
            workstream_id="source-literature-audit",
            kind=WorkstreamKind.SOURCE,
            goal="Search and certify literature/source support for the exact statement and each external theorem.",
            owner="source_auditor",
            claim_ids=["source-grounding"],
            metadata={
                "role_id": "source_auditor",
                "executor": "source_literature",
                "paper_capability": "literature_search",
                "context_paths": [str(path) for path in context_files],
            },
        ),
        WorkstreamRecord(
            workstream_id="computation-exploration",
            kind=WorkstreamKind.COMPUTE,
            goal="Run seeded computational probes with reproducible command manifests and verification certificates.",
            owner="computational_explorer",
            claim_ids=["computational-evidence"],
            metadata={"role_id": "computational_explorer", "executor": "computation_repro", "paper_capability": "computational_exploration"},
        ),
        WorkstreamRecord(
            workstream_id="lean-formalization",
            kind=WorkstreamKind.LEAN,
            goal="Formalize reviewed proof candidates in Lean and keep placeholder audits attached.",
            owner="lean_formalizer",
            dependencies=["source-literature-audit"],
            claim_ids=["lean-formalization-target"],
            metadata={"role_id": "lean_formalizer", "executor": "lean_formalization", "paper_capability": "theorem_proving"},
        ),
        WorkstreamRecord(
            workstream_id="theory-building-memory",
            kind=WorkstreamKind.PROOF,
            goal="Maintain conjecture graph, reusable lemma inventory, novelty notes, and new direction candidates.",
            owner="theory_builder",
            dependencies=["ideation-route-discovery"],
            claim_ids=["theory-memory"],
            metadata={"role_id": "theory_builder", "paper_capability": "theory_building"},
        ),
        WorkstreamRecord(
            workstream_id="global-review",
            kind=WorkstreamKind.REVIEW,
            goal="Assemble approved outputs and reject final claims with open source, computation, Lean, or statement-drift debt.",
            owner="project_coordinator",
            dependencies=[
                "ideation-route-discovery",
                "source-literature-audit",
                "computation-exploration",
                "lean-formalization",
                "theory-building-memory",
            ],
            claim_ids=["global-closure"],
            metadata={"role_id": "project_coordinator", "reviewers": ["logic", "source", "lean", "computation", "global"]},
        ),
    ]
    for workstream in workstreams:
        add_workstream(project_dir, workstream)

    state = load_project_state(project_dir)
    state.status = ProjectStatus.GOALS_PLANNED
    state.metadata["intake"] = {
        "refined_goal": refined_goal,
        "domain": domain,
        "context_files": [str(path) for path in context_files],
        "generated_at": utc_now_iso(),
    }
    for claim in [
        ClaimRecord(
            claim_id="route-space",
            title="Proof route search space",
            statement=refined_goal,
            status=ClaimStatus.ROUTE_CANDIDATE,
            owner_workstream_id="ideation-route-discovery",
        ),
        ClaimRecord(
            claim_id="source-grounding",
            title="Source grounding for original theorem",
            statement=refined_goal,
            status=ClaimStatus.HYPOTHESIS,
            owner_workstream_id="source-literature-audit",
            source_status=SourceDebtStatus.EXTERNAL_THEOREM_NEEDED.value,
        ),
        ClaimRecord(
            claim_id="computational-evidence",
            title="Computational evidence and reproducibility",
            statement="Computational probes must be reproducible before they can support a proof route.",
            status=ClaimStatus.HYPOTHESIS,
            owner_workstream_id="computation-exploration",
        ),
        ClaimRecord(
            claim_id="lean-formalization-target",
            title="Lean formalization target",
            statement=refined_goal,
            status=ClaimStatus.LEAN_STUBBED,
            owner_workstream_id="lean-formalization",
        ),
        ClaimRecord(
            claim_id="theory-memory",
            title="Theory-building memory",
            statement="Conjectures, reusable lemmas, failed hypotheses, and novelty notes for this project.",
            status=ClaimStatus.HYPOTHESIS,
            owner_workstream_id="theory-building-memory",
        ),
        ClaimRecord(
            claim_id="global-closure",
            title="Global project closure",
            statement=refined_goal,
            status=ClaimStatus.ROUTE_CANDIDATE,
            owner_workstream_id="global-review",
            dependency_ids=["source-grounding", "lean-formalization-target", "computational-evidence", "theory-memory"],
        ),
    ]:
        _upsert_claim(state, claim)
    save_project_state(project_dir, state)

    paths = comath_paths(project_dir)
    graph = load_artifact_graph(paths.artifact_graph)
    graph.record_claim(
        claim_id="route-space",
        title="Proof route search space",
        statement=refined_goal,
        status=ClaimStatus.ROUTE_CANDIDATE,
        workstream_id="ideation-route-discovery",
    )
    graph.record_claim(
        claim_id="source-grounding",
        title="Source grounding for original theorem",
        statement=refined_goal,
        status=ClaimStatus.HYPOTHESIS,
        workstream_id="source-literature-audit",
        metadata={"source_debt_status": SourceDebtStatus.EXTERNAL_THEOREM_NEEDED.value},
    )
    graph.record_claim(
        claim_id="computational-evidence",
        title="Computational evidence and reproducibility",
        statement="Computational probes must be reproducible before supporting proof claims.",
        status=ClaimStatus.HYPOTHESIS,
        workstream_id="computation-exploration",
    )
    graph.record_claim(
        claim_id="lean-formalization-target",
        title="Lean formalization target",
        statement=refined_goal,
        status=ClaimStatus.LEAN_STUBBED,
        workstream_id="lean-formalization",
    )
    graph.record_claim(
        claim_id="theory-memory",
        title="Theory-building memory",
        statement="Conjecture graph and novelty memory for the project.",
        status=ClaimStatus.HYPOTHESIS,
        workstream_id="theory-building-memory",
    )
    graph.record_claim(
        claim_id="global-closure",
        title="Global project closure",
        statement=refined_goal,
        status=ClaimStatus.ROUTE_CANDIDATE,
        workstream_id="global-review",
    )
    for source_id, target_id, relation, status, rationale in [
        ("source-grounding", "original-theorem", DependencyRelation.DEPENDS_ON, DependencyStatus.PENDING, "Source grounding must certify the original statement."),
        ("lean-formalization-target", "source-grounding", DependencyRelation.DEPENDS_ON, DependencyStatus.PENDING, "Lean proof depends on source-certified mathematical claims."),
        ("computational-evidence", "original-theorem", DependencyRelation.SUPPORTS, DependencyStatus.PENDING, "Computation may support route discovery but cannot replace proof."),
        ("theory-memory", "route-space", DependencyRelation.SUPPORTS, DependencyStatus.PENDING, "Theory memory suppresses duplicate failed routes and proposes new directions."),
        ("global-closure", "lean-formalization-target", DependencyRelation.DEPENDS_ON, DependencyStatus.PENDING, "Global review needs Lean status."),
        ("global-closure", "source-grounding", DependencyRelation.DEPENDS_ON, DependencyStatus.PENDING, "Global review needs source status."),
        ("global-closure", "computational-evidence", DependencyRelation.DEPENDS_ON, DependencyStatus.PENDING, "Global review needs reproducibility status when computation was used."),
        ("global-closure", "original-theorem", DependencyRelation.DEPENDS_ON, DependencyStatus.PENDING, "Global review must connect back to original theorem."),
    ]:
        graph.add_edge(source_id=source_id, target_id=target_id, relation=relation, status=status, rationale=rationale)
    save_artifact_graph(paths.artifact_graph, graph)

    ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
    ledger.upsert_item(
        UncertaintyItem(
            item_id="intake-source-certification",
            kind=UncertaintyKind.SOURCE_DEBT,
            title="Source certification is required for the refined goal",
            description="The intake stage has not yet certified that the exact statement and external theorem dependencies are sourced.",
            owner_workstream_id="source-literature-audit",
            claim_id="source-grounding",
            source_debt_status=SourceDebtStatus.EXTERNAL_THEOREM_NEEDED,
            severity="high",
        )
    )
    ledger.upsert_item(
        UncertaintyItem(
            item_id="intake-computation-reproducibility",
            kind=UncertaintyKind.COMPUTATION_DEBT,
            title="Computational probes require reproducible certificates before use",
            description="No verified computation manifest has been attached yet.",
            owner_workstream_id="computation-exploration",
            claim_id="computational-evidence",
            severity="medium",
        )
    )
    save_uncertainty_ledger(paths.uncertainty_ledger, ledger)

    role_payload = install_specialist_role_contracts(project_dir)
    intake_payload = {
        "generated_at": utc_now_iso(),
        "paper_mapping": "intent refinement and project decomposition",
        "original_goal": original_goal,
        "refined_goal": refined_goal,
        "domain": domain,
        "assumptions": assumptions,
        "context_files": _read_context_files(context_files),
        "workstream_ids": [workstream.workstream_id for workstream in workstreams],
        "role_ids": [role["role_id"] for role in role_payload["roles"]],
    }
    write_json(paths.root / "intake_plan.json", intake_payload)
    write_text(
        paths.root / "intake_plan.md",
        "\n".join(
            [
                "# CoMath Intake Plan",
                "",
                "## Refined Goal",
                "",
                refined_goal,
                "",
                "## Assumptions",
                "",
                *[f"- {item}" for item in assumptions],
                "",
                "## Workstreams",
                "",
                *[f"- `{workstream.workstream_id}`: {workstream.goal}" for workstream in workstreams],
                "",
            ]
        ),
    )
    append_jsonl(
        paths.messages,
        {
            "ts": utc_now_iso(),
            "type": "intake_refined",
            "workstream_ids": [workstream.workstream_id for workstream in workstreams],
        },
    )
    render_project_dashboard(project_dir, ledger=ledger)
    return {
        "project_dir": str(project_dir),
        "dashboard_path": str(paths.dashboard),
        "intake_plan": intake_payload,
        "roles": role_payload,
        "workstreams": [workstream.to_dict() for workstream in load_project_state(project_dir).workstreams],
    }


def _manifest_dir(project_dir: Path, workstream_id: str) -> Path:
    return comath_paths(project_dir).root / "computation" / slugify(workstream_id)


def create_computation_certificate(
    project_dir: Path,
    *,
    workstream_id: str,
    command: list[str],
    cwd: Path | None = None,
    input_paths: list[Path] | None = None,
    output_paths: list[Path] | None = None,
    seed: str = "",
    timeout_seconds: int = 120,
    run: bool = True,
) -> dict[str, Any]:
    project_dir = Path(project_dir)
    initialize_comath_project(project_dir)
    if not command:
        raise ValueError("A computation certificate requires a non-empty command.")
    exec_cwd = (cwd or project_dir).expanduser().resolve()
    run_dir = _manifest_dir(project_dir, workstream_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    manifest_id = f"{slugify(workstream_id)}-{utc_now_iso().replace(':', '').replace('+', 'z')}"
    resolved_inputs = [_resolve_project_path(project_dir, path, cwd=exec_cwd) for path in input_paths or []]
    resolved_outputs = [_resolve_project_path(project_dir, path, cwd=exec_cwd) for path in output_paths or []]
    run_payload: dict[str, Any] = {"executed": False, "returncode": None, "stdout": "", "stderr": ""}
    if run:
        completed = subprocess.run(
            command,
            cwd=exec_cwd,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        run_payload = {
            "executed": True,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "stdout_sha256": hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest(),
            "stderr_sha256": hashlib.sha256(completed.stderr.encode("utf-8")).hexdigest(),
        }
    manifest = {
        "manifest_id": manifest_id,
        "generated_at": utc_now_iso(),
        "workstream_id": workstream_id,
        "command": list(command),
        "cwd": str(exec_cwd),
        "seed": seed,
        "timeout_seconds": timeout_seconds,
        "inputs": [_path_record(project_dir, path) for path in resolved_inputs],
        "expected_outputs": [_path_record(project_dir, path) for path in resolved_outputs],
        "run": run_payload,
    }
    certificate = {
        "certificate_id": f"{manifest_id}-certificate",
        "manifest_id": manifest_id,
        "generated_at": utc_now_iso(),
        "workstream_id": workstream_id,
        "verified": bool(run_payload["executed"] and run_payload["returncode"] == 0),
        "command": list(command),
        "cwd": str(exec_cwd),
        "seed": seed,
        "input_hashes": {record["path"]: record["sha256"] for record in manifest["inputs"]},
        "output_hashes": {record["path"]: record["sha256"] for record in manifest["expected_outputs"]},
        "stdout_sha256": run_payload.get("stdout_sha256", ""),
        "returncode": run_payload["returncode"],
    }
    certificate["certificate_hash"] = _json_hash(certificate)
    manifest["certificate_hash"] = certificate["certificate_hash"]
    manifest_path = run_dir / f"{manifest_id}.manifest.json"
    certificate_path = run_dir / f"{manifest_id}.certificate.json"
    write_json(manifest_path, manifest)
    write_json(certificate_path, certificate)

    paths = comath_paths(project_dir)
    graph = load_artifact_graph(paths.artifact_graph)
    graph.record_computation_certificate(
        node_id=f"computation-certificate:{manifest_id}",
        label=f"Computation certificate for {workstream_id}",
        path=str(certificate_path),
        certificate_hash=certificate["certificate_hash"],
        workstream_id=workstream_id,
        metadata={
            "verified": certificate["verified"],
            "manifest_path": str(manifest_path),
            "command": list(command),
            "seed": seed,
        },
    )
    save_artifact_graph(paths.artifact_graph, graph)

    ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
    if certificate["verified"]:
        item = ledger.get_item("intake-computation-reproducibility")
        if item is not None:
            item.resolve()
            ledger.upsert_item(item)
    else:
        ledger.upsert_item(
            UncertaintyItem(
                item_id=f"computation-unverified:{manifest_id}",
                kind=UncertaintyKind.COMPUTATION_DEBT,
                title="Computation certificate did not verify",
                description=f"Command returned {run_payload['returncode']}; see {certificate_path}.",
                owner_workstream_id=workstream_id,
                severity="high",
                related_artifact_ids=[f"computation-certificate:{manifest_id}"],
            )
        )
    save_uncertainty_ledger(paths.uncertainty_ledger, ledger)

    state = load_project_state(project_dir)
    workstream = state.get_workstream(workstream_id)
    if workstream is not None:
        artifact_id = f"computation-certificate:{manifest_id}"
        workstream.artifact_ids = sorted(set([*workstream.artifact_ids, artifact_id]))
        workstream.artifact_paths = sorted(set([*workstream.artifact_paths, str(manifest_path), str(certificate_path)]))
        workstream.metadata["latest_computation_certificate"] = {
            "manifest_path": str(manifest_path),
            "certificate_path": str(certificate_path),
            "verified": certificate["verified"],
            "certificate_hash": certificate["certificate_hash"],
        }
        workstream.status = WorkstreamStatus.NEEDS_REVIEW if certificate["verified"] else WorkstreamStatus.REVISION
        state.upsert_workstream(workstream)
        save_project_state(project_dir, state)
        write_json(paths.workstream_dir(workstream_id) / "status.json", workstream.to_dict())

    append_jsonl(
        paths.messages,
        {
            "ts": utc_now_iso(),
            "type": "computation_certificate_recorded",
            "workstream_id": workstream_id,
            "verified": certificate["verified"],
            "manifest_path": str(manifest_path),
            "certificate_path": str(certificate_path),
        },
    )
    render_project_dashboard(project_dir, ledger=ledger)
    return {
        "project_dir": str(project_dir),
        "manifest_path": str(manifest_path),
        "certificate_path": str(certificate_path),
        "manifest": manifest,
        "certificate": certificate,
    }


def verify_computation_certificate(
    project_dir: Path,
    *,
    manifest_path: Path,
    rerun: bool = False,
    timeout_seconds: int | None = None,
) -> dict[str, Any]:
    project_dir = Path(project_dir)
    manifest_path = Path(manifest_path).expanduser()
    manifest = read_json(manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError(f"Invalid computation manifest: {manifest_path}")
    exec_cwd = Path(str(manifest.get("cwd") or project_dir)).expanduser().resolve()
    input_results = []
    output_results = []
    for record in manifest.get("inputs", []):
        path = _resolve_project_path(project_dir, record.get("absolute_path") or record.get("path", ""), cwd=exec_cwd)
        actual = _path_record(project_dir, path)
        input_results.append({**actual, "expected_sha256": record.get("sha256", ""), "matches": actual["sha256"] == record.get("sha256", "")})
    for record in manifest.get("expected_outputs", []):
        path = _resolve_project_path(project_dir, record.get("absolute_path") or record.get("path", ""), cwd=exec_cwd)
        actual = _path_record(project_dir, path)
        output_results.append({**actual, "expected_sha256": record.get("sha256", ""), "matches": actual["sha256"] == record.get("sha256", "")})
    rerun_payload: dict[str, Any] = {"executed": False}
    if rerun:
        completed = subprocess.run(
            [str(item) for item in manifest.get("command", [])],
            cwd=exec_cwd,
            text=True,
            capture_output=True,
            timeout=timeout_seconds or int(manifest.get("timeout_seconds", 120) or 120),
            check=False,
        )
        rerun_payload = {
            "executed": True,
            "returncode": completed.returncode,
            "stdout_sha256": hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest(),
            "stderr_sha256": hashlib.sha256(completed.stderr.encode("utf-8")).hexdigest(),
        }
    original_run = manifest.get("run") if isinstance(manifest.get("run"), dict) else {}
    original_run_ok = not original_run.get("executed") or original_run.get("returncode") == 0
    expected_stdout = str(original_run.get("stdout_sha256", ""))
    stdout_matches = not rerun or not expected_stdout or rerun_payload.get("stdout_sha256") == expected_stdout
    verified = all(item["matches"] for item in input_results + output_results) and stdout_matches and original_run_ok
    if rerun:
        verified = verified and rerun_payload.get("returncode") == 0
    report = {
        "generated_at": utc_now_iso(),
        "manifest_path": str(manifest_path),
        "manifest_id": manifest.get("manifest_id", ""),
        "workstream_id": manifest.get("workstream_id", ""),
        "verified": verified,
        "input_results": input_results,
        "output_results": output_results,
        "rerun": rerun_payload,
        "stdout_matches": stdout_matches,
    }
    report_path = manifest_path.with_suffix(".verification.json")
    write_json(report_path, report)
    append_jsonl(
        comath_paths(project_dir).messages,
        {
            "ts": utc_now_iso(),
            "type": "computation_certificate_verified",
            "manifest_path": str(manifest_path),
            "verified": verified,
        },
    )
    return {"project_dir": str(project_dir), "verification_path": str(report_path), "report": report}


def _load_theory_memory(project_dir: Path) -> dict[str, Any]:
    path = comath_paths(project_dir).root / "theory_memory.json"
    payload = read_json(path, default={}) or {}
    return {
        "generated_at": payload.get("generated_at", utc_now_iso()),
        "conjectures": list(payload.get("conjectures", [])),
        "lemmas": list(payload.get("lemmas", [])),
        "failed_hypotheses": list(payload.get("failed_hypotheses", [])),
        "novelty_notes": list(payload.get("novelty_notes", [])),
        "new_direction_candidates": list(payload.get("new_direction_candidates", [])),
    }


def update_theory_memory(
    project_dir: Path,
    *,
    conjecture: str = "",
    lemma: str = "",
    failed_hypothesis: str = "",
    novelty_note: str = "",
    new_direction: str = "",
    owner_workstream_id: str = "theory-building-memory",
) -> dict[str, Any]:
    project_dir = Path(project_dir)
    initialize_comath_project(project_dir)
    paths = comath_paths(project_dir)
    memory = _load_theory_memory(project_dir)
    additions: list[dict[str, Any]] = []

    def add_entry(bucket: str, text: str, **metadata: Any) -> None:
        if not text.strip():
            return
        entry_id = f"{bucket}:{hashlib.sha256(text.strip().lower().encode('utf-8')).hexdigest()[:12]}"
        if any(item.get("id") == entry_id for item in memory[bucket]):
            return
        entry = {
            "id": entry_id,
            "text": text.strip(),
            "owner_workstream_id": owner_workstream_id,
            "created_at": utc_now_iso(),
            "metadata": metadata,
        }
        memory[bucket].append(entry)
        additions.append({"bucket": bucket, **entry})

    add_entry("conjectures", conjecture, status="candidate")
    add_entry("lemmas", lemma, status="reusable_candidate")
    add_entry("failed_hypotheses", failed_hypothesis, status="suppressed_until_changed")
    add_entry("novelty_notes", novelty_note)
    add_entry("new_direction_candidates", new_direction, status="needs_review")
    memory["generated_at"] = utc_now_iso()
    write_json(paths.root / "theory_memory.json", memory)
    write_text(
        paths.root / "theory_memory.md",
        "\n".join(
            [
                "# CoMath Theory Memory",
                "",
                "## Conjectures",
                "",
                *([f"- `{item['id']}`: {item['text']}" for item in memory["conjectures"]] or ["- None recorded."]),
                "",
                "## Reusable Lemmas",
                "",
                *([f"- `{item['id']}`: {item['text']}" for item in memory["lemmas"]] or ["- None recorded."]),
                "",
                "## Failed Hypotheses",
                "",
                *([f"- `{item['id']}`: {item['text']}" for item in memory["failed_hypotheses"]] or ["- None recorded."]),
                "",
                "## New Direction Candidates",
                "",
                *([f"- `{item['id']}`: {item['text']}" for item in memory["new_direction_candidates"]] or ["- None recorded."]),
                "",
            ]
        ),
    )

    graph = load_artifact_graph(paths.artifact_graph)
    for entry in additions:
        if entry["bucket"] in {"conjectures", "lemmas", "new_direction_candidates"}:
            graph.record_claim(
                claim_id=entry["id"],
                title=entry["bucket"].replace("_", " ").title(),
                statement=entry["text"],
                status=ClaimStatus.HYPOTHESIS if entry["bucket"] != "lemmas" else ClaimStatus.ROUTE_CANDIDATE,
                workstream_id=owner_workstream_id,
                metadata={"theory_memory_bucket": entry["bucket"]},
            )
            graph.add_edge(
                source_id=entry["id"],
                target_id="original-theorem",
                relation=DependencyRelation.SUPPORTS,
                status=DependencyStatus.PENDING,
                rationale="Theory-memory item may support a future proof route after review.",
            )
    save_artifact_graph(paths.artifact_graph, graph)

    if failed_hypothesis.strip():
        ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
        existing = ledger.find_failed_route(failed_hypothesis)
        route = ledger.add_failed_route(
            route_id=f"theory-memory-{slugify(failed_hypothesis)[:48]}",
            summary=failed_hypothesis,
            failure_reason="Recorded in theory memory as a failed hypothesis.",
            owner_workstream_id=owner_workstream_id,
            metadata={"source": "theory_memory"},
        )
        save_uncertainty_ledger(paths.uncertainty_ledger, ledger)
        if existing is None:
            append_failed_route_jsonl(paths.failed_routes, route)
    append_jsonl(paths.messages, {"ts": utc_now_iso(), "type": "theory_memory_updated", "addition_count": len(additions)})
    render_project_dashboard(project_dir)
    return {"project_dir": str(project_dir), "theory_memory_path": str(paths.root / "theory_memory.json"), "memory": memory, "additions": additions}


@dataclass(slots=True)
class CapabilityCheck:
    capability: str
    status: str
    evidence: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability": self.capability,
            "status": self.status,
            "evidence": list(self.evidence),
            "missing": list(self.missing),
        }


def _status_from(evidence: list[str], missing: list[str]) -> str:
    if evidence and not missing:
        return "implemented"
    if evidence and missing:
        return "partial"
    return "missing"


def run_comath_evaluation(project_dir: Path) -> dict[str, Any]:
    project_dir = Path(project_dir)
    initialize_comath_project(project_dir)
    paths = comath_paths(project_dir)
    state = load_project_state(project_dir)
    graph = load_artifact_graph(paths.artifact_graph)
    ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
    intake_path = paths.root / "intake_plan.json"
    roles_path = paths.root / "specialist_roles.json"
    theory_path = paths.root / "theory_memory.json"
    computation_dir = paths.root / "computation"
    loop_dir = paths.root / "loop_runs"
    specialist_runs = list((paths.root / "specialists").glob("*/runs/*/result.json"))
    specialist_loop_reports = list((paths.root / "specialist_loops").glob("*/report.json"))
    checks: list[CapabilityCheck] = []

    def add_check(capability: str, evidence: list[str], missing: list[str]) -> None:
        checks.append(CapabilityCheck(capability=capability, status=_status_from(evidence, missing), evidence=evidence, missing=missing))

    add_check(
        "intent_refinement",
        [str(intake_path)] if intake_path.exists() and read_json(intake_path, default={}).get("refined_goal") else [],
        ["Run intake-comath-project to write comath/intake_plan.json."] if not intake_path.exists() else [],
    )
    add_check(
        "asynchronous_stateful_workspace",
        [str(paths.project_state), str(paths.dashboard), str(paths.artifact_graph), str(paths.uncertainty_ledger)],
        [path.name for path in [paths.project_state, paths.dashboard, paths.artifact_graph, paths.uncertainty_ledger] if not path.exists()],
    )
    add_check(
        "parallel_workstreams",
        [str(loop_dir)] if loop_dir.exists() else ["run_comath_loop supports bounded parallel resource slots"],
        [] if any(item.metadata.get("executor") for item in state.workstreams) else ["No workstreams with executor metadata are present."],
    )
    role_payload = read_json(roles_path, default={}) or {}
    role_ids = {item.get("role_id") for item in role_payload.get("roles", []) if isinstance(item, dict)}
    required_roles = {item["role_id"] for item in SPECIALIST_ROLE_DEFINITIONS}
    add_check(
        "specialist_agents",
        [str(roles_path)] if required_roles <= role_ids else [],
        sorted(required_roles - role_ids),
    )
    add_check(
        "llm_specialist_orchestration",
        [str(path) for path in specialist_runs[:5]] + [str(path) for path in specialist_loop_reports[:3]],
        ["No Codex/fake specialist run has been persisted under comath/specialists/."] if not specialist_runs else [],
    )
    add_check(
        "uncertainty_tracking",
        [str(paths.uncertainty_ledger), f"open_items={len(ledger.open_items())}"],
        [] if paths.uncertainty_ledger.exists() else ["Missing uncertainty ledger."],
    )
    add_check(
        "failed_hypothesis_memory",
        [str(paths.failed_routes), f"failed_routes={len(ledger.failed_routes)}"] if paths.failed_routes.exists() else [],
        [] if paths.failed_routes.exists() else ["Missing failed route ledger."],
    )
    add_check(
        "native_mathematical_artifacts",
        [f"artifact_nodes={len(graph.nodes)}", f"workstreams={len(state.workstreams)}"],
        [] if graph.nodes and state.workstreams else ["Artifact graph or workstream records are empty."],
    )
    add_check(
        "literature_search",
        [workstream.workstream_id for workstream in state.workstreams if workstream.kind == WorkstreamKind.SOURCE],
        [] if any(workstream.kind == WorkstreamKind.SOURCE for workstream in state.workstreams) else ["No source/literature workstream."],
    )
    verified_certs = [
        node.node_id
        for node in graph.nodes
        if node.kind.value == "computation_certificate" and bool(node.metadata.get("verified"))
    ]
    add_check(
        "computational_exploration",
        verified_certs or ([str(computation_dir)] if computation_dir.exists() else []),
        [] if verified_certs else ["No verified computation certificate recorded."],
    )
    add_check(
        "theorem_proving",
        [workstream.workstream_id for workstream in state.workstreams if workstream.kind == WorkstreamKind.LEAN],
        [] if any(workstream.kind == WorkstreamKind.LEAN for workstream in state.workstreams) else ["No Lean formalization workstream."],
    )
    theory_payload = read_json(theory_path, default={}) or {}
    theory_evidence = []
    for key in ("conjectures", "lemmas", "failed_hypotheses", "new_direction_candidates"):
        if theory_payload.get(key):
            theory_evidence.append(f"{key}={len(theory_payload[key])}")
    add_check(
        "theory_building",
        theory_evidence,
        [] if theory_evidence else ["No theory memory entries recorded."],
    )
    add_check(
        "review_gates",
        [f"reviews={len(state.reviews)}"] if state.reviews else ["review_gate module is available"],
        [] if state.reviews else ["No project review records yet."],
    )
    add_check(
        "progressive_disclosure",
        [str(paths.dashboard), str(paths.workstreams)] if paths.dashboard.exists() and paths.workstreams.exists() else [],
        [] if paths.dashboard.exists() and paths.workstreams.exists() else ["Dashboard or workstream detail directories missing."],
    )
    add_check(
        "evaluation_harness",
        ["run_comath_evaluation"],
        [],
    )

    implemented = sum(1 for check in checks if check.status == "implemented")
    partial = sum(1 for check in checks if check.status == "partial")
    report = {
        "generated_at": utc_now_iso(),
        "project_dir": str(project_dir),
        "paper_reference": "arXiv:2605.06651",
        "scope_note": "Local architecture parity only; this does not claim access to Google internal systems or benchmark performance.",
        "score": {
            "implemented": implemented,
            "partial": partial,
            "missing": len(checks) - implemented - partial,
            "total": len(checks),
        },
        "checks": [check.to_dict() for check in checks],
    }
    write_json(paths.root / "evaluation_report.json", report)
    write_text(
        paths.root / "evaluation_report.md",
        "\n".join(
            [
                "# CoMath Capability Evaluation",
                "",
                f"- Implemented: `{implemented}`",
                f"- Partial: `{partial}`",
                f"- Missing: `{len(checks) - implemented - partial}`",
                "",
                "| Capability | Status | Missing |",
                "| --- | --- | --- |",
                *[
                    f"| {check.capability} | {check.status} | {', '.join(check.missing) if check.missing else '-'} |"
                    for check in checks
                ],
                "",
            ]
        ),
    )
    append_jsonl(paths.messages, {"ts": utc_now_iso(), "type": "comath_evaluation_completed", "score": report["score"]})
    return {"project_dir": str(project_dir), "evaluation_path": str(paths.root / "evaluation_report.json"), "report": report}
