# Plan — Spec 023 / Keyed Transcription Layer over CISI Vols. 1–2 (PROPOSAL)

> **DRAFT — PROPOSAL FOR OWNER ADJUDICATION — NOT
> FROZEN.** This plan describes the approach that
> *would* be executed if the owner approves spec 023
> (in whole or amended) and the spec is frozen under
> a separate freeze commit. Nothing in this plan is
> authorized yet, and no task in tasks.md may be
> started on the authority of this document.

## Approach (proposed)

1. **Adjudicate, then freeze.** The owner rules on
   spec §11's five decision asks. The approved values
   (tranche shape, gate thresholds, orientation
   convention, publication form) are written into the
   spec text, the DRAFT banner is replaced by a
   freeze header naming the approval, and the frozen
   spec is committed alone — the spec 021/022
   pattern. The build takes the next ledger phase
   number at that moment.
2. **Pilot before scale, always.** Stage P (~50
   objects, §3.1) exists to measure the three unit
   quantities the whole program currently lacks:
   per-object effort, inter-transcriber agreement,
   and adjudicated per-sign error. Its stop-rule is
   part of the design, not an embarrassment clause:
   a pilot that stops the build has done its job.
3. **Keys from plates, never from OCR.** The
   Phase-124 catalogue is the frame and locator; the
   canonical key is the transcriber-read printed ID,
   volume-scoped (§4.1 — the `H-311` cross-volume
   collision is the standing reminder of why). The
   ambiguity log, not adjudicator discretion, absorbs
   every keying exception.
4. **Blindness as infrastructure.** Pass isolation is
   enforced by process, not by promise: separate pass
   workspaces in the local store, no access path from
   a pass workspace to existing transcriptions of the
   same objects, per-object blindness attestation in
   provenance (§5.5). The gold sample's third pass
   (§5.6) is what turns "we were careful" into an
   error rate.
5. **Born conformant.** Records are written against
   intake schema v1 from the first pilot object, and
   the intake validator + license gate + spec-018
   dedup module are run at every stage close — the
   layer never needs a retrofit to be consumable
   (spec §6, §9.4).
6. **Publication is sequences and metadata only.**
   Plates, renders, crops, and pre-adjudication pass
   files never leave the gitignored local store;
   repository artifacts are verified image-free
   before every commit, in the Phase-124 pattern.
   Whether a completed dataset is published at all
   is Decision Ask 4, not a default.
7. **The layer is not a study.** Nothing in the
   build computes a positional profile, a distance,
   or an evaluation. The unlocks in spec §9 are
   stated as what *successor specs* could do; the
   first consumer, if any, arrives with its own
   frozen spec and its own authorization (§12).

## Principal risks the staging is designed to retire

- **Unit effort is unknown** (retired by the pilot's
  measurements; no total is estimated before then).
- **Transcription error may exceed usable bounds**
  (retired by the gold sample and the stop-rule —
  including the possibility that the answer is
  "stop", which routes to alternative §10(b) with
  numbers in hand).
- **The frame's legibility mix may be worse than the
  crop grades suggest** (surfaced in the pilot's
  legibility-grade distribution and UNK rate, both
  reported, §5.2/§7).
- **Keying exceptions may be more frequent than the
  catalogue implies** (counted by the ambiguity log
  from the first object; a pilot ambiguity rate
  above the frame's apparent rate is itself a
  reported finding).
