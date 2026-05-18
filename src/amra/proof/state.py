from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ProofArtifactTracker:
    """Durable state layout for the unified proof-development loop."""

    ARTIFACT_NAMES = [
        "proof_notes.md",
        "lemma_backlog.md",
        "blockers.md",
        "experiments.jsonl",
        "lean_probe_log.md",
        "verified_lean_declarations.md",
        "source_notes.md",
        "proof_package.md",
        "formalizer_handoff.md",
        "dependency_graph.md",
        "partial_lemmas.md",
        "failed_routes.md",
        "invariant_candidates.md",
        "counterexample_report.md",
    ]

    BOOTSTRAP_FILES = {
        "proof_notes.md": "# Proof Notes\n\n",
        "lemma_backlog.md": "# Lemma Backlog\n\n",
        "blockers.md": "# Blockers\n\n",
        "experiments.jsonl": "",
        "lean_probe_log.md": "# Lean Probe Log\n\n",
        "verified_lean_declarations.md": "# Verified Lean Declarations\n\n",
        "source_notes.md": "# Source Notes\n\n",
    }

    def __init__(self, run_dir: Path) -> None:
        self.run_dir = run_dir

    def bootstrap(
        self,
        *,
        statement: str,
        workspace: Path | None,
        build_command: list[str],
        target_name: str,
        tool_registry_path: Path,
    ) -> dict[str, Any]:
        self.run_dir.mkdir(parents=True, exist_ok=True)
        for name, content in self.BOOTSTRAP_FILES.items():
            path = self.run_dir / name
            if not path.exists():
                path.write_text(content, encoding="utf-8")
        payload = {
            "statement": statement.strip(),
            "workspace": str(workspace) if workspace is not None else "",
            "build_command": build_command,
            "target_name": target_name,
            "tool_registry_path": str(tool_registry_path),
            "mode": "unified_proof_development",
            "status": "initialized",
            "artifacts": self.snapshot(workspace=workspace),
        }
        self.write_state(payload)
        return payload

    def write_state(self, payload: dict[str, Any]) -> None:
        (self.run_dir / "proof_state.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def snapshot(self, *, workspace: Path | None = None) -> dict[str, Any]:
        artifacts = {
            name: {
                "exists": (self.run_dir / name).exists(),
                "size": (self.run_dir / name).stat().st_size if (self.run_dir / name).exists() else 0,
            }
            for name in self.ARTIFACT_NAMES
        }
        workspace_payload: dict[str, Any] = {}
        if workspace is not None:
            lean_files = []
            if workspace.exists():
                lean_files = sorted(
                    str(path.relative_to(workspace))
                    for path in workspace.rglob("*.lean")
                    if ".lake" not in path.parts
                )
            workspace_payload = {
                "path": str(workspace),
                "exists": workspace.exists(),
                "lean_files": lean_files,
                "lean_scratch_exists": (workspace / "MathProject" / "LeanScratch.lean").exists(),
            }
        return {
            "run_artifacts": artifacts,
            "workspace": workspace_payload,
        }

    def has_useful_progress(self) -> bool:
        snapshot = self.snapshot()["run_artifacts"]
        for name in ("proof_package.md", "formalizer_handoff.md", "partial_lemmas.md", "invariant_candidates.md"):
            if snapshot[name]["exists"] and snapshot[name]["size"] > 0:
                return True
        notes = snapshot["proof_notes.md"]
        backlog = snapshot["lemma_backlog.md"]
        return notes["size"] > len(self.BOOTSTRAP_FILES["proof_notes.md"]) or backlog["size"] > len(
            self.BOOTSTRAP_FILES["lemma_backlog.md"]
        )


__all__ = ["ProofArtifactTracker"]
