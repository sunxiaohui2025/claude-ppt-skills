#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "assets" / "html-template"
STYLE_BODY_CLASSES = {
    "dune": "",
    "ink-classic": "style-ink-classic",
    "indigo-porcelain": "style-indigo-porcelain",
    "white-stage": "style-white-stage",
    "editorial-mono": "style-editorial-mono",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_class_token(html: str, token: str) -> bool:
    for match in re.finditer(r'class=(["\'])(.*?)\1', html, re.S):
        if token in match.group(2).split():
            return True
    return False


def merge_deck(deck_folder: str) -> dict:
    deck = Path(deck_folder).resolve()
    sources = deck / "sources"
    if not sources.exists():
        raise FileNotFoundError(f"Missing sources folder: {sources}")
    config_path = sources / "deck.config.json"
    config = json.loads(read(config_path)) if config_path.exists() else {}
    title = config.get("title", deck.name)
    style_pack = config.get("stylePack", config.get("style", "dune"))
    if style_pack not in STYLE_BODY_CLASSES:
        allowed = ", ".join(sorted(STYLE_BODY_CLASSES))
        raise ValueError(f"Unknown stylePack '{style_pack}'. Allowed: {allowed}")
    body_class = STYLE_BODY_CLASSES[style_pack]
    body_attrs = f' class="{body_class}"' if body_class else ""
    base_css = read(TEMPLATE_DIR / "base.css")
    custom_css = read(sources / "style.css") if (sources / "style.css").exists() else ""
    runtime_js = read(TEMPLATE_DIR / "runtime.js")
    slide_files = sorted(sources.glob("slide-*.html"))
    if not slide_files:
        raise ValueError("No slide-*.html files found")
    slides = []
    for i, path in enumerate(slide_files, 1):
        html = read(path).strip()
        if not re.search(r'<section\s+class="slide', html):
            raise ValueError(f"Slide source must contain <section class=\"slide...\">: {path}")
        if has_class_token(html, "stage"):
            raise ValueError(f"Slide source must use .slide-stage, not legacy .stage: {path}")
        if len([m for m in re.finditer(r'class=(["\'])(.*?)\1', html, re.S) if "slide-stage" in m.group(2).split()]) != 1:
            raise ValueError(f"Slide source must contain exactly one .slide-stage wrapper: {path}")
        if 'section-ghost-number' in html and re.search(r'</div>\s*</div>\s*<div class="proof-object', html):
            raise ValueError(f"Numbered section slide must not contain top-level .proof-object; split content to next slide: {path}")
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
        .replace("{{BODY_ATTRS}}", body_attrs)
        .replace("{{DECK_CSS}}", base_css + "\n\n" + custom_css)
        .replace("{{SLIDES}}", "\n\n".join(slides))
        .replace("{{DECK_JS}}", runtime_js))
    output_path = deck / "index.html"
    output_path.write_text(output, encoding="utf-8")
    validator = SKILL_DIR / "scripts" / "validate_deck_contract.py"
    result = subprocess.run([sys.executable, str(validator), str(output_path)], text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError((result.stdout + "\n" + result.stderr).strip())
    return {
        "ok": True,
        "output_path": str(output_path),
        "slides": len(slides),
        "validator_output": result.stdout.strip(),
    }


def run(deck_folder: str, **kwargs) -> dict:
    return merge_deck(deck_folder)


def generate(deck_folder: str = None, deck: str = None, **kwargs) -> dict:
    return merge_deck(deck_folder or deck or kwargs.get("deck_folder") or kwargs.get("deck"))


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: merge_deck.py <deck-folder>", file=sys.stderr)
        return 2
    try:
        result = merge_deck(sys.argv[1])
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(result["validator_output"])
    print(f"Wrote {result['output_path']} ({result['slides']} slides)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
