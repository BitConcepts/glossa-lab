# Amendment 6 to Spec 083 — The T027 chip wording: the shipped dataset chip stands (owner, 2026-11-05)

**Status**: Adopted by the owner's decision of 2026-11-05. This
amendment corrects one task text (T027) to the shipped reading and
changes nothing else: no design, no claim, and no shipped code is
affected. Amendments 1–3 and 5 are unaffected; Amendment 4 remains
superseded in full by Amendment 5. Where this amendment and any
earlier text differ, **this amendment governs**.

## 1. The decision, in the owner's terms

Task T027's text named an "install chip (desktop install revision ·
source commit · origin health — Amendment 5's replacement for the
retired dataset/bundle chip)". The frontend as shipped (Step 3,
PR #476) carries no such component. What shipped is the **dataset
chip**: the wireframe-07 program-surface header chip
(`frontend/src/cloud/widgets.tsx`, `DatasetChip` / `DatasetChipRow`,
rendered on the program surfaces), whose text is:

> Dataset <bundle id> · source <commit> · hydrated <time>

The flagged ambiguity — the task text's install chip against the
shipped dataset chip — was put to the owner, and the owner ruled:
**the shipped UI stands, and the task text is corrected to match
it.** The install-chip wording is retired as a drafting error
carried in Amendment 5's task text; no install chip was built, and
none is owed.

## 2. The correction

- `tasks.md` T027 now reads "dataset chip (Dataset <bundle id> ·
  source <commit> · hydrated <time> — the wireframe-07
  program-surface header chip as shipped; text corrected to the
  shipped reading by Amendment 6, 2026-11-05)".
- `plan.md`'s carryover description carries the same superseded
  phrase ("the install chip (desktop install revision · source
  commit · origin health…)"); it is not edited by this act, and
  this amendment governs over it wherever the two differ.
- The check-off state of T027 is unchanged: the step was verified
  against the shipped screens at Step 3, and this correction moves
  no verification result.

*This amendment does not establish:* that the dataset chip is the
right header element — only that it is the one that shipped, that
the task text now says so, and that the owner's ruling, not the
drafting error, is the record.
