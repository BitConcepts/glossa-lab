#!/usr/bin/env python3
"""Spec 088 Stage S4 (T402) — Playwright render verification.

Renders the committed generated page (glossa-indus/map/
program-map.html) at desktop 1440x900 and mobile 390x844 and
checks the T402 design points against the generated data:
sections collapse; class filters change the visible set
correctly; search narrows to generated-field matches; header
counts match the coverage block; the restricted node shows
no standing, chip, or counts; the finds panel renders all
four kinds, the empty kind as an honest empty state.

Screenshots and this script's output (results.txt) are kept
in this directory with the stage record. Run with the
playwright venv:

    ~/workspace/venvs/playwright/bin/python verify_page.py

Exit code 0 iff every check passes.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PAGE_PATH = ROOT / "glossa-indus" / "map" / "program-map.html"
DATA = json.loads(
    (ROOT / "glossa-indus" / "map" / "program-map.json").read_text(
        encoding="utf-8"
    )
)
FINDS = json.loads(
    (ROOT / "glossa-indus" / "map" / "program-map-finds.json").read_text(
        encoding="utf-8"
    )
)

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), detail))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))


def visible_claim_rows(page) -> list[dict]:
    return page.evaluate(
        """() => [...document.querySelectorAll('.claim-row')]
          .filter(r => r.checkVisibility())
          .map(r => ({cls: r.dataset.class, search: r.dataset.search}))"""
    )


def main() -> int:
    coverage = DATA["coverage"]
    negative_ids = [
        n["id"] for n in DATA["nodes"]["claims"] if n["class"] == "negative"
    ]
    extracted_ids = [
        n["id"] for n in DATA["nodes"]["claims"] if n["population"] == "extracted"
    ]
    find_counts = Counter(f["kind"] for f in FINDS["finds"])
    url = PAGE_PATH.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # ── Desktop 1440x900 ──────────────────────────────────────────────
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(url)
        page.wait_for_selector("#pm-tree details.domain")

        check(
            "desktop: all claim rows rendered",
            page.locator(".claim-row").count() == coverage["claims"]["total"],
            f"{page.locator('.claim-row').count()} rows",
        )
        study_groups = page.locator("details.study:not(.doc-group)")
        check(
            "desktop: all study groups rendered",
            study_groups.count() == coverage["studies"]["total"],
            f"{study_groups.count()} studies, "
            f"{page.locator('details.doc-group').count()} document groups",
        )
        stamp_text = page.locator("#pm-stamp").inner_text()
        check(
            "desktop: header stamp is the artifact stamp",
            DATA["stamp"]["ledger_sha256"] in stamp_text
            and str(DATA["stamp"]["ledger_lines"]) in stamp_text
            and DATA["stamp"]["ledger_latest_entry_date"] in stamp_text,
            stamp_text[:110],
        )
        header_counts = page.locator(".pm-domain-count").all_inner_texts()
        counts_ok = len(header_counts) == len(coverage["domains"]) and all(
            any(
                d in text
                and f"{b['studies']} studies" in text
                and f"{b['claims']} claims" in text
                for text in header_counts
            )
            for d, b in coverage["domains"].items()
        )
        check(
            "desktop: header per-domain counts match the coverage block",
            counts_ok,
            "; ".join(header_counts),
        )
        page.screenshot(path=str(HERE / "desktop.png"))

        # A study expanded: claim rows with chips and standings.
        page.evaluate(
            """() => {
              const studies = [...document.querySelectorAll('details.study')];
              const target = studies.find(
                s => s.querySelectorAll('.claim-row').length > 0);
              target.open = true;
              target.scrollIntoView({block: 'start'});
            }"""
        )
        page.wait_for_timeout(250)
        first_row = page.locator(".claim-row").filter(
            has=page.locator(".chip")
        ).first
        check(
            "desktop: claim rows carry chip + standing text",
            "Ledger standing:" in first_row.inner_text(),
            first_row.inner_text()[:130],
        )
        page.screenshot(path=str(HERE / "desktop-study.png"))

        # Collapse: closing a domain hides its studies; reopening restores.
        first_domain = page.locator("details.domain").first
        first_domain.locator("summary").first.click()
        page.wait_for_timeout(200)
        hidden_ok = (
            first_domain.locator("details.study").first.is_visible() is False
        )
        first_domain.locator("summary").first.click()
        page.wait_for_timeout(200)
        restored_ok = (
            first_domain.locator("details.study").first.is_visible() is True
        )
        check(
            "desktop: domain section collapses and reopens",
            hidden_ok and restored_ok,
        )

        # Filter: Negative shows exactly the negative claims, all negative.
        page.locator('button[data-value="negative"]').click()
        page.wait_for_timeout(250)
        rows = visible_claim_rows(page)
        check(
            "desktop: Negative filter shows exactly the negative claims",
            len(rows) == len(negative_ids)
            and all(r["cls"] == "negative" for r in rows),
            f"{len(rows)} visible rows, expected {len(negative_ids)}",
        )
        page.screenshot(path=str(HERE / "desktop-filtered.png"))
        page.locator('button[data-value="all"]').click()
        page.wait_for_timeout(250)
        check(
            "desktop: All filter restores the full visible set",
            len(visible_claim_rows(page)) > len(negative_ids),
        )

        # Search: a distinctive extracted-claim fragment narrows to matches.
        query = extracted_ids[0][-14:].lower()
        page.fill("#pm-search", query)
        page.wait_for_timeout(250)
        rows = visible_claim_rows(page)
        check(
            "desktop: search narrows to generated-field matches",
            0 < len(rows) < coverage["claims"]["total"]
            and all(query in r["search"] for r in rows),
            f"query {query!r}: {len(rows)} rows",
        )
        page.fill("#pm-search", "")
        page.wait_for_timeout(250)

        # Restricted: name-only — no chip, no counts, no derived standing.
        restricted = page.locator("details.study.restricted")
        check(
            "desktop: exactly one restricted study node",
            restricted.count() == 1,
        )
        restricted.evaluate("n => { n.open = true; n.scrollIntoView({block: 'center'}); }")
        page.wait_for_timeout(250)
        summary = restricted.locator("summary").first
        # The restriction binds the study node's own
        # presentation (its header row and its name-only
        # line); its member claims keep their own nodes and
        # standings, as they do in program-map.json itself.
        name_only = restricted.locator(".name-only").inner_text()
        check(
            "desktop: restricted node is name-only",
            summary.locator(".chip").count() == 0
            and summary.locator(".counts").count() == 0
            and "Ledger standing" not in summary.inner_text()
            and name_only == "executed — held under the Roif gate",
            (summary.inner_text() or "")[:110],
        )
        page.screenshot(path=str(HERE / "desktop-restricted.png"))

        # Finds panel: four kinds, counts from the find list, honest empty.
        kinds = page.locator(".find-kind")
        find_texts = kinds.all_inner_texts()
        finds_ok = kinds.count() == 4 and all(
            any(label in t and f"— {find_counts.get(kind, 0)}" in t for t in find_texts)
            for kind, label in (
                ("bundle_less_study", "Bundle-less studies"),
                ("judgment_call", "Judgment calls"),
                ("extracted_null_falsifier", "Extracted claims with no falsifier"),
                ("restricted_node", "Restricted nodes"),
            )
        )
        judgment_text = next(
            t for t in find_texts if "Judgment calls" in t
        )
        check(
            "desktop: finds panel renders all four kinds with find-list counts",
            finds_ok,
            f"judgment_call live count {find_counts.get('judgment_call', 0)}",
        )
        check(
            "desktop: empty judgment-call kind shows its honest empty state",
            "None on the current ledger." in judgment_text,
        )
        page.close()

        # ── Mobile 390x844 ────────────────────────────────────────────────
        mobile = browser.new_page(viewport={"width": 390, "height": 844})
        mobile.goto(url)
        mobile.wait_for_selector("#pm-tree details.domain")
        check(
            "mobile: page renders, header and tree visible",
            mobile.locator("#pm-stamp").is_visible()
            and mobile.locator("details.domain").first.is_visible()
            and mobile.locator(".claim-row").count()
            == coverage["claims"]["total"],
        )
        mobile.screenshot(path=str(HERE / "mobile.png"))
        mobile.close()
        browser.close()

    failed = [r for r in RESULTS if not r[1]]
    summary = f"{len(RESULTS) - len(failed)}/{len(RESULTS)} checks passed"
    print(summary)
    (HERE / "results.txt").write_text(
        "\n".join(
            f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {d}" if d else "")
            for name, ok, d in RESULTS
        )
        + f"\n{summary}\n",
        encoding="utf-8",
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
