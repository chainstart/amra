"""Deprecated compatibility alias for :mod:`amra.evaluation.scouting`."""

from __future__ import annotations

import sys as _sys

from amra.evaluation import scouting as _canonical

_sys.modules[__name__] = _canonical
