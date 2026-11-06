#!/usr/bin/env python3
"""Compatibility wrapper for running Distort directly from a source checkout.

When imported from the repository root, this file also exposes the ``src/distort``
package path so the legacy filename does not shadow the installable package.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SOURCE_DIR = Path(__file__).resolve().parent / "src"
_PACKAGE_DIR = _SOURCE_DIR / "distort"

if __name__ != "__main__":
    # A root-level distort.py is required for legacy CLI compatibility, but it
    # would normally shadow src/distort during local imports and pytest runs.
    # Giving the shim a package path keeps both compatibility modes working.
    __path__ = [str(_PACKAGE_DIR)]
    __version__ = "0.2.0"

    from distort.mutations import generate_variants, generate_wordlist

    __all__ = ["generate_variants", "generate_wordlist"]


def _main() -> int:
    if str(_SOURCE_DIR) not in sys.path:
        sys.path.insert(0, str(_SOURCE_DIR))

    from distort.cli import main

    return main()


if __name__ == "__main__":
    raise SystemExit(_main())
