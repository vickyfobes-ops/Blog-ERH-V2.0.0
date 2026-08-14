# Shopify browser workflow

## Browser and authorization

Use the user's current logged-in Chrome session. Never inspect or export cookies, local storage, passwords, API keys, tokens, or private customer data. If Shopify shows login or 2FA, let the user complete it in Chrome. Ask before solving any CAPTCHA.

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

## Image upload

Upload only the six reviewed article images. Use one featured image and five Shopify-hosted body images. Record the resulting Shopify URLs in the publication manifest. Never leave local paths or `SHOPIFY_IMAGE_*_URL` placeholders in saved body HTML.

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
