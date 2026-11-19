#!/usr/bin/env python3
"""Spec 095 T404 remediation — dashboard-leg re-run driver.

Re-runs the eight-step researcher protocol and the accessibility
pass over the seven researcher-dashboard surfaces, as constituted
by records/t404-dashboard-leg-addendum-2026-11-18.md, against a
scratch instance of the remediated tree, scored against the
thresholds fixed in advance in records/t404-thresholds-2026-11-17.md
(P1 at least 6 of 8 completable; A1 zero axe-core critical; A2 at
most 3 serious plus keyboard-traversable primary navigation).

The instance is the same audit instance the filed T404 driver
uses (~/glossa-work/spec095-s4/audit-instance on 127.0.0.1:8417,
GLOSSA_API_AUTH=off), started and owned by this driver. The pass
evidence for P6 is the instance's staging store, not the screen,
per records/t404-scoring-corrections.json. P8 is verified from the
downloaded file's contents. The driver also re-performs the F15
served-vs-dist identity check against the asset the served
index.html actually names.

Outputs: a results JSON (path given by --out) and screenshots
under <out dir>/t404-remediation-screenshots/. The exit code is 0
whenever the audit itself ran; verdicts are data in the results.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "http://127.0.0.1:8417"
S4 = Path.home() / "glossa-work" / "spec095-s4"
INSTANCE = S4 / "audit-instance"
CI_PY = str(Path.home() / "glossa-work" / "venvs" / "glossa-ci" / "bin" / "python")
AXE = S4 / "axe.min.js"

STEPS: dict[str, dict] = {}
CANDIDATE_STATEMENT = (
    "T404 remediation candidate: sign M044 carries the value ku in syllabic slots."
)
CANDIDATE_FALSIFIER = (
    "A verified syllabic context in which M044 cannot read ku would falsify this candidate."
)
SETTLING_RUN = "settling-20261116T034814Z-3681c4"


def record(step: str, ok: bool, evidence: str):
    STEPS[step] = {"pass": bool(ok), "evidence": evidence}
    print(f"[{step}] {'PASS' if ok else 'FAIL'} — {evidence[:220]}", flush=True)


def req(method: str, path: str, timeout=30):
    r = urllib.request.Request(BASE + path, method=method)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}".encode()


def wait_health(proc, timeout=120) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if proc.poll() is not None:
            return False
        try:
            code, _ = req("GET", "/api/v1/health", timeout=5)
            if code == 200:
                return True
        except Exception:
            pass
        time.sleep(2)
    return False


def start_instance(log_path: Path) -> subprocess.Popen:
    subprocess.run(["pkill", "-f", "uvicorn.*8417"], capture_output=True)
    time.sleep(2)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(INSTANCE / "backend")
    env["PYTHONUNBUFFERED"] = "1"
    env["GLOSSA_API_AUTH"] = "off"
    log = open(log_path, "ab")
    proc = subprocess.Popen(
        [CI_PY, "-m", "uvicorn", "glossa_lab.main:create_app", "--factory",
         "--host", "127.0.0.1", "--port", "8417",
         "--app-dir", str(INSTANCE / "backend")],
        cwd=str(INSTANCE / "backend"), env=env,
        stdout=log, stderr=subprocess.STDOUT, start_new_session=True,
    )
    if not wait_health(proc):
        raise RuntimeError("audit instance did not become healthy")
    return proc


def section(page, name: str):
    page.get_by_test_id(f"section-{name}").click()
    page.get_by_test_id(f"dashboard-{name}").wait_for(state="visible", timeout=30000)


def wait_text(page, testid: str, needle: str, timeout: int = 30000) -> str:
    """Poll a surface's text until it contains needle (the surfaces
    load their records asynchronously; a single read races them)."""
    deadline = time.time() + timeout / 1000
    text = ""
    while time.time() < deadline:
        text = page.get_by_test_id(testid).inner_text()
        if needle in text:
            return text
        page.wait_for_timeout(500)
    return text


def f15_identity() -> dict:
    code, body = req("GET", "/")
    if code != 200:
        return {"pass": False, "evidence": f"GET / -> {code}"}
    m = re.search(rb"/assets/(index-[A-Za-z0-9_-]+\.js)", body)
    if not m:
        return {"pass": False, "evidence": "served index.html names no JS asset"}
    asset = m.group(1).decode()
    code2, served = req("GET", f"/assets/{asset}")
    dist_file = INSTANCE / "frontend" / "dist" / "assets" / asset
    if code2 != 200 or not dist_file.exists():
        return {"pass": False,
                "evidence": f"asset {asset}: served GET -> {code2}, dist file exists={dist_file.exists()}"}
    dist_bytes = dist_file.read_bytes()
    same = hashlib.sha256(served).hexdigest() == hashlib.sha256(dist_bytes).hexdigest()
    return {
        "pass": same,
        "evidence": (f"served asset {asset} ({len(served)} bytes) "
                     f"{'is byte-identical to' if same else 'DIFFERS FROM'} "
                     f"the instance dist asset ({len(dist_bytes)} bytes)"),
        "asset": asset,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    shots = args.out.parent / "t404-remediation-screenshots"
    shots.mkdir(parents=True, exist_ok=True)

    proc = start_instance(S4 / "remediation-driver-instance.log")
    print("instance healthy", flush=True)
    axe_results: dict[str, list] = {}
    keyboard: dict = {}
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.goto(BASE + "/#/researcher-dashboard", wait_until="networkidle")
            page.get_by_test_id("researcher-dashboard").wait_for(state="visible", timeout=30000)
            page.get_by_test_id("dashboard-home").wait_for(state="visible", timeout=30000)

            # ── P1 — home ────────────────────────────────────────────
            try:
                census = page.get_by_test_id("census-claims").inner_text().strip()
                body = page.get_by_test_id("dashboard-home").inner_text()
                ok = (census == "994"
                      and "What this program does not claim" in body
                      and "NOT IDENTIFIABLE" in body)
                record("P1", ok,
                       f"home census {census} claims; does-not-claim panel "
                       f"{'present' if 'What this program does not claim' in body else 'ABSENT'}; "
                       f"strongest readings carry NOT IDENTIFIABLE: {'NOT IDENTIFIABLE' in body}")
            except Exception as e:
                record("P1", False, f"{type(e).__name__}: {e}")
            page.screenshot(path=str(shots / "p1-home.png"))

            # ── P2 — program status ──────────────────────────────────
            try:
                section(page, "status")
                body = wait_text(page, "dashboard-status", "GR-088-01")
                ok = "Blocked items, with their blockers" in body and "GR-088-01" in body
                record("P2", ok,
                       "program status renders blocked items with blockers"
                       + ("; GR-088-01 named" if "GR-088-01" in body else "; GR-088-01 NOT named"))
            except Exception as e:
                record("P2", False, f"{type(e).__name__}: {e}")
            page.screenshot(path=str(shots / "p2-status.png"))

            # ── P3 — inscription explorer ────────────────────────────
            try:
                section(page, "inscriptions")
                page.get_by_text(re.compile(r"15,508 inscriptions")).wait_for(timeout=30000)
                # Filter by sign 145 through the (now labelled) sign input.
                page.get_by_test_id("filter-sign").fill("145")
                page.wait_for_timeout(2500)
                filtered = page.get_by_test_id("dashboard-inscriptions").inner_text()
                n_filtered = len(re.findall(r"GLI-IND-\d+", filtered))
                page.get_by_test_id("filter-sign").fill("")
                page.wait_for_timeout(2500)
                page.get_by_text("GLI-IND-0000206").first.click()
                page.get_by_text("Observation", exact=True).wait_for(state="visible", timeout=20000)
                layers = [w for w in ("Observation", "Transcription", "Hypothesis", "Claim")
                          if page.get_by_text(w, exact=True).count() > 0]
                page.get_by_test_id("sign-pos-1").click()
                page.get_by_text(re.compile(r"Position 2: sign 145")).wait_for(timeout=20000)
                ok = len(layers) == 4
                record("P3", ok,
                       f"explorer filters by sign 145 ({n_filtered} inscription ids in the filtered "
                       f"render); opened GLI-IND-0000206; labelled layers found: {layers}; "
                       f"sign position 1 selects its statements (Position 2: sign 145 shown)")
            except Exception as e:
                record("P3", False, f"{type(e).__name__}: {e}")
            page.screenshot(path=str(shots / "p3-inscriptions.png"))

            # ── P4 — hypothesis comparison ───────────────────────────
            try:
                section(page, "hypotheses")
                body = page.get_by_test_id("dashboard-hypotheses").inner_text()
                markers = body.count("NOT IDENTIFIABLE")
                ok = ("The program holds no translation of any inscription" in body
                      and "The nonlinguistic position" in body and markers > 0)
                record("P4", ok,
                       f"hypothesis comparison: no translation held stated; nonlinguistic "
                       f"position present; {markers} NOT IDENTIFIABLE markers on the surface")
            except Exception as e:
                record("P4", False, f"{type(e).__name__}: {e}")
            page.screenshot(path=str(shots / "p4-hypotheses.png"))

            # ── P5 — evidence inspection ─────────────────────────────
            opened = {"id": None, "statement": None}
            try:
                section(page, "evidence")
                page.get_by_test_id("claim-falsifier").select_option("absent")
                page.get_by_text("9 claims match").wait_for(state="visible", timeout=30000)
                first = page.locator("[data-testid=dashboard-evidence] button").filter(
                    has_text="no falsifier — the gap").first
                btn_text = first.inner_text()
                first.click()
                page.get_by_test_id("claim-detail").wait_for(state="visible", timeout=30000)
                detail = wait_text(page, "claim-detail", "Lineage")
                # inner_text wraps long lines at the layout width;
                # The claim id is the detail's first line, read from
                # the RAW text before any normalization.
                opened["id"] = detail.splitlines()[0].strip() if detail else None
                # The record of truth for the statement is the claim
                # record itself, read through the same API the
                # surface uses (screen text wraps; the record does not).
                if opened["id"]:
                    code_c, payload_c = req(
                        "GET", f"/api/v1/researcher-dashboard/claims/{opened['id']}")
                    if code_c == 200:
                        opened["statement"] = json.loads(payload_c).get("statement")
                # Collapse whitespace before substring checks (the
                # same normalization Playwright's text matching does).
                detail = re.sub(r"\s+", " ", detail)
                # The lineage block's title is uppercased by the
                # surface's own styling in rendered text.
                ok = ("lineage — claim, evidence, derivation, source" in detail.lower()
                      and "none recorded — this claim is in the falsifier-less class" in detail)
                record("P5", ok,
                       f"falsifier-absent class is exactly 9; opened claim {opened['id']} "
                       f"(row: {btn_text[:80]}…) with its detail and lineage")
            except Exception as e:
                record("P5", False, f"{type(e).__name__}: {e}")
            page.screenshot(path=str(shots / "p5-evidence.png"))

            # ── P8 — audit-trail export (from the P5 claim's detail) ─
            try:
                if not opened["id"]:
                    raise RuntimeError("no claim opened in P5")
                with page.expect_download(timeout=30000) as dl_info:
                    page.get_by_role("button", name="Export the audit trail").click()
                dl = dl_info.value
                target = shots / dl.suggested_filename
                dl.save_as(str(target))
                payload = json.loads(target.read_text(encoding="utf-8"))
                has_row = isinstance(payload.get("ledger_row"), dict)
                cid = payload.get("claim_id") or (payload.get("ledger_row") or {}).get("claim_id")
                stmt = payload.get("statement") or (payload.get("ledger_row") or {}).get("statement")
                ok = has_row and cid == opened["id"] and stmt == opened["statement"]
                record("P8", ok,
                       f"audit trail downloaded as {dl.suggested_filename} "
                       f"({target.stat().st_size} bytes); ledger_row present: {has_row}; "
                       f"claim id matches the opened claim: {cid == opened['id']}; "
                       f"statement matches the record: {stmt == opened['statement']}")
            except Exception as e:
                record("P8", False, f"{type(e).__name__}: {e}")

            # ── P6 — contribution (store-verified) ───────────────────
            try:
                section(page, "contribute")
                page.get_by_test_id("contrib-statement").fill(CANDIDATE_STATEMENT)
                page.get_by_test_id("contrib-falsifier").fill(CANDIDATE_FALSIFIER)
                page.get_by_test_id("contrib-refs").fill("M044")
                page.get_by_test_id("contrib-submitter").fill("T404 Remediation Audit")
                page.get_by_role("button", name="Submit to the staging queue").click()
                ok_el = page.get_by_test_id("contrib-ok")
                ok_el.wait_for(state="visible", timeout=30000)
                msg = ok_el.inner_text()
                m_id = re.search(r"RDC-\d+-\d+", msg)
                cand_id = m_id.group(0) if m_id else None
                staging = (INSTANCE / "outputs" / "anchor_staging.json").read_text(encoding="utf-8")
                n_stmt = staging.count(CANDIDATE_STATEMENT)
                n_id = staging.count(cand_id) if cand_id else 0
                entries = json.loads(staging)
                pool = entries if isinstance(entries, list) else entries.get("candidates", [])
                mine = [e for e in pool if isinstance(e, dict)
                        and (e.get("statement") == CANDIDATE_STATEMENT
                             or e.get("text") == CANDIDATE_STATEMENT)]
                stage = mine[0].get("stage") if mine else None
                # The corrections' standard: the candidate id and the
                # exact candidate text present in the store, exactly
                # once. The parsed-entry match corroborates when the
                # store's shape exposes it.
                ok = cand_id is not None and n_stmt == 1 and n_id >= 1 and len(mine) <= 1
                record("P6", ok,
                       f"submission accepted ({msg.strip()[:120]}); store check on "
                       f"outputs/anchor_staging.json: statement occurs {n_stmt} time(s), "
                       f"candidate id occurs {n_id} time(s), matching entries {len(mine)}, "
                       f"stage {stage!r}")
            except Exception as e:
                record("P6", False, f"{type(e).__name__}: {e}")
            page.screenshot(path=str(shots / "p6-contribute.png"))

            # ── P7 capability — the submitted candidate is followable ──
            # The legacy protocol's P7 follows the candidate it
            # submitted in P6 to its adjudication surface. The filed
            # legacy driver's P6 cannot land (its fill never satisfies
            # the form's named-submitter and evidence-reference
            # requirements), so the capability is verified here on the
            # candidate this leg submitted: it must be visible on the
            # claims register with its stage named.
            try:
                page.goto(BASE + "/#/claims", wait_until="networkidle")
                page.get_by_text("Candidates in the staging queue").wait_for(
                    state="visible", timeout=30000)
                claims_text = page.locator("body").inner_text()
                idx = claims_text.find("T404 remediation candidate")
                visible = idx >= 0
                ctx = claims_text[max(0, idx - 40):idx + 260] if visible else ""
                ok = visible and "staged" in ctx
                STEPS["P7-capability"] = {
                    "pass": ok,
                    "evidence": (f"candidate visible on the claims register with its "
                                 f"stage: {ok}; context: {ctx[:240]!r}"),
                }
                print(f"[P7-capability] {'PASS' if ok else 'FAIL'} — {STEPS['P7-capability']['evidence'][:220]}", flush=True)
            except Exception as e:
                STEPS["P7-capability"] = {"pass": False, "evidence": f"{type(e).__name__}: {e}"}
                print(f"[P7-capability] FAIL — {e}", flush=True)
            page.screenshot(path=str(shots / "p7-capability-claims.png"))

            # ── P7 — experiment reproduction ─────────────────────────
            try:
                # The capability leg detoured to the claims route;
                # return to the dashboard before its section tabs exist.
                page.goto(BASE + "/#/researcher-dashboard", wait_until="networkidle")
                page.get_by_test_id("researcher-dashboard").wait_for(state="visible", timeout=30000)
                section(page, "reproduction")
                page.get_by_text("not reproducible").first.wait_for(state="visible", timeout=30000)
                body = page.get_by_test_id("dashboard-reproduction").inner_text()
                legacy_named = "missing:" in body
                clicked = page.evaluate(
                    """(runId) => {
                      const btns = [...document.querySelectorAll('button')];
                      const b = btns.find(x => x.textContent.includes('Re-run (scratch only)')
                        && x.parentElement && x.parentElement.textContent.includes(runId));
                      if (b) { b.click(); return true; }
                      return false;
                    }""", SETTLING_RUN)
                if not clicked:
                    raise RuntimeError(f"no Re-run button found on the {SETTLING_RUN} row")
                result = page.get_by_test_id("rerun-result")
                result.wait_for(state="visible", timeout=240000)
                rtext = result.inner_text()
                m_ac = re.search(r"assigned_count\s+recorded:\s*(\S+)\s+re-run:\s*(\S+)", rtext)
                m_as = re.search(r"assigned_share\s+recorded:\s*(\S+)\s+re-run:\s*(\S+)", rtext)
                ac_ok = bool(m_ac) and m_ac.group(1) == m_ac.group(2)
                as_ok = bool(m_as) and m_as.group(1) == m_as.group(2)
                corpus_ok = "corpus identity: verified" in rtext
                ok = legacy_named and ac_ok and as_ok and corpus_ok
                record("P7", ok,
                       f"legacy runs marked not reproducible with missing pieces named: "
                       f"{legacy_named}; re-run of {SETTLING_RUN}: corpus identity verified: "
                       f"{corpus_ok}; assigned_count recorded {m_ac.group(1) if m_ac else '?'} "
                       f"vs re-run {m_ac.group(2) if m_ac else '?'}; assigned_share identical: {as_ok}")
            except Exception as e:
                record("P7", False, f"{type(e).__name__}: {e}")
            page.screenshot(path=str(shots / "p7-reproduction.png"))

            # ── Axe over the seven dashboard surfaces (light theme) ──
            # The dashboard restores its last section on re-entry, so
            # wait for the shell, not for the home section.
            page.goto(BASE + "/#/researcher-dashboard", wait_until="networkidle")
            page.get_by_test_id("researcher-dashboard").wait_for(state="visible", timeout=30000)
            axe_src = AXE.read_text(encoding="utf-8")
            surfaces = ["home", "status", "inscriptions", "hypotheses",
                        "evidence", "contribute", "reproduction"]
            for name in surfaces:
                try:
                    section(page, name)
                    page.wait_for_timeout(1200)
                    page.evaluate(axe_src)
                    res = page.evaluate(
                        "async () => { const r = await axe.run(); "
                        "return r.violations.map(v => ({id: v.id, impact: v.impact, "
                        "nodes: v.nodes.length})); }")
                    axe_results[name] = res
                except Exception as e:
                    axe_results[name] = [{"id": f"driver-error: {type(e).__name__}: {e}",
                                          "impact": "unknown", "nodes": 0}]
                print(f"[axe] {name}: {axe_results[name]}", flush=True)

            # ── Keyboard: the section navigation traverses in order ──
            try:
                section(page, "home")
                page.get_by_test_id("section-home").focus()
                stops = []
                for _ in range(6):
                    page.keyboard.press("Tab")
                    stops.append(page.evaluate(
                        "() => { const el = document.activeElement; "
                        "return el ? (el.getAttribute('data-testid') || el.textContent || el.tagName) : ''; }"))
                expected = [f"section-{s}" for s in
                            ["status", "inscriptions", "hypotheses",
                             "evidence", "reproduction", "contribute"]]
                tabs_first = stops[:6] == expected
                keyboard = {"stops_after_section_home": stops,
                            "section_tabs_traverse_in_order": tabs_first}
            except Exception as e:
                keyboard = {"error": f"{type(e).__name__}: {e}",
                            "section_tabs_traverse_in_order": False}
            print(f"[keyboard] {keyboard}", flush=True)

            browser.close()
    finally:
        try:
            proc.terminate()
        except Exception:
            pass

    f15 = f15_identity()
    print(f"[F15] {f15}", flush=True)

    passed = sum(1 for k, s in STEPS.items()
                 if re.fullmatch(r"P[1-8]", k) and s["pass"])
    crit, serious = [], []
    for surface, res in axe_results.items():
        for v in res:
            if v.get("impact") == "critical":
                crit.append(f"{surface}: {v['id']} ({v['nodes']} nodes)")
            elif v.get("impact") == "serious":
                serious.append(f"{surface}: {v['id']} ({v['nodes']} nodes)")
    scores = {
        "protocol_steps_passed": passed,
        "P1_protocol_ge_6_of_8": passed >= 6,
        "A1_zero_critical": len(crit) == 0,
        "A2_serious_le_3_and_keyboard": len(serious) <= 3 and bool(keyboard.get("section_tabs_traverse_in_order")),
        "axe_critical": crit,
        "axe_serious": serious,
    }
    def _step_key(s: str):
        m = re.match(r"P(\d+)", s)
        return (int(m.group(1)) if m else 99, s)

    ordered_steps = {k: STEPS[k] for k in sorted(STEPS, key=_step_key)}
    out = {"steps": ordered_steps, "axe": axe_results, "keyboard": keyboard,
           "f15_identity": f15, "scores": scores}
    args.out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(scores, indent=2), flush=True)
    print(f"DASHBOARD LEG: P1 {'MET' if scores['P1_protocol_ge_6_of_8'] else 'NOT MET'}, "
          f"A1 {'MET' if scores['A1_zero_critical'] else 'NOT MET'}, "
          f"A2 {'MET' if scores['A2_serious_le_3_and_keyboard'] else 'NOT MET'}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
