"""Deprecated compatibility alias for :mod:`amra.proof.goal_campaign`."""

from __future__ import annotations

import sys as _sys

from amra.proof import goal_campaign as _canonical

_sys.modules[__name__] = _canonical
