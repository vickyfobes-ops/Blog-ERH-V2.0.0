#!/usr/bin/env python3
"""Validate an ERH V2 review, hidden-draft, or publication package."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ALLOWED_TAGS = {"h4", "h5", "p", "ul", "ol", "li", "strong", "em", "a", "img", "blockquote", "br", "hr", "code"}
PRODUCT_STYLE = "color:#000000;text-decoration:underline;"


class ArticleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[str] = []
        self.links: list[dict[str, str]] = []
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
            if key == "style" and not (tag == "a" and value == PRODUCT_STYLE):
                self.errors.append(f"Unapproved inline style on <{tag}>")
        if tag == "a":
            self.links.append(values)
        elif tag == "img":
            self.images.append(values)


def host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")


def is_product(url: str) -> bool:
    parsed = urlparse(url)
    return host(url) == "eliterangehood.com" and parsed.path.startswith("/products/")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, type=Path)
    parser.add_argument("--slug", required=True)
    args = parser.parse_args()
    root = args.dir.expanduser().resolve()
    slug = args.slug
    paths = {
        "markdown": root / f"{slug}.md",
        "meta": root / f"{slug}.meta.json",
        "publish": root / f"{slug}.publish.json",
    }
    errors = [f"Missing {label}: {path}" for label, path in paths.items() if not path.is_file()]
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        return 1

    markdown = paths["markdown"].read_text(encoding="utf-8")
    meta = json.loads(paths["meta"].read_text(encoding="utf-8"))
    publish = json.loads(paths["publish"].read_text(encoding="utf-8"))
    html_name = publish.get("shopifyBodyHtml") or publish.get("bodyHtml") or f"{slug}.shopify.html"
    html_path = root / str(html_name)
    if not html_path.is_file():
        print(f"ERROR: Missing HTML: {html_path}")
        return 1
    body_html = html_path.read_text(encoding="utf-8")
    article = ArticleParser()
    article.feed(body_html)
    errors.extend(article.errors)

    h1 = len(re.findall(r"^#\s+", markdown, flags=re.M))
    h2 = len(re.findall(r"^##\s+", markdown, flags=re.M))
    h3 = len(re.findall(r"^###\s+", markdown, flags=re.M))
    if h1 != 1:
        errors.append(f"Expected one Markdown H1; found {h1}")
    if h2 < 4:
        errors.append(f"Expected at least four Markdown H2 sections; found {h2}")
    if "h1" in article.tags or "h2" in article.tags or "h3" in article.tags:
        errors.append("Shopify body must use only H4/H5 headings under the theme-rendered title")
    if article.tags.count("h4") != h2:
        errors.append("Markdown H2 to Shopify H4 mapping is incomplete")
    if article.tags.count("h5") != h3:
        errors.append("Markdown H3 to Shopify H5 mapping is incomplete")
    if not re.search(r"<h4>Sources and Technical References</h4>", body_html, flags=re.I):
        errors.append("Visible Sources and Technical References section is missing")
    if re.search(r"<(script|style|iframe|figure|figcaption|table)\b|\{[%{]", body_html, flags=re.I):
        errors.append("Unapproved script/style/iframe/figure/table/Liquid content found")
    if body_html.count("AI-generated design visualizations") < 1:
        errors.append("Generated-image disclosure is missing")

    if len(article.images) != 5:
        errors.append(f"Expected five body images; found {len(article.images)}")
    final_state = publish.get("state") in {"ready-for-hidden-shopify-draft", "shopify-hidden-draft-created", "published"}
    for number, image in enumerate(article.images, start=2):
        src = image.get("src", "")
        if final_state and "SHOPIFY_IMAGE_" in src:
            errors.append(f"Body image {number} retains an unresolved placeholder")
        if not final_state and src != f"SHOPIFY_IMAGE_{number}_URL":
            errors.append(f"Unexpected image placeholder at body position {number}")
        if not image.get("alt", "").strip():
            errors.append(f"Body image {number} has no alt text")

    product_links = [link for link in article.links if is_product(link.get("href", ""))]
    distinct_products = sorted({link.get("href", "") for link in product_links})
    if len(distinct_products) < 2:
        errors.append(f"Expected at least two distinct ERH product-detail links; found {len(distinct_products)}")
    for link in product_links:
        if link.get("style") != PRODUCT_STYLE:
            errors.append(f"Product link lacks approved black-underlined style: {link.get('href', '')}")

    if len(meta.get("researchSources", [])) < 2:
        errors.append("Expected at least two authority sources")
    if len(meta.get("backlinkPlan", [])) < 2:
        errors.append("Expected at least two reverse-link tasks")
    seo = meta.get("seo", {})
    seo_title_chars = len(str(seo.get("title", "")))
    meta_description_chars = len(str(seo.get("metaDescription", "")))
    if not 40 <= seo_title_chars <= 65:
        errors.append("SEO title should contain 40–65 characters")
    if not 130 <= meta_description_chars <= 165:
        errors.append("Meta description should contain 130–165 characters")

    if publish.get("storeHandle") != "97256c-fc":
        errors.append("Shopify store handle is not the configured ERH store")
    if publish.get("blog") != "News" or publish.get("blogHandle") != "news":
        errors.append("Target blog must be News/news")
    if publish.get("author") != "YMQ":
        errors.append("Configured author must be YMQ unless explicitly approved otherwise")
    if publish.get("themeTemplate") != "Default blog post":
        errors.append("Theme template must be Default blog post")
    if publish.get("visibility") not in {"hidden", "visible"}:
        errors.append("Visibility must be hidden or visible")
    if publish.get("visibility") == "visible" and publish.get("publishAuthorization") != "审核通过并发布":
        errors.append("Visible publication lacks the exact approval phrase")

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
        "html": html_path.name,
        "state": publish.get("state"),
        "checks": {
            "markdownH1": h1,
            "shopifyH4": article.tags.count("h4"),
            "shopifyH5": article.tags.count("h5"),
            "bodyImages": len(article.images),
            "manifestImages": len(image_manifest),
            "distinctProductLinks": len(distinct_products),
            "styledProductLinks": sum(link.get("style") == PRODUCT_STYLE for link in product_links),
            "authoritySources": len(meta.get("researchSources", [])),
            "backlinkTasks": len(meta.get("backlinkPlan", [])),
            "seoTitleCharacters": seo_title_chars,
            "metaDescriptionCharacters": meta_description_chars,
            "optimizedImageBytes": optimized_bytes,
            "unsafeHtmlFindings": len(article.errors),
        },
        "verifiedProductUrls": distinct_products,
        "errors": errors,
        "shopifyWritePerformed": bool(publish.get("shopifyWritePerformed")),
    }
    report_path = root / f"{slug}.validation.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
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
