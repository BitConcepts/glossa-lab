"""CBETA Chinese Buddhist corpus acquisition — correct URLs.

CBETA repository ecosystem (2025-2026):
  cbeta-org/xml-p5          → OFFICIAL public TEI P5 (~2GB, updated 2025-12-25)
  cbeta-git/xml-p5a         → Internal editing version (exists but not for public)
  DILA-edu/cbeta-normal-text → Plain text, 一卷一檔 (smaller, 2025)
  DILA-edu/CBETA-txt        → TAF plain text (T/X/J canons only, stats-friendly)
  mahawu/BM_u8              → Basic Markup UTF-8 (simple format)
  DILA-edu/CBETA_TAFxml     → TAF XML (analysis-friendly subset)

License: CC BY-NC-SA 3.0 Taiwan (non-commercial, share-alike)
  → license_class: research_use
  → Safe for academic/research corpus, NOT for commercial training

What went wrong in Batch 1:
  cbeta-org/xml-p5a  — WRONG: p5a is under cbeta-git not cbeta-org
  cbeta-git/cbeta-open-data — WRONG: this repo never existed

Strategy for this acquisition:
  1. Clone DILA-edu/cbeta-normal-text (plain text, smallest, most useful for LM)
  2. Clone mahawu/BM_u8 (basic markup, fast clone)
  3. Try cbeta-org/xml-p5 (full TEI P5 — large but the canonical version)
  4. DILA-edu/CBETA-txt (TAF text subset as fallback)
"""
import subprocess, sys, json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parents[2]
CORPUS = ROOT / "glossa-corpus"
TODAY = datetime.utcnow().strftime("%Y-%m-%d")

def log(msg, lf):
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    with open(lf, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def clone(url, dest, lf, timeout=600):
    if dest.exists() and any(dest.iterdir()):
        log(f"  EXISTS (skip): {dest.name}", lf)
        return True, "existed"
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(
            ["git", "clone", "--depth=1", "--filter=blob:none", url, str(dest)],
            capture_output=True, text=True, timeout=timeout,
        )
        if r.returncode == 0:
            log(f"  OK cloned: {url} -> {dest.name}", lf)
            return True, "cloned"
        log(f"  FAIL {url}: {r.stderr[:300]}", lf)
        return False, r.stderr[:200]
    except subprocess.TimeoutExpired:
        log(f"  TIMEOUT {url} (>{timeout}s)", lf)
        return False, "timeout"
    except Exception as e:
        log(f"  ERR {url}: {e}", lf)
        return False, str(e)

def count_files(p, ext=None):
    if not p.exists():
        return 0
    if ext:
        return sum(1 for _ in p.rglob(f"*.{ext}"))
    return sum(1 for _ in p.rglob("*") if _.is_file())

# ── Setup ─────────────────────────────────────────────────────────────────────
src = CORPUS / "sources" / "cbeta"
logfile = src / "logs" / "acquisition.log"
logfile.parent.mkdir(parents=True, exist_ok=True)
log("=" * 60, logfile)
log("START: CBETA acquisition (corrected URLs)", logfile)
log(f"cbeta-org org created: 2026-02-21 (new)", logfile)
log(f"Correct repos identified from cbdata.dila.edu.tw", logfile)

results = []

# ════════════════════════════════════════════════════════════════════════════════
# 1. Plain text (cbeta-normal-text) — smallest, most useful for LM
# ════════════════════════════════════════════════════════════════════════════════
print("\n1. CBETA Normal Text (plain text, 一卷一檔)")
raw = src / "raw" / TODAY / "cbeta-normal-text"
ok, reason = clone(
    "https://github.com/DILA-edu/cbeta-normal-text",
    raw, logfile, timeout=300
)
n = count_files(raw, "txt") + count_files(raw, "md")
log(f"  normal-text: {n} files ({reason})", logfile)
results.append({"source": "cbeta-normal-text (DILA-edu)", "status": "OK" if ok else "FAIL",
                "url": "https://github.com/DILA-edu/cbeta-normal-text",
                "files": n, "note": "Plain text 一卷一檔, CC BY-NC-SA 3.0"})

# ════════════════════════════════════════════════════════════════════════════════
# 2. BM (Basic Markup) — simple format, UTF-8
# ════════════════════════════════════════════════════════════════════════════════
print("\n2. CBETA Basic Markup UTF-8 (BM_u8)")
raw2 = src / "raw" / TODAY / "BM_u8"
ok2, reason2 = clone(
    "https://github.com/mahawu/BM_u8",
    raw2, logfile, timeout=300
)
n2 = count_files(raw2)
log(f"  BM_u8: {n2} files ({reason2})", logfile)
results.append({"source": "BM_u8 (mahawu)", "status": "OK" if ok2 else "FAIL",
                "url": "https://github.com/mahawu/BM_u8",
                "files": n2, "note": "Basic Markup UTF-8, simple format"})

# ════════════════════════════════════════════════════════════════════════════════
# 3. Official TEI P5 (cbeta-org/xml-p5) — ~2GB, canonical version
#    Use --sparse-checkout to avoid downloading everything
# ════════════════════════════════════════════════════════════════════════════════
print("\n3. CBETA XML P5 (official TEI P5, cbeta-org)")
raw3 = src / "raw" / TODAY / "xml-p5"
# Use sparse checkout: only get T (Taisho, most important) directory first
if raw3.exists() and any(raw3.iterdir()):
    log(f"  EXISTS (skip): xml-p5", logfile)
    ok3, reason3 = True, "existed"
else:
    raw3.mkdir(parents=True, exist_ok=True)
    try:
        # Initialize with no-checkout, then sparse checkout just T canon
        r1 = subprocess.run(
            ["git", "clone", "--filter=blob:none", "--sparse", "--depth=1",
             "https://github.com/cbeta-org/xml-p5", str(raw3)],
            capture_output=True, text=True, timeout=300
        )
        if r1.returncode == 0:
            # Set sparse checkout to get only the T (Taisho) canon
            subprocess.run(
                ["git", "-C", str(raw3), "sparse-checkout", "set", "T", "X"],
                capture_output=True, timeout=120
            )
            log(f"  OK sparse-cloned xml-p5 (T+X canons)", logfile)
            ok3, reason3 = True, "sparse-cloned"
        else:
            log(f"  FAIL xml-p5: {r1.stderr[:200]}", logfile)
            ok3, reason3 = False, r1.stderr[:100]
    except subprocess.TimeoutExpired:
        log(f"  TIMEOUT xml-p5", logfile)
        ok3, reason3 = False, "timeout"
    except Exception as e:
        log(f"  ERR xml-p5: {e}", logfile)
        ok3, reason3 = False, str(e)

n3 = count_files(raw3, "xml")
log(f"  xml-p5: {n3} XML files ({reason3})", logfile)
results.append({"source": "xml-p5 (cbeta-org)", "status": "OK" if ok3 else "FAIL",
                "url": "https://github.com/cbeta-org/xml-p5",
                "files": n3, "note": "Official TEI P5 (T+X sparse), CC BY-NC-SA 3.0"})

# ════════════════════════════════════════════════════════════════════════════════
# 4. TAF Text (statistics-friendly plain text, T/X/J canons)
# ════════════════════════════════════════════════════════════════════════════════
print("\n4. CBETA TAF Text (DILA-edu, stats-friendly)")
raw4 = src / "raw" / TODAY / "CBETA-txt"
ok4, reason4 = clone(
    "https://github.com/DILA-edu/CBETA-txt",
    raw4, logfile, timeout=300
)
n4 = count_files(raw4, "txt")
log(f"  CBETA-txt: {n4} files ({reason4})", logfile)
results.append({"source": "CBETA-txt (DILA-edu)", "status": "OK" if ok4 else "FAIL",
                "url": "https://github.com/DILA-edu/CBETA-txt",
                "files": n4, "note": "TAF plain text T/X/J canons"})

# ════════════════════════════════════════════════════════════════════════════════
# 5. Gaiji (Chinese character database)
# ════════════════════════════════════════════════════════════════════════════════
print("\n5. CBETA Gaiji database (missing characters)")
raw5 = src / "raw" / TODAY / "cbeta_gaiji"
ok5, reason5 = clone(
    "https://github.com/cbeta-org/cbeta_gaiji",
    raw5, logfile, timeout=120
)
n5 = count_files(raw5)
log(f"  cbeta_gaiji: {n5} files ({reason5})", logfile)
results.append({"source": "cbeta_gaiji (cbeta-org)", "status": "OK" if ok5 else "FAIL",
                "url": "https://github.com/cbeta-org/cbeta_gaiji",
                "files": n5, "note": "Gaiji (missing characters + Sanskrit characters) DB"})

# ════════════════════════════════════════════════════════════════════════════════
# Write provenance and report
# ════════════════════════════════════════════════════════════════════════════════
prov = {
    "item_id": "cbeta/corpus",
    "source_name": "CBETA — Chinese Buddhist Electronic Text Association / Foundation",
    "source_url": "https://cbeta.org",
    "download_date": TODAY,
    "local_path": str((src / "raw" / TODAY).relative_to(CORPUS)),
    "license": "CC BY-NC-SA 3.0 Taiwan",
    "license_url": "https://www.cbeta.org/copyright.php",
    "rights_status": "research_use",
    "license_class": "research_use",
    "language": "zho",
    "script": "Han (Chinese characters)",
    "period": "200 BCE - 1900 CE",
    "source_format": "tei_xml; plain_text",
    "processing_stage": "raw",
    "status": "keep",
    "confidence": "0.97",
    "notes": (
        "CC BY-NC-SA 3.0 Taiwan: non-commercial use, share-alike. "
        "Academic/research use: permitted. Commercial use: requires permission. "
        "Organization restructured 2023: CBETA Foundation. "
        "New GitHub org cbeta-org created 2026-02-21. "
        "Previous attempts failed: cbeta-org/xml-p5a (wrong — p5a is under cbeta-git), "
        "cbeta-git/cbeta-open-data (never existed)."
    ),
    "repositories": {
        "xml-p5 (canonical public TEI P5)": "https://github.com/cbeta-org/xml-p5",
        "cbeta-normal-text (plain text)": "https://github.com/DILA-edu/cbeta-normal-text",
        "CBETA-txt (TAF plain text)": "https://github.com/DILA-edu/CBETA-txt",
        "BM_u8 (basic markup)": "https://github.com/mahawu/BM_u8",
        "xml-p5a (internal, not public)": "https://github.com/cbeta-git/xml-p5a",
    },
    "source_score": {
        "textual_value": 5, "metadata_quality": 5, "license_clarity": 5,
        "language_coverage": 5, "scholarly_reliability": 5, "annotation_depth": 4,
    },
}
import yaml
(src / "provenance.yaml").write_text(
    yaml.dump(prov, allow_unicode=True, default_flow_style=False), "utf-8"
)

# Summary
total_ok = sum(1 for r in results if r["status"] == "OK")
total_files = sum(r["files"] for r in results)
print(f"\n{'='*60}")
print(f"CBETA acquisition: {total_ok}/{len(results)} OK, {total_files:,} files")
for r in results:
    icon = "✓" if r["status"] == "OK" else "✗"
    print(f"  {icon} {r['source']:35s} files={r['files']:6,}  {r['note']}")

# Save report
rpt = CORPUS / "reports" / f"{TODAY}_cbeta_acquisition.md"
rpt.parent.mkdir(parents=True, exist_ok=True)
rpt.write_text(f"""# CBETA Acquisition Report

**Date:** {TODAY}  
**Result:** {total_ok}/{len(results)} OK, {total_files:,} total files

## Key Finding: Why Batch 1 Failed

- We tried `cbeta-org/xml-p5a` → **WRONG**: `p5a` is the internal version under `cbeta-git` user account, not the `cbeta-org` organization
- We tried `cbeta-git/cbeta-open-data` → **WRONG**: this repo never existed

**Correct public version:** `https://github.com/cbeta-org/xml-p5`  
(the `cbeta-org` GitHub organization was only created on 2026-02-21)

## CBETA Repository Map

| Repository | Purpose | License |
|---|---|---|
| `cbeta-org/xml-p5` | Official TEI P5 (public) | CC BY-NC-SA 3.0 TW |
| `cbeta-git/xml-p5a` | Internal editing version | not public |
| `DILA-edu/cbeta-normal-text` | Plain text, 一卷一檔 | CC BY-NC-SA 3.0 TW |
| `DILA-edu/CBETA-txt` | TAF plain text (T/X/J) | CC BY-NC-SA 3.0 TW |
| `mahawu/BM_u8` | Basic Markup UTF-8 | CC BY-NC-SA 3.0 TW |
| `cbeta-org/cbeta_gaiji` | Missing characters DB | CC BY-NC-SA 3.0 TW |

## License Note
CC BY-NC-SA 3.0 Taiwan: **non-commercial research use permitted**.  
Commercial use requires permission from CBETA Foundation + original copyright holders.

## Acquisition Results

""" + "\n".join(f"- **{r['source']}**: {r['status']} ({r['files']:,} files) — {r['note']}" for r in results),
encoding="utf-8")
print(f"\nReport: {rpt}")
log(f"DONE: {total_ok}/{len(results)} OK, {total_files} files", logfile)
