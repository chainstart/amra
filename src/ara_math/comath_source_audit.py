"""Deprecated compatibility alias for :mod:`amra.sources.source_audit`."""

from __future__ import annotations

import sys as _sys

from amra.sources import source_audit as _canonical

_sys.modules[__name__] = _canonical
