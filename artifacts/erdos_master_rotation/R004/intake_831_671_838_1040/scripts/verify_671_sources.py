#!/usr/bin/env python3
"""Verify the #671 public Lean source and the API-only compatibility rewrite.

Usage:
  python3 verify_671_sources.py ORIGINAL.lean COMPAT.lean
"""

import hashlib
import re
import sys
from pathlib import Path


ORIGINAL_SHA256 = "3854ae85aca322b5ad2c65fb9c7bae5ca19ed939ceca99521365d8690b8d8923"
COMPAT_SHA256 = "2da73e90ffcde451b6479f8b63f81e2150c26c40e6e1002e71d2e4b596a045a6"

REPLACEMENTS = {
    "continuous_finsetSum": "continuous_finset_sum",
    "Polynomial.eval_finsetSum": "Polynomial.eval_finset_sum",
    "tendsto_finsetProd": "tendsto_finset_prod",
    "tendsto_finsetSum": "tendsto_finset_sum",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    original_bytes = Path(sys.argv[1]).read_bytes()
    compat_bytes = Path(sys.argv[2]).read_bytes()
    assert sha256(original_bytes) == ORIGINAL_SHA256
    assert sha256(compat_bytes) == COMPAT_SHA256
    original = original_bytes.decode()
    compat = compat_bytes.decode()
    expected = original
    for old, new in REPLACEMENTS.items():
        expected = expected.replace(old, new)
    # The decoded Lean-live source has no terminal newline. `apply_patch`, used
    # for the local compatibility copy, normalised it to exactly one terminal
    # newline. This byte-only normalisation is modelled explicitly.
    assert not original.endswith("\n")
    assert compat.endswith("\n") and not compat.endswith("\n\n")
    expected += "\n"
    assert compat == expected
    forbidden = re.compile(r"(?m)^\s*(?:axiom|opaque)\b|\b(?:sorry|admit|sorryAx)\b")
    assert forbidden.search(original) is None
    assert original.count("continuous_finsetSum") == 2
    assert original.count("Polynomial.eval_finsetSum") == 1
    assert original.count("tendsto_finsetProd") == 3
    assert original.count("tendsto_finsetSum") == 1
    print("ERDOS_671_SOURCE_HASHES_OK")
    print("API_ONLY_COMPATIBILITY_REWRITE_OK replacements=7 terminal_newlines_added=1")
    print("NO_SORRY_ADMIT_AXIOM_OPAQUE_OK")


if __name__ == "__main__":
    main()
