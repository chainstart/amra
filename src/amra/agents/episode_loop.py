from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from amra.agents.env import agent_environment
from amra.agents.source_policy import apply_codex_source_policy, mark_policy_violation, source_policy_prompt


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or "agent-run"


def read_text(path: Path, *, max_chars: int | None = None) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if max_chars is not None and len(text) > max_chars:
        return text[:max_chars] + "\n[truncated]\n"
    return text


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _resolve_loose(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def _tail(value: str, limit: int) -> str:
    if len(value) <= limit:
        return value
    return value[-limit:]


def _new_run_dir(output_root: Path, run_name: str | None, default_name: str) -> Path:
    output_root = _resolve_loose(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    base = slugify(run_name or f"{default_name}-{utc_now_iso()}")
    candidate = output_root / base
    if not candidate.exists():
        return candidate
    suffix = 2
    while True:
        candidate = output_root / f"{base}-{suffix}"
        if not candidate.exists():
            return candidate
        suffix += 1


def _extract_status(text: str, fallback: str = "partial") -> str:
    match = re.search(r"(?im)^\s*STATUS\s*:\s*([a-zA-Z_ -]+)\s*$", text)
    if not match:
        return fallback
    return match.group(1).strip().lower().replace("-", "_").replace(" ", "_")


def _extract_next(text: str) -> str:
    match = re.search(r"(?im)^\s*NEXT\s*:\s*([a-zA-Z_ -]+)\s*$", text)
    if not match:
        return ""
    return match.group(1).strip().lower().replace("-", "_").replace(" ", "_")


def _strip_lean_comments(text: str) -> str:
    text = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    return re.sub(r"--.*$", "", text, flags=re.MULTILINE)


def _iter_project_lean_files(workspace: Path) -> list[Path]:
    if not workspace.exists():
        return []
    return sorted(path for path in workspace.rglob("*.lean") if ".lake" not in path.parts)


def _extract_lean_target_name(text: str) -> str:
    match = re.search(r"(?m)^\s*(?:theorem|lemma)\s+([A-Za-z0-9_'.]+)", _strip_lean_comments(text))
    return match.group(1).rstrip(".,:;") if match else ""


def _lean_target_exists(workspace: Path, target_name: str) -> bool | None:
    if not target_name:
        return None
    pattern = re.compile(rf"^\s*(?:theorem|lemma)\s+{re.escape(target_name)}(?:\s|:|\(|\{{|\[|$)", re.MULTILINE)
    for path in _iter_project_lean_files(workspace):
        if pattern.search(read_text(path)):
            return True
    return False


def _count_lean_pattern(workspace: Path, pattern: re.Pattern[str]) -> int:
    total = 0
    for path in _iter_project_lean_files(workspace):
        total += len(pattern.findall(_strip_lean_comments(read_text(path))))
    return total


def _run_command(command: list[str], *, cwd: Path, timeout_sec: int) -> dict[str, Any]:
    started = time.monotonic()
    try:
        completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=max(1, timeout_sec))
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "timeout",
            "returncode": None,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "command": command,
            "stdout_tail": _tail(str(exc.stdout or exc.output or ""), 8000),
            "stderr_tail": _tail(str(exc.stderr or ""), 8000),
        }
    return {
        "status": "passed" if completed.returncode == 0 else "failed",
        "returncode": completed.returncode,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "command": command,
        "stdout_tail": _tail(completed.stdout, 8000),
        "stderr_tail": _tail(completed.stderr, 8000),
    }


@dataclass
class CodexEpisodeConfig:
    name: str
    system_prompt: str
    workspace: Path
    output_root: Path
    run_name: str | None = None
    backend: str = "codex"
    model: str | None = None
    reasoning_effort: str | None = None
    enable_search: bool = True
    max_episodes: int = 8
    time_budget_sec: int = 3600
    episode_timeout_sec: int = 600
    sandbox: str = "workspace-write"


EpisodeObserver = Callable[[int, Path, str, dict[str, Any]], dict[str, Any]]


class CodexEpisodeLoopAgent:
    """Host-supervised Codex episode loop.

    Codex owns the inner action loop inside each episode. The host owns durable
    state, observations, independent checks, budgets, and stop conditions.
    """

    def __init__(self, config: CodexEpisodeConfig) -> None:
        self.config = config
        self.workspace = _resolve_loose(config.workspace)
        self.run_dir = _new_run_dir(config.output_root, config.run_name, config.name)

    def _call_codex(
        self,
        *,
        prompt: str,
        cwd: Path,
        output_path: Path,
        timeout_sec: int,
    ) -> dict[str, Any]:
        stdout_path = output_path.parent / "stdout.log"
        stderr_path = output_path.parent / "stderr.log"
        if self.config.backend == "none":
            text = "\n".join(
                [
                    "STATUS: blocked",
                    "",
                    "Backend is disabled. No autonomous Codex episode was run.",
                    "",
                    "NEXT: rerun with --backend codex",
                    "",
                ]
            )
            write_text(output_path, text)
            return {"backend": "none", "status": "skipped", "returncode": 0, "elapsed_seconds": 0.0}

        if self.config.backend != "codex":
            text = "\n".join(
                [
                    "STATUS: blocked",
                    "",
                    f"Unsupported backend: {self.config.backend}",
                    "",
                    "NEXT: use --backend codex",
                    "",
                ]
            )
            write_text(output_path, text)
            return {
                "backend": self.config.backend,
                "status": "unsupported",
                "returncode": None,
                "elapsed_seconds": 0.0,
            }

        backend_bin = shutil.which("codex")
        if not backend_bin:
            text = "\n".join(
                [
                    "STATUS: blocked",
                    "",
                    "The codex executable is not available on PATH.",
                    "",
                    "NEXT: install or expose codex, then rerun",
                    "",
                ]
            )
            write_text(output_path, text)
            return {"backend": "codex", "status": "unavailable", "returncode": None, "elapsed_seconds": 0.0}

        command = [backend_bin, "-s", self.config.sandbox, "-a", "never"]
        apply_codex_source_policy(command, enable_search=self.config.enable_search)
        if self.config.model:
            command.extend(["-m", self.config.model])
        if self.config.reasoning_effort:
            command.extend(["-c", f'model_reasoning_effort="{self.config.reasoning_effort}"'])
        command.extend(["exec", "-C", str(cwd), "--output-last-message", str(output_path), "-"])

        started = time.monotonic()
        try:
            completed = subprocess.run(
                command,
                cwd=cwd,
                input=prompt,
                text=True,
                capture_output=True,
                timeout=max(1, timeout_sec),
                env={
                    **os.environ,
                    **agent_environment(run_dir=self.run_dir, workspace=self.workspace),
                },
            )
        except subprocess.TimeoutExpired as exc:
            stdout = str(exc.stdout or exc.output or "")
            stderr = str(exc.stderr or "")
            write_text(stdout_path, stdout)
            write_text(stderr_path, stderr)
            if not output_path.exists():
                write_text(output_path, "STATUS: partial\n\nCodex episode timed out before final response.\n")
            return mark_policy_violation(
                report={
                    "backend": "codex",
                    "status": "timeout",
                    "returncode": None,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "command": [*command[:-1], "<prompt omitted>"],
                    "stdout_tail": _tail(stdout, 4000),
                    "stderr_tail": _tail(stderr, 4000),
                    "stdout_path": str(stdout_path),
                    "stderr_path": str(stderr_path),
                },
                output_path=output_path,
                stdout=stdout,
                stderr=stderr,
                enable_search=self.config.enable_search,
            )

        write_text(stdout_path, completed.stdout)
        write_text(stderr_path, completed.stderr)
        if not output_path.exists():
            write_text(output_path, (completed.stdout + "\n" + completed.stderr).strip() + "\n")
        return mark_policy_violation(
            report={
                "backend": "codex",
                "status": "completed" if completed.returncode == 0 else "failed",
                "returncode": completed.returncode,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "command": [*command[:-1], "<prompt omitted>"],
                "stdout_tail": _tail(completed.stdout, 4000),
                "stderr_tail": _tail(completed.stderr, 4000),
                "stdout_path": str(stdout_path),
                "stderr_path": str(stderr_path),
            },
            output_path=output_path,
            stdout=completed.stdout,
            stderr=completed.stderr,
            enable_search=self.config.enable_search,
        )

    def _build_episode_prompt(
        self,
        *,
        goal: str,
        episode: int,
        observations: list[dict[str, Any]],
        remaining_seconds: int,
    ) -> str:
        continuation_directives = [
            str(observation.get("next_episode_directive", "")).strip()
            for observation in observations[-3:]
            if str(observation.get("next_episode_directive", "")).strip()
        ]
        directive_lines: list[str] = []
        if continuation_directives:
            directive_lines = [
                "Host continuation directive:",
                continuation_directives[-1],
                "",
            ]
        return "\n".join(
            [
                self.config.system_prompt.strip(),
                "",
                "You are running one bounded autonomous Codex episode.",
                "Inside this episode, use your native tools directly: inspect files, run commands, edit allowed files, and iterate.",
                "Do not return JSON tool actions. The host will not execute single-step JSON actions for you.",
                "The host will persist your final message, run independent observations, then decide whether to launch another episode.",
                "",
                f"Agent name: {self.config.name}",
                f"Episode: {episode} of {self.config.max_episodes}",
                f"Workspace: {self.workspace}",
                f"Run directory: {self.run_dir}",
                f"Remaining host budget seconds: {remaining_seconds}",
                "",
                source_policy_prompt(enable_search=self.config.enable_search),
                "",
                "Current host observations:",
                json.dumps(observations[-8:], indent=2, ensure_ascii=False),
                "",
                *directive_lines,
                "Goal:",
                goal.strip(),
                "",
                "At the end of this episode, include these plain-text lines in your final response:",
                "STATUS: proved_candidate|verified|partial|blocked|counterexample_suspected|failed",
                "NEXT: continue|stop|needs-human",
                "CHANGED: <files or artifacts changed>",
                "BLOCKER: <current first blocker, or none>",
                "",
            ]
        )

    def run(
        self,
        *,
        goal: str,
        episode_cwd: Path,
        observer: EpisodeObserver,
        initial_observation: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.run_dir.mkdir(parents=True, exist_ok=True)
        episodes_dir = self.run_dir / "episodes"
        episodes_dir.mkdir(parents=True, exist_ok=True)
        observations: list[dict[str, Any]] = []
        if initial_observation is not None:
            observations.append(initial_observation)
        started = time.monotonic()
        deadline = started + max(1, self.config.time_budget_sec)
        episode_reports: list[dict[str, Any]] = []
        stop_reason = "max_episodes_exhausted"

        write_json(
            self.run_dir / "state.json",
            {
                "agent": self.config.name,
                "status": "running",
                "started_at": utc_now_iso(),
                "workspace": str(self.workspace),
                "run_dir": str(self.run_dir),
                "initial_observation": initial_observation,
            },
        )

        if initial_observation and initial_observation.get("terminal"):
            stop_reason = "initial_observation_terminal"

        if stop_reason != "initial_observation_terminal":
            for episode in range(1, max(0, self.config.max_episodes) + 1):
                remaining = int(deadline - time.monotonic())
                if remaining <= 0:
                    stop_reason = "time_budget_exhausted"
                    break
                episode_dir = episodes_dir / f"episode_{episode:03d}"
                episode_dir.mkdir(parents=True, exist_ok=True)
                prompt = self._build_episode_prompt(
                    goal=goal,
                    episode=episode,
                    observations=observations,
                    remaining_seconds=remaining,
                )
                prompt_path = episode_dir / "prompt.txt"
                last_message_path = episode_dir / "last_message.md"
                write_text(prompt_path, prompt)
                backend_report = self._call_codex(
                    prompt=prompt,
                    cwd=episode_cwd,
                    output_path=last_message_path,
                    timeout_sec=min(max(1, self.config.episode_timeout_sec), remaining),
                )
                last_message = read_text(last_message_path)
                observation = observer(episode, episode_dir, last_message, backend_report)
                observations.append(observation)
                episode_report = {
                    "episode": episode,
                    "backend": backend_report,
                    "last_message_path": str(last_message_path),
                    "observation": observation,
                }
                episode_reports.append(episode_report)
                write_json(episode_dir / "backend_report.json", backend_report)
                write_json(episode_dir / "observation.json", observation)
                write_json(episode_dir / "episode_report.json", episode_report)
                write_json(
                    self.run_dir / "state.json",
                    {
                        "agent": self.config.name,
                        "status": "running",
                        "workspace": str(self.workspace),
                        "run_dir": str(self.run_dir),
                        "episodes_completed": len(episode_reports),
                        "latest_observation": observation,
                    },
                )
                if observation.get("terminal"):
                    stop_reason = str(observation.get("stop_reason") or "terminal_observation")
                    break

        final_observation = observations[-1] if observations else {}
        status = str(final_observation.get("status") or ("blocked" if not episode_reports else "partial"))
        report = {
            "agent": self.config.name,
            "status": status,
            "stop_reason": stop_reason,
            "generated_at": utc_now_iso(),
            "workspace": str(self.workspace),
            "run_dir": str(self.run_dir),
            "backend": self.config.backend,
            "max_episodes": self.config.max_episodes,
            "episodes_completed": len(episode_reports),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "observations": observations,
            "episodes": episode_reports,
            "final_observation": final_observation,
            "report_path": str(self.run_dir / "report.json"),
        }
        write_json(self.run_dir / "observations.json", observations)
        write_json(self.run_dir / "report.json", report)
        write_json(self.run_dir / "state.json", report)
        write_text(
            self.run_dir / "final.md",
            "\n".join(
                [
                    f"# {self.config.name}",
                    "",
                    f"- Status: {status}",
                    f"- Stop reason: {stop_reason}",
                    f"- Episodes completed: {len(episode_reports)}",
                    "",
                    "## Final Observation",
                    "",
                    json.dumps(final_observation, indent=2, ensure_ascii=False),
                    "",
                ]
            ),
        )
        return report



__all__ = [
    "CodexEpisodeConfig",
    "CodexEpisodeLoopAgent",
    "EpisodeObserver",
    "utc_now_iso",
    "slugify",
    "read_text",
    "write_text",
    "write_json",
]
