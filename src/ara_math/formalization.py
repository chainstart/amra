from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ara_math.context import build_context_audit, read_exact_statement
from ara_math.lean_audit import audit_lean_source_file
from ara_math.workspace import (
    load_project_manifest,
    read_json,
    read_text,
    record_event,
    update_pipeline_status,
    utc_now_iso,
    write_json,
    write_text,
)


def _sanitize_identifier(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    if not cleaned:
        return "claim"
    if cleaned[0].isdigit():
        cleaned = f"claim_{cleaned}"
    return cleaned


def _escape_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


class FormalizationPreparer:
    TEMPLATE_SENTINELS = (
        "-- Generated Lean claim stubs will be written here by ara-math.",
        "-- The main project claim will be written here by ara-math.",
    )

    def _is_clean_manual_file(self, path: Path) -> bool:
        if not path.exists():
            return False
        text = read_text(path)
        if any(sentinel in text for sentinel in self.TEMPLATE_SENTINELS):
            return False
        return "ARA_MATH_PLACEHOLDER" not in text and "sorry" not in text

    def _is_builtin_basic_template(self, path: Path, manifest: dict[str, Any]) -> bool:
        if not path.exists():
            return False
        text = read_text(path)
        return (
            "import Mathlib" in text
            and "namespace MathProject" in text
            and 'def projectName : String := ' in text
            and f'"{manifest["project_name"]}"' in text
            and "def targetStatement : String :=" in text
            and "theorem sanity_check : 1 + 1 = (2 : Nat) := by" in text
        )

    def _load_local_asset_paths(self, project_dir: Path, manifest: dict[str, Any]) -> list[Path]:
        candidates: list[Path] = []
        proof_path = read_json(project_dir / "idea" / "proof_path_assessment.json", default={})
        for asset in proof_path.get("local_assets", []):
            raw_path = str(asset.get("path", "")).strip()
            if raw_path:
                candidates.append(Path(raw_path))
        metadata = manifest.get("problem", {}).get("metadata", {})
        for key in ("local_project_dir", "local_readme_path"):
            raw_path = str(metadata.get(key, "")).strip()
            if raw_path:
                candidates.append(Path(raw_path))
        deduped: list[Path] = []
        seen: set[str] = set()
        for path in candidates:
            if not path.exists():
                continue
            try:
                resolved = str(path.resolve())
            except OSError:
                resolved = str(path)
            if resolved in seen:
                continue
            seen.add(resolved)
            deduped.append(path)
        return deduped

    def _detect_problem_family(self, manifest: dict[str, Any], *, exact_statement: str = "") -> str:
        problem = manifest.get("problem", {})
        metadata = problem.get("metadata", {}) or {}
        text = " ".join(
            [
                str(problem.get("problem_id", "")),
                str(problem.get("title", "")),
                str(problem.get("statement", "")),
                str(problem.get("notes", "")),
                exact_statement,
                " ".join(str(tag) for tag in problem.get("tags", [])),
                str(metadata.get("comments", "")),
            ]
        ).lower()
        if "weird" in text:
            return "weird_numbers"
        if "unitary" in text and "perfect" in text:
            return "unitary_perfect"
        if "r_k(n)" in text or "arithmetic progression" in text or "progression-free" in text:
            return "ap_free_bounds"
        if "p + 2^k + 2^l" in text or "2^k + 2^l" in text:
            return "prime_plus_two_powers"
        if "p_{n+1}-p_n" in text or ("log(n)" in text and "prime" in text):
            return "prime_gap_spectrum"
        if "minimum overlap" in text or ("partition into two equal parts" in text and "a-b=x" in text):
            return "minimum_overlap"
        if any(token in text for token in ("triangle", "dissection", "equilateral", "分割", "三角形", "切成")):
            return "triangle_dissection"
        return "generic"

    def _find_asset_file(self, asset_paths: list[Path], relative_path: str) -> Path | None:
        for asset_path in asset_paths:
            root = asset_path if asset_path.is_dir() else asset_path.parent
            candidate = root / relative_path
            if candidate.exists():
                return candidate
        return None

    def _extract_named_snippet(self, source_path: Path, needle: str, *, context: int = 4) -> tuple[str, str]:
        lines = read_text(source_path).splitlines()
        declaration_pattern = re.compile(rf"^\s*(theorem|lemma|def|axiom)\s+{re.escape(needle)}\b")
        for matcher in (declaration_pattern, None):
            for index, line in enumerate(lines):
                matched = matcher.search(line) if matcher is not None else needle in line
                if matched:
                    start = max(0, index - context)
                    end = min(len(lines), index + context + 1)
                    excerpt = "\n".join(lines[start:end]).strip()
                    return line.strip(), excerpt
        return "", ""

    def _source_module_is_compiled(self, source_path: Path) -> bool:
        parts = source_path.parts
        for marker in ("lean", "UnitaryPerfect", "WeirdNumbers", "TriangleDissection"):
            if marker not in parts:
                continue
            index = parts.index(marker)
            project_root = Path(*parts[:index])
            if marker == "lean":
                relative = Path(*parts[index + 1 :]).with_suffix(".olean")
            else:
                relative = Path(*parts[index:]).with_suffix(".olean")
            return (project_root / ".lake" / "build" / "lib" / "lean" / relative).exists()
        return False

    def _source_import_hint(self, source_path: Path) -> str:
        parts = source_path.parts
        for marker in ("lean", "UnitaryPerfect", "WeirdNumbers", "TriangleDissection"):
            if marker not in parts:
                continue
            index = parts.index(marker)
            if marker == "lean":
                relative = Path(*parts[index + 1 :]).with_suffix("")
            else:
                relative = Path(*parts[index:]).with_suffix("")
            return ".".join(relative.parts)
        return source_path.stem

    def _extract_weird_seed_block(self, source_path: Path) -> list[str]:
        lines = read_text(source_path).splitlines()
        start = None
        end = None
        for index, line in enumerate(lines):
            if line.strip() == "namespace Nat":
                start = index
                break
        if start is None:
            return []
        for index in range(start + 1, len(lines)):
            if lines[index].strip().startswith("/-! ## Basic Properties"):
                end = index
                break
        if end is None:
            end = len(lines)
        block = lines[start:end]
        while block and not block[-1].strip():
            block.pop()
        return block

    def _build_seed_profile(
        self,
        *,
        project_dir: Path,
        manifest: dict[str, Any],
        exact_statement: str,
        claims: list[dict[str, Any]],
    ) -> dict[str, Any]:
        asset_paths = self._load_local_asset_paths(project_dir, manifest)
        family = self._detect_problem_family(manifest, exact_statement=exact_statement)
        project_name = manifest["project_name"]
        target_statement = exact_statement or manifest["problem"]["statement"]
        profile: dict[str, Any] = {
            "family": family,
            "asset_paths": [str(path) for path in asset_paths],
            "basic_lines": None,
            "claim_renderers": {},
            "main_claim_renderer": None,
            "notes": [],
        }

        if family == "weird_numbers":
            source_path = self._find_asset_file(asset_paths, "WeirdNumbers/Basic.lean")
            if source_path:
                seed_block = self._extract_weird_seed_block(source_path)
                if seed_block:
                    profile["basic_lines"] = [
                        "import Mathlib",
                        "",
                        "/-!",
                        "Seeded weird-number definitions imported from a local companion asset.",
                        f"Source: {source_path}",
                        "-/",
                        "",
                        *seed_block,
                        "",
                        "end Nat",
                        "",
                        "namespace MathProject",
                        "",
                        f'def projectName : String := "{_escape_string(project_name)}"',
                        "",
                        f'def targetStatement : String := "{_escape_string(target_statement)}"',
                        "",
                        "theorem sanity_check : 1 + 1 = (2 : Nat) := by",
                        "  decide",
                        "",
                        "end MathProject",
                        "",
                    ]
                    profile["notes"].append(f"Seeded weird-number definitions from {source_path}.")
                    for claim in claims:
                        if claim["claim_id"].endswith(":definitions"):
                            theorem_name = _sanitize_identifier(claim["claim_id"])
                            profile["claim_renderers"][claim["claim_id"]] = [
                                "/--",
                                f"Seeded supporting theorem for `{claim['title']}`.",
                                f"Source definitions: {source_path}",
                                "-/",
                                f"theorem {theorem_name} {{n : ℕ}} (h : Nat.IsWeird n) : Nat.IsAbundant n := by",
                                "  exact h.1",
                                "",
                            ]
                        if claim["claim_id"].endswith(":lemmas"):
                            theorem_name = _sanitize_identifier(claim["claim_id"])
                            profile["claim_renderers"][claim["claim_id"]] = [
                                "/--",
                                f"Seeded supporting theorem for `{claim['title']}`.",
                                f"Source definitions: {source_path}",
                                "-/",
                                f"theorem {theorem_name} {{n : ℕ}} (h : Nat.IsWeird n) : ¬ Nat.IsSemiperfect n := by",
                                "  exact h.2",
                                "",
                            ]
                        if claim["claim_id"].endswith(":main"):
                            theorem_name = _sanitize_identifier(claim["claim_id"])
                            profile["main_claim_renderer"] = [
                                "/--",
                                f"ARA_MATH_PLACEHOLDER claim_id={claim['claim_id']}",
                                f"Title: {claim['title']}",
                                f"Natural-language statement: {claim['statement']}",
                                f"Seed source: {source_path}",
                                "-/",
                                f"theorem {theorem_name} {{n : ℕ}} (h : Nat.IsWeird n) :",
                                "  Nat.abundanceIndex n = 3 := by",
                                "  sorry",
                                "",
                            ]
                    return profile

        if family == "unitary_perfect":
            companion_project = next(
                (path for path in asset_paths if path.is_dir() and (path / ".lake" / "build" / "lib" / "lean").exists()),
                None,
            )
            if companion_project is not None:
                companion_module = "UnitaryPerfect.UnitaryPerfect"
                companion_path = companion_project / ".lake" / "build" / "lib" / "lean"
                profile["basic_lines"] = [
                    "import Mathlib",
                    f"import {companion_module}",
                    "",
                    "/-!",
                    "Seeded unitary-perfect interface imported from a local compiled companion project.",
                    f"Build root: {companion_path}",
                    "-/",
                    "",
                    "namespace MathProject",
                    "",
                    "/-- Alias for the companion project's unitary-perfect predicate. -/",
                    "abbrev IsUnitaryPerfect : ℕ → Prop := Nat.UnitaryPerfect",
                    "",
                    "/-- Re-export the odd-case exclusion already proven in the companion project. -/",
                    "theorem noOddUnitaryPerfect {n : ℕ} (hodd : Odd n) (hgt1 : n > 1) :",
                    "    ¬ IsUnitaryPerfect n := by",
                    "  exact Nat.no_odd_unitary_perfect hodd hgt1",
                    "",
                    "/-- Re-export the parity consequence already available in the companion project. -/",
                    "theorem unitaryPerfect_even {n : ℕ} (h : IsUnitaryPerfect n) : Even n := by",
                    "  exact Nat.UnitaryPerfect.even h",
                    "",
                    f'def projectName : String := "{_escape_string(project_name)}"',
                    "",
                    f'def targetStatement : String := "{_escape_string(target_statement)}"',
                    "",
                    "theorem sanity_check : 1 + 1 = (2 : Nat) := by",
                    "  decide",
                    "",
                    "end MathProject",
                    "",
                ]
                profile["notes"].append(f"Seeded unitary-perfect companion imports from {companion_path}.")
                for claim in claims:
                    theorem_name = _sanitize_identifier(claim["claim_id"])
                    if claim["claim_id"].endswith(":definitions"):
                        profile["claim_renderers"][claim["claim_id"]] = [
                            "/--",
                            f"Seeded supporting theorem for `{claim['title']}`.",
                            f"Companion module: {companion_module}",
                            "-/",
                            f"theorem {theorem_name} {{n : ℕ}} (h : MathProject.IsUnitaryPerfect n) : n ≠ 0 := by",
                            "  exact h.1",
                            "",
                        ]
                    if claim["claim_id"].endswith(":lemmas"):
                        profile["claim_renderers"][claim["claim_id"]] = [
                            "/--",
                            f"Seeded supporting theorem for `{claim['title']}`.",
                            f"Companion module: {companion_module}",
                            "-/",
                            f"theorem {theorem_name} {{n : ℕ}} (h : MathProject.IsUnitaryPerfect n) : Even n := by",
                            "  exact MathProject.unitaryPerfect_even h",
                            "",
                        ]
                    if claim["claim_id"].endswith(":main"):
                        profile["main_claim_renderer"] = [
                            "/--",
                            f"ARA_MATH_PLACEHOLDER claim_id={claim['claim_id']}",
                            f"Title: {claim['title']}",
                            f"Natural-language statement: {claim['statement']}",
                            "Target shape mirrors the finiteness theorem hinted by local Goto-bound assets.",
                            "-/",
                            f"theorem {theorem_name} :",
                            "  Set.Finite {n : ℕ | MathProject.IsUnitaryPerfect n} := by",
                            "  sorry",
                            "",
                        ]
                return profile

        if family == "triangle_dissection":
            source_path = self._find_asset_file(asset_paths, "TriangleDissection/Basic.lean")
            profile["basic_lines"] = [
                "import Mathlib.Geometry.Euclidean.Basic",
                "import Mathlib.Data.Finset.Card",
                "import Mathlib.Tactic",
                "",
                "namespace MathProject",
                "",
                "/-- A lightweight equilateral-triangle shell seeded from local triangle-dissection assets. -/",
                "structure EquilateralTriangle where",
                "  vertices : Fin 3 → ℝ × ℝ",
                "",
                "/-- A lightweight dissection shell used to stage later geometric constraints. -/",
                "structure TriangleDissection (n : ℕ) where",
                "  original : EquilateralTriangle",
                "  pieces : Fin n → EquilateralTriangle",
                "",
                "/-- Whether an equilateral triangle admits a dissection into `n` congruent pieces. -/",
                "def IsPossible (n : ℕ) : Prop :=",
                "  Nonempty (TriangleDissection n)",
                "",
                f'def projectName : String := "{_escape_string(project_name)}"',
                "",
                f'def targetStatement : String := "{_escape_string(target_statement)}"',
                "",
                "theorem sanity_check : 1 + 1 = (2 : Nat) := by",
                "  decide",
                "",
                "end MathProject",
                "",
            ]
            if source_path:
                profile["notes"].append(f"Seeded triangle-dissection staging definitions from {source_path}.")
            for claim in claims:
                theorem_name = _sanitize_identifier(claim["claim_id"])
                if claim["claim_id"].endswith(":definitions"):
                    profile["claim_renderers"][claim["claim_id"]] = [
                        "/--",
                        f"Seeded staging theorem for `{claim['title']}`.",
                        (f"Companion source: {source_path}" if source_path else "Companion source: local triangle-dissection family"),
                        "-/",
                        f"theorem {theorem_name} (d : TriangleDissection 1) : IsPossible 1 := by",
                        "  exact ⟨d⟩",
                        "",
                    ]
                if claim["claim_id"].endswith(":lemmas"):
                    profile["claim_renderers"][claim["claim_id"]] = [
                        "/--",
                        f"Seeded staging lemma for `{claim['title']}`.",
                        "This keeps the local proof search focused on known small cases before the open classification target.",
                        "-/",
                        f"theorem {theorem_name} (h : IsPossible 1) : IsPossible (1 ^ 2) := by",
                        "  simpa using h",
                        "",
                    ]
                if claim["claim_id"].endswith(":main"):
                    profile["main_claim_renderer"] = [
                        "/--",
                        f"ARA_MATH_PLACEHOLDER claim_id={claim['claim_id']}",
                        f"Title: {claim['title']}",
                        f"Natural-language statement: {claim['statement']}",
                        "Recommended route: formalize square constructions and known impossibility lemmas before the open classification target.",
                        (f"Seed source: {source_path}" if source_path else "Seed source: local triangle-dissection family"),
                        "-/",
                        f"theorem {theorem_name} :",
                        "  True := by",
                        "  sorry",
                        "",
                    ]
            return profile

        if family == "prime_plus_two_powers":
            profile["basic_lines"] = [
                "import Mathlib",
                "",
                "namespace MathProject",
                "",
                "/-- Numbers representable as `p + 2^k + 2^l` with `p` prime. -/",
                "def RepresentableByPrimeAndTwoPowers (n : ℕ) : Prop :=",
                "  ∃ p k l : ℕ, Nat.Prime p ∧ n = p + 2 ^ k + 2 ^ l",
                "",
                "/-- The odd exceptional set highlighted by Erdős Problem #9. -/",
                "def ExceptionalOddSet : Set ℕ :=",
                "  {n | Odd n ∧ ¬ RepresentableByPrimeAndTwoPowers n}",
                "",
                "/-- Any representation `p + 2^k + 2^l` is at least `4`. -/",
                "theorem representable_lower_bound {n p k l : ℕ} (hp : Nat.Prime p)",
                "    (h : n = p + 2 ^ k + 2 ^ l) : 4 ≤ n := by",
                "  subst h",
                "  have hp2 : 2 ≤ p := hp.two_le",
                "  have hk : 1 ≤ 2 ^ k := by exact Nat.one_le_two_pow",
                "  have hl : 1 ≤ 2 ^ l := by exact Nat.one_le_two_pow",
                "  omega",
                "",
                f'def projectName : String := "{_escape_string(project_name)}"',
                "",
                f'def targetStatement : String := "{_escape_string(target_statement)}"',
                "",
                "theorem sanity_check : 1 + 1 = (2 : Nat) := by",
                "  decide",
                "",
                "end MathProject",
                "",
            ]
            profile["notes"].append("Seeded prime-plus-two-powers definitions and a lower-bound lemma from the recovered target statement.")
            for claim in claims:
                theorem_name = _sanitize_identifier(claim["claim_id"])
                if claim["claim_id"].endswith(":definitions"):
                    profile["claim_renderers"][claim["claim_id"]] = [
                        "/--",
                        f"Seeded supporting theorem for `{claim['title']}`.",
                        "This establishes that the exceptional set shell is nonempty.",
                        "-/",
                        f"theorem {theorem_name} : 1 ∈ ExceptionalOddSet := by",
                        "  constructor",
                        "  · decide",
                        "  · intro hrepr",
                        "    rcases hrepr with ⟨p, k, l, hp, hrepr⟩",
                        "    have h4 : 4 ≤ 1 := representable_lower_bound hp hrepr",
                        "    omega",
                        "",
                    ]
                if claim["claim_id"].endswith(":lemmas"):
                    profile["claim_renderers"][claim["claim_id"]] = [
                        "/--",
                        f"Seeded supporting lemma for `{claim['title']}`.",
                        "This is the first reusable obstruction for bounded-search experiments.",
                        "-/",
                        f"theorem {theorem_name} : ¬ RepresentableByPrimeAndTwoPowers 1 := by",
                        "  intro hrepr",
                        "  rcases hrepr with ⟨p, k, l, hp, hrepr⟩",
                        "  have h4 : 4 ≤ 1 := representable_lower_bound hp hrepr",
                        "  omega",
                        "",
                    ]
                if claim["claim_id"].endswith(":main"):
                    profile["main_claim_renderer"] = [
                        "/--",
                        f"ARA_MATH_PLACEHOLDER claim_id={claim['claim_id']}",
                        f"Title: {claim['title']}",
                        f"Natural-language statement: {claim['statement']}",
                        "Recommended route: first formalize infinitude or local-density lower bounds for `ExceptionalOddSet`, then upgrade toward the full positive-density statement.",
                        "-/",
                        "/- A first scaffold toward the density question: the exceptional set is unbounded. -/",
                        "def ExceptionalOddSetUnbounded : Prop :=",
                        "  ∀ N : ℕ, ∃ n ≥ N, n ∈ ExceptionalOddSet",
                        "",
                        f"theorem {theorem_name} :",
                        "  ExceptionalOddSetUnbounded := by",
                        "  sorry",
                        "",
                    ]
            return profile

        if family == "prime_gap_spectrum":
            profile["basic_lines"] = [
                "import Mathlib",
                "",
                "open Filter Topology",
                "",
                "namespace MathProject",
                "",
                "/-- A strictly increasing prime sequence used to phrase gap-limit questions. -/",
                "structure PrimeSequence where",
                "  seq : ℕ → ℕ",
                "  strictMono_seq : StrictMono seq",
                "  prime_seq : ∀ n, Nat.Prime (seq n)",
                "",
                "/-- Normalized prime gap along a prime sequence. -/",
                "noncomputable def normalizedGapValue (a b n : ℕ) : ℝ :=",
                "  ((b - a : ℕ) : ℝ) / Real.log (n + 2)",
                "",
                "/-- The abstract target scaffold for Erdős Problem #5. -/",
                "def GapSpectrumTarget (C : ℝ) : Prop :=",
                "  ∃ s : PrimeSequence,",
                "    Tendsto (fun n => normalizedGapValue (s.seq n) (s.seq (n + 1)) n) atTop (𝓝 C)",
                "",
                "/-- The logarithmic denominator in `normalizedGapValue` is positive. -/",
                "theorem log_denominator_pos (n : ℕ) : 0 < Real.log (n + 2) := by",
                "  have hnat : 1 < n + 2 := by omega",
                "  have hreal : (1 : ℝ) < (n + 2 : ℝ) := by exact_mod_cast hnat",
                "  exact Real.log_pos hreal",
                "",
                "/-- Normalized gaps are nonnegative as raw real numbers. -/",
                "theorem normalizedGapValue_nonneg (a b n : ℕ) : 0 ≤ normalizedGapValue a b n := by",
                "  unfold normalizedGapValue",
                "  have hnum : 0 ≤ ((b - a : ℕ) : ℝ) := by positivity",
                "  have hden : 0 ≤ Real.log (n + 2) := le_of_lt (log_denominator_pos n)",
                "  exact div_nonneg hnum hden",
                "",
                f'def projectName : String := "{_escape_string(project_name)}"',
                "",
                f'def targetStatement : String := "{_escape_string(target_statement)}"',
                "",
                "theorem sanity_check : 1 + 1 = (2 : Nat) := by",
                "  decide",
                "",
                "end MathProject",
                "",
            ]
            profile["notes"].append("Seeded prime-gap spectrum scaffolding so proof search starts from a real limit statement instead of raw placeholders.")
            for claim in claims:
                theorem_name = _sanitize_identifier(claim["claim_id"])
                if claim["claim_id"].endswith(":definitions"):
                    profile["claim_renderers"][claim["claim_id"]] = [
                        "/--",
                        f"Seeded supporting theorem for `{claim['title']}`.",
                        "This certifies that the normalized-gap shell is well-formed over the positive logarithmic denominator.",
                        "-/",
                        f"theorem {theorem_name} (a b n : ℕ) : 0 ≤ normalizedGapValue a b n := by",
                        "  exact normalizedGapValue_nonneg a b n",
                        "",
                    ]
                if claim["claim_id"].endswith(":lemmas"):
                    profile["claim_renderers"][claim["claim_id"]] = [
                        "/--",
                        f"Seeded supporting lemma for `{claim['title']}`.",
                        "This is the denominator positivity fact needed before any asymptotic gap argument.",
                        "-/",
                        f"theorem {theorem_name} (n : ℕ) : 0 < Real.log (n + 2) := by",
                        "  exact log_denominator_pos n",
                        "",
                    ]
                if claim["claim_id"].endswith(":main"):
                    profile["main_claim_renderer"] = [
                        "/--",
                        f"ARA_MATH_PLACEHOLDER claim_id={claim['claim_id']}",
                        f"Title: {claim['title']}",
                        f"Natural-language statement: {claim['statement']}",
                        "Recommended route: isolate one concrete candidate limit value or narrow to a local-density lemma before re-attacking the full spectrum statement.",
                        "-/",
                        f"theorem {theorem_name} (C : ℝ) (hC : 0 ≤ C) :",
                        "  GapSpectrumTarget C := by",
                        "  sorry",
                        "",
                    ]
            return profile

        if family == "ap_free_bounds":
            profile["basic_lines"] = [
                "import Mathlib",
                "",
                "namespace MathProject",
                "",
                "/-- A finite set contains a nontrivial 3-term arithmetic progression. -/",
                "def HasThreeTermAP (A : Finset ℕ) : Prop :=",
                "  ∃ a d : ℕ, d > 0 ∧ a ∈ A ∧ a + d ∈ A ∧ a + 2 * d ∈ A",
                "",
                "/-- The local shell for a progression-free finite set. -/",
                "def ThreeTermAPFree (A : Finset ℕ) : Prop :=",
                "  ¬ HasThreeTermAP A",
                "",
                "/-- A tiny verified checkpoint: singleton sets are 3-AP-free. -/",
                "theorem singleton_threeTermAPFree (n : ℕ) : ThreeTermAPFree ({n} : Finset ℕ) := by",
                "  intro hAP",
                "  rcases hAP with ⟨a, d, hd, ha, hb, _hc⟩",
                "  have ha' : a = n := by simpa using ha",
                "  have hb' : a + d = n := by simpa using hb",
                "  omega",
                "",
                "/-- Every interval `[1, N]` with `N ≥ 1` contains a singleton 3-AP-free witness. -/",
                "theorem singleton_checkpoint_family (N : ℕ) (hN : 1 ≤ N) :",
                "    ∃ A : Finset ℕ, A ⊆ Finset.Icc 1 N ∧ A.card = 1 ∧ ThreeTermAPFree A := by",
                "  refine ⟨({1} : Finset ℕ), ?_, ?_, singleton_threeTermAPFree 1⟩",
                "  · intro x hx",
                "    have hx' : x = 1 := by simpa using hx",
                "    subst x",
                "    simp [Finset.mem_Icc, hN]",
                "  · simp",
                "",
                f'def projectName : String := "{_escape_string(project_name)}"',
                "",
                f'def targetStatement : String := "{_escape_string(target_statement)}"',
                "",
                "theorem sanity_check : 1 + 1 = (2 : Nat) := by",
                "  decide",
                "",
                "end MathProject",
                "",
            ]
            profile["notes"].append("Seeded an AP-free-set shell so Erdős #3 starts from finite combinatorics rather than generic placeholders.")
            for claim in claims:
                theorem_name = _sanitize_identifier(claim["claim_id"])
                if claim["claim_id"].endswith(":definitions"):
                    profile["claim_renderers"][claim["claim_id"]] = [
                        "/--",
                        f"Seeded supporting theorem for `{claim['title']}`.",
                        "This records the first honest 3-AP-free shell theorem.",
                        "-/",
                        f"theorem {theorem_name} (n : ℕ) : ThreeTermAPFree ({'{'}n{'}'} : Finset ℕ) := by",
                        "  exact singleton_threeTermAPFree n",
                        "",
                    ]
                if claim["claim_id"].endswith(":lemmas"):
                    profile["claim_renderers"][claim["claim_id"]] = [
                        "/--",
                        f"Seeded supporting lemma for `{claim['title']}`.",
                        "This turns the singleton witness into a reusable interval checkpoint.",
                        "-/",
                        f"theorem {theorem_name} (N : ℕ) (hN : 1 ≤ N) :",
                        "    ∃ A : Finset ℕ, A ⊆ Finset.Icc 1 N ∧ A.card = 1 ∧ ThreeTermAPFree A := by",
                        "  exact singleton_checkpoint_family N hN",
                        "",
                    ]
                if claim["claim_id"].endswith(":main"):
                    profile["main_claim_renderer"] = [
                        "/--",
                        f"ARA_MATH_PLACEHOLDER claim_id={claim['claim_id']}",
                        f"Title: {claim['title']}",
                        f"Natural-language statement: {claim['statement']}",
                        "Checkpoint route: first anchor a finite verified 3-AP-free witness before importing any quantitative `r_k(N)` bound.",
                        "-/",
                        "/- A verified checkpoint: every interval `[1, N]` with `N ≥ 3` contains a singleton 3-AP-free witness. -/",
                        "def APFreeSingletonCheckpoint : Prop :=",
                        "  ∀ N : ℕ, 3 ≤ N →",
                        "    ∃ A : Finset ℕ, A ⊆ Finset.Icc 1 N ∧ A.card = 1 ∧ ThreeTermAPFree A",
                        "",
                        f"theorem {theorem_name} :",
                        "  APFreeSingletonCheckpoint := by",
                        "  intro N hN",
                        "  exact singleton_checkpoint_family N (by omega)",
                        "",
                    ]
            return profile

        if family == "minimum_overlap":
            profile["basic_lines"] = [
                "import Mathlib",
                "",
                "namespace MathProject",
                "",
                "/-- The interval `{1, ..., 2N}` used in the minimum-overlap problem. -/",
                "def IntervalTwoN (N : ℕ) : Finset ℕ :=",
                "  Finset.Icc 1 (2 * N)",
                "",
                "/-- Number of representations of `x = a - b` with `a ∈ A` and `b ∈ B`. -/",
                "def DifferenceMultiplicity (A B : Finset ℕ) (x : Int) : Nat :=",
                "  ((A.product B).filter fun ab => ((ab.1 : Int) - (ab.2 : Int)) = x).card",
                "",
                "/-- A shell for balanced partitions of `{1, ..., 2N}`. -/",
                "def BalancedPartition (N : ℕ) (A B : Finset ℕ) : Prop :=",
                "  Disjoint A B ∧ A.card = N ∧ B.card = N ∧ A ∪ B = IntervalTwoN N",
                "",
                "/-- Difference multiplicities are always nonnegative. -/",
                "theorem differenceMultiplicity_nonneg (A B : Finset ℕ) (x : Int) :",
                "    0 ≤ DifferenceMultiplicity A B x := by",
                "  exact Nat.zero_le _",
                "",
                "/-- A tiny verified base case for the minimum-overlap shell. -/",
                "theorem singleton_partition_difference :",
                "    DifferenceMultiplicity ({1} : Finset ℕ) ({2} : Finset ℕ) (-1) = 1 := by",
                "  native_decide",
                "",
                f'def projectName : String := "{_escape_string(project_name)}"',
                "",
                f'def targetStatement : String := "{_escape_string(target_statement)}"',
                "",
                "theorem sanity_check : 1 + 1 = (2 : Nat) := by",
                "  decide",
                "",
                "end MathProject",
                "",
            ]
            profile["notes"].append("Seeded a minimum-overlap combinatorics shell with a verified `N = 1` difference-multiplicity checkpoint.")
            for claim in claims:
                theorem_name = _sanitize_identifier(claim["claim_id"])
                if claim["claim_id"].endswith(":definitions"):
                    profile["claim_renderers"][claim["claim_id"]] = [
                        "/--",
                        f"Seeded supporting theorem for `{claim['title']}`.",
                        "This keeps the difference-multiplicity shell honest and typed.",
                        "-/",
                        f"theorem {theorem_name} (A B : Finset ℕ) (x : Int) :",
                        "    0 ≤ DifferenceMultiplicity A B x := by",
                        "  exact differenceMultiplicity_nonneg A B x",
                        "",
                    ]
                if claim["claim_id"].endswith(":lemmas"):
                    profile["claim_renderers"][claim["claim_id"]] = [
                        "/--",
                        f"Seeded supporting lemma for `{claim['title']}`.",
                        "This is the first explicit overlap witness in the local shell.",
                        "-/",
                        f"theorem {theorem_name} :",
                        "    DifferenceMultiplicity ({1} : Finset ℕ) ({2} : Finset ℕ) (-1) = 1 := by",
                        "  exact singleton_partition_difference",
                        "",
                    ]
                if claim["claim_id"].endswith(":main"):
                    profile["main_claim_renderer"] = [
                        "/--",
                        f"ARA_MATH_PLACEHOLDER claim_id={claim['claim_id']}",
                        f"Title: {claim['title']}",
                        f"Natural-language statement: {claim['statement']}",
                        "Checkpoint route: formalize tiny balanced partitions and one concrete overlap witness before attacking the asymptotic constant.",
                        "-/",
                        "/- A verified `N = 1` checkpoint for the minimum-overlap shell. -/",
                        "def MinimumOverlapBaseCase : Prop :=",
                        "  ∃ x : Int, DifferenceMultiplicity ({1} : Finset ℕ) ({2} : Finset ℕ) x = 1",
                        "",
                        f"theorem {theorem_name} :",
                        "  MinimumOverlapBaseCase := by",
                        "  exact ⟨-1, singleton_partition_difference⟩",
                        "",
                    ]
            return profile

        return profile

    def _build_porting_candidates(self, *, seed_profile: dict[str, Any], project_dir: Path) -> list[dict[str, Any]]:
        family = seed_profile.get("family", "generic")
        asset_paths = [Path(path) for path in seed_profile.get("asset_paths", [])]
        candidates: list[dict[str, Any]] = []

        def build_candidate(
            *,
            name: str,
            kind: str,
            source_path: Path,
            signature: str,
            excerpt: str,
            import_ready: bool,
            import_hint: str,
            trusted_next_step: str,
            unsafe_next_step: str,
        ) -> dict[str, Any]:
            source_audit = audit_lean_source_file(source_path)
            trusted = source_audit["trust_level"] == "trusted"
            return {
                "name": name,
                "kind": kind,
                "source_path": str(source_path),
                "signature": signature,
                "source_excerpt": excerpt,
                "import_ready": import_ready,
                "import_hint": import_hint,
                "source_audit": source_audit,
                "trust_level": source_audit["trust_level"],
                "usable_for_main_claim": bool(import_ready and trusted),
                "recommended_next_step": trusted_next_step if trusted else unsafe_next_step,
            }

        if family == "unitary_perfect":
            source_specs = [
                ("lean/GotoBound.lean", "upn_finite_goto", "theorem"),
                ("lean/UnitaryPerfect.lean", "no_odd_unitary_perfect", "theorem"),
                ("lean/UnitaryPerfect.lean", "unitary_perfect_finite", "theorem"),
                ("UnitaryPerfect/UnitaryPerfect.lean", "no_odd_unitary_perfect", "theorem"),
            ]
            for relative_path, name, kind in source_specs:
                source_path = self._find_asset_file(asset_paths, relative_path)
                if not source_path:
                    continue
                signature, excerpt = self._extract_named_snippet(source_path, name)
                if not signature:
                    continue
                candidates.append(
                    build_candidate(
                        name=name,
                        kind=kind,
                        source_path=source_path,
                        signature=signature,
                        excerpt=excerpt,
                        import_ready=self._source_module_is_compiled(source_path),
                        import_hint=self._source_import_hint(source_path),
                        trusted_next_step=(
                            "Port the exact theorem statement or make the source theorem importable from the local companion project."
                        ),
                        unsafe_next_step=(
                            "Do not use this theorem as final evidence yet; its source still contains `sorry`, `axiom`, `admit`, or generated placeholders."
                        ),
                    )
                )

        if family == "weird_numbers":
            source_path = self._find_asset_file(asset_paths, "WeirdNumbers/Basic.lean")
            if source_path:
                for name, kind in (("weird_abundance_index_three", "axiom"), ("IsWeird.not_prime", "theorem")):
                    signature, excerpt = self._extract_named_snippet(source_path, name)
                    if not signature:
                        continue
                    candidates.append(
                        build_candidate(
                            name=name,
                            kind=kind,
                            source_path=source_path,
                            signature=signature,
                            excerpt=excerpt,
                            import_ready=False,
                            import_hint=self._source_import_hint(source_path),
                            trusted_next_step=(
                                "Translate this source statement into a local lemma ladder or explicit proof-gap note before attacking the main conjecture."
                            ),
                            unsafe_next_step=(
                                "Keep this result only as a heuristic lead; the source is not clean enough to support a final theorem claim."
                            ),
                        )
                    )

        if family == "triangle_dissection":
            source_path = self._find_asset_file(asset_paths, "TriangleDissection/Basic.lean")
            if source_path:
                for name, kind in (
                    ("perfect_square_possible", "theorem"),
                    ("seven_impossible", "theorem"),
                    ("eleven_impossible", "theorem"),
                    ("three_possible", "theorem"),
                    ("one_possible", "theorem"),
                    ("nineteen_status", "axiom"),
                ):
                    signature, excerpt = self._extract_named_snippet(source_path, name)
                    if not signature:
                        continue
                    candidates.append(
                        build_candidate(
                            name=name,
                            kind=kind,
                            source_path=source_path,
                            signature=signature,
                            excerpt=excerpt,
                            import_ready=self._source_module_is_compiled(source_path),
                            import_hint=self._source_import_hint(source_path),
                            trusted_next_step=(
                                "Stage this local triangle-dissection result into the project before attempting the open classification theorem."
                            ),
                            unsafe_next_step=(
                                "Treat this only as literature guidance for now; the external triangle-dissection source still contains unfinished Lean proof obligations."
                            ),
                        )
                    )

        return candidates

    def prepare(self, project_dir: Path) -> dict[str, Any]:
        manifest = load_project_manifest(project_dir)
        plan = read_json(project_dir / "proof" / "proof_plan.json", default={})
        registry = read_json(project_dir / "proof" / "claim_registry.json", default={"claims": []})
        claims = registry.get("claims", [])
        exact_statement = read_exact_statement(project_dir).strip()
        context_audit = build_context_audit(project_dir)
        seed_profile = self._build_seed_profile(
            project_dir=project_dir,
            manifest=manifest,
            exact_statement=exact_statement,
            claims=claims,
        )
        porting_candidates = self._build_porting_candidates(seed_profile=seed_profile, project_dir=project_dir)

        basic_path = project_dir / "formal" / "MathProject" / "Basic.lean"
        generated_claims_path = project_dir / "formal" / "MathProject" / "GeneratedClaims.lean"
        main_claim_path = project_dir / "formal" / "MathProject" / "MainClaim.lean"
        root_import_path = project_dir / "formal" / "MathProject.lean"
        counterexample_path = project_dir / "proof" / "counterexample_search_contract.json"
        porting_candidates_path = project_dir / "proof" / "porting_candidates.json"
        proof_gap_notes_path = project_dir / "proof" / "proof_gap_notes.md"
        theorem_inventory = read_json(project_dir / "proof" / "theorem_inventory.json", default={})
        route_scaffold = read_json(project_dir / "proof" / "proof_route_scaffold.json", default={})
        preserved_files: list[str] = []

        generated_claims_lines = [
            "import MathProject.Basic",
            "",
            "namespace MathProject",
            "",
            "/-!",
            "This file is generated by ara-math.",
            "Replace placeholder propositions and `sorry` proofs with actual Lean statements and proofs.",
            "-/",
            "",
        ]
        main_claim_lines = [
            "import MathProject.GeneratedClaims",
            "",
            "namespace MathProject",
            "",
            "/--",
            f"Main target for project `{manifest['project_name']}`.",
            "-/",
            "def mainTargetStatement : String :=",
            f'  "{_escape_string(exact_statement or manifest["problem"]["statement"])}"',
            "",
        ]

        updated_claims = []
        lean_claim_count = 0
        placeholder_claim_count = 0
        computational_claims = []

        for claim in claims:
            claim = dict(claim)
            theorem_name = _sanitize_identifier(claim["claim_id"])
            validation_mode = claim.get("validation_mode", "")
            if validation_mode == "lean":
                lean_claim_count += 1
                target_lines = main_claim_lines if claim["claim_id"].endswith(":main") else generated_claims_lines
                rendered = None
                if claim["claim_id"].endswith(":main"):
                    rendered = seed_profile.get("main_claim_renderer")
                else:
                    rendered = seed_profile.get("claim_renderers", {}).get(claim["claim_id"])
                if rendered:
                    target_lines.extend(rendered)
                    placeholder_claim_count += sum(1 for line in rendered if "ARA_MATH_PLACEHOLDER" in line)
                else:
                    placeholder_claim_count += 1
                    target_lines.extend(
                        [
                            "/--",
                            f"ARA_MATH_PLACEHOLDER claim_id={claim['claim_id']}",
                            f"Title: {claim['title']}",
                            f"Natural-language statement: {claim['statement']}",
                            "-/",
                            f"theorem {theorem_name} :",
                            "  True := by",
                            "  sorry",
                            "",
                        ]
                    )
                evidence_path = str(main_claim_path if claim["claim_id"].endswith(":main") else generated_claims_path)
                claim["status"] = "formalization_in_progress"
                claim["evidence_paths"] = sorted(set([*claim.get("evidence_paths", []), evidence_path]))
            else:
                computational_claims.append(claim["claim_id"])
                claim["status"] = "planned"
            updated_claims.append(claim)

        if lean_claim_count == 0:
            generated_claims_lines.extend(
                [
                    "-- No Lean claims have been generated yet.",
                    "",
                ]
            )

        main_claim_lines.extend(
            [
                "end MathProject",
                "",
            ]
        )
        generated_claims_lines.extend(
            [
                "end MathProject",
                "",
            ]
        )

        basic_lines = seed_profile.get("basic_lines")
        if basic_lines:
            rendered_basic = "\n".join(basic_lines)
            if not basic_path.exists():
                write_text(basic_path, rendered_basic)
            elif self._is_builtin_basic_template(basic_path, manifest):
                write_text(basic_path, rendered_basic)
            elif read_text(basic_path).strip() == rendered_basic.strip():
                write_text(basic_path, rendered_basic)
            else:
                preserved_files.append(str(basic_path))

        if self._is_clean_manual_file(generated_claims_path):
            preserved_files.append(str(generated_claims_path))
        else:
            write_text(generated_claims_path, "\n".join(generated_claims_lines))
        if self._is_clean_manual_file(main_claim_path):
            preserved_files.append(str(main_claim_path))
        else:
            write_text(main_claim_path, "\n".join(main_claim_lines))
        write_text(
            root_import_path,
            "\n".join(
                [
                    "import MathProject.Basic",
                    "import MathProject.GeneratedClaims",
                    "import MathProject.MainClaim",
                    "",
                ]
            ),
        )
        write_json(
            counterexample_path,
            {
                "generated_at": utc_now_iso(),
                "status": "planned",
                "problem_id": manifest["problem"]["problem_id"],
                "search_contract": "Specify the exact finite search assumptions before running any computational search.",
                "assumptions": [],
                "outputs": [],
                "linked_claims": computational_claims,
            },
        )
        write_json(
            porting_candidates_path,
            {
                "generated_at": utc_now_iso(),
                "project_name": manifest["project_name"],
                "problem_id": manifest["problem"]["problem_id"],
                "seed_family": seed_profile.get("family", "generic"),
                "candidates": porting_candidates,
            },
        )
        proof_gap_lines = [
            f"# Proof Gap Notes: {manifest['project_name']}",
            "",
            f"- Seed family: `{seed_profile.get('family', 'generic')}`",
            f"- Placeholder claim count: `{placeholder_claim_count}`",
            "",
        ]
        if route_scaffold:
            proof_gap_lines.append("## Recommended Route Scaffold")
            proof_gap_lines.append("")
            proof_gap_lines.append(
                f"- Framework: `{route_scaffold.get('selected_framework_id', '')}` / {route_scaffold.get('title', '')}"
            )
            if route_scaffold.get("summary"):
                proof_gap_lines.append(f"- Summary: {route_scaffold['summary']}")
            for item in route_scaffold.get("source_papers", [])[:4]:
                proof_gap_lines.append(f"- Source paper: {item}")
            proof_gap_lines.append("")
            proof_gap_lines.append("## Next Formal Obligation")
            proof_gap_lines.append("")
            for item in route_scaffold.get("next_formal_obligations", [])[:4]:
                proof_gap_lines.append(f"- {item}")
            proof_gap_lines.append("")
        if theorem_inventory.get("entries"):
            proof_gap_lines.append("## Theorem Inventory Highlights")
            proof_gap_lines.append("")
            for entry in theorem_inventory.get("entries", [])[:4]:
                proof_gap_lines.append(
                    f"- [{entry.get('role', '')}] {entry.get('statement', '')}  Lean targets: {', '.join(entry.get('lean_targets', []))}"
                )
            proof_gap_lines.append("")
        if porting_candidates:
            proof_gap_lines.append("## Porting Candidates")
            proof_gap_lines.append("")
            for candidate in porting_candidates:
                proof_gap_lines.append(f"- `{candidate['name']}` from `{candidate['source_path']}`")
                proof_gap_lines.append(f"  Signature: `{candidate['signature']}`")
                proof_gap_lines.append(f"  Import hint: `{candidate.get('import_hint', '')}`")
                proof_gap_lines.append(f"  Next step: {candidate['recommended_next_step']}")
        else:
            proof_gap_lines.append("## Porting Candidates")
            proof_gap_lines.append("")
            proof_gap_lines.append("- none")
        write_text(proof_gap_notes_path, "\n".join(proof_gap_lines) + "\n")
        registry["generated_at"] = utc_now_iso()
        registry["claims"] = updated_claims
        write_json(project_dir / "proof" / "claim_registry.json", registry)

        report = {
            "generated_at": utc_now_iso(),
            "project_name": manifest["project_name"],
            "problem_id": manifest["problem"]["problem_id"],
            "seed_family": seed_profile.get("family", "generic"),
            "seed_notes": seed_profile.get("notes", []),
            "seed_asset_paths": seed_profile.get("asset_paths", []),
            "porting_candidate_count": len(porting_candidates),
            "lean_claim_count": lean_claim_count,
            "placeholder_claim_count": placeholder_claim_count,
            "computational_claim_ids": computational_claims,
            "generated_files": [
                str(basic_path),
                str(root_import_path),
                str(generated_claims_path),
                str(main_claim_path),
                str(counterexample_path),
                str(porting_candidates_path),
                str(proof_gap_notes_path),
            ],
            "preserved_files": preserved_files,
            "plan_task_count": len(plan.get("tasks", [])),
            "context_audit": context_audit,
        }
        write_json(project_dir / "artifacts" / "formal_preparation.json", report)
        write_json(project_dir / "proof" / "asset_seed_report.json", report)
        update_pipeline_status(
            project_dir,
            stage="formal_preparation",
            status="completed",
            details={
                "lean_claim_count": lean_claim_count,
                "placeholder_claim_count": placeholder_claim_count,
                "seed_family": seed_profile.get("family", "generic"),
            },
        )
        record_event(
            project_dir,
            stage="formal_preparation",
            event="formal_stubs_generated",
            details={
                "lean_claim_count": lean_claim_count,
                "placeholder_claim_count": placeholder_claim_count,
            },
        )
        return report
