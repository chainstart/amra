from __future__ import annotations

from typing import Any


def empirical_complexity_summary(comparisons: list[dict[str, Any]]) -> dict[str, Any]:
    improvements = [
        float(item["improvement_pct"])
        for item in comparisons
        if isinstance(item, dict) and isinstance(item.get("improvement_pct"), (int, float))
    ]
    if not improvements:
        return {
            "schema_version": "amra.empirical_complexity_summary.v1",
            "status": "insufficient_data",
            "mean_improvement_pct": 0.0,
            "claim_boundary": "benchmark_evidence_only",
        }
    return {
        "schema_version": "amra.empirical_complexity_summary.v1",
        "status": "recorded",
        "mean_improvement_pct": round(sum(improvements) / len(improvements), 6),
        "claim_boundary": "benchmark_evidence_only",
    }


__all__ = ["empirical_complexity_summary"]
