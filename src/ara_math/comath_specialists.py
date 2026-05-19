"""Deprecated compatibility alias for :mod:`amra.evaluation.specialists`."""

from __future__ import annotations

import sys as _sys

from amra.evaluation import specialists as _canonical

_sys.modules[__name__] = _canonical
