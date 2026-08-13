#!/usr/bin/env python3
"""Build a Shopify-safe ERH HTML and WebP package from six-image Markdown."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

from PIL import Image


INLINE_RE = re.compile(
    r"!\[([^\]]*)\]\(([^)]+)\)|"
    r"\[([^\]]+)\]\((https?://[^)]+)\)|"
    r"\*\*([^*]+)\*\*|"
    r"(?<!\*)\*([^*]+)\*(?!\*)|"
    r"`([^`]+)`"
)


def render_inline(text: str) -> str:
    output: list[str] = []
    cursor = 0
    for match in INLINE_RE.finditer(text):
        output.append(html.escape(text[cursor : match.start()], quote=False))
        image_alt, _image_path, link_text, url, strong, emphasis, code = match.groups()
        if image_alt is not None:
            raise ValueError("Images must be handled as block elements")
        if link_text is not None:
            output.append(
                f'<a href="{html.escape(url, quote=True)}">'
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
        if not source.is_file() or (source != root and root not in source.parents):
            raise FileNotFoundError(f"Invalid or missing image: {relative_path}")
        target = web_dir / optimized_name(index, source)
        with Image.open(source) as image:
            rgb = image.convert("RGB")
            rgb.save(target, "WEBP", quality=82, method=6)
            width, height = rgb.size
        manifest.append(
            {
                "order": index,
                "source": str(source.relative_to(root)),
                "uploadFile": str(target.relative_to(root)),
                "width": width,
                "height": height,
                "alt": alt,
                "role": "featured image" if index == 1 else "body image",
            }
        )
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
            level = len(heading.group(1))
            if level > 1:
                output.append(f"<h{level}>{render_inline(heading.group(2))}</h{level}>")
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
                next_caption = re.match(r"^\*(.+)\*$", lines[lookahead].strip())
                if next_caption:
                    caption_text = next_caption.group(1)
                    index = lookahead
            if image_index == 1:
                if caption_text:
                    output.append(f"<p><em>{render_inline(caption_text)}</em></p>")
            else:
                output.extend(
                    [
                        "<figure>",
                        f'  <img src="SHOPIFY_IMAGE_{image_index}_URL" alt="{html.escape(record["alt"], quote=True)}" width="{record["width"]}" height="{record["height"]}" loading="lazy">',
                    ]
                )
                if caption_text:
                    output.append(f"  <figcaption>{render_inline(caption_text)}</figcaption>")
                output.append("</figure>")
            index += 1
        elif stripped.startswith("|") and index + 1 < len(lines) and re.match(
            r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$", lines[index + 1].strip()
        ):
            flush()
            table_lines: list[str] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index].strip())
                index += 1

            def cells(row: str) -> list[str]:
                return [value.strip() for value in row.strip().strip("|").split("|")]

            headers = cells(table_lines[0])
            rows = [cells(row) for row in table_lines[2:]]
            output.extend(["<table>", "  <thead>", "    <tr>"])
            output.extend(f'      <th scope="col">{render_inline(cell)}</th>' for cell in headers)
            output.extend(["    </tr>", "  </thead>", "  <tbody>"])
            for row in rows:
                output.append("    <tr>")
                for cell_index, cell in enumerate(row):
                    if cell_index == 0:
                        output.append(f'      <th scope="row">{render_inline(cell)}</th>')
                    else:
                        output.append(f"      <td>{render_inline(cell)}</td>")
                output.append("    </tr>")
            output.extend(["  </tbody>", "</table>"])
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
        elif caption:
            flush()
            output.append(f"<p><em>{render_inline(caption.group(1))}</em></p>")
            index += 1
        else:
            paragraph.append(stripped)
            index += 1
    flush()
    return "\n".join(output) + "\n"


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
    meta_path = root / f"{slug}.meta.json"
    markdown = markdown_path.read_text(encoding="utf-8")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    image_records = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", markdown)
    if len(image_records) != 6:
        raise ValueError(f"Expected exactly six images, found {len(image_records)}")
    if any(not alt.strip() for alt, _ in image_records):
        raise ValueError("Every image must have non-empty alt text")
    manifest = optimize_images(root, image_records)
    html_path = root / f"{slug}.shopify.html"
    html_path.write_text(markdown_to_shopify(markdown, manifest), encoding="utf-8")

    seo = meta["seo"]
    publish = {
        "schemaVersion": "erh-shopify-publish-2.0.0",
        "state": "ready-for-shopify-upload",
        "title": meta["finalH1"],
        "blog": meta.get("shopify", {}).get("targetBlog", "News"),
        "author": "REQUIRED: select an approved ERH public author or team in Shopify",
        "handle": seo["handle"],
        "seoTitle": seo["title"],
        "metaDescription": seo["metaDescription"],
        "excerpt": seo["excerpt"],
        "tags": seo["tags"],
        "featuredImage": manifest[0],
        "bodyHtml": html_path.name,
        "images": manifest,
        "imageUrlPlaceholders": [f"SHOPIFY_IMAGE_{i}_URL" for i in range(2, 7)],
        "expectedPublicUrl": f'https://eliterangehood.com/blogs/news/{seo["handle"]}',
        "publishAuthorization": "not granted",
        "shopifyWritePerformed": False,
    }
    publish_path = root / f"{slug}.publish.json"
    publish_path.write_text(json.dumps(publish, indent=2) + "\n", encoding="utf-8")
    print(html_path)
    print(publish_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
