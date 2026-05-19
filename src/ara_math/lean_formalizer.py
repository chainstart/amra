"""Deprecated compatibility alias for :mod:`amra.lean.formalizer`."""

from __future__ import annotations

import sys as _sys

from amra.lean import formalizer as _canonical

_sys.modules[__name__] = _canonical
