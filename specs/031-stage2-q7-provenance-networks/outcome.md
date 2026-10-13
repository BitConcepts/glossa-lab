# Spec 031 / Phase-395 — Outcome record (2026-10-13)

Execution of the frozen Spec 031 contract under the owner's
authorisation of 2026-10-13 ("Do ALL that remains now").
Registration: OSF https://osf.io/jtwvc/, DOI
10.17605/OSF.IO/JTWVC, approved and public before execution
(record: `osf-registration.md` in this directory; PR #193,
merge `69f42320`). Infrastructure: PR #196, merge
`b287e7d9`. Frozen text was not edited by this execution;
this record is an append-only outcome document.

**Result in one paragraph.** Q7 asks whether sites that
share provenanced material sources also resemble each other
more in their ceramics or their bead-making, beyond what
distance alone would explain. The frozen design could not
be run to a verdict, for a plain reason found at the
margins step, before any similarity was computed: the
design's site universe is the Stage 0 gazetteer, and the
frozen period rule admits only sites whose gazetteer
record itself labels them as Mature Harappan-period sites.
The gazetteer carries such a label for **no site at all** —
its period fields are empty for every Indus site — so both
response arms have zero eligible sites. The bead/craft arm
therefore closes **NOT-YET-TESTABLE** and the ceramic arm
closes **NOT ESTIMABLE**, exactly the closures the freeze
pre-registered for this situation. No response was
computed, no verdict exists, and nothing here is a finding
about ancient exchange: it is a finding about what the
program's own frozen records can and cannot yet support.

## 1. What was executed

The frozen execution shape (spec section 7), in order:

1. **Graph-first build (E1).** Script
   (`backend/scripts/phase395_q7_execution.py`), graph
   module (`backend/glossa_lab/experiment_graph_phase395.py`,
   node `IndusPhase395Q7Execution`), registration in the
   experiment graph, then the run (PR #196).
2. **Digitisation design step (E2)** — section 2 below.
   Its products are research inputs in the gitignored
   local store (`corpora/downloads/spec031_phase395/`),
   hash-pinned in the results file; the digitised link
   data itself is not released (F031-C11).
3. **Margins step (E3)** — section 4 below. The
   population record was written and hashed before any
   response was computed. Both arms closed here.
4. **Outcome step (E4).** Not run for either arm: the
   frozen rules run it only for an arm that passes
   margins. The section 5 machinery (matrix regression,
   permutation test, controls, jackknife, verdict rules)
   was built and is fenced by unit tests on synthetic
   populations with known structure
   (`backend/tests/test_phase395_build.py`), so the
   pipeline exists and is verified even though the data
   never reached it.

## 2. Digitisation design step

**Law (2011), the link basis.** The book's chapters are
posted as PDFs on the project site (harappa.com) at
read-only posture. The posted set was inventoried from
the Wayback Machine's index of that directory (the live
host refuses plain fetches) and the archived copies of
the postings were retrieved into the local store: 11 of
the 14 chapters (1, 2, 3, 6, 7, 8, 10, 11, 12, 13, 14)
plus front matter. **Chapters 4, 5 and 9 have no PDF in
the posted set.** The artifact-level determination
tables are in the printed appendices (Part 2), which are
not posted.

**Residual (ii) re-verification** (the D8 audit left this
open): whether every printed appendix table records the
method per determination **cannot be re-verified from the
posted set**, because the appendices are print-only. What
the posted chapters do record is the method per material
study, and the summary chapter states the study totals
(more than 2,100 determinations at Harappa, almost 120 at
all other sites combined). This digitisation therefore
works at study level for method, and at the granularity
the posted chapter text supports for counts.

**The method split** (the frozen rule, spec section 3):
a determination enters the primary tier only if it was
made by an instrumental method the D8 audit's Stage 1
record names — **INAA** and **strontium/sulfur isotopes**.
That admits exactly three of Law's studies: agate (INAA),
vesuvianite-grossular (INAA) and alabaster (Sr/S
isotopes). The chert, steatite, limestone, metals and
grindingstone studies enter **neither** tier: their
methods are not named as instrumental in the audit
record, and the sensitivity tier is Chapter 4's
reference-based assignments only. Two of the three
admitted studies could be counted from the posted text;
the third could not (see section 3).

**Ceramic sources (postures assigned as section 4.2
prescribes).** Nine principal classification-bearing
reports for gazetteer sites were audited in the D8
pattern. Two sit at a posture that permits internal
digitisation — the Harappa excavation report (Vats
1940) and the Mohenjo-daro reports (Marshall 1931;
Mackay 1938), both openly posted as scans with no open
licence (`open_access_read_only`). The other seven
(Banawali, Kalibangan, Lothal, Rojdi, Kunal, Khirsara,
Shahr-i Sokhta reports) are print or journal items with
no openly posted full text located (`catalogue_only`),
so a site resting solely on them could not enter the
arm in any case.

**Bead/craft sources.** The classification's own record
stands as the D8 audit found it: there is **no collected
per-object dataset**; the published applications are
per-assemblage and qualitative, concentrated at Harappa,
Chanhu-Daro and Mohenjo-Daro. The two principal posted
applications (Kenoyer & Vidale 1992; Kenoyer 1997) were
re-checked: neither tabulates per-site counts of
classified beads, so the arm's floor (at least 10
classified beads per site) cannot be evidenced for any
site from a countable published source. The arm's
closure does not rest on this — it rests on the period
screen (section 4) — but the floor step is recorded
honestly rather than passed over.

## 3. Link construction (primary tier)

Counted from the posted chapter text, at the granularity
it supports (per-site totals; the per-source splits the
text states). Assignments to the Shahr-i-Sokhta proxy
source-group are **not** attributions to a named source
area — the actual source is unnamed, presumed somewhere
in eastern Iran — and never count (spec section 3).

- **Agate (INAA).** 56 artifacts analysed from six
  sites; 47 attributed to the three named Gujarat
  source areas (Mardak Bet 26, Khandek 16, Ratanpur 5);
  9 assigned to the proxy group and excluded from the
  counts. Named-source determinations per site: Harappa
  20, Mohenjo-daro 7, Mehrgarh 7, Chanhu-Daro 5,
  Nausharo 5, Nagwada 3.
- **Alabaster (Sr/S isotopes).** 33 artifacts in the
  analysed set: Harappa 29 (attributed regionally, to
  Salt Range units), Mohenjo-daro 1 (matched none of
  the examined source regions — not attributed, not
  counted), and 3 from Musa Khel and Rehman Dheri,
  which are not gazetteer sites and sit outside the
  site universe. No new link-eligible site, no new
  linked pair.
- **Vesuvianite-grossular (INAA).** Chapter 9 is not in
  the posted set. The posted summary names the two
  sites analysed (Harappa and Mohenjo-daro) and the
  matched regions (Balochistan and the NWFP) but gives
  no per-site counts, so this study contributes **0
  countable determinations**. Both sites are already
  link-eligible via agate and their pair is already
  linked, so the missing chapter changes no count —
  recorded as a limit of the posted set, not filled in.

**Totals.** 76 counted named-source determinations
(47 agate + 29 alabaster). Sites meeting the frozen
link-eligibility floor (at least 3 named-source
determinations): **6** — Harappa (49 across both
studies), Mohenjo-daro (7), Mehrgarh (7), Chanhu-Daro
(5), Nausharo (5), Nagwada (3). Site pairs sharing at
least one named source, counted only where the posted
text states the sharing with certainty: **13 of the 15**
pairs among those six sites. The remaining two pairs
(both involving Mehrgarh) turn on per-artifact
assignments that sit in the print-only appendix table;
they are recorded as **uncertain, not linked** — never
resolved by guesswork. The Meluhha compilation
contributes **0** links, as frozen (F031-C04).

Inside the design's actual site universe, the picture
is far thinner: of the six link-eligible sites, only
**Harappa and Mohenjo-daro are Stage 0 gazetteer
sites**, and they share one named source (Mardak Bet)
— **1 linked pair** in-universe.

## 4. Margins step — the population record

Computed per arm under sections 3–4 from the Stage 0
gazetteer (36 source-asserted rows, 30 program sites)
and the link construction above. Population record
SHA-256:
`a0c98d56780051b46795621b644457e7674f7266321073e65a67ef51f83b54b8`
(full record in `reports/phase395_results.json`).

| Screen | Sites passing |
|---|---|
| Gazetteer sites | 30 |
| Defensible coordinates (section 6) | 21 |
| Period-eligible (section 6, labels as published) | **0** |
| Bead/craft floor evidenced | 0 (not countable, section 2) |
| **Eligible — bead/craft arm** | **0** |
| **Eligible — ceramic arm** | **0** |
| Linked pairs among eligible sites (either arm) | 0 |

**Why the period screen is empty.** This is a property
of the frozen record, stated exactly: the gazetteer's
`period_label_as_published` is empty on 33 of its 36
rows, and the only labels present anywhere are
"PN"/"Neo." (pre-Neolithic / Neolithic) on three
Central Asian sites — labels that do not indicate
Mature Harappan occupation. Its
`program_period_assignment` is empty on all 36 rows.
The frozen test (spec section 6; claim F031-C10) admits
a site only when one of those two fields, as published,
indicates Mature Harappan occupation. No site passes.
Reading eligibility off other fields, or off the
chronology spine, would be exactly the inference the
freeze forbids (adopted 4A; Spec 027 section 5.2
discipline), so it was not done.

**Closures (in writing, at margins, as frozen).**

- **Bead/craft arm — NOT-YET-TESTABLE** (section 4.3):
  0 eligible sites against the frozen minimum of 8, and
  0 linked pairs among eligible sites against the
  minimum of 10. The arm is not re-based on the
  sensitivity tier, on a lower threshold, or on the
  ceramic arm's site set.
- **Ceramic arm — NOT ESTIMABLE** (section 4.2, DD-7):
  sources at audited postures cannot evidence the
  frozen minimum of 8 eligible ceramic sites — they
  evidence 0, on the period screen alone (and only two
  sites have classification-bearing reports at an
  audited posture at all). No ceramic response was
  computed.
- **Sensitivity tier: not constructed.** The freeze
  computes it only alongside a testable primary arm
  (section 4.3); there is none. Chapter 4 is also
  absent from the posted set.
- **River-network distance (DD-8): not pinned.** The
  pin belongs to pair construction in the outcome
  step; no pair set was constructed and no distance
  was computed.
- **Population reproduction** (the section 5.2
  precondition) is moot: no outcome run exists whose
  population could fail to reproduce.

A second margins fact is recorded for completeness,
although the closures above do not rest on it: even
the link side, inside the gazetteer universe, stands
at 2 link-eligible sites and 1 linked pair — far below
the frozen viability floor of 8 eligible sites and 10
linked pairs. The provenance literature's site
coverage and the gazetteer's site universe barely
overlap.

## 5. Statuses

| Arm | Status | Basis |
|---|---|---|
| Bead/craft | **NOT-YET-TESTABLE** | Section 4.3 viability fails at margins (0 eligible sites, 0 linked pairs among them) |
| Ceramic | **NOT ESTIMABLE** | Section 4.2 / DD-7: audited-posture sources evidence 0 of the required 8 eligible sites |

These are registration statuses assigned at the margins
step, before outcomes exist (spec section 5.2) — they
are not verdicts, and no verdict (SUPPORTED /
CONTRADICTED / INCONCLUSIVE / INVALID) exists for
either arm. Q7 itself remains owned by Spec 027
(F027-C15); this execution changes no Spec 027, 028,
029 or 030 record (the cross-record filed under Spec
027 is a new pointer file only). No outcome here
upgrades Q1, and none says anything about people,
workshops as populations, migration, or language
(F031-C01).

## 6. Claim stage determinations (Spec 029 machinery)

Recorded in this outcome record only; the frozen
register (`claims.json`) is not edited. No claim is
explained, accepted or digested — those are human-lane
outcomes the machinery cannot manufacture.

| Claim | Determination | Basis |
|---|---|---|
| F031-C01 | No change | No verdict was issued whose scope could be assessed; the closures are statuses, and both were kept inside the claim's boundary (craft evidence only). |
| F031-C02 | Checked (execution) | The primary link set was built under the claim's rule and contains only INAA / Sr-S-isotope determinations to named source areas; proxy-group assignments excluded by construction and fenced by test. |
| F031-C03 | Checked (execution) | Reference-based (Chapter 4) assignments entered no set; the labelled sensitivity tier was not constructed, per section 4.3's condition. |
| F031-C04 | Checked (execution) | The Meluhha compilation contributed zero links; it appears nowhere in the link construction. |
| F031-C05 | Checked (execution) | The two arms were screened, counted and closed separately, on the same gazetteer universe but never pooled. |
| F031-C06 | No change | The bead response was never assembled (the arm closed at margins); its source record was honoured — the classification basis and its limits are documented in section 2 — but the claim's proposition was not exercised. |
| F031-C07 | Checked (execution) | The claim's own condition fired: the margins step could not evidence 8 eligible ceramic sites, and the arm closed NOT ESTIMABLE with no ceramic response computed. |
| F031-C08 | Checked (execution) | The bead/craft arm failed the frozen viability thresholds and closed NOT-YET-TESTABLE without re-basing on weaker links, exactly as the claim requires. |
| F031-C09 | No change | No verdict was issued on any arm, so the claim's verdict-gating proposition never arose; the control machinery it names was exercised only on synthetic fixtures in the build tests. |
| F031-C10 | Checked (execution) | Period eligibility was applied from the Stage 0 labels exactly as published; no pair was admitted on any finer or inferred assignment, and no sub-period variant was tested. |
| F031-C11 | Checked (execution) | No released row is derived from a read-only source: the digitisation stays in the gitignored local store; the committed products carry counts, site identities from the gazetteer, and hashes only. The registration half of the claim was discharged before execution (OSF record). |
| F031-C12 | Checked (execution) | Every threshold applied is the frozen D8-margin value (floors 3 / 10 / 20; viability 8 / 10; margin 0.02), enforced as build constants and pinned by `test_frozen_constants`. |

## 7. What remains not understood, and open items

- The per-artifact assignment tables (print-only
  appendices) would settle the two uncertain
  Mehrgarh pairs and the vesuvianite-grossular counts.
  They were not lawfully reachable in this execution;
  the counts above stand at the granularity the posted
  text supports, with the gaps named.
- Whether Q7 can ever be tested inside this program
  turns on a record this execution was forbidden to
  change: the Stage 0 gazetteer carries no Mature
  Harappan period assignment for any site. A future
  Spec 027 gazetteer act — making program period
  assignments under its own adjudication, with the
  mapping rule and reviewer recorded, as Spec 027
  section 6.2 provides — is the named route that would
  change the period screen. It is a separate owner
  decision; nothing in this record pre-judges it.
  Even with such an act, the in-universe link mass
  (2 sites, 1 pair) would still fail the frozen
  viability floors by a wide margin; that gap is a
  property of the published provenance record itself
  (almost 120 other-site determinations, concentrated
  at sites the gazetteer does not carry).
- Nothing here re-opens the sensitivity tier,
  dose-response, or any sub-period variant: all remain
  as the freeze declared them.

## 8. Products and gates

`reports/phase395_results.json` (the full margins
record, with input hashes),
`reports/phase395_margins_report.md`, this outcome
record, and the Spec 027 cross-record
(`specs/027-movement-culture-language/stage2-q7-outcome-cross-record.md`).
Build: `backend/scripts/phase395_q7_execution.py` via
the experiment graph node `IndusPhase395Q7Execution`
(H23 steps 1–5; PR #196 + this record's PR). Gates:
foundation check 40 passed / 0 failed / 8 warnings;
full backend suite green in CI on PR #196 (1,409
passed / 20 skipped / 0 failed) and on this PR (see PR
record); branding sweep clean. The digitised link data
stays in the gitignored local store and is not part of
any product (F031-C11).

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
