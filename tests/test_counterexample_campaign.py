from __future__ import annotations

import json
from pathlib import Path

import yaml

from amra.cli import main
from amra.discovery.counterexample_campaign import (
    COUNTEREXAMPLE_CAMPAIGN_FILE,
    COUNTEREXAMPLE_RESULTS_FILE,
    run_counterexample_campaign,
)


def _problem(
    problem_id: str,
    title: str,
    statement: str,
    *,
    flags: list[str] | None = None,
    statement_quality: str = "detail_page",
) -> dict:
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
            "statement_quality": statement_quality,
            "source_consistency_flags": list(flags or []),
            "erdos_set_member": False,
            "duplicate_of": None,
        },
    }


def test_campaign_runs_bounded_template_and_classifies_unsupported_claims(tmp_path: Path) -> None:
    bank = tmp_path / "bank.yaml"
    output = tmp_path / "campaign"
    bank.write_text(
        yaml.safe_dump(
            [
                _problem(
                    "goldbach",
                    "Goldbach's Conjecture",
                    "Every even integer greater than 2 is the sum of two primes.",
                ),
                _problem(
                    "twins",
                    "Twin Prime Conjecture",
                    "Are there infinitely many primes p for which p + 2 is prime?",
                ),
                _problem(
                    "conflict",
                    "Wrong detail title",
                    "Every integer has property P.",
                    flags=["title_conflict", "statement_conflict"],
                ),
                _problem(
                    "collision",
                    "Index-only collision",
                    "Every finite object has property C.",
                    statement_quality="index_collision_snippet",
                ),
            ],
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    payload = run_counterexample_campaign(
        bank_path=bank,
        output_dir=output,
        resume=True,
        max_integer=100,
    )
    results = [
        json.loads(line)
        for line in (output / COUNTEREXAMPLE_RESULTS_FILE).read_text(encoding="utf-8").splitlines()
    ]

    assert payload["counts"]["result_records"] == 4
    assert payload["counts"]["executed_builtin_searches"] == 1
    assert payload["counts"]["candidate_counterexamples"] == 0
    assert results[0]["status"] == "bounded_search_no_counterexample"
    assert results[0]["search_execution"]["bounds"]["max_even"] == 100
    assert results[1]["status"] == "not_finitely_refutable"
    assert results[2]["status"] == "source_conflict_requires_review"
    assert results[3]["status"] == "statement_recovery_required"

    resumed = run_counterexample_campaign(
        bank_path=bank,
        output_dir=output,
        resume=True,
        max_integer=100,
    )
    assert resumed["counts"]["reused_results"] == 4


def test_counterexample_campaign_cli_smoke(tmp_path: Path, capsys) -> None:
    bank = tmp_path / "bank.yaml"
    output = tmp_path / "cli-campaign"
    bank.write_text(
        yaml.safe_dump(
            [
                _problem(
                    "legendre",
                    "Legendre's Conjecture",
                    "For every positive integer n, there is a prime between n^2 and (n+1)^2.",
                )
            ],
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    exit_code = main(
        [
            "discovery",
            "campaign-counterexamples",
            "--bank",
            str(bank),
            "--out",
            str(output),
            "--max-square-base",
            "30",
            "--json",
        ]
    )
    printed = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert printed["schema_version"] == "amra.counterexample_campaign.v1"
    assert printed["counts"]["executed_builtin_searches"] == 1
    assert (output / COUNTEREXAMPLE_CAMPAIGN_FILE).exists()
