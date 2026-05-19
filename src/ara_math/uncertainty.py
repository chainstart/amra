"""Deprecated compatibility alias for :mod:`amra.orchestration.uncertainty`."""

from __future__ import annotations

import sys as _sys

from amra.orchestration import uncertainty as _canonical

_sys.modules[__name__] = _canonical
