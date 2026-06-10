#!/usr/bin/env python3
"""Render-level sanity checks for generated HTML decks.

This script complements validate_deck_contract.py. The contract validator checks
static structure; this script opens the merged deck in a real browser viewport
and catches layout failures such as stacked slides, viewport overflow, and
content colliding with the footer on 13-inch laptop sizes.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


VIEWPORTS = [(1366, 768), (1280, 720), (1920, 1080)]
CHROME_CANDIDATES = [
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
]


def resolve_html(path_value: str) -> Path:
    path = Path(path_value).expanduser().resolve()
    if path.is_dir():
        path = path / "index.html"
    if not path.exists():
        raise FileNotFoundError(f"missing deck HTML: {path}")
    return path


def check_deck(html_path: Path, screenshots_dir: Path | None = None) -> list[str]:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # pragma: no cover - depends on local environment
        raise RuntimeError(
            "render_check.py requires Playwright. Install with: "
            "python3 -m pip install playwright && python3 -m playwright install chromium. "
            "If Google Chrome is installed, the script can also use it as a fallback."
        ) from exc

    failures: list[str] = []
    url = html_path.as_uri()

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            executable = next((path for path in CHROME_CANDIDATES if path.exists()), None)
            if not executable:
                raise
            browser = p.chromium.launch(executable_path=str(executable))
        try:
            for width, height in VIEWPORTS:
                page = browser.new_page(viewport={"width": width, "height": height})
                page.goto(url, wait_until="load")
                # Freeze entrance animations so geometry checks see final layout,
                # and wait for CJK font fallback to settle metrics.
                page.add_style_tag(
                    content="*{animation-duration:0s !important;animation-delay:0s !important;transition-duration:0s !important}"
                )
                page.evaluate("document.fonts.ready")
                page.wait_for_timeout(250)
                slide_count = page.evaluate("document.querySelectorAll('.slide').length")
                if not slide_count:
                    failures.append(f"{width}x{height}: no slides found")
                    continue

                viewport_dir = None
                if screenshots_dir:
                    viewport_dir = screenshots_dir / f"{width}x{height}"
                    viewport_dir.mkdir(parents=True, exist_ok=True)

                for index in range(slide_count):
                    page.evaluate("(slideIndex) => showSlide(slideIndex)", index)
                    page.wait_for_timeout(120)
                    result = page.evaluate(
                        """
                        () => {
                          const visibleSlides = Array.from(document.querySelectorAll('.slide'))
                            .filter((slide) => {
                              const rect = slide.getBoundingClientRect();
                              const style = getComputedStyle(slide);
                              return style.display !== 'none' && rect.width > 5 && rect.height > 5;
                            });
                          const active = document.querySelector('.slide.active');
                          if (!active) return { ok: false, reason: 'missing active slide' };
                          const footer = document.querySelector('.footer')?.getBoundingClientRect();
                          const slideRect = active.getBoundingClientRect();
                          const stage = active.querySelector('.slide-stage');
                          if (!stage) return { ok: false, reason: 'missing .slide-stage' };
                          const footerTop = footer ? footer.top : slideRect.bottom - 34;
                          const ignoreSelector = [
                            '.cover-atmosphere',
                            '.stage-mark',
                            '.thanks-mark',
                            '.thanks-orbit',
                            '.section-orbit',
                            '.section-sand',
                            '.ambient-mark',
                            '.noise',
                            'svg[aria-hidden="true"]'
                          ].join(',');
                          const offenders = [];
                          const nodes = Array.from(stage.querySelectorAll('*'))
                            .filter((node) => !node.closest(ignoreSelector));
                          for (const node of nodes) {
                            const rect = node.getBoundingClientRect();
                            const style = getComputedStyle(node);
                            if (style.visibility === 'hidden' || style.display === 'none') continue;
                            if (rect.width < 2 || rect.height < 2) continue;
                            const tooHigh = rect.top < slideRect.top + 14;
                            const tooLow = rect.bottom > Math.min(footerTop - 8, slideRect.bottom - 34);
                            const tooLeft = rect.left < slideRect.left + 10;
                            const tooRight = rect.right > slideRect.right - 10;
                            if (tooHigh || tooLow || tooLeft || tooRight) {
                              offenders.push({
                                tag: node.tagName.toLowerCase(),
                                cls: String(node.className || '').slice(0, 80),
                                text: String(node.textContent || '').trim().slice(0, 36),
                                rect: {
                                  top: Math.round(rect.top),
                                  bottom: Math.round(rect.bottom),
                                  left: Math.round(rect.left),
                                  right: Math.round(rect.right)
                                }
                              });
                              if (offenders.length >= 5) break;
                            }
                          }
                          return {
                            ok: visibleSlides.length === 1 && offenders.length === 0,
                            visibleSlides: visibleSlides.length,
                            offenders
                          };
                        }
                        """
                    )
                    label = f"{width}x{height} slide {index + 1:02d}"
                    if result.get("visibleSlides") != 1:
                        failures.append(f"{label}: {result.get('visibleSlides')} visible slides")
                    for offender in result.get("offenders", []):
                        failures.append(
                            f"{label}: overflow {offender['tag']}.{offender['cls']} "
                            f"{offender['rect']} {offender['text']!r}"
                        )
                    if viewport_dir:
                        page.screenshot(path=str(viewport_dir / f"slide-{index + 1:02d}.png"))
                page.close()
        finally:
            browser.close()

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Render-check a merged Dune keynote HTML deck.")
    parser.add_argument("deck", help="Deck folder or merged index.html")
    parser.add_argument("--screenshots", help="Optional folder for per-slide screenshots")
    args = parser.parse_args()

    try:
        html_path = resolve_html(args.deck)
        screenshots_dir = Path(args.screenshots).expanduser().resolve() if args.screenshots else None
        failures = check_deck(html_path, screenshots_dir)
    except Exception as exc:
        print(f"Render check failed: {exc}", file=sys.stderr)
        return 1

    if failures:
        print("Render check found layout issues:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Render check passed: {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
