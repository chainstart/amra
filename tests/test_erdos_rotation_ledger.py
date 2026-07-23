from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts/manage_erdos_rotation.py"
VERIFY_1056 = (
    REPO_ROOT
    / "artifacts/erdos_master_rotation/R001/verify_1056_k14.py"
)
ANALYSE_327 = (
    REPO_ROOT
    / "artifacts/erdos_master_rotation/R001/analyze_327_near_square_sieve.py"
)
VERIFY_18 = (
    REPO_ROOT
    / "artifacts/erdos_master_rotation/R002/verify_18_small_factorials.py"
)
VERIFY_141 = (
    REPO_ROOT
    / "artifacts/erdos_master_rotation/R002/verify_141_crt_cover.py"
)


def test_builds_complete_rotation_ledger(tmp_path: Path) -> None:
    output_dir = tmp_path / "ledger"
    plan_path = tmp_path / "plan.md"
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--output-dir",
            str(output_dir),
            "--plan-path",
            str(plan_path),
            "build",
            "--cycle",
            "R001",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr

    ledger = json.loads((output_dir / "master_ledger.json").read_text(encoding="utf-8"))
    assert ledger["schema_version"] == "amra.erdos_master_ledger.v1"
    assert len(ledger["problems"]) == 630
    assert len({row["problem_id"] for row in ledger["problems"]}) == 630
    assert ledger["statistics"]["status_counts"]["open"] == 550
    assert [row["problem_id"] for row in ledger["current_queue"]["closure_core"]] == [
        "776",
        "635",
        "809",
        "592",
    ]
    assert [row["problem_id"] for row in ledger["current_queue"]["intake"]] == [
        "1056",
        "327",
    ]
    assert [
        row["cycle_progress"] for row in ledger["current_queue"]["intake"]
    ] == ["completed", "completed"]
    effort = ledger["effort_accounting"]
    assert effort["event_agent_hours"] >= 1.5
    assert effort["combined_known_agent_hours_lower_bound"] == round(
        effort["legacy_campaign_agent_hours_lower_bound"]
        + effort["event_agent_hours"],
        2,
    )
    assert ledger["cycle_history"][0]["cycle_id"] == "R001"
    assert "## 630题紧凑总台账" in plan_path.read_text(encoding="utf-8")


def test_validate_command_passes(tmp_path: Path) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--output-dir",
            str(tmp_path / "ledger"),
            "--plan-path",
            str(tmp_path / "plan.md"),
            "validate",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "PASS: 630 unique problems" in completed.stdout


def test_unforced_cycle_selects_twelve_new_intake_problems(tmp_path: Path) -> None:
    output_dir = tmp_path / "ledger"
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--output-dir",
            str(output_dir),
            "--plan-path",
            str(tmp_path / "plan.md"),
            "build",
            "--cycle",
            "R003",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    ledger = json.loads((output_dir / "master_ledger.json").read_text(encoding="utf-8"))
    intake = ledger["current_queue"]["intake"]
    assert len(intake) == 12
    assert len({row["problem_id"] for row in intake}) == 12
    assert all(row["attempt_count"] == 0 for row in intake)


def test_r002_queue_is_frozen_for_reproducibility(tmp_path: Path) -> None:
    output_dir = tmp_path / "ledger"
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--output-dir",
            str(output_dir),
            "--plan-path",
            str(tmp_path / "plan.md"),
            "build",
            "--cycle",
            "R002",
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    ledger = json.loads((output_dir / "master_ledger.json").read_text(encoding="utf-8"))
    assert [row["problem_id"] for row in ledger["current_queue"]["intake"]] == [
        "18",
        "620",
        "141",
        "598",
        "521",
        "757",
        "536",
        "596",
        "52",
        "949",
        "517",
        "174",
    ]


def test_1056_finite_certificate_is_reproducible(tmp_path: Path) -> None:
    output_path = tmp_path / "1056.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(VERIFY_1056),
            "--output",
            str(output_path),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["passed"] is True
    assert payload["prime_verified_by_trial_division"] is True
    assert payload["endpoint_count"] == 15
    assert payload["interval_count"] == 14
    assert payload["common_factorial_residue"] == 8_978_998


def test_327_sieve_is_independent_on_finite_audit(tmp_path: Path) -> None:
    output_path = tmp_path / "327.json"
    completed = subprocess.run(
        [
            sys.executable,
            str(ANALYSE_327),
            "--limit",
            "5000",
            "--verify-limit",
            "1000",
            "--checkpoints",
            "1000,5000",
            "--output",
            str(output_path),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["passed"] is True
    assert payload["primitive_converse_verified"] is True
    assert payload["finite_edge_implication_verified"] is True
    assert payload["densities"][-1] == {
        "N": 5000,
        "independent_set_size": 2885,
        "density": 0.577,
    }


def test_18_small_factorial_values_are_exactly_reproduced(tmp_path: Path) -> None:
    output_path = tmp_path / "18.json"
    completed = subprocess.run(
        [sys.executable, str(VERIFY_18), "--output", str(output_path)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["passed"] is True
    assert [row["h"] for row in payload["rows"]] == [2, 3, 4, 5, 5, 6, 7, 7]


def test_141_corrected_crt_cover_is_locally_admissible(tmp_path: Path) -> None:
    output_path = tmp_path / "141.json"
    completed = subprocess.run(
        [sys.executable, str(VERIFY_141), "--output", str(output_path)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["passed"] is True
    assert [row["k"] for row in payload["rows"]] == [3, 4]
    assert all(row["gaps_verified"] for row in payload["rows"])
    assert all(row["local_admissibility_verified"] for row in payload["rows"])
