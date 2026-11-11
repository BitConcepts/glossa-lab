# Spec 083 — Go-live readiness record (2026-11-05)

**State: NOT READY TO LAUNCH. This record is the stop point.** The
repo-side and wiring legs of the go-live sequence are built (PR
referenced in §6); the launch itself waits on gate 2 (Cloudflare
scopes, owner act). At actual go-live,
the glassbreak one-time setup code + URL are delivered to the owner
ONCE in the Glossa-Lab chat — no launch act has been taken, no setup
code has been generated, and nothing in this record performs one.

**Update (2026-11-06): the desktop legs are COMPLETE.** The restore,
the resubmitted sync, the backend restart, and the T057 live run all
executed on 2026-11-05 with payload verdicts read from their
gatekeeper queue records (§4 carries each job id, run id, and
markers). T057 is DISCHARGED (PASS, violations=0). What remains is
gate 2 and the legs it gates: T053's Cloudflare-side execution,
T054, T059, T060 (§6).

**Update (2026-11-11): LAUNCHED.** Gate 2 was discharged
2026-11-06 and the T053 Cloudflare-side execution completed
the same day (tunnel and VPC Service live; the T053 and T054
rows below predate that execution and are corrected by this
paragraph, per their own follow-on note). The origin host
moved from the desktop to the mini-server under the approved
Linux re-stand-up (2026-11-09/10). Setup completed
2026-11-11T13:53:33.868Z after the KDF amendments (PRs #549,
#551, #552). Proofs: P1, P2 PASS (live-route legs); P3
discharged by the completion; P7 PASS 2026-11-10; P8 PASS
(edge legs); P4-P6 and P9-P12 NOT RUN, named as the launch
remainder in the T060 rollout record section 9 - they need
live sessions and are not waived. T060 is complete in that
record's section 9.

Owner approval to proceed: 2026-11-05 (decision queue item 6).
Gate 1 (Spec 080 cutover-final): SATISFIED (prior record).

## 1. Per-task state, T052–T060

| Task | State | Evidence / what remains |
|---|---|---|
| T052 cloudflared desktop service | INSTALL DONE — Desktop Access chat's leg | Their completion record (2026-11-05, job `glossa-cloudflared-install-2026-11-05`, run `42017703151`, payload CF_DONE): cloudflared 2026.10.7, sha256-pinned (`2493dbc1…`), at `C:\Users\trist\Development\Syncyard\services\cloudflared`, windowless logon task `GlossaCloudflared` registered and in its designed wait state (token file absent, CF_TOKEN_ABSENT — the tunnel is created under T053 once gate 2 lands, and the token is then staged via the grab pattern). Their record governs; this record consumes it, does not assert it. |
| T053 Tunnel + VPC as checklist | REPO-SIDE DONE; Cloudflare-side BLOCKED (gate 2) | Checklist: `records/t053-tunnel-vpc-checklist.md` — creation steps, §2.3 rotation, token staging via the gatekeeper grab pattern (§3 of the checklist), no-published-route / no-CNAME assertions (§4), ID slots (§5). Tunnel and VPC Service do not exist yet: the token lacks the Tunnel write scope and Connectivity Directory scopes (§2). D1 leg discharged (below). |
| T054 Custom Domain + DNS verification | BLOCKED (gate 2) | Cannot be read, let alone verified, with the current token (Workers domains read 403; DNS read 403). The parent brief's statement that the Worker exists as a Custom Domain is **not verifiable with this token** and is recorded as such, not assumed. Executes at deploy time once scopes land (checklist §2 step 7 + §4 assertions). |
| T055 Edge retarget to the VPC origin | CODE DONE (this PR) | `GLOSSA_ORIGIN` Workers VPC binding replaces the GlossaFront/container seam; origin-unreachable becomes the edge's own noindex 503; project-data responses stamped `Cache-Control: no-store`; method/path/query/body/streaming pass through. Edge suite: 98/98 vitest + tsc clean (measured locally, §5). Deploy waits on gate 2 + the real VPC Service ID (wrangler placeholder stands; the deploy workflow refuses while it does). |
| T056 Desktop acceptance of edge identity | CODE DONE (this PR) | Desktop posture of `CloudScopeMiddleware`: engages only on edge-provenance requests while a credential is configured; credential resolves env → protected keys store (`glossa_service_credential`, T024's desktop storage leg); validated edge requests marked so `ApiTokenMiddleware` stands down; host management (shutdown, env) scoped-404 through the edge for every role; terminal gate unchanged. Tests: `backend/tests/test_cloud_desktop_posture.py` (§5). The credential VALUE is provisioned at go-live (checklist §2 step 6) — never before, never in a record. |
| T057 Primary-workspace scope reconciliation | DONE — LIVE RUN PASS (2026-11-05) | Checker: `backend/glossa_lab/workspace_scope_check.py` + `tools/workspace-scope/check_workspace_scope.py` (+ unit tests, §5). Live run executed on the DESKTOP against the dataset in place (read-only; dataset never copied): job `20261105T165053Z-glossa-spec083-desktop-t057-check-2026-11-05-42e996`, run `42075508802`, wrapper success, payload **`T057_VERDICT=PASS`** (checker exit 0) — `VERDICT: PASS violations=0`; primary workspace present (`workspaces=1 primary[indus_decipherment] present=yes`); every scoped table clean (citations, correspondences, hypotheses, notebooks: total=0, unscoped=0, misassigned=0); evidence store consistent (`owner='indus_decipherment' primary='indus_decipherment' consistent=yes`). Full leg record in §4. The verdict also lands in the T060 rollout record at go-live. |
| T058 Bundle production path retirement | DONE (this PR) | `[[r2_buckets]]`, `[[containers]]`, the DO binding/exports are out of `wrangler.toml`; `src/front.ts` deleted; the deploy workflow's container leg removed. Guard tests in `test/config-guards.test.ts` ("bundle production path retired") fail if any of it returns. The compose build remains the local verification shape only. The dataset/bundle reaches the hosted origin as part of the desktop dataset itself (sync + T057), not via a store. |
| T059 Pre-launch proofs on the real route | READY TO RUN (§3) | Cannot execute until the route exists (gate 2 + T052 + deploy). The proof list is fixed in §3; deltas vs Phase 3 are named there. |
| T060 Rollout record | PENDING (assembled at go-live) | Will record: Tunnel ID, VPC Service ID, Custom Domain state, desktop install revision, T057 verdict, T059 proof results, go-live timestamp; plus the LEDGER.md entry. Slots live in the T053 checklist §5. |

## 2. Gate 2 — exact missing scopes (measured 2026-11-05, read-only probes)

BitConcepts Cloudflare account `2df9ae83aa3913feaeec0fd96cbf3614`;
zone `bitconcepts.tech` `167534fd53e0f7a88f20211d60045f32` (active,
Free plan); stored BitConcepts Ops account token id
`1682058e702cc76acb831aa3e280f9be` (verified active). The token HAS
D1 Read/Write, Pages Read/Write, Zero Trust Read/Write and more.
Missing, each with its API evidence:

1. **Workers Scripts Read/Write** — `GET /accounts/{acct}/workers/domains` → 403 (code 10000); `GET …/workers/subdomain` → 403 (10000); `GET /zones/{zone}/workers/routes` → 403. Blocks the edge deploy and any read of the Custom Domain state.
2. **DNS Read/Write (zone)** — zone policy is Zone Read + Dynamic URL Redirects only; `GET /zones/{zone}/dns_records` → 403 (10000). Blocks T054's verification leg.
3. **Tunnel write scope** — tunnel list reads 200 with **zero** tunnels; `glossa-desktop` does not exist and cannot be created. Blocks T053 + token staging.
4. **Connectivity Directory Admin + Bind (+ Read)** — `GET /accounts/{acct}/connectivity/directory/services` → 403 (10000). Blocks the VPC Service registration; Worker deploys carrying `vpc_services` bindings also require Read + Bind on the deploying token (workers-sdk #11884).

**Owner act:** extend the BitConcepts Ops token (or mint a
deployment token) with those four scope groups. That is the whole
of gate 2 — nothing else is missing.

**Discharged within gate 2's reach:** the D1 database
`glossa-identity` was created 2026-11-05 (D1 Write was in scope):
id `5de6e49e-bc67-4eaf-94da-728ae9b1d8a7`, committed in
`cloud/edge/wrangler.toml`. Migrations intentionally not
hand-applied; the deploy workflow applies them.

## 3. T059 — proof list ready to run (real route, at go-live)

Phase 3's proofs re-run against `https://glossa.bitconcepts.tech`
with the desktop as origin, plus the deltas named in T059:

- P1 Anonymous wall: `/api/*` → edge 401 with no data; pages → 302 to `/login`; the public surface is exactly the Amendment 2 table.
- P2 Noindex: `X-Robots-Tag: noindex, nofollow` on every response class incl. errors and redirects; `/robots.txt` disallows all.
- P3 Glassbreak setup: seed → `/setup` completes → owner session works → `/setup` answers 404 thereafter. (The code + URL are delivered to the owner once, in the parent chat, at this step — and nowhere else.)
- P4 Login/logout + sliding session; revocation cascades (disable/type change/matrix change delete sessions instantly).
- P5 Invite lifecycle: create → redeem → member session; second redemption, expired, and revoked codes all fail.
- P6 Workspace scope on the REAL desktop dataset: member/viewer/outsider matrix against primary-workspace records (scoped 404 body exactly `{"detail": "Not found"}`); T057's verdict is the dataset-side precondition.
- P7 **Desktop-offline proof (delta)**: stop the desktop backend (or the tunnel) → the edge answers its own noindex 503 `origin_unavailable` with no project data; restore → service resumes. (Phase 3 proved the container equivalent; the desktop is now the thing that can be off.)
- P8 **Credential-in-wrong-position proofs (delta)**: the Spec 082 install token in cookie/header/query positions yields no authenticated access (T024 suite, re-run on the real route); identity headers sent directly to the edge without a session are stripped and confer nothing.
- P9 **Host-management proof (delta)**: through the edge, an admin session's POST `/api/v1/shutdown` and GET `/api/v1/env/status` answer the scoped 404; locally on the desktop both remain reachable (T056 tests pin the same split pre-launch).
- P10 Terminal gate: member → 403 with `X-Glossa-Denial: terminal-admin-only` + an edge audit row; admin passes.
- P11 Attribution: a mutating act through the edge is stamped with the edge actor on the desktop record (created_by / "via desktop import" conventions unchanged).
- P12 Streaming/terminal + large-response pass-through over the tunnel (the T055 delta surface: method/path/query/body/streaming preserved end to end).

## 4. Desktop legs — state from their own records

- **Sync (this sequence's leg a):** gatekeeper job
  `20261105T113411Z-glossa-spec083-desktop-sync-2026-11-05-b3df72`
  (run.yml, quick lane, `--cwd C:\Users\trist`, payload: ff-only sync
  of `C:\Users\trist\Development\BitConcepts\glossa-lab` to
  origin/main, refusing on dirty/diverged). The job sat undispatched
  ~95 minutes (queue starvation: the quick lane's serialization gate
  plus the fleet-mirror's 10-minute occupancy, diagnosed by the
  Desktop Access chat from the gatekeeper's own code) and was then
  dispatched by operator priority as run `42033093267`. **Payload
  verdict (queue record, verdict_source=markers): REFUSED by
  design** — `BRANCH=main`, `OLD_HEAD=309ea63c`, `DIRTY_COUNT=5`,
  `SYNC_FAIL reason=dirty-tree` (payload exit 4; run conclusion
  failure). The sync touched nothing: no stash, no reset, no fetch
  past the refusal point. The desktop checkout therefore still
  stands at `309ea63c`, ~118+ commits behind main.
  **Follow-on enumeration (read-only):** job
  `20261105T131620Z-glossa-spec083-desktop-dirty-enum-2026-11-05-862c60`
  lists the 5 dirty paths with their nature. **Enumeration
  result (queue record, run `42035796835`, run conclusion success,
  payload exit 0):** `HEAD=309ea63c`, `BRANCH=main`,
  `DIRTY_COUNT=5`, `ENUM_DONE=1`. All five paths are modified and
  unstaged (` M`), and the staged diff stat is empty:
  - `frontend/dist/index.html`
  - `outputs/anchor_staging.json`
  - `outputs/anchor_staging_archive.json`
  - `outputs/partial_loop_result.json`
  - `outputs/study_loop_sessions.json`

  Diff stat across the five: 5 files changed, 3857 insertions(+),
  243 deletions(-). **Disposition:** all five are regenerable
  runtime products of the backend running from that clone; none is
  a hand-authored source edit. Under the follow-on sequence of
  2026-11-05 they are restored to their committed state by a
  dedicated restore job (leg 2), and the ff-only sync is then
  resubmitted unchanged (leg 3); both payload verdicts are read
  from their queue records. **Named follow-on design item (not
  done here):** the sync's dirty gate will refuse again after any
  backend run that regenerates these paths, so scoping the gate
  to exclude the runtime-output paths (`outputs/*`,
  `frontend/dist/index.html`) is a design question for a later
  spec amendment; this sequence does not change the gate. (The
  restart this paragraph originally deferred has since executed —
  see the restart leg below.)
- **Restore (leg 2, executed 2026-11-05):** job
  `20261105T141515Z-glossa-spec083-desktop-restore-dirty-2026-11-05-419f02`,
  dispatched by operator priority (the same quick-lane starvation)
  as run `42047390682`. **Payload verdict (queue record,
  verdict_source=markers): RESTORE_OK tree-clean** —
  `HEAD_BEFORE=309ea63c`, `BRANCH=main`, `CHECKOUT_RC=0`,
  `DIRTY_AFTER_COUNT=0` (wrapper conclusion success). The five
  enumerated paths were restored to their committed state by
  `git checkout`; nothing else was touched.
- **Sync resubmission (leg 3, executed 2026-11-05):** job
  `20261105T155824Z-glossa-spec083-desktop-sync-resubmit-2026-11-05-de56b5`,
  run `42061190779`, the byte-identical script (sha256 `e8424c13…`,
  verified against the original job's queue record before
  submitting). **Payload verdict (queue record,
  verdict_source=markers): SYNC_OK** — `FETCH: 309ea63c..c7712b1d
  main -> origin/main`, `NEW_HEAD=c7712b1d6ce652a0007d22ad31506b993cc1fc98`,
  `COMMITS_APPLIED=187`, `DIRTY_AFTER=0` (fast-forward, wrapper
  conclusion success, payload exit 0). The desktop checkout stands
  at `c7712b1d`, the main tip at the time (the PR #529 merge
  commit).
- **Backend restart (executed 2026-11-05):** job
  `20261105T162555Z-glossa-spec083-desktop-restart-2026-11-05-89b0ab`,
  run `42066999403`. **Payload verdict (queue record,
  verdict_source=markers): RESTART_OK** — the backend was stopped
  through its own supervision (`setup-os.cmd stop`, `APP_STOP_EXIT=0`,
  "APP_STOP_TAIL [OK] Stopped."), and the `\GlossaLab` scheduled
  task's starter/ensure shape brought it back (`TASK_FIRED=1`,
  `TASK_LASTRESULT=0x00000000`); no new launcher, no console
  window. Markers: `HEAD=c7712b1d6ce652a0007d22ad31506b993cc1fc98`
  (the synced tree); health before `uptime_seconds: 158923.6`,
  health after `{"status":"healthy","version":"0.1.0","uptime_seconds":3.9,"component":"glossa-lab-backend","build":"dev","auth":"token"}`
  — the 3.9-second uptime is the restarted process answering on
  the synced code. Identity verified BY CONTENT through the VM's
  tailnet forwarder: the desktop health payload, with MCP
  `get_status` reading host `TRISTEN-DESKTOP` (the forwarder,
  found down as a VM-replacement casualty, was restored first by
  its standing install rule; no VM backend unit was touched).
- **T057 live run (executed 2026-11-05):** job
  `20261105T165053Z-glossa-spec083-desktop-t057-check-2026-11-05-42e996`,
  run `42075508802` (operator-priority dispatch after the same
  starvation). **Payload verdict (queue record,
  verdict_source=markers): `T057_VERDICT=PASS`** (checker exit 0)
  against the live dataset in place at
  `C:\Users\trist\AppData\Local\GlossaLab\data`, opened read-only:
  `PRIMARY projects: workspaces=1 primary[indus_decipherment] present=yes`;
  scoped tables all clean (citations, correspondences, hypotheses,
  notebooks each total=0 primary=0 other-workspace=0 unscoped=0
  misassigned=0); global counts anchor_sets 8, corpus_catalogue
  39, discovery_items 969, jobs 18, job_results 17, model_scores
  9042, report_templates 90, studies 13, texts 9;
  `STORE evidence-store: owner='indus_decipherment' primary='indus_decipherment' consistent=yes`;
  **`VERDICT: PASS violations=0`**. T057 is discharged; the
  verdict carries into the T060 rollout record.
- **cloudflared (T052):** install complete (see T052 row). When
  gate 2 creates the tunnel, the token is staged via the
  grab pattern for their launcher (checklist §3); the tunnel then
  connects with no further install work.

## 5. Verification measured for this PR (local, pre-merge)

- Edge: `npm run typecheck` clean; `npm test` 98/98 PASS (6 files) —
  includes the new T055 tests (origin-down 503, no-store split,
  single-binding routing) and the T058 config guards.
- Backend: full local enumeration per the program's standing method
  (glossa-ci venv, no `-x`, verdict from the log file
  `enumeration-2026-11-05.log` in the program's build-record dir,
  phase392 deselected by name): **2694 passed, 108 skipped,
  1 deselected, 2 failed** in 26:25. The 2 failures, dispositioned:
  (1) `test_phase133_stage0_inventory.py::test_builder_recomputation_skips_without_inputs`
  — the accepted phase133 environmental baseline (a local-only
  research file absent on this VM); (2)
  `test_auth_consumers.py::test_auth_proof_kit_end_to_end` — its
  spawned uvicorn backend missed the test's 30 s health deadline
  under full-suite load; standalone rerun on this tree **passes**
  (1 passed, 34.6 s — the test's own runtime sits at its deadline,
  so the full-run miss is load, not code). No tray-teardown ERROR
  occurred this run. New modules in this PR: desktop posture 10/10,
  workspace-scope checker 5/5 (also inside the enumeration totals).
- Ledger gate, both modes verbatim (2026-11-05, this tree): full
  mode **29 PASS / 0 FAIL / 1 NOT-RUN — RESULT: PASS**; `--regen`
  **32 PASS / 0 FAIL / 0 NOT-RUN — RESULT: PASS** (the standing
  post-Spec-089 profile, unchanged by this PR's LEDGER.md entry).

## 6. What remains, in order, after this PR merges

1. Owner extends the Cloudflare token scopes (gate 2, §2).
2. Execute the T053 checklist §2 (tunnel → token staging via grab →
   VPC Service → wrangler service_id → SERVICE_CREDENTIAL on both
   ends → deploy).
3. T054 verification + T059 proofs (§3) against the real route.
4. T060 rollout record + LEDGER.md entry; glassbreak delivery to the
   owner in the parent chat. **Launch happens only there.**

(The former step 3 — desktop sync, backend restart on the synced
code, T057 live reconciliation — is COMPLETE as of 2026-11-05; see
§4. T057 named no violations to reconcile.)
