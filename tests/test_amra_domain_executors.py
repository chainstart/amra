from __future__ import annotations

from amra.core.models import ProblemRecord
from amra.domain_executors import (
    DOMAIN_EXECUTOR_METADATA_KEY,
    RESULT_SCHEMA_VERSION,
    BoundedAmicableExecutor,
    BoundedCarmichaelExecutor,
    BoundedUnitaryPerfectExecutor,
    DomainSearchRequest,
    SearchBudget,
    TriangleDissectionCertificateExecutor,
    attach_executor_metadata,
    available_executors,
    run_domain_executor,
)


def test_domain_executor_registry_exposes_bounded_deterministic_interfaces() -> None:
    executors = available_executors()

    assert set(executors) == {
        "unitary_perfect.bounded_divisor_scan.v1",
        "amicable.bounded_divisor_sum_scan.v1",
        "triangle_dissection.certificate_stub.v1",
        "carmichael.korselt_scan.v1",
    }
    for executor in executors.values():
        metadata = executor.metadata.to_dict()
        assert metadata["interface_schema"] == "amra.domain_search_executor.v1"
        assert metadata["deterministic"] is True
        assert metadata["bounded"] is True
        assert metadata["default_parameters"]


def test_unitary_perfect_executor_finds_small_known_examples() -> None:
    result = BoundedUnitaryPerfectExecutor().run({"problem_id": "unitary-fixture"}, max_n=100)

    assert result.schema_version == RESULT_SCHEMA_VERSION
    assert result.status == "completed"
    assert result.witnesses == [6, 60, 90]
    assert result.observations[0]["certificate"] == "sigma_star(n) = 2n"
    assert result.candidate_count == 100


def test_amicable_executor_finds_small_amicable_pair() -> None:
    result = BoundedAmicableExecutor().run(
        DomainSearchRequest(problem_id="amicable-fixture", budget=SearchBudget(max_n=300))
    )

    assert result.status == "completed"
    assert [220, 284] in result.witnesses
    assert result.observations[0]["proper_divisor_sum"] == {"220": 284, "284": 220}


def test_carmichael_executor_finds_first_korselt_witness() -> None:
    result = BoundedCarmichaelExecutor().run({"problem_id": "carmichael-fixture"}, max_n=600)

    assert result.status == "completed"
    assert result.witnesses == [561]
    assert result.observations == [
        {
            "n": 561,
            "prime_factors": [3, 11, 17],
            "squarefree": True,
            "korselt_divisibility": {"3": 280, "11": 56, "17": 35},
            "certificate": "composite squarefree and p - 1 divides n - 1 for every p | n",
        }
    ]


def test_triangle_dissection_executor_is_certificate_stub_not_unbounded_search() -> None:
    request = DomainSearchRequest(problem_id="triangle-dissection-fixture", candidates=[1, 4, 19])
    result = TriangleDissectionCertificateExecutor().run(request, max_cases=3)

    assert result.status == "completed"
    assert result.candidate_count == 3
    statuses = {item["triangle_count"]: item["status"] for item in result.observations}
    assert statuses == {
        1: "constructible_by_square_grid",
        4: "constructible_by_square_grid",
        19: "requires_external_certificate",
    }
    assert result.metadata["does_not_enumerate_dissections"] is True


def test_problem_record_metadata_selects_executor_without_running_unbounded_search() -> None:
    problem = ProblemRecord(
        problem_id="korselt-fixture",
        title="Korselt fixture",
        source="unit",
        statement="Check small Carmichael examples.",
        domain="number_theory",
        tags=["carmichael_numbers"],
    )

    enriched = attach_executor_metadata(problem)
    metadata = enriched.metadata[DOMAIN_EXECUTOR_METADATA_KEY][0]
    assert metadata["executor_id"] == "carmichael.korselt_scan.v1"
    assert metadata["bounded"] is True

    result = run_domain_executor(enriched, max_n=600)
    assert result.executor_id == "carmichael.korselt_scan.v1"
    assert result.witnesses == [561]


def test_run_domain_executor_uses_problem_metadata_defaults_with_call_overrides() -> None:
    problem = ProblemRecord(
        problem_id="amicable-bounded-fixture",
        title="Amicable bounded fixture",
        source="unit",
        statement="Check a bounded amicable search.",
        domain="number_theory",
        tags=["amicable_numbers"],
        metadata={
            DOMAIN_EXECUTOR_METADATA_KEY: [
                {
                    "executor_id": "amicable.bounded_divisor_sum_scan.v1",
                    "default_parameters": {"max_n": 100, "pair_parity": "any"},
                }
            ]
        },
    )

    bounded = run_domain_executor(problem)
    assert bounded.parameters["max_n"] == 100
    assert bounded.witnesses == []

    overridden = run_domain_executor(problem, max_n=300)
    assert overridden.parameters["max_n"] == 300
    assert [220, 284] in overridden.witnesses
