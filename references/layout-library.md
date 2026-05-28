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

- `cover`: giant title, author/time tags, faint animated cover mark.
- `agenda-index`: 3-5 chapter rows only; do not reuse as content page.
- `text-only`: title + clean text panel; split if body exceeds 120 Chinese characters.
- `statement`: centered title, centered claim, centered clay rule.
- `cinematic-section`: numbered chapter divider only; no cards, no list, no table, no diagram, no proof object.
- `closing`: centered all text, author/time tags, animated mark echoing cover.

## Capacity Gate

Estimate slide capacity before writing HTML. Split first; shrink second.

- Numbered section pages are not content pages. If a page has `.section-ghost-number`, it must not contain `.proof-object`, cards, layers, tables, timelines, charts, or lists.
- A section page may contain only: kicker, section number, title, one short subtitle/claim, and low-opacity ambient icons.
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

- `text-image-right`: left title/claim, right large visual.
- `image-text-right`: left visual, right title/claim.
- `image-top-text-bottom`: wide visual above concise explanation.
- `text-top-image-bottom`: concise claim above wide visual.
- `full-image`: large visual surface with minimal overlay text.
- `icon-text`: 3-4 icon short statements.

## Cards And Lists

- `two-cards`: two equal panels.
- `three-cards`: three equal panels; only one highlighted colored card by default.
- `grid-four`: 2x2 grid.
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

Avoid tiny proof objects on content-heavy pages.

- Card groups must occupy at least 55% of slide width and 32% of slide height.
- Three cards should use min-height `clamp(190px, 29vh, 250px)` and large card titles.
- Four grids should use a 2x2 block centered in the proof area, not small icon buttons.
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
- If an agenda/list has more than 5 rows, use a balanced two-column list instead of a single tall list.
- If a layer stack, architecture stack, quote + conclusion, or three-card page exceeds the safe stage height, reduce vertical gaps, card padding, list line-height, and conclusion-band height before reducing title hierarchy.
- Footer controls must stay visually quiet; they should never compete with content or look like a decorative bottom bar.

Add these corrective layouts when needed:

- `case-transform`: old pain -> new architecture -> bottom conclusion.
- `system-map`: left inputs, large central engine, right outputs.
- `reuse-hero`: giant reuse metric or claim + application tags.

## Case Transform Sizing

For `case-transform` slides, keep the footer safe and avoid over-tall cards.

- Keep the subtitle/claim on one line when possible: `white-space: nowrap`; shorten text rather than wrapping.
- Use compact card internals: secondary list text can be `14-17px`, smaller than normal body text.
- Recommended card min-height: `clamp(178px, 27vh, 236px)`.
- Recommended card padding: `clamp(20px, 2.4vw, 28px)`.
- Bottom conclusion band should be compact: `54-64px` tall.
- Proof object margin should be smaller than normal: `18-28px`.
- If content still overlaps footer, split the case into two slides: old pain and new architecture.

## Alignment Rules

Apply these before merging:

- Except cover pages, primary `h2` titles should be larger: `clamp(50px, min(5.7vw, 9.6vh), 82px)` unless the slide is dense technical content.
- `statement`, `closing`, and `thanks` pages must center the full title block: kicker, h2, claim, rule, author tags.
- Centering a parent grid is not enough; set `h2 { margin-left:auto; margin-right:auto; text-align:center; }` for centered pages.
- Normal content pages default to left alignment for title, claim, and subtitle. Do not center subtitles in `main-branches`, `cards`, `case-transform`, `system-map`, or `timeline` unless explicitly requested.
- Avoid inline `text-align:center` on claims except statement/closing pages.

## Cinematic Section Rules

Use cinematic section pages for chapter dividers and one-sentence theme pages.

- Add a low-opacity chapter number as a left-side mark: `.section-ghost-number` with `01`, `02`, etc.
- Section title should be very large: `clamp(62px, min(7.2vw, 12vh), 106px)`.
- Keep the section title on one line when possible. If it must wrap, allow at most one line break.
- Subtitle/claim should have at most one `<br>`; shorten or split if it becomes three lines.
- Use low-opacity ambient icons only; do not let glyphs compete with the title.
- Do not use ordinary small statement pages for chapter dividers; use the left-side number + large title composition.
- Do not add `<div class="statement-rule"></div>` under numbered chapter titles. Chapter pages should stay clean and rely on number, title, subtitle, and faint ambient icons.
- For one-line statement or major viewpoint pages that are not chapter dividers, keep the centered `statement-rule` as a deliberate pause and emphasis device.

## Cover Motion Positioning

Cover atmosphere and mark must stay inside the 16:9 safe stage.

- Put cover visual elements inside or visually anchored to the slide stage.
- Right-side orbit should sit in the right third, vertically centered, not at the far corner.
- Main burst mark should sit near right-center/bottom-safe area, not beyond the bottom-right edge.
- If overview thumbnails show cover icons in corners, treat it as a layout bug and tighten `.cover-atmosphere` / `.stage-mark` positioning.

## Refined Chapter Mark Placement

For cinematic section pages, use the chapter number as a left-side mark, not as a ghost layer under the text.

- Place the number to the left of the title group in the same visual row.
- Reduce the number size by roughly 30% compared with a full-background ghost number.
- Use `rgba(168,85,61,.18-.22)` so the number is visible but still secondary.
- Keep a moderate gap between number and title: `28-56px`.
- Align kicker, title, subtitle, and rule as one text group to the right of the number.
- On mobile/narrow viewports, stack number above and center the text group.

## Refined Cover Mark Placement

The cover burst mark should visually align with the title block instead of drifting to the bottom-right corner.

- Move the mark left from the extreme edge: use `right: clamp(150px, 18vw, 260px)` as a default.
- Align the mark bottom with the approximate bottom of the title/metadata group: `bottom: calc(var(--stage-bottom) + 4px)`.
- Keep the mark size around `150-210px`, not oversized.
- Orbit atmosphere should sit in the right third but closer to the title: `right: clamp(70px, 9vw, 150px)`.

## Final Cover Motion Alignment

For dune cover pages, anchor motion elements to the title block:

- `.cover-atmosphere` should sit around the upper-right of the text group, not the far page corner.
- Recommended default: `right: clamp(190px, 23vw, 340px); top: clamp(72px, 12vh, 128px)`.
- `.stage-mark` should align visually with the author/tag row, with its bottom near the tag baseline.
- Recommended default: `right: clamp(190px, 22vw, 330px); bottom: calc(var(--stage-bottom) + 78px)`.
- Keep `stage-mark` compact: `138-196px`.

## Footer Line Rule

Do not add a long decorative horizontal line above the footer. Keep only the actual progress bar in `.footer .progress`.

## Cover Mark Target Position

Place `.stage-mark` in the open area to the right of the title group, below the orbit but above the tag row, rather than near the page corner.

Recommended default:

```css
.layout-cover .stage-mark {
  position: absolute;
  right: clamp(140px, 9.5vw, 230px);
  bottom: clamp(132px, 16vh, 214px);
  width: clamp(150px, 12vw, 210px);
  height: clamp(150px, 12vw, 210px);
}
```

The visual bottom of `.stage-mark` should align near the lower-right open area of the cover, never on top of the large title. It must stay inside `<section class="slide layout-cover">`; do not use `position: fixed` or negative right offsets for cover marks.

The upper-right orbit `.cover-atmosphere` should sit to the right of the title group without covering text:

```css
.layout-cover .cover-atmosphere {
  position: absolute;
  right: clamp(34px, 3.6vw, 84px);
  top: clamp(92px, 12vh, 150px);
  width: clamp(330px, 31vw, 520px);
  height: clamp(330px, 31vw, 520px);
  opacity: .34;
}
```

When the title is very wide, remove or reduce `.layout-cover .title-block` right padding rather than letting the stage mark overlap the headline.

## Projection Safe Area Rules

All slides must preserve a visible 16:9 safe area in both normal mode and overview thumbnails.

- Keep top safe padding around `60-92px` and bottom safe padding around `104-148px` on desktop projection.
- The proof object should usually start `20-34px` below the title block. Dense pages may use `14-24px`, but never `0`.
- Long lists: more than 5 rows become two balanced columns. More than 8 rows should be split into two slides unless the text is very short.
- Dense stacks: use compact vertical rhythm, not smaller unreadable text. Prefer reducing gaps, padding, and conclusion bands before shrinking body below `14px`.
- Conclusion bands should be compact (`14-20px` padding) on dense slides and should not sit on top of the footer.
- Footer progress should be 2px high, low opacity, and close to the bottom edge. Navigation buttons should use light translucent styling instead of solid dark circles.
