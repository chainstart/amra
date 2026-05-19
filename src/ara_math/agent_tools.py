"""Deprecated compatibility alias for :mod:`amra.agents.tools`."""

from __future__ import annotations

import sys as _sys

from amra.agents import tools as _canonical

_sys.modules[__name__] = _canonical
