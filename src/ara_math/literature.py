"""Deprecated compatibility alias for :mod:`amra.sources.literature`."""

from __future__ import annotations

import sys as _sys

from amra.sources import literature as _canonical

_sys.modules[__name__] = _canonical
