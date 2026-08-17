#!/usr/bin/env python3
"""Check cross-platform local dependencies used by the Elite Range Hood Skill."""

from __future__ import annotations

import importlib.util
import platform
import sys


def main() -> int:
    missing: list[str] = []
    for module, package in (("PIL", "Pillow"), ("docx", "python-docx")):
        if importlib.util.find_spec(module) is None:
            missing.append(package)

    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {platform.system()} {platform.release()}")
    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10 or newer is required")
        return 1
    if missing:
        print("ERROR: Missing Python packages: " + ", ".join(missing))
        print("Use the bundled Codex workspace dependency runtime when available.")
        return 1
    print("PASS: Pillow and python-docx are available")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
