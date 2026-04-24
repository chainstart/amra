from __future__ import annotations

import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from ara_math.problem_bank import load_problem_bank
from ara_math.runtime import env_float, env_int, env_str, run_guarded_command, wait_for_system_headroom
from ara_math.workspace import append_jsonl, load_project_manifest, read_json, read_text, utc_now_iso, write_json, write_text


LEAN_DECL_PATTERN = re.compile(
    r"^\s*(theorem|lemma|def)\s+([A-Za-z0-9_'.]+)(?:\s*\([^)]*\))*\s*:\s*(.+?)(?:\s*:=\s*by|\s*:=|\s*where|\s*$)"
)


def _slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or "item"


class ProofSearchRunner:
    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.backend_max_memory_mb = env_int("ARA_MATH_BACKEND_MAX_MEMORY_MB", 6144)
        self.backend_max_cpu_seconds = env_int("ARA_MATH_BACKEND_MAX_CPU_SECONDS", 240)
        self.backend_max_processes = env_int("ARA_MATH_BACKEND_MAX_PROCESSES", 256)
        self.backend_niceness = env_int("ARA_MATH_BACKEND_NICENESS", 10)
        self.backend_model = env_str("ARA_MATH_BACKEND_MODEL", "")
        self.backend_reasoning_effort = env_str("ARA_MATH_BACKEND_REASONING_EFFORT", "medium")
        self.min_available_memory_mb = env_int("ARA_MATH_MIN_AVAILABLE_MEMORY_MB", 2048)
        self.max_load_per_cpu = env_float("ARA_MATH_MAX_LOAD_PER_CPU", 1.5)
        self.wait_max_seconds = env_int("ARA_MATH_SYSTEM_WAIT_SECONDS", 30)
        self.wait_poll_seconds = env_int("ARA_MATH_SYSTEM_WAIT_POLL_SECONDS", 5)

    def _proof_search_root(self, project_dir: Path) -> Path:
        return project_dir / "proof"

    def _attempts_root(self, project_dir: Path) -> Path:
        return self._proof_search_root(project_dir) / "attempts"

    def _status_path(self, project_dir: Path) -> Path:
        return self._proof_search_root(project_dir) / "proof_search_status.json"

    def _existing_attempt_reports(self, project_dir: Path) -> list[tuple[int, dict[str, Any]]]:
        indexed_dirs: list[tuple[int, Path]] = []
        for attempt_dir in self._attempts_root(project_dir).glob("attempt_*"):
            if not attempt_dir.is_dir():
                continue
            suffix = attempt_dir.name.removeprefix("attempt_")
            if not suffix.isdigit():
                continue
            indexed_dirs.append((int(suffix), attempt_dir))

        attempts: list[tuple[int, dict[str, Any]]] = []
        for attempt_index, attempt_dir in sorted(indexed_dirs, key=lambda item: item[0]):
            report_path = attempt_dir / "attempt_report.json"
            if not report_path.exists():
                continue
            attempts.append((attempt_index, read_json(report_path, default={})))
        return attempts

    def _route_discovery_snapshot(self, project_dir: Path) -> dict[str, str]:
        snapshot: dict[str, str] = {}
        for relative_path in (
            "formal/MathProject/Basic.lean",
            "formal/MathProject/GeneratedClaims.lean",
            "formal/MathProject/MainClaim.lean",
        ):
            path = project_dir / relative_path
            if path.exists():
                snapshot[str(path)] = path.read_text(encoding="utf-8")
        return snapshot

    def _restore_route_discovery_snapshot(self, snapshot: dict[str, str]) -> None:
        for raw_path, content in snapshot.items():
            path = Path(raw_path)
            path.write_text(content, encoding="utf-8")

    def _wait_for_headroom(self) -> dict[str, Any]:
        return wait_for_system_headroom(
            min_available_memory_mb=self.min_available_memory_mb,
            max_load_per_cpu=self.max_load_per_cpu,
            max_wait_seconds=self.wait_max_seconds,
            poll_seconds=self.wait_poll_seconds,
        )

    def _find_local_asset_paths(self, project_dir: Path) -> list[Path]:
        proof_path = read_json(project_dir / "idea" / "proof_path_assessment.json", default={})
        candidates: list[Path] = []
        for asset in proof_path.get("local_assets", []):
            raw_path = str(asset.get("path", "")).strip()
            if not raw_path:
                continue
            path = Path(raw_path)
            if path.exists():
                candidates.append(path)
        deduped: list[Path] = []
        seen: set[str] = set()
        for path in candidates:
            key = str(path.resolve())
            if key in seen:
                continue
            seen.add(key)
            deduped.append(path)
        return deduped

    def _scan_lean_inventory(self, asset_paths: list[Path], *, limit: int = 80) -> list[dict[str, Any]]:
        inventory: list[dict[str, Any]] = []
        seen: set[tuple[str, str, str]] = set()
        for asset_path in asset_paths:
            roots = [asset_path] if asset_path.is_dir() else [asset_path.parent]
            for root in roots:
                for lean_file in root.rglob("*.lean"):
                    try:
                        lines = lean_file.read_text(encoding="utf-8", errors="ignore").splitlines()
                    except OSError:
                        continue
                    for index, line in enumerate(lines, start=1):
                        match = LEAN_DECL_PATTERN.match(line)
                        if not match:
                            continue
                        kind, name, statement = match.groups()
                        key = (kind, name, statement)
                        if key in seen:
                            continue
                        seen.add(key)
                        inventory.append(
                            {
                                "kind": kind,
                                "name": name,
                                "statement": statement.strip(),
                                "path": str(lean_file),
                                "line": index,
                                "source_root": str(root),
                            }
                        )
                        if len(inventory) >= limit:
                            return inventory
        return inventory

    def _scan_script_inventory(self, asset_paths: list[Path], *, limit: int = 40) -> list[dict[str, Any]]:
        inventory: list[dict[str, Any]] = []
        seen: set[str] = set()
        for asset_path in asset_paths:
            roots = [asset_path] if asset_path.is_dir() else [asset_path.parent]
            for root in roots:
                for pattern in ("*.py", "*.sh"):
                    for script_path in root.rglob(pattern):
                        if any(token in script_path.parts for token in (".venv", "site-packages", ".lake", "__pycache__")):
                            continue
                        name_lower = script_path.name.lower()
                        if not any(token in name_lower for token in ("search", "compute", "analy", "proof", "bound")):
                            continue
                        key = str(script_path.resolve())
                        if key in seen:
                            continue
                        seen.add(key)
                        try:
                            excerpt = "\n".join(script_path.read_text(encoding="utf-8", errors="ignore").splitlines()[:20])
                        except OSError:
                            excerpt = ""
                        inventory.append(
                            {
                                "path": str(script_path),
                                "name": script_path.name,
                                "source_root": str(root),
                                "excerpt": excerpt,
                            }
                        )
                        if len(inventory) >= limit:
                            return inventory
        return inventory

    def _select_theorem_hints(
        self,
        inventory: list[dict[str, Any]],
        *,
        recovered_statement: str,
        evidence: dict[str, Any],
        limit: int = 8,
    ) -> list[dict[str, Any]]:
        text = " ".join(
            [
                recovered_statement,
                *[str(item.get("statement", "")) for item in evidence.get("known_results", [])],
                *[str(item.get("statement", "")) for item in evidence.get("open_gaps", [])],
                *[str(item.get("statement", "")) for item in evidence.get("proof_ingredients", [])],
            ]
        ).lower()
        scored: list[tuple[int, dict[str, Any]]] = []
        for item in inventory:
            score = 0
            name = str(item.get("name", "")).lower()
            statement = str(item.get("statement", "")).lower()
            for token in ("weird", "triangle", "unitary", "perfect", "finit", "bound", "odd", "impossible", "possible"):
                if token in text and (token in name or token in statement):
                    score += 2
            if any(word in statement for word in ("finite", "bound", "impossible", "¬", "set.finite")):
                score += 1
            if score > 0:
                scored.append((score, item))
        scored.sort(key=lambda entry: (-entry[0], len(str(entry[1].get("statement", "")))))
        return [item for _, item in scored[:limit]]

    def _extract_latest_next_obligation(self, project_dir: Path, *, limit: int = 6) -> list[str]:
        notes = read_text(project_dir / "proof" / "proof_gap_notes.md")
        if not notes.strip():
            return []
        lines = notes.splitlines()
        latest_start: int | None = None
        for index, line in enumerate(lines):
            if line.strip().startswith("## Next Formal Obligation"):
                latest_start = index
        if latest_start is None:
            return []
        obligations: list[str] = []
        for line in lines[latest_start + 1 :]:
            stripped = line.strip()
            if stripped.startswith("## "):
                break
            if stripped.startswith("- "):
                obligations.append(stripped[2:].strip())
                if len(obligations) >= limit:
                    break
        return obligations

    def _build_prompt(
        self,
        *,
        project_dir: Path,
        attempt_index: int,
        focus_mode: str,
        recovered_statement: str,
        proof_path: dict[str, Any],
        literature_evidence: dict[str, Any],
        literature_theorem_inventory: dict[str, Any],
        proof_path_frameworks: dict[str, Any],
        route_scaffold: dict[str, Any],
        route_discovery_brief: dict[str, Any],
        porting_candidates: list[dict[str, Any]],
        theorem_hints: list[dict[str, Any]],
        script_inventory: list[dict[str, Any]],
        previous_attempt: dict[str, Any] | None,
        seed_family: str,
        placeholder_claim_count: int | None,
        convergence_plan: dict[str, Any] | None,
    ) -> str:
        project_root = project_dir.resolve()
        formal_dir = project_dir / "formal"
        latest_next_obligation = self._extract_latest_next_obligation(project_dir)
        current_focus_override = read_text(project_dir / "proof" / "current_focus.md").strip()
        lines = [
            f"You are working on the math research project at {project_root}.",
            f"This is proof-search attempt {attempt_index}.",
            "",
            "Goal:",
            "Improve the project toward a real Lean-verified proof attempt on the current open problem.",
            "For open problems, do not try to magically finish the main theorem in one step.",
            "Instead, prefer one concrete, high-value move: import definitions, restate one known supporting lemma, narrow the claim, or leave a precise proof-gap note with provenance.",
            "",
            f"Focus mode: {focus_mode}",
            "",
            "Rules:",
            f"- Edit only files under {project_root / 'formal'} and {project_root / 'proof'}.",
            "- Do not claim a theorem is solved unless `lake build` passes with no placeholder, `sorry`, `axiom`, or `admit` remaining in project-owned files.",
            "- Prefer narrowing the proof goal, formalizing supporting lemmas, or encoding a bounded-search contract over inventing unsupported proofs.",
            "- Reuse local asset theorems and known proof ingredients when helpful, but keep provenance explicit in project files.",
            "- Avoid spending the whole attempt reading unrelated directories; make one bounded edit path and execute it.",
            "- Do not read more than 4 project files before making the first edit.",
            "",
            "Current target statement:",
            recovered_statement or "(no recovered statement yet)",
            "",
            "Formal seed state:",
            f"- Seed family: {seed_family or 'generic'}",
            f"- Placeholder Lean claims remaining: {placeholder_claim_count if placeholder_claim_count is not None else 'unknown'}",
            "- If only one placeholder remains, edit `formal/MathProject/MainClaim.lean` first unless a stronger porting candidate exists.",
            "",
        ]
        if focus_mode == "route_discovery":
            lines.extend(
                [
                    "Route-discovery discipline:",
                    "- First decide whether a globally plausible proof path exists right now.",
                    "- Prefer updating proof-route files over touching Lean code.",
                    "- Do not spend the attempt on local shell cleanup unless it directly advances a named literature-backed route.",
                    "- If no route survives scrutiny, leave a blocked-route assessment and stop.",
                    "",
                ]
            )
        elif focus_mode == "paper_first":
            lines.extend(
                [
                    "Paper-first discipline:",
                    "- Do not edit Lean files in this attempt; use project notes and route artifacts only.",
                    "- Work in ordinary mathematical language first: theorem dependencies, case splits, and blockers.",
                    "- If a route is not yet mathematically explicit, record the missing theorem bridge rather than refining Lean shells.",
                    "- The only acceptable progress is a narrower theorem chain, a better selected route, or a sharper mathematical blocker report.",
                    "",
                ]
            )
        if convergence_plan:
            lines.extend(
                [
                    "Convergence focus:",
                    f"- Current phase: {convergence_plan.get('phase', 'unknown')}",
                    f"- Verified milestone: {convergence_plan.get('current_milestone', 'unknown')}",
                ]
            )
            for item in convergence_plan.get("next_formal_objectives", [])[:4]:
                lines.append(f"- Next objective: {item}")
            for requirement in convergence_plan.get("external_requirements", [])[:3]:
                lines.append(
                    f"- External requirement: {requirement.get('title', '')} [{requirement.get('status', 'unknown')}]"
                )
            lines.extend(
                [
                    "- If an external paper or theorem is missing, encode the exact dependency in project files rather than inventing its contents.",
                    "",
                ]
            )
        if latest_next_obligation:
            lines.extend(
                [
                    "Latest proof-gap obligation:",
                ]
            )
            for item in latest_next_obligation:
                lines.append(f"- {item}")
            lines.extend(
                [
                    "- Treat this section as the highest-priority bounded target for the current attempt.",
                    "",
                ]
            )
        if current_focus_override:
            lines.extend(
                [
                    "Current explicit focus override:",
                    current_focus_override,
                    "",
                ]
            )
        if seed_family == "prime_plus_two_powers":
            lines.extend(
                [
                    "Default edit path for this seed family:",
                    "- Read `formal/MathProject/MainClaim.lean` and `proof/proof_gap_notes.md` first.",
                    "- Replace any naked placeholder with an explicit intermediate proposition about `ExceptionalOddSet`.",
                    "- Prefer a bounded milestone such as unboundedness, infinitude, or a local-density surrogate over the full open density claim.",
                    "",
                ]
            )
        elif seed_family == "prime_gap_spectrum":
            lines.extend(
                [
                    "Default edit path for this seed family:",
                    "- Read `formal/MathProject/MainClaim.lean` and `formal/MathProject/Basic.lean` first.",
                    "- Keep the seeded definitions intact and narrow the remaining `GapSpectrumTarget` obligation.",
                    "- Prefer one precise subgoal, such as a fixed candidate `C` scaffold or one named asymptotic lemma, over broad discussion.",
                    "",
                ]
            )
        elif seed_family == "ap_free_bounds":
            lines.extend(
                [
                    "Default edit path for this seed family:",
                    "- Read `formal/MathProject/MainClaim.lean`, `formal/MathProject/Basic.lean`, and `proof/proof_gap_notes.md` first.",
                    "- Keep the AP-free definitions stable and replace only the checkpoint theorem or the next quantitative contract.",
                    "- Prefer one fixed-`k` or fixed-`N` theorem import over a vague statement about all `r_k(N)`.",
                    "",
                ]
            )
        elif seed_family == "minimum_overlap":
            lines.extend(
                [
                    "Default edit path for this seed family:",
                    "- Read `formal/MathProject/MainClaim.lean` and `formal/MathProject/Basic.lean` first.",
                    "- Keep the `DifferenceMultiplicity` shell stable and import one explicit bound or base case before touching the optimal-constant statement.",
                    "- Prefer a theorem that improves the current `N = 1` checkpoint to a literature-backed quantitative inequality.",
                    "",
                ]
            )
        lines.extend(
            [
            "Proof-path hypothesis:",
            ]
        )
        for item in proof_path.get("proof_path_hypothesis", [])[:6]:
            lines.append(f"- {item}")
        lines.extend(["", "Literature evidence:"])
        for heading, key in (
            ("Known results", "known_results"),
            ("Proof ingredients", "proof_ingredients"),
            ("Modern tools", "modern_tools"),
            ("Open gaps", "open_gaps"),
        ):
            lines.append(f"{heading}:")
            entries = literature_evidence.get(key, [])
            if entries:
                for item in entries[:4]:
                    lines.append(f"- {item['statement']}  Source: {item['source']}")
            else:
                lines.append("- none")
        lines.extend(["", "Structured theorem inventory:"])
        theorem_entries = literature_theorem_inventory.get("entries", [])
        if theorem_entries:
            for entry in theorem_entries[:6]:
                lines.append(
                    f"- [{entry['role']}] {entry['statement']}  Lean targets: {', '.join(entry.get('lean_targets', []))}"
                )
        else:
            lines.append("- none")
        lines.extend(["", "Proof-path frameworks:"])
        frameworks = proof_path_frameworks.get("frameworks", [])
        if frameworks:
            for framework in frameworks[:3]:
                lines.append(f"- {framework['framework_id']}: {framework['title']}")
                lines.append(f"  Summary: {framework['summary']}")
                for milestone in framework.get("milestones", [])[:3]:
                    lines.append(f"  Milestone: {milestone}")
        else:
            lines.append("- none")
        if route_scaffold:
            lines.extend(
                [
                    "",
                    "Recommended route scaffold:",
                    f"- Framework: {route_scaffold.get('selected_framework_id', '')} / {route_scaffold.get('title', '')}",
                    f"- Summary: {route_scaffold.get('summary', '')}",
                ]
            )
            for item in route_scaffold.get("next_formal_obligations", [])[:4]:
                lines.append(f"- Next formal obligation: {item}")
            for item in route_scaffold.get("first_edit_targets", [])[:3]:
                lines.append(f"- First edit target: {item}")
        if route_discovery_brief:
            lines.extend(
                [
                    "",
                    "Route-discovery brief:",
                    f"- Objective: {route_discovery_brief.get('objective', '')}",
                    f"- Preferred framework: {route_discovery_brief.get('preferred_framework_id', '')} / {route_discovery_brief.get('preferred_framework_title', '')}",
                ]
            )
            for candidate in route_discovery_brief.get("route_candidates", [])[:3]:
                lines.append(f"- Candidate {candidate.get('framework_id', '')}: {candidate.get('title', '')}")
                lines.append(f"  Summary: {candidate.get('summary', '')}")
                for criterion in candidate.get("acceptance_criteria", [])[:3]:
                    lines.append(f"  Acceptance: {criterion}")
                for supporting in candidate.get("supporting_inventory", [])[:2]:
                    lines.append(
                        f"  Supporting theorem: [{supporting.get('role', '')}] {supporting.get('statement', '')}"
                    )
            for item in route_discovery_brief.get("anti_patterns", [])[:4]:
                lines.append(f"- Anti-pattern: {item}")
            for item in route_discovery_brief.get("deliverables", [])[:3]:
                lines.append(f"- Deliverable: {item}")
        lines.extend(["", "Local Lean theorem hints:"])
        if theorem_hints:
            for item in theorem_hints[:8]:
                lines.append(f"- {item['name']}: {item['statement']} ({item['path']}:{item['line']})")
        else:
            lines.append("- none")
        lines.extend(["", "Local script hints:"])
        if script_inventory:
            for item in script_inventory[:6]:
                lines.append(f"- {item['name']} ({item['path']})")
        else:
            lines.append("- none")
        lines.extend(["", "Porting candidates:"])
        if porting_candidates:
            for item in porting_candidates[:4]:
                lines.append(f"- {item['name']}: {item['signature']} ({item['source_path']})")
                if item.get("trust_level"):
                    lines.append(f"  Trust: {item['trust_level']}")
                source_audit = item.get("source_audit") or {}
                counts = source_audit.get("counts") or {}
                if counts and any(int(value) for value in counts.values()):
                    lines.append(
                        "  Source audit: "
                        f"sorry={counts.get('sorry', 0)}, "
                        f"axiom={counts.get('axiom', 0)}, "
                        f"admit={counts.get('admit', 0)}, "
                        f"placeholder={counts.get('placeholder', 0)}"
                    )
                if item.get("import_hint"):
                    lines.append(f"  Import hint: {item['import_hint']}")
                if item.get("recommended_next_step"):
                    lines.append(f"  Next step: {item['recommended_next_step']}")
        else:
            lines.append("- none")
        lines.append("Companion build and source roots discovered from local assets are added to Lean search paths during build verification.")
        if previous_attempt:
            lines.extend(
                [
                    "",
                    "Previous attempt outcome:",
                    f"- Status: {previous_attempt.get('outcome', 'unknown')}",
                    f"- Build status: {previous_attempt.get('build_status', 'not_run')}",
                ]
            )
            for diag in previous_attempt.get("diagnostics", [])[:8]:
                lines.append(f"- Diagnostic: {diag}")
            for blocker in previous_attempt.get("blockers", [])[:6]:
                lines.append(f"- Blocker: {blocker}")
        lines.extend(
            [
                "",
                "Required workflow:",
                "1. Read at most four project files before your first edit, prioritizing `proof/current_focus.md`, `proof/route_discovery_brief.json`, `proof/proof_route_scaffold.json`, and `formal/MathProject/MainClaim.lean`.",
                "2. Commit to one route from `proof/proof_path_frameworks.json` or explicitly reject the current route set before touching broad Lean code.",
                "3. Turn one theorem-inventory entry into either a bounded Lean checkpoint, a route note, or a blocked-route report; do not branch into multiple local micro-lemmas.",
                f"4. If you changed Lean files, run `cd {self.repo_root} && python3 run.py --json build-lean --project {project_root}` to validate the current state.",
                "5. If no route survives, update `proof/proof_gap_notes.md` with a blocked-route assessment and stop rather than polishing local shell code.",
                "6. End with a concise summary of which route you advanced or rejected and what external theorem, paper, or modeling bridge is still required.",
            ]
        )
        if focus_mode == "paper_first":
            lines.extend(
                [
                    "",
                    "Paper-first workflow override:",
                    "1. Read `proof/selected_route.md`, `proof/route_candidates.json`, `proof/mathematical_blockers.json`, and `proof/proof_gap_notes.md` first.",
                    "2. Do not edit any file under `formal/` in this attempt.",
                    "3. Update only proof-route artifacts or proof-gap notes to narrow the mathematical theorem chain.",
                    "4. Treat Lean as deferred until the selected route is explicit enough for one literature theorem to be restated verbatim.",
                ]
            )
        return "\n".join(lines) + "\n"

    def _invoke_backend(
        self,
        *,
        backend: str,
        project_dir: Path,
        prompt_path: Path,
        output_path: Path,
        timeout_sec: int,
    ) -> dict[str, Any]:
        prompt = prompt_path.read_text(encoding="utf-8")
        if backend == "none":
            output_path.write_text("No prover backend selected.\n", encoding="utf-8")
            return {
                "backend": backend,
                "status": "skipped",
                "returncode": 0,
                "elapsed_seconds": 0.0,
                "command": [],
            }

        backend_bin = shutil.which(backend)
        if not backend_bin:
            output_path.write_text(f"Backend `{backend}` is not available.\n", encoding="utf-8")
            return {
                "backend": backend,
                "status": "unavailable",
                "returncode": None,
                "elapsed_seconds": 0.0,
                "command": [],
            }

        if backend == "codex":
            command = [
                backend_bin,
                "exec",
                "-C",
                str(self.repo_root),
                "--full-auto",
            ]
            if self.backend_model:
                command.extend(["-m", self.backend_model])
            if self.backend_reasoning_effort:
                command.extend(["-c", f'model_reasoning_effort="{self.backend_reasoning_effort}"'])
            command.extend(
                [
                "--output-last-message",
                str(output_path),
                prompt,
                ]
            )
        else:
            output_path.write_text(f"Backend `{backend}` is not implemented yet.\n", encoding="utf-8")
            return {
                "backend": backend,
                "status": "unsupported",
                "returncode": None,
                "elapsed_seconds": 0.0,
                "command": [],
            }

        started = time.monotonic()
        try:
            completed = run_guarded_command(
                command,
                cwd=self.repo_root,
                timeout=timeout_sec,
                memory_mb=self.backend_max_memory_mb,
                cpu_seconds=min(self.backend_max_cpu_seconds, max(timeout_sec + 10, timeout_sec)),
                max_processes=self.backend_max_processes,
                niceness=self.backend_niceness,
            )
        except subprocess.TimeoutExpired as exc:
            output_path.write_text((str(exc.stdout or exc.output or "")) + "\n" + (str(exc.stderr or "")), encoding="utf-8")
            return {
                "backend": backend,
                "status": "timeout",
                "returncode": None,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "command": command,
                "resource_policy": {
                    "memory_mb": self.backend_max_memory_mb,
                    "cpu_seconds": min(self.backend_max_cpu_seconds, max(timeout_sec + 10, timeout_sec)),
                    "max_processes": self.backend_max_processes,
                    "niceness": self.backend_niceness,
                    "model": self.backend_model,
                    "reasoning_effort": self.backend_reasoning_effort,
                },
            }
        if not output_path.exists():
            output_path.write_text(
                "\n".join(
                    [
                        f"backend={backend}",
                        f"returncode={completed.returncode}",
                        "",
                        "STDOUT:",
                        completed.stdout,
                        "",
                        "STDERR:",
                        completed.stderr,
                    ]
                ).strip()
                + "\n",
                encoding="utf-8",
            )
        return {
            "backend": backend,
            "status": "completed" if completed.returncode == 0 else "failed",
            "returncode": completed.returncode,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "command": command,
            "stdout_tail": "\n".join(completed.stdout.splitlines()[-20:]),
            "stderr_tail": "\n".join(completed.stderr.splitlines()[-20:]),
            "resource_policy": {
                "memory_mb": self.backend_max_memory_mb,
                "cpu_seconds": min(self.backend_max_cpu_seconds, max(timeout_sec + 10, timeout_sec)),
                "max_processes": self.backend_max_processes,
                "niceness": self.backend_niceness,
                "model": self.backend_model,
                "reasoning_effort": self.backend_reasoning_effort,
            },
        }

    def run_project(
        self,
        *,
        project_dir: Path,
        orchestrator: Any,
        backend: str = "codex",
        max_attempts: int = 3,
        max_runtime_sec: int = 900,
        attempt_timeout_sec: int = 180,
        build_timeout_sec: int = 90,
        focus_mode: str = "default",
    ) -> dict[str, Any]:
        project_dir = project_dir.resolve()
        manifest = load_project_manifest(project_dir)
        attempts_root = self._attempts_root(project_dir)
        attempts_root.mkdir(parents=True, exist_ok=True)

        existing_plan = read_json(project_dir / "proof" / "proof_plan.json", default={})
        existing_registry = read_json(project_dir / "proof" / "claim_registry.json", default={})
        existing_assessment = read_json(project_dir / "idea" / "proof_path_assessment.json", default={})
        existing_literature = read_json(project_dir / "idea" / "literature_evidence.json", default={})
        existing_statement = read_json(project_dir / "idea" / "statement_recovery.json", default={})
        existing_theorem_inventory = read_json(project_dir / "proof" / "theorem_inventory.json", default={})
        existing_frameworks = read_json(project_dir / "proof" / "proof_path_frameworks.json", default={})
        existing_route_scaffold = read_json(project_dir / "proof" / "proof_route_scaffold.json", default={})
        existing_route_discovery_brief = read_json(project_dir / "proof" / "route_discovery_brief.json", default={})
        needs_refresh = not (project_dir / "proof" / "proof_plan.json").exists()
        needs_refresh = needs_refresh or not existing_plan.get("tasks")
        needs_refresh = needs_refresh or not existing_registry.get("claims")
        needs_refresh = needs_refresh or not (project_dir / "idea" / "proof_path_assessment.json").exists()
        needs_refresh = needs_refresh or existing_assessment.get("status") == "not_generated"
        needs_refresh = needs_refresh or not (project_dir / "idea" / "literature_evidence.json").exists()
        needs_refresh = needs_refresh or not any(int(value) for value in existing_literature.get("counts", {}).values())
        needs_refresh = needs_refresh or not (project_dir / "idea" / "statement_recovery.json").exists()
        needs_refresh = needs_refresh or existing_statement.get("status") in {"not_recovered", "placeholder", ""}
        needs_refresh = needs_refresh or not existing_theorem_inventory.get("entries")
        needs_refresh = needs_refresh or not existing_frameworks.get("frameworks")
        needs_refresh = needs_refresh or not existing_route_scaffold.get("selected_framework_id")
        needs_refresh = needs_refresh or not existing_route_discovery_brief.get("route_candidates")
        if needs_refresh:
            orchestrator.plan_project(project_dir)

        recovered_statement = str(read_json(project_dir / "idea" / "statement_recovery.json", default={}).get("statement", "")).strip()
        proof_path = read_json(project_dir / "idea" / "proof_path_assessment.json", default={})
        literature_evidence = read_json(project_dir / "idea" / "literature_evidence.json", default={})
        paper_inventory = read_json(project_dir / "idea" / "paper_inventory.json", default={})
        literature_theorem_inventory = read_json(project_dir / "proof" / "theorem_inventory.json", default={})
        proof_path_frameworks = read_json(project_dir / "proof" / "proof_path_frameworks.json", default={})
        route_scaffold = read_json(project_dir / "proof" / "proof_route_scaffold.json", default={})
        route_discovery_brief = read_json(project_dir / "proof" / "route_discovery_brief.json", default={})
        porting_candidates = read_json(project_dir / "proof" / "porting_candidates.json", default={}).get("candidates", [])
        asset_paths = self._find_local_asset_paths(project_dir)
        existing_formal = read_json(project_dir / "artifacts" / "formal_preparation.json", default={})
        needs_formal_refresh = not (project_dir / "artifacts" / "formal_preparation.json").exists()
        needs_formal_refresh = needs_formal_refresh or not (project_dir / "proof" / "asset_seed_report.json").exists()
        needs_formal_refresh = needs_formal_refresh or bool(recovered_statement) != bool(
            (existing_formal.get("context_audit") or {}).get("has_exact_statement", False)
        )
        needs_formal_refresh = needs_formal_refresh or len(asset_paths) > len(existing_formal.get("seed_asset_paths", []))
        if needs_formal_refresh:
            orchestrator.prepare_formal(project_dir)
            porting_candidates = read_json(project_dir / "proof" / "porting_candidates.json", default={}).get("candidates", [])

        theorem_inventory = self._scan_lean_inventory(asset_paths)
        script_inventory = self._scan_script_inventory(asset_paths)
        theorem_hints = self._select_theorem_hints(
            theorem_inventory,
            recovered_statement=recovered_statement,
            evidence=literature_evidence,
        )
        convergence_plan = orchestrator.plan_convergence(project_dir)
        convergence_external = read_json(project_dir / "artifacts" / "external_requirements.json", default={})
        convergence_prompt_payload = {
            **convergence_plan,
            "external_requirements": convergence_external.get("requirements", []),
        }

        context_payload = {
            "generated_at": utc_now_iso(),
            "project_name": manifest["project_name"],
            "problem_id": manifest["problem"]["problem_id"],
            "recovered_statement": recovered_statement,
            "asset_paths": [str(path) for path in asset_paths],
            "porting_candidate_count": len(porting_candidates),
            "theorem_inventory_count": len(theorem_inventory),
            "script_inventory_count": len(script_inventory),
            "downloaded_paper_count": int(paper_inventory.get("downloaded_pdf_count", 0)),
            "paper_candidate_count": int(paper_inventory.get("candidate_count", 0)),
            "manual_followup_paper_count": int(paper_inventory.get("manual_followup_count", 0)),
            "literature_theorem_inventory_count": int(literature_theorem_inventory.get("entry_count", 0)),
            "proof_framework_count": int(proof_path_frameworks.get("framework_count", 0)),
            "recommended_framework_id": str(route_scaffold.get("selected_framework_id", "")).strip(),
            "focus_mode": focus_mode,
            "route_candidate_count": len(route_discovery_brief.get("route_candidates", [])),
            "theorem_hints": theorem_hints,
            "script_inventory": script_inventory[:10],
            "convergence_phase": convergence_plan.get("phase", ""),
            "convergence_ready_for_long_run": convergence_plan.get("ready_for_long_run", False),
        }
        write_json(project_dir / "proof" / "proof_search_context.json", context_payload)

        started = time.monotonic()
        historical_attempts = self._existing_attempt_reports(project_dir)
        completed_attempts = historical_attempts[-1][0] if historical_attempts else 0
        previous_attempt: dict[str, Any] | None = historical_attempts[-1][1] if historical_attempts else None
        formal_preparation = read_json(project_dir / "artifacts" / "formal_preparation.json", default={})
        seed_family = str(formal_preparation.get("seed_family", "generic")).strip() or "generic"
        placeholder_claim_count_raw = formal_preparation.get("placeholder_claim_count")
        placeholder_claim_count = (
            int(placeholder_claim_count_raw) if isinstance(placeholder_claim_count_raw, (int, float)) else None
        )
        final_report: dict[str, Any] | None = None

        for local_attempt_index in range(1, max_attempts + 1):
            attempt_index = completed_attempts + local_attempt_index
            elapsed = time.monotonic() - started
            if elapsed >= max_runtime_sec:
                final_report = {
                    "generated_at": utc_now_iso(),
                    "project_name": manifest["project_name"],
                    "problem_id": manifest["problem"]["problem_id"],
                    "status": "timeout",
                    "backend": backend,
                    "focus_mode": focus_mode,
                    "attempts_completed": attempt_index - 1,
                    "elapsed_seconds": round(elapsed, 3),
                    "message": "Overall proof-search runtime budget exhausted before the next attempt started.",
                }
                break

            headroom_report = self._wait_for_headroom()
            if headroom_report["status"] != "ready":
                final_report = {
                    "generated_at": utc_now_iso(),
                    "project_name": manifest["project_name"],
                    "problem_id": manifest["problem"]["problem_id"],
                    "status": "deferred",
                    "backend": backend,
                    "focus_mode": focus_mode,
                    "attempts_completed": attempt_index - 1,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "message": "Proof search was deferred because the local system stayed above guarded resource thresholds.",
                    "system_guard": headroom_report,
                }
                break

            attempt_dir = attempts_root / f"attempt_{attempt_index:02d}"
            attempt_dir.mkdir(parents=True, exist_ok=True)
            prompt_path = attempt_dir / "prompt.txt"
            output_path = attempt_dir / "backend_last_message.txt"
            route_snapshot = self._route_discovery_snapshot(project_dir) if focus_mode in {"route_discovery", "paper_first"} else {}
            prompt = self._build_prompt(
                project_dir=project_dir,
                attempt_index=attempt_index,
                focus_mode=focus_mode,
                recovered_statement=recovered_statement,
                proof_path=proof_path,
                literature_evidence=literature_evidence,
                literature_theorem_inventory=literature_theorem_inventory,
                proof_path_frameworks=proof_path_frameworks,
                route_scaffold=route_scaffold,
                route_discovery_brief=route_discovery_brief,
                porting_candidates=porting_candidates,
                theorem_hints=theorem_hints,
                script_inventory=script_inventory,
                previous_attempt=previous_attempt,
                seed_family=seed_family,
                placeholder_claim_count=placeholder_claim_count,
                convergence_plan=convergence_prompt_payload,
            )
            write_text(prompt_path, prompt)
            backend_report = self._invoke_backend(
                backend=backend,
                project_dir=project_dir,
                prompt_path=prompt_path,
                output_path=output_path,
                timeout_sec=min(attempt_timeout_sec, max(1, int(max_runtime_sec - elapsed))),
            )
            if focus_mode == "paper_first" and route_snapshot:
                self._restore_route_discovery_snapshot(route_snapshot)
            build_report = orchestrator.build_lean(project_dir, timeout_sec=build_timeout_sec)
            route_rollback_applied = False
            if focus_mode == "route_discovery" and build_report["status"] != "passed" and route_snapshot:
                self._restore_route_discovery_snapshot(route_snapshot)
                build_report = orchestrator.build_lean(project_dir, timeout_sec=build_timeout_sec)
                route_rollback_applied = True
            manuscript_report = orchestrator.write_manuscript(project_dir)
            review_report = orchestrator.review_project(project_dir)
            convergence_plan = read_json(project_dir / "artifacts" / "convergence_plan.json", default={})
            attempt_payload = {
                "generated_at": utc_now_iso(),
                "attempt_index": attempt_index,
                "backend": backend_report["backend"],
                "backend_status": backend_report["status"],
                "backend_returncode": backend_report.get("returncode"),
                "backend_elapsed_seconds": backend_report.get("elapsed_seconds", 0.0),
                "backend_resource_policy": backend_report.get("resource_policy", {}),
                "prompt_path": str(prompt_path),
                "backend_last_message_path": str(output_path),
                "system_guard": headroom_report,
                "build_status": build_report["status"],
                "manuscript_path": manuscript_report["manuscript_path"],
                "review_status": review_report["status"],
                "diagnostics": build_report.get("diagnostics", []),
                "blockers": review_report.get("blockers", []),
                "warnings": review_report.get("warnings", []),
                "lean_system_guard": build_report.get("system_guard", {}),
                "theorem_hint_count": len(theorem_hints),
                "script_inventory_count": len(script_inventory),
                "literature_theorem_inventory_count": int(literature_theorem_inventory.get("entry_count", 0)),
                "proof_framework_count": int(proof_path_frameworks.get("framework_count", 0)),
                "recommended_framework_id": str(route_scaffold.get("selected_framework_id", "")).strip(),
                "focus_mode": focus_mode,
                "route_discovery_rollback_applied": route_rollback_applied,
                "theorem_hints": theorem_hints[:8],
                "script_inventory": script_inventory[:8],
                "convergence_phase": convergence_plan.get("phase", ""),
                "ready_for_long_run": convergence_plan.get("ready_for_long_run", False),
            }
            attempt_payload["outcome"] = (
                "converged"
                if review_report["status"] == "ready_for_human_review" and build_report["status"] == "passed"
                else "checkpoint"
                if review_report["status"] == "checkpoint_verified" and build_report["status"] == "passed"
                else "stalled"
            )
            write_json(attempt_dir / "attempt_report.json", attempt_payload)
            append_jsonl(project_dir / "proof" / "proof_search_attempts.jsonl", attempt_payload)
            previous_attempt = attempt_payload

            if attempt_payload["outcome"] == "converged":
                final_report = {
                    "generated_at": utc_now_iso(),
                    "project_name": manifest["project_name"],
                    "problem_id": manifest["problem"]["problem_id"],
                    "status": "converged",
                    "backend": backend,
                    "focus_mode": focus_mode,
                    "attempts_completed": attempt_index,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "best_attempt": attempt_payload,
                }
                break

        if final_report is None:
            best_attempt = previous_attempt or {}
            final_status = "checkpoint" if best_attempt.get("outcome") == "checkpoint" else "exhausted"
            final_report = {
                "generated_at": utc_now_iso(),
                "project_name": manifest["project_name"],
                "problem_id": manifest["problem"]["problem_id"],
                "status": final_status,
                "backend": backend,
                "focus_mode": focus_mode,
                "attempts_completed": completed_attempts + max_attempts,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "best_attempt": best_attempt,
                "message": "Proof-search attempts were exhausted without a clean convergence."
                if final_status == "exhausted"
                else "Proof-search stabilized at a verified checkpoint but did not complete the main theorem.",
            }

        write_json(self._status_path(project_dir), final_report)
        return final_report

    def _find_existing_project(self, *, projects_root: Path, problem_id: str) -> Path | None:
        if not projects_root.exists():
            return None
        for candidate in sorted(projects_root.iterdir()):
            manifest_path = candidate / "project_manifest.json"
            if not manifest_path.exists():
                continue
            manifest = read_json(manifest_path, default={})
            manifest_problem_id = str((manifest.get("problem") or {}).get("problem_id", "")).strip()
            if manifest_problem_id == str(problem_id):
                return candidate
        return None

    def _problem_sort_key(self, problem: Any) -> tuple[int, str]:
        problem_id = str(problem.problem_id)
        if problem_id.isdigit():
            return (0, f"{int(problem_id):06d}")
        return (1, problem_id)

    def _light_attempt_supports_backend(
        self,
        *,
        statement_status: str,
        recovered_statement: str,
        proof_path: dict[str, Any],
        literature_evidence: dict[str, Any],
    ) -> bool:
        if statement_status in {"recovered", "updated", "candidate_found_existing_statement_kept"} and recovered_statement:
            return True
        if proof_path.get("readiness_tier") == "promising":
            return True
        counts = literature_evidence.get("counts", {})
        return any(int(counts.get(key, 0)) for key in ("known_results", "proof_ingredients", "modern_tools"))

    def _light_attempt_priority(self, entry: dict[str, Any]) -> int:
        score = 0
        if entry.get("review_status") == "ready_for_human_review":
            score += 10
        elif entry.get("review_status") == "checkpoint_verified":
            score += 7
        elif entry.get("lean_status") == "passed":
            score += 5
        elif entry.get("lean_status") == "needs_attention":
            score += 3
        if entry.get("proof_search_status") == "converged":
            score += 10
        elif entry.get("proof_search_status") == "checkpoint":
            score += 6
        elif entry.get("proof_search_status") == "exhausted":
            score += 1
        if entry.get("readiness_tier") == "promising":
            score += 4
        elif entry.get("readiness_tier") == "exploratory":
            score += 2
        if entry.get("statement_status") in {"recovered", "updated", "candidate_found_existing_statement_kept"}:
            score += 2
        if int(entry.get("theorem_hint_count", 0)) > 0:
            score += 2
        if int(entry.get("local_asset_count", 0)) > 0:
            score += 2
        return score

    def run_campaign(
        self,
        *,
        orchestrator: Any,
        scout_report_path: Path,
        bank_name: str | None = None,
        limit: int = 3,
        backend: str = "codex",
        max_attempts: int = 2,
        max_runtime_sec: int = 600,
        attempt_timeout_sec: int = 180,
        build_timeout_sec: int = 90,
        create_missing: bool = True,
    ) -> dict[str, Any]:
        scout_report = read_json(scout_report_path, default={})
        shortlist = scout_report.get("shortlist_candidates", [])[:limit]
        campaign_entries: list[dict[str, Any]] = []
        for candidate in shortlist:
            headroom_report = self._wait_for_headroom()
            problem_id = str(candidate["problem_id"])
            if headroom_report["status"] != "ready":
                campaign_entries.append(
                    {
                        "problem_id": problem_id,
                        "status": "deferred",
                        "message": "Skipped because the local system stayed above guarded resource thresholds.",
                        "system_guard": headroom_report,
                    }
                )
                continue
            project_dir = self._find_existing_project(projects_root=orchestrator.projects_root, problem_id=problem_id)
            if project_dir is None and create_missing:
                project_name = f"{problem_id}-campaign-{utc_now_iso()[:10].replace('-', '')}"
                project_dir = orchestrator.create_project(problem_id=problem_id, name=project_name)
            if project_dir is None:
                campaign_entries.append(
                    {
                        "problem_id": problem_id,
                        "status": "missing_project",
                        "message": "No existing project was found and automatic creation was disabled.",
                    }
                )
                continue
            result = self.run_project(
                project_dir=project_dir,
                orchestrator=orchestrator,
                backend=backend,
                max_attempts=max_attempts,
                max_runtime_sec=max_runtime_sec,
                attempt_timeout_sec=attempt_timeout_sec,
                build_timeout_sec=build_timeout_sec,
            )
            campaign_entries.append(
                {
                    "problem_id": problem_id,
                    "project_dir": str(project_dir),
                    "status": result["status"],
                    "attempts_completed": result.get("attempts_completed", 0),
                    "system_guard": result.get("system_guard", {}),
                }
            )

        payload = {
            "generated_at": utc_now_iso(),
            "backend": backend,
            "scout_report_path": str(scout_report_path),
            "bank_name": bank_name or "",
            "limit": limit,
            "entries": campaign_entries,
        }
        write_json(self.repo_root / "artifacts" / "open_problem_campaign.json", payload)
        return payload

    def run_light_sweep(
        self,
        *,
        orchestrator: Any,
        bank_path: Path,
        bank_name: str | None = None,
        backend: str = "codex",
        problem_limit: int | None = None,
        start_index: int = 0,
        max_runtime_sec: int = 3600,
        attempt_timeout_sec: int = 45,
        build_timeout_sec: int = 45,
        create_missing: bool = True,
        allow_backend_without_seed: bool = False,
    ) -> dict[str, Any]:
        problems = sorted(
            [problem for problem in load_problem_bank(bank_path) if problem.open_problem],
            key=self._problem_sort_key,
        )
        if start_index:
            problems = problems[start_index:]
        if problem_limit is not None:
            problems = problems[:problem_limit]

        report_path = self.repo_root / "artifacts" / "erdos_light_sweep.json"
        existing_report = read_json(report_path, default={})
        existing_entries = existing_report.get("entries", []) if str(existing_report.get("bank_path", "")) == str(bank_path) else []
        processed_ids = {str(entry.get("problem_id", "")) for entry in existing_entries}
        entries = [entry for entry in existing_entries if str(entry.get("problem_id", ""))]

        started = time.monotonic()
        stop_reason = "completed"

        for offset, problem in enumerate(problems, start=start_index):
            if time.monotonic() - started >= max_runtime_sec:
                stop_reason = "time_budget_exhausted"
                break
            problem_id = str(problem.problem_id)
            if problem_id in processed_ids:
                continue

            headroom_report = self._wait_for_headroom()
            if headroom_report["status"] != "ready":
                entry = {
                    "problem_id": problem_id,
                    "title": problem.title,
                    "project_dir": "",
                    "status": "deferred",
                    "message": "Skipped because the local system stayed above guarded resource thresholds.",
                    "system_guard": headroom_report,
                    "position": offset,
                }
                entries.append(entry)
                processed_ids.add(problem_id)
                write_json(
                    report_path,
                    {
                        "generated_at": utc_now_iso(),
                        "backend": backend,
                        "bank_path": str(bank_path),
                        "bank_name": bank_name or "",
                        "start_index": start_index,
                        "problem_limit": problem_limit,
                        "max_runtime_sec": max_runtime_sec,
                        "attempt_timeout_sec": attempt_timeout_sec,
                        "build_timeout_sec": build_timeout_sec,
                        "entries": entries,
                        "stop_reason": "system_guard_blocked",
                    },
                )
                continue

            project_dir = self._find_existing_project(projects_root=orchestrator.projects_root, problem_id=problem_id)
            if project_dir is None and create_missing:
                project_name = f"erdos-{problem_id}-sweep-{utc_now_iso()[:10].replace('-', '')}"
                project_dir = orchestrator.create_project(problem_id=problem_id, name=project_name)
            if project_dir is None:
                entry = {
                    "problem_id": problem_id,
                    "title": problem.title,
                    "project_dir": "",
                    "status": "missing_project",
                    "message": "No existing project was found and automatic creation was disabled.",
                    "position": offset,
                }
                entries.append(entry)
                processed_ids.add(problem_id)
                continue

            plan_report = orchestrator.plan_project(project_dir)
            statement_recovery = read_json(project_dir / "idea" / "statement_recovery.json", default={})
            proof_path = read_json(project_dir / "idea" / "proof_path_assessment.json", default={})
            literature_evidence = read_json(project_dir / "idea" / "literature_evidence.json", default={})
            recovered_statement = str(statement_recovery.get("statement", "")).strip()
            statement_status = str(statement_recovery.get("status", "")).strip()
            counts = literature_evidence.get("counts", {})
            blank_seed = (
                not recovered_statement
                and not proof_path.get("local_assets", [])
                and not any(int(value) for value in counts.values())
            )
            backend_eligible = allow_backend_without_seed or self._light_attempt_supports_backend(
                statement_status=statement_status,
                recovered_statement=recovered_statement,
                proof_path=proof_path,
                literature_evidence=literature_evidence,
            )

            proof_search_report: dict[str, Any] | None = None
            if blank_seed:
                formal_report = {"placeholder_claim_count": 0, "status": "skipped_blank_seed"}
                build_report = {"status": "skipped_blank_seed"}
                manuscript_report = {"manuscript_path": "", "deliverable_type": "seed_gap"}
                review_report = {"status": "seed_gap"}
                proof_search_report = {
                    "status": "seed_only",
                    "attempts_completed": 0,
                    "best_attempt": {},
                }
            else:
                formal_report = orchestrator.prepare_formal(project_dir)
                build_report = orchestrator.build_lean(project_dir, timeout_sec=build_timeout_sec)

            if not blank_seed and backend_eligible:
                proof_search_report = self.run_project(
                    project_dir=project_dir,
                    orchestrator=orchestrator,
                    backend=backend,
                    max_attempts=1,
                    max_runtime_sec=max(attempt_timeout_sec + build_timeout_sec + 30, attempt_timeout_sec + 15),
                    attempt_timeout_sec=attempt_timeout_sec,
                    build_timeout_sec=build_timeout_sec,
                )
            elif not blank_seed:
                proof_search_report = {
                    "status": "seed_only",
                    "attempts_completed": 0,
                    "best_attempt": {},
                }
            if not blank_seed:
                manuscript_report = orchestrator.write_manuscript(project_dir)
                review_report = orchestrator.review_project(project_dir)
            context_payload = read_json(project_dir / "proof" / "proof_search_context.json", default={})
            theorem_hint_count = len(context_payload.get("theorem_hints", []))
            entry = {
                "problem_id": problem_id,
                "title": problem.title,
                "project_dir": str(project_dir),
                "position": offset,
                "status": proof_search_report["status"],
                "statement_status": statement_status,
                "recovered_statement": recovered_statement,
                "readiness_tier": str(proof_path.get("readiness_tier", "")).strip(),
                "local_asset_count": len(proof_path.get("local_assets", [])),
                "literature_counts": {key: int(value) for key, value in counts.items()},
                "plan_task_count": len(plan_report.get("tasks", [])),
                "formal_placeholder_count": int(formal_report.get("placeholder_claim_count", 0)),
                "lean_status": build_report.get("status", ""),
                "review_status": review_report.get("status", ""),
                "proof_search_status": proof_search_report.get("status", ""),
                "attempts_completed": int(proof_search_report.get("attempts_completed", 0)),
                "theorem_hint_count": theorem_hint_count,
                "deliverable_type": manuscript_report.get("deliverable_type", ""),
                "artifacts": {
                    "proof_path_assessment": str(project_dir / "idea" / "proof_path_assessment.json"),
                    "statement_recovery": str(project_dir / "idea" / "statement_recovery.json"),
                    "literature_evidence": str(project_dir / "idea" / "literature_evidence.json"),
                    "proof_search_status": str(project_dir / "proof" / "proof_search_status.json"),
                    "lean_build_report": str(project_dir / "artifacts" / "lean_build_report.json"),
                    "review_report": str(project_dir / "artifacts" / "review_report.json"),
                },
                "proof_search_mode": "backend" if backend_eligible else "seed_only",
            }
            entry["priority_score"] = self._light_attempt_priority(entry)
            entries.append(entry)
            processed_ids.add(problem_id)
            ranked = sorted(entries, key=lambda item: (-int(item.get("priority_score", 0)), str(item.get("problem_id", ""))))
            write_json(
                report_path,
                {
                    "generated_at": utc_now_iso(),
                    "backend": backend,
                    "bank_path": str(bank_path),
                    "bank_name": bank_name or "",
                    "start_index": start_index,
                    "problem_limit": problem_limit,
                    "max_runtime_sec": max_runtime_sec,
                    "attempt_timeout_sec": attempt_timeout_sec,
                    "build_timeout_sec": build_timeout_sec,
                    "entries": entries,
                    "next_focus_candidates": ranked[:25],
                    "stop_reason": stop_reason,
                },
            )

        ranked = sorted(entries, key=lambda item: (-int(item.get("priority_score", 0)), str(item.get("problem_id", ""))))
        payload = {
            "generated_at": utc_now_iso(),
            "backend": backend,
            "bank_path": str(bank_path),
            "bank_name": bank_name or "",
            "start_index": start_index,
            "problem_limit": problem_limit,
            "max_runtime_sec": max_runtime_sec,
            "attempt_timeout_sec": attempt_timeout_sec,
            "build_timeout_sec": build_timeout_sec,
            "entries": entries,
            "processed_problem_count": len(entries),
            "next_focus_candidates": ranked[:25],
            "stop_reason": stop_reason,
        }
        write_json(report_path, payload)
        return payload
