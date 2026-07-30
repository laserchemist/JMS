#!/usr/bin/env python3
"""
generate_deck.py

Builds a self-contained reveal.js index.html for a folder of slide images
(exported from a PDF/Keynote deck). Each image becomes one full-bleed
reveal.js slide. Reveal.js itself is pulled from a CDN, so the repo you
push only needs this generated index.html plus the slides/ folder.

Usage:
    python3 generate_deck.py \
        --slides-dir slides \
        --title "BCCE Summer 2026" \
        --output index.html
"""

import argparse
import re
from pathlib import Path


REVEAL_VERSION = "5.1.0"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@{reveal_version}/dist/reveal.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@{reveal_version}/dist/theme/black.css" id="theme">

<style>
  :root {{
    --accent: #5ec8d8;
  }}
  html, body {{
    background: #111;
  }}
  .reveal .slides section {{
    padding: 0;
    height: 100%;
  }}
  .reveal .slides section img.slide-img {{
    width: 100%;
    height: 100%;
    max-height: none;
    margin: 0;
    border: none;
    box-shadow: none;
    object-fit: contain;
    background: #000;
  }}
  .reveal .progress {{
    color: var(--accent);
    height: 4px;
  }}
  .reveal .slide-number {{
    background: rgba(0,0,0,0.55);
    color: #ddd;
    font-size: 14px;
  }}
  /* cover / title slide */
  :root {{
    --navy: #0c2438;
    --navy-2: #143a54;
    --teal: #2fb8ae;
    --gold: #c9a24b;
    --paper: #f6f4ef;
  }}
  .reveal .slides section.cover-slide {{
    height: 100%;
    padding: 0;
  }}
  .cover {{
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    margin: 0 auto;
    text-align: left;
    color: #26313a;
    background: var(--paper);
    box-sizing: border-box;
    overflow: hidden;
  }}
  .cover.scroll .cover-body {{
    overflow-y: auto;
  }}
  .cover-bar {{
    background: linear-gradient(100deg, var(--navy) 0%, var(--navy-2) 65%, #1c4f66 100%);
    padding: 0.85em 3.5% 0.9em 3.5%;
    border-bottom: 4px solid var(--gold);
    flex: 0 0 auto;
  }}
  .cover-bar .eyebrow {{
    color: var(--teal);
    font-size: 0.42em;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 0 0 0.5em 0;
    font-weight: 600;
  }}
  .cover-bar h1 {{
    font-size: 1.55em;
    line-height: 1.28;
    margin: 0;
    color: #fdfdfb;
    font-weight: 700;
  }}
  .cover-body {{
    flex: 1 1 auto;
    padding: 1.1em 3.5% 1.3em 3.5%;
  }}
  .cover .meta {{
    display: flex;
    gap: 2.2em;
    flex-wrap: wrap;
    margin-bottom: 1em;
  }}
  .cover .meta .chip {{
    border-left: 3px solid var(--teal);
    padding-left: 0.7em;
  }}
  .cover .meta .label {{
    color: #1c4f66;
    font-size: 0.5em;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    margin-bottom: 0.25em;
    font-weight: 700;
  }}
  .cover .meta .value {{
    font-size: 0.68em;
    color: #26313a;
    font-weight: 600;
  }}
  .cover .meta .value .sub {{
    display: block;
    color: #6b6b63;
    font-size: 0.82em;
    font-weight: 400;
  }}
  .cover .abstract-label {{
    color: var(--navy);
    font-size: 0.48em;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    margin: 0.9em 0 0.5em 0;
    font-weight: 700;
    border-bottom: 1px solid #d8d3c4;
    padding-bottom: 0.4em;
  }}
  .cover .abstract {{
    font-size: 0.5em;
    line-height: 1.6;
    color: #3c4650;
    max-width: 1420px;
  }}
  .cover .abstract p {{
    margin: 0 0 1em 0;
  }}
  .cover .conference {{
    margin-top: 1.3em;
    padding: 0.8em 1em;
    background: #eef0e9;
    border-radius: 4px;
    border-left: 3px solid var(--gold);
    font-size: 0.52em;
    color: #3c4650;
    display: inline-block;
  }}
  .cover .conference a {{
    color: #1c4f66;
    font-weight: 700;
    text-decoration: none;
    border-bottom: 1px solid var(--teal);
  }}
  .cover .conference a:hover {{
    color: var(--teal);
  }}
  .cover .hint {{
    margin-top: 1em;
    color: #8a8a80;
    font-size: 0.38em;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }}
</style>
</head>
<body>
<div class="reveal">
  <div class="slides">
    <section class="cover-slide">
{cover_html}
    </section>
{slide_sections}
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/reveal.js@{reveal_version}/dist/reveal.js"></script>
<script>
  Reveal.initialize({{
    hash: true,
    controls: true,
    progress: true,
    slideNumber: true,
    center: true,
    transition: 'slide',
    width: 1920,
    height: 1080,
    margin: 0,
    minScale: 0.2,
    maxScale: 2.0,
    keyboard: true,
    touch: true,
  }});
</script>
</body>
</html>
"""

SLIDE_SECTION = '    <section data-background-color="#000">\n      <img class="slide-img" src="{src}" alt="Slide {num}" loading="lazy">\n    </section>\n'

DEFAULT_COVER = """      <div class="cover">
        <div class="cover-bar">
          <h1>{title}</h1>
        </div>
        <div class="cover-body">
          <p class="hint">Use \u2192 / \u2190 or swipe to browse &middot; press F for fullscreen</p>
        </div>
      </div>"""


def natural_key(path: Path):
    """Sort slide-2.jpg before slide-10.jpg."""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", path.name)]


def main():
    parser = argparse.ArgumentParser(description="Generate a reveal.js deck from slide images.")
    parser.add_argument("--slides-dir", default="slides", help="Folder of slide images (relative to output file)")
    parser.add_argument("--title", required=True, help="Deck title, shown on the cover slide and <title>")
    parser.add_argument("--output", default="index.html", help="Output HTML file path")
    parser.add_argument("--extensions", default="jpg,jpeg,png", help="Comma-separated image extensions to include")
    parser.add_argument(
        "--cover-file",
        default="cover.html",
        help="Path to an HTML fragment used as the cover/title slide. "
             "If missing, falls back to a plain title-only cover. "
             "Edit this file directly to change the cover without touching this script.",
    )
    args = parser.parse_args()

    slides_dir = Path(args.slides_dir)
    exts = {e.strip().lower() for e in args.extensions.split(",")}
    images = sorted(
        (p for p in slides_dir.iterdir() if p.suffix.lower().lstrip(".") in exts),
        key=natural_key,
    )

    if not images:
        raise SystemExit(f"No images found in {slides_dir} with extensions {exts}")

    sections = []
    for i, img in enumerate(images, start=1):
        rel_src = f"{slides_dir.as_posix()}/{img.name}"
        sections.append(SLIDE_SECTION.format(src=rel_src, num=i))

    cover_path = Path(args.cover_file)
    if cover_path.exists():
        cover_html = cover_path.read_text(encoding="utf-8")
        print(f"Using cover fragment from {cover_path}")
    else:
        cover_html = DEFAULT_COVER.format(title=args.title)
        print(f"No {cover_path} found — using plain title cover. "
              f"Create {cover_path} to customize (see README).")

    html = TEMPLATE.format(
        title=args.title,
        reveal_version=REVEAL_VERSION,
        cover_html=cover_html,
        slide_sections="".join(sections),
    )

    out_path = Path(args.output)
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path} with {len(images)} slides.")


if __name__ == "__main__":
    main()
