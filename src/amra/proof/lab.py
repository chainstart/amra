from __future__ import annotations

import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from amra.infra.runtime import env_int, env_str, run_guarded_command, wait_for_system_headroom
from amra.core.workspace import read_text, slugify, utc_now_iso, write_json, write_text


CLEAN_ATTEMPT_LABELS: tuple[str, ...] = (
    "Route title",
    "Claim status",
    "Key lemma",
    "Dependency graph",
    "Proof sketch",
    "Dependencies",
    "Failure mode",
    "Formalization target",
    "Self-audit",
)

AUDIT_LABELS: tuple[str, ...] = (
    "Audit status",
    "First fatal gap",
    "Needed repair",
    "Formalization consequence",
    "Recommendation",
)

GROUNDING_LABELS: tuple[str, ...] = (
    "Statement convention",
    "Existing formal assets",
    "Known results",
    "Do not redo",
    "Open continuation target",
    "Lean entry points",
    "Source gaps",
    "Recommended attack target",
)

PROOF_LAB_DOCTRINE: tuple[str, ...] = (
    "Run multiple independent clean-room attempts before showing attempts to one another.",
    "When source-first mode is enabled, extract and obey existing papers, comments, and Lean assets before attempting new proof work.",
    "Do not start with Lean repair. First identify the exact theorem, route, key lemma, and dependency graph.",
    "Treat local lemmas as valuable only when they remove or sharpen a blocker on the main theorem route.",
    "Cluster attempts by key lemma or proof route before spending more tokens on a branch.",
    "Use an adversarial audit pass on promising routes before claiming progress.",
    "Convert a route to formalization only after its dependencies are precise enough to become Lean statements or executable certificates.",
    "If a branch stalls, produce a freeze package naming the missing theorem, certificate, source, or counterexample search.",
)

STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "lemma",
    "of",
    "on",
    "or",
    "prove",
    "proof",
    "reduce",
    "reduction",
    "route",
    "show",
    "the",
    "to",
    "using",
    "via",
    "with",
}

STATUS_PRIORITY = {
    "closed_candidate": 0,
    "proof_candidate": 0,
    "formalization_only": 1,
    "known_result_needed": 2,
    "external_theorem_needed": 2,
    "partial": 3,
    "statement_gap": 4,
    "counterexample_suspected": 5,
    "fatal_gap": 6,
    "failed": 7,
    "unknown": 8,
}


def _label_key(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", label.strip().lower()).strip("_")


def parse_labeled_fields(text: str, labels: tuple[str, ...] = CLEAN_ATTEMPT_LABELS) -> dict[str, str]:
    """Parse a Markdown-ish labeled report into stable snake_case fields."""

    if not labels:
        return {}
    label_pattern = "|".join(re.escape(label) for label in labels)
    pattern = re.compile(rf"(?im)^\s*(?:[-*]\s*)?({label_pattern})\s*:\s*(.*)$")
    matches = list(pattern.finditer(text))
    parsed: dict[str, str] = {}
    for index, match in enumerate(matches):
        label = _label_key(match.group(1))
        inline_value = match.group(2).strip()
        body_start = match.end()
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body_value = text[body_start:body_end].strip()
        if inline_value and body_value:
            value = f"{inline_value}\n{body_value}".strip()
        else:
            value = inline_value or body_value
        parsed[label] = value.strip()
    return parsed


def _first_line(value: str) -> str:
    for line in value.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _normalize_choice_fields(fields: dict[str, str], keys: tuple[str, ...]) -> dict[str, str]:
    normalized = dict(fields)
    for key in keys:
        if key in normalized:
            normalized[key] = _first_line(normalized[key])
    return normalized


def _normalize_status(value: str) -> str:
    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    normalized = re.sub(r"[^a-z0-9_]+", "", normalized)
    aliases = {
        "closed": "closed_candidate",
        "complete": "closed_candidate",
        "solved": "closed_candidate",
        "candidate": "proof_candidate",
        "proofcandidate": "proof_candidate",
        "external_needed": "external_theorem_needed",
        "known_theorem": "known_result_needed",
        "gap": "fatal_gap",
        "no_route": "failed",
    }
    normalized = aliases.get(normalized, normalized)
    return normalized if normalized in STATUS_PRIORITY else "unknown"


def route_signature(fields: dict[str, str]) -> str:
    seed = fields.get("key_lemma") or fields.get("route_title") or fields.get("formalization_target") or ""
    tokens = [
        token
        for token in re.findall(r"[a-z0-9]+", seed.lower())
        if token not in STOPWORDS and len(token) > 1
    ]
    if not tokens:
        return "unclassified"
    return "-".join(tokens[:10])


def cluster_route_attempts(attempts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    clusters_by_signature: dict[str, dict[str, Any]] = {}
    for attempt in attempts:
        parsed = dict(attempt.get("parsed_fields") or {})
        signature = str(attempt.get("route_signature") or route_signature(parsed))
        cluster = clusters_by_signature.setdefault(
            signature,
            {
                "signature": signature,
                "attempt_numbers": [],
                "count": 0,
                "best_status": "unknown",
                "representative_attempt": None,
                "key_lemma": parsed.get("key_lemma", ""),
                "route_title": parsed.get("route_title", ""),
            },
        )
        cluster["attempt_numbers"].append(attempt.get("attempt"))
        cluster["count"] += 1
        status = _normalize_status(str(parsed.get("claim_status", "")))
        if STATUS_PRIORITY.get(status, 99) < STATUS_PRIORITY.get(str(cluster["best_status"]), 99):
            cluster["best_status"] = status
            cluster["representative_attempt"] = attempt.get("attempt")
            cluster["key_lemma"] = parsed.get("key_lemma", cluster.get("key_lemma", ""))
            cluster["route_title"] = parsed.get("route_title", cluster.get("route_title", ""))
        elif cluster["representative_attempt"] is None:
            cluster["representative_attempt"] = attempt.get("attempt")

    return sorted(
        clusters_by_signature.values(),
        key=lambda item: (
            -int(item["count"]),
            STATUS_PRIORITY.get(str(item["best_status"]), 99),
            str(item["signature"]),
        ),
    )


class AIProofLabRunner:
    """Experimental AI proof module inspired by successful clean-room proof attempts.

    The runner is intentionally outside the normal ARA project workflow. It
    writes standalone artifacts under artifacts/proof_lab and never mutates a
    project workspace or Lean files.
    """

    def __init__(self, *, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.backend_max_memory_mb = env_int("ARA_PROOF_LAB_BACKEND_MAX_MEMORY_MB", 6144)
        self.backend_max_cpu_seconds = env_int("ARA_PROOF_LAB_BACKEND_MAX_CPU_SECONDS", 900)
        self.backend_max_processes = env_int("ARA_PROOF_LAB_BACKEND_MAX_PROCESSES", 4096)
        self.backend_niceness = env_int("ARA_PROOF_LAB_BACKEND_NICENESS", 10)
        self.backend_model = env_str("ARA_PROOF_LAB_MODEL", env_str("ARA_MATH_BACKEND_MODEL", ""))
        self.backend_reasoning_effort = env_str(
            "ARA_PROOF_LAB_REASONING_EFFORT",
            env_str("ARA_MATH_BACKEND_REASONING_EFFORT", "high"),
        )
        self.min_available_memory_mb = env_int("ARA_MATH_MIN_AVAILABLE_MEMORY_MB", 2048)
        self.wait_max_seconds = env_int("ARA_MATH_SYSTEM_WAIT_SECONDS", 30)
        self.wait_poll_seconds = env_int("ARA_MATH_SYSTEM_WAIT_POLL_SECONDS", 5)

    def _new_run_dir(self, *, output_root: Path, run_name: str | None) -> Path:
        base = slugify(run_name or f"proof-lab-{utc_now_iso()}")
        output_root.mkdir(parents=True, exist_ok=True)
        candidate = output_root / base
        if not candidate.exists():
            return candidate
        suffix = 2
        while True:
            candidate = output_root / f"{base}-{suffix}"
            if not candidate.exists():
                return candidate
            suffix += 1

    def _read_context_bundle(self, context_paths: list[Path], *, max_chars_each: int = 16000) -> str:
        if not context_paths:
            return "No external context files supplied.\n"
        chunks: list[str] = []
        for path in context_paths:
            resolved = path.expanduser().resolve()
            text = read_text(resolved)
            truncated = len(text) > max_chars_each
            if truncated:
                text = text[:max_chars_each] + "\n\n[truncated]\n"
            chunks.extend(
                [
                    f"## Context File: {resolved}",
                    "",
                    f"- Exists: {resolved.exists()}",
                    f"- Truncated: {truncated}",
                    "",
                    "```text",
                    text.strip() or "<empty>",
                    "```",
                    "",
                ]
            )
        return "\n".join(chunks).rstrip() + "\n"

    def _build_clean_attempt_prompt(
        self,
        *,
        statement: str,
        context_bundle_path: Path,
        grounding_path: Path | None,
        attempt: int,
        attempts: int,
    ) -> str:
        doctrine = [f"- {item}" for item in PROOF_LAB_DOCTRINE]
        grounding_lines: list[str] = []
        if grounding_path is not None:
            grounding_lines = [
                "",
                "Mandatory source-grounding artifact:",
                f"- {grounding_path}",
                "",
                "You must read the source-grounding artifact before proposing a route.",
                "Do not redo existing formal assets or already solved subresults unless the task is explicitly to formalize them.",
                "Target the listed open continuation target unless you explicitly find it mathematically impossible or mis-specified.",
            ]
        return "\n".join(
            [
                "You are running a clean-room mathematical proof attempt for ARA Proof Lab.",
                "",
                "Hard constraints:",
                "- Do not edit files.",
                "- Do not optimize the repository or workflow.",
                "- Treat the problem as a normal theorem candidate; do not assume it is open, solved, or impossible.",
                "- This is an independent attempt. Do not rely on other attempts unless context explicitly contains them.",
                "- Prefer one precise route over many vague ideas.",
                "- Do not claim a proof unless every dependency is named and checkable.",
                "- If a dependency is external, state whether it is a standard theorem, a source/provenance gap, a computation, or a new lemma.",
                "",
                "Proof-lab doctrine:",
                *doctrine,
                "",
                f"Attempt: {attempt} of {attempts}",
                "",
                "Problem statement:",
                "",
                "```text",
                statement.strip(),
                "```",
                "",
                "Additional context is available here:",
                f"- {context_bundle_path}",
                *grounding_lines,
                "",
                "Task:",
                "1. Find the strongest plausible proof route.",
                "2. Identify the key lemma that would close or materially reduce the main theorem.",
                "3. Give the actual proof attempt, not just a plan.",
                "4. Audit your own route globally: does it move the main theorem, or only a local subproblem?",
                "5. State the Lean/formalization target only if the route is precise enough.",
                "",
                "Output exactly these labeled fields first, then optional supporting details:",
                "Route title: <short name>",
                "Claim status: <closed_candidate|proof_candidate|partial|known_result_needed|external_theorem_needed|statement_gap|counterexample_suspected|fatal_gap|failed>",
                "Key lemma: <the one lemma or theorem the route pivots on>",
                "Dependency graph: <main theorem -> dependencies -> evidence/formalization nodes>",
                "Proof sketch: <best rigorous proof attempt>",
                "Dependencies: <standard theorem / new lemma / computation / source / Lean gap>",
                "Failure mode: <empty if closed_candidate, otherwise exact first missing step>",
                "Formalization target: <Lean theorem or certificate target if applicable>",
                "Self-audit: <why this route should continue, switch, or freeze>",
            ]
        ).strip() + "\n"

    def _build_source_grounding_prompt(self, *, statement: str, context_bundle_path: Path) -> str:
        return "\n".join(
            [
                "You are running the source-first grounding stage for ARA Proof Lab.",
                "",
                "Hard constraints:",
                "- Do not edit files.",
                "- Do not attempt a new proof yet.",
                "- Treat supplied papers, issue/forum comments, and Lean files as primary assets.",
                "- Separate proved Lean facts from informal comments, conjectures, and source gaps.",
                "- Identify what the next proof attempts must not redo.",
                "- If source context is insufficient, say exactly which source or theorem statement is missing.",
                "",
                "Problem statement or working target:",
                "",
                "```text",
                statement.strip(),
                "```",
                "",
                "Source/context bundle to read:",
                f"- {context_bundle_path}",
                "",
                "Output exactly these labeled fields first, then optional notes:",
                "Statement convention: <witness domains, positivity, distinctness, boundary conventions, or missing source requirement>",
                "Existing formal assets: <Lean files/theorems/certificates already available>",
                "Known results: <mathematical results already established by sources>",
                "Do not redo: <subresults that proof attempts should not rediscover>",
                "Open continuation target: <the exact unsolved node to attack next>",
                "Lean entry points: <declarations/files/definitions to reuse or create>",
                "Source gaps: <missing citations, ambiguous definitions, or provenance blockers>",
                "Recommended attack target: <one concrete target for the next proof-lab attempts>",
            ]
        ).strip() + "\n"

    def _build_audit_prompt(self, *, statement: str, candidate_output: str) -> str:
        return "\n".join(
            [
                "You are an adversarial mathematical reviewer for ARA Proof Lab.",
                "",
                "Hard constraints:",
                "- Do not edit files.",
                "- Your job is to find the first fatal gap or certify that the candidate deserves formalization.",
                "- Be stricter than the prover. Hidden appeals to nontrivial theorems must be named.",
                "- Distinguish mathematical gaps from formalization-only gaps.",
                "",
                "Problem statement:",
                "",
                "```text",
                statement.strip(),
                "```",
                "",
                "Candidate route:",
                "",
                "```text",
                candidate_output.strip(),
                "```",
                "",
                "Output exactly these labeled fields first, then a concise review:",
                "Audit status: <passes_initial_audit|formalization_only|partial|external_theorem_needed|statement_mismatch|counterexample_suspected|fatal_gap>",
                "First fatal gap: <empty if passes_initial_audit, otherwise exact failure>",
                "Needed repair: <one concrete mathematical or formalization repair>",
                "Formalization consequence: <what Lean/certificate task follows>",
                "Recommendation: <formalize|repair_route|switch_route|freeze>",
            ]
        ).strip() + "\n"

    def _backend_resource_policy(self, timeout_sec: int) -> dict[str, Any]:
        return {
            "memory_mb": self.backend_max_memory_mb,
            "cpu_seconds": min(self.backend_max_cpu_seconds, max(timeout_sec + 10, timeout_sec)),
            "max_processes": self.backend_max_processes,
            "niceness": self.backend_niceness,
            "model": self.backend_model,
            "reasoning_effort": self.backend_reasoning_effort,
        }

    def _redacted_command(self, command: list[str]) -> list[str]:
        if not command:
            return []
        return [*command[:-1], "<prompt omitted; see prompt artifact>"]

    def _none_output(self, *, stage: str) -> str:
        if stage == "grounding":
            return "\n".join(
                [
                    "Statement convention: unavailable without a proof backend",
                    "Existing formal assets: not inspected",
                    "Known results: not inspected",
                    "Do not redo: unknown",
                    "Open continuation target: unknown",
                    "Lean entry points: unknown",
                    "Source gaps: run with a real backend or provide explicit source-grounding context",
                    "Recommended attack target: run source-first grounding with backend=codex",
                    "",
                ]
            )
        if stage == "audit":
            return "\n".join(
                [
                    "Audit status: partial",
                    "First fatal gap: Backend none did not audit the route.",
                    "Needed repair: Run with a real backend.",
                    "Formalization consequence: No formalization target can be trusted.",
                    "Recommendation: repair_route",
                    "",
                ]
            )
        return "\n".join(
            [
                "Route title: backend-none placeholder",
                "Claim status: failed",
                "Key lemma: unavailable without a proof backend",
                "Dependency graph: main theorem -> backend output unavailable",
                "Proof sketch: No proof attempt was made because backend=none.",
                "Dependencies: real backend required",
                "Failure mode: backend was intentionally disabled",
                "Formalization target: none",
                "Self-audit: switch to backend=codex for a real clean-room attempt.",
                "",
            ]
        )

    def _invoke_backend(
        self,
        *,
        backend: str,
        run_dir: Path,
        prompt: str,
        output_path: Path,
        timeout_sec: int,
        enable_search: bool,
        stage: str,
    ) -> dict[str, Any]:
        if backend == "none":
            write_text(output_path, self._none_output(stage=stage))
            return {
                "backend": backend,
                "status": "skipped",
                "returncode": 0,
                "elapsed_seconds": 0.0,
                "command": [],
            }

        backend_bin = shutil.which(backend)
        if not backend_bin:
            write_text(output_path, f"Backend `{backend}` is not available.\n")
            return {
                "backend": backend,
                "status": "unavailable",
                "returncode": None,
                "elapsed_seconds": 0.0,
                "command": [],
            }
        if backend != "codex":
            write_text(output_path, f"Backend `{backend}` is not implemented for proof-lab runs.\n")
            return {
                "backend": backend,
                "status": "unsupported",
                "returncode": None,
                "elapsed_seconds": 0.0,
                "command": [],
            }

        command = [backend_bin, "-s", "read-only", "-a", "never"]
        if enable_search:
            command.append("--search")
        if self.backend_model:
            command.extend(["-m", self.backend_model])
        if self.backend_reasoning_effort:
            command.extend(["-c", f'model_reasoning_effort="{self.backend_reasoning_effort}"'])
        resolved_run_dir = run_dir.resolve()
        resolved_output_path = output_path.resolve()
        command.extend(["exec", "-C", str(resolved_run_dir), "--output-last-message", str(resolved_output_path), prompt])

        started = time.monotonic()
        try:
            completed = run_guarded_command(
                command,
                cwd=resolved_run_dir,
                timeout=timeout_sec,
                memory_mb=self.backend_max_memory_mb,
                cpu_seconds=min(self.backend_max_cpu_seconds, max(timeout_sec + 10, timeout_sec)),
                max_processes=self.backend_max_processes,
                niceness=self.backend_niceness,
            )
        except subprocess.TimeoutExpired as exc:
            if not output_path.exists():
                write_text(output_path, "Timed out before producing a final backend message.\n")
            return {
                "backend": backend,
                "status": "timeout",
                "returncode": None,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "command": self._redacted_command(command),
                "stdout_tail": str(exc.stdout or exc.output or "")[-4000:],
                "stderr_tail": str(exc.stderr or "")[-4000:],
                "resource_policy": self._backend_resource_policy(timeout_sec),
            }

        if not output_path.exists():
            write_text(output_path, (completed.stdout + "\n\nSTDERR\n" + completed.stderr).strip() + "\n")
        return {
            "backend": backend,
            "status": "completed" if completed.returncode == 0 else "failed",
            "returncode": completed.returncode,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "command": self._redacted_command(command),
            "stdout_tail": completed.stdout[-4000:],
            "stderr_tail": completed.stderr[-4000:],
            "resource_policy": self._backend_resource_policy(timeout_sec),
        }

    def _select_audit_candidates(
        self,
        *,
        attempts: list[dict[str, Any]],
        clusters: list[dict[str, Any]],
        audits: int,
    ) -> list[dict[str, Any]]:
        if audits <= 0:
            return []
        attempts_by_number = {attempt.get("attempt"): attempt for attempt in attempts}
        selected: list[dict[str, Any]] = []
        for cluster in clusters:
            attempt = attempts_by_number.get(cluster.get("representative_attempt"))
            if attempt:
                selected.append(attempt)
            if len(selected) >= audits:
                break
        return selected

    def _derive_next_action(
        self,
        *,
        clusters: list[dict[str, Any]],
        audit_entries: list[dict[str, Any]],
    ) -> str:
        for audit in audit_entries:
            parsed = audit.get("parsed_fields") or {}
            status = str(parsed.get("audit_status", "")).lower()
            recommendation = str(parsed.get("recommendation", "")).lower()
            if "passes_initial_audit" in status or recommendation == "formalize":
                return "Promote the audited route into a precise Lean/certificate target."
            if "formalization_only" in status:
                return "Keep the route and work on Lean statement/dependency formalization."
        for audit in audit_entries:
            parsed = audit.get("parsed_fields") or {}
            if parsed.get("needed_repair"):
                return f"Repair top route: {parsed['needed_repair']}"
        if clusters:
            top = clusters[0]
            return f"Run more independent attempts or targeted repair around `{top['signature']}`."
        return "No usable route was found; broaden source acquisition and clean-room attempts."

    def _write_summary(
        self,
        *,
        path: Path,
        statement: str,
        grounding: dict[str, Any] | None,
        attempts: list[dict[str, Any]],
        clusters: list[dict[str, Any]],
        audits: list[dict[str, Any]],
        next_action: str,
    ) -> None:
        lines = [
            "# ARA Proof Lab Report",
            "",
            "## Statement",
            "",
            statement.strip(),
            "",
            "## Source Grounding",
            "",
        ]
        if grounding:
            parsed_grounding = grounding.get("parsed_fields") or {}
            lines.extend(
                [
                    f"- Statement convention: {parsed_grounding.get('statement_convention', '<missing>')}",
                    f"- Existing formal assets: {parsed_grounding.get('existing_formal_assets', '<missing>')}",
                    f"- Do not redo: {parsed_grounding.get('do_not_redo', '<missing>')}",
                    f"- Open continuation target: {parsed_grounding.get('open_continuation_target', '<missing>')}",
                    f"- Recommended attack target: {parsed_grounding.get('recommended_attack_target', '<missing>')}",
                    "",
                ]
            )
        else:
            lines.extend(["- Source-first grounding was not enabled.", ""])
        lines.extend(
            [
            "## Attempts",
            "",
            f"- Clean attempts completed: {len(attempts)}",
            f"- Route clusters: {len(clusters)}",
            f"- Audits completed: {len(audits)}",
            "",
            "## Top Route Clusters",
            "",
            ]
        )
        if clusters:
            for cluster in clusters[:5]:
                lines.append(
                    f"- `{cluster['signature']}`: count={cluster['count']}, "
                    f"best_status={cluster['best_status']}, representative={cluster['representative_attempt']}"
                )
        else:
            lines.append("- No clusters.")
        lines.extend(["", "## Audit Results", ""])
        if audits:
            for audit in audits:
                parsed = audit.get("parsed_fields") or {}
                lines.append(
                    f"- Attempt {audit.get('attempt')}: "
                    f"{parsed.get('audit_status', 'unknown')} -> {parsed.get('recommendation', 'unknown')}"
                )
        else:
            lines.append("- No audits.")
        lines.extend(["", "## Next Action", "", next_action.strip(), ""])
        write_text(path, "\n".join(lines))

    def run(
        self,
        *,
        statement: str,
        context_paths: list[Path] | None = None,
        backend: str = "codex",
        attempts: int = 4,
        audits: int = 2,
        time_budget_sec: int = 3600,
        attempt_timeout_sec: int = 600,
        audit_timeout_sec: int = 300,
        source_first: bool = False,
        grounding_timeout_sec: int = 300,
        output_root: Path | None = None,
        run_name: str | None = None,
        enable_search: bool = False,
    ) -> dict[str, Any]:
        if not statement.strip():
            raise ValueError("Proof-lab statement must not be empty.")

        output_root = output_root or (self.repo_root / "artifacts" / "proof_lab")
        run_dir = self._new_run_dir(output_root=output_root, run_name=run_name)
        grounding_dir = run_dir / "grounding"
        attempts_dir = run_dir / "attempts"
        audits_dir = run_dir / "audits"
        grounding_dir.mkdir(parents=True, exist_ok=True)
        attempts_dir.mkdir(parents=True, exist_ok=True)
        audits_dir.mkdir(parents=True, exist_ok=True)

        started = time.monotonic()
        deadline = started + max(1, time_budget_sec)
        context_bundle = self._read_context_bundle(context_paths or [])
        statement_path = run_dir / "statement.md"
        context_bundle_path = run_dir / "context_bundle.md"
        write_text(statement_path, statement.strip() + "\n")
        write_text(context_bundle_path, context_bundle)
        write_json(
            run_dir / "state.json",
            {
                "status": "running",
                "started_at": utc_now_iso(),
                "backend": backend,
                "attempts_requested": attempts,
                "audits_requested": audits,
                "source_first": source_first,
                "time_budget_sec": time_budget_sec,
                "statement_path": str(statement_path),
                "context_bundle_path": str(context_bundle_path),
            },
        )

        grounding_entry: dict[str, Any] | None = None
        grounding_output_path: Path | None = None
        stop_reason = "completed"
        if source_first:
            remaining = int(deadline - time.monotonic())
            if remaining <= 0:
                stop_reason = "time_budget_exhausted"
            else:
                headroom = wait_for_system_headroom(
                    min_available_memory_mb=self.min_available_memory_mb,
                    max_load_per_cpu=1.5,
                    max_wait_seconds=self.wait_max_seconds,
                    poll_seconds=self.wait_poll_seconds,
                )
                if headroom["status"] != "ready":
                    stop_reason = "system_guard_blocked"
                else:
                    grounding_prompt = self._build_source_grounding_prompt(
                        statement=statement,
                        context_bundle_path=context_bundle_path,
                    )
                    grounding_prompt_path = grounding_dir / "source_grounding_prompt.txt"
                    grounding_output_path = grounding_dir / "source_grounding_output.md"
                    grounding_meta_path = grounding_dir / "source_grounding_meta.json"
                    write_text(grounding_prompt_path, grounding_prompt)
                    backend_report = self._invoke_backend(
                        backend=backend,
                        run_dir=run_dir,
                        prompt=grounding_prompt,
                        output_path=grounding_output_path,
                        timeout_sec=min(max(30, grounding_timeout_sec), max(1, remaining)),
                        enable_search=enable_search,
                        stage="grounding",
                    )
                    parsed_grounding = parse_labeled_fields(read_text(grounding_output_path), GROUNDING_LABELS)
                    grounding_entry = {
                        "parsed_fields": parsed_grounding,
                        "backend_report": backend_report,
                        "artifacts": {
                            "prompt": str(grounding_prompt_path),
                            "output": str(grounding_output_path),
                            "meta": str(grounding_meta_path),
                        },
                    }
                    write_json(
                        grounding_meta_path,
                        {
                            **grounding_entry,
                            "system_headroom": headroom,
                            "generated_at": utc_now_iso(),
                        },
                    )
                    if backend_report.get("status") not in {"completed", "skipped"}:
                        stop_reason = "source_grounding_failed"

        attempt_entries: list[dict[str, Any]] = []
        attempt_count = max(0, attempts)
        for attempt in range(1, attempt_count + 1):
            if stop_reason != "completed":
                break
            remaining = int(deadline - time.monotonic())
            if remaining <= 0:
                stop_reason = "time_budget_exhausted"
                break
            headroom = wait_for_system_headroom(
                min_available_memory_mb=self.min_available_memory_mb,
                max_load_per_cpu=1.5,
                max_wait_seconds=self.wait_max_seconds,
                poll_seconds=self.wait_poll_seconds,
            )
            if headroom["status"] != "ready":
                stop_reason = "system_guard_blocked"
                break
            prompt = self._build_clean_attempt_prompt(
                statement=statement,
                context_bundle_path=context_bundle_path,
                grounding_path=grounding_output_path,
                attempt=attempt,
                attempts=attempt_count,
            )
            prompt_path = attempts_dir / f"attempt_{attempt:03d}_prompt.txt"
            output_path = attempts_dir / f"attempt_{attempt:03d}_output.md"
            meta_path = attempts_dir / f"attempt_{attempt:03d}_meta.json"
            write_text(prompt_path, prompt)
            backend_report = self._invoke_backend(
                backend=backend,
                run_dir=run_dir,
                prompt=prompt,
                output_path=output_path,
                timeout_sec=min(max(30, attempt_timeout_sec), max(1, remaining)),
                enable_search=enable_search,
                stage="clean_attempt",
            )
            output_text = read_text(output_path)
            parsed = _normalize_choice_fields(parse_labeled_fields(output_text, CLEAN_ATTEMPT_LABELS), ("claim_status",))
            entry = {
                "attempt": attempt,
                "parsed_fields": parsed,
                "route_signature": route_signature(parsed),
                "backend_report": backend_report,
                "artifacts": {
                    "prompt": str(prompt_path),
                    "output": str(output_path),
                    "meta": str(meta_path),
                },
            }
            attempt_entries.append(entry)
            write_json(
                meta_path,
                {
                    **entry,
                    "system_headroom": headroom,
                    "generated_at": utc_now_iso(),
                },
            )

        clusters = cluster_route_attempts(attempt_entries)
        write_json(run_dir / "route_clusters.json", {"generated_at": utc_now_iso(), "clusters": clusters})

        audit_entries: list[dict[str, Any]] = []
        for candidate in self._select_audit_candidates(attempts=attempt_entries, clusters=clusters, audits=max(0, audits)):
            remaining = int(deadline - time.monotonic())
            if remaining <= 0:
                stop_reason = "time_budget_exhausted"
                break
            attempt_number = int(candidate.get("attempt") or 0)
            candidate_output = read_text(Path(candidate["artifacts"]["output"]))
            prompt = self._build_audit_prompt(statement=statement, candidate_output=candidate_output)
            prompt_path = audits_dir / f"audit_attempt_{attempt_number:03d}_prompt.txt"
            output_path = audits_dir / f"audit_attempt_{attempt_number:03d}_output.md"
            meta_path = audits_dir / f"audit_attempt_{attempt_number:03d}_meta.json"
            write_text(prompt_path, prompt)
            backend_report = self._invoke_backend(
                backend=backend,
                run_dir=run_dir,
                prompt=prompt,
                output_path=output_path,
                timeout_sec=min(max(30, audit_timeout_sec), max(1, remaining)),
                enable_search=enable_search,
                stage="audit",
            )
            parsed = _normalize_choice_fields(
                parse_labeled_fields(read_text(output_path), AUDIT_LABELS),
                ("audit_status", "recommendation"),
            )
            audit_entry = {
                "attempt": attempt_number,
                "parsed_fields": parsed,
                "backend_report": backend_report,
                "artifacts": {
                    "prompt": str(prompt_path),
                    "output": str(output_path),
                    "meta": str(meta_path),
                },
            }
            audit_entries.append(audit_entry)
            write_json(meta_path, {**audit_entry, "generated_at": utc_now_iso()})

        next_action = self._derive_next_action(clusters=clusters, audit_entries=audit_entries)
        payload = {
            "generated_at": utc_now_iso(),
            "status": "completed" if stop_reason == "completed" else "partial",
            "stop_reason": stop_reason,
            "backend": backend,
            "run_dir": str(run_dir),
            "statement_path": str(statement_path),
            "context_bundle_path": str(context_bundle_path),
            "source_first": source_first,
            "grounding": grounding_entry,
            "attempts_completed": len(attempt_entries),
            "audits_completed": len(audit_entries),
            "clusters": clusters,
            "attempts": attempt_entries,
            "audits": audit_entries,
            "next_action": next_action,
            "summary_path": str(run_dir / "summary.md"),
            "elapsed_seconds": round(time.monotonic() - started, 3),
        }
        write_json(run_dir / "report.json", payload)
        self._write_summary(
            path=run_dir / "summary.md",
            statement=statement,
            grounding=grounding_entry,
            attempts=attempt_entries,
            clusters=clusters,
            audits=audit_entries,
            next_action=next_action,
        )
        write_json(run_dir / "state.json", payload)
        return payload
