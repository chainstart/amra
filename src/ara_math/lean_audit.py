"""Deprecated compatibility alias for :mod:`amra.lean.audit`."""

from __future__ import annotations

import sys as _sys

from amra.lean import audit as _canonical

_sys.modules[__name__] = _canonical
