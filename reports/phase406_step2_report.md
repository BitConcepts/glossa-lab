# Phase-406 — Spec 047 step 2 report (the distribution test)

Held under the Roif gate (spec section 10): an internal
program record; nothing in it is published.

**Headline.** Corpus: the primary layer as pinned in spec
section 2 (backend/glossa_lab/data/
yajnadevam_inscriptions.csv, 5,679 records; the
site-attributed layer of Specs 027/028). Asset B digest
`a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85` over
specs/047-roif-ledger-distribution/asset-b/
site-functions.jsonl (30 rows; testable
2). Ledger-sign list digest
`dfa48f50907a3374b45d6270f0ffbed8a2492c5d33c186da36950140b233292b` (extraction census:
8 entered,
3 mapped,
5 UNMAPPED). Headline outcome:
**INCONCLUSIVE (classification)** — the section 6.3
classification gate fired at E5, the distribution test
did not run, and no distribution quantity was computed
(no R, no permutation p-value, no R_ledger exists).
This result concerns the distribution component of Roif's ledger thesis only; the guild-authority and Akkadian-influence components were not tested.

## The section 7 wording (INCONCLUSIVE, classification)

"The distribution test did not run: 2 of the gazetteer's 30 sites survived the two-source agreement rule as testable (floor 12), and one side of the comparison is empty in the test population (the pooled ADMIN-TRADE-GATEWAY side carries both testable sites; the domestic/ritual contrast side carries none). The finding of this execution is the classification itself (Asset B, digest a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85): AGREED 3 (of which 1, shahr i sokhta, agreed at mixed/unknown and excluded by section 4.2), DISAGREED 1, SINGLE-SOURCE 10, NO-SOURCE 16, with the disagreed and unclassifiable sites named in full. No distribution quantity was computed. The claim stands UNTESTED for its distribution component, now with the reason measured rather than asserted."

## Step 0 gates (re-run at step 2)

- 0.1 input integrity: PASS — every section-2 input
  hashes to its freeze pin (recorded in
  reports/phase406_step2_results.json).
- 0.2 spine reproduction: PASS — 36 rows, 30 distinct
  clusters, the frozen cluster list.
- 0.3 join census: PASS — all
  5679 records accounted for in
  exactly one class (identical to the step-1 census):
- joined to a spine cluster: 5106 records
- non-spine sites: 573 records over 66 site values:
  - Alamgirpur: 3
  - Allahdino: 12
  - Altyn Depe: 1
  - Bakkar Buthi: 1
  - Bala-kot: 7
  - Baror: 1
  - Bhirrana: 6
  - Chandigarh: 3
  - Chanhu-daro: 74
  - Daimabad: 2
  - Derawar Ther: 1
  - Dholavira: 238
  - Failaka: 2
  - Farmana: 8
  - Ganweriwala: 2
  - Gharo Bhiro: 1
  - Girsu: 1
  - Gola Dhoro (Bagasra): 6
  - Gonur Depe: 1
  - Guddal A: 1
  - Gumla: 2
  - Hajar: 1
  - Hissam-dheri: 2
  - Hulas: 1
  - Janabiyah: 1
  - Juna Khatiya: 1
  - Kalba: 1
  - Kanmer: 10
  - Karanpura: 8
  - Karzakan: 3
  - Kish: 2
  - Kot-Diji: 11
  - Lakhanjo-daro: 15
  - Lohumjo-daro: 1
  - Luristan: 1
  - Miri Qalat: 2
  - Murda Sang: 1
  - Naru-Waro-dharo: 3
  - Nausharo: 38
  - Nindowari-damb: 2
  - Nippur: 1
  - Nuhato: 5
  - Ornach area: 1
  - Pabumath: 1
  - Pirak: 1
  - Qala'at al-Bahrain: 1
  - Ra's al-Junayz: 4
  - Rahman-deri: 2
  - Rajanpur: 2
  - Rakhigarhi: 13
  - Rappwala Ther: 1
  - Rodji: 4
  - Rupar: 5
  - Saar: 1
  - Salut: 2
  - Shikarpur: 8
  - Shortughai: 1
  - Sibri: 1
  - Susa: 2
  - Tarkhanewala-dera: 3
  - Tell Umma: 1
  - Tello: 1
  - Tepe Yahya: 1
  - Unknown: 28
  - Ur: 5
  - Wattoowala: 1
- no site value: 0 records

## Asset B pin re-assertion

Asset B hashes to the digest recorded in the step-1
outcome record (`a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85`), and the ledger-sign
list to its step-1 digest (`dfa48f50907a3374b45d6270f0ffbed8a2492c5d33c186da36950140b233292b`). The
asset's section 4.1 form and status mechanics were
re-validated from the committed bytes. Per-status
counts:
- AGREED: 3
- DISAGREED: 1
- NO-SOURCE: 16
- SINGLE-SOURCE: 10

Testable sites (AGREED, non-mixed/unknown class):
2 —
  - harappa: administrative (ADMIN-TRADE-GATEWAY)
  - lothal: port/trade (ADMIN-TRADE-GATEWAY)

## The classification gate (E5, spec section 6.3)

- Testable sites: 2 — the frozen
  floor is 12. The floor does not pass.
- Test population (section 6.1): the testable sites
  carrying at least one joined inscription —
  harappa (2,717 joined records, administrative, pooled)
  and lothal (208 joined records, port/trade, pooled).
- Pooled ADMIN-TRADE-GATEWAY side in the test
  population: 2 sites. Contrast
  (domestic/ritual) side: 0 sites —
  empty.
- The gate fires on both of its clauses. The test does
  not run; E6 (the primaries and sensitivities) was not
  run. The each-source-alone and five-largest
  recomputations of section 6.4 presuppose a primary
  test and are recorded not run; the section 6.4
  exclusions are restated in full below.

## Exclusions restated (spec section 6.4)

- DISAGREED: 1 — surkotada
- SINGLE-SOURCE: 10 — hiregudda, kalibangan, khirsara, mohenjo daro, piklihal, rojdi, sannarachamma, sheri khan tarakai, ter kala dheri, tigrana
- NO-SOURCE: 16 — amri, banawali, chagylly, desalpur, islam chowki, jhukar, joenniemi, kanispur, kunal, mullali, ojiyana, qasim bagh, rangpur, sheri khan tarakai 3, sheri khan tarakai 4, yalangach
- AGREED_mixed_unknown: 1 — shahr i sokhta
- NO-CORPUS-COVERAGE: 0 — none

## Records

- results: reports/phase406_step2_results.json
- step-1 record: reports/phase406_results.json;
  reports/phase406_step1_report.md
- asset: specs/047-roif-ledger-distribution/asset-b/
  site-functions.jsonl
- ledger list: specs/047-roif-ledger-distribution/
  asset-b/ledger-signs.jsonl
- outcome record: specs/047-roif-ledger-distribution/
  outcome.md (step-2 append)
- anchors asserted byte-identical before and after.

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen Pierson, per constitution section VI.*
