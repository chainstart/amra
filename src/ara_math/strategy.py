"""Deprecated compatibility alias for :mod:`amra.evaluation.strategy`."""

from __future__ import annotations

import sys as _sys

from amra.evaluation import strategy as _canonical

_sys.modules[__name__] = _canonical
