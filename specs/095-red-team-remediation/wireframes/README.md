# Researcher Dashboard Wireframes — Spec 095 Stage 4 (T403)

**Status: WIREFRAMES ONLY, awaiting the owner's approval by name.**

T403's build is owner-gated: the dashboard is built only after
Tristen approves these wireframes by name. This stage produces the
wireframes and nothing else — no dashboard code, no frontend
change, no served-surface change. T403 is therefore **not ticked**
by Stage 4; it stands at wireframes, and the T404 audit's
dashboard leg re-runs after the build lands.

## The set

Static HTML, one file per surface, openable directly in a browser
(no build step, no JavaScript, no external assets). The program's
wireframe convention, as used by the website programs' wireframe
gates.

| File | Surface |
|---|---|
| `index.html` | Dashboard home: census band, feature entries, the does-not-claim panel, recent adjudications |
| `feature-program-status.html` | Program status |
| `feature-inscription-explorer.html` | Inscription explorer |
| `feature-hypothesis-comparison.html` | Hypothesis comparison |
| `feature-evidence-inspection.html` | Evidence inspection (incl. audit-trail export) |
| `feature-experiment-reproduction.html` | Experiment reproduction |
| `feature-researcher-contribution.html` | Researcher contribution |

The feature set is C095-12's enumeration of record: program
status, inscription explorer, hypothesis comparison, evidence
inspection, experiment reproduction, researcher contribution,
plus the dashboard home that carries them and the multi-script
abstraction of T401 (the surfaces are specified script-neutrally;
the Indus record is their first instantiation, per
`docs/MULTISCRIPT_MODEL.md` §6).

## The eight-step protocol against these surfaces (C095-13)

1. Arrive from the public page → the home's entry points.
2. Establish what the system claims and does not claim → home
   does-not-claim panel + program status.
3. Find one inscription and its evidence trail → inscription
   explorer → evidence inspection.
4. Distinguish observation, transcription, hypothesis, claim →
   the explorer's four labelled layers.
5. Reproduce one published result → experiment reproduction.
6. Submit one candidate with a falsifier → researcher
   contribution (falsifier is a required field).
7. Follow its adjudication → contribution's adjudication trail.
8. Export the audit trail → evidence inspection's export.

## Refusals, per feature

Each wireframe carries its own "refuses to" panel. The set-wide
refusals, from C095-12: **no automatic promotion** of any
candidate at any stage; **no self-certification** (a submitter
never adjudicates their own candidate; no surface certifies its
own outputs); the Research Assistant's boundary is Spec 025
advisory-only, and approval is a named human act under Spec 094's
landed gates.

## Copies of record

- In the PR tree: this directory,
  `specs/095-red-team-remediation/wireframes/`.
- Review copy: the goal workspace,
  `files/095-stage4-wireframes/` (VM), copied at Stage 4 for the
  owner's review.
