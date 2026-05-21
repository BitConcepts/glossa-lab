"""Phase-60: Contact Zone Deep Mining with Parpola Sign Numbers.
Re-mines publications using Parpola P-number patterns (not M-numbers).
GPU: torch for passage relevance scoring. Output: reports/phase60_contact_deep.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))  # add backend/ to sys.path
from glossa_lab.gpu_utils import detect_device as _detect_device  # noqa: E402

try:
    import torch
except ImportError:
    torch = None

DEVICE = _detect_device()
if DEVICE == "cuda" and torch is not None:
    print(f"[GPU] torch {torch.__version__} — device: cuda")

REPO    = Path(__file__).parents[2]
PUBS    = REPO / "corpora/downloads/contact_zone/publications"
ANCHORS = REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
P56     = REPO / "reports/phase56_parpola_expansion.json"
REPORTS = REPO / "reports"; REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase60_contact_deep.json"

# All Parpola sign numbers we care about — from Phase-56 master crosswalk
TARGET_P_NUMS = list(range(1, 420))

# Reading/phoneme patterns in Parpola's text
READING_PATTERNS = [
    r"sign\s+(?:no\.?\s*)?(\d{1,3})\b[^.]{0,80}(?:read|reads?|means?|represents?|stands?\s+for)\s+[\'\"]([^\'\"\n]{2,25})[\'\"]",
    r"[\'\"]([a-z\u0080-\uffff\-]{2,20})[\'\"]\s+(?:\(|=\s*)sign\s+(\d{1,3})",
    r"P\.?\s*(\d{1,3})\s*[=:]\s*[\'\"]([^\'\"\n]{2,25})[\'\"]",
    r"(\d{1,3})\s+[\'\"]([a-z\u0080-\uffff]{2,20})[\'\"].*?dravidian",
    r"sign\s+(\d{1,3})\s+.*?phoneme\s+/([^/\n]{1,15})/",
]

def mine_for_p_numbers(text: str) -> list[dict]:
    """Extract P-number to reading associations from text."""
    findings = []
    seen = set()
    for pat in READING_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            g = m.groups()
            p_num = next((x for x in g if x and x.isdigit()), None)
            reading = next((x for x in g if x and not x.isdigit()), None)
            if p_num and reading and 1 <= int(p_num) <= 420:
                key = (p_num, reading.lower()[:8])
                if key not in seen:
                    seen.add(key)
                    ctx = text[max(0,m.start()-80):m.end()+80].replace("\n"," ").strip()
                    findings.append({"p_num": p_num, "reading": reading.strip(), "context": ctx[:200]})
    return findings


def score_passages_gpu(passages: list[str], target_p_nums: set) -> list[float]:
    """GPU: score passages by P-number density."""
    if torch is None or not passages: return [1.0]*len(passages)
    scores = torch.zeros(len(passages), device=DEVICE)
    for i, p in enumerate(passages):
        nums = re.findall(r'\b(\d{1,3})\b', p)
        hits = sum(1 for n in nums if int(n) in target_p_nums) if nums else 0
        scores[i] = float(hits)
    normed = (scores / scores.clamp(min=1).max()).cpu().tolist()
    print(f"[GPU:{DEVICE}] Scored {len(passages)} passages")
    return normed


def main():
    print("Phase-60: Contact Zone Deep Mining (Parpola P-numbers)\n")
    # Load Phase-56 master to know what P-numbers map to what
    master = {}
    if P56.exists():
        p56 = json.loads(P56.read_text("utf-8"))
        master = p56.get("master_crosswalk", {})
    target_p_set = set(range(1, 420))
    all_findings: list[dict] = []
    pub_files = sorted(PUBS.glob("*.txt"))
    print(f"Mining {len(pub_files)} publications for Parpola sign numbers...")
    for pub in pub_files:
        text = pub.read_text("utf-8", errors="replace")
        findings = mine_for_p_numbers(text)
        for f in findings:
            f["source"] = pub.stem
            # Cross-reference with Phase-56 master
            p_num = f["p_num"]
            if p_num in master:
                f["known_m_number"] = master[p_num].get("m_number", "")
                f["known_reading"] = master[p_num].get("reading", "")
                f["reading_match"] = f["reading"].lower()[:4] == master[p_num].get("reading","").lower()[:4]
        all_findings.extend(findings)
        if findings:
            print(f"  {pub.stem}: {len(findings)} P-number readings found")
    # Score high-density passages GPU
    paras = []
    for pub in pub_files:
        text = pub.read_text("utf-8", errors="replace")
        for para in re.split(r'\n{2,}', text):
            if 50 < len(para) < 1000:
                nums = re.findall(r'\b(\d{1,3})\b', para)
                if sum(1 for n in nums if int(n) in target_p_set) >= 3:
                    paras.append(para.replace("\n"," ").strip()[:400])
    scores = score_passages_gpu(paras, target_p_set)
    top_passages = sorted(zip(paras, scores), key=lambda x: -x[1])[:15]
    # New readings not in Phase-56
    new_readings = [f for f in all_findings
                    if f.get("known_m_number") and not f.get("reading_match", True)]
    print("\n=== Phase-60 Results ===")
    print(f"  Total P-number findings: {len(all_findings)}")
    print(f"  Potential new/corrected readings: {len(new_readings)}")
    print(f"  High-density passages: {len(top_passages)}")
    for f in all_findings[:10]:
        print(f"  P{f['p_num']} = {f['reading']!r} (source: {f['source']})")
    result = {
        "_citation": {"primary": ["A.1","A.13"], "parpola_1994": True},
        "gpu_device": DEVICE,
        "n_findings": len(all_findings),
        "n_new_potential": len(new_readings),
        "all_findings": all_findings[:50],
        "new_readings": new_readings[:20],
        "top_passages": [{"text": p[:200], "score": round(s,3)} for p,s in top_passages[:10]],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"Report: {OUT}")


if __name__ == "__main__":
    main()
