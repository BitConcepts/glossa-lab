"""Corpus acquisition module for Glossa Lab.

Downloads public corpus data from known sources and converts it into
the glossa_lab format (list of sign-sequence lists).

Each corpus in the CATALOG has:
  id          — unique string identifier used in acquire_corpus actions
  name        — human-readable name
  description — what it is and why it matters for decipherment research
  source      — where the data comes from (institution + URL)
  format      — data format of the raw download
  tier        — which Glossa Lab experimental tier it targets
  size_estimate — approximate token count after acquisition
  status      — available | requires_auth | requires_manual | paid
  fetch_fn    — name of the Python function to call (or None if manual)

FETCH FUNCTIONS encode the download-and-convert logic.
All return: {"inscriptions": [[sign, sign, ...], ...], "metadata": {...}}
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# ── Catalog of acquirable corpora ─────────────────────────────────────────────

CATALOG: list[dict[str, Any]] = [

    # ── CDLI — Cuneiform Digital Library Initiative ────────────────────────
    {
        "id":           "cdli_proto_elamite",
        "name":         "Proto-Elamite (CDLI)",
        "description":  (
            "~5,000 administrative tablets from ancient Iran (c. 3200–2900 BCE). "
            "Oldest undeciphered script with a large corpus. Sign sequences encode "
            "numerical/commodity records. Ideal for structural analysis (Tier 3). "
            "Source: CDLI public API — no authentication required."
        ),
        "source":       "CDLI (cdli.ucla.edu)",
        "url":          "https://cdli.ucla.edu/api/search/texts?period=Proto-Elamite&wt=json&rows=500",
        "format":       "cdli_json",
        "tier":         "Tier 3 — logographic structure detection",
        "size_estimate": "~15,000–50,000 sign tokens",
        "status":       "available",
        "fetch_fn":     "fetch_cdli",
        "period":       "Proto-Elamite",
        "note":         "CDLI API returns cuneiform transliterations; signs are space-separated strings.",
    },
    {
        "id":           "cdli_sumerian_ur3",
        "name":         "Sumerian Ur III (CDLI)",
        "description":  (
            "Sumerian administrative texts from the Ur III period (c. 2100–2000 BCE). "
            "Deciphered script with known vocabulary — excellent as a logographic "
            "reference model for Tier 3 comparisons against Indus Script structure."
        ),
        "source":       "CDLI (cdli.ucla.edu)",
        "url":          "https://cdli.ucla.edu/api/search/texts?period=Ur+III&wt=json&rows=500",
        "format":       "cdli_json",
        "tier":         "Tier 3 — reference logographic LM",
        "size_estimate": "~30,000–100,000 sign tokens",
        "status":       "available",
        "fetch_fn":     "fetch_cdli",
        "period":       "Ur III",
        "note":         "Sumerian is already partially represented in backend/tests/corpora/fixtures/sumerian.txt",
    },
    {
        "id":           "oracc_akkadian",
        "name":         "Akkadian — ORACC Corpus",
        "description":  (
            "Open Richly Annotated Cuneiform Corpus (ORACC). Akkadian texts spanning "
            "Old Babylonian to Neo-Assyrian periods. Rich morphological annotation. "
            "Useful as a Semitic reference LM alongside Hebrew for cross-validation."
        ),
        "source":       "ORACC (oracc.museum.upenn.edu)",
        "url":          "https://github.com/oracc/json-dump/raw/main/epsd2.zip",
        "format":       "oracc_json",
        "tier":         "Tier 1 — alternative Semitic LM",
        "size_estimate": "~200,000+ tokens",
        "status":       "available",
        "fetch_fn":     "fetch_oracc",
        "note":         "Large corpus; download may take 30–60 seconds.",
    },

    # ── Linear A / Aegean scripts ──────────────────────────────────────────
    {
        "id":           "sigla_linear_a",
        "name":         "Linear A — SigLA Database",
        "description":  (
            "Signary of Linear A (SigLA) from Oxford. ~1,500 inscriptions from "
            "Crete and the Aegean (c. 1800–1450 BCE). Undeciphered Minoan language. "
            "Share ~50 sign values with Linear B (AB-signs), giving partial phonetic "
            "anchors. Tier 4 candidate with a known script-overlap LM."
        ),
        "source":       "tylerlengyel.com Phase 1 / SigLA (sigla.classics.ox.ac.uk)",
        "url":          "https://raw.githubusercontent.com/TylerLengyel/linear-a/main/linear_a_phase1.csv",
        "format":       "csv_sequences",
        "tier":         "Tier 4 — Ventris-style grid recovery",
        "size_estimate": "~7,500–10,000 sign tokens",
        "status":       "available",
        "fetch_fn":     "fetch_url_csv",
        "note":         "CSV with columns: inscription_id, sequence (space-separated sign codes).",
    },
    {
        "id":           "tylerlengyel_linear_a",
        "name":         "Linear A — TylerLengyel Phase 1 (fallback)",
        "description":  (
            "Alternative source for Linear A sign sequences using the GORILA sign codes. "
            "Fallback when SigLA download is unavailable."
        ),
        "source":       "tylerlengyel.com Phase 1 data",
        "url":          "https://raw.githubusercontent.com/TylerLengyel/linear-a/refs/heads/main/phase1_sequences.json",
        "format":       "json_sequences",
        "tier":         "Tier 4",
        "size_estimate": "~7,000 sign tokens",
        "status":       "available",
        "fetch_fn":     "fetch_url_json",
        "note":         "JSON array of inscription objects with 'signs' array.",
    },

    # ── Meroitic (expanded) ────────────────────────────────────────────────
    {
        "id":           "meroitic_rilly_expanded",
        "name":         "Meroitic — Rilly (2007) Appendix",
        "description":  (
            "Expanded Meroitic corpus from Rilly (2007) La langue du Royaume de Méroé. "
            "~300+ funerary and royal inscriptions; more representative than our "
            "current 551-token sample. Required for meaningful Tier 1f experiments "
            "testing Meroitic language family hypotheses beyond Coptic."
        ),
        "source":       "Rilly (2007); REM (Répertoire d'épigraphie méroïtique)",
        "url":          None,
        "format":       "manual",
        "tier":         "Tier 1f — graceful degradation + language family testing",
        "size_estimate": "~5,000–20,000 sign tokens",
        "status":       "requires_manual",
        "fetch_fn":     None,
        "note":         (
            "Requires purchasing or borrowing Rilly (2007) from a library. "
            "Once obtained, use execute_script to load and register the data. "
            "Contact: claude.rilly@cnrs.fr for digital access."
        ),
    },

    # ── Indus Script supplements ───────────────────────────────────────────
    {
        "id":           "yadav2010_indus",
        "name":         "Indus Script — Yadav et al. (2010) Statistical Analysis",
        "description":  (
            "Statistical corpus from Yadav et al. (2010) 'Statistical Analysis of the "
            "Indus Script Using n-grams'. Contains ~1,750 inscriptions with frequency "
            "tables. Useful for validating our entropy results against published statistics."
        ),
        "source":       "Yadav et al. (2010), PLOS ONE doi:10.1371/journal.pone.0009810",
        "url":          "https://doi.org/10.1371/journal.pone.0009810",
        "format":       "manual_paper",
        "tier":         "Tier 5 — validation reference",
        "size_estimate": "~8,000 sign tokens",
        "status":       "requires_manual",
        "fetch_fn":     None,
        "note":         (
            "Open access paper. Supplementary data contains inscription sequences. "
            "Download at: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0009810"
        ),
    },
    {
        "id":           "mahadevan1977_concordance",
        "name":         "Mahadevan (1977) Concordance — Full Transcription",
        "description":  (
            "The canonical Indus Script corpus. 3,450 inscriptions with Mahadevan M-codes. "
            "Our OCR extraction (reports/icit_extracted_corpus.json) covers this but may "
            "have recognition errors. A clean digital transcription would improve quality."
        ),
        "source":       "Mahadevan (1977) The Indus Script; archive.org digitisation",
        "url":          "https://archive.org/details/mahadevan-1977-the-indus-script",
        "format":       "manual_ocr",
        "tier":         "Tier 5 — primary research corpus",
        "size_estimate": "~14,000+ sign tokens",
        "status":       "requires_manual",
        "fetch_fn":     None,
        "note":         "OCR pipeline already implemented. Run: python -m glossa_lab.experiments.ocr_experiments",
    },

    # ── Comparative / reference corpora ───────────────────────────────────
    {
        "id":           "rongorongo_fischer",
        "name":         "Rongorongo — Fischer (1997) Catalogue",
        "description":  (
            "Easter Island script. 25 surviving objects with ~14,000 glyph tokens. "
            "Completely undeciphered — oral tradition lost after 1862 slave raids. "
            "Polynesian LM available (Hawaiian, Māori) as candidate target. "
            "Tier 5 candidate but corpus per inscription is very small."
        ),
        "source":       "Fischer (1997) RongoRongo: The Easter Island Script",
        "url":          None,
        "format":       "manual_book",
        "tier":         "Tier 5 — Polynesian hypothesis",
        "size_estimate": "~14,000 total glyphs, ~25 inscriptions",
        "status":       "requires_manual",
        "fetch_fn":     None,
        "note":         (
            "Fischer (1997) ISBN 978-0-19-823791-7. Hochenburger database has partial "
            "digitisation. Contact: Steven Roger Fischer for digital access."
        ),
    },
    {
        "id":           "cretan_hieroglyphic_chic",
        "name":         "Cretan Hieroglyphic — CHIC Corpus",
        "description":  (
            "~300 inscribed objects from Crete (c. 2100 BCE). Completely undeciphered. "
            "CHIC publication (Olivier & Godart 1996) is the primary source. "
            "Small corpus (~800–1,200 tokens) — marginal for statistical methods."
        ),
        "source":       "CHIC (Corpus Hieroglyphicarum Inscriptionum Cretae) 1996",
        "url":          None,
        "format":       "manual_book",
        "tier":         "Tier 3 — structural analysis only",
        "size_estimate": "~800–1,200 sign tokens",
        "status":       "requires_manual",
        "fetch_fn":     None,
        "note":         "Too small for reliable statistical decipherment. Use for structural comparison only.",
    },
    {
        "id":           "proto_sinaitic_sass",
        "name":         "Proto-Sinaitic — Sass (1988) Complete Corpus",
        "description":  (
            "Complete scholarly corpus of Proto-Sinaitic inscriptions (Sass 1988). "
            "~40 inscriptions from Serabit el-Khadim and Wadi el-Hol. "
            "Our current corpus (576 tokens) already exceeds the attested material — "
            "this acquisition would validate our corpus quality."
        ),
        "source":       "Sass (1988) The Genesis of the Alphabet",
        "url":          None,
        "format":       "manual_book",
        "tier":         "Tier 1e — floor test",
        "size_estimate": "~400–500 sign tokens (attested)",
        "status":       "requires_manual",
        "fetch_fn":     None,
        "note":         "Our glossa_lab.data.proto_sinaitic corpus already covers this material.",
    },

    # ── Generic URL ────────────────────────────────────────────────────────
    {
        "id":           "custom_url",
        "name":         "Custom URL Corpus",
        "description":  (
            "Download a corpus from any URL. Supports CSV (one sequence per row, "
            "signs space-separated), JSON (array of arrays or objects with 'signs'/'sequence' key), "
            "and plain text (one sequence per line, tokens separated by spaces or commas)."
        ),
        "source":       "User-specified URL",
        "url":          None,
        "format":       "auto_detect",
        "tier":         "Any",
        "size_estimate": "Varies",
        "status":       "available",
        "fetch_fn":     "fetch_custom_url",
        "note":         "Provide url, name, and corpus_type in the action params.",
    },
]


# ── Fetch functions ────────────────────────────────────────────────────────────

_TIMEOUT = 60  # seconds


def _get(url: str, timeout: int = _TIMEOUT) -> bytes:
    """Download URL, return raw bytes. Raises RuntimeError on failure."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}: {url}") from exc
    except Exception as exc:
        raise RuntimeError(f"Download failed ({url}): {exc}") from exc


def fetch_cdli(entry: dict[str, Any]) -> dict[str, Any]:
    """Download from CDLI API and convert to sign sequences.

    CDLI returns JSON with an array of text objects.  Each text has a
    'transliteration' field with lines of cuneiform tokens.
    """
    url = entry.get("url", "")
    if not url:
        raise ValueError("No URL specified for CDLI source")

    raw = _get(url)
    try:
        data = json.loads(raw)
    except Exception as exc:
        raise RuntimeError(f"CDLI JSON parse error: {exc}") from exc

    # CDLI API format: {"results": [{"cdli_num": "...", "transliteration": "..."}, ...]}
    results = data.get("results", [])
    if not results and isinstance(data, list):
        results = data

    inscriptions: list[list[str]] = []
    for item in results:
        translit = item.get("transliteration", "") or item.get("body", "")
        if not translit:
            continue
        # Split into lines, tokenise each line
        for line in translit.replace("\r", "\n").split("\n"):
            tokens = [t.strip() for t in line.split() if t.strip() and not t.startswith("#")]
            if len(tokens) >= 2:
                inscriptions.append(tokens)

    if not inscriptions:
        raise RuntimeError(
            f"CDLI returned 0 inscriptions. "
            f"The API may require a different query. Try fetching manually from {url}"
        )

    n_tokens = sum(len(ins) for ins in inscriptions)
    alphabet = sorted({s for ins in inscriptions for s in ins})
    return {
        "inscriptions": inscriptions,
        "metadata": {
            "source": entry["source"],
            "n_inscriptions": len(inscriptions),
            "n_tokens": n_tokens,
            "alphabet_size": len(alphabet),
            "period": entry.get("period", ""),
        },
    }


def fetch_url_csv(entry: dict[str, Any], url: str | None = None) -> dict[str, Any]:
    """Download a CSV with columns: id, sequence (space-separated signs)."""
    target = url or entry.get("url", "")
    if not target:
        raise ValueError("No URL specified")
    raw = _get(target)
    text = raw.decode("utf-8", errors="replace")
    inscriptions: list[list[str]] = []
    for line in text.splitlines():
        parts = line.split(",", 1)
        seq_str = parts[-1].strip().strip('"')
        tokens = seq_str.split()
        if len(tokens) >= 2:
            inscriptions.append(tokens)
    if not inscriptions:
        raise RuntimeError(f"No sequences found in CSV from {target}")
    n_tokens = sum(len(i) for i in inscriptions)
    return {
        "inscriptions": inscriptions,
        "metadata": {
            "source": entry["source"],
            "n_inscriptions": len(inscriptions),
            "n_tokens": n_tokens,
            "alphabet_size": len({s for i in inscriptions for s in i}),
        },
    }


def fetch_url_json(entry: dict[str, Any], url: str | None = None) -> dict[str, Any]:
    """Download a JSON corpus.

    Accepts:
      - list of lists (direct sequences)
      - list of objects with 'signs', 'sequence', or 'tokens' key
      - {"inscriptions": [...]} or {"data": [...]} wrapper
    """
    target = url or entry.get("url", "")
    if not target:
        raise ValueError("No URL specified")
    raw = _get(target)
    data = json.loads(raw)

    # Unwrap common wrappers
    if isinstance(data, dict):
        data = data.get("inscriptions") or data.get("data") or data.get("texts") or list(data.values())[0]

    inscriptions: list[list[str]] = []
    for item in data:
        if isinstance(item, list):
            tokens = [str(s) for s in item if str(s).strip()]
        elif isinstance(item, dict):
            raw_seq = item.get("signs") or item.get("sequence") or item.get("tokens") or item.get("text", "")
            if isinstance(raw_seq, list):
                tokens = [str(s) for s in raw_seq]
            else:
                tokens = str(raw_seq).split()
        else:
            continue
        if len(tokens) >= 2:
            inscriptions.append(tokens)

    if not inscriptions:
        raise RuntimeError(f"No sequences found in JSON from {target}")
    n_tokens = sum(len(i) for i in inscriptions)
    return {
        "inscriptions": inscriptions,
        "metadata": {
            "source": entry["source"],
            "n_inscriptions": len(inscriptions),
            "n_tokens": n_tokens,
            "alphabet_size": len({s for i in inscriptions for s in i}),
        },
    }


def fetch_oracc(entry: dict[str, Any]) -> dict[str, Any]:
    """Download from ORACC JSON dump.

    ORACC distributes project data as zipped JSON.
    We download and extract a representative sample.
    """
    # ORACC has multiple projects; start with epsd2 (Electronic Pennsylvania
    # Sumerian Dictionary) which is freely downloadable
    url = entry.get("url", "https://github.com/oracc/json-dump/raw/main/epsd2.zip")
    import io
    import zipfile

    raw = _get(url, timeout=120)
    inscriptions: list[list[str]] = []

    try:
        zf = zipfile.ZipFile(io.BytesIO(raw))
        for name in zf.namelist():
            if not name.endswith(".json") or "catalogue" in name:
                continue
            if len(inscriptions) >= 2000:
                break
            try:
                d = json.loads(zf.read(name))
                # ORACC structure: {"cdl": [...nodes...]}
                for node in d.get("cdl", []):
                    tokens = _extract_oracc_tokens(node)
                    if len(tokens) >= 2:
                        inscriptions.append(tokens)
            except Exception:  # noqa: BLE001
                continue
    except zipfile.BadZipFile:
        # Fall back: try plain JSON
        data = json.loads(raw)
        inscriptions = [[str(t) for t in item] for item in data if isinstance(item, list) and len(item) >= 2]

    if not inscriptions:
        raise RuntimeError("ORACC download returned no sequences. Try fetch_url_json with a specific project URL.")

    n_tokens = sum(len(i) for i in inscriptions)
    return {
        "inscriptions": inscriptions,
        "metadata": {
            "source": entry["source"],
            "n_inscriptions": len(inscriptions),
            "n_tokens": n_tokens,
            "alphabet_size": len({s for i in inscriptions for s in i}),
        },
    }


def _extract_oracc_tokens(node: Any, depth: int = 0) -> list[str]:
    """Recursively extract sign/word tokens from an ORACC CDL node."""
    if depth > 8:
        return []
    tokens: list[str] = []
    if isinstance(node, dict):
        if node.get("node") == "c" and node.get("type") == "sentence":
            for child in node.get("cdl", []):
                tokens.extend(_extract_oracc_tokens(child, depth + 1))
        elif node.get("node") == "l":
            # Lemma node — extract normalised form
            f = node.get("f", {})
            form = f.get("form") or f.get("gdl_utf8") or f.get("n", "")
            if form:
                tokens.append(form)
        elif "cdl" in node:
            for child in node.get("cdl", []):
                tokens.extend(_extract_oracc_tokens(child, depth + 1))
    return tokens


def fetch_custom_url(entry: dict[str, Any], url: str | None = None) -> dict[str, Any]:
    """Download from a user-specified URL, auto-detecting format."""
    target = url or entry.get("url", "")
    if not target:
        raise ValueError("Provide a URL in the action params")
    raw = _get(target)

    # Try JSON first
    try:
        return fetch_url_json(entry, url=target)
    except Exception:  # noqa: BLE001
        pass

    # Fall back to CSV/text
    try:
        return fetch_url_csv(entry, url=target)
    except Exception:  # noqa: BLE001
        pass

    # Plain text: one sequence per line
    text = raw.decode("utf-8", errors="replace")
    inscriptions: list[list[str]] = []
    for line in text.splitlines():
        tokens = line.replace(",", " ").split()
        if len(tokens) >= 2:
            inscriptions.append(tokens)
    if not inscriptions:
        raise RuntimeError(f"Could not parse corpus from {target}")
    n_tokens = sum(len(i) for i in inscriptions)
    return {
        "inscriptions": inscriptions,
        "metadata": {
            "source": target,
            "n_inscriptions": len(inscriptions),
            "n_tokens": n_tokens,
            "alphabet_size": len({s for i in inscriptions for s in i}),
        },
    }


# ── Public API ────────────────────────────────────────────────────────────────

_FETCH_FNS = {
    "fetch_cdli":       fetch_cdli,
    "fetch_url_csv":    fetch_url_csv,
    "fetch_url_json":   fetch_url_json,
    "fetch_oracc":      fetch_oracc,
    "fetch_custom_url": fetch_custom_url,
}


def get_catalog() -> list[dict[str, Any]]:
    """Return the full acquirable corpus catalog (metadata only, no URLs)."""
    return [
        {
            "id":           c["id"],
            "name":         c["name"],
            "description":  c["description"],
            "source":       c["source"],
            "tier":         c["tier"],
            "size_estimate": c["size_estimate"],
            "status":       c["status"],
            "note":         c.get("note", ""),
        }
        for c in CATALOG
    ]


def acquire(
    source_id: str,
    custom_url: str | None = None,
) -> dict[str, Any]:
    """Download and convert a corpus by catalog ID.

    Returns:
        {
            "inscriptions": [[sign, ...], ...],
            "metadata": {source, n_inscriptions, n_tokens, alphabet_size, ...},
        }

    Raises ValueError if source_id is not in catalog or status != available.
    Raises RuntimeError on network/parse failure.
    """
    entry = next((c for c in CATALOG if c["id"] == source_id), None)
    if entry is None:
        ids = [c["id"] for c in CATALOG]
        raise ValueError(f"Unknown source_id '{source_id}'. Available: {ids}")

    if entry["status"] != "available":
        raise ValueError(
            f"'{source_id}' requires manual acquisition. "
            f"Note: {entry.get('note', 'See docs/undeciphered_scripts.md')}"
        )

    fn_name = entry.get("fetch_fn")
    if not fn_name:
        raise ValueError(f"No fetch function for '{source_id}'")

    fn = _FETCH_FNS.get(fn_name)
    if fn is None:
        raise ValueError(f"Fetch function '{fn_name}' not found")

    if custom_url:
        return fn(entry, url=custom_url)
    return fn(entry)
