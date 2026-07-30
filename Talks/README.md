# Talks — Data-Driven Science in Chemistry (BCCE Summer 2026)

A browsable version of the presentation, built with [reveal.js](https://revealjs.com/).

## View it locally
Open `index.html` in a browser (reveal.js loads from a CDN, so you need
internet access but no build step or server).

## Where this lives in the repo
This whole `Talks/` folder is meant to sit at the root of the `JMS` repo:

```
JMS/
  Talks/
    index.html
    generate_deck.py
    cover.html
    README.md
    slides/
      slide-01.jpg
      slide-02.jpg
      ...
```

## Publish on GitHub Pages
1. From your local `JMS` repo directory, copy this `Talks` folder in, then:
   ```bash
   git add Talks
   git commit -m "Add BCCE Summer 2026 talk as reveal.js deck"
   git push
   ```
2. In the repo on GitHub: **Settings → Pages**.
3. Under "Build and deployment", set **Source** to "Deploy from a branch",
   branch `main`, folder `/ (root)`. Save.
4. Since the deck is nested in a subfolder, it will be served at:
   `https://laserchemist.github.io/JMS/Talks/`

## Navigating
- Arrow keys or swipe to move between slides
- `F` for fullscreen
- `Esc` for a slide overview grid
- On the cover slide, scroll to read the full abstract

## Editing the cover / title slide
The first slide (title bar, presenter, abstract, conference link) comes
from `cover.html` — a plain HTML fragment, not something baked into the
Python script. Edit `cover.html` directly for wording or color changes,
then rebuild `index.html` (see below). If `cover.html` is missing, the
script falls back to a plain title-only cover automatically.

Cover color palette (defined in `generate_deck.py`, easy to retint):
- `--navy` / `--navy-2`: title bar background gradient
- `--teal`: accent for eyebrow text, chip borders, links
- `--gold`: title bar bottom border, conference panel accent
- `--paper`: warm off-white background for the rest of the cover

## Regenerating the deck
If you re-export new slide images into `slides/`, or edit `cover.html`,
rebuild `index.html` with:

```bash
python3 generate_deck.py --slides-dir slides --title "Data-Driven Science in Chemistry" --output index.html --cover-file cover.html
```
