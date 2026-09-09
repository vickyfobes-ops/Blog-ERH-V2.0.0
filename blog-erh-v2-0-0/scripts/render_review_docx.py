#!/usr/bin/env python3
"""Render a review DOCX while exposing a macOS CJK font to bundled LibreOffice."""

from __future__ import annotations

import importlib.util
import os
import shutil
import sys
from pathlib import Path


def find_renderer() -> Path:
    explicit = os.environ.get("CODEX_DOCUMENT_RENDERER")
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if path.is_file():
            return path
        raise FileNotFoundError(f"CODEX_DOCUMENT_RENDERER does not exist: {path}")

    root = Path.home() / ".codex" / "plugins" / "cache" / "openai-primary-runtime" / "documents"
    candidates = sorted(
        root.glob("*/skills/documents/render_docx.py"),
        key=lambda path: path.parent.parent.parent.parent.name,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError(
            "The bundled documents renderer was not found. Load the documents workspace dependency first."
        )
    return candidates[0]


def find_macos_cjk_font() -> Path | None:
    candidates = (
        Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
        Path("/System/Library/Fonts/PingFang.ttc"),
        Path("/System/Library/Fonts/STHeiti Medium.ttc"),
    )
    return next((path for path in candidates if path.is_file()), None)


def main() -> int:
    renderer_path = find_renderer()
    spec = importlib.util.spec_from_file_location("codex_render_docx", renderer_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load renderer: {renderer_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if sys.platform == "darwin":
        font_source = find_macos_cjk_font()
        if font_source is not None:
            original_build_env = module._build_lo_env
            dependencies_root = Path(sys.executable).resolve().parents[2]
            bundled_fonts = (
                dependencies_root
                / "native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype"
            )

            def build_env_with_font(user_profile: str) -> dict:
                font_dir = Path(user_profile) / "Library" / "Fonts"
                font_dir.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(font_source, font_dir / font_source.name)
                cache_dir = Path(user_profile) / "fontconfig-cache"
                cache_dir.mkdir(parents=True, exist_ok=True)
                config_path = Path(user_profile) / "fonts.conf"
                font_dirs = [font_dir, Path("/System/Library/Fonts"), Path("/System/Library/Fonts/Supplemental")]
                if bundled_fonts.is_dir():
                    font_dirs.append(bundled_fonts)
                directory_xml = "\n".join(f"  <dir>{path}</dir>" for path in font_dirs)
                config_path.write_text(
                    "<?xml version=\"1.0\"?>\n"
                    "<!DOCTYPE fontconfig SYSTEM \"urn:fontconfig:fonts.dtd\">\n"
                    "<fontconfig>\n"
                    f"{directory_xml}\n"
                    f"  <cachedir>{cache_dir}</cachedir>\n"
                    "  <config><rescan><int>0</int></rescan></config>\n"
                    "</fontconfig>\n",
                    encoding="utf-8",
                )
                env = original_build_env(user_profile)
                env["FONTCONFIG_FILE"] = str(config_path)
                env["FONTCONFIG_PATH"] = str(Path(user_profile))
                env["SAL_FONTPATH"] = str(font_dir)
                return env

            module._build_lo_env = build_env_with_font

    return module.main()


if __name__ == "__main__":
    raise SystemExit(main())
