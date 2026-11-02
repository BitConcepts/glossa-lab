# Decisions — Spec 087 Stage S5 Logs view wireframes

Two questions for the owner. Each states the options and the
drafting worker's recommendation. The owner rules by name at
the wireframe approval act; the S5 build follows the ruling.

## Q1 — Placement: own tab, or inside the System / Status area?

**Options.**

- **(a) Own tab.** A "Logs" entry in the sidebar's Tool home
  group, between Jobs and Status, opening the two-tab view in
  these wireframes. This is what the wireframes draw.
- **(b) Inside System.** The stream and records become panels
  inside an existing surface (the Status view is the natural
  host; the System graph tab is the program's map surface and
  is not a host candidate in the drafting worker's judgment).

**Recommendation: (a) own tab.** Three reasons. First,
precedent: Spec 086 Stage 5 added the System graph as its own
tab for a new surface of exactly this kind, and the current
chrome absorbed it without disturbing the other screens.
Second, the two halves of this view (a live stream the
operator sits in, and a records list the operator searches)
are both full-screen work; as panels inside Status they would
compete with the health surface for the same space and inherit
its much smaller visual budget. Third, the pre-081 product had
logs as a distinct surface (the bottom panel); a named tab is
the honest restoration of that surface in the post-081 shell,
and it is the placement the manuals' stale descriptions come
closest to, which keeps the Stage S4 manual corrections
smallest.

*This does not establish* that a future consolidation of the
Tool home group would be wrong — only that, for this restore,
a tab is the placement that matches the surface's weight and
the shell's own precedent.

## Q2 — Purge: UI control with confirmation, or read-only view?

**Options.**

- **(a) Ship purge in the UI, behind a confirmation.** The
  stream tab carries the "Purge log…" control exactly as drawn
  in wireframe 01: pressing it shows the confirmation state
  naming what purge does (clears the current `glossa.log`
  through `POST /terminal/log/purge`, returns
  `{cleared, file}`, rotated backups untouched, cannot be
  undone) before anything is sent.
- **(b) Read-only view.** No purge control; purge stays
  available only through the API (and the `api.ts` wrapper
  stays unreferenced, as today).

**Recommendation: (a) ship it, with the confirmation as
drawn.** The endpoint exists, is authenticated through the
same token path as every other surface, and its one
destructive property is fully described by the confirmation
state — the wireframe shows the operator the line count being
cleared before the act, which is a stronger guard than the
bare API call offers. The pre-081 panel offered purge from
the UI; removing the capability from the restored view would
make the restore narrower than the surface it replaces, for
no safety gain the confirmation does not already provide.
The confirmation is part of the approval: if the owner
approves (a) without the confirmation state as drawn, that is
a design change to record, not a detail for the build to
decide.

*This does not establish* anything about purge policy for the
other log-like records — the records tab is read-only under
both options, and no option here touches `job_results`,
`phase_actions`, or the cloud audit log.
