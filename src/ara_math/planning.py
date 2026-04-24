from __future__ import annotations

import re
from typing import Any

from ara_math.models import ClaimRecord, ProblemRecord, ProofPlan, ProofTask
from ara_math.workspace import utc_now_iso


class MathPlanner:
    """Generate a first-pass proof plan from structured problem metadata."""

    LITERATURE_IMPORT_FAMILIES = {
        "triangle_dissection",
        "unitary_perfect",
        "prime_gap_spectrum",
        "prime_plus_two_powers",
        "minimum_overlap",
        "ap_free_bounds",
        "weird_numbers",
    }
    GENERIC_ROUTE_NOISE = (
        "write up and publish",
        "formalization still valuable",
        "computational verification",
        "show no valid configuration exists",
        "prove no valid dissection exists",
        "detailed statement should be imported",
    )

    def _target_statement(self, problem: ProblemRecord, proof_path_assessment: dict[str, Any] | None) -> str:
        literature = (proof_path_assessment or {}).get("literature", {})
        recovered = str(literature.get("recovered_statement", "")).strip()
        return recovered or problem.statement

    def _infer_problem_family(self, problem: ProblemRecord, *, target_statement: str) -> str:
        metadata = problem.metadata or {}
        text = " ".join(
            [
                problem.problem_id,
                problem.title,
                target_statement,
                problem.statement,
                " ".join(problem.tags),
                str(metadata.get("comments", "")),
            ]
        ).lower()
        if "triangle" in text or "equilateral" in text or "dissection" in text or "三角形" in text or "分割" in text:
            return "triangle_dissection"
        if "unitary" in text and "perfect" in text:
            return "unitary_perfect"
        if "weird" in text:
            return "weird_numbers"
        if "p + 2^k + 2^l" in text or "2^k + 2^l" in text:
            return "prime_plus_two_powers"
        if "minimum overlap" in text or ("partition" in text and "overlap" in text):
            return "minimum_overlap"
        if "arithmetic progression" in text or "r_k" in text or "progression-free" in text:
            return "ap_free_bounds"
        if "p_{n+1}" in text or ("prime" in text and "log" in text and "gap" in text):
            return "prime_gap_spectrum"
        return "generic"

    def _inventory_role(self, *, statement: str, bucket: str, family: str) -> str:
        lower = statement.lower()
        if bucket == "modern_tools":
            return "method"
        if any(token in lower for token in ("impossible", "nonexistence", "cannot", "no valid", "no odd", "finite", "bounded")):
            return "obstruction"
        if any(token in lower for token in ("construct", "construction", "achievable", "possible", "there exists", "n²", "square")):
            return "positive_family"
        if any(
            token in lower
            for token in (
                "lemma",
                "criterion",
                "constraint",
                "graph",
                "encoding",
                "parity",
                "bound",
                "density",
                "lower bound",
                "upper bound",
                "support",
                "degree",
            )
        ):
            return "supporting_lemma"
        if family == "triangle_dissection" and any(token in lower for token in ("tiling", "triangle", "equilateral", "tutte", "beeson")):
            return "supporting_lemma"
        return "checkpoint"

    def _lean_targets_for_role(self, role: str) -> list[str]:
        if role == "method":
            return ["proof/proof_gap_notes.md", "proof/proof_route_scaffold.json"]
        if role == "obstruction":
            return ["formal/MathProject/GeneratedClaims.lean", "formal/MathProject/MainClaim.lean"]
        if role == "positive_family":
            return ["formal/MathProject/Basic.lean", "formal/MathProject/GeneratedClaims.lean"]
        return ["formal/MathProject/GeneratedClaims.lean", "formal/MathProject/MainClaim.lean"]

    def _inventory_priority(self, role: str) -> int:
        if role == "obstruction":
            return 9
        if role == "positive_family":
            return 8
        if role == "supporting_lemma":
            return 7
        if role == "method":
            return 6
        return 5

    def _supporting_entries_for_framework(
        self,
        framework: dict[str, Any],
        *,
        theorem_inventory: dict[str, Any],
    ) -> list[dict[str, Any]]:
        entry_map = {entry["inventory_id"]: entry for entry in theorem_inventory.get("entries", [])}
        return [
            entry_map[inventory_id]
            for inventory_id in framework.get("supporting_inventory_ids", [])
            if inventory_id in entry_map
        ]

    def _problem_keywords(self, problem: ProblemRecord, *, target_statement: str, family: str) -> set[str]:
        text = " ".join(
            [
                problem.problem_id,
                problem.title,
                target_statement,
                problem.statement,
                " ".join(problem.tags),
                str(problem.metadata or {}),
            ]
        ).lower()
        keywords = {token for token in re.findall(r"[a-z0-9_+-]+", text) if len(token) >= 4}
        family_keywords = {
            "triangle_dissection": {"triangle", "triangles", "equilateral", "dissection", "tiling", "tutte", "beeson"},
            "unitary_perfect": {
                "unitary",
                "perfect",
                "divisor",
                "divisors",
                "harmonic",
                "subbarao",
                "warren",
                "goto",
                "wall",
                "biunitary",
            },
            "prime_gap_spectrum": {"prime", "gaps", "gap", "spectrum", "limit", "normalized", "pintz", "maynard"},
            "prime_plus_two_powers": {"prime", "powers", "exceptional", "odd", "density", "crocker", "pan"},
            "minimum_overlap": {"overlap", "difference", "partition", "multiplicity", "white", "haugland"},
            "weird_numbers": {"weird", "abundant", "semiperfect", "abundance"},
            "ap_free_bounds": {"progression", "ap-free", "density", "bound", "capset", "behrend"},
        }
        keywords.update(family_keywords.get(family, set()))
        return keywords

    def _inventory_negative_markers(self, family: str) -> set[str]:
        negatives = {
            "triangle_dissection": {"unitary", "perfect number", "unitary perfect", "odd unitary"},
            "unitary_perfect": {
                "triangle tiling",
                "equilateral triangle",
                "triangle dissection",
                "tiling",
                "cayley graph",
                "cayley graphs",
                "unitary group",
                "unitary groups",
                "hermitian form",
                "hermitian forms",
                "centralizers",
                "classical groups",
                "entanglement",
                "qudit",
                "locc",
            },
            "prime_gap_spectrum": {"triangle tiling", "unitary perfect", "weird number"},
            "prime_plus_two_powers": {"triangle tiling", "unitary perfect", "overlap problem"},
        }
        return negatives.get(family, set())

    def _statement_relevance(
        self,
        *,
        statement: str,
        title: str,
        source: str,
        bucket: str,
        keywords: set[str],
        family: str,
    ) -> int:
        statement_text = statement.lower()
        metadata_text = " ".join([title, source]).lower()
        text = f"{statement_text} {metadata_text}"
        score = 0
        for keyword in keywords:
            if keyword in statement_text:
                score += 2
            elif keyword in metadata_text:
                score += 1
        family_negatives = self._inventory_negative_markers(family)
        if family == "unitary_perfect" and any(marker in text for marker in family_negatives):
            if not any(token in text for token in ("unitary perfect", "perfect number", "perfect numbers", "unitary totient", "ϕ∗", "divisor")):
                return -10
        if any(noise in text for noise in self.GENERIC_ROUTE_NOISE):
            score -= 4
        if family == "triangle_dissection" and any(token in text for token in ("triangle", "equilateral", "tiling", "dissection")):
            score += 2
        if family == "triangle_dissection" and any(token in text for token in ("7-tiling", "11-tiling", "any triangle by any tile", "cannot be tiled")):
            score += 4
        if family == "unitary_perfect" and any(token in text for token in ("unitary", "perfect", "divisor", "goto", "wall", "subbarao", "warren")):
            score += 2
        if family == "unitary_perfect" and any(token in text for token in ("ϕ∗", "phi*", "divisible by", "odd usp", "unitary totient")):
            score += 4
        if any(
            token in text
            for token in (
                "there is no",
                "cannot be",
                "for every",
                "if ",
                "then ",
                "only n-tilings",
                "there are finitely many",
                "no odd",
                "equivalent",
                "if p is a positive prime",
            )
        ):
            score += 3
        if re.search(r"\b(?:7|11|19|24|1052)\b", text):
            score += 2
        if any(marker in text for marker in family_negatives):
            score -= 4
        if any(
            noise in text
            for noise in (
                "write up and publish",
                "arxiv, google scholar",
                "geogebra, mathematica",
                "computational verification",
            )
        ):
            score -= 3
        if bucket == "paper_theorem":
            score += 4
        if bucket == "modern_tools" and any(token in text for token in ("lean", "formal", "proof assistant")):
            score += 2
        return score

    def build_theorem_inventory(
        self,
        *,
        problem: ProblemRecord,
        proof_path_assessment: dict[str, Any] | None = None,
        paper_inventory: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        target_statement = self._target_statement(problem, proof_path_assessment)
        family = self._infer_problem_family(problem, target_statement=target_statement)
        keywords = self._problem_keywords(problem, target_statement=target_statement, family=family)
        literature = (proof_path_assessment or {}).get("literature", {})
        candidates: list[tuple[int, int, dict[str, Any]]] = []
        seen: set[str] = set()
        candidate_sources = (
            ("known_results", literature.get("known_results", [])),
            ("proof_ingredients", literature.get("proof_ingredients", [])),
            ("modern_tools", literature.get("modern_tools", [])),
        )
        for bucket, items in candidate_sources:
            for item in items:
                statement = str(item.get("statement", "")).strip()
                if len(statement) < 12:
                    continue
                normalized = re.sub(r"\s+", " ", statement).strip().lower()
                if normalized in seen:
                    continue
                relevance = self._statement_relevance(
                    statement=statement,
                    title=str(item.get("title", "")).strip(),
                    source=str(item.get("source", "")).strip(),
                    bucket=bucket,
                    keywords=keywords,
                    family=family,
                )
                if bucket == "modern_tools":
                    if relevance <= 0:
                        continue
                elif relevance <= 0:
                    continue
                role = self._inventory_role(statement=statement, bucket=bucket, family=family)
                seen.add(normalized)
                priority = self._inventory_priority(role)
                candidates.append(
                    (
                        relevance,
                        priority,
                        {
                            "inventory_id": "",
                            "statement": statement,
                            "role": role,
                            "bucket": bucket,
                            "source": str(item.get("source", "")).strip(),
                            "title": str(item.get("title", "")).strip(),
                            "priority": priority,
                            "relevance": relevance,
                            "lean_targets": self._lean_targets_for_role(role),
                            "recommended_action": (
                                "restage_as_local_checkpoint"
                                if role in {"obstruction", "positive_family"}
                                else "extract_supporting_lemma"
                                if role == "supporting_lemma"
                                else "turn_into_route_note"
                            ),
                        },
                    )
                )

        for record in (paper_inventory or {}).get("records", []):
            title = str(record.get("title", "")).strip()
            source = str(record.get("local_path", "")).strip() or str(record.get("source_url", "")).strip()
            for snippet in record.get("theorem_snippets", [])[:6]:
                statement = str(snippet.get("statement", "")).strip()
                if len(statement) < 24:
                    continue
                normalized = re.sub(r"\s+", " ", statement).strip().lower()
                if normalized in seen:
                    continue
                relevance = self._statement_relevance(
                    statement=statement,
                    title=title,
                    source=source,
                    bucket="paper_theorem",
                    keywords=keywords,
                    family=family,
                )
                if relevance <= 0:
                    continue
                role = self._inventory_role(statement=statement, bucket="known_results", family=family)
                snippet_kind = str(snippet.get("kind", "")).strip().lower()
                if snippet_kind == "remark" and not any(
                    token in statement.lower() for token in ("there is no", "cannot", "for every", "if p is", "if n is")
                ):
                    continue
                seen.add(normalized)
                priority = max(self._inventory_priority(role), 10 if role in {"obstruction", "positive_family"} else 8)
                if snippet_kind == "remark":
                    priority = max(priority - 2, 6)
                label = str(snippet.get("label", "")).strip()
                heading = str(snippet.get("kind", "")).strip().title() or "Theorem"
                title_prefix = f"{heading} {label}".strip() if label else heading
                candidates.append(
                    (
                        relevance + 4,
                        priority,
                        {
                            "inventory_id": "",
                            "statement": statement,
                            "role": role,
                            "bucket": "paper_theorem",
                            "source": source,
                            "title": f"{title_prefix} from {title}".strip(),
                            "priority": priority,
                            "relevance": relevance + 4,
                            "lean_targets": self._lean_targets_for_role(role),
                            "recommended_action": "restage_as_local_checkpoint"
                            if role in {"obstruction", "positive_family"}
                            else "extract_supporting_lemma",
                        },
                    )
                )

        candidates.sort(key=lambda item: (-item[0], -item[1], len(str(item[2].get("statement", "")))))
        entries: list[dict[str, Any]] = []
        for _, _, candidate in candidates[:12]:
            candidate["inventory_id"] = f"{problem.problem_id}:inv:{len(entries) + 1:02d}"
            entries.append(candidate)

        if not entries:
            entries.append(
                {
                    "inventory_id": f"{problem.problem_id}:inv:01",
                    "statement": target_statement,
                    "role": "checkpoint",
                    "bucket": "target_statement",
                    "source": "problem statement",
                    "title": problem.title,
                    "priority": 5,
                    "lean_targets": self._lean_targets_for_role("checkpoint"),
                    "recommended_action": "narrow_main_claim",
                }
            )

        paper_records = (paper_inventory or {}).get("records", [])
        accessible_papers = [
            {
                "title": str(record.get("title", "")).strip(),
                "status": str(record.get("status", "")).strip(),
                "source_url": str(record.get("source_url", "")).strip(),
                "local_path": str(record.get("local_path", "")).strip(),
            }
            for record in paper_records
            if str(record.get("status", "")).strip() in {"downloaded_pdf", "existing_local_copy", "saved_landing_snapshot"}
        ]
        unresolved_papers = [
            {
                "title": str(record.get("title", "")).strip(),
                "status": str(record.get("status", "")).strip(),
                "source_url": str(record.get("source_url", "")).strip(),
            }
            for record in paper_records
            if str(record.get("status", "")).strip() in {"metadata_only", "manual_followup_required", "download_error"}
        ]

        entries.sort(key=lambda entry: (-int(entry.get("priority", 0)), len(str(entry.get("statement", "")))))
        return {
            "generated_at": utc_now_iso(),
            "problem_id": problem.problem_id,
            "problem_family": family,
            "target_statement": target_statement,
            "entry_count": len(entries),
            "entries": entries,
            "accessible_papers": accessible_papers[:8],
            "unresolved_papers": unresolved_papers[:8],
        }

    def build_proof_path_frameworks(
        self,
        *,
        problem: ProblemRecord,
        proof_path_assessment: dict[str, Any] | None = None,
        theorem_inventory: dict[str, Any],
    ) -> dict[str, Any]:
        family = str(theorem_inventory.get("problem_family", "generic")).strip() or "generic"
        entries = list(theorem_inventory.get("entries", []))
        obstructions = [entry for entry in entries if entry.get("role") == "obstruction"]
        positive = [entry for entry in entries if entry.get("role") == "positive_family"]
        support = [entry for entry in entries if entry.get("role") in {"supporting_lemma", "checkpoint"}]
        methods = [entry for entry in entries if entry.get("role") == "method"]
        blockers = list((proof_path_assessment or {}).get("blockers", []))[:4]
        accessible_papers = list(theorem_inventory.get("accessible_papers", []))

        frameworks: list[dict[str, Any]] = []

        primary_entry = (obstructions or positive or support or entries)[0]
        frameworks.append(
            {
                "framework_id": "route_literature_checkpoint",
                "title": "Literature-backed checkpoint import",
                "route_type": "literature_import",
                "summary": (
                    f"Use `{primary_entry['statement']}` as the first imported checkpoint before attacking the full target."
                ),
                "supporting_inventory_ids": [entry["inventory_id"] for entry in (obstructions + positive + support)[:3]],
                "first_edit_targets": [
                    "proof/proof_gap_notes.md",
                    "formal/MathProject/GeneratedClaims.lean",
                    "formal/MathProject/MainClaim.lean",
                ],
                "milestones": [
                    "Normalize notation and theorem shape against one cited paper theorem.",
                    "Restage that theorem as a local Lean checkpoint or narrowed main claim.",
                    "Only after the checkpoint builds, extend it toward the open target.",
                ],
                "source_papers": [paper["title"] for paper in accessible_papers[:3]],
                "blockers": blockers,
                "priority": 9 if family in self.LITERATURE_IMPORT_FAMILIES else 7,
            }
        )

        secondary_entry = (support or obstructions or positive or entries)[0]
        frameworks.append(
            {
                "framework_id": "route_supporting_lemma_chain",
                "title": "Supporting-lemma chain",
                "route_type": "lemma_chain",
                "summary": (
                    f"Decompose the target through `{secondary_entry['statement']}` and one or two reusable lemma obligations."
                ),
                "supporting_inventory_ids": [entry["inventory_id"] for entry in (support + methods + obstructions)[:4]],
                "first_edit_targets": [
                    "proof/proof_gap_notes.md",
                    "formal/MathProject/Basic.lean",
                    "formal/MathProject/GeneratedClaims.lean",
                ],
                "milestones": [
                    "Turn one literature hint into a formal supporting lemma skeleton.",
                    "Record the dependency chain from that lemma to the current main target.",
                    "Prove or restage the strongest reusable lemma before touching the open theorem.",
                ],
                "source_papers": [paper["title"] for paper in accessible_papers[:2]],
                "blockers": blockers,
                "priority": 8,
            }
        )

        if any(tag in problem.tags for tag in ("computational_search", "finite_case", "divisors")) or family in {
            "minimum_overlap",
            "prime_plus_two_powers",
            "weird_numbers",
        }:
            frameworks.append(
                {
                    "framework_id": "route_certificate_or_search",
                    "title": "Certificate or bounded-search route",
                    "route_type": "certificate_search",
                    "summary": "Use a literature-backed finite certificate, bounded search, or explicit obstruction family as the first nontrivial milestone.",
                    "supporting_inventory_ids": [entry["inventory_id"] for entry in (support + methods)[:4]],
                    "first_edit_targets": [
                        "proof/counterexample_search_contract.json",
                        "proof/proof_gap_notes.md",
                        "formal/MathProject/GeneratedClaims.lean",
                    ],
                    "milestones": [
                        "Specify one exact finite contract justified by the literature.",
                        "Encode the search/certificate assumptions explicitly.",
                        "Connect the certificate theorem back into the Lean claim graph.",
                    ],
                    "source_papers": [paper["title"] for paper in accessible_papers[:2]],
                    "blockers": blockers,
                    "priority": 7,
                }
            )

        frameworks.sort(key=lambda item: -int(item.get("priority", 0)))
        recommended = frameworks[0] if frameworks else {}
        return {
            "generated_at": utc_now_iso(),
            "problem_id": problem.problem_id,
            "problem_family": family,
            "framework_count": len(frameworks),
            "recommended_framework_id": str(recommended.get("framework_id", "")),
            "recommended_rationale": (
                "Prefer the route that imports one literature-backed checkpoint before any broad Lean proof search."
                if recommended
                else "No framework available."
            ),
            "frameworks": frameworks,
        }

    def build_theorem_graph(
        self,
        *,
        problem: ProblemRecord,
        theorem_inventory: dict[str, Any],
        proof_path_frameworks: dict[str, Any],
    ) -> dict[str, Any]:
        nodes = [
            {
                "node_id": entry["inventory_id"],
                "statement": entry["statement"],
                "role": entry["role"],
                "bucket": entry["bucket"],
                "title": entry.get("title", ""),
                "source": entry.get("source", ""),
                "priority": int(entry.get("priority", 0)),
            }
            for entry in theorem_inventory.get("entries", [])
        ]
        target_node_id = f"{problem.problem_id}:target"
        nodes.append(
            {
                "node_id": target_node_id,
                "statement": theorem_inventory.get("target_statement", problem.statement),
                "role": "open_target",
                "bucket": "target_statement",
                "title": problem.title,
                "source": "problem statement",
                "priority": 10,
            }
        )

        edges: list[dict[str, Any]] = []
        seen_edges: set[tuple[str, str, str]] = set()
        for framework in proof_path_frameworks.get("frameworks", []):
            supporting_entries = self._supporting_entries_for_framework(framework, theorem_inventory=theorem_inventory)
            supporting_ids = [entry["inventory_id"] for entry in supporting_entries]
            for source_id, target_id in zip(supporting_ids, supporting_ids[1:]):
                key = (source_id, target_id, str(framework.get("framework_id", "")))
                if key in seen_edges:
                    continue
                seen_edges.add(key)
                edges.append(
                    {
                        "source": source_id,
                        "target": target_id,
                        "relation": "route_dependency",
                        "framework_id": framework.get("framework_id", ""),
                    }
                )
            if supporting_ids:
                key = (supporting_ids[-1], target_node_id, str(framework.get("framework_id", "")))
                if key not in seen_edges:
                    seen_edges.add(key)
                    edges.append(
                        {
                            "source": supporting_ids[-1],
                            "target": target_node_id,
                            "relation": "route_target",
                            "framework_id": framework.get("framework_id", ""),
                        }
                    )

        return {
            "generated_at": utc_now_iso(),
            "problem_id": problem.problem_id,
            "target_node_id": target_node_id,
            "recommended_framework_id": str(proof_path_frameworks.get("recommended_framework_id", "")),
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes": nodes,
            "edges": edges,
        }

    def _family_route_blockers(
        self,
        *,
        family: str,
        supporting_entries: list[dict[str, Any]],
        theorem_inventory: dict[str, Any],
        framework: dict[str, Any],
        proof_path_assessment: dict[str, Any] | None,
    ) -> list[str]:
        blockers = [str(item).strip() for item in (proof_path_assessment or {}).get("blockers", []) if str(item).strip()]
        unresolved_papers = theorem_inventory.get("unresolved_papers", [])
        if unresolved_papers:
            unresolved_titles = [str(item.get("title", "")).strip() for item in unresolved_papers[:3] if str(item.get("title", "")).strip()]
            if unresolved_titles:
                blockers.append(
                    "Resolve access or precise metadata for these papers before Lean formalization: "
                    + ", ".join(unresolved_titles)
                    + "."
                )

        route_type = str(framework.get("route_type", "")).strip()
        statements_lower = " ".join(entry.get("statement", "") for entry in supporting_entries).lower()
        if route_type == "literature_import":
            blockers.append(
                "Write the first checkpoint as a paper-faithful theorem statement with explicit assumptions before encoding any Lean shell around it."
            )
        if family == "triangle_dissection":
            if any(token in statements_lower for token in ("7-tiling", "11-tiling", "cannot be tiled", "similar to abc")):
                blockers.append(
                    "Need a theorem-level bridge from Beeson-style similar-right split hypotheses to boundary-support or strict-smaller-than-host consequences."
                )
            blockers.append(
                "Do not widen to the full classification until one cited nonexistence or positive-family theorem is written as a complete prose checkpoint."
            )
        elif family == "unitary_perfect":
            blockers.append(
                "Need a paper-level reduction chain from odd-unitary-perfect exclusion and finiteness/boundedness results to the chosen checkpoint theorem."
            )
        elif family == "minimum_overlap":
            blockers.append(
                "Need one explicit quantitative overlap theorem with its exact constant and hypotheses before formal search contracts are trustworthy."
            )
        elif family == "prime_gap_spectrum":
            blockers.append(
                "Need one exact interval or limit-point theorem from the literature, not just qualitative statements about prime gaps."
            )

        deduped: list[str] = []
        seen: set[str] = set()
        for blocker in blockers:
            if blocker in seen:
                continue
            seen.add(blocker)
            deduped.append(blocker)
        return deduped[:6]

    def build_route_candidates(
        self,
        *,
        problem: ProblemRecord,
        theorem_inventory: dict[str, Any],
        theorem_graph: dict[str, Any],
        proof_path_frameworks: dict[str, Any],
        proof_path_assessment: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        recommended_id = str(proof_path_frameworks.get("recommended_framework_id", "")).strip()
        accessible_papers = theorem_inventory.get("accessible_papers", [])
        candidates: list[dict[str, Any]] = []
        for framework in proof_path_frameworks.get("frameworks", []):
            supporting_entries = self._supporting_entries_for_framework(framework, theorem_inventory=theorem_inventory)
            blockers = self._family_route_blockers(
                family=str(theorem_inventory.get("problem_family", "generic")).strip() or "generic",
                supporting_entries=supporting_entries,
                theorem_inventory=theorem_inventory,
                framework=framework,
                proof_path_assessment=proof_path_assessment,
            )
            route_type = str(framework.get("route_type", "")).strip()
            has_checkpoint = any(
                entry.get("recommended_action") == "restage_as_local_checkpoint"
                or entry.get("role") in {"obstruction", "positive_family"}
                for entry in supporting_entries
            )
            hard_route_blockers = (
                "Resolve access or precise metadata",
                "Write the first checkpoint as a paper-faithful theorem statement",
                "Need a theorem-level bridge",
                "Need a paper-level reduction chain",
            )
            ready_for_formalization = (
                bool(accessible_papers)
                and has_checkpoint
                and not any(blocker.startswith(hard_blocker) for blocker in blockers for hard_blocker in hard_route_blockers)
            )
            candidates.append(
                {
                    "route_id": str(framework.get("framework_id", "")).strip(),
                    "title": str(framework.get("title", "")).strip(),
                    "route_type": route_type,
                    "selected": str(framework.get("framework_id", "")).strip() == recommended_id,
                    "mathematical_objective": str(framework.get("summary", "")).strip(),
                    "theorem_chain": [
                        {
                            "inventory_id": entry.get("inventory_id", ""),
                            "role": entry.get("role", ""),
                            "statement": entry.get("statement", ""),
                            "source": entry.get("source", ""),
                        }
                        for entry in supporting_entries
                    ],
                    "source_papers": list(framework.get("source_papers", [])),
                    "graph_edges": [
                        edge
                        for edge in theorem_graph.get("edges", [])
                        if edge.get("framework_id") == framework.get("framework_id", "")
                    ],
                    "mathematical_blockers": blockers,
                    "next_non_lean_steps": [
                        "Write the exact first checkpoint theorem in ordinary mathematical language.",
                        "Record the theorem-to-theorem dependency chain that connects that checkpoint back to the open target.",
                        "Delay Lean formalization until the first checkpoint theorem and its prerequisites are fixed in prose.",
                    ],
                    "formalization_gate": [
                        "One cited theorem is chosen as the first checkpoint.",
                        "Its full assumptions are rewritten in project-local notation without Lean placeholders.",
                        "The dependency chain from that theorem to the main open target is explicit.",
                    ],
                    "ready_for_formalization": ready_for_formalization,
                    "why_plausible": (
                        "This route is anchored in cited theorems and keeps the first milestone narrow."
                        if route_type == "literature_import"
                        else "This route decomposes the target into supporting lemmas before any broad theorem attempt."
                    ),
                }
            )

        selected_route_id = recommended_id or (candidates[0]["route_id"] if candidates else "")
        return {
            "generated_at": utc_now_iso(),
            "problem_id": problem.problem_id,
            "target_statement": theorem_inventory.get("target_statement", problem.statement),
            "selected_route_id": selected_route_id,
            "candidate_count": len(candidates),
            "candidates": candidates,
        }

    def build_mathematical_blockers(
        self,
        *,
        problem: ProblemRecord,
        theorem_inventory: dict[str, Any],
        route_candidates: dict[str, Any],
    ) -> dict[str, Any]:
        selected_id = str(route_candidates.get("selected_route_id", "")).strip()
        candidates = list(route_candidates.get("candidates", []))
        selected = next(
            (candidate for candidate in candidates if candidate.get("route_id") == selected_id),
            candidates[0] if candidates else {},
        )
        blockers = list((selected or {}).get("mathematical_blockers", []))
        blockers.append(
            "Do not treat Lean shell growth as progress unless it shortens the explicit theorem chain in the selected paper-first route."
        )
        return {
            "generated_at": utc_now_iso(),
            "problem_id": problem.problem_id,
            "selected_route_id": selected_id,
            "blocker_count": len(blockers),
            "blockers": blockers,
            "ready_for_formalization": bool((selected or {}).get("ready_for_formalization", False)),
        }

    def render_selected_route_markdown(
        self,
        *,
        problem: ProblemRecord,
        theorem_inventory: dict[str, Any],
        route_candidates: dict[str, Any],
        mathematical_blockers: dict[str, Any],
    ) -> str:
        selected_id = str(route_candidates.get("selected_route_id", "")).strip()
        candidates = list(route_candidates.get("candidates", []))
        selected = next(
            (candidate for candidate in candidates if candidate.get("route_id") == selected_id),
            candidates[0] if candidates else {},
        ) or {}
        lines = [
            f"# Selected Route for {problem.problem_id}",
            "",
            f"- Problem: {problem.title}",
            f"- Target statement: {theorem_inventory.get('target_statement', problem.statement)}",
            f"- Selected route: {selected.get('route_id', '')} / {selected.get('title', '')}",
            f"- Ready for formalization: {'yes' if selected.get('ready_for_formalization') else 'not yet'}",
            "",
            "## Mathematical Objective",
            "",
            str(selected.get("mathematical_objective", "")).strip() or "No route objective recorded.",
            "",
            "## Theorem Chain",
            "",
        ]
        theorem_chain = selected.get("theorem_chain", [])
        if theorem_chain:
            for item in theorem_chain:
                lines.append(
                    f"- [{item.get('role', '')}] {item.get('statement', '')}"
                    + (f"  Source: {item.get('source', '')}" if item.get("source") else "")
                )
        else:
            lines.append("- No theorem chain recorded yet.")
        lines.extend(
            [
                "",
                "## Next Non-Lean Steps",
                "",
            ]
        )
        for item in selected.get("next_non_lean_steps", []):
            lines.append(f"- {item}")
        lines.extend(
            [
                "",
                "## Formalization Gate",
                "",
            ]
        )
        for item in selected.get("formalization_gate", []):
            lines.append(f"- {item}")
        lines.extend(
            [
                "",
                "## Mathematical Blockers",
                "",
            ]
        )
        for blocker in mathematical_blockers.get("blockers", []):
            lines.append(f"- {blocker}")
        lines.append("")
        return "\n".join(lines)

    def build_route_scaffold(
        self,
        *,
        problem: ProblemRecord,
        theorem_inventory: dict[str, Any],
        proof_path_frameworks: dict[str, Any],
    ) -> dict[str, Any]:
        frameworks = list(proof_path_frameworks.get("frameworks", []))
        recommended_id = str(proof_path_frameworks.get("recommended_framework_id", "")).strip()
        recommended = next((item for item in frameworks if item.get("framework_id") == recommended_id), frameworks[0] if frameworks else {})
        entry_map = {entry["inventory_id"]: entry for entry in theorem_inventory.get("entries", [])}
        supporting_entries = [
            entry_map[inventory_id]
            for inventory_id in recommended.get("supporting_inventory_ids", [])
            if inventory_id in entry_map
        ]
        next_obligations = []
        for entry in supporting_entries[:3]:
            next_obligations.append(
                f"Restage `{entry['statement']}` as `{entry['recommended_action']}` in {', '.join(entry['lean_targets'])}."
            )
        if not next_obligations:
            next_obligations.append("Narrow the main claim to one literature-backed checkpoint theorem.")
        return {
            "generated_at": utc_now_iso(),
            "problem_id": problem.problem_id,
            "selected_framework_id": str(recommended.get("framework_id", "")),
            "title": str(recommended.get("title", "")).strip(),
            "summary": str(recommended.get("summary", "")).strip(),
            "first_edit_targets": list(recommended.get("first_edit_targets", [])),
            "milestones": list(recommended.get("milestones", [])),
            "supporting_inventory_ids": list(recommended.get("supporting_inventory_ids", [])),
            "next_formal_obligations": next_obligations,
            "source_papers": list(recommended.get("source_papers", [])),
        }

    def _route_discovery_anti_patterns(self, family: str) -> list[str]:
        anti_patterns = [
            "Do not spend the attempt on local Lean cleanup unless it directly unlocks a named literature-backed route.",
            "Do not keep refining shell lemmas that fail to move closer to the original open statement.",
            "If no route survives scrutiny, explicitly record that the current evidence is insufficient and stop.",
        ]
        if family == "triangle_dissection":
            anti_patterns.append(
                "Do not add more boundary/parity shell lemmas unless they directly bridge to `seven_impossible`, `eleven_impossible`, or another cited nonexistence theorem."
            )
        elif family == "unitary_perfect":
            anti_patterns.append(
                "Do not chase local divisor-function cleanup unless it clearly reduces the project to one placeholder-free finiteness theorem in the Goto/Wall line."
            )
        return anti_patterns

    def build_route_discovery_brief(
        self,
        *,
        problem: ProblemRecord,
        theorem_inventory: dict[str, Any],
        proof_path_frameworks: dict[str, Any],
        route_scaffold: dict[str, Any],
        proof_path_assessment: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        family = str(theorem_inventory.get("problem_family", "")).strip() or self._infer_problem_family(
            problem,
            target_statement=self._target_statement(problem, proof_path_assessment),
        )
        entry_map = {entry["inventory_id"]: entry for entry in theorem_inventory.get("entries", [])}
        frameworks = list(proof_path_frameworks.get("frameworks", []))
        route_candidates: list[dict[str, Any]] = []
        for framework in frameworks[:4]:
            supporting_entries = [
                entry_map[inventory_id]
                for inventory_id in framework.get("supporting_inventory_ids", [])
                if inventory_id in entry_map
            ]
            route_candidates.append(
                {
                    "framework_id": framework.get("framework_id", ""),
                    "title": framework.get("title", ""),
                    "summary": framework.get("summary", ""),
                    "supporting_inventory": [
                        {
                            "inventory_id": entry.get("inventory_id", ""),
                            "role": entry.get("role", ""),
                            "statement": entry.get("statement", ""),
                        }
                        for entry in supporting_entries[:3]
                    ],
                    "first_edit_targets": list(framework.get("first_edit_targets", [])),
                    "acceptance_criteria": [
                        "Names at least one literature-backed theorem, obstruction, or checkpoint that can be imported or restaged.",
                        "Identifies the first Lean or proof-note target that would embody that route.",
                        "Explains why this route moves the project toward the original theorem rather than only polishing a local shell.",
                    ],
                    "exit_signal": (
                        "The route can be written as a bounded theorem-import or reduction chain that reaches the original target."
                    ),
                }
            )
        blockers = list((proof_path_assessment or {}).get("blockers", []))[:5]
        return {
            "generated_at": utc_now_iso(),
            "problem_id": problem.problem_id,
            "problem_family": family,
            "objective": (
                "Identify one globally plausible proof path before broad Lean edits; reject routes that only yield local shell refinements."
            ),
            "preferred_framework_id": str(route_scaffold.get("selected_framework_id", "")).strip(),
            "preferred_framework_title": str(route_scaffold.get("title", "")).strip(),
            "route_candidates": route_candidates,
            "preferred_next_formal_obligations": list(route_scaffold.get("next_formal_obligations", [])),
            "anti_patterns": self._route_discovery_anti_patterns(family),
            "current_blockers": blockers,
            "deliverables": [
                "A chosen route or an explicit rejection of every current route candidate.",
                "One literature-backed checkpoint theorem or reduction target that should be formalized next.",
                "A proof-gap note explaining what missing paper, theorem, or modeling bridge still blocks progress.",
            ],
        }

    def build_plan(
        self,
        *,
        project_name: str,
        problem: ProblemRecord,
        proof_path_assessment: dict[str, Any] | None = None,
        theorem_inventory: dict[str, Any] | None = None,
        proof_path_frameworks: dict[str, Any] | None = None,
        route_candidates: dict[str, Any] | None = None,
        mathematical_blockers: dict[str, Any] | None = None,
    ) -> ProofPlan:
        target_statement = self._target_statement(problem, proof_path_assessment)
        main_claim_id = f"{problem.problem_id}:main"
        definition_claim_id = f"{problem.problem_id}:definitions"
        lemma_claim_id = f"{problem.problem_id}:lemmas"
        counterexample_claim_id = f"{problem.problem_id}:counterexamples"
        proof_path_claim_id = f"{problem.problem_id}:proof_path"

        claims = [
            ClaimRecord(
                claim_id=definition_claim_id,
                title="Definitions and notation are formalized",
                statement=f"Core definitions required for {problem.title} are implemented in Lean.",
                status="candidate",
                validation_mode="lean",
            ),
            ClaimRecord(
                claim_id=lemma_claim_id,
                title="Known structural lemmas are formalized",
                statement=f"Reusable structural lemmas for {problem.title} are available to downstream proofs.",
                status="candidate",
                validation_mode="lean",
                depends_on=[definition_claim_id],
            ),
            ClaimRecord(
                claim_id=main_claim_id,
                title=problem.title,
                statement=target_statement,
                status="candidate",
                validation_mode="lean",
                depends_on=[definition_claim_id, lemma_claim_id],
            ),
            ClaimRecord(
                claim_id=proof_path_claim_id,
                title="A plausible proof path is documented",
                statement=f"Historical proof ingredients and modern tool choices are documented for {problem.title}.",
                status="candidate",
                validation_mode="manual_review",
            ),
        ]

        tasks = [
            ProofTask(
                task_id="task_01_definition_audit",
                task_type="definition_audit",
                title="Audit exact theorem statement and dependencies",
                description=(
                    "Recover the authoritative theorem statement, list prerequisite definitions, "
                    "and identify whether the current problem is a known theorem formalization, "
                    "an open conjecture, or a bounded search target."
                ),
                success_contract="problem_context.json is complete enough to avoid formalizing the wrong statement.",
                validation_mode="manual_review",
                claim_id=definition_claim_id,
            ),
            ProofTask(
                task_id="task_02_historical_foundations",
                task_type="historical_foundation_audit",
                title="Recover historical proof ingredients and companion theorems",
                description=(
                    "Collect older proofs, reductions, known special cases, and reusable companion theorems before attempting a new result."
                ),
                success_contract="idea/literature_foundations.json records the best historical base currently available.",
                validation_mode="manual_review",
                depends_on=["task_01_definition_audit"],
                claim_id=proof_path_claim_id,
            ),
            ProofTask(
                task_id="task_03_modern_tool_synthesis",
                task_type="modern_tool_synthesis",
                title="Map modern mathematical tools onto the target problem",
                description=(
                    "Identify which modern toolkits, finite certificates, or formal methods might plausibly shorten the route to a proof."
                ),
                success_contract="idea/proof_path_assessment.json lists modern tools, blockers, and a first route hypothesis.",
                validation_mode="manual_review",
                depends_on=["task_02_historical_foundations"],
                claim_id=proof_path_claim_id,
            ),
            ProofTask(
                task_id="task_04_proof_path_design",
                task_type="proof_path_design",
                title="Design a narrow first proof route",
                description=(
                    "Combine the historical base and modern tools into a concrete first proof obligation rather than attacking the full conjecture at once."
                ),
                success_contract="The project has a documented proof-path hypothesis with explicit blockers and near-term milestones.",
                validation_mode="manual_review",
                depends_on=["task_02_historical_foundations", "task_03_modern_tool_synthesis"],
                claim_id=proof_path_claim_id,
            ),
            ProofTask(
                task_id="task_04b_theorem_inventory",
                task_type="theorem_inventory_audit",
                title="Build a literature-backed theorem inventory",
                description=(
                    "Extract reusable theorems, obstructions, positive families, and methods from the current paper base before editing Lean proofs."
                ),
                success_contract="proof/theorem_inventory.json records literature-backed theorem targets with explicit Lean entry points.",
                validation_mode="manual_review",
                depends_on=["task_02_historical_foundations", "task_03_modern_tool_synthesis"],
                claim_id=proof_path_claim_id,
            ),
            ProofTask(
                task_id="task_04c_route_scaffold",
                task_type="proof_route_scaffold",
                title="Commit to one concrete proof-route scaffold",
                description=(
                    "Pick one candidate framework, list its milestones, and define the next formal obligation before any broad code generation."
                ),
                success_contract="proof/proof_route_scaffold.json and proof_gap_notes.md point to a single bounded route rather than an unconstrained theorem search.",
                validation_mode="manual_review",
                depends_on=["task_04_proof_path_design", "task_04b_theorem_inventory"],
                claim_id=proof_path_claim_id,
            ),
            ProofTask(
                task_id="task_04d_theorem_graph",
                task_type="theorem_graph_construction",
                title="Construct a paper-level theorem graph",
                description=(
                    "Turn the current literature base into a dependency graph of candidate theorems, reductions, and obstructions before Lean proof work begins."
                ),
                success_contract="proof/theorem_graph.json records a dependency graph from cited theorems toward the open target.",
                validation_mode="manual_review",
                depends_on=["task_04b_theorem_inventory", "task_04c_route_scaffold"],
                claim_id=proof_path_claim_id,
            ),
            ProofTask(
                task_id="task_04e_route_selection",
                task_type="paper_first_route_selection",
                title="Select a paper-first proof route",
                description=(
                    "Choose one theorem chain in ordinary mathematical language and defer Lean formalization until that chain is explicit and bounded."
                ),
                success_contract="proof/route_candidates.json, proof/mathematical_blockers.json, and proof/selected_route.md describe one bounded route and its blockers.",
                validation_mode="manual_review",
                depends_on=["task_04d_theorem_graph"],
                claim_id=proof_path_claim_id,
            ),
            ProofTask(
                task_id="task_05_definition_formalization",
                task_type="definition_formalization",
                title="Formalize definitions and basic examples",
                description=(
                    "Implement the core objects, notation, and sanity-check lemmas in Lean without using `sorry`."
                ),
                success_contract="The Lean project builds with definitions and at least one verified sanity theorem.",
                validation_mode="lean",
                depends_on=["task_01_definition_audit", "task_04e_route_selection"],
                claim_id=definition_claim_id,
            ),
            ProofTask(
                task_id="task_06_known_results_audit",
                task_type="known_result_formalization",
                title="Map known results into a lemma inventory",
                description=(
                    "Decompose the problem into reusable lemmas, existing literature facts, and any finite-search subclaims."
                ),
                success_contract="claim_registry.json and theorem_inventory.json agree on a main claim and reusable supporting lemmas.",
                validation_mode="manual_review",
                depends_on=["task_02_historical_foundations", "task_04c_route_scaffold"],
                claim_id=lemma_claim_id,
            ),
            ProofTask(
                task_id="task_07_lemma_formalization",
                task_type="lemma_formalization",
                title="Formalize structural lemmas",
                description=(
                    "Convert the highest-value supporting lemmas into Lean theorems that the main claim can consume."
                ),
                success_contract="At least one nontrivial supporting lemma is proven in Lean with no `sorry` placeholders.",
                validation_mode="lean",
                depends_on=["task_05_definition_formalization", "task_06_known_results_audit"],
                claim_id=lemma_claim_id,
            ),
            ProofTask(
                task_id="task_08_main_claim_stub",
                task_type="main_theorem_formalization",
                title="State the main claim in Lean",
                description=(
                    "Create the target theorem or conjecture statement in Lean, with dependencies wired to the supporting lemmas."
                ),
                success_contract="The main claim is stated in Lean and compiles, even if proof work remains.",
                validation_mode="lean",
                depends_on=["task_07_lemma_formalization"],
                claim_id=main_claim_id,
            ),
            ProofTask(
                task_id="task_09_sorry_audit",
                task_type="formal_audit",
                title="Audit unresolved proof gaps",
                description=(
                    "Run `lake build`, collect diagnostics, and reject any result that still depends on `sorry` placeholders."
                ),
                success_contract="artifacts/lean_build_report.json shows either a clean build or a precise blocked status.",
                validation_mode="lean",
                depends_on=["task_08_main_claim_stub"],
                claim_id=main_claim_id,
            ),
        ]

        if any(tag in problem.tags for tag in ("computational_search", "finite_case", "divisors")):
            claims.append(
                ClaimRecord(
                    claim_id=counterexample_claim_id,
                    title="Counterexample search obligations are discharged",
                    statement=(
                        "Finite search or bounded counterexample obligations are either completed or shown to be unnecessary."
                    ),
                    status="candidate",
                    validation_mode="exhaustive_search",
                    depends_on=[definition_claim_id],
                )
            )
            tasks.insert(
                4,
                ProofTask(
                    task_id="task_03b_counterexample_search",
                    task_type="counterexample_search",
                    title="Run bounded counterexample or finite-case search",
                    description=(
                        "Use computation only where it is mathematically justified and record the exact search contract."
                    ),
                    success_contract="Any bounded search range, assumptions, and outputs are written to artifacts.",
                    validation_mode="exhaustive_search",
                    depends_on=["task_04_proof_path_design"],
                    claim_id=counterexample_claim_id,
                ),
            )

        notes = [
            "This is a math track plan. Progress is measured by verified claims, not by generated prose.",
            "No main result should be treated as publishable until Lean verification succeeds without `sorry` placeholders.",
            "The system should audit historical proof ingredients and modern tools before attempting any main theorem formalization.",
        ]
        if problem.formalized in {"partial", "yes"}:
            notes.append("Existing formalization work is indicated by the problem bank; reuse should be audited before adding new code.")
        if proof_path_assessment:
            readiness = str(proof_path_assessment.get("readiness_tier", "")).strip()
            if readiness:
                notes.append(f"Current scouting readiness tier: {readiness}.")
            literature = proof_path_assessment.get("literature", {})
            literature_snapshot_count = int(literature.get("snapshot_count", 0) or 0)
            if literature_snapshot_count:
                notes.append(f"Literature intake captured {literature_snapshot_count} snapshot(s) for this project.")
            recovered_statement = str(literature.get("recovered_statement", "")).strip()
            recovered_statement_source = str(literature.get("recovered_statement_source", "")).strip()
            if recovered_statement:
                notes.append(f"Recovered target statement: {recovered_statement}")
            if recovered_statement_source:
                notes.append(f"Recovered statement source: {recovered_statement_source}")
            for item in literature.get("known_results", [])[:2]:
                notes.append(f"Known-result evidence: {item['statement']}")
            for item in literature.get("proof_ingredients", [])[:2]:
                notes.append(f"Proof-ingredient hint: {item['statement']}")
            for item in literature.get("modern_tools", [])[:2]:
                notes.append(f"Literature tool hint: {item['statement']}")
            local_literature_signal = proof_path_assessment.get("local_literature_signal", {})
            for signal in local_literature_signal.get("evidence_signals", [])[:3]:
                notes.append(f"Local literature signal: {signal}")
            for blocker in proof_path_assessment.get("blockers", [])[:3]:
                notes.append(f"Proof-path blocker: {blocker}")
        if theorem_inventory:
            notes.append(f"Theorem inventory entries: {int(theorem_inventory.get('entry_count', 0))}.")
            for entry in theorem_inventory.get("entries", [])[:2]:
                notes.append(f"Theorem inventory candidate [{entry['role']}]: {entry['statement']}")
        if proof_path_frameworks:
            recommended_id = str(proof_path_frameworks.get("recommended_framework_id", "")).strip()
            if recommended_id:
                notes.append(f"Recommended proof framework: {recommended_id}.")
            for framework in proof_path_frameworks.get("frameworks", [])[:2]:
                notes.append(f"Route scaffold candidate: {framework['title']}")
        if route_candidates:
            selected_route_id = str(route_candidates.get("selected_route_id", "")).strip()
            if selected_route_id:
                notes.append(f"Paper-first selected route: {selected_route_id}.")
            notes.append(f"Paper-first route candidates: {int(route_candidates.get('candidate_count', 0))}.")
        if mathematical_blockers:
            notes.append(f"Mathematical blockers recorded: {int(mathematical_blockers.get('blocker_count', 0))}.")
            for blocker in mathematical_blockers.get("blockers", [])[:2]:
                notes.append(f"Mathematical blocker: {blocker}")

        return ProofPlan(
            project_name=project_name,
            generated_at=utc_now_iso(),
            problem=problem.to_dict(),
            tasks=tasks,
            claims=claims,
            notes=notes,
        )
