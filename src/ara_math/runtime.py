"""Deprecated compatibility alias for :mod:`amra.infra.runtime`."""

from __future__ import annotations

import sys as _sys

from amra.infra import runtime as _canonical

_sys.modules[__name__] = _canonical
