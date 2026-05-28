---
name: dune-keynote-slide
description: Generate high-end dune-color keynote-style HTML presentations from outlines, markdown, notes, or rough content. Use when Codex needs to create or edit a launch-event, speech, product keynote, technical talk, strategy deck, or HTML PPT with modular source slides, warm sand visual style, layout routing, information reduction, cinematic section pages, and runtime shortcuts for edit/overview/fullscreen modes.
---

# Dune Keynote Slide

## Output Contract

Create a self-contained HTML deck with modular source files. This contract is mandatory and must not be bypassed:

```text
<deck-folder>/
├── index.html
└── sources/
    ├── outline.md
    ├── style.css
    ├── deck.config.json
    └── slide-01.html ... slide-NN.html
```

Use the bundled template in `assets/html-template/` and merge with `scripts/merge_deck.py`.

Never hand-write the final `index.html` from scratch. Never create a simplified one-file runtime. Never replace the bundled overview, edit toolbar, footer, or keyboard runtime. Agents may only author:

- `sources/slide-XX.html`
- `sources/style.css`
- `sources/outline.md`
- `sources/deck.config.json`

The final `index.html` must be produced by `scripts/merge_deck.py`, which injects the canonical CSS, overview thumbnails, edit mode, save support, footer, and runtime.

Do not add QA automation, image generation, web search, or complex external dependencies. Use CSS/SVG/HTML diagrams and provided images only.

## Required Workflow

1. Select a style pack. Default to `references/style-packs/dune.md` unless the user asks for another style. If adding a new style later, keep the same workflow and layout library; only swap style tokens, components, and motion rules.
2. Read `references/dune-style-guide.md` only as needed for detailed visual rules.
3. Convert user content into a slide outline with one main claim per page.
4. For each slide, identify the protagonist object: `title`, `image`, `flow`, `data`, `comparison`, `hierarchy`, `cards`, `timeline`, or `conclusion`.
5. Apply information reduction: if a slide has too much content, split it instead of shrinking text.
6. Apply the section-page gate before layout routing: a numbered cinematic chapter page may contain only kicker, section number, title, one short subtitle/claim, and faint ambient icons. If there is any list, card, diagram, table, timeline, or proof object, split it into the following content slide.
7. Estimate capacity before writing HTML: if cards, layers, tables, or lists would approach the bottom safe area, split the slide instead of compressing below readable sizes.
8. Route each slide to a layout from `references/layout-library.md` or the full guide.
9. Avoid repetitive layouts: do not use card/list/directory-like layouts more than 2 times in a row.
10. Apply motion budget: cover, cinematic sections, and closing may have stronger ambient motion; normal content pages get subtle entrance or no motion.
11. Perform a final layout review pass from `references/layout-library.md`: catch content-rich bullet pages, content-light dense grids, tiny radial diagrams, tiny timelines, section pages with proof objects, and repeated visual grammar. Revise slide layout choices before merging.
12. Generate only `sources/slide-XX.html`, `sources/style.css`, `sources/outline.md`, and `sources/deck.config.json`. Do not write root-level custom HTML manually.
13. Run `python3 <skill>/scripts/merge_deck.py <deck-folder>` to create `index.html`.
14. Run or rely on `python3 <skill>/scripts/validate_deck_contract.py <deck-folder>` after merging. If validation fails, fix the sources and merge again. Do not deliver a deck that fails the contract.

## Runtime Shortcuts

The generated deck must support:

- `ArrowRight`, `PageDown`, `Space`: next slide.
- `ArrowLeft`, `PageUp`: previous slide.
- `F`: enter fullscreen.
- `Esc`: exit fullscreen, edit mode, or overview mode.
- `O`: overview mode with slide previews in a 3-column grid.
- `E`: edit mode for the current slide. Edits should save back to the source slide file when served by the bundled local editor server. If opened as `file://`, show a clear message that saving requires the local editor server.

These runtime features are provided only by `assets/html-template/index.template.html` and `assets/html-template/runtime.js`. Do not reimplement them in a custom script.

Runtime robustness requirements:

- Do not hard-code slide lookup as `slide-${n}` when slide ids are `slide-01`, `slide-02`, etc. Use the slide array index as the primary source of truth, or pad numbers with `String(n).padStart(2, "0")`.
- `showSlide()` must guard against missing slides and missing footer/progress elements. A missing optional control must never black-screen the deck.
- Derive total slide count from `document.querySelectorAll(".slide").length`; do not hard-code the count unless it is only a fallback.

## Editing Model

Each source slide must be wrapped like:

```html
<section class="slide layout-name" data-slide-id="slide-01" data-source="sources/slide-01.html">
  <div class="slide-stage">
    ...
  </div>
</section>
```

Each source slide must contain exactly one `.slide-stage` wrapper. Do not use legacy `.stage` containers or absolute full-screen stage positioning in slide sources.

In edit mode, make the current slide content editable in the browser. Save behavior:

- `Cmd/Ctrl+S` first tries the local editor endpoint.
- If no local server is available and the browser supports File System Access API, ask the user to select the deck root folder that contains `sources/`, then write the current slide back to `sources/slide-XX.html`.
- If neither method is available, show a clear message recommending Chrome/Edge or `scripts/serve_editor.py`.
- Do not save generated `index.html` directly; save source slide and re-merge when a persistent rebuilt deck is needed.
- Preserve `section.slide` and `data-source` attributes.

## Style Pack Architecture

This skill is extensible. Keep the generation pipeline stable and add new styles as separate files under `references/style-packs/`.

Each style pack should define:

- Color tokens and accent ratio.
- Typography personality.
- Cover mark / section mark / closing mark components.
- Card, chip, chart, and diagram styling.
- Motion budget rules.
- Any forbidden visual patterns.

Default style pack: `references/style-packs/dune.md`.



## Controlled Edit Toolbar

When implementing or modifying the runtime, keep edit mode as a controlled slide editor rather than a full PowerPoint clone.

In `E` edit mode, support:

- Click to select editable elements: headings, paragraphs, list items, cards, panels, grid items, comparison cards, tags, and nodes.
- Text controls: continuous font size decrease/increase, bold, line-height tight/normal/loose, color ink/clay/stone, align left/center/right.
- Line break controls: insert `<br>` and clear `<br>`.
- Size controls: width decrease/increase, height decrease/increase, reset automatic size, toggle nowrap, and padding compact/normal/loose. Element controls: duplicate/delete selected element, reset movement. Block controls: duplicate/delete nearest container, toggle highlighted colored-card state.
- Slide density controls: compact, normal, loose. Selected elements can be moved by dragging or nudged with arrow keys; movement is stored as controlled translate values (`data-x`, `data-y`).

Save must clean editor state before writing:

- Remove `body.editing`.
- Remove `.edit-selected`.
- Remove `contenteditable` attributes.
- Hide overview, toast, and toolbar states.

Do not implement arbitrary freeform CSS editing, multi-select, or full rich-text editor behavior in the default runtime. Dragging is allowed only for the selected element as controlled `translate()` movement with reset support.

## Design Rules

Use the dune keynote style by default:

- Pure or near-pure warm cream background `#fbf7ef`.
- Main accent `#a8553d` with visible use in titles, numbers, progress, rules, chips, selected cards, and diagram paths.
- Big black titles with 1 key phrase highlighted in `#a8553d`.
- Generous 16:9 safe area using clamp-based stage variables.
- Minimal gradients; use subtle paper texture, faint lines, low-opacity glyphs, and slow ambient motion.
- Author/time tags on cover and closing.
- Closing page must center all text and may reuse the cover mark as a deeper colored animated icon.

## Layout Selection

Prefer semantic layouts over generic cards:

- Big idea or conclusion: `statement`, `cover`, `closing`, `cinematic-section`.
- Important subtitle/context: `subtitle-band-cards`.
- Delivery model or role transition: `delivery-flow-cards`.
- Process: `step-flow`, `horizontal-timeline`, `vertical-timeline`, `cycle-loop`.
- Comparison: `left-right-compare`, `pros-cons`, `before-after`, `comparison-matrix`.
- Structure: `main-branches`, `tree-hierarchy`, `radial-hub`, `nested-hierarchy`, `system-map`.
- Evidence: `bar-chart`, `pie-chart`, `line-chart`, `combo-chart`.
- Visual explanation: `text-image-right`, `image-text-right`, `full-image`, `icon-text`.
- Case correction: `case-transform` for rich old/new case content; `reuse-hero` for light reuse-value slides.

## Resources

- `references/dune-style-guide.md`: complete visual and layout specification.
- `references/layout-library.md`: concise layout routing and markup patterns.
- `references/style-packs/dune.md`: default style pack and example for future style packs.
- `assets/html-template/`: runtime template with shortcuts, edit mode, overview mode, and base CSS.
- `scripts/merge_deck.py`: merges modular sources into `index.html`.
- `scripts/serve_editor.py`: optional local editor server for `E` edit mode save-back. Chrome/Edge users can also save source slides through File System Access API without Python.


**最后所有的单页PPT组合成最终一个html的ppt时候再调用 `save_output_file` 工具保存,中间生成过程的单页面的不用调用该方法，也不要把 HTML 代码打字给用户。**

正确做法:
```
工具调用: save_output_file
  filename: "智能体介绍.html"
  content: <完整 HTML 字符串>
  mime: "text/html"
```

调用成功后,前端会显示一张文件卡片(下载按钮 + 打开预览按钮),用户可以直接在右侧分屏看渲染效果。

**绝对不要**:
- 把整段 HTML 用 ``` 包起来贴给用户
- 让用户"复制保存为 xxx.html 文件"
- 输出"将上面代码保存为..."这种指引

如果 HTML 比较大,直接放进 `content` 参数里即可,工具支持很大的字符串。
