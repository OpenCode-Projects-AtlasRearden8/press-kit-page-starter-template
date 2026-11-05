#!/usr/bin/env python3
"""offline-render-test.py — offline render/structure test for the press kit.

Parses index.html with the Python standard library (no network, no
build tools, no browser) and asserts the page would render completely:

  * valid HTML structure (doctype, head, body, stylesheet link)
  * every image has alt text and matching width/height attributes
  * all required sections exist and heading hierarchy is sane
  * nav anchor links point to real section ids
  * all download links point to files that exist locally

Usage: python3 tests/offline-render-test.py
Exit code 0 = pass, nonzero = fail.
"""

import os
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")

errors: list[str] = []
checks = 0


def check(condition, message):
    global checks
    checks += 1
    if not condition:
        errors.append(message)


class PressKitParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.doctype = False
        self.in_body = False
        self.body_text_length = 0
        self.depth = 0
        self.headings = []          # (tag, level)
        self.section_ids = set()
        self.imgs = []              # dicts of img attributes
        self.links = []             # (href, has_download)
        self.cur_heading = None
        self.in_heading = False

    def handle_decl(self, decl):
        if decl.strip().lower().startswith("doctype html"):
            self.doctype = True

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "body":
            self.in_body = True
        if tag in ("h1", "h2", "h3", "h4"):
            self.cur_heading = tag
            self.in_heading = True
        if tag in ("section", "main") and a.get("id"):
            self.section_ids.add(a["id"])
        if tag == "img":
            self.imgs.append({"src": a.get("src"), "alt": a.get("alt"),
                              "width": a.get("width"), "height": a.get("height")})
        if tag == "a" and a.get("href"):
            self.links.append((a["href"], "download" in a))
        if tag == "link" and a.get("rel") == "stylesheet":
            self.links.append((a.get("href"), None))

    def handle_endtag(self, tag):
        if tag == "body":
            self.in_body = False
        if tag in ("h1", "h2", "h3", "h4"):
            self.in_heading = False
            self.headings.append(self.cur_heading)

    def handle_data(self, data):
        if self.in_body and self.in_heading:
            self.body_text_length += sum(1 for c in data if not c.isspace())
        elif self.in_body:
            self.body_text_length += sum(1 for c in data if not c.isspace())


def main():
    if not os.path.isfile(INDEX):
        print(f"FAIL: {INDEX} not found")
        return 1

    with open(INDEX, encoding="utf-8") as fh:
        src = fh.read()

    parser = PressKitParser()
    parser.feed(src)
    parser.close()

    # --- structure ---
    check(parser.doctype, "missing <!DOCTYPE html> declaration")
    check('lang="en"' in src, "html element lacks lang attribute")
    check("<head>" in src and "</head>" in src, "<head> element missing")
    check("<body>" in src and "</body>" in src, "<body> element missing")
    check('rel="stylesheet"' in src and 'href="styles.css"' in src,
          "stylesheet link to styles.css missing")
    check(os.path.isfile(os.path.join(ROOT, "styles.css")),
          "styles.css file does not exist on disk")
    check("<title>" in src and "Press Kit" in src, "page title missing")
    check('name="description"' in src, "meta description missing")

    # --- required sections ---
    required_ids = {"bios", "headshots", "books", "fact-sheet",
                    "interviews", "events", "contact", "main"}
    missing = required_ids - parser.section_ids
    check(not missing, f"missing section ids: {sorted(missing)}")

    # --- headings hierarchy ---
    check(len(parser.headings) > 0, "no headings found")
    check(parser.headings and parser.headings[0] == "h1", "first heading is not h1")
    for i, tag in enumerate(parser.headings):
        level = int(tag[1])
        if i == 0:
            continue
        prev = int(parser.headings[i - 1][1])
        check(level <= prev + 1,
              f"heading level jump before heading #{i + 1} ({tag})")

    # --- images ---
    for img in parser.imgs:
        check(img["src"], f"img missing src: {img}")
        path = os.path.join(ROOT, img["src"])
        check(os.path.isfile(path), f"img file missing: {img['src']}")
        check(img["alt"], f"img missing alt text: {img['src']}")
        check(img["width"] and img["height"],
              f"img missing width/height attributes: {img['src']}")

    # --- links ---
    for href, has_download in parser.links:
        if href.startswith("#"):
            target = href[1:]
            check(target in parser.section_ids or target == "",
                  f"nav link points to unknown id: {href}")
        elif href.startswith(("http:", "https:", "mailto:")):
            pass  # external, allowed
        elif has_download is None:
            # stylesheet: only verify the file exists
            check(os.path.isfile(os.path.join(ROOT, href)),
                  f"stylesheet file missing: {href}")
        else:
            path = os.path.join(ROOT, href)
            check(os.path.isfile(path), f"link target missing: {href}")
            check(has_download, f"local asset link lacks download attr: {href}")

    # --- visible content sanity ---
    check(parser.body_text_length > 500,
          "page body has too little text to be a complete press kit")

    # --- report ---
    print(f"Press kit offline render test: {checks} checks run")
    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print(f"RESULT: FAILED ({len(errors)} problem(s))")
        return 1
    print("RESULT: OFFLINE RENDER TEST PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
