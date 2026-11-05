# STATUS.md — Press Kit Page Starter Template

Copyright (c) 2026 Asdale Dynamics, LLC — MIT licensed (see LICENSE)

## What was built

A copy-ready, static, one-page press kit (media kit) for an author /
small publisher, written for Dylan Asdale (registered nurse turned AI
author, founder of Asdale Dynamics, LLC, author of *The Massive AI
Manual*). Everything is plain HTML/CSS — no JavaScript, no build tools,
no external dependencies — and works fully offline.

Delivered pieces:

- **Short and long bios** with copy-paste blocks and `.txt` download
  links (`index.html` → `#bios`, `assets/press/bio-short.txt`,
  `bio-long.txt`).
- **Headshot slots**: square (480×480) and tall (480×640) placeholder
  images (`SVG`) with download links, ready to be swapped for real
  headshots (`assets/headshots/`).
- **Book section**: cover art (400×600 SVG placeholder for *The Massive
  AI Manual*), blurb, metadata table, cover + one-sheet download links
  (`assets/covers/`, `assets/press/the-massive-ai-manual-one-sheet.txt`).
- **Fact sheet**: accessible HTML table plus a downloadable
  `fact-sheet.txt`.
- **Sample interview Q&As**: five starter Q&A pairs, downloadable as a
  single `sample-interview-qa.txt`.
- **Event-request card**: print/copy-friendly appearance-request
  checklist for libraries, clubs, and classrooms.
- **Contact block** with an obvious `.example` placeholder address.
- **Asset checklist script** (`check-assets.sh`, pure bash): verifies
  every `src`/`href` in `index.html` resolves to a real file, checks
  required assets exist and are non-empty, verifies local download
  links carry the `download` attribute, checks required content
  sections, and validates the LICENSE/README requirements.
- **Offline render test** (`tests/offline-render-test.py`, Python 3
  standard library only): parses the actual HTML offline and checks
  structure, alt text, image dimensions, section anchors, nav targets,
  heading hierarchy, download targets, and stylesheet wiring.

Distinct from the sibling templates: this is a single media-kit page
(not a whole author site like `author-site-starter-template`, and not a
support hub like `faq-help-center-starter-template`).

## How to run it

```bash
# Open directly
xdg-open index.html          # Linux (open on macOS)

# Or serve the folder (matches GitHub Pages behavior)
python3 -m http.server 8000  # then visit http://localhost:8000
```

## Verification results (this build)

- `bash check-assets.sh` → **24 passed, 0 failed**
  (`RESULT: ALL ASSET CHECKS PASS`; the only check pending earlier was
  STATUS.md itself, which now exists).
- `python3 tests/offline-render-test.py` → **65 checks run**
  `RESULT: OFFLINE RENDER TEST PASS`.
- Negative test: removing `assets/press/fact-sheet.txt` made both
  scripts fail as intended, then restored and both went green again.
- Static-serve smoke test: `index.html`, `styles.css`, cover SVG, and a
  press `.txt` all returned HTTP 200 from `python3 -m http.server`.

## GitHub Pages

Ready as-is: static files, relative paths, no build step. Settings →
Pages → Deploy from branch → main.

## Known gaps / intentional limitations

- Placeholder content by design: cover art and headshots are SVG
  placeholders; `press@asdaledynamics.example` must be replaced with a
  real press address; book format/price lines say "details pending".
- Print/PDF file downloads (e.g. PDF one-sheets) are not included; only
  `.txt` and `.svg` assets to keep the repo secret-free and tool-free.
- No JavaScript at all, so there is no live form on the event-request
  card — it is a copy-into-email checklist on purpose.
- Accessibility and large-print are addressed (base font floor, high
  contrast, print stylesheet, alt text, skip link), but a full manual
  screen-reader pass (NVDA/VoiceOver) has not been done by the author.
- The asset checklist script is line-oriented; it uses `grep` on the
  HTML, so extremely unusual formatting (e.g. a tag spanning lines with
  the href split across them) could be missed. The Python render test
  covers the same ground properly as a second net.
