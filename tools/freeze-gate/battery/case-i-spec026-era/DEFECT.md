# Battery case (i) — the real Spec 026-era design

**Artifact:** `design.md` in this directory — a byte-identical copy
of `specs/012-phase113-blind-affiliation/spec.md` on main
(SHA-256 `066768c26f606002f7bac542084ba67e089f97ab4c749ccd96fa56bb9269908c`
for both files; verify with `sha256sum`).

**What this design is.** The Phase-114 blind-affiliation study
(Spec 012, frozen 2026-10-07; renumbered from Phase-113 in its own
note). It is a pre-audit design from the Spec 026 era: Spec 026's
spec (§1) names this study's instrument class as the era's
instructive local failure, in its own words: "the Phase-114
blind-affiliation generator (grammar-free system won 100% of
draws — a non-discriminating instrument discovered only in
execution)". The wider method family it belongs to was later
falsified as sufficiency evidence and quarantined (Spec 026,
`historical-assessments.md`, H26 entries).

**The defect, in plain words.** The study's generator could not
tell the property it was testing for apart from generic cases:
a grammar-free control system won every draw. An instrument that
cannot discriminate cannot support a verdict either way — but
nothing in the design's own claim structure says so. The defect
lived in the instrument, and it was found by running it, not by
reading the design.

**What the battery asks of the evaluator.** Run the current
evaluator over this real design, exactly as a freeze would. If it
raises a correctness finding that names this defect class, the
gate catches the case. If it passes the design with only
draft-stage hygiene findings — or extracts no assessable claims
from it at all — that is recorded as a named blind spot of the
evaluator, in the battery results, in plain words. The blind
spot, if any, belongs to the evaluator; the programme's own
record caught this defect by execution, and no wording in the
battery results may suggest the evaluator caught it too unless
its output does.
