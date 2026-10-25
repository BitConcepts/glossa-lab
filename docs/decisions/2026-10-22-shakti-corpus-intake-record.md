# Shakti corpus intake record — P-F1 as adopted (2026-10-22)

**Date:** 2026-10-22
**Owner act:** Proposal P-F1 adopted as written by Tristen Pierson on
2026-10-22 (see
`docs/decisions/2026-10-22-shakti-readiness-decisions.md`, decision 1).
**Status:** This is the standing citation form for the Shakti corpus.
A successor spec cites the corpus only through this record.

This record states the intake gates for *this* corpus. It replaces
nothing: the V1–V4 loader-verification gates remain in force,
unchanged, for the RMRL dump route they were written for.

## Corpus identity

- **Corpus:** ShaktiOSindia reproducibility deposit,
  `sanitized_corpus.json`
- **File size:** 1,570,041 bytes
- **SHA-256:**
  `345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`
- **Upstream commit:** `e48b3ec1` (2026-08-12)
- **Licence, as stated by the deposit:** the corpus is GPL-3.0; the
  analysis scripts are MIT.
- **Where it is held:** restricted-local, at
  `~/workspace/research_notes/indus-data-deep-sweep-20261008/downloads/shaktiosindia-indus-sign-regimes-deposit/`
  — held under its GPL-3.0 terms, **never in git**. No part of the
  corpus file is committed to this or any other repository.

## Row-grades file

- **File:** `shakti_row_grades_2026-10-22.csv` — the row-level grades
  from the provenance audit of 2026-10-22 (all 5,704 rows, with match
  status, lineage status, and grade).
- **Where it is held:** beside the corpus, in the same downloads tree
  (`~/workspace/research_notes/indus-data-deep-sweep-20261008/downloads/`),
  restricted-local, not in any git repository.
- **SHA-256:**
  `02394241773cf8700f49ba19c30cdbaa589cf119d2c97c35e15e0447434dd739`

Stated plainly: the 2026-10-22 provenance audit recorded this file's
path but **no hash**. The hash above was computed on the held file
and is **pinned for the first time by this intake record**
(2026-10-22). Gate S1 below recomputes against this pin.

## Lineage evidence pin

- **Yajnadevam `population-script.sql`** — the upstream extraction the
  documented-lineage grade is measured against.
- **SHA-256:**
  `a1bcc150e91ede5e1c3ce813073d8ac7bfe370d2709be320132a651ba9c7a54c`

The copy in the Yajnadevam download and the copy vendored inside the
Shakti deposit are byte-identical, and both match the deposit README
pin (provenance audit, 2026-10-22).

## Census (the gate S2 figures)

From the provenance audit of 2026-10-22, counted in the file:

- **5,704 rows** in total;
- **5,536 analyzable** rows (excluding the 168 entirely-illegible
  all-`000` rows);
- grades: **3,212 documented-lineage** / **2,087
  undocumented-corroborated** / **405 undocumented-uncorroborated**;
- **4,904 of 5,536 analyzable rows (88.6%) carry a CISI identifier**;
- **18,065 true sign tokens** (ICIT-000 gated);
- **713 distinct signs** (ICIT-000 gated);
- **77 sites**.

Grade meanings, in plain words: *documented-lineage* means the row's
sign sequence occurs in the Yajnadevam/ICIT extraction under the
deposit's stated rule. *Undocumented-corroborated* means no upstream
match, but the identical sequence for the same CISI artefact is
present in the program's pre-existing ICIT-lineage layer,
census-verified. *Undocumented-uncorroborated* means no upstream match
and no lineage-layer check was possible. No undocumented row is
promoted out of the "undocumented" label by corroboration.

## The four gates, S1–S4 (adopted standing form)

The ShaktiOSindia corpus (`sanitized_corpus.json`, SHA-256
`345241b13fedada87b4783c24cd241123491bbd7edaf5bf636f9cdb36c01da68`)
is held restricted-local under its GPL-3.0 terms and cited only
through this intake record and the row-grades file of the 2026-10-22
provenance audit. A successor spec may cite the corpus only if its
step 0 asserts all of:

- **S1 — Identity:** the file's SHA-256 recomputes to the pinned
  value, and the row-grades file's SHA-256 recomputes to its pinned
  value as recorded in this intake record.
- **S2 — Census:** the corpus counts reproduce the audit's census:
  5,704 rows; 5,536 analyzable; grade counts 3,212 documented-lineage
  / 2,087 undocumented-corroborated / 405
  undocumented-uncorroborated; 4,904 of 5,536 analyzable rows
  (88.6%) carrying a CISI identifier.
- **S3 — Lineage statement:** every product of the citing spec states,
  in its headline block: "This corpus is an ICIT-lineage corpus.
  Agreement between it and the program's earlier ICIT-lineage layer
  is consistency within one tradition, not independent
  corroboration." A product without the statement does not cite the
  corpus.
- **S4 — Grade discipline:** rows graded
  undocumented-uncorroborated enter no count, statistic, or argument.
  Any load-bearing result computed over documented +
  corroborated rows is also computed over documented-lineage rows
  alone, and both are reported; a result that changes between the
  two is reported as grade-sensitive wherever it is cited.

Failure of S1 or S2 closes the citing spec at step 0 as
**SHAKTI INTAKE NOT REPRODUCED**. S3/S4 failures are integrity
findings, reported as such, not repaired silently.

## Citation rule

A successor spec cites the corpus **only through this record** and
asserts S1/S2 in its step-0 record. A citation that bypasses this
record, or a step 0 that does not assert S1/S2, does not cite the
corpus under the adopted form.

## What this record does not establish

- It does not establish that the corpus's transcriptions are correct.
  The provenance audit established lineage and internal consistency,
  and expressly did not verify any transcription against a non-ICIT
  tradition.
- It does not make the corpus independent of the ICIT lineage, and it
  qualifies the corpus for no gate that demands that independence.
- It changes no frozen record, register term, or campaign outcome.

---

*AI disclosure: produced by an AI agent (Muse Spark, via Muse) at
the direction of Tristen Pierson, per constitution §VI.*


---

## Definition note — 2026-10-25 (programme red team, finding C-5)

The grade **"documented-lineage"** in this record is a
**sequence-equality** measure: a row is graded documented when its
sign sequence occurs in the Yajnadevam/ICIT extraction under the
deposit's stated rule — not when that artefact's own reading is
documented. Verified by independent recomputation from the
deposit (2026-10-25): 3,212/5,704 rows match (56.31%), with 0
mismatches against the row-grades file on all 5,704 rows. Two
consequences every downstream use should carry: (1) only 1,790
distinct sequences stand behind the 3,212 documented rows, and
1,571 of the 3,045 primary-population rows (51.6%) share their
sequence with at least one other corpus row, so the grade
certifies the sequence, possibly on a different artefact; (2) the
corroborated tier (2,087 rows) depends on the programme's
pre-existing ICIT-lineage layer, which is not in the deposit, and
is not reproducible from the deposit alone. Read
"documented-lineage" throughout as "sequence-documented."
