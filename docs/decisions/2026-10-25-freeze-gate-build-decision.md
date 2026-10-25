# Decision record — building the correctness-bearing freeze gate (2026-10-25)

**Act:** the owner commissioned the build of the correctness-bearing
freeze gate designed in the realignment plan's item 3.1
(`2026-10-25-correctness-bearing-gate-design.md`, goal record;
components C1–C5), in the same order as the endings-atlas design
("Commission the gate build + endings atlas design (3+4 together)",
2026-10-25 10:03 EDT).

**The design's three open choices, resolved by the design's own
recommendations under the owner's commission and his
programme-success North Star rule:**

1. **C1 battery case (i) is the REAL Spec 026-era design, not a
   reconstruction.** The artifact is the design Spec 026's own text
   names as the era's instructive failure: the Phase-114
   blind-affiliation study — Spec 012's spec
   (`specs/012-phase113-blind-affiliation/spec.md`, renumbered
   Phase-114 in its own renumbering note; SHA-256
   `066768c26f606002f7bac542084ba67e089f97ab4c749ccd96fa56bb9269908c`
   on main), copied byte-identically into the battery. Spec 026 §1
   records the defect: its generator was a non-discriminating
   instrument (a grammar-free system won 100% of draws), discovered
   only in execution; the method family was later falsified and
   quarantined (Spec 026's historical assessments, H26).
2. **C2's sample for non-gate-turning quantities is a fraction:
   25%, minimum 3.** (Every gate-turning quantity is always
   recomputed; the fraction governs only the rest.)
3. **C4 runs one shadow freeze first.** The CI check is built and
   demonstrated able to fail now, and it runs on freeze PRs from
   this build onward — but it is **not** a required check in branch
   protection yet. The first strengthened freeze (the endings
   atlas, designated in its design) is the shadow: the gate runs in
   full and is reported, and mechanical enforcement as a required
   check begins with the freeze after it.

**Enforcement state, stated honestly (and repeated wherever the
build is described):** as of this build, the C4 check exists in CI
as a non-required job. It is demonstrated able to fail (the
demonstration is filed with the build). Nothing about branch
protection changed in this act.

**What this act does not do:** it does not re-score, re-open, or
cast any shadow on any past freeze; the existing AEE
register-discipline scoring stays, described as what it is. It
authorises no freeze and no execution.

*AI disclosure: prepared by an AI agent (Muse Spark, via Muse
Code) at the direction of Tristen Pierson, per constitution §VI.*
