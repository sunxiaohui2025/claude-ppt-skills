# Dune Keynote Slide

一个用于生成高端宣讲风格 HTML PPT 的 Codex Skill。

它适合把大纲、笔记、Markdown、粗略想法或技术材料，转换成一套可以直接演示的 HTML 幻灯片。默认视觉风格是「沙丘色」：暖米色背景、陶土主色、克制动效、大标题叙事、宽松留白，整体更接近发布会 / Keynote / 技术宣讲，而不是传统 PPT 模板。

## 效果图
### 基础风格效果
<img width="1427" height="701" alt="截屏2026-05-28 10 23 35" src="https://github.com/user-attachments/assets/0dc4eaa9-8799-438a-b777-b8d6d1dac842" />

### 缩略图效果
<img width="1422" height="700" alt="截屏2026-05-28 10 24 13" src="https://github.com/user-attachments/assets/ff0fdf09-9a56-478f-a19b-d4c18fe1d711" />

### html格式编辑
<img width="1432" height="703" alt="截屏2026-05-28 10 24 33" src="https://github.com/user-attachments/assets/60a78fd2-0986-4fe7-abec-af958721b5a9" />


## 这个 Skill 解决什么问题

它希望解决 AI 生成 PPT 时常见的几个问题：

- 页面像传统办公 PPT，不够高级。
- 内容硬塞在一页里，字号越来越小。
- 连续多页都是卡片或列表，视觉疲劳。
- 章节页、封面页、结尾页没有舞台感。
- HTML PPT 生成后缺少稳定的快捷键、缩略图和编辑能力。
- 不同智能体生成时容易改坏运行时代码，导致黑屏或保存失败。

这个 Skill 的核心目标是：让 AI 不只是“把内容放进页面”，而是先判断内容主角，再选择合适版式，并通过标准模板生成稳定可维护的 HTML PPT。

## 核心能力

- 生成高端沙丘色宣讲风格 HTML PPT。
- 支持模块化源文件，便于后续维护和二次编辑。
- 内置标准运行时，支持翻页、缩略图、全屏、编辑模式。
- 根据内容自动选择版式：封面、章节、目录、卡片、图文、对比、流程、时间轴、层级、图表、结论、封底等。
- 自动执行信息减法：内容过多时拆页，而不是压缩到看不清。
- 避免连续多页重复使用同一种卡片 / 目录 / 列表版式。
- 章节页采用 Cinematic Section 风格，更像镜头切换。
- 支持未来扩展多种视觉风格，不需要重写生成流程。
- 内置校验脚本，避免生成缺少运行时、缺少数据源、JS 双重转义等问题的坏文件。

## 默认设计风格

默认风格：`dune` 沙丘色。

核心色彩：

- 背景色：`#fbf7ef`
- 主色调：`#a8553d`
- 正文色：深墨色 / 暖黑色
- 整体气质：高级、克制、宽松、建筑感、适合投屏宣讲

设计原则：

- 每页只表达一个主观点。
- 标题要大，重点词用主色突出。
- 上下左右要有足够留白，贴近 16:9 安全内容区。
- 封面、章节页、结尾页可以有更明显的舞台感和动效。
- 内容页动效要克制，优先保证清晰、稳定、可读。
- 发现内容太多时，优先拆页，不要硬塞。
- 避免连续多页都是卡片、目录或普通列表。

## 目录结构

```text
dune-keynote-slide/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── html-template/
│       ├── base.css
│       ├── index.template.html
│       └── runtime.js
├── references/
│   ├── dune-style-guide.md
│   ├── layout-library.md
│   └── style-packs/
│       └── dune.md
└── scripts/
    ├── merge_deck.py
    ├── serve_editor.py
    └── validate_deck_contract.py
```

重点文件说明：

- `SKILL.md`：Skill 的核心使用规范，告诉智能体如何生成 PPT。
- `assets/html-template/`：标准 HTML 模板、基础样式和运行时代码。
- `references/dune-style-guide.md`：沙丘色视觉规范。
- `references/layout-library.md`：各种页面版式的选择规则和结构示例。
- `references/style-packs/dune.md`：默认风格包，后续可参考它扩展新风格。
- `scripts/merge_deck.py`：把单页源文件合并成最终 `index.html`。
- `scripts/serve_editor.py`：本地编辑保存服务。
- `scripts/validate_deck_contract.py`：生成结果校验脚本。

## 生成后的 PPT 结构

一个生成后的 PPT 项目应该长这样：

```text
my-deck/
├── index.html
└── sources/
    ├── outline.md
    ├── style.css
    ├── deck.config.json
    ├── slide-01.html
    ├── slide-02.html
    └── slide-NN.html
```

说明：

- `sources/slide-XX.html` 是每一页幻灯片的源文件。
- `sources/style.css` 是当前 PPT 的补充样式。
- `sources/deck.config.json` 存放标题等配置。
- `index.html` 是最终可打开、可演示的完整 HTML PPT。

智能体应该只编写 `sources/` 里的文件，最终的 `index.html` 必须由 `merge_deck.py` 生成。

## 基础使用方式

创建一个 PPT 目录：

```bash
mkdir -p my-deck/sources
```

创建 `sources/deck.config.json`：

```json
{
  "title": "AI 技术战略分享"
}
```

创建第一页 `sources/slide-01.html`：

```html
<section class="slide layout-cover" data-slide-id="slide-01" data-source="sources/slide-01.html">
  <div class="slide-stage">
    <div class="cover-copy">
      <p class="eyebrow">TECH STRATEGY</p>
      <h1>AI 正在改变企业的<span>运行方式</span></h1>
      <p class="subtitle">从工具升级，到流程重构，再到组织协同方式的变化。</p>
    </div>
  </div>
</section>
```

合并生成最终 PPT：

```bash
python3 dune-keynote-slide/scripts/merge_deck.py my-deck
```

打开预览：

```bash
open my-deck/index.html
```

## 生成约束

为了保证生成结果稳定，必须遵守以下约束：

- 不要手写最终的 `index.html`。
- 不要替换标准运行时、缩略图、编辑工具栏、底部进度条和快捷键逻辑。
- 智能体只能生成或修改 `sources/slide-XX.html`、`sources/style.css`、`sources/outline.md`、`sources/deck.config.json`。
- 最终 PPT 必须通过 `scripts/merge_deck.py` 合并。
- 合并后必须通过 `scripts/validate_deck_contract.py` 校验。
- 每一页都要判断内容主角：标题、图片、流程、数据、对比、层级、卡片、时间轴或结论。
- 内容太多时必须拆页，不能通过无限缩小字号硬塞。
- 章节页只能放章节编号、标题、一句短副标题和淡色动态图标，不要塞证明材料、列表或卡片。
- 不要连续超过两页使用相似的卡片 / 列表 / 目录型版式。
- 封面、章节页、封底可以更有动效，普通内容页要克制。

## 快捷键

生成后的 HTML PPT 支持以下快捷键：

| 快捷键 | 功能 |
| --- | --- |
| `ArrowRight`、`PageDown`、`Space` | 下一页 |
| `ArrowLeft`、`PageUp` | 上一页 |
| `O` | 打开缩略图预览 |
| `E` | 进入当前页编辑模式 |
| `F` | 全屏 |
| `Esc` | 退出全屏、缩略图或编辑模式 |
| `Cmd/Ctrl + S` | 编辑模式下保存当前页 |

## 编辑模式

按 `E` 可以进入编辑模式。

当前编辑模式不是完整 PowerPoint 编辑器，而是一个轻量、可控的 HTML PPT 编辑器。它支持常用的演示稿微调能力：

- 选择标题、段落、列表项、卡片、面板、标签、节点等元素。
- 修改字号、加粗、颜色、对齐方式、行高。
- 插入或清除换行。
- 调整元素宽度、高度、内边距。
- 设置文字不换行。
- 复制或删除选中元素。
- 复制、删除或强调选中的容器。
- 按住 `Alt / Option` 拖拽移动元素。
- 使用方向键微调元素位置。

保存逻辑：

1. 如果通过 `scripts/serve_editor.py` 启动，本地服务会把当前页保存回 `sources/slide-XX.html`。
2. 如果直接用 Chrome / Edge 打开 HTML，可以通过 File System Access API 授权访问文件夹后保存源文件。
3. 如果浏览器或环境不支持保存，会显示明确提示。

启动本地编辑服务：

```bash
cd my-deck
python3 ../dune-keynote-slide/scripts/serve_editor.py 8765
```

然后打开：

```text
http://127.0.0.1:8765/index.html
```

## 版式系统

这个 Skill 不是简单套卡片，而是根据内容语义选择版式。

常见版式包括：

- 封面页。
- 目录页。
- 章节页。
- 纯文字页。
- 一句话观点页。
- 图文组合页。
- 单大图页。
- 图标文字页。
- 双卡片、三卡片、四宫格、多列列表。
- 左右对比、优劣对比、新旧对比、多维对比。
- 横向时间轴、纵向时间轴、步骤流程、循环闭环。
- 总分结构、树状层级、中心辐射、嵌套层级、系统图。
- 柱状图、饼图、折线图、组合图表。
- 问题对策、目标规划、观点结论、致谢封底。

详细版式规则见：`references/layout-library.md`。

## 校验

校验整个 PPT 目录：

```bash
python3 dune-keynote-slide/scripts/validate_deck_contract.py my-deck
```

校验单个 HTML 文件：

```bash
python3 dune-keynote-slide/scripts/validate_deck_contract.py my-deck/index.html
```

校验内容包括：

- 是否包含标准运行时代码。
- 是否包含缩略图预览能力。
- 是否包含编辑工具栏。
- 是否包含底部页码、进度条和翻页按钮。
- 每页是否包含 `data-source` 和 `data-slide-id`。
- 每页是否包含且只包含一个 `.slide-stage`。
- 是否误用了旧版 `.stage` 容器。
- 首页动态图标是否使用了危险定位方式。
- 最终 JS 是否出现了被错误转义的模板字符串，比如 `\`` 或 `\${...}`。
- 最终 JS 是否出现了双重转义的正则语法。

## 多风格扩展

这个 Skill 支持未来扩展多种风格。

新增风格建议放在：

```text
references/style-packs/
```

例如：

```text
references/style-packs/midnight.md
references/style-packs/pearl.md
references/style-packs/jade.md
```

每个风格包建议定义：

- 颜色 Token。
- 字体气质。
- 封面图形 / 章节图形 / 结尾图形。
- 卡片、标签、图表和结构图样式。
- 动效预算。
- 禁止使用的视觉模式。

注意：新增风格应该只改变视觉语言，不要改变生成契约和运行时结构。

## 推荐工作流

```bash
# 1. 生成或修改模块化源文件
$EDITOR my-deck/sources/slide-01.html

# 2. 合并成最终 HTML PPT
python3 dune-keynote-slide/scripts/merge_deck.py my-deck

# 3. 校验生成结果
python3 dune-keynote-slide/scripts/validate_deck_contract.py my-deck

# 4. 打开预览
open my-deck/index.html

# 5. 可选：启动本地编辑保存服务
cd my-deck
python3 ../dune-keynote-slide/scripts/serve_editor.py 8765
```

## 当前限制

- 它是 HTML PPT 生成系统，不是完整 PowerPoint 替代品。
- 编辑模式是轻量编辑，不做复杂多选、自由 CSS 编辑或完整富文本编辑器。
- 不包含 QA 自动化、图片生成、联网搜索或大型外部依赖。
- 复杂页面结构调整建议直接改 `sources/slide-XX.html` 和 `sources/style.css`，然后重新合并。

## 发布前建议

提交 GitHub 前建议补充：

- `LICENSE`：选择你希望使用的开源协议。
- 示例 Deck：可以放一个 `examples/` 目录，展示生成效果。
- 截图：可以在 README 里加入封面页、章节页、缩略图模式、编辑模式截图。

## License

请在发布前补充你的开源协议。
