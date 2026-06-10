# Dune Style Pack

Default style pack for warm keynote decks. `stylePack: "dune"`.

Tokens (everything else derives from these via `color-mix` in the template):

- Background `--cream`: `#fbf7ef`
- Panel `--porcelain`: `#fffdf8`
- Accent `--clay`: `#a8553d` (deep variant `--clay-deep`: `#8a4430`)
- Secondary accent `--accent-2`: `#45635a` — charts and diagram second voice only
- Ink `--ink`: `#211f1c` / Stone `--stone`: `#6b635b` / Muted `--muted`: `#a49a90`

Motion (provided by the template motion layer):

- Cover: orbit rings, floating glyphs, burst mark.
- Section: low-opacity glyphs or fine orbit.
- Closing: reuse cover burst as `thanks-mark`.
- All pages: automatic staggered entrance for title block and proof-object children; bar/pie charts grow in. `prefers-reduced-motion` disables everything.

Rules:

- Use pure warm background, not heavy gradients. The template adds a faint paper grain.
- Highlight one key phrase per title in accent.
- Use colored card for current/recommended/core item.
- Never hard-code rgba accent values in deck CSS; use tokens.
