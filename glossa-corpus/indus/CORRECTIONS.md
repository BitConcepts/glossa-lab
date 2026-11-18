# CORRECTIONS — Indus paper v11 correction round (2026-11-18)

**What this round is.** After the v11 fix round produced the final draft
(`pierson_2026_indus_decipherment_v11_final.tex`, SHA-256
`8c98ae3bf82065829eca3cb7f6d78344a91aa6ddf3fec8e15f112da479a1ebb8`), an
external review of that draft reached the program through the owner (an
independent AI reviewer, Co-scientist, whose change brief the owner
received on 2026-11-18). The program adjudicated every finding against
its own records before any text changed (`ADJUDICATION.md`, filed beside
this file: recomputation from the Holdat corpus snapshot, the comparison
records, and the study records). This round applies the corrections the
adjudication supports, plus the owner's 2026-11-18 ruling to soften the
language-family wording (Finding 5).

**Output.** `pierson_2026_indus_decipherment_v11_corrected.tex`,
SHA-256 `eaeadb50e230e6185a86070f76f160aea55b226ac5ea597cd7568b6efe82de51`;
built PDF `pierson_2026_indus_decipherment_preprint_v11_CORRECTED.pdf`,
SHA-256 `f767f5388fa3821e5bef6d09cd892e6c8480864b4e082cee18209e5fb5c5dcd2`;
40 pages; word count 22,286, printed in the paper and re-measured on the
final build by the note's method (`pdftotext | wc -w`) — printed equals
measured at the fixed point. The pre-correction final draft was left
byte-untouched (hash re-verified after the round). The §3.5
withheld-study paragraph was not touched, and nothing outside the list
below was changed.

---

## Finding 1 — the §3.3 terminal rates (adjudication: REAL, a hard numerical error)

Source records: the recomputation in `ADJUDICATION.md` Finding 1 from
the Holdat corpus snapshot (the records' own named input CSV, SHA-256
`62d14d2b…`), agreeing to the unit with `backend/reports/phase133_resolution.json`
(initial/terminal counts 12/70 and 13/68) and with the formula bigram
record `backend/reports/phase142_collocate_network.json` and its
supplemental table. No record generates the printed 96%/94%.

- **C-1 — §3.3 table, M342 row.**
  Old: "Candidate case suffix: 584 tokens, 96% of them inscription-final;
  the case-suffix label is an interpretation of that distribution, not a
  demonstrated paradigm"
  New: "Candidate case suffix: 584 tokens, 70 of them inscription-final
  (12.0%); the sign is predominantly medial (502 tokens, 85.9%), and the
  case-suffix label is an interpretation of its distribution, not a
  demonstrated paradigm"
- **C-2 — §3.3 table, M176 row.**
  Old: "Candidate masculine suffix: 356 tokens, 94% of them
  inscription-final; the gender label is likewise an interpretation of
  distribution. HIGH on the audit's recorded iconographic +
  distributional evidence pair (see the note above); the 94% figure
  alone does not meet the >95% terminal-marker criterion"
  New: "Candidate masculine suffix: 356 tokens, 68 of them
  inscription-final (19.1%); the sign is predominantly medial (275
  tokens, 77.2%), and the gender label is likewise an interpretation of
  distribution. HIGH on the audit's recorded iconographic +
  distributional evidence pair (see the note above); the 19.1% figure
  is nowhere near the >95% terminal-marker criterion"
- **C-3 — §3.3 prose above the table.**
  Old: "but M342 and M176 rest substantially on their terminal
  distributions, and M261's row rests…"
  New: "but M342 and M176 rest substantially on their positional
  distributions (both signs are predominantly medial: M342 in 502 of
  its 584 tokens, 85.9%; M176 in 275 of its 356, 77.2%), and M261's row
  rests…"
  And the caution sentence —
  Old: "And M176's printed terminal figure — 94% of its 356 tokens
  inscription-final — does not by itself meet §2.2's terminal-marker
  criterion (>95%); its HIGH status rests on the audit's recorded
  evidence pair, stated here so that a reader applying §2.2 to this
  table alone is not misled."
  New: "And M176's terminal figure — 68 of its 356 tokens
  inscription-final (19.1%) — is nowhere near §2.2's terminal-marker
  criterion (>95%); its HIGH status rests on the audit's recorded
  evidence pair, stated here so that a reader applying §2.2 to this
  table alone is not misled."
  (The adjudication: at 19.1% the figure is nowhere near the criterion;
  the sentence's second half — HIGH rests on the recorded evidence
  pair — is the part the record supports, and it stands.)
- **C-4 — §3.7 bigram counts (seals vs occurrences).** The bigram
  record counts pair occurrences; the paper labelled them seals.
  Old: "which appears on 122 seals (7.3% of corpus, PMI=2.43)"
  New: "which occurs 122 times, on 120 seals (7.2% of corpus,
  PMI=2.43)" (120/1,670 recomputed).
  Old: "(iN/in·kol/koḷ, 84 seals), M099·M342 (81 seals), and
  M176·M099 (74 seals)"
  New: "(iN/in·kol/koḷ, 84 occurrences on 82 seals), M099·M342 (81
  occurrences on 80 seals), and M176·M099 (74 occurrences on 74
  seals)" — the occurrence/seal pairs are the adjudication's, from
  the same record.
- **C-5 — §3.2, Slot 3 example.**
  Old: "M342=ay/ā (genitive terminal, most frequent terminal at 584
  tokens)"
  New: "M342=ay/ā (genitive terminal; the most frequent sign in the
  corpus, at 584 tokens)"
  (By final count M342 ends 70 seals; M233 and M367 each end 92. Its
  record distinction is most frequent sign overall.)
- **C-6 — §5, qualification paragraph.**
  Old: "Two of the five are this paper's headline terminal signs
  (M342, the most frequent terminal in the corpus, and M176)"
  New: "Two of the five are this paper's headline signs (M342, the
  most frequent sign in the corpus, and M176)"
- **C-7 — §2.2, terminal-marker criterion example (found by this
  round's sweep).** The criterion's own example named M342 as its
  exemplar of a sign inscription-final in >95% of cases; at 12.0%
  M342 does not meet the criterion it illustrated.
  Old: "Terminal marker evidence: sign appears in >95% of cases as
  inscription-final, matching known Dravidian case suffix (M342=ay/ā,
  genitive terminal)"
  New: "Terminal marker evidence: sign appears in >95% of cases as
  inscription-final, matching a known Dravidian case suffix
  (M305=ōṭu/comitative: 97.6% of its tokens inscription-final)"
  Basis: the Tamil-Brahmi comparison record's terminal rate for M305,
  0.976, re-derived from the corpus in `ADJUDICATION.md` Finding 2;
  the measure is the same quantity the criterion names ('cases' in
  the criterion means the sign's corpus tokens, per §2.2's own gloss,
  and the Holdat corpus contains no single-sign inscriptions). §2.2's
  standing disclaimer — that no record gives a criterion-by-criterion
  pass/fail for any HIGH sign — is unchanged and still governs how
  the example may be read.

## Finding 2 — §3.18's seven-sign list (adjudication: NOT REAL as charged)

The list is exactly its record's output (`backend/reports/phase155_phonotactic_sibilant.json`):
under the record's own rule M342 and M176 score 0.120 and 0.191, below
its 0.50 threshold, so nothing was omitted. No list change. One
presentational gap was real: §3.18 never defined its rate.

- **C-8 — §3.18, definition added at the rate's first use.**
  New opening sentence: "The terminal rate (t_rate) is the share of a
  sign's tokens that are the last sign of a multi-sign inscription,
  on the Holdat corpus." — the comparison record's own definition,
  per `ADJUDICATION.md` Finding 2.

## Finding 3 — the atlas population gap (adjudication: REAL, minor)

Source record: the depicted-kinds study record (its spec §4.3 and
step-0 record, Gate 0.4), quoted in `ADJUDICATION.md` Finding 3:
token 999, "2 primary rows, 2 occurrences — counted, never keyed or
classed"; the category sums (556 signs / 11,803 occurrences) plus
token 999 reconcile exactly to the stated 557 / 11,805.

- **C-9 — §3.31.1, accounting sentence added** after the
  unidentified-signs sentence:
  "The remaining sign of the 557 is token 999, the one population
  sign with no published identity: its 2 occurrences are counted in
  the population totals, but the sign was never keyed or classed,
  and it enters no per-kind rate, ratio, or test."
  No printed number changes.

## Finding 4 — the "about 43 genuinely significant" estimate (adjudication: REAL)

Source records: `backend/reports/phase143_iconographic_formula.json`
(394 attested filter-passing pairs; 63 selected at single-cell
contribution χ² > 1.0 with observed > expected; exactly 14 at or
above ≈14.7) and `backend/reports/phase149_adversarial_challenge.json`
challenge C2, whose "≈43" is an assertion built by subtracting
394 × 0.05 = 19.7 — the expectation for a family of valid 5%-level
tests — from a set never selected by a 5% test. No record supports
it as an estimate.

- **C-10 — §3.8.** The estimate sentence ("An adversarial recheck
  estimates about 43 of the 63 are genuinely significant — by
  subtracting the roughly 20 false positives expected among 394
  tests at an uncorrected 5% level, not by counting pairs at the
  threshold — the rest marginal, and several expected counts are
  small (as low as 1.0), so the largest associations are the
  reliable ones.") is deleted and replaced by the record-supported
  summary: "Of the 394 attested, filter-passing pairs, 63 had a
  single-cell contribution above 1.0, and 14 crossed the reported
  numerical threshold of approximately 14.7; neither count estimates
  the number of true associations."
  The two glosses are deleted with it: the "`Robust' in the
  adversarial recheck is that recheck's word for the roughly 43
  pairs…" sentence, and "The remaining roughly 20 of the 63 are the
  recheck's marginal remainder…" together with the self-referential
  "Earlier wording that called the roughly 20…" sentence. The 19.7
  comparison itself stands at the strength the adjudication records,
  reworded so it no longer hangs on the deleted remainder: "For
  scale: the count expected by chance among 394 tests at an
  uncorrected 5% level is 19.7 (394 × 0.05), and at the Bonferroni
  threshold the expected count under the null is about 0.05;
  neither figure converts the 63 into an estimate of genuinely
  significant pairs, because the 63 were not selected at the 5%
  level." The paragraph's other sentences (the selection criterion,
  the threshold's derivation, the single-cell definition, the
  unrounded expected counts) are unchanged.

## Finding 5 — claim strength (owner ruling 2026-11-18: SOFTEN)

- **C-11 — §5, Tier 2 definition.**
  Old: "Tier 2 means a probable linguistic interpretation —
  supported, not proven"
  New: "Tier 2 means a candidate linguistic interpretation —
  supported by the program's own tests, not proven, and not
  measured against rival frameworks"
- **C-12 — §5, closing family sentence.**
  Old: "Within that limit, the evidence favours a Proto-Dravidian
  reading framework under the tested assumptions."
  New: "Proto-Dravidian remains the candidate framework explored
  here. The present tests do not establish its superiority to rival
  language-family or non-phonetic interpretations, and the recorded
  evidence does not uniquely identify the six readings credited
  with outside support."
- **C-13 — §2.4, the two record bases stated.** One clarifying
  sentence added after "…so a true SA-free headline cannot be
  computed from the records.":
  "The limit is the status-audit table's: it records the evidence
  type by which each reading was promoted and cannot by itself
  determine a corrected headline; the strict core of 94 readings
  (§5) rests on the separate per-sign provenance audit, which
  records whether each reading's recorded history passed through
  the SA simulation."
  Basis (`ADJUDICATION.md` Finding 5b): the §2.4 sentence rests on
  the status-audit table (397 rows; promotion-route evidence types;
  SA+DEDR verified at exactly 43), the strict 94 on the provenance
  audit (the per-sign provenance register and its recorded
  strict-core rule, strict_count 94). The two answer different
  questions and do not contradict each other; the paper now says so.
  No internal study or record identifiers were added — the
  no-references rule binds this round as it bound the last.

## Mechanical items

- **C-14 — title-page version-note pointer.** The corrected draft's
  identifying note is this round's note, so the title page now
  names `v11_version_note_CORRECTED.md` where it named
  `v11_version_note_FINAL.md`. §6's pointer is generic ("its
  version note") and needed no change.
- **C-15 — printed word count.** 22,159 → 22,286, re-measured on
  the corrected build by the note's method and rebuilt to the fixed
  point (printed = measured). Page count 39 → 40 on the added
  sentences.

## Sweep dispositions — checked, verified unaffected, not changed

The whole text was swept for the wrong rates and their dependents
(96%, 94%, terminal/final-rate claims naming M342 or M176, "122
seals", PRIMARILY TERMINAL verdict language, "probable"/"favours"
applications). Beyond C-1…C-13, the sweep found:

- **Abstract.** The family sentence ("the evidence is consistent
  with a Proto-Dravidian reading framework under the tested
  assumptions, though Dravidian superiority over proto-Munda has
  not been formally quantified") is at the softened strength
  already; "consistent with" stands by the ruling's own terms. No
  other abstract sentence exceeds the new §5 formulation; the
  abstract carries no M342/M176 rate.
- **§4.4.** "…remains necessary before the linguistic interpretation
  can be treated as discriminative rather than merely compatible
  with Proto-Dravidian" and its mixed-comparisons sentence are
  already at or below the new strength.
- **§5, Tier 2 application sentence** ("The candidate
  Proto-Dravidian readings … are Tier 2 claims supported by
  multiple tests"). It takes its strength from the corrected
  definition (C-11) and is bounded by the qualification paragraph
  that follows it; no separate edit.
- **§2.2 summary list** ("4 of 7 strictly terminal signs match a
  Tamil-Brahmi terminal category; see §3.18"). Finding 2 stands;
  the list and the 4/7 result are their record's output.
- **§2.2 MEDIUM criterion** ("Positional profile matching a known
  morpheme class (INITIAL=title prefix, TERMINAL=case suffix)") and
  **§2.3's class vocabulary** (INITIAL-dominant / TERMINAL-dominant
  / MEDIAL): generic criterion and class statements naming no sign
  and no rate.
- **§3.2's Slot 3 listing of M176** ("M176=an/aṇ (masculine
  suffix)"): slot membership is the grammar model's fitted
  positional class, not a final-rate claim; the adjudication
  recomputed rates, not the model's class assignments. The
  corrected §3.3 figures now sit in the paper beside it.
- **§3.2.1 (the second-corpus-layer pattern test).** Its seven
  final-position signs and their rates (0.750–0.967) are that
  study's own, on the Shakti layer, naming no M-sign of the Holdat
  model.
- **§3.7 worked example** ("M342·M176 occurs 122 times"; the PMI
  fractions 122/5,332, 584/7,002, 356/7,002): already in
  occurrences; the counts are the record's.
- **§3.4 (M267).** Its positional counts (324 MEDIAL / 59 TERMINAL
  / 17 INITIAL of 400) are the validation recount's for a different
  sign and sum correctly.
- **§3.9 worked decodings** (e.g. "M211 M099 M342 = kol-kol-ay"):
  illustrative readings of individual seals; no rate claims.
- **§3.18's non-matching-signs passage** and **§5's
  phonotactic-violation sentence** (M328, M211, M176 and M342 as
  violation drivers): violation counts from their own record, not
  final rates.
- **§3.31.1's keying paragraph** ("556 population signs key to 424
  distinct rows…"): consistent with C-9 — 556 keyed signs plus
  token 999 are the 557.
- **"PRIMARILY TERMINAL"**: the phase133 record's verdict language;
  it occurs nowhere in the paper text (0 occurrences before and
  after this round). The verdict's basis — the low initial rates
  alone, against medial shares of 85.9%/77.2% — is now answered in
  the text by C-1…C-3's corrected figures.
- **"probable"**: one occurrence remains in the corrected text,
  "most probable syllable" in §2.4 — the SA's modal output, a
  technical term of the simulation's definition, not a strength
  claim about any reading or the family hypothesis. Left as is.
- **"genuinely significant"**: one occurrence remains, inside
  C-10's corrective sentence ("neither figure converts the 63 into
  an estimate of genuinely significant pairs") — a negation of the
  deleted estimate, not an instance of it.

## Flagged UNSETTLED — not changed in this round

- **§3.14 (formula semantics): "All domains share the same terminal
  sign profile (M342/M176 dominant) — a measured fact about the
  model's own sign assignments."** The sentence cites no rate and
  describes the formula-clustering record's per-cluster terminal
  profiles (the model's own assignments), a different quantity from
  the corpus final shares this round corrected. The adjudication
  neither recomputed that record's profiles nor falsified the
  sentence, and this round does not edit what it cannot ground: on
  raw seal-ending counts the adjudicated figures (M342 ends 70
  seals, M176 68; M233 and M367 each end 92) do not by themselves
  show an M342/M176-dominant terminal profile, so the sentence's
  "dominant" characterization stands in need of a check against its
  own record's measure (the formula-clustering record,
  `backend/reports/phase148_formula_semantics.json`) before the
  deposit round. Flagged here, and in the corrected version note's
  deposit checklist, rather than silently left or silently
  rewritten.

## Build and verification

- LuaLaTeX (TeX Live 2026, VM durable install), two passes on the
  final corrected source: 0 errors, 0 undefined references or
  citations; 40 pages.
- Word count re-measured by the note's method (`pdftotext | wc -w`):
  22,286; the printed count was updated and the build repeated to
  the fixed point (printed = measured on the shipped PDF).
- Residue scan over the corrected PDF text: the wrong rates in
  their old contexts 0 (every remaining "inscription-final"
  percentage is a corrected one: 12.0%, 19.1%, and the §2.2
  criterion example's 97.6%); "favours" 0; "probable" 1 (the
  dispositioned technical use above); "122 seals" 0; "most frequent
  terminal" 0; "headline terminal" 0; "roughly 43" 0; "BitConcepts"
  in any case 0; the former correspondence address 0; internal
  study/spec/phase/register identifiers in prose 0.
- Verified in the rendered PDF text: the Axiovex identity block;
  the corrected §3.3 rows and prose; §3.7's occurrence counts; the
  §3.8 summary in place of the estimate; the §3.18 definition
  sentence; the §3.31.1 token-999 sentence; the §5 Tier 2
  definition, headline-signs descriptor, and softened closing
  sentences; the §2.4 clarifying sentence; the printed word count
  22,286.
- The pre-correction source
  (`pierson_2026_indus_decipherment_v11_final.tex`) is byte-untouched:
  SHA-256 `8c98ae3bf82065829eca3cb7f6d78344a91aa6ddf3fec8e15f112da479a1ebb8`
  before and after the round.

## Addendum (parent, 2026-11-18): the section 3.14 sentence, settled and corrected

The correction round left section 3.14's "All domains share the same terminal sign profile (M342/M176 dominant)" UNSETTLED. The follow-up check (S314-CHECK.md) found it WRONG EVEN THERE: in its own record (the formula-clustering record), M342 appears in one domain's terminal profile (ANIMAL_GUILD, 3rd, 24 seals), M176 in none, and neither heads any domain; the printed claim traces to a hardcoded gloss string in the generating script that the stored profiles beside it contradict. The parent applied the check's record-supported replacement sentence verbatim (domains named with the record's leaders: M367 UNRESOLVED, M233 ANIMAL_GUILD, M051 MATERIAL, M065 DEITY_TITLE, M099 CIVIC_ROLE), rebuilt to a fixed point (LuaLaTeX x2, 0 errors, 0 undefined references, 40 pages, word count re-measured 22,326 = printed), and updated the version note's hashes and count in the same motion. Final hashes after this addendum: corrected .tex SHA-256 `8de26083419a1f801cb9f0e4d6d28e289763abc0f6205fb90f91a7e514473c81`; CORRECTED PDF SHA-256 `aceaa8cd5f412541c01db760da26bee965b5734daceceedf9aa573db764bb245`.
