from __future__ import annotations

import os
import resource
import signal
import subprocess
import time
from pathlib import Path
from typing import Any


def env_int(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    if not raw:
        return default
    return raw in {"1", "true", "yes", "on"}


def env_str(name: str, default: str = "") -> str:
    raw = os.environ.get(name, "")
    return raw.strip() if raw.strip() else default


def build_resource_policy(
    *,
    memory_mb: int,
    cpu_seconds: int,
    max_processes: int,
    niceness: int,
    allow_cold_cache: bool = False,
) -> dict[str, Any]:
    return {
        "memory_mb": memory_mb,
        "cpu_seconds": cpu_seconds,
        "max_processes": max_processes,
        "niceness": niceness,
        "allow_cold_cache": allow_cold_cache,
    }


def env_float(name: str, default: float) -> float:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def read_meminfo_kb() -> dict[str, int]:
    meminfo: dict[str, int] = {}
    try:
        for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            field = value.strip().split()
            if not field:
                continue
            try:
                meminfo[key] = int(field[0])
            except ValueError:
                continue
    except OSError:
        return {}
    return meminfo


def current_system_snapshot() -> dict[str, Any]:
    cpu_count = max(1, os.cpu_count() or 1)
    try:
        load1, load5, load15 = os.getloadavg()
    except OSError:
        load1 = load5 = load15 = 0.0
    meminfo = read_meminfo_kb()
    available_kb = int(meminfo.get("MemAvailable", 0))
    total_kb = int(meminfo.get("MemTotal", 0))
    return {
        "captured_at": int(time.time()),
        "cpu_count": cpu_count,
        "load1": round(load1, 3),
        "load5": round(load5, 3),
        "load15": round(load15, 3),
        "load_per_cpu": round(load1 / cpu_count, 3),
        "mem_total_mb": round(total_kb / 1024, 1) if total_kb else 0.0,
        "mem_available_mb": round(available_kb / 1024, 1) if available_kb else 0.0,
    }


def check_system_headroom(
    *,
    min_available_memory_mb: int,
    max_load_per_cpu: float,
) -> dict[str, Any]:
    snapshot = current_system_snapshot()
    blockers: list[str] = []
    if snapshot["mem_available_mb"] and snapshot["mem_available_mb"] < min_available_memory_mb:
        blockers.append(
            f"Available memory {snapshot['mem_available_mb']} MB is below the guarded minimum of {min_available_memory_mb} MB."
        )
    if snapshot["load_per_cpu"] > max_load_per_cpu:
        blockers.append(
            f"Load per CPU {snapshot['load_per_cpu']} exceeds the guarded maximum of {max_load_per_cpu}."
        )
    return {
        "status": "ready" if not blockers else "blocked",
        "snapshot": snapshot,
        "blockers": blockers,
        "thresholds": {
            "min_available_memory_mb": min_available_memory_mb,
            "max_load_per_cpu": max_load_per_cpu,
        },
    }


def wait_for_system_headroom(
    *,
    min_available_memory_mb: int,
    max_load_per_cpu: float,
    max_wait_seconds: int,
    poll_seconds: int,
) -> dict[str, Any]:
    started = time.monotonic()
    polls: list[dict[str, Any]] = []
    while True:
        report = check_system_headroom(
            min_available_memory_mb=min_available_memory_mb,
            max_load_per_cpu=max_load_per_cpu,
        )
        polls.append(report["snapshot"])
        if report["status"] == "ready":
            report["waited_seconds"] = round(time.monotonic() - started, 3)
            report["poll_count"] = len(polls)
            report["polls"] = polls[-5:]
            return report
        elapsed = time.monotonic() - started
        if elapsed >= max_wait_seconds:
            report["waited_seconds"] = round(elapsed, 3)
            report["poll_count"] = len(polls)
            report["polls"] = polls[-5:]
            return report
        time.sleep(max(1, poll_seconds))


def _apply_rlimit(limit_name: str, soft: int | None, hard: int | None = None) -> None:
    limit = getattr(resource, limit_name, None)
    if limit is None or soft is None or soft <= 0:
        return
    resource.setrlimit(limit, (soft, soft if hard is None else hard))


def _preexec_fn(
    *,
    memory_mb: int,
    cpu_seconds: int,
    max_processes: int,
    niceness: int,
) -> None:
    os.setsid()
    if niceness:
        try:
            os.nice(niceness)
        except OSError:
            pass
    _apply_rlimit("RLIMIT_CPU", cpu_seconds)
    _apply_rlimit("RLIMIT_NPROC", max_processes)
    _apply_rlimit("RLIMIT_NOFILE", max(64, min(512, max_processes * 8)))
    if memory_mb > 0:
        _apply_rlimit("RLIMIT_AS", memory_mb * 1024 * 1024)


def run_guarded_command(
    command: list[str],
    *,
    cwd: Path,
    timeout: int,
    env: dict[str, str] | None = None,
    memory_mb: int,
    cpu_seconds: int,
    max_processes: int,
    niceness: int,
) -> subprocess.CompletedProcess[str]:
    process = subprocess.Popen(
        command,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        preexec_fn=lambda: _preexec_fn(
            memory_mb=memory_mb,
            cpu_seconds=cpu_seconds,
            max_processes=max_processes,
            niceness=niceness,
        ),
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        stdout, stderr = process.communicate()
        raise subprocess.TimeoutExpired(command, timeout, output=stdout or exc.output, stderr=stderr or exc.stderr)
    return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
