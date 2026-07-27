from __future__ import annotations

import csv
import json
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
import yaml

from amra.discovery import first_batch_campaign
from amra.discovery.campaign_status import CampaignStatusStore


def _problem(problem_id: str, title: str, statement: str) -> dict:
    return {
        "problem_id": problem_id,
        "title": title,
        "source": "fixture",
        "statement": statement,
        "domain": "number_theory",
        "tags": [],
        "open_problem": True,
        "formalized": "no",
        "metadata": {
            "source_id": problem_id.upper(),
            "source_url": f"https://example.test/{problem_id}",
            "difficulty_level": 1,
            "sets": [],
        },
    }


def _configure_one_problem(monkeypatch, *, max_integer: int = 100) -> dict:
    selected_spec = {
        "problem_id": "goldbach",
        "source_id": "GOLDBACH",
        "title": "Goldbach conjecture",
        "default_bounds": {"max_integer": max_integer},
        "model_contract": "Find an even integer with no two-prime representation.",
    }
    monkeypatch.setattr(
        first_batch_campaign, "BUILTIN_SEARCH_SPECS", (selected_spec,)
    )
    monkeypatch.setattr(first_batch_campaign, "GRAPH_PROBLEM_IDS", ())
    monkeypatch.setattr(
        first_batch_campaign, "FIRST_BATCH_PROBLEM_IDS", ("goldbach",)
    )
    return selected_spec


def _write_one_problem_bank(path: Path) -> None:
    path.write_text(
        yaml.safe_dump(
            [
                _problem(
                    "goldbach",
                    "Goldbach conjecture",
                    "Every even integer greater than 2 is the sum of two primes.",
                )
            ],
            sort_keys=False,
        ),
        encoding="utf-8",
    )


def test_total_table_runs_and_resumes_one_selected_problem(
    tmp_path: Path,
    monkeypatch,
) -> None:
    bank = tmp_path / "bank.yaml"
    campaign = tmp_path / "campaign"
    bank.write_text(
        yaml.safe_dump(
            [
                _problem(
                    "goldbach",
                    "Goldbach conjecture",
                    "Every even integer greater than 2 is the sum of two primes.",
                ),
                _problem("later", "Later problem", "Every integer has property P."),
            ],
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    selected_spec = {
        "problem_id": "goldbach",
        "source_id": "GOLDBACH",
        "title": "Goldbach conjecture",
        "default_bounds": {"max_integer": 100},
        "model_contract": "Find an even integer with no two-prime representation.",
    }
    monkeypatch.setattr(first_batch_campaign, "BUILTIN_SEARCH_SPECS", (selected_spec,))
    monkeypatch.setattr(first_batch_campaign, "GRAPH_PROBLEM_IDS", ())
    monkeypatch.setattr(first_batch_campaign, "FIRST_BATCH_PROBLEM_IDS", ("goldbach",))

    initialized = first_batch_campaign.initialize_status_table(
        bank_path=bank,
        campaign_dir=campaign,
    )
    assert initialized["summary"]["total_problems"] == 2
    assert initialized["summary"]["status_counts"] == {"parked": 1, "queued": 1}

    first = first_batch_campaign.run_first_batch(
        bank_path=bank,
        campaign_dir=campaign,
        max_problems=1,
    )
    assert first["processed_this_run"] == 1
    assert first["summary"]["status_counts"] == {"completed": 1, "parked": 1}

    resumed = first_batch_campaign.run_first_batch(
        bank_path=bank,
        campaign_dir=campaign,
    )
    assert resumed["processed_this_run"] == 0
    store = CampaignStatusStore(campaign / first_batch_campaign.STATUS_DATABASE_FILE)
    status = store.get_problem("goldbach")
    assert status["attempt_count"] == 1
    assert status["last_result"]["outcome"] == "no_counterexample_within_bound"
    assert store.latest_checkpoint("goldbach")["cursor"] == {
        "phase": "search_completed"
    }

    with (campaign / first_batch_campaign.STATUS_CSV_FILE).open(
        encoding="utf-8", newline=""
    ) as handle:
        csv_rows = list(csv.DictReader(handle))
    assert len(csv_rows) == 2
    assert (campaign / first_batch_campaign.STATUS_JSONL_FILE).exists()
    assert "Goldbach conjecture" in (
        campaign / first_batch_campaign.STATUS_MARKDOWN_FILE
    ).read_text(encoding="utf-8")


def test_attempt_artifact_matches_status_result(tmp_path: Path, monkeypatch) -> None:
    bank = tmp_path / "bank.yaml"
    campaign = tmp_path / "campaign"
    bank.write_text(
        yaml.safe_dump(
            [
                _problem(
                    "goldbach",
                    "Goldbach conjecture",
                    "Every even integer greater than 2 is the sum of two primes.",
                )
            ],
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    spec = {
        "problem_id": "goldbach",
        "source_id": "GOLDBACH",
        "title": "Goldbach conjecture",
        "default_bounds": {"max_integer": 50},
        "model_contract": "Find an even integer with no two-prime representation.",
    }
    monkeypatch.setattr(first_batch_campaign, "BUILTIN_SEARCH_SPECS", (spec,))
    monkeypatch.setattr(first_batch_campaign, "GRAPH_PROBLEM_IDS", ())
    monkeypatch.setattr(first_batch_campaign, "FIRST_BATCH_PROBLEM_IDS", ("goldbach",))

    first_batch_campaign.run_first_batch(bank_path=bank, campaign_dir=campaign)
    store = CampaignStatusStore(campaign / first_batch_campaign.STATUS_DATABASE_FILE)
    result = store.get_problem("goldbach")["last_result"]
    artifact = Path(result["attempt_artifact"])
    artifact_payload = json.loads(artifact.read_text(encoding="utf-8"))

    assert artifact_payload["problem_id"] == "goldbach"
    assert artifact_payload["execution"]["bounds"]["max_even"] == 50
    assert artifact_payload["statement_hash"] == store.get_problem("goldbach")[
        "statement_hash"
    ]
    assert artifact_payload["attempt_artifact"] == str(artifact)


def test_changed_config_invalidates_old_checkpoint_and_runs_new_generation(
    tmp_path: Path,
    monkeypatch,
) -> None:
    bank = tmp_path / "bank.yaml"
    campaign = tmp_path / "campaign"
    _write_one_problem_bank(bank)
    _configure_one_problem(monkeypatch, max_integer=50)

    first_batch_campaign.run_first_batch(bank_path=bank, campaign_dir=campaign)
    store = CampaignStatusStore(campaign / first_batch_campaign.STATUS_DATABASE_FILE)
    original = store.get_problem("goldbach")
    original_checkpoint = store.latest_checkpoint("goldbach")
    assert original["metadata"]["search_generation"] == 1

    _configure_one_problem(monkeypatch, max_integer=100)
    first_batch_campaign.initialize_status_table(
        bank_path=bank,
        campaign_dir=campaign,
    )
    invalidated = store.get_problem("goldbach")
    assert invalidated["status"] == "queued"
    assert invalidated["last_result"] is None
    assert invalidated["metadata"]["search_generation"] == 2
    assert original_checkpoint["state"]["search_generation"] == 1

    first_batch_campaign.run_first_batch(bank_path=bank, campaign_dir=campaign)
    refreshed = store.get_problem("goldbach")
    assert refreshed["status"] == "completed"
    assert refreshed["attempt_count"] == 2
    assert refreshed["last_result"]["execution"]["bounds"]["max_even"] == 100
    assert refreshed["last_result"]["search_generation"] == 2
    assert "resumed_from_completed_artifact" not in refreshed["last_result"]


def test_legacy_completed_row_without_identity_is_invalidated(
    tmp_path: Path,
    monkeypatch,
) -> None:
    bank = tmp_path / "bank.yaml"
    campaign = tmp_path / "campaign"
    _write_one_problem_bank(bank)
    _configure_one_problem(monkeypatch)
    first_batch_campaign.run_first_batch(bank_path=bank, campaign_dir=campaign)

    database = campaign / first_batch_campaign.STATUS_DATABASE_FILE
    with sqlite3.connect(database) as connection:
        metadata = json.loads(
            connection.execute(
                "SELECT metadata_json FROM problems WHERE problem_id = 'goldbach'"
            ).fetchone()[0]
        )
        metadata.pop("search_config_fingerprint")
        metadata.pop("search_generation")
        connection.execute(
            "UPDATE problems SET metadata_json = ? WHERE problem_id = 'goldbach'",
            (json.dumps(metadata),),
        )

    first_batch_campaign.initialize_status_table(
        bank_path=bank,
        campaign_dir=campaign,
    )
    row = CampaignStatusStore(database).get_problem("goldbach")
    assert row["status"] == "queued"
    assert row["last_result"] is None
    assert row["metadata"]["search_generation"] == 2


def test_rerun_recovers_expired_lease_before_reset(
    tmp_path: Path,
    monkeypatch,
) -> None:
    bank = tmp_path / "bank.yaml"
    campaign = tmp_path / "campaign"
    _write_one_problem_bank(bank)
    _configure_one_problem(monkeypatch)
    first_batch_campaign.initialize_status_table(
        bank_path=bank,
        campaign_dir=campaign,
    )
    store = CampaignStatusStore(campaign / first_batch_campaign.STATUS_DATABASE_FILE)
    abandoned = store.claim("abandoned-worker", lease_seconds=0.05)
    assert abandoned is not None
    time.sleep(0.1)

    result = first_batch_campaign.run_first_batch(
        bank_path=bank,
        campaign_dir=campaign,
        resume=False,
        max_problems=1,
    )

    assert result["completed_this_run"] == ["goldbach"]
    assert [attempt["status"] for attempt in store.attempts("goldbach")] == [
        "expired",
        "completed",
    ]


def test_heartbeat_renews_short_lease(tmp_path: Path) -> None:
    store = CampaignStatusStore(tmp_path / "status.sqlite3")
    store.upsert_problem("p1", title="P1")
    claim = store.claim("worker", lease_seconds=0.12)
    assert claim is not None

    with first_batch_campaign._lease_heartbeat(
        store,
        problem_id="p1",
        worker_id="worker",
        fencing_token=claim.fencing_token,
        lease_seconds=0.12,
    ) as errors:
        time.sleep(0.3)

    assert errors == []
    completed = store.complete("p1", "worker", claim.fencing_token, result={})
    assert completed["status"] == "completed"


def test_parallel_status_exports_are_consistent(
    tmp_path: Path,
    monkeypatch,
) -> None:
    bank = tmp_path / "bank.yaml"
    campaign = tmp_path / "campaign"
    _write_one_problem_bank(bank)
    _configure_one_problem(monkeypatch)
    first_batch_campaign.initialize_status_table(
        bank_path=bank,
        campaign_dir=campaign,
    )

    with ThreadPoolExecutor(max_workers=4) as executor:
        initializations = list(
            executor.map(
                lambda _: first_batch_campaign.initialize_status_table(
                    bank_path=bank,
                    campaign_dir=campaign,
                ),
                range(8),
            )
        )
    assert all(item["refresh_skipped"] for item in initializations)

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(
            executor.map(
                lambda _: first_batch_campaign.export_status_tables(campaign),
                range(12),
            )
        )

    assert len(results) == 12
    with (campaign / first_batch_campaign.STATUS_CSV_FILE).open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert [row["problem_id"] for row in rows] == ["goldbach"]


def test_deterministic_executor_error_is_parked(
    tmp_path: Path,
    monkeypatch,
) -> None:
    bank = tmp_path / "bank.yaml"
    campaign = tmp_path / "campaign"
    _write_one_problem_bank(bank)
    _configure_one_problem(monkeypatch)

    def fail_search(*args, **kwargs):
        raise ValueError("invalid model")

    monkeypatch.setattr(first_batch_campaign, "_execute_search", fail_search)
    result = first_batch_campaign.run_first_batch(
        bank_path=bank,
        campaign_dir=campaign,
        max_problems=1,
    )

    row = CampaignStatusStore(
        campaign / first_batch_campaign.STATUS_DATABASE_FILE
    ).get_problem("goldbach")
    assert result["failed_this_run"] == ["goldbach"]
    assert row["status"] == "parked"
    assert row["last_error"] == "ValueError: invalid model"


def test_status_query_rejects_missing_campaign_directory(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="status database not found"):
        first_batch_campaign.status_summary(tmp_path / "missing")
