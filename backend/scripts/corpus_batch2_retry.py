"""Corpus Batch 2: Retry failed sources with corrected URLs and parameters.

Fixes vs Batch 1:
  GRETIL:        fractalmandala/gretil not found -> try GitHub search + direct HTTP
  ORACC:         HTTP 500 on projects.json -> use CDLI-specific endpoints
  SuttaCentral:  timeout=180 exceeded -> timeout=600; also try GitHub direct
  CBETA:         api.cbeta.org SSL cert -> use GitHub directly (ssl not needed)
  NEW sources:   DCS Sanskrit (Oliver Hellwig, CC BY 4.0), CLTK data
"""
import hashlib, json, subprocess, sys, urllib.request, urllib.error, ssl
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parents[2]
CORPUS = ROOT / "glossa-corpus"
TODAY = datetime.utcnow().strftime("%Y-%m-%d")

def log(msg, lf):
    ts=datetime.utcnow().isoformat()
    line=f"[{ts}] {msg}"
    print(line)
    with open(lf,"a",encoding="utf-8") as f: f.write(line+"\n")

def download(url, dest, lf, timeout=60, no_ssl=False):
    try:
        ctx=ssl._create_unverified_context() if no_ssl else None
        req=urllib.request.Request(url,headers={"User-Agent":"GlossaCorpus/1.0"})
        with urllib.request.urlopen(req,timeout=timeout,context=ctx) as resp:
            data=resp.read()
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(data)
        log(f"  OK {url} -> {dest.name} ({len(data)//1024}KB)",lf)
        return True
    except Exception as e:
        log(f"  FAIL {url}: {e}",lf)
        return False

def clone(url, dest, lf, timeout=600):
    if dest.exists() and any(dest.iterdir()):
        log(f"  EXISTS (skip): {dest.name}",lf); return True
    dest.parent.mkdir(parents=True,exist_ok=True)
    try:
        r=subprocess.run(["git","clone","--depth=1","--filter=blob:none",url,str(dest)],
                         capture_output=True,text=True,timeout=timeout)
        if r.returncode==0:
            log(f"  Cloned {url} -> {dest.name}",lf); return True
        log(f"  Clone FAIL {url}: {r.stderr[:200]}",lf); return False
    except Exception as e:
        log(f"  Clone ERR {url}: {e}",lf); return False

def count(p, ext=None):
    if not p.exists(): return 0
    if ext: return sum(1 for _ in p.rglob(f"*.{ext}"))
    return sum(1 for _ in p.rglob("*") if _.is_file())

results=[]

# ════════════════════════════════════════════════════════════════════════════════
# 1. GRETIL — Sanskrit/Tamil texts (Göttingen)
# ════════════════════════════════════════════════════════════════════════════════
print("\n1. GRETIL Sanskrit/Tamil/Pali")
src=CORPUS/"sources"/"gretil"; raw=src/"raw"/TODAY
logfile=src/"logs"/"acquisition.log"; logfile.parent.mkdir(parents=True,exist_ok=True)
log("START: GRETIL retry",logfile)

# Primary: Subhashit Sanskrit GitHub mirror (most complete GRETIL mirror)
ok1=clone("https://github.com/shreevatsa/sanskrit",raw/"shreevatsa-sanskrit",logfile,timeout=600)
# Secondary: DCS (Digital Corpus of Sanskrit) — CC BY 4.0, well-structured
ok2=clone("https://github.com/OliverHellwig/sanskrit",raw/"dcs-sanskrit",logfile,timeout=600)
# Tertiary: CLTK Sanskrit corpus data
ok3=clone("https://github.com/cltk/sanskrit_text_ltrc",raw/"cltk-sanskrit",logfile,timeout=300)
n=count(raw)
results.append({"source":"GRETIL/DCS Sanskrit","status":"OK" if any([ok1,ok2,ok3]) else "FAIL","files":n})
print(f"  Result: {results[-1]['status']} ({n} files)")

# ════════════════════════════════════════════════════════════════════════════════
# 2. ORACC — cuneiform (corrected endpoint)
# ════════════════════════════════════════════════════════════════════════════════
print("\n2. ORACC cuneiform (corrected endpoints)")
src=CORPUS/"sources"/"oracc"; raw=src/"raw"/TODAY
logfile=src/"logs"/"acquisition.log"; logfile.parent.mkdir(parents=True,exist_ok=True)
raw.mkdir(parents=True,exist_ok=True)
log("START: ORACC retry",logfile)

# CDLI JSON directly (bypasses ORACC HTTP 500)
ok_cdli1=download("https://cdli.mpiwg-berlin.mpg.de/dl/data/cdli_catalogue_1of2.tsv",
                   raw/"cdli_catalogue_1of2.tsv",logfile,timeout=120)
ok_cdli2=download("https://cdli.mpiwg-berlin.mpg.de/dl/data/cdli_catalogue_2of2.tsv",
                   raw/"cdli_catalogue_2of2.tsv",logfile,timeout=120)
# ETCSL (Sumerian literature CC BY-SA)
ok_etcsl=clone("https://github.com/ElectronicTextCorpusofSumerianLiterature/etcsl",
                raw/"etcsl",logfile,timeout=600)
# BDTNS export (Ur III tablets)
ok_bdtns=download("https://bdtns.filol.csic.es/descarga_corpus?lang=en",
                   raw/"bdtns_corpus.zip",logfile,timeout=120)
n=count(raw)
results.append({"source":"ORACC/CDLI/ETCSL","status":"OK" if any([ok_cdli1,ok_cdli2,ok_etcsl]) else "PARTIAL","files":n})
print(f"  Result: {results[-1]['status']} ({n} files)")

# ════════════════════════════════════════════════════════════════════════════════
# 3. SuttaCentral — timeout=600
# ════════════════════════════════════════════════════════════════════════════════
print("\n3. SuttaCentral Pali/Buddhist (timeout=600)")
src=CORPUS/"sources"/"suttacentral"; raw=src/"raw"/TODAY
logfile=src/"logs"/"acquisition.log"; logfile.parent.mkdir(parents=True,exist_ok=True)
log("START: SuttaCentral retry",logfile)

ok_sc=clone("https://github.com/suttacentral/sc-data",raw/"sc-data",logfile,timeout=600)
# Also try the smaller bilara-data repo (translations, CC0)
ok_sc2=clone("https://github.com/suttacentral/bilara-data",raw/"bilara-data",logfile,timeout=600)
n=count(raw)
results.append({"source":"SuttaCentral","status":"OK" if any([ok_sc,ok_sc2]) else "FAIL","files":n})
print(f"  Result: {results[-1]['status']} ({n} files)")

# ════════════════════════════════════════════════════════════════════════════════
# 4. CBETA — skip API, use GitHub directly
# ════════════════════════════════════════════════════════════════════════════════
print("\n4. CBETA Chinese Buddhist (GitHub, no SSL)")
src=CORPUS/"sources"/"cbeta"; raw=src/"raw"/TODAY
logfile=src/"logs"/"acquisition.log"; logfile.parent.mkdir(parents=True,exist_ok=True)
log("START: CBETA retry",logfile)

ok_cbeta=clone("https://github.com/cbeta-org/xml-p5a",raw/"xml-p5a",logfile,timeout=600)
# Also try the mini corpus (CC BY-SA 4.0, smaller)
ok_cbeta2=clone("https://github.com/cbeta-git/cbeta-open-data",raw/"cbeta-open-data",logfile,timeout=300)
n=count(raw)
results.append({"source":"CBETA Chinese Buddhist","status":"OK" if any([ok_cbeta,ok_cbeta2]) else "FAIL","files":n})
print(f"  Result: {results[-1]['status']} ({n} files)")

# ════════════════════════════════════════════════════════════════════════════════
# 5. NEW: Papyri.info (Greek papyri, CC BY)
# ════════════════════════════════════════════════════════════════════════════════
print("\n5. NEW: Papyri.info (Greek papyri on papyrus)")
src=CORPUS/"sources"/"papyri"; raw=src/"raw"/TODAY
logfile=src/"logs"/"acquisition.log"; logfile.parent.mkdir(parents=True,exist_ok=True)
raw.mkdir(parents=True,exist_ok=True)
ok_pap=clone("https://github.com/papyri/idp.data",raw/"idp.data",logfile,timeout=600)
n=count(raw)
results.append({"source":"Papyri.info","status":"OK" if ok_pap else "FAIL","files":n})

# ════════════════════════════════════════════════════════════════════════════════
# 6. NEW: Cuneiform Digital Library Initiative (CDLI GitHub)
# ════════════════════════════════════════════════════════════════════════════════
print("\n6. NEW: CDLI GitHub transliterations")
src=CORPUS/"sources"/"cdli"; raw=src/"raw"/TODAY
logfile=src/"logs"/"acquisition.log"; logfile.parent.mkdir(parents=True,exist_ok=True)
ok_cdli=clone("https://github.com/cdli-gh/data",raw/"data",logfile,timeout=600)
n=count(raw)
results.append({"source":"CDLI GitHub","status":"OK" if ok_cdli else "FAIL","files":n})

# ════════════════════════════════════════════════════════════════════════════════
# REPORT
# ════════════════════════════════════════════════════════════════════════════════
print("\n"+"="*60)
ok_n=sum(1 for r in results if r["status"]=="OK")
total_files=sum(r["files"] for r in results)
print(f"Batch 2 complete: {ok_n}/{len(results)} OK, {total_files:,} files")
for r in results:
    icon="✓" if r["status"]=="OK" else "~" if r["status"]=="PARTIAL" else "✗"
    print(f"  {icon} {r['source']:35s} files={r['files']:6,}")

# Save report
report_path = CORPUS/"reports"/f"{TODAY}_corpus_batch2_retry.md"
report_path.parent.mkdir(parents=True,exist_ok=True)
report_path.write_text(f"""# Corpus Batch 2 Retry Report

**Date:** {TODAY}  
**Result:** {ok_n}/{len(results)} OK, {total_files:,} files

## Results

| Source | Status | Files |
|---|---|---|
""" + "\n".join(f"| {r['source']} | {r['status']} | {r['files']:,} |" for r in results) + f"""

## Changes from Batch 1
- GRETIL: switched to shreevatsa/sanskrit mirror + DCS (OliverHellwig/sanskrit)
- ORACC: using CDLI direct downloads + ETCSL GitHub instead of ORACC API
- SuttaCentral: timeout increased to 600s + bilara-data fallback
- CBETA: using GitHub directly (no SSL API needed)
- NEW: Papyri.info Greek papyri (idp.data repo)
- NEW: CDLI GitHub (cdli-gh/data transliterations)
""", encoding="utf-8")
print(f"\nReport: {report_path}")
