"""Deprecated compatibility alias for :mod:`amra.scheduler.executors`."""

from __future__ import annotations

import sys as _sys

from amra.scheduler import executors as _canonical

_sys.modules[__name__] = _canonical
