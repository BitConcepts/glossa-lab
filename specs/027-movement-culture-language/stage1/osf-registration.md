# Spec 027 — Stage 1 OSF Registration Record (Phase-392)

Filed 2026-10-11, after the Stage 1 freeze merged and before
any Stage 1 execution, per the program's recorded follow-on
requirement (from the OSF full-utilization build-out,
owner-directed 2026-10-11; the Spec 027 design registration
recorded the same follow-on).

- **Registration: https://osf.io/pnqrx/** (id `pnqrx`)
- Filed: 2026-10-11T14:02:01Z (OSF timestamp)
- Schema: OSF Preregistration
  (`697b72f611a8e98484c6139b`) — the same schema as the Spec
  027 design registration https://osf.io/a2xvc/
- Node: `zsnfy` — "Spec 027 Stage 1 (Phase-392) — Q2
  Repertoire Gate: Frozen Contract (Stage 1 freeze, merged
  2026-10-11)", created for this filing because the design
  registration's source node (`nxtmg`) returns HTTP 410
  (no longer available) on the OSF API.
- Draft: `6acb96b0a379d7b7402674fc`; all 29 response fields
  of the frozen contract (bounded claim, corpus rules,
  frozen statistics, controls, verdict rules, provenance)
  filed from `stage1-freeze.md` as amended; read-back
  verified — stored responses match the filed text except
  OSF's server-side HTML escaping of `<`/`>` on read.
- Subjects (mirroring the design registration):
  Computational Linguistics; Social and Behavioral Sciences;
  Anthropology; Linguistics; Archaeological Anthropology.
- Posture: public, no embargo (registration choice
  `immediate`). State at filing: `initial`, pending admin
  approval — the registration becomes public on approval
  (owner action or OSF's 48-hour backstop). Filing and
  timestamp are the operative facts for the program's
  sequencing rule; approval is not a Stage 1 gate.
- Freeze filed: `stage1-freeze.json` digest
  `30861f04e5968ed5c488c01dbc74891c7977cd256bc7cf9ed075c1513d145762`
  (stage1-freeze.md as amended by Amendment 1), merged as
  PR #154, merge commit `4684408f`, CI run 38144799989
  verified success from the run's own conclusion.
- Filing route: OSF API (api.osf.io only) via the program's
  osf skill CLI with the stored `custom.osf` credential.
  One API note: the CLI's draft-submit action endpoint
  returned 404 on the current API; the draft was registered
  directly (POST /registrations/), which is the operative
  filing step. No other filing irregularity.
