---
name: blog-erh-v2-0-0
description: "Run the preconfigured Elite Range Hood Shopify blog workflow from one English topic on any supported operator computer: research and generate the complete English article, meaning-matched Chinese review copy, a linked English Word document, Shopify-safe HTML with verified contextual internal links, SEO metadata, and the V10 three-image set; pause for human review; then, after the exact approval phrase, upload through the operator's signed-in Chrome, publish, and verify the public article and homepage. Use when an operator invokes $blog-erh-v2-0-0, asks for an Elite Range Hood blog package, or says 审核通过并发布 for the current reviewed package. The fixed store profile works on supported Windows and macOS Codex desktop apps and never requires a Shopify API key or custom app."
---

# Blog—ERH—V2.0.0

Operate the fixed Elite Range Hood workflow as three user-visible outcomes:

1. The operator inputs one English topic.
2. Generate and present the complete linked Word, HTML, and three-image review package.
3. After exact approval, automatically upload, publish, and verify the already-reviewed package.

Do not expose research, image generation, link discovery, HTML conversion, image upload, or verification as extra operator steps. Do not ask the operator to configure the store again.

## Load the fixed profile

Read these for every run:

- `assets/elite-range-hood.json`
- `references/site-config.md`
- `references/brand-facts-and-guardrails.md`
- `references/shopify-output-contract.md`
- `references/v10-output-standard.md`

Read `references/operator-setup.md` on a new computer or when browser control is unavailable. Read `references/shopify-browser-workflow.md` before any Shopify action. Read `references/security-and-handoff.md` before packaging or handing the Skill to another operator.

Resolve bundled resources relative to this installed `SKILL.md`. Write article outputs in the operator's current workspace, never in the installed Skill directory. The original author's workspace and V10 HTML file are not required on another computer.

## Required capabilities and routing

- Use internet research for current facts and authoritative sources.
- Prefer approved Elite Range Hood project photography for the V10 three-image set. Use deterministic proportional crop and resize tools for real photography. Use `imagegen` only when an explicitly approved outpaint is required or when suitable approved photography is unavailable.
- Use `documents` for the linked English Word document and Chinese Word review artifact when available; use `scripts/build_review_docx.py` as the deterministic fallback.
- Prefer `chrome:control-chrome` for Shopify because it reuses the operator's authorized Chrome session.
- If Chrome control is unavailable but Computer Use is installed, use Computer Use to operate Chrome visually.
- On Windows, keep Chrome visible on the active unlocked desktop while Computer Use runs. On macOS, follow the permissions requested by Computer Use.
- Never switch to API-key automation, request credentials, inspect cookies, or export a browser profile.

Local Word, HTML, and image generation does not require Chrome control or Shopify authentication. Check browser setup only if the operator requests an online action. Never claim that an upload occurred when only local files were generated.

## First run on another operator's computer

Installation carries the fixed non-secret Elite Range Hood store profile, content rules, scripts, and upload runbook. It does not and must not carry authentication.

Before local generation, run `scripts/check_runtime.py` with the workspace Python runtime. If unavailable or missing packages, follow the isolated-environment fallback in `references/operator-setup.md`. Read `references/local-build.md` for input filenames, metadata fields, and script order.

Before the first Shopify write:

1. Run `scripts/check_runtime.py` with the available workspace Python runtime.
2. Confirm the Chrome/Computer Use plugin is enabled.
3. Confirm the ChatGPT Chrome extension is installed in the active Chrome profile and file-URL access is enabled for image uploads.
4. Let the operator sign in to Shopify and complete password, 2FA, or CAPTCHA themselves.
5. Confirm the visible store handle is `97256c-fc`, the public domain is `eliterangehood.com`, and the target blog is `News`.
6. Use a Hidden draft for the first online test unless the current reviewed package has the exact publication approval.

Do not ask for a Shopify API key, OpenAI API key, password, cookie, token, or custom application.

## Action 1 — Input one topic and generate

Accept a plain English title or topic after `$blog-erh-v2-0-0`. If specific enough, start immediately.

### Research and write

1. Check current Elite Range Hood articles for intent overlap.
2. Verify relevant live Elite Range Hood product pages and current product facts.
3. Verify volatile, technical, health, safety, code, cost, policy, and specification claims with current primary sources.
4. Discover and open at least two genuinely relevant live `https://eliterangehood.com/products/...` pages. Record their visible H1 titles, then insert the verified product links and other useful Elite Range Hood internal links contextually in the source article.
5. Write a formal US-English article that answers the buyer's main question in its first 100–150 words.
6. Create a complete meaning-matched Chinese version; do not summarize and preserve the verified link destinations.
7. Keep external authority links in the final visible `Sources and Technical References` section.
8. Never invent Elite Range Hood dimensions, CFM, noise, pricing, lead time, warranty, certifications, materials, mounting, or care claims.
9. Never guess a product URL. Word and HTML must contain the same verified product-link set before human review.

### Brand naming

- Write the public brand name exactly as `Elite Range Hood` in every customer-facing English or Chinese deliverable.
- Do not publish the abbreviation `ERH` in article copy, headings, SEO title, meta description, excerpt, CTA, anchor text, image alt text, captions, Word review copy, Shopify body HTML, or public article fields.
- Allow `ERH` only inside the existing Skill/repository name, internal filenames, internal audit IDs, and technical schema identifiers. Never let those internal identifiers leak into customer-facing copy.
- Run the bundled validator and replace every forbidden standalone abbreviation before review or Shopify upload.

### Prepare the V10 three-image set

- Prepare exactly one featured image and two body images.
- Follow `references/visual-direction.md`.
- Prefer approved, brand-owned Elite Range Hood project photography from current Elite Range Hood pages and record the source page for every image.
- Lock each body image to a specific article section and reader decision. Do not use generic kitchens or near-duplicate hood views.
- Build the featured source at an exact `2:1` ratio. Keep the complete hood crown, body, lower apron, cooktop or range, and the article's essential planning context inside the safe frame; never depend on Shopify to repair a vertical or tightly cropped composition.
- Build both body images at an exact `3:2` ratio, using `1536 × 1024` as the reference size.
- Preserve real hood and room geometry. Never redraw, shorten, stretch, flatten, or fabricate a photographed Elite Range Hood product.
- Default to exterior silhouette, finish, proportion, and craftsmanship. Do not show a cutaway, exposed internals, or invented engineering construction unless the operator explicitly requests a documented technical illustration.
- Reject malformed, unsafe, near-duplicate, distorted, or misleading images.
- Visually inspect all three source files before review and inspect the Shopify-rendered featured crop and two responsive body images after save.
- If generated design visualizations are necessary, disclose them accurately and never call them customer projects.
- Save accurate alt text for every image.

### Produce the review package

Create a topic-specific output directory containing:

- English Markdown article;
- complete Chinese Markdown article;
- linked English Word review document named `<handle>.review.docx`;
- complete Chinese Word review document;
- SEO title, description, handle, excerpt, tags, intent, cluster, funnel, and CTA;
- Shopify-safe HTML that already contains the verified contextual internal links;
- exactly three reviewed image files: one `1774 × 887` featured image and two `1536 × 1024` body images;
- local Elite Range Hood theme preview;
- source log, internal-link plan, publication manifest, and validation report.

Use the bundled scripts with the available cross-platform Python runtime. Prefer the workspace dependency runtime when available. On Windows, `py -3` or `python` may replace `python3`; do not make the operator run commands that Codex can run itself.

Present the article, linked Word document, linked Shopify HTML, SEO information, sources, images, preview, and validation result. Then wait.

## Action 2 — Human review

Apply requested content, source, image, SEO, link-placement, or layout revisions. Regenerate affected Word, HTML, and image artifacts so they remain synchronized. Comments such as “可以” or “看起来不错” do not authorize publication.

Only the exact phrase `审核通过并发布` authorizes visible publication of the current reviewed package. Approval freezes the reviewed article, authority sources, verified internal links, and three images. Any material editorial change after approval returns to review.

For a narrowly scoped correction to an already published article, such as “replace the featured image” or “fix the crop,” change only the requested field. Preserve the verified article ID, body, body images, links, SEO fields, author, blog, template, and visibility unless the operator explicitly expands the scope. A correction never authorizes creation of a duplicate article.

## Action 3 — Automatic Shopify delivery

After `审核通过并发布`:

1. Read `references/shopify-browser-workflow.md` completely.
2. Reconfirm the current package, store `97256c-fc`, blog `News`, author `YMQ`, template, title, handle, and three reviewed images. Search by recorded Shopify article ID first, then exact handle and title. Update the verified article when it exists; never create a second article for the same package.
3. Reopen and reverify the reviewed product links against the current storefront, product sitemap, or Shopify admin. Preserve the reviewed anchors and URLs when they remain current.
4. Confirm at least two genuinely relevant live `https://eliterangehood.com/products/...` pages and their visible H1 titles. Collections, pages, blogs, searches, previews, redirects, guessed URLs, and admin URLs do not count.
5. Confirm counted links are styled exactly as `style="color:#000000;text-decoration:underline;"`.
6. Preserve reviewed authority sources unchanged.
7. Build and validate Shopify-safe HTML. Fix every validation error before any save.
8. Upload the one featured image and two body images through Shopify. Select by exact filename, verify the selected thumbnail and alt text before confirming, replace local placeholders with Shopify-hosted HTTPS URLs, and rerun validation.
9. Fill title, body, excerpt, author, blog, tags, SEO title, meta description, handle, template, and visibility.
10. Publish, save, reopen, and confirm that all fields persisted.
11. Open the public article; verify layout, three images, sources, product links, SEO handle, and mobile-readable flow. Confirm the `2:1` featured source renders without losing the hood crown, lower apron, cooking appliance, or other decision-critical content, and confirm both `3:2` body images keep their natural aspect ratios.
12. Click every counted product link and confirm the intended live product page.
13. Confirm the homepage `Blogs` module displays the new article normally.

Continue autonomously through Action 3. Stop only for login, password, 2FA, CAPTCHA, insufficient Shopify permission, unavailable browser control, or fewer than two relevant live product pages. Never weaken the product-link minimum.

## Validation and completion

Use:

- `scripts/build_review_docx.py` for Word review output when needed;
- `scripts/render_review_docx.py` to render Word pages for visual QA, including macOS CJK-font exposure;
- `scripts/check_runtime.py` for first-run cross-platform dependency checks;
- `scripts/build_shopify_bundle.py` to build optimized WebP assets, preview, manifest, and initial HTML;
- `scripts/finalize_shopify_images.py` after Shopify provides hosted image URLs;
- `scripts/validate_blog_package.py` before Shopify save and again before publication.

For local delivery, report absolute artifact paths, validation results, and verified product URLs. After an authorized online action, also report Shopify article state, admin/public URLs, product-link click results, and homepage result. Never describe a local package or Hidden draft as published.
