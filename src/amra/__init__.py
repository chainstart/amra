"""AMRA canonical package.

AMRA is the public package name for Automated Mathematical Research Agents.
The legacy ``ara_math`` package remains importable during migration.
"""

from __future__ import annotations

from pathlib import Path

__all__ = ["__version__"]

__version__ = "0.2.0"

# During the rename window, let imports such as ``amra.math_scout`` resolve to
# the legacy implementation modules without copying every file at once.
_legacy_package = Path(__file__).resolve().parents[1] / "ara_math"
if _legacy_package.exists():
    __path__.append(str(_legacy_package))  # type: ignore[name-defined]
