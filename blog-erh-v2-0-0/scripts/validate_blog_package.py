#!/usr/bin/env python3
"""Validate an Elite Range Hood V2 review, hidden-draft, or publication package."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

from PIL import Image


ALLOWED_TAGS = {"h4", "h5", "p", "ul", "ol", "li", "strong", "em", "a", "img", "blockquote", "br", "hr", "code"}
PRODUCT_STYLE = "color:#000000;text-decoration:underline;"
FORBIDDEN_PUBLIC_BRAND_ABBREVIATION = re.compile(r"(?<![A-Za-z0-9_-])ERH(?![A-Za-z0-9_-])")
IMAGE_COUNT = 3
BODY_IMAGE_COUNT = 2
FEATURED_WIDTH = 1774
FEATURED_HEIGHT = 887
BODY_WIDTH = 1536
BODY_HEIGHT = 1024
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"


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


def inspect_word(path: Path) -> dict:
    try:
        with ZipFile(path) as archive:
            media = [name for name in archive.namelist() if name.startswith("word/media/")]
            document = ET.fromstring(archive.read("word/document.xml"))
            relationships = ET.fromstring(archive.read("word/_rels/document.xml.rels"))
    except (BadZipFile, KeyError, ET.ParseError) as exc:
        return {"error": f"Unreadable Word document {path.name}: {exc}"}

    hyperlink_urls = []
    for relationship in relationships.findall(f"{{{REL_NS}}}Relationship"):
        if relationship.attrib.get("Type", "").endswith("/hyperlink"):
            hyperlink_urls.append(relationship.attrib.get("Target", ""))
    text = " ".join(
        node.text or "" for node in document.iter(f"{{{WORD_NS}}}t")
    )
    alt_texts = [
        node.attrib.get("descr", "").strip()
        for node in document.iter(f"{{{DRAWING_NS}}}docPr")
    ]
    return {
        "mediaCount": len(media),
        "hyperlinkCount": len(hyperlink_urls),
        "productUrls": sorted({url for url in hyperlink_urls if is_product(url)}),
        "missingImageAlt": sum(not value for value in alt_texts),
        "forbiddenBrandAbbreviation": len(FORBIDDEN_PUBLIC_BRAND_ABBREVIATION.findall(text)),
    }


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
        "word": root / f"{slug}.review.docx",
        "chineseWord": root / f"{slug}.zh-CN.review.docx",
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
    image_source_type = str(publish.get("imageSourceType", ""))
    allowed_image_source_types = {
        "approved-real-project-photography",
        "mixed-approved-and-generated",
        "ai-generated-design-visualizations",
    }
    if image_source_type not in allowed_image_source_types:
        errors.append("Publication manifest has an invalid or missing imageSourceType")
    if "generated" in image_source_type.lower() and not re.search(
        r"AI-generated design visualization", body_html, flags=re.I
    ):
        errors.append("Generated-image disclosure is missing")

    if len(article.images) != BODY_IMAGE_COUNT:
        errors.append(f"Expected two body images; found {len(article.images)}")
    final_state = publish.get("state") in {"ready-for-hidden-shopify-draft", "shopify-hidden-draft-created", "published"}
    for number, image in enumerate(article.images, start=2):
        src = image.get("src", "")
        if final_state and "SHOPIFY_IMAGE_" in src:
            errors.append(f"Body image {number} retains an unresolved placeholder")
        if not final_state and src != f"SHOPIFY_IMAGE_{number}_URL":
            errors.append(f"Unexpected image placeholder at body position {number}")
        if not image.get("alt", "").strip():
            errors.append(f"Body image {number} has no alt text")
        if image.get("width") or image.get("height"):
            errors.append(
                f"Body image {number} must not use fixed width/height attributes; "
                "the Elite Range Hood theme constrains width without resetting height"
            )

    product_links = [link for link in article.links if is_product(link.get("href", ""))]
    distinct_products = sorted({link.get("href", "") for link in product_links})
    if len(distinct_products) < 2:
        errors.append(
            f"Expected at least two distinct Elite Range Hood product-detail links; "
            f"found {len(distinct_products)}"
        )
    for link in product_links:
        if link.get("style") != PRODUCT_STYLE:
            errors.append(f"Product link lacks approved black-underlined style: {link.get('href', '')}")

    word_checks: dict[str, dict] = {}
    for label in ("word", "chineseWord"):
        word_path = paths[label]
        if not word_path.is_file():
            continue
        check = inspect_word(word_path)
        word_checks[label] = check
        if check.get("error"):
            errors.append(str(check["error"]))
            continue
        if check.get("mediaCount") != IMAGE_COUNT:
            errors.append(f"{word_path.name} must contain exactly three images")
        if check.get("missingImageAlt"):
            errors.append(f"{word_path.name} contains image(s) without accessible alt text")
        if check.get("forbiddenBrandAbbreviation"):
            errors.append(f"{word_path.name} contains the forbidden customer-facing abbreviation ERH")
        if check.get("productUrls") != distinct_products:
            errors.append(
                f"{word_path.name} product-link set does not match the Shopify HTML product-link set"
            )

    if len(meta.get("researchSources", [])) < 2:
        errors.append("Expected at least two authority sources")
    if len(meta.get("backlinkPlan", [])) < 2:
        errors.append("Expected at least two reverse-link tasks")
    meta_internal_links = meta.get("internalLinks", [])
    for url in distinct_products:
        matches = [
            item for item in meta_internal_links
            if isinstance(item, dict) and item.get("url") == url
        ]
        if not matches:
            errors.append(f"Missing metadata verification record for product link: {url}")
            continue
        record = matches[0]
        if record.get("verified") is not True or not record.get("verifiedAt") or not record.get("visibleH1"):
            errors.append(
                f"Product-link metadata must include verified=true, verifiedAt, and visibleH1: {url}"
            )
    image_plan = meta.get("imagePlan", [])
    if len(image_plan) != IMAGE_COUNT:
        errors.append(f"Expected three image-plan records; found {len(image_plan)}")
    for index, record in enumerate(image_plan, start=1):
        if not isinstance(record, dict):
            errors.append(f"Image-plan record {index} is not an object")
            continue
        for field in ("file", "purpose", "alt", "sourcePage", "usageBasis"):
            if not str(record.get(field, "")).strip():
                errors.append(f"Image-plan record {index} is missing {field}")
    seo = meta.get("seo", {})
    seo_title_chars = len(str(seo.get("title", "")))
    meta_description_chars = len(str(seo.get("metaDescription", "")))
    if not 40 <= seo_title_chars <= 65:
        errors.append("SEO title should contain 40–65 characters")
    if not 130 <= meta_description_chars <= 165:
        errors.append("Meta description should contain 130–165 characters")

    public_brand_surfaces = {
        "English Markdown": markdown,
        "Shopify body HTML": body_html,
        "final H1": str(meta.get("finalH1", "")),
        "SEO title": str(seo.get("title", "")),
        "meta description": str(seo.get("metaDescription", "")),
        "excerpt": str(seo.get("excerpt", "")),
        "Shopify title": str(publish.get("title", "")),
        "Shopify SEO title": str(publish.get("seoTitle", "")),
        "Shopify meta description": str(publish.get("metaDescription", "")),
        "Shopify excerpt": str(publish.get("excerpt", "")),
    }
    chinese_markdown_path = root / f"{slug}.zh-CN.md"
    if chinese_markdown_path.is_file():
        public_brand_surfaces["Chinese review Markdown"] = chinese_markdown_path.read_text(encoding="utf-8")
    forbidden_brand_findings: dict[str, int] = {}
    for label, value in public_brand_surfaces.items():
        count = len(FORBIDDEN_PUBLIC_BRAND_ABBREVIATION.findall(value))
        if count:
            forbidden_brand_findings[label] = count
            errors.append(
                f"Use 'Elite Range Hood' instead of standalone 'ERH' in {label}; found {count} occurrence(s)"
            )

    if publish.get("storeHandle") != "97256c-fc":
        errors.append("Shopify store handle is not the configured Elite Range Hood store")
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
    if len(image_manifest) != IMAGE_COUNT:
        errors.append(f"Expected three manifest images; found {len(image_manifest)}")
    optimized_bytes = 0
    featured_dimensions: dict[str, int] = {}
    for index, record in enumerate(image_manifest, start=1):
        if record.get("order") != index:
            errors.append(f"Image manifest position {index} has unexpected order {record.get('order')!r}")
        expected_role = "featured image" if index == 1 else "body image"
        if record.get("role") != expected_role:
            errors.append(f"Image manifest position {index} must use role {expected_role!r}")
        alt_text = str(record.get("alt", ""))
        if FORBIDDEN_PUBLIC_BRAND_ABBREVIATION.search(alt_text):
            label = f"image {index} alt text"
            forbidden_brand_findings[label] = len(FORBIDDEN_PUBLIC_BRAND_ABBREVIATION.findall(alt_text))
            errors.append(f"Use 'Elite Range Hood' instead of standalone 'ERH' in {label}")
        path = root / str(record.get("uploadFile", ""))
        if not path.is_file():
            errors.append(f"Missing optimized image: {path}")
            continue
        optimized_bytes += path.stat().st_size
        if path.stat().st_size >= 300_000:
            errors.append(f"Optimized image exceeds 300 KB: {path.name}")
        try:
            with Image.open(path) as image:
                actual_width, actual_height = image.size
        except OSError as exc:
            errors.append(f"Unreadable optimized image {path.name}: {exc}")
            continue
        manifest_width = record.get("width")
        manifest_height = record.get("height")
        if (manifest_width, manifest_height) != (actual_width, actual_height):
            errors.append(
                f"Image dimensions do not match manifest for {path.name}: "
                f"manifest={manifest_width}x{manifest_height}, actual={actual_width}x{actual_height}"
            )
        if index == 1:
            featured_dimensions = {"width": actual_width, "height": actual_height}
            if (actual_width, actual_height) != (FEATURED_WIDTH, FEATURED_HEIGHT):
                errors.append(
                    f"Featured image must be exactly {FEATURED_WIDTH}x{FEATURED_HEIGHT}; "
                    f"found {actual_width}x{actual_height}: {path.name}"
                )
        elif (actual_width, actual_height) != (BODY_WIDTH, BODY_HEIGHT):
            errors.append(
                f"Body image {index} must be exactly {BODY_WIDTH}x{BODY_HEIGHT}; "
                f"found {actual_width}x{actual_height}: {path.name}"
            )

    layout_reference = publish.get("layoutReference", {})
    if layout_reference and layout_reference.get("featuredAspectRatio") not in {None, "2:1"}:
        errors.append("Publication layout reference must use featuredAspectRatio 2:1")
    if layout_reference and layout_reference.get("bodyAspectRatio") not in {None, "3:2"}:
        errors.append("Publication layout reference must use bodyAspectRatio 3:2")

    report = {
        "schemaVersion": "erh-blog-validation-2.1.0",
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
            "imageSourceType": image_source_type,
            "featuredImageDimensions": featured_dimensions,
            "featuredImageExact2to1": bool(
                featured_dimensions
                and featured_dimensions["width"] == featured_dimensions["height"] * 2
            ),
            "forbiddenBrandAbbreviationFindings": forbidden_brand_findings,
            "distinctProductLinks": len(distinct_products),
            "styledProductLinks": sum(link.get("style") == PRODUCT_STYLE for link in product_links),
            "authoritySources": len(meta.get("researchSources", [])),
            "backlinkTasks": len(meta.get("backlinkPlan", [])),
            "seoTitleCharacters": seo_title_chars,
            "metaDescriptionCharacters": meta_description_chars,
            "optimizedImageBytes": optimized_bytes,
            "unsafeHtmlFindings": len(article.errors),
            "word": word_checks,
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
