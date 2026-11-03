#!/usr/bin/env python3
"""Install this extracted Skill, retaining any replaced version outside discovery."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from uuid import uuid4


NAME = "blog-erh-v2-0-0"
IGNORE = shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".DS_Store")


def verify(source: Path) -> None:
    subprocess.run(
        [sys.executable, str(source / "scripts" / "verify_skill_package.py")],
        check=True,
    )


def install(source: Path, skills_dir: Path, replace: bool = False) -> tuple[Path, Path | None]:
    source = source.resolve()
    skills_dir = skills_dir.expanduser().resolve()
    target = skills_dir / NAME
    if target.is_symlink():
        raise ValueError(f"Installation target is a symlink; keep it intact: {target}")
    verify(source)
    if source == target:
        return target, None
    if target in source.parents or source in target.parents:
        raise ValueError("Source and target must not contain each other")
    if target.exists() and not target.is_dir():
        raise ValueError(f"Installation target is not a directory: {target}")
    if target.exists() and not replace:
        raise FileExistsError(f"Already installed: {target}. Use --replace to back up and update.")

    skills_dir.mkdir(parents=True, exist_ok=True)
    backup = None
    with tempfile.TemporaryDirectory(prefix=".erh-install-", dir=skills_dir) as staging:
        prepared = Path(staging) / NAME
        shutil.copytree(source, prepared, ignore=IGNORE)
        verify(prepared)
        if target.exists():
            backups = skills_dir.parent / "skill-backups"
            backups.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            backup = backups / f"{NAME}-{stamp}-{uuid4().hex[:8]}"
            target.rename(backup)
        try:
            prepared.rename(target)
        except OSError:
            if backup is not None and not target.exists():
                backup.rename(target)
            raise
    return target, backup


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    codex_root = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    parser.add_argument("--dest", type=Path, default=codex_root / "skills", help="Skills directory")
    parser.add_argument("--replace", action="store_true", help="Back up an existing version before updating")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent.parent
    try:
        target, backup = install(source, args.dest, args.replace)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Installed: {target}")
    if backup is not None:
        print(f"Previous version retained: {backup}")
    print("The Skill is available on your next Codex turn.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
