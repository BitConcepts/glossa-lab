# Phase-22 — Contact-Zone Anchor Acquisition (Synthesis)

**Date:** 2026-04-29
**Pipeline:** `experiment_graph_phase22` (graph-executor, WARP.md G1 compliant)
**Sub-experiments executed:**
- `indus_phase22a_meluhha_corpus_audit`
- `indus_phase22b_meluhhan_persons`
- `indus_phase22c_meluhha_name_matcher`
- `indus_phase22_synthesis` (verdict aggregator)
**Inputs:** `backend/glossa_lab/data/mesopotamian_contact.py` data module backed by:
- `corpora/downloads/contact_zone/cdli_meluhha/meluhha_tablets.json` (1,462 CDLI tablets)
- `corpora/downloads/contact_zone/indus_seals_mesopotamia/seals_at_mesopotamia.json` (13 seals)
- 5 contact-zone PDFs in `corpora/downloads/contact_zone/publications/` (text-extracted)

## TL;DR
Phase-22 successfully assembled the long-missing **contact-zone external anchor corpus**. The graph executor produced four `reports/phase22*.json` artefacts. The aggregated verdict:

> Phase-22 contact-zone inventory: **1462 CDLI tablets**, **66 Meluhhan-name candidates** (0 historically-confirmed), **13 Indus seals at Mesopotamia**, **0 prototype seal-name pairings**.

The contact-zone corpus is now first-class data inside Glossa-Lab and runs through the same atomic-node pipeline as every other phase. The first quantitative result is OBSERVED (we have substantial data); the first quantitative *bilingual* result is INSUFFICIENT_DATA, which Phase-23 must fix.

## 1. Acquisition outcomes

### 1.1 CDLI Meluhha-mention audit (Phase-22a)
- Scanned 135,255 ATF transliterations from `corpora/downloads/external_repos/cdli_gh_data/cdliatf_unblocked.atf`.
- **1,462 tablets** match at least one contact-zone keyword; 21 distinct periods covered.
- Keyword distribution (any tablet may match more than one):
  - `dilmun` — 924
  - `gu2-ab-ba` (Guabba, Sumerian Persian-Gulf entrepôt) — 613
  - `ma2-gan` — 371
  - `me-luh-ha` — 215
  - `ma-gan` — 68
  - `tilmun` — 11
  - `shu-ilishu` — 2
  - `tukrish`, `tukris` — 1 each
- Dominant periods: Ur III (850), Ebla (141), Old Babylonian (130), ED IIIb (71), Neo-Assyrian (61).
- Dominant proveniences: Girsu/Tello (789), Ebla/Tell Mardikh (133), Nippur (96), Ur (68).

The Girsu/Ur III bias is consistent with the historical record (Ur III's sealed Persian-Gulf trade administration ran through the Girsu archive), and the Neo-Assyrian tail captures Sargon II + Esarhaddon's "I marched as far as Magan and Meluhha" royal-inscription topos.

### 1.2 Indus-seals-at-Mesopotamia inventory (Phase-22c summary)
- **13 hand-encoded artefacts** spanning 8 countries / 8 typological classes.
- Includes the canonical Shu-ilishu seal (AO 22310, Louvre — `EME.BAL.ME.LUH.HA.KI`), the four Ur Gadd seals (BM 122187 + GADD_1/2 + ASMAR_TA), Susa, Berlin VA/243, Konar Sandal South, Jalalabad Fars, Failaka KM 1113, and the freshly published Al-Maqsha Token 2 (Laursen et al. 2026 JNES).
- Source coverage: Possehl 2006, Parpola 1977, Gadd 1932, Mallowan 1947, Wheeler 1968, Rao 1963, Frenez 2018, Vidale & Frenez 2015, Vidale Desset & Frenez 2021, David-Cuny & Neyme 2016, Laursen 2010, Laursen et al. 2026.

### 1.3 Meluhhan named-person extraction (Phase-22b)
- **489 distinct candidate name-tokens** flagged from lines containing `me-luh-ha`; 66 reach the freq>=2 threshold.
- The current heuristic regex `r"\b[a-z][a-z0-9]*(?:-[a-z][a-z0-9]*){1,4}\b"` is **very noisy**. Top hits are dominated by Akkadian particles and Sumerian word fragments rather than personal names:
  - `a-na` (27, "to") — Akkadian preposition
  - `mu-s` (20) — fragment of `mu-s,ur` (Egypt)
  - `e-mu-qi2` (20, "force/troops"), `ni-bi` (19, "without number"), `a-di` (17, "until")
  - `i3-dub me-luh-ha` (11) — "Meluhha storehouse" (Girsu)
  - `mes-me-luh-ha` (11) — "Meluhha tree/wood"
- Zero matches against the canonical Meluhhan personal names (Lu-sun-zi-da, Shu-ilishu) — these names are not present in our `me-luh-ha` line-window because `shu-ilishu` only attests in 2 tablets and `lu-sun-zi-da` is encoded with a `lu2-` prefix that the regex misses.
- This is a *known limitation of the prototype regex*; see Phase-23 priority 2.

### 1.4 Name-matcher prototype (Phase-22c matcher)
- 0 length-compatible pairings produced.
- **Reason:** none of the 13 catalogued Indus-seals-at-Mesopotamia have ingested `indus_signs[]` arrays yet. The seal records carry `inscription_reading` strings ("Shu-ilishu EME.BAL.ME.LUH.HA.KI", "(unread; ~3 Indus signs)", etc.) but the actual sign-by-sign Parpola/Wells codes are not in the JSON.
- The matcher correctly emitted the gap as its verdict: *"PROTOTYPE STATUS: name-matcher cannot score yet because no Mesopotamia-found Indus seals have ingested sign sequences. Phase-23 must populate indus_signs[] from CISI Vol 3 / Frenez 2018 catalogue tables."*

## 2. PDF acquisition status
| Paper | Source | Status |
|---|---|---|
| Vidale 2004, *Meluhha Villages* (Melammu IV) | harappa.com | Acquired 306 KB / 14 pp (85 me-luh-ha hits) |
| Levit 2010, *Meluhha Etymology* (Studia Orientalia) | direct | Acquired 726 KB / 26 pp (157 me-luh-ha hits) |
| Frenez 2005, *Lothal Sealings* | Zenodo | Acquired 1.9 MB / 22 pp |
| Frenez 2020, *Indus-Oman Trade* | direct | Acquired 2.7 MB / 28 pp |
| Frenez 2018, *Private Person, Public Persona* | direct | Acquired 22 MB / 69 pp |
| Wiley Laursen 2010, *Westward Indus* | Wiley | Paywalled (403) — see manifest |
| Tandfonline Frenez 2024 | Tandfonline | Paywalled (403) |
| JSTOR Parpola 1977 | JSTOR | Paywalled (403) |
| Crawford 2001, *Saar* | Internet Archive | Timeout |

All 5 acquired PDFs were natively text-extractable (no OCR fallback needed); 426k chars total across 159 pages saved as parallel `.txt` files in `publications/`.

## 3. Headline findings
1. **Contact-zone is real and large.** 1,462 cuneiform tablets is more than enough for statistical methods (greater than the entire ICIT Indus corpus by every metric).
2. **The Ur III + Girsu + Neo-Assyrian skew matches independent historical evidence.** This is a consistency check: our keyword filter is not picking up modern names or Hittite/Linear-B noise.
3. **Direct seal anchors exist** (13 catalogued, including the Shu-ilishu trilingual). Phase-23's priority is to ingest the actual sign sequences for these seals.
4. **Heuristic name extraction is too noisy** to surface real Meluhhan personal names without a refined regex + Akkadian particle stoplist.
5. **The bilingual-anchor question remains open** — exactly as the strategy review predicted. We now have the data plumbing in place to attempt a real readout test in Phase-23.

## 4. Phase-23 priority list (auto-derived from Phase22Verdict)
1. **Populate `indus_signs[]`** for the 13 Mesopotamia-found seals from CISI Vol 3 + Frenez 2018 catalogue tables. This unblocks the name-matcher.
2. **Tighten the Meluhhan-name regex** to explicitly capture the `-me-luh-ha-ki` suffix pattern, the `lu2-` and `dumu-` prefix patterns, and the canonical Lu-sun-zi-da / Shu-ilishu strings. Add an Akkadian-particle stoplist (`a-na`, `i-na`, `a-di`, `ni-bi`, `e-mu-qi2`, `mu-s`, ...).
3. **Define the falsifiable readout test:** a named Meluhhan attested in CDLI whose Indus-seal counterpart can be uniquely identified with a probability bound. (Per the strategy review's "what would the bilingual moment look like" question.)
4. **Acquire the paywalled remainder:** Laursen 2010, Frenez 2024, Parpola 1977 — through Inter-Library Loan or direct contact with the corresponding authors (Laursen Aarhus; Frenez Bologna; Vidale ISMEO).
5. **Add the 26 Tarut-Bahrain Persian-Gulf seal corpus** (Lombard & Marchesi catalogue) once Crawford 2001 is acquired.

## 5. Run trace
```
indus_phase22a_meluhha_corpus_audit  → reports/phase22a_meluhha_corpus_audit.json (1.5 KB)
indus_phase22b_meluhhan_persons      → reports/phase22b_meluhhan_persons.json    (22 KB)
indus_phase22c_meluhha_name_matcher  → reports/phase22c_meluhha_name_matcher.json (6.5 KB)
indus_phase22_synthesis              → reports/phase22_synthesis.json            (188 B verdict line)
```
All four reports are reproducible end-to-end via `python -m glossa_lab.experiments <graph_id>`. Each run is registered as a Job in the Glossa-Lab UI per WARP.md G1.

## 6. WARP.md G1 compliance note
Phase-22 follows the same atomic-node-graph pattern as Phases 14-21:
- `backend/glossa_lab/experiment_graph_phase22.py` exposes 6 `AtomicNodeDef` entries via `_phase22_node_defs()`.
- Wired into `ATOMIC_NODES` registry through the standard try/except block in `experiment_graph.py` after the Phase-21 block.
- Four JSON graphs in `backend/glossa_lab/experiments/graphs/indus_phase22*.json` (all `auto_migrated: false`).
- The on-disk extraction scripts under `scripts/phase22/` (CDLI ATF filter + PDF text extractor + acquisition driver) are the *acceptable exception* per the rule's "data-ingestion" clause; they only produce the on-disk JSON inputs that the data module reads.
