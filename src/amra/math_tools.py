from __future__ import annotations

import importlib
import importlib.util
import os
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

from amra.core.workspace import write_json, write_text
from amra.infra.runtime import env_bool, env_int, run_guarded_command


MATH_TOOL_REPORT_SCHEMA_VERSION = "amra.math_tools_report.v1"
MATH_TOOL_PROFILES = ("essential", "extended", "full")


@dataclass(frozen=True)
class MathToolSpec:
    tool_id: str
    name: str
    purpose: str
    profile: str
    executables: list[str] = field(default_factory=list)
    python_modules: list[str] = field(default_factory=list)
    pip_packages: list[str] = field(default_factory=list)
    apt_packages: list[str] = field(default_factory=list)
    smoke_commands: list[list[str]] = field(default_factory=list)
    command_templates: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


TOOL_SPECS: tuple[MathToolSpec, ...] = (
    MathToolSpec(
        tool_id="python_math_stack",
        name="Python math stack",
        purpose="Finite search, symbolic checks, numerical sanity checks, graph probes, and counterexample search.",
        profile="essential",
        executables=["python3"],
        python_modules=["sympy", "numpy", "scipy", "networkx", "mpmath"],
        pip_packages=["sympy", "numpy", "scipy", "networkx", "mpmath"],
        smoke_commands=[
            [
                "python3",
                "-c",
                "import sympy,numpy,scipy,networkx,mpmath; print(sympy.factorint(360)); print(numpy.eye(1).shape)",
            ]
        ],
        command_templates=[
            "python3 $AMRA_AGENT_RUN_DIR/experiments/<experiment>.py",
            "python3 - <<'PY'\nimport sympy as sp\n# finite or symbolic check\nPY",
        ],
        notes=["Computation is route evidence unless converted into a checked certificate or Lean proof."],
    ),
    MathToolSpec(
        tool_id="z3",
        name="Z3",
        purpose="Bounded model checks and SMT sanity checks for arithmetic, ordering, graph, and incidence constraints.",
        profile="essential",
        executables=["z3"],
        python_modules=["z3"],
        pip_packages=["z3-solver"],
        apt_packages=["z3"],
        smoke_commands=[
            ["python3", "-c", "from z3 import *; x=Int('x'); s=Solver(); s.add(x>0,x<2); print(s.check())"],
            ["z3", "-version"],
        ],
        command_templates=[
            "python3 - <<'PY'\nfrom z3 import *\n# bounded model check\nPY",
            "z3 <problem>.smt2",
        ],
        notes=["Keep encodings explicit; a SAT/UNSAT result only applies to the encoded finite model."],
    ),
    MathToolSpec(
        tool_id="lean4",
        name="Lean 4 / lake / mathlib",
        purpose="Final trusted formal verification and small theorem-shape probes.",
        profile="essential",
        executables=["lean", "lake"],
        smoke_commands=[["lean", "--version"], ["lake", "--version"]],
        command_templates=[
            "cd $AMRA_AGENT_WORKSPACE && lake build",
            "cd $AMRA_AGENT_WORKSPACE && lake env lean $AMRA_AGENT_RUN_DIR/lean_probes/<probe>.lean",
            "rg -n '<keyword>' .lake/packages/mathlib/Mathlib",
        ],
        notes=["AMRA accepts formal completion only after Lean builds without sorry/admit/axiom/constant/opaque."],
    ),
    MathToolSpec(
        tool_id="pari_gp",
        name="PARI/GP",
        purpose="Fast number-theory experiments, modular arithmetic, algebraic number checks, and sequence probes.",
        profile="extended",
        executables=["gp"],
        apt_packages=["pari-gp"],
        smoke_commands=[["gp", "-q", "-f", "-e", "print(factor(360)); quit"]],
        command_templates=["gp -q <script.gp>"],
        notes=["Use for candidate generation; certify final facts separately."],
    ),
    MathToolSpec(
        tool_id="gap",
        name="GAP",
        purpose="Group theory, finite algebra, combinatorics, and exact discrete computations.",
        profile="extended",
        executables=["gap"],
        apt_packages=["gap"],
        smoke_commands=[["gap", "-q", "-c", "Print(Size(SymmetricGroup(3)),\"\\n\"); QUIT;"]],
        command_templates=["gap -q <script.g>"],
    ),
    MathToolSpec(
        tool_id="singular",
        name="Singular",
        purpose="Polynomial ideals, Groebner bases, and computational commutative algebra.",
        profile="extended",
        executables=["Singular"],
        apt_packages=["singular"],
        smoke_commands=[["Singular", "--version"]],
        command_templates=["Singular -q <script.sing>"],
    ),
    MathToolSpec(
        tool_id="maxima",
        name="Maxima",
        purpose="Classical symbolic algebra and calculus sanity checks.",
        profile="extended",
        executables=["maxima"],
        apt_packages=["maxima"],
        smoke_commands=[["maxima", "--very-quiet", "--batch-string=print(expand((x+1)^3)); quit();"]],
        command_templates=["maxima --batch=<script.mac>"],
    ),
    MathToolSpec(
        tool_id="cvc5",
        name="cvc5",
        purpose="SMT solving complementary to Z3, especially for quantified or arithmetic encodings.",
        profile="extended",
        executables=["cvc5"],
        apt_packages=["cvc5"],
        smoke_commands=[["cvc5", "--version"]],
        command_templates=["cvc5 <problem>.smt2"],
    ),
    MathToolSpec(
        tool_id="sagemath",
        name="SageMath",
        purpose="Broad CAS environment for number theory, algebra, combinatorics, and exact computation.",
        profile="full",
        executables=["sage"],
        apt_packages=["sagemath"],
        smoke_commands=[["sage", "-c", "print(factor(360))"]],
        command_templates=["sage <script.sage>", "sage -python <script.py>"],
        notes=["Large package; full-profile installation can take substantial disk and time."],
    ),
    MathToolSpec(
        tool_id="coq",
        name="Coq / Rocq compatibility",
        purpose="External proof assistant experiments when a source theorem already exists in Coq/Rocq.",
        profile="full",
        executables=["coqc"],
        apt_packages=["coq"],
        smoke_commands=[["coqc", "-v"]],
        command_templates=["coqc <file.v>"],
        notes=["AMRA does not currently translate Coq proofs into Lean automatically."],
    ),
)


def selected_tool_specs(profile: str = "essential", tool_ids: list[str] | None = None) -> list[MathToolSpec]:
    normalized = profile if profile in MATH_TOOL_PROFILES else "essential"
    max_index = MATH_TOOL_PROFILES.index(normalized)
    allowed_profiles = set(MATH_TOOL_PROFILES[: max_index + 1])
    requested = {item.strip() for item in (tool_ids or []) if item.strip()}
    specs = [spec for spec in TOOL_SPECS if spec.profile in allowed_profiles]
    if requested:
        known = {spec.tool_id: spec for spec in TOOL_SPECS}
        specs.extend(known[item] for item in requested if item in known and known[item] not in specs)
    return specs


def executable_status(name: str) -> dict[str, Any]:
    path = shutil.which(name)
    return {"name": name, "available": bool(path), "path": path or ""}


def python_module_status(name: str) -> dict[str, Any]:
    spec = importlib.util.find_spec(name)
    return {"name": name, "available": spec is not None}


def _missing_for_spec(spec: MathToolSpec) -> dict[str, list[str]]:
    missing_executables = [name for name in spec.executables if not shutil.which(name)]
    missing_modules = [name for name in spec.python_modules if importlib.util.find_spec(name) is None]
    return {"executables": missing_executables, "python_modules": missing_modules}


def _tool_available(spec: MathToolSpec) -> bool:
    missing = _missing_for_spec(spec)
    return not missing["executables"] and not missing["python_modules"]


def _apt_command(packages: list[str]) -> list[str]:
    if not packages:
        return []
    if os.geteuid() == 0:
        return ["apt-get", "install", "-y", *packages]
    sudo = shutil.which("sudo")
    if sudo:
        return [sudo, "-n", "apt-get", "install", "-y", *packages]
    return []


def _run_command(
    command: list[str],
    *,
    cwd: Path | None = None,
    timeout_sec: int,
    command_runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> dict[str, Any]:
    started = time.monotonic()
    try:
        runner = command_runner or run_guarded_command
        completed = runner(
            command,
            cwd=cwd or Path.cwd(),
            timeout=max(1, timeout_sec),
            memory_mb=env_int("AMRA_MATH_TOOLS_MAX_MEMORY_MB", 4096),
            cpu_seconds=max(1, timeout_sec + 10),
            max_processes=env_int("AMRA_MATH_TOOLS_MAX_PROCESSES", 1024),
            niceness=env_int("AMRA_MATH_TOOLS_NICENESS", 10),
        )
        return {
            "command": command,
            "status": "completed" if completed.returncode == 0 else "failed",
            "returncode": completed.returncode,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "stdout_tail": str(completed.stdout or "")[-4000:],
            "stderr_tail": str(completed.stderr or "")[-4000:],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "status": "timeout",
            "returncode": None,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "stdout_tail": str(exc.stdout or exc.output or "")[-4000:],
            "stderr_tail": str(exc.stderr or "")[-4000:],
        }
    except Exception as exc:  # pragma: no cover - defensive for platform package managers.
        return {
            "command": command,
            "status": "error",
            "returncode": None,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "stdout_tail": "",
            "stderr_tail": repr(exc),
        }


def _install_python_packages(
    packages: list[str],
    *,
    timeout_sec: int,
    command_runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> dict[str, Any]:
    if not packages:
        return {"status": "skipped", "reason": "no python packages requested", "command": []}
    command = ["python3", "-m", "pip", "install", "--user", *packages]
    return _run_command(command, timeout_sec=timeout_sec, command_runner=command_runner)


def _install_apt_packages(
    packages: list[str],
    *,
    timeout_sec: int,
    command_runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> dict[str, Any]:
    command = _apt_command(packages)
    if not command:
        return {
            "status": "unavailable",
            "reason": "apt-get requires root or passwordless sudo",
            "command": [],
            "packages": packages,
        }
    return _run_command(command, timeout_sec=timeout_sec, command_runner=command_runner)


def ensure_math_tools(
    *,
    output_dir: Path,
    profile: str = "essential",
    install_missing: bool | None = None,
    tool_ids: list[str] | None = None,
    run_smoke: bool | None = None,
    timeout_sec: int = 300,
    workspace: Path | None = None,
    command_runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> dict[str, Any]:
    """Ensure and document the math tools AMRA exposes to agents.

    Installation is intentionally performed only when this function is called,
    not at import time. Missing selected tools are installed through pip or
    apt-get when possible; failed installs remain visible in the report.
    """

    if install_missing is None:
        install_missing = env_bool("AMRA_INSTALL_MISSING_MATH_TOOLS", True)
    if run_smoke is None:
        run_smoke = env_bool("AMRA_RUN_MATH_TOOL_SMOKE", True)
    output_dir.mkdir(parents=True, exist_ok=True)
    specs = selected_tool_specs(profile=profile, tool_ids=tool_ids)
    install_reports: list[dict[str, Any]] = []
    entries: list[dict[str, Any]] = []

    for spec in specs:
        before_missing = _missing_for_spec(spec)
        if install_missing and (before_missing["executables"] or before_missing["python_modules"]):
            missing_pip = list(spec.pip_packages) if before_missing["python_modules"] else []
            missing_apt = list(spec.apt_packages) if before_missing["executables"] else []
            pip_report = _install_python_packages(
                missing_pip,
                timeout_sec=timeout_sec,
                command_runner=command_runner,
            )
            apt_report = _install_apt_packages(
                missing_apt,
                timeout_sec=timeout_sec,
                command_runner=command_runner,
            )
            install_reports.append(
                {
                    "tool_id": spec.tool_id,
                    "before_missing": before_missing,
                    "pip": pip_report,
                    "apt": apt_report,
                }
            )
            importlib.invalidate_caches()

        after_missing = _missing_for_spec(spec)
        smoke_reports: list[dict[str, Any]] = []
        if run_smoke and not after_missing["executables"] and not after_missing["python_modules"]:
            for command in spec.smoke_commands:
                smoke_reports.append(
                    _run_command(command, cwd=workspace, timeout_sec=min(timeout_sec, 8), command_runner=command_runner)
                )
        entries.append(
            {
                "spec": spec.to_dict(),
                "available": not after_missing["executables"] and not after_missing["python_modules"],
                "missing": after_missing,
                "executables": [executable_status(name) for name in spec.executables],
                "python_modules": [python_module_status(name) for name in spec.python_modules],
                "smoke": smoke_reports,
            }
        )

    payload = {
        "schema_version": MATH_TOOL_REPORT_SCHEMA_VERSION,
        "profile": profile if profile in MATH_TOOL_PROFILES else "essential",
        "install_missing": bool(install_missing),
        "run_smoke": run_smoke,
        "workspace": str(workspace or ""),
        "tools": entries,
        "install_reports": install_reports,
        "available_tool_ids": [entry["spec"]["tool_id"] for entry in entries if entry["available"]],
        "unavailable_tool_ids": [entry["spec"]["tool_id"] for entry in entries if not entry["available"]],
        "all_selected_available": all(bool(entry["available"]) for entry in entries),
        "report_path": str(output_dir / "math_tools_report.json"),
        "summary_path": str(output_dir / "math_tools_report.md"),
    }
    write_json(output_dir / "math_tools_report.json", payload)
    write_text(output_dir / "math_tools_report.md", render_math_tool_report(payload))
    return payload


def render_math_tool_report(payload: dict[str, Any]) -> str:
    lines = [
        "# AMRA Math Tools Report",
        "",
        f"- Schema: `{payload.get('schema_version')}`",
        f"- Profile: `{payload.get('profile')}`",
        f"- Install missing tools: `{payload.get('install_missing')}`",
        f"- Smoke checks: `{payload.get('run_smoke')}`",
        f"- All selected available: `{payload.get('all_selected_available')}`",
        "",
        "## Tools",
        "",
    ]
    for entry in list(payload.get("tools") or []):
        spec = dict(entry.get("spec") or {})
        lines.extend(
            [
                f"### {spec.get('name')} (`{spec.get('tool_id')}`)",
                "",
                f"- Available: `{entry.get('available')}`",
                f"- Purpose: {spec.get('purpose')}",
                f"- Missing executables: `{', '.join(entry.get('missing', {}).get('executables', [])) or '<none>'}`",
                f"- Missing Python modules: `{', '.join(entry.get('missing', {}).get('python_modules', [])) or '<none>'}`",
                "- Command templates:",
            ]
        )
        templates = list(spec.get("command_templates") or [])
        lines.extend(f"  - `{template}`" for template in templates) if templates else lines.append("  - <none>")
        smoke = list(entry.get("smoke") or [])
        if smoke:
            lines.append("- Smoke checks:")
            for item in smoke:
                lines.append(
                    "  - `{}` -> `{}`".format(
                        " ".join(str(part) for part in item.get("command", [])),
                        item.get("status"),
                    )
                )
        notes = list(spec.get("notes") or [])
        if notes:
            lines.append("- Notes:")
            lines.extend(f"  - {note}" for note in notes)
        lines.append("")
    if payload.get("install_reports"):
        lines.extend(["## Install Reports", ""])
        for item in list(payload.get("install_reports") or []):
            lines.append(f"- `{item.get('tool_id')}`: pip=`{(item.get('pip') or {}).get('status')}`, apt=`{(item.get('apt') or {}).get('status')}`")
        lines.append("")
    lines.extend(
        [
            "## Agent Guidance",
            "",
            "- Use these tools before committing to a long proof route when a finite search, SMT encoding, CAS check, or Lean probe can falsify the plan quickly.",
            "- Treat CAS/SMT/Python output as evidence or certificate material, not as final proof unless translated into a checked Lean artifact.",
            "- Record every nontrivial tool check in `experiments.jsonl`, `lean_probe_log.md`, or the run-specific proof notes.",
            "",
        ]
    )
    return "\n".join(lines)


__all__ = [
    "MATH_TOOL_PROFILES",
    "MATH_TOOL_REPORT_SCHEMA_VERSION",
    "MathToolSpec",
    "TOOL_SPECS",
    "ensure_math_tools",
    "render_math_tool_report",
    "selected_tool_specs",
]
