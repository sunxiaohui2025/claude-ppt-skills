#!/usr/bin/env python3
import re
import sys
from pathlib import Path


REQUIRED_SNIPPETS = {
    "template version": "DUNE_KEYNOTE_TEMPLATE_VERSION: 2026-05-28-stylepack-runtime-v2",
    "runtime version": "DUNE_KEYNOTE_RUNTIME_VERSION",
    "standard runtime": "const slides = Array.from(document.querySelectorAll('.slide'))",
    "overview grid": 'id="overviewGrid"',
    "iframe thumbnails": "iframe.srcdoc",
    "style-aware thumbnails": "deckStyleClass",
    "thumbnail scaling": "--preview-scale",
    "edit toolbar": 'id="editToolbar"',
    "edit action buttons": "data-edit=",
    "width edit controls": 'data-edit="width-dec"',
    "height edit controls": 'data-edit="height-dec"',
    "padding edit controls": 'data-edit="pad-compact"',
    "density edit controls": 'data-edit="density-compact"',
    "toast": 'id="editorToast"',
    "page text": 'id="pageText"',
    "progress bar": 'id="progressBar"',
    "navigation buttons": 'id="prevBtn"',
}

FORBIDDEN_LAYOUT_CLASSES = {
    "content-block",
    "statement-slide",
    "section-slide",
    "closing-slide",
    "cover-content",
    "cover-meta",
    "cover-visual",
    "burst-mark",
    "lead",
    "highlight",
}

FORBIDDEN_INLINE_STYLE_PATTERNS = re.compile(
    r"(display|grid-template|font-size|line-height|margin|padding|background|border|color)\s*:",
    re.I,
)


def fail(message: str) -> int:
    print(f"Deck contract failed: {message}", file=sys.stderr)
    return 1


def class_tokens(tag: str) -> list[str]:
    match = re.search(r'class=(["\'])(.*?)\1', tag, re.S)
    return match.group(2).split() if match else []


def validate_deck(target_path: str) -> dict:
    target = Path(target_path).resolve()
    html_path = target / "index.html" if target.is_dir() else target
    if not html_path.exists():
        raise FileNotFoundError(f"missing HTML file: {html_path}")

    html = html_path.read_text(encoding="utf-8")
    if "scrollIntoView" in html:
        raise ValueError(
            "found scrollIntoView navigation; use the canonical runtime from merge_deck.py, "
            "not a scrolling HTML document"
        )
    if re.search(r'\.slide\s*\{[^}]*min-height\s*:\s*100vh', html, re.S):
        raise ValueError(
            "found scrolling .slide min-height:100vh layout; final decks must use the "
            "canonical 16:9 slide shell from assets/html-template"
        )
    if "<script" not in html:
        raise ValueError(
            "missing script block; final decks must be produced by merge_deck.py "
            "with the canonical runtime, not hand-written static HTML"
        )
    if "id=\"overviewGrid\"" not in html and "id='overviewGrid'" not in html:
        raise ValueError(
            "missing overview grid; final decks must keep the canonical overview/runtime shell"
        )
    if "id=\"editToolbar\"" not in html and "id='editToolbar'" not in html:
        raise ValueError(
            "missing edit toolbar; final decks must keep the canonical edit/runtime shell"
        )
    for label, snippet in REQUIRED_SNIPPETS.items():
        if snippet not in html:
            raise ValueError(f"missing {label} marker ({snippet})")

    script_blocks = re.findall(r'<script\b[^>]*>(.*?)</script>', html, flags=re.S | re.I)
    for block_index, script in enumerate(script_blocks, 1):
        if "\\`" in script or "\\${" in script:
            raise ValueError(
                f"script block {block_index} contains escaped template literals; "
                "write real backticks and ${...} expressions in final HTML"
            )
        if r"/<br\\s*\\/?>(\\n)?/gi" in script:
            raise ValueError(
                f"script block {block_index} contains double-escaped regex syntax; "
                "write runtime JavaScript directly, not as an escaped string"
            )

    markup = re.sub(r'<style\b[^>]*>.*?</style>', '', html, flags=re.S | re.I)
    markup = re.sub(r'<script\b[^>]*>.*?</script>', '', markup, flags=re.S | re.I)
    slides = [
        tag for tag in re.findall(r'<section\b[^>]*>', markup)
        if "slide" in class_tokens(tag)
    ]
    if not slides:
        raise ValueError("no <section class=\"slide...\"> slides found")

    class_tags = [match.group(0) for match in re.finditer(r'<[^>]*class=(["\']).*?\1[^>]*>', markup, re.S)]
    used_classes = set()
    for tag in class_tags:
        used_classes.update(class_tokens(tag))
    forbidden_used = sorted(FORBIDDEN_LAYOUT_CLASSES & used_classes)
    if forbidden_used:
        raise ValueError(
            "found custom/legacy layout classes that bypass the layout library: "
            + ", ".join(forbidden_used)
        )

    for style_match in re.finditer(r'\sstyle=(["\'])(.*?)\1', markup, flags=re.S | re.I):
        style_value = style_match.group(2).strip()
        normalized = re.sub(r"\s+", "", style_value)
        allowed_inline = (
            re.fullmatch(r"--i:\d+;?", normalized)
            or re.fullmatch(r"height:\d+%;?", normalized)
        )
        if not allowed_inline and FORBIDDEN_INLINE_STYLE_PATTERNS.search(style_value):
            raise ValueError(
                "found inline layout styling in slide markup; use layout-library classes "
                "and sources/style.css instead of per-element style attributes"
            )

    for i, section_open in enumerate(slides, 1):
        if 'data-slide-id=' not in section_open:
            raise ValueError(f"slide {i} missing data-slide-id")
        if 'data-source=' not in section_open:
            raise ValueError(f"slide {i} missing data-source")

    last_slide_classes = class_tokens(slides[-1])
    if not any(token in last_slide_classes for token in ("layout-closing", "closing", "thanks")):
        raise ValueError(
            "last slide must be a closing/thanks page; use class layout-closing, closing, or thanks"
        )

    section_blocks = re.findall(
        r'<section\b[^>]*>.*?</section>',
        markup,
        flags=re.S | re.I,
    )
    for i, section_html in enumerate(section_blocks, 1):
        if "section-ghost-number" in section_html and "statement-rule" in section_html:
            raise ValueError(
                f"slide {i} is a numbered chapter page but contains .statement-rule; "
                "chapter dividers must not use the decorative horizontal rule"
            )

    if section_blocks:
        last_slide_html = section_blocks[-1]
        if "author-meta" not in last_slide_html or "thanks-mark" not in last_slide_html:
            raise ValueError(
                "closing slide must echo the cover with .thanks-mark and .author-meta "
                "for speaker/date/logo metadata"
            )
        if "statement-rule" in last_slide_html:
            raise ValueError(
                "closing slide must not contain .statement-rule; keep the ending clean and centered"
            )

    if any("stage" in class_tokens(tag) for tag in class_tags):
        raise ValueError('found legacy class="stage"; use .slide-stage inside the standard template')

    slide_stage_count = sum(1 for tag in class_tags if "slide-stage" in class_tokens(tag))
    if slide_stage_count < len(slides):
        raise ValueError("each slide must contain .slide-stage")

    if "slide-${n}" in html:
        raise ValueError("runtime contains unsafe unpadded slide-${n} lookup")

    if re.search(r'\.layout-cover\s+\.stage-mark\s*\{[^}]*position\s*:\s*fixed', html, re.S):
        raise ValueError("cover stage-mark must stay section-bound; position: fixed is forbidden")

    if re.search(r'\.layout-cover\s+\.stage-mark\s*\{[^}]*right\s*:\s*clamp\(\s*-', html, re.S):
        raise ValueError("cover stage-mark must not use negative right offsets")

    return {
        "ok": True,
        "html_path": str(html_path),
        "slides": len(slides),
        "message": f"Deck contract valid: {html_path} ({len(slides)} slides)",
    }


def run(target: str = None, target_path: str = None, **kwargs) -> dict:
    return validate_deck(target or target_path)


def generate(target: str = None, target_path: str = None, html_path: str = None, deck_folder: str = None, **kwargs) -> dict:
    return validate_deck(target or target_path or html_path or deck_folder or kwargs.get("target"))


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_deck_contract.py <deck-folder-or-html>", file=sys.stderr)
        return 2
    try:
        result = validate_deck(sys.argv[1])
    except Exception as exc:
        return fail(str(exc))
    print(result["message"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
