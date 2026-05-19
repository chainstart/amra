"""Deprecated compatibility alias for :mod:`amra.math_scout`."""

from __future__ import annotations

import sys as _sys

from amra import math_scout as _canonical

_sys.modules[__name__] = _canonical
