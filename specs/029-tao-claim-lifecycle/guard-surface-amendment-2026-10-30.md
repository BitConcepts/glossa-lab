# Amendment record — E2/G display guards re-pointed to the program home (2026-10-30)

**What changed.** The Phase E2 and Phase G rendered-surface guards
assert the standing position (`data-testid="standing-position"`) and
the lane-2 stage summary (`data-testid="stage-summary"`, with the
OD-4 legend) on the home surface. Spec 081's D2.2 replaced that home
surface: the dashboard — and with it the embedded DeciphermentPanel,
the only component rendering those testids — retired in favour of
the program home. The guards' surface therefore moved, and this
record is the amendment: **the guards now assert on the program home,
with every assertion's text and intent unchanged.**

**Why the guards survive verbatim.** The guard exists so the UI can
never silently drop the program's standing position. Retiring the
assertions because the furniture moved was considered and rejected
(2026-10-29 adjudication, recorded as Spec 081 Amendment 2): a guard
is not retired because a redesign rearranged the room. Placing the
position on the claims surface was also rejected — the standing
position is the program's lead verdict, and the program home is the
surface designed to lead with verdicts.

**How the position is carried now.** The standing position is program
data: a field of the program's own record
(`projects.standing_position`, schema v25), rendered on the program
home directly under the program title. The seeded default program
carries this spec's standing position on its record — the E2 text
verbatim in substance, with its two panel-relative phrases ("lane 2,
below"; "on this panel") in surface-neutral form, because the record
is not a panel. The stage summary renders the decipherment payload's
`by_stage` counts under the FR-029-08 framing with the OD-4 legend,
exactly as the panel rendering does. The guard specs' mocked program
record carries the position, as a record under guard should; no
assertion text changed.

**What did not change.** DeciphermentPanel keeps its own rendering
of both blocks and its backend source pin
(`backend/tests/test_spec029_phase_e2.py`) untouched. The lane-1 /
lane-2 separation guards, the verbatim-name guards, the
not_understood absence-form guards, and the withdrawn-headline guards
are all unchanged and still assert on their original surfaces. No
frozen file of this spec is modified by this amendment (the freeze
`sources` list is untouched); this record is a new file in the
spec's documents.

**Freeze note.** This amendment is recorded after the Phase G
closeout. It changes no claim, stage, or verdict of this spec — it
records where two guarded renderings live after Spec 081's redesign,
so the guards' continued green is read as the same protection on a
new surface, not as a weakened gate.

---

*AI disclosure: executed by an AI agent (Muse, via Muse) at
the direction of Tristen Pierson, per constitution §VI.*
