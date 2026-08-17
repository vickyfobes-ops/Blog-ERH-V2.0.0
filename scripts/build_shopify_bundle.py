#!/usr/bin/env python3
"""Build a theme-aligned ERH Shopify package from six-image Markdown."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image


INLINE_RE = re.compile(
    r"!\[([^\]]*)\]\(([^)]+)\)|"
    r"\[([^\]]+)\]\((https?://[^)]+)\)|"
    r"\*\*([^*]+)\*\*|"
    r"(?<!\*)\*([^*]+)\*(?!\*)|"
    r"`([^`]+)`"
)
PRODUCT_LINK_STYLE = "color:#000000;text-decoration:underline;"
FEATURED_ASPECT_WIDTH = 2
FEATURED_ASPECT_HEIGHT = 1


def is_erh_product(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.hostname in {"eliterangehood.com", "www.eliterangehood.com"} and parsed.path.startswith("/products/")


def render_inline(text: str) -> str:
    output: list[str] = []
    cursor = 0
    for match in INLINE_RE.finditer(text):
        output.append(html.escape(text[cursor:match.start()], quote=False))
        image_alt, _image_path, link_text, url, strong, emphasis, code = match.groups()
        if image_alt is not None:
            raise ValueError("Images must be handled as block elements")
        if link_text is not None:
            style = f' style="{PRODUCT_LINK_STYLE}"' if is_erh_product(url) else ""
            output.append(
                f'<a href="{html.escape(url, quote=True)}"{style}>'
                f"{html.escape(link_text, quote=False)}</a>"
            )
        elif strong is not None:
            output.append(f"<strong>{html.escape(strong, quote=False)}</strong>")
        elif emphasis is not None:
            output.append(f"<em>{html.escape(emphasis, quote=False)}</em>")
        elif code is not None:
            output.append(f"<code>{html.escape(code, quote=False)}</code>")
        cursor = match.end()
    output.append(html.escape(text[cursor:], quote=False))
    return "".join(output)


def optimized_name(order: int, source: Path) -> str:
    stem = re.sub(r"[^a-z0-9]+", "-", source.stem.lower()).strip("-")
    return f"{order:02d}-{stem}.webp"


def optimize_images(root: Path, records: list[tuple[str, str]]) -> list[dict]:
    web_dir = root / "images" / "web"
    web_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    for index, (alt, relative_path) in enumerate(records, start=1):
        source = (root / relative_path).resolve()
        if not source.is_file() or root not in source.parents:
            raise FileNotFoundError(f"Invalid or missing image: {relative_path}")
        target = web_dir / optimized_name(index, source)
        with Image.open(source) as image:
            rgb = image.convert("RGB")
            width, height = rgb.size
            if index == 1 and width * FEATURED_ASPECT_HEIGHT != height * FEATURED_ASPECT_WIDTH:
                raise ValueError(
                    f"Featured image must be exact 2:1 before Shopify upload; "
                    f"found {width}x{height}: {relative_path}"
                )
            if index > 1 and width <= height:
                raise ValueError(
                    f"ERH body images must be landscape-oriented; "
                    f"found {width}x{height}: {relative_path}"
                )
            rgb.save(target, "WEBP", quality=82, method=6)
        manifest.append({
            "order": index,
            "source": str(source.relative_to(root)),
            "uploadFile": str(target.relative_to(root)),
            "width": width,
            "height": height,
            "alt": alt,
            "role": "featured image" if index == 1 else "body image",
        })
    return manifest


def markdown_to_shopify(markdown: str, images: list[dict]) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    image_index = 0
    index = 0

    def flush() -> None:
        if paragraph:
            text = " ".join(item.strip() for item in paragraph).strip()
            paragraph.clear()
            if text:
                output.append(f"<p>{render_inline(text)}</p>")

    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped:
            flush()
            index += 1
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        image = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", stripped)
        bullet = re.match(r"^[-+*]\s+(.+)$", stripped)
        numbered = re.match(r"^\d+\.\s+(.+)$", stripped)
        caption = re.match(r"^\*(.+)\*$", stripped)
        if heading:
            flush()
            source_level = len(heading.group(1))
            if source_level > 1:
                theme_level = 4 if source_level == 2 else 5
                output.append(f"<h{theme_level}>{render_inline(heading.group(2))}</h{theme_level}>")
            index += 1
        elif image:
            flush()
            record = images[image_index]
            image_index += 1
            caption_text = ""
            lookahead = index + 1
            while lookahead < len(lines) and not lines[lookahead].strip():
                lookahead += 1
            if lookahead < len(lines):
                following = re.match(r"^\*(.+)\*$", lines[lookahead].strip())
                if following:
                    caption_text = following.group(1)
                    index = lookahead
            if image_index == 1:
                if caption_text:
                    output.append(f"<p><em>{render_inline(caption_text)}</em></p>")
            else:
                output.append(
                    '<p><img '
                    f'src="SHOPIFY_IMAGE_{image_index}_URL" '
                    f'alt="{html.escape(record["alt"], quote=True)}" '
                    'loading="lazy"></p>'
                )
                if caption_text:
                    output.append(f"<p><em>{render_inline(caption_text)}</em></p>")
            index += 1
        elif bullet or numbered:
            flush()
            pattern = r"^[-+*]\s+(.+)$" if bullet else r"^\d+\.\s+(.+)$"
            tag = "ul" if bullet else "ol"
            items: list[str] = []
            while index < len(lines):
                current = re.match(pattern, lines[index].strip())
                if not current:
                    break
                items.append(current.group(1))
                index += 1
            output.append(f"<{tag}>")
            output.extend(f"  <li>{render_inline(item)}</li>" for item in items)
            output.append(f"</{tag}>")
        elif stripped.startswith("|"):
            raise ValueError("ERH live-theme output does not use Markdown tables by default; rewrite as a list")
        elif caption:
            flush()
            output.append(f"<p><em>{render_inline(caption.group(1))}</em></p>")
            index += 1
        else:
            paragraph.append(stripped)
            index += 1
    flush()
    if image_index != 6:
        raise ValueError(f"Expected six processed images, found {image_index}")
    return "\n".join(output) + "\n"


def build_preview(body_html: str, meta: dict, manifest: list[dict]) -> str:
    preview_body = body_html
    for record in manifest[1:]:
        preview_body = preview_body.replace(
            f'SHOPIFY_IMAGE_{record["order"]}_URL',
            html.escape(record["uploadFile"], quote=True),
        )
    title = html.escape(meta["finalH1"], quote=False)
    hero = manifest[0]
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — ERH local preview</title>
<style>
*{{box-sizing:border-box}} body{{margin:0;background:#fbf8ef;color:#3b3933;font:16px/28px Arial,sans-serif}}
.band{{background:#f1eee2;padding:42px 24px 0}} .crumb,.hero{{display:block;max-width:1140px;margin:auto}} .crumb{{padding-bottom:28px;font-size:13px}}
.article{{width:calc(100% - 40px);max-width:760px;margin:42px auto 86px}} h2{{font-size:40px;line-height:50px;font-weight:500}}
.rte{{color:rgba(59,57,51,.75)}} .rte h4{{color:#3b3933;font-size:32px;line-height:42px;font-weight:500;margin:40px 0 16px}}
.rte h5{{color:#3b3933;font-size:23px;line-height:32px;font-weight:500;margin:30px 0 12px}} .rte p{{margin:0 0 22px}}
.rte img{{display:block;width:100%;height:auto;margin:48px 0}} .rte p:has(>img){{margin:0}} .rte a{{text-underline-offset:2px}}
@media(max-width:800px){{.band{{padding:24px 16px 0}}.article{{width:calc(100% - 32px)}}h2{{font-size:32px;line-height:40px}}.rte h4{{font-size:26px;line-height:34px}}}}
</style></head><body>
<section class="band"><div class="crumb">Home / Blog / {title}</div><img class="hero" src="{html.escape(hero["uploadFile"], quote=True)}" alt="{html.escape(hero["alt"], quote=True)}"></section>
<article class="article"><p>YMQ · Hidden local draft</p><h2>{title}</h2><div class="rte rte--blog-post">{preview_body}</div></article>
</body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", required=True, type=Path)
    parser.add_argument("--slug", help="Source filename stem; auto-detected when omitted")
    args = parser.parse_args()
    root = args.source_dir.expanduser().resolve()
    markdown_path = root / f"{args.slug}.md" if args.slug else next(
        path for path in root.glob("*.md")
        if not path.name.endswith((".zh-CN.md", ".review.md", ".publish.md"))
    )
    slug = markdown_path.stem
    meta = json.loads((root / f"{slug}.meta.json").read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")
    image_records = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", markdown)
    if len(image_records) != 6 or any(not alt.strip() for alt, _ in image_records):
        raise ValueError("Exactly six images with non-empty alt text are required")
    manifest = optimize_images(root, image_records)
    body_html = markdown_to_shopify(markdown, manifest)
    html_path = root / f"{slug}.shopify.html"
    preview_path = root / f"{slug}.site-preview.html"
    html_path.write_text(body_html, encoding="utf-8")
    preview_path.write_text(build_preview(body_html, meta, manifest), encoding="utf-8")
    seo = meta["seo"]
    publish = {
        "schemaVersion": "erh-shopify-publish-2.0.0",
        "state": "requires-shopify-image-upload",
        "storeHandle": "97256c-fc",
        "storeDomain": "97256c-fc.myshopify.com",
        "publicDomain": "eliterangehood.com",
        "title": meta["finalH1"],
        "blog": "News",
        "blogHandle": "news",
        "author": "YMQ",
        "themeTemplate": "Default blog post",
        "visibility": "hidden",
        "handle": seo["handle"],
        "seoTitle": seo["title"],
        "metaDescription": seo["metaDescription"],
        "excerpt": seo["excerpt"],
        "tags": seo["tags"],
        "featuredImage": manifest[0],
        "bodyHtml": html_path.name,
        "localThemePreview": preview_path.name,
        "images": manifest,
        "imageUrlPlaceholders": [f"SHOPIFY_IMAGE_{i}_URL" for i in range(2, 7)],
        "layoutReference": {
            "url": "https://eliterangehood.com/blogs/news/the-value-of-handmade-in-a-mass-produced-world",
            "desktopHeroWidthPx": 1140,
            "desktopBodyWidthPx": 760,
            "featuredAspectRatio": "2:1",
            "featuredReferenceSizePx": {"width": 1774, "height": 887},
            "bodyImageSizing": "responsive-natural-height",
            "bodyHeadingMap": {"markdownH2": "shopifyH4", "markdownH3": "shopifyH5"},
        },
        "expectedPublicUrl": f'https://eliterangehood.com/blogs/news/{seo["handle"]}',
        "publishAuthorization": "not granted",
        "shopifyWritePerformed": False,
    }
    publish_path = root / f"{slug}.publish.json"
    publish_path.write_text(json.dumps(publish, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(html_path)
    print(preview_path)
    print(publish_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
