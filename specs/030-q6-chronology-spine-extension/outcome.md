# Spec 030 / Phase-394 — Outcome record (2026-10-12)

Execution of the frozen Spec 030 contract under the owner's
authorisation of 2026-10-12 ("Register Spec 030 on OSF and
execute Phase-394"). Registration: OSF https://osf.io/bge3k/,
DOI 10.17605/OSF.IO/BGE3K (record:
`osf-registration.md` in this directory; PR #176, merge
`9a30b4f8`). Infrastructure: PR #177, merge `09589443`.
Frozen text was not edited by this execution; this record is
an append-only outcome document.

## The re-test (frozen §4 criteria, verbatim, on the extended spine)

Stage 0 baseline (deduped under rule 2; identical criteria to
the raw baseline): C1 1, C2 5, C3 0.0, C4 70 —
NOT-YET-TESTABLE.

After all five routes, the extended spine (205 rows) re-tests
as:

| Criterion | Value | Bar | Verdict |
|---|---|---|---|
| C1 regions with ≥2 window d/a sites | 1 (PK only) | ≥3 | FAIL |
| C2 window direct/associated sites | 6 | ≥10 | FAIL |
| C3 short-lived share of window d/a rows | 0.0 (0 of 37) | ≥0.50 | FAIL |
| C4 median σ of window d/a rows | 70 BP | ≤80 | PASS |

**Q6 status after Phase-394: NOT-YET-TESTABLE** — under the
as-frozen computation AND under the CONTESTED-excluded
computation (identical values; no CONTESTED row sits in the
window direct/associated pool). Per integrity rule 5, both
computations are reported; whether the sensitivity binds a
future Q6 freeze is **not decided here** (Ask 2, reserved to
a future Q6 freeze adjudication under Spec 027 §8.2). Per
F030-C07, this negative outcome is a valid closure of the
extension program: the spine grew by 70 traced rows and the
frozen bars did not move.

## Per-route outcomes (frozen order; margins-only interims)

- **R5 XRONOS re-retrieval** — the fresh full export
  (314,030 records; sha256
  `8570bfd9b256ced2f9e840183ea52325b9a7079b79a2957c7db797f09c118655`)
  is **byte-identical to the frozen Stage 0 export**: the
  served database has not changed. 144 in-box records (the
  same set), 0 new records, 0 field corrections, 0 rule-7
  admissions (25,474 coordinate-less records export-wide;
  none names a gazetteer-established site). Interim margins
  unchanged: C1 1, C2 5, C3 0.0, C4 70.
- **R1 origin-record tracing** — 10 material corrections +
  10 origin citations, 0 grade corrections, 0 new rows. The
  Qasim Bagh series was traced to its origin table (Betts
  et al. 2019, Table 4): the aggregator's material strings
  embed layer codes ('Charcoal/QB8'); the origin strings are
  plain — three wheat determinations confirmed short-lived
  (all below the window), and OZT-624 (4030±60) reclassifies
  unknown → long_lived on its origin string 'Charcoal' (a
  layer code is not a feature: no grade earned). The
  aggregator chain's 'Llagostera 1979' attribution for
  OZT-624 is an empty bibliographic stub. Not traced, with
  reasons recorded per target: Tigrana OxA-30023 (circulates
  via a 2018 compilation with no publication reference; no
  published context table reached), the Shahr-i Sokhta
  P-2076A/P-2081-A origin list (Fishman, Forbes & Lawn
  1977, Radiocarbon 19(2)) — identified but its text is
  bot-gated at the journal archive and access-gated at the
  publisher; no lawful copy reached, so no correction was
  made on speculated content — and Hiregudda K-4246.
  Interim margins unchanged.
- **R2 c14bazAAR audit** — 29 databases enumerated. Ingested
  (verified open): p3k14c v2025-07 (CC0-1.0; 63 in-box
  records, all age-corroborations → 63 citations), NERD v6.0
  (CC BY 4.0; 32 records → 32 citations; its context column
  confirms the spine's existing grading pattern exactly),
  RADON-B daily export (CC BY 3.0; 78 in-box records → 29
  citations + **49 new rows, all unassessed**, at Mehrgarh,
  Mundigak, Balakot, Amri, Rana Ghundai, Damp Sadaat, Kili
  Ghul Mohammad, Aq Kupruk I and II). Audited, not ingested:
  CalPal (**catalogue_only** — no open licence verifiable;
  its 18 in-box records all duplicate pooled measurements),
  14SEA / AgriChange / AIDA (0 in-scope records), Tegiszhol
  (1 record, rejected: a Siberian burial with a mistyped
  latitude, out-of-window regardless), xronos (R5's object),
  and 20 further regional databases audited by stated scope.
  Grading census: all 49 admitted rows carry RADON-B's
  Rosenstock type/layer formula and no named sample feature
  — the same evidence class held non-grading in R1 — so the
  rows stay unassessed uniformly, including 15 in-window
  rows. Coordinate note: RADON-B asserts (29.3, 67.5) for
  its Mehrgarh records; published references place Mehrgarh
  at the Bolan Pass (approx. 29.8 N, 64.6 E). The assertion
  is carried as published (the build mints no coordinates);
  the conflict is recorded here and in the results file;
  the pair is in-box either way. Interim margins unchanged.
- **R4 TwoRains supplement audit** — one data-bearing
  supplement located: Petrie, Bates, Higham & Singh 2016
  (Antiquity 90(354), CC BY-NC-ND, open_access_read_only)
  publishes 28 AMS determinations for Masudpur VII and
  Masudpur I with trench + numbered, typed context and
  taxon material per sample, plus the authors' own flags
  (intrusive / problematic / inaccurate — carried verbatim;
  Bates's 2016 thesis corroborates the flags). The samples'
  contexts are named excavation contexts, so the
  determinations would grade associated — **but the rows
  are NOT ADMITTED in this build**: neither site is
  gazetteer-established, no publication reached states
  coordinates for them, and rule 7 admits coordinate-less
  rows only for gazetteer-established sites. The full
  extraction (all 28 determinations with contexts,
  materials and flags) is preserved in
  `reports/phase394_results.json` (route R4 audit) so a
  future build or gazetteer act can admit the rows without
  re-extraction. Had they been admitted: C2 6→8, C1's IN
  region would hold 2 sites (C1 still fails: TM and IR hold
  fewer than 2), C3 3/48 ≈ 0.06 — the verdict would not have
  changed. No data-bearing supplement was located for Burj,
  Bahola, Dabli-vas Chugta or Girawad under the postures.
  Interim margins unchanged.
- **R3 targeted published-date extraction**
  (open_access_read_only; internal-spine-only, never
  released) — 21 determinations extracted from Dales &
  Kenoyer 1993 (The Harappa Project 1986–1989), Table 40.1
  + text: 10 grade associated on the report's own feature
  evidence (the table's ** notation, "charcoal inside
  hearths or kilns", and four narrative-tied samples —
  including Beta-33874, carried with the excavators' own
  anomaly flag verbatim), 11 unassessed at mound/period
  resolution. Six in-window associated rows (all charcoal)
  make Harappa the sixth window d/a site: interim C2 5→6,
  window rows 31→37. All other named targets were attempted
  with dispositions recorded in the results file
  (Mohenjo-Daro, Dholavira, Kalibangan, Lothal, Rakhigarhi
  — the IUAC series publishes ages by trench depth without
  lab codes or named contexts, ineligible as published —
  Banawali/Kunal, Bhirrana, the RADON-B sites' origin lists,
  Shortugai; second-IR-site and second-TM-site searches:
  none found eligible).

## The §3.5 early stop

Never triggered: no interim assessment reached
SUPPORTED-FOR-FREEZE-DESIGN, so all five routes ran, as
designed.

## What the extension established (and what it did not)

The spine grew from 177 Stage 0 rows to a 205-row extended
spine (135 baseline measurements after rule-2 dedupe merged
42 duplicate sightings — the Bannu series ingested once per
source database — plus 49 RADON-B rows and 21 Harappa rows),
with 134 corroborating citations attached and 10 traced
material corrections. The window d/a pool grew 31 → 37
rows and 5 → 6 sites. C3 remains the binding constraint:
**zero** short-lived rows sit in the window d/a pool — every
traced short-lived determination the routes reached is
either below the window (Qasim Bagh wheats, 3,240–3,750 BP),
ungradeable on its published evidence (Tigrana's wheat), or
behind the Masudpur coordinate gap (3 short-lived
determinations among the 28 extracted). C1 fails on IN
(0 window d/a sites — Tigrana and Hiregudda stay unassessed)
and on IR/TM (1 and 0). No criterion was loosened, no row
was graded on anything but its origin record, and no
CONTESTED row was silently dropped or silently kept: the
sensitivity is reported both ways above and its bindingness
is expressly reserved (Ask 2).

Open items this record leaves, for any future act (none is
authorised by this record): admission of the extracted
Masudpur determinations awaits a published coordinate
source or a Spec 027 gazetteer act; the RADON-B new-site
rows await origin-list tracing when the journal date lists
become lawfully reachable; Q6 itself remains
NOT-YET-TESTABLE, owned by Spec 027 F027-C16.

## Products

`data/movement/chronology_rows_phase394.jsonl` (205 rows),
`data/movement/gazetteer_rows_phase394.jsonl` (36 baseline
rows + 8 source-asserted rows for genuinely new sites),
`data/movement/extension_register_phase394.json`,
`reports/phase394_results.json`,
`reports/phase394_extension_report.md`. Build:
`backend/scripts/phase394_spine_extension.py` via the
experiment graph node `IndusPhase394SpineExtension`
(H23 steps 1–5; PR #177 + this record's PR). Gates:
foundation check 40 passed / 0 failed / 8 warnings; full
backend suite green (see PR record); branding sweep clean.
