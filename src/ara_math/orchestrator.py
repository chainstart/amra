"""Deprecated compatibility alias for :mod:`amra.orchestrator`."""

from __future__ import annotations

import sys as _sys

from amra import orchestrator as _canonical

_sys.modules[__name__] = _canonical
