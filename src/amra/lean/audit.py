from __future__ import annotations

import re
from pathlib import Path
from typing import Any


BLOCK_COMMENT_PATTERN = re.compile(r"/-.*?-/", re.DOTALL)
LINE_COMMENT_PATTERN = re.compile(r"--.*?$", re.MULTILINE)
SORRY_PATTERN = re.compile(r"\bsorry\b")
AXIOM_PATTERN = re.compile(r"^\s*axiom\b", re.MULTILINE)
ADMIT_PATTERN = re.compile(r"\badmit\b")
PLACEHOLDER_PATTERN = re.compile(r"ARA_MATH_PLACEHOLDER")


def strip_lean_comments(text: str) -> str:
    without_blocks = BLOCK_COMMENT_PATTERN.sub("", text)
    return LINE_COMMENT_PATTERN.sub("", without_blocks)


def audit_lean_source_text(text: str) -> dict[str, Any]:
    stripped = strip_lean_comments(text)
    sorry_count = len(SORRY_PATTERN.findall(stripped))
    axiom_count = len(AXIOM_PATTERN.findall(stripped))
    admit_count = len(ADMIT_PATTERN.findall(stripped))
    placeholder_count = len(PLACEHOLDER_PATTERN.findall(stripped))
    issue_count = sorry_count + axiom_count + admit_count + placeholder_count
    return {
        "trust_level": "trusted" if issue_count == 0 else "unsafe",
        "issue_count": issue_count,
        "counts": {
            "sorry": sorry_count,
            "axiom": axiom_count,
            "admit": admit_count,
            "placeholder": placeholder_count,
        },
    }


def audit_lean_source_file(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return {
            "trust_level": "missing",
            "issue_count": 0,
            "counts": {"sorry": 0, "axiom": 0, "admit": 0, "placeholder": 0},
        }
    audit = audit_lean_source_text(text)
    return {
        **audit,
        "path": str(path),
    }
