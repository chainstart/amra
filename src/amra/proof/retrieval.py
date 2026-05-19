from __future__ import annotations

import re
from typing import Any

from amra.core.workspace import utc_now_iso


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9_']+", text.lower()) if len(token) >= 3}


class PremiseRetriever:
    """Build a lightweight retrieval report for proof search.

    This is deliberately simple, but it makes premise selection explicit and inspectable.
    """

    def _score(self, query_tokens: set[str], *texts: str, bonus: int = 0) -> int:
        haystack_tokens: set[str] = set()
        for text in texts:
            haystack_tokens.update(_tokenize(text))
        overlap = query_tokens.intersection(haystack_tokens)
        return len(overlap) * 3 + bonus

    def build_report(
        self,
        *,
        recovered_statement: str,
        checkpoint_contract: dict[str, Any],
        route_scaffold: dict[str, Any],
        theorem_hints: list[dict[str, Any]],
        literature_theorem_inventory: dict[str, Any],
        porting_candidates: list[dict[str, Any]],
        latest_next_obligation: list[str],
    ) -> dict[str, Any]:
        query_seeds = [
            recovered_statement,
            str(checkpoint_contract.get("checkpoint_statement", "")),
            *[str(item) for item in checkpoint_contract.get("dependency_chain", [])[:3]],
            *[str(item) for item in route_scaffold.get("next_formal_obligations", [])[:3]],
            *latest_next_obligation[:4],
        ]
        query_tokens = set()
        for seed in query_seeds:
            query_tokens.update(_tokenize(seed))

        local_candidates: list[dict[str, Any]] = []
        for item in theorem_hints:
            score = self._score(
                query_tokens,
                str(item.get("name", "")),
                str(item.get("statement", "")),
                str(item.get("path", "")),
            )
            local_candidates.append(
                {
                    "kind": "local_lean",
                    "name": item.get("name", ""),
                    "statement": item.get("statement", ""),
                    "path": item.get("path", ""),
                    "line": item.get("line"),
                    "score": score,
                }
            )
        local_candidates.sort(key=lambda item: (-int(item["score"]), len(str(item.get("statement", "")))))

        literature_candidates: list[dict[str, Any]] = []
        for entry in literature_theorem_inventory.get("entries", []):
            score = self._score(
                query_tokens,
                str(entry.get("statement", "")),
                str(entry.get("title", "")),
                str(entry.get("source", "")),
                bonus=2 if entry.get("recommended_action") == "restage_as_local_checkpoint" else 0,
            )
            literature_candidates.append(
                {
                    "kind": "literature",
                    "inventory_id": entry.get("inventory_id", ""),
                    "role": entry.get("role", ""),
                    "statement": entry.get("statement", ""),
                    "source": entry.get("source", ""),
                    "score": score,
                }
            )
        literature_candidates.sort(key=lambda item: (-int(item["score"]), len(str(item.get("statement", "")))))

        porting_hits: list[dict[str, Any]] = []
        for entry in porting_candidates:
            score = self._score(
                query_tokens,
                str(entry.get("name", "")),
                str(entry.get("signature", "")),
                str(entry.get("recommended_next_step", "")),
                bonus=3 if entry.get("usable_for_main_claim") else 0,
            )
            porting_hits.append(
                {
                    "kind": "porting_candidate",
                    "name": entry.get("name", ""),
                    "signature": entry.get("signature", ""),
                    "source_path": entry.get("source_path", ""),
                    "recommended_next_step": entry.get("recommended_next_step", ""),
                    "score": score,
                }
            )
        porting_hits.sort(key=lambda item: (-int(item["score"]), len(str(item.get("signature", "")))))

        edit_targets: list[dict[str, Any]] = []
        for item in route_scaffold.get("first_edit_targets", []):
            edit_targets.append({"target": str(item), "score": self._score(query_tokens, str(item), bonus=2)})
        for item in route_scaffold.get("next_formal_obligations", []):
            edit_targets.append({"target": str(item), "score": self._score(query_tokens, str(item), bonus=1)})
        edit_targets.sort(key=lambda item: (-int(item["score"]), len(str(item.get("target", "")))))

        return {
            "generated_at": utc_now_iso(),
            "query_seed_texts": [item for item in query_seeds if item],
            "query_token_count": len(query_tokens),
            "local_lean_premises": local_candidates[:8],
            "literature_premises": literature_candidates[:8],
            "porting_candidates": porting_hits[:5],
            "edit_targets": edit_targets[:6],
        }
