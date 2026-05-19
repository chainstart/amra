"""Deprecated compatibility alias for :mod:`amra.deliverables`."""

from __future__ import annotations

import sys as _sys

from amra import deliverables as _canonical

_sys.modules[__name__] = _canonical
