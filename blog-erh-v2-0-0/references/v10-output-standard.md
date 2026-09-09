# V10 linked Word and HTML output standard

This reference defines the default local deliverable produced after an operator enters one sufficiently specific English topic on any supported computer.

## Primary outcome

The same researched article must be delivered in two primary customer-review formats before any Shopify write:

1. An English Word document named `<handle>.review.docx`.
2. A Shopify body fragment named `<handle>.shopify.html`.

Both files must be derived from the same English Markdown source. They must contain the same contextual Elite Range Hood internal links, the same authority sources, and the same article meaning. Also create the complete Chinese Markdown and Word review copies required by the Skill, but treat the English Word document and Shopify HTML as the primary handoff.

## Internal-link contract

- Discover and verify links during the local review-package stage, not after editorial approval.
- Include at least two distinct, genuinely relevant, live `https://eliterangehood.com/products/...` links.
- Add useful collection, buying-guide, measurement, samples, ordering, contact, care, or supporting-blog links where the reader needs the next step.
- Use descriptive anchors. Never use guessed URLs or `click here`.
- In Shopify HTML, every counted product-detail link must use exactly `style="color:#000000;text-decoration:underline;"`.
- Word hyperlinks must remain clickable. The product-link set in Word and HTML must match.
- Reopen counted product pages and record their visible H1 titles before review, then reverify them immediately before an authorized publication.

## Image contract

Use exactly three reviewed images:

1. One featured image at exactly `1774 × 887` pixels (`2:1`). It appears in the Word document and the Shopify article image field, not in Shopify body HTML.
2. Two body images at exactly `1536 × 1024` pixels (`3:2`). They appear in both the Word document and Shopify body HTML.

Prefer approved, brand-owned Elite Range Hood project photography from current Elite Range Hood pages. Record the source page and usage basis for each image. Preserve the actual hood and room geometry: do not redraw, shorten, stretch, flatten, or fabricate the product. A proportional crop is allowed only when the complete decision-critical hood context remains visible.

If suitable approved project photography is unavailable for the topic, generated design visualizations are a fallback. Keep the same three-image count and dimensions, visually inspect every output, and disclose generated imagery accurately. Never describe a generated scene as a customer project.

All images require factual alt text. Shopify body image tags must be plain `<p><img ...></p>` with no fixed `width` or `height` attributes. Do not use fixed-height wrappers or `object-fit: fill`.

## Shopify HTML contract

- Do not repeat the article H1 in body HTML.
- Map Markdown H2 to `<h4>` and Markdown H3 to `<h5>`.
- Use short paragraphs, parallel lists, ordinary links, and plain image paragraphs.
- Do not add scripts, Liquid, iframes, embedded styles, `<figure>`, `<figcaption>`, or tables by default.
- Keep `Sources and Technical References` visible near the end of the article and place the visible FAQ after it when the search intent supports an FAQ.
- Use the public brand name `Elite Range Hood`; never expose the standalone abbreviation `ERH`.

## Word contract

- Use US Letter portrait layout and a clear black title.
- Include the complete English article, all three reviewed images, captions where useful, visible sources, and clickable contextual links.
- Preserve factual alt text in the Word drawing metadata.
- Use the public brand name `Elite Range Hood`; never expose the standalone abbreviation `ERH`.
- Render every page to PNG and visually inspect it before delivery. No clipping, overlap, distorted image, broken link styling, or missing glyph is acceptable.

## Publication boundary

Generating the linked Word and HTML package is local work. It does not authorize Shopify upload or publication. Visible publication still requires the exact phrase `审核通过并发布` for the current reviewed package.
