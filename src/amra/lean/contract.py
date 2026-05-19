from __future__ import annotations

import re
from typing import Any


_DECL_RE = re.compile(r"^\s*(theorem|lemma)\s+(`[^`]+`|[A-Za-z_][A-Za-z0-9_'.!?]*)\b")
_FENCE_RE = re.compile(r"```(?:lean|lean4)?\s*\n(.*?)```", re.S | re.I)


def _unquote_identifier(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def _declaration_name_matches(actual: str, expected: str | None) -> bool:
    if not expected:
        return True
    actual = _unquote_identifier(actual)
    expected = _unquote_identifier(expected.strip())
    return actual == expected or actual.endswith(f".{expected}")


def _candidate_blocks(text: str) -> list[str]:
    fences = [match.group(1) for match in _FENCE_RE.finditer(text)]
    return fences or [text]


def trim_lean_proof_from_header(text: str) -> str:
    """Return a Lean declaration header without its proof introducer."""

    match = re.search(r"\s*:=\s*(?:by\b)?", text)
    if not match:
        return text.strip()
    return text[: match.start()].rstrip()


def extract_lean_declaration_header(text: str, name: str | None = None) -> dict[str, Any] | None:
    """Extract a theorem/lemma declaration header from Lean or markdown text.

    The extractor is intentionally conservative: it looks for a named Lean
    declaration at line starts, keeps contiguous header lines, and trims any
    proof body. It is meant for source-contract checking, not for full Lean
    parsing.
    """

    for block in _candidate_blocks(text):
        lines = block.splitlines()
        for index, line in enumerate(lines):
            match = _DECL_RE.match(line)
            if not match:
                continue
            declaration_name = _unquote_identifier(match.group(2))
            if not _declaration_name_matches(declaration_name, name):
                continue
            header_lines: list[str] = []
            for current in lines[index : index + 80]:
                if header_lines and _DECL_RE.match(current):
                    break
                if header_lines and not current.strip():
                    break
                header_lines.append(current.rstrip())
                if ":=" in current:
                    break
            header = trim_lean_proof_from_header("\n".join(header_lines))
            if header:
                return {
                    "kind": match.group(1),
                    "name": declaration_name,
                    "header": header,
                    "line": index + 1,
                }
    return None


def normalize_lean_declaration_header(text: str) -> str:
    text = trim_lean_proof_from_header(text)
    text = re.sub(r"/-.*?-/", " ", text, flags=re.S)
    text = re.sub(r"--.*$", " ", text, flags=re.M)
    return re.sub(r"\s+", " ", text).strip()


def compare_lean_declaration_headers(
    *,
    actual_header: str,
    expected_header: str,
    target_theorem: str | None = None,
) -> dict[str, Any]:
    expected = extract_lean_declaration_header(expected_header, target_theorem)
    if expected is None:
        expected = extract_lean_declaration_header(expected_header)
    actual = extract_lean_declaration_header(actual_header, target_theorem)
    if actual is None:
        actual = extract_lean_declaration_header(actual_header)
    expected_text = str((expected or {}).get("header") or expected_header)
    actual_text = str((actual or {}).get("header") or actual_header)
    expected_normalized = normalize_lean_declaration_header(expected_text)
    actual_normalized = normalize_lean_declaration_header(actual_text)
    return {
        "matched": bool(expected_normalized and actual_normalized and expected_normalized == actual_normalized),
        "expected": expected or {},
        "actual": actual or {},
        "expected_normalized": expected_normalized,
        "actual_normalized": actual_normalized,
    }


def render_lean_header_with_sorry(header: str) -> list[str]:
    lines = trim_lean_proof_from_header(header).splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        return []
    lines[-1] = f"{lines[-1]} := by"
    lines.append("  sorry")
    return lines
