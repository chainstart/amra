"""Deprecated compatibility alias for :mod:`amra.orchestration.uncertainty`."""

from __future__ import annotations

import importlib as _importlib
import sys as _sys

_canonical = _importlib.import_module("amra.orchestration.uncertainty")

_sys.modules[__name__] = _canonical
