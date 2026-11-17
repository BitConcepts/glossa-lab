# Spec 095 — Stage 5 Scoping Record (T501, T502)

**Date: 2026-11-17. Commission: Stage 5's two second-target
scopings only. T503 (closeout) is NOT started by this record —
see §4. Base: origin/main `c2be9869` (the Spec 095 Stage 4
merge). Branch: `spec/095-s5-second-target-scoping`. No code was
added, changed or executed against any corpus: this stage is
documents only. No Eteocypriot analysis exists under this spec;
no Meroitic benchmark result exists under this spec.**

## 1. Placement of the deliverables, and the reasoning

The two scopings are filed in this spec's own package, at
`specs/095-red-team-remediation/second-targets/`:

- `eteocypriot-proposal-2026-11-17.md` (T501, the proposal)
- `eteocypriot-preregistration-draft-2026-11-17.md` (T501, the
  preregistration draft)
- `meroitic-benchmark-scoping-2026-11-17.md` (T502, the study
  spec)

Reasoning, following the Stage 4 placement precedent
(`docs/MULTISCRIPT_MODEL.md`): a new `specs/` directory is an
adoption act (program-map assignment and claims intake), which
neither scoping is — both are deliverables *of* Spec 095, and
C095-15/C095-16 forbid their claims from being intaken by this
spec. A `docs/` placement was rejected for the mirror reason:
these are spec records with falsifiers fixed in them, not
platform documentation, and C095-17's derived-document rule
keeps derived sets separate from records of decision. Inside
the owning spec's package, beside Stage 4's `wireframes/`, is
where this package's conventions put stage deliverables.

## 2. T501 — the Eteocypriot proposal and preregistration draft (C095-15)

**Outcome: scoped in full. No analysis executed.**

- **Corpus legal status and source, as established.** The
  Eteocypriot-defining corpus is 20–30 inscriptions, chiefly
  4th c. BCE, centred on Amathus with a Golgoi stratum (Steele
  2013 as reported). Editions of record: Masson's ICS (1961;
  2nd ed. 1983) — the bilingual is ICS 196, the long Amathus
  text ICS 194/195; Perna 2019's Louvre-autopsy re-edition
  supersedes Masson for ICS 194/195; IG XV 1,1 (published,
  covering Amathus) is the successor corpus; Perna 2015 is the
  delimitation reference (1,397 syllabic inscriptions). Legal
  status stated on the proposal's face: the ancient texts are
  uncopyrighted; the critical editions are copyrighted
  scholarship usable with citation, not redistributable;
  museum image rights are institutional; and the Amathus
  bilingual's **stone is lost** (published by Sittig 1914;
  lost thereafter, possibly in transport to America), so the
  anchor text rests on a 1914 photograph permanently.
- **What remains UNVERIFIED, labelled as such in the
  proposal:** the existence of an openly licensed
  machine-readable Eteocypriot corpus (none found by this
  scoping's survey — a survey result, not proof of absence);
  the IG digital platform's terms for IG XV; and the review's
  cited 2024 Liverpool-repository analysis of the bilingual,
  which this scoping's searches did not independently locate
  and which is carried as the review's citation only.
- **Bilingual and sign-list basis, named.** Bilinguals: ICS
  196 (Ariston / Aristonax name anchors; the Eteocypriot
  version roughly twice the Greek's length — broadly
  corresponding, not a literal translation) and the Androkles
  dedications (Orestheus / Andragoras). The Idalion bilingual
  is expressly excluded as Eteocypriot evidence (it is
  Phoenician–Greek; it grounds sign values only). Sign list:
  the Cypriot syllabary signary (56 signs, Common frame for
  the primary stratum, Paphian carried as a variant frame),
  values settled since Smith 1872. A dating discrepancy is
  recorded on the record: the scholarly edition dates ICS 196
  to the second half of the 4th c. BCE; a "ca. 600 BC" date in
  popular sources is not the edition's.
- **Held-out design.** Freeze under a C095-3 identity record;
  development set = the bilingual-bearing material + the Greek
  syllabic control corpus; held-out set = all remaining
  primary-stratum inscriptions (ICS 194/195 under Perna 2019),
  sealed at freeze, split by inscription; competing alignment
  assumptions (strict segment-parallel vs name-anchored free)
  carried as rivals; thinness floors registered in advance
  with TOO THIN as an outcome class; identifiability protocol
  (Standards Part III) before any SUPPORTED scoring.
- **Adjudication route.** The program's existing machinery,
  named end to end in the proposal §6: ledger intake in claim
  form; hash-pinned evidence in Spec 094's registered classes;
  standing changes only by recorded adjudication with a named
  human approver (`NAMED_HUMAN_APPROVERS`); an expert
  adjudication package for Cypriot-epigraphy specialists as
  execution-stage, owner-approved external evidence. No
  specialist was contacted by this scoping.
- **The preregistration draft** follows the program's
  preregistration form and states on its face that it is a
  draft — not filed, not registered, execution separately
  owner-gated. Its four draft claims (EC-D1..EC-D4) exist only
  inside the draft document and were **not** intaken into the
  ledger. It asserts no pins: there is no corpus to pin, and
  the draft says so.
- **Instantiation.** Both documents instantiate against
  `docs/MULTISCRIPT_MODEL.md` (the proposal §2 mapping sketch)
  and bind the Standards of Record Parts I–III.
- **Open questions left for the owner** (proposal §8):
  priority against the adopted queue; corpus acquisition and
  IG terms; expert outreach; Golgoi scope.

## 3. T502 — the Meroitic benchmark scoping (C095-16)

**Outcome: scoped in full, as a study spec. No execution.**

- **The existing fixture, named exactly:**
  `backend/glossa_lab/data/meroitic.py` — 19-sign inventory
  (Griffith 1911 values, ME01–ME19 in frequency-rank order),
  a 50-line / 551-token constructed formulaic corpus, a Sahidic
  Coptic LM corpus, and `get_full_answer_key()`; legacy
  benchmark `backend/glossa_lab/experiments/_legacy/
  meroitic_benchmark.py` with output of record `outputs/
  meroitic_benchmark.json`. Census re-derived at scoping from
  the module itself: 551 tokens, 50 lines, 19 signs. The
  scoping states the fixture's limit on its face: the corpus
  is constructed formulaic material, not transcriptions of
  identified inscriptions; per C095-16 the module is the
  benchmark's **starting inventory**, not its data, and the
  legacy benchmark's output is not a reproduction target.
- **The 2025 result to be reproduced, identified and cited as
  the paper gives it:** Otten & Anastasopoulos, "Towards
  Ancient Meroitic Decipherment: A Computational Approach",
  ALP workshop at NAACL 2025, pp. 208–219, ACL Anthology
  2025.alp-1.11, DOI 10.18653/v1/2025.alp-1.11 — read in full
  for this scoping. **Citation correction recorded:** the
  review's source page cited this work via a Wiley-hosted
  link; the work is the ACL paper above. The review's
  substance (a 2025 computational paper providing a
  machine-readable corpus and baseline alignment work)
  matches the identified paper. Published targets named in
  the scoping: Table 1 (193 / 897 / 302 / 708); §5.3 counts
  (871 phrases pre-augmentation; Egyptian 1,729 types /
  99,338 tokens; post-augmentation 1,868 forms / 17,257
  phrases / 782,761 words); Table 2 dictionaries (26/18/15/
  14/9/6/3); §6/§6.2 alignment headlines (0% unseen; ≤20%
  training, best = numerals at 100d; French–English skyline
  70% / ~68%); the REM limitation (1,000+ inscriptions as
  images requiring transcription).
- **Success criteria, fixed in the scoping** (three legs):
  Leg A (census) — all ten counts reproduced exactly, or each
  divergence named with its cause; Leg B (sign-frequency and
  positional) — attested sign set equals the fixture's 19
  after explicit reconciliation of the paper's `E`-for-/o/
  convention, and computed frequency ranks agree with the
  fixture's ME rank order at Spearman ρ ≥ 0.90, positional
  distributions computed and archived; Leg C (alignment) —
  unseen-dictionary precision@10 = 0%, training-dictionary
  accuracy ≤ 25% band, numerals best-or-tied at 100d, all
  under the paper's hyperparameters with attempts accounted.
- **Falsifier, fixed in the scoping:** the benchmark's premise
  is falsified if Leg A fails on a majority of its counts with
  divergences tracing to the published corpus or the paper's
  stated methods (by re-derivation), or if the corpus
  repository is unavailable or unlicensable at step 0 — the
  outcome record then being NOT REPRODUCED / NOT EXECUTABLE
  AS SCOPED.
- **An interpretation, flagged in the scoping (§2) rather than
  hidden:** the paper publishes no sign-frequency or
  positional tables, so C095-16's "sign-frequency and
  positional results" is mapped onto Legs A–C as stated; a
  narrower owner reading drops Leg B to an extension and
  leaves Legs A and C intact.
- **What execution would require:** a separate owner
  commission; step-0 pinning of the corpus repository by
  commit with its license recorded and a C095-3 identity
  record before any computation; the independence rule (the
  program's own implementation from the paper's stated
  methods; the authors' code readable for the mapping scheme
  only, with readings recorded); Spec 089 run discipline;
  Standards Part II reporting. **UNVERIFIED at the repository
  itself:** the corpus repository's license and current
  commit — not visited by this scoping (no corpus
  acquisition), and named as execution step-0 acts.

## 4. T503 — NOT started, and the remainders it must carry

T503 (closeout: register re-checked against C095-1; every
claim discharged or carried as a named remainder) is expressly
outside this commission. It follows the resolution of the
Stage 4 remainders, which are still open at this writing:

1. **C095-12, build half** — T403 unticked: the dashboard home
   and feature set stand at wireframes (Stage 4), awaiting the
   owner's approval of the wireframes by name; the build, and
   the Playwright verification the claim requires, do not
   exist yet.
2. **C095-13** — T404 unticked: the audit package's verdict is
   FAIL (thresholds F2, P1, A2 unmet), with remainders (the
   dashboard leg after the T403 build; the authenticated legs
   on the owner's sessions) and its remediation undecided.
3. **The T303 remainder** — the Stage 3 identifiability
   application re-stated the six anchors' standings in its
   application record, but the ledger mutation was not
   performed: as the Stage 3 record states, a vehicle that can
   carry anchor standings as acts does not yet exist. The
   closeout must carry this remainder by name.
4. **The RT-03 README item** — the supersession banner on the
   anchor-model README remains an owner-gated micro-task
   (D-095-5), outside this spec's stages; it is also the
   standing failure of the composed release gate's
   public-claims component (Stage 4 record: the real-candidate
   run's public-claims component FAILS with RT-03
   outstanding).

The closeout, when commissioned, must also re-check this
record's two scopings against C095-1 (no duplicate worked
twice — T501/T502's targets are register NEW items 11 and 12;
no NEW item lost — items 1–10, 13, 14 are discharged by Stages
1–4 as their records state, subject to the remainders above).

## 5. Claims discharged by this stage

- **C095-15 — discharged (scoping).** The draft exists and
  states the corpus's legal status and source, the bilingual
  and sign-list basis, the held-out design, and the
  adjudication route, before any analysis exists; no
  Eteocypriot analysis output exists under this spec (the
  stage adds three documents and a tasks tick, nothing else —
  verifiable from the commit's file list). The claim's
  falsifier is checked and does not fire.
- **C095-16 — discharged (scoping).** The reproduction
  benchmark is scoped as a study spec on the existing fixture
  as its starting inventory, with success criteria and a
  falsifier fixed in the scoping document (§3 of the scoping,
  summarized in §3 above); no Meroitic benchmark result was
  produced as a stage task of this spec. The claim's falsifier
  is checked and does not fire.

Discharge here is of the *scoping* claims as written: both
claims govern what enters under this spec, and both reserve
execution to a separate owner decision. Nothing in this stage
commissions, schedules or pre-approves either execution.

## 6. Gates and tests (local readings; no CI claim)

Ledger gates, run sequentially on the quiet final tree of this
change, verbatim:

```
--all:           summary: 29 PASS / 0 FAIL / 1 NOT-RUN
                 RESULT: PASS
--regen:         summary: 32 PASS / 0 FAIL / 0 NOT-RUN
                 RESULT: PASS
--contamination: contamination class (Spec 095 T301, C095-7): 1025 presentations scanned, 0 flag(s)
                 CONTAMINATION: PASS
```

The standing gate profile holds exactly. In-tree
regenerations from the gate runs were restored; `git status`
afterwards shows only this stage's intended files.

Targeted conformance set (this stage adds no code, so the
requirement is the conformance set that enumerates `specs/`
and the map/ledger surfaces, per the commission):
`test_program_map_conformance.py`,
`test_spec088_program_map.py`, `test_manual_conformance.py`,
`test_policy_sync_conformance.py`,
`test_spec095_stage4_instantiation.py`,
`test_spec095_contamination_gate.py` — **72 passed** in
15.65s (box venv `glossa-ci`), with no side-effect files left
in the tree. No full-suite run was made and none is claimed;
the full union is CI's on the PR.

## 7. Deviations

- **The review's Meroitic citation was corrected, not
  followed.** The review's source page pointed at a
  Wiley-hosted link for the 2025 Meroitic paper; the work is
  Otten & Anastasopoulos 2025 in the ACL Anthology
  (2025.alp-1.11). The correction is recorded in the scoping
  document and in §3 above; the review itself, a preserved
  external record, was not edited.
- **C095-16's "sign-frequency and positional results" needed
  an interpretation** (the paper publishes no such tables).
  The interpretation is stated openly in the scoping (§2) and
  flagged as an open question for the owner, rather than
  silently resolved.
- **Two source-level imperfections were recorded rather than
  smoothed over:** the Amathus bilingual's popular "ca. 600
  BC" dating against the edition's 4th-century dating
  (proposal §4.1), and the review's 2024 Liverpool-repository
  citation, which this scoping could not independently locate
  and carries as UNVERIFIED.
- No other deviations. No frozen record was modified; the
  live origin was never touched; the backend was never
  restarted; the research loop was not run; nothing was
  downloaded; no one was contacted.
