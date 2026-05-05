from __future__ import annotations

from pathlib import Path
from typing import Any

from ara_math.strategy import OpenProblemStrategyPlanner
from ara_math.context import build_context_audit
from ara_math.workspace import load_project_manifest, read_json, read_text, record_event, update_pipeline_status, utc_now_iso, write_json


class ConvergencePlanner:
    def __init__(self) -> None:
        self.strategy_planner = OpenProblemStrategyPlanner()

    def _has_local_source_match(self, sources: list[str], fragment: str) -> bool:
        lowered = fragment.lower()
        return any(lowered in source.lower() for source in sources)

    def _has_any_local_source_match(self, sources: list[str], fragments: list[str]) -> bool:
        return any(self._has_local_source_match(sources, fragment) for fragment in fragments)

    def _collect_local_documents(self, asset_paths: list[str], *, project_dir: Path, limit: int = 120) -> list[str]:
        documents: list[str] = []
        seen: set[str] = set()
        suffixes = {".pdf", ".djvu", ".ps", ".tex", ".md", ".txt"}
        project_roots = [
            project_dir / "idea" / "papers",
            project_dir / "idea" / "reference_cache",
            project_dir / "idea",
        ]
        for raw_path in asset_paths:
            path = Path(raw_path)
            if not path.exists():
                continue
            primary_roots = [path] if path.is_dir() else [path.parent]
            roots: list[Path] = []
            for root in primary_roots:
                candidates = [
                    root,
                    root / "docs",
                    root / "ref-paper",
                    root / "ref-praper",
                    root.parent / "docs",
                    root.parent / "ref-paper",
                    root.parent / "ref-praper",
                ]
                for candidate in candidates:
                    if candidate.exists() and candidate not in roots:
                        roots.append(candidate)
            for root in roots:
                for candidate in root.rglob("*"):
                    if not candidate.is_file():
                        continue
                    if candidate.suffix.lower() not in suffixes:
                        continue
                    key = str(candidate)
                    if key in seen:
                        continue
                    seen.add(key)
                    documents.append(key)
                    if len(documents) >= limit:
                        return documents
        for root in project_roots:
            if not root.exists():
                continue
            for candidate in root.rglob("*"):
                if not candidate.is_file():
                    continue
                if candidate.suffix.lower() not in suffixes:
                    continue
                key = str(candidate)
                if key in seen:
                    continue
                seen.add(key)
                documents.append(key)
                if len(documents) >= limit:
                    return documents
        return documents

    def _extract_milestone(self, *, seed_family: str, main_claim_text: str, review_status: str) -> str:
        if review_status == "ready_for_human_review":
            return "The Lean workspace has a clean main theorem candidate and is ready for human mathematical audit."
        if "ExceptionalOddSetContainsAllOddNumbersBelowFour" in main_claim_text:
            return "A verified base-case checkpoint shows every odd natural number below four is already in the exceptional set shell."
        if "PositiveLengthIntervalInGapSpectrum" in main_claim_text:
            return "A verified checkpoint reduces Erdős #5 to importing one literature-backed theorem asserting a positive-length interval inside the normalized prime-gap spectrum."
        if "GapSpectrumTarget" in main_claim_text and "proof contract" in main_claim_text.lower():
            return "A verified proof contract isolates the exact future theorem obligation for the prime-gap spectrum target."
        if "claim_634_checkpoint" in main_claim_text:
            return "A verified checkpoint records square-case and shell-level area progress for the triangle-dissection track."
        if "erdos_1052_main_of_goto" in main_claim_text:
            return "The unitary-perfect track has reduced the main theorem to importing or reconstructing Goto's finiteness theorem."
        if seed_family == "ap_free_bounds":
            return "The project has a formal shell for AP-free-set reasoning, but not yet a verified quantitative bound."
        return "The project currently has only preparatory or placeholder-level progress."

    def _default_run_profile(self, *, seed_family: str, review_status: str, build_status: str) -> dict[str, Any]:
        profile = {
            "backend": "codex",
            "attempts": 2,
            "time_budget_sec": 1800,
            "attempt_timeout_sec": 420,
            "build_timeout_sec": 120,
            "reasoning_effort": "high",
            "allow_network": True,
        }
        if seed_family in {"triangle_dissection", "prime_gap_spectrum", "prime_plus_two_powers"}:
            profile["attempts"] = 3
            profile["time_budget_sec"] = 2400
            profile["attempt_timeout_sec"] = 480
        if seed_family == "unitary_perfect":
            profile["time_budget_sec"] = 1500
            profile["attempt_timeout_sec"] = 360
            profile["build_timeout_sec"] = 90
        if seed_family == "ap_free_bounds":
            profile["attempts"] = 2
            profile["time_budget_sec"] = 2100
            profile["attempt_timeout_sec"] = 450
        if review_status == "blocked" and build_status == "blocked":
            profile["attempts"] = 1
            profile["time_budget_sec"] = 600
            profile["attempt_timeout_sec"] = 180
            profile["reasoning_effort"] = "medium"
        return profile

    def _family_specific_actions(
        self,
        *,
        seed_family: str,
        review_status: str,
        build_report: dict[str, Any],
        literature_sources: list[str],
        local_documents: list[str],
        porting_candidates: list[dict[str, Any]],
    ) -> tuple[str, list[str], list[dict[str, Any]], list[str]]:
        phase = "deeper_proof_search"
        objectives: list[str] = []
        external_requirements: list[dict[str, Any]] = []
        notes: list[str] = []

        if seed_family == "unitary_perfect":
            phase = "import_verified_finiteness"
            objectives.extend(
                [
                    "Make a placeholder-free finiteness theorem importable, preferably as a local theorem mirroring Goto's bound pipeline.",
                    "If the companion theorem remains source-only, restage it as a MathProject-owned lemma chain ending in an explicit boundedness theorem.",
                    "Only after the build cache is ready should the backend spend long attempts on theorem import or proof repair.",
                ]
            )
            external_requirements.extend(
                [
                    {
                        "kind": "paper",
                        "title": "Goto (2007), Upper Bounds for Unitary Perfect Numbers and Unitary Harmonic Numbers",
                        "authors": ["Takeshi Goto"],
                        "year": 2007,
                        "venue": "Rocky Mountain Journal of Mathematics 37(5), 1557-1576",
                        "doi": "",
                        "source_url": "https://oeis.org/A006086",
                        "reason": "Needed to justify or reconstruct the exact finiteness theorem currently referenced only through local companion code.",
                        "status": "local_copy_available"
                        if self._has_any_local_source_match(local_documents, ["goto", "upper-bounds-for-unitary-perfect"])
                        else "summary_available_only"
                        if self._has_local_source_match(literature_sources, "goto")
                        else "manual_acquisition_required",
                        "required_for_stage": phase,
                    },
                    {
                        "kind": "paper",
                        "title": "Wall (1975), The Fifth Unitary Perfect Number",
                        "authors": ["Charles R. Wall"],
                        "year": 1975,
                        "venue": "Canadian Mathematical Bulletin 18(1)",
                        "doi": "10.4153/CMB-1975-021-9",
                        "source_url": "https://doi.org/10.4153/CMB-1975-021-9",
                        "reason": "Needed to understand the classical search boundary and avoid redoing already-settled low-range arguments.",
                        "status": "local_copy_available"
                        if self._has_any_local_source_match(local_documents, ["wall", "fifth-unitary-perfect", "the-fifth-unitary-perfect-number"])
                        else "summary_available_only"
                        if self._has_any_local_source_match(literature_sources, ["wall", "fifth unitary perfect"])
                        else "manual_acquisition_required",
                        "required_for_stage": phase,
                    },
                ]
            )
            if build_report.get("status") == "blocked":
                external_requirements.append(
                    {
                        "kind": "lean_cache",
                        "title": "Build-ready Lean cache or placeholder-free companion build for the unitary-perfect assets",
                        "reason": "The verifier is blocked before theorem import can be exercised under guarded mode.",
                        "status": "manual_setup_required",
                        "required_for_stage": "unblock_verifier",
                    }
                )
        elif seed_family == "triangle_dissection":
            phase = "strengthen_geometry_shell"
            objectives.extend(
                [
                    "Strengthen `TriangleDissection n` so placement, exact coverage, and interior-disjointness become part of the shell.",
                    "After the shell is stronger, port exactly one literature-backed theorem such as `seven_impossible` or `perfect_square_possible`.",
                    "Keep `n = 19` as a downstream search/certificate target until the impossibility and positive-family lemmas live in the stronger shell.",
                ]
            )
            external_requirements.append(
                {
                    "kind": "paper",
                    "title": "Tutte (1948), The dissection of equilateral triangles into equilateral triangles",
                    "authors": ["W. T. Tutte"],
                    "year": 1948,
                    "venue": "Mathematical Proceedings of the Cambridge Philosophical Society 44(4), 463-482",
                    "doi": "10.1017/S030500410002449X",
                    "source_url": "https://doi.org/10.1017/S030500410002449X",
                    "reason": "Primary source for the classical nonexistence machinery behind the `n = 7` obstruction and the graph-theoretic encoding of equilateral-triangle dissections.",
                    "status": "local_copy_available"
                    if self._has_any_local_source_match(local_documents, ["tutte", "dissection-of-equilateral-triangles"])
                    else "summary_available_only"
                    if self._has_any_local_source_match(literature_sources, ["tutte", "equilateral triangles"])
                    else "manual_acquisition_required",
                    "required_for_stage": phase,
                }
            )
            external_requirements.append(
                {
                    "kind": "paper",
                    "title": "Beeson (2012), Triangle Tiling II: Nonexistence theorems",
                    "authors": ["Michael Beeson"],
                    "year": 2012,
                    "venue": "arXiv",
                    "doi": "10.48550/arXiv.1206.2230",
                    "source_url": "https://arxiv.org/abs/1206.2230",
                    "reason": "Needed for the `n = 11` nonexistence route and for a modern source spelling out the nonexistence families that the local triangle-dissection notes cite.",
                    "status": "local_copy_available"
                    if self._has_any_local_source_match(local_documents, ["beeson", "triangle-tiling-ii", "1206.2230"])
                    else "summary_available_only"
                    if self._has_any_local_source_match(literature_sources, ["beeson", "triangle tiling ii"])
                    else "manual_acquisition_required",
                    "required_for_stage": phase,
                }
            )
        elif seed_family == "prime_gap_spectrum":
            phase = "import_partial_spectrum_theorem"
            objectives.extend(
                [
                    "Replace the current proof contract by one specific literature-backed partial theorem, such as bounded gaps in `S` or `[0,c] ⊆ S` for some explicit `c > 0`.",
                    "Once a partial theorem is formalized, narrow the main target from the full spectrum conjecture to the imported partial statement.",
                    "Only after a stable partial theorem exists should long backend attempts try to strengthen the asymptotic shell again.",
                ]
            )
            external_requirements.extend(
                [
                    {
                        "kind": "paper",
                        "title": "Pintz (2014), On the distribution of gaps between consecutive primes",
                        "authors": ["János Pintz"],
                        "year": 2014,
                        "venue": "arXiv",
                        "doi": "",
                        "source_url": "https://arxiv.org/abs/1407.2213",
                        "reason": "Current best candidate source for the interval-style statement that some nontrivial interval `[0,c]` belongs to the normalized prime-gap limit set.",
                        "status": "local_copy_available"
                        if self._has_any_local_source_match(local_documents, ["pintz", "distribution-of-gaps-between-consecutive-primes", "1407.2213"])
                        else "summary_available_only"
                        if self._has_any_local_source_match(literature_sources, ["pintz", "distribution of gaps"])
                        else "manual_acquisition_required",
                        "required_for_stage": phase,
                    },
                    {
                        "kind": "paper",
                        "title": "Banks-Freiberg-Maynard (2016), On limit points of the sequence of normalized prime gaps",
                        "authors": ["William D. Banks", "Tristan Freiberg", "James Maynard"],
                        "year": 2016,
                        "venue": "Proceedings of the London Mathematical Society 113(4), 515-539",
                        "doi": "10.1112/plms/pdw036",
                        "source_url": "https://doi.org/10.1112/plms/pdw036",
                        "reason": "Needed to justify the positive-proportion / bounded-gap checkpoint for the normalized prime-gap spectrum before attempting the full Erdős conjecture.",
                        "status": "local_copy_available"
                        if self._has_any_local_source_match(local_documents, ["banks", "freiberg", "maynard", "limit-points-of-the-sequence-of-normalized-prime-gaps", "1404.5094"])
                        else "summary_available_only"
                        if self._has_any_local_source_match(literature_sources, ["banks", "freiberg", "maynard", "normalized prime gaps"])
                        else "manual_acquisition_required",
                        "required_for_stage": phase,
                    },
                ]
            )
        elif seed_family == "prime_plus_two_powers":
            phase = "upgrade_to_density_surrogate"
            objectives.extend(
                [
                    "Upgrade the current base-case checkpoint to an unboundedness, infinitude, or lower-density surrogate for the exceptional set.",
                    "Prefer one explicit arithmetic obstruction family over broad heuristic claims about density.",
                    "After a real infinitude-style lemma exists, revisit whether a stronger density statement is worth formalizing.",
                ]
            )
            external_requirements.append(
                {
                    "kind": "paper",
                    "title": "Pan (2011), On the integers not of the form p+2^a+2^b",
                    "authors": ["Hao Pan"],
                    "year": 2011,
                    "venue": "Acta Arithmetica 148(1), 55-61",
                    "doi": "10.4064/aa148-1-4",
                    "source_url": "https://eudml.org/doc/279148",
                    "reason": "Needed to replace the tiny local checkpoint by a literature-backed large-set surrogate (`\\gg_\\epsilon N^{1-\\epsilon}` many exceptions).",
                    "status": "local_copy_available"
                    if self._has_any_local_source_match(local_documents, ["pan", "p-2-a-2-b", "0905.3809"])
                    else "summary_available_only"
                    if self._has_any_local_source_match(literature_sources, ["hao pan", "p+2^a+2^b", "p+2^a+2^b"])
                    else "manual_acquisition_required",
                    "required_for_stage": phase,
                }
            )
            external_requirements.append(
                {
                    "kind": "paper",
                    "title": "Crocker (1971), On the sum of a prime and of two powers of two",
                    "authors": ["Roger Crocker"],
                    "year": 1971,
                    "venue": "Pacific Journal of Mathematics 36(1), 103-107",
                    "doi": "10.2140/pjm.1971.36.103",
                    "source_url": "https://doi.org/10.2140/pjm.1971.36.103",
                    "reason": "Needed for the first infinitude-style obstruction theorem showing infinitely many odd integers avoid the form `p + 2^k + 2^l`.",
                    "status": "local_copy_available"
                    if self._has_any_local_source_match(local_documents, ["crocker", "sum-of-a-prime-and-of-two-powers-of-two"])
                    else "summary_available_only"
                    if self._has_any_local_source_match(literature_sources, ["crocker", "two powers of two"])
                    else "manual_acquisition_required",
                    "required_for_stage": phase,
                }
            )
        elif seed_family == "minimum_overlap":
            phase = "import_quantitative_overlap_bound"
            objectives.extend(
                [
                    "Replace the tiny `N = 1` overlap checkpoint by one literature-backed quantitative lower or upper bound for the asymptotic constant.",
                    "Only after a concrete bound is imported should the backend spend long attempts on the optimal-constant statement itself.",
                    "Keep the formal shell centered on `DifferenceMultiplicity` and `BalancedPartition` until the exact asymptotic theorem is grounded.",
                ]
            )
            external_requirements.extend(
                [
                    {
                        "kind": "paper",
                        "title": "White (2023), A new bound for Erdős' minimum overlap problem",
                        "authors": ["Ethan Patrick White"],
                        "year": 2023,
                        "venue": "Acta Arithmetica 208, 235-255",
                        "doi": "10.4064/aa220728-7-6",
                        "source_url": "https://www.impan.pl/get/doi/10.4064/aa220728-7-6",
                        "reason": "Needed to import the strongest published lower bound for the overlap constant into Lean.",
                        "status": "local_copy_available"
                        if self._has_any_local_source_match(local_documents, ["white", "minimum-overlap", "aa220728-7-6"])
                        else "summary_available_only"
                        if self._has_any_local_source_match(literature_sources, ["minimum overlap", "ethan patrick white"])
                        else "manual_acquisition_required",
                        "required_for_stage": phase,
                    },
                    {
                        "kind": "paper",
                        "title": "Haugland (2016), The minimum overlap problem revisited",
                        "authors": ["Jan Kristian Haugland"],
                        "year": 2016,
                        "venue": "arXiv",
                        "doi": "10.48550/arXiv.1609.08000",
                        "source_url": "https://arxiv.org/abs/1609.08000",
                        "reason": "Needed to bracket the target constant with a concrete upper-bound source close to the current best published values.",
                        "status": "local_copy_available"
                        if self._has_any_local_source_match(local_documents, ["haugland", "minimum-overlap-problem-revisited", "1609.08000"])
                        else "summary_available_only"
                        if self._has_any_local_source_match(literature_sources, ["haugland", "minimum overlap problem revisited"])
                        else "manual_acquisition_required",
                        "required_for_stage": phase,
                    },
                ]
            )
        elif seed_family == "ap_free_bounds":
            phase = "fix_quantitative_target"
            objectives.extend(
                [
                    "Choose an explicit fixed-`k` quantitative target before spending long proof-search budget on the full Erdős statement.",
                    "Formalize one AP-free combinatorics shell around `ThreeTermAPFree` or a fixed-`k` progression-free predicate.",
                    "Import exactly one modern quantitative bound or finite witness theorem before retrying the main target.",
                ]
            )
            external_requirements.extend(
                [
                    {
                        "kind": "paper",
                        "title": "Kelley-Meka bound for 3-term progression-free sets or a comparable modern bound paper",
                        "reason": "Needed to anchor the first nontrivial imported theorem for Erdős #3.",
                        "status": "manual_acquisition_required",
                        "required_for_stage": phase,
                    },
                    {
                        "kind": "paper",
                        "title": "Leng-Sah-Sawhney general-`k` bound paper or equivalent modern source",
                        "reason": "Needed if the project escalates from a fixed-`k` checkpoint to the broader `r_k(N)` target.",
                        "status": "manual_acquisition_required",
                        "required_for_stage": phase,
                    },
                ]
            )
        else:
            notes.append("No family-specific convergence recipe is available yet; the project still needs manual scoping.")

        if review_status == "checkpoint_verified":
            notes.append("The current best state is a verified checkpoint, not a solved main theorem.")
        for candidate in porting_candidates:
            if candidate.get("usable_for_main_claim"):
                notes.append(f"Usable porting candidate detected: {candidate['name']}.")
                break
        return phase, objectives, external_requirements, notes

    def plan(self, project_dir: Path) -> dict[str, Any]:
        manifest = load_project_manifest(project_dir)
        context_audit = build_context_audit(project_dir)
        review_report = read_json(project_dir / "artifacts" / "review_report.json", default={})
        build_report = read_json(project_dir / "artifacts" / "lean_build_report.json", default={})
        formal_preparation = read_json(project_dir / "artifacts" / "formal_preparation.json", default={})
        literature_evidence = read_json(project_dir / "idea" / "literature_evidence.json", default={})
        proof_path = read_json(project_dir / "idea" / "proof_path_assessment.json", default={})
        theorem_inventory = read_json(project_dir / "proof" / "theorem_inventory.json", default={})
        route_discovery_brief = read_json(project_dir / "proof" / "route_discovery_brief.json", default={})
        checkpoint_contract = read_json(project_dir / "proof" / "checkpoint_contract.json", default={})
        proof_system_benchmark = read_json(project_dir / "proof" / "proof_system_benchmark.json", default={})
        proof_search_agenda = read_json(project_dir / "proof" / "proof_search_agenda.json", default={})
        verifier_feedback = read_json(project_dir / "proof" / "verifier_feedback.json", default={})
        porting_candidates = read_json(project_dir / "proof" / "porting_candidates.json", default={}).get("candidates", [])
        proof_gap_notes = read_text(project_dir / "proof" / "proof_gap_notes.md")
        main_claim_text = read_text(project_dir / "formal" / "MathProject" / "MainClaim.lean")

        seed_family = str(formal_preparation.get("seed_family", "generic")).strip() or "generic"
        review_status = str(review_report.get("status", "not_run")).strip() or "not_run"
        build_status = str(build_report.get("status", "not_run")).strip() or "not_run"
        literature_sources = [str(item.get("source", "")).strip() for key in ("known_results", "proof_ingredients", "modern_tools", "open_gaps") for item in literature_evidence.get(key, [])]
        local_asset_paths = [
            str(item.get("path", "")).strip()
            for item in proof_path.get("local_assets", [])
            if str(item.get("path", "")).strip()
        ]
        local_documents = self._collect_local_documents(local_asset_paths, project_dir=project_dir)

        phase = "statement_recovery_required"
        objectives: list[str] = []
        external_requirements: list[dict[str, Any]] = []
        notes: list[str] = []
        blockers: list[str] = []

        if not context_audit["has_exact_statement"] and not context_audit.get("has_recovered_statement", False):
            blockers.append("No exact statement or recovered statement is available yet.")
            objectives.append("Recover and confirm the exact mathematical statement before spending long proof-search budget.")
        else:
            phase, objectives, external_requirements, notes = self._family_specific_actions(
                seed_family=seed_family,
                review_status=review_status,
                build_report=build_report,
                literature_sources=literature_sources,
                local_documents=local_documents,
                porting_candidates=porting_candidates,
            )

        if build_status == "blocked":
            phase = "unblock_verifier"
            blockers.extend(build_report.get("diagnostics", [])[:3])
        elif review_status == "ready_for_human_review":
            phase = "human_audit"
        elif review_status == "checkpoint_verified" and phase == "statement_recovery_required":
            phase = "checkpoint_extension"

        if not objectives:
            objectives.append("No convergence objective has been synthesized yet; inspect proof-gap notes manually.")

        if review_status == "blocked" and review_report.get("blockers"):
            blockers.extend(str(item) for item in review_report.get("blockers", [])[:3])
        if bool(manifest.get("problem", {}).get("open_problem", False)) and not checkpoint_contract.get("checkpoint_statement"):
            blockers.append("No explicit checkpoint contract has been synthesized for this open problem yet.")

        strategy_report = self.strategy_planner.analyze(
            project_dir=project_dir,
            manifest=manifest,
            context_audit=context_audit,
            review_report=review_report,
            build_report=build_report,
            proof_path=proof_path,
            literature_evidence=literature_evidence,
            theorem_inventory=theorem_inventory,
            route_discovery_brief=route_discovery_brief,
        )
        notes.append(f"Strategy profile: {strategy_report['strategy_profile_id']}.")
        notes.extend(f"Strategy lesson: {item}" for item in strategy_report.get("highlighted_lessons", [])[:2])
        if proof_system_benchmark:
            execution_policy = proof_system_benchmark.get("execution_policy", {})
            notes.append(f"Proof-system policy: {execution_policy.get('search_policy', '')}.")
        if proof_search_agenda:
            notes.append(
                f"Agenda mode: {proof_search_agenda.get('execution_mode', '')} on {proof_search_agenda.get('selected_item_id', '')}."
            )
        if verifier_feedback.get("attempt_count", 0):
            notes.append(f"Verifier feedback tracks {verifier_feedback.get('attempt_count', 0)} past attempt(s).")

        current_milestone = self._extract_milestone(
            seed_family=seed_family,
            main_claim_text=main_claim_text,
            review_status=review_status,
        )
        stop_conditions = [
            "Stop the backend loop once the project reaches `ready_for_human_review` with no placeholder, `sorry`, `axiom`, or `admit` in project-owned Lean files.",
            "Stop and mark the project for manual acquisition if a key external theorem or paper is still missing after the current convergence phase.",
            "If the time budget is exhausted without a stronger checkpoint, preserve the best verified milestone and move to the next problem.",
        ]

        if "proof contract" in main_claim_text.lower():
            stop_conditions.append("Do not treat a pure proof contract as a solved theorem; it is only a checkpoint.")
        if "checkpoint" in proof_gap_notes.lower():
            notes.append("Proof-gap notes already record checkpoint-level progress for this project.")

        run_profile = self._default_run_profile(seed_family=seed_family, review_status=review_status, build_status=build_status)
        run_profile["focus_mode"] = str(strategy_report.get("recommended_focus_mode", "default")).strip() or "default"
        run_profile["search_policy"] = str((proof_system_benchmark.get("execution_policy") or {}).get("search_policy", "best_first_frontier"))
        run_profile["execution_mode"] = str(proof_search_agenda.get("execution_mode", ""))
        if phase == "statement_recovery_required":
            run_profile = {
                "backend": "none",
                "attempts": 0,
                "time_budget_sec": 0,
                "attempt_timeout_sec": 0,
                "build_timeout_sec": 0,
                "reasoning_effort": "medium",
                "allow_network": True,
                "focus_mode": "paper_first",
            }
        elif phase == "unblock_verifier":
            run_profile["attempts"] = 1
            run_profile["time_budget_sec"] = min(run_profile["time_budget_sec"], 600)
            run_profile["attempt_timeout_sec"] = min(run_profile["attempt_timeout_sec"], 180)

        readiness_for_long_run = (
            phase not in {"statement_recovery_required", "human_audit"}
            and build_status != "blocked"
            and (not bool(manifest.get("problem", {}).get("open_problem", False)) or bool(proof_system_benchmark))
            and bool((strategy_report.get("gates") or {}).get("route_ready", True))
            and (not bool(manifest.get("problem", {}).get("open_problem", False)) or bool(checkpoint_contract.get("checkpoint_statement")))
            and not any(req.get("status") == "manual_setup_required" for req in external_requirements)
        )

        payload = {
            "generated_at": utc_now_iso(),
            "project_name": manifest["project_name"],
            "problem_id": manifest["problem"]["problem_id"],
            "seed_family": seed_family,
            "review_status": review_status,
            "build_status": build_status,
            "phase": phase,
            "current_milestone": current_milestone,
            "next_formal_objectives": objectives,
            "blockers": blockers,
            "notes": notes,
            "ready_for_long_run": readiness_for_long_run,
            "recommended_run_profile": run_profile,
            "strategy_profile_id": strategy_report["strategy_profile_id"],
            "recommended_focus_mode": strategy_report["recommended_focus_mode"],
            "stop_conditions": stop_conditions,
            "external_requirement_count": len(external_requirements),
        }
        external_payload = {
            "generated_at": utc_now_iso(),
            "project_name": manifest["project_name"],
            "problem_id": manifest["problem"]["problem_id"],
            "phase": phase,
            "requirements": external_requirements,
        }
        write_json(project_dir / "artifacts" / "convergence_plan.json", payload)
        write_json(project_dir / "artifacts" / "external_requirements.json", external_payload)
        write_json(project_dir / "artifacts" / "open_problem_strategy.json", strategy_report)
        update_pipeline_status(
            project_dir,
            stage="convergence",
            status=phase,
            details={
                "ready_for_long_run": readiness_for_long_run,
                "external_requirement_count": len(external_requirements),
                "strategy_profile_id": strategy_report["strategy_profile_id"],
            },
        )
        record_event(
            project_dir,
            stage="convergence",
            event="convergence_plan_updated",
            details={
                "phase": phase,
                "ready_for_long_run": readiness_for_long_run,
                "external_requirement_count": len(external_requirements),
                "strategy_profile_id": strategy_report["strategy_profile_id"],
            },
        )
        return payload
