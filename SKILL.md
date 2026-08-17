---
name: blog-erh-v2-0-0
description: "Run the preconfigured Elite Range Hood Shopify blog workflow from one English topic: research and generate the complete English article, meaning-matched Chinese Word review copy, SEO metadata, Shopify-safe layout, and exactly six images; pause for human review; then, after the exact approval phrase, verify and insert at least two live ERH product-detail links, upload through the operator's signed-in Chrome, publish, and verify the public article and homepage. Use when an operator invokes $blog-erh-v2-0-0, asks for an ERH blog package, or says 审核通过并发布 for the current reviewed package. The fixed store profile works on supported Windows and macOS Codex desktop apps and never requires a Shopify API key or custom app."
---

# Blog—ERH—V2.0.0

Operate the fixed Elite Range Hood workflow as three user-visible outcomes:

1. The operator inputs one English topic.
2. Generate and present the complete article review package.
3. After exact approval, automatically add verified product links, format, upload, publish, and verify.

Do not expose research, image generation, link discovery, HTML conversion, image upload, or verification as extra operator steps. Do not ask the operator to configure the store again.

## Load the fixed profile

Read these for every run:

- `assets/elite-range-hood.json`
- `references/site-config.md`
- `references/brand-facts-and-guardrails.md`
- `references/shopify-output-contract.md`

Read `references/operator-setup.md` on a new computer or when browser control is unavailable. Read `references/shopify-browser-workflow.md` before any Shopify action. Read `references/security-and-handoff.md` before packaging or handing the Skill to another operator.

## Required capabilities and routing

- Use internet research for current facts and authoritative sources.
- Use `imagegen` for exactly six original images.
- Use `documents` for the Chinese Word review artifact when available; use `scripts/build_review_docx.py` as the deterministic fallback.
- Prefer `chrome:control-chrome` for Shopify because it reuses the operator's authorized Chrome session.
- If Chrome control is unavailable but Computer Use is installed, use Computer Use to operate Chrome visually.
- On Windows, keep Chrome visible on the active unlocked desktop while Computer Use runs. On macOS, follow the permissions requested by Computer Use.
- Never switch to API-key automation, request credentials, inspect cookies, or export a browser profile.

If neither Chrome control nor Computer Use is available, complete the local review package, then stop with the precise setup steps from `references/operator-setup.md`. Never claim that an upload occurred.

## First run on another operator's computer

Installation carries the fixed non-secret ERH store profile, content rules, scripts, and upload runbook. It does not and must not carry authentication.

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

1. Check current ERH articles for intent overlap.
2. Verify relevant live ERH product pages and current product facts.
3. Verify volatile, technical, health, safety, code, cost, policy, and specification claims with current primary sources.
4. Write a formal US-English article that answers the buyer's main question in its first 100–150 words.
5. Create a complete meaning-matched Chinese version; do not summarize.
6. Keep external authority links in the final visible `Sources and Technical References` section.
7. Never invent ERH dimensions, CFM, noise, pricing, lead time, warranty, certifications, materials, mounting, or care claims.
8. Mark natural product-link insertion points but never guess a product URL.

### Generate six images

- Generate exactly one featured image and five body images.
- Follow `references/visual-direction.md`.
- Lock each body image to a specific article section and reader decision before generation. Do not fill the package with generic kitchens or near-duplicate hood views.
- Build the featured source at an exact `2:1` ratio. Keep the complete hood crown, body, lower apron, cooktop or range, and the article's essential planning context inside the safe frame; never depend on Shopify to repair a vertical or tightly cropped composition.
- Default to exterior silhouette, finish, proportion, and craftsmanship. Do not show a cutaway, exposed internals, or invented engineering construction unless the operator explicitly requests a documented technical illustration.
- Reject malformed, unsafe, near-duplicate, or misleading generated images.
- Visually inspect all six source files before review and inspect the Shopify-rendered featured crop and five responsive body images after save.
- Disclose generated kitchens as design visualizations.
- Save accurate alt text for every image.

### Produce the review package

Create a topic-specific output directory containing:

- English Markdown article;
- complete Chinese Markdown article;
- Chinese Word review document;
- SEO title, description, handle, excerpt, tags, intent, cluster, funnel, and CTA;
- exactly six reviewed image files;
- local ERH-theme preview;
- Shopify-safe body HTML;
- source log, internal-link plan, publication manifest, and validation report.

Use the bundled scripts with the available cross-platform Python runtime. Prefer the workspace dependency runtime when available. On Windows, `py -3` or `python` may replace `python3`; do not make the operator run commands that Codex can run itself.

Present the article, Word document, SEO information, sources, images, preview, and validation result. Then wait.

## Action 2 — Human review

Apply requested content, source, image, SEO, link-placement, or layout revisions. Regenerate affected artifacts. Comments such as “可以” or “看起来不错” do not authorize publication.

Only the exact phrase `审核通过并发布` authorizes visible publication of the current reviewed package. Approval freezes the reviewed article, authority sources, and six images. Any material editorial change after approval returns to review.

For a narrowly scoped correction to an already published article, such as “replace the featured image” or “fix the crop,” change only the requested field. Preserve the verified article ID, body, body images, links, SEO fields, author, blog, template, and visibility unless the operator explicitly expands the scope. A correction never authorizes creation of a duplicate article.

## Action 3 — Automatic Shopify delivery

After `审核通过并发布`:

1. Read `references/shopify-browser-workflow.md` completely.
2. Reconfirm the current package, store `97256c-fc`, blog `News`, author `YMQ`, template, title, handle, and six reviewed images. Search by recorded Shopify article ID first, then exact handle and title. Update the verified article when it exists; never create a second article for the same package.
3. Discover current products from the storefront, product sitemap, or Shopify admin.
4. Open and verify at least two genuinely relevant live `https://eliterangehood.com/products/...` pages and record their visible H1 titles.
5. Insert at least two distinct contextual product links. Collections, pages, blogs, searches, previews, redirects, guessed URLs, and admin URLs do not count.
6. Style counted links exactly as `style="color:#000000;text-decoration:underline;"`.
7. Preserve reviewed authority sources unchanged.
8. Build and validate Shopify-safe HTML. Fix every validation error before any save.
9. Upload the one featured image and five body images through Shopify. Select by exact filename, verify the selected thumbnail and alt text before confirming, replace local placeholders with Shopify-hosted HTTPS URLs, and rerun validation.
10. Fill title, body, excerpt, author, blog, tags, SEO title, meta description, handle, template, and visibility.
11. Publish, save, reopen, and confirm that all fields persisted.
12. Open the public article; verify layout, six images, sources, product links, SEO handle, and mobile-readable flow. Confirm the `2:1` featured source renders without losing the hood crown, lower apron, cooking appliance, or other decision-critical content, and confirm body images keep their natural aspect ratios.
13. Click every counted product link and confirm the intended live product page.
14. Confirm the homepage `Blogs` module displays the new article normally.

Continue autonomously through Action 3. Stop only for login, password, 2FA, CAPTCHA, insufficient Shopify permission, unavailable browser control, or fewer than two relevant live product pages. Never weaken the product-link minimum.

## Validation and completion

Use:

- `scripts/build_review_docx.py` for Word review output when needed;
- `scripts/check_runtime.py` for first-run cross-platform dependency checks;
- `scripts/build_shopify_bundle.py` to build optimized WebP assets, preview, manifest, and initial HTML;
- `scripts/finalize_shopify_images.py` after Shopify provides hosted image URLs;
- `scripts/validate_blog_package.py` before Shopify save and again before publication.

Always report absolute artifact paths, validation results, verified product URLs, unchanged authority sources, Shopify article state, admin/public URLs, product-link click results, and homepage result. Never describe a local package or Hidden draft as published.
