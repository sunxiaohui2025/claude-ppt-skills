# Sample Layout Index

Use `assets/html-template/dune-sample-deck.html` as the source-of-truth layout library. This path is relative to the skill root.

The generation rule is template-first:

1. Choose one sample slide from the index below.
2. Copy that slide's DOM structure into `sources/slide-XX.html`.
3. Replace text, counts, labels, and simple repeated nodes only.
4. Keep the same component classes and hierarchy.
5. Do not invent generic structures such as `content-block`, `statement-slide`, `section-slide`, or custom inline-styled grids.

## Source Slides

- `01 cover`: `layout-cover`; opening page with large left title, author/time tags, upper-right orbit, lower-right burst mark.
- `02 agenda`: `layout-agenda` + `agenda-runway`; 3-5 chapter rows. If more rows, split.
- `03 text-only`: `text-page-clean`; title + claim + short explanatory body and up to 3 bullets.
- `04 text-image-right`: `split`; left text, right visual/image proof.
- `05 image-text-right`: `split reverse`; left visual/image proof, right text.
- `06 top-image`: `stack-vertical`; image above, concise text below.
- `07 bottom-image`: `stack-vertical`; text above, image below.
- `08 full-image`: `full-image`; one dominant image surface with minimal overlay.
- `09 icon-text`: `icons-grid`; 3-4 icon statements.
- `10 two-cards`: `cards-2`; two equal panels.
- `11 three-cards`: `cards-3`; three equal panels, short copy only.
- `12 four-grid`: `grid-4`; four compact blocks.
- `13 multi-column`: `multi-columns`; three columns of short list items.
- `14 left-right-compare`: `compare-2`; neutral vs highlighted comparison.
- `15 pros-cons`: `compare-2`; strengths vs risks.
- `16 before-after`: `compare-2`; old vs new state.
- `17 comparison-matrix`: `table`; 3-4 dimensions.
- `18 horizontal-timeline`: `timeline-h`; 3-4 phases across page.
- `19 vertical-timeline`: `timeline-v`; 3 stages down page.
- `20 step-flow`: `flow`; 4-5 steps.
- `21 cycle-loop`: `split` + `cycle`; text + cycle diagram.
- `22 main-branches`: `branch`; large main claim + branch list.
- `23 tree-hierarchy`: `tree`; root and child nodes.
- `24 radial-hub`: `radial`; central core + surrounding nodes.
- `25 nested-hierarchy`: `nested`; nested container relationship.
- `26 bar-chart`: `chart-card` + `bars`; categorical comparison.
- `27 pie-chart`: `pie-wrap`; share of whole.
- `28 line-chart`: `line-chart`; trend over time.
- `29 combo-chart`: `combo`; two compact chart views.
- `30 statement`: `statement-stage`; centered conclusion/major viewpoint. Keep `statement-rule` only for non-chapter statement pages.
- `31 problem-solution`: `problem-solution`; paired issues and solutions.
- `32 goal-plan`: `goal-plan`; large goal number + plan list.
- `33 subtitle-band-cards`: `layout-subtitle-band`; important subtitle band + three support cards.
- `34 delivery-flow`: `layout-delivery-flow` + `flow-cards`; user/FDE/platform delivery chain.
- `35 closing`: `thanks`; mandatory final page with `thanks-mark`, centered text, and `author-meta`. Do not include `statement-rule`.

## Routing Rules

- Cover and closing must use sample `01` and `35`.
- Chapter divider pages should use the cinematic section structure from the current template rules, not ordinary content layouts.
- If content has no obvious proof object, use `03 text-only` or `30 statement`.
- If content contains two contrasting states, use `14`, `15`, or `16`; do not use custom two-column inline grids.
- If content contains 3 parallel ideas, use `11`; if copy is long, split or use `31`.
- If content contains an operating model or handoff, use `34`.
- If content contains case old/new logic, use `16` or `31`.
- If a generated page needs inline `style="font-size..."` or `style="display:grid..."`, the chosen sample layout is wrong.

## Allowed Edits To A Copied Sample

- Replace headings, claims, labels, dates, numbers, and card text.
- Add or remove repeated nodes within the same pattern, within capacity limits.
- Swap card highlight class such as `hot` or `colored-card`.
- Replace placeholder image boxes with provided image assets.
- Change chart values by editing SVG points, bar heights, or legend text.

## Forbidden Edits

- Do not replace sample components with `content-block`.
- Do not create new layout names unless updating `base.css`, this index, and the validator together.
- Do not use dense inline CSS for layout, spacing, color, or typography.
- Do not use small `1rem` body text for projected slides.
- Do not put content below numbered chapter dividers.
