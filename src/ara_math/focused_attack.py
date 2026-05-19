"""Deprecated compatibility alias for :mod:`amra.proof.focused_attack`."""

from __future__ import annotations

import sys as _sys

from amra.proof import focused_attack as _canonical

_sys.modules[__name__] = _canonical
