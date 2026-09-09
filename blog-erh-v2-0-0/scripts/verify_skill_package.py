#!/usr/bin/env python3
"""Verify the distributable Blog—ERH—V2.0.0 Skill package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED = (
    "SKILL.md",
    "agents/openai.yaml",
    "assets/elite-range-hood.json",
    "assets/shopify-blog-draft.md",
    "references/brand-facts-and-guardrails.md",
    "references/operator-setup.md",
    "references/security-and-handoff.md",
    "references/shopify-browser-workflow.md",
    "references/shopify-output-contract.md",
    "references/site-config.md",
    "references/v10-output-standard.md",
    "scripts/build_review_docx.py",
    "scripts/build_shopify_bundle.py",
    "scripts/check_runtime.py",
    "scripts/finalize_shopify_images.py",
    "scripts/render_review_docx.py",
    "scripts/validate_blog_package.py",
)

SECRET_PATTERNS = (
    re.compile(r"shpat_[A-Za-z0-9]+"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|password)\s*[:=]\s*['\"][^'\"]+"),
)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []

    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"missing {relative}")

    profile_path = root / "assets/elite-range-hood.json"
    if profile_path.is_file():
        try:
            profile = json.loads(profile_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid profile JSON: {exc}")
        else:
            expected = {
                "schemaVersion": "2.1.0",
                "brand": "Elite Range Hood",
                "publicBrandName": "Elite Range Hood",
                "customerFacingAbbreviationAllowed": False,
                "productionDomain": "eliterangehood.com",
                "shopifyStoreHandle": "97256c-fc",
                "targetBlog": "News",
                "minimumProductLinks": 2,
                "outputStandard": "v10-real-project-linked-word-html",
                "primaryReviewFormat": "english-word-and-shopify-html",
                "linkInsertionStage": "local-review-package",
                "imageCount": 3,
                "bodyImageCount": 2,
                "imageSourcePreference": "approved-real-project-photography",
                "featuredImageAspectRatio": "2:1",
                "featuredImageReferenceWidth": 1774,
                "featuredImageReferenceHeight": 887,
                "bodyImageAspectRatio": "3:2",
                "bodyImageReferenceWidth": 1536,
                "bodyImageReferenceHeight": 1024,
                "bodyImageFixedDimensionsAllowed": False,
                "existingArticleUpdateMode": "update-by-verified-article-id",
                "publicationApprovalPhrase": "审核通过并发布",
            }
            for key, value in expected.items():
                if profile.get(key) != value:
                    errors.append(f"profile {key} must be {value!r}")

    skill_text = (root / "SKILL.md").read_text(encoding="utf-8", errors="ignore")
    for required_text in (
        "chrome:control-chrome",
        "Computer Use",
        "Windows",
        "macOS",
        "审核通过并发布",
        "color:#000000;text-decoration:underline;",
        "exact `2:1` ratio",
        "exact `3:2` ratio",
        "linked English Word review document",
        "Word and HTML must contain the same verified product-link set",
        "never create a second article",
        "Do not publish the abbreviation `ERH`",
    ):
        if required_text not in skill_text:
            errors.append(f"SKILL.md is missing required portable workflow text: {required_text}")

    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() in {
            ".pyc", ".png", ".jpg", ".jpeg", ".webp", ".docx", ".zip"
        }:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"possible secret in {path.relative_to(root)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS: Blog—ERH—V2.0.0 portable package")
    print("Platforms: Windows and macOS")
    print("Browser route: Chrome control; Computer Use fallback")
    print("Store: 97256c-fc / eliterangehood.com")
    print("Target blog: News")
    print("Secrets: none detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
