"""Deprecated compatibility alias for :mod:`amra.proof.closure`."""

from __future__ import annotations

import sys as _sys

from amra.proof import closure as _canonical

_sys.modules[__name__] = _canonical
