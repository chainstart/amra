from __future__ import annotations

from pathlib import Path
from typing import Any

from ara_math.models import ProblemRecord
from ara_math.problem_bank import (
    DATA_ROOT,
    DEFAULT_BANK_PATH,
    DEFAULT_BANK_REGISTRY_PATH,
    import_erdos_open_problems,
    import_erdos_problem_catalog,
    load_problem_bank,
    save_bank_registry,
    save_problem_bank,
)
from ara_math.workspace import utc_now_iso


def _asset_metadata(*, bank_name: str, formal_math_root: Path, project_dir: str | None = None) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "bank_name": bank_name,
        "statement_quality": "curated",
    }
    if project_dir:
        project_path = formal_math_root / project_dir
        metadata["local_project_dir"] = str(project_path)
        readme_path = project_path / "README.md"
        if readme_path.exists():
            metadata["local_readme_path"] = str(readme_path)
    return metadata


def _amicable_track(formal_math_root: Path) -> list[ProblemRecord]:
    common_metadata = _asset_metadata(bank_name="amicable_track", formal_math_root=formal_math_root, project_dir="amicable-numbers")
    references = [
        "https://en.wikipedia.org/wiki/Amicable_numbers",
        "https://oeis.org/A063990",
        str(formal_math_root / "amicable-numbers" / "README.md"),
    ]
    return [
        ProblemRecord(
            problem_id="amicable-odd-odd",
            title="Odd-Odd Amicable Pair Conjecture",
            source="Classical Number Theory",
            statement="Determine whether there exists an amicable pair in which both numbers are odd.",
            domain="number_theory",
            tags=["amicable_numbers", "parity", "conjecture", "formalization_candidate"],
            open_problem=True,
            formalized="no",
            notes="Open problem highlighted in the local amicable-numbers project. Partial progress should focus on parity, divisor-sum, and coprimality constraints.",
            references=references,
            hypotheses=[
                "A reusable divisor-sum formalization is a prerequisite for any credible attack on the conjecture.",
                "Parity constraints and bounded searches should be packaged as reusable lemmas rather than ad hoc experiments.",
            ],
            recommended_strategy=[
                "Recover the exact historical statement and known impossibility regions.",
                "Formalize divisor-sum and amicable-pair infrastructure in Lean.",
                "Combine parity lemmas with bounded search certificates before attempting any global claim.",
            ],
            metadata=common_metadata,
        ),
        ProblemRecord(
            problem_id="amicable-infinite-pairs",
            title="Infinitely Many Amicable Pairs Conjecture",
            source="Classical Number Theory",
            statement="Determine whether there are infinitely many amicable pairs.",
            domain="number_theory",
            tags=["amicable_numbers", "infinitude", "conjecture"],
            open_problem=True,
            formalized="no",
            notes="This is a long-range open question. The practical route is to formalize known construction families and extract reusable generation lemmas.",
            references=references,
            hypotheses=[
                "Known constructive families should be formalized before searching for new infinite families.",
            ],
            recommended_strategy=[
                "Audit historical construction rules such as Thabit-style families.",
                "Formalize the generation rules and their verified instances.",
                "Separate theorem-formalization progress from any new infinitude claims.",
            ],
            metadata=common_metadata,
        ),
        ProblemRecord(
            problem_id="amicable-coprime-pairs",
            title="No Coprime Amicable Pairs Conjecture",
            source="Classical Number Theory",
            statement="Determine whether there exists an amicable pair whose two members are coprime.",
            domain="number_theory",
            tags=["amicable_numbers", "coprimality", "conjecture", "formalization_candidate"],
            open_problem=True,
            formalized="no",
            notes="The local amicable-numbers notes list this as a natural open conjecture alongside the odd-odd case.",
            references=references,
            hypotheses=[
                "Coprimality constraints can likely be phrased using divisor-sum multiplicativity and gcd lemmas.",
            ],
            recommended_strategy=[
                "Formalize coprimality lemmas for divisor sums.",
                "Search for finite exclusions and structural contradictions.",
                "Record every partial obstruction in the project idea ledger for reuse.",
            ],
            metadata=common_metadata,
        ),
        ProblemRecord(
            problem_id="amicable-prime-exclusion",
            title="Prime Numbers Are Not Amicable",
            source="Classical Number Theory",
            statement="Prove that no prime number is amicable.",
            domain="number_theory",
            tags=["amicable_numbers", "primes", "starter_theorem", "formalization_candidate"],
            open_problem=False,
            formalized="yes",
            notes="Starter theorem for building the amicable-number formalization stack.",
            references=references,
            hypotheses=["The proof should pass through the proper divisor sum of a prime."],
            recommended_strategy=[
                "Use this theorem as a smoke test for the amicable-number Lean library.",
            ],
            metadata=common_metadata,
        ),
    ]


def _triangle_track(formal_math_root: Path) -> list[ProblemRecord]:
    metadata = _asset_metadata(bank_name="triangle_dissection_track", formal_math_root=formal_math_root, project_dir="erdos-634-triangle")
    references = [
        "https://www.erdosproblems.com/634",
        str(formal_math_root / "erdos-634-triangle" / "README.md"),
    ]
    return [
        ProblemRecord(
            problem_id="triangle-dissection-19",
            title="Triangle Dissection into 19 Congruent Triangles",
            source="Erdős Problems",
            statement="Determine whether an equilateral triangle can be dissected into 19 congruent triangles.",
            domain="geometry",
            tags=["geometry", "finite_case", "computational_search", "formalization_candidate"],
            open_problem=True,
            formalized="no",
            notes="The local triangle-dissection project identifies n=19 as the main historically significant target after the n=7 and n=11 impossibility results.",
            references=references,
            hypotheses=[
                "A viable route starts by formalizing known impossibility lemmas before any search for n=19.",
            ],
            recommended_strategy=[
                "Recover Tutte and Beeson arguments as reusable lemmas.",
                "Represent admissible dissection constraints as finite certificates.",
                "Treat any search output as a Lean-checkable certificate rather than a raw script result.",
            ],
            metadata=metadata,
        ),
        ProblemRecord(
            problem_id="triangle-dissection-13",
            title="Triangle Dissection into 13 Congruent Triangles",
            source="Erdős Problems",
            statement="Determine whether an equilateral triangle can be dissected into 13 congruent triangles.",
            domain="geometry",
            tags=["geometry", "finite_case", "computational_search"],
            open_problem=True,
            formalized="no",
            notes="The local notes list n=13 as another open finite case that may be easier than the historically famous n=19 target.",
            references=references,
            hypotheses=["A finite search with strong structural constraints may be more realistic than a general proof attack."],
            recommended_strategy=[
                "Reuse the same constraint language and certificate pipeline as the n=19 case.",
            ],
            metadata=metadata,
        ),
        ProblemRecord(
            problem_id="triangle-dissection-17",
            title="Triangle Dissection into 17 Congruent Triangles",
            source="Erdős Problems",
            statement="Determine whether an equilateral triangle can be dissected into 17 congruent triangles.",
            domain="geometry",
            tags=["geometry", "finite_case", "computational_search"],
            open_problem=True,
            formalized="no",
            notes="Another finite target adjacent to n=19. Useful for benchmarking the finite-certificate pipeline.",
            references=references,
            hypotheses=["The same combinatorial encoding used for n=19 should be portable to n=17."],
            recommended_strategy=[
                "Treat n=17 as a companion finite-case benchmark for the triangle-dissection track.",
            ],
            metadata=metadata,
        ),
    ]


def _weird_track(formal_math_root: Path) -> list[ProblemRecord]:
    metadata = _asset_metadata(bank_name="weird_numbers_track", formal_math_root=formal_math_root, project_dir="erdos-825-weird")
    return [
        ProblemRecord(
            problem_id="erdos-825-weird",
            title="Weird Numbers Abundance Index Conjecture",
            source="Erdős Problems",
            statement="Determine whether every weird number has abundance index C = 3, equivalently whether σ(n)/n < 4 for all weird numbers n.",
            domain="number_theory",
            tags=["weird_numbers", "computational_search", "counterexample_search", "formalization_candidate"],
            open_problem=True,
            formalized="no",
            notes="The local weird-number project already lays out a dual route: exhaustive counterexample search plus structural theorems about weird numbers.",
            references=[
                "https://www.erdosproblems.com/825",
                "https://oeis.org/A006037",
                str(formal_math_root / "erdos-825-weird" / "README.md"),
            ],
            hypotheses=[
                "A bounded counterexample search can generate strong negative evidence quickly.",
                "Formalizing the abundant/semiperfect/weird hierarchy should produce reusable number-theoretic infrastructure.",
            ],
            recommended_strategy=[
                "Audit the exact definition of abundance index from the primary source before proving anything.",
                "Build a Lean library for abundant, semiperfect, and weird numbers.",
                "Treat every search bound as a certificate with explicit assumptions.",
            ],
            metadata=metadata,
        )
    ]


def _unitary_perfect_track(formal_math_root: Path) -> list[ProblemRecord]:
    metadata = _asset_metadata(bank_name="unitary_perfect_track", formal_math_root=formal_math_root, project_dir="erdos-1052-unitary-perfect")
    return [
        ProblemRecord(
            problem_id="erdos-1052",
            title="Finite Number of Unitary Perfect Numbers",
            source="Erdős Problems",
            statement="Determine whether there are only finitely many unitary perfect numbers.",
            domain="number_theory",
            tags=["divisors", "multiplicative_functions", "computational_search", "formalization_candidate"],
            open_problem=True,
            formalized="partial",
            notes="Local formal-math work already covers unitary and bi-unitary divisor theory, which makes this track one of the strongest near-term candidates.",
            references=[
                "https://www.erdosproblems.com/1052",
                "https://oeis.org/A034898",
                str(formal_math_root / "erdos-1052-unitary-perfect" / "README.md"),
                str(formal_math_root / "unitary-biunitary-perfect-lean4" / "README.md"),
            ],
            hypotheses=[
                "The best first milestone is to consolidate existing unitary-divisor lemmas and the nonexistence of odd unitary perfect numbers.",
            ],
            recommended_strategy=[
                "Audit local unitary and bi-unitary formalization assets first.",
                "Separate theorem reuse from any new search over candidate numbers.",
                "Turn every structural theorem into a Lean-verified reusable lemma before attacking finiteness.",
            ],
            metadata=metadata,
        ),
        ProblemRecord(
            problem_id="odd-unitary-perfect-exclusion",
            title="No Odd Unitary Perfect Numbers",
            source="Classical Number Theory",
            statement="Prove that no odd unitary perfect numbers exist.",
            domain="number_theory",
            tags=["divisors", "multiplicative_functions", "starter_theorem", "formalization_candidate"],
            open_problem=False,
            formalized="yes",
            notes="Closed theorem already supported by the local unitary-perfect projects. Useful as a foundation theorem for the full Erdős #1052 track.",
            references=[
                str(formal_math_root / "unitary-biunitary-perfect-lean4" / "README.md"),
                str(formal_math_root / "unitary-perfect-lean4" / "README.md"),
            ],
            hypotheses=["This theorem should be treated as a reusable base lemma, not as a publication target by itself."],
            recommended_strategy=["Use this theorem to validate the divisor-sum formalization stack."],
            metadata=metadata,
        ),
    ]


def _carmichael_track(formal_math_root: Path) -> list[ProblemRecord]:
    metadata = _asset_metadata(bank_name="carmichael_track", formal_math_root=formal_math_root, project_dir="carmichael-numbers")
    return [
        ProblemRecord(
            problem_id="infinitely-many-carmichael",
            title="Infinitely Many Carmichael Numbers",
            source="Classical Number Theory",
            statement="Determine whether there are infinitely many Carmichael numbers.",
            domain="number_theory",
            tags=["carmichael_numbers", "infinitude", "formalization_candidate"],
            open_problem=False,
            formalized="partial",
            notes="Mathematically solved, but the local track treats it as a statement-only north star while focusing on formalizing Korselt's criterion and small examples.",
            references=[
                "https://oeis.org/A002997",
                str(formal_math_root / "carmichael-numbers" / "README.md"),
            ],
            hypotheses=["This should be treated as a long-horizon statement; the practical value lies in formalizing the surrounding infrastructure."],
            recommended_strategy=[
                "Formalize Korselt's criterion first.",
                "Prove small structural theorems before attempting any statement-level discussion of infinitude.",
            ],
            metadata={**metadata, "bank_mode": "mixed_foundation"},
        ),
        ProblemRecord(
            problem_id="korselt-criterion",
            title="Korselt's Criterion for Carmichael Numbers",
            source="Classical Number Theory",
            statement="Prove that a positive integer n is Carmichael iff n is composite, squarefree, and p - 1 divides n - 1 for every prime p dividing n.",
            domain="number_theory",
            tags=["carmichael_numbers", "starter_theorem", "formalization_candidate"],
            open_problem=False,
            formalized="partial",
            notes="Foundation theorem from the local Carmichael project.",
            references=[
                str(formal_math_root / "carmichael-numbers" / "README.md"),
            ],
            hypotheses=["This theorem is a high-value infrastructure result for any Carmichael-number track."],
            recommended_strategy=["Use it as a reusable theorem in the Carmichael library."],
            metadata={**metadata, "bank_mode": "mixed_foundation"},
        ),
    ]


def _build_local_topic_banks(formal_math_root: Path) -> dict[str, dict[str, Any]]:
    return {
        "amicable_track": {
            "description": "Open and foundational amicable-number problems drawn from the local formal-math workspace.",
            "category": "local_topic",
            "provenance": str(formal_math_root / "amicable-numbers"),
            "focus_tags": ["amicable_numbers", "parity", "coprimality", "infinitude"],
            "problems": _amicable_track(formal_math_root),
        },
        "triangle_dissection_track": {
            "description": "Finite-case triangle-dissection targets centered on the Erdős #634 family.",
            "category": "local_topic",
            "provenance": str(formal_math_root / "erdos-634-triangle"),
            "focus_tags": ["geometry", "finite_case", "computational_search"],
            "problems": _triangle_track(formal_math_root),
        },
        "weird_numbers_track": {
            "description": "Weird-number conjectures and search-oriented targets from the local Erdős #825 project.",
            "category": "local_topic",
            "provenance": str(formal_math_root / "erdos-825-weird"),
            "focus_tags": ["weird_numbers", "counterexample_search", "computational_search"],
            "problems": _weird_track(formal_math_root),
        },
        "unitary_perfect_track": {
            "description": "Unitary-perfect-number research track combining Erdős #1052 with local foundation theorems.",
            "category": "local_topic",
            "provenance": str(formal_math_root / "erdos-1052-unitary-perfect"),
            "focus_tags": ["divisors", "multiplicative_functions", "formalization_candidate"],
            "problems": _unitary_perfect_track(formal_math_root),
        },
        "carmichael_track": {
            "description": "Carmichael-number formalization and long-horizon statement bank.",
            "category": "local_topic",
            "provenance": str(formal_math_root / "carmichael-numbers"),
            "focus_tags": ["carmichael_numbers", "starter_theorem"],
            "problems": _carmichael_track(formal_math_root),
        },
    }


def sync_local_problem_banks(
    *,
    formal_math_root: Path | str,
    data_root: Path | str | None = None,
    registry_output: Path | str | None = None,
) -> dict[str, Any]:
    formal_root = Path(formal_math_root)
    target_root = Path(data_root) if data_root else DATA_ROOT
    banks_dir = target_root / "banks"
    banks_dir.mkdir(parents=True, exist_ok=True)

    registry_entries: list[dict[str, Any]] = [
        {
            "name": "curated_starters",
            "path": str(DEFAULT_BANK_PATH),
            "description": "Small curated starter bank bundled with AMRA.",
            "category": "bundled",
            "problem_count": len(load_problem_bank(DEFAULT_BANK_PATH)),
            "provenance": str(DEFAULT_BANK_PATH),
            "focus_tags": ["starter_theorem", "formalization_candidate"],
            "synced_at": utc_now_iso(),
        }
    ]

    erdos_open_path = banks_dir / "erdos_open_637.yaml"
    import_erdos_open_problems(formal_root / "docs" / "open_problems.yaml", erdos_open_path)
    registry_entries.append(
        {
            "name": "erdos_open_637",
            "path": str(erdos_open_path),
            "description": "All open Erdős problems imported from the local formal-math metadata snapshot.",
            "category": "erdos_catalog",
            "problem_count": len(load_problem_bank(erdos_open_path)),
            "provenance": str(formal_root / "docs" / "open_problems.yaml"),
            "focus_tags": ["number theory", "graph theory", "geometry", "ramsey theory"],
            "synced_at": utc_now_iso(),
        }
    )

    erdos_full_path = banks_dir / "erdos_full_1120.yaml"
    import_erdos_problem_catalog(formal_root / "docs" / "problems.yaml", erdos_full_path, open_only=False)
    registry_entries.append(
        {
            "name": "erdos_full_1120",
            "path": str(erdos_full_path),
            "description": "Full Erdős problem catalog with open and non-open entries from the local metadata snapshot.",
            "category": "erdos_catalog",
            "problem_count": len(load_problem_bank(erdos_full_path)),
            "provenance": str(formal_root / "docs" / "problems.yaml"),
            "focus_tags": ["number theory", "graph theory", "geometry", "ramsey theory"],
            "synced_at": utc_now_iso(),
        }
    )

    generated_paths: dict[str, str] = {}
    for name, spec in _build_local_topic_banks(formal_root).items():
        output_path = banks_dir / f"{name}.yaml"
        save_problem_bank(spec["problems"], output_path)
        generated_paths[name] = str(output_path)
        registry_entries.append(
            {
                "name": name,
                "path": str(output_path),
                "description": spec["description"],
                "category": spec["category"],
                "problem_count": len(spec["problems"]),
                "provenance": spec["provenance"],
                "focus_tags": spec["focus_tags"],
                "synced_at": utc_now_iso(),
            }
        )

    registry_path = save_bank_registry(registry_entries, registry_output or DEFAULT_BANK_REGISTRY_PATH)
    return {
        "generated_at": utc_now_iso(),
        "formal_math_root": str(formal_root),
        "registry_path": str(registry_path),
        "bank_count": len(registry_entries),
        "generated_paths": generated_paths,
    }
