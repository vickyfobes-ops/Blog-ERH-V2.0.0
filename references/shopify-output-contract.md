# ERH Shopify local-output contract

## Article object

Use these fields when applicable:

```yaml
title: ""
handle: ""
author: ""
blog_handle: "news"
tags: []
excerpt: ""
body_html: ""
seo_title: ""
seo_description: ""
featured_image:
  source: ""
  alt: ""
status: "draft"
publish_at: null
sources: []
internal_links: []
backlink_tasks: []
```

Keep `status: draft` by default. Require separate, explicit authorization to create a draft online and to publish or schedule it.

## Body HTML

- Start at `<h2>`; the Shopify theme normally renders the article H1.
- Use semantic `<p>`, `<h2>`, `<h3>`, `<ul>`, `<ol>`, `<li>`, `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>`, `<figure>`, `<img>`, `<figcaption>`, `<strong>`, `<em>`, and `<a>`.
- Do not use scripts, Liquid, iframes, embedded style sheets, tracking code, or inline event handlers.
- Avoid inline styles so the theme controls presentation.
- Give table headers the correct `scope` attribute.
- Keep visible FAQ content in the article. Do not add FAQ JSON-LD unless the theme's schema behavior has been verified and duplication is impossible.
- Use external commercial links only when required; do not link competitors in the customer-facing final article.

## Images

Store the featured image separately when the theme renders it. Do not insert the same hero in `body_html`. For a six-image package, the manifest should list one featured image and five body images with upload file, width, height, alt text, and role.

Use Shopify-hosted image URLs in the final online body. Local package placeholders are acceptable before upload and must be listed in the publication sheet.

## Local deliverables

A complete upload package should contain:

- source Markdown;
- metadata JSON;
- Shopify-safe HTML;
- optimized WebP images;
- publication manifest JSON;
- human-readable publication sheet;
- validation report.

Optionally include a Word review copy or ZIP when requested. Do not treat a generated package as a published article.

## Preflight

Check:

- handle collision with existing articles;
- title and meta lengths;
- exact author and blog destination;
- no duplicate H1 or featured image;
- internal URLs exist and point to the intended canonical pages;
- every image has an accurate alt and permitted source;
- sources and disclosure are present;
- no unsafe HTML;
- all online actions remain unauthorized until the user explicitly grants them.
