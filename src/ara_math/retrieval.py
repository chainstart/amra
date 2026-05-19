"""Deprecated compatibility alias for :mod:`amra.proof.retrieval`."""

from __future__ import annotations

import sys as _sys

from amra.proof import retrieval as _canonical

_sys.modules[__name__] = _canonical
