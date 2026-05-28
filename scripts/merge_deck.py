#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "assets" / "html-template"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_class_token(html: str, token: str) -> bool:
    for match in re.finditer(r'class=(["\'])(.*?)\1', html, re.S):
        if token in match.group(2).split():
            return True
    return False


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: merge_deck.py <deck-folder>", file=sys.stderr)
        return 2
    deck = Path(sys.argv[1]).resolve()
    sources = deck / "sources"
    if not sources.exists():
        print(f"Missing sources folder: {sources}", file=sys.stderr)
        return 1
    config_path = sources / "deck.config.json"
    config = json.loads(read(config_path)) if config_path.exists() else {}
    title = config.get("title", deck.name)
    base_css = read(TEMPLATE_DIR / "base.css")
    custom_css = read(sources / "style.css") if (sources / "style.css").exists() else ""
    runtime_js = read(TEMPLATE_DIR / "runtime.js")
    slide_files = sorted(sources.glob("slide-*.html"))
    if not slide_files:
        print("No slide-*.html files found", file=sys.stderr)
        return 1
    slides = []
    for i, path in enumerate(slide_files, 1):
        html = read(path).strip()
        if not re.search(r'<section\s+class="slide', html):
            print(f"Slide source must contain <section class=\"slide...\">: {path}", file=sys.stderr)
            return 1
        if has_class_token(html, "stage"):
            print(f"Slide source must use .slide-stage, not legacy .stage: {path}", file=sys.stderr)
            return 1
        if len([m for m in re.finditer(r'class=(["\'])(.*?)\1', html, re.S) if "slide-stage" in m.group(2).split()]) != 1:
            print(f"Slide source must contain exactly one .slide-stage wrapper: {path}", file=sys.stderr)
            return 1
        if 'section-ghost-number' in html and re.search(r'</div>\s*</div>\s*<div class="proof-object', html):
            print(f"Numbered section slide must not contain top-level .proof-object; split content to next slide: {path}", file=sys.stderr)
            return 1
        html = re.sub(r'data-slide-id="[^"]*"', f'data-slide-id="slide-{i:02d}"', html)
        if 'data-slide-id=' not in html.split('>', 1)[0]:
            html = html.replace('<section ', f'<section data-slide-id="slide-{i:02d}" ', 1)
        html = re.sub(r'data-source="[^"]*"', f'data-source="sources/{path.name}"', html)
        if 'data-source=' not in html.split('>', 1)[0]:
            html = html.replace('<section ', f'<section data-source="sources/{path.name}" ', 1)
        slides.append("    " + html.replace("\n", "\n    "))
    template = read(TEMPLATE_DIR / "index.template.html")
    output = (template
        .replace("{{DECK_TITLE}}", title)
        .replace("{{DECK_CSS}}", base_css + "\n\n" + custom_css)
        .replace("{{SLIDES}}", "\n\n".join(slides))
        .replace("{{DECK_JS}}", runtime_js))
    output_path = deck / "index.html"
    output_path.write_text(output, encoding="utf-8")
    validator = SKILL_DIR / "scripts" / "validate_deck_contract.py"
    result = subprocess.run([sys.executable, str(validator), str(output_path)], text=True, capture_output=True)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result.returncode
    print(result.stdout.strip())
    print(f"Wrote {output_path} ({len(slides)} slides)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
