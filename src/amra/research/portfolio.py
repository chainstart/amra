from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from amra.orchestration.workstreams import utc_now_iso
from amra.portfolio_memory import append_jsonl, write_json
from amra.research.objects import ResearchObjectRecord


RESEARCH_CAMPAIGN_SCHEMA_VERSION = "amra.research_portfolio_campaign.v1"
RESEARCH_PORTFOLIO_SCHEMA_VERSION = "amra.research_portfolio.v1"
RESEARCH_RANKING_SCHEMA_VERSION = "amra.research_portfolio_ranking.v1"
RESEARCH_THEORY_MAP_SCHEMA_VERSION = "amra.research_theory_map.v1"
RESEARCH_PROMOTION_CANDIDATES_SCHEMA_VERSION = "amra.research_promotion_candidates.v1"

RESEARCH_OBJECTS_FILE = "research_objects.json"
RESEARCH_ARTIFACT_GRAPH_FILE = "research_artifact_graph.json"
EXPERIMENT_REPORTS_FILE = "experiment_reports.jsonl"
BENCHMARK_REPORTS_FILE = "benchmark_reports.jsonl"
NEGATIVE_RESULTS_FILE = "negative_results.jsonl"
NOVELTY_REPORTS_FILE = "novelty_reports.jsonl"
REPRODUCIBILITY_REPORTS_FILE = "reproducibility_reports.jsonl"
MODEL_VALIDATION_REPORTS_FILE = "model_validation_reports.jsonl"
SECURITY_REVIEW_REPORTS_FILE = "security_review_reports.jsonl"
THEORY_MAP_FILE = "theory_map.json"
PROMOTION_CANDIDATES_FILE = "promotion_candidates.json"

RESEARCH_BUNDLE_FILES = (
    RESEARCH_OBJECTS_FILE,
    RESEARCH_ARTIFACT_GRAPH_FILE,
    EXPERIMENT_REPORTS_FILE,
    BENCHMARK_REPORTS_FILE,
    NEGATIVE_RESULTS_FILE,
    NOVELTY_REPORTS_FILE,
    REPRODUCIBILITY_REPORTS_FILE,
    MODEL_VALIDATION_REPORTS_FILE,
    SECURITY_REVIEW_REPORTS_FILE,
    THEORY_MAP_FILE,
    PROMOTION_CANDIDATES_FILE,
)

RESEARCH_TASK_TYPES = {
    "prove_theorem",
    "formalize_statement",
    "mine_conjecture",
    "search_counterexample",
    "optimize_algorithm",
    "run_benchmark",
    "build_model",
    "validate_model",
    "define_security_game",
    "search_attack",
    "probe_ml_theory",
    "organize_theory",
}

SCORING_DIMENSIONS = (
    "expected_information_gain",
    "novelty_potential",
    "evaluator_availability",
    "proof_promotion_potential",
    "computation_cost",
    "reproducibility_risk",
    "source_quality",
    "negative_result_value",
    "paper_value",
    "reusable_asset_value",
    "safety_or_security_risk",
)

_COST_DIMENSIONS = {"computation_cost", "reproducibility_risk", "safety_or_security_risk"}


def _slug(value: str, *, fallback: str = "campaign") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or fallback


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.resolve(strict=False).relative_to(root.resolve(strict=False)))
    except ValueError:
        return str(path)


def _read_fixture(fixture: Path) -> dict[str, Any]:
    payload = json.loads(fixture.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("research portfolio fixture must be a JSON object")
    return payload


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _list_value(value: Any) -> list[Any]:
    if value is None:
        return []
    return list(value) if isinstance(value, list) else [value]


def _normalize_object(payload: dict[str, Any]) -> dict[str, Any]:
    record = ResearchObjectRecord.from_dict(payload)
    return record.to_dict()


def _object_status(object_payload: dict[str, Any]) -> str:
    return str(object_payload.get("status") or "draft").strip().lower()


def _object_type(object_payload: dict[str, Any]) -> str:
    return str(object_payload.get("object_type") or "hypothesis").strip().lower()


def _default_task_type(object_payload: dict[str, Any]) -> str:
    object_type = _object_type(object_payload)
    status = _object_status(object_payload)
    if status == "lean_candidate":
        return "formalize_statement"
    if status == "proof_candidate" or object_type in {"conjecture", "hypothesis"}:
        return "prove_theorem" if status in {"proof_candidate", "lean_candidate"} else "search_counterexample"
    if object_type == "experiment":
        return "run_benchmark"
    if object_type == "algorithm":
        return "optimize_algorithm"
    if object_type == "benchmark":
        return "run_benchmark"
    if object_type == "model":
        return "validate_model"
    if object_type == "security_game":
        return "search_attack"
    if object_type == "security_assumption":
        return "define_security_game"
    if object_type == "ml_theory_claim":
        return "probe_ml_theory"
    if object_type in {"negative_result", "counterexample"}:
        return "organize_theory"
    return "organize_theory"


def _coerce_score(value: Any, default: float = 0.0) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return default


def _default_scores(object_payload: dict[str, Any], task_type: str) -> dict[str, float]:
    object_type = _object_type(object_payload)
    status = _object_status(object_payload)
    metadata = _dict_value(object_payload.get("metadata"))
    evidence_count = len(_list_value(object_payload.get("evidence_ids"))) + len(_list_value(object_payload.get("artifact_ids")))
    source_count = len(_list_value(object_payload.get("source_ids")))
    proof_ready = status in {"proof_candidate", "lean_candidate", "verified"} or task_type in {
        "prove_theorem",
        "formalize_statement",
    }
    negative_result = object_type in {"negative_result", "counterexample"} or status in {
        "counterexample_found",
        "rejected",
    }
    scores = {
        "expected_information_gain": 0.55,
        "novelty_potential": 0.5,
        "evaluator_availability": 0.45,
        "proof_promotion_potential": 0.75 if proof_ready else 0.25,
        "computation_cost": 0.3,
        "reproducibility_risk": 0.25,
        "source_quality": 0.35 + min(0.4, 0.15 * source_count),
        "negative_result_value": 0.85 if negative_result else 0.2,
        "paper_value": 0.45,
        "reusable_asset_value": 0.45,
        "safety_or_security_risk": 0.2,
    }
    if object_type in {"experiment", "benchmark", "algorithm", "ml_theory_claim"}:
        scores["expected_information_gain"] = 0.75
        scores["evaluator_availability"] = 0.65
        scores["source_quality"] = max(scores["source_quality"], 0.55)
    if object_type in {"security_game", "security_assumption"}:
        scores["safety_or_security_risk"] = 0.55
        scores["negative_result_value"] = 0.55
    if evidence_count:
        scores["reproducibility_risk"] = max(0.05, scores["reproducibility_risk"] - min(0.2, 0.05 * evidence_count))
        scores["evaluator_availability"] = min(1.0, scores["evaluator_availability"] + min(0.2, 0.05 * evidence_count))
    if metadata.get("source_debt"):
        scores["source_quality"] = min(scores["source_quality"], 0.25)
        scores["reproducibility_risk"] = max(scores["reproducibility_risk"], 0.65)
    return scores


def _score_task(object_payload: dict[str, Any], task_payload: dict[str, Any]) -> dict[str, Any]:
    task_type = str(task_payload.get("task_type") or _default_task_type(object_payload)).strip()
    if task_type not in RESEARCH_TASK_TYPES:
        task_type = _default_task_type(object_payload)
    scores = _default_scores(object_payload, task_type)
    for key, value in _dict_value(task_payload.get("scores") or object_payload.get("scores")).items():
        if key in scores:
            scores[key] = _coerce_score(value, scores[key])
    positive = sum(value for key, value in scores.items() if key not in _COST_DIMENSIONS)
    cost = sum(value for key, value in scores.items() if key in _COST_DIMENSIONS)
    priority = round((positive - cost) * 10.0, 2)
    status = _object_status(object_payload)
    object_type = _object_type(object_payload)
    if object_type in {"negative_result", "counterexample"} or status in {"counterexample_found", "rejected"}:
        recommendation = "record_negative_result"
    elif scores["proof_promotion_potential"] >= 0.7 and scores["source_quality"] >= 0.45 and scores["reproducibility_risk"] <= 0.55:
        recommendation = "promote_to_proof"
    elif scores["novelty_potential"] < 0.25 or scores["source_quality"] < 0.3 or scores["reproducibility_risk"] >= 0.7:
        recommendation = "park"
    elif scores["expected_information_gain"] >= 0.65 and scores["computation_cost"] <= 0.65:
        recommendation = "schedule_bounded_executor"
    else:
        recommendation = "organize_theory"
    return {
        "task_id": str(task_payload.get("task_id") or f"{object_payload['object_id']}:{task_type}"),
        "object_id": object_payload["object_id"],
        "object_type": object_type,
        "title": object_payload.get("title", ""),
        "task_type": task_type,
        "status": status,
        "scores": {key: round(scores[key], 3) for key in SCORING_DIMENSIONS},
        "priority": priority,
        "recommendation": recommendation,
        "budget_seconds": int(task_payload.get("budget_seconds") or task_payload.get("timeout_seconds") or 0),
        "promotion_target": str(task_payload.get("promotion_target") or object_payload.get("promotion_target") or ""),
        "blocked_by": list(object_payload.get("blocked_by", [])),
    }


def _promotion_candidate(task: dict[str, Any], object_payload: dict[str, Any]) -> dict[str, Any]:
    target = str(task.get("promotion_target") or object_payload.get("promotion_target") or "proof_task")
    return {
        "candidate_id": f"promotion:{task['object_id']}",
        "object_id": task["object_id"],
        "object_type": task["object_type"],
        "title": task.get("title", ""),
        "task_type": task["task_type"],
        "promotion_target": target,
        "priority": task["priority"],
        "proof_promotion_potential": task["scores"]["proof_promotion_potential"],
        "source_quality": task["scores"]["source_quality"],
        "reproducibility_risk": task["scores"]["reproducibility_risk"],
        "status": "candidate",
        "verification_boundary": "promotion_candidate_not_lean_verified",
    }


def _negative_result_record(task: dict[str, Any], object_payload: dict[str, Any]) -> dict[str, Any]:
    metadata = _dict_value(object_payload.get("metadata"))
    return {
        "schema_version": "amra.research_negative_result.v1",
        "object_id": task["object_id"],
        "object_type": task["object_type"],
        "title": task.get("title", ""),
        "target_object_id": str(object_payload.get("target_object_id") or metadata.get("target_object_id") or ""),
        "failure_mode": str(object_payload.get("failure_mode") or metadata.get("failure_mode") or "bounded_negative_evidence"),
        "result_summary": str(object_payload.get("result_summary") or object_payload.get("statement") or ""),
        "search_bound": _dict_value(object_payload.get("search_bound") or metadata.get("search_bound")),
        "task_id": task["task_id"],
        "negative_result_value": task["scores"]["negative_result_value"],
        "verification_boundary": "bounded_negative_result_not_theorem",
    }


def _artifact_graph(objects: list[dict[str, Any]], relations: list[dict[str, Any]]) -> dict[str, Any]:
    nodes = [
        {
            "id": item["object_id"],
            "kind": item.get("object_type", "hypothesis"),
            "title": item.get("title", ""),
            "status": item.get("status", "draft"),
        }
        for item in objects
    ]
    object_ids = {node["id"] for node in nodes}
    edges: list[dict[str, Any]] = []
    for relation in relations:
        source = str(relation.get("from") or relation.get("source") or "").strip()
        target = str(relation.get("to") or relation.get("target") or "").strip()
        if not source or not target:
            continue
        edges.append(
            {
                "from": source,
                "to": target,
                "relation": str(relation.get("relation") or "RELATED_TO").strip().upper(),
                "confidence": str(relation.get("confidence") or "unknown"),
                "notes": str(relation.get("notes") or ""),
            }
        )
    for item in objects:
        if _object_type(item) == "negative_result":
            target = str(item.get("target_object_id") or _dict_value(item.get("metadata")).get("target_object_id") or "").strip()
            if target and target in object_ids:
                edges.append({"from": item["object_id"], "to": target, "relation": "REFUTES", "confidence": "medium", "notes": ""})
    return {
        "schema_version": "amra.research_artifact_graph.v1",
        "nodes": nodes,
        "edges": edges,
    }


def _theory_map(objects: list[dict[str, Any]], graph: dict[str, Any], promotions: list[dict[str, Any]], negatives: list[dict[str, Any]]) -> dict[str, Any]:
    nodes = []
    for item in objects:
        nodes.append(
            {
                "object_id": item["object_id"],
                "object_type": item.get("object_type", "hypothesis"),
                "title": item.get("title", ""),
                "status": item.get("status", "draft"),
                "role": "failure" if item.get("object_type") == "negative_result" else "research_object",
            }
        )
    return {
        "schema_version": RESEARCH_THEORY_MAP_SCHEMA_VERSION,
        "nodes": nodes,
        "edges": list(graph.get("edges", [])),
        "promotion_candidate_ids": [item["candidate_id"] for item in promotions],
        "negative_result_object_ids": [item["object_id"] for item in negatives],
        "taxonomy": {
            "definitions": [item["object_id"] for item in objects if item.get("object_type") == "theory_node"],
            "conjectures": [item["object_id"] for item in objects if item.get("object_type") == "conjecture"],
            "proof_candidates": [item["object_id"] for item in promotions],
            "failures": [item["object_id"] for item in negatives],
        },
    }


def _render_final_report(*, campaign_id: str, ranking: list[dict[str, Any]], promotions: list[dict[str, Any]], negatives: list[dict[str, Any]]) -> str:
    lines = [
        f"# AMRA Research Campaign: {campaign_id}",
        "",
        f"- Ranked tasks: `{len(ranking)}`",
        f"- Promotion candidates: `{len(promotions)}`",
        f"- Negative results: `{len(negatives)}`",
        "",
        "## Ranking",
        "",
    ]
    for item in ranking:
        lines.append(
            f"- `{item['object_id']}` task=`{item['task_type']}` priority={item['priority']} recommendation=`{item['recommendation']}`"
        )
    lines.extend(["", "## Verification Boundary", ""])
    lines.append("- Promotion candidates are not Lean-verified theorem claims.")
    lines.append("- Negative results are bounded research evidence unless separately verified.")
    lines.append("- Empirical, benchmark, model, security, and theory-map artifacts are research evidence only.")
    lines.append("")
    return "\n".join(lines)


def _campaign_artifact_manifest(campaign_dir: Path, *, repo_root: Path, campaign_id: str) -> dict[str, Any]:
    files = []
    for path in sorted(item for item in campaign_dir.iterdir() if item.is_file()):
        if path.name == "artifact_manifest.json":
            continue
        files.append(
            {
                "path": path.name,
                "kind": {
                    "campaign_manifest.json": "campaign_manifest",
                    "research_portfolio.json": "research_portfolio",
                    "ranking.json": "research_task_ranking",
                    "promotion_candidates.json": "research_promotion_candidates",
                    "negative_results.jsonl": "negative_result_ledger",
                    "theory_map.json": "theory_map",
                    "research_objects.json": "research_object_ledger",
                    "research_artifact_graph.json": "research_artifact_graph",
                    "campaign_log.jsonl": "campaign_log",
                    "final_report.md": "final_report",
                }.get(path.name, "research_supporting_artifact"),
                "bytes": path.stat().st_size,
                "lean_verified_claim_source": False,
            }
        )
    return {
        "schema_version": "amra.research_campaign_artifact_manifest.v1",
        "campaign_id": campaign_id,
        "generated_at": utc_now_iso(),
        "campaign_dir": _relative(campaign_dir, repo_root),
        "verification_boundary": {
            "campaign_artifacts": "research_evidence_only",
            "promotion_candidates": "not_lean_verified",
            "negative_results": "bounded_evidence_not_theorem",
        },
        "files": files,
    }


@dataclass(frozen=True)
class ResearchPortfolioCampaignRunner:
    repo_root: Path

    def run_fixture(self, *, fixture: Path, output_dir: Path) -> dict[str, Any]:
        payload = _read_fixture(fixture)
        generated_at = utc_now_iso()
        campaign_id = _slug(str(payload.get("campaign_id") or payload.get("run_name") or fixture.stem), fallback="research-campaign")
        campaign_dir = output_dir.expanduser().resolve()
        campaign_dir.mkdir(parents=True, exist_ok=True)

        object_payloads = [_normalize_object(dict(item)) for item in _list_value(payload.get("objects")) if isinstance(item, dict)]
        objects_by_id = {item["object_id"]: item for item in object_payloads}
        explicit_tasks = [dict(item) for item in _list_value(payload.get("tasks")) if isinstance(item, dict)]
        tasks: list[dict[str, Any]] = []
        if explicit_tasks:
            for task in explicit_tasks:
                object_id = str(task.get("object_id") or "").strip()
                if object_id in objects_by_id:
                    tasks.append(_score_task(objects_by_id[object_id], task))
        else:
            tasks = [_score_task(item, {}) for item in object_payloads]
        ranking = sorted(tasks, key=lambda item: (-float(item["priority"]), str(item["object_id"]), str(item["task_type"])))
        promotions = [
            _promotion_candidate(task, objects_by_id[task["object_id"]])
            for task in ranking
            if task["recommendation"] == "promote_to_proof"
        ]
        negatives = [
            _negative_result_record(task, objects_by_id[task["object_id"]])
            for task in ranking
            if task["recommendation"] == "record_negative_result"
        ]
        graph = _artifact_graph(object_payloads, [dict(item) for item in _list_value(payload.get("relations")) if isinstance(item, dict)])
        theory_map = _theory_map(object_payloads, graph, promotions, negatives)

        manifest = {
            "schema_version": RESEARCH_CAMPAIGN_SCHEMA_VERSION,
            "campaign_id": campaign_id,
            "created_at": generated_at,
            "fixture": str(fixture),
            "object_count": len(object_payloads),
            "task_count": len(ranking),
            "task_types": sorted({item["task_type"] for item in ranking}),
            "live_model_calls": False,
            "output_dir": str(campaign_dir),
        }
        portfolio = {
            "schema_version": RESEARCH_PORTFOLIO_SCHEMA_VERSION,
            "campaign_id": campaign_id,
            "generated_at": generated_at,
            "scoring_dimensions": list(SCORING_DIMENSIONS),
            "task_types": sorted(RESEARCH_TASK_TYPES),
            "objects": object_payloads,
            "tasks": ranking,
            "scheduling_policy": {
                "low_cost_first": True,
                "proof_ready_promotes_to_existing_pipeline": True,
                "negative_findings_recorded_before_retry": True,
                "live_model_calls": False,
            },
        }

        write_json(campaign_dir / "campaign_manifest.json", manifest)
        write_json(campaign_dir / "research_portfolio.json", portfolio)
        write_json(campaign_dir / "ranking.json", {"schema_version": RESEARCH_RANKING_SCHEMA_VERSION, "ranking": ranking})
        write_json(
            campaign_dir / "promotion_candidates.json",
            {
                "schema_version": RESEARCH_PROMOTION_CANDIDATES_SCHEMA_VERSION,
                "generated_at": generated_at,
                "candidates": promotions,
            },
        )
        write_json(campaign_dir / "research_objects.json", {"schema_version": "amra.research_objects.v1", "objects": object_payloads})
        write_json(campaign_dir / "research_artifact_graph.json", graph)
        write_json(campaign_dir / "theory_map.json", theory_map)
        (campaign_dir / "negative_results.jsonl").write_text("", encoding="utf-8")
        for item in negatives:
            append_jsonl(campaign_dir / "negative_results.jsonl", item)
        self._write_report_ledgers(campaign_dir=campaign_dir, payload=payload, generated_at=generated_at)
        append_jsonl(
            campaign_dir / "campaign_log.jsonl",
            {
                "event": "research_campaign_created",
                "at": generated_at,
                "campaign_id": campaign_id,
                "object_count": len(object_payloads),
                "task_count": len(ranking),
            },
        )
        (campaign_dir / "final_report.md").write_text(
            _render_final_report(campaign_id=campaign_id, ranking=ranking, promotions=promotions, negatives=negatives),
            encoding="utf-8",
        )
        self._write_object_directories(
            campaign_dir=campaign_dir,
            objects=object_payloads,
            graph=graph,
            promotions=promotions,
            negatives=negatives,
            ranking=ranking,
        )
        write_json(campaign_dir / "artifact_manifest.json", _campaign_artifact_manifest(campaign_dir, repo_root=self.repo_root, campaign_id=campaign_id))

        return {
            "schema_version": "amra.research_portfolio_campaign_result.v1",
            "campaign_id": campaign_id,
            "campaign_dir": _relative(campaign_dir, self.repo_root),
            "manifest": _relative(campaign_dir / "campaign_manifest.json", self.repo_root),
            "research_portfolio": _relative(campaign_dir / "research_portfolio.json", self.repo_root),
            "ranking": _relative(campaign_dir / "ranking.json", self.repo_root),
            "promotion_candidates": _relative(campaign_dir / "promotion_candidates.json", self.repo_root),
            "theory_map": _relative(campaign_dir / "theory_map.json", self.repo_root),
            "negative_results": _relative(campaign_dir / "negative_results.jsonl", self.repo_root),
            "artifact_manifest": _relative(campaign_dir / "artifact_manifest.json", self.repo_root),
            "promoted_count": len(promotions),
            "negative_result_count": len(negatives),
            "task_count": len(ranking),
            "live_model_calls": False,
        }

    def _write_report_ledgers(self, *, campaign_dir: Path, payload: dict[str, Any], generated_at: str) -> None:
        ledgers = {
            EXPERIMENT_REPORTS_FILE: "experiment_reports",
            BENCHMARK_REPORTS_FILE: "benchmark_reports",
            NOVELTY_REPORTS_FILE: "novelty_reports",
            REPRODUCIBILITY_REPORTS_FILE: "reproducibility_reports",
            MODEL_VALIDATION_REPORTS_FILE: "model_validation_reports",
            SECURITY_REVIEW_REPORTS_FILE: "security_review_reports",
        }
        for filename, key in ledgers.items():
            path = campaign_dir / filename
            path.write_text("", encoding="utf-8")
            for item in _list_value(payload.get(key)):
                if isinstance(item, dict):
                    append_jsonl(path, {"schema_version": f"amra.{key}.entry.v1", "recorded_at": generated_at, **item})

    def _write_object_directories(
        self,
        *,
        campaign_dir: Path,
        objects: list[dict[str, Any]],
        graph: dict[str, Any],
        promotions: list[dict[str, Any]],
        negatives: list[dict[str, Any]],
        ranking: list[dict[str, Any]],
    ) -> None:
        promotion_by_object = {item["object_id"]: item for item in promotions}
        negatives_by_object = {item["object_id"]: item for item in negatives}
        tasks_by_object: dict[str, list[dict[str, Any]]] = {}
        for task in ranking:
            tasks_by_object.setdefault(task["object_id"], []).append(task)
        edges_by_object: dict[str, list[dict[str, Any]]] = {}
        for edge in graph.get("edges", []):
            if isinstance(edge, dict):
                edges_by_object.setdefault(str(edge.get("from") or ""), []).append(edge)
                edges_by_object.setdefault(str(edge.get("to") or ""), []).append(edge)
        for item in objects:
            object_id = item["object_id"]
            object_dir = campaign_dir / "objects" / _slug(object_id, fallback="object")
            for child in ("review", "runs", "promotion"):
                (object_dir / child).mkdir(parents=True, exist_ok=True)
            write_json(object_dir / "object.json", item)
            (object_dir / "evidence.jsonl").write_text("", encoding="utf-8")
            for evidence_id in _list_value(item.get("evidence_ids")):
                append_jsonl(object_dir / "evidence.jsonl", {"object_id": object_id, "evidence_id": str(evidence_id)})
            write_json(
                object_dir / "artifact_graph.json",
                {
                    "schema_version": "amra.research_object_artifact_graph.v1",
                    "object_id": object_id,
                    "edges": edges_by_object.get(object_id, []),
                },
            )
            write_json(object_dir / "runs" / "scheduled_tasks.json", {"tasks": tasks_by_object.get(object_id, [])})
            if object_id in promotion_by_object:
                write_json(object_dir / "promotion" / "candidate.json", promotion_by_object[object_id])
            if object_id in negatives_by_object:
                write_json(object_dir / "review" / "negative_result.json", negatives_by_object[object_id])
            project_dir = campaign_dir / "projects" / _slug(object_id, fallback="object")
            for child in ("evidence", "experiments", "benchmarks", "sources", "review", "promotion", "notes"):
                (project_dir / child).mkdir(parents=True, exist_ok=True)
            (project_dir / "object.yaml").write_text(json.dumps(item, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
            write_json(
                project_dir / "state.json",
                {
                    "schema_version": "amra.research_object_state.v1",
                    "object_id": object_id,
                    "state": item.get("status", "draft"),
                    "updated_at": utc_now_iso(),
                    "campaign": _relative(campaign_dir, self.repo_root),
                },
            )
            append_jsonl(
                project_dir / "state_history.jsonl",
                {
                    "schema_version": "amra.research_object_state_transition.v1",
                    "object_id": object_id,
                    "state": item.get("status", "draft"),
                    "changed_at": utc_now_iso(),
                    "reason": "initialized by research portfolio campaign",
                },
            )


def run_research_portfolio_campaign_fixture(*, fixture: Path, output_dir: Path, repo_root: Path | None = None) -> dict[str, Any]:
    root = repo_root.expanduser().resolve() if repo_root is not None else Path.cwd().resolve()
    return ResearchPortfolioCampaignRunner(repo_root=root).run_fixture(fixture=fixture, output_dir=output_dir)


__all__ = [
    "BENCHMARK_REPORTS_FILE",
    "EXPERIMENT_REPORTS_FILE",
    "MODEL_VALIDATION_REPORTS_FILE",
    "NEGATIVE_RESULTS_FILE",
    "NOVELTY_REPORTS_FILE",
    "PROMOTION_CANDIDATES_FILE",
    "REPRODUCIBILITY_REPORTS_FILE",
    "RESEARCH_ARTIFACT_GRAPH_FILE",
    "RESEARCH_BUNDLE_FILES",
    "RESEARCH_CAMPAIGN_SCHEMA_VERSION",
    "RESEARCH_OBJECTS_FILE",
    "RESEARCH_PORTFOLIO_SCHEMA_VERSION",
    "RESEARCH_RANKING_SCHEMA_VERSION",
    "RESEARCH_TASK_TYPES",
    "SCORING_DIMENSIONS",
    "SECURITY_REVIEW_REPORTS_FILE",
    "THEORY_MAP_FILE",
    "ResearchPortfolioCampaignRunner",
    "run_research_portfolio_campaign_fixture",
]
