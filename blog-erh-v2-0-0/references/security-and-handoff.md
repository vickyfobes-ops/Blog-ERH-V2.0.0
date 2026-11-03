# Security and operator handoff

## Included in the portable Skill

- Public Elite Range Hood storefront and non-secret Shopify store identifiers.
- Fixed `News` destination, approved author, theme formatting, and homepage module.
- Research, writing, translation, SEO, image, product-link, layout, validation, upload, publication, and verification rules.
- Cross-platform scripts and Windows/macOS browser-control setup.
- The V10 local-output contract: linked English Word and Shopify HTML plus one featured and two body images.

## Never include or request

- Shopify passwords, API keys, Admin API tokens, custom-app secrets, cookies, local storage, browser profiles, password-manager entries, or 2FA recovery data.
- The owner's authenticated Chrome state.
- OpenAI API keys. Operators use their own authenticated Codex/ChatGPT product session and installed tools.

## What each operator needs

1. A Codex environment with local Skill, file and command support, plus internet research access.
2. Python 3.10+ with the packages in `requirements.txt` (prefer the bundled workspace runtime), and DOCX rendering for visual QA.
3. Only for an authorized online action: Chrome control or Computer Use, an authorized Shopify staff account, and a Shopify sign-in on that computer.

The Skill removes repeated store configuration; it cannot safely package authentication. Login, 2FA, CAPTCHA, and sensitive confirmations remain human steps.
