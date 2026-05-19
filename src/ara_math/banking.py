"""Deprecated compatibility alias for :mod:`amra.problem_banks.sync`."""

from __future__ import annotations

import sys as _sys

from amra.problem_banks import sync as _canonical

_sys.modules[__name__] = _canonical
