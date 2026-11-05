# Elite Range Hood 博客 Skill

在另一台电脑的 Codex 中安装 `blog-erh-v2-0-0` 后，输入选题即可研究并生成带内链的英文 Word、Shopify HTML、中文审阅稿和 V10 标准三张图片。规则、模板和脚本都在本仓库；不需要原作者电脑上的文件或历史对话。

当前交接修订版：`2026.11.04`（见 Skill 内 `release.json`）。安装名保持不变；更新时可直接覆盖旧版并保留备份。

## 复制一句话安装或更新

把下面整句发给 Codex。未安装时安装；已安装时备份旧版并更新：

```text
请使用 $skill-installer 从 https://github.com/vickyfobes-ops/Blog-ERH-V2.0.0 的 main 分支安装 blog-erh-v2-0-0；若已安装，先下载到临时目录，再运行新版 scripts/install_local.py --replace 备份并更新，完成后验证安装。
```

安装完成后，在下一条消息调用，不需要重复安装：

```text
使用 $blog-erh-v2-0-0，选题是：How to Choose a Custom Range Hood。输出带内链的英文 Word、Shopify HTML 和 V10 标准图片。
```

将示例选题换成自己的选题即可。安装器不支持直接覆盖已存在目录，所以更新时使用临时下载加备份安装的方式。旧版保留在 Codex 配置目录下的 `skill-backups`，不参与 Skill 自动发现。

## 用 ZIP 安装

将安装包发给对方，解压后把所在文件夹交给 Codex，并说：

```text
请安装这个文件夹中的 blog-erh-v2-0-0，运行其中的 scripts/install_local.py --replace；已有版本先备份，完成后验证安装。
```

完整交接包还提供 `Install-macOS.command` 和 `Install-Windows.cmd`，可双击安装；建议先复制到本地再运行。安装前会核验包内文件哈希，重复安装完全相同的版本会直接通过。安装脚本会忽略移动硬盘和网络盘产生的 `._*` 元数据文件。

也可在解压目录的终端手动运行：

- macOS：`python3 blog-erh-v2-0-0/scripts/install_local.py --replace`
- Windows PowerShell：`py -3 blog-erh-v2-0-0/scripts/install_local.py --replace`

脚本默认安装到 `$CODEX_HOME/skills/blog-erh-v2-0-0`；未设置 `CODEX_HOME` 时使用用户目录下的 `.codex/skills/blog-erh-v2-0-0`。安装脚本只需 Python 标准库。

## 输入选题后得到什么

- `<handle>.review.docx`：完整英文正文、三张图、可点击的内链与来源。
- `<handle>.shopify.html`：符合 V10 的 Shopify 正文，产品内链与 Word 一致。
- 中文 Markdown 和 Word 审阅稿、SEO 信息、来源与内链核验记录。
- 一张 `1774 × 887` 封面、两张 `1536 × 1024` 正文图，优先选用获准使用的品牌真实项目摄影，并保留产品比例。
- 本地网页预览、图片文件和验证报告。

图片尚未上传 Shopify 时，Shopify HTML 中的图片地址保留为待替换标记；本地预览和 Word 可查看完整图片。上传后才生成含 Shopify CDN 图片地址的最终 HTML。产品内链在本地交付阶段就已插入。

## 运行条件

对方需要可使用本地 Skill、文件和命令工具的 Codex，以及联网研究能力。文章生成脚本需要 Python 3.10+、Pillow 和 python-docx；优先使用 Codex 内置运行环境，缺失时由 Codex 按包内说明创建独立环境。Word 逐页检查需要文档渲染能力。只有使用 AI 配图回退方案时才需要图像生成工具。

生成本地文件不需要 Shopify 登录。只有要求上传或发布时，才需要对方自己登录有权限的 Shopify 账户；发布仍需对当前稿件明确说“审核通过并发布”。

详细说明：[跨电脑配置](blog-erh-v2-0-0/references/operator-setup.md) · [V10 输出标准](blog-erh-v2-0-0/references/v10-output-standard.md)。

## 维护者打包

在干净的已提交仓库中运行 `python3 tools/package_handoff.py --output <新建交付目录>`，生成完整 Skill、双系统安装入口、中文交接说明、ZIP 和 SHA-256 校验文件。内部交接可额外传入 `--reference-dir <原始V10文章目录>`，将已批准的 HTML、Word 和三张图按原样附入包内；这些内部样例不会自动加入 GitHub。
