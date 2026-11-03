# Local package build

Use one output directory per article under the operator's current workspace. `SKILL_DIR` below means the installed Skill folder; `OUTPUT_DIR` means the article folder. Resolve both on the current computer. Run commands yourself; the operator supplies the topic, not JSON or shell commands.

## Inputs

- `<handle>.md`: English article with one H1, Markdown H2/H3 sections and verified contextual links. Include exactly three separate Markdown image paragraphs in order: featured, body 1, body 2. Use relative image paths and factual alt text.
- `<handle>.zh-CN.md`: complete meaning-matched translation with the same three image paths and product URL set.
- `images/`: one `1774 × 887` featured image and two `1536 × 1024` body images.
- `<handle>.meta.json`: actual researched values using the keys below, not the presentation-field names in the editorial Markdown template.

```json
{
  "finalH1": "",
  "primaryKeyword": "",
  "searchIntent": "",
  "cluster": "",
  "funnelStage": "",
  "primaryCTA": "",
  "seo": {
    "title": "",
    "metaDescription": "",
    "handle": "",
    "excerpt": "",
    "tags": []
  },
  "imageSourceType": "approved-real-project-photography",
  "internalLinks": [
    {"url": "", "anchor": "", "verified": false, "verifiedAt": "", "visibleH1": ""}
  ],
  "researchSources": [{"url": "", "title": "", "accessedAt": "", "supports": ""}],
  "backlinkPlan": [{"sourceUrl": "", "anchor": "", "insertionPoint": ""}],
  "imagePlan": [{"file": "", "purpose": "", "alt": "", "sourcePage": "", "usageBasis": ""}]
}
```

Populate at least two verified product-link records, two authority-source records and two proposed reverse-link tasks, plus exactly three image-plan records. Set `verified` to true only after opening and checking the live page. Keep image-plan filenames and alt text synchronized with the Markdown. For generated imagery, use the source type and disclosure specified in `v10-output-standard.md` and record the generation provenance instead of inventing a source page.

## Build order

Use the interpreter that passed `check_runtime.py`; substitute actual quoted paths and handle in these commands:

```text
python SKILL_DIR/scripts/build_shopify_bundle.py --source-dir OUTPUT_DIR --slug HANDLE
python SKILL_DIR/scripts/build_review_docx.py --source-dir OUTPUT_DIR
python SKILL_DIR/scripts/validate_blog_package.py --dir OUTPUT_DIR --slug HANDLE
python SKILL_DIR/scripts/render_review_docx.py OUTPUT_DIR/HANDLE.review.docx --output_dir OUTPUT_DIR/qa-en
python SKILL_DIR/scripts/render_review_docx.py OUTPUT_DIR/HANDLE.zh-CN.review.docx --output_dir OUTPUT_DIR/qa-zh
```

Inspect all rendered pages and the local theme preview. Keep the English source, translation, Word files and HTML synchronized when revising.

The initial Shopify HTML contains `SHOPIFY_IMAGE_2_URL` and `SHOPIFY_IMAGE_3_URL`; the preview resolves images locally. Explain this distinction in the delivery. Product links are already real clickable URLs. Only after authorized image upload, create a mapping JSON with these two keys and the actual Shopify image URLs, then run `finalize_shopify_images.py --dir OUTPUT_DIR --slug HANDLE --mapping-json MAPPING_FILE` and revalidate. Do not invent CDN URLs or upload just to remove placeholders from a local review package.
