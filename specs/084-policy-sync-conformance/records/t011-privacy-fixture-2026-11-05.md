# T011 record — privacy / data-handling statement fixtured and served (2026-11-05)

Task: Spec 084 T011 (owner-gated follow-on; inventory gap A4).
Approval act: the owner approved the 2026-10-31 draft statement
on 2026-11-05 and directed closure of its five [UNVERIFIED]
items. Branch `feat/084-t011-privacy-fixture` off `27ce5550`.

## The five items — closure evidence

1. **Contact address — OWNER DEFAULT.** `tristen@bitconcepts.tech`,
   the program mailbox of record, stated in §8. Correctable by a
   new approval act; not independently verifiable beyond the
   mailbox-of-record standing.
2. **Hosting-provider logging/retention — SET TO VERIFIED FACTS
   ONLY.** Read first-hand through the program's Cloudflare
   token (2026-11-05): zone `bitconcepts.tech` active on the
   Free plan; NO Workers scripts deployed on the account (cloud
   edition pre-launch); the repo's `cloud/edge/wrangler.toml`
   carries no observability, logpush, or analytics settings, and
   refuses deploy while its D1 `database_id` is a placeholder.
   NOT readable with this token (HTTP 403, codes 9109/10000):
   zone settings and Logpush jobs. §3 therefore states only
   what the Worker's own configuration does (no logging or
   measurement collection of its own) and that Cloudflare's own
   operational records are governed by Cloudflare's terms; the
   statement asserts nothing resting on the unreadable settings.
3. **Web analytics — VERIFIED ENABLED.** The account's RUM
   (Web Analytics) read shows exactly one site for the zone,
   created 2025-10-20, `auto_install: true`, ruleset enabled,
   no host-exclusion rules — it applies to
   glossa.bitconcepts.tech. §5 discloses it, dated 2026-11-05.
4. **Retention — OWNER POLICY DEFAULT.** No purge/TTL code for
   invitations or audit entries exists in `cloud/edge/src`
   (only the 30-day session TTL); the audit log is append-only
   by database trigger. §3 states the owner's default as
   policy: expired invitations and audit entries are retained
   12 months; applying it to audit entries is an operator act,
   not an automated process. Correctable by a recorded
   decision.
5. **Member export — VERIFIED PRESENT.** `GET /{project_id}/export`
   in `backend/glossa_lab/api/projects.py` returns the project
   (workspace) JSON bundle (the frontend calls it);
   `GET /reports/{report_name}/download` serves report
   downloads; `GET /texts/{text_id}/export` exports corpus
   texts as txt/csv/json. §6 states exactly that.

## The fixture and the serving surface

The approved text is the fixture
`fixtures/privacy-data-handling.txt` (the draft reproduced
verbatim except the five closures; the fixture header carries
the approval citation and per-item evidence). The spec
prescribes no surface; the minimal one it implies was built:
`backend/glossa_lab/privacy_statement.py` carries the served
copy (`PRIVACY_STATEMENT`, generated from the fixture body so
the two cannot drift at birth), `GET /api/v1/privacy` serves it
(`backend/glossa_lab/api/privacy.py`, registered in `main.py`),
and the SPA renders the SERVED text in a Privacy view on the
utility route `privacy` (palette-reached, following the
Spec 081 ai-tools/foundation-check precedent; the view carries
no copy of the text). The route stays behind the install-token
gate like every route except health — §2 of the statement
says the health readout is the only unauthenticated answer,
and the serving keeps that true. Conformance
(`backend/tests/test_policy_sync_conformance.py`, claim
C084-12): presence (served copy equals the fixture body
exactly), wiring (route registered), absence (no
`[UNVERIFIED` placeholder in `frontend/src`, `cloud/edge/src`,
or `backend/glossa_lab`; no baked copy of the statement in
`frontend/src`).

## The ledger intake — executed, verified end-to-end, then HELD on a named machinery gap

C084-12 was drafted into this spec's `claims.json` (a second
bundle file: `aee-claims.json` is frozen at its 2026-10-31
intake — editing it would break the recorded-hash arm of gate
V1 for C084-1..11 permanently). The intake chain was executed
on this branch and every step verified:

- `import_bundle` appended C084-12 (1 appended, 11 already
  canonical); ledger 943 → 944 lines, canonical SHA
  `6a997a31be478e33106c40753f90653c4155141324ee198904dc333e2ebda922`.
- Matrix regenerated without refusal.
- `run_settling.py verify-canonicals`: **6/6 reproduce** over
  the new build (C084-12 carries no sign_refs, no outcome
  blocks; no scenario input changed).
- `settling-canonical.json` gained `re_derivations[4]` and its
  provenance pin moved to the new build (the Spec 087/090
  adoption-refresh discipline).
- The T405 pair was re-derived over the new build per the
  Spec 090 adoption precedent (commit `198e9143`): results
  byte-equal to the standing records, only the ledger pin
  lines changed, files renamed under the content rule to
  `t405-incumbent-over-full-frame--17334e1dfc65.json` and
  `t405-full-register-over-full-frame--47287ced3385.json`;
  the dual-run comparison record was re-filed the same way.
  (Two settling runs first executed through the run-id writer
  were the wrong instrument for legacy records — results also
  byte-equal — and were removed uncommitted with their index
  acts reverted.)
- Map regenerated carrying the refreshed pair (2 runs);
  program map regenerated at 913 claims.

The chain then stops at the run index. Gate run over the
refreshed tree (full output:
`records/t011-gate-run-intake-attempt-2026-11-05.txt`):
**28 PASS / 1 FAIL / 1 NOT-RUN**, the failure being V11 leg
(c) with four findings, all about the departed pair: their
index entries "neither stand in the store nor are accounted
as a superseded legacy record (a superseding commit and the
record's blob hash named)", and the refreshed pair's files
"stand in the store with no index entry".

Why no registered act can close those four findings today:

- Leg (c) counts a departed record as accounted only when its
  ENTRY carries `superseded_by_commit` + `git_blob` +
  `blob_sha256` (ledger_gate.py, V11 leg (c)).
- The run index is append-only and relations change by
  appended acts, never by editing a line (RUN-DEFINITIONS.md
  §7.1). The fold refuses a second entry act for an id
  ("an id is one execution, entered once",
  `run_records._apply_entry`); the remaining act kinds
  (supersedes, quarantine, adjudication) do not amend an
  entry's fields.
- The departed pair was entered STANDING by the Spec 089
  completion builder (T501) — before any superseding commit
  or blob accounting could exist for it. Every earlier
  generation was entered only after departing, which is why
  the gap never fired before: this intake is the first
  ledger growth since the legacy index was completed.
- The completion builder itself cannot repair it:
  `tools/ledger/build_legacy_index.py` skips already-entered
  ids, and its history pass refuses on post-spec
  (header-carrying) records instead of skipping them —
  verbatim: "LEGACY INDEX REFUSED: legacy recovery: record
  'settling-20261105T022535Z-a7b4e5.json' carries no
  'candidate' to recover" — so it appends nothing at all over
  the current store.

Disposition: the intake and all derived-layer changes were
reverted on this branch; the ledger stands at its pinned
state (943 lines, SHA-256
`15a5fbad24f400631ace1ebc88bfb7712c9bf6f68fae23e56fedbcac5fd5a794`,
verified after the revert). C084-12 stands at spec level; its
claim record is preserved in the appendix below, and the
bundle file ships with the intake act rather than before it
(an unimported bundle proposition in the tree fails the
migration-reconciliation test on exactly that difference).
The follow-on is a Spec 089-lineage act of its
own: a run-defs amendment registering how a departed legacy
generation is accounted (e.g. a registered accounting act, or
builder authority to complete an entered-standing entry at
departure), plus the builder's header-skip repair. When it
lands, this intake replays mechanically — every step above
is verified and the numbers are recorded here.

*This does not establish:* that the statement's facts hold at
cloud go-live (the fixture header carries the go-live
re-check list), or that the intake is complete — it is
expressly held, above.

## Appendix — the C084-12 claim record (preserved for the intake act)

The claim record below was carried in this spec's `claims.json` during the intake attempt. It is preserved here verbatim; the follow-on intake act re-creates `claims.json` with this record as its first step and imports it. (While the bundle file stood in the tree unimported, `test_spec086_ledger_migration.py::test_p2_reconciliation` failed on exactly the one-proposition difference — the reconciliation invariant doing its work; the bundle therefore ships with the intake act, not before it.)

```json
{
 "claims": [
  {
   "boundary": [],
   "conflicts_with": [],
   "depends_on": [],
   "evidence": [
    {
     "description": "Spec 084 FR-084-09 / task T011 (inventory gap A4). Owner approval act 2026-11-05 on the 2026-10-31 draft text, with its five [UNVERIFIED] items closed as recorded in the fixture header (contact address = the program mailbox of record, an owner default; hosting-provider text set to the verified facts; Web Analytics verified ENABLED for the zone at account level; 12-month retention as the owner's policy default; member export verified present). This claim is carried in claims.json, the spec's second bundle file, because aee-claims.json is frozen at its 2026-10-31 intake (its recorded hash governs C084-1..11). Exercised by backend/tests/test_policy_sync_conformance.py::test_privacy_statement_matches_fixture, test_privacy_route_is_registered and test_no_unverified_placeholder_text in the Backend tests CI job.",
     "direction": "supports",
     "kind": "asserted",
     "ref": "spec.md",
     "source_quality": "unknown"
    }
   ],
   "falsification_tests": [
    "PRIVACY_STATEMENT in backend/glossa_lab/privacy_statement.py differing from the fixture body in any character beyond trailing whitespace; or GET /api/v1/privacy not being registered in backend/glossa_lab/main.py.",
    "Any file under frontend/src, cloud/edge/src or backend/glossa_lab containing the superseded draft placeholder '[UNVERIFIED', or frontend/src carrying a baked copy of the statement (its distinctive sentences) instead of rendering the served text."
   ],
   "id": "C084-12",
   "kind": "requirement",
   "source_ref": "spec.md",
   "stage": "created",
   "status": "draft",
   "text": "The app's privacy / data-handling statement, served by GET /api/v1/privacy from backend/glossa_lab/privacy_statement.py and rendered in the SPA's Privacy view, matches the approved fixture specs/084-policy-sync-conformance/fixtures/privacy-data-handling.txt exactly (owner approval 2026-11-05), and no served source carries the superseded draft placeholder text.",
   "uncertainty": "insufficient_evidence"
  }
 ]
}
```
