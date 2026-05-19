"""Deprecated compatibility alias for :mod:`amra.lean.executor`."""

from __future__ import annotations

import sys as _sys

from amra.lean import executor as _canonical

_sys.modules[__name__] = _canonical
