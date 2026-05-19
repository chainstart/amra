"""Deprecated compatibility alias for :mod:`amra.writing`."""

from __future__ import annotations

import sys as _sys

from amra import writing as _canonical

_sys.modules[__name__] = _canonical
