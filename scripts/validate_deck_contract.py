#!/usr/bin/env python3
import re
import sys
from pathlib import Path


REQUIRED_SNIPPETS = {
    "standard runtime": "const slides = Array.from(document.querySelectorAll('.slide'))",
    "overview grid": 'id="overviewGrid"',
    "iframe thumbnails": "iframe.srcdoc",
    "edit toolbar": 'id="editToolbar"',
    "edit action buttons": "data-edit=",
    "toast": 'id="editorToast"',
    "page text": 'id="pageText"',
    "progress bar": 'id="progressBar"',
    "navigation buttons": 'id="prevBtn"',
}


def fail(message: str) -> int:
    print(f"Deck contract failed: {message}", file=sys.stderr)
    return 1


def class_tokens(tag: str) -> list[str]:
    match = re.search(r'class=(["\'])(.*?)\1', tag, re.S)
    return match.group(2).split() if match else []


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_deck_contract.py <deck-folder-or-html>", file=sys.stderr)
        return 2

    target = Path(sys.argv[1]).resolve()
    html_path = target / "index.html" if target.is_dir() else target
    if not html_path.exists():
        return fail(f"missing HTML file: {html_path}")

    html = html_path.read_text(encoding="utf-8")
    for label, snippet in REQUIRED_SNIPPETS.items():
        if snippet not in html:
            return fail(f"missing {label} marker ({snippet})")

    script_blocks = re.findall(r'<script\b[^>]*>(.*?)</script>', html, flags=re.S | re.I)
    for block_index, script in enumerate(script_blocks, 1):
        if "\\`" in script or "\\${" in script:
            return fail(
                f"script block {block_index} contains escaped template literals; "
                "write real backticks and ${...} expressions in final HTML"
            )
        if r"/<br\\s*\\/?>(\\n)?/gi" in script:
            return fail(
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
        return fail("no <section class=\"slide...\"> slides found")

    for i, section_open in enumerate(slides, 1):
        if 'data-slide-id=' not in section_open:
            return fail(f"slide {i} missing data-slide-id")
        if 'data-source=' not in section_open:
            return fail(f"slide {i} missing data-source")

    class_tags = [match.group(0) for match in re.finditer(r'<[^>]*class=(["\']).*?\1[^>]*>', markup, re.S)]
    if any("stage" in class_tokens(tag) for tag in class_tags):
        return fail('found legacy class="stage"; use .slide-stage inside the standard template')

    slide_stage_count = sum(1 for tag in class_tags if "slide-stage" in class_tokens(tag))
    if slide_stage_count < len(slides):
        return fail("each slide must contain .slide-stage")

    if "slide-${n}" in html:
        return fail("runtime contains unsafe unpadded slide-${n} lookup")

    if re.search(r'\.layout-cover\s+\.stage-mark\s*\{[^}]*position\s*:\s*fixed', html, re.S):
        return fail("cover stage-mark must stay section-bound; position: fixed is forbidden")

    if re.search(r'\.layout-cover\s+\.stage-mark\s*\{[^}]*right\s*:\s*clamp\(\s*-', html, re.S):
        return fail("cover stage-mark must not use negative right offsets")

    print(f"Deck contract valid: {html_path} ({len(slides)} slides)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
