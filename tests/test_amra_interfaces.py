import json
import importlib
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import yaml

from amra.cli import main as amra_main
from amra.core.models import ProblemRecord
from amra.problem_banks.registry import save_problem_bank
from amra.portfolio_campaign import PortfolioCampaignRunner
from amra.portfolio_memory import append_state_transition, load_claim_ledger, upsert_claim


ALLOWED_LEGACY_DISPOSITIONS = {
    "keep-core",
    "move",
    "split",
    "merge",
    "deprecate",
    "shim",
    "delete-later",
}


def test_canonical_and_legacy_cli_metadata_are_declared() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    pyproject = tomllib.loads((repo_root / "pyproject.toml").read_text(encoding="utf-8"))
    scripts = pyproject["project"]["scripts"]

    assert pyproject["project"]["name"] == "amra"
    assert scripts["amra"] == "amra.cli:main"
    assert scripts["ara-math"] == "ara_math.cli:main"
    assert scripts["ara_math"] == "ara_math.cli:main"


def test_research_lab_prefers_amra_and_marks_legacy_cli_deprecated() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    lab = yaml.safe_load((repo_root / "research_lab.yaml").read_text(encoding="utf-8"))
    interfaces = lab["interfaces"]

    assert lab["lab_id"] == "amra"
    assert interfaces["canonical_package"] == "amra"
    assert interfaces["canonical_cli"] == ["python3 -m amra", "amra"]
    assert {"python3 -m ara_math", "ara-math", "ara_math"} <= set(interfaces["compatibility_cli"])
    assert set(interfaces["compatibility_cli"]) <= set(interfaces["deprecated_compatibility_cli"])
    assert lab["commands"]["allow_prefixes"].index("python3 -m amra") < lab["commands"]["allow_prefixes"].index(
        "python3 -m ara_math"
    )


def test_legacy_module_disposition_table_covers_ara_math_files() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    doc_path = repo_root / "docs" / "amra_legacy_module_disposition.zh.md"
    ara_math_dir = repo_root / "src" / "ara_math"
    expected = {path.name for path in ara_math_dir.glob("*.py")}
    rows: dict[str, set[str]] = {}
    duplicates: list[str] = []

    for line in doc_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        match = re.fullmatch(r"`([^`]+\.py)`", cells[0])
        if not match:
            continue

        module_name = match.group(1)
        labels = {
            label.strip()
            for label in cells[3].strip("`").split("+")
            if label.strip()
        }
        if module_name in rows:
            duplicates.append(module_name)
        rows[module_name] = labels

    assert not duplicates
    assert set(rows) == expected
    assert all(rows.values())
    assert all(labels <= ALLOWED_LEGACY_DISPOSITIONS for labels in rows.values())


def test_amra_package_exposes_legacy_modules() -> None:
    import amra.math_scout as math_scout

    assert math_scout.MathScoutRunner is not None


def test_src_amra_package_does_not_tunnel_into_ara_math(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "\n".join(
                [
                    "import importlib.util, json, amra",
                    "spec = importlib.util.find_spec('amra.math_scout')",
                    "import amra.math_scout as math_scout",
                    "print(json.dumps({",
                    "    'legacy_path_tunnel': any(path.endswith('/src/ara_math') for path in amra.__path__),",
                    "    'math_scout_origin': spec.origin,",
                    "    'runner': math_scout.MathScoutRunner.__name__,",
                    "}))",
                ]
            ),
        ],
        cwd=tmp_path,
        env=env,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    payload = json.loads(result.stdout)

    assert payload["legacy_path_tunnel"] is False
    assert Path(payload["math_scout_origin"]) == repo_root / "src" / "amra" / "math_scout.py"
    assert payload["runner"] == "MathScoutRunner"


def test_canonical_core_imports_and_legacy_shims_share_modules() -> None:
    module_pairs = {
        "ara_math.models": "amra.core.models",
        "ara_math.workspace": "amra.core.workspace",
        "ara_math.runtime": "amra.infra.runtime",
        "ara_math.context": "amra.core.context",
        "ara_math.problem_bank": "amra.problem_banks.registry",
        "ara_math.artifact_graph": "amra.core.artifact_graph",
        "ara_math.lean_audit": "amra.lean.audit",
        "ara_math.lean_contract": "amra.lean.contract",
    }

    for legacy_name, canonical_name in module_pairs.items():
        assert importlib.import_module(legacy_name) is importlib.import_module(canonical_name)


def test_uninstalled_checkout_amra_shim_exposes_legacy_modules() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import amra.math_scout; print(amra.math_scout.MathScoutRunner.__name__)",
        ],
        cwd=repo_root,
        env=env,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert result.stdout.strip() == "MathScoutRunner"


def test_amra_portfolio_campaign_cli_writes_scaffold(tmp_path: Path, monkeypatch) -> None:
    bank_path = tmp_path / "bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="easy-exact",
                title="Easy Exact",
                source="test",
                statement="Prove that every even integer greater than two is the sum of two primes.",
                domain="number_theory",
                tags=["number theory"],
                references=["https://example.test/easy"],
            ),
            ProblemRecord(
                problem_id="needs-source",
                title="Needs Source",
                source="test",
                statement="Detailed statement should be imported from the full problem source before theorem work begins.",
                domain="geometry",
                tags=["geometry"],
                metadata={"statement_quality": "placeholder"},
            ),
        ],
        bank_path,
    )
    monkeypatch.setenv("AMRA_REPO_ROOT", str(tmp_path))

    exit_code = amra_main(
        [
            "--json",
            "run-portfolio-campaign",
            "--bank",
            str(bank_path),
            "--run-name",
            "unit portfolio",
            "--scout-limit",
            "2",
            "--promote-top",
            "1",
        ]
    )

    campaign_dir = tmp_path / "artifacts" / "portfolio_campaigns" / "unit-portfolio"
    ranking = json.loads((campaign_dir / "ranking.json").read_text(encoding="utf-8"))

    assert exit_code == 0
    assert ranking["schema_version"] == "amra.ranking.v1"
    assert len(ranking["ranking"]) == 2
    assert (campaign_dir / "final_report.md").exists()


def test_portfolio_memory_problem_state_and_claim_ledger(tmp_path: Path) -> None:
    project = tmp_path / "projects" / "problem-1"

    state = append_state_transition(
        project,
        problem_id="problem-1",
        state="scouted",
        reason="unit test",
        evidence=["probe/report.json"],
    )
    claim = upsert_claim(
        project,
        {
            "claim_id": "problem-1-main",
            "kind": "theorem",
            "statement_nl": "A sample theorem.",
            "status": "hypothesis",
            "dependencies": [],
            "proof_evidence": [],
            "counterexample_evidence": [],
            "reusable": False,
        },
    )
    ledger = load_claim_ledger(project)

    assert state["state"] == "scouted"
    assert claim["claim_id"] == "problem-1-main"
    assert ledger["claims"][0]["status"] == "hypothesis"


def test_evaluate_problem_cli_writes_report(tmp_path: Path) -> None:
    project = tmp_path / "problem-project"
    runner = PortfolioCampaignRunner(repo_root=tmp_path)
    runner.initialize_problem_project(project=project, problem_id="problem-project", state="scouted")

    report = runner.evaluate_problem(project=project, run_name="eval-1")

    assert report["schema_version"] == "amra.difficulty_evaluation.v1"
    assert (project / "runs" / "eval-1" / "difficulty.json").exists()


def test_json_flag_is_accepted_after_subcommand(tmp_path: Path, capsys) -> None:
    bank_path = tmp_path / "bank.yaml"
    save_problem_bank(
        [
            ProblemRecord(
                problem_id="json-flag",
                title="JSON Flag",
                source="test",
                statement="A statement.",
                domain="number_theory",
            )
        ],
        bank_path,
    )

    exit_code = amra_main(["list-problems", "--bank", str(bank_path), "--json"])
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload[0]["problem_id"] == "json-flag"
