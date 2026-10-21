# Phase-414 — Spec 055 sign-900 numeral test report

Executed 2026-10-21 by Muse Spark via Muse (AI agent), under the frozen Spec 055 contract (freeze digest `42ef82829ade894918b0bf946ac44354224d689202e2f7bf00eb747821bdedfc`; OSF registration tbyqg, approved + public before the run).

## Outcome

**NOT NUMERAL-LIKE**

The sign that Fuls's paper numbers 900, identified in Spec 055's recovery record as P154, does not behave as a numeral sign behaves in the pinned strict corpus: on 3 of the three frozen measures it sits inside the range of frequency-matched ordinary signs (per-measure table in the run's results record). The numeral reading the fragment carries is contradicted at the behaviour stage. The identification itself stands as recovered; what fails is the behaviour the reading predicts.

This result is about how one identified sign behaves in recorded data. It is not evidence of what any sign means, and it does not establish the value six.

Design D-16 does not join this campaign even though this recovery is the act that would unblock it; D-16 waits for its own planning gate (campaign decision E-7).

## Identification (from the recovery record)

Sign list named from the document's own text: the extended Wells (2011, 2015) sign list of 702 distinct signs (Wells 2015; the ICIT database's sign list, Appendix A)

> "The signs are coded according to an extended sign list with 702 distinct signs (W ells 2015)." — p. 57, opening section (introduction)

> "The sign list by W ells (2011, 2015) has been extended to currently 702 distinct signs" — p. 59, 'SIGN LIST'

> "They involve a sign list of about 702 distinct signs" — p. 85, 'SUMMARY'

> "APPENDIX A: SIGN LIST WITH 702 SIGNS OF THE ICIT DA T ABASE." — p. 88, 'APPENDIX A'

Target sign: source no. 900; basis crosswalk-registry; registry id P154; named-list locator extended Wells (2011, 2015) list, sign 900 (Wells PhD 2006, Fig. 3.2, thesis p. 92, per the Phase-123 Wells segmentation witness).

## Records

- Recovery record: `specs/055-sign900-numeral/source-table-recovery.json` (schema glossa.source-table-recovery/1).
- Results record: `reports/phase414_results.json`.
- Corpus export: `specs/055-sign900-numeral/strict-corpus-export.jsonl` — SHA-256 `1e421af1b75f09f49c928ef7eaa86e4c9a382e059d4771f164256a069896e02c` (2906 records, 11507 tokens; target 79 occurrences, floor 5).

## Per-measure table

| Measure | Target | Numeral range | Control range | Numeral-side | Control-side |
|---|---|---|---|---|---|
| short_text_share | 0.164557 | [0.0, 1.0] | [0.161765, 0.395062] | True | True |
| numeral_adjacency_share | 0.455696 | [0.0, 1.0] | [0.098592, 0.662651] | False | True |
| positional_entropy_bits | 2.708415 | [-0.0, 2.893777] | [1.490324, 2.972423] | False | True |

Numeral-side 1, control-side 3 → **NOT NUMERAL-LIKE** by the frozen section 5.3 mapping alone.

---

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution §VI.*
