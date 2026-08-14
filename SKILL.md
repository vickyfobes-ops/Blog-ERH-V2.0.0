---
name: blog-erh-v2-0-0
description: Generate, review, illustrate, internally link, upload, and verify source-backed English Shopify blog posts for Elite Range Hood (ERH). Use when the user invokes $blog-erh-v2-0-0, supplies an English ERH blog topic, requests an English formal article with a Chinese Word review copy and six images, or says “审核通过并发布” for the reviewed ERH package. Use the user's logged-in Chrome Shopify session, never API keys or passwords. Create hidden drafts by default and publish only after the exact approval phrase.
---

# Blog—ERH—V2.0.0

Create original ERH blogs that are ready for the live Elite Range Hood theme, while keeping research, review, Shopify drafting, and publication as separate states.

## Non-negotiable boundaries

- Work only for `eliterangehood.com` and the Shopify store recorded in `references/site-config.md`.
- Do not modify Blog—FSE—V3.0.0 or any other Skill.
- Use the user's currently logged-in Chrome session for Shopify. Do not request or store a Shopify API key, password, cookie, token, or 2FA code.
- Stop only for Shopify login, 2FA, insufficient permission, CAPTCHA confirmation, or a genuine inability to find two relevant live ERH product pages.
- Never publish or schedule without the exact user phrase `审核通过并发布` for the current reviewed package.
- First-time configuration and any ordinary unapproved online test must remain `Hidden`.
- Do not edit a different existing Shopify article unless the user explicitly identifies and authorizes it.

## Load memory

Read these for every run:

- `references/site-config.md`
- `references/brand-facts-and-guardrails.md`
- `references/shopify-output-contract.md`

Read as needed:

- `references/content-model.md` for topic choice, cannibalization, clusters, or links.
- `references/source-audit.md` for competitor research; never use it as ERH product truth.
- `references/visual-direction.md` before generating or selecting images.
- `references/shopify-browser-workflow.md` before any Shopify browser action.
- `references/mind-map.md` for strategy, roadmap, or system memory.
- `assets/shopify-blog-draft.md` for the standard delivery structure.

## Operator workflow

### Action 1 — Receive one English topic

Accept a plain English topic after `$blog-erh-v2-0-0`. Infer audience, intent, cluster, funnel, and primary CTA from current evidence. Ask only when a missing choice would materially change the article.

Before writing:

1. Search existing ERH articles and workspace topics for intent overlap.
2. Verify current ERH product facts and relevant product detail pages.
3. Verify volatile, technical, health, safety, code, cost, policy, and specification claims with current primary sources.
4. Prepare the brief, outline, link plan, reverse-link plan, source plan, and six-image plan.

### Action 2 — Produce the review package and wait

Create all of these before asking for approval:

- one formal US-English article;
- one Chinese `.docx` review copy containing the translated article, SEO fields, image captions, source notes, and review status;
- SEO title, meta description, handle, excerpt, tags, intent, cluster, funnel, and CTA;
- exactly six relevant images: one featured image and five body images;
- a local ERH-theme preview and Shopify-safe body HTML;
- a publication manifest and deterministic validation report.

The English article must directly answer the search intent in its first 100–150 words. Generated kitchens must be disclosed as design visualizations. Keep external authority links in a visible `Sources and Technical References` section. Customer-facing body links should prioritize ERH destinations.

At the end of Action 2, report the files and wait. Do not interpret comments, revisions, or “looks good” as publication approval.

### Action 3 — Exact approval phrase

Only `审核通过并发布` authorizes publication of the currently reviewed package.

After that phrase:

1. Reopen `references/site-config.md` and the reviewed manifest.
2. Reverify the store, `News` blog, article handle, author, featured image, visibility, and at least two relevant live ERH product detail pages.
3. Add or confirm at least two contextual links whose targets are `/products/...` pages on `eliterangehood.com`. Do not count collection, page, or blog URLs as product links.
4. Render each product link black and underlined using exactly `style="color:#000000;text-decoration:underline;"` unless the live theme configuration recorded in site memory provides an approved equivalent.
5. Upload the six images to Shopify, replace all body-image placeholders with Shopify-hosted URLs, and run final HTML/link checks.
6. Set the approved author and `News` blog. Confirm the article is the reviewed package, then make it visible and save.
7. Reopen the public article and verify the title, featured image, five body images, headings, sources, FAQ when present, product links, SEO handle, and mobile-readable flow.
8. Open every inserted product link and confirm it lands on the intended live product detail page.
9. Verify the homepage `Blogs` module shows the new article normally. If the homepage module has a fixed five-card limit, confirm the new article appears in the current ordering.

Do not leave a partially published article without reporting its exact state and URL.

## Shopify hidden-draft test

When the user explicitly requests first-time configuration testing, an online write is authorized only as a Hidden draft:

- upload the six approved test images;
- create a new post in the configured `News` blog;
- select the approved author recorded in site memory;
- set Visibility to `Hidden` before saving;
- save, reopen, and verify the draft fields and preview when Shopify provides one;
- verify that the hidden draft does not appear in the public homepage `Blogs` module;
- record the Shopify article ID, admin URL, visibility, and test time locally.

This test does not authorize publication.

## Writing and originality

- Use natural professional American English and short mobile-friendly paragraphs.
- Treat the hood as ventilation equipment, an architectural proportion tool, and handcrafted metalwork.
- Use one H1 in Markdown; omit H1 from Shopify body HTML because the theme renders the article title.
- Match the live ERH body hierarchy recorded in site memory: Markdown H2 → Shopify H4, Markdown H3 → Shopify H5.
- Do not copy a competitor's wording, examples, distinctive sequence, product facts, images, or layouts.
- Do not invent ERH dimensions, metal grades, CFM, noise, price, lead time, warranty, certification, origin, mounting, or care claims.

## Images

Follow `references/visual-direction.md`. Default to rich residential interiors and exterior form or craftsmanship. Do not create cutaways, transparent shells, internal blowers, ducts, exploded assemblies, or fabricated engineering anatomy. Use current ERH pages to understand exterior geometry; never present a generated scene as customer photography or an exact installed SKU.

## Package and validation

Use `scripts/build_shopify_bundle.py` to build the theme-aligned HTML, six WebP assets, local preview, and manifest. Use `scripts/finalize_shopify_images.py` after Shopify returns image URLs. Use `scripts/validate_blog_package.py` before any Shopify save and again before publication.

The validator supplements, but does not replace, fact checking and visual inspection.

## Required handoff

Always state:

- files created and their absolute paths;
- validation results;
- verified product URLs;
- Shopify article state: local only, Hidden draft, Visible, or scheduled;
- whether a Shopify write occurred;
- draft/admin/public URL when available;
- any homepage or product-link verification result.

Never describe a local package or Hidden draft as published.
