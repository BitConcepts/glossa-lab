# Feature Specification: POLICY-SYNC Conformance — Approved-Text Fixtures for Glossa Lab's Web Surfaces (Spec 084)

**Feature Branch**: `spec/084-policy-sync`
**Created**: 2026-10-31
**Status**: ACTIVE — built under the owner's standing POLICY-SYNC directive (2026-10-31, issued in the Arcturus chat and delegated to every website-owning chat). Claims frozen before code (spec-kit + AEE flow).
**Input**: The POLICY-SYNC directive: every public policy or claims-bearing text served by the app (privacy/data-handling statements, terms, and UI copy carrying factual claims about what the system does with data) must be (1) carried as requirements in the project's spec-kit specs with AEE claims; (2) have its owner-approved text stored as an approved-text FIXTURE that is the single source of truth; (3) be covered by automated conformance tests in CI that diff the served/source text against the fixtures, including ABSENCE checks for removed or superseded text — drift turns CI red and the work is not done; (4) fixtures change ONLY through a recorded owner-approval act on the actual text (a fixture edit without one is itself a finding); (5) claims whose falsifier cannot execute today stay HELD in spec text with the reason recorded — never invent a test to complete the table.
**Predecessors**: Spec 029 (the standing position and the FR-029-08 framing, and the pin-test precedent), Spec 081 (the D4 removal list; the ratified wireframe package), Spec 082 (the token UI contract), Spec 083 (the cloud perimeter texts: robots/noindex, the anonymous-surface copy).
**Inventory of record**: `files/2026-10-31-policy-sync-inventory.md` in the goal workspace (20 inventoried items; the coverage table ships with this spec's closeout).

## Problem statement

Glossa Lab's surfaces carry texts that make factual claims — the
program's standing position, the framing that keeps stage counts
from reading as decipherment progress, the token-handling rules the
UI states, the tray's account of what the supervisor does, the
cloud edge's crawler perimeter, the cloud login/setup/invite copy,
and the public tracker's standing numbers. Until today none of
these texts had a single source of truth: each lived wherever it
was typed, and drift was discovered by accident or not at all. The
program has already eaten one public drift of exactly this class:
bitconcepts.tech/llms.txt still names the superseded v8 preprint
as the latest release (verified live 2026-10-31) while v9 is the
current deposit. POLICY-SYNC mechanizes the defence for the texts
this repo serves: an approved fixture per text, a CI test that
diffs the source against it, and absence checks so removed or
superseded text cannot quietly return.

## Design summary

- **Fixtures** live in `specs/084-policy-sync-conformance/fixtures/`,
  one file per text, each headed by its approval citation (the
  recorded act the text rests on) and carrying the verbatim
  approved text after a `# ---` marker. The fixture is the source
  of truth; the surface conforms to it, never the reverse.
- **Conformance tests** live in
  `backend/tests/test_policy_sync_conformance.py` and run in the
  existing **Backend tests (pytest)** CI job on every PR and push —
  no new job, no weakened check. A diff in either direction (the
  surface drifted, or the fixture was edited without an approval
  act) turns that job red.
- **Absence checks** cover two superseded/removed classes: the
  preprint-era "161" headline framing (superseded by the October
  2026 audit's strict-core re-grade) and the Spec 081 D4-removed
  surfaces (component files, their imports, and the
  REAL_CATALOG_SUMMARY fallback-data symbol).
- **HELD claims** are entered in this spec and in `aee-claims.json`
  with their reasons, and deliberately have no test: their
  falsifiers cannot execute today (the source is not on main, or
  not in this repo, or the text has no approval act to fixture).
  Inventing a test for them is a violation of the directive.
- **Unapproved texts are findings, not fixtures.** The inventory
  found three (HelpView, the AI-settings data-flow copy, the
  seeder's description/prompt context) and one open gap (the app
  carries no privacy/data-handling/terms text at all). They are
  recorded here and in the inventory; fixturing them requires an
  owner-approval act on the actual text first.

## Requirements

- **FR-084-01** — The program's standing position, as rendered on
  ProgramHome from the default project record, matches the
  approved fixture `fixtures/standing-position.txt` exactly.
- **FR-084-02** — The stage-count framing sentence on ProgramHome
  matches `fixtures/stage-count-framing.txt`.
- **FR-084-03** — The cloud edge's robots.txt body and its
  X-Robots-Tag value match `fixtures/edge-robots.txt` and
  `fixtures/edge-noindex.txt`.
- **FR-084-04** — The API-token gate copy in ApiToken.tsx contains
  every approved string in `fixtures/token-gate-copy.txt`.
- **FR-084-05** — The tray's status/tooltip copy contains every
  approved string/template in `fixtures/tray-status-copy.txt`.
- **FR-084-06** — No served surface in this repo carries the
  superseded "161" headline framing (161 candidate readings /
  161 readings / 161 anchors, in any case).
- **FR-084-07** — The Spec 081 D4-removed surfaces stay removed:
  no source file and no import for any removed component in
  `frontend/src`, and the REAL_CATALOG_SUMMARY symbol stays absent.
- **FR-084-08** — A fixture under this spec changes only through a
  recorded owner-approval act on the actual text, cited in the
  fixture header and in the change's ledger entry. A fixture edit
  without one is a finding, and the conformance failure it causes
  is not to be "fixed" by editing the surface to match.
- **FR-084-09** — The cloud anonymous-surface copy (login,
  glassbreak setup, invite acceptance) in
  `frontend/src/cloud/pages.tsx` contains every approved string
  in `fixtures/cloud-anonymous-surface-copy.txt`, and the
  superseded wireframe-01 reset-link sentence appears nowhere in
  `frontend/src`. (Added at the C084-8 activation, 2026-11-05.)

## Activated claims (were HELD at the spec's landing)

- **C084-8 (ACTIVATED 2026-11-05)** — Cloud anonymous-surface
  copy (login, glassbreak setup, invite acceptance). Held at the
  landing because the source (`frontend/src/cloud/pages.tsx`)
  existed only on feat/083-frontend. The condition was met when
  feat/083-frontend landed on main in PR #476 (2026-11-01); the
  owner approved activation 2026-11-05. The fixture
  (`fixtures/cloud-anonymous-surface-copy.txt`) is written from
  the landed text and its approval record: the Spec 083 wireframe
  package (PR #463) for the login lede, the no-public-registration
  footer, and the setup audit-log statement; the 2026-10-31
  parent decisions on the Phase 3 flags (Spec 083 BUILD-RECORD)
  for the password-recovery posture and the invite issued-address
  binding. Exercised by
  `test_cloud_anonymous_surface_copy_matches_fixture` and
  `test_superseded_reset_link_promise_absent` (the wireframe-01
  reset-link sentence the posture decision superseded). The
  claim's entry in `aee-claims.json` stands as intaken: the
  bundle is the ledger's SHA-pinned source of record and is
  never edited after intake (the Spec 087–090 precedent), so
  its intake-time HELD wording is superseded by this activation
  record, not rewritten.

## HELD claims (entered, with reasons — no tests, by design)
- **C084-9 (HELD)** — Public tracker standing texts
  (bitconcepts.tech/research/ and /research/indus-script/).
  Reason: the source is the tracker artifact, not this repo; a
  pytest in this repo cannot diff it. Conformance belongs to the
  tracker publish path (build + served-identity check).
- **C084-10 (HELD)** — llms.txt latest-release line. Reason: the
  drift is confirmed (v8 named; v9 is current), but the
  correction text is owner-gated — it is bundled with the
  prepared v10 corrections package awaiting the owner's approval
  of the exact text — and the source is outside this repo.
- **C084-11 (HELD)** — In-app Help text and AI-settings data-flow
  copy. Reason: no owner-approval act on record for these texts;
  rule (4) forbids fixturing unapproved text. They stand as
  unapproved-text findings until an approval act exists.
- **Gap (not a claim)** — The app has no privacy / data-handling /
  terms text (inventory A4). Creating one is an owner text act;
  when an approved text exists it enters this regime as a new
  fixture + claim.

## Assumptions (epistemic boundaries)

- The approval citations in the fixture headers are taken from the
  merged record (ratified packages, merged contracts, owner
  orders, recorded parent decisions). Where the record supports
  approval only at contract level (FR-084-04), the fixture header
  says so plainly rather than claiming a text-level act.
- Source-text diffing is the executable falsifier available today.
  It proves the repo's sources carry the approved text; it does
  **not** establish what any deployed surface serves — the desktop
  install serves the build it was settled to, and the cloud
  edition is pre-go-live. Deployed-surface conformance is a
  go-live-era check (Spec 083 T059 class) and is not claimed here.
- The preprint (a deposited artifact on Zenodo) is not a served
  surface of the app and is out of scope; its superseded headline
  is handled by the owner's v10 approval gate, not by this spec.
- "Fuls" as a corpus/source name in living views is legitimate
  content, not the removed fallback data; the absence check
  targets the REAL_CATALOG_SUMMARY symbol and the removed
  components, not the name.
