# Eteocypriot Program — Execution Freeze Record

**Date:** 2026-11-20. **Program:** Spec 096 — Eteocypriot
Program, Stage 1 (corpus assembly and freeze). **Commission:**
the owner lifted the execution gate in chat on 2026-11-20 ("in
parallel start the other ancient language decoding work") and
directed the same day that the work stand as its own program.
This record converts the preregistration draft of 2026-11-17
into the filed freeze record for the program's study. It is
repo-filed only: the external (OSF) filing named in the draft's
§10 is **not** performed — no external act of any kind is
authorized in this execution, and that deviation from the
draft's §10 is recorded here as the executing instruction's
explicit bound. No expert was contacted; nothing was purchased.

Founding documents pinned by this freeze (SHA-256), standing
unedited in Spec 095's package as provenance:

- Preregistration draft
  (`specs/095-red-team-remediation/second-targets/eteocypriot-preregistration-draft-2026-11-17.md`):
  `ab680522bffcf7a87bfebe784aaae54b5226f0df1deb8330120a0b962277f30f`
- Proposal
  (`specs/095-red-team-remediation/second-targets/eteocypriot-proposal-2026-11-17.md`):
  `6034663dba1c7a0bfc88d5475031f7b894240a2e4f0e25eb748733c9f1af12d6`
- Stage 5 scoping record
  (`specs/095-red-team-remediation/records/stage-5-scoping-record-2026-11-17.md`):
  `3b1fa6c5587c74b245b40f3a6dcf4682f89d9a78629582739254b8d87624fadf`

## 1. Step-0 corpus-availability survey (draft §3.1, item 1)

The proposal §3.3's unverified items, resolved or carried as
named gaps:

- **ICS 196 (Amathus bilingual): OBTAINED, complete as
  transmitted.** Masson's text (ICS no. 196) is reproduced
  concordantly by two open sources consulted (Wikipedia,
  CC BY-SA; Woudhuizen 2012), and Duhoux 2009's segment-by-
  segment discussion agrees. The stone is lost (Sittig 1914
  photograph is the witness of record).
- **Androkles dedications A and B: Greek sides held; Eteocypriot
  sides NOT OBTAINED.** The edition of record is Hermary &
  Masson 1982 (BCH 106, pp. 235–244; dedication A is its no. 66;
  B was first published by Hermary & Hellmann 1980, p. 262, with
  an improved reading in the 1982 article). SEG 32.1318's
  translations of record were obtained (attalus.org). The
  syllabic side of A is described in the edition's abstract of
  record as very mutilated; the sign-level transcriptions
  (pp. 236–238) are served by Persée as page images and were not
  text-accessible through the lawful route available at
  execution. No Eteocypriot sign of either dedication is held,
  and none is reconstructed.
- **ICS 194/195 (the great Amathus inscription): Perna 2019's
  re-edition NOT OBTAINED; Masson's readings attested at form
  level only.** Perna 2019 (BCH Suppl. 60, pp. 213–220) is the
  edition of record for this pilot: a new edition from autopsy
  changing 48 of 216 signs and 24 words, its reading printed at
  a glance on p. 220. The volume is open access on OpenEdition,
  but the chapter text was not reachable through the route
  available at execution. What is held is a form-level inventory
  cited from Duhoux 2009's concordance discussion, keyed to ICS
  line numbers: the corpus file intakes 7 forms totalling 45
  signs (43 legible, 2 damaged); Duhoux's discussion also names
  following sequences (ma-lu-?-?-ni-ka-to-ro; ta-sa-ma) that are
  recorded in the forms' notes and are not intaken as forms.
  Sensitivity S1's Perna leg is therefore recorded NOT OBTAINED
  (§6 below).
- **ICS 193: one form attested** (pu-e-ne-mi-na, line 3; Duhoux
  2009). Full text not obtained.
- **Greek syllabic control (ICS 217, Idalion tablet): excerpt
  held** — face A, lines 3–4 (66 signs) as reproduced in
  Chadwick 1987. The full control corpus was not obtained.
- **IG XV 1,1:** published 2020 (Karnava, Perna & Egetmeyer),
  covering Amathus, Kourion and Marion, with improved readings;
  its digital text and terms were not verified at execution —
  carried as a named gap. No machine-readable Eteocypriot corpus
  with a usable licence was found; intake is by transcription
  of the ancient text with citation, per §2's licensing basis.
- **Delimitation inventory:** the delimitation of record (Perna
  2015) stands behind a reference corpus of 23 records, 585
  syllabograms (540 identified), 49 distinct signs attested
  (Egetmeyer's Wörterbuch as counted by Duhoux 2009). Beyond the
  items itemized in the corpus file, individual primary-stratum
  texts were not obtained; they stand in the held-out set by
  delimitation, sealed. Golgoi is a separate stratum, excluded.

## 2. Corpus identity record (C095-3 style)

- **Corpus file:**
  `specs/096-eteocypriot-program/corpus/corpus.json`, version
  1.0.0, assembled 2026-11-20.
- **Corpus file SHA-256:**
  `5077285e8eac4b21785ca29cb151d47407f780998d85fa1eea27ef9d7e04f2dd`
  (13,440 bytes).
- **Pinning basis:** each inscription's pin is the SHA-256 of
  the canonical serialization of its corpus record
  (`json.dumps(record, sort_keys=True, ensure_ascii=False)`,
  UTF-8). The analysis driver verifies the corpus file hash
  before loading and refuses to run on a mismatch (fail-closed).
- **Verification venue:** the census and pins in this record
  were computed on the mini-server over the filed corpus bytes
  on 2026-11-20, under the owner's standing execution-home rule;
  all six per-inscription pins match the values the step-0
  survey produced, and the census below is that run's output.
- **Per-inscription pins:**

  | Inscription | Split | Pin (SHA-256) |
  |---|---|---|
  | ICS196 | development | `959c2796c3ef1dabc509db38488cfc0efa209a36c2fe4d6233baef8abe0d65d0` |
  | ANDROKLES-A | development | `fca9630563718d0f9f55cbbeb8c2ecca88737766e1f3c16077ee2c459d0744e4` |
  | ANDROKLES-B | development | `1c8d2cb98afefa42a7dc5a670b386d4e84b5f9270bb940eb969c384603e271fb` |
  | ICS217 | control | `38e35f2599d5430c5d99e4655ef2b7098c4ea1f2fa86b01754f3caace1d1a61d` |
  | ICS194-195 | held-out (sealed) | `4261b57bacdfa0f6cefa2e5f1b0049d311ddebd6188958a52d608b6565e8ad73` |
  | ICS193 | held-out (sealed) | `f453f7486329865a6970d661a05c47674bc521d1cd68b2ea2e2d2a1d145da127` |

- **Counting basis:** one syllabogram token in reading order =
  one sign. Restored signs (token `[x]`) and damaged signs
  (token `?`) are counted separately from legible signs, never
  merged into them.
- **Normalization rules:** transliteration in the Common
  syllabary's settled sign values, syllabograms hyphen-joined
  within a segment; segments are the edition's word-divider
  sequences in reading order; `[x]` marks a sign restored by
  the edition; `?` marks a sign the edition of record does not
  read. Orientation: Eteocypriot lines are right-to-left; the
  file carries reading order as data. Reading variants (ICS 196
  line 1 ma-to-ri vs the argued we-to-ri; Gordon's ku-no
  conjecture for the two damaged signs of line 2) are carried
  in the corpus record as variants, never silently adopted;
  analysis uses the edition of record.
- **Licensing basis:** the ancient texts are uncopyrighted.
  Only the ancient text is transcribed, with citation of the
  edition of record; no edition apparatus, commentary,
  copyrighted translation, or scan is reproduced. Sources
  consulted are CC BY-SA reproductions (Wikipedia), publisher
  open access (Persée, OpenEdition), the SEG translation of
  record as presented at attalus.org, and published scholarship
  (Duhoux 2009; Woudhuizen 2012; Egetmeyer's 2016–2020 report).

## 3. Frozen census

| Inscription | Split | Status | Segments/forms | Signs | Legible | Restored | Damaged |
|---|---|---|---|---|---|---|---|
| ICS 196 | development | held complete | 11 segments | 54 | 51 | 1 | 2 |
| Androkles A | development | Greek side only | 0 | 0 | 0 | 0 | 0 |
| Androkles B | development | Greek side only | 0 | 0 | 0 | 0 | 0 |
| ICS 217 (excerpt) | control | partial excerpt | 16 segments | 66 | 66 | 0 | 0 |
| ICS 194/195 | held-out | form attestations only | 7 forms | 45 | 43 | 0 | 2 |
| ICS 193 | held-out | form attestation only | 1 form | 5 | 5 | 0 | 0 |

Development-set Eteocypriot text held: **54 signs, one
inscription (ICS 196)**. Held-out continuous text held:
**0 signs**. The signary frame is the Common syllabary; the
Paphian signary is carried as a named variant frame only, and
no Paphian-stratum inscription is intaken. Signs attested in
the held development + control material: 37 (a, e, i, ja, ka,
ke, ki, ko, ku, la, li, lo, ma, me, mi, mu, na, ne, ni, no, o,
po, ra, re, ri, ro, sa, se, si, so, ta, te, ti, to, tu, u, wa).

## 4. The split (draft §3.2, as frozen)

- **Development:** ICS 196; the Androkles pair; the Greek
  syllabic control corpus (represented by the ICS 217 excerpt).
- **Held-out (sealed):** every other primary-stratum
  inscription, including ICS 194/195. The seal is procedural:
  the analysis driver loads development records only, and the
  held-out records in the corpus file carry form attestations,
  not continuous text — there is no held-out continuous text in
  the analysis environment to load.

## 5. Frozen E1 procedure

Fixed here, before any run; the driver
(`specs/096-eteocypriot-program/records/eteocypriot-e1-driver.py`)
implements exactly this.

- **Segmentation:** the editions' word dividers (corpus file's
  segments, reading order, flattened across lines). Greek side:
  whitespace-delimited words of the alphabetic text.
- **Derived spelling D(name):** the mechanical Cypriot
  syllabic spelling of a Greek name, by rules R1–R3 and nothing
  else: R1, a vowel letter maps to its vowel sign (ω→o, η→e);
  R2, a consonant followed by a vowel maps to the CV sign;
  R3, a consonant not followed by a vowel (cluster member or
  word-final) maps to C plus a dead vowel copying the
  *preceding* vowel of the name (default a). No name
  information beyond the Greek texts is supplied (P1's terms).
- **Match score:** LCCS — the length of the longest common
  contiguous syllabogram subsequence between D(name) and a
  segment.
- **A1 (strict segment-parallel):** the k-th Greek word is
  paired with the k-th Eteocypriot segment, in order. A name
  correspondence is recovered iff its positional partner is the
  ground-truth correspondent segment.
- **A2 (name-anchored free):** each Greek name is paired with
  the segment maximizing LCCS(D(name), segment), ties broken by
  earliest segment. Recovered iff the paired segment is the
  ground-truth correspondent segment.
- **Ground truth** (preregistration §2 foreknowledge, scoring
  only, never a procedure input): Ἀρίστωνα (Greek word 5) ↔
  segment 6, a-ri-si-to-no-se; Ἀριστώνακτος (Greek word 6) ↔
  segment 7, a-ra-to-wa-na-ka-so-ko-o-se. Androkles ground
  truth: A names Androkles, Orestheus, Andragoras; B names
  Androkles, Orestheus — untestable, no Eteocypriot side held.

## 6. Registered floors, instantiated (draft §4)

The draft fixes the floors in form; this freeze instantiates
them against the §3 census. A floor that cannot be met closes
the affected experiment as TOO THIN at freeze (draft §4).

- **F-E1a (E1, ICS 196 leg) — MET, administrable.** Basis: one
  complete bilingual with both ground-truth correspondences in
  legible segments. Census: 54 signs, 51 legible + 1 restored;
  both correspondent segments fully legible.
- **F-E1b (E1, Androkles leg) — NOT MET; leg closes TOO THIN
  at freeze.** Floor: at least one Androkles dedication with at
  least one legible Eteocypriot name-bearing segment held.
  Census: 0 Eteocypriot signs held for either dedication.
  Consequence, registered now: P1 is a conjunction over both
  legs; its Androkles conjunct cannot be met, so **P1 cannot
  pass as registered**, whatever the ICS 196 leg scores.
- **F-E2 (E2 census floor) — NOT MET; E2 closes TOO THIN at
  freeze.** Floor: held-out continuous text of at least 100
  legible signs under the edition of record (basis: P2 scoring
  needs registered occurrence positions in a continuous
  held-out text; 100 signs is under half of the great
  inscription's 216). Census: 0. This closure is independent
  of E1's outcome; E2 also does not run if E1's falsifier is
  met (C096-1).
- **P1 (E1)** stands as drafted: under at least one assumption,
  both ICS 196 correspondences and at least one Androkles
  correspondence recovered at segment level.
- **P2 (E2)** stands as drafted; no candidate is registered,
  because E2 is closed at freeze (F-E2) and its precondition
  (E1 success) is assessed in the outcome record.
- **P3 (E3)** stands as drafted; E3 engages only for E2
  survivors, of which there are none.
- **Sensitivities:** S1 — the Perna leg is NOT OBTAINED and
  the Masson leg holds form attestations only; S1 is recorded
  as not administered. S2 (Golgoi) — not run; E2/E3 are closed.
  S3 — satisfied by per-assumption reporting of the E1 leg that
  runs.

## 7. Step-0 closure check (draft §3.1)

The closure rule closes the study at step 0 on any identity
mismatch, licensing bar, or unresolved delimitation dispute.
None obtains: the identity of record (§2) pins exactly what is
held, with every gap named in the record itself rather than
silently absent; the licensing basis (§2) bars nothing that
was intaken; the delimitation of record is adopted as
registered, and the one reading variant carried (ma-to-ri /
we-to-ri) is a reading variant carried as data, not a
delimitation dispute. **The study does not close at step 0.**
Its experiments close, where they close, under §6's floors —
the draft's own stated mechanism, recorded here so the
closures cannot be mistaken for results (draft §4).

## 8. Claims (proposal §6)

The program's claims C096-1..C096-4, re-expressing the draft
claims EC-D1..EC-D4, were intaken into the claims ledger in
claim form at the program's adoption, through the sanctioned
importer only, from the bundle at the spec package root
(`specs/096-eteocypriot-program/aee-claims.json`): 4 appended,
0 already canonical; the ledger stands at 1,029 lines, 998
claims, canonical SHA-256
`09ca2407e2a7769e5fe73ded8402d22998ef8388ede777617fbfa678eb6f9a53`
(adoption record, PR #604, merged at
`5768ed31db6b5d9d5fd998b087df02d2e062fe3f`). The claims stand at
intake state (draft / created). **No standing is set by this
execution:** verdicts are recorded in the study's outcome
record, and any ledger standing change remains a recorded
adjudication by a named human approver (proposal §6, item 3) —
an automated actor never approves, verifies, or promotes. The
Indus program's claims and standings are untouched (the four
C096 propositions are new; the importer merges, never deletes).

## 9. What runs next

The E1 ICS 196 leg under §5's frozen procedure (both
assumptions), producing a run record; then the outcome record
stating every claim's verdict with its precision basis,
including the TOO THIN closures frozen here. The held-out seal
is never broken in this execution: E2 is closed at freeze, so
no prediction is registered and no held-out text is scored.

**AI disclosure:** executed by an AI agent (Muse, via Muse) at
the direction of Tristen Pierson, per constitution sec. VI.
