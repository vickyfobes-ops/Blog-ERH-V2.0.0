# Elite Range Hood Shopify output contract

## Article fields

```yaml
title: ""
handle: ""
author: "YMQ"
blog: "News"
blog_handle: "news"
tags: []
excerpt: ""
body_html: ""
seo_title: ""
seo_description: ""
featured_image:
  source: ""
  alt: ""
visibility: "hidden"
publish_at: null
sources: []
internal_links: []
backlink_tasks: []
```

Each counted product record in `internal_links` must include its contextual anchor, exact product URL, `verified: true`, verification date, and the visible product-page H1 captured during review.

The default online state is `Hidden`. Visible publication requires the exact phrase `审核通过并发布` for the current reviewed package.

## Elite Range Hood live-theme body HTML

- Do not include the article H1; the theme renders the title.
- Map Markdown H2 sections to `<h4>` and Markdown H3 subsections or FAQ questions to `<h5>`.
- Use `<p>`, `<h4>`, `<h5>`, `<ul>`, `<ol>`, `<li>`, `<strong>`, `<em>`, `<a>`, and plain `<p><img ...></p>`.
- Avoid `<figure>`, `<figcaption>`, and tables by default because the verified Elite Range Hood reference article does not establish those layouts.
- Do not include scripts, Liquid, iframes, embedded style sheets, tracking code, or inline event handlers.
- The only default inline style exception is a verified Elite Range Hood product-detail link. It must use exactly `style="color:#000000;text-decoration:underline;"`.
- Keep visible FAQs in the article when the intent supports them. Do not add FAQ JSON-LD unless duplicate schema is ruled out.
- Do not link competitors in customer-facing content.

## Product internal links

- Include at least two contextual links to current, relevant `https://eliterangehood.com/products/...` pages in the local Word and HTML review package.
- A collection, page, blog article, search result, or homepage does not count as a product link.
- Open each selected product page before local review and record its visible H1. Reopen it immediately before an authorized publication.
- Product links must be readable, descriptive, black, underlined, and placed where the linked model helps the reader make the current decision.
- The body may also link to collections, samples, ordering, contact, care, and supporting blogs, but these do not replace the product-link minimum.
- The English Word document and Shopify HTML must contain the same counted product-link set.

## External authority sources

Keep necessary primary external sources in a final visible `<h4>Sources and Technical References</h4>` section. In-body citations are acceptable when they directly support a technical statement, but Elite Range Hood links should dominate ordinary navigation and commercial CTAs.

## Brand-name validation

- Use `Elite Range Hood` everywhere the public brand is named.
- Reject standalone `ERH` in the English article, Chinese review copy, title, SEO title, meta description, excerpt, CTA, anchor text, image alt text, captions, and final Shopify HTML.
- Internal Skill names, repository paths, audit IDs, and technical schema identifiers are exempt because customers do not see them.

## V10 images

- Exactly three images per standard package: one featured image plus two body images.
- The featured image is stored in Shopify's article image field and is not repeated in body HTML.
- The final featured source must be exactly `2:1`; `1774 × 887` is the verified reference size for the current theme.
- The featured safe frame must contain the complete hood crown, body, lower apron, cooking appliance, and any article-specific planning material. Do not rely on Shopify crop controls to rescue the composition.
- Both body images must be exactly `3:2`; `1536 × 1024` is the reference size. Each must support a named article section and use responsive natural height. Do not output fixed `width` or `height` attributes on body-image tags.
- Prefer approved Elite Range Hood project photography. Record the source page and preserve the real hood and room geometry without redrawing, shortening, stretching, flattening, or fabricating the product.
- Final body HTML must use Shopify-hosted HTTPS URLs; no local paths or unresolved placeholders.
- Each image requires a factual alt text. Generated kitchens require a visible design-visualization disclosure; authentic project photography must not be mislabeled as generated.
- Before review and after Shopify save, visually verify the full frame, product geometry, crop, and section relevance of all three images.

## Local deliverables

- English source Markdown and metadata JSON.
- Linked English Word review document named `<handle>.review.docx`.
- Complete Chinese Markdown and Word review copies.
- Three optimized WebP images.
- Shopify-safe HTML and local theme preview.
- Publication manifest and validation report.
- Optional review ZIP.

## Preflight

- Confirm no handle collision.
- Confirm store `97256c-fc`, blog `News`, author `YMQ`, and template `Default blog post`.
- Confirm exactly one featured image and two body images.
- Confirm the featured image is exact `2:1`, both body images are exact `3:2`, essential content is not cropped, and body-image tags have no fixed dimensions.
- Confirm two or more live product-detail links with the approved style.
- Confirm the Word and HTML product-link sets match.
- Confirm all authority sources, alt text, disclosure, CTA, and SEO fields.
- Confirm no duplicate H1 or unresolved image placeholder.
- Confirm Visibility is `Hidden` for testing or explicitly approved `Visible` for publication.
