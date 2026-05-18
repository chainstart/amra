"""Legacy compatibility shim for AMRA agent tool registry."""

from __future__ import annotations

from amra.agents.tools import ToolRegistry, ToolSpec

__all__ = ["ToolSpec", "ToolRegistry"]
