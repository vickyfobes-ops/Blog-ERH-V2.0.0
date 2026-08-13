#!/usr/bin/env python3
"""Validate the reusable structural contract for an ERH Shopify blog package."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ALLOWED_TAGS = {
    "h2", "h3", "p", "ul", "ol", "li", "strong", "em", "a", "figure",
    "img", "figcaption", "blockquote", "table", "thead", "tbody", "tr", "th", "td", "br", "hr", "code",
}


class ArticleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[str] = []
        self.links: list[str] = []
        self.images: list[dict[str, str]] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        values = {key.lower(): value or "" for key, value in attrs}
        self.tags.append(tag)
        if tag not in ALLOWED_TAGS:
            self.errors.append(f"Unsupported tag: <{tag}>")
        for key, value in values.items():
            if key.startswith("on"):
                self.errors.append(f"Inline event handler: {tag}[{key}]")
            if key in {"href", "src"} and value.strip().lower().startswith("javascript:"):
                self.errors.append(f"JavaScript URL: {tag}[{key}]")
        if tag == "a":
            self.links.append(values.get("href", ""))
        elif tag == "img":
            self.images.append(values)


def host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, type=Path)
    parser.add_argument("--slug", required=True)
    args = parser.parse_args()
    root = args.dir.expanduser().resolve()
    slug = args.slug
    paths = {
        "markdown": root / f"{slug}.md",
        "html": root / f"{slug}.shopify.html",
        "meta": root / f"{slug}.meta.json",
        "publish": root / f"{slug}.publish.json",
    }
    errors = [f"Missing {label}: {path}" for label, path in paths.items() if not path.is_file()]
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        return 1

    markdown = paths["markdown"].read_text(encoding="utf-8")
    body_html = paths["html"].read_text(encoding="utf-8")
    meta = json.loads(paths["meta"].read_text(encoding="utf-8"))
    publish = json.loads(paths["publish"].read_text(encoding="utf-8"))
    html_parser = ArticleParser()
    html_parser.feed(body_html)
    errors.extend(html_parser.errors)

    h1_count = len(re.findall(r"^#\s+", markdown, flags=re.M))
    h2_count = len(re.findall(r"^##\s+", markdown, flags=re.M))
    h3_count = len(re.findall(r"^###\s+", markdown, flags=re.M))
    if h1_count != 1:
        errors.append(f"Expected one Markdown H1; found {h1_count}")
    if h2_count < 4:
        errors.append(f"Expected at least four H2 sections; found {h2_count}")
    if "h1" in html_parser.tags:
        errors.append("Shopify body must not contain H1")
    if len(html_parser.images) != 5:
        errors.append(f"Expected five body images; found {len(html_parser.images)}")
    for number, image in enumerate(html_parser.images, start=2):
        if image.get("src") != f"SHOPIFY_IMAGE_{number}_URL":
            errors.append(f"Unexpected image placeholder at body position {number}")
        if not image.get("alt", "").strip():
            errors.append(f"Body image {number} has no alt text")
    if re.search(r"<(script|style|iframe)\b|\{[%{]", body_html, flags=re.I):
        errors.append("Unsafe script/style/iframe/Liquid content found")
    if body_html.count("AI-generated design visualizations") < 1:
        errors.append("Generated-image disclosure is missing")

    internal_links = [url for url in html_parser.links if host(url) == "eliterangehood.com"]
    if len(set(internal_links)) < 3:
        errors.append("Expected at least three distinct ERH internal links")
    if len(meta.get("researchSources", [])) < 2:
        errors.append("Expected at least two authority sources")
    if len(meta.get("backlinkPlan", [])) < 2:
        errors.append("Expected at least two backlink tasks")
    seo = meta.get("seo", {})
    seo_title_chars = len(str(seo.get("title", "")))
    meta_description_chars = len(str(seo.get("metaDescription", "")))
    if not 40 <= seo_title_chars <= 65:
        errors.append("SEO title should contain 40–65 characters")
    if not 130 <= meta_description_chars <= 165:
        errors.append("Meta description should contain 130–165 characters")
    if publish.get("state") != "ready-for-shopify-upload":
        errors.append("Publication manifest is not ready-for-shopify-upload")
    if publish.get("publishAuthorization") != "not granted":
        errors.append("Local package must record that publish authorization is not granted")
    if publish.get("shopifyWritePerformed") is not False:
        errors.append("Local package must record that no Shopify write occurred")

    image_manifest = publish.get("images", [])
    if len(image_manifest) != 6:
        errors.append(f"Expected six manifest images; found {len(image_manifest)}")
    optimized_bytes = 0
    for record in image_manifest:
        path = root / str(record.get("uploadFile", ""))
        if not path.is_file():
            errors.append(f"Missing optimized image: {path}")
            continue
        optimized_bytes += path.stat().st_size
        if path.stat().st_size >= 300_000:
            errors.append(f"Optimized image exceeds 300 KB: {path.name}")

    report = {
        "schemaVersion": "erh-blog-validation-2.0.0",
        "passed": not errors,
        "slug": slug,
        "checks": {
            "markdownH1": h1_count,
            "h2": h2_count,
            "h3": h3_count,
            "bodyImages": len(html_parser.images),
            "manifestImages": len(image_manifest),
            "distinctInternalLinks": len(set(internal_links)),
            "authoritySources": len(meta.get("researchSources", [])),
            "backlinkTasks": len(meta.get("backlinkPlan", [])),
            "seoTitleCharacters": seo_title_chars,
            "metaDescriptionCharacters": meta_description_chars,
            "optimizedImageBytes": optimized_bytes,
            "unsafeHtmlFindings": len(html_parser.errors),
        },
        "errors": errors,
        "shopifyWritePerformed": False,
    }
    report_path = root / f"{slug}.validation.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        print(report_path)
        return 1
    print(f"PASS: {slug}")
    print(json.dumps(report["checks"], indent=2))
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
