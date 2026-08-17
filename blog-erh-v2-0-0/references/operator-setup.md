# Operator setup for Windows and macOS

This is a one-time setup for each operator computer. The Skill already contains the fixed ERH store profile and does not require a Shopify custom app or API key.

## Install the Skill

Canonical repository: `https://github.com/vickyfobes-ops/Blog-ERH-V2.0.0`

Ask Codex to use `$skill-installer` with repository `vickyfobes-ops/Blog-ERH-V2.0.0`, path `blog-erh-v2-0-0`, branch `main`, and installation name `blog-erh-v2-0-0`.

The deterministic macOS/Linux installer command is:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo vickyfobes-ops/Blog-ERH-V2.0.0 \
  --path blog-erh-v2-0-0 \
  --ref main \
  --name blog-erh-v2-0-0
```

On Windows PowerShell, replace `python3` with `py -3` and `~` with `$env:USERPROFILE`. Alternatively, copy the complete folder to:

- Windows: `%USERPROFILE%\.codex\skills\blog-erh-v2-0-0`
- macOS: `~/.codex/skills/blog-erh-v2-0-0`

Restart the desktop app or start a new Codex task so the Skill appears.

## Enable Chrome control

1. Open the desktop app and select Codex, or ChatGPT Work.
2. Open **Plugins**, install **Chrome**, and enable it.
3. Follow the setup flow to install the official ChatGPT extension in Google Chrome.
4. Approve Chrome's permission prompts.
5. In Chrome, open **Extensions → Manage Extensions → ChatGPT → Details** and enable **Allow access to file URLs** so Shopify image uploads can use reviewed local files.
6. Use the same Chrome profile for Shopify and the ChatGPT extension.
7. In **Settings → Computer Use**, allow `admin.shopify.com` and `eliterangehood.com` when prompted. Prefer site-scoped permission over allowing every site.

Other Chromium browsers are not a substitute for the supported Google Chrome extension.

## Optional Computer Use fallback

Install **Plugins → Computer Use** and enable its server and skill toggles. This is a fallback when direct Chrome control is unavailable.

- Windows: keep Chrome visible on the active unlocked desktop; Computer Use takes over foreground mouse and keyboard input.
- macOS: approve Screen Recording and Accessibility when prompted.

## Shopify authentication

The operator must have an authorized Shopify staff account for store `97256c-fc`. Sign in once at `https://admin.shopify.com/store/97256c-fc` in the same Chrome profile. Complete password, 2FA, and CAPTCHA personally.

Never paste credentials, cookies, tokens, browser profiles, or recovery codes into Codex or the Skill.

## Connection test

Start a new Codex task and say:

```text
Use Chrome to open my signed-in Elite Range Hood Shopify admin and confirm the store name and store handle. Do not modify anything.
```

Successful read-only confirmation means browser control and authentication are ready. The normal command is:

```text
使用 $blog-erh-v2-0-0，选题是：How to Choose a Custom Range Hood
```

After reviewing the generated package, authorize publication only with:

```text
审核通过并发布
```
