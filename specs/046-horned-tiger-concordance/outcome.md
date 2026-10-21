# Spec 046 / Phase-405 — Outcome record (EXECUTED 2026-10-21 — IDENTIFICATION FAILED, sign unmatched)

> ## EXECUTED — 2026-10-21
>
> Executed under the frozen Spec 046 contract
> (freeze-act digest
> `80c3be31e5af5236f71cb2c1894b2946f9b8ad47b12bdeab9d03cd76468af405`;
> successor digest
> `e0d7add84b9d28ae5f6a6b392dca578b727ad4d99a117360a57d39f3b94b01c6`
> in `freeze.json` as merged, PR #245 merged at
> `881947a0`), as **Phase-405**, in Wave 3 group 1
> of the runnable-experiments campaign (plan
> approved AS WRITTEN on 2026-10-21), before
> Asset A freezes. The execution gate was
> satisfied before the run: OSF registration
> **dnts8** is APPROVED + PUBLIC. Outcome:
> **IDENTIFICATION FAILED (sign unmatched)** —
> step 0 passed in full, step 1 named the
> source's list from the book's own apparatus,
> and the drawn sign could not be matched by
> drawn form from the held record. No list was
> scored, no statement about the sign is made,
> and nothing is fed to Asset A.

## 1. What was executed

The frozen contract's execution shape (spec §12),
in order. Graph-first build (H15/H23): experiment
script `backend/scripts/phase405_concordance.py`;
graph module
`backend/glossa_lab/experiment_graph_phase405.py`
(node `IndusPhase405HornedTigerConcordance`);
registration in
`backend/glossa_lab/experiment_graph.py`; the
registration verified by import in the run
environment before the phase ran (the node is
present in `ATOMIC_NODES`). The run's own records:
`reports/phase405_results.json` (SHA-256
`88f6cd1636a9a402c48cb76ec0bce6fc5d328423428816785e76cadf6d8c99e6`)
and `reports/phase405_concordance_report.md`. The
delivery of record:
`specs/046-horned-tiger-concordance/concordance-297.json`,
SHA-256
`772db4df152ec4f1071bed088250677e55f69743532c9e89f339a8cf9134aaaf`
(derived twice by independent routes — the
`sha256sum` tool and a Python `hashlib` recomputation
— with identical results; the script is deterministic
and a second run reproduced both output files
byte-identically).

**Headline (spec §5.3 wording, IDENTIFICATION
FAILED form).** "The fragment 'sign 297 is the
horned tiger' cannot be carried to a concordance:
the drawn sign could not be matched from Wells's
published list. The record stays a stated gap. No
statement about the sign is made, and nothing is
fed to Asset A."

**The passage (spec §8, element 1), quoted with
its locator.** Wells (2015), printed p. 97 (held
cleaned text, lines 2938–2941):

> "Sign 532 and sign 297 are positioned in such a
> way as to resemble the position of the graphic
> element and several of their features are
> repeated in the image field. It is proposed here
> that sign 532 is a logograph for the
> anthropomorphic figure and that sign 297
> represents the horned tiger, or perhaps just
> ‘tiger’ generically."

**Fence sentence (spec §8, element 5).** "This
result settles what the published lists say the
drawn sign depicts. It is not evidence of what
the sign meant in use."

## 2. Step 0, gate by gate (all passed)

- **0.1 Input integrity — PASS.** Every spec §2
  input was recomputed at the run's base
  (`main` at `9786265a`) by two independent routes
  (a fresh clone's working tree and the GitHub
  contents API), with identical results, and each
  hash matches its frozen pin: claim record
  `bd0f7abddc9c26537f4ebe5f66f6a1fc69d394a4c2edbe745a8b7eb1ddc3333a`;
  held cleaned text of Wells 2015
  `62acf855ac3ecf39fc7a7e6597dba9a3cb6e35948528f69e9424eb81308d261e`;
  Phase-104 evaluation
  `2d0b83e8055a04b96635007054cfadde472f605dc7e5b249a61c8f9ea89b858d`;
  crosswalk registry (803 rows)
  `8a0b2a82ac8d226d574ce01f5550c581efd91a97cab86201a62f7a7e435bd420`;
  lane-2 adopted drafts
  `3f645c9a4132ba5a0bc5fca4ca22810b8b6169a2f1f9f85f35990c7b72df33fb`.
  The phase script re-verifies all five pins
  fail-closed before any output is written.
- **0.2 Source producible — PASS.** The source
  book was produced from the program's held copy
  (the pin-verified cleaned text) and the §1
  passage was located in it verbatim (quoted
  above).
- **0.3 All four lists producible or citable —
  PASS.** Each list of record is accounted for
  with its citation and locator form, verified
  against the program's citation record
  (CITATIONS.md): **WELLS** — HELD (the held
  cleaned text itself; §A.7; locator chapter/
  figure plus the book's own sign number);
  **CISI** — HELD (Vols. 1–2, §§A.2–A.3; the
  Phase-124 catalogue layers: committed local-store
  manifest present, catalogue files
  `cisi_vol1_catalogue.csv` /
  `cisi_vol2_catalogue.csv` verified present in
  the program's local store; locator volume plus
  catalogue/object entry plus page or plate);
  **PARPOLA** — CITABLE (*Deciphering the Indus
  Script*, 1994, §C.1; locator P-number; the
  registry is keyed to Parpola 1982 numbering);
  **MAHADEVAN** — CITABLE (*The Indus Script:
  Texts, Concordance and Tables*, MASI No. 77,
  1977, §A.1; locator M-number plus
  concordance/tables page or entry; Mahadevan
  crosswalk data held in the pinned registry).

## 3. Step 1 — identification

**1.1 The source's sign list, named from the
document — NAMED.** The passage names no list at
the passage itself; the book's apparatus names it:
"Chapter 2 gives the Indus sign list used in this
analysis"; "The sign list used here (Wells 2011)";
Chapter 2 is "The Indus Sign List" and its
Figure 2.6 is "An Indus Sign List". The numbering
of the passage is Wells's own — Wells 2011, as
given in Wells 2015, Chapter 2 / Figure 2.6 —
exactly the list of record fixed at the freeze
(DD-046-10).

**1.2 The drawn-sign match — FAILED.** Wells's
sign 297 could not be matched by drawn form:

- The pinned crosswalk registry carries **no
  entry for the drawn sign**. Its only `W297`
  value sits inside the 17-value `wells_ids` cell
  (`W289|…|W306`) on the P205 row, whose
  description is "Prismed light rays, with
  opposite slanting on top vs bottom, more rays
  on bottom" — the trap the frozen spec names in
  advance (§4.3): that cell does not by itself
  identify the passage's sign, and it was not
  used as a match. No registry row carries `W297`
  as its sole Wells value, and no registry
  description names a tiger (0 of 803 rows).
- The registry's other 297 is Parpola's P297,
  described as "Ladder motif. Two nearby vertical
  lines with a number of horizontal lines going
  across the middle…" — a different sign, the
  second frozen trap. It was not used: numbers
  are not identities (F046-C07).
- The Phase-123 Wells segmentation witness (157
  signs) carries **no Wells grapheme 297**.
- In Wells's published list itself (Figure 2.6),
  the drawn forms **did not survive the held
  copy's text extraction**: the figure's pages in
  the held cleaned text carry captions only, so
  no drawn-sign reference exists in the held
  record that the executor can inspect and defend
  (spec §7: a match that cannot be defended from
  the recorded reference fails step 1 rather than
  being argued at scoring time). The word "297"
  occurs in the held text only in the passage
  itself.
- The prior in-repo search stands unrebutted:
  Spec 004 WS2 (`glossa-indus/LEDGER.md`,
  2026-10-05) recorded for this fragment three
  candidate referents — M297, P297,
  W297→P205/M180 — "**none matching the
  description in-repo**". The Phase-161/165
  extraction's keying of the passage under "M297"
  is number-identity keying of Wells numbers, the
  inference the frozen spec forbids and the
  program's crosswalk work holds back as
  unadmitted; it is not drawn-form evidence.

The execution therefore closes at step 1 under
the frozen class **IDENTIFICATION FAILED (sign
unmatched)**, with the §5.3 wording above. What
would unblock a future concordance is a record
outside this frozen run's inputs: an inspectable
drawn-form reference for Wells's sign 297 (for
example the Figure 2.6 figure pages as images, or
a published drawn-form cross-match for this sign)
preserved as a committed, hashed record. This
record does not commission that act.

## 4. Step 2 — scoring (not reached)

No list was opened for scoring, no row exists,
no concurrence state was computed, and the
§5.2 mapping was not engaged. The delivery
carries the frozen closure form instead of rows
(spec §6): `signs` is an empty array and the top
level carries `closure: {class, wording}`. An
empty feed is a stated state, never an absent
file: **nothing is fed to Asset A**, and Spec
045's build proceeds without this feed and
records its absence, per spec §8 — the closure
does not block the asset, and the asset may not
reconstruct the feed from its own labels.

## 5. What this outcome does and does not establish

It establishes that, on the held record, the
fragment cannot be carried to a concordance:
the source's list is named (Wells's own), and
the drawn sign that list numbers 297 is not
identified by any held record the frozen rules
allow — not by the crosswalk registry, not by
the Wells witness, and not by an inspectable
reference to Wells's published list entry in
the program's held copy. It does **not**
establish anything about the sign itself: not
that Wells's identification is wrong, not that
any list disagrees with it, and nothing about
what the sign meant in use (spec §9). The
hypothesis of §1.2 was neither supported nor
falsified on concurrence grounds — no list was
scored, so the falsifier's concurrence test
never ran; what fired is the identification
gate in front of it. The record stays a stated
gap.

## 6. Claim consequences (governed register)

Executed under register 0.7-draft (frozen); one
line per claim, F046-C01…C15.

- **F046-C01** (an outcome states only published-
  list concurrence on this sign's identification):
  HELD — the outcome states no concurrence and
  nothing about the sign; it records an
  identification gap only.
- **F046-C02** (the record under test is this
  fragment): CHECKED — the claim record was read
  and pin-verified at gate 0.1; its verbatim
  wording, UNTESTED status, and Phase-104 RULE-NUM
  stop are as the frozen record states.
- **F046-C03** (the identification is the
  published consensus): NOT REACHED — no list was
  scored; the hypothesis is unjudged, neither
  supported nor falsified on concurrence grounds.
- **F046-C04** (a non-concurrence outcome is
  recorded with CONSENSUS-level prominence):
  NOT REACHED in its scoring sense — no
  non-concurrence outcome arose; the closure is
  recorded with the same prominence (§9.5).
- **F046-C05** (execution closes at step 0 on a
  step-0 gate failure): HELD — the gates ran in
  the frozen order before any identification
  work; all passed, so no step-0 closure arose.
- **F046-C06** (step 1 names the list from the
  apparatus; the drawn sign is matched by form,
  or the execution closes as IDENTIFICATION
  FAILED with the reason named): FIRED — the
  list was named from the apparatus (§3.1 of this
  record) and the execution closed as
  IDENTIFICATION FAILED (sign unmatched) with
  the reason named (§3.2).
- **F046-C07** (cross-list matching is by drawn
  sign; numbers are not identities): HELD — no
  number-match was used or attempted as a match;
  both registry traps (P297 the ladder motif;
  W297 inside the P205 multi-value cell) were
  asserted as traps in the run's record.
- **F046-C08** (Wells scores as SOURCE, never
  toward CONSENSUS): NOT REACHED — no rows were
  scored, so the counting rule was not engaged.
- **F046-C09** (each row carries one scored state
  from AGREE / DISAGREE / SILENT): NOT REACHED —
  no rows exist.
- **F046-C10** (the concurrence state comes from
  the §5.2 mapping over the four rows): NOT
  REACHED — no rows, no state computed.
- **F046-C11** (the delivery is
  `concordance-297.json` in the §6 form, produced
  on every terminal outcome): HELD — the file was
  produced in the closure form (empty `signs`,
  `closure` block), digest recorded in §1.
- **F046-C12** (the concordance draws solely on
  published-list sources; no Asset A material,
  labels, or positional results): HELD — the run
  consulted only the four lists' records of
  record, the citation record, the crosswalk
  registry as matching instrument, and the
  program's in-repo search records; no Asset A
  material, depicted-kind label, or positional
  result was consulted at any point.
- **F046-C13** (every outcome product carries the
  §8 reporting elements): HELD in the closure
  form the claim's own boundary prescribes — the
  passage quoted with its locator (§1), the
  closure wording and closure block in place of
  rows the run does not have, the gate-0.3
  accounting for all four lists (§2), the
  delivery exactly as delivered (§4), and the
  fence sentence (§1).
- **F046-C14** (an outcome establishes
  identification-layer agreement only): HELD —
  no statement beyond the identification layer
  is made; no generalisation from this one sign,
  and no reading of any inscription.
- **F046-C15** (the claim record receives a dated
  first-check append, in the §5.3 wording, with
  the frozen records unedited): HELD — the append
  was made to the claim
  `the_archaeology_and_epigraphy_of_indus_w_27f45a68_sign_val_0002`'s
  record as a new `first_check` entry (Phase-405,
  2026-10-21, the §5.3 wording, the delivery digest);
  verification at the act: removing the appended
  entry reproduces the pre-act file byte-identically,
  and the claim's status and stage are unchanged.
  The Phase-104 evaluation and the lane-2 adopted
  explanation were not edited.

**Anchors.** `backend/reports/INDUS_FINAL_ANCHORS.json`
recomputed before and after the run: SHA-256
`df0cf620a0d66b71d778300b93a91d96b2f30f23580088e6086592b32d34f569`
at both points — byte-identical, asserted.

## 7. Records

- Delivery: `specs/046-horned-tiger-concordance/concordance-297.json`
  (SHA-256 in §1); results record:
  `reports/phase405_results.json`; report:
  `reports/phase405_concordance_report.md`.
- Claim first-check append: `first_check` entry on
  the claim's record (see F046-C15 above).
- Root LEDGER entry: "Spec 046 (Phase-405)" entry
  added with this record.
- Handover to Spec 045: the empty-feed state is
  the delivery; Asset A's step 1 consumes
  `concordance-297.json` in this closure form (or
  records its absence as a feed) — no other
  handover artefact exists, by design.
- CI and foundation check (H21) at the record
  merge: appended below after the record PR
  merges, in the Spec 039 completion pattern —
  this section is completed by append, not
  edited.

---

*AI disclosure: executed by an AI agent (Muse Spark,
via Muse) at the direction of Tristen Pierson, per
constitution §VI.*
