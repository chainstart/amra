"""Deprecated compatibility alias for :mod:`amra.review.project_review`."""

from __future__ import annotations

import importlib as _importlib
import sys as _sys

_canonical = _importlib.import_module("amra.review.project_review")

_sys.modules[__name__] = _canonical
