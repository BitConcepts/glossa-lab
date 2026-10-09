# Tasks — Spec 023 / Keyed Transcription Layer over CISI Vols. 1–2

> **FROZEN 2026-10-09** with spec 023 (owner:
> Tristen Pierson — "merge #99 and execute the new
> plan"). The build is **Phase-132** (Stage P pilot).
> Stage T tasks are written only after the post-pilot
> owner decision (T9).

## Pre-freeze (owner)

- [x] T0 Owner adjudication of spec §11 Decision
  Asks 1–5 — answered 2026-10-09 with the proposed
  values as drafted (recorded in spec §11 freeze
  record and §5.6 freeze block); DRAFT banner
  replaced by freeze header; frozen spec committed
  alone (this commit).

## Stage P — Pilot = Phase-132 (starts only after T0)

- [ ] T1 Frame draw: deterministic ~50-object pilot
  frame per spec §3.1 (strata 25/15/10; ~10
  mayig-overlap objects), rule + seed recorded;
  frame published with the pilot report.
- [ ] T2 Pass workspaces + blindness plumbing in the
  local store (§5.5): isolated pass areas, no access
  to existing transcriptions of frame objects,
  provenance fields (pass role, date, blindness
  attestation) wired to intake schema v1.
- [ ] T3 Orientation declarations (§5.1) recorded for
  all frame objects before any transcription.
- [ ] T4 Pass A and Pass B executed blind; pass files
  committed to the local store under lock (hash +
  timestamp) before either is visible to the other
  side or to adjudication.
- [ ] T5 Adjudication of all inter-pass
  disagreements; adjudication log preserved;
  ambiguity log (§4.3) closed for the pilot frame.
- [ ] T6 Gold sample (20%): third independent pass +
  adjudication; error-rate estimator applied as
  frozen; quality measurements vs §5.6 gates and
  the §3.1 stop-rule evaluated and reported as found.
- [ ] T7 Pilot dataset assembled (intake schema v1),
  intake validator + license gate + spec-018 dedup
  run; §7 coverage/attestation checks recorded.
- [ ] T8 Pilot report: frame as drawn, counts,
  measured per-object effort, agreement + error
  measurements, UNK / crosswalk-unmapped rates,
  ambiguity counts — the Stage-T decision input.
  Ledger entries (both ledgers; AI disclosure);
  anchors sha256 asserted unchanged.
- [ ] T9 Stage-T owner decision (Decision Ask 2,
  revisited with pilot numbers in hand). Stage T
  tasks are written only after this decision.

## Explicitly not tasks of this build (any stage)

- Any positional profile, TV distance, agreement
  statistic about an existing compilation, or PRED
  evaluation — each requires its own frozen spec
  (spec §12).
- Any anchor, claim, PRED, or status change.
- Any use of Holdat `cisi_number` as a key, field,
  or selection criterion (spec §4.3 prohibition).
- Any publication of plate images, renders, or
  crops; any back-filling of museum / material /
  dimensions fields (spec §4.2).
- Any contact with outside parties (including data
  holders) — external correspondence is not part of
  this build.
