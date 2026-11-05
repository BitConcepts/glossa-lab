# Spec 083 — Go-live readiness record (2026-11-05)

**State: NOT READY TO LAUNCH. This record is the stop point.** The
repo-side and wiring legs of the go-live sequence are built (PR
referenced in §6); the launch itself waits on gate 2 (Cloudflare
scopes, owner act) and on the desktop legs below. At actual go-live,
the glassbreak one-time setup code + URL are delivered to the owner
ONCE in the Glossa-Lab chat — no launch act has been taken, no setup
code has been generated, and nothing in this record performs one.

Owner approval to proceed: 2026-11-05 (decision queue item 6).
Gate 1 (Spec 080 cutover-final): SATISFIED (prior record).

## 1. Per-task state, T052–T060

| Task | State | Evidence / what remains |
|---|---|---|
| T052 cloudflared desktop service | IN PROGRESS — Desktop Access chat's leg | Accepted and executing there: cloudflared 2026.10.7, sha256-pinned, at `C:\Users\trist\Development\Syncyard\services\cloudflared`, windowless logon task `GlossaCloudflared` via a launcher, persistent/self-restarting. Their completion record governs; this record consumes it, does not assert it. |
| T053 Tunnel + VPC as checklist | REPO-SIDE DONE; Cloudflare-side BLOCKED (gate 2) | Checklist: `records/t053-tunnel-vpc-checklist.md` — creation steps, §2.3 rotation, token staging via the gatekeeper grab pattern (§3 of the checklist), no-published-route / no-CNAME assertions (§4), ID slots (§5). Tunnel and VPC Service do not exist yet: the token lacks the Tunnel write scope and Connectivity Directory scopes (§2). D1 leg discharged (below). |
| T054 Custom Domain + DNS verification | BLOCKED (gate 2) | Cannot be read, let alone verified, with the current token (Workers domains read 403; DNS read 403). The parent brief's statement that the Worker exists as a Custom Domain is **not verifiable with this token** and is recorded as such, not assumed. Executes at deploy time once scopes land (checklist §2 step 7 + §4 assertions). |
| T055 Edge retarget to the VPC origin | CODE DONE (this PR) | `GLOSSA_ORIGIN` Workers VPC binding replaces the GlossaFront/container seam; origin-unreachable becomes the edge's own noindex 503; project-data responses stamped `Cache-Control: no-store`; method/path/query/body/streaming pass through. Edge suite: 98/98 vitest + tsc clean (measured locally, §5). Deploy waits on gate 2 + the real VPC Service ID (wrangler placeholder stands; the deploy workflow refuses while it does). |
| T056 Desktop acceptance of edge identity | CODE DONE (this PR) | Desktop posture of `CloudScopeMiddleware`: engages only on edge-provenance requests while a credential is configured; credential resolves env → protected keys store (`glossa_service_credential`, T024's desktop storage leg); validated edge requests marked so `ApiTokenMiddleware` stands down; host management (shutdown, env) scoped-404 through the edge for every role; terminal gate unchanged. Tests: `backend/tests/test_cloud_desktop_posture.py` (§5). The credential VALUE is provisioned at go-live (checklist §2 step 6) — never before, never in a record. |
| T057 Primary-workspace scope reconciliation | CHECKER DONE (this PR); LIVE RUN PENDING | Checker: `backend/glossa_lab/workspace_scope_check.py` + `tools/workspace-scope/check_workspace_scope.py` (+ unit tests, §5). Per-class counts (scoped classes fail loudly on unscoped/misassigned; global classes counted and named; experiments linkage reported; evidence-store ownership verified against the primary). Live run executes on the DESKTOP against the dataset in place (read-only; dataset never copied) via gatekeeper payload `desktop-t057-check-2026-11-05.ps1` — submittable only after the desktop sync lands (the checker file arrives with it). Its verdict lands in the T060 rollout record. |
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
  lists the 5 dirty paths with their nature — result:
  _(filled from its queue record when it lands)_. Nothing is
  cleared, stashed, or reset: if the files are runtime state the
  sync design must accommodate them; if they are source edits they
  are someone's work. Either way the disposition is the parent's
  call, recorded here when known. After a successful sync the
  desktop backend still runs pre-sync code until restarted — the
  restart belongs to the go-live sequence proper (T059/T060), and
  no readiness claim in this record assumes it.
- **cloudflared (T052):** Desktop Access chat executing — see T052
  row. When gate 2 creates the tunnel, the token is staged via the
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
3. Desktop sync job dispatches and lands (or Desktop Access clears
   the lane anomaly); restart the desktop backend on the synced
   code; run the T057 live reconciliation; reconcile any violations
   it names before proceeding.
4. T054 verification + T059 proofs (§3) against the real route.
5. T060 rollout record + LEDGER.md entry; glassbreak delivery to the
   owner in the parent chat. **Launch happens only there.**
