from __future__ import annotations

from amra.amra_library import (
    AMRA_LIBRARY_ROOT,
    AMRA_MODULE_PREFIX,
    LEGACY_LIBRARY_ROOT,
    LEGACY_MODULE_PREFIX,
    AmraLibraryManager,
    LegacyAraLibraryManager,
)


class AraLibraryManager(LegacyAraLibraryManager):
    """Deprecated compatibility shim for `ara_library` / `AraLibrary`.

    New code should import `amra.amra_library.AmraLibraryManager` and use
    `amra_library` / `AmraLibrary`.
    """


__all__ = [
    "AMRA_LIBRARY_ROOT",
    "AMRA_MODULE_PREFIX",
    "LEGACY_LIBRARY_ROOT",
    "LEGACY_MODULE_PREFIX",
    "AmraLibraryManager",
    "AraLibraryManager",
    "LegacyAraLibraryManager",
]
