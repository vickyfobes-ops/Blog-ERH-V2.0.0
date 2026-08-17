#!/usr/bin/env python3
"""Replace Elite Range Hood body-image placeholders with uploaded Shopify CDN URLs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


def valid_shopify_image(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname in {
        "cdn.shopify.com", "eliterangehood.com", "www.eliterangehood.com"
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", required=True, type=Path)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--mapping-json", required=True, type=Path)
    args = parser.parse_args()
    root = args.dir.expanduser().resolve()
    mapping = json.loads(args.mapping_json.expanduser().read_text(encoding="utf-8"))
    required = {f"SHOPIFY_IMAGE_{i}_URL" for i in range(2, 7)}
    if set(mapping) != required:
        raise ValueError(f"Mapping keys must be exactly {sorted(required)}")
    if any(not valid_shopify_image(str(value)) for value in mapping.values()):
        raise ValueError("Every mapped image must be an approved HTTPS Shopify/storefront URL")

    source_path = root / f"{args.slug}.shopify.html"
    output_path = root / f"{args.slug}.shopify.final.html"
    body = source_path.read_text(encoding="utf-8")
    for placeholder, url in mapping.items():
        if body.count(placeholder) != 1:
            raise ValueError(f"Expected one occurrence of {placeholder}")
        body = body.replace(placeholder, str(url))
    if "SHOPIFY_IMAGE_" in body:
        raise ValueError("Unresolved Shopify image placeholder remains")
    output_path.write_text(body, encoding="utf-8")

    publish_path = root / f"{args.slug}.publish.json"
    publish = json.loads(publish_path.read_text(encoding="utf-8"))
    publish["state"] = "ready-for-hidden-shopify-draft"
    publish["shopifyBodyHtml"] = output_path.name
    publish["bodyImageUrls"] = mapping
    publish_path.write_text(json.dumps(publish, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(output_path)
    print(publish_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
