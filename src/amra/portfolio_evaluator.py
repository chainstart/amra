from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from amra.source_quality import SOURCE_QUALITY_RECOVERY_THRESHOLD, build_source_quality_audit
from amra.portfolio_memory import (
    load_claim_ledger,
    load_failed_routes,
    load_route_ledger,
    read_json,
    utc_now_iso,
    write_json,
)


DIFFICULTY_SCHEMA_VERSION = "amra.difficulty_evaluation.v1"
RECOMMENDATIONS = (
    "promote",
    "continue",
    "park",
    "abandon",
    "freeze",
    "source_recover",
    "counterexample_review",
)

PLACEHOLDER_STATEMENT_MARKERS = (
    "placeholder",
    "detailed statement should be imported",
    "statement should be imported",
    "todo",
    "tbd",
)
LEAN_PLACEHOLDER_RE = re.compile(r"\b(sorry|admit)\b|^\s*(axiom|constant|opaque)\b", re.MULTILINE)
LEAN_DECL_RE = re.compile(r"^\s*(theorem|lemma)\s+(`[^`]+`|[A-Za-z_][A-Za-z0-9_'.!?]*)\b", re.MULTILINE)
REPORT_JSON_NAMES = {
    "report.json",
    "state.json",
    "decision.json",
    "attempt_report.json",
    "after_audit.json",
    "before_audit.json",
    "initial_audit.json",
    "best_audit.json",
    "build_report.json",
    "after_build.json",
    "route_clusters.json",
    "verified_declarations.json",
}
TEXT_ARTIFACT_PATTERNS = (
    "proof/sketches/*.md",
    "proof/audits/*.md",
    "proof/blockers/*.md",
    "runs/**/summary.md",
    "runs/**/manual_summary.md",
    "runs/**/*_output.md",
)


def _clamp(value: float, lower: float = 0.0, upper: float = 10.0) -> float:
    return max(lower, min(upper, value))


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.resolve(strict=False).relative_to(root.resolve(strict=False)))
    except ValueError:
        return str(path)


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        cleaned = str(value).strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        deduped.append(cleaned)
    return deduped


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, set):
        return sorted(value, key=str)
    return [value]


def _string_list(value: Any) -> list[str]:
    return _dedupe([str(item).strip() for item in _as_list(value) if str(item).strip()])


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _read_structured(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        if path.suffix.lower() == ".json":
            payload = json.loads(path.read_text(encoding="utf-8"))
        else:
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, yaml.YAMLError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(key, "")).strip() or "unknown"
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _walk_strings(payload: Any) -> list[str]:
    values: list[str] = []
    if isinstance(payload, dict):
        for value in payload.values():
            values.extend(_walk_strings(value))
    elif isinstance(payload, list):
        for value in payload:
            values.extend(_walk_strings(value))
    elif isinstance(payload, str):
        values.append(payload)
    return values


def _walk_numbers_by_key(payload: Any, wanted_keys: set[str]) -> list[float]:
    values: list[float] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in wanted_keys:
                values.append(_safe_float(value))
            values.extend(_walk_numbers_by_key(value, wanted_keys))
    elif isinstance(payload, list):
        for value in payload:
            values.extend(_walk_numbers_by_key(value, wanted_keys))
    return values


def _path_looks_like_private_prompt(path: Path) -> bool:
    name = path.name.lower()
    return name in {"prompt.txt", "context_bundle.md"} or name.endswith("_prompt.txt")


@dataclass(frozen=True)
class PortfolioEvaluator:
    """Independent evaluator over durable AMRA portfolio artifacts.

    The evaluator does not call proof agents or reuse transient/private prompt
    context. It scores only persisted ledgers, run reports, summaries, proof
    notes, and Lean files that are already present under the project directory.
    """

    repo_root: Path

    def evaluate_project(self, *, project: Path, run_name: str | None = None) -> dict[str, Any]:
        project = project.resolve()
        problem_id = self._problem_id(project)
        state = read_json(project / "state.json", {})
        source = self._source_signal(project)
        claims = list(load_claim_ledger(project).get("claims", []))
        routes = list(load_route_ledger(project).get("routes", []))
        failed_routes = list(load_failed_routes(project).get("failed_routes", []))
        report_signal = self._report_signal(project)
        proof_signal = self._proof_text_signal(project)
        lean_signal = self._lean_signal(project, report_signal=report_signal)
        artifact_paths = self._artifact_paths(
            project=project,
            source_paths=source["artifact_paths"],
            report_paths=report_signal["artifact_paths"],
            proof_paths=proof_signal["artifact_paths"],
            lean_paths=lean_signal["artifact_paths"],
        )

        claim_status_counts = _count_by(claims, "status")
        route_status_counts = _count_by(routes, "status")
        failed_mode_counts = _count_by(failed_routes, "failure_mode")
        verified_claim_count = claim_status_counts.get("lean_verified", 0)
        false_claim_count = claim_status_counts.get("false", 0)
        route_supported_count = claim_status_counts.get("route_supported", 0)
        sketch_claim_count = claim_status_counts.get("sketch", 0)
        route_promising_count = route_status_counts.get("promising", 0) + route_status_counts.get("completed", 0)
        blocked_route_count = route_status_counts.get("blocked", 0) + route_status_counts.get("failed", 0)
        failed_route_count = len(failed_routes)

        counterexample = self._counterexample_signal(
            claims=claims,
            failed_routes=failed_routes,
            routes=routes,
            report_signal=report_signal,
        )
        source_gap_from_routes = self._has_source_gap(routes=routes, failed_routes=failed_routes)
        route_progress = self._route_progress_signal(routes)
        repeated_failures = failed_route_count + blocked_route_count
        no_progress = self._no_progress(
            report_signal=report_signal,
            route_progress=route_progress,
            repeated_failures=repeated_failures,
            lean_signal=lean_signal,
        )

        risk_flags: list[str] = []
        if not source["has_manifest"]:
            risk_flags.append("missing_problem_manifest")
        if not source["has_exact_statement"]:
            risk_flags.append("missing_exact_statement")
        if not source["has_source_provenance"]:
            risk_flags.append("missing_source_provenance")
        if source["source_quality_score"] < SOURCE_QUALITY_RECOVERY_THRESHOLD:
            risk_flags.append("low_source_quality")
        if source["source_debt"]:
            risk_flags.append("source_debt")
        if source_gap_from_routes:
            risk_flags.append("source_gap")
        if counterexample["suspected"]:
            risk_flags.append("counterexample_candidate")
            risk_flags.append("long_budget_blocked")
        if counterexample["strong"]:
            risk_flags.append("strong_counterexample")
        if report_signal["statement_mismatch"] or failed_mode_counts.get("lean_statement_mismatch", 0):
            risk_flags.append("lean_statement_mismatch")
        if lean_signal["placeholder_count"]:
            risk_flags.append("lean_placeholders")
        if lean_signal["build_failed_count"]:
            risk_flags.append("lean_build_failed")
        if failed_mode_counts.get("missing_mathlib_api", 0):
            risk_flags.append("missing_mathlib_api")
        if repeated_failures >= 3:
            risk_flags.append("repeated_failed_routes")
        if no_progress:
            risk_flags.append("no_measurable_progress")
        risk_flags = _dedupe(risk_flags)

        known_theorem_signal = self._known_theorem_signal(claims=claims, routes=routes, report_signal=report_signal)
        proof_confidence = self._proof_confidence(
            verified_claim_count=verified_claim_count,
            route_supported_count=route_supported_count,
            sketch_claim_count=sketch_claim_count,
            known_theorem_signal=known_theorem_signal,
            report_signal=report_signal,
            proof_signal=proof_signal,
            counterexample=counterexample,
        )
        formalization_score = self._formalization_score(
            lean_signal=lean_signal,
            report_signal=report_signal,
            verified_claim_count=verified_claim_count,
        )
        formalization_confidence = self._formalization_confidence(
            lean_signal=lean_signal,
            report_signal=report_signal,
            formalization_score=formalization_score,
        )
        feasibility_score = self._feasibility_score(
            source=source,
            proof_confidence=proof_confidence,
            formalization_score=formalization_score,
            verified_claim_count=verified_claim_count,
            route_promising_count=route_promising_count,
            repeated_failures=repeated_failures,
            known_theorem_signal=known_theorem_signal,
            counterexample=counterexample,
            risk_flags=risk_flags,
        )
        expected_hours = self._expected_hours(
            feasibility_score=feasibility_score,
            lean_signal=lean_signal,
            repeated_failures=repeated_failures,
            counterexample=counterexample,
            source=source,
        )
        confidence = self._overall_confidence(
            source=source,
            proof_confidence=proof_confidence,
            formalization_confidence=formalization_confidence,
            artifact_count=len(artifact_paths),
            counterexample=counterexample,
        )
        recommendation, reasons = self._recommend(
            state=str(state.get("state", "unseen")),
            source=source,
            source_gap_from_routes=source_gap_from_routes,
            feasibility_score=feasibility_score,
            proof_confidence=proof_confidence,
            formalization_confidence=formalization_confidence,
            verified_claim_count=verified_claim_count,
            lean_verified=lean_signal["verified"],
            known_theorem_signal=known_theorem_signal,
            route_promising_count=route_promising_count,
            repeated_failures=repeated_failures,
            no_progress=no_progress,
            counterexample=counterexample,
            false_claim_count=false_claim_count,
        )
        primary_blocker = self._primary_blocker(
            recommendation=recommendation,
            risk_flags=risk_flags,
            routes=routes,
            failed_routes=failed_routes,
        )
        long_budget_allowed = recommendation not in {
            "abandon",
            "freeze",
            "source_recover",
            "counterexample_review",
        } and not counterexample["suspected"]

        payload = {
            "schema_version": DIFFICULTY_SCHEMA_VERSION,
            "run_name": run_name or "",
            "problem_id": problem_id,
            "generated_at": utc_now_iso(),
            "project": str(project),
            "evaluator": "amra.portfolio_evaluator.PortfolioEvaluator",
            "mode": "read_only_durable_artifacts",
            "state": state.get("state", "unseen"),
            "difficulty_score": round(_clamp(10.0 - feasibility_score), 2),
            "feasibility_score": round(feasibility_score, 2),
            "formalization_score": round(formalization_score, 2),
            "expected_hours_to_result": round(expected_hours, 2),
            "confidence": round(confidence, 2),
            "proof_confidence": round(proof_confidence, 2),
            "formalization_confidence": round(formalization_confidence, 2),
            "recommendation": recommendation,
            "recommendation_reasons": reasons,
            "primary_blocker": primary_blocker,
            "risk_flags": risk_flags,
            "long_budget_allowed": long_budget_allowed,
            "budget_gate": {
                "long_budget_allowed": long_budget_allowed,
                "reason": (
                    "counterexample_suspected_route_requires_review"
                    if counterexample["suspected"]
                    else primary_blocker
                ),
            },
            "claim_count": len(claims),
            "route_count": len(routes),
            "failed_route_count": failed_route_count,
            "claim_status_counts": claim_status_counts,
            "route_status_counts": route_status_counts,
            "failed_route_mode_counts": failed_mode_counts,
            "source_signal": {key: value for key, value in source.items() if key != "artifact_paths"},
            "proof_signal": {key: value for key, value in proof_signal.items() if key != "artifact_paths"},
            "lean_signal": {key: value for key, value in lean_signal.items() if key != "artifact_paths"},
            "counterexample_signal": counterexample,
            "progress_signal": {
                "positive_progress_events": report_signal["positive_progress_events"]
                + route_progress["positive_progress_events"],
                "nonpositive_progress_events": report_signal["nonpositive_progress_events"]
                + route_progress["nonpositive_progress_events"],
                "progress_velocity": max(report_signal["progress_velocity"], route_progress["progress_velocity"]),
                "no_measurable_progress": no_progress,
            },
            "evidence": artifact_paths,
            "input_artifacts": [{"path": path} for path in artifact_paths],
            "allowed_recommendations": list(RECOMMENDATIONS),
        }
        return payload

    def write_evaluation(self, *, project: Path, run_name: str) -> dict[str, Any]:
        payload = self.evaluate_project(project=project, run_name=run_name)
        report_path = project.resolve() / "runs" / run_name / "difficulty.json"
        write_json(report_path, payload)
        latest_path = project.resolve() / "difficulty.json"
        write_json(latest_path, payload)
        return {**payload, "report_path": str(report_path), "latest_report_path": str(latest_path)}

    def _problem_id(self, project: Path) -> str:
        state = read_json(project / "state.json", {})
        if state.get("problem_id"):
            return str(state["problem_id"])
        for path in (project / "problem.yaml", project / "project_manifest.json"):
            payload = _read_structured(path)
            if payload.get("problem_id"):
                return str(payload["problem_id"])
        return project.name

    def _source_signal(self, project: Path) -> dict[str, Any]:
        artifact_paths: list[str] = []
        payloads: list[dict[str, Any]] = []
        for name in ("problem.yaml", "problem.yml", "project_manifest.json", "project_manifest.yaml", "problem.json"):
            path = project / name
            payload = _read_structured(path)
            if payload:
                artifact_paths.append(_relative(path, self.repo_root))
                payloads.append(payload)
        statement = ""
        source = ""
        references: list[str] = []
        statement_quality = ""
        known_source = False
        metadata_payloads: list[dict[str, Any]] = []
        for payload in payloads:
            statement = statement or str(payload.get("statement") or payload.get("exact_statement") or "")
            source = source or str(payload.get("source") or payload.get("provenance") or "")
            references.extend(_string_list(payload.get("references") or payload.get("source_references")))
            metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
            if metadata:
                metadata_payloads.append(metadata)
            statement_quality = statement_quality or str(metadata.get("statement_quality") or payload.get("statement_quality") or "")
            known_source = known_source or bool(payload.get("known_theorem") or metadata.get("known_theorem"))
        exact_statement_path = project / "idea" / "exact_statement.md"
        if exact_statement_path.exists():
            idea_statement = exact_statement_path.read_text(encoding="utf-8", errors="ignore").strip()
            if idea_statement and not any(marker in idea_statement.lower() for marker in PLACEHOLDER_STATEMENT_MARKERS):
                statement = idea_statement
                statement_quality = "exact"
                artifact_paths.append(_relative(exact_statement_path, self.repo_root))
        lowered_statement = statement.lower()
        has_exact_statement = bool(statement.strip()) and not any(marker in lowered_statement for marker in PLACEHOLDER_STATEMENT_MARKERS)
        if statement_quality.lower() in {"placeholder", "unknown", "needs_source"}:
            has_exact_statement = False
        has_source_provenance = bool(source.strip() or references or known_source)
        metadata = metadata_payloads[0] if metadata_payloads else {}
        source_quality_path = project / "idea" / "source_quality_audit.json"
        persisted_source_quality = read_json(source_quality_path, default={}) if source_quality_path.exists() else {}
        snapshots_payload = read_json(project / "idea" / "reference_snapshots.json", default={})
        snapshots = snapshots_payload.get("snapshots", []) if isinstance(snapshots_payload, dict) else []
        skipped_sources = snapshots_payload.get("skipped_sources", []) if isinstance(snapshots_payload, dict) else []
        recovery = read_json(project / "idea" / "statement_recovery.json", default={})
        has_source_provenance = has_source_provenance or bool(
            isinstance(recovery, dict) and str(recovery.get("source", "")).strip()
        )
        if (
            isinstance(persisted_source_quality, dict)
            and persisted_source_quality.get("schema_version") == "amra.source_quality.v1"
            and float(persisted_source_quality.get("score", 0.0) or 0.0) > 0
        ):
            source_quality = persisted_source_quality
        else:
            source_quality = build_source_quality_audit(
                problem_id=self._problem_id(project),
                statement=statement,
                source=source,
                references=references,
                metadata=metadata,
                snapshots=snapshots if isinstance(snapshots, list) else [],
                skipped_sources=skipped_sources if isinstance(skipped_sources, list) else [],
                recovery=recovery if isinstance(recovery, dict) else {},
            )
        source_debt = _string_list(source_quality.get("source_debt"))
        if source_quality_path.exists():
            artifact_paths.append(_relative(source_quality_path, self.repo_root))
        return {
            "has_manifest": bool(payloads),
            "has_exact_statement": has_exact_statement,
            "has_source_provenance": has_source_provenance,
            "statement_quality": "exact" if has_exact_statement else "missing_or_placeholder",
            "source": source,
            "reference_count": len(_dedupe(references)),
            "known_source": known_source,
            "source_quality_score": float(source_quality.get("score", 0.0) or 0.0),
            "source_quality_tier": str(source_quality.get("tier", "")),
            "trusted_source_count": int(source_quality.get("trusted_source_count", 0) or 0),
            "usable_source_count": int(source_quality.get("usable_source_count", 0) or 0),
            "source_debt": source_debt,
            "trust_reasons": _string_list(source_quality.get("trust_reasons"))[:12],
            "statement_provenance": source_quality.get("statement_provenance", {}),
            "top_sources": source_quality.get("top_sources", [])[:8],
            "source_quality_artifact": _relative(source_quality_path, self.repo_root) if source_quality_path.exists() else "",
            "artifact_paths": artifact_paths,
        }

    def _report_signal(self, project: Path) -> dict[str, Any]:
        reports: list[dict[str, Any]] = []
        artifact_paths: list[str] = []
        for path in sorted(project.rglob("*.json")):
            if ".lake" in path.parts or path.name == "difficulty.json":
                continue
            if path.name not in REPORT_JSON_NAMES:
                continue
            if path == project / "state.json":
                continue
            payload = read_json(path, {})
            if not isinstance(payload, dict):
                continue
            reports.append(payload)
            artifact_paths.append(_relative(path, self.repo_root))
            if len(reports) >= 200:
                break
        strings = [value.lower() for report in reports for value in _walk_strings(report)]
        status_values = [str(report.get("status", "")).lower() for report in reports]
        build_statuses = [
            str(report.get("build_status", "")).lower()
            for report in reports
            if str(report.get("build_status", "")).strip()
        ]
        verified = any(
            status == "verified"
            or bool(report.get("verified"))
            or bool((report.get("best_audit") or {}).get("verified"))
            or bool((report.get("final_observation") or {}).get("contract_satisfied"))
            for status, report in zip(status_values, reports)
        )
        progress_deltas = _walk_numbers_by_key(reports, {"progress_delta"})
        progress_velocity_values = _walk_numbers_by_key(reports, {"progress_velocity"})
        return {
            "report_count": len(reports),
            "verified": verified,
            "counterexample_suspected": any(
                "counterexample_suspected" in status_values
                or "counterexample_suspected" in value
                or "counterexample candidate" in value
                for value in strings
            ),
            "proof_candidate": any(
                "proof_candidate" in value or "closed_candidate" in value or "passes_initial_audit" in value
                for value in strings
            ),
            "known_theorem": any("known_theorem" in value or "known theorem" in value for value in strings),
            "formalize_recommended": any("formalize" == value.strip() or "formalization_only" in value for value in strings),
            "statement_mismatch": any("statement_mismatch" in value or "statement mismatch" in value for value in strings),
            "build_passed_count": sum(1 for status in build_statuses if status == "passed"),
            "build_failed_count": sum(1 for status in build_statuses if status in {"failed", "timeout"}),
            "positive_progress_events": sum(1 for value in progress_deltas if value > 0),
            "nonpositive_progress_events": sum(1 for value in progress_deltas if value <= 0),
            "progress_velocity": round(max(progress_velocity_values or [0.0]), 3),
            "artifact_paths": artifact_paths,
        }

    def _proof_text_signal(self, project: Path) -> dict[str, Any]:
        artifact_paths: list[str] = []
        text_chunks: list[str] = []
        for pattern in TEXT_ARTIFACT_PATTERNS:
            for path in sorted(project.glob(pattern)):
                if _path_looks_like_private_prompt(path):
                    continue
                if not path.is_file():
                    continue
                artifact_paths.append(_relative(path, self.repo_root))
                text_chunks.append(path.read_text(encoding="utf-8", errors="ignore")[:12000])
                if len(artifact_paths) >= 100:
                    break
        text = "\n".join(text_chunks).lower()
        return {
            "text_artifact_count": len(artifact_paths),
            "has_proof_sketch": "proof sketch" in text or "proof:" in text or bool(text_chunks),
            "proof_candidate": "proof_candidate" in text or "closed_candidate" in text,
            "known_theorem": "known theorem" in text or "known_theorem" in text,
            "counterexample_suspected": "counterexample_suspected" in text or "counterexample candidate" in text,
            "artifact_paths": artifact_paths,
        }

    def _lean_signal(self, project: Path, *, report_signal: dict[str, Any]) -> dict[str, Any]:
        search_roots = [project / "formal"] if (project / "formal").exists() else [project]
        lean_files: list[Path] = []
        for root in search_roots:
            lean_files.extend(
                sorted(path for path in root.rglob("*.lean") if ".lake" not in path.parts and path.is_file())
            )
        lean_files = sorted(set(lean_files))
        placeholder_count = 0
        declaration_count = 0
        for path in lean_files:
            text = path.read_text(encoding="utf-8", errors="ignore")
            placeholder_count += len(LEAN_PLACEHOLDER_RE.findall(text))
            declaration_count += len(LEAN_DECL_RE.findall(text))
        return {
            "lean_file_count": len(lean_files),
            "declaration_count": declaration_count,
            "placeholder_count": placeholder_count,
            "verified": bool(report_signal["verified"]) or (bool(lean_files) and placeholder_count == 0 and report_signal["build_passed_count"] > 0),
            "build_passed_count": report_signal["build_passed_count"],
            "build_failed_count": report_signal["build_failed_count"],
            "artifact_paths": [_relative(path, self.repo_root) for path in lean_files],
        }

    def _artifact_paths(
        self,
        *,
        project: Path,
        source_paths: list[str],
        report_paths: list[str],
        proof_paths: list[str],
        lean_paths: list[str],
    ) -> list[str]:
        paths: list[str] = []
        for path in (
            project / "state.json",
            project / "memory" / "claim_ledger.json",
            project / "memory" / "route_ledger.json",
            project / "memory" / "failed_routes.json",
            project / "memory" / "evidence_index.json",
        ):
            if path.exists():
                paths.append(_relative(path, self.repo_root))
        paths.extend(source_paths)
        paths.extend(report_paths)
        paths.extend(proof_paths)
        paths.extend(lean_paths)
        return _dedupe(paths)

    def _counterexample_signal(
        self,
        *,
        claims: list[dict[str, Any]],
        failed_routes: list[dict[str, Any]],
        routes: list[dict[str, Any]],
        report_signal: dict[str, Any],
    ) -> dict[str, Any]:
        claim_suspected = [
            str(claim.get("claim_id", ""))
            for claim in claims
            if str(claim.get("status", "")) in {"counterexample_suspected", "false"}
        ]
        failed_suspected = [
            str(item.get("route_id", ""))
            for item in failed_routes
            if str(item.get("failure_mode", "")) == "counterexample_candidate"
        ]
        route_suspected = [
            str(route.get("route_id", ""))
            for route in routes
            if "counterexample" in str(route.get("status", "")).lower()
            or "counterexample" in str(route.get("blocker", "")).lower()
            or "counterexample" in json.dumps(route.get("evaluator_verdict", {}), ensure_ascii=False).lower()
        ]
        strong = any(str(claim.get("status", "")) == "false" for claim in claims)
        for item in failed_routes:
            if str(item.get("failure_mode", "")) != "counterexample_candidate":
                continue
            strength = str(item.get("strength") or item.get("confidence_label") or "").lower()
            confidence = _safe_float(item.get("confidence"), 0.0)
            evidence_text = json.dumps(item.get("evidence", []), ensure_ascii=False).lower()
            strong = strong or strength in {"strong", "formal", "verified", "confirmed"}
            strong = strong or confidence >= 0.8
            strong = strong or bool(item.get("formal_counterexample") or item.get("verified_counterexample"))
            strong = strong or "formal_counterexample" in evidence_text or "verified_counterexample" in evidence_text
        suspected = bool(claim_suspected or failed_suspected or route_suspected or report_signal["counterexample_suspected"])
        return {
            "suspected": suspected,
            "strong": bool(strong and suspected),
            "claim_ids": _dedupe(claim_suspected),
            "route_ids": _dedupe(failed_suspected + route_suspected),
            "from_reports": bool(report_signal["counterexample_suspected"]),
        }

    def _has_source_gap(self, *, routes: list[dict[str, Any]], failed_routes: list[dict[str, Any]]) -> bool:
        source_terms = ("source", "provenance", "exact_statement", "statement source")
        for route in routes:
            blocker = str(route.get("blocker", "")).lower()
            if any(term in blocker for term in source_terms):
                return True
        return any(str(item.get("failure_mode", "")) == "source_gap" for item in failed_routes)

    def _known_theorem_signal(
        self,
        *,
        claims: list[dict[str, Any]],
        routes: list[dict[str, Any]],
        report_signal: dict[str, Any],
    ) -> bool:
        for item in [*claims, *routes]:
            if item.get("known_theorem") or item.get("source_theorem"):
                return True
            text = json.dumps(item, ensure_ascii=False).lower()
            if "known_theorem" in text or "known theorem" in text:
                return True
        return bool(report_signal["known_theorem"])

    def _route_progress_signal(self, routes: list[dict[str, Any]]) -> dict[str, Any]:
        progress_deltas: list[float] = []
        velocity_values: list[float] = []
        for route in routes:
            for attempt in _as_list(route.get("attempt_history") or route.get("attempts")):
                if not isinstance(attempt, dict):
                    continue
                if "progress_delta" in attempt:
                    progress_deltas.append(_safe_float(attempt.get("progress_delta")))
                if "progress_velocity" in attempt:
                    velocity_values.append(_safe_float(attempt.get("progress_velocity")))
        return {
            "positive_progress_events": sum(1 for value in progress_deltas if value > 0),
            "nonpositive_progress_events": sum(1 for value in progress_deltas if value <= 0),
            "progress_velocity": round(max(velocity_values or [0.0]), 3),
        }

    def _no_progress(
        self,
        *,
        report_signal: dict[str, Any],
        route_progress: dict[str, Any],
        repeated_failures: int,
        lean_signal: dict[str, Any],
    ) -> bool:
        positive_events = report_signal["positive_progress_events"] + route_progress["positive_progress_events"]
        nonpositive_events = report_signal["nonpositive_progress_events"] + route_progress["nonpositive_progress_events"]
        if positive_events > 0 or lean_signal["verified"]:
            return False
        return repeated_failures >= 2 and nonpositive_events >= 1

    def _proof_confidence(
        self,
        *,
        verified_claim_count: int,
        route_supported_count: int,
        sketch_claim_count: int,
        known_theorem_signal: bool,
        report_signal: dict[str, Any],
        proof_signal: dict[str, Any],
        counterexample: dict[str, Any],
    ) -> float:
        score = 0.2
        score += min(0.55, 0.55 * verified_claim_count)
        score += min(0.25, 0.12 * route_supported_count)
        score += min(0.18, 0.06 * sketch_claim_count)
        if known_theorem_signal:
            score += 0.25
        if report_signal["proof_candidate"] or proof_signal["proof_candidate"]:
            score += 0.2
        if proof_signal["has_proof_sketch"]:
            score += 0.08
        if counterexample["suspected"]:
            score -= 0.35 if counterexample["strong"] else 0.2
        return _clamp(score, 0.0, 0.95)

    def _formalization_score(
        self,
        *,
        lean_signal: dict[str, Any],
        report_signal: dict[str, Any],
        verified_claim_count: int,
    ) -> float:
        score = 3.0
        if lean_signal["lean_file_count"]:
            score += 1.0
        if lean_signal["declaration_count"]:
            score += min(1.5, 0.4 * lean_signal["declaration_count"])
        if report_signal["build_passed_count"]:
            score += 1.5
        if lean_signal["verified"] or verified_claim_count:
            score += 2.0
        if report_signal["formalize_recommended"]:
            score += 0.75
        score -= min(2.5, 0.35 * lean_signal["placeholder_count"])
        score -= min(1.5, 0.75 * report_signal["build_failed_count"])
        return _clamp(score)

    def _formalization_confidence(
        self,
        *,
        lean_signal: dict[str, Any],
        report_signal: dict[str, Any],
        formalization_score: float,
    ) -> float:
        confidence = 0.2 + formalization_score / 20.0
        if lean_signal["verified"]:
            confidence += 0.25
        if report_signal["build_passed_count"]:
            confidence += 0.1
        if lean_signal["placeholder_count"]:
            confidence -= min(0.2, 0.03 * lean_signal["placeholder_count"])
        return _clamp(confidence, 0.0, 0.95)

    def _feasibility_score(
        self,
        *,
        source: dict[str, Any],
        proof_confidence: float,
        formalization_score: float,
        verified_claim_count: int,
        route_promising_count: int,
        repeated_failures: int,
        known_theorem_signal: bool,
        counterexample: dict[str, Any],
        risk_flags: list[str],
    ) -> float:
        score = 3.0
        score += 1.4 if source["has_exact_statement"] else -2.0
        score += 0.8 if source["has_source_provenance"] else -0.8
        score += (float(source.get("source_quality_score", 0.0)) - 5.0) * 0.2
        score += proof_confidence * 2.3
        score += formalization_score * 0.25
        score += min(1.0, 0.35 * route_promising_count)
        if verified_claim_count:
            score += 1.5
        if known_theorem_signal:
            score += 1.4
        score -= min(2.0, 0.45 * repeated_failures)
        if "lean_statement_mismatch" in risk_flags:
            score -= 1.5
        if "low_source_quality" in risk_flags:
            score -= 0.8
        if counterexample["suspected"]:
            score -= 3.5 if counterexample["strong"] else 2.5
        return _clamp(score)

    def _expected_hours(
        self,
        *,
        feasibility_score: float,
        lean_signal: dict[str, Any],
        repeated_failures: int,
        counterexample: dict[str, Any],
        source: dict[str, Any],
    ) -> float:
        if lean_signal["verified"]:
            return 1.0
        if counterexample["suspected"]:
            return 2.0
        if not source["has_exact_statement"]:
            return 3.0
        return max(1.0, 14.0 - feasibility_score * 1.1 + lean_signal["placeholder_count"] * 0.35 + repeated_failures * 0.75)

    def _overall_confidence(
        self,
        *,
        source: dict[str, Any],
        proof_confidence: float,
        formalization_confidence: float,
        artifact_count: int,
        counterexample: dict[str, Any],
    ) -> float:
        confidence = 0.25 + proof_confidence * 0.35 + formalization_confidence * 0.25
        if source["has_exact_statement"]:
            confidence += 0.08
        if source["has_source_provenance"]:
            confidence += 0.05
        confidence += min(0.08, float(source.get("source_quality_score", 0.0)) * 0.008)
        confidence += min(0.12, artifact_count * 0.01)
        if counterexample["suspected"]:
            confidence += 0.08
        return _clamp(confidence, 0.0, 0.95)

    def _recommend(
        self,
        *,
        state: str,
        source: dict[str, Any],
        source_gap_from_routes: bool,
        feasibility_score: float,
        proof_confidence: float,
        formalization_confidence: float,
        verified_claim_count: int,
        lean_verified: bool,
        known_theorem_signal: bool,
        route_promising_count: int,
        repeated_failures: int,
        no_progress: bool,
        counterexample: dict[str, Any],
        false_claim_count: int,
    ) -> tuple[str, list[str]]:
        if false_claim_count or counterexample["strong"] or state == "frozen":
            return "freeze", ["strong_or_confirmed_counterexample_blocks_the_current_statement_or_route"]
        if counterexample["suspected"]:
            return "counterexample_review", ["counterexample_suspected_route_cannot_receive_long_budget_by_default"]
        if (
            not source["has_exact_statement"]
            or not source["has_source_provenance"]
            or source_gap_from_routes
            or float(source.get("source_quality_score", 0.0)) < SOURCE_QUALITY_RECOVERY_THRESHOLD
        ):
            return "source_recover", ["exact_statement_or_source_provenance_is_missing"]
        if verified_claim_count or lean_verified:
            return "promote", ["lean_verified_or_claim_verified_artifact_is_available"]
        if known_theorem_signal and formalization_confidence >= 0.35:
            return "promote", ["known_theorem_or_source_route_makes_formalization_bounded"]
        if feasibility_score >= 7.0 and proof_confidence >= 0.6 and formalization_confidence >= 0.35:
            return "promote", ["feasibility_score_exceeds_promotion_threshold_without_severe_risk"]
        if no_progress or (repeated_failures >= 3 and feasibility_score < 6.0) or feasibility_score < 4.5:
            if state == "parked" and repeated_failures >= 5 and no_progress:
                return "abandon", ["parked_target_has_exhausted_repeated_routes_without_new_progress"]
            return "park", ["low_progress_or_low_feasibility_under_current_artifacts"]
        if state in {"active_attack", "promising", "formalization_ready"} or route_promising_count or proof_confidence >= 0.35:
            return "continue", ["some_route_or_progress_signal_exists_but_promotion_threshold_is_not_met"]
        return "park", ["insufficient_evidence_for_more_budget_now"]

    def _primary_blocker(
        self,
        *,
        recommendation: str,
        risk_flags: list[str],
        routes: list[dict[str, Any]],
        failed_routes: list[dict[str, Any]],
    ) -> str:
        if recommendation == "promote":
            return ""
        priority = [
            "strong_counterexample",
            "counterexample_candidate",
            "missing_exact_statement",
            "missing_source_provenance",
            "low_source_quality",
            "source_gap",
            "source_debt",
            "lean_statement_mismatch",
            "lean_build_failed",
            "lean_placeholders",
            "repeated_failed_routes",
            "no_measurable_progress",
            "missing_mathlib_api",
        ]
        if recommendation == "abandon":
            priority.extend(["low_progress_or_low_feasibility", "abandon"])
        for flag in priority:
            if flag in risk_flags:
                return flag
        for route in routes:
            blocker = str(route.get("blocker", "")).strip()
            if blocker:
                return blocker
        for failed_route in failed_routes:
            mode = str(failed_route.get("failure_mode", "")).strip()
            if mode:
                return mode
        return recommendation
