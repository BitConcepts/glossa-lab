# Phase-406 — Spec 047 step 1 report (Asset B build and freeze)

Held under the Roif gate (spec section 10): an internal
program record; nothing in it is published.

**Headline.** Corpus: the primary layer as pinned in spec
section 2 (backend/glossa_lab/data/
yajnadevam_inscriptions.csv, 5,679 records; the
site-attributed layer of Specs 027/028). Asset B digest
`a1a9e48422ab7ab2ef1d340c5ca0eb81a315253b196fdc199d77d2e5739c9f85` over
specs/047-roif-ledger-distribution/asset-b/
site-functions.jsonl (30 rows; testable
2: harappa, lothal).
Ledger-sign list digest `dfa48f50907a3374b45d6270f0ffbed8a2492c5d33c186da36950140b233292b`
(extraction census: 8 entered,
3 mapped,
5 UNMAPPED). Step 2 was not
run: no distribution quantity exists. This result
concerns the distribution component of Roif's ledger
thesis only; the guild-authority and Akkadian-influence
components were not tested.

## Step 0 gates

- 0.1 input integrity: PASS — every section-2 input
  hashes to its freeze pin (recorded in
  reports/phase406_results.json).
- 0.2 spine reproduction: PASS — 36 rows, 30 distinct
  clusters, the frozen cluster list.
- 0.3 join census: PASS — all
  5679 records accounted for in
  exactly one class:
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
- joined records by cluster (accounting only; computed
  by the machinery after the asset froze):
  - amri: 5
  - banawali: 26
  - chagylly: 0
  - desalpur: 3
  - harappa: 2717
  - hiregudda: 0
  - islam chowki: 0
  - jhukar: 1
  - joenniemi: 0
  - kalibangan: 212
  - kanispur: 0
  - khirsara: 4
  - kunal: 0
  - lothal: 208
  - mohenjo daro: 1923
  - mullali: 0
  - ojiyana: 0
  - piklihal: 0
  - qasim bagh: 0
  - rangpur: 0
  - rojdi: 0
  - sannarachamma: 0
  - shahr i sokhta: 0
  - sheri khan tarakai: 0
  - sheri khan tarakai 3: 0
  - sheri khan tarakai 4: 0
  - surkotada: 6
  - ter kala dheri: 0
  - tigrana: 1
  - yalangach: 0

## Asset B (step 1a)

Per-status counts:
- AGREED: 3
- DISAGREED: 1
- NO-SOURCE: 16
- SINGLE-SOURCE: 10

Testable sites (AGREED, non-mixed/unknown class):
2 — harappa, lothal.
The number of testable sites is not a build gate
(DD-047-1); its thinness is adjudicated by the step-2
classification gate (spec section 6.3), which has not
run.

## Ledger-sign list (step 1b)

Frozen in the same act under its own digest (above).
Extraction from the two Academia.edu postings of spec
section 2.1 only. Census: sought 13 depicted sign
classes; 8 entered;
3 mapped to the primary
layer's numbering; 5
UNMAPPED (recorded in the list and excluded from
counting by rule). The all-UNMAPPED case of DD-047-13
does not fire.

## Records

- results: reports/phase406_results.json
- asset: specs/047-roif-ledger-distribution/asset-b/
  site-functions.jsonl
- ledger list: specs/047-roif-ledger-distribution/
  asset-b/ledger-signs.jsonl
- outcome record: specs/047-roif-ledger-distribution/
  outcome.md (the build record, the section 4.3
  verification pass in full, the section 4.5
  attestation, and the digests — the pin source fixed
  by Spec 051 DD-051-14)
- anchors asserted byte-identical before and after.

*AI disclosure: executed by an AI agent (Muse Spark, via Muse) at the direction of Tristen
Pierson, per constitution section VI.*
