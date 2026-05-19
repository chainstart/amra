"""Deprecated compatibility alias for :mod:`amra.proof.search`."""

from __future__ import annotations

import sys as _sys

from amra.proof import search as _canonical

_sys.modules[__name__] = _canonical
