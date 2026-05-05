from __future__ import annotations

import time
from pathlib import Path

from ara_math.math_attack import MathAttackRunner


def _runner(tmp_path: Path) -> MathAttackRunner:
    return MathAttackRunner(repo_root=tmp_path)


def test_adaptive_sleep_treats_sleep_seconds_as_cap(tmp_path: Path) -> None:
    runner = _runner(tmp_path)

    plan = runner._sleep_plan(
        run_dir=tmp_path / "run",
        iteration=1,
        iterations=10,
        deadline=time.monotonic() + 3600,
        sleep_mode="adaptive",
        sleep_seconds=1200,
        min_sleep_seconds=60,
        max_sleep_seconds=None,
        sleep_jitter_seconds=0,
        backend_report={"status": "completed", "elapsed_seconds": 120},
    )

    assert plan["seconds"] == 60
    assert plan["seconds"] < 1200
    assert plan["max_sleep_seconds"] == 1200
    assert plan["reason"] == "adaptive_elapsed"


def test_adaptive_sleep_backs_off_on_rate_limit(tmp_path: Path) -> None:
    runner = _runner(tmp_path)

    plan = runner._sleep_plan(
        run_dir=tmp_path / "run",
        iteration=1,
        iterations=10,
        deadline=time.monotonic() + 3600,
        sleep_mode="adaptive",
        sleep_seconds=1200,
        min_sleep_seconds=60,
        max_sleep_seconds=300,
        sleep_jitter_seconds=30,
        backend_report={"status": "failed", "elapsed_seconds": 20, "stderr_tail": "HTTP 429 rate limit"},
    )

    assert plan["seconds"] == 300
    assert plan["reason"] == "backend_backoff"
    assert plan["rate_or_usage_backoff"] is True


def test_adaptive_sleep_does_not_backoff_on_date_path_containing_429(tmp_path: Path) -> None:
    runner = _runner(tmp_path)

    plan = runner._sleep_plan(
        run_dir=tmp_path / "run_20260429",
        iteration=1,
        iterations=10,
        deadline=time.monotonic() + 3600,
        sleep_mode="adaptive",
        sleep_seconds=600,
        min_sleep_seconds=45,
        max_sleep_seconds=600,
        sleep_jitter_seconds=0,
        backend_report={
            "status": "completed",
            "elapsed_seconds": 62,
            "stdout_tail": "/tmp/run_20260429/iterations/iter_001_output.md\nStatus: rigorous",
            "stderr_tail": "tokens used\n48,278\n",
        },
    )

    assert plan["reason"] == "adaptive_elapsed"
    assert plan["rate_or_usage_backoff"] is False
    assert plan["seconds"] == 45


def test_fixed_sleep_preserves_old_exact_wait_semantics(tmp_path: Path) -> None:
    runner = _runner(tmp_path)

    plan = runner._sleep_plan(
        run_dir=tmp_path / "run",
        iteration=1,
        iterations=10,
        deadline=time.monotonic() + 3600,
        sleep_mode="fixed",
        sleep_seconds=1200,
        min_sleep_seconds=60,
        max_sleep_seconds=None,
        sleep_jitter_seconds=0,
        backend_report={"status": "completed", "elapsed_seconds": 120},
    )

    assert plan["seconds"] == 1200
    assert plan["reason"] == "fixed"


def test_adaptive_sleep_is_disabled_without_sleep_budget(tmp_path: Path) -> None:
    runner = _runner(tmp_path)

    plan = runner._sleep_plan(
        run_dir=tmp_path / "run",
        iteration=1,
        iterations=10,
        deadline=time.monotonic() + 3600,
        sleep_mode="adaptive",
        sleep_seconds=0,
        min_sleep_seconds=None,
        max_sleep_seconds=None,
        sleep_jitter_seconds=None,
        backend_report={"status": "completed", "elapsed_seconds": 120},
    )

    assert plan["seconds"] == 0
    assert plan["reason"] == "no_sleep_budget"


def test_prompt_embeds_problem_independent_attack_doctrine(tmp_path: Path) -> None:
    runner = _runner(tmp_path)
    run_dir = tmp_path / "run"
    run_dir.mkdir()

    prompt = runner._build_prompt(
        run_dir=run_dir,
        iteration=3,
        target="prove the target theorem",
        context_bundle="# Context\n",
    )

    assert "Generic proof-attack doctrine (problem-independent):" in prompt
    assert "dependency graph" in prompt
    assert "Freeze a branch when" in prompt
    assert "Grep hits, prose echoes, and token coincidences are not proof" in prompt
    assert "- Dependency graph delta" in prompt
    assert "- Blocker classification" in prompt
    assert "- Continue / switch / freeze decision" in prompt
    assert "Erdos" not in prompt
