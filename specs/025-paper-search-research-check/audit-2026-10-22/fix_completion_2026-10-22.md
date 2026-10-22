# Fix completion record — Material Audit 2026-10-22 (batch C: P9, P10, preprint v6)

Companion to `fix_execution_addendum_2026-10-22.md` (batches A and B).
This record closes the fix commission: proposals P9 and P10 executed,
the preprint finished as a submission-ready package, and the gates
asserted. **Nothing was submitted, deposited, or published.** The
owner gives the go on the actual text before any of that happens.

## P9 — LANDED (preprint v6, §8 + §3.23)

Executed on the WS3 evidence (`raw/fix_ws3_evidence_notes.md` §E):

- **Five §8 entries added** for the Mahadevan works the text already
  relied on: 1981 "Place Signs in the Indus Script" (Proc. Fifth Int.
  Conf.-Seminar of Tamil Studies 1(2):91–107, Madurai: IATR); 1982
  "Terminal Ideograms in the Indus Script" (in Possehl (ed.),
  *Harappan Civilization*, pp. 311–317, Oxford & IBH); 1986 "Towards
  a Grammar of the Indus Texts" (*Tamil Civilization* 4(3&4):15–30);
  1989 "What Do We Know about the Indus Script?" (*Journal of the
  Institute of Asian Studies* 7(1):1–38); 2011 "The Indus Fish Swam in
  the Great Bath" (*Bulletin of the Indus Research Centre* 2:1–73,
  Chennai: Indus Research Centre, Roja Muthiah Research Library).
  Evidence level: **verified at published-bibliography level**
  (Jyothibabu 2023, DOI 10.23993/store.85246, bibliography; the 1982
  entry independently corroborated verbatim; 1986 corroborated by
  Mukhopadhyay 2019; 2011 corroborated twice). These are not direct
  Crossref/WorldCat records, and the level is stated here so it
  travels with the entries. Two bounds: the 1989 entry's possible
  1988 *Proceedings of the Indian History Congress* version is flagged
  in the evidence notes, not merged; **the 2011 identification is
  inferred** — it is the only 2011 Mahadevan Indus work found, and
  the preprint's in-text reference ("the akam-puram (2011) paper")
  carries no title.
- **The aggregate counts are qualified in the text.** No verifiable
  source exists for "10 Mahadevan papers (1972–2018)" or "38
  Mahadevan papers (1970–2018)". §3.23 now states in place, after the
  first use, that the paper counts in that section and the next are
  this program's own text-mining corpus counts — internal outputs,
  not externally sourced figures (P9's alternative limb). The §1.x
  summary line ("10/10 Mahadevan papers (1972–2018)") describes the
  same internal mining and is covered by that qualification; it was
  not separately edited, and that decision is recorded here.

## P10 — EXECUTED AS FAR AS THE EVIDENCE ALLOWS; STAYS OPEN, FLAGGED

The fresh session narrowed the question with positive evidence
(`raw/fix_ws3_evidence_notes.md` §F): the titled article "On the
identity of the toponym LÚ.SU(.A)" is JAOS 108(2):197–202 (1988),
DOI 10.2307/603646 — corroborated by PhilPapers, by a scholarly
citation giving pages 197–202, and by a footnote in JAOS 108.1
(1988) calling it "JAOS 108.2, forthcoming", which positively
excludes a 1982 JAOS publication of that titled article. A genuine
1982 Steinkeller demonstration of the Su = Shimashki identification
is attested secondarily, so the preprint's *in-text* reliance on
"Steinkeller 1982" has a real referent — but that item's venue and
pages were not verified, and the contents of JAOS 102(2) pp. 299–309
were never directly inspected (the coordinator's one web search for
the issue contents returned nothing usable).

Per the proposal's own text — verify against a JAOS backfile source
before citing further; **do not substitute the 1988 record** — the
fix executed is: the §8 entry is **unchanged** in v6, and the flag is
carried in `docs/research/PREPRINT_VERSIONING.md` (v6 row), in this
record, and in the submission summary, so no reader of the repo
record can mistake the entry for verified. What closes P10: one
direct inspection of the JAOS 102(2) contents (or the 1982 item's
venue/pages) — a named, single remaining check, recorded as an open
gap, never rounded into a correction.

## Preprint v6 — the package

- Source: `glossa-corpus/indus/pierson_2026_indus_decipherment.tex`
  bumped v5 → v6 per `docs/research/PREPRINT_VERSIONING.md` (version
  lines in the title block and closing line; the version table and
  the AGENTS.md version fields updated). The 2026-10-06 addendum
  draft (`pierson_2026_indus_decipherment_addendum_v5.md`) was **not**
  renumbered — that remains an owner decision, as the version record
  already noted.
- PDF: `pierson_2026_indus_decipherment_preprint_v6.pdf` (the v4 PDF
  is superseded and removed in this batch, per the versioning doc's
  rename-on-bump rule). Build route: XeLaTeX was absent from the
  audit environment, so TinyTeX-1 (TeX Live 2026) was provisioned
  under `~/workspace/tex-tools/` — nothing system-wide. (Tectonic was
  tried first; its bundle relay returned 403 through this network and
  it was abandoned, recorded here so nobody re-tries it blind.) Two
  passes, **zero errors**, **18 pages**, 110,480 bytes, SHA-256
  `797fa2957cf5d0653443051c188cd585fbb4a290165e8fe373f86127a57ba4fd`.
  Verified in the **rendered output** (pdftotext), not just the
  source: both v6 stamps present, no v5 version line remains; all
  five new Mahadevan entries render with their fields; the §3.23
  qualifier renders; the Steinkeller entry renders as printed
  (unchanged, flagged in the records above).
- Adversarial pass: run on the v6 source by an independent engine
  (GPT-4-Turbo; route history and depth limits stated honestly in the
  record) and adjudicated finding-by-finding against primary sources
  — `adversarial_pass_2026-10-22.md`, raw findings at
  `raw/fix_adversarial_findings_gpt4turbo.md`. Outcome: one finding
  sustained in narrow form (the §2.1 Zipf exponent ~1.7 — the paper's
  own unreleased-corpus statistic without a checkable derivation;
  recommended owner action filed, the sentence **not** rewritten by
  this commission), one caution already carried by the paper (the
  >90% coverage sentence), three not sustained (including an alleged
  arithmetic inconsistency that checks out exact: 75 + 86 = 161;
  6,363/7,002 = 90.87%).
- One-page summary for the owner: `submission_package_summary_2026-10-22.md`.

## Gates and posture

- No claim status, stage, anchor, score, or PRED changed anywhere in
  the fix commission; H26 is satisfied by construction, with the
  audit records as the cited non-SA evidence for every note.
- H21 foundation check: **not triggered** by any fix batch, on the
  rule's own trigger list (`docs/governance/rules.md` H21: modifying
  `backend/reports/INDUS_FINAL_ANCHORS.json`, promoting anchor
  confidence, updating `dravidian_*.json` language models, or adding
  `phase*.json` result files to `reports/`). The three batches' file
  lists were checked first-hand: none touches any of those. The
  committed foundation report on main
  (`outputs/foundation_check_report.json`, read at the batch-C base)
  stands at **59 OK / 0 failed / 6 warnings** — unchanged by this
  commission, since nothing it checks was modified. (A live re-run
  against a fresh tree was attempted; the 161 MB archive transfer
  stalled repeatedly in this environment and the attempt was
  abandoned rather than reported as a result. The audit's own merge
  addendum took the same not-triggered position for its record-only
  changes, PR #332.) CI's claims-store hash tests, which do run per
  batch, are green on batches A and B (see below).
- CI: each batch merged only on a genuine full run verified from its
  own job conclusions. (Batch A's backend job failed once on a
  claims-combined-hash assertion and passed identically on re-run;
  the failing assertion's expected value matched the committed
  foundation report byte-for-byte, identifying the failure as the
  documented cold-start/cache transient the audit's own PR #331 hit —
  recorded in batch A's PR history, not hidden.)

## What remains open after this commission (stated, not rounded up)

1. **P10's last check** — JAOS 102(2) contents, or the 1982
   Steinkeller item's venue/pages. The entry stays flagged until then.
2. **Kak 1988's full text** — a Zipf attribution to Kak is unsupported
   at the reached evidence level; outright falsification needs the
   Taylor & Francis text.
3. **The Wells 1998 thesis's direct repository fetch** — resolved at
   record level; the landing page itself was not fetched.
4. **The §2.1 Zipf exponent** — the adversarial pass's sustained
   finding; an owner decision (add the derivation, or qualify in
   place) at submission time.
5. **A deeper adversarial pass** — recommended before any actual
   submission, when a frontier-model route with credit is available.
6. **The public page's clarifying note** — drafted and filed
   (`public_surface_check_2026-10-22.md`); publishing it goes through
   the website chat with the owner's approval. The page's "Study
   papers & key links" bibliography entries were not in the fetched
   text and should be checked at the page's next edit.
7. **The download-chain defect** — `download_with_fallback` via the
   Crossref source serves wrong artifacts (twice, for the same DOI);
   the Europe PMC route is proven. An upstream fix is out of this
   commission's scope; the identity-check discipline stands.
