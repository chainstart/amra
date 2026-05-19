"""Deprecated compatibility alias for :mod:`amra.cli`."""

from __future__ import annotations

import sys as _sys

from amra import cli as _canonical

_sys.modules[__name__] = _canonical
