"""Deprecated compatibility alias for :mod:`amra.proof.proof_system`."""

from __future__ import annotations

import sys as _sys

from amra.proof import proof_system as _canonical

_sys.modules[__name__] = _canonical
