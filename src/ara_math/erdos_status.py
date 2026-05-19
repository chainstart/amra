"""Deprecated compatibility alias for :mod:`amra.problem_banks.erdos`."""

from __future__ import annotations

import sys as _sys

from amra.problem_banks import erdos as _canonical

_sys.modules[__name__] = _canonical
