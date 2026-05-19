"""Deprecated compatibility alias for :mod:`amra.review.gates`."""

from __future__ import annotations

import sys as _sys

from amra.review import gates as _canonical

_sys.modules[__name__] = _canonical
