"""Deprecated compatibility alias for :mod:`amra.review.project_review`."""

from __future__ import annotations

import sys as _sys

from amra.review import project_review as _canonical

_sys.modules[__name__] = _canonical
