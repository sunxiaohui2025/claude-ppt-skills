---
name: dune-keynote-slide
description: Generate high-end keynote-style HTML presentations only through modular source slides and scripts/merge_deck.py, never by hand-writing a standalone HTML file. Use when Codex needs to create or edit a launch-event, speech, product keynote, technical talk, strategy deck, or HTML PPT with required canonical runtime, overview thumbnails, edit mode, footer controls, style packs, content-aware layouts, information reduction, and cinematic section pages.
---

# Dune Keynote Slide

## Absolute First Rule

This skill does not mean "write an HTML presentation from scratch." It means:

1. Create or update modular files under `<deck-folder>/sources/`.
2. Run `scripts/merge_deck.py <deck-folder>`.
3. Validate with `scripts/validate_deck_contract.py <deck-folder>`.
4. When Playwright is available, run `scripts/render_check.py <deck-folder>` to catch viewport overflow and stacked slides.
5. Deliver only the merged `<deck-folder>/index.html`.

Any other final HTML is invalid, even if it visually looks like slides.

Never deliver a deck that has any of these anti-patterns:

- A custom `.slide { min-height: 100vh; ... }` scrolling document.
- Keyboard navigation implemented with `scrollIntoView`.
- Slide content built with ad-hoc classes such as `content-block`, `statement-slide`, `section-slide`, `closing-slide`, `cover-content`, `cover-meta`, or `highlight`.
- Dense inline styling such as `style="font-size:..."`, `style="display:grid..."`, `style="padding:..."`, `style="background:..."`, or `style="color:..."` inside slide markup. Use layout-library classes and `sources/style.css` instead.
- No `id="overviewGrid"`.
- No `id="editToolbar"`.
- No `id="pageText"`, `id="prevBtn"`, or `id="nextBtn"`.
- No `data-source` or `data-slide-id` on each slide.
- Slides that are not wrapped as `<section class="slide ..."><div class="slide-stage">...</div></section>`.
- A hand-written `<script>` replacing the bundled `assets/html-template/runtime.js`.

If you find yourself writing `<!doctype html>`, `<head>`, `<body>`, footer controls, keyboard handlers, or overview/edit runtime manually, stop. You are bypassing the skill. Write slide source files instead and merge them.

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

Hard stop: if the current output does not contain the canonical runtime, overview grid, edit toolbar, footer, `data-source`, and `.slide-stage`, it is not a valid deck. Do not deliver it, do not call any save/export tool with it, and do not claim the deck is complete.

Hard stop: having the canonical shell is not enough. Slide internals must use the sample-deck layout components (`cards-3`, `compare-2`, `subtitle-band`, `flow-cards`, `system-map`, `case-transform`, `thanks`, etc.). Do not create a generic custom page system with `content-block` and inline CSS; that bypasses the design rules and produces low-quality pages.

Hard stop: do not invent descriptive layout aliases. These are invalid: `layout-split`, `layout-statement`, `layout-cinematic-section`, `layout-flow-cards`, `layout-icons-grid`, `layout-compare-2`, and similar model-made `layout-*` names. Use the actual sample tokens: `split`, `statement-stage`, `icons-grid`, `compare-2`, `layout-delivery-flow`, `layout-subtitle-band`, `thanks`, etc.

## Local Claude Code Operating Model

When running in local Claude Code, use the normal filesystem and shell. Do not use platform-specific save helpers, sandbox wrappers, or one-off HTML builders.

Stable architecture:

1. **Narrative layer**: confirm audience, thesis, chapter arc, and page-level claims.
2. **Source layer**: write only `sources/outline.md`, `sources/deck.config.json`, `sources/style.css`, and `sources/slide-XX.html`.
3. **Template layer**: copy DOM patterns from `assets/html-template/dune-sample-deck.html` through `references/sample-layout-index.md`.
4. **Merge layer**: run `scripts/merge_deck.py`; only this script creates `index.html`.
5. **Contract layer**: run `scripts/validate_deck_contract.py`; fix sources if it fails.
6. **Render layer**: run `scripts/render_check.py` when available; fix density, overflow, or stacked-slide issues before delivery.

If any step fails, revise the modular source files and rerun the same pipeline. Never recover by hand-writing a standalone final HTML file.

## Template-First Layout Rule

The stable design source is `assets/html-template/dune-sample-deck.html` relative to this skill root.

For each generated slide:

1. Read `references/sample-layout-index.md`.
2. Select the closest sample slide number.
3. Copy that sample slide's DOM pattern into the source slide.
4. Replace only content and repeated items within the same component grammar.
5. Keep component classes such as `split`, `cards-3`, `compare-2`, `timeline-h`, `problem-solution`, `layout-delivery-flow`, and `thanks`.

Do not design page layout from scratch unless you are deliberately adding a new reusable layout to `base.css`, `references/sample-layout-index.md`, `references/layout-library.md`, and the validator in the same change. New `layout-*` class names are rejected unless explicitly added to the validator allowlist.

Do not add QA automation, image generation, web search, or complex external dependencies. Use CSS/SVG/HTML diagrams and provided images only.

## Required Workflow

0. Run the pre-generation alignment gate before writing any deck files. Do not skip it unless the user explicitly says to use a previously confirmed outline.
1. Collect or infer the presentation brief:
   - Topic/title.
   - Target audience.
   - Presentation goal.
   - Occasion/scenario.
   - Desired length or rough slide count.
   - Style pack. Default to `references/style-packs/dune.md` if the user does not specify a style. Supported built-in packs: `dune`, `ink-classic`, `indigo-porcelain`, `white-stage`, `editorial-mono`. If adding a new style later, keep the same workflow and layout library; only swap style tokens, components, and motion rules.
   - Speaker/author and date if the cover or closing should show them.
   If key information is missing, make reasonable assumptions and clearly label them. Ask at most 3 focused questions only when the missing information would materially change the deck.
2. Produce a confirmation outline before generating HTML:
   - Target audience.
   - Core message / main thesis.
   - Narrative arc.
   - Chapter structure.
   - Proposed slide list with one main claim per slide.
   - Closing thought.
   - Selected style pack and tone.
   If the user only provides a title or very short prompt, expand it into a thoughtful outline instead of generating slides immediately. If the user provides a detailed outline, preserve the user's intent, lightly polish the logic, extract one main claim per page, and avoid over-rewriting.
3. Stop and wait for user confirmation after showing the outline. Do not create `sources/slide-XX.html`, `sources/style.css`, `sources/deck.config.json`, or final `index.html` until the user approves the outline or explicitly asks to proceed.
4. After confirmation, read `references/dune-style-guide.md` only as needed for detailed visual rules.
   For non-default styles, read the matching file under `references/style-packs/` and set `sources/deck.config.json` with `"stylePack": "<style-id>"`.
5. Convert the confirmed outline into slide content with one main claim per page.
6. For each slide, identify the protagonist object: `title`, `image`, `flow`, `data`, `comparison`, `hierarchy`, `cards`, `timeline`, or `conclusion`.
7. Apply information reduction: if a slide has too much content, split it instead of shrinking text.
8. Apply the section-page gate before layout routing: a numbered cinematic chapter page may contain only kicker, section number, title, one short subtitle/claim, and faint ambient icons. If there is any list, card, diagram, table, timeline, or proof object, split it into the following content slide.
9. Estimate capacity before writing HTML: if cards, layers, tables, or lists would approach the bottom safe area, split the slide instead of compressing below readable sizes. Count rough Chinese characters before writing markup: cards should usually stay under 28 Chinese characters of support text each, flow cards under 34, comparison panels under 48, and normal claims under 42. If one card is much longer than the others, shorten it or split the slide; do not let one card stretch the grid.
10. Route each slide using `references/sample-layout-index.md` first. Pick the closest sample slide from `assets/html-template/dune-sample-deck.html`, copy its DOM structure, and replace content. Use `references/layout-library.md` only for capacity and routing rules around those sample layouts.
11. Avoid repetitive layouts: do not use card/list/directory-like layouts more than 2 times in a row.
12. Apply motion budget: cover, cinematic sections, and closing may have stronger ambient motion; normal content pages get subtle entrance or no motion.
13. Perform a final layout review pass from `references/layout-library.md`: catch content-rich bullet pages, content-light dense grids, tiny radial diagrams, tiny timelines, section pages with proof objects, uneven card heights, four-card rows that wrap, image/text pages with cramped text columns, long chapter titles without `<br>`, and repeated visual grammar. Revise slide layout choices before merging.
14. Always end with a real closing/thanks page. The last slide must use `layout-closing`, `closing`, or `thanks`, must include `thanks-mark`, and must include `author-meta` with speaker/date/logo metadata echoed from the cover. Closing text must be centered, the main title should be larger than normal content titles, and the closing slide must not include `<div class="statement-rule"></div>`.
15. Generate only `sources/slide-XX.html`, `sources/style.css`, `sources/outline.md`, and `sources/deck.config.json`. Do not write root-level custom HTML manually.
16. Run `python3 <skill>/scripts/merge_deck.py <deck-folder>` to create `index.html`.
17. Run `python3 <skill>/scripts/validate_deck_contract.py <deck-folder>` after merging. If validation fails, fix the sources and merge again. Do not deliver a deck that fails the contract.
18. Run `python3 <skill>/scripts/render_check.py <deck-folder>` when Playwright is installed. Treat failures as real design bugs: split dense slides, choose a larger template, or reduce vertical rhythm before reducing readability. If Playwright is unavailable, do a manual 13-inch laptop sanity check at `1366x768` and `1280x720`.
19. The deck must remain readable at `1366x768`, and should still preserve top/bottom breathing room at `1280x720` without requiring browser zoom-out. If a page only works at 80% browser zoom, split the content or use a more compact layout. Do not optimize for phone or extremely narrow windows if that would weaken keynote composition.
20. If the final answer or environment requires a single downloadable HTML artifact, read the merged `<deck-folder>/index.html` and export/save exactly that merged content. Never export a hand-written substitute.
21. Validate the exact exported HTML file, not only the deck folder. If export tooling escapes JavaScript template strings into `\`` or `\${...}`, the deck will throw `Invalid or unexpected token`; treat that as a failed export and copy the merged `index.html` bytes directly.

## Pre-Generation Confirmation Gate

Before creating any slide files, align with the user on content and style. This is mandatory because presentation quality depends on narrative choices before visual execution.

When the request is brief, such as only a title, topic, or one sentence:

- Do not start generating the PPT immediately.
- Infer a reasonable audience, purpose, and narrative arc.
- Draft a complete outline with chapters and proposed slide claims.
- Clearly mark assumptions.
- Ask the user to confirm or adjust.

When the request already contains detailed material:

- Do not over-process or rewrite the user's meaning.
- Preserve the user's core structure and terminology.
- Improve only the story flow, section grouping, page-level claims, and ending thought.
- Return a refined outline for confirmation before generating.

The confirmation message should be concise but complete:

```text
风格：默认沙丘色 / 用户指定风格
目标受众：...
主旨：...
叙事线：...
章节结构：...
页级大纲：
1. ...
2. ...
结尾思想：...

请确认这个方向，我确认后再开始生成 HTML PPT。
```

Only after the user confirms should the agent write deck sources and run the merge pipeline.

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

Built-in style pack ids:

- `dune`: default warm sand keynote style.
- `ink-classic`: black/cream/gold commercial keynote style for business launches and internal talks.
- `indigo-porcelain`: deep blue technical style for AI, research, architecture, and technology launches.
- `white-stage`: pure white product stage style for product launches, Demo Day, and product walkthroughs.
- `editorial-mono`: black-and-white magazine/editorial style for personal, opinionated, or salon-style talks.

To select a style in a deck, write:

```json
{
  "title": "Deck title",
  "stylePack": "ink-classic"
}
```



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
- For the default dune style, keep the background plain and stable. Do not add large radial glow gradients, obvious bloom, or a deck-wide frame line.
- Main accent `#a8553d` with visible use in titles, numbers, progress, rules, chips, selected cards, and diagram paths.
- Big black titles with 1 key phrase highlighted in `#a8553d`.
- Generous 16:9 safe area using clamp-based stage variables.
- Minimal gradients; use subtle paper texture, faint lines, low-opacity glyphs, and slow ambient motion.
- Author/time tags on cover and closing.
- Closing page must center all text and may reuse the cover mark as a deeper colored animated icon.

Cover pages should follow the reference sample composition in `assets/html-template/dune-sample-deck.html`: large left title, author/time tags below, `cover-atmosphere` orbit in the upper-right, and `stage-mark` burst in the lower-right open area. Do not replace the burst with random icons such as stars or badges.

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
- `references/sample-layout-index.md`: source-of-truth mapping from content intent to the stable sample slides in `dune-sample-deck.html`.
- `references/layout-library.md`: concise layout routing and markup patterns.
- `references/style-packs/dune.md`: default style pack and example for future style packs.
- `assets/html-template/`: runtime template with shortcuts, edit mode, overview mode, and base CSS.
- `scripts/merge_deck.py`: merges modular sources into `index.html`.
- `scripts/validate_deck_contract.py`: static contract check for canonical runtime, slide wrappers, layout classes, and forbidden hand-written HTML patterns.
- `scripts/render_check.py`: optional browser check for 13-inch viewport overflow, stacked slides, and footer collisions.
- `scripts/serve_editor.py`: optional local editor server for `E` edit mode save-back. Chrome/Edge users can also save source slides through File System Access API without Python.
