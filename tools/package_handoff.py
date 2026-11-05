#!/usr/bin/env python3
"""Build a clean, checksummed handoff folder and ZIP from the committed Skill."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile


NAME = "Blog-ERH-V2.0.0"
SKILL = "blog-erh-v2-0-0"
REFERENCE_FILES = (
    "custom-range-hood-buying-guide.shopify.manual-replace-v10.html",
    "custom-range-hood-buying-guide.v10-real-project-images.review.docx",
    "custom-range-hood-buying-guide.images-v10-review.html",
    "images/v10-site-project-outpaint/01-featured-real-project-v10.webp",
    "images/v10-site-project-outpaint/02-proportion-real-project-v10.webp",
    "images/v10-site-project-outpaint/03-craftsmanship-real-project-v10.webp",
    "images/v10-site-project-outpaint/production-notes.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--reference-dir", type=Path, help="Optional approved V10 article folder")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    git = lambda *parts: subprocess.check_output(["git", "-C", str(repo), *parts]).decode("utf-8").strip()
    if git("status", "--porcelain", "--untracked-files=normal"):
        raise ValueError("Commit the release files first; the handoff must match a clean Git commit")
    commit = git("rev-parse", "HEAD")
    release = json.loads((repo / SKILL / "release.json").read_text(encoding="utf-8"))
    release_date = release["packageRevision"].replace(".", "-")
    output = args.output.expanduser().resolve()
    folder = output / NAME
    archive = output / f"{NAME}-portable-{release_date}.zip"
    checksum = archive.with_suffix(".zip.sha256")
    if any(path.exists() for path in (folder, archive, checksum)):
        raise FileExistsError("The target release already exists; choose a new output directory")
    if args.reference_dir:
        for relative in REFERENCE_FILES:
            if not (args.reference_dir / relative).is_file():
                raise FileNotFoundError(f"Missing V10 reference: {relative}")

    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="erh-release-") as temporary:
        stage = Path(temporary) / NAME
        stage.mkdir()
        tracked = git("ls-files", "-z", SKILL, "handoff", "README.md").split("\0")
        for relative in filter(None, tracked):
            path = Path(relative)
            destination = stage / (Path(*path.parts[1:]) if path.parts[0] == "handoff" else path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(repo / path, destination)
        reference_hashes = {}
        if args.reference_dir:
            for relative in REFERENCE_FILES:
                source = args.reference_dir / relative
                destination = stage / "V10参考样例" / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
                reference_hashes[relative] = digest(source)
        (stage / "Install-macOS.command").chmod(0o755)
        # Batch files use CRLF so Explorer/cmd can invoke the extracted file normally.
        batch = stage / "Install-Windows.cmd"
        batch.write_bytes(batch.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8"))
        manifest = {
            "skill": SKILL,
            "packageRevision": release["packageRevision"],
            "gitCommit": commit,
            "repository": release["repository"],
            "outputStandard": release["outputStandard"],
            "originalReferenceSha256": reference_hashes,
            "files": {p.relative_to(stage).as_posix(): digest(p) for p in sorted(stage.rglob("*")) if p.is_file()},
        }
        (stage / "PACKAGE-MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        subprocess.run([sys.executable, str(stage / "verify_package.py")], check=True)
        subprocess.run([sys.executable, str(stage / SKILL / "scripts/verify_skill_package.py")], check=True)
        staged_zip = Path(temporary) / archive.name
        with ZipFile(staged_zip, "w", ZIP_DEFLATED) as bundle:
            for path in sorted(stage.rglob("*")):
                if path.is_file():
                    bundle.write(path, Path(NAME) / path.relative_to(stage))
        shutil.copytree(stage, folder)
        shutil.copyfile(staged_zip, archive)
        if digest(staged_zip) != digest(archive):
            raise OSError("ZIP checksum changed during transfer")
        checksum.write_text(f"{digest(archive)}  {archive.name}\n", encoding="utf-8")
    subprocess.run([sys.executable, str(folder / "verify_package.py")], check=True)
    print(folder)
    print(archive)
    print(checksum)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
