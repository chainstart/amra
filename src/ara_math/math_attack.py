"""Deprecated compatibility alias for :mod:`amra.proof.attack`."""

from __future__ import annotations

import sys as _sys

from amra.proof import attack as _canonical

_sys.modules[__name__] = _canonical
