# Layout Library

Use one main protagonist object per slide.

## Non-Negotiable Deck Shell

All layouts below are slide-source patterns only. They must be placed inside the canonical deck shell from `assets/html-template/`.

- Do not write a custom full HTML runtime.
- Do not replace overview thumbnails, edit toolbar, footer, or keyboard handling.
- Every source slide uses `<section class="slide ..."><div class="slide-stage">...</div></section>`.
- Never use legacy `.stage` containers.
- The merged `index.html` must pass `scripts/validate_deck_contract.py`.

## Foundation

- `cover`: giant left title, author/time tags, upper-right orbit, lower-right burst mark matching `dune-sample-deck.html`.
- `agenda-index`: 3-5 chapter rows only; do not reuse as content page.
- `text-only`: title + clean text panel; split if body exceeds 120 Chinese characters.
- `statement`: centered title, centered claim, centered clay rule.
- `cinematic-section`: numbered chapter divider only; no cards, no list, no table, no diagram, no proof object.
- `closing`: mandatory final page with centered "感谢 / Thank You", `thanks-mark`, author/time/logo tags, and animation echoing cover.

## Capacity Gate

Estimate slide capacity before writing HTML. Split first; shrink second.

- Count rough text length before choosing a layout. A page that is semantically correct but visually overfilled is still wrong.
- Cards should have comparable text weight. If one card is more than 1.5x longer than its siblings, shorten it, split the card group, or choose a comparison/problem-solution layout.
- Four cards must never appear as an orphan wrapped card. If using `flow-cards` with four stages, use the four-card variant without visible arrows, or switch to `grid-4` when text is longer.
- For `cards-3`, keep support text around 16-28 Chinese characters per card. For `flow-cards`, keep support text around 20-34 Chinese characters. For `compare-2`, keep each panel under 48 Chinese characters unless it is the only proof object on the page.
- Numbered section pages are not content pages. If a page has `.section-ghost-number`, it must not contain `.proof-object`, cards, layers, tables, timelines, charts, or lists.
- A section page may contain only: kicker, section number, title, one short subtitle/claim, and low-opacity ambient icons.
- Only insert `<br>` in numbered section titles when the title would genuinely overflow the stage. Do not split short titles just for symmetry; if it is only over by 1-2 characters, keep one line and let CSS size/width handle it.
- If section context needs examples, architecture, scenarios, or bullets, create the next slide as the content slide.
- A normal content slide should have one protagonist proof object. If it needs both a chapter title and a proof object, split into `cinematic-section` + content layout.
- Five-layer stacks, four-card grids, and long roadmaps often need their own page. Do not attach them under a chapter divider.
- If the proof object plus title would exceed the bottom safe area, split the slide. Do not reduce body text below `14px`.

## Layout Coverage From Sample Deck

The old `dune-sample-deck.html` layout library has been folded into these requirements. When generating decks, choose from these families instead of inventing new shell structures:

- Foundation: cover, agenda, cinematic section, statement, closing.
- Basic content: text-only, text-image-right, image-text-right, top/bottom image, full-image, icon-text.
- Blocks: two-cards, three-cards, four-grid, multi-column-list.
- Analysis: left-right-compare, pros-cons, before-after, comparison-matrix.
- Flow: horizontal/vertical timeline, step-flow, cycle-loop.
- Logic: main-branches, tree-hierarchy, radial-hub, nested-hierarchy, system-map.
- Data: bar, pie, line, combo chart.
- Special: problem-solution, goal-plan, subtitle-band-cards, delivery-flow-cards, case-transform, reuse-hero.

## Visual

- `text-image-right`: left title/claim, right large 16:9 visual.
- `image-text-right`: left large 16:9 visual, right title/claim.
- `image-top-text-bottom`: wide visual above concise explanation.
- `text-top-image-bottom`: concise claim above wide visual.
- `full-image`: large visual surface with minimal overlay text.
- `icon-text`: 3-4 icon short statements.

## Cards And Lists

- `two-cards`: two equal panels.
- `three-cards`: three equal panels; only one highlighted colored card by default. Keep cards visually equal height and comparable text length.
- `grid-four`: 2x2 grid. Use this instead of forcing a fourth item into a three-card row when content is not extremely short.
- `multi-column-list`: 3 columns of short list items.
- `subtitle-band-cards`: important subtitle band + three cards + bottom conclusion.
- `delivery-flow-cards`: three role/stage cards with arrows and chips.

## Comparison

- `left-right-compare`: neutral left, highlighted right.
- `pros-cons`: strengths vs risks.
- `before-after`: old state vs new state.
- `comparison-matrix`: 3-4 dimensions, highlighted winning cells.

## Flow And Time

- `horizontal-timeline`: 3-5 phases across the page.
- `vertical-timeline`: 3-4 vertical stages.
- `step-flow`: 4-5 steps with direct arrows.
- `cycle-loop`: 4 nodes around a loop.

## Hierarchy

- `main-branches`: large main claim + 3 branch panels.
- `tree-hierarchy`: root and 2-4 child nodes.
- `radial-hub`: core in center, 4-6 surrounding nodes.
- `nested-hierarchy`: outer container, inner group, child items.

## Data

- `bar-chart`: categorical comparison.
- `pie-chart`: share of whole.
- `line-chart`: trend over time.
- `combo-chart`: two related data views.

## Anti-Repetition

If three consecutive pages would be cards/lists, convert one to statement, comparison, image, flow, or hierarchy.

## Detail Page Sizing Rules

Avoid tiny proof objects on content-heavy pages. All sizes are design px on the fixed 1280x720 canvas.

- Card groups must occupy at least 55% of slide width and 32% of slide height.
- Three cards use the template min-height (`200px`) and large card titles.
- Card groups must look equal-height. Do not allow one card to grow taller while siblings stay short; normalize by shortening text or using the tallest-card height for the whole grid.
- Four grids should use a 2x2 block centered in the proof area, not small icon buttons. Four short cards in one row should use `cards-4` explicitly.
- Radial hub diagrams should use a 360-460px core area and place nodes around it with visible spacing.
- Timeline layouts should stretch across 80-90% of stage width; do not leave a tiny timeline in the middle.
- Case/story pages should avoid small bullet clusters; use subtitle band, split layout, or large text panel.
- If a proof object looks smaller than the title block, enlarge it or split the slide.

## Final Layout Review Pass

Before merging the deck, perform a human-design review pass. This is not QA automation and does not require screenshots.

Review every slide for layout-content fit:

- If a content-rich case slide is only bullets, convert it to `case-transform`, `problem-solution`, `subtitle-band-cards`, or split it.
- If a content-light slide uses a dense grid, convert it to `statement`, `reuse-hero`, `icon-text`, or `full-image`.
- If a radial diagram has few short nodes and looks tiny, convert to `system-map` with a larger core and clear input/output zones.
- If a timeline has only 3 stages and lots of empty space, either enlarge it into a runway or convert to `delivery-flow-cards`.
- If a proof object is smaller than the title block, enlarge the object or choose a more theatrical layout.
- If three consecutive slides share the same visual grammar, swap the middle one to statement, split, image, flow, or hierarchy.
- If a numbered section page contains a proof object, split it immediately. The section page keeps only chapter number/title/subtitle; the proof object moves to the next page.
- If any slide's content visually approaches the top or bottom edge, compress the proof object, split the slide, or switch to a two-column structure. Never let content touch the viewport edge in overview thumbnails.
- If any card row wraps unexpectedly, treat it as a failed layout. Use shorter text, smaller secondary text, or switch to `grid-4`; do not accept an orphan card on a second row.
- If image/text slides produce too many text line breaks, rebalance the split: keep the visual close to 16:9 and large, give the text column enough width, shorten the claim, or split the explanation into the next slide. The image can be large, but the text side cannot become a narrow caption column.
- If an agenda/list has more than 5 rows, use a balanced two-column list instead of a single tall list.
- If a layer stack, architecture stack, quote + conclusion, or three-card page exceeds the safe stage height, reduce vertical gaps, card padding, list line-height, and conclusion-band height before reducing title hierarchy.
- Footer controls must stay visually quiet; they should never compete with content or look like a decorative bottom bar.

Add these corrective layouts when needed:

- `case-transform`: old pain -> new architecture -> bottom conclusion.
- `system-map`: left inputs, large central engine, right outputs.
- `reuse-hero`: giant reuse metric or claim + application tags.

## Case Transform Sizing

`case-transform` is a built-in component (`.case-transform` + `.case-panel` + `.flow-arrow` + `.bottom-conclusion`). Keep the footer safe and avoid over-tall cards.

- Keep the subtitle/claim on one line when possible; shorten text rather than wrapping.
- Use compact card internals: secondary list text can be `14-17px`, smaller than normal body text.
- The template provides card min-height `250px` and padding `26px`; do not override per deck.
- Bottom conclusion band should stay one line.
- If content still feels dense, split the case into two slides: old pain and new architecture.

## Alignment Rules

Apply these before merging:

- Except cover pages, primary `h2` titles use the template scale (`60px`); do not shrink them for dense slides — split instead.
- `statement`, `closing`, and `thanks` pages must center the full title block: kicker, h2, claim, rule, author tags.
- One-sentence statement pages without `.section-ghost-number` should use chapter-scale h2 sizing and must highlight one key phrase inside the h2 with `.title-accent` or `.accent`.
- Centering a parent grid is not enough; set `h2 { margin-left:auto; margin-right:auto; text-align:center; }` for centered pages.
- Normal content pages default to left alignment for title, claim, and subtitle. Do not center subtitles in `main-branches`, `cards`, `case-transform`, `system-map`, or `timeline` unless explicitly requested.
- Avoid inline `text-align:center` on claims except statement/closing pages.

## Cinematic Section Rules

Use cinematic section pages for chapter dividers and one-sentence theme pages.

- Add a low-opacity chapter number as a left-side mark: `.section-ghost-number` with `01`, `02`, etc. Keep it about half the height of the section title block, not a giant background number.
- Section title should be very large: the template provides `76px` for numbered chapters and `82px` for one-sentence statements.
- Keep the section title on one line when it fits. Only add one semantic `<br>` for genuinely long Chinese titles, usually above about 18 characters or when render checking shows overflow.
- Subtitle/claim should have at most one `<br>`; shorten or split if it becomes three lines.
- Use low-opacity ambient icons only; do not let glyphs compete with the title.
- Do not use ordinary small statement pages for chapter dividers; use the left-side number + large title composition.
- Do not add `<div class="statement-rule"></div>` under numbered chapter titles. Chapter pages should stay clean and rely on number, title, subtitle, and faint ambient icons.
- For one-line statement or major viewpoint pages that are not chapter dividers, keep the centered `statement-rule` as a deliberate pause and emphasis device.
- These one-line statement pages must not be visually smaller than chapter pages; keep their h2 at chapter-title scale while preserving the centered composition.

## Cover And Chapter Mark Placement

Cover and chapter marks are positioned by the template; do not re-position them in deck CSS.

- The cover stage is a two-column grid: the title block fills the left column; `.stage-mark` is a grid child anchored to the lower-right of the composition; `.cover-atmosphere` sits absolutely in the upper-right of the stage. Copy the cover DOM from `dune-sample-deck.html` and the placement is automatic.
- Never use `position: fixed`, negative offsets, or viewport units for cover marks.
- Chapter pages place the number to the left of the title group in the same visual row via `.section-ghost-number` inside `.title-block`. The number is visible but secondary (about 110px, 20% clay); kicker, title, and subtitle align as one text group to its right.

## Footer Line Rule

Do not add a long decorative horizontal line above the footer. Keep only the actual progress bar in `.footer .progress`.

## Image Text Balance

For split image/text slides, the text side must read as equal in importance to the image side.

- Use `.split` or `.split.reverse`, not tiny body text beside a large image.
- Text-side title should stay around `46-76px` on desktop and should not shrink below `36px` on 13-inch laptops.
- Text-side claim/body should stay around `20-28px`; if more explanation is needed, split the slide.
- Image panels may be visually dominant, but not more than roughly 55-60% of the perceived composition unless the slide is a single-image page.

## Projection Safe Area Rules

The deck renders on a fixed 1280x720 design canvas that the runtime scales to any viewport, so a slide that fits the canvas fits every resolution identically.

- Write all sizes in design px. Never use `vw/vh` units or `@media` queries in slide sources or `sources/style.css` (the validator rejects them).
- The template safe area is `--stage-top: 56px`, `--stage-bottom: 88px`, `--stage-x: 84px`; the content stage is `1112x576`.
- The proof object should usually start `20-34px` below the title block. Dense pages may use `14-24px`, but never `0`.
- Long lists: more than 5 rows become two balanced columns. More than 8 rows should be split into two slides unless the text is very short.
- Dense stacks: use compact vertical rhythm, not smaller unreadable text. Prefer reducing gaps, padding, and conclusion bands before shrinking body below `14px`.
- Conclusion bands should stay one line and must not sit on top of the footer.
- Footer progress is 2px high, low opacity, and close to the bottom edge; navigation buttons use light translucent styling. The template provides this; do not restyle.
- `scripts/render_check.py` verifies overflow at 1366x768, 1280x720, and 1920x1080; fix failures by splitting or choosing a roomier layout, not by shrinking text.

## Cover Anchor Rule

The cover motion marks are anchored to the title composition, not to the viewport corners.

- The title block occupies the left/main column.
- `.stage-mark` sits in the lower-right of the title-block composition area, visually aligned with the bottom of the title/meta group.
- `.cover-atmosphere` sits in the upper-right as a pale background icon/orbit.
- Do not place the main icon at the very top, outside the stage, or in a random page corner.

## Laptop Capacity Routing

Use this pass before writing source slides. It prevents good-looking large-screen pages from collapsing on 13-inch laptops.

- Cover: title may use at most two lines; if the title is longer, shorten the displayed title and move context into the subtitle.
- Cover subtitle/meta is the second information layer, not body text. Keep it visually strong, usually 24-38px on desktop, with 1-2 balanced lines.
- Agenda: 3-5 rows are single-column; 6 rows should become two columns; more than 6 rows should split into a chapter overview plus detailed agenda.
- Cinematic section: title + one subtitle only. Never place cards, bullets, proof objects, or architecture content below the chapter title.
- Three-card pages: each card should carry one headline and 1-2 short support lines. If a card needs bullets, split or use `problem-solution`.
- Flow pages: 3 steps should become a large runway; 4-5 steps can use horizontal flow. More than 5 steps should split into timeline or two pages.
- Data pages: one chart protagonist only. If a chart needs a table plus interpretation, split into chart page + conclusion page.
- Dense technical pages: use `system-map`, `case-transform`, `comparison-matrix`, or split. Do not solve density by shrinking labels below `14px`.
- Closing: final page is mandatory, all text is centered, title is large, and no `statement-rule` is used.
