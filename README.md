# Press Kit Page — Starter Template

A copy-ready **static press kit / media kit page** for authors and small
publishers. One HTML file + one stylesheet, no build tools, works offline,
and is ready for GitHub Pages. Built and maintained by
**Asdale Dynamics, LLC**.

This kit is written for **Dylan Asdale** — registered nurse turned AI author
and founder of Asdale Dynamics, LLC (Indiana, formed October 2026) — author
of *The Massive AI Manual*. He explains AI "like a friend would": plain
English, step by step, never condescending. The template is fully generic:
swap the names, bios, and assets to make it your own.

## Distinct from other templates

- `author-site-starter-template` is a whole author website (home, books,
  blog, about...). This template is **one media-kit page** only, meant to be
  handed to journalists, podcasters, and event organizers.
- `faq-help-center-starter-template` is a Q&A/support hub. This template is
  for **press and media**, not customer support.

## What is inside

| Piece | Where |
|---|---|
| Short + long bios | `index.html` → `#bios` |
| Headshot slots (square + tall placeholders) | `index.html` → `#headshots`, `assets/headshots/` |
| Book cover + one-sheet with download links | `index.html` → `#books`, `assets/covers/` |
| Fact sheet table | `index.html` → `#fact-sheet` |
| Sample interview Q&As | `index.html` → `#interviews` |
| Event-request card (copy-into-email checklist) | `index.html` → `#events` |
| Contact block (placeholder address — replace it) | `index.html` → `#contact` |
| Asset checklist script | `check-assets.sh` |
| Offline render test | `tests/offline-render-test.py` |

## How to run it

Nothing to build. Just open the page:

```bash
# Option A: open directly
open index.html            # macOS
xdg-open index.html        # Linux

# Option B: serve the folder (recommended, matches GitHub Pages)
python3 -m http.server 8000
# then visit http://localhost:8000
```

## How to test it

```bash
./check-assets.sh                        # every referenced asset exists
python3 tests/offline-render-test.py     # offline render/structure checks
```

Both scripts use only the shell and Python 3 standard library — no installs,
no network. `check-assets.sh` walks every `src`/`href` in `index.html`,
confirms the file exists, verifies local asset links carry the `download`
attribute, and checks required content sections. The render test parses the
HTML offline and verifies structure, alt text, image dimensions, section
anchors, heading order, and that all download targets are real files.

## Customizing

1. Replace placeholder headshots in `assets/headshots/` (keep file names or
   update both `src` and `download` links).
2. Swap the cover art in `assets/covers/` (cover is a 400x600 SVG; use
   2:3 ratio art for ebooks/print).
3. Edit the two bios, fact sheet, and Q&As in `index.html`, and mirror the
   text into `assets/press/*.txt` so downloads match the page.
4. Replace `press@asdaledynamics.example` with your real press address.
5. Adding a book? Copy the `book-card` block, add its cover, then re-run
   `./check-assets.sh`.

## GitHub Pages

The repo is Pages-ready as-is: static files only, relative paths, no
build step. Enable Pages on the repository (Settings → Pages → Deploy from
branch → main), and the kit is live at `https://<user>.github.io/<repo>/`.

## Design notes

- **Large-print friendly:** roomy base font size, high contrast, generous
  line height, `prefers-reduced-motion` respected, screen-reader skip link,
  and a print stylesheet that strips navigation.
- **Local-first / offline:** no external fonts, scripts, or tracking; all
  assets are local; everything renders with no network.
- **No secrets or personal data:** contact details use an obvious
  `.example` placeholder until you swap them in.

## License

MIT — see `LICENSE`. Copyright (c) 2026 Asdale Dynamics, LLC. Press copy
inside this template may be quoted with attribution.
