"""Compatibility alias for the legacy math scout implementation.

The canonical portfolio scout package is still being split out. This explicit
facade keeps ``amra.math_scout`` importable without extending the package path
into ``ara_math``.
"""

from __future__ import annotations

import sys as _sys

from ara_math import math_scout as _legacy

_sys.modules[__name__] = _legacy
