# Eteocypriot — Research Proposal

**Status: PROPOSAL under Spec 095 Stage 5 (T501), discharging the
proposal half of C095-15. Scoping only. No Eteocypriot analysis has
been executed under this proposal, and none is authorized by it:
execution requires a separate owner decision recorded outside this
spec's stages (D-095-4; C095-15).** The companion preregistration
draft is `eteocypriot-preregistration-draft-2026-11-17.md` in this
directory.

**Register basis.** RT-34 (NEW, register section N item 11): the
Eteocypriot pilot — source survey; syllabic representation with
uncertainty; competing bilingual alignments including the Amathus
bilinguals; falsifiable grammatical and lexical hypotheses against
held-out inscriptions; expert adjudication package; preregistered
experiment. RT-34's acceptance shape governs this proposal: the
proposal states its corpus sources' legal status, its held-out
design, and its adjudication route before any analysis runs.

## 1. What is proposed, and why this target

A pilot study of Eteocypriot, the non-Greek language of Iron Age
Cyprus written in the Cypriot syllabary, run as the first genuine
second target of the multi-script platform (the model specified at
`docs/MULTISCRIPT_MODEL.md`, Spec 095 Stage 4). The review's
argument, adopted by the register: this is the most constrained
unknown-language problem available to the program —

- the **writing system is readable**: the Cypriot syllabary's sign
  values were established in the 19th century (George Smith, 1872,
  from the Idalion bilingual) and are not in dispute, so sign shape
  and phonetic value arrive already separated — the model's G2
  separation is given by the evidence, not imposed on it;
- **bilingual evidence survives**: Greek–Eteocypriot bilingual
  texts from Amathus give the study a ground-truth-bearing
  development set (§4);
- the **language is genuinely unknown**: beyond a small vocabulary
  attested in the bilinguals, Eteocypriot's grammar and lexicon are
  not understood, so the pilot tests the platform's
  hypothesis-and-adjudication machinery where the answer is not
  already known — unlike a solved-script benchmark (the Meroitic
  scoping, T502, tests the complementary property: pipeline
  fidelity where the answer *is* known).

The pilot's first useful result, in the review's framing, would be
one independently reproducible grammatical constraint or one newly
supported lexical interpretation — not a claimed translation.

## 2. Instantiation against the multi-script model

The pilot instantiates `docs/MULTISCRIPT_MODEL.md`; it builds no
Eteocypriot-specific machinery. Sketch of the instantiation (the
census-proven mapping table is execution work, under the model's
§5 contract):

| Entity | Eteocypriot instantiation (sketch) |
|---|---|
| WritingSystem | The Cypriot syllabary (Iron Age), identified independently of any language hypothesis |
| LanguageHypothesis | "Eteocypriot" — the non-Greek language of the Amathus-centred corpus; the Golgoi material carried as a separate, possibly distinct LanguageHypothesis (§3.4); the nonlinguistic position is not live for this corpus but is carried by the same machinery |
| Corpus | The frozen corpus of §3, under an identity record per C095-3 |
| Artifact | The inscribed objects (statue pedestals, the lost bilingual slab, vessels, handles); the bilingual slab is an Artifact whose only surviving Transcription basis is a 1914 photograph (§3.3) |
| Inscription | One written act per object, damage and completeness as recorded by the edition of record |
| Sign | Syllabary signs under the Common frame (§4.2) |
| SignVariant | Common vs Paphian groupings, preserved as frames, never silently resolved (G4) |
| Transcription | The editions of record (§3.2), each a named Transcription with its basis; Perna 2019 supersedes Masson for ICS 194/195 without deleting Masson (append-only) |
| ReadingHypothesis | Sign values are *not* hypotheses here — they are the deciphered syllabary; what is hypothesized is morpheme segmentation and grammatical function, carried as ReadingHypotheses over sign sequences |
| TranslationHypothesis | Lexical and grammatical interpretations, never stronger than the weakest reading they rest on (ME-10) |
| Context | Site (Amathus, Golgoi), period (chiefly 4th c. BCE), object association, from the editions |
| Evidence | Pinned by hash under Spec 094's evidence standard, in its registered classes (§6) |
| Claim / Falsifier / Experiment / Execution / Result / Adjudication | The program's existing machinery, unchanged |

## 3. Corpus: source and legal status

### 3.1 What the corpus is

The Eteocypriot-defining corpus is small: **between 20 and 30
inscriptions** show the features that define "Eteocypriot"
(Steele 2013, as reported in the Ancient Cyprus compendium's
writing-and-literacy survey), most of them from **Amathus**, with
a few short inscriptions from **Golgoi** (modern Athienou). The
language is attested from roughly the 10th to the 4th century BCE
and is extinct by about the 4th century BCE; the defining corpus
is chiefly 4th century. Several hundred further syllabic
inscriptions cannot be interpreted as Greek, but non-Greek
content is not thereby proven for each of them — the corpus
delimitation is a design decision (§3.4), not a given.

### 3.2 Editions of record

- **Masson, *Les inscriptions chypriotes syllabiques* (ICS)** —
  Olivier Masson, *Les inscriptions chypriotes syllabiques:
  recueil critique et commenté*, Études chypriotes 1 (Paris: E.
  de Boccard, 1961; reprinted with supplement, 1983). The corpus
  of record for the syllabic inscriptions, Eteocypriot included:
  the Amathus bilingual is **ICS 196** (1983 ed., pp. 206–209);
  the long Amathus Eteocypriot text is **ICS 194/195**.
- **Perna 2019** — Massimo Perna's new edition of ICS 194/195,
  made from autopsy in the Louvre, with a high number of improved
  readings (as reported in Egetmeyer's 2016–2020 report on the
  Cypriot syllabic inscriptions, *Ariadne*). For those two texts,
  Perna 2019 — not Masson — is the reading of record.
- **Inscriptiones Graecae XV 1.1 (IG XV 1,1)** — the successor
  Cypro-Greek syllabic corpus by Egetmeyer, Karnava, Landenius
  Enegren and Perna; its first part is published and covers
  Amathus, Kourion and Marion — i.e., it includes the principal
  Eteocypriot-bearing city. Where IG XV 1,1 covers a text, it is
  the edition of record at execution.
- **Perna 2015** — Massimo Perna's consolidated and corrected
  corpus of the Cypriot syllabary, totalling 1,397 inscriptions
  (all syllabic texts, Greek and non-Greek): the delimitation
  reference for the wider syllabic corpus from which the
  Eteocypriot stratum is drawn.

### 3.3 Legal status, stated plainly

- The inscription **texts are ancient** (1st millennium BCE). No
  copyright subsists in the ancient wording as such.
- The **critical editions are modern copyrighted scholarship**:
  Masson's ICS (de Boccard), Perna's editions, and IG XV 1,1
  (Berlin-Brandenburg Academy / De Gruyter) carry their editors'
  and publishers' rights in the readings, apparatus, commentary,
  drawings and photographs. A reading is a scholarly act (a
  Transcription, in the model's terms), and the program may not
  redistribute an edition's text, apparatus or images as its own.
  Scholarly use with citation — transcribing sign sequences for
  analysis and publishing derived statistics and the program's
  own hypotheses — is the use this proposal contemplates; bulk
  republication of an edition is not.
- The **Amathus bilingual's stone is lost**. Found in a Limassol
  antique shop in 1913/1914 and published by Sittig in 1914, the
  black marble slab, broken in two, was subsequently lost —
  possibly during transport to America (Sittig, as reported by
  Masson; the loss is recounted in Woudhuizen 2012). No autopsy
  of the pilot's anchor text is possible, ever: ICS 196 rests on
  Sittig's 1914 photograph and Masson's treatment of it. The
  corpus identity record must carry this provenance fact on its
  face; a reading dispute over the bilingual cannot be settled
  against the stone.
- **Photographs and drawings** of the surviving objects belong
  to their holding institutions (the Louvre holds ICS 194/195's
  object; other objects sit in the Cyprus Museum, the British
  Museum, the Ashmolean and elsewhere) under each institution's
  reproduction terms. This proposal requires no image
  redistribution; if execution ever does, permissions are an
  execution-stage task, owner-approved.
- **No openly licensed machine-readable Eteocypriot corpus was
  found** by this scoping's survey (two search phrasings across
  general web sources, 2026-11-17). That is a survey result, not
  proof of absence: **UNVERIFIED as a negative.** The execution
  commission's first task is a dedicated corpus-availability
  survey (including the IG digital platform's terms for IG XV,
  which are likewise **UNVERIFIED** here) before any intake.
- Until a corpus is acquired and pinned, there is nothing to
  analyse — which is the correct state for a scoping: the
  fail-closed corpus discipline (C095-3) applies from intake:
  version, content hash, source, licensing terms, counts under a
  named basis, normalization rules, and orientation basis (the
  syllabary runs right-to-left for these texts; orientation is
  carried as data, per C095-10) recorded before any loader runs.

### 3.4 Corpus delimitation decisions the design fixes now

1. **Primary stratum: Amathus.** The bilingual-bearing and
   longest-attested material. The Androkles dedications and ICS
   196 are Amathus; ICS 194/195 are Amathus.
2. **Golgoi is a separate stratum, not merged.** Egetmeyer has
   suggested the Golgoi short inscriptions' language may differ
   from Amathus's ("Golgian"). Merging them silently would be a
   contamination shape (the same data under an assumed identity);
   the design carries Golgoi as its own stratum, includable only
   as a registered sensitivity.
3. **Uninterpreted syllabic inscriptions are not Eteocypriot by
   default.** The several hundred non-Greek-readable texts enter
   only if the execution freeze names a delimitation rule and
   applies it mechanically.

## 4. Bilingual and sign-list basis

### 4.1 The bilingual basis (ground truth)

- **ICS 196 — the Amathus bilingual.** Eteocypriot in the
  syllabary (two lines, right-to-left) above Greek in the
  alphabet (two lines). The Greek text is an honorific: the city
  of the Amathusians honours **Ariston, son of Aristonax**. The
  Eteocypriot version names the same men in Eteocypriot form
  (*a-ri-si-to-no-se*, *a-ra-to-wa-na-ka-so-ko-o-se*) and is
  roughly **twice as long** as the Greek: the two versions are
  broadly corresponding, **not literal translations of one
  another** (Woudhuizen 2012; Steele 2013). Any alignment method
  that assumes sentence-by-sentence equivalence is wrong for
  this text by design; the preregistration carries competing
  alignment assumptions for exactly this reason. Dating: second
  half of the 4th century BCE on script features (Sittig, via
  Masson); a "ca. 600 BC" date circulates in popular sources and
  is **not** the scholarly edition's dating — the discrepancy is
  recorded here so it cannot propagate.
- **The Androkles dedications.** Two statue pedestals from
  Amathus (4th c. BCE) dedicated by Androkles, last king of
  Amathus, for his sons **Orestheus and Andragoras**, each
  inscribed in Eteocypriot (syllabary) and Greek (alphabet).
  A second, independent name-anchor set: the same
  known-name-recovery test the bilingual supports, on different
  objects.
- **What is NOT Eteocypriot bilingual evidence: the Idalion
  bilingual.** It is Phoenician–Greek (in the syllabary). It
  grounds the syllabary's sign *values* (§4.2); it attests no
  Eteocypriot word. Counting it as Eteocypriot evidence would be
  a provenance error of exactly the shape the contamination
  class (C095-7) exists to flag.

### 4.2 The sign-list basis

- The **Cypriot syllabary signary**: 56 signs in the standard
  count, each standing for a syllable, in two variant frames —
  **Common** and **Paphian**. Sign values were established in
  the 19th century (Smith 1872, via the Idalion bilingual) and
  refined against the Greek syllabic corpus; they are the
  field's settled basis, not a hypothesis of this study.
- The Eteocypriot texts of the primary stratum use the **Common**
  frame. The study's sign list of record is the signary as
  carried by the editions of record (Masson's ICS signary,
  superseded where IG XV 1,1 publishes its own), with Common /
  Paphian groupings carried as SignVariant frames under the
  model (G4) — never silently unified.
- Because the values are known, the study's unknowns are
  segmentation, morphology and meaning — the proposal's
  hypotheses are framed at that level (§5, and the
  preregistration draft).

## 5. Held-out design (summary; the binding form is the draft)

The corpus is tiny, so the design's first duty is honesty about
what can be tested at all.

- **Freeze first.** The corpus is intaken under an identity
  record (C095-3) and frozen; the freeze record's hash and the
  run-index discipline (Spec 089) are the seal.
- **Development set** = every ground-truth-bearing item: ICS 196
  and the Androkles pair (Greek sides known), plus the Greek
  syllabic corpus as a structural control (same script, known
  language — the control that separates "the method finds
  structure" from "the method finds *this* language's
  structure").
- **Held-out set** = all remaining primary-stratum inscriptions,
  including ICS 194/195 under Perna 2019's readings, sealed at
  freeze: predictions about held-out texts are registered
  before any held-out text is loaded into the analysis
  environment. The split is by inscription, never by line or
  sign; the one long text is its own stratum.
- **Competing alignments** for the bilingual material are
  carried as rivals (strict segment-parallel vs name-anchored
  free alignment), and every reading hypothesis faces the
  identifiability protocol (Standards of Record, Part III)
  before it can be scored SUPPORTED; NOT IDENTIFIABLE is an
  expected, respectable outcome at this corpus size.
- **Thinness floors are registered in advance.** A proposed
  morpheme or ending is scorable only if the preregistration's
  floor for its predicted held-out occurrences is met; below the
  floor the outcome class is TOO THIN — not failure, and not
  support. Reporting follows the Standards of Record, Part II
  (effect size, interval, multiplicity handling, precision
  basis; never a bare p-value), and Part I (no equivalence from
  a non-significant difference).

## 6. Adjudication route

Nothing new is built; the route is the program's existing
machinery, named end to end:

1. **Intake.** Every hypothesis enters the claims ledger through
   the sanctioned importer, in claim form — statement, falsifier
   fixed before its test, evidence references, does-not-establish
   bound (model G5 / ME-13, ME-14). Draft claims inside the
   preregistration draft are not intaken; intake is an execution
   act.
2. **Evidence.** Evidence is pinned by content hash under Spec
   094's evidence standard, in its registered classes
   (`external_corpus_record`, `published_concordance_entry`,
   `independent_expert_record`, `adjudicated_claim_dossier`).
   The editions of record enter as published concordance /
   external corpus records; no loop- or self-generated item is
   evidence for its own claim.
3. **Standing changes.** Only by recorded adjudication (ME-18),
   through the lifecycle machinery of record; promotion requires
   a named human approver from `NAMED_HUMAN_APPROVERS`
   (`backend/glossa_lab/claim_stage.py`; the owner at adoption)
   — automated actors never approve, verify or promote (Spec
   094). A reading is scored SUPPORTED only with a
   rival-construction record under the identifiability protocol
   (Standards, Part III).
4. **Expert adjudication package.** Following the review's
   Phase D: at execution, a dossier of the pilot's claims,
   evidence and rival constructions is prepared for qualified
   Cypriot-epigraphy specialists (the field of the IG XV
   editors and the Kadmos reporting line) and their responses
   enter as `independent_expert_record` evidence. **Preparing
   the package is execution work; contacting any specialist is
   an external act requiring the owner's approval at the time.**
   This scoping has contacted no one.
5. **Publication discipline.** Any public statement of a pilot
   result goes through the program's standing publication gates
   (owner approval of the actual text; the composed release
   gate, C095-14).

## 7. What the pilot would and would not establish

Would establish, if executed and if its outcomes are positive:
that the platform's machinery — corpus identity, claim form,
held-out discipline, identifiability protocol, named-human
adjudication — operates on a genuinely different research
problem without script-specific forks (the multi-script model's
first live test), and at most a small number of individually
adjudicated grammatical or lexical results about Eteocypriot.

Would not establish (C095-15's bound, carried verbatim in
substance): that Eteocypriot is tractable in general, that it is
related to any other language or script tradition, or anything —
in either direction — about the Indus script.

## 8. Open questions left for the owner

1. **Priority.** The register takes no position on sequencing
   this pilot against the adopted Indus queue (D-095-2);
   execution is a separate owner decision in any case.
2. **Corpus access.** Whether to acquire IG XV 1,1 (and on what
   terms) and whether the execution's corpus-availability survey
   may approach the IG digital platform — a licensing question
   this scoping leaves open (§3.3's unverified items).
3. **Expert outreach.** Whether, and to whom, the adjudication
   package may be sent at execution (§6.4).
4. **Golgoi.** Whether the Golgoi stratum is in the pilot's
   scope at all, or held for a later study (§3.4).

## Sources relied on, with verification state

| Source | What it grounds | State |
|---|---|---|
| Spec 095 claims.md (C095-15), tasks.md (T501), register-draft.md (RT-34), REVIEW.md §5.8/§8 | The commission, its acceptance shape, the review's pilot phases | Program record, read in the clone at `c2be9869` |
| `docs/MULTISCRIPT_MODEL.md` (Stage 4) | The instantiation contract (§5) and entity vocabulary | Program record, read in the clone |
| `glossa-indus/STANDARDS.md` Parts I–III | Reporting, equivalence, identifiability bindings | Program record, read in the clone |
| Steele, *A Linguistic History of Ancient Cyprus* (CUP, 2013), as reported by the Ancient Cyprus compendium (ancientcyprus.com, writing-and-literacy survey) | Corpus size (20–30 defining inscriptions), Amathus centre, the bilingual's name forms and relative length | Secondary report of the scholarly source; the compendium page was read in full for this scoping |
| Masson, ICS (1961; 2nd ed. 1983), via Google Books bibliographic record and Woudhuizen 2012 | ICS numbering (194/195, 196), edition identity, pp. 206–209 for the bilingual | Bibliographic facts verified; the edition itself was not opened (no copy is held) |
| Woudhuizen, "The Amathus Bilingual Inscription" (2012) | The slab's loss, its 1914 Sittig publication, 4th-c. dating, non-literal correspondence of the versions | Read in full for this scoping |
| Egetmeyer, 2016–2020 report on Cypriot syllabic inscriptions (*Ariadne*) | Perna 2019's re-edition of ICS 194/195 (Louvre autopsy); IG XV 1,1's publication and coverage | Read in full for this scoping |
| Cypriot syllabary reference summaries (Wikipedia, citing the standard literature) | 56-sign signary; Perna 2015's 1,397-inscription consolidated corpus; Smith 1872 / Idalion decipherment of values | Tertiary; used only for facts that agree with the scholarly sources above |
| The review's citation of a 2024 analysis of the bilingual (University of Liverpool repository) documenting unresolved readings | Noted as the review gives it | **UNVERIFIED** — not independently located by this scoping's searches; carried as the review's citation, not as a fact relied on |
| Existence of an openly licensed machine-readable Eteocypriot corpus; IG digital terms | §3.3 | **UNVERIFIED as negatives** — survey found none; absence from search results is not proof of absence |
