---
name: blog-erh-v2-0-0
description: Create, rewrite, audit, illustrate, internally link, validate, and package source-backed English SEO blog articles for Elite Range Hood (ERH), including Shopify-ready local drafts. Use when a user asks for an ERH blog topic, content brief, buying guide, material or style article, range-hood images, SEO fields, internal-link plan, Word review copy, or Shopify blog draft. Default to local files only; never write to or publish on Shopify without explicit authorization for that exact action.
---

# Blog—ERH—V2.0.0

Create original, evidence-backed ERH articles that treat a custom range hood as ventilation equipment, an architectural proportion tool, and a handcrafted metal focal point.

## Operating boundary

- Default to research, planning, writing, image creation, validation, and local drafts.
- Do not create, update, or publish a Shopify article unless the user explicitly authorizes the exact online action.
- Keep Shopify output in `draft` state by default.
- Never store credentials, access tokens, or private customer data in the Skill or output bundle.
- Do not modify another Skill. Write only inside this Skill directory and the task's chosen output directory.

## Inputs

Accept a topic, product, collection, keyword, competitor reference, existing article, or content goal. Infer ordinary editorial details when evidence supports them. Ask only when a missing choice would materially change the article or authorize an external write.

Before drafting, establish:

- target reader and main question;
- primary keyword, search intent, cluster, and funnel stage;
- target ERH product, collection, samples, support, or contact page;
- requested deliverables and output directory;
- whether the user wants local review, Shopify-ready files, or an explicitly authorized Shopify action.

## Load memory progressively

Read only the references needed for the task:

- Read `references/brand-facts-and-guardrails.md` for every article.
- Read `references/content-model.md` when choosing a topic, checking cannibalization, planning structure, or building internal links.
- Read `references/source-audit.md` when using competitor material or looking for content gaps. Treat competitor pages as question and structure research only.
- Read `references/visual-direction.md` before creating or selecting article images.
- Read `references/shopify-output-contract.md` before producing Shopify HTML, a publication manifest, or any upload instructions.
- Read `references/mind-map.md` when planning a content system, pillar, cluster, roadmap, or operator memory.
- Use `assets/shopify-blog-draft.md` as the editable article-delivery template when a full draft package is requested.

## Workflow

### 1. Inspect and deconflict

Search the current workspace, ERH blog, and known URLs for the proposed intent. Prefer updating or consolidating an existing page when its primary question and likely search-result type substantially overlap. Record the cannibalization result in the brief.

### 2. Verify current facts

Browse the current ERH product, collection, ordering, sample, care, policy, and support pages used by the article. Recheck volatile facts at publication time, including product availability, materials, options, specifications, dimensions, price, lead time, warranty, code, and contact information.

For technical, health, safety, legal, code, or cost claims, use current primary sources such as the exact ERH liner/manual, a government or standards body, peer-reviewed research, or manufacturer documentation. State disagreements and product or jurisdiction dependence; never invent a universal number.

### 3. Create the brief first

Define:

- direct answer in one or two sentences;
- reader problem and unique ERH value;
- H2/H3 answer order;
- facts requiring verification and sources;
- one useful table, calculation, checklist, or decision aid when the intent supports it;
- image plan and disclosure language;
- three to seven contextual internal links;
- two to five reverse-link tasks from existing pages;
- one primary CTA.

### 4. Write original US English

- Answer the primary question within the first 100–150 words.
- Use one H1 in the source Markdown. Omit H1 from Shopify `body_html` because the theme renders the article title.
- Choose the article prototype that matches intent: technical guide, comparison, care, style, buying/value, or project case.
- Use short mobile-friendly paragraphs and semantic headings, tables, ordered steps, and lists.
- Write in a clear, professional, aesthetically informed voice without inflated sales language.
- Do not reuse a competitor's phrasing, examples, image concepts, or distinctive paragraph sequence.

### 5. Build contextual internal links

Verify that every target exists and is canonical before linking it. Usually include:

- one pillar or hub;
- one to three supporting articles;
- one relevant collection or verified product;
- one samples, ordering, contact, care, or support destination when useful.

Use descriptive anchors in the sentence where the next question arises. Avoid `click here`, repetitive exact-match anchors, and rows of unrelated commercial links.

### 6. Create or select visuals

Follow `references/visual-direction.md` exactly. For the default ERH editorial treatment:

- show full residential kitchen scenes with cabinetry, range, counters, lighting, and room proportion;
- emphasize exterior silhouette, metal finish, texture, straps, rivets, crowns, aprons, trim joints, and material coordination;
- use verified ERH product pages and approved ERH assets to understand the actual exterior design;
- never copy or reuse a competitor's image;
- do not create cutaways, cross-sections, exploded views, transparent shells, ducts, internal blowers, or fabricated installation anatomy unless the user explicitly asks for a technical diagram;
- identify generated scenes as design visualizations rather than customer-project photography;
- give every image factual, readable alt text without keyword stuffing.

### 7. Produce the local package

Create, as requested:

- complete English Markdown;
- metadata JSON with keyword, intent, cluster, funnel, SEO fields, sources, links, backlink tasks, and image plan;
- clean Shopify-safe HTML;
- six-image manifest with one featured image and five body images when using the V2 standard visual package;
- publication sheet and validation report;
- optional English Word review copy.

Use `scripts/build_shopify_bundle.py` to convert a conforming six-image Markdown article into HTML, WebP assets, and a publication manifest. Use `scripts/validate_blog_package.py` for deterministic package checks. These scripts validate formatting and package contracts; they do not replace editorial fact checking.

### 8. Run final QA

Confirm all of the following before calling the article publication-ready:

- opening directly answers the search intent;
- ERH claims match current verified pages or approved internal facts;
- volatile and high-risk claims have current primary sources;
- article is original and not a competitor rewrite;
- headings are logical and not repetitive;
- SEO title, meta description, handle, excerpt, tags, alt text, CTA, and source log exist;
- internal links resolve to intended ERH pages and backlink tasks are included;
- image identities, product references, disclosure, and captions are accurate;
- Shopify HTML contains no H1, scripts, Liquid, inline event handlers, unsafe URLs, or duplicate featured image;
- publication state remains local/draft unless the user explicitly authorizes an online write.

## Shopify authorization gate

Separate these actions:

1. Generate a local payload.
2. Create or update a Shopify draft.
3. Publish or schedule an article.

Authorization for one action does not imply authorization for the next. Before any online write, show or summarize the exact blog, handle, title, author, tags, featured image, and state. After an authorized write, reopen the article and verify the rendered title, images, links, table, FAQ, handle, and SEO fields.

## Required handoff

State what was created, where it was saved, what validations passed, which facts or links require human confirmation, and whether any Shopify write occurred. Never imply that a local draft was published.
