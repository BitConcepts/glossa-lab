# Blinding protocol v1 — W1 independent coding (full blind)

**Spec:** 091-anchor-comparison-integrity, Stage 1, task T102.
**Claim:** C091-2 (protocol side). **Version:** v1 (2026-11-17).
**Ratified substance:** decision D-091-2, ratified as a block by
the owner at T003 (record:
`records/ratification-2026-11-06.md`). **Status:** filed before
any coding starts, as C091-2 requires. This is the coder-facing
document: it is written to be handed to the engaged coder as-is.

## 1. Purpose

The Mahadevan–Parpola crosswalk's readings are to be coded from
their primary sources by a coder who did not derive the project
readings, so that the eligibility recomputation (eligibility-defs
v1) rests on evidence independent of the project's derivation.
This protocol is the standard that independence is judged
against. Compliance is Stage 4's oracle act (T401); this filing
establishes the standard, not any coder's compliance with it.

## 2. What the coder receives (inputs)

The coder receives, per crosswalk entry assigned to them:

1. The **primary sources** named by the locator record for that
   entry's reading fields — the works themselves, at the
   entry-level locators the locator record carries.
2. The **sign list**: the sign-number correspondence the entry
   turns on (Mahadevan ↔ Parpola numbering) and the sign
   identities needed to find each sign in the primary sources.
3. The **coding sheet**: per entry and reading field, the
   locator (work, pinpoint, sign scheme), blank fields for the
   coded value exactly as the source prints it, and the source
   revision (edition / printing) coded from.

Nothing else is an input. In particular the coder does not
receive the staged crosswalk file, the anchor table, or any
project publication.

## 3. What the coder never sees before filing (exclusions)

Until the coder's coding is filed (§5), the coder must not be
shown, and must not consult:

1. The **project readings** — the anchor table's reading for
   any sign in the assignment, in any form (including project
   publications, the tracker, or the preprint line).
2. The **WP4 classifications** — the provenance classification
   of any entry (independently sourced / used during candidate
   construction / project-derived / unverified / ineligible),
   and any count or summary of them.
3. The **audit dispositions** — the WP5 anchor-support audit's
   classes and the register's routing of any anchor.
4. Any project member's expectation about any entry's coded
   value, expressed in any channel.

The blind is **full**: it covers readings and classifications
alike (D-091-2 option (a), as ratified). A coder who has
previously worked from the project readings or classifications
for an assigned entry is inside the derivation lineage for
that entry and cannot code it; §6 applies.

## 4. The coding act

For each assigned entry and reading field, the coder records,
from the primary source at the cited locator and from nothing
else:

- the value exactly as printed (byte-for-byte, with its
  diacritics), or a **not attested** outcome where the source
  at that locator does not carry a value for the sign;
- the source revision coded from;
- any ambiguity in the source's presentation, noted as found
  (alternative printed forms are all recorded, not resolved).

The coder does not compare the coded value against any other
value, does not score agreement, and does not learn whether a
coded value matches anything. Agreement is computed later, by
the recomputation, from the filed records.

## 5. The filing act that ends the blind

The blind for an assignment ends at a single act: **the coder
files the completed coding record** — the coding sheet of §2.3
with every assigned entry/field carrying a coded value or a
not-attested outcome, signed with the coder's identity and the
date, and delivered to the project through the channel the
engagement names. Filing is per assignment (the whole assigned
set), not per entry: a partial filing does not end the blind
for the remainder.

Only after the filing is on record may the coder be shown the
project readings or classifications, and any post-filing
discussion is recorded as post-filing. A coded value changed
after filing is not an amendment of the coding: it is a new
record, and the change, its reason, and its post-filing status
are recorded with it; the recomputation consumes the filed
coding, and a post-filing change is handled as a deviation
(§6) unless the change is itself filed as a fresh blind coding
by a coder still blind for that entry.

## 6. The deviation rule

A **deviation** is any departure from §§2–5: exposure to an
excluded input before filing (by any route, including the
coder's own prior work), coding from a source other than the
cited primary source at the cited locator, assistance from a
person inside the derivation lineage on an entry's value, or
a post-filing change not handled per §5.

- Every deviation is **recorded**: the entry or entries it
  touches, what happened, when it was discovered, and who
  discovered it. An unrecorded deviation discovered later is
  recorded when discovered; concealment is itself recorded.
- A deviation **voids the coding it touches** (C091-2). The
  affected entries are then either **redone** — by the same
  coder only if the deviation left them blind for those
  entries in fact (a judgment recorded with its reasons), or
  by another lineage-excluded coder — or they **fall back to
  their WP4 classes** in the recomputation (eligibility-defs
  v1 §4).
- A deviation that touches the assignment as a whole (for
  example, exposure to the classification summary before
  filing) voids the assignment's coding as a whole.
- The deviation record is part of the coding record and is
  filed with it or, for later discoveries, appended to it as
  a dated supplement. Stage 4's protocol-compliance record
  (T401) rules on the filed protocol against this document.

## 7. Who may code (lineage exclusion)

The coder must be outside the derivation lineage of the
project readings: not an author of the anchor readings, the
crosswalk, the WP4 classification, or any derivation the
readings rest on, and not a person whose prior work on these
entries used the project readings as inputs. The coder's
identity and the lineage-exclusion statement are part of the
coding record (eligibility-defs v1 §3.2 consumes them).
Engaging the coder is the owner's D-091-1 act; this protocol
names the standard the engaged coder works under, and nobody
is contacted by this filing.

## 8. Mapping to the ratified record (the reviewer's table)

| # | Protocol element | Ratified source it restates |
|---|---|---|
| P1 | Full blind: sources + sign list visible; project readings and WP4 classifications never visible before filing (§§2–3) | D-091-2 option (a), ratified at T003 (`records/ratification-2026-11-06.md`, D-091-2 entry); spec.md D-091-2 |
| P2 | Inputs are the primary sources and the sign list (§2) | D-091-2: "the coder sees the primary sources and the sign list" |
| P3 | The filing act ends the blind (§5) | D-091-2: "until their coding is filed"; C091-2: "the blinding protocol filed before coding starts" |
| P4 | Deviations void the coding they touch; redo or fallback to WP4 classes (§6) | spec.md D-091-2: "Any deviation from the filed protocol voids the coding it touches (C091-2)"; C091-2: "a deviation voids the coding it touches, which is then redone or the affected entries fall back to their WP4 classes" |
| P5 | Coder outside the derivation lineage (§7) | C091-2: "coded … by a coder who did not derive the project readings"; D-091-1 (engagement is the owner's act) |
| P6 | Protocol filed before coding starts; compliance judged later against it (§1) | C091-2; tasks.md T102's "does not establish" line |
