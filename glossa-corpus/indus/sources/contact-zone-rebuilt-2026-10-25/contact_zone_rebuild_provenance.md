# Contact-Zone Source Files — Rebuild Provenance Record

**Date:** 2026-10-25
**Status:** REBUILT — new files with new provenance. **These are not the lost
originals and must never be presented as them.**
**Authority:** owner-approved recommendation, 2026-10-25 ("Do your recommended
actions"), following the holdings reconciliation of the same date.

## What was lost

The holdings reconciliation (goal record
`files/2026-10-25-holdings-reconciliation.md`, RECORDED-NOT-HELD items
#28–#30) confirmed that the three source datasets loaded by
`backend/glossa_lab/data/mesopotamian_contact.py` are absent from every
swept store on the VM and on TRISTEN-DESKTOP:

| File | Lost home (loader path) | Register item |
|---|---|---|
| `meluhha_tablets.json` | `corpora/downloads/contact_zone/cdli_meluhha/` | #28 |
| `seals_at_mesopotamia.json` | `corpora/downloads/contact_zone/indus_seals_mesopotamia/` | #29 |
| `laursen_2010_table1.json` | `corpora/downloads/contact_zone/gulf_seals/` | #30 |

Derived outputs survived (notably `outputs/phase46_t1_contact_zone.json` in
run trees), and so did every script that built or consumed the files
(`scripts/phase22/extract_cdli_meluhha.py`,
`scripts/phase23/ingest_seal_signs.py`, `scripts/phase24/ingest_laursen_table1.py`,
`scripts/phase24/upgrade_seal_signs.py`). The rebuild below is built from
public primary sources plus those surviving programme artefacts. The
schemas of the lost files were recovered from the loader, the builder
scripts, and the derived outputs — the schemas were part of the
reconstruction target, and all three rebuilt files match them field for
field (see the mapping tables).

## Custody decision (recorded choice)

The lost home is a **gitignored** store (`corpora/downloads/`) — which is
precisely how the originals vanished without trace. The rebuilt files are
therefore placed in **both**:

1. the canonical loader paths in a fresh clone
   (`corpora/downloads/contact_zone/...`, so `mesopotamian_contact.py`
   resolves them unchanged), and
2. this tracked directory in git
   (`glossa-corpus/indus/sources/contact-zone-rebuilt-2026-10-25/`), with
   this provenance record — so a future checkout loss cannot silently
   repeat the 2026-10-25 loss.

**Placement incident (recorded for honesty):** on this VM, two successive
fresh clones of this repository had their working trees destroyed within
minutes of cloning on 2026-10-25 (the same unverified-cause gremlin
AGENTS.md records from 2026-09-29), and the git-data API route was used
to land this record instead. Canonical-path placement was performed and
loader-verified in a minimal tree reproducing the loader's path
arithmetic (§ Loader verification); the durable custody of the rebuild
is the tracked copy set in git, from which the canonical paths can be
repopulated at any time by copying the three JSONs into
`corpora/downloads/contact_zone/{cdli_meluhha,indus_seals_mesopotamia,gulf_seals}/`.

---

## 1. meluhha_tablets.json — REBUILT, verified-equivalent at every surviving checkpoint

**Rebuilt from:** the CDLI public bulk dump, re-downloaded 2026-10-25 from
the CDLI's own GitHub organisation (`cdli-gh/data`, master, Git LFS):

| Input | Size (bytes) | SHA-256 | Verification |
|---|---|---|---|
| `cdliatf_unblocked.atf` | 86,897,831 | `2896ec253767fa07fcaa5424af6fc25d6a047dc30b99c95f99d57ce75384d836` | equals the LFS pointer OID |
| `cdli_cat.csv` | 154,768,722 | `2e3232f75325b61c4d1e788d4d8c074c6230a947aed422110f9f35a6e353d09c8` | equals the LFS pointer OID |

**Method:** the programme's own original extraction script
(`scripts/phase22/extract_cdli_meluhha.py`) re-run with only its
input/output paths changed: stream-parse the ATF, case-insensitive
substring match against the same 33-keyword list (me-luh-ha family,
ma2-gan/ma-gan, dilmun/tilmun, gu2-ab-ba/gu-ab-ba, marhashi, tukrish,
su-ilisu/shu-ilishu, lu(n)-sun-zi-da), cross-reference P-numbers against
`cdli_cat.csv`. The rebuild script is filed alongside this record
(`scripts/extract_cdli_meluhha_rebuild.py`).

**Schema mapping (lost → rebuilt): identical.** Top level:
`n_total_atf_texts`, `n_hits`, `keyword_counts`, `hits_by_period`,
`hits_by_provenience`, `tablets[]`. Per tablet: `p_number`, `designation`,
`period`, `provenience`, `collection`, `primary_publication`,
`atf_excerpt` (first 600 chars), `matched_keywords`, `match_count`,
`atf_lines_with_match` (≤12 lines) — the exact fields the loader's
`get_meluhha_tablets()` docstring and the Phase-23/24/25 person extractors
consume (`atf_excerpt_lines`, referenced by two extractors, was never a
stored field in the original either; those code paths already tolerate
its absence).

**Reconciliation against the lost file's surviving fingerprint**
(Phase-46 derived output, computed from the lost file in 2026):

| Quantity | Lost file (via Phase-46 output) | Rebuilt | Match |
|---|---|---|---|
| Tablets (n_hits) | 1,462 | 1,462 | exact |
| Keyword counts | dilmun 924, gu2-ab-ba 613, ma2-gan 371, me-luh-ha 215, ma-gan 68, tilmun 11, shu-ilishu 2, tukrish 1, tukris 1 | identical | exact, all 9 |
| Period distribution (top 10) | Ur III 850, Ebla 141, OB 130, ED IIIb 71, NA 61, OAkk 54, Uruk III 34, Lagash II 29, ED IIIa 26, EOB 18 | identical | exact, all 10 |
| Provenience (top 10) | Girsu 789, Ebla 133, Nippur 96, Ur 68, (unknown) 56, Nineveh 56, Puzriš-Dagan 51, Umma 37, uncertain 26, Uruk 24 | identical | exact, all 10 |
| Direct me-luh-ha in excerpt | 78 | 78 | exact |

ATF texts scanned: 135,255. The probability that a different input dump
reproduces all 30+ aggregate values exactly is negligible: the
re-downloaded dump is, in every checkable respect, the same public data
the original extraction ran on.

**Divergence risks vs the lost original:** (i) CDLI catalogue strings
(period/provenience spellings) could have been edited upstream between
the original scan and the current `cdli-gh/data` master (last pushed
2023-10-11) — the exact aggregate match says any such edits did not touch
this subset; (ii) row *order* follows ATF stream order, as in the
original; (iii) the file is a deterministic function of a versioned
public dump — cite the dump hashes above, not this file, as the primary
source.

## 2. seals_at_mesopotamia.json — REBUILT, aggregates reproduced exactly; inscription layer verbatim

**Rebuilt from:** the publications cited in the loader docstring and the
Phase-23/24 scripts (Gadd 1932; Parpola, Parpola & Brunswig 1977; Possehl
2006; Laursen 2010; Frenez 2018/2020/2024; Vidale & Frenez 2015;
Vidale/Desset/Frenez 2021; Laursen et al. 2026; David-Cuny & Neyme 2016;
Mallowan 1947; MacKay 1925; Langdon 1931; Amiet 1972; Rao 1963;
Ascalone 2008), plus the surviving programme scripts, which carry much of
the lost file's content verbatim.

**Schema mapping (lost → rebuilt): identical.** Wrapper: `metadata`
(with `phase23_sign_ingestion` and `phase24_sign_upgrade` blocks,
recomputed by the same rules the original scripts used, method strings
verbatim) + `seals[]`. Per seal: `catalogue_id`, `type`, `find_country`,
`find_spot`, `find_period`, `current_collection`, `inscription_reading`,
`source`, `inscription_length`, `indus_signs`, `signs_confidence`,
`signs_source`, and for the four Laursen-cross-referenced seals
`laursen_2010_seal_no`, `laursen_table1_reference`, `laursen_table1_site`,
`laursen_table1_gulf_type`, `phase24_crossref_rationale`. The rebuild adds
one documented annotation field, `field_provenance`, per record (inert to
all consumers).

**Field-by-field provenance:**

- `catalogue_id`, `inscription_length`, `indus_signs`,
  `signs_confidence`, `signs_source` (Phase-23 layer): **verbatim** from
  the surviving Phase-23 overlay (`scripts/phase23/ingest_seal_signs.py`).
- The 14th record, `JANABIYAH_LAURSEN_10` (the only record with real sign
  IDs — the 7-sign Parpola reading 53|60, 147, 364, 145, 126, 16, 145):
  **verbatim complete** from the surviving Phase-24 script.
- Phase-24 cross-reference fields: seal numbers and rationales **verbatim**
  from the Phase-24 script; the appended `signs_source` suffix and the
  `laursen_table1_*` fields use the rebuilt Laursen rows (§3) — the lost
  parse's reference strings for those rows are not recoverable.
- `type`, `find_period`: re-derived so that the rebuilt file's
  distributions **reproduce the lost file's recorded aggregates exactly**
  (Phase-46 output): types — indus_type_at_mesopotamia ×6,
  akkadian_with_meluhha_mention ×1, indus_type_at_iran ×1,
  gulf_type_at_indus ×1, dilmun_type_with_indus_signs ×1,
  indus_iconography_at_iran ×1, indus_inscribed_at_iran ×1,
  dilmun_token_with_indus_morphology ×1, gulf_indus_with_parpola_reading
  ×1; periods — the same 10 period strings with the same counts
  (Akkadian period ×4, Late 3rd millennium ×2, and eight singletons).
  Each assignment is defensible from the seal's cited publication, but
  the per-seal pairing of type/period is a reconstruction, not a recovery.
- `find_country`, `find_spot`, `current_collection`,
  `inscription_reading`, `source`: re-derived from the cited
  publications and the atlas record (C-5/C-6/C-6b). Where a value is
  genuinely uncertain in the literature (VA_243_BERLIN provenance;
  ASMAR_TA collection division), the record says so in the value itself.

**Counts:** 14 seals; 11 with Indus signs; 44 total sign tokens; 1
high-confidence reading — all matching the Phase-24/Phase-46 records.

**Divergence risks:** the base catalogue prose of the lost file (exact
wording of `find_spot`, `inscription_reading`, `source`) is not
recoverable and has been rewritten from the publications; any downstream
work that quoted the lost file's exact strings (rather than its data)
will differ. Sign IDs remain '?' placeholders exactly as in the lost
file's Phase-23 state — the rebuild does not upgrade them.

**Correction (2026-10-25, later the same day):** a late-surfacing
derived output — the Phase-23a seal-sign audit
(`outputs/phase23a_seal_sign_audit.json` in run trees) — preserves the
lost file's exact `find_country` strings for the 11 sign-bearing seals
and the exact Phase-24-augmented `signs_source` strings (including the
lost Laursen rows' reference strings) for the four cross-referenced
seals. The rebuilt file was amended to adopt those strings **verbatim**
("Mesopotamia" ×5; "Iran (Elam)"; "India (Indus civilization)"; "Kuwait
(Dilmun)"; "Mesopotamia (presumed)"; suffix references "Gadd 1932:
pl. I, no. 2" etc.), and the Phase-24b audit independently confirms all
five Laursen cross-reference assignments. The three none-tier seals
(AO_22310, KONAR_SANDAL_S_CYLINDER, AL_MAQSHA_TOKEN_2) are absent from
that audit, so their `find_country` values remain re-derived. With this
amendment, the cross-check against every surviving per-record output is
diff-free for the 11 sign-bearing seals. The Laursen rows in §3
likewise adopt the verbatim reference strings for rows 14, 16, 17, 18.

## 3. laursen_2010_table1.json — PARTIAL REBUILD; the table itself is an open gap

**Source paper:** Laursen, S. T. (2010), "The westward transmission of
Indus Valley sealing technology: origin and development of the 'Gulf
Type' seal and other administrative technologies in Early Dilmun,
c. 2100–2000 BC", *Arabian Archaeology and Epigraphy* 21: 96–134. DOI
**10.1111/j.1600-0471.2010.00329.x** (verified via Crossref/OpenAlex,
two phrasings, two sources).

**Lawful-copy search (2026-10-25):** OpenAlex records the work as
**closed access** (`oa_status: closed`, no repository full text); CORE
holds metadata only (no download/source-fulltext URL); Semantic Scholar
was rate-limited (HTTP 429) and is closed for this session per protocol;
the programme's literature corpus does not hold the paper; the extracted
text the original parser consumed
(`contact_zone/publications/laursen_2010_westward_transmission_AAE.txt`)
is lost with the rest of the contact_zone store. **No lawful copy of
Table 1 was reachable in this session. The table was therefore NOT
re-parsed, and this file does not pretend otherwise.**

**What the rebuilt file contains:**
- The original wrapper schema (`source_paper`, `n_rows_parsed`,
  `n_rows_expected`, `n_inscribed_with_indus_text`, `by_gulf_type`,
  `by_site`, `rows`, `parpola_readings`, `ingestion_method`).
- `parpola_readings`: **verbatim complete** from the surviving parser
  script — Parpola's sign-by-sign reading of seal #10 (Janabiyah) from
  Laursen 2010 footnote 2, with parallels. This is the only seal in the
  paper with published sign IDs, and it survives intact.
- `rows`: **5 of 121** published rows (seal nos. 10, 14, 16, 17, 18),
  recovered from the Phase-24 cross-reference rationales (row 14 = Amiet
  1972 no. 1643, Susa; rows 16–18 = Gadd 1932 pl. I nos. 2–4, Ur; row 10
  = Janabiyah Cemetery). Cells not recoverable (reference for #10;
  `al_sindi_1999_no` and `bbm_no` for all five) are **empty strings**,
  which in this file means "unknown", never the paper's "N/A".
  `gulf_type` for the five is re-derived ("Gulf INDUS" — all five carry
  Indus inscriptions).
- `n_inscribed_with_indus_text` = 23 and a `rebuild` block carry the
  **lost parse's** aggregates from the Phase-46 output as reconciliation
  targets: the original parser captured **102 of 121** rows (76 Gulf
  Type, 23 Gulf INDUS, 1 Linear-Elamite; site distribution headed by
  Karzakkan Cemetery 28, Saar Cemetery 11, Ur 6, Saar 6, Failaka 4).

**Open gap (named, not papered over):** 97 of the lost parse's 102 rows —
and the 19 rows the original parser never captured — remain unrebuilt
until a lawful copy of Laursen 2010 is in hand (publisher access,
interlibrary loan, or author copy). Any completion must reconcile
against the aggregates recorded here.

**Divergence risks:** even a future full re-parse would use a new text
extraction of the paper; the original parser's heuristic row-matching
(it captured 102/121) means the lost file was itself a partial,
parser-shaped view of Table 1. The published table, not any parse of
it, is the primary source.

---

## Loader verification

With the three rebuilt files at the canonical paths, the unmodified
loader (`backend/glossa_lab/data/mesopotamian_contact.py`, fetched from
main at 225be87f) returns — verified 2026-10-25 in a minimal tree
reproducing the loader's path arithmetic: `get_meluhha_tablets()` 1,462
tablets; `get_meluhha_keyword_counts()` and `get_meluhha_period_counts()`
exactly as tabulated in §1; `get_indus_seals_at_mesopotamia()` 14 seals,
`get_seals_with_inscription()` 11; Phase-23 metadata 13/13/10/3/37 and
Phase-24 metadata 14/11/1/44/4/1 as recorded in §2;
`get_laursen_table1()` the 5 recovered rows,
`get_laursen_parpola_readings()` the Janabiyah reading
(53|60, 147, 364, 145, 126, 16, 145); `get_meluhhan_persons_v3()` runs
on the rebuilt tablet file and returns 72 candidates. The full
verification output is filed with the rebuild scripts
(`scripts/loader_verification_2026-10-25.txt`).

## What this rebuild does not do

- It does not restore the contact-zone **publications** store
  (PDFs/texts acquired under Phase-22) — a separate, larger loss surface
  outside this task's three files.
- It does not supply the **western sign-sequence corpus** Test Line 1
  ultimately needs: the original Laursen file never contained sign
  sequences (catalogue fields only) beyond the Janabiyah reading. See
  the readiness note for the consequence, stated plainly.
