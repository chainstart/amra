from __future__ import annotations

import os


def pytest_configure() -> None:
    os.environ.setdefault("AMRA_INSTALL_MISSING_MATH_TOOLS", "0")
    os.environ.setdefault("AMRA_RUN_MATH_TOOL_SMOKE", "0")
