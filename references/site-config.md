# Elite Range Hood Shopify site configuration

Verified through the user's logged-in Chrome session on 2026-08-14 (Asia/Shanghai). Reverify changing fields before an online write.

## Store identity

- Brand: Elite Range Hood
- Public primary domain: `https://eliterangehood.com`
- Shopify admin store handle: `97256c-fc`
- Shopify admin root: `https://admin.shopify.com/store/97256c-fc`
- Permanent Shopify domain: `97256c-fc.myshopify.com`
- Connected secondary domains observed: `artistryhood.com`, `www.artistryhood.com`, and `www.eliterangehood.com`
- Primary public domain observed in Shopify Domains: `eliterangehood.com`

## Blog destination

- Blog title: `News`
- Blog handle: `news`
- Storefront blog URL: `https://eliterangehood.com/blogs/news`
- Shopify blog-post manager: `https://admin.shopify.com/store/97256c-fc/content/articles`
- Approved author observed on current 2026 articles: `YMQ`
- Default theme template: `Default blog post`
- First-time configuration visibility: `Hidden`

Do not silently switch author, blog, or template. Reverify them in the article editor before saving.

## Live article format

Reference article: `https://eliterangehood.com/blogs/news/the-value-of-handmade-in-a-mass-produced-world`

- The theme renders breadcrumb, featured image, author/date, article title, share controls, footer metadata, and previous/next navigation.
- Desktop featured-image width observed: about 1140 px.
- Desktop body width observed: about 760 px.
- Article title is theme-rendered, not repeated in body HTML.
- Existing body section headings are H4; nested FAQ headings should use H5.
- Use plain `<p><img ...></p>` for body images; the current article pattern does not depend on `<figure>` or inline tables.
- Keep external authority sources in a final visible `Sources and Technical References` section.

## Homepage blog module

Verified at `https://eliterangehood.com/`.

- Module heading: `Blogs`
- Displays five recent News articles.
- Each card includes featured image, date/comments, H6 title, excerpt, and `Read more`.
- Module includes a `View More` link to `/blogs/news`.
- A Hidden draft must not appear here. After a publication, confirm that the new article enters the current five-card ordering and that its image, title, excerpt, and link render.

## Verified product-detail links

Verified in Chrome on 2026-08-14. Reopen the two or more selected for each article immediately before publication.

1. `https://eliterangehood.com/products/elite-chicago-classic-custom-brass-range-hoods-el1-b01`
   - Product H1: `ELITE Chicago Brass Minimalist Vent Hoods for Kitchens EL1-B01`
2. `https://eliterangehood.com/products/elite-houston-luxury-curved-brass-kitchen-range-hoods-el7-b02`
   - Product H1: `ELITE Houston Luxury Curved Brass Kitchen Range Hoods EL7-B02`
3. `https://eliterangehood.com/products/elite-retro-non-direction-antique-brass-range-hoods-el5-b03`
   - Product H1: `ELITE Retro Non-direction Antique Brass Kitchen Exhaust Hood EL5-B03`

These are seed references, not a permanent product whitelist. Choose products that are genuinely relevant to the topic and current catalog.

## Publication gates

- Online test during first configuration: Hidden draft only.
- Normal publication phrase: exactly `审核通过并发布`.
- API keys and passwords: never requested or used.
- Allowed browser: the user's currently logged-in Chrome Shopify session.
- Stop conditions: login, 2FA, insufficient permissions, CAPTCHA confirmation, or fewer than two relevant live product pages.
