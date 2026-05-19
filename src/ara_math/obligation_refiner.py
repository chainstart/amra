"""Deprecated compatibility alias for :mod:`amra.scheduler.obligations`."""

from __future__ import annotations

import sys as _sys

from amra.scheduler import obligations as _canonical

_sys.modules[__name__] = _canonical
