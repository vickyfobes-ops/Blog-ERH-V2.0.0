# Operator setup for Windows and macOS

This is a one-time setup for each operator computer. The Skill already contains the fixed Elite Range Hood store profile and does not require a Shopify custom app or API key.

## Install the Skill

Canonical repository: `https://github.com/vickyfobes-ops/Blog-ERH-V2.0.0`

Ask Codex to use `$skill-installer` with repository `vickyfobes-ops/Blog-ERH-V2.0.0`, path `blog-erh-v2-0-0`, branch `main`, and installation name `blog-erh-v2-0-0`.

Resolve the bundled `$skill-installer` script from its installed location rather than assuming a fixed app path. A default macOS command is:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo vickyfobes-ops/Blog-ERH-V2.0.0 \
  --path blog-erh-v2-0-0 \
  --ref main \
  --name blog-erh-v2-0-0
```

On Windows PowerShell, the equivalent default command is:

```powershell
py -3 "$env:USERPROFILE/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" --repo vickyfobes-ops/Blog-ERH-V2.0.0 --path blog-erh-v2-0-0 --ref main --name blog-erh-v2-0-0
```

If `CODEX_HOME` is configured, resolve the installer and destination from that directory instead. The standard installer refuses an existing destination. For an update, use the standard installer with `--dest` pointing at a new temporary directory, then run the downloaded `blog-erh-v2-0-0/scripts/install_local.py --replace`. It validates the new package before moving the old version to `skill-backups` outside the discovered `skills` folder, and restores the old version if activation fails. Never delete the old directory first.

For an extracted ZIP, run `python3 blog-erh-v2-0-0/scripts/install_local.py --replace` (Windows: `py -3` in place of `python3`). The script supports a custom skills parent through `--dest`. Default destinations:

- Windows: `%USERPROFILE%\.codex\skills\blog-erh-v2-0-0`
- macOS: `~/.codex/skills/blog-erh-v2-0-0`

The full handoff ZIP also provides `Install-macOS.command` and `Install-Windows.cmd`, with package integrity verification before installation. Copy the extracted folder to a local disk first. Identical reinstalls do not create duplicate backups; `._*` transfer metadata is ignored. Read `release.json` to identify the installed package revision.

The Skill is available on the next Codex turn. If the current task still shows stale instructions, start a new task. Use the invocation alone after installation; do not repeatedly run the installation prompt.

For local generation only, no Shopify login or browser plugin is required. After entering one topic, the Skill can produce the linked English Word document, linked Shopify HTML, Chinese review copy, and V10 three-image package locally. The remaining browser setup is needed only for an explicitly authorized Shopify upload or publication.

## Local runtime

1. Locate the workspace dependency Python runtime when provided by Codex. Run `scripts/check_runtime.py` with that interpreter before generation.
2. If it is unavailable or lacks packages, create `.venv-erh` inside the article workspace using Python 3.10+ and install the Skill's `requirements.txt` there. Do not install dependencies globally.
3. On macOS use `python3 -m venv .venv-erh`, then `.venv-erh/bin/python -m pip install -r <installed-skill>/requirements.txt`. On Windows use `py -3 -m venv .venv-erh`, then `.venv-erh/Scripts/python.exe -m pip install -r <installed-skill>/requirements.txt`.
4. Re-run `check_runtime.py` with that interpreter. If Python is absent, state that concrete missing prerequisite.
5. Use `references/local-build.md` for the data contract and build order. All input images are local files within the article output folder; no path on the author's computer is needed.

The bundled Word builder works without a documents plugin. Visual QA still needs a DOCX renderer (prefer the available documents skill); `scripts/render_review_docx.py` accepts `CODEX_DOCUMENT_RENDERER` for a renderer installed outside its default discovery path. If rendering is unavailable, report visual QA as incomplete instead of claiming it passed.

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

Expected local primary outputs are `<handle>.review.docx` and `<handle>.shopify.html`, with the same verified contextual product links and one `2:1` featured image plus two `3:2` body images.

After reviewing the generated package, authorize publication only with:

```text
审核通过并发布
```
