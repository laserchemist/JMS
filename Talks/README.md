# Talks — BCCE Summer 2026

A browsable version of the presentation, built with [reveal.js](https://revealjs.com/).

## View it locally
Open `index.html` in a browser (reveal.js loads from a CDN, so you need
internet access but no build step or server).

## Where this lives in the repo
This whole `Talks/` folder is meant to be dropped into the root of the
`JMS` repo, so the final layout looks like:

```
JMS/
  Talks/
    index.html
    generate_deck.py
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
   (not the bare repo URL — GitHub Pages only auto-serves an `index.html`
   sitting at the very root of the repo for the bare URL).

## Navigating
- Arrow keys or swipe to move between slides
- `F` for fullscreen
- `Esc` for a slide overview grid

## Regenerating the deck
If you re-export new slide images into `slides/`, rebuild `index.html` with:

```bash
python3 generate_deck.py --slides-dir slides --title "BCCE Summer 2026" --output index.html
```
