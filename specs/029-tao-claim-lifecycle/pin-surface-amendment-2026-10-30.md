# Amendment record — E2/G claims-surface pin moved to ClaimsView (2026-10-30)

**What changed.** The Phase E2 and Phase G source guards assert the
lane-separated claims rendering — `data-testid="lane1-region"` and
`data-testid="lane2-region"`, the two lane labels verbatim, the OD-4
`StageLegend` on the surface, no per-status colours on lane-1 badges
(`STATUS_COLORS` absent), the AEE library scoring line inside the
lane-1 region, `mean_propagated_score` absent, the `NotUnderstood`
slot renderer present, and the program-wide stage-synonym scan
(`verified` / `proven` / `confirmed` outside the governed
`verified_unexplained` flag name) — on the claims surface. That
surface was the claims tab of `IndusEvidenceView.tsx`. Spec 081's
consolidation retired that three-tab workspace: its library became
the Library tab of Evidence & sources, its sweep moved under the
research loop, and its claims tab was superseded by the Claims
register built in Spec 081 step 3 (`ClaimsView.tsx`). The guards'
surface therefore moved, and this record is the amendment: **the
guards now assert on `ClaimsView.tsx`, with every assertion's text
and intent unchanged.**

**Why the guards survive verbatim.** The guards exist so the claims
surface can never silently drop the lane separation, the OD-4
legend, or the absence-form `not_understood` rendering. Retiring
them because the redesign closed the file they pinned was rejected
for the same reason as the 2026-10-30 guard-surface amendment: a
guard is not retired because a redesign rearranged the room.
`ClaimsView` was verified to satisfy every assertion before the
re-point — the lane regions, both lane labels, `StageLegend`,
`NotUnderstood`, and "AEE library scoring" are present; 
`STATUS_COLORS` and `mean_propagated_score` are absent.

**The one wording change.** The synonym scan strips only the
governed flag name before scanning, so the ordinary English word
"provenance" in a `ClaimsView` header comment tripped the `proven`
substring. The comment now says "source record" instead. No
assertion was weakened: the scan still forbids the three synonyms
as stage vocabulary across all touched surfaces, and the reworded
comment carries the same meaning.

**How the surface is carried now.** Claims are read on the Claims
register (Spec 081 step 3, program-scoped routes); the evidence
workspace's other two tabs live on as the Evidence & sources
Library tab and the research loop's sweep section, neither of which
carries a Spec 029 pin. `DeciphermentPanel.tsx` keeps its own pin,
untouched, exactly as the 2026-10-30 guard-surface amendment left
it.

**What did not change.** No assertion text in
`backend/tests/test_spec029_phase_e2.py` or
`backend/tests/test_spec029_phase_g.py` changed — only the two path
constants (and their explanatory comments) name the new file. The
standing-position / stage-summary guards, the verbatim stage-name
guards, the withdrawn-headline guards, and every backend-payload
guard are unchanged. No frozen file of this spec is modified by
this amendment; this record is a new file in the spec's documents.

**Freeze note.** This amendment is recorded after the Phase G
closeout. It changes no claim, stage, or verdict of this spec — it
records where the guarded claims rendering lives after Spec 081's
redesign, so the guards' continued green is read as the same
protection on the new surface, not as a weakened gate.

---

*AI disclosure: executed by an AI agent (Muse, via Muse) at
the direction of Tristen Pierson, per constitution §VI.*
