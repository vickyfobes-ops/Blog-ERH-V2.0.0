# Shopify browser workflow

## Browser and authorization

Use the user's current logged-in Chrome session. Prefer the Chrome plugin/browser-control surface. If direct Chrome control is unavailable but Computer Use is installed, use Computer Use to operate Chrome visually. Never inspect or export cookies, local storage, passwords, API keys, tokens, or private customer data. If Shopify shows login or 2FA, let the user complete it in Chrome. Ask before solving any CAPTCHA.

This workflow is platform-neutral:

- On Windows, keep Chrome visible on the active unlocked desktop while Computer Use runs; it occupies foreground mouse and keyboard input.
- On macOS, grant the Screen Recording and Accessibility permissions requested by Computer Use.
- With direct Chrome control, use the same Chrome profile where the ChatGPT extension and Shopify login are active.
- Enable the extension's file-URL access before uploading reviewed local images.

If neither browser route is available, stop before Shopify and follow `operator-setup.md`. Do not substitute API keys or claim a write occurred.

Treat these as three separate permissions:

1. Local package generation.
2. Hidden Shopify draft creation or update.
3. Visible publication or scheduling.

The exact phrase `审核通过并发布` grants step 3 only for the currently reviewed package. A request for a blog, Shopify HTML, or a draft does not grant publication.

## Preflight inspection

Before a Shopify write, visibly confirm:

- admin store handle `97256c-fc` and store name `Elite Range Hood`;
- blog `News` and handle `news`;
- author `YMQ`, unless the user approved another public author;
- theme template `Default blog post`;
- handle does not collide with another article;
- six final WebP images and accurate alt text;
- at least two live, relevant `eliterangehood.com/products/...` destinations;
- body HTML has no H1, scripts, Liquid, iframe, event handlers, or unresolved image placeholders.
- the featured file is exactly `2:1`, the five body images have no fixed HTML dimensions, and all six passed full-frame visual QA;
- whether the package already has a recorded Shopify article ID or an existing exact handle/title match.

## Create-versus-update guard

Search in this order before opening **Add blog post**:

1. Recorded Shopify article ID and admin URL in the publication manifest.
2. Exact handle in the News blog.
3. Exact title in the Shopify article manager.

If any verified match represents the same package, reopen and update that article. Never create a duplicate to repair an image, crop, link, excerpt, or SEO field. If different records appear to share the handle or intent, stop before writing and report the collision.

For a scoped correction to a published article, record the permitted fields before editing. Change only those fields and confirm that body HTML, five body-image URLs, links, SEO, author, blog, template, and visibility remain unchanged unless the operator explicitly requested otherwise.

## Image upload

Upload only the six reviewed article images. Use one featured image and five Shopify-hosted body images. Choose each upload by its exact filename or direct local path; before selecting **Done**, confirm the selected checkbox, thumbnail, filename, and alt text so an adjacent media item cannot be substituted. Record the resulting Shopify URLs in the publication manifest. Never leave local paths or `SHOPIFY_IMAGE_*_URL` placeholders in saved body HTML.

The featured source must be exact `2:1`. The five body-image tags must omit fixed `width` and `height` attributes so the theme can render them responsively with natural height.

## Hidden draft test

1. Open Content → Blog posts → Add blog post.
2. Fill title and HTML body.
3. Add the excerpt.
4. Upload/select the featured image and verify its alt text.
5. Set author `YMQ`, blog `News`, tags, and `Default blog post`.
6. Edit the search-engine listing with the reviewed SEO title, description, and handle.
7. Set Visibility to `Hidden` before Save.
8. Save once, then reopen the new article by its Shopify article ID.
9. Verify title, blog, author, hidden state, featured image, body images, product links, sources, and SEO fields.
10. Confirm the public homepage `Blogs` module does not display the hidden draft.

Record the article ID and admin URL. Do not make it visible.

## Approved publication

After `审核通过并发布`:

1. Reverify the exact reviewed package and all publication fields.
2. Reverify at least two relevant live product pages.
3. Confirm the final body includes two or more contextual product links styled `color:#000000;text-decoration:underline;`.
4. Upload/resolve all six images and rerun package validation.
5. Set Visibility to `Visible` only after all fields are correct.
6. Save and wait for Shopify's success state.
7. Open the public article, not only the admin editor.
8. Click every inserted product link and confirm the intended product H1.
9. Check the public homepage `Blogs` module for the new article card.
10. Compare the source and rendered featured image. Confirm that the hood crown, exterior body, lower apron, cooking appliance, and article-specific planning context remain visible. Confirm that every body image is undistorted and uncropped.

If the public post is incorrect, report the live state immediately. Do not delete or overwrite another post as an attempted repair.

## Completion evidence

Capture locally:

- store, blog, author, and template;
- article ID and admin URL;
- hidden/visible state;
- final public URL when visible;
- verified product URLs and visible product H1s;
- homepage module result;
- time of verification;
- validation report path.
