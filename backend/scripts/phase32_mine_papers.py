"""Phase-32 T1: Mine the 53 RMRL-scraped papers (Mahadevan + Balakrishnan)
for sign-ID references, DEDR cross-references, and proposed phonetic readings.

Output: backend/glossa_lab/data/mahadevan_papers_extracted.json
   {
     "_citation": {...},
     "_summary": {n_papers, n_sign_refs, n_dedr_refs, ...},
     "sign_references": [{paper_id, page, sign_id, context, candidate_reading}],
     "dedr_references": [{paper_id, page, dedr_id, tamil_word, context}],
     "m_catalogue_references": [{paper_id, page, m_id, context}],
     "candidate_readings_aggregated": {sign_id: [{phoneme, gloss, source_paper, dedr_ids}]}
   }
"""
from __future__ import annotations
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RMRL = REPO / "corpora" / "downloads" / "rmrl" / "research_papers"
OUT = REPO / "backend" / "glossa_lab" / "data" / "mahadevan_papers_extracted.json"

# ─── Regex patterns ──────────────────────────────────────────────────

SIGN_RE = re.compile(r"\bsign\s+(?:no\.?\s+)?(\d{1,3})\b", re.IGNORECASE)
DEDR_RE = re.compile(r"\bDEDR\s+(\d{1,5}[a-z]?)\b", re.IGNORECASE)
M_RE = re.compile(r"\bM-(\d{2,4})\b")  # Mahadevan catalogue IDs
PARPOLA_RE = re.compile(r"\bParpola\s+(?:no\.?\s+)?(\d{1,3})\b", re.IGNORECASE)

# Italicized Dravidian words tend to be in the form `*word*` after our OCR cleanup,
# but the OCR text from book_config.js doesn't preserve italics. Instead, we look
# for typical Dravidian glossing patterns:
#   `tamil-word (DEDR XXXX)`
#   `Dravidian *XXX*`
#   `Tamil XXX`
#   `< rebus XXX`
DEDR_WORD_RE = re.compile(
    r"\b([a-zA-Z\u00c0-\u017f][a-zA-Z\u00c0-\u017f\-']{2,30})\s*[\(\,;]?\s*(?:DEDR|D\.E\.D\.R\.?)\s+(\d{1,5}[a-z]?)",
    re.IGNORECASE,
)
TAMIL_GLOSS_RE = re.compile(
    r"\b(?:Tamil|Old\s+Tamil|Dr\.|Dr\s+|Dravidian)\s+([a-zA-Z\u00c0-\u017f][a-zA-Z\u00c0-\u017f\-'\u002f]{2,30})\b"
)

# ─── Extraction helpers ──────────────────────────────────────────────


def _ctx(text: str, start: int, end: int, window: int = 250) -> str:
    """Return context window around match, normalized whitespace."""
    a = max(0, start - window)
    b = min(len(text), end + window)
    snippet = text[a:b]
    snippet = re.sub(r"\s+", " ", snippet).strip()
    return snippet


def extract_paper(paper_dir: Path, author: str) -> dict:
    """Extract sign refs, DEDR refs, M-catalogue refs from one paper."""
    text_path = paper_dir / "text.json"
    if not text_path.exists():
        return None  # type: ignore
    d = json.loads(text_path.read_text(encoding="utf-8"))
    pages = d.get("pages", [])
    paper_id = d.get("id", paper_dir.name)

    sign_refs = []
    dedr_refs = []
    m_refs = []
    parpola_refs = []
    dedr_with_word = []

    for page_idx, page_text in enumerate(pages, 1):
        if not page_text:
            continue
        # Sign-ID references
        for m in SIGN_RE.finditer(page_text):
            sign_refs.append({
                "paper_id": paper_id,
                "page": page_idx,
                "sign_id": m.group(1),
                "context": _ctx(page_text, m.start(), m.end(), 200),
            })
        # DEDR alone
        for m in DEDR_RE.finditer(page_text):
            dedr_refs.append({
                "paper_id": paper_id,
                "page": page_idx,
                "dedr_id": m.group(1),
                "context": _ctx(page_text, m.start(), m.end(), 200),
            })
        # DEDR paired with a Tamil word
        for m in DEDR_WORD_RE.finditer(page_text):
            dedr_with_word.append({
                "paper_id": paper_id,
                "page": page_idx,
                "tamil_word": m.group(1),
                "dedr_id": m.group(2),
                "context": _ctx(page_text, m.start(), m.end(), 200),
            })
        # M-catalogue IDs
        for m in M_RE.finditer(page_text):
            m_refs.append({
                "paper_id": paper_id,
                "page": page_idx,
                "m_id": m.group(1),
                "context": _ctx(page_text, m.start(), m.end(), 150),
            })
        # Parpola sign IDs
        for m in PARPOLA_RE.finditer(page_text):
            parpola_refs.append({
                "paper_id": paper_id,
                "page": page_idx,
                "parpola_sign": m.group(1),
                "context": _ctx(page_text, m.start(), m.end(), 200),
            })

    return {
        "paper_id": paper_id,
        "author": author,
        "n_pages": len(pages),
        "n_chars": sum(len(p) for p in pages),
        "n_sign_refs": len(sign_refs),
        "n_dedr_refs": len(dedr_refs),
        "n_dedr_with_word": len(dedr_with_word),
        "n_m_catalogue_refs": len(m_refs),
        "n_parpola_refs": len(parpola_refs),
        "sign_refs": sign_refs,
        "dedr_refs": dedr_refs,
        "dedr_with_word": dedr_with_word,
        "m_catalogue_refs": m_refs,
        "parpola_refs": parpola_refs,
    }


# ─── Aggregator: collapse per-sign candidate readings ────────────────


def aggregate_candidate_readings(extracts: list[dict]) -> dict:
    """For each sign-ID, gather all proposed readings + DEDR cross-refs that
    co-occur in close context.
    """
    # Build paper-wide indices
    sign_to_evidence: dict[str, list[dict]] = defaultdict(list)
    for paper in extracts:
        # Each sign_ref already has context
        for ref in paper["sign_refs"]:
            sign_id = ref["sign_id"]
            ctx = ref["context"]
            # Look for DEDR / Tamil-word in the same context
            dedr_in_ctx = DEDR_RE.findall(ctx)
            words_in_ctx = []
            for m in DEDR_WORD_RE.finditer(ctx):
                words_in_ctx.append((m.group(1), m.group(2)))
            sign_to_evidence[sign_id].append({
                "paper_id": ref["paper_id"],
                "page": ref["page"],
                "context": ctx,
                "dedr_ids_in_context": dedr_in_ctx,
                "tamil_words_in_context": words_in_ctx,
            })
    return dict(sign_to_evidence)


# ─── Aggregate DEDR words across whole corpus ────────────────────────


def aggregate_dedr_words(extracts: list[dict]) -> dict:
    """Build a DEDR-id -> [(word, paper, page)] index."""
    dedr_index: dict[str, list[dict]] = defaultdict(list)
    for paper in extracts:
        for ref in paper["dedr_with_word"]:
            dedr_index[ref["dedr_id"]].append({
                "word": ref["tamil_word"],
                "paper_id": ref["paper_id"],
                "page": ref["page"],
                "context": ref["context"],
            })
    return dict(dedr_index)


# ─── Main ────────────────────────────────────────────────────────────


def main() -> int:
    print("=== Phase-32 T1: Mining 53 papers for sign + DEDR + reading evidence ===")
    extracts = []
    for author_dir in sorted(RMRL.iterdir()):
        if not author_dir.is_dir():
            continue
        author = author_dir.name
        paper_dirs = sorted(p for p in author_dir.iterdir() if p.is_dir())
        for pd in paper_dirs:
            r = extract_paper(pd, author)
            if r:
                extracts.append(r)
                if (r["n_sign_refs"] + r["n_dedr_refs"] + r["n_m_catalogue_refs"]) > 0:
                    print(f"  [{author}] {pd.name[:70]}: "
                          f"sign={r['n_sign_refs']:3d} dedr={r['n_dedr_refs']:3d} "
                          f"dedr+word={r['n_dedr_with_word']:3d} m={r['n_m_catalogue_refs']:3d}")

    # Aggregations
    print("\n[aggregate] sign-id -> evidence...")
    sign_evidence = aggregate_candidate_readings(extracts)
    print(f"  {len(sign_evidence)} distinct sign-IDs with at least one reference")
    print("\n[aggregate] DEDR-id -> Tamil-word evidence...")
    dedr_index = aggregate_dedr_words(extracts)
    print(f"  {len(dedr_index)} distinct DEDR-IDs with at least one paired word")

    # Top sign-IDs by reference frequency
    sign_freq = sorted(
        ((sid, len(ev)) for sid, ev in sign_evidence.items()),
        key=lambda kv: -kv[1],
    )
    print("\n[top 20 sign-IDs by mention count]")
    for sid, n in sign_freq[:20]:
        # Show DEDR cross-refs in context if any
        ev = sign_evidence[sid]
        dedrs = set()
        words = set()
        for e in ev:
            for d in e["dedr_ids_in_context"]:
                dedrs.add(d)
            for w, d in e["tamil_words_in_context"]:
                words.add(f"{w}/DEDR{d}")
        extras = ""
        if dedrs:
            extras += f"  DEDRs={','.join(sorted(dedrs))}"
        if words:
            extras += f"  words={','.join(list(words)[:5])}"
        print(f"  sign {sid}: {n} mentions{extras}")

    # Top DEDR-IDs by mention count
    dedr_freq = sorted(
        ((did, len(refs)) for did, refs in dedr_index.items()),
        key=lambda kv: -kv[1],
    )
    print("\n[top 20 DEDR-IDs by mention count]")
    for did, n in dedr_freq[:20]:
        words = set()
        for r in dedr_index[did]:
            words.add(r["word"].lower())
        print(f"  DEDR {did}: {n} mentions; words={','.join(sorted(words)[:5])}")

    # Save the structured output
    output = {
        "_citation": {
            "primary_source": "RMRL Digital Library research-paper collection",
            "full_reference": (
                "Mahadevan, Iravatham (38 papers, 1970-2018) + Balakrishnan, R "
                "(17 papers, place-name + Dravidian heritage research). Roja "
                "Muthiah Research Library, Chennai. https://rmrl.in/"
            ),
            "license": (
                "Mined from RMRL public flipbook viewer with rate-limited polite "
                "scraping (1.5-3s delay, descriptive User-Agent). Reference use "
                "only; consult CITATIONS.md."
            ),
            "see_also": "CITATIONS.md sections C.5 (Mahadevan papers) + Balakrishnan",
            "compiled_by": "Glossa-Lab Phase-32 T1 paper-text miner.",
        },
        "_summary": {
            "n_papers_processed": len(extracts),
            "n_total_sign_refs": sum(p["n_sign_refs"] for p in extracts),
            "n_total_dedr_refs": sum(p["n_dedr_refs"] for p in extracts),
            "n_total_dedr_with_word": sum(p["n_dedr_with_word"] for p in extracts),
            "n_total_m_catalogue_refs": sum(p["n_m_catalogue_refs"] for p in extracts),
            "n_distinct_sign_ids_referenced": len(sign_evidence),
            "n_distinct_dedr_ids_referenced": len(dedr_index),
        },
        "papers": extracts,
        "sign_evidence": sign_evidence,
        "dedr_word_index": dedr_index,
    }

    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote: {OUT}")
    print(f"  Size: {OUT.stat().st_size / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
