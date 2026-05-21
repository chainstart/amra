from __future__ import annotations

import json
from pathlib import Path

from amra.cli import main
from amra.discovery import (
    CONJECTURE_MINING_COUNTEREXAMPLES_FILE,
    CONJECTURE_MINING_CONJECTURES_FILE,
    CONJECTURE_MINING_NEGATIVE_RESULTS_FILE,
    CONJECTURE_MINING_NOVELTY_HANDOFF_FILE,
    CONJECTURE_MINING_RUN_FILE,
    run_conjecture_mining_fixture,
)
from amra.research import ConjectureRecord, CounterexampleRecord, NegativeResultRecord, ResearchObjectRecord


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "conjecture_mining_fixture.json"


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_conjecture_mining_persists_records_and_novelty_handoff(tmp_path: Path) -> None:
    output = tmp_path / "discovery"

    payload = run_conjecture_mining_fixture(fixture=FIXTURE, output_dir=output)

    conjectures = _read_json(output / CONJECTURE_MINING_CONJECTURES_FILE)
    counterexamples = _read_json(output / CONJECTURE_MINING_COUNTEREXAMPLES_FILE)
    negative_results = _read_json(output / CONJECTURE_MINING_NEGATIVE_RESULTS_FILE)
    handoff = _read_json(output / CONJECTURE_MINING_NOVELTY_HANDOFF_FILE)

    assert payload["status"] == "succeeded"
    assert payload["counts"] == {
        "conjectures": 1,
        "counterexamples": 1,
        "constructions": 3,
        "negative_results": 1,
    }
    assert isinstance(ResearchObjectRecord.from_dict(conjectures[0]), ConjectureRecord)
    assert isinstance(ResearchObjectRecord.from_dict(counterexamples[0]), CounterexampleRecord)
    assert isinstance(ResearchObjectRecord.from_dict(negative_results[0]), NegativeResultRecord)
    assert conjectures[0]["status"] == "counterexample_found"
    assert counterexamples[0]["assignment"] == {"n": 7}
    assert negative_results[0]["target_object_id"] == "conjecture-sigma-even"
    assert handoff["items"][0]["novelty_status"] == "likely_known"
    assert handoff["items"][0]["recommended_action"] == "record_negative_result"
    assert (output / CONJECTURE_MINING_RUN_FILE).exists()


def test_conjecture_mining_cli_accepts_required_smoke_shape(tmp_path: Path, capsys) -> None:
    output = tmp_path / "cli-discovery"

    exit_code = main(["discovery", "mine-conjectures", "--fixture", str(FIXTURE), "--out", str(output), "--json"])
    printed = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert printed["schema_version"] == "amra.conjecture_mining_run.v1"
    assert printed["counts"]["conjectures"] == 1
    assert printed["counts"]["counterexamples"] == 1
    assert (output / CONJECTURE_MINING_NOVELTY_HANDOFF_FILE).exists()
