"""Local source-tree shim for the legacy ``ara_math`` package."""

from __future__ import annotations

import sys
from pathlib import Path

_repo_root = Path(__file__).resolve().parents[1]
_src_root = _repo_root / "src"
_src_package = _src_root / "ara_math"

if str(_src_root) not in sys.path:
    sys.path.insert(0, str(_src_root))
if _src_package.exists():
    __path__.append(str(_src_package))  # type: ignore[name-defined]

__version__ = "0.2.0"
