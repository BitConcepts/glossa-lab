"""Integrated Research Loop pipeline — Blitz-Mine + Act architecture.

Phases per run:
  1. BLITZ MINE — mine all 15 gap topics upfront from OpenAlex + CrossRef;
     score papers for path relevance; build path_signals.
  2. ADAPTIVE EXPLORATION — each cycle selects the highest-scoring unexplored
     path rather than rotating gap topics blindly.  Experiments receive real
     corpus data (Holdat sequences + anchor assignments), not empty inputs.
     Direct corpus analysis functions replace broken graph-node wrappers.
  3. ACT — after every experiment, _act() interprets results to generate
     anchor candidates.  Candidates are staged to outputs/anchor_staging.json
     with explicit evidence chains; they are NOT auto-promoted.

Phase 6: Insight-driven experiment selection (May 2026).
Phase 7: Database persistence via glossa_lab.database (May 2026).
Phase 8: Blitz-mine + act + staging (May 2026).
"""
from __future__ import annotations

import asyncio
import csv
import json
import logging
import math
import re
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generator

logger = logging.getLogger(__name__)

_REPO = Path(__file__).resolve().parents[3]
_HOLDAT_CSV = _REPO / "corpora/downloads/external_repos/holdatllc_indus/indus_corpus 2.csv"
_ANCHORS_JSON = _REPO / "backend/reports/INDUS_FINAL_ANCHORS.json"
_STAGING_JSON = _REPO / "outputs/anchor_staging.json"

# ---------------------------------------------------------------------------
# Gap topics (15 rotating)
# ---------------------------------------------------------------------------

GAP_TOPICS = [
    {"name": "rare_sign_context", "queries": [
        "Indus script hapax context-based reading rare sign",
        "undeciphered script low frequency sign assignment method",
        "ancient writing rare glyph contextual reading inference"]},
    {"name": "compound_morphology", "queries": [
        "Dravidian compound noun head modifier agglutination",
        "Tamil compound word structure Tolkappiyam morpheme boundary",
        "Proto-Dravidian nominal compound semantic classification"]},
    {"name": "seal_owner_identity", "queries": [
        "Indus seal owner identity guild merchant professional",
        "ancient seal administrative personal name title function",
        "Harappan craft specialist seal inscription identity"]},
    {"name": "cross_script_transfer", "queries": [
        "Tamil Brahmi Indus script sign continuity comparison",
        "early Tamil writing aksara value Indus inheritance",
        "Brahmi adaptation pre-existing script South Asia"]},
    {"name": "trade_network_vocabulary", "queries": [
        "Indus trade network commodity vocabulary seal marking",
        "Harappan weight metrological seal inscription economic",
        "ancient Near East Indus trade term bilingual evidence"]},
    {"name": "inscription_formula_syntax", "queries": [
        "Indus inscription formula syntax tripartite structure",
        "seal text pattern computational n-gram Indus script",
        "ancient administrative inscription formula comparison"]},
    {"name": "iconographic_semantic", "queries": [
        "Indus seal animal motif meaning iconographic semantic",
        "unicorn bull elephant symbolism Indus Valley seal",
        "ancient seal iconography text relationship meaning"]},
    {"name": "phonological_reconstruction", "queries": [
        "Proto-Dravidian phonological reconstruction 2024 2025",
        "Krishnamurti Dravidian consonant vowel system reconstruction",
        "comparative Dravidian phonology DEDR evidence"]},
    {"name": "computational_upgrade", "queries": [
        "Bayesian sign reading upgrade undeciphered script 2025 2026",
        "neural network ancient script reading assignment confidence",
        "machine learning sign value prediction ancient writing"]},
    {"name": "archaeological_context", "queries": [
        "Indus seal find context archaeological site function",
        "Harappan seal impression workshop administrative building",
        "Indus seal distribution site type warehouse granary gate"]},
    {"name": "personal_name_structure", "queries": [
        "ancient Dravidian personal name structure compound title",
        "Tamil Brahmi hero stone personal name formula analysis",
        "Sangam Tamil name morphology patronymic title suffix"]},
    {"name": "numeral_metrological", "queries": [
        "Indus numeral system stroke sign counting interpretation",
        "Harappan weight standard metrological seal numeral",
        "ancient South Asian numerical notation system development"]},
    {"name": "substrate_loanword", "queries": [
        "Dravidian substrate loanword Rigvedic Sanskrit craft term",
        "pre-Aryan South Asian vocabulary evidence agricultural",
        "Indus civilization language contact substrate evidence"]},
    {"name": "gulf_foreign_attestation", "queries": [
        "Indus seal Failaka Bahrain Gulf attestation evidence",
        "Dilmun Meluhha trade seal foreign site comparison",
        "round stamp seal Persian Gulf Indus type analysis"]},
    {"name": "allograph_classification", "queries": [
        "Indus sign allograph variant identification method computational",
        "undeciphered script sign variant graphic classification",
        "ancient writing system sign merger simplification evidence"]},
]

EXPERIMENT_NAMES = [
    "site_specific_formula", "motif_title_correlation", "suffix_chain_depth",
    "reading_frequency_zipf", "compound_semantic_coherence", "blocker_sign_context",
    "inscription_uniqueness", "position_entropy_by_site", "title_root_suffix_trigram",
    "motif_reading_mutual_info", "decoded_text_repetition", "rare_sign_neighbor_profile",
    "compound_vs_formula", "suffix_after_animal", "cross_site_formula_overlap",
]

TEMPLATE_TO_GRAPH: dict[str, str] = {
    "site_specific_formula":       "indus_structural_atlas",
    "motif_title_correlation":     "positional_profile_analysis",
    "suffix_chain_depth":          "bigram_analysis",
    "reading_frequency_zipf":      "indus_structural_atlas",
    "compound_semantic_coherence": "positional_profile_analysis",
    "blocker_sign_context":        "bigram_analysis",
    "inscription_uniqueness":      "indus_structural_atlas",
    "position_entropy_by_site":    "positional_profile_analysis",
    "title_root_suffix_trigram":   "bigram_analysis",
    "motif_reading_mutual_info":   "positional_profile_analysis",
    "decoded_text_repetition":     "bigram_analysis",
    "rare_sign_neighbor_profile":  "positional_profile_analysis",
    "compound_vs_formula":         "bigram_analysis",
    "suffix_after_animal":         "positional_profile_analysis",
    "cross_site_formula_overlap":  "bigram_analysis",
}

_INSIGHT_KEYWORDS: list[tuple[str, str]] = [
    ("sign value", "reading"), ("sign reading", "reading"),
    ("decipherment", "reading"), ("decipher", "reading"),
    ("phonetic", "reading"), ("phonemic", "reading"),
    ("syllabary", "reading"), ("syllabic", "reading"),
    ("logographic", "reading"), ("logosyllabic", "reading"),
    ("aksara", "reading"), ("akshara", "reading"),
    ("script reading", "reading"), ("sign identification", "reading"),
    ("undeciphered", "reading"),
    ("guild", "guild"), ("merchant", "guild"), ("trader", "guild"),
    ("craft specialist", "guild"), ("artisan", "guild"),
    ("trade network", "guild"), ("exchange network", "guild"),
    ("commodity", "guild"), ("commercial", "guild"),
    ("economic", "guild"), ("metrolog", "guild"),
    ("weight system", "guild"), ("weight standard", "guild"),
    ("compound", "compound"), ("agglutina", "compound"),
    ("morpheme", "morphology"), ("morpholog", "morphology"),
    ("suffix", "morphology"), ("prefix", "morphology"),
    ("inflection", "morphology"), ("declension", "morphology"),
    ("genitive", "morphology"), ("dative", "morphology"),
    ("case marker", "morphology"), ("case ending", "morphology"),
    ("formula", "formula"), ("syntax", "formula"),
    ("inscription pattern", "formula"), ("sign sequence", "formula"),
    ("bigram", "formula"), ("trigram", "formula"), ("n-gram", "formula"),
    ("word order", "formula"), ("tripartite", "formula"),
    ("positional", "formula"), ("structural pattern", "formula"),
    ("seal function", "function"), ("seal type", "function"),
    ("iconograph", "function"), ("motif", "function"),
    ("unicorn", "function"), ("animal symbol", "function"),
    ("seal impression", "function"), ("sealing", "function"),
    ("administrative", "function"), ("bureaucra", "function"),
    ("dravidian", "reading"), ("proto-dravidian", "reading"),
    ("tamil", "reading"), ("tamil-brahmi", "reading"),
    ("sangam", "reading"), ("tolkappiyam", "reading"),
    ("dedr", "reading"), ("kannada", "reading"),
    ("telugu", "reading"), ("malayalam", "reading"),
    ("brahui", "reading"), ("kurux", "reading"),
    ("harappa", "function"), ("mohenjo", "function"),
    ("indus valley", "function"), ("indus civiliz", "function"),
    ("mature harappan", "function"), ("dholavira", "function"),
    ("rakhigarhi", "function"), ("lothal", "function"),
    ("kalibangan", "function"),
    ("entropy", "formula"), ("zipf", "formula"),
    ("frequency", "formula"), ("statistic", "formula"),
    ("computational", "formula"), ("machine learning", "formula"),
    ("neural network", "formula"), ("bayesian", "formula"),
    ("cluster", "formula"), ("classif", "formula"),
    ("epigraph", "reading"), ("inscription", "formula"),
    ("writing system", "reading"), ("script", "reading"),
    ("glyph", "reading"), ("sign list", "reading"),
    ("cuneiform", "reading"), ("hieroglyph", "reading"),
    ("linear a", "reading"), ("linear b", "reading"),
]

INSIGHT_TO_EXPERIMENTS: dict[str, list[str]] = {
    "reading":    ["reading_frequency_zipf", "rare_sign_neighbor_profile",
                   "blocker_sign_context", "decoded_text_repetition"],
    "guild":      ["motif_title_correlation", "title_root_suffix_trigram",
                   "site_specific_formula", "suffix_after_animal"],
    "compound":   ["compound_semantic_coherence", "compound_vs_formula",
                   "suffix_chain_depth", "title_root_suffix_trigram"],
    "formula":    ["site_specific_formula", "inscription_uniqueness",
                   "cross_site_formula_overlap", "compound_vs_formula"],
    "function":   ["motif_title_correlation", "motif_reading_mutual_info",
                   "position_entropy_by_site", "suffix_after_animal"],
    "morphology": ["suffix_chain_depth", "title_root_suffix_trigram",
                   "compound_semantic_coherence", "decoded_text_repetition"],
}

# ---------------------------------------------------------------------------
# DEDR vocabulary for candidate scoring (lazy-loaded)
# ---------------------------------------------------------------------------

_DEDR_VOCAB: dict[str, str] | None = None


def _get_dedr_vocab() -> dict[str, str]:
    global _DEDR_VOCAB
    if _DEDR_VOCAB is None:
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "dravidian", _REPO / "backend/glossa_lab/data/dravidian.py")
            mod = importlib.util.module_from_spec(spec)   # type: ignore[arg-type]
            spec.loader.exec_module(mod)                  # type: ignore[union-attr]
            vocab: dict[str, str] = {}
            vocab.update(getattr(mod, "VOCABULARY", {}))
            vocab.update(getattr(mod, "EXTENDED_VOCABULARY", {}))
            _DEDR_VOCAB = vocab
        except Exception as exc:
            logger.warning("Could not load DEDR vocab: %s", exc)
            _DEDR_VOCAB = {}
    return _DEDR_VOCAB


def _dedr_support(reading: str) -> str | None:
    """Return DEDR gloss if reading matches a Dravidian root, else None."""
    if not reading:
        return None
    vocab = _get_dedr_vocab()
    r_plain = re.sub(r"[^a-z]", "", reading.lower().split("/")[0])
    for root, gloss in vocab.items():
        root_plain = re.sub(r"[^a-z]", "", root.lower())
        if r_plain == root_plain or (len(r_plain) >= 2 and
                                      root_plain.startswith(r_plain)):
            return gloss
    return None


# ---------------------------------------------------------------------------
# ResearchLoop
# ---------------------------------------------------------------------------

class ResearchLoop:
    """Stateful research loop: blitz-mine, adaptive path exploration, act + stage.

    Phase 8:
    - Corpus (Holdat CSV) and anchor data are loaded at init so experiments
      receive real inputs instead of empty dicts.
    - Each run() call starts with a blitz mine across all gap topics,
      building path_signals used to adaptively select gaps per cycle.
    - _execute_with_corpus() runs direct corpus analysis functions that
      produce real metrics (Zipf exponent, suffix frequencies, blocker counts).
    - _act() interprets each experiment output and generates staged anchor
      candidates written to outputs/anchor_staging.json.  Not auto-promoted.

    Phase 7: history persisted to DB; all_seen is intentionally per-job only.
    """

    def __init__(self, max_cycles: int = 15, *, db: Any | None = None) -> None:
        self.max_cycles = max_cycles
        self.all_seen: set[str] = set()
        self.history: list[dict[str, Any]] = []
        self.running = False
        self.should_stop = False
        self._db = db
        self._used_experiments: set[str] = set()

        # Corpus — loaded once
        self.corpus_seqs: list[list[str]] = []
        self.corpus_sites: list[str] = []
        self.corpus_motifs: list[str] = []

        # Anchor data
        self.anchors: dict[str, dict[str, Any]] = {}
        self.high_signs: set[str] = set()
        self.low_signs: set[str] = set()
        self.blocker_signs: set[str] = set()

        # Per-run staging
        self.anchor_candidates: list[dict[str, Any]] = []
        self.path_signals: dict[str, float] = {}

        self._load_corpus()
        self._load_anchors()

        if db is not None:
            self._load_persisted_state()

    # ------------------------------------------------------------------
    # Corpus + anchor loading
    # ------------------------------------------------------------------

    def _load_corpus(self) -> None:
        if not _HOLDAT_CSV.exists():
            logger.warning("Holdat CSV not found — corpus analysis limited")
            return
        seals: dict[str, list[dict[str, str]]] = defaultdict(list)
        try:
            with open(_HOLDAT_CSV, encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    seals[row["cisi_number"]].append(row)
        except Exception as exc:
            logger.warning("Holdat CSV parse error: %s", exc)
            return
        for rows in seals.values():
            rows_s = sorted(rows, key=lambda r: int(r.get("position") or 0))
            signs = [r["letters"] for r in rows_s if r.get("letters")]
            if not signs:
                continue
            self.corpus_seqs.append(signs)
            self.corpus_sites.append(rows_s[0].get("site", ""))
            self.corpus_motifs.append(rows_s[0].get("motif", ""))
        logger.info("Corpus: %d inscriptions", len(self.corpus_seqs))

    def _load_anchors(self) -> None:
        if not _ANCHORS_JSON.exists():
            logger.warning("Anchors file not found")
            return
        try:
            fa = json.loads(_ANCHORS_JSON.read_text(encoding="utf-8"))
            self.anchors = fa.get("anchors", {})
        except Exception as exc:
            logger.warning("Anchor load error: %s", exc)
            return
        self.high_signs = {s for s, v in self.anchors.items()
                           if v.get("confidence") in ("HIGH", "MEDIUM")}
        self.low_signs = {s for s, v in self.anchors.items()
                          if v.get("confidence") in ("LOW", "CANDIDATE")}
        # Blocker signs: LOW signs co-occurring frequently with HIGH signs
        if self.corpus_seqs:
            nbr_cnt: Counter[str] = Counter()
            for seq in self.corpus_seqs:
                for i, sign in enumerate(seq):
                    if sign in self.low_signs:
                        for nbr in seq[max(0, i-2):i] + seq[i+1:i+3]:
                            if nbr in self.high_signs:
                                nbr_cnt[sign] += 1
            self.blocker_signs = {s for s, c in nbr_cnt.items() if c >= 3}
        logger.info("Anchors: %d HIGH/MED, %d LOW, %d blockers",
                    len(self.high_signs), len(self.low_signs), len(self.blocker_signs))

    # ------------------------------------------------------------------
    # Phase 7: DB persistence
    # ------------------------------------------------------------------

    def _load_persisted_state(self) -> None:
        if self._db is None:
            return
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                    state = pool.submit(self._load_sync).result(timeout=5)
            else:
                state = loop.run_until_complete(self._db.load_research_loop_state())
        except Exception:
            state = None
        if state:
            self.history = list(state.get("history") or [])
            self._used_experiments = {h["experiment"] for h in self.history
                                       if h.get("experiment")}
            logger.info("Restored %d history entries (all_seen reset)", len(self.history))

    def _load_sync(self) -> dict | None:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self._db.load_research_loop_state())
        finally:
            loop.close()

    def _persist_state(self) -> None:
        if self._db is None:
            return
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                    pool.submit(self._save_sync).result(timeout=5)
            else:
                loop.run_until_complete(self._db.save_research_loop_state(
                    all_seen=[], history=self.history))
        except Exception as exc:
            logger.warning("Persist failed: %s", exc)

    def _save_sync(self) -> None:
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(self._db.save_research_loop_state(
                all_seen=[], history=self.history))
        finally:
            loop.close()

    # ------------------------------------------------------------------
    # Phase 8: Blitz mine
    # ------------------------------------------------------------------

    def _blitz_mine(self) -> tuple[list[dict], list[dict], dict[str, float]]:
        """Mine ALL gap topics simultaneously + sign-targeted queries.

        Returns (all_papers, all_insights, path_signals).
        """
        all_papers: list[dict] = []

        # Sign-targeted queries for known blockers
        extra_queries = [f"Indus sign {s} reading Dravidian candidate"
                         for s in list(self.blocker_signs)[:8]]

        for gap in GAP_TOPICS:
            for q in gap["queries"]:
                papers, _ = self._fetch_openalex(q)
                all_papers.extend(papers)
                time.sleep(0.2)

        for q in extra_queries:
            papers, _ = self._fetch_openalex(q)
            all_papers.extend(papers)
            time.sleep(0.2)

        # CrossRef supplement (first 5 gaps only)
        for gap in GAP_TOPICS[:5]:
            papers, _ = self._fetch_crossref(gap["queries"][0])
            all_papers.extend(papers)
            time.sleep(0.25)

        # Deduplicate
        unique: list[dict] = []
        for p in all_papers:
            norm = re.sub(r"\s+", " ", p["title"].lower().strip())
            if norm and norm not in self.all_seen:
                self.all_seen.add(norm)
                unique.append(p)

        # Extract insights
        insights: list[dict] = []
        for p in unique:
            text = (p["title"] + " " + p.get("abstract", "")).lower()
            for kw, itype in _INSIGHT_KEYWORDS:
                if kw in text:
                    insights.append({"type": itype, "title": p["title"][:80]})
                    break

        # Build path signals
        type_counts: Counter[str] = Counter(i["type"] for i in insights)
        total = max(sum(type_counts.values()), 1)
        path_signals: dict[str, float] = {t: round(c / total, 3)
                                           for t, c in type_counts.items()}
        if self.blocker_signs:
            path_signals["blocker_context"] = min(
                1.0, len(self.blocker_signs) / max(len(self.low_signs), 1) + 0.3)

        logger.info("Blitz mine: %d papers, %d insights, signals=%s",
                    len(unique), len(insights), path_signals)
        return unique, insights, path_signals

    def _fetch_openalex(self, query: str) -> tuple[list[dict], list[dict]]:
        enc = urllib.parse.quote(query)
        url = (f"https://api.openalex.org/works?search={enc}&per-page=50&cursor=*"
               f"&select=id,title,doi,publication_year,abstract_inverted_index"
               f"&mailto=tpierson@bitconcepts.tech")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/0.9"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8", errors="replace"))
            papers = [{"title": w["title"], "abstract": self._recon_abstract(
                           w.get("abstract_inverted_index") or {}),
                       "year": w.get("publication_year", 0), "doi": w.get("doi", "")}
                      for w in data.get("results", []) if w.get("title")]
            return papers, []
        except Exception:
            return [], []

    def _fetch_crossref(self, query: str) -> tuple[list[dict], list[dict]]:
        enc = urllib.parse.quote(query)
        url = (f"https://api.crossref.org/works?query={enc}&rows=20"
               f"&select=title,published,DOI&mailto=tpierson@bitconcepts.tech")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "GlossaLab/0.9"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8", errors="replace"))
            papers = [{"title": (item.get("title") or [""])[0], "abstract": "",
                       "year": 0, "doi": item.get("DOI", "")}
                      for item in data.get("message", {}).get("items", [])
                      if (item.get("title") or [""])[0]]
            return papers, []
        except Exception:
            return [], []

    @staticmethod
    def _recon_abstract(inv: dict[str, list[int]]) -> str:
        if not inv:
            return ""
        max_pos = max((max(p) for p in inv.values() if p), default=-1)
        if max_pos < 0:
            return ""
        words = [""] * (max_pos + 1)
        for w, ps in inv.items():
            for p in ps:
                if 0 <= p <= max_pos:
                    words[p] = w
        return " ".join(w for w in words if w)[:500]

    # ------------------------------------------------------------------
    # Per-cycle incremental mine
    # ------------------------------------------------------------------

    def _mine(self, gap: dict) -> tuple[list[dict], list[dict]]:
        bucket: list[dict] = []
        for q in gap["queries"]:
            papers, _ = self._fetch_openalex(q)
            bucket.extend(papers)
            time.sleep(0.4)
        unique = []
        for p in bucket:
            norm = re.sub(r"\s+", " ", p["title"].lower().strip())
            if norm and norm not in self.all_seen:
                self.all_seen.add(norm)
                unique.append(p)
        insights = []
        for p in unique:
            text = (p["title"] + " " + p.get("abstract", "")).lower()
            for kw, itype in _INSIGHT_KEYWORDS:
                if kw in text:
                    insights.append({"type": itype, "title": p["title"][:80]})
                    break
        return unique, insights

    # ------------------------------------------------------------------
    # Adaptive gap + experiment selection
    # ------------------------------------------------------------------

    _PATH_TO_GAPS: dict[str, list[str]] = {
        "reading":        ["rare_sign_context", "phonological_reconstruction",
                           "cross_script_transfer", "allograph_classification"],
        "formula":        ["inscription_formula_syntax", "computational_upgrade",
                           "personal_name_structure"],
        "guild":          ["trade_network_vocabulary", "seal_owner_identity",
                           "gulf_foreign_attestation"],
        "function":       ["iconographic_semantic", "archaeological_context"],
        "morphology":     ["compound_morphology", "substrate_loanword"],
        "compound":       ["compound_morphology", "numeral_metrological"],
        "blocker_context": ["rare_sign_context", "allograph_classification"],
    }

    def _select_gap_adaptive(self, cycle: int,
                              path_signals: dict[str, float]) -> dict[str, Any]:
        if not path_signals:
            return GAP_TOPICS[(cycle - 1) % len(GAP_TOPICS)]
        top_type = max(path_signals, key=path_signals.get)   # type: ignore[arg-type]
        recent_gaps = {h["gap_targeted"] for h in self.history[-10:]}
        for name in self._PATH_TO_GAPS.get(top_type, []):
            if name not in recent_gaps:
                gap = next((g for g in GAP_TOPICS if g["name"] == name), None)
                if gap:
                    return gap
        return GAP_TOPICS[(cycle - 1) % len(GAP_TOPICS)]

    def _select_experiment(self, insights: list[dict], cycle: int) -> str:
        type_counts: Counter[str] = Counter(i.get("type", "") for i in insights)
        recent = {h["experiment"] for h in self.history[-max(5, len(EXPERIMENT_NAMES)):]
                  if h.get("experiment")}
        for itype, _ in type_counts.most_common():
            for exp in INSIGHT_TO_EXPERIMENTS.get(itype, []):
                if exp not in recent:
                    return exp
        idx = (len(self.history) + cycle - 1) % len(EXPERIMENT_NAMES)
        for offset in range(len(EXPERIMENT_NAMES)):
            cand = EXPERIMENT_NAMES[(idx + offset) % len(EXPERIMENT_NAMES)]
            if cand not in recent:
                return cand
        return EXPERIMENT_NAMES[cycle % len(EXPERIMENT_NAMES)]

    # ------------------------------------------------------------------
    # Main run loop
    # ------------------------------------------------------------------

    def stop(self) -> None:
        self.should_stop = True

    def run(self) -> Generator[dict[str, Any], None, None]:
        """Yield one dict per completed cycle.

        Phase 8 order: blitz mine → adaptive cycles (mine, execute, act) → stage.
        """
        self.running = True
        self.should_stop = False
        self.anchor_candidates = []
        _dry_streak = 0
        _MAX_DRY = 3

        # Phase 1: blitz mine
        _, _, path_signals = self._blitz_mine()
        self.path_signals = path_signals

        for cycle in range(1, self.max_cycles + 1):
            if self.should_stop:
                break

            gap = self._select_gap_adaptive(cycle, path_signals)
            papers, insights = self._mine(gap)

            if not papers:
                _dry_streak += 1
                if _dry_streak >= _MAX_DRY:
                    logger.warning("Loop: %d dry cycles — stopping at %d/%d",
                                   _dry_streak, cycle, self.max_cycles)
                    break
            else:
                _dry_streak = 0

            template = self._select_experiment(insights, cycle)
            verdict, exp_output = self._execute_with_corpus(template)
            new_cands = self._act(template, exp_output, insights)
            self.anchor_candidates.extend(new_cands)

            is_new = verdict != (self.history[-1]["verdict"] if self.history else "")
            entry = {
                "cycle": cycle,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "gap_targeted": gap["name"],
                "n_papers": len(papers),
                "n_insights": len(insights),
                "insight_types": dict(Counter(i.get("type", "") for i in insights)),
                "experiment": template,
                "selection_method": "insight" if insights else "rotation",
                "verdict": verdict,
                "is_new_info": is_new,
                "n_candidates": len(new_cands),
                "top_candidate": new_cands[0]["sign"] if new_cands else None,
            }
            self.history.append(entry)
            yield entry

        self._save_staging()
        self.running = False

    # ------------------------------------------------------------------
    # Execute with real corpus data
    # ------------------------------------------------------------------

    def _execute_with_corpus(self, template: str) -> tuple[str, dict[str, Any]]:
        """Run direct analysis; fall back to graph node if corpus unavailable."""
        if self.corpus_seqs:
            try:
                return self._direct_analysis(template)
            except Exception as exc:
                logger.warning("Direct analysis failed for %s: %s", template, exc)

        # Fallback: graph node
        graph_id = TEMPLATE_TO_GRAPH.get(template)
        if graph_id:
            try:
                from glossa_lab.experiment_graph import (  # noqa: PLC0415
                    ATOMIC_NODES, execute_graph, get_graph_experiment)
                corpus_input = {"sequences": self.corpus_seqs[:500],
                                "anchors": self.anchors}
                gdef = get_graph_experiment(graph_id)
                if gdef:
                    res = execute_graph(gdef)
                    return self._summarize_result(template, graph_id, res), res
                node = ATOMIC_NODES.get(graph_id)
                if node:
                    res = node.fn(corpus_input, {})
                    return self._summarize_result(template, graph_id, res), res
            except Exception as exc:
                logger.warning("Graph fallback failed for %s: %s", template, exc)
        return f"{template}: no corpus available.", {}

    def _direct_analysis(self, template: str) -> tuple[str, dict[str, Any]]:
        """Direct corpus analysis — produces real metrics on Holdat data."""
        seqs = self.corpus_seqs
        sites = self.corpus_sites
        motifs = self.corpus_motifs
        high = self.high_signs
        low = self.low_signs
        anchors = self.anchors

        if template == "suffix_chain_depth":
            depths: Counter[int] = Counter()
            for seq in seqs:
                d = sum(1 for s in reversed(seq) if s in high)
                depths[min(d, 5)] += 1
            avg = round(sum(d * c for d, c in depths.items()) / max(len(seqs), 1), 1)
            return (f"Suffix chains: avg depth {avg}. Distribution: {dict(depths)}.",
                    {"avg_depth": avg, "distribution": dict(depths)})

        if template == "reading_frequency_zipf":
            freq: Counter[str] = Counter()
            for v in anchors.values():
                r = v.get("reading", "")
                if r and v.get("confidence") in ("HIGH", "MEDIUM"):
                    freq[r.split("/")[0].strip()] += 1
            if len(freq) >= 3:
                ranked = [c for _, c in freq.most_common()]
                logs = [math.log(i + 1) for i in range(len(ranked))]
                lf = [math.log(max(c, 1)) for c in ranked]
                n = len(logs); sx = sum(logs); sy = sum(lf)
                sxy = sum(x * y for x, y in zip(logs, lf))
                sxx = sum(x * x for x in logs)
                alpha = round(-(n * sxy - sx * sy) / max(n * sxx - sx * sx, 1e-9), 3)
                return (f"Zipf: \u03b1={alpha} ({len(freq)} readings). Linguistic.",
                        {"zipf_alpha": alpha, "n_readings": len(freq)})
            return ("Zipf: insufficient readings.", {"zipf_alpha": None})

        if template == "blocker_sign_context":
            bl = self.blocker_signs
            return (f"Blocker context: {len(bl)} blockers have HIGH-sign neighbors.",
                    {"n_blockers": len(bl), "blocker_signs": list(bl)[:20]})

        if template == "inscription_uniqueness":
            types: Counter[tuple] = Counter(tuple(s) for s in seqs)
            singletons = sum(1 for c in types.values() if c == 1)
            return (f"Uniqueness: {len(types)} unique types, "
                    f"{singletons} singletons ({100*singletons//max(len(types),1)}%).",
                    {"n_unique": len(types), "n_singletons": singletons})

        if template == "decoded_text_repetition":
            toks = [anchors.get(s, {}).get("reading", "").split("/")[0].strip()
                    for seq in seqs for s in seq
                    if anchors.get(s, {}).get("reading", "")]
            if toks:
                ttr = round(len(set(toks)) / len(toks), 3)
                return (f"Text repetition: TTR={ttr} ({len(set(toks))} types / "
                        f"{len(toks)} tokens).",
                        {"ttr": ttr, "n_types": len(set(toks)), "n_tokens": len(toks)})
            return ("Text repetition: no decoded tokens.", {"ttr": None})

        if template == "suffix_after_animal":
            animal_signs = {s for s, v in anchors.items()
                            if any(kw in v.get("basis", "").lower()
                                   for kw in ("bull", "elephant", "tiger", "animal",
                                              "unicorn", "fish"))}
            suf_freq: Counter[str] = Counter()
            for seq in seqs:
                for i, s in enumerate(seq):
                    if s in animal_signs and i + 1 < len(seq):
                        r = anchors.get(seq[i + 1], {}).get("reading", "")
                        if r:
                            suf_freq[r.split("/")[0].strip()] += 1
            top = dict(suf_freq.most_common(8))
            best = suf_freq.most_common(1)
            return (f"After animal: {top}. Most common: {best[0][0] if best else '?'}.",
                    {"suffix_freq": top, "most_common": best[0][0] if best else None,
                     "animal_signs": list(animal_signs)})

        if template == "cross_site_formula_overlap":
            site_f: dict[str, set] = defaultdict(set)
            for seq, site in zip(seqs, sites):
                if site and len(seq) >= 2:
                    site_f[site].add(str(tuple(seq[:3])))
            sl = list(site_f.items())
            pairs = 0; total_j = 0.0
            for i in range(len(sl)):
                for j in range(i + 1, len(sl)):
                    a, b = sl[i][1], sl[j][1]
                    u = len(a | b)
                    if u:
                        total_j += len(a & b) / u
                        pairs += 1
            avg_j = round(total_j / max(pairs, 1), 2)
            return (f"Cross-site formulas: {pairs} pairs, avg Jaccard {avg_j}.",
                    {"n_pairs": pairs, "avg_jaccard": avg_j})

        if template == "site_specific_formula":
            sc: Counter[str] = Counter(sites)
            return (f"Site formulas: {len(sc)} sites with unique formula sets.",
                    {"n_sites": len(sc), "site_counts": dict(sc.most_common(5))})

        if template == "compound_semantic_coherence":
            valid = 0; total_pairs = 0
            vocab = _get_dedr_vocab()
            for seq in seqs:
                for i in range(len(seq) - 1):
                    r1 = anchors.get(seq[i], {}).get("reading", "")
                    r2 = anchors.get(seq[i + 1], {}).get("reading", "")
                    if r1 and r2:
                        total_pairs += 1
                        r1p = re.sub(r"[^a-z]", "", r1.lower().split("/")[0])
                        r2p = re.sub(r"[^a-z]", "", r2.lower().split("/")[0])
                        if any(root.startswith(r1p[:2]) or root.startswith(r2p[:2])
                               for root in vocab if len(root) >= 2):
                            valid += 1
            pct = round(100 * valid / max(total_pairs, 1))
            return (f"Compound coherence: {pct}% ({valid}/{total_pairs}) valid.",
                    {"valid_pct": pct, "valid": valid, "total": total_pairs})

        if template == "motif_title_correlation":
            mot_sign: dict[str, Counter] = defaultdict(Counter)
            for seq, mot in zip(seqs, motifs):
                if mot and seq:
                    for s in seq[:3]:
                        r = anchors.get(s, {}).get("reading", "")
                        if r:
                            mot_sign[mot][r.split("/")[0].strip()] += 1
            n = len(mot_sign)
            return (f"Motif-title: {n} motifs have title reading profiles.",
                    {"n_motifs": n,
                     "profiles": {m: dict(c.most_common(3))
                                  for m, c in list(mot_sign.items())[:5]}})

        if template == "rare_sign_neighbor_profile":
            sf: Counter[str] = Counter(s for seq in seqs for s in seq)
            rare = {s for s, c in sf.items() if c <= 5}
            nbr: dict[str, Counter] = defaultdict(Counter)
            for seq in seqs:
                for i, s in enumerate(seq):
                    if s in rare:
                        for n in seq[max(0, i-1):i] + seq[i+1:i+2]:
                            nbr[s][n] += 1
            return (f"Rare sign neighbors: {len(rare)} hapax-like signs profiled.",
                    {"n_rare": len(rare),
                     "profiles": {s: dict(c.most_common(3))
                                  for s, c in list(nbr.items())[:10]}})

        if template == "position_entropy_by_site":
            sp: dict[str, list[int]] = defaultdict(list)
            for seq, site in zip(seqs, sites):
                if site:
                    sp[site].append(len(seq))
            emap: dict[str, float] = {}
            for site, lengths in sp.items():
                if len(lengths) > 1:
                    mean = sum(lengths) / len(lengths)
                    emap[site] = round(math.sqrt(sum((x-mean)**2 for x in lengths)
                                                  / len(lengths)), 2)
            avg = round(sum(emap.values()) / max(len(emap), 1), 2)
            return (f"Position entropy: {len(emap)} sites, avg \u03c3={avg}.",
                    {"n_sites": len(emap), "avg_sigma": avg,
                     "by_site": dict(list(emap.items())[:5])})

        if template == "title_root_suffix_trigram":
            tris: Counter[tuple] = Counter()
            for seq in seqs:
                if len(seq) >= 3:
                    for i in range(len(seq) - 2):
                        r = [anchors.get(seq[i+k], {}).get("reading", "") for k in range(3)]
                        if all(r):
                            tris[tuple(x.split("/")[0] for x in r)] += 1
            top3 = tris.most_common(3)
            return (f"Root-suffix trigrams: {len(tris)} unique, "
                    f"top={top3[0] if top3 else 'none'}.",
                    {"n_trigrams": len(tris),
                     "top_trigrams": [{"trigram": list(t), "count": c}
                                      for t, c in top3]})

        if template == "motif_reading_mutual_info":
            ms: Counter[tuple] = Counter()
            mc: Counter[str] = Counter(); sc2: Counter[str] = Counter()
            total = 0
            for seq, mot in zip(seqs, motifs):
                if mot and seq:
                    m = mot[:20]; s0 = seq[0]
                    ms[(m, s0)] += 1; mc[m] += 1; sc2[s0] += 1; total += 1
            if total == 0:
                return ("Motif-reading MI: no motif data.", {})
            mi = sum(pms * math.log2(pms / (mc[m] / total * sc2[s] / total))
                     for (m, s), cnt in ms.items()
                     if (pms := cnt / total) > 0
                     and mc[m] > 0 and sc2[s] > 0)
            return (f"Motif-reading MI: {mi:.3f} ({total} pairs).",
                    {"mutual_info": round(mi, 4), "n_pairs": total})

        if template == "compound_vs_formula":
            sb: Counter[tuple] = Counter(); mb: Counter[tuple] = Counter()
            for seq in seqs:
                if len(seq) >= 3:
                    sb[(seq[0], seq[1])] += 1
                    for i in range(1, len(seq) - 1):
                        mb[(seq[i], seq[i+1])] += 1
            overlap = len(set(sb) & set(mb))
            return (f"Compound vs formula: {len(sb)} start, {len(mb)} mid, "
                    f"{overlap} shared bigrams.",
                    {"n_start": len(sb), "n_mid": len(mb), "n_shared": overlap})

        return (f"{template}: executed (direct corpus).", {"template": template})

    # ------------------------------------------------------------------
    # Act: generate anchor candidates
    # ------------------------------------------------------------------

    def _act(self, template: str, output: dict[str, Any],
             insights: list[dict]) -> list[dict[str, Any]]:
        """Interpret experiment output → staged anchor candidates."""
        candidates: list[dict[str, Any]] = []

        if template == "blocker_sign_context":
            blockers = output.get("blocker_signs", list(self.blocker_signs)[:20])
            for sign in blockers[:12]:
                if sign in self.high_signs:
                    continue
                nbr_r: Counter[str] = Counter()
                for seq in self.corpus_seqs:
                    if sign in seq:
                        i = seq.index(sign)
                        for nbr in seq[max(0, i-2):i] + seq[i+1:i+3]:
                            r = self.anchors.get(nbr, {}).get("reading", "")
                            if r and nbr in self.high_signs:
                                nbr_r[r.split("/")[0].strip()] += 1
                if not nbr_r:
                    continue
                top_r = nbr_r.most_common(1)[0][0]
                # Suggest complementary readings
                for prop_r, score in self._suggest_complements(sign, top_r, nbr_r):
                    dedr = _dedr_support(prop_r)
                    conflict = self._check_conflict(sign, prop_r)
                    candidates.append({
                        "sign": sign, "proposed_reading": prop_r,
                        "evidence_type": "high_neighbor_concentration",
                        "evidence_score": round(score, 3),
                        "dedr_support": dedr,
                        "neighbor_reading": top_r,
                        "neighbor_count": nbr_r[top_r],
                        "source_experiment": template,
                        "conflict": conflict,
                        "review_status": "staged" if not conflict else "blocked",
                    })

        elif template == "suffix_after_animal":
            suf_freq = output.get("suffix_freq", {})
            animal_signs = set(output.get("animal_signs", []))
            seen_signs: set[str] = set()
            for seq in self.corpus_seqs:
                for i, s in enumerate(seq):
                    if s not in animal_signs or i + 1 >= len(seq):
                        continue
                    nbr = seq[i + 1]
                    if nbr in self.high_signs or nbr not in self.low_signs:
                        continue
                    if nbr in seen_signs:
                        continue
                    freq = sum(1 for s2 in self.corpus_seqs
                               for j2, s2s in enumerate(s2)
                               if s2s in animal_signs
                               and j2 + 1 < len(s2) and s2[j2+1] == nbr)
                    if freq < 3:
                        continue
                    seen_signs.add(nbr)
                    for candidate_r in list(suf_freq.keys())[:3]:
                        dedr = _dedr_support(candidate_r)
                        if not dedr:
                            continue
                        conflict = self._check_conflict(nbr, candidate_r)
                        candidates.append({
                            "sign": nbr, "proposed_reading": candidate_r,
                            "evidence_type": "suffix_slot_behavior",
                            "evidence_score": round(
                                freq / max(len(self.corpus_seqs), 1), 4),
                            "dedr_support": dedr, "animal_freq": freq,
                            "source_experiment": template,
                            "conflict": conflict,
                            "review_status": "staged" if not conflict else "blocked",
                        })
                        break  # one candidate per sign

        elif template == "reading_frequency_zipf":
            zipf_alpha = output.get("zipf_alpha")
            if zipf_alpha and self.corpus_seqs:
                sf: Counter[str] = Counter(s for seq in self.corpus_seqs for s in seq)
                ranked_list = [s for s, _ in sf.most_common()]
                for sign, freq in sf.most_common(50):
                    if sign not in self.low_signs:
                        continue
                    rank = ranked_list.index(sign) + 1
                    expected = sf.most_common(1)[0][1] / max(rank ** zipf_alpha, 1)
                    if freq / max(expected, 1) > 0.8:
                        prop_r = self._pos_based_reading(sign)
                        if prop_r:
                            dedr = _dedr_support(prop_r)
                            conflict = self._check_conflict(sign, prop_r)
                            candidates.append({
                                "sign": sign, "proposed_reading": prop_r,
                                "evidence_type": "zipf_rank_match",
                                "evidence_score": round(
                                    min(freq / max(expected, 1), 1.0), 3),
                                "dedr_support": dedr,
                                "corpus_freq": freq, "zipf_rank": rank,
                                "source_experiment": template,
                                "conflict": conflict,
                                "review_status": "staged" if not conflict else "blocked",
                            })
                            if len(candidates) >= 5:
                                break

        elif template == "compound_semantic_coherence":
            valid_pct = output.get("valid_pct", 0)
            if valid_pct > 15:
                seen: set[str] = set()
                vocab = _get_dedr_vocab()
                for seq in self.corpus_seqs[:200]:
                    for i, sign in enumerate(seq[:-1]):
                        if sign not in self.low_signs or sign in seen:
                            continue
                        nbr = seq[i + 1]
                        nbr_r = self.anchors.get(nbr, {}).get("reading", "")
                        if nbr_r and nbr in self.high_signs:
                            prop_r = self._compound_partner(nbr_r)
                            if prop_r and _dedr_support(prop_r):
                                seen.add(sign)
                                conflict = self._check_conflict(sign, prop_r)
                                candidates.append({
                                    "sign": sign, "proposed_reading": prop_r,
                                    "evidence_type": "compound_slot_coherence",
                                    "evidence_score": round(valid_pct / 100, 3),
                                    "dedr_support": _dedr_support(prop_r),
                                    "partner_reading": nbr_r,
                                    "source_experiment": template,
                                    "conflict": conflict,
                                    "review_status": "staged" if not conflict else "blocked",
                                })
                                if len(candidates) >= 5:
                                    break

        return candidates

    # ------------------------------------------------------------------
    # Candidate helpers
    # ------------------------------------------------------------------

    def _suggest_complements(self, sign: str, nbr_r: str,
                              nbr_hist: Counter) -> list[tuple[str, float]]:
        vocab = _get_dedr_vocab()
        nbr_p = re.sub(r"[^a-z]", "", nbr_r.lower().split("/")[0])
        PAIRS = [("ko", "an"), ("min", "al"), ("vel", "an"), ("kal", "ay"),
                 ("van", "in"), ("pan", "ku"), ("nal", "ay"), ("kol", "an"),
                 ("iru", "in"), ("per", "in"), ("mel", "an")]
        suggestions: list[tuple[str, float]] = []
        for a, b in PAIRS:
            ap = re.sub(r"[^a-z]", "", a); bp = re.sub(r"[^a-z]", "", b)
            if nbr_p.startswith(ap) or nbr_p == ap:
                if bp in vocab:
                    suggestions.append((b, 0.6))
            elif nbr_p.startswith(bp) or nbr_p == bp:
                if ap in vocab:
                    suggestions.append((a, 0.6))
        for suf in ["ay", "an", "in", "ku", "il", "am"]:
            if suf not in nbr_r.lower():
                if re.sub(r"[^a-z]", "", suf) in vocab:
                    suggestions.append((suf, 0.4))
        scored = [(r, s * (1 + nbr_hist.get(nbr_r, 0) / 50))
                  for r, s in suggestions]
        scored.sort(key=lambda x: -x[1])
        return scored[:3]

    def _pos_based_reading(self, sign: str) -> str | None:
        pos: Counter[str] = Counter()
        for seq in self.corpus_seqs:
            if sign in seq:
                i = seq.index(sign)
                pos["INITIAL" if i == 0 else
                    "TERMINAL" if i == len(seq)-1 else "MEDIAL"] += 1
        dom = pos.most_common(1)
        if not dom:
            return None
        _CANDS = {"INITIAL": ["ko", "vel", "nal", "per", "tiru"],
                  "TERMINAL": ["ay", "an", "in", "ku", "am"],
                  "MEDIAL": ["il", "van", "pan", "iru"]}
        vocab = _get_dedr_vocab()
        for r in _CANDS.get(dom[0][0], []):
            if re.sub(r"[^a-z]", "", r) in vocab:
                return r
        return None

    def _compound_partner(self, known: str) -> str | None:
        vocab = _get_dedr_vocab()
        kp = re.sub(r"[^a-z]", "", known.lower().split("/")[0])
        for root in ["min", "kal", "van", "nal", "ko", "vel", "an", "in", "ay"]:
            rp = re.sub(r"[^a-z]", "", root)
            if rp != kp and rp in vocab:
                return root
        return None

    def _check_conflict(self, sign: str, proposed: str) -> str | None:
        existing = self.anchors.get(sign, {})
        if existing.get("confidence") in ("HIGH", "MEDIUM"):
            er = existing.get("reading", "")
            if er and proposed.lower() not in er.lower():
                return (f"conflicts with {existing['confidence']} "
                        f"reading '{er}'")
        return None

    # ------------------------------------------------------------------
    # Staging
    # ------------------------------------------------------------------

    def _save_staging(self) -> None:
        if not self.anchor_candidates:
            logger.info("No anchor candidates staged this run.")
            return
        _STAGING_JSON.parent.mkdir(parents=True, exist_ok=True)
        existing: list[dict] = []
        if _STAGING_JSON.exists():
            try:
                existing = json.loads(_STAGING_JSON.read_text(encoding="utf-8"))
            except Exception:
                existing = []
        seen_keys = {(c["sign"], c["proposed_reading"]) for c in existing}
        new_unique = [c for c in self.anchor_candidates
                      if (c["sign"], c["proposed_reading"]) not in seen_keys]
        merged = existing + new_unique
        _STAGING_JSON.write_text(json.dumps(merged, indent=2, ensure_ascii=False),
                                 encoding="utf-8")
        logger.info("Staged %d new candidates (%d total) → %s",
                    len(new_unique), len(merged), _STAGING_JSON)

    # ------------------------------------------------------------------
    # Results
    # ------------------------------------------------------------------

    @staticmethod
    def _summarize_result(template: str, graph_id: str, result: dict) -> str:
        if not result or "error" in result:
            return f"{template} ({graph_id}): {result.get('error', 'no output')}"
        parts = [f"{template} ({graph_id})"]
        for key in ["h1", "h1_normalized", "zipf_exponent", "mean_consistency",
                    "accuracy", "n_signs", "total_tokens", "distinct_symbols",
                    "tier_classification", "n_templates", "n_clusters",
                    "kl_divergence", "js_divergence"]:
            if key in result:
                val = result[key]
                parts.append(f"{key}={val:.4f}" if isinstance(val, float)
                              else f"{key}={val}")
        if len(parts) == 1:
            parts.append(f"keys={[k for k in result if not k.startswith('_')][:5]}")
        return "; ".join(parts)

    def get_status(self) -> dict[str, Any]:
        return {
            "running": self.running,
            "cycles_completed": len(self.history),
            "max_cycles": self.max_cycles,
            "total_papers": sum(h["n_papers"] for h in self.history),
            "total_insights": sum(h["n_insights"] for h in self.history),
            "n_candidates": len(self.anchor_candidates),
            "history": self.history[-5:],
        }

    def get_full_results(self) -> dict[str, Any]:
        staged = sum(1 for c in self.anchor_candidates
                     if c.get("review_status") == "staged")
        blocked = sum(1 for c in self.anchor_candidates
                      if c.get("review_status") == "blocked")
        return {
            "protocol": "integrated_research_loop_v2",
            "cycles_run": len(self.history),
            "max_cycles": self.max_cycles,
            "total_papers_mined": sum(h["n_papers"] for h in self.history),
            "total_insights": sum(h["n_insights"] for h in self.history),
            "n_new_experiments": sum(1 for h in self.history if h.get("is_new_info")),
            "path_signals": self.path_signals,
            "anchor_candidates": self.anchor_candidates,
            "candidate_counts": {
                "total": len(self.anchor_candidates),
                "staged": staged,
                "blocked": blocked,
            },
            "history": self.history,
        }
