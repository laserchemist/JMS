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
  /* simple title/cover slide */
  .cover {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    color: #f2f2f2;
  }}
  .cover h1 {{
    font-size: 2.2em;
    margin-bottom: 0.3em;
  }}
  .cover p {{
    color: #9ad6df;
    font-size: 0.9em;
    letter-spacing: 0.04em;
    text-transform: uppercase;
  }}
</style>
</head>
<body>
<div class="reveal">
  <div class="slides">
    <section>
      <div class="cover">
        <h1>{title}</h1>
        <p>Use \u2192 / \u2190 or swipe to browse &middot; press F for fullscreen &middot; press S for speaker notes</p>
      </div>
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


def natural_key(path: Path):
    """Sort slide-2.jpg before slide-10.jpg."""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", path.name)]


def main():
    parser = argparse.ArgumentParser(description="Generate a reveal.js deck from slide images.")
    parser.add_argument("--slides-dir", default="slides", help="Folder of slide images (relative to output file)")
    parser.add_argument("--title", required=True, help="Deck title, shown on the cover slide and <title>")
    parser.add_argument("--output", default="index.html", help="Output HTML file path")
    parser.add_argument("--extensions", default="jpg,jpeg,png", help="Comma-separated image extensions to include")
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

    html = TEMPLATE.format(
        title=args.title,
        reveal_version=REVEAL_VERSION,
        slide_sections="".join(sections),
    )

    out_path = Path(args.output)
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path} with {len(images)} slides.")


if __name__ == "__main__":
    main()
