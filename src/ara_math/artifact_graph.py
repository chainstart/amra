"""Deprecated compatibility alias for :mod:`amra.core.artifact_graph`."""

from __future__ import annotations

import sys as _sys

from amra.core import artifact_graph as _canonical

_sys.modules[__name__] = _canonical
