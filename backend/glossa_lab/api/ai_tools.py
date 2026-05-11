"""AI Tools API — advanced AI-powered research assistance.

Endpoints:
  POST /ai/chat                    -- freeform Q&A with optional corpus/experiment context
  POST /ai/decipher                -- Indus sign sequence decipherment assistant
  POST /ai/draft-section           -- experiment result → academic paper paragraph
  POST /ai/hypotheses/generate     -- generate hypotheses from study results
  POST /ai/experiment-chain        -- plan a sequence of experiments for a hypothesis
  POST /ai/synthesize              -- cross-study synthesis
  POST /ai/sign-reading            -- probabilistic sign reading suggestions
"""

from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["ai-tools"])


# ── Action helpers ─────────────────────────────────────────────────────────────

# Primary: %%ACTIONS%%...%%END_ACTIONS%%
# Also match common model mistakes: %%CREATE_*%%, %%RUN_*%%, %%PROPOSED_*%%...%%END_*%%
_ACTION_RE = re.compile(
    r"%%(?:ACTIONS|CREATE_HYPOTHESIS|CREATE_NOTEBOOK|RUN_EXPERIMENT|PROPOSED_ACTIONS)%%"
    r"(.*?)"
    r"%%(?:END_ACTIONS|END_HYPOTHESIS|END_NOTEBOOK|END_EXPERIMENT|END)%%",
    re.DOTALL,
)


# Fields that belong inside params{} but models sometimes emit at top-level
_PARAM_FIELDS = frozenset({
    "title", "statement", "id", "key", "value", "view",
    "pipeline", "script", "name", "content", "query",
})
_TOP_LEVEL_FIELDS = frozenset({"type", "label", "description", "requires_approval"})


def _normalize_action(raw: dict[str, Any]) -> dict[str, Any]:
    """If the model put params at the top level instead of in params{}, fix it.

    Example bad format: {"type":"create_hypothesis", "title":"...", "statement":"..."}
    Fixed format:       {"type":"create_hypothesis", "params":{"title":"...", "statement":"..."}}
    """
    if raw.get("params"):  # already has a populated params dict
        return raw
    elevated: dict[str, Any] = {}
    for key, val in raw.items():
        if key not in _TOP_LEVEL_FIELDS and key != "params":
            if key in _PARAM_FIELDS:
                elevated[key] = val
    if elevated:
        return {**{k: v for k, v in raw.items() if k in _TOP_LEVEL_FIELDS},
                "params": {**raw.get("params", {}), **elevated}}
    return {**raw, "params": raw.get("params") or {}}


def _parse_actions(text: str) -> tuple[str, list[dict[str, Any]]]:
    """Extract %%ACTIONS%%...%%END_ACTIONS%% block from LLM response.

    Handles models that emit multiple separate [...] arrays instead of one.
    Filters to only items that are dicts with a 'type' key (action objects),
    so sign-sequence numbers like [520] in the text never cause parse errors.
    Normalises flat param keys into params{} when models forget the nesting.
    Returns (clean_text, actions_list).
    """
    match = _ACTION_RE.search(text)
    if not match:
        return text, []
    raw = match.group(1).strip()

    def _try_parse(s: str) -> list[dict[str, Any]]:
        """Try json.loads; on failure, strip trailing junk chars and retry."""
        for attempt in (s, re.sub(r"[}\]]+$", "", s).rstrip() + "]"):
            try:
                parsed = json.loads(attempt)
                if isinstance(parsed, list):
                    return [_normalize_action(a) for a in parsed
                            if isinstance(a, dict) and "type" in a]
            except (json.JSONDecodeError, ValueError):
                pass
        return []

    # Collect all [...] array blocks, keep only dict items with 'type'
    arrays = re.findall(r"\[.*?\]", raw, re.DOTALL)
    actions: list[dict[str, Any]] = []
    for arr in arrays:
        actions.extend(_try_parse(arr))

    if not actions:
        # Try the whole block as a single array (with junk-tolerance)
        actions = _try_parse(raw)
        if not actions:
            return text, []
    return text[: match.start()].rstrip(), actions


def _build_settings_context() -> str:
    """Return a compact summary of current AI provider / key status."""
    from glossa_lab.api.settings import get_key  # noqa: PLC0415

    lines = ["\n=== CURRENT SETTINGS ==="]
    providers = [
        ("mistral_api_key",   "Mistral"),
        ("openai_api_key",    "OpenAI"),
        ("anthropic_api_key", "Anthropic"),
        ("google_api_key",    "Google"),
    ]
    for key_name, label in providers:
        val = get_key(key_name)
        status = f"set ({val[:4]}…)" if val else "not set"
        lines.append(f"  {label}: {status}")
    # Ollama installed models
    try:
        import urllib.request  # noqa: PLC0415
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2) as r:
            data = json.loads(r.read())
        names = [m["name"] for m in data.get("models", [])]
        lines.append(f"  Ollama models installed: {', '.join(names) or 'none'}")
    except Exception:  # noqa: BLE001
        lines.append("  Ollama: not reachable")
    lines.append("=== END SETTINGS ===")
    return "\n".join(lines)


_ACTION_SYSTEM_ADDENDUM = """

=== GLOSSA LAB ACTIONS ===
You can propose actions for the user to approve. After your response text, if you want to
propose one or more actions include a block formatted EXACTLY as shown:

%%ACTIONS%%
[{"type": "run_experiment", "params": {"id": "contact_zone_analysis"}, "label": "Run Contact Zone Analysis", "description": "Runs KL divergence on contact-zone vs heartland sites (~30 seconds)."}]
%%END_ACTIONS%%

Available action types — title/statement/id/etc. go INSIDE params{}, not at the top level:
  run_experiment:    {"type":"run_experiment",  "params":{"id":"<exp_id>"},                             "label":"...", "description":"..."}
  run_pipeline:      {"type":"run_pipeline",    "params":{"pipeline":"<id>","params":{},"name":"..."},   "label":"...", "description":"..."}
  change_setting:    {"type":"change_setting",  "params":{"key":"<key>","value":"<val>"},               "label":"...", "description":"..."}
  generate_report:   {"type":"generate_report", "params":{"script":"<script.py>"},                      "label":"...", "description":"..."}
  create_hypothesis: {"type":"create_hypothesis","params":{"title":"...","statement":"..."},            "label":"...", "description":"..."}
  create_notebook:   {"type":"create_notebook", "params":{"title":"...","content":"..."},               "label":"...", "description":"..."}
  open_view:         {"type":"open_view",        "params":{"view":"<view_id>"},                         "label":"...", "description":"..."}
  clear_jobs:        {"type":"clear_jobs",       "params":{},                                            "label":"...", "description":"..."}
  execute_script:    {"type":"execute_script",   "params":{"code":"<python_code>","description":"..."},  "label":"...", "description":"..."}   ← runs Python inline against the corpus
  query_corpus:      {"type":"query_corpus",     "params":{"pattern":["sign_id",...],"position":"any"},  "label":"...", "description":"..."}   ← find inscriptions matching a sign pattern
  compare_results:   {"type":"compare_results",  "params":{"file_a":"<report.json>","file_b":"..."},    "label":"...", "description":"..."}   ← diff two experiment result files
  summarize_session: {"type":"summarize_session","params":{"title":"..."},                              "label":"...", "description":"..."}   ← save this conversation as a notebook entry
  acquire_corpus:    {"type":"acquire_corpus",  "params":{"source_id":"<id>","name":"...","corpus_type":"ancient","url":"<opt>"},  "label":"...", "description":"..."}   ← download & register a corpus from a known source

ACQUIRABLE CORPUS SOURCE IDs (use exactly in acquire_corpus):
  cdli_proto_elamite    — Proto-Elamite ~5k tablets from Iran via CDLI API (available now)
  cdli_sumerian_ur3     — Sumerian Ur III via CDLI API (available now)
  oracc_akkadian        — Akkadian ORACC corpus, ~200k tokens (available now, 30-60s download)
  sigla_linear_a        — Linear A SigLA/TylerLengyel CSV ~7.5k tokens (available now)
  tylerlengyel_linear_a — Linear A JSON fallback (available now)
  custom_url            — Any URL: provide url param; auto-detects CSV/JSON/text format
  meroitic_rilly_expanded — Requires manual book acquisition (contact rilly@cnrs.fr)
  rongorongo_fischer    — Requires Fischer 1997 book
  cretan_hieroglyphic_chic — Requires CHIC 1996 book
  yadav2010_indus       — Requires PLOS ONE supplementary download
  mahadevan1977_concordance — Already covered by OCR pipeline

View IDs for open_view: studies, builder, experiments, corpora, reports, entropy, signs,
  timeline, hypotheses, notebooks, citations, ai-tools, status, pipelines, jobs, settings

Rules:
- Only propose actions when the user explicitly asks you to DO something.
- NEVER propose actions unsolicited.
- Always explain what you're proposing and why, BEFORE the %%ACTIONS%% block.
- One %%ACTIONS%% block per response, containing a JSON array (even for a single action).
- NEVER ask for or suggest API key values in change_setting actions.
=== END GLOSSA LAB ACTIONS ==="""

_REPORTS = Path(__file__).resolve().parent.parent.parent.parent / "reports"
_LEDGER  = Path(__file__).resolve().parent.parent.parent.parent / "LEDGER.md"


def _build_benchmark_context() -> str:
    """Return a compact table of all current decipherment benchmark scores.

    Tries to load from cached report JSON files first.  Falls back to the
    hard-coded session results if reports are not present.
    """
    lines = ["\n=== DECIPHERMENT BENCHMARK SCORES (verified results) ==="]

    # Try to load live scores from report JSON files
    score_files = {
        "beam_benchmark": _REPORTS / "beam_decipher_benchmark.json",
        "transparency":   _REPORTS / "transparency_benchmark.json",
        "prior_ablation": _REPORTS / "prior_ablation_benchmark.json",
        "proto_sinaitic": _REPORTS / "proto_sinaitic_benchmark.json",
        "meroitic":       _REPORTS / "meroitic_benchmark.json",
        "ventris":        _REPORTS / "ventris_validation.json",
    }
    live: dict[str, Any] = {}
    for key, path in score_files.items():
        if path.exists():
            try:
                live[key] = json.loads(path.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                pass

    # ---- Tier 1a: Ugaritic → Hebrew ----------------------------------------
    lines.append("\nTIER 1a — Ugaritic → Hebrew (Snyder 2010 protocol, 30 signs, 945 tokens)")
    if "beam_benchmark" in live:
        b = live["beam_benchmark"]
        sa = b.get("sa_baseline", {})
        best = b.get("best_overall", "?")
        lines.append(f"  SA bijective (25 restarts):        {sa.get('bijective','?')}/30")
        lines.append(f"  SA surjective:                     {sa.get('surjective','?')}/30")
        lines.append(f"  SA + 10 anchors:                   {sa.get('surjective_anchored','?')}/30")
        lines.append(f"  Beam + tight phono + 10 anchors:  {best}/30  ← 100% with full constraints")
    else:
        lines.append("  SA bijective:  0/30 = 0.0%    SA surjective: 2/30 = 6.7%")
        lines.append("  SA + 10 anchors: 12/30 = 40.0%")
        lines.append("  Beam + tight phono groups + 10 anchors: 30/30 = 100.0%  ← BEST")

    # ---- Transparency breakdown --------------------------------------------
    lines.append("\nTRANSPARENCY BENCHMARK (attribution for Tier 1a):")
    if "transparency" in live:
        t = live["transparency"]
        for tier in t.get("tiers", []):
            acc = tier.get("accuracy", "?")
            delta = tier.get("oracle_delta")
            d_str = f"oracle Δ={delta:+.0f}" if delta is not None else "oracle Δ=N/A"
            lines.append(f"  {tier.get('label',''):<40} {acc}/30  {d_str}")
    else:
        lines.append("  T0 freq-rank floor:   0/30 = 0%    (nothing injected)")
        lines.append("  T1 + bigram SA:       2/30 = 6.7%  oracle Δ = -1718  (INVERTED)")
        lines.append("  T2 + ling. priors:    3/30 = 10.0% oracle Δ = -5480  (MORE inverted)")
        lines.append("  T3 + human anchors:  30/30 = 100%  oracle Δ = 0")
        lines.append("  Attribution: algorithm=7%, linguistic priors=3%, human anchors=90%")
    lines.append("  CRITICAL FINDING: The score landscape is INVERTED — the correct")
    lines.append("  Ugaritic→Hebrew mapping scores LOWER than SA's best under ALL")
    lines.append("  statistical scoring methods, including all prior combinations.")
    lines.append("  Hebrew bigram statistics do not separate Ugaritic phoneme assignments.")

    # ---- Prior ablation ----------------------------------------------------
    lines.append("\nPRIOR ABLATION STUDY (Tier 1a, 7 levels):")
    if "prior_ablation" in live:
        pa = live["prior_ablation"]
        floor = pa.get("floor", 0)
        peak  = pa.get("peak", 0)
        lines.append(f"  Floor (no optimizer): {floor}/30   Peak (all priors): {peak}/30")
        for r in pa.get("results", []):
            d = r.get("delta")
            d_str = f"Δ={d:+.0f}" if d is not None else "Δ=N/A"
            lines.append(f"  Level {r['level']}: {r['label']:<44} acc={r['accuracy']}/30  {d_str}  {r['landscape']}")
    else:
        lines.append("  Level 0 (freq-rank seed, no optimizer): 0/30   oracle Δ = N/A")
        lines.append("  Level 1 (+ bigram SA):    2/30  oracle Δ = -1718  FLAT/INV")
        lines.append("  Level 2 (+ positional):   2/30  oracle Δ =  -855  FLAT/INV")
        lines.append("  Level 3 (+ OCP):          1/30  oracle Δ = -1165  FLAT/INV")
        lines.append("  Level 4 (+ word bigrams): 2/30  oracle Δ =  -939  FLAT/INV")
        lines.append("  Level 5 (+ root prior):   2/30  oracle Δ = -7418  FLAT/INV")
        lines.append("  Level 6 (all combined):   3/30  oracle Δ = -5480  FLAT/INV")

    # ---- Tier 1b -----------------------------------------------------------
    lines.append("\nTIER 1b — Ugaritic self-decipherment: 22/22 = 100%")
    lines.append("TIER 1c — Ugaritic → Phoenician: 29/30 = 96.7% (best beam + anchors)")

    # ---- Tier 1e: Proto-Sinaitic -------------------------------------------
    lines.append("\nTIER 1e — Proto-Sinaitic → Hebrew (floor test, 576 tokens, 21/22 signs)")
    if "proto_sinaitic" in live:
        ps = live["proto_sinaitic"]
        sa_d = ps.get("sa", {})
        best = ps.get("best_overall", "?")
        lines.append(f"  SA no anchors: {sa_d.get('no_anchors','?')}/22   SA+10 anchors: {sa_d.get('anchors_10','?')}/22")
        lines.append(f"  Best (beam + phono + anchors): {best}/22")
    else:
        lines.append("  SA no anchors: 1/22 = 4.5%   SA + 10 anchors: 19/22 = 86.4%")
        lines.append("  Beam + tight phono + 10 anchors: 19/22 = 86.4%")
    lines.append("  Interpretation: minimum corpus size (~576 tokens) works with anchors.")

    # ---- Tier 1f: Meroitic -------------------------------------------------
    lines.append("\nTIER 1f — Meroitic → Coptic (graceful degradation test, 551 tokens)")
    if "meroitic" in live:
        mr = live["meroitic"]
        cop = mr.get("coptic", {})
        slf = mr.get("self", {})
        lines.append(f"  Wrong target (Coptic): {cop.get('beam','?')}/19   oracle Δ = {cop.get('oracle_delta','?'):.0f}")
        lines.append(f"  Self-model ceiling:   {slf.get('beam','?')}/19   oracle Δ = {slf.get('oracle_delta','?'):.1f}")
        lines.append(f"  Degradation ratio: {mr.get('degradation_ratio','?')}")
    else:
        lines.append("  Wrong target (Coptic): 1/19 = 5.3%   oracle Δ = -3972  (NEGATIVE → engine rejects wrong LM)")
        lines.append("  Self-model ceiling:   16/19 = 84.2%  oracle Δ = -8.7")
        lines.append("  Degradation ratio: 0.06 — engine correctly detects wrong language hypothesis")

    # ---- Tier 4: Linear B / Ventris ----------------------------------------
    lines.append("\nTIER 4 — Linear B / Ventris (3429 words, 9242 tokens, 69 signs)")
    lines.append("  F1 = 0.148 (vowel rows=0.165, consonant cols=0.131) — PARTIAL recovery")
    lines.append("  Bottleneck: corpus diversity, not size. Scaling curve shows F1 ∝ sqrt(tokens).")
    lines.append("=== END BENCHMARK SCORES ===")
    return "\n".join(lines)


_CODEBASE_API_REFERENCE = """
=== DECIPHERMENT ENGINE API — CORRECT IMPORTS (use exactly these paths) ===
from glossa_lab.pipelines.decipher import (
    LanguageModel,    # bigram/trigram/positional/word-cooccur language model
    decipher,         # Simulated Annealing decipherment
    score_accuracy,   # {correct, total, accuracy, details} given proposed vs gt
    _score_mapping,   # float log-likelihood score for a complete mapping
)
from glossa_lab.pipelines.beam_decipher import (
    beam_decipher,               # beam-search decipherment (preferred over SA)
    UGARITIC_PHONO_GROUPS,       # broad phonological groups (per Segert 1984)
    UGARITIC_PHONO_GROUPS_TIGHT, # tight 1-to-1 groups (achieves 30/30 Tier 1a)
)

KEY SIGNATURES:
  LanguageModel(symbols: list[str], inscriptions: list[list[str]] | None = None)
    attrs: .bigram_freq, .word_bigram_freq, .word_cooccur, .ocp_rate, .ranked,
           .positional, .trigram_freq, .unigram_freq

  decipher(cipher_signs, target_model, seed=42, max_iterations=15000,
           restarts=25, cipher_inscriptions=None, surjective=False,
           use_word_bigrams=False, ocp_weight=0.0, positional_weight=0.005,
           root_prior_weight=0.0, anchors=None) -> {proposed_mapping, score, ...}

  beam_decipher(cipher_signs, target_model, beam_width=200,
                cipher_inscriptions=None, surjective=True, anchors=None,
                phono_groups=None, rank_prior_weight=0.0, max_target_reuse=0,
                ocp_weight=0.0, use_word_bigrams=False, root_prior_weight=0.0)
                -> same shape as decipher() plus {"engine":"beam"}

  score_accuracy(proposed: dict[str,str], answer_key: dict[str,str])
                -> {correct: int, total: int, accuracy: float, details: list}

  _score_mapping(cipher_signs, mapping, target_model, cipher_positional={},
                 use_word_bigrams=False, cipher_inscriptions=None,
                 ocp_weight=0.0, positional_weight=0.005, root_prior_weight=0.0)
                -> float (negative log-likelihood; higher = better fit)

DATA MODULES:
  from glossa_lab.data.old_hebrew import (
      get_corpus_symbols,        # list[str] — flat Hebrew consonant tokens
      get_word_inscriptions,     # list[list[str]] — word-level (4-sign chunks)
      get_corpus_inscriptions,   # list[list[str]] — line-level (verse)
      get_ugaritic_to_hebrew_map,# dict[str, str] — Ug consonant → Heb consonant
  )
  from glossa_lab.data.proto_sinaitic import (
      get_corpus_symbols, get_corpus_inscriptions,
      get_full_answer_key, get_partial_answer_key,  # PS01..PS22 → Hebrew phoneme
  )
  from glossa_lab.data.meroitic import (
      get_corpus_symbols, get_corpus_inscriptions, get_full_answer_key,
      get_coptic_symbols, get_coptic_inscriptions,
  )
  # (add backend/tests/ to sys.path first)
  from corpora.ugaritic import (
      _BAAL_CYCLE_LINES, _SIGN_TO_ID, get_answer_key, get_word_level_inscriptions,
  )

DO NOT use: glossa_lab.utils.corpus, decipherment.SimulatedAnnealing,
            target_lm.score(), scipy, or any other non-existent modules.

WORKING EXAMPLE 1 — SA decipherment with Hebrew target:
  import os, sys
  sys.path.insert(0, "<backend_dir>")
  sys.path.insert(0, "<backend_dir>/tests")
  from glossa_lab.pipelines.decipher import LanguageModel, decipher, score_accuracy, _score_mapping
  from glossa_lab.data.old_hebrew import get_corpus_symbols, get_word_inscriptions, get_ugaritic_to_hebrew_map
  heb_flat = get_corpus_symbols()
  lm = LanguageModel(heb_flat, inscriptions=get_word_inscriptions())
  result = decipher(cipher_signs, lm, seed=42, restarts=25, surjective=True)
  acc = score_accuracy(result["proposed_mapping"], answer_key)
  print(acc["correct"], acc["total"], acc["accuracy"])

WORKING EXAMPLE 2 — Beam search with phonological groups:
  from glossa_lab.pipelines.beam_decipher import beam_decipher, UGARITIC_PHONO_GROUPS_TIGHT
  result = beam_decipher(
      cipher_signs, lm,
      beam_width=50, surjective=True,
      anchors={"U24": "r", "U15": "m", "U06": "h"},
      phono_groups=UGARITIC_PHONO_GROUPS_TIGHT,
  )
  acc = score_accuracy(result["proposed_mapping"], answer_key)

WORKING EXAMPLE 3 — Corpus sub-sampling:
  import random
  def subsample(flat, fraction):
      n = int(len(flat) * fraction)
      return flat[:n]  # sequential slice (preserves bigram structure)
  for frac in [0.25, 0.5, 0.75, 1.0]:
      sub = subsample(cipher_flat, frac)
      lm_sub = LanguageModel(sub)  # rebuild LM on sub-corpus
      res = decipher(sub, lm, seed=42, restarts=10, surjective=True)
      a = score_accuracy(res["proposed_mapping"], gt)
      print(f"{frac:.2f}  {len(sub)} tokens  {a['correct']}/{a['total']}")

=== END API REFERENCE ==="""


def _build_research_context() -> str:
    """Assemble current Indus decipherment research state into a compact context block.

    Loads from reports/sign_expansion.json and the last ~80 lines of LEDGER.md
    so any AI model has the full current state without needing file uploads.
    Also injects verified benchmark scores and the codebase API reference.
    """
    lines: list[str] = []
    lines.append("=== GLOSSA LAB — INDUS SCRIPT DECIPHERMENT RESEARCH CONTEXT ===")

    # ---- Sign assignments from sign_expansion.json --------------------------
    catalog_path = _REPORTS / "sign_expansion.json"
    if catalog_path.exists():
        try:
            data = json.loads(catalog_path.read_text(encoding="utf-8"))
            cov = data.get("token_coverage", {})
            lines.append(
                "\nCorpus: 4,410 inscriptions | 14,213 tokens | 713 sign types"
            )
            lines.append(
                f"Token coverage: {cov.get('pct', '?')}% "
                f"({cov.get('known_tokens','?')}/{cov.get('total_tokens','?')}) "
                "with current assignments"
            )

            # Sign catalog table
            top100 = data.get("top100_catalog", [])
            assigned = [r for r in top100 if r.get("confidence") in ("HIGH","MED","LOW")]
            lines.append("\nSIGN ASSIGNMENTS (current session):")
            lines.append("  Fuls  Count   T    I    M   M77  Conf   Value       Description")
            for r in sorted(assigned, key=lambda x: x.get("rank", 999)):
                lines.append(
                    f"  {r['fuls']:>4}  {r['count']:>5}  "
                    f"{r['t_rate']:.2f}  {r['i_rate']:.2f}  {r['m_rate']:.2f}  "
                    f"{r['best_m77']:>4}  {r['confidence']:>4}  "
                    f"{r['known_value']:>10}  {r.get('m77_desc','')[:20]}"
                )
        except Exception:  # noqa: BLE001
            lines.append("(sign catalog unavailable)")

    # ---- Key findings from decipherment_synthesis.json ----------------------
    synth_path = _REPORTS / "decipherment_synthesis.json"
    if synth_path.exists():
        try:
            d = json.loads(synth_path.read_text(encoding="utf-8"))
            fish = d.get("fish_ranking", [])
            if fish:
                lines.append("\nFISH SIGN RANKING (M77 profile distance):")
                for f in fish:
                    lines.append(
                        f"  Fuls {f['fuls']:>3} → M059 dist={f['m77_dist']:.3f}  "
                        f"M-rate={f['m_rate']:.3f}  n={f['total']}"
                    )
            patts = d.get("readable_inscriptions", {})
            lines.append(
                f"\nReadable inscriptions: "
                f"{patts.get('total_100pct',0)} fully known, "
                f"{patts.get('total_50pct',0)} at >50%"
            )
            top = patts.get("top_patterns", [])[:8]
            if top:
                lines.append("Top patterns:")
                for p in top:
                    lines.append(
                        f"  {' '.join(p['pattern'])} ({p['count']}x) = {p['reading']}"
                    )
        except Exception:  # noqa: BLE001
            pass

    # ---- Last LEDGER entry (open TODOs + next step) -------------------------
    if _LEDGER.exists():
        try:
            ledger_text = _LEDGER.read_text(encoding="utf-8", errors="replace")
            ledger_lines = ledger_text.splitlines()
            # Find the last '## [' heading
            last_entry_idx = max(
                (i for i, ln in enumerate(ledger_lines) if ln.startswith("## [")),
                default=max(0, len(ledger_lines) - 80),
            )
            snippet = "\n".join(ledger_lines[last_entry_idx:][-80:])
            lines.append("\n=== LAST LEDGER ENTRY (current state + open TODOs) ===")
            lines.append(snippet)
        except Exception:  # noqa: BLE001
            pass

    # ---- Benchmark scores + engine API reference (high-value for research tasks)
    lines.append(_build_benchmark_context())
    lines.append(_CODEBASE_API_REFERENCE)

    lines.append("""
=== PYTHON SCRIPTING PATTERNS (for writing runnable analysis scripts) ===
Corpus file: reports/icit_extracted_corpus.json  (relative to backend/)
Load pattern — ALWAYS use this EXACT pattern:
  import json
  from collections import Counter, defaultdict
  from pathlib import Path
  R = Path(__file__).parent.parent / "reports"
  data = json.loads((R / "icit_extracted_corpus.json").read_text("utf-8"))
  inscriptions = [i["sequence"] for i in data["inscriptions"] if i.get("sequence")]
  # inscriptions is a list of lists of STRINGS: [["32","817"], ["400","520","752"], ...]
  # Signs are strings (Fuls numbers), NOT integers.

WRONG load — these patterns are ALL BROKEN, NEVER use them:
  with open(f) as fp: corpus = json.load(fp)  # WRONG: json.load() loads a dict, not a list
  inscriptions = json.load(f)                  # WRONG: same issue
  inscriptions = data["inscriptions"]          # WRONG: items have 'sequence' key, must extract
  for insc in corpus: ...                      # WRONG: corpus is a DICT not a list

Profile computation pattern (always use this):
  total_c    = Counter(s for ins in inscriptions for s in ins)
  terminal_c = Counter(ins[-1] for ins in inscriptions if len(ins) > 1)
  initial_c  = Counter(ins[0]  for ins in inscriptions if len(ins) > 1)
  medial_c   = Counter(s for ins in inscriptions for s in ins[1:-1])
  # t_rate = terminal_c[sign] / total_c[sign]

L1 distance (NO scipy — not installed):
  dist = abs(t1-t2) + abs(i1-i2) + abs(m1-m2)

M77 profiles (inline in scripts as needed):
  {"M088": (0.056,0.333,0.611,"Figure+staff"), "M200": (0.038,0.811,0.151,"Bull head"),
   "M028": (0.044,0.923,0.033,"Arrow"), "M059": (0.047,0.094,0.812,"Fish"),
   "M012": (0.863,0.013,0.125,"Small circle TMK"), "M282": (0.730,0.016,0.254,"Bracket TMK"),
   "M500": (0.125,0.250,0.625,"Plant/tree"), "M342": (0.138,0.241,0.517,"Short stroke"),
   "M086": (0.060,0.360,0.540,"Standing figure"), "M083": (0.059,0.588,0.353,"Kneeling figure"),
   "M029": (0.030,0.101,0.869,"Comb/rake"), "M005": (0.000,0.019,0.981,"Six strokes")}

Script output: save JSON to Path(__file__).parent.parent / "reports" / "<name>.json"

CRITICAL: total_c[sign] returns an INTEGER (count), NOT a tuple.
T/I/M rates MUST be computed from 4 SEPARATE Counter objects.
CORRECT loop pattern:
  for sign in total_c:
      n = total_c[sign]              # int - count of occurrences
      if n < 20: continue
      t = terminal_c[sign] / n       # float - T-rate  (separate Counter!)
      i = initial_c[sign] / n        # float - I-rate  (separate Counter!)
      m = medial_c[sign] / n         # float - M-rate  (separate Counter!)
      # now (t, i, m) is the sign's profile - compare against M77

WRONG (never do this):
  for sign, (t, i, m) in total_c.items():  # BROKEN - Counter values are ints
  t, i, m = total_c[sign]                  # BROKEN - can't unpack int

ALL 12 M77 profiles must always be included in scripts, not just 2.
DO NOT invent T-rates/counts not in context; say 'run a script to obtain this'.

EXPERIMENT CLASS IMPORTS (for running experiments from Python):
  # Each experiment class lives in its own module:
  from glossa_lab.experiments.prior_ablation_benchmark import PriorAblationBenchmark
  from glossa_lab.experiments.transparency_benchmark import TransparencyBenchmark
  from glossa_lab.experiments.beam_decipher_benchmark import BeamDecipherBenchmark
  from glossa_lab.experiments.proto_sinaitic_benchmark import ProtoSinaiticBenchmark
  from glossa_lab.experiments.meroitic_benchmark import MeroiticBenchmark
  from glossa_lab.experiments.sequence_eval_benchmark import SequenceEvalBenchmark
  from glossa_lab.experiments.ventris_validation import VentrisValidation
  # Run any experiment with: result = ExperimentClass().run()
  # WRONG: from experiments import X   ← missing glossa_lab prefix
  # WRONG: from glossa_lab.experiments import X  ← experiments package __init__ not exported
  # CORRECT: from glossa_lab.experiments.<module_name> import <ClassName>

SAVING RESULTS:
  import json; from pathlib import Path
  R = Path(__file__).parent.parent / "reports"
  (R / "result_file.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

BENCHMARK SCORE FACTS (use EXACTLY these, never approximate):
  Tier 1a Ugaritic→Hebrew best: 30/30 = 100.0% (NOT 0.967 — that is Tier 1c)
  Tier 1c Ugaritic→Phoenician: 29/30 = 96.7%
  Tier 1e Proto-Sinaitic→Hebrew: 19/22 = 86.4%
  Tier 1f Meroitic→Coptic: 1/19 = 5.3% (oracle delta = -3972)
  Tier 4 F1: 0.148
  Oracle deltas at each ablation level (Tier 1a): L1=-1718, L2=-855, L3=-1165, L4=-939, L5=-7418, L6=-5480
  ZIPF NOTE: rank×freq should be constant. If rank-1 gives 1200 and rank-10 gives 2800, the
  product is NOT constant (1200 vs 2800) — this is SUPER-ZIPFIAN (faster-than-Zipf decay),
  which is stronger evidence for structured language than pure Zipf.
=== END SCRIPTING PATTERNS ===""")

    lines.append("""
=== DOMAIN KNOWLEDGE: KANDLES SYSTEM ===
The Kandles system (Merkur patent) assigns each phoneme a colour based on
the articulatory/acoustic features of the consonant. It provides an
independent cross-validation channel: if a proposed decipherment maps Indus
sign frequencies to phoneme frequencies, the Kandles colour distribution of
the decoded text should match the target language's Kandles profile.

In the Glossa Lab engine, _kandles_validate(deciphered, target_symbols)
compares the colour-grid of the decoded text against the target corpus and
returns a confidence score in [0, 1].  A high Kandles confidence means the
decoded phoneme distribution is plausible for the target language.

M77 PROFILES — CRITICAL: M77 IDs are strings like "M059", "M029", "M012". They are NOT Fuls sign
numbers (like 690, 740, etc.). Never cite an M77 profile as "sign 690" or similar.
When a question asks about M77 profiles, compute L1 distances against these 12 entries:
  M088 (Figure+staff):  T=0.056  I=0.333  M=0.611  — HIGH MEDIAL
  M200 (Bull head):     T=0.038  I=0.811  M=0.151  — HIGH INITIAL
  M028 (Arrow):         T=0.044  I=0.923  M=0.033  — ALMOST PURE INITIAL
  M059 (Fish):          T=0.047  I=0.094  M=0.812  — HIGH MEDIAL (candidate sentence-ender)
  M012 (Small circle):  T=0.863  I=0.013  M=0.125  — HIGH TERMINAL (TMK candidate)
  M282 (Bracket):       T=0.730  I=0.016  M=0.254  — HIGH TERMINAL (TMK candidate)
  M500 (Plant/tree):    T=0.125  I=0.250  M=0.625  — HIGH MEDIAL
  M342 (Short stroke):  T=0.138  I=0.241  M=0.517  — HIGH MEDIAL
  M086 (Stand. figure): T=0.060  I=0.360  M=0.540  — MEDIAL-BIASED
  M083 (Kneel. figure): T=0.059  I=0.588  M=0.353  — INITIAL-BIASED
  M029 (Comb/rake):     T=0.030  I=0.101  M=0.869  — VERY HIGH MEDIAL
  M005 (Six strokes):   T=0.000  I=0.019  M=0.981  — ALMOST PURE MEDIAL

Sign function categories from positional analysis:
  TERMINAL MARKERS (TMK): high T-rate — likely grammatical suffixes or determinatives
  INITIALS: high I-rate — likely word-initial signs (roots or determinatives)
  MEDIALS: high M-rate — likely syllabic cores or root consonants
  L1 distance formula (no scipy): dist = abs(t1-t2) + abs(i1-i2) + abs(m1-m2)

WORKED M77 EXAMPLE — query sign T=0.04, I=0.09, M=0.87:
  M029 (Comb/rake): L1 = |0.04-0.030| + |0.09-0.101| + |0.87-0.869| = 0.010+0.011+0.001 = 0.022  ← CLOSEST
  M059 (Fish):      L1 = |0.04-0.047| + |0.09-0.094| + |0.87-0.812| = 0.007+0.004+0.058 = 0.069
  M005 (Six strks): L1 = |0.04-0.000| + |0.09-0.019| + |0.87-0.981| = 0.040+0.071+0.111 = 0.222
  NEVER cite "sign 690" or any Fuls sign number as an M77 result.
  ALWAYS use M77 IDs like "M029", "M059", "M088" exactly as listed above.
=== END DOMAIN KNOWLEDGE ===
""")

    lines.append("""
=== GLOSSA LAB RESEARCH TIER HIERARCHY ===
Tier 1a: Ugaritic → Hebrew (cross-language NW Semitic, 30 signs)
         The CORE benchmark. Tests if Hebrew bigrams can guide Ugaritic decipherment.
         KEY RESULT: Statistical landscape inverted. Works ONLY with phono groups + anchors.
Tier 1b: Ugaritic → Ugaritic (self-decipherment)
         Ceiling test: 22/22 = 100%. Confirms the engine works with correct target LM.
Tier 1c: Ugaritic → Phoenician (cross-language NW Semitic, different from Hebrew)
         Sister-language test: V→E (not G) differs. 29/30 = 96.7%.
Tier 1e: Proto-Sinaitic → Hebrew (floor test, minimal corpus ~576 tokens)
         Minimum corpus size validation. Works with anchors (19/22 = 86.4%).
Tier 1f: Meroitic → Coptic (graceful degradation, WRONG target language)
         Tests if engine rejects wrong hypotheses. Oracle delta -3972 = YES.
Tier 3:  Sumerian / Oracle Bone classification (logographic detection)
         Tests whether the engine can identify sign FUNCTION categories.
Tier 4:  Linear B / Ventris grid recovery (syllabary structure)
         Tests syllable-grid reconstruction. F1=0.148. Bottleneck: corpus diversity.
Tier 5:  Indus Script → Dravidian (the research frontier)
         No known answer key. Z-score tests whether Dravidian provides any signal.
         Current: Dravidian leads but Z-scores do not cross significance threshold.
=== END TIER HIERARCHY ===
""")

    # ---- Acquirable corpus catalog -------------------------------------------
    try:
        from glossa_lab.corpus_acquirer import get_catalog as _get_cat  # noqa: PLC0415
        cat = _get_cat()
        available = [c for c in cat if c["status"] == "available"]
        manual    = [c for c in cat if c["status"] != "available"]
        lines.append("\n=== ACQUIRABLE CORPUS CATALOG (use with acquire_corpus action) ===")
        lines.append("AVAILABLE NOW (downloadable automatically):")
        for c in available:
            lines.append(f"  {c['id']:<30} {c['name']} | {c['tier']} | {c['size_estimate']}")
        lines.append("REQUIRES MANUAL ACQUISITION:")
        for c in manual:
            lines.append(f"  {c['id']:<30} {c['name']} | {c['note'][:80]}")
        lines.append("=== END CORPUS CATALOG ===")
    except Exception:  # noqa: BLE001
        pass

    lines.append("\n=== END RESEARCH CONTEXT ===")
    lines.append(
        "You are acting as a decipherment research collaborator. "
        "Reason from the evidence above ONLY. Do not invent T-rates, I-rates, or counts "
        "that are not in context; if data is missing say so and recommend running a script. "
        "When writing Python code: copy imports VERBATIM from WORKING EXAMPLES in the "
        "DECIPHERMENT ENGINE API section — never use any other module paths. "
        "When citing benchmark numbers, use the DECIPHERMENT BENCHMARK SCORES table above EXACTLY. "
        "Propose hypotheses with explicit confidence levels (HIGH/MED/LOW). "
        "Reference Fuls sign numbers (e.g. 'sign 817'). "
        "Give thorough, complete answers — write your FULL response text FIRST, "
        "then append the %%ACTIONS%% block at the very end if needed. "
        "Never truncate a response by inserting %%ACTIONS%% mid-answer."
    )
    return "\n".join(lines)


# ── Request models ─────────────────────────────────────────────────────────────


class ChatMessage(BaseModel):
    role: str = "user"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    context_type: str | None = None  # "corpus" | "experiment" | "study" | "research"
    context_id: str | None = None
    stream: bool = False
    provider: str | None = None   # model picker override: "ollama"|"mistral"|"openai"|"anthropic"
    model: str | None = None      # model name override


class ActionExecuteRequest(BaseModel):
    type: str
    params: dict[str, Any] = {}


class DecipherRequest(BaseModel):
    sign_sequence: list[str]
    theory: str = "linguistic"  # linguistic | logo-syllabic | acrophonic | dravidian
    corpus_id: str | None = None


class DraftSectionRequest(BaseModel):
    experiment_id: str
    section_type: str = "results"  # abstract | introduction | methods | results | discussion
    result_json: dict[str, Any] = {}


class HypothesisGenRequest(BaseModel):
    study_id: str | None = None
    context: str = ""  # free-form context if no study_id


class ExperimentChainRequest(BaseModel):
    hypothesis: str
    available_experiment_ids: list[str] = []


class SynthesisRequest(BaseModel):
    study_ids: list[str]
    question: str = ""


class SignReadingRequest(BaseModel):
    sign_ids: list[str]  # e.g. ["740", "400", "700"]
    theory: str = "dravidian"
    context: str = ""


# ── Shared helper ─────────────────────────────────────────────────────────────


def _build_system_prompt(
    base: str,
    context_block: str,
    settings_ctx: str,
    action_addendum: str,
    style: str,
) -> str:
    """Assemble the system prompt in the style best suited to the model."""
    if style == "xml":
        # Claude responds well to explicit XML structure
        return (
            f"<role>\n{base}\n</role>\n"
            f"<context>{context_block}{settings_ctx}\n</context>\n"
            "<instructions>\n"
            "Be concise, precise, and scientifically rigorous. "
            "Cite specific numbers. Say so when uncertain."
            f"\n{action_addendum}\n</instructions>"
        )
    if style == "sections":
        # Mistral / Qwen / Llama prefer clear section headers
        return (
            f"### Role\n{base}\n\n"
            f"### Context{context_block}{settings_ctx}\n\n"
            "### Instructions\n"
            "Be concise, precise, and scientifically rigorous. "
            "Cite specific numbers. Say so when uncertain."
            f"{action_addendum}"
        )
    # "plain" — single paragraph (smallest models, o1)
    return (
        f"{base}"
        f"{context_block}"
        f"{settings_ctx}\n\n"
        "Be concise, precise, and scientifically rigorous. "
        "Cite specific numbers. When uncertain, say so."
        f"{action_addendum}"
    )


async def _run_llm(
    messages: list[dict[str, str]],
    json_mode: bool = False,
    provider: str | None = None,
    model: str | None = None,
    bucket: str = "conversational",
) -> str:
    from glossa_lab.ai_utils import call_llm  # noqa: PLC0415
    from glossa_lab.model_profiles import get_profile, trim_history  # noqa: PLC0415

    profile = get_profile(model)
    # Trim history to model's context budget (chars = tokens * 4)
    messages = trim_history(messages, budget_chars=profile["ctx_budget"] * 4)

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: call_llm(
            messages,
            bucket=bucket,
            json_mode=json_mode,
            max_tokens=profile["max_tokens"],
            temperature=profile["temperature"],
            provider_override=provider,
            model_override=model,
        ),
    )


# ── Endpoints ──────────────────────────────────────────────────────────────────


@router.post("/chat")
async def ai_chat(body: ChatRequest) -> dict[str, Any]:
    """Conversational AI with optional corpus / experiment / study context.

    Pass context_type + context_id to inject relevant data into the system prompt.
    """
    from glossa_lab.database import get_db
    from glossa_lab.experiment_base import get_experiment

    context_block = ""

    # ── Research context: load full decipherment state from reports + LEDGER ──
    if body.context_type == "research":
        context_block = "\n\n" + _build_research_context()
        # Augment with RAG-retrieved chunks relevant to the latest user message
        try:
            from glossa_lab.rag import query as rag_query, index_size  # noqa: PLC0415
            last_user = next(
                (m.content for m in reversed(body.messages) if m.role == "user"), ""
            )
            if last_user and index_size() > 0:
                rag_chunks = rag_query(last_user, top_k=3)
                if rag_chunks:
                    rag_section = "\n\n=== RETRIEVED RESEARCH ARTIFACTS (RAG) ==="
                    for ch in rag_chunks:
                        rag_section += f"\n[{ch['source_type']}:{ch['source']} score={ch['score']:.2f}]\n{ch['text'][:400]}"
                    rag_section += "\n=== END RAG ==="
                    context_block += rag_section
        except Exception:  # noqa: BLE001
            pass

    elif body.context_type and body.context_id:
        db = get_db()
        if db:
            if body.context_type == "corpus":
                text = await db.get_text(body.context_id)
                if text:
                    from collections import Counter

                    freq = Counter(text["content"])
                    top10 = ", ".join(f"{t}={c}" for t, c in freq.most_common(10))
                    context_block = (
                        f"\n\n[Active corpus: {text['name']} | "
                        f"{len(text['content'])} tokens | alphabet {text['alphabet_size']} | "
                        f"top tokens: {top10}]"
                    )
            elif body.context_type == "study":
                study = await db.get_study(body.context_id)
                if study:
                    nodes_in_study = study.get('graph', {}).get('nodes', [])
                    context_block = (
                        f"\n\n[Active study: {study['name']} — {study.get('description', '')} | "
                        f"{len(nodes_in_study)} nodes]"
                    )
                    # Augment with RAG chunks relevant to the study description
                    try:
                        from glossa_lab.rag import query as rag_query, index_size  # noqa: PLC0415
                        if index_size() > 0:
                            study_query = study.get('description', '') or study['name']
                            rag_chunks = rag_query(study_query, top_k=2)
                            if rag_chunks:
                                context_block += "\n\n[Related artifacts: " + " | ".join(
                                    f"{c['source']} ({c['score']:.2f})"
                                    for c in rag_chunks
                                ) + "]"  
                    except Exception:  # noqa: BLE001
                        pass
        if body.context_type == "experiment" and body.context_id:
            cls = get_experiment(body.context_id)
            if cls:
                m = cls.to_dict()
                context_block = (
                    f"\n\n[Active experiment: {m['name']} ({m['category']}) — {m['description']}]"
                )

    from glossa_lab.model_profiles import get_profile  # noqa: PLC0415
    from glossa_lab.experiment_base import discover_experiments  # noqa: PLC0415

    profile = get_profile(body.model)
    settings_ctx = _build_settings_context()

    # Build action addendum with live experiment IDs so the AI never hallucinates IDs.
    # Use list_graph_experiments() directly (reads JSON files, no Python registry cache)
    # so this is immune to the discover_experiments() cache-invalidation race.
    if profile["action_capable"]:
        try:
            from glossa_lab.experiment_graph import list_graph_experiments  # noqa: PLC0415
            graph_ids = sorted(e["id"] for e in list_graph_experiments())
            exp_id_note = (
                f"\n\nREGISTERED EXPERIMENT IDs (use EXACTLY these in run_experiment actions): "
                f"{', '.join(graph_ids)}"
            )
            action_addendum = _ACTION_SYSTEM_ADDENDUM + exp_id_note
        except Exception:  # noqa: BLE001
            action_addendum = _ACTION_SYSTEM_ADDENDUM
    else:
        action_addendum = ""

    base_role = (
        "You are Glossa, an expert AI research assistant for Glossa Lab — a computational "
        "linguistics platform studying the Indus Script. You have deep knowledge of "
        "information theory, computational linguistics, ancient scripts, and the specific "
        "methodology used at Glossa Lab (entropy analysis, n-gram statistics, Zipf law, "
        "comparative linguistics with Sumerian, Proto-Elamite, Luwian, Linear A, etc.)."
    )

    system = _build_system_prompt(
        base=base_role,
        context_block=context_block,
        settings_ctx=settings_ctx,
        action_addendum=action_addendum,
        style=profile["prompt_style"],
    )

    messages = [{"role": "system", "content": system}] + [
        {"role": m.role, "content": m.content} for m in body.messages
    ]

    try:
        raw_reply = await _run_llm(messages, provider=body.provider, model=body.model)
        clean_reply, actions = _parse_actions(raw_reply)
        return {
            "role": "assistant",
            "content": clean_reply,
            "actions": actions,
            "context_type": body.context_type,
            "context_id": body.context_id,
        }
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/execute-action")
async def execute_action(body: ActionExecuteRequest) -> dict[str, Any]:
    """Execute an AI-proposed action that the user has approved."""
    t = body.type
    p = body.params

    # ── Safety: unknown types and malformed requests return 400, not 500 ──────
    # Wrap entire handler so unhandled exceptions surface as descriptive errors.
    try:
        return await _execute_action_inner(t, p)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        import logging as _log
        _log.getLogger("glossa_lab").error("execute-action failed",
                                            extra={"type": t, "error": str(exc)})
        raise HTTPException(500, f"Action '{t}' raised an unexpected error: {exc}") from exc


async def _execute_action_inner(t: str, p: dict) -> dict[str, Any]:  # noqa: PLR0912,PLR0915
    """Inner handler for execute_action — raises HTTPException on all errors."""
    from typing import Any as _Any  # already imported above but needed for linter

    # ── open_view — client-side navigation, nothing to do on server ────────────
    if t == "open_view":
        return {"ok": True, "navigate": p.get("view"), "summary": f"Navigating to {p.get('view', '?')}"}

    # ── run_experiment ─────────────────────────────────────────────────────────────────
    if t == "run_experiment":
        from glossa_lab.experiment_base import get_experiment  # noqa: PLC0415
        from glossa_lab.experiment_graph import (  # noqa: PLC0415
            get_graph_experiment, list_graph_experiments, register_graph_experiments,
        )
        exp_id = p.get("id", "")
        # Always re-register graph experiments — the Python registry cache may have been
        # invalidated by auto_migrate_hardcoded_experiments() at startup.
        register_graph_experiments()
        cls = get_experiment(exp_id)
        if cls is None:
            # ID not in Python registry. Check if it exists as a raw graph file.
            gdata = get_graph_experiment(exp_id)
            if gdata is None:
                all_ids = sorted(e["id"] for e in list_graph_experiments())
                raise HTTPException(
                    404,
                    f"Experiment '{exp_id}' not found. "
                    f"Valid IDs are: {', '.join(all_ids[:40])}",
                )
            # It's a valid graph experiment — run it via the engine pipeline (creates a job)
            from glossa_lab.database import get_db  # noqa: PLC0415
            db = get_db()
            if db is None:
                raise HTTPException(503, "Database unavailable")
            job = await db.create_job(
                name=f"{gdata.get('name', exp_id)}  [AI]",
                pipeline="exp_run",
                params={"exp_id": exp_id, "source": "ai_action"},
                created_at=__import__("datetime").datetime.utcnow().isoformat(),
            )
            return {
                "ok": True,
                "summary": f"Graph experiment '{exp_id}' queued (job {job['id']}).",
                "job_id": job["id"],
            }
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: cls().run())
        n = len(result) if isinstance(result, dict) else "?"
        return {"ok": True, "summary": f"Experiment '{exp_id}' completed ({n} result keys).", "result": result}

    # ── run_pipeline ────────────────────────────────────────────────────────────
    if t == "run_pipeline":
        from glossa_lab.database import get_db  # noqa: PLC0415
        db = get_db()
        if db is None:
            raise HTTPException(503, "Database unavailable")
        job = await db.create_job({
            "name": p.get("name", p.get("pipeline", "ai-job")),
            "pipeline": p.get("pipeline", ""),
            "params": p.get("params", {}),
            "status": "pending",
        })
        return {"ok": True, "summary": f"Pipeline job queued (id={job['id']}).", "job_id": job["id"]}

    # ── change_setting ──────────────────────────────────────────────────────────
    if t == "change_setting":
        from glossa_lab.api.settings import set_key  # noqa: PLC0415
        key = p.get("key", "")
        value = p.get("value", "")
        if not key:
            raise HTTPException(400, "Missing setting key")
        set_key(key, str(value))
        return {"ok": True, "summary": f"Setting '{key}' updated."}

    # ── generate_report ──────────────────────────────────────────────────────────────
    if t == "generate_report":
        script = p.get("script", "")
        url = p.get("url", "")
        if not script and not url:
            raise HTTPException(400, "Missing script name or URL")

        # If a URL is provided (e.g. arxiv paper), fetch and cache it instead of running a script
        if url or (script and "fetch" in script.lower() and "paper" in script.lower()):
            target_url = url or p.get("paper_url", "")
            if not target_url:
                return {"ok": False, "summary": "Paper fetching requested but no URL provided. "
                        "Use the Discovery → Fetch feature or provide a direct URL."}
            import urllib.request  # noqa: PLC0415
            try:
                req = urllib.request.Request(target_url, headers={"User-Agent": "GlossaLab/1.0"})
                with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
                    content_type = resp.headers.get("Content-Type", "")
                    size = int(resp.headers.get("Content-Length", 0))
                return {
                    "ok": True,
                    "summary": f"Paper accessible at {target_url} ({content_type}, ~{size//1024}KB). "
                               f"Use Discovery → Fetch to ingest, or download manually.",
                    "url": target_url,
                    "content_type": content_type,
                }
            except Exception as exc:  # noqa: BLE001
                return {"ok": False, "summary": f"Could not reach {target_url}: {exc}"}

        import subprocess  # noqa: PLC0415, S404
        import sys
        backend_dir = Path(__file__).resolve().parent.parent.parent
        script_path = backend_dir / script
        if not script_path.exists():
            # Try scripts/ subdirectory as fallback
            script_path = backend_dir / "scripts" / script
        if not script_path.exists():
            return {
                "ok": False,
                "summary": f"Script '{script}' not found. Use run_experiment with a valid "
                           f"experiment ID, or provide a URL for paper fetching.",
            }
        proc = subprocess.run(  # noqa: S603
            [sys.executable, str(script_path)],
            capture_output=True, text=True, timeout=300,
        )
        ok = proc.returncode == 0
        return {"ok": ok, "summary": f"Report script finished (exit {proc.returncode}).",
                "stdout": proc.stdout[-500:], "stderr": proc.stderr[-200:]}

    # ── create_hypothesis ───────────────────────────────────────────────────────
    if t == "create_hypothesis":
        from glossa_lab.database import get_db  # noqa: PLC0415
        db = get_db()
        if db is None:
            raise HTTPException(503, "Database unavailable")
        h = await db.create_hypothesis({
            "title": p.get("title", "AI-generated hypothesis"),
            "statement": p.get("statement", ""),
            "status": "active", "evidence": [], "study_ids": [], "exp_ids": [],
        })
        return {"ok": True, "summary": f"Hypothesis '{h['title']}' created.", "id": h["id"]}

    # ── create_notebook ─────────────────────────────────────────────────────────
    if t == "create_notebook":
        from glossa_lab.database import get_db  # noqa: PLC0415
        db = get_db()
        if db is None:
            raise HTTPException(503, "Database unavailable")
        nb = await db.create_notebook({
            "title": p.get("title", "AI note"),
            "content": p.get("content", ""),
            "study_id": None, "tags": ["ai-generated"],
        })
        return {"ok": True, "summary": f"Notebook entry '{nb['title']}' created.", "id": nb["id"]}

    # ── clear_jobs ──────────────────────────────────────────────────────────────
    if t == "clear_jobs":
        from glossa_lab.database import get_db  # noqa: PLC0415
        db = get_db()
        if db is None:
            raise HTTPException(503, "Database unavailable")
        n = await db.clear_jobs()
        return {"ok": True, "summary": f"Cleared {n} jobs."}

    # ── execute_script ──────────────────────────────────────────────────────────
    if t == "execute_script":
        import subprocess  # noqa: PLC0415, S404
        import sys
        import tempfile
        code = p.get("code", "")
        if not code or len(code.strip()) < 5:
            raise HTTPException(400, "Missing or empty code")
        # Write to a temp file; set PYTHONPATH so glossa_lab is importable
        backend_dir = Path(__file__).resolve().parent.parent.parent
        tests_dir   = backend_dir / "tests"
        env = dict(__import__("os").environ)
        existing_pp = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = str(backend_dir) + __import__("os").pathsep + str(tests_dir) + (
            __import__("os").pathsep + existing_pp if existing_pp else ""
        )
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py",
                                         delete=False, encoding="utf-8") as fh:
            fh.write(code)
            tmp = fh.name
        try:
            proc = subprocess.run(  # noqa: S603
                [sys.executable, tmp],
                capture_output=True, text=True, timeout=120, env=env,
            )
        finally:
            __import__("os").unlink(tmp)
        ok = proc.returncode == 0
        stdout = proc.stdout[-3000:]
        stderr = proc.stderr[-500:]
        # Try to parse last JSON line from stdout as structured result
        result_json: dict[str, Any] | None = None
        for raw_line in reversed(stdout.splitlines()):
            try:
                result_json = json.loads(raw_line.strip())
                break
            except Exception:  # noqa: BLE001
                pass
        return {
            "ok": ok,
            "summary": f"Script executed (exit {proc.returncode}). "
                       f"{len(stdout.splitlines())} output lines.",
            "stdout": stdout,
            "stderr": stderr,
            "result_json": result_json,
        }

    # ── query_corpus ────────────────────────────────────────────────────────────
    if t == "query_corpus":
        pattern: list[str] = p.get("pattern", [])
        position: str = p.get("position", "any")  # any | initial | terminal | medial
        max_results: int = min(int(p.get("max_results", 50)), 200)
        corpus_file = Path(__file__).resolve().parent.parent.parent.parent / "reports" / "icit_extracted_corpus.json"
        if not corpus_file.exists():
            return {"ok": False, "summary": "Corpus file not found.", "matches": []}
        try:
            corpus_data = json.loads(corpus_file.read_text(encoding="utf-8"))
            inscriptions = [i["sequence"] for i in corpus_data.get("inscriptions", []) if i.get("sequence")]
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(500, f"Corpus load error: {exc}") from exc

        if not pattern:
            return {"ok": False, "summary": "No pattern provided.", "matches": []}

        matches: list[dict[str, Any]] = []
        for insc in inscriptions:
            if len(insc) < len(pattern):
                continue
            found = False
            if position == "initial":
                found = insc[:len(pattern)] == pattern
            elif position == "terminal":
                found = insc[-len(pattern):] == pattern
            else:  # any — sliding window
                for i in range(len(insc) - len(pattern) + 1):
                    if insc[i:i+len(pattern)] == pattern:
                        found = True
                        break
            if found:
                matches.append({"inscription": insc, "length": len(insc)})
                if len(matches) >= max_results:
                    break
        return {
            "ok": True,
            "summary": f"Found {len(matches)} inscriptions matching {pattern} ({position}).",
            "matches": matches,
            "pattern": pattern,
            "position": position,
        }

    # ── compare_results ─────────────────────────────────────────────────────────
    if t == "compare_results":
        file_a = p.get("file_a", "")
        file_b = p.get("file_b", "")
        if not file_a or not file_b:
            raise HTTPException(400, "Both file_a and file_b are required")
        reports_dir = Path(__file__).resolve().parent.parent.parent.parent / "reports"
        def _safe_load(name: str) -> dict[str, Any] | None:
            p = reports_dir / name
            if not p.exists():
                return None
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                return None
        a = _safe_load(file_a)
        b = _safe_load(file_b)
        if a is None:
            raise HTTPException(404, f"Report '{file_a}' not found")
        if b is None:
            raise HTTPException(404, f"Report '{file_b}' not found")
        # Build a flat diff of numeric values
        def _flatten(d: Any, prefix: str = "") -> dict[str, Any]:
            out: dict[str, Any] = {}
            if isinstance(d, dict):
                for k, v in d.items():
                    out.update(_flatten(v, f"{prefix}.{k}" if prefix else k))
            elif isinstance(d, (int, float, str)):
                out[prefix] = d
            return out
        flat_a = _flatten(a)
        flat_b = _flatten(b)
        diffs: list[dict[str, Any]] = []
        all_keys = set(flat_a) | set(flat_b)
        for key in sorted(all_keys):
            va = flat_a.get(key, "<missing>")
            vb = flat_b.get(key, "<missing>")
            if va != vb:
                diffs.append({"key": key, "a": va, "b": vb})
        return {
            "ok": True,
            "summary": f"Compared {file_a} vs {file_b}: {len(diffs)} differences.",
            "file_a": file_a,
            "file_b": file_b,
            "n_diffs": len(diffs),
            "diffs": diffs[:100],
        }

    # ── acquire_corpus ──────────────────────────────────────────────────────────
    if t == "acquire_corpus":
        from glossa_lab.corpus_acquirer import acquire, get_catalog  # noqa: PLC0415
        from glossa_lab.database import get_db  # noqa: PLC0415

        source_id  = p.get("source_id", "custom_url")
        corpus_name = p.get("name") or p.get("corpus_name", source_id.replace("_", " ").title())
        corpus_type = p.get("corpus_type", "ancient")
        custom_url  = p.get("url") or None
        description = p.get("description", "")

        # Acquire and convert
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(
                None, lambda: acquire(source_id, custom_url=custom_url)
            )
        except (ValueError, RuntimeError) as exc:
            raise HTTPException(400, str(exc)) from exc

        inscriptions = result["inscriptions"]
        meta = result["metadata"]
        flat_tokens: list[str] = [s for ins in inscriptions for s in ins]

        # Register in the corpus database
        db = get_db()
        if db is None:
            raise HTTPException(503, "Database unavailable")

        corpus = await db.create_text({
            "name":         corpus_name,
            "corpus_type":  corpus_type,
            "content":      flat_tokens,
            "description":  description or f"Acquired from {meta['source']}",
        })

        n_insc = meta["n_inscriptions"]
        n_tok  = meta["n_tokens"]
        alpha  = meta["alphabet_size"]
        return {
            "ok": True,
            "corpus_id":      corpus["id"],
            "corpus_name":    corpus_name,
            "n_inscriptions": n_insc,
            "n_tokens":       n_tok,
            "alphabet_size":  alpha,
            "source":         meta["source"],
            "summary": (
                f"Corpus '{corpus_name}' acquired: {n_insc} inscriptions, "
                f"{n_tok} tokens, {alpha} distinct signs. Registered with ID {corpus['id']}."
            ),
        }

    # ── summarize_session ───────────────────────────────────────────────────────
    if t == "summarize_session":
        from glossa_lab.database import get_db  # noqa: PLC0415
        db = get_db()
        if db is None:
            raise HTTPException(503, "Database unavailable")
        title = p.get("title", "AI Session Summary")
        # Use any provided conversation content; otherwise generate a stub
        conv_content = p.get("content", "")
        nb = await db.create_notebook({
            "title": title,
            "content": conv_content or f"Session summary saved at {__import__('datetime').datetime.utcnow().isoformat()}",
            "study_id": None,
            "tags": ["ai-generated", "session-summary"],
        })
        return {"ok": True, "summary": f"Session summary '{title}' saved to notebooks.", "id": nb["id"]}

    # ── Unknown action type — return 400 with helpful message ────────────────
    known = [
        "open_view", "run_experiment", "run_pipeline", "change_setting",
        "generate_report", "create_hypothesis", "create_notebook",
        "clear_jobs", "execute_script", "query_corpus", "compare_results",
        "acquire_corpus", "summarize_session",
    ]
    raise HTTPException(
        400,
        f"Unknown action type: '{t}'. "
        f"Valid types: {', '.join(known)}"
    )


# ── Streaming chat endpoint ──────────────────────────────────────────────────


@router.post("/chat/stream")
async def ai_chat_stream(body: ChatRequest):
    """Streaming version of /ai/chat using Server-Sent Events.

    Streams token-by-token from Ollama (or falls back to a single event for
    remote providers).  Frontend receives:
      data: {"delta": "token text"}       — partial token
      data: {"done": true, "actions": [...]}  — final event with parsed actions
    """
    from fastapi.responses import StreamingResponse  # noqa: PLC0415
    from glossa_lab.ai_utils import _get_provider_prefs, _call_ollama  # noqa: PLC0415
    from glossa_lab.model_profiles import get_profile, trim_history  # noqa: PLC0415
    from glossa_lab.experiment_base import discover_experiments  # noqa: PLC0415
    import urllib.request  # noqa: PLC0415

    # Build the same system prompt as /ai/chat
    context_block = ""
    if body.context_type == "research":
        context_block = "\n\n" + _build_research_context()

    profile = get_profile(body.model)
    settings_ctx = _build_settings_context()
    action_addendum = ""
    if profile["action_capable"]:
        try:
            exp_ids = sorted(discover_experiments().keys())
            action_addendum = _ACTION_SYSTEM_ADDENDUM + (
                f"\n\nREGISTERED EXPERIMENT IDs: {', '.join(exp_ids)}"
            )
        except Exception:  # noqa: BLE001
            action_addendum = _ACTION_SYSTEM_ADDENDUM

    base_role = (
        "You are Glossa, an expert AI research assistant for Glossa Lab. "
        "You have deep knowledge of computational linguistics, information theory, "
        "and the specific decipherment methodology used at Glossa Lab."
    )
    system = _build_system_prompt(
        base=base_role, context_block=context_block,
        settings_ctx=settings_ctx, action_addendum=action_addendum,
        style=profile["prompt_style"],
    )
    messages = [{"role": "system", "content": system}] + [
        {"role": m.role, "content": m.content} for m in body.messages
    ]
    messages = trim_history(messages, budget_chars=profile["ctx_budget"] * 4)

    # Try Ollama streaming; fall back to blocking call for remote providers
    prefs = _get_provider_prefs()
    ollama_pref = prefs.get("ollama", {})
    use_ollama_stream = (
        not body.provider
        and ollama_pref.get("enabled")
        and ollama_pref.get("selected_model")
    ) or (body.provider == "ollama" and body.model)

    async def _sse_stream():
        accumulated = ""
        if use_ollama_stream:
            model = body.model or ollama_pref.get("selected_model", "")
            payload = json.dumps({
                "model": model,
                "messages": messages,
                "stream": True,
                "options": {"temperature": profile["temperature"],
                            "num_predict": profile["max_tokens"]},
            }).encode()
            req = urllib.request.Request(
                "http://localhost:11434/api/chat",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=180) as resp:
                    for raw_line in resp:
                        if not raw_line.strip():
                            continue
                        try:
                            chunk = json.loads(raw_line.decode())
                            token = chunk.get("message", {}).get("content", "")
                            if token:
                                accumulated += token
                                yield f"data: {json.dumps({'delta': token})}\n\n"
                            if chunk.get("done"):
                                break
                        except Exception:  # noqa: BLE001
                            pass
            except Exception as exc:  # noqa: BLE001
                yield f"data: {json.dumps({'error': str(exc)})}\n\n"
        else:
            # Fall back: run blocking call in thread, emit full reply as one event
            loop = asyncio.get_event_loop()
            from glossa_lab.ai_utils import call_llm  # noqa: PLC0415
            try:
                full = await loop.run_in_executor(
                    None,
                    lambda: call_llm(messages, max_tokens=profile["max_tokens"],
                                     temperature=profile["temperature"],
                                     provider_override=body.provider,
                                     model_override=body.model),
                )
                accumulated = full
                yield f"data: {json.dumps({'delta': full})}\n\n"
            except Exception as exc:  # noqa: BLE001
                yield f"data: {json.dumps({'error': str(exc)})}\n\n"

        # Final event: parse actions from assembled text
        clean, actions = _parse_actions(accumulated)
        yield f"data: {json.dumps({'done': True, 'content': clean, 'actions': actions})}\n\n"

    return StreamingResponse(
        _sse_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── AI Report Synthesis ───────────────────────────────────────────────────


class ReportSynthesisRequest(BaseModel):
    report_contents: list[dict[str, Any]]  # [{name, filename, data}]
    study_ids: list[str] = []
    title: str = "Research Report"


@router.post("/report-synthesis")
async def ai_report_synthesis(body: ReportSynthesisRequest) -> dict[str, Any]:
    """Generate a comprehensive AI research report from selected report files.

    Takes the content of selected JSON reports and optionally study metadata,
    and produces a structured Markdown synthesis suitable for export as PDF
    or sharing with collaborators.
    """
    from glossa_lab.database import get_db  # noqa: PLC0415

    # Build context from report contents
    report_sections: list[str] = []
    for r in body.report_contents[:8]:  # cap at 8 reports
        name = r.get("name", "Report")
        data = r.get("data", {})
        if isinstance(data, dict):
            # Compact JSON snippet (first 800 chars)
            snippet = json.dumps(data, indent=2, default=str)[:800]
        else:
            snippet = str(data)[:800]
        report_sections.append(f"**{name}**:\n```json\n{snippet}\n```")

    # Build context from studies
    study_context = ""
    db = get_db()
    if db and body.study_ids:
        study_summaries = []
        for sid in body.study_ids[:4]:
            study = await db.get_study(sid)
            if study:
                nodes = study.get("graph", {}).get("nodes", [])
                study_summaries.append(
                    f"Study '{study['name']}': {study.get('description', '')} "
                    f"| {len(nodes)} nodes"
                )
        if study_summaries:
            study_context = "\n\n**Studies included:**\n" + "\n".join(f"- {s}" for s in study_summaries)

    system = (
        "You are an expert research scientist specialising in computational linguistics, "
        "ancient script analysis, and statistical decipherment methods. "
        "Generate a comprehensive, rigorous research report in Markdown format. "
        "The report must include:\n"
        "1. Executive Summary (3-4 sentences)\n"
        "2. Data & Methodology section\n"
        "3. Results section with all numerical findings in a structured table format\n"
        "4. Analysis & Interpretation section\n"
        "5. Limitations section (be honest and specific)\n"
        "6. Next Steps / Recommendations (concrete, actionable)\n\n"
        "Use precise scientific language. Include ALL numerical results from the data. "
        "Format numbers as tables where possible. Be specific about what succeeded and what failed."
    )

    user = (
        f"Generate a comprehensive research report titled: '{body.title}'\n"
        f"{study_context}\n\n"
        f"**Report data ({len(body.report_contents)} files):**\n\n"
        + "\n\n---\n\n".join(report_sections)
    )

    try:
        markdown = await _run_llm(
            [{"role": "system", "content": system}, {"role": "user", "content": user}]
        )
        return {
            "title": body.title,
            "markdown": markdown,
            "n_reports": len(body.report_contents),
            "study_ids": body.study_ids,
        }
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/decipher")
async def ai_decipher(body: DecipherRequest) -> dict[str, Any]:
    """Indus Script decipherment assistant — apply a theory to a sign sequence."""
    theory_descriptions = {
        "linguistic": "general linguistic analysis treating signs as syllabic or logographic units",
        "logo-syllabic": "logo-syllabic hypothesis: leading sign is logographic, rest syllabic",
        "acrophonic": "acrophonic principle: each sign represents the first sound of its name in a Dravidian language",
        "dravidian": "Dravidian proto-language hypothesis: signs map to Proto-Tamil/Dravidian morphemes",
    }
    theory_desc = theory_descriptions.get(body.theory, body.theory)
    seq = " → ".join(body.sign_sequence)

    system = (
        "You are an expert in ancient script decipherment, specialising in the Indus Script. "
        "Return ONLY valid JSON:\n"
        '{"reading": "proposed phonetic/semantic reading", '
        '"confidence": "low|medium|high", '
        '"reasoning": "step-by-step reasoning", '
        '"alternative_readings": ["alt 1", "alt 2"], '
        '"parallels": ["parallel in other scripts"], '
        '"caveats": ["caveat 1"]}'
    )
    user = (
        f"Apply the {body.theory} theory ({theory_desc}) to interpret this Indus sign sequence:\n"
        f"Signs: {seq}\n"
        f"Sign IDs: {body.sign_sequence}"
    )

    try:
        raw = await _run_llm(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            json_mode=True,
        )
        from glossa_lab.ai_utils import _extract_json  # noqa: PLC0415
        result = json.loads(_extract_json(raw))
        result["sign_sequence"] = body.sign_sequence
        result["theory"] = body.theory
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/draft-section")
async def ai_draft_section(body: DraftSectionRequest) -> dict[str, Any]:
    """Turn an experiment result into a draft academic paper section."""
    from glossa_lab.experiment_base import get_experiment

    cls = get_experiment(body.experiment_id)
    meta = cls.to_dict() if cls else {"name": body.experiment_id, "description": "", "category": ""}

    section_instructions = {
        "abstract": "Write a 150-word abstract summarising the experiment and its key finding.",
        "introduction": "Write an Introduction paragraph (200 words) motivating this experiment.",
        "methods": "Write a Methods paragraph (200 words) describing how the experiment was conducted.",
        "results": "Write a Results paragraph (200 words) reporting the numerical findings.",
        "discussion": "Write a Discussion paragraph (250 words) interpreting the results in the context of Indus Script research.",
    }
    instr = section_instructions.get(body.section_type, section_instructions["results"])

    system = (
        "You are an academic writer specialising in computational linguistics and ancient script research. "
        "Write formal, journal-quality prose. Return ONLY valid JSON:\n"
        '{"section_type": "...", "text": "the paragraph text", '
        '"suggested_title": "...", "keywords": ["kw1", "kw2"]}'
    )
    user = (
        f"Experiment: {meta['name']}\n"
        f"Category: {meta.get('category', '')}\n"
        f"Description: {meta.get('description', '')}\n"
        f"Results: {json.dumps(body.result_json, indent=2)[:1500]}\n\n"
        f"{instr}"
    )

    try:
        raw = await _run_llm(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            json_mode=True,
        )
        from glossa_lab.ai_utils import _extract_json  # noqa: PLC0415
        result = json.loads(_extract_json(raw))
        result["experiment_id"] = body.experiment_id
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/hypotheses/generate")
async def ai_generate_hypotheses(body: HypothesisGenRequest) -> dict[str, Any]:
    """Generate testable hypotheses from study results or a free-text context."""
    from glossa_lab.database import get_db
    from glossa_lab.experiment_base import get_experiment

    context = body.context
    if body.study_id:
        db = get_db()
        if db:
            study = await db.get_study(body.study_id)
            if study:
                graph = study.get("graph", {})
                exp_descs = []
                for node in graph.get("nodes", []):
                    cls = get_experiment(node.get("ref_id", ""))
                    if cls:
                        m = cls.to_dict()
                        exp_descs.append(f"- {m['name']}: {m['description']}")
                context = (
                    f"Study: {study['name']}\n"
                    f"Description: {study.get('description', '')}\n"
                    f"Experiments:\n" + "\n".join(exp_descs)
                ) + ("\n\n" + body.context if body.context else "")

    system = (
        "You are a research hypothesis generator for Indus Script computational linguistics. "
        "Return ONLY valid JSON:\n"
        '{"hypotheses": [{"title": "H1: ...", "statement": "full statement", '
        '"testability": "how to test this", "priority": "high|medium|low", '
        '"related_experiments": ["exp_id_hint"]}], '
        '"research_gaps": ["gap 1", "gap 2"]}'
    )
    user = f"Generate 3-5 testable research hypotheses based on:\n{context}"

    try:
        raw = await _run_llm(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            json_mode=True,
        )
        from glossa_lab.ai_utils import _extract_json  # noqa: PLC0415
        result = json.loads(_extract_json(raw))
        if body.study_id:
            result["study_id"] = body.study_id
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/experiment-chain")
async def ai_experiment_chain(body: ExperimentChainRequest) -> dict[str, Any]:
    """Plan a sequence of experiments to test a research hypothesis."""
    from glossa_lab.experiment_base import list_discovered_experiments

    exps = list_discovered_experiments()
    exp_list = "\n".join(
        f"  id={e['id']!r}, name={e['name']!r}, desc={e['description'][:60]!r}" for e in exps[:25]
    )

    system = (
        "You are an experimental research planner for Indus Script linguistics. "
        "Return ONLY valid JSON:\n"
        '{"chain": [{"step": 1, "experiment_id": "...", "experiment_name": "...", '
        '"purpose": "why this step", "expected_output": "what this step produces", '
        '"depends_on": []}], '
        '"rationale": "overall experimental strategy", '
        '"success_criteria": "how to know the hypothesis is confirmed/refuted"}'
    )
    user = (
        f"Plan an experiment chain to test:\n{body.hypothesis}\n\n"
        f"Available experiments:\n{exp_list}"
    )

    try:
        raw = await _run_llm(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            json_mode=True,
        )
        result = json.loads(raw)
        result["hypothesis"] = body.hypothesis
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/synthesize")
async def ai_synthesize(body: SynthesisRequest) -> dict[str, Any]:
    """Cross-study synthesis: find patterns and insights across multiple studies."""
    from glossa_lab.database import get_db
    from glossa_lab.experiment_base import get_experiment

    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    study_summaries = []
    for sid in body.study_ids[:6]:
        study = await db.get_study(sid)
        if not study:
            continue
        nodes = study.get("graph", {}).get("nodes", [])
        exp_names = []
        for node in nodes:
            cls = get_experiment(node.get("ref_id", ""))
            if cls:
                exp_names.append(cls.to_dict()["name"])
        study_summaries.append(
            f"Study '{study['name']}': {study.get('description', '')} | "
            f"experiments: {', '.join(exp_names) or 'none'}"
        )

    system = (
        "You are a meta-researcher synthesising findings across multiple Indus Script studies. "
        "Return ONLY valid JSON:\n"
        '{"synthesis": "narrative synthesis of key cross-study findings", '
        '"convergent_findings": ["finding 1"], '
        '"contradictions": ["contradiction 1"], '
        '"emerging_patterns": ["pattern 1"], '
        '"recommended_next_studies": [{"name": "...", "rationale": "..."}], '
        '"overall_assessment": "where does the research stand?"}'
    )
    question_block = f"\nResearch question: {body.question}" if body.question else ""
    user = f"Synthesise these studies:{question_block}\n\n" + "\n".join(study_summaries)

    try:
        raw = await _run_llm(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            json_mode=True,
        )
        result = json.loads(raw)
        result["study_ids"] = body.study_ids
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/sign-reading")
async def ai_sign_reading(body: SignReadingRequest) -> dict[str, Any]:
    """Probabilistic sign reading suggestions for Indus Script sign IDs."""
    system = (
        "You are an Indus Script specialist with knowledge of all major decipherment theories. "
        "Return ONLY valid JSON:\n"
        '{"readings": [{"sign_id": "...", "theory": "...", '
        '"phonetic_reading": "...", "semantic_reading": "...", "confidence": 0.0-1.0, '
        '"notes": ""}], '
        '"sequence_reading": "overall sequence interpretation", '
        '"parallels": ["parallel in Sumerian/Elamite/Dravidian"]}'
    )
    user = (
        f"Apply the {body.theory} theory to give readings for these Indus signs:\n"
        f"Sign IDs: {', '.join(body.sign_ids)}\n"
        + (f"Context: {body.context}" if body.context else "")
    )

    try:
        raw = await _run_llm(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            json_mode=True,
        )
        result = json.loads(raw)
        result["sign_ids"] = body.sign_ids
        result["theory"] = body.theory
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/corpus-catalog")
async def get_corpus_catalog() -> dict[str, Any]:
    """Return the catalog of acquirable corpora.

    Each entry includes: id, name, description, source, tier, size_estimate,
    status (available | requires_manual), and a usage note.
    The frontend uses this to let users browse what can be downloaded and
    propose acquire_corpus actions via the AI.
    """
    from glossa_lab.corpus_acquirer import get_catalog  # noqa: PLC0415
    catalog = get_catalog()
    available = [c for c in catalog if c["status"] == "available"]
    manual    = [c for c in catalog if c["status"] != "available"]
    return {
        "catalog":   catalog,
        "available": [c["id"] for c in available],
        "manual":    [c["id"] for c in manual],
        "total":     len(catalog),
    }


@router.get("/research-context")
async def get_research_context() -> dict[str, Any]:
    """Return the current Indus decipherment research context as a plain-text block.

    The frontend uses this to show a preview and to inject research state
    into the AI chat when context_type='research' is selected.
    """
    context = _build_research_context()
    # Count how many sign assignments are loaded
    catalog_path = _REPORTS / "sign_expansion.json"
    n_assigned = 0
    coverage_pct = 0.0
    next_steps: list[str] = []
    if catalog_path.exists():
        try:
            data = json.loads(catalog_path.read_text(encoding="utf-8"))
            top100 = data.get("top100_catalog", [])
            n_assigned = sum(
                1 for r in top100 if r.get("confidence") in ("HIGH", "MED", "LOW")
            )
            cov = data.get("token_coverage", {})
            coverage_pct = cov.get("pct", 0.0)
        except Exception:  # noqa: BLE001
            pass
    # Pull next step from LEDGER
    if _LEDGER.exists():
        try:
            text = _LEDGER.read_text(encoding="utf-8", errors="replace")
            for line in reversed(text.splitlines()):
                line = line.strip()
                if line.startswith("Next step:"):
                    next_steps = [line[len("Next step:"):].strip()]
                    break
        except Exception:  # noqa: BLE001
            pass
    return {
        "context": context,
        "summary": {
            "n_assigned_signs": n_assigned,
            "token_coverage_pct": coverage_pct,
            "next_steps": next_steps,
            "context_chars": len(context),
        },
    }
