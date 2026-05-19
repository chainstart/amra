from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from amra.source_quality import SOURCE_QUALITY_SCHEMA_VERSION, score_source_record
from amra.core.artifact_graph import load_artifact_graph, save_artifact_graph
from amra.evaluation.capabilities import refine_intake_project
from amra.evaluation.specialists import SpecialistProvider, run_specialist
from amra.orchestration.coordinator import comath_paths, initialize_comath_project, load_project_state, render_project_dashboard, save_project_state
from amra.orchestration.uncertainty import (
    SourceDebtStatus,
    UncertaintyItem,
    UncertaintyKind,
    load_uncertainty_ledger,
    save_uncertainty_ledger,
)
from amra.core.workspace import append_jsonl, read_json, slugify, write_json, write_text
from amra.orchestration.workstreams import WorkstreamStatus, utc_now_iso


def _goal_terms(text: str, *, limit: int = 8) -> list[str]:
    stopwords = {
        "the",
        "and",
        "for",
        "that",
        "with",
        "prove",
        "show",
        "find",
        "from",
        "this",
        "there",
        "whether",
        "mathematical",
        "objective",
    }
    terms: list[str] = []
    for raw in text.replace("_", " ").replace("-", " ").split():
        token = "".join(ch for ch in raw.lower() if ch.isalnum())
        if len(token) < 4 or token in stopwords or token in terms:
            continue
        terms.append(token)
        if len(terms) >= limit:
            break
    return terms


def build_source_query_plan(
    project_dir: Path,
    *,
    rounds: int = 3,
    seed_terms: list[str] | None = None,
) -> dict[str, Any]:
    project_dir = Path(project_dir)
    initialize_comath_project(project_dir)
    state = load_project_state(project_dir)
    intake = read_json(comath_paths(project_dir).root / "intake_plan.json", default={}) or {}
    goal = str(intake.get("refined_goal") or state.original_goal or "").strip()
    terms = seed_terms or _goal_terms(goal)
    if not terms:
        terms = [state.project_name, "theorem", "source"]
    base_query = " ".join(terms[:6])
    templates = [
        "{base_query} theorem source assumptions",
        "{base_query} arXiv proof reference",
        "{base_query} Lean formalization mathlib",
        "{base_query} counterexample open problem",
        "{base_query} survey known result",
    ]
    queries = []
    for index in range(max(1, rounds)):
        template = templates[index % len(templates)]
        queries.append(
            {
                "round": index + 1,
                "query": template.format(base_query=base_query),
                "goal": goal,
                "required_outputs": [
                    "source inventory",
                    "exact theorem statement candidates",
                    "assumption match notes",
                    "citation confidence",
                    "source debt items",
                ],
            }
        )
    plan = {
        "generated_at": utc_now_iso(),
        "project_dir": str(project_dir),
        "rounds": len(queries),
        "seed_terms": terms,
        "queries": queries,
    }
    source_dir = comath_paths(project_dir).root / "source_audit"
    write_json(source_dir / "query_plan.json", plan)
    return plan


def _confidence_from_result(result: dict[str, Any]) -> float:
    parsed = result.get("result", {}).get("parsed_output", {})
    fields = parsed.get("fields", {}) if isinstance(parsed, dict) else {}
    blockers = parsed.get("blockers", []) if isinstance(parsed, dict) else []
    confidence = 0.35
    evidence = str(fields.get("evidence", "")).strip().lower()
    claims = str(fields.get("claims", "")).strip().lower()
    if evidence and evidence not in {"none", "n/a"}:
        confidence += 0.25
    if claims and claims not in {"none", "n/a"}:
        confidence += 0.15
    if not blockers:
        confidence += 0.15
    return round(min(confidence, 0.95), 3)


def _source_task(query: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"Run source audit round {query['round']}.",
            f"Search/query focus: {query['query']}",
            "",
            "Return source inventory, exact theorem statement candidates, assumption matching notes, citation confidence, and source debt.",
            "If using web search, prefer primary sources, papers, DOI/arXiv pages, and official documentation.",
        ]
    )


def run_source_audit_loop(
    project_dir: Path,
    *,
    rounds: int = 3,
    backend: str = "codex",
    provider: SpecialistProvider | None = None,
    model: str = "",
    reasoning_effort: str = "",
    timeout_seconds: int = 900,
    allow_search: bool = True,
    max_parallel_rounds: int = 1,
    run_name: str | None = None,
    workstream_id: str = "source-literature-audit",
    seed_terms: list[str] | None = None,
) -> dict[str, Any]:
    project_dir = Path(project_dir)
    initialize_comath_project(project_dir)
    state = load_project_state(project_dir)
    if state.get_workstream(workstream_id) is None:
        refine_intake_project(project_dir, goal=state.original_goal, project_name=state.project_name)
    source_dir = comath_paths(project_dir).root / "source_audit"
    source_dir.mkdir(parents=True, exist_ok=True)
    loop_id = slugify(run_name or f"source-audit-{utc_now_iso()}")
    plan = build_source_query_plan(project_dir, rounds=rounds, seed_terms=seed_terms)
    selected_queries = plan["queries"][: max(1, rounds)]
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max(1, min(max_parallel_rounds, len(selected_queries)))) as pool:
        futures = {
            pool.submit(
                run_specialist,
                project_dir,
                role_id="source_auditor",
                workstream_id=workstream_id,
                task=_source_task(query),
                backend=backend,
                provider=provider,
                model=model,
                reasoning_effort=reasoning_effort,
                timeout_seconds=timeout_seconds,
                allow_search=allow_search,
                run_name=f"{loop_id}-round-{query['round']}",
            ): query
            for query in selected_queries
        }
        for future in as_completed(futures):
            query = futures[future]
            result = future.result()
            results.append({"query": query, **result})
    results.sort(key=lambda item: item["query"]["round"])

    inventory_items: list[dict[str, Any]] = []
    for item in results:
        inventory_item = {
            "round": item["query"]["round"],
            "query": item["query"]["query"],
            "output_path": item["output_path"],
            "provider": item["provider"]["provider"],
            "provider_status": item["provider"]["status"],
            "parsed_fields": item["result"]["parsed_output"]["fields"],
            "blockers": item["result"]["parsed_output"]["blockers"],
        }
        inventory_item["source_quality"] = score_source_record(
            {
                "source": str(item["output_path"]),
                "kind": "source_audit_round",
                "status": "ok" if item["provider"]["status"] == "completed" else str(item["provider"]["status"]),
                "source_type": "local_path",
                "evidence_items": [
                    value
                    for value in inventory_item["parsed_fields"].values()
                    if str(value).strip() and str(value).strip().lower() not in {"none", "n/a"}
                ],
            }
        )
        inventory_items.append(inventory_item)

    inventory = {
        "generated_at": utc_now_iso(),
        "loop_id": loop_id,
        "workstream_id": workstream_id,
        "items": inventory_items,
    }
    confidence_items = [
        {
            "round": item["query"]["round"],
            "query": item["query"]["query"],
            "confidence": _confidence_from_result(item),
            "blocker_count": len(item["result"]["parsed_output"]["blockers"]),
        }
        for item in results
    ]
    confidence = {
        "generated_at": utc_now_iso(),
        "loop_id": loop_id,
        "threshold": 0.65,
        "items": confidence_items,
        "max_confidence": max((item["confidence"] for item in confidence_items), default=0.0),
    }
    quality_ranked = sorted(
        [item["source_quality"] for item in inventory_items],
        key=lambda quality: (-float(quality.get("score", 0.0)), str(quality.get("source", ""))),
    )
    source_quality = {
        "schema_version": SOURCE_QUALITY_SCHEMA_VERSION,
        "generated_at": utc_now_iso(),
        "loop_id": loop_id,
        "workstream_id": workstream_id,
        "score": float(quality_ranked[0].get("score", 0.0)) if quality_ranked else 0.0,
        "tier": str(quality_ranked[0].get("tier", "source_debt")) if quality_ranked else "source_debt",
        "trusted_source_count": sum(1 for item in quality_ranked if item.get("tier") == "trusted"),
        "usable_source_count": sum(1 for item in quality_ranked if item.get("tier") in {"trusted", "usable"}),
        "source_count": len(quality_ranked),
        "source_debt": (
            ["citation_confidence_below_threshold"]
            if confidence["max_confidence"] < confidence["threshold"]
            else []
        ),
        "trust_reasons": sorted({reason for item in quality_ranked for reason in item.get("trust_reasons", [])}),
        "top_sources": [
            {
                "source": item.get("source", ""),
                "score": item.get("score", 0.0),
                "tier": item.get("tier", "source_debt"),
                "trust_reasons": item.get("trust_reasons", [])[:6],
                "source_debt": item.get("source_debt", [])[:6],
            }
            for item in quality_ranked[:8]
        ],
    }
    report = {
        "project_dir": str(project_dir),
        "loop_id": loop_id,
        "generated_at": utc_now_iso(),
        "query_plan_path": str(source_dir / "query_plan.json"),
        "source_inventory_path": str(source_dir / "source_inventory.json"),
        "citation_confidence_path": str(source_dir / "citation_confidence.json"),
        "source_quality_audit_path": str(source_dir / "source_quality_audit.json"),
        "executed_rounds": len(results),
        "backend": backend,
        "allow_search": allow_search,
        "confidence": confidence,
        "source_quality": source_quality,
        "results": results,
    }
    write_json(source_dir / "source_inventory.json", inventory)
    write_json(source_dir / "citation_confidence.json", confidence)
    write_json(source_dir / "source_quality_audit.json", source_quality)
    write_json(source_dir / "report.json", report)
    write_text(
        source_dir / "report.md",
        "\n".join(
            [
                f"# Source Audit Loop: {loop_id}",
                "",
                f"- Executed rounds: `{len(results)}`",
                f"- Max confidence: `{confidence['max_confidence']}`",
                f"- Source quality: `{source_quality['score']}` ({source_quality['tier']})",
                f"- Backend: `{backend}`",
                "",
            ]
        ),
    )

    paths = comath_paths(project_dir)
    graph = load_artifact_graph(paths.artifact_graph)
    for filename in ("query_plan.json", "source_inventory.json", "citation_confidence.json", "source_quality_audit.json", "report.json"):
        graph.record_file(
            node_id=f"source-audit:{loop_id}:{filename}",
            path=str(source_dir / filename),
            label=f"Source audit {filename}",
            workstream_id=workstream_id,
            metadata={"loop_id": loop_id, "source_audit": True},
        )
    save_artifact_graph(paths.artifact_graph, graph)

    ledger = load_uncertainty_ledger(paths.uncertainty_ledger)
    if confidence["max_confidence"] < confidence["threshold"]:
        ledger.upsert_item(
            UncertaintyItem(
                item_id=f"source-audit-low-confidence:{loop_id}",
                kind=UncertaintyKind.SOURCE_DEBT,
                title="Source audit loop did not reach citation confidence threshold",
                description=f"Max confidence {confidence['max_confidence']} is below {confidence['threshold']}.",
                owner_workstream_id=workstream_id,
                source_debt_status=SourceDebtStatus.EXTERNAL_THEOREM_NEEDED,
                severity="high",
            )
        )
    save_uncertainty_ledger(paths.uncertainty_ledger, ledger)

    state = load_project_state(project_dir)
    workstream = state.get_workstream(workstream_id)
    if workstream is not None:
        workstream.metadata["latest_source_audit_loop"] = {
            "loop_id": loop_id,
            "report_path": str(source_dir / "report.json"),
            "max_confidence": confidence["max_confidence"],
            "executed_rounds": len(results),
        }
        if confidence["max_confidence"] >= confidence["threshold"]:
            workstream.status = WorkstreamStatus.NEEDS_REVIEW
        else:
            workstream.status = WorkstreamStatus.REVISION
        state.upsert_workstream(workstream)
        save_project_state(project_dir, state)
        write_json(paths.workstream_dir(workstream_id) / "status.json", workstream.to_dict())
    append_jsonl(
        paths.messages,
        {
            "ts": utc_now_iso(),
            "type": "source_audit_loop_completed",
            "loop_id": loop_id,
            "executed_rounds": len(results),
            "max_confidence": confidence["max_confidence"],
        },
    )
    render_project_dashboard(project_dir)
    return report
