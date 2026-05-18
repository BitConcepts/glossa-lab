"""Phase-60b: Contact Zone Re-Investigation.

Phase-60 found 0 P-number readings. This script investigates why:
  1. Audits OCR quality of each publication file
  2. Tries broader regex (no quotes required, just number + reading context)
  3. Scans for any Parpola sign-number context patterns
  4. Produces a quality report and recommendation

GPU: torch for passage scoring.
Output: reports/phase60b_contact_investigation.json
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parents[1]))
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
P56     = REPO / "reports/phase56_parpola_expansion.json"
REPORTS = REPO / "reports"
REPORTS.mkdir(exist_ok=True)
OUT     = REPORTS / "phase60b_contact_investigation.json"

# ── BROADER patterns (no quotes required) ──────────────────────────────────
# Pattern 1: sign/Sign N reads/read "X"
# Pattern 2: P.N = X (Parpola sign N equals X)
# Pattern 3: sign N, transliteration X
# Pattern 4: number immediately followed by a romanized word
BROAD_PATTERNS = [
    r"sign[s]?\s+(?:no\.?\s*)?(\d{1,3})\b[^.]{0,60}(?:read|transliter|pronounce)[s]?\s+(?:as\s+)?[\"']?([a-z\u0100-\u017f\-]{2,20})[\"']?",
    r"P\.?\s*(\d{1,3})\s*[=:]\s*[\"']?([a-zāīūēōḍṭṇṅñśṣ\-]{2,20})[\"']?",
    r"parpola\s+(\d{1,3})[^.]{0,40}([a-z]{2,15})",
    r"sign\s+(\d{1,3})\s+(?:means?|represents?|is\s+read\s+as)\s+[\"']?([a-z\u0100-\u017f]{2,20})[\"']?",
    r"\b(\d{1,3})\s+(?:=|:)\s+[\"']?([a-z]{2,15}[āīūēō]?)[\"']?(?:\s+\(dravidian|\s+\(tamil|\s+in\s+dravidian)",
    r"sign\s+number\s+(\d{1,3})[^.]{0,60}[\"']([a-z]{2,20})[\"']",
]


def assess_ocr_quality(text: str, filename: str) -> dict:
    """Quick heuristic OCR quality assessment."""
    n_chars = len(text)
    n_alpha = sum(1 for c in text if c.isalpha())
    n_digit = sum(1 for c in text if c.isdigit())
    alpha_ratio = n_alpha / max(n_chars, 1)

    # Check for common OCR artefacts
    garbled = len(re.findall(r'[^\x00-\x7F]{3,}', text))  # runs of non-ASCII
    # Check if text has actual sentences
    n_sentences = len(re.findall(r'[.!?]\s+[A-Z]', text))
    # Check for Parpola-relevant vocabulary
    parpola_hits = len(re.findall(r'\b(?:parpola|dravidian|indus|sign|script|tamil|rebus|reading)\b', text, re.I))
    # Check for sign-number patterns at all
    sign_numbers = len(re.findall(r'\b\d{1,3}\b', text))

    quality = "GOOD"
    if alpha_ratio < 0.4:
        quality = "POOR_OCR"
    elif n_sentences < 5 and n_chars > 1000:
        quality = "MOSTLY_GARBLED"
    elif parpola_hits == 0:
        quality = "NO_RELEVANT_CONTENT"
    elif sign_numbers < 10:
        quality = "NO_SIGN_NUMBERS"

    return {
        "filename":     filename,
        "n_chars":      n_chars,
        "alpha_ratio":  round(alpha_ratio, 3),
        "n_sentences":  n_sentences,
        "parpola_hits": parpola_hits,
        "sign_numbers": sign_numbers,
        "garbled_runs": garbled,
        "quality":      quality,
    }


def broad_mine(text: str, source: str) -> list[dict]:
    """Mine with broader patterns."""
    findings = []
    seen = set()
    for pat in BROAD_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            g = m.groups()
            p_num = next((x for x in g if x and x.isdigit()), None)
            reading = next((x for x in g if x and not x.isdigit()), None)
            if p_num and reading and 1 <= int(p_num) <= 420 and len(reading) >= 2:
                key = (p_num, reading.lower()[:6])
                if key not in seen:
                    seen.add(key)
                    ctx = text[max(0, m.start()-80):m.end()+80].replace("\n", " ").strip()
                    findings.append({
                        "p_num": p_num, "reading": reading.strip(),
                        "source": source, "context": ctx[:200],
                        "pattern_type": "broad",
                    })
    return findings


def score_passages_gpu(passages: list[str]) -> list[float]:
    """GPU: score passages by Parpola-relevant keyword density."""
    if torch is None or not passages:
        return [0.0] * len(passages)
    scores = torch.zeros(len(passages), device=DEVICE)
    keywords = ["parpola", "dravidian", "indus", "sign", "reads", "tamil", "rebus"]
    for i, p in enumerate(passages):
        p_lower = p.lower()
        hits = sum(p_lower.count(kw) for kw in keywords)
        nums = re.findall(r'\b(\d{1,3})\b', p)
        scores[i] = float(hits) + float(len(nums)) * 0.5
    normed = (scores / scores.clamp(min=1).max()).cpu().tolist()
    return normed


def main():
    print("Phase-60b: Contact Zone Re-Investigation\n")

    pub_files = sorted(PUBS.glob("*.txt")) if PUBS.exists() else []
    print(f"  Publication files found: {len(pub_files)}")

    if not pub_files:
        print(f"  WARNING: No .txt files in {PUBS}")
        result = {
            "_citation": {"primary": ["A.1"]},
            "gpu_device": DEVICE,
            "n_pub_files": 0,
            "n_new_readings": 0,
            "recommendation": "No publication .txt files found in contact_zone/publications. "
                              "Files may need to be extracted from PDFs or downloaded separately.",
            "new_readings": [],
            "pub_quality": {},
        }
        OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
        return

    pub_quality = {}
    all_broad_findings = []
    high_relevance_passages = []

    for pub in pub_files:
        text = pub.read_text("utf-8", errors="replace")
        qa = assess_ocr_quality(text, pub.stem)
        pub_quality[pub.stem] = qa

        # Broad mining regardless of quality
        findings = broad_mine(text, pub.stem)
        all_broad_findings.extend(findings)
        if findings:
            print(f"  {pub.stem}: {len(findings)} broad findings (quality={qa['quality']})")
        else:
            print(f"  {pub.stem}: 0 findings (quality={qa['quality']}, "
                  f"parpola_hits={qa['parpola_hits']}, sign_nums={qa['sign_numbers']})")

        # Collect high-relevance passages for GPU scoring
        for para in re.split(r'\n{2,}', text):
            if (50 < len(para) < 1500 and
                    re.search(r'\b\d{1,3}\b', para) and
                    re.search(r'(?:sign|read|dravidian|parpola|rebus|tamil)', para, re.I)):
                high_relevance_passages.append({"text": para[:400], "source": pub.stem})

    scores = score_passages_gpu([p["text"] for p in high_relevance_passages])
    for i, score in enumerate(scores):
        high_relevance_passages[i]["score"] = round(score, 3)
    high_relevance_passages.sort(key=lambda x: -x["score"])

    print(f"\n[GPU:{DEVICE}] Scored {len(high_relevance_passages)} high-relevance passages")

    # Analysis
    quality_summary = Counter(v["quality"] for v in pub_quality.values())
    n_good_files = quality_summary.get("GOOD", 0)
    n_no_content = quality_summary.get("NO_RELEVANT_CONTENT", 0)
    n_poor_ocr   = quality_summary.get("POOR_OCR", 0) + quality_summary.get("MOSTLY_GARBLED", 0)

    print(f"\n=== Phase-60b Results ===")
    print(f"  Files analysed:      {len(pub_files)}")
    print(f"  Good quality:        {n_good_files}")
    print(f"  Poor OCR/garbled:    {n_poor_ocr}")
    print(f"  No relevant content: {n_no_content}")
    print(f"  Broad findings:      {len(all_broad_findings)}")
    print(f"  High-relevance passages: {len(high_relevance_passages)}")

    if all_broad_findings:
        print(f"\n  Sample findings:")
        for f in all_broad_findings[:5]:
            print(f"  P{f['p_num']} = {f['reading']!r} (source: {f['source']})")

    # Recommendation
    if n_poor_ocr >= len(pub_files) * 0.5:
        recommendation = ("POOR_OCR: More than half of publication files have poor OCR quality. "
                          "Recommend: re-extract PDFs with better OCR tool (Tesseract or Mistral). "
                          "Phase-47 T2 already found P-number hits in Levit 2010 and Parpola 2010 — "
                          "those should be the primary mining targets.")
    elif n_no_content >= len(pub_files) * 0.5:
        recommendation = ("NO_RELEVANT_CONTENT: Publication files do not contain Parpola-relevant "
                          "vocabulary. Files may be non-Indus publications or wrong format. "
                          "Verify publication list in contact_zone/publications/.")
    elif len(all_broad_findings) == 0:
        recommendation = ("0 HITS WITH BROAD PATTERNS: Publications exist but contain no "
                          "sign-number + reading patterns even with broad regex. "
                          "These are likely non-technical texts (popular articles, not academic). "
                          "Recommend: obtain Parpola 1994 book OCR or use Phase-47 T2 data directly.")
    else:
        recommendation = (f"PARTIAL_SUCCESS: {len(all_broad_findings)} broad findings with relaxed patterns. "
                          "Review and curate — some may be false positives from number+word coincidences.")

    print(f"\n  Recommendation: {recommendation}")

    result = {
        "_citation": {"primary": ["A.1", "A.13"]},
        "gpu_device": DEVICE,
        "n_pub_files":    len(pub_files),
        "n_new_readings": len(all_broad_findings),
        "new_readings":   all_broad_findings[:30],
        "pub_quality":    pub_quality,
        "quality_summary": dict(quality_summary),
        "top_passages":   high_relevance_passages[:10],
        "recommendation": recommendation,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nReport: {OUT}")


if __name__ == "__main__":
    main()
