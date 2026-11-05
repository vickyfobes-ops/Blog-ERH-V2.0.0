#!/usr/bin/env python3
"""Verify every distributed file against the handoff manifest."""
import hashlib
import json
from pathlib import Path
import sys


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "PACKAGE-MANIFEST.json").read_text(encoding="utf-8"))
    errors = []
    for relative, expected in manifest["files"].items():
        path = (root / relative).resolve()
        if root not in path.parents or not path.is_file():
            errors.append(f"Missing or invalid file: {relative}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(f"Checksum mismatch: {relative}")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: {len(manifest['files'])} files; revision {manifest['packageRevision']}; source {manifest['gitCommit'][:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
