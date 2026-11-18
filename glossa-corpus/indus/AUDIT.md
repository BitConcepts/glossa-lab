# Audit of the Indus decipherment paper, v10 → v11 draft — 2026-11-18

**Paper:** "A Falsifiable Computational Decipherment Hypothesis for the
Indus Valley Script: 161 Candidate Proto-Dravidian Anchors and a
Three-Slot Positional Grammar", Tristen Kyle Pierson.
**Version audited:** Preprint v10, Zenodo record 23977473 (created
2026-11-05), concept DOI 10.5281/zenodo.20379070.
**Files audited** (downloaded from the record 2026-11-18, MD5 verified
against the record before work began):

- `pierson_2026_indus_decipherment.tex` — 155,460 B, md5
  `c0135fa99c3984b5083314cfdfaa3a18` ✓ (record's checksum)
- `pierson_2026_indus_decipherment_preprint_v10.pdf` — md5
  `9eefb62473233d1fa8c330e6085e2b3c` ✓
- `v10_version_note_2026-11-05.md` — md5
  `810ddf94317f8e3a8b2ef5c16055d9c5` ✓

**Audit standard (records read, in the order given):**
`files/PROGRAM-STATE.md` (goal workspace); the repo
BitConcepts/glossa-lab on main via the GitHub API —
`glossa-indus/map/gap-register.md`; Spec 091 records (stage-1 record,
stage-2 record, stage-2 supplement record,
stage-3-battery-v2-record-2026-11-17.md,
t302-reclassification-acts.json); Spec 095 records (stage-3 record,
t303-identifiability-application-2026-11-16.md); Spec 090 records
(stage-g3-outcome-record.md, stage-g3-audit-record.md); and, for the
fifth item, the acts and stage record on PR #588's branch
`feat/091-s3-single-line` (t303-reclassification-acts.json,
stage-3-single-line-record-2026-11-18.md), read from that branch
because the PR was still open at audit time. Cross-checks: the live
public tracker page (bitconcepts.tech/research/indus-script/,
fetched 2026-11-18) and the program's papers inventory
(`~/workspace/research_notes/papers-management/inventory.md`, read
2026-10-13, corrected 2026-10-25).

**Headline counts: 41 statement blocks checked — 39 STILL ACCURATE,
2 SUPERSEDED, 0 CONTRADICTED.** Both superseded blocks sit in §5 and
both are corrected in the v11 draft. Nothing was published; this
audit and the draft are working papers only.

---

## 1. Statement-by-statement audit

Verdicts: **STILL ACCURATE** = the current record supports the
statement as written. **SUPERSEDED** = true when deposited, no
longer the program's standing; corrected in v11. **CONTRADICTED** =
the current record shows the statement is wrong.

### Title block and front matter

| # | Statement (location) | Verdict | Record |
|---|---|---|---|
| 1 | Title: "161 Candidate Proto-Dravidian Anchors and a Three-Slot Positional Grammar" | STILL ACCURATE | The 161 set is the paper's subject and the deposit title of record (Zenodo record 23977473 metadata, read 2026-11-18). The v10 head note governs how the figure is read. PROGRAM-STATE standing state: the audited census is 287 recorded anchors / 94 strict; the title's 161 is the paper's own set, not the census. |
| 2 | Head note (added in v10): the 161 readings are no longer the headline set; the headline set is the strict core of 94; results about the 161 stand as the record of that set; the script remains undeciphered | STILL ACCURATE | PROGRAM-STATE (standing state; standing bars: "the Indus script is not deciphered"). One element is completed by later work — the note points to §5 for the re-grading, whose numbers are superseded (row 36); v11 adds one sentence to the note recording that the revalidation has since been carried out for 33 of the 37 flagged readings. |
| 3 | "Version: Preprint v10"; "Date: May 2026 (revised October 2026)" | Mechanics, not a finding | Restated for the draft in v11 (v11 draft label; revised November 2026). No factual claim. |

### Abstract

| # | Statement | Verdict | Record |
|---|---|---|---|
| 4 | Corpus: Holdat LLC Indus Corpus V3 — 1,670 seals, 9 sites, 390 distinct signs, 7,002 sign tokens, Mahadevan M-numbers | STILL ACCURATE | Spec 091 stage-3 records pin the same corpus by hash (corpus `62d14d2b…`); the T303 foundation check reads the staged corpus as 1,670 seals / 7,002 tokens / 390 signs (PR #588 handoff record; stage-3-single-line record). |
| 5 | Robust non-random positional structure, z = 10.3, permutation statement (0 of 2,000; add-one estimate 0.0005) | STILL ACCURATE | No post-v10 record re-runs or alters the Phase-134 F1 test. Spec 095 Stage 3's orientation work recomputed the Phase-125 positional arms in both orientations and found that verdict orientation-invariant (095 stage-3 record) — a different test; no contradiction. |
| 6 | Three-slot pattern at sign level; whole-inscription match 5.1% full / 38.4% partial (Phase-133) | STILL ACCURATE | Unchanged by any later record. |
| 7 | 161 candidate readings at HIGH or MEDIUM; 90.96% of tokens; 69.8% of seals fully covered; 4 provisional; 157 readings / 90.75% without them | STILL ACCURATE | The anchor table these figures come from is unchanged: Spec 094's closeout verified the anchor files byte-identical as a boundary of record (PROGRAM-STATE, Spec 094 Stage 5), and the November disposition acts expressly live in the audit line, not the table (stage-3-battery-v2 record §2: "the frozen WP5 audit, the anchors file, and the claims ledger are unmodified"). |
| 8 | Fish-sign isolation count: 0 isolated among 113 fish-bearing seals; not fish-specific because the corpus has no single-sign inscriptions at all | STILL ACCURATE | Restated identically on the live tracker page (fetched 2026-11-18): "0 of 113 fish-bearing seals in the corpus show an isolated fish sign", stated separately from the Gulf count. |
| 9 | Correction of the earlier 268 count (107 heuristic placeholders removed) | STILL ACCURATE | Historical correction; stands as the record of the May 2026 model work. |
| 10 | 44 of 75 HIGH readings' strings appear in Parpola (1994) — appearances in his text, not a sign-by-sign check | STILL ACCURATE | This is a text-mining appearance count (Phase-159), stated in the paper at exactly that strength. It is a different instrument from the 184-entry comparison crosswalk whose eligibility classification is 0 of 184 (gap register GR-088-01) — that finding does not contradict this count, and no v10 sentence claims the crosswalk comparison as validation. The supplement (row 36 note) now verifies 9 individual attributions in Parpola's texts, including two the paper relies on: M047 mīn (§10.4) and M261 muruku (§13.1). |
| 11 | Internal consistency suite: 59 of 59 at Phase-170 (May 2026); on the October 2026 tree, 40 passed / 0 failed / 8 warnings | STILL ACCURATE | Dated statements about named suite states; both stand as recorded. (The program's current foundation check reports 17/17 PASS in the November 2026 records — a later state of a changed suite; the abstract's dated claims are not affected.) |
| 12 | "Dravidian superiority over proto-Munda has not been formally quantified" | STILL ACCURATE | No later record quantifies it; §4.4's mixed-comparison statement stands with it. |

### §1 Introduction

| # | Statement | Verdict | Record |
|---|---|---|---|
| 13 | §1.3 component list (161 set and coverage; the 43 SA+DEDR bound; three-slot grammar; M374/M351 DEDR basis; fish count; M267 correction; anchor-table DEDR column 15 of 161; KL pair; Tamil-Brahmi 4 of 7; Nair 2026 framing; Parpola 44/75; Meluhhan 25-name null; blocker plausibility; 32-item synthesis; 93.2% retest) | STILL ACCURATE | Each item is the record of the May 2026 model work it cites; no post-v10 record re-runs or alters any of them. The list's M261 gloss withdrawal is consistent with the supplement's located muruku attribution (Parpola 1994 §13.1). |

### §2 Data and Methods

| # | Statement | Verdict | Record |
|---|---|---|---|
| 14 | §2.1 corpus and catalogue: 390 attested signs; anchor table covers all 397 catalogue signs; 7 catalogue-only signs named | STILL ACCURATE | Same corpus pins as row 4; catalogue arithmetic unchanged in every later record. |
| 15 | §2.1: the earlier Zipf exponent of about 1.7 is withdrawn as evidence that the script is a language | STILL ACCURATE | Stands; §2.1.1's registered test is the replacement treatment (row 16). |
| 16 | §2.1.1: the registered frequency-curve test (Spec 068) — fit values, comparison systems, verdict UNINFORMATIVE; the four exponents must not be compared | STILL ACCURATE | PROGRAM-STATE baseline: "Spec 068 stands" (052 INCONSISTENT; 054r2 NOT SUPPORTED; 068's comparison uninformative). No later record changes it. |
| 17 | §2.1: "25-entry Mahadevan–Parpola crosswalk … for iconographic anchor validation" | STILL ACCURATE | The file named is the 25-entry crosswalk used in the paper's own work — a different file from the 184-entry comparison crosswalk. See the omission note after this table. |
| 18 | §2.2 confidence criteria (HIGH 75 / MEDIUM 86 / PROVISIONAL_MEDIUM 4 / LOW 236), incl. the stated limit that no criterion-by-criterion pass/fail is recorded for any HIGH sign | STILL ACCURATE | The anchor table and audit file behind these labels are unchanged (row 7's record). |
| 19 | §2.3 positional analysis: F1 statistic and inputs; F7 held-out check (85 of 87 signs, 97.7%, split by site) | STILL ACCURATE | No later record alters Phase-134. Orientation invariance was proven for the Phase-125 arms (095 stage-3 record), not claimed for F1, and the paper claims it for neither. |
| 20 | §2.4 SA simulation: the held-out test's agreement 0.000 and indistinguishable controls; the 43-sign SA+DEDR bound (118 signs, 85.28% if all removed) | STILL ACCURATE | The falsification of SA agreement as evidence is the premise of the strict core's definition and of every November record; nothing reinstates it. |
| 21 | §2.5 substrate analysis: M374/M351 rest on DEDR 1709 / 5388; a Munda derivation was proposed but not established | STILL ACCURATE | Unchanged in all later records. |

### §3 Results

| # | Statement | Verdict | Record |
|---|---|---|---|
| 22 | §3.1 confidence table (75 HIGH / 82 MEDIUM / 4 provisional / 86 MEDIUM incl. / 236 LOW; H+M 161; 90.96%; 6,369 of 7,002 tokens) | STILL ACCURATE | Anchor-table figures; table unchanged (row 7). |
| 23 | §3.2 three-slot grammar and slot examples | STILL ACCURATE | Model statements, unchanged. Reader's note: two Slot-3 examples (M176, M342) are strict-core anchors whose audit grade changed in November 2026 (row 36); their readings and their places in this paper's tables are unchanged — the grade lives in the audit line, not the table. The v11 §5 text says this in so many words. |
| 24 | §3.2.1: the registered Farmer-pattern test (Spec 052) — both conditions present; outcome INCONSISTENT | STILL ACCURATE | PROGRAM-STATE baseline: Spec 052 INCONSISTENT. |
| 25 | §3.3 selected readings table and preamble (incl. M342/M176 resting on the audit file's recorded iconographic + distributional pair; M176's 94% not meeting the >95% criterion) | STILL ACCURATE | The "audit file" here is the anchor status audit behind the table — a different record from the support audit behind §5 — and it is unchanged. |
| 26 | §3.4 M267 correction: 400 tokens across all nine motif types; chi-square 12.98, p = 0.1124; M047 is the fish sign | STILL ACCURATE | Consistent with the supplement: M047's value mīn is now located in Parpola 1994 §10.4 (pp. 194–195) and fig. 15.2 no. 1 — the crosswalk verification the paper cites now has a primary-source pinpoint behind it. |
| 27 | §3.5 fish-sign isolation test, incl. the closing paragraph naming the registered fish-family follow-up as executed — held under the Roif gate, results not stated | STILL ACCURATE | The held standing is unchanged in every later record; the study is still named only in the permitted form, and the paper states no result from it in either direction. |
| 28 | §3.6 seal coverage statistics (1,165 fully covered, 69.8%; 505 blocked; the 18 signs / 92 tokens) | STILL ACCURATE | The live tracker carries the same figures, labelled as history of the 161 set (fetched 2026-11-18). |
| 29 | §§3.7–3.21 results block (collocate network; iconographic cross-encoding; the registered animal-openings test, NOT SUPPORTED; blocking signs; CISI comparison and Nair 2026; phonological exclusivity, INCONCLUSIVE; formula clustering; polysemy null, INCONCLUSIVE; site KL bootstrap; Shu-ilishu; sibilant inventory; V12 unresolved; Tamil-Brahmi 4 of 7 and the 23.4% V07 rate; Gulf text search; Wells & Fuls mining; Mahadevan mining) | STILL ACCURATE | No post-v10 record re-runs, corrects, or supersedes any of these. PROGRAM-STATE baselines confirm the registered outcomes among them (074 NOT SUPPORTED). |
| 30 | §3.22 Parpola 1994 reading overlap count, 44/75 (59%), stated as appearances, not cross-validation | STILL ACCURATE | See row 10. |
| 31 | §§3.23–3.31.1 results block (Mahadevan per-paper counts; literature extraction ceiling; sibilant exploratory promotions; Meluhhan matching nulls; sibilant DEDR check; decode-blocker plausibility; master evidence synthesis, 32 items; grammar variance retest 93.2%; the registered depicted-kinds test, family IN QUESTION) | STILL ACCURATE | No later record alters any of these; PROGRAM-STATE baseline confirms the depicted-kinds study's standing (075: family not falsified, no kind supported). |

### §4 Discussion

| # | Statement | Verdict | Record |
|---|---|---|---|
| 32 | §4.1–4.3: illustrative seal readings under the model; the substrate scenario stated as speculation; the 18 signs resisting promotion | STILL ACCURATE | Model-internal statements with their caveats printed; unchanged. (For M329's appearance in the 18, see open question 1.) |
| 33 | §4.4 limitations (no bilingual text; corpus size; single corpus; SA training set not reconstructible; confidence standards uncalibrated; language-family baseline comparisons mixed) | STILL ACCURATE | Every limitation stands; the November work adds one the section does not name — the etymological dataset behind one battery leg is not held (row 36) — which v11 states in §5 where that leg's outcome is reported. |
| 34 | §4.5 validation path (bilingual discovery; Gulf material complete with no counterexample and no confirmation; radiocarbon direction not yet a test) | STILL ACCURATE | Unchanged standings. |

### §5 Conclusion

| # | Statement | Verdict | Record |
|---|---|---|---|
| 35 | The Tier 2 sentence and tier definitions: the 161 candidate readings are Tier 2 claims supported by multiple tests, with the printed caveats (tests not independent; labels uncalibrated; V12 warning and 23.4% V07 rate carried) | STILL ACCURATE | A claim about the 161 set as constituted; the audit-line work grades the strict core, a different set, and does not re-grade the 161 (both revalidation records state this boundary). |
| 36 | The qualification paragraph (added in v10): of the 94 strict-core readings, 6 independently supported / 46 internal only / **37 require revalidation** / 3 expert-pending / 2 insufficient; "only 52 of the 94 as supported at all; the remaining 42…" | **SUPERSEDED** | The 37 have been re-tested. (i) The 28 battery promotions were re-run under a rebuilt battery with the pass-by-default paths removed: **19 → supported on internal evidence only, 9 → insufficient evidence** (M328, M059, M162, M233, M336, M012, M305, M039, M077 — including all 3 promotions that had stood on defaults alone); the old battery's output was retired as evidence for all 28; the etymological-dataset leg could not be run because that dataset is not held, so no reading could earn its credit (stage-3-battery-v2-record-2026-11-17.md §2, §4; t302-reclassification-acts.json: 19/9 counted from the filed acts). (ii) The 5 single-line anchors were re-tested with the corrected site-statistics checker: **all 5 → insufficient evidence** — M042, M046, M108 on insufficient data; M176 (χ² = 22.8589, df 14, p = 0.0626) and M342 (χ² = 25.2468, df 16, p = 0.0656) on difference-not-detected, which under the program's standards cannot re-earn support (t303-reclassification-acts.json on PR #588's branch, read from the filed acts; lands with PR #588). (iii) The remaining **4** (M087, M165, M264, M311 — the crosswalk/literature-import group) still require revalidation (gap register GR-088-03's routing: 37 = 28 + 5 + 4). **Current picture: 6 independently supported / 65 internal only / 4 require revalidation / 3 expert-pending / 16 insufficient; 71 of 94 supported at all.** Cross-check: the live tracker's current-status section states the intermediate (post-re-run, pre-checker-arm) picture as 6 / 65 / 9 / 3 / 11 — the same arithmetic with the 5 still in revalidation. |
| 37 | §5's presentation of the six independently supported readings as the audit's last word on them | **SUPERSEDED** (incomplete standing) | The six were put to the program's identifiability protocol (2026-11-16): **all six readings NOT IDENTIFIABLE** — M044 ku; M047 mīn (the value is not identifiable; the meaning 'fish' carries the one discriminating observation of the six); M124 kuTam; M202 can (the sibilant class is discriminated by the Shu-ilishu slot; the value is not); M329 poṇ; M330 can (t303-identifiability-application-2026-11-16.md; Spec 095 stage-3 record). The application expressly leaves the support classifications unchanged and does not disprove any reading; it records that the evidence does not exclude the rival constructions. The paper, deposited 2026-11-05, predates the test and cannot state it; a current version must. |
| 38 | §5 closing: the evidence favours a Proto-Dravidian reading framework under the tested assumptions; ICIT is the immediate priority; the script is not claimed deciphered | STILL ACCURATE | Standing position unchanged in every later record. |

### §6 and appendices

| # | Statement | Verdict | Record |
|---|---|---|---|
| 39 | §6 data availability and the pin text (v10 text on branch `preprint-v10-corrections-prep`, commit `47639918`) | STILL ACCURATE for v10 | Deposit mechanics of the v10 round (v10 version note). In the v11 draft the passage is restated as provenance: the draft is prepared from that deposited text and has not itself been deposited. |
| 40 | Appendix A (Phase-128/129 anchor summary) and Appendix B (the 18 irresolvable signs, 92 tokens) | STILL ACCURATE | Anchor-table records; unchanged. For M329's double appearance (Appendix B's LOW set; the support audit's six), see open question 1. |
| 41 | Appendix C foundation validation summary (59 checks May 2026 as provenance; 40 passed / 0 failed / 8 warnings on the October 2026 tree) | STILL ACCURATE | Dated statements; see row 11. |

### Omission note (no verdict — no v10 sentence asserts the contrary)

The paper nowhere reports the comparison crosswalk's eligibility
classification: of the 184 Mahadevan–Parpola comparisons, **zero are
eligible as independent validation**, and 116 carry the project's own
readings under a Parpola source label (gap register GR-088-01). The
locator work has since established what can be pointed to: in the
holdings first searched, 0 of 184 comparisons could be located in a
primary source on either reading field; with Parpola's 1994 and 2010
texts recovered and searched, **9 of 184 phonetic readings are now
located** (M047 mīn, M087 veḷ, M088 mu(m), M091 aru, M092 elu,
M175 katir, M261 muruku, M281 piḷḷai, M311 vaṭa — eight in the 1994
book, image-verified; M175 in the 2010 text), and **semantic readings
remain 0 of 184** (stage-2 record and T202 run record;
stage-2-supplement-record-2026-11-17.md §§2–4). Locatability only:
the supplement files no eligibility, disposition, or claim-standing
change, and eligibility re-derivation belongs to a later stage. The
live tracker already states the eligibility finding publicly. No v10
sentence is corrected by this — §3.22's count is a different
measurement, stated at its correct strength — but whether a current
version should carry the finding in the body is a real question for
the deposit round (open question 2). The v11 draft therefore does
not add it; it records the located passages only where they bear on
the four readings still requiring revalidation (§5).

### Checked and absent (no correction owed)

- **The 605 and 185 framings do not appear in v10.** Full read plus
  text search: no "605", no 185-readings claim. (605 was the rejected
  SSRN draft's framing, never posted; 185 was the v3.0.0 title line.
  Both are superseded in the lineage and neither survives in the
  deposited text.)
- **The 287-anchor census is not stated in the paper.** The paper's
  sign universe is the 397-sign catalogue; the strict core of 94 is
  stated and current (rows 2, 36).
- **The claims-ledger census is not stated in the paper.** Current
  record: ledger 1,025 lines; **994 claims across 96 studies**;
  standings 2 positive / 6 negative / 986 remaining (PROGRAM-STATE
  2026-11-18; contamination gate scanned 1,025 presentations, 0
  flags). It is stated on the live tracker. Nothing in the paper
  needs correcting for it.
- **The framework generalization study (Spec 090, G3) is not
  mentioned in the paper and does not touch it.** G3 closed
  2026-11-12: outcome SEPARATED, independent audit CONFIRMED, its
  headline claim carried at capped strength, and its outcome record
  states expressly that it "establishes nothing about the Indus
  script, which remains undeciphered" (stage-g3-outcome-record.md
  §§4–6; stage-g3-audit-record.md: "Overall audit verdict:
  CONFIRMED").
- **The 2026-11-18 sign result** (the sign numbered 900 in Parpola's
  system, identified with a Mahadevan-catalogue sign and found not
  to behave like a numeral sign; published as a tracker article)
  contradicts no v10 statement: the paper makes no claim about that
  sign (full-text search: no occurrence).
- **Citations:** still zero (OpenAlex cited_by_count 0; DataCite
  citationCount 0 on the concept, v9, and v10 DOIs — PROGRAM-STATE,
  verified 2026-11-15). The paper claims no citations; consistent.

---

## 2. Places inventory — where the paper currently lives

| Place | What is there | Current version state |
|---|---|---|
| **Zenodo** (canonical) | The deposit chain under concept DOI 10.5281/zenodo.20379070: source .tex, PDF, and a version note per version | **v10 is current** — record 23977473, DOI 10.5281/zenodo.23977473, created 2026-11-05 (this audit's subject). Chain read from the Zenodo versions API 2026-11-18: v10 (23977473) ← v9 (23668053, 2026-10-26) ← v8 (23604590, 2026-10-23) ← 5.2.0 (23520218) ← 5.1.0 ← 5.0.0 (23351365, 2026-10-13) ← 4.10.0 and earlier back to 1.0 (20379071, 2026-05-25). |
| **ResearchGate** | Publication 405297740, full text posted | **Behind — at v5.0.0.** Refreshed 2026-10-13 (owner's signed-in browser): title, displayed DOI (10.5281/zenodo.23351365), description (correction notice + v5 abstract), and rendered full text all match Zenodo v5.0.0, verified by first-hand re-read after saving. **Residual:** the superseded v3 file remains attached as a second public file — the publication page exposes no per-file removal control. Canonical has since moved v5.0.0 → v8 → v9 → v10; none of those is posted there. (Papers inventory §1, corrected 2026-10-25; the page has not been re-verifiable from this machine since 2026-10-13 — see open question 3.) |
| **GitHub** | BitConcepts/glossa-lab — the living source: data, code, study records, and the release files that feed each Zenodo version | Live; source of truth for content. The v10 paper text is on branch `preprint-v10-corrections-prep`, commit `47639918` (the paper's §6; v10 version note). |
| **BitConcepts tracker page** | bitconcepts.tech/research/indus-script/ — the program's public tracker: current-status section, verdict board, dated research articles | Not a copy of the paper; it presents the program's current standings and supersedes the dated articles' evidential wording. Fetched 2026-11-18: its re-grading counts (6 / 65 / 9 / 3 / 11) reflect the record after the November 17 re-run and **before** the checker-arm leg (which moves 5 from revalidation to insufficient: 6 / 65 / 4 / 3 / 16). Its ledger sentence (994 claims / 96 studies) is current. Its method-study paragraph predates the framework study's separator-test closeout. |
| **OSF** | Registrations for individual studies the paper cites (the frequency-curve test, the Farmer-pattern test, the animal-openings test, the depicted-kinds test, and others) | Provenance records for those studies, each frozen before its run. The paper itself is not an OSF item. |
| **SSRN** | Abstract ID 6827038 — an earlier, larger draft ("…605 Proto-Dravidian Sign Readings…") | **Rejected by SSRN 2026-06-06; never posted.** Closed — history only. (Papers inventory §1.) |
| **Academia.edu** | No copy found | None found in the record (papers inventory §1, 2026-10-13); the owner had left the platform. Any copy uploaded by the owner manually in November 2026 would postdate these records. |
| **arXiv** | None of the author's | The arXiv identifier in earlier versions' metadata (2604.17828) is another author's scorecard study, cited by the paper as a work, not a supplement; the relation was corrected to *cites* in v5.0.0. |

---

## 3. Open questions (not resolvable from the record read)

1. **Per-sign label tension between two records.** The paper's
   Appendix B lists M329 among the 18 LOW signs resisting promotion,
   and §§2.2/3.27 carry M202 and M330 as PROVISIONAL_MEDIUM; the
   support audit and the identifiability application treat M329
   (poṇ), M202 (can), and M330 (can) as three of the six
   independently supported strict-core readings. The records keep
   the two vocabularies apart on purpose (anchor-table confidence
   labels vs support-lineage dispositions — the identifiability
   application states the two-vocabulary rule expressly), and no
   record read reconciles the per-sign labels. The v11 draft follows
   the identifiability record's own practice: it reports the six as
   a group, under their support classification, without asserting
   table labels for them. Whether the two records should be
   reconciled sign by sign is a program question, not settled here.
2. **Whether the comparison-eligibility finding belongs in the
   paper's body.** No v10 sentence asserts the crosswalk
   comparison's validity, so no correction was owed (omission note,
   §1). The finding is already public on the tracker. Adding it to
   the paper is an authorial decision for the deposit round, not an
   audit correction.
3. **ResearchGate's present state is unverified.** The inventory's
   v5.0.0 state was verified first-hand on 2026-10-13 and recorded
   as behind on 2026-10-25; the page has not been re-verifiable from
   this machine since. Whether anything there changed after
   2026-10-25 is unknown from the record.
4. **The draft's own pin does not exist yet.** §6's pin procedure
   names a deposit-round commit; a draft has none. The v11 draft
   states its provenance from the deposited v10 text instead, and
   its word count is the draft build's measured count. Both must be
   replaced by the real pin and a re-measured count at any deposit
   round.
5. **The unheld etymological dataset.** The re-run behind row 36(i)
   could not execute its etymological leg because the dataset is
   not in the program's holdings (an unpopulated submodule pointer;
   the 2026-11-17 recovery hunt established it was never in the
   repos and is not openly fetchable under its recorded identity;
   re-derivation from public sources is an owner decision, still
   open). If the dataset is ever restored, that leg could be re-run
   and the 28 dispositions revisited; the v11 text states the leg
   as not run, at that strength.
6. **The deposited text's own study names.** The v10 text names
   its studies in the program's internal numbering throughout
   (the frequency-curve test, the Farmer-pattern test, the
   animal-openings test, the depicted-kinds test, the held
   fish-family study, and two older internal references). Those
   names are part of the deposited scholarly record, present since
   long before v10, and no audit finding required changing them;
   under the minimal-edit rule they are untouched. Every sentence
   v11 adds or rewrites is free of such references. Whether a
   de-referencing pass should be run over the paper itself, as was
   done for the program's website and articles in November 2026,
   is an owner decision for the deposit round, flagged here rather
   than taken.

---

## 4. What v11 changes (summary; the draft and its note carry the detail)

1. §5 qualification paragraph rewritten to the current record
   (row 36): 6 / 65 / 4 / 3 / 16; 71 of 94 supported at all; the
   two revalidation legs reported with their outcomes, the unrun
   leg stated, and the four remaining readings named.
2. New §5 paragraph reporting the identifiability outcome for the
   six (row 37), at its recorded strength: it does not disprove
   any reading and does not change the support grades.
3. One sentence added to the head note: the revalidation has been
   carried out for 33 of the 37 flagged readings, and the
   identifiability test has been run; §5 reports both.
4. Mechanics only: version label, date line, §6 provenance
   restated for a draft, end matter, and the printed word count
   re-measured on the draft build.

No other sentence of v10 is changed. The title, abstract, §§1–4,
§6's substance, and the appendices stand as deposited. No new
claims beyond the record; no strengthened language; the
falsifiable-hypothesis framing and the standing position — the
Indus script is not deciphered — are preserved. No sentence added
or rewritten in v11 contains a requirement reference of any kind;
the deposited text's own internal study names are untouched, for
the reason given in open question 6.
