# Security and operator handoff

## Included in the portable Skill

- Public ERH storefront and non-secret Shopify store identifiers.
- Fixed `News` destination, approved author, theme formatting, and homepage module.
- Research, writing, translation, SEO, image, product-link, layout, validation, upload, publication, and verification rules.
- Cross-platform scripts and Windows/macOS browser-control setup.

## Never include or request

- Shopify passwords, API keys, Admin API tokens, custom-app secrets, cookies, local storage, browser profiles, password-manager entries, or 2FA recovery data.
- The owner's authenticated Chrome state.
- OpenAI API keys. Operators use their own authenticated Codex/ChatGPT product session and installed tools.

## What each operator needs

1. A supported Windows or macOS desktop app with this Skill installed.
2. Chrome control enabled; Computer Use is an optional fallback.
3. An authorized Shopify staff account for Elite Range Hood.
4. A one-time Shopify sign-in in the same Chrome profile.

The Skill removes repeated store configuration; it cannot safely package authentication. Login, 2FA, CAPTCHA, and sensitive confirmations remain human steps.
