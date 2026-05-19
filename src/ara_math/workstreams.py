"""Deprecated compatibility alias for :mod:`amra.orchestration.workstreams`."""

from __future__ import annotations

import importlib as _importlib
import sys as _sys

_canonical = _importlib.import_module("amra.orchestration.workstreams")

_sys.modules[__name__] = _canonical
