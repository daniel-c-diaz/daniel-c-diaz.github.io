# ddiaz-site-slim

Personal academic site for Daniel Diaz. One page, one stylesheet, no build step.

```
index.html          everything
assets/style.css    ~135 lines
assets/CV_DanielDiaz.pdf
assets/img/         portrait goes here
```

Edit `index.html` directly. There is no templating, no generator and nothing to
install — the sections are plain HTML in the order they appear on the page.

## Publish

```bash
gh repo create ddiaz-site-slim --public --source=. --remote=origin --push
```

Then **Settings → Pages → Deploy from a branch → `main` / `(root)`**. It appears
at `https://ddiaz006.github.io/ddiaz-site-slim/`.

To make it your main site instead, rename the repository to
`ddiaz006.github.io` — every path here is relative, so it works at either
address. Update the two `og:url` / `canonical` tags in `index.html` if you do.

## Still to do

- [ ] Drop a square photo at `assets/img/portrait.jpg`, then replace the
      placeholder `<div class="portrait portrait-ph">…</div>` with
      `<img class="portrait" src="assets/img/portrait.jpg" alt="Daniel Diaz">`
- [ ] Add a news entry whenever something happens — it is the section people
      actually check to see whether a site is maintained

## Local preview

```bash
python3 -m http.server 4174
```
