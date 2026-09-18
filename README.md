# ddiaz-site-slim

Personal site for Daniel Diaz. One HTML file, one stylesheet, no build step.

```
index.html               everything
assets/style.css         ~170 lines
assets/img/portrait.jpg  800x800
assets/img/event-display.png CMS published figure for EXO-20-003 (credited)
assets/CV_DanielDiaz.pdf
```

## Layout

A sticky identity rail on the left (photo, name, links, "previously") beside a
wide content column that uses the full browser width rather than a narrow
centred measure:

- **Intro**: the physics motivation, then machine learning as the method throughout
- **Research**: four blocks in a 2x2 grid. One physics (long-lived particles and
  dark sectors), three machine learning (real-time ML, ML for physics analysis,
  AI infrastructure for science). Keep the two blocks in each row within ~20
  words of each other or the grid shows a gap.
- **One event**: the EXO-20-003 event display
- **Selected work | Recent**: side by side, single-column publication list
- **Students and teaching**: two columns of prose

The page is pitched at HEP + AI/ML faculty searches, so three of the four research
blocks are machine learning. Every
claim is sourced from a paper, the CV or research statement, or a CMS page.

Breakpoints account for the 280 px rail, not just the viewport. The
`Selected work | Recent` split only goes two-up at 75 rem, because below that
the content column is too narrow for two readable columns.

## The event display

The "One event" band shows a real CMS event from EXO-20-003, the search Daniel
led. It is a **click-to-load facade**: the page ships a static poster
(`assets/img/event-display.png`, the figure CMS published) and only loads
CERN's live 3D viewer at <https://cms3d.web.cern.ch/EXO-20-003/> when the
visitor asks for it.

That is deliberate, for three reasons:

- the CERN viewer takes ~10 s to pull its detector geometry, which would
  otherwise stall the page;
- no third-party request or cookie until the visitor opts in;
- CMS's viewer overlays two blocks of text sized for a desktop window, and they
  collide with each other below roughly 960 px. It is cross-origin, so it cannot
  be restyled from here. Below 960 px the button opens it in a new tab instead
  of embedding it.

Nothing from CERN is rehosted except the published poster image, which is
credited in the caption along with the analysis, the CMS feature and the paper.

## Theme

Light by default, whatever the visitor's OS prefers. The toggle in the rail
switches to dark and the choice is remembered in `localStorage`. A small inline
script in `<head>` applies the stored preference before first paint so there is
no flash.

## Publish

Live at **https://ddiaz006.github.io**, served by GitHub Pages from `main`
of the `ddiaz006/ddiaz006.github.io` repository. Push to `main` and the site
updates within a minute or two.

## Keeping it current

Add a `<div>` to the `Recent` list when something happens. That section is what
tells a visitor the site is maintained, and it is the only part that goes stale
on its own.

## Local preview

```bash
python3 -m http.server 4174
```
