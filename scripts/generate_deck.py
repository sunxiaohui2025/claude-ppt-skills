#!/usr/bin/env python3
"""Build a full HTML deck from source-slide payloads.

This wrapper is for restricted agent runtimes that cannot create a deck folder
with normal file writes. The caller passes slide source HTML as kwargs; this
script creates the required sources/ folder, runs merge_deck.py, validates, and
copies the final index.html to the injected output path when provided.
"""
from __future__ import annotations

import json
import shutil
import tempfile
import importlib.util
from pathlib import Path
from typing import Any


def _load_merge_deck():
    script_path = Path(__file__).resolve().with_name("merge_deck.py")
    spec = importlib.util.spec_from_file_location("_dune_merge_deck", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load {script_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.merge_deck


merge_deck = _load_merge_deck()


def _coerce_slides(slides: Any) -> list[tuple[str, str]]:
    if isinstance(slides, dict):
        items = sorted(slides.items())
        return [(str(name), str(html)) for name, html in items]
    if isinstance(slides, list):
        result: list[tuple[str, str]] = []
        for idx, item in enumerate(slides, 1):
            if isinstance(item, dict):
                name = item.get("filename") or item.get("name") or f"slide-{idx:02d}.html"
                html = item.get("html") or item.get("content") or ""
            else:
                name = f"slide-{idx:02d}.html"
                html = str(item)
            result.append((str(name), str(html)))
        return result
    raise ValueError("slides must be a list or dict of slide source HTML")


def _normalize_slide_name(name: str, index: int) -> str:
    clean = Path(name).name
    if not clean.startswith("slide-") or not clean.endswith(".html"):
        clean = f"slide-{index:02d}.html"
    return clean


def generate(
    title: str = "Dune Keynote Deck",
    stylePack: str = "dune",
    slides: Any = None,
    outline_md: str = "",
    style_css: str = "",
    deck_config: dict[str, Any] | None = None,
    deck_folder: str | None = None,
    output: str | None = None,
    output_path: str | None = None,
    **kwargs: Any,
):
    """Create, merge, validate, and return/copy a complete HTML deck.

    Parameters are intentionally simple for tool calling:
    - slides: list[{filename, html}] or {filename: html}
    - outline_md: content for sources/outline.md
    - style_css: content for sources/style.css
    - deck_config: optional extra config merged with title/stylePack
    - output/output_path: optional final HTML path injected by host runtimes
    """
    slide_items = _coerce_slides(slides)
    if not slide_items:
        raise ValueError("slides cannot be empty")

    if deck_folder:
        deck = Path(deck_folder).expanduser().resolve()
        if deck.name == "sources":
            deck = deck.parent
        deck.mkdir(parents=True, exist_ok=True)
    else:
        deck = Path(tempfile.mkdtemp(prefix="dune-keynote-deck-"))

    sources = deck / "sources"
    if sources.exists():
        shutil.rmtree(sources)
    sources.mkdir(parents=True, exist_ok=True)

    config = {"title": title, "stylePack": stylePack}
    if deck_config:
        config.update(deck_config)
    sources.joinpath("deck.config.json").write_text(
        json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    sources.joinpath("outline.md").write_text(outline_md or f"# {title}\n", encoding="utf-8")
    sources.joinpath("style.css").write_text(style_css or "", encoding="utf-8")

    for idx, (name, html) in enumerate(slide_items, 1):
        filename = _normalize_slide_name(name, idx)
        sources.joinpath(filename).write_text(html.strip() + "\n", encoding="utf-8")

    result = merge_deck(str(deck))
    final_path = Path(result["output_path"])
    target = output or output_path or kwargs.get("output") or kwargs.get("output_path")
    if target:
        target_path = Path(target).expanduser().resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(final_path, target_path)
        return str(target_path)
    return result


def run(**kwargs: Any):
    return generate(**kwargs)


if __name__ == "__main__":
    raise SystemExit(
        "generate_deck.py is intended for run_skill_script/generate(**kwargs). "
        "Use merge_deck.py for CLI folder-based merging."
    )
