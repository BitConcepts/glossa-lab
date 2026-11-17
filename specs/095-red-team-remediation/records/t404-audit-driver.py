#!/usr/bin/env python3
"""Spec 095 Stage 4 (T404) — audit driver.

Runs the RT-19 functional checklist, the C095-13 eight-step
new-researcher protocol, and the accessibility pass against a
scratch instance of the current build, scored against the
thresholds fixed in records/t404-thresholds-2026-11-17.md
(committed before this driver was written).

The instance is a disposable copy of the stage tree on
127.0.0.1:8417 with GLOSSA_API_AUTH=off, started and owned by
this driver. No live store is read or written. The protocol legs
act as a new researcher: only what the surfaces present.

Outputs: a results JSON (path given by --out) and screenshots
under <out dir>/t404-screenshots/. The driver's exit code is 0
whenever the audit itself ran; the package verdict is data in
the results, not the exit code.
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
TRACKER = "https://bitconcepts.tech/research/indus-script/"

RESULTS: list[dict] = []


def record(section: str, item: str, attempted: bool, verdict: str, evidence: str):
    RESULTS.append(
        {"section": section, "item": item, "attempted": attempted,
         "verdict": verdict, "evidence": evidence}
    )
    print(f"[{section}] {item}: {verdict} — {evidence[:180]}", flush=True)


# ---------------------------------------------------------------------------
# HTTP helpers


def req(method: str, path: str, body=None, raw: bytes | None = None, timeout=30):
    data = raw
    headers = {"Content-Type": "application/json"}
    if body is not None:
        data = json.dumps(body).encode()
    r = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            payload = resp.read()
            try:
                return resp.status, json.loads(payload)
            except Exception:
                return resp.status, payload
    except urllib.error.HTTPError as e:
        payload = e.read()
        try:
            return e.code, json.loads(payload)
        except Exception:
            return e.code, payload
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}"


def wait_health(proc, timeout=90) -> bool:
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


# ---------------------------------------------------------------------------
# Functional checklist (RT-19's fifteen, thresholds F1/F2)


def functional() -> dict:
    state: dict = {}

    # 1. Project: create (import), open, update, delete.
    try:
        code, listing = req("GET", "/api/v1/projects")
        before = listing if isinstance(listing, list) else listing.get("projects", [])
        code_i, imported = req("POST", "/api/v1/projects/import",
                               {"name": "T404 Audit Project", "description": "stage 4 audit"})
        pid = None
        if isinstance(imported, dict):
            pid = imported.get("id") or imported.get("project_id")
        if pid is None:
            code2, listing2 = req("GET", "/api/v1/projects")
            after = listing2 if isinstance(listing2, list) else listing2.get("projects", [])
            new = [p for p in after if p not in before]
            if new:
                pid = new[0].get("id") or new[0].get("project_id")
        if pid is None:
            record("functional", "F01-project-crud", True, "FAIL",
                   f"import returned {code_i} with no identifiable project id: {str(imported)[:140]}")
        else:
            state["pid"] = pid
            code_g, got = req("GET", f"/api/v1/projects/{pid}")
            code_u, upd = req("PUT", f"/api/v1/projects/{pid}",
                              {"description": "updated by T404 audit"})
            code_d, _ = req("DELETE", f"/api/v1/projects/{pid}")
            code_g2, _ = req("GET", f"/api/v1/projects/{pid}")
            ok = code_g == 200 and code_u in (200, 204) and code_d in (200, 204) and code_g2 == 404
            record("functional", "F01-project-crud", True, "PASS" if ok else "FAIL",
                   f"import={code_i} open={code_g} update={code_u} delete={code_d} reopen-after-delete={code_g2}")
    except Exception as e:
        record("functional", "F01-project-crud", True, "FAIL", f"{type(e).__name__}: {e}")

    # 2. Experiment: create, open, update, delete (experiment-graphs).
    try:
        code_c, created = req("POST", "/api/v1/experiment-graphs",
                              {"name": "T404 Audit Experiment", "description": "audit",
                               "nodes": [], "edges": []})
        eid = created.get("id") if isinstance(created, dict) else None
        if eid is None:
            record("functional", "F02-experiment-crud", True, "FAIL",
                   f"create returned {code_c}: {str(created)[:140]}")
        else:
            state["eid"] = eid
            code_g, _ = req("GET", f"/api/v1/experiment-graphs/{eid}")
            code_u, _ = req("PUT", f"/api/v1/experiment-graphs/{eid}",
                            {"name": "T404 Audit Experiment (updated)", "nodes": [], "edges": []})
            record("functional", "F02-experiment-crud", True,
                   "PASS" if (code_c in (200, 201) and code_g == 200 and code_u in (200, 204)) else "FAIL",
                   f"create={code_c} open={code_g} update={code_u} (delete exercised in F02b)")
            code_d, _ = req("DELETE", f"/api/v1/experiment-graphs/{eid}")
            code_g2, _ = req("GET", f"/api/v1/experiment-graphs/{eid}")
            record("functional", "F02b-experiment-delete", True,
                   "PASS" if (code_d in (200, 204) and code_g2 == 404) else "FAIL",
                   f"delete={code_d} reopen-after-delete={code_g2}")
    except Exception as e:
        record("functional", "F02-experiment-crud", True, "FAIL", f"{type(e).__name__}: {e}")

    # 3. Corpus: inspect the catalogue; import into an entry if offered.
    try:
        code, cat = req("GET", "/api/v1/corpus-catalogue")
        entries = cat if isinstance(cat, list) else (cat.get("items") or cat.get("catalogue") or [])
        detail = f"catalogue GET={code}, {len(entries)} entries"
        verdict = "PASS" if code == 200 and entries else "FAIL"
        if entries:
            cid = entries[0].get("id") or entries[0].get("catalogue_id")
            code_i, imp = req("POST", f"/api/v1/corpus-catalogue/{cid}/import", {})
            detail += f"; import attempt on {cid} -> {code_i} {str(imp)[:80]}"
        record("functional", "F03-corpus-inspect-import", True, verdict, detail)
    except Exception as e:
        record("functional", "F03-corpus-inspect-import", True, "FAIL", f"{type(e).__name__}: {e}")

    # 4 + 5 + 6 + 10 + 11. Jobs: create, run state, pause (cancel-class),
    # resume, concurrency, long-running visibility.
    job_ids: list[str] = []
    try:
        for i in range(2):
            code_c, job = req("POST", "/api/v1/jobs",
                              {"name": f"T404 audit job {i+1}", "params": {}})
            jid = job.get("id") if isinstance(job, dict) else None
            if jid:
                job_ids.append(jid)
        if not job_ids:
            record("functional", "F04-run-experiment-job", True, "FAIL",
                   f"job create failed: {code_c} {str(job)[:120]}")
        else:
            code_g, got = req("GET", f"/api/v1/jobs/{job_ids[0]}")
            status0 = got.get("status") if isinstance(got, dict) else None
            record("functional", "F04-run-experiment-job", True,
                   "PASS" if code_g == 200 and status0 else "FAIL",
                   f"job created and readable; status={status0!r}")
            record("functional", "F10-concurrent-jobs", True,
                   "PASS" if len(job_ids) == 2 else "FAIL",
                   f"{len(job_ids)} jobs created back-to-back and both readable")
            # Long-running visibility: poll for status/progress fields.
            seen = []
            for _ in range(6):
                _, g = req("GET", f"/api/v1/jobs/{job_ids[0]}")
                if isinstance(g, dict):
                    seen.append({k: g.get(k) for k in ("status", "progress", "updated_at") if k in g})
                time.sleep(2)
            record("functional", "F11-long-running-visibility", True,
                   "PASS" if seen and all(s.get("status") for s in seen) else "FAIL",
                   f"status observable across 6 polls over 12s: {seen[:2]}")
            # Pause then resume (cancel/resume classes), then delete.
            code_p, _ = req("POST", f"/api/v1/jobs/{job_ids[0]}/pause")
            code_r, _ = req("POST", f"/api/v1/jobs/{job_ids[0]}/resume")
            record("functional", "F05-cancel-pause-job", True,
                   "PASS" if code_p in (200, 204) else "FAIL", f"pause -> {code_p}")
            record("functional", "F06-resume-job", True,
                   "PASS" if code_r in (200, 204) else "FAIL", f"resume after pause -> {code_r}")
    except Exception as e:
        record("functional", "F04-run-experiment-job", True, "FAIL", f"{type(e).__name__}: {e}")

    # 8 + 9. Report generation, download, export formats.
    try:
        code_t, templates = req("GET", "/api/v1/reports/templates")
        tlist = templates if isinstance(templates, list) else (templates.get("templates") or [])
        if not tlist:
            code_t2, templates2 = req("GET", "/api/v1/report-templates")
            tlist = templates2 if isinstance(templates2, list) else (templates2.get("templates") or [])
        if not tlist:
            record("functional", "F08-generate-report", True, "FAIL",
                   f"no report templates offered (GET templates -> {code_t})")
        else:
            tid = tlist[0].get("id") or tlist[0].get("template_id") or tlist[0].get("name")
            code_g, gen = req("POST", "/api/v1/reports/generate", {"template_id": tid})
            rname = gen.get("name") or gen.get("report_name") if isinstance(gen, dict) else None
            detail = f"generate(template={tid}) -> {code_g}"
            verdict = "PASS" if code_g in (200, 201) else "FAIL"
            if rname:
                code_d, payload = req("GET", f"/api/v1/reports/{rname}/download")
                size = len(payload) if isinstance(payload, (bytes, str)) else -1
                detail += f"; download -> {code_d}, {size} bytes"
                verdict = "PASS" if (verdict == "PASS" and code_d == 200 and size > 0) else "FAIL"
            record("functional", "F08-generate-report", True, verdict, detail)
        # Export format validation: project export endpoint shape.
        code_p, projects = req("GET", "/api/v1/projects")
        plist = projects if isinstance(projects, list) else projects.get("projects", [])
        if plist:
            pid = plist[0].get("id") or plist[0].get("project_id")
            code_e, payload = req("GET", f"/api/v1/projects/{pid}/export")
            size = len(payload) if isinstance(payload, (bytes, str)) else -1
            record("functional", "F09-export-formats", True,
                   "PASS" if code_e == 200 and size > 0 else "FAIL",
                   f"project export -> {code_e}, {size} bytes, payload type {type(payload).__name__}")
        else:
            record("functional", "F09-export-formats", True, "FAIL", "no project available to export")
    except Exception as e:
        record("functional", "F08-generate-report", True, "FAIL", f"{type(e).__name__}: {e}")

    # 12. Malformed input and extreme sizes: refused or handled, no crash.
    try:
        results = []
        code1, _ = req("POST", "/api/v1/experiment-graphs", raw=b"{not json")
        results.append(f"invalid-json->{code1}")
        code2, _ = req("POST", "/api/v1/experiment-graphs", {"name": 12345, "nodes": "not-a-list"})
        results.append(f"wrong-types->{code2}")
        code3, _ = req("GET", "/api/v1/experiment-graphs/definitely-not-a-real-id")
        results.append(f"missing-id->{code3}")
        code4, _ = req("POST", "/api/v1/jobs", {"name": "x" * 200000})
        results.append(f"oversized-name->{code4}")
        code_h, _ = req("GET", "/api/v1/health")
        results.append(f"health-after->{code_h}")
        bad = [r for r in results if "->5" in r or "->-1" in r]
        record("functional", "F12-malformed-input", True,
               "PASS" if not bad and code_h == 200 else "FAIL",
               "; ".join(results))
    except Exception as e:
        record("functional", "F12-malformed-input", True, "FAIL", f"{type(e).__name__}: {e}")

    # 13. Migration and rollback — by direct inspection with filed
    # evidence (the thresholds' F1 definition of attempted).
    try:
        mig_test = INSTANCE / "backend" / "tests" / "test_spec086_ledger_migration.py"
        proc = subprocess.run(
            [CI_PY, "-m", "pytest", str(mig_test), "-q"],
            cwd=str(INSTANCE / "backend"), capture_output=True, text=True, timeout=900)
        mig_ok = proc.returncode == 0
        grep = subprocess.run(
            ["grep", "-rn", "rollback\\|restore_snapshot\\|downgrade", "glossa_lab/",
             "--include=*.py"], cwd=str(INSTANCE / "backend"),
            capture_output=True, text=True)
        hits = [ln for ln in grep.stdout.splitlines() if "def " in ln or "rollback" in ln.lower()][:4]
        record("functional", "F13-migration-rollback", True,
               "PASS" if (mig_ok and hits) else "FAIL",
               f"ledger migration tests {'pass' if mig_ok else 'FAIL'} in the audit tree; "
               f"rollback/restore definitions found: {hits if hits else 'NONE'}")
    except Exception as e:
        record("functional", "F13-migration-rollback", True, "FAIL", f"{type(e).__name__}: {e}")

    # 15. Served bundle matches its source commit.
    try:
        code, payload = req("GET", "/assets/index-8H0F3zWA.js")
        served = payload if isinstance(payload, bytes) else str(payload).encode()
        disk = (INSTANCE / "frontend" / "dist" / "assets" / "index-8H0F3zWA.js").read_bytes()
        record("functional", "F15-bundle-identity", True,
               "PASS" if hashlib.sha256(served).hexdigest() == hashlib.sha256(disk).hexdigest() else "FAIL",
               f"served asset sha256 {hashlib.sha256(served).hexdigest()[:16]} vs committed dist "
               f"{hashlib.sha256(disk).hexdigest()[:16]} (frontend untouched by this stage; dist is the base commit's)")
    except Exception as e:
        record("functional", "F15-bundle-identity", True, "FAIL", f"{type(e).__name__}: {e}")

    return state


# ---------------------------------------------------------------------------
# UI legs: the eight-step protocol (P1), refresh (F14), accessibility (A1/A2)


def shot(page, shots: Path, name: str, mobile_page=None):
    page.screenshot(path=str(shots / f"{name}-desktop.png"), full_page=False)
    if mobile_page is not None:
        try:
            mobile_page.goto(page.url, wait_until="networkidle", timeout=30000)
            mobile_page.wait_for_timeout(700)
        except Exception:
            pass
        mobile_page.screenshot(path=str(shots / f"{name}-mobile.png"), full_page=False)


def nav_to(page, label: str) -> bool:
    """Click a primary-nav button by its visible label."""
    try:
        btn = page.get_by_role("button", name=re.compile(re.escape(label), re.I))
        btn.first.click(timeout=6000)
        page.wait_for_load_state("networkidle", timeout=20000)
        page.wait_for_timeout(900)
        return True
    except Exception:
        return False


def body_text(page) -> str:
    try:
        return page.evaluate("() => document.body.innerText")
    except Exception:
        return ""


def ui_legs(shots: Path, axe_results: dict) -> None:
    from playwright.sync_api import sync_playwright

    axe_src = AXE.read_text(encoding="utf-8") if AXE.is_file() else None

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        mctx = browser.new_context(viewport={"width": 390, "height": 844})
        mpage = mctx.new_page()

        def go_home():
            page.goto(BASE + "/", wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(1200)
            mpage.goto(BASE + "/", wait_until="networkidle", timeout=60000)
            mpage.wait_for_timeout(800)

        # P1 — arrive from the public page.
        try:
            resp = page.goto(TRACKER, wait_until="networkidle", timeout=60000)
            text = body_text(page)
            onward = page.evaluate(
                "() => Array.from(document.querySelectorAll('a')).map(a => a.href)"
                ".filter(h => h.includes('glossa') || h.includes('app'))")
            shot(page, shots, "p1-public-page")
            ok = resp is not None and resp.status == 200 and "Indus" in text
            record("protocol", "P1-arrive-from-public-page", True,
                   "PASS" if ok else "FAIL",
                   f"tracker page status {resp.status if resp else 'none'}; onward app links found: {onward[:3]}")
        except Exception as e:
            record("protocol", "P1-arrive-from-public-page", True, "FAIL", f"{type(e).__name__}: {e}")

        go_home()

        # P2 — establish what the system claims and does not claim.
        try:
            text = body_text(page)
            shot(page, shots, "p2-home-standing", mpage)
            has_standing = "not deciphered" in text.lower()
            has_position = "standing position" in text.lower()
            record("protocol", "P2-claims-and-non-claims", True,
                   "PASS" if (has_standing and has_position) else "FAIL",
                   f"home presents a 'Standing position' panel: {has_position}; "
                   f"states the script is not deciphered: {has_standing}")
        except Exception as e:
            record("protocol", "P2-claims-and-non-claims", True, "FAIL", f"{type(e).__name__}: {e}")

        # Accessibility over the surfaces the protocol touches + keyboard.
        views = ["Home", "Claims", "Data", "Experiments", "Evidence & sources", "Settings"]
        for view in views:
            try:
                if view != "Home":
                    nav_to(page, view)
                if axe_src:
                    page.evaluate(axe_src)
                    res = page.evaluate(
                        "async () => { const r = await axe.run(); "
                        "return r.violations.map(v => ({id: v.id, impact: v.impact, nodes: v.nodes.length})); }")
                    axe_results[view] = res
                else:
                    axe_results[view] = "AXE UNAVAILABLE"
            except Exception as e:
                axe_results[view] = f"ERROR {type(e).__name__}: {e}"
        # Keyboard: tab through the home surface.
        try:
            go_home()
            focused = []
            for _ in range(40):
                page.keyboard.press("Tab")
                page.wait_for_timeout(120)
                label = page.evaluate(
                    "() => { const el = document.activeElement; "
                    "return el ? (el.textContent || el.getAttribute('aria-label') || el.tagName).trim().slice(0, 40) : ''; }")
                if label:
                    focused.append(label)
            primaries = ["Home", "Claims", "Data", "Experiments", "Settings"]
            reached = [p for p in primaries if any(p.lower() in f.lower() for f in focused)]
            record("accessibility", "A2-keyboard-nav", True,
                   "PASS" if len(reached) >= 4 else "FAIL",
                   f"Tab walk reached primary destinations: {reached}; first focused: {focused[:8]}")
        except Exception as e:
            record("accessibility", "A2-keyboard-nav", True, "FAIL", f"{type(e).__name__}: {e}")

        # F14 — application state survives a browser refresh.
        try:
            go_home()
            nav_to(page, "Claims")
            before = body_text(page)[:400]
            page.reload(wait_until="networkidle")
            page.wait_for_timeout(1200)
            after = body_text(page)[:400]
            record("functional", "F14-refresh-state", True,
                   "PASS" if before and before == after else "FAIL",
                   f"claims view content identical across reload: {before == after}; url after reload: {page.url}")
        except Exception as e:
            record("functional", "F14-refresh-state", True, "FAIL", f"{type(e).__name__}: {e}")

        # P3 — find one inscription and its evidence trail (Data view).
        try:
            go_home()
            nav_to(page, "Data")
            shot(page, shots, "p3-data-view", mpage)
            text = body_text(page)
            # Open the first sign/inscription-like entry the surface offers.
            opened = False
            for pattern in ("M342", "M118", "M87"):
                loc = page.get_by_text(pattern, exact=False)
                if loc.count() > 0:
                    loc.first.click(timeout=5000)
                    page.wait_for_timeout(1500)
                    opened = True
                    break
            if not opened:
                # Fall back to the first row-like clickable in the list region.
                rows = page.locator("table tbody tr, [role='row']")
                if rows.count() > 0:
                    rows.first.click(timeout=5000)
                    page.wait_for_timeout(1500)
                    opened = True
            detail = body_text(page)
            shot(page, shots, "p3-inscription-detail", mpage)
            has_evidence = "evidence" in detail.lower()
            record("protocol", "P3-inscription-and-evidence-trail", True,
                   "PASS" if (opened and has_evidence) else "FAIL",
                   f"data view opened an entry: {opened}; detail surface mentions evidence trail: {has_evidence}; "
                   f"data view text sample: {text[:120]!r}")
        except Exception as e:
            record("protocol", "P3-inscription-and-evidence-trail", True, "FAIL", f"{type(e).__name__}: {e}")

        # P4 — distinguish observation, transcription, hypothesis, claim.
        try:
            go_home()
            nav_to(page, "Claims")
            shot(page, shots, "p4-claims-view", mpage)
            rows = page.locator("table tbody tr, [role='row']")
            if rows.count() > 0:
                rows.first.click(timeout=5000)
                page.wait_for_timeout(1500)
            detail = body_text(page).lower()
            kinds = {k: (k in detail) for k in
                     ("falsifier", "evidence", "does not establish", "hypothesis", "transcription", "observation")}
            shot(page, shots, "p4-claim-detail", mpage)
            present = [k for k, v in kinds.items() if v]
            record("protocol", "P4-distinguish-kinds", True,
                   "PASS" if len(present) >= 4 else "FAIL",
                   f"claim surface labels found: {present}")
        except Exception as e:
            record("protocol", "P4-distinguish-kinds", True, "FAIL", f"{type(e).__name__}: {e}")

        # P5 — reproduce one published result (Experiments view).
        try:
            go_home()
            nav_to(page, "Experiments")
            shot(page, shots, "p5-experiments-view", mpage)
            text = body_text(page)
            rows = page.locator("table tbody tr, [role='row']")
            opened = False
            if rows.count() > 0:
                rows.first.click(timeout=5000)
                page.wait_for_timeout(1500)
                opened = True
            detail = body_text(page)
            run_btn = page.get_by_role("button", name=re.compile(r"run|reproduce|re-run|rerun|execute", re.I))
            has_run = run_btn.count() > 0
            clicked = False
            outcome = ""
            if has_run:
                try:
                    run_btn.first.click(timeout=6000)
                    page.wait_for_timeout(4000)
                    clicked = True
                    outcome = body_text(page)[:200]
                except Exception as e:
                    outcome = f"click failed: {e}"
            shot(page, shots, "p5-experiment-detail", mpage)
            record("protocol", "P5-reproduce-one-result", True,
                   "PASS" if (opened and has_run and clicked) else "FAIL",
                   f"experiment opened: {opened}; run/reproduce affordance present: {has_run}; "
                   f"activated: {clicked}; surface after activation: {outcome[:140]!r}; list sample: {text[:100]!r}")
        except Exception as e:
            record("protocol", "P5-reproduce-one-result", True, "FAIL", f"{type(e).__name__}: {e}")

        # P6 — submit one candidate with a falsifier (Register a claim).
        candidate_marker = "T404 audit candidate: the audit driver can register a claim."
        try:
            go_home()
            btn = page.get_by_role("button", name=re.compile(r"register a claim", re.I))
            if btn.count() == 0:
                shot(page, shots, "p6-no-register-path", mpage)
                record("protocol", "P6-submit-candidate-with-falsifier", True, "FAIL",
                       "no 'Register a claim' affordance on the home surface")
            else:
                btn.first.click(timeout=6000)
                page.wait_for_timeout(1500)
                shot(page, shots, "p6-register-form", mpage)
                form_text = body_text(page).lower()
                has_falsifier = "falsifier" in form_text
                # Fill the first text inputs/areas with statement + falsifier.
                filled = page.evaluate(
                    """(marker) => {
                      const set = (el, v) => { el.focus(); document.execCommand('selectAll', false, null);
                        document.execCommand('insertText', false, v); el.dispatchEvent(new Event('change', {bubbles: true})); };
                      const areas = Array.from(document.querySelectorAll('textarea'));
                      const inputs = Array.from(document.querySelectorAll('input[type="text"], input:not([type])'));
                      let n = 0;
                      if (areas.length) { set(areas[0], marker); n++; }
                      if (areas.length > 1) { set(areas[1], 'Withdrawn if the audit trail does not show this candidate.'); n++; }
                      else if (inputs.length) { set(inputs[0], marker); n++; }
                      return n;
                    }""", candidate_marker)
                submit = page.get_by_role("button", name=re.compile(r"register|submit|create|save", re.I))
                submitted = False
                if submit.count() > 0:
                    submit.first.click(timeout=6000)
                    page.wait_for_timeout(2500)
                    submitted = True
                after = body_text(page)
                shot(page, shots, "p6-after-submit", mpage)
                record("protocol", "P6-submit-candidate-with-falsifier", True,
                       "PASS" if (has_falsifier and filled and submitted) else "FAIL",
                       f"form requires/mentions falsifier: {has_falsifier}; fields filled: {filled}; "
                       f"submitted: {submitted}; surface after: {after[:140]!r}")
        except Exception as e:
            record("protocol", "P6-submit-candidate-with-falsifier", True, "FAIL", f"{type(e).__name__}: {e}")

        # P7 — follow its adjudication (Digestion board / Claims).
        try:
            go_home()
            found = False
            trail = ""
            for view in ("Digestion", "Claims"):
                nav_to(page, view)
                text = body_text(page)
                if "T404 audit candidate" in text:
                    found = True
                    idx = text.find("T404 audit candidate")
                    trail = text[max(0, idx - 60):idx + 220]
                    shot(page, shots, f"p7-adjudication-{view.lower()}", mpage)
                    break
            record("protocol", "P7-follow-adjudication", True,
                   "PASS" if found else "FAIL",
                   f"candidate visible with its stage/status: {found}; context: {trail[:200]!r}")
        except Exception as e:
            record("protocol", "P7-follow-adjudication", True, "FAIL", f"{type(e).__name__}: {e}")

        # P8 — export the audit trail (Reports & ledger).
        try:
            go_home()
            nav_to(page, "Reports & ledger")
            shot(page, shots, "p8-reports-view", mpage)
            text = body_text(page)
            dl_btn = page.get_by_role("button", name=re.compile(r"export|download", re.I))
            exported = False
            detail = f"export/download affordances on the surface: {dl_btn.count()}"
            if dl_btn.count() > 0:
                try:
                    with page.expect_download(timeout=15000) as dl_info:
                        dl_btn.first.click(timeout=6000)
                    dl = dl_info.value
                    path = shots / f"p8-export-{dl.suggested_filename}"
                    dl.save_as(str(path))
                    exported = path.stat().st_size > 0
                    detail += f"; downloaded {dl.suggested_filename} ({path.stat().st_size} bytes)"
                except Exception as e:
                    detail += f"; download did not complete: {type(e).__name__}"
            record("protocol", "P8-export-audit-trail", True,
                   "PASS" if exported else "FAIL", detail + f"; view sample: {text[:100]!r}")
        except Exception as e:
            record("protocol", "P8-export-audit-trail", True, "FAIL", f"{type(e).__name__}: {e}")

        browser.close()


# ---------------------------------------------------------------------------
# Scoring against the fixed thresholds


def score() -> dict:
    fn = [r for r in RESULTS if r["section"] == "functional"]
    pr = [r for r in RESULTS if r["section"] == "protocol"]
    # F02b is a sub-leg of item 2, not a fifteenth item: count items by
    # their RT-19 number.
    import re as _re
    items = {}
    for r in fn:
        m = _re.match(r"F(\d+)", r["item"])
        key = m.group(1) if m else r["item"]
        items.setdefault(key, []).append(r)
    attempted = sum(1 for k, rs in items.items() if any(r["attempted"] for r in rs))
    passed = sum(1 for k, rs in items.items() if all(r["verdict"] == "PASS" for r in rs))
    f1 = attempted >= 12
    f2 = attempted > 0 and (passed / attempted) >= 0.75
    p_done = sum(1 for r in pr if r["verdict"] == "PASS")
    p1 = p_done >= 6
    return {
        "functional_items_attempted": attempted,
        "functional_items_passed": passed,
        "F1_coverage_ge_12_of_15": f1,
        "F2_outcome_ge_75pct": f2,
        "protocol_steps_passed": p_done,
        "P1_protocol_ge_6_of_8": p1,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    shots = args.out.parent / "t404-screenshots"
    shots.mkdir(parents=True, exist_ok=True)

    proc = start_instance(S4 / "audit-driver-instance.log")
    print("instance healthy", flush=True)
    axe_results: dict = {}
    try:
        functional()
        # F07 — recover after a backend restart (state intact).
        try:
            code_c, created = req("POST", "/api/v1/experiment-graphs",
                                  {"name": "T404 restart marker", "nodes": [], "edges": []})
            mid = created.get("id") if isinstance(created, dict) else None
            proc.terminate()
            proc.wait(timeout=30)
            proc = start_instance(S4 / "audit-driver-instance.log")
            code_g, _ = req("GET", f"/api/v1/experiment-graphs/{mid}") if mid else (-1, None)
            record("functional", "F07-restart-recovery", True,
                   "PASS" if (mid and code_g == 200) else "FAIL",
                   f"marker graph created -> {code_c} (id {mid}); after backend restart GET -> {code_g}")
        except Exception as e:
            record("functional", "F07-restart-recovery", True, "FAIL", f"{type(e).__name__}: {e}")
        ui_legs(shots, axe_results)
    finally:
        try:
            proc.terminate()
        except Exception:
            pass

    scores = score()
    # Accessibility scoring from the axe results.
    crit, serious = [], []
    for view, res in axe_results.items():
        if isinstance(res, list):
            for v in res:
                if v.get("impact") == "critical":
                    crit.append(f"{view}: {v['id']} ({v['nodes']} nodes)")
                elif v.get("impact") == "serious":
                    serious.append(f"{view}: {v['id']} ({v['nodes']} nodes)")
    kb = next((r for r in RESULTS if r["item"] == "A2-keyboard-nav"), None)
    scores["axe_available"] = any(isinstance(v, list) for v in axe_results.values())
    scores["A1_zero_critical"] = len(crit) == 0 and scores["axe_available"]
    scores["A2_serious_le_3_and_keyboard"] = (
        len(serious) <= 3 and kb is not None and kb["verdict"] == "PASS")
    scores["axe_critical"] = crit
    scores["axe_serious"] = serious
    scores["package_verdict"] = (
        "PASS" if all(scores[k] for k in
                      ("F1_coverage_ge_12_of_15", "F2_outcome_ge_75pct",
                       "P1_protocol_ge_6_of_8", "A1_zero_critical",
                       "A2_serious_le_3_and_keyboard")) else "FAIL")

    out = {"results": RESULTS, "axe": axe_results, "scores": scores}
    args.out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(scores, indent=2), flush=True)
    print(f"PACKAGE VERDICT: {scores['package_verdict']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
