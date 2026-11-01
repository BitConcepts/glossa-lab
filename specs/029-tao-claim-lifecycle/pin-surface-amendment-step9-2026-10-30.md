# Spec 029 pin-surface amendment — Spec 081 step 9 (2026-10-30)

**What changed.** Spec 081 step 9 (T021) deleted
`frontend/src/components/DeciphermentPanel.tsx` as dead code: its
only mounter, DashboardView, left the shell in step 5, and
nothing has rendered the panel since. Three Spec 029 guard files
named the panel as a pinned surface; their pins are re-pointed
by this amendment. No assertion's text or intent changes except
where a pin's object itself moved, as detailed below.

**E1 (test_spec029_phase_e1.py).** The E1.1/E1.4 purge tests
asserted the withdrawn constructions ("signs deciphered", "SA
Confidence", the withdrawn dashboard fields, …) are absent from
the panel's source. With the panel deleted, the scan is widened
to the WHOLE shipped frontend source tree (`frontend/src`,
`.ts`/`.tsx`): the constructions must appear nowhere. That is
strictly stronger than the single-file scan it replaces. The
E1.2/E1.3 payload withdrawals are untouched.

**E2 (test_spec029_phase_e2.py).** `_PANEL` re-points to
`ProgramHome.tsx`, which has rendered the standing position and
the lane-2 stage summary since Spec 081 step 4 (Amendment 2 —
the blocks moved there as program data precisely so the panel
could retire). `test_panel_leads_with_standing_position_and_
stage_summary` becomes `test_home_leads_with_…`: the testids,
`by_stage`, the `StageLegend` rendering and the withdrawn-strings
absence are asserted on ProgramHome verbatim. One assertion
moves with its object: the standing-position TEXT ("The Indus
script is not deciphered…") is program data since Amendment 2,
so it is asserted on `backend/glossa_lab/project_seeder.py`,
which seeds the default program's record — the text's actual
home. The synonym scan's surface set swaps the panel for
ProgramHome the same way.

**Phase G (test_spec029_phase_g.py).** `CLAIM_SURFACES[0]`
re-points from DeciphermentPanel.tsx to ProgramHome.tsx (the
synonym scan set). Entries [1] (ClaimsView, per the step-6
amendment) and [2] (StageLegend) are unchanged.

**What did not change.** Every guard value, purge string,
synonym, and stage name is identical. The rendered e2e guards
never asserted on the panel (they read the home and claims
surfaces), so they are untouched. The dashboard decipherment
payload the panel consumed is unchanged — other consumers
(ProgramHome's stage summary) still read it.

**Freeze note.** Recorded after the Phase G closeout, in the
same pattern as the step-6 amendment
(`pin-surface-amendment-2026-10-30.md`). It changes no claim,
stage, or verdict of this spec — it records where the guarded
surfaces live after Spec 081's redesign, so the guards'
continued green is read as the same protection on the living
surfaces, not as a weakened gate.

---

*AI disclosure: executed by an AI agent (Muse, via Muse) at
the direction of Tristen Pierson, per constitution §VI.*
