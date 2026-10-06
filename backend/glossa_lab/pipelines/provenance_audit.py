"""Anchor provenance audit library (spec 006, ledger Phase-108).

Assembles per-anchor evidence trails from in-repo sources ONLY,
implements the pre-registered pass-1 classifier, and the Step-3
subset recomputations (coverage / phonotactics / Parpola agreement /
site invariance) reusing the original phases' own machinery.

Taxonomy and rules are pre-registered in
``specs/006-anchor-provenance-audit/spec.md`` — do not change them
here without amending the spec first.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
BACKEND = REPO / "backend"
ANCHORS_PATH = BACKEND / "reports" / "INDUS_FINAL_ANCHORS.json"
HOLDAT_CSV = (REPO / "corpora" / "downloads" / "external_repos"
              / "holdatllc_indus" / "indus_corpus 2.csv")
CROSSWALK_V2 = BACKEND / "glossa_lab" / "data" / "mahadevan_parpola_crosswalk_v2.json"
GLOSSA_LEDGER = REPO / "glossa-indus" / "LEDGER.md"
ROOT_LEDGER = REPO / "LEDGER.md"
CHANGELOG = REPO / "CHANGELOG.md"
CLAIMS_DIR = REPO / "glossa-indus" / "claims" / "extracted_claims"
ARTIFACT_DIRS = [REPO / "reports", BACKEND / "reports", REPO / "outputs",
                 REPO / "glossa-indus" / "reports"]

SIGN_RE = re.compile(r"\bM\d{3}\b")
PHASE_FILE_RE = re.compile(r"phase(\d+)(?:_(\d+))?")

CATEGORIES = [
    "ICONOGRAPHIC", "LITERATURE", "DEDR", "GRAMMAR", "FORMULA",
    "CROSSWALK_CORPUS", "SA_DERIVED", "SA_CONFIRMED_ONLY", "MIXED",
    "UNTRACEABLE",
]

# ── SA lineage (spec 006, enumerated; extended by name evidence) ─────
# role: origin        = SA decipherment run that can first-propose values
#       agreement_only= measures agreement with existing anchors (Phase-77)
#       falsification = SA run against a non-Dravidian target (cannot
#                       confirm Dravidian values)
#       validation    = Phase-107 held-out validation (proposed nothing)
#       contains_sa   = mixed-method bundle including SA (hand-review)
SA_PHASES: dict[int, str] = {
    9: "origin", 34: "origin", 35: "origin", 36: "origin", 37: "origin",
    40: "origin", 41: "origin", 42: "origin", 46: "origin", 47: "origin",
    52: "origin", 55: "origin", 57: "origin", 62: "origin", 63: "origin",
    66: "falsification", 67: "falsification", 73: "origin",
    77: "agreement_only", 93: "origin", 97: "origin", 106: "origin",
    107: "validation", 110: "origin", 116: "origin", 122: "origin",
    168: "origin", 190: "origin", 193: "origin", 199: "contains_sa",
    207: "origin", 213: "origin", 216: "origin", 229: "origin",
    245: "origin", 246: "origin", 257: "origin", 264: "origin",
    265: "origin", 266: "contains_sa", 267: "contains_sa",
    299: "contains_sa", 302: "contains_sa", 303: "contains_sa",
    307: "contains_sa",
}

# Phases whose primary method assigns values by DEDR rebus/etymology.
DEDR_PHASES = {50, 80, 89, 153, 163, 166, 198, 244, 266, 267}
# Positional / morphological grammar phases.
GRAMMAR_PHASES = {64, 69, 74, 98, 112, 117, 132, 133, 154, 155, 170,
                  177, 191, 195, 224, 309, 310, 311, 313, 316}
# Formula-decomposition phases.
FORMULA_PHASES = {53, 59, 68, 76, 84, 143, 148, 227, 228}
# Literature mining / adoption phases.
LITERATURE_PHASES = {72, 75, 88, 94, 125, 152, 157, 158, 159, 160, 164,
                     167, 179, 180, 181, 182, 183, 184, 196, 202, 204,
                     208, 231, 232, 259, 278, 280, 295, 296, 297, 298,
                     317, 320, 321, 322}
# Crosswalk / comparative-corpus phases.
CROSSWALK_PHASES = {28, 51, 56, 65, 71, 85, 96, 123, 186, 190, 206, 209,
                    220, 222, 228, 234, 235, 250, 251, 253, 308}
# Iconographic-identification phases.
ICONOGRAPHIC_PHASES = {27, 28, 101, 124, 143, 185}

PHASE_METHOD: dict[int, str] = {}
for _p in DEDR_PHASES:
    PHASE_METHOD[_p] = "DEDR"
for _p in GRAMMAR_PHASES:
    PHASE_METHOD.setdefault(_p, "GRAMMAR")
for _p in FORMULA_PHASES:
    PHASE_METHOD.setdefault(_p, "FORMULA")
for _p in LITERATURE_PHASES:
    PHASE_METHOD.setdefault(_p, "LITERATURE")
for _p in CROSSWALK_PHASES:
    PHASE_METHOD.setdefault(_p, "CROSSWALK_CORPUS")
for _p in ICONOGRAPHIC_PHASES:
    PHASE_METHOD.setdefault(_p, "ICONOGRAPHIC")
for _p in SA_PHASES:
    PHASE_METHOD[_p] = "SA"


def phase_of_filename(name: str) -> tuple[int, int] | None:
    m = PHASE_FILE_RE.match(name)
    if not m:
        return None
    lo = int(m.group(1))
    hi = int(m.group(2)) if m.group(2) else lo
    return (lo, hi)


def load_anchors() -> dict:
    return json.loads(ANCHORS_PATH.read_text(encoding="utf-8"))


def load_module_by_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# ── Normalisation (shared conventions) ───────────────────────────────

def strip_diacritics(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def first_segment(reading: str) -> str:
    return (reading or "").split("/")[0].strip()


def normalize_reading(reading: str) -> str:
    """Registered match normalisation (spec 006 Step 3c): lowercase,
    NFD-strip diacritics, first segment before '/', strip parenthetical
    glosses, keep letters only."""
    s = first_segment(reading or "")
    s = re.sub(r"\([^)]*\)", " ", s)
    s = strip_diacritics(s.lower())
    s = re.sub(r"[^a-z]", "", s)
    return s


# ── Mention index over artifact files ────────────────────────────────

def build_mention_index(dirs: list[Path] | None = None) -> dict[str, list[dict]]:
    """sign -> [{file, phase_lo, phase_hi, kind}] for every JSON artifact
    in the indexed dirs whose raw text mentions the sign."""
    index: dict[str, list[dict]] = defaultdict(list)
    for d in (dirs or ARTIFACT_DIRS):
        if not d.exists():
            continue
        for f in sorted(d.rglob("*.json")):
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            signs = set(SIGN_RE.findall(text))
            if not signs:
                continue
            ph = phase_of_filename(f.name)
            rel = str(f.relative_to(REPO))
            for s in signs:
                index[s].append({
                    "file": rel,
                    "phase_lo": ph[0] if ph else None,
                    "phase_hi": ph[1] if ph else None,
                    "kind": artifact_kind(f.name),
                })
    return index


def artifact_kind(name: str) -> str:
    n = name.lower()
    if "decipherment_table" in n or n.endswith("_sa.json") or "_sa_" in n \
            or "sa_rerun" in n or "sa_recal" in n or "blocker_sa" in n:
        return "sa_table"
    if "injection" in n:
        return "injection"
    if "upgrade" in n:
        return "upgrade"
    if "proposal" in n:
        return "proposal"
    if "validation" in n or "falsif" in n or "audit" in n:
        return "validation"
    if "mine" in n or "mining" in n:
        return "mine"
    return "other"


def ledger_sections(path: Path) -> list[dict]:
    """Split a markdown ledger into header sections."""
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    sections, cur = [], {"header": "(preamble)", "line": 1, "lines": []}
    for i, ln in enumerate(lines, 1):
        if re.match(r"^#{1,4}\s", ln) and cur["lines"]:
            sections.append(cur)
            cur = {"header": ln.strip(), "line": i, "lines": []}
        elif re.match(r"^#{1,4}\s", ln):
            cur["header"] = ln.strip()
            cur["line"] = i
        cur["lines"].append(ln)
    sections.append(cur)
    for s in sections:
        s["text"] = "\n".join(s.pop("lines"))
    return sections


def sign_ledger_mentions(sign: str, sections: list[dict],
                         source: str) -> list[dict]:
    out = []
    for s in sections:
        if re.search(rf"\b{sign}\b", s["text"]):
            snippet = ""
            for ln in s["text"].splitlines():
                if re.search(rf"\b{sign}\b", ln):
                    snippet = ln.strip()[:240]
                    break
            out.append({"source": source, "header": s["header"],
                        "line": s["line"], "snippet": snippet})
    return out


# ── Structured per-sign extracts ─────────────────────────────────────

def _rows_by_sign(data) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    if isinstance(data, list):
        for r in data:
            if isinstance(r, dict) and isinstance(r.get("sign"), str):
                rows[r["sign"]] = r
    elif isinstance(data, dict):
        for k, v in data.items():
            if SIGN_RE.fullmatch(k) and isinstance(v, dict):
                rows[k] = v
    return rows


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def structured_extracts(sign: str) -> dict:
    """Per-sign rows from the structured provenance artifacts."""
    out: dict = {}
    p52 = load_json(REPO / "reports" / "phase52_full_decipherment_table.json")
    if p52:
        row = _rows_by_sign(p52).get(sign)
        if row:
            out["phase52_sa_table"] = {
                "sa_reading": row.get("sa_reading"),
                "sa_consensus_pct": row.get("sa_consensus_pct"),
                "sa_agrees_confirmed": row.get("sa_agrees_confirmed"),
                "confirmed_reading_then": row.get("confirmed_reading"),
                "citation": "reports/phase52_full_decipherment_table.json",
            }
    p57 = load_json(REPO / "reports" / "phase57_decipherment_table.json")
    if p57:
        row = _rows_by_sign(p57).get(sign)
        if row:
            out["phase57_sa_table"] = {
                "row": {k: row.get(k) for k in list(row)[:8]},
                "citation": "reports/phase57_decipherment_table.json",
            }
    p107 = load_json(REPO / "reports" / "phase107_decipherment_table.json")
    if p107:
        row = _rows_by_sign(p107).get(sign)
        if row:
            out["phase107_sa_table"] = {
                "row": {k: row.get(k) for k in list(row)[:8]},
                "citation": "reports/phase107_decipherment_table.json",
            }
    # Anchor-file dated backups: presence brackets additions/promotions.
    snaps = {}
    for b in sorted((BACKEND / "reports").glob("INDUS_FINAL_ANCHORS.backup_*.json")):
        d = load_json(b)
        if d and sign in d.get("anchors", {}):
            e = d["anchors"][sign]
            snaps[b.name] = {"reading": e.get("reading"),
                             "confidence": e.get("confidence")}
    if snaps:
        out["anchor_snapshots"] = snaps
    # Crosswalk v2.1 entry.
    cw = load_json(CROSSWALK_V2)
    if cw and sign in cw.get("crosswalk", {}):
        out["crosswalk_v2"] = cw["crosswalk"][sign]
    return out


def claims_citing_sign(sign: str) -> list[dict]:
    out = []
    if not CLAIMS_DIR.exists():
        return out
    for f in sorted(CLAIMS_DIR.glob("*.json")):
        d = load_json(f)
        if not d:
            continue
        for c in d.get("claims", []):
            blob = json.dumps(c, ensure_ascii=False)
            if re.search(rf"\b{sign}\b", blob):
                out.append({"claim_id": c.get("claim_id"),
                            "status": c.get("claim_status"),
                            "file": f"glossa-indus/claims/extracted_claims/{f.name}"})
    return out


# ── Trail assembly ───────────────────────────────────────────────────

_ENTRY_TEXT_FIELDS = ("basis", "source", "upgrade_basis", "gloss",
                      "semantic_constraint", "substrate_note")


def entry_text(entry: dict) -> str:
    parts = []
    for k, v in entry.items():
        if isinstance(v, str):
            parts.append(f"{k}: {v}")
        elif isinstance(v, dict):
            parts.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    return "\n".join(parts)


def build_trail(sign: str, entry: dict, mention_index: dict,
                ledger_hits: list[dict]) -> dict:
    mentions = sorted(mention_index.get(sign, []),
                      key=lambda m: (m["phase_lo"] is None, m["phase_lo"] or 0))
    sa_mentions = [m for m in mentions
                   if m["phase_lo"] is not None
                   and any(SA_PHASES.get(p) for p in range(m["phase_lo"], (m["phase_hi"] or m["phase_lo"]) + 1))]
    upgrade_mentions = [m for m in mentions if m["kind"] in ("upgrade", "injection", "proposal")]
    return {
        "sign": sign,
        "reading": entry.get("reading"),
        "confidence": entry.get("confidence"),
        "entry_fields": {k: v for k, v in entry.items()
                         if k not in ("reading", "confidence")},
        "phase_upgraded": entry.get("phase_upgraded"),
        "dedr": entry.get("dedr") or entry.get("dedr_id"),
        "structured": structured_extracts(sign),
        "ledger_mentions": ledger_hits,
        "artifact_mentions": {
            "n_total": len(mentions),
            "earliest": mentions[:8],
            "sa_artifacts": sa_mentions,
            "upgrade_artifacts": upgrade_mentions,
        },
        "claims_citing": claims_citing_sign(sign),
    }


# ── Pass-1 classifier (pre-registered rules; explicit cases only) ────

_SA_TEXT_RE = re.compile(
    r"simulated annealing|\bSA\b|sa[-_ ](?:agree|consensus|z|rerun|recal)|"
    r"annealing", re.I)
_DEDR_TEXT_RE = re.compile(r"\bDEDR\b|dedr", re.I)
_LIT_NAMES_RE = re.compile(
    r"Parpola|Mahadevan|Wells|Fuls|Levit|Laursen|McAlpin|Krishnamurti|"
    r"Witzel|Fairservis|Knorr|Zvelebil", re.I)
_GRAMMAR_TEXT_RE = re.compile(
    r"grammar|positional|suffix|genitive|case marker|morpholog|"
    r"motif-independence|slot", re.I)
_FORMULA_TEXT_RE = re.compile(r"formula", re.I)
_CROSSWALK_TEXT_RE = re.compile(r"crosswalk|CISI|cisi", re.I)
_ICONO_TEXT_RE = re.compile(r"iconograph|depict|pictorial|fish sign|"
                            r"rebus depiction", re.I)


def text_signals(text: str) -> dict[str, bool]:
    return {
        "sa": bool(_SA_TEXT_RE.search(text)),
        "dedr": bool(_DEDR_TEXT_RE.search(text)),
        "literature": bool(_LIT_NAMES_RE.search(text)),
        "grammar": bool(_GRAMMAR_TEXT_RE.search(text)),
        "formula": bool(_FORMULA_TEXT_RE.search(text)),
        "crosswalk": bool(_CROSSWALK_TEXT_RE.search(text)),
        "iconographic": bool(_ICONO_TEXT_RE.search(text)),
    }


_PHASE_MENTION_RE = re.compile(r"[Pp]hase[- ](\d{1,3})")


def structured_signals(trail: dict) -> dict:
    """Method families attested by STRUCTURED signals only: the dedr
    fields, dedr_source, phase mentions in entry text, the source
    field's literature names, and phase_upgraded's method. Keyword
    co-occurrence in a basis string is NOT a structured signal."""
    entry = {"reading": trail["reading"], "confidence": trail["confidence"],
             **trail["entry_fields"]}
    text = entry_text(entry)
    families: set[str] = set()
    if trail.get("dedr") or entry.get("dedr_support") \
            or entry.get("dedr_source"):
        families.add("DEDR")
    mentioned = {int(m.group(1)) for m in _PHASE_MENTION_RE.finditer(text)}
    sa_phases_mentioned = sorted(p for p in mentioned if p in SA_PHASES)
    for p in mentioned:
        m = PHASE_METHOD.get(p)
        if m and m != "SA":
            families.add(m)
    pu = trail.get("phase_upgraded")
    if isinstance(pu, str) and pu.strip().isdigit():
        pu = int(pu.strip())
    if isinstance(pu, int):
        m = PHASE_METHOD.get(pu)
        if m and m != "SA":
            families.add(m)
        if pu in SA_PHASES:
            sa_phases_mentioned.append(pu)
    src = str(entry.get("source") or "")
    if _LIT_NAMES_RE.search(src):
        families.add("LITERATURE")
    return {"families": sorted(families),
            "sa_phases_mentioned": sorted(set(sa_phases_mentioned)),
            "sa_text": bool(_SA_TEXT_RE.search(text))}


def classify_pass1(trail: dict) -> dict:
    """Apply the pre-registered rules where the trail is explicit
    (structured signals only; see structured_signals). Returns
    {category|null, decision: explicit|needs_review, signals,
    components, reasons}. Anything ambiguous returns needs_review —
    pass 1 never guesses."""
    entry = {"reading": trail["reading"], "confidence": trail["confidence"],
             **trail["entry_fields"]}
    text = entry_text(entry)
    ss = structured_signals(trail)
    families = ss["families"]
    sig = text_signals(text)
    reasons: list[str] = []
    components: list[dict] = []
    st = trail["structured"]
    if "phase52_sa_table" in st:
        components.append({"type": "SA", "role": "phase52_table",
                           "citation": "reports/phase52_full_decipherment_table.json"})
    fam_to_cat = {"DEDR": "DEDR", "LITERATURE": "LITERATURE",
                  "GRAMMAR": "GRAMMAR", "FORMULA": "FORMULA",
                  "CROSSWALK_CORPUS": "CROSSWALK_CORPUS",
                  "ICONOGRAPHIC": "ICONOGRAPHIC"}
    for fam in families:
        components.append({"type": fam_to_cat[fam], "role": "structured_signal",
                           "citation": "INDUS_FINAL_ANCHORS.json entry"})
    if ss["sa_phases_mentioned"]:
        reasons.append(f"SA phases mentioned in entry: {ss['sa_phases_mentioned']}")

    # Explicit SA origin: origin language in the entry text AND no
    # non-SA method family attested by structured signals.
    origin_lang = re.search(
        r"(proposed|derived|assigned|first read|reading from|value from)"
        r"[^.]{0,60}(SA|annealing)|(SA|annealing)[^.]{0,40}"
        r"(proposed|derived|assigned)", text, re.I)
    if origin_lang and not families:
        return {"category": "SA_DERIVED", "decision": "explicit",
                "signals": {**sig, **ss}, "components": components,
                "reasons": reasons + ["entry text states SA origin; no "
                                      "non-SA family attested"]}
    # Explicit single-family non-SA origin.
    if not ss["sa_text"] and not ss["sa_phases_mentioned"] \
            and len(families) == 1:
        return {"category": fam_to_cat[families[0]], "decision": "explicit",
                "signals": {**sig, **ss}, "components": components,
                "reasons": reasons + [f"single structured family: {families[0]}"]}
    return {"category": None, "decision": "needs_review",
            "signals": {**sig, **ss}, "components": components,
            "reasons": reasons}


def sa_dependent(rec: dict) -> bool:
    return rec.get("category") in ("SA_DERIVED", "SA_CONFIRMED_ONLY") \
        or bool(rec.get("sa_in_chain"))


# ── Step 3 recomputations ────────────────────────────────────────────

def load_holdat_tokens() -> list[str]:
    with open(HOLDAT_CSV, encoding="utf-8") as f:
        return [(row.get("letters") or "").strip()
                for row in csv.DictReader(f)]


def token_coverage(tokens: list[str], signs: set[str]) -> dict:
    n = len(tokens)
    cov = sum(1 for t in tokens if t in signs)
    return {"n_tokens": n, "n_covered": cov,
            "coverage": round(cov / n, 6) if n else 0.0}


def phonotactic_check(anchor_subset: dict) -> dict:
    """Reuse Phase-58's own machinery (imported by file path)."""
    mod = load_module_by_path(
        "phase58_phonological_gap",
        BACKEND / "scripts" / "phase58_phonological_gap.py")
    freq: Counter = Counter(load_holdat_tokens())
    res = mod.analyze_phoneme_inventory(anchor_subset, freq)
    by_init = res["by_initial_phoneme"]
    total = sum(len(v) for v in by_init.values())
    max_share = (max((len(v) for v in by_init.values()), default=0) / total
                 if total else 0.0)
    return {
        "n_readings_checked": total,
        "n_violations": len(res["phonotactic_violations"]),
        "violations": res["phonotactic_violations"],
        "n_distinct_initials": res["n_distinct_initials"],
        "max_phoneme_share": round(max_share, 4),
        "violation_rate": round(len(res["phonotactic_violations"]) / total, 6)
        if total else 0.0,
    }


def parpola_agreement(signs: set[str], anchors: dict) -> dict:
    cw = load_json(CROSSWALK_V2)["crosswalk"]
    compared, agreed, details = 0, 0, []
    for s in sorted(signs):
        e = cw.get(s)
        if not e or not e.get("reading"):
            continue
        a = normalize_reading(anchors[s].get("reading", ""))
        p = normalize_reading(e["reading"])
        if not a or not p:
            continue
        compared += 1
        ok = a == p
        agreed += ok
        details.append({"sign": s, "anchor_norm": a, "parpola_norm": p,
                        "agree": ok})
    return {"n_compared": compared, "n_agree": agreed,
            "rate": round(agreed / compared, 6) if compared else None,
            "details": details}


def site_invariance(signs: set[str]) -> dict:
    """Phase-69 machinery: its chi2_test + I/M/T counting, eligibility
    rule quoted from phase69_site_stratification.py main(): per sign,
    sites with per-site token total >= 3 enter the table; a sign with
    < 2 such sites is INSUFFICIENT_DATA (counted separately, p=1.0)."""
    mod = load_module_by_path(
        "phase69_site_stratification",
        BACKEND / "scripts" / "phase69_site_stratification.py")
    seals: dict[str, dict] = {}
    with open(HOLDAT_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            c = row["cisi_number"]
            p = int(row.get("position", 0) or 0)
            s = (row.get("letters") or "").strip()
            site = (row.get("site") or "UNKNOWN").strip()
            if c not in seals:
                seals[c] = {"signs": [], "site": site}
            while len(seals[c]["signs"]) <= p:
                seals[c]["signs"].append("")
            seals[c]["signs"][p] = s
    site_ins: dict[str, list] = defaultdict(list)
    for sd in seals.values():
        ss = [s for s in sd["signs"] if s]
        if ss:
            site_ins[sd["site"]].append(ss)
    sites = sorted(site_ins)
    profiles: dict[str, dict] = {}
    for site in sites:
        counts: dict[str, list] = defaultdict(lambda: [0, 0, 0])
        for ins in site_ins[site]:
            n = len(ins)
            for pos, sign in enumerate(ins):
                if sign not in signs:
                    continue
                if pos == 0 and n > 1:
                    counts[sign][0] += 1
                elif pos == n - 1 and n > 1:
                    counts[sign][2] += 1
                else:
                    counts[sign][1] += 1
        profiles[site] = {s: counts[s] for s in signs if sum(counts[s]) > 0}
    n_inv = n_var = n_ins = 0
    variant_signs = []
    for sign in sorted(signs):
        observed = []
        for site in sites:
            cnt = profiles.get(site, {}).get(sign, [0, 0, 0])
            if sum(cnt) >= 3:
                observed.append(cnt)
        if len(observed) < 2:
            n_ins += 1
            continue
        _, p = mod.chi2_test(observed)
        if p >= 0.05:
            n_inv += 1
        else:
            n_var += 1
            variant_signs.append(sign)
    tested = n_inv + n_var
    return {"n_signs": len(signs), "n_tested": tested,
            "n_invariant": n_inv, "n_variant": n_var,
            "n_insufficient_data": n_ins,
            "invariant_rate_of_tested": round(n_inv / tested, 6)
            if tested else None,
            "variant_signs": variant_signs}
