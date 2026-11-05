#!/usr/bin/env bash
# check-assets.sh — checklist script for the press kit template.
# Verifies every locally referenced asset in index.html (src, href)
# actually exists on disk, plus required template files.
#
# Usage: ./check-assets.sh
# Exit code 0 = all good, nonzero = problems found. No dependencies.

set -u

cd "$(dirname "$0")"
fail=0
pass=0

say_pass() { printf '  OK  %s\n' "$1"; pass=$((pass + 1)); }
say_fail() { printf 'FAIL  %s\n' "$1"; fail=$((fail + 1)); }

echo "1. Required template files"
for f in index.html styles.css README.md LICENSE STATUS.md check-assets.sh tests/offline-render-test.py; do
  if [ -f "$f" ]; then say_pass "$f"; else say_fail "missing: $f"; fi
done

echo "2. Downloadable / referenced assets in index.html"
# Pull src="..." and href="..." values, ignore external and anchor links.
refs=$(grep -oE '(src|href)="[^"]+"' index.html \
  | sed -E 's/^(src|href)="//; s/"$//' \
  | grep -vE '^(#|https?:|mailto:)' | sort -u)

# Find local asset <a> tags missing the download attribute.
# Match whole tags so trailing attributes are seen.
dl_missing=$(grep -oE '<a [^>]+>' index.html \
  | grep 'href="[^"]' \
  | grep -vE 'href="#|href="https?:|href="mailto:' \
  | grep -v 'download[>"]' || true)
if [ -z "$dl_missing" ]; then
  say_pass "all local asset links carry the download attribute"
else
  say_fail "local asset link(s) missing download attribute:"
  printf '%s\n' "$dl_missing" | sed 's/^/      /'
fi

echo "4. Expected content sections in index.html"
for section in bios headshots books fact-sheet interviews events contact; do
  if grep -q "id=\"$section\"" index.html; then
    say_pass "section anchor id=$section"
  else
    say_fail "missing section anchor id=$section"
  fi
done

for term in "Short bio" "Long bio" "Fact Sheet" "Sample Interview" "Event Requests" "Download cover" "Download short bio" "Download long bio"; do
  if grep -q "$term" index.html; then
    say_pass "content present: \"$term\""
  else
    say_fail "content missing: \"$term\""
  fi
done

echo "5. LICENSE / README requirements"
grep -q "Copyright (c) 2026 Asdale Dynamics, LLC" LICENSE \
  && say_pass "LICENSE copyright line" \
  || say_fail "LICENSE copyright line missing or wrong"
grep -q "Asdale Dynamics, LLC" README.md \
  && say_pass "README credits Asdale Dynamics, LLC" \
  || say_fail "README does not credit Asdale Dynamics, LLC"

echo
echo "Checked: $pass passed, $fail failed"
if [ "$fail" -gt 0 ]; then
  echo "RESULT: FAILED"
  exit 1
fi
echo "RESULT: ALL ASSET CHECKS PASS"
