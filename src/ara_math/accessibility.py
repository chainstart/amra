"""Deprecated compatibility alias for :mod:`amra.proof.accessibility`."""

from __future__ import annotations

import sys as _sys

from amra.proof import accessibility as _canonical

_sys.modules[__name__] = _canonical
