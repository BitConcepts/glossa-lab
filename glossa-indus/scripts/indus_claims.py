"""Batch 4: Claim extraction pipeline.

Processes registered literature documents and extracts scholarly claims about:
  - Sign values and functions
  - Language hypotheses
  - Positional patterns
  - Sequence readings
  - Archaeological contexts
  - Statistical findings
  - Critiques

Uses keyword + pattern matching against extracted text.
Output: claims/extracted_claims/{doc_id}.json

Per instruction plan section 9 — all claims preserve disagreement.
Claim status defaults to 'untested' until corpus testing is run.
"""
from __future__ import annotations
import json, re, sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parents[1]
LIT_DOCS = BASE / "literature" / "documents"
PROCESSED_TEXT = BASE / "processed" / "cleaned_text"
EXTRACTED_CLAIMS = BASE / "claims" / "extracted_claims"
QUEUE_FILE = BASE / "logs" / "claim_extraction_queue.json"
LOGS = BASE / "logs"

EXTRACTED_CLAIMS.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)

# ── Claim extraction patterns ──────────────────────────────────────────────────

# Sign value claims: "sign X means/represents/encodes Y" patterns
SIGN_VALUE_PATTERNS = [
    r"(?:sign|symbol)\s+(?:M77\s*/?\s*)?(\d+)\s+(?:means?|represents?|encodes?|reads?)\s+['\"]?([^.'\"]+)",
    r"(?:fish\s+sign)\s+(?:means?|represents?|encodes?|reads?)\s+['\"]?([^.'\"]{3,40})",
    r"(?:meen|min|mīn)\s+(?:fish|star|lightning)",
    r"rebus\s+principle.*?fish.*?([A-Za-z-]{3,20})",
    r"genitive\s+suffix\s+(?:in\s+Tamil|Proto-Dravidian)\s+['\"]([^'\"]+)['\"]",
]

# Language hypothesis claims
LANGUAGE_PATTERNS = [
    r"Indus\s+(?:script|writing)\s+(?:encodes?|represents?|records?)\s+(Proto-Dravidian|Dravidian|Indo-Aryan|Vedic|Munda|non-linguistic)",
    r"underlying\s+language\s+(?:is|was|may\s+be)\s+(Proto-Dravidian|Dravidian|Indo-Aryan|Munda|unknown|non-linguistic)",
    r"Dravidian\s+(?:hypothesis|interpretation|solution)\s+(?:is|remains?)\s+(most\s+likely|plausible|supported|controversial|unproven)",
    r"non-linguistic\s+(?:symbols?|hypothesis|interpretation)",
    r"logosyllabic\s+(?:script|writing\s+system)",
]

# Statistical claims  
STATISTICAL_PATTERNS = [
    r"conditional\s+entropy.*?linguistic",
    r"block\s+entropy.*?natural\s+language",
    r"Zipf[-\s]Mandelbrot\s+(?:law|distribution)",
    r"terminal\s+(?:signs?|symbols?)\s+(?:are|show|indicate|suggest)\s+(?:Dravidian|case\s+suffix|grammatical)",
    r"initial\s+(?:signs?|symbols?)\s+(?:are|function\s+as?|suggest)\s+(?:determinative|title|logogram)",
    r"positional\s+(?:analysis|statistics?|distribution)",
]

# Critique claims
CRITIQUE_PATTERNS = [
    r"(?:script\s+is|Indus\s+signs?\s+are)\s+non-linguistic",
    r"myth\s+of\s+a\s+literate\s+Harappan",
    r"collapse\s+of\s+the\s+Indus.?script\s+thesis",
    r"Sproat.*?non-linguistic|non-linguistic.*?Sproat",
    r"religious\s+or\s+political\s+symbols?",
]

# Archaeological context claims
ARCHAEOLOGICAL_PATTERNS = [
    r"(?:fish|jar|arrow|cattle|boat)\s+sign(?:s?)\s+cluster(?:s?)\s+(?:at|in|near)\s+([A-Za-z\s]+sites?)",
    r"(?:Mohenjo-?daro|Harappa|Lothal|Dholavira|Chanhu-?daro)\s+(?:exclusively|only|enriched)",
    r"contact\s+zone\s+(?:signs?|inscriptions?)\s+(?:differ|are\s+distinct|show)",
    r"trade\s+(?:route|network)\s+(?:evidence|sign)",
]

# ── Extraction functions ───────────────────────────────────────────────────────

def extract_claims_from_text(text: str, doc_id: str) -> list[dict]:
    """Pattern match claims from extracted text."""
    claims = []
    text_lower = text.lower()
    claim_counter = 0

    def add_claim(claim_type: str, normalized: str, quote: str = "", confidence: float = 0.5):
        nonlocal claim_counter
        claim_counter += 1
        claims.append({
            "claim_id": f"{doc_id}_{claim_type[:8]}_{claim_counter:04d}",
            "source_document_id": doc_id,
            "claim_type": claim_type,
            "normalized_claim": normalized,
            "quote_fragment": quote[:200],
            "claim_status": "untested",
            "testability": "directly_testable",
            "confidence_in_source": confidence,
            "extracted_at": datetime.utcnow().isoformat(),
        })

    # Sign value claims
    for pat in SIGN_VALUE_PATTERNS:
        matches = re.findall(pat, text, re.IGNORECASE)
        for m in matches[:3]:
            val = m if isinstance(m, str) else " / ".join(m)
            add_claim("sign_value_claim", f"Sign value: {val[:80]}", val, 0.6)

    # Language claims
    for pat in LANGUAGE_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            snippet = re.search(pat, text, re.IGNORECASE)
            add_claim("language_claim", f"Language hypothesis: {snippet.group(0)[:80]}", snippet.group(0), 0.7)

    # Statistical claims
    for pat in STATISTICAL_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            snippet = re.search(pat, text, re.IGNORECASE)
            add_claim("statistical_claim", f"Statistical finding: {snippet.group(0)[:80]}", snippet.group(0), 0.8)

    # Critique claims
    for pat in CRITIQUE_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            snippet = re.search(pat, text, re.IGNORECASE)
            add_claim("critique_claim", f"Critique: {snippet.group(0)[:80]}", snippet.group(0), 0.8)

    # Archaeological claims
    for pat in ARCHAEOLOGICAL_PATTERNS:
        matches = re.findall(pat, text, re.IGNORECASE)
        for m in matches[:2]:
            val = m if isinstance(m, str) else " / ".join(m)
            add_claim("archaeological_context_claim", f"Archaeological context: {val[:80]}", val, 0.5)

    return claims

def add_manual_claims(doc_id: str) -> list[dict]:
    """Manually curated claims for key papers that require precise encoding."""
    manual = []
    ts = datetime.utcnow().isoformat()

    if "parpola_2010" in doc_id:
        manual = [
            {
                "claim_id": f"{doc_id}_manual_001",
                "source_document_id": doc_id,
                "claim_type": "language_claim",
                "normalized_claim": "Indus script encodes Proto-Dravidian language using the rebus principle.",
                "claim_status": "partially_supported",
                "testability": "directly_testable",
                "falsification_condition": "If Dravidian phonotactics do not fit Indus sign bigrams better than Sanskrit.",
                "glossa_lab_evidence": "Phase-41: 1.0566x SA advantage; Phase-43: +0.484 log-units on V3 corpus [VERIFIED]",
                "confidence_in_source": 0.85,
                "extracted_at": ts,
            },
            {
                "claim_id": f"{doc_id}_manual_002",
                "source_document_id": doc_id,
                "claim_type": "sign_value_claim",
                "normalized_claim": "The fish sign (meen in Dravidian) is the primary rebus sign in the Indus script.",
                "signs_involved": ["fish sign family"],
                "sign_ids": {"mahadevan": ["72", "64", "70"], "glossa_note": "M77/72=phonetic meen [PARTIALLY_VERIFIED Phase-43]"},
                "proposed_value": "meen/min (fish; also star, lightning in Proto-Dravidian)",
                "proposed_language": "Proto-Dravidian",
                "claim_status": "partially_supported",
                "testability": "directly_testable",
                "falsification_condition": "If fish signs do not show terminal-sign followers consistent with case suffixes.",
                "glossa_lab_evidence": "Phase-43 T2.4: M77/72 terminal_frac=25.9% [SUPPORTED]",
                "confidence_in_source": 0.75,
                "extracted_at": ts,
            },
        ]
    elif "farmer_sproat_witzel" in doc_id:
        manual = [
            {
                "claim_id": f"{doc_id}_manual_001",
                "source_document_id": doc_id,
                "claim_type": "non_linguistic_claim",
                "normalized_claim": "The Indus script is not a writing system encoding language but consists of non-linguistic symbols.",
                "claim_status": "contradicted",
                "testability": "directly_testable",
                "falsification_condition": "Conditional entropy data in linguistic range; positional pattern above random baseline.",
                "contradicting_evidence": [
                    "Rao et al. 2009: conditional entropy falls in linguistic range",
                    "Phase-43: 20 TERMINAL_STRONG signs consistent with morphological suffixes",
                    "Phase-43: [M77/267][M77/99] = fixed title formula at inscription start",
                ],
                "confidence_in_source": 0.9,
                "extracted_at": ts,
            },
        ]
    elif "yadav_2010" in doc_id or "yadav_2009" in doc_id:
        manual = [
            {
                "claim_id": f"{doc_id}_manual_001",
                "source_document_id": doc_id,
                "claim_type": "statistical_claim",
                "normalized_claim": "Indus script sign frequencies follow a Zipf-Mandelbrot distribution.",
                "claim_status": "strongly_supported",
                "testability": "directly_testable",
                "falsification_condition": "If frequency distribution deviates from Zipf-Mandelbrot law.",
                "glossa_lab_evidence": "Phase-43: V3 Zipf exponent ~1.35 (super-Zipfian) [VERIFIED]",
                "confidence_in_source": 0.95,
                "extracted_at": ts,
            },
            {
                "claim_id": f"{doc_id}_manual_002",
                "source_document_id": doc_id,
                "claim_type": "sign_position_claim",
                "normalized_claim": "There are specific text-beginning and text-ending signs in the Indus corpus.",
                "claim_status": "strongly_supported",
                "testability": "directly_testable",
                "glossa_lab_evidence": "Phase-43: 20 TERMINAL_STRONG + 40 INITIAL_STRONG signs identified in V3 corpus [VERIFIED]",
                "confidence_in_source": 0.95,
                "extracted_at": ts,
            },
        ]

    return manual

# ── Main ───────────────────────────────────────────────────────────────────────

def process_document(doc_id: str) -> dict:
    """Extract claims from one document. Returns result dict."""
    doc_path = LIT_DOCS / f"{doc_id}.json"
    if not doc_path.exists():
        return {"doc_id": doc_id, "status": "not_found"}

    doc = json.loads(doc_path.read_text("utf-8"))

    # Try to get extracted text
    text = ""
    txt_path = PROCESSED_TEXT / f"{doc_id}.txt"
    if txt_path.exists():
        text = txt_path.read_text("utf-8", errors="replace")

    all_claims = []

    # Pattern-based extraction from text
    if text:
        auto_claims = extract_claims_from_text(text, doc_id)
        all_claims.extend(auto_claims)

    # Manual curated claims for key papers
    manual_claims = add_manual_claims(doc_id)
    all_claims.extend(manual_claims)

    if not all_claims:
        return {"doc_id": doc_id, "status": "no_claims", "text_available": bool(text)}

    # Save claims
    out = EXTRACTED_CLAIMS / f"{doc_id}.json"
    record = {
        "document_id": doc_id,
        "title": doc.get("title", ""),
        "extraction_date": datetime.utcnow().isoformat(),
        "total_claims": len(all_claims),
        "auto_extracted": len([c for c in all_claims if not c.get("source_document_id", "").endswith("_manual_001")]),
        "manually_curated": len(manual_claims),
        "claims": all_claims,
        "_citation": {
            "system": "Glossa-Lab Indus Evidence Graph Batch 4",
            "source_doc": doc_id,
        },
    }
    out.write_text(json.dumps(record, indent=2, ensure_ascii=False), "utf-8")
    return {"doc_id": doc_id, "status": "extracted", "n_claims": len(all_claims)}

def main() -> int:
    # Load claim extraction queue
    queue = []
    if QUEUE_FILE.exists():
        try:
            queue = json.loads(QUEUE_FILE.read_text("utf-8"))
        except Exception:
            pass

    # Also process all registered documents
    all_docs = [f.stem for f in LIT_DOCS.glob("*.json")]

    if not all_docs:
        # No literature yet — just show status
        print("No literature documents registered yet.")
        print("Run: python scripts/indus_literature_batch3.py")
        return 0

    print(f"\n{'='*60}")
    print(f"Batch 4: Claim Extraction — {len(all_docs)} documents")
    print(f"{'='*60}\n")

    results = []
    total_claims = 0

    for doc_id in all_docs:
        result = process_document(doc_id)
        results.append(result)
        n = result.get("n_claims", 0)
        total_claims += n
        status = result["status"]
        print(f"  {doc_id:40s} → {status} ({n} claims)")

    # Update queue status
    for item in queue:
        if item["doc_id"] in all_docs:
            item["status"] = "done"
    if QUEUE_FILE.exists():
        QUEUE_FILE.write_text(json.dumps(queue, indent=2), "utf-8")

    print(f"\n{'='*60}")
    print(f"Claim extraction complete:")
    print(f"  Documents processed: {len(results)}")
    print(f"  Total claims extracted: {total_claims}")
    print(f"  Output: {EXTRACTED_CLAIMS}")

    rpt = BASE / "reports" / "claim_reports" / "batch4_claims_report.json"
    rpt.parent.mkdir(parents=True, exist_ok=True)
    rpt.write_text(json.dumps({
        "batch_id": f"BATCH4-CLAIMS-{datetime.utcnow().strftime('%Y%m%d')}",
        "timestamp": datetime.utcnow().isoformat(),
        "total_documents": len(all_docs),
        "total_claims": total_claims,
        "results": results,
    }, indent=2), "utf-8")
    print(f"  Report: {rpt}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
