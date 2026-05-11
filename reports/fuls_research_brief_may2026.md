# Glossa Lab — Research Update for Dr. Andreas Fuls
## May 2026 — ICIT Access Request Follow-Up

*This document is a brief for attachment to the ICIT access request email.*
*It supplements the detailed request in fuls_contact_email.md with current research results.*

---

### Project summary

**Glossa Lab** is an open-source computational platform for structural analysis and
hypothesis-driven decipherment of undeciphered writing systems. The platform implements
a rigorous structure-first, corpus-first methodology:

1. Multi-source corpus ingestion with full provenance metadata
2. Canonical sign registry and cross-system crosswalk (Mahadevan ↔ Parpola ↔ Wells ↔ Fuls)
3. Non-destructive sequence normalization
4. Frequency, positional, n-gram, and spectral structural analysis
5. Latent sign class discovery (positional behavior clustering)
6. Candidate degree-of-freedom schema estimation
7. Only then: controlled linguistic hypothesis testing with explicit anti-circularity protocols

All computations are reproducible. Every experiment is version-controlled and registered
in a structured job ledger with JSON output files. The platform is built on FastAPI
(Python), React/TypeScript, and SQLite.

---

### Current research state (as of May 2026)

**Corpus:** Holdat LLC corpus (1,670 seals, 9 sites — Mohenjo-daro, Harappa, Dholavira,
Chanhu-daro, Kalibangan, Lothal, Surkotada, Amri, Rakhigarhi), supplemented with
Mahadevan 1977 (M77, 1,669 inscriptions) for statistical analysis.

**Decipherment progress after V24 (17 autonomous distributional rounds):**

| Metric | Value |
|---|---|
| Signs assigned (of 390 in corpus) | 333 / 390 (85.4%) |
| Token coverage | 99.2% |
| Fully decoded inscriptions | 96.7% (1,615 / 1,670) |
| Weighted confidence score | 64.8% (H×1.0 + M×0.6 + L×0.3) |
| Confidence breakdown | HIGH: 9 signs / MEDIUM: 63 / LOW: 261 |
| Tamil-Brahmi phoneme correlation | **0.914** (Pearson r) |

**The Tamil-Brahmi phoneme correlation of 0.914** measures the alignment between
the phoneme frequency distribution implied by the current sign assignments and the
Tamil-Brahmi phoneme frequency distribution from Mahadevan 2003 (Harvard Oriental
Series 62). This is a structural alignment metric, not a claim of phonetic identity.

**Supplementary structural tests (Phase-31):**
- Zipf slope: M77 slope 0.75 vs Tamil-Brahmi slope 0.93 — delta 0.18, within the
  preregistered threshold of 0.3 for syllabic/logo-syllabic script class alignment
- Both corpora fall in the recognized 0.5–1.5 Zipf regime for syllabic scripts

**What these results mean (epistemic caveat):**
The 333-sign assignments are distributional hypotheses based on PDR positional
inventory and Tamil-Brahmi frequency modeling. They are NOT:
- Verified phonetic readings
- Cross-validated against bilingual material

The 0.914 correlation is the strongest quantitative evidence produced so far that the
Indus script's phoneme distribution is structurally consistent with a Dravidian family
script. It is consistent with, but does not prove, the Dravidian hypothesis.

---

### Why ICIT access is critical for the next phase

The current Holdat corpus (1,670 seals) is the largest freely available digital Indus
corpus, but it has known limitations:
- Site coverage is uneven (only 9 sites, Mohenjo-daro-heavy)
- Sign transcriptions use a non-standard scheme requiring crosswalk to Mahadevan/Fuls
- No iconographic metadata in the CSV format

Your ICIT database (4,537 artefacts, as described in your 2023 Corpus preview) would:

1. **Expand the corpus 2.7×** — the single highest-impact data acquisition step
   available. Re-running the V24 distributional analysis on 4,537 seals would be
   expected to push weighted confidence from 64.8% toward 70%+.

2. **Enable site-stratified analysis** — with your site categories (Failaka, Janabiyah,
   Karzakkan, Qala'at al-Bahrain, Saar, Susa, Luristan, Girsu, Ur, etc.), we can
   test whether sign assignments derived from Indus heartland inscriptions generalize
   to the western Gulf contact zone — a direct test of the contact-zone hypothesis.

3. **Enable CISI crosswalk** — your ICIT IDs, CISI numbers, and excavation numbers
   in a single database would allow us to resolve the crosswalk between the Holdat
   sign IDs, Mahadevan P-numbers, and your Fuls/Wells typology, which is currently
   partial.

4. **Western Gulf seal corpus** — we have identified 23 western "Gulf INDUS" objects
   (Laursen 2010 Table 1, nos. 6–27 and 56) from Qala'at al-Bahrain, Failaka, Saar,
   Janabiyah, Susa, Luristan, Ur, Girsu, and Mesopotamia provenances. The published
   CISI volumes through 3.3 do not appear to include a dedicated western corpus volume.
   An ICIT site-extract for these provenances would be uniquely valuable.

---

### Specific ICIT data request

We would be grateful for any of the following:

1. **Read access to ICIT** at indus.epigraphica.de for standard research queries
   (inscription sequences, site attributions, artefact types, sign IDs)

2. **Site-level export or extract** for the following western sites:
   Failaka, Janabiyah, Karzakkan, Qala'at al-Bahrain, Saar, Susa, Luristan,
   Girsu, Ur, Tell Umma, Tello, Kish, Nippur

3. **Sign crosswalk table**: Fuls/Wells sign IDs ↔ Parpola P-numbers ↔ Mahadevan
   sign numbers (even a partial table for the most frequent signs would be valuable)

4. **Preferred citation format** for ICIT data in publications

---

### What we can offer in return

- Full attribution of ICIT in all outputs (software, papers, reports)
- Sharing of our structural analysis outputs (positional profiles, TB correlation
  metrics, site-stratified spectral fingerprints) — these may be useful cross-validation
  for your sign catalog methodology
- Open-source codebase: all analysis pipelines are at GitHub under BitConcepts/glossa-lab
- Citation of your Corpus of Indus Inscriptions (2023), A Catalog of Indus Signs (2023),
  and all relevant Epigrafika papers throughout our outputs

---

### Contact

**Tristen Pierson**
BitConcepts
tpierson@bitconcepts.tech
GitHub: BitConcepts/glossa-lab

---

*This brief accompanies the detailed access request in fuls_contact_email.md.*
*Platform documentation and example outputs available on request.*
