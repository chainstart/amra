import json
from pathlib import Path

from ara_math.banking import sync_local_problem_banks
from ara_math.models import ProblemRecord
from ara_math.problem_bank import load_bank_registry, save_problem_bank
from ara_math.scouting import scout_problem_bank


def _write_minimal_formal_math_tree(root: Path) -> None:
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "open_problems.yaml").write_text(
        "\n".join(
            [
                "- number: '1052'",
                "  prize: '$10'",
                "  status:",
                "    state: open",
                "  formalized:",
                "    state: partial",
                "  tags:",
                "    - number theory",
                "    - divisors",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "docs" / "problems.yaml").write_text(
        "\n".join(
            [
                "- number: '1052'",
                "  prize: '$10'",
                "  status:",
                "    state: open",
                "  formalized:",
                "    state: partial",
                "  tags:",
                "    - number theory",
                "    - divisors",
                "- number: '4'",
                "  prize: '$10000'",
                "  status:",
                "    state: proved",
                "  formalized:",
                "    state: yes",
                "  tags:",
                "    - number theory",
                "    - primes",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    for relative in [
        "amicable-numbers/README.md",
        "erdos-634-triangle/README.md",
        "erdos-825-weird/README.md",
        "erdos-1052-unitary-perfect/README.md",
        "unitary-biunitary-perfect-lean4/README.md",
        "carmichael-numbers/README.md",
    ]:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {path.parent.name}\n", encoding="utf-8")


def test_sync_local_problem_banks_creates_registry_and_banks(tmp_path: Path) -> None:
    formal_math_root = tmp_path / "formal-math"
    _write_minimal_formal_math_tree(formal_math_root)

    payload = sync_local_problem_banks(
        formal_math_root=formal_math_root,
        data_root=tmp_path / "data",
        registry_output=tmp_path / "data" / "bank_registry.yaml",
    )

    registry = load_bank_registry(tmp_path / "data" / "bank_registry.yaml")
    names = {entry["name"] for entry in registry}

    assert payload["bank_count"] >= 7
    assert "curated_starters" in names
    assert "erdos_open_637" in names
    assert "amicable_track" in names
    assert (tmp_path / "data" / "banks" / "amicable_track.yaml").exists()


def test_scout_problem_bank_prefers_local_assets_and_search_friendly_tags(tmp_path: Path) -> None:
    formal_math_root = tmp_path / "formal-math"
    readme_path = formal_math_root / "erdos-1052-unitary-perfect" / "README.md"
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    readme_path.write_text(
        "\n".join(
            [
                "# Local asset",
                "",
                "This folder contains Lean code for unitary perfect numbers.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    companion_readme = formal_math_root / "unitary-biunitary-perfect-lean4" / "README.md"
    companion_readme.parent.mkdir(parents=True, exist_ok=True)
    companion_readme.write_text(
        "\n".join(
            [
                "# Companion asset",
                "",
                "1. **Finiteness**: There are finitely many unitary perfect numbers.",
                "This proof uses an explicit bound and a Lean formalization.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    bank_path = tmp_path / "bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="1052",
                title="Erdős Problem #1052",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="number_theory",
                tags=["divisors", "computational_search"],
                open_problem=True,
                formalized="partial",
                references=["https://www.erdosproblems.com/1052"],
            ),
            ProblemRecord(
                problem_id="hard-problem",
                title="Hard Problem",
                source="Synthetic",
                statement="A placeholder statement.",
                domain="analysis",
                tags=["analysis"],
                open_problem=True,
                formalized="no",
                references=[],
            ),
        ],
        bank_path,
    )

    report = scout_problem_bank(
        bank_path=bank_path,
        formal_math_root=formal_math_root,
        top_k=5,
        output_path=tmp_path / "scout.json",
    )

    assert report["top_candidates"][0]["problem_id"] == "1052"
    assert report["shortlist_candidates"][0]["problem_id"] == "1052"
    assert report["top_candidates"][0]["score"] > report["top_candidates"][1]["score"]
    assert report["top_candidates"][0]["local_literature_signal"]["statement_recoverable"] is True
    assert report["top_candidates"][0]["local_literature_signal"]["snapshot_count"] == 2
    assert report["top_candidates"][0]["local_literature_signal"]["evidence_signals"]
    saved = json.loads((tmp_path / "scout.json").read_text(encoding="utf-8"))
    assert saved["global_idea_themes"]


def test_scout_problem_bank_uses_local_erdos_doc_signals_for_related_candidates(tmp_path: Path) -> None:
    formal_math_root = tmp_path / "formal-math"
    triangle_readme = formal_math_root / "erdos-634-triangle" / "README.md"
    triangle_readme.parent.mkdir(parents=True, exist_ok=True)
    triangle_readme.write_text(
        "\n".join(
            [
                "# Triangle dissection notes",
                "",
                "问题 #633 和问题 #634 共享大量几何约束与有限证书思路。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    docs_dir = formal_math_root / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / "simple_problems_analysis.md").write_text(
        "\n".join(
            [
                "# Local focus",
                "",
                "### 问题 #633",
                "这是一个值得持续跟进的几何候选。",
                "",
                "### 问题 #634",
                "同属三角形分割题族。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    bank_path = tmp_path / "bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="633",
                title="Erdős Problem #633",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="geometry",
                tags=["geometry"],
                open_problem=True,
                formalized="no",
                references=["https://www.erdosproblems.com/633"],
                metadata={"source_catalog": "erdosproblems", "prize": "$25", "statement_quality": "placeholder"},
            ),
            ProblemRecord(
                problem_id="271",
                title="Erdős Problem #271",
                source="Erdős Problems",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="combinatorics",
                tags=["additive combinatorics"],
                open_problem=True,
                formalized="no",
                references=["https://www.erdosproblems.com/271"],
                metadata={"source_catalog": "erdosproblems", "prize": "no", "statement_quality": "placeholder"},
            ),
        ],
        bank_path,
    )

    report = scout_problem_bank(
        bank_path=bank_path,
        formal_math_root=formal_math_root,
        top_k=5,
    )

    top_candidate = report["top_candidates"][0]
    assert top_candidate["problem_id"] == "633"
    assert top_candidate["erdos_focus_signal"]["doc_count"] >= 1
    assert top_candidate["erdos_focus_signal"]["related_banks"] == ["triangle_dissection_track"]
    assert report["shortlist_candidates"][0]["problem_id"] == "633"
