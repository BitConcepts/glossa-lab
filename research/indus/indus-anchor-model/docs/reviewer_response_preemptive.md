# Preemptive Reviewer Response
## Anticipated Concerns — Indus Anchor Model Manuscript

This document anticipates likely reviewer concerns and states our position on each. Prepared for Digital Scholarship in the Humanities submission.

---

### R1 — No bilingual inscription exists; claims are unverifiable

**Concern:** Without a Rosetta-stone equivalent, all proposed readings are speculation.

**Our position:** We agree. The manuscript does not claim verified readings. It proposes *candidate anchors* — hypotheses that are explicitly tiered by confidence level and explicitly marked as unverified. The abstract states: "coverage measures anchor-model assignment, not verified phonetic transcription." The conclusion states: "This study does not claim epigraphic finality in the absence of a bilingual inscription."

The contribution is a reproducible, falsifiable model with explicit criteria for refutation — not a claim of solved decipherment.

**What would resolve it definitively:** A bilingual inscription with Indus signs alongside Sumerian, Akkadian, or Elamite.

---

### R2 — The Holdat corpus is not publicly available; results cannot be reproduced

**Concern:** If the primary corpus is proprietary, no one can verify the counts.

**Our position:** This is a genuine limitation and is acknowledged explicitly in the data availability statement. We address it three ways: (1) all scripts are published so analyses can be rerun on any equivalent corpus; (2) the public tables in `data/public/` support independent testing of the core structural claims; (3) the ICIT corpus is identified as the target for independent cross-corpus validation.

The structural claims (fish-sign isolation rate, betweenness centrality from the public bigram table, anchor table integrity) are testable without Holdat.

**What would resolve it:** ICIT crosswalk and replication (see `docs/icit_validation_plan.md`).

---

### R3 — Proto-Dravidian matching may be circular; DEDR lookup is flexible enough to confirm almost any reading

**Concern:** With 4,000+ DEDR entries, a sufficiently creative researcher can match any reading to Dravidian roots.

**Our position:** This is a real methodological risk. We address it through: (1) a five-layer evidence hierarchy that requires two independent evidence sources for HIGH confidence; (2) the exclusion of heuristic placeholders (107 removed by Phase-133); (3) a Dravidian phoneme exclusivity test — 0/157 readings require Sanskrit-exclusive phonemes, while 35/157 require Dravidian-exclusive ones; (4) the 59% convergence with Parpola (1994), which was written before our computational analysis.

The model does not claim to prove Dravidian superiority over proto-Munda or other alternatives. The preprint explicitly states this has not been formally quantified.

**What would resolve it:** A formal comparison against proto-Munda, Indo-Aryan, and language-neutral syllabic baselines, which remains necessary before any linguistic interpretation is treated as discriminative.

---

### R4 — High-frequency signs will dominate coverage; rare signs are effectively unanchored

**Concern:** Achieving high token coverage by correctly identifying a few very common signs (M342, M267, M099) does not demonstrate that the model works for the full sign inventory.

**Our position:** This is correct and acknowledged. The H+M token coverage (90.96%) is inflated by the high frequency of a small number of well-evidenced signs. The structural ceiling section (§3.9) explicitly notes that 505/1,670 seals are not fully covered by H+M readings, and that 18 signs with frequency 5–7 resist decipherment entirely. The manuscript does not present 90.96% as evidence of near-complete decipherment.

---

### R5 — Sign-list crosswalk incompatibility makes ICIT comparison unreliable

**Concern:** Mahadevan M-numbers and ICIT sign codes do not map one-to-one; a crosswalk introduces error that could inflate or deflate any comparative metric.

**Our position:** This is a real concern and is why the crosswalk is identified as the first technical ask in the ICIT outreach package. A partial crosswalk covering the top-50 signs by token frequency would be sufficient to test the structural claims (Tests T1–T3 in the ICIT validation plan). The failure-case analysis (Test T8) specifically measures how much of the H+M anchor set lacks a clean crosswalk equivalent.

---

### R6 — The AI-assisted pipeline may introduce systematic biases

**Concern:** Automated pattern extraction is susceptible to overfitting and confirmation bias, especially if the same pipeline that generates hypotheses is also used to test them.

**Our position:** The AI Disclosure in §7 explicitly states that AI tooling was used for scripting, data management, and literature search — not for hypothesis generation or interpretation. All statistical tests (permutation, bootstrap, chi-square) are standard methods run on the corpus data; the pipeline automates the computation, not the reasoning. Hypotheses are generated by the DEDR matching and positional analysis pipeline; tests are then run against the null distribution or against independent sources (Parpola, Mahadevan, Wells, Laursen).

The manuscript is honest that the AI layer cannot be fully separated from the research process. The falsification suite is designed specifically so that external researchers without access to Glossa-Lab can verify or contradict the structural claims.

---

### R7 — Token coverage is not the same as decipherment; the paper should not imply otherwise

**Concern:** Saying "90.96% token coverage" sounds like the script is mostly decoded.

**Our position:** The abstract explicitly states: "coverage measures anchor-model assignment, not verified phonetic transcription." The introduction and conclusion repeat this caveat. Coverage means that for 90.96% of corpus tokens, a sign exists in the anchor table with some candidate reading at some confidence level. It does not mean those readings are correct.

We are open to strengthening this caveat further in the manuscript if reviewers find the current language insufficient.

---

### R8 — Non-linguistic (semasiographic) explanations remain viable

**Concern:** Farmer, Sproat & Witzel (2004) argued the Indus script is non-linguistic. This manuscript does not directly engage with that argument.

**Our position:** The manuscript does engage with the structural predictions of the non-linguistic hypothesis implicitly. If the script were non-linguistic and semasiographic, we would expect: (1) near-random positional distribution of signs (but z=10.3 against null); (2) fish signs to appear in various contextual roles including isolation (but 0/140 isolated); (3) no formula grammar skeleton (but 97 formula types all share the same INITIAL–MEDIAL–TERMINAL structure). None of these are predictions of semasiographic systems. The manuscript does not prove the script is linguistic, but the structural results are more consistent with a linguistic system than with the specific semasiographic hypothesis.

A formal quantitative comparison against the Farmer-Sproat-Witzel predictions remains useful and is acknowledged as future work.

---

### R9 — The language-family comparison (Dravidian vs. Munda vs. Indo-Aryan) has not been quantified

**Concern:** The manuscript claims Proto-Dravidian compatibility but does not formally compare against alternatives.

**Our position:** This limitation is explicitly stated in the Limitations section (§4.4, point 6): "A formal comparison against Proto-Munda, early Indo-Aryan, and language-neutral syllabic models remains necessary before the linguistic interpretation can be treated as discriminative rather than merely compatible with Proto-Dravidian." We do not claim Dravidian superiority.

---

### R10 — ICIT replication is not yet complete

**Concern:** The model is presented as if validated, but the most important validation (ICIT cross-corpus test) is still pending.

**Our position:** Agreed. This is why the ICIT crosswalk is framed as the *immediate validation priority* in the preprint (§3.24, §5). The manuscript is submitted as a preprint ahead of that validation precisely so that the community can engage with the model, suggest improvements, and potentially participate in the ICIT testing. The falsification protocol (`docs/falsification_protocol.md`) clearly marks all ICIT-dependent tests as NOT YET TESTED.
