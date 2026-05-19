"""Deprecated compatibility alias for :mod:`amra.core.context`."""

from __future__ import annotations

import sys as _sys

from amra.core import context as _canonical

_sys.modules[__name__] = _canonical
