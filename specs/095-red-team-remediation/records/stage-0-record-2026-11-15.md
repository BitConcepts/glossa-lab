# Spec 095 — Stage 0 record: reconciliation and register (2026-11-15)

Stage 0 was executed on 2026-11-15, before adoption, and is complete
at adoption (D-095-2). This record is the stage's in-repo face; the
four deliverables themselves live in the goal workspace at
`hidden_files/red-team-2026-11-15/`, preserved with the review they
reconcile. All hashes below were recomputed from the files at
adoption time and match the values the parent verified on
2026-11-15.

## The source

The external red-team review, preserved verbatim:
`REVIEW.md`, 30,751 bytes, SHA-256
`fa72ca0dc8ed541037273c9c5d5d5e8ed4482f217b961b768da3f16add47712e`.

## The four deliverables

1. **The register** — `register-draft.md`, 52,966 bytes, SHA-256
   `8c2812681b02d5631c90e69af43da8a775d23b35fab17c2953c53517ba6375e9`.
   43 rows, RT-01..RT-43, each with exactly one disposition:
   23 DUPLICATE-OF-RECORD (each mapped to its owning vehicle by ID;
   RT-06 among them, classified a security risk requiring
   verification under its Spec 083 vehicle), 18 rows carrying the
   14 NEW items of its section N (RT-03 among them: the review's
   one confirmed defect, a NEW micro-task on a duplicate family),
   2 FACT-DISPUTED (RT-42, RT-43; the record governs both).
   23 + 18 + 2 = 43. The register is this spec's scope of record
   (C095-1, D-095-1).
2. **The pinnability pass** — `pinnability-p0.md`, 11,632 bytes,
   SHA-256
   `ad456e0974010beb6f20f0c3370fc4177df5e0b5ebc6f050efa124c7abae81ea`.
   Verdict: SAME LAYER, SAME ARTIFACT — a placement defect, not a
   missing corpus. The missing artifact is
   `firestore_indusarrays_full.jsonl`, sole data file of the V3
   loader (`backend/glossa_lab/data/indus_corpus_v3.py`), expected
   at `glossa-corpus/indus/sources/rmrl/raw/indusscript-probe/
   firestore_indusarrays_full.jsonl`, a path no checkout carries
   because the raw subtree is gitignored by design. Phase-43
   identification standard: source "indusscript.in Firestore
   'indusarrays' (2026-05-14)"; 3,916 records / 3,137 sequences /
   2,665 dockeys / 12,494 sign instances. Intake pin (PR #393,
   2026-10-25): source SHA-256
   `073a83aa5e0f81055e7b68d2ccdf160027bb5061b4b870e58f3d3457cad1a578`;
   canonical export pin prefix `e90fd7ce41121529`. Spec 054 lost the
   identical file at the identical gate, located it in place,
   intake-pinned it, and reproduced the census exactly through the
   same loader. Spec 053 ran 2026-10-21, before the pin, from a tree
   without the file; gates 0.1 and 0.2 passed; 0.4/0.5 were never
   reached; every substitute was rejected on the record. Bound: the
   file's present physical location is not determinable from the
   record (last recorded venue: the desktop clone, 2026-10-25; that
   machine was formatted 2026-11-09). The claim
   `yadav_2009_arxiv_manual_001` stands unchanged.
3. **The public-surfaces pass** — `public-surfaces.md`, 8,369
   bytes, SHA-256
   `5207257bfa7cd035011f3c006312d9803da6c359cc57fdb4748e24c5209494de`.
   (1) RT-03 CONFIRMED: `research/indus/indus-anchor-model/README.md`
   foregrounds "161 H+M signs have BC > 0", "141/161", the 397-sign
   anchor table and "Token coverage percentages (90.96% H+M, 9.34%
   LOW)", cited as "Preprint v2", with no supersession notice (no
   287 anchors, 94 strict, October 26 audit, WP5, or v10 anywhere).
   The defect is presenting the v2-era package as current; v10's
   own title legitimately carries 161. (2) The public tracker
   matches the record on every checked figure except one STALE
   sentence, quoted exactly: "On the current ledger the program
   holds 912 claims across 91 studies" (canonical at the pass:
   977 claims, 95 studies, 1,008 ledger lines). The standings line
   in the same sentence ("2 carry a positive standing and 6 a
   negative one") is NOT RE-VERIFIED and is presumed equally stale.
   (3) The review's app claim is the reviewer's tool limit, not a
   defect: the edge serves and the backend health payload was
   verified by identity. Accessibility is covered by no program
   record; that gap is carried into C095-13.
4. **The validator census** — `validator-census.md`, 13,487 bytes,
   SHA-256
   `2968812cfb26451d89fa79b6145289b7efce14328397b91e1889cd4899ff51fb`.
   At the census clone's HEAD, every corrected v2 module's only
   consumers are its own repair tests, and the v1 routines remain
   executable inside the live app as registered Experiment Builder
   nodes with no guard of any kind: phonotactics v1 via the
   Phase-58 node and the Phase-108 provenance recompute (which
   dynamically loads the Phase-58 script); site-statistics v1 via
   the Phase-69 node and the provenance recompute's site-invariance
   leg; crosswalk v1 via the Phase-96 node. The site-statistics
   wrapper prints the script's p-value into its output text,
   surfacing v1 preset p-values as current output. No current
   evidence path computes with v1 (the live foundation check reads
   archived outputs and the v2 crosswalk only). Exposure is
   prospective, not contamination. corpus_frames has no v1 module;
   replay076 is a frozen pilot invoked by nothing, and its wrapper's
   hash gate is the one real guard in the set.

## The owner-gated micro-tasks (D-095-5)

Recorded here, outside this spec's stages, each executable on the
owner's word alone:

- **MT-095-1 (RT-03):** add a supersession banner to
  `research/indus/indus-anchor-model/README.md` naming the current
  state (287 recorded anchors, 94 strict, the October 26 audit and
  WP5 dispositions, deposit v10) and pointing at the tracker. Text
  changes on a public surface; the owner's approval of the actual
  text governs, per standing rule.
- **MT-095-2 (tracker sentence):** correct the tracker's stale
  ledger sentence to the canonical census at the time of the fix,
  and recount its standings line in the same act (the line was not
  re-verified by the pass and must not be carried forward on the
  pass's authority).

## What Stage 0 does not establish

It does not establish that any duplicate row's work is done, that
the located artifact (when found) will match its pin, that the v1
exposure has contaminated anything (the census found the opposite),
or that the review's remaining judgments are endorsed. It
establishes the scope of record and the four passes' findings,
nothing more.
