# Plan: Per-Install API Token Authentication (Spec 082)

Claims first (this spec PR), then three implementation PRs, each landing green
on its own under the repo discipline (genuine 8/8 CI from per-job conclusions,
C4 freeze gate included; branches deleted on merge). Nothing deploys to the
desktop and nothing restarts there — the migration worker's cutover carries
this code, and "cutover declared final" is gated on the proof kit (step 4).

## Step 0 — this PR (spec only)

`specs/082-api-token-auth/`: spec.md, plan.md, tasks.md, aee-claims.json
(C082-1…6, normalized format, assessed under the pinned AEE 1.5.3),
ui-contract.md (published now so the Spec 081 Phase 2 build can implement the
frontend side in parallel). Plus a LEDGER.md entry (H1).

## Step 1 — backend enforcement (PR: `feat/082-backend-auth`)

| Work | Notes |
|---|---|
| `backend/glossa_lab/auth.py` | Token resolution (env → data-dir file → generate+persist), CSPRNG generation, `0600` POSIX perms, atomic write, mtime-cached re-read (live rotation), constant-time compare, token fingerprint (SHA-256[:8]) for display surfaces, and the operator CLI: `python -m glossa_lab.auth ensure \| rotate \| path \| fingerprint` (never prints the value). |
| Middleware in `create_app()` | Pure ASGI (streaming-safe). Protects every path except the spec's open list; added before CORS so dev-mode preflights are answered by CORS, not rejected. Honors `GLOSSA_API_AUTH=off` with a startup warning (FR-006). |
| `api/health.py` | Payload gains `"auth": "token" \| "disabled"` (identity, C-08 style). |
| `backend/glossa_mcp/server.py` | Sends the header on all backend calls; token from `GLOSSA_API_TOKEN` env, falling back to the token-file candidates. A 401 from the backend surfaces as the tool's JSON error, naming the token as the cause. |
| Test seam + tests | `tests/conftest.py`: session test token via env + default `Authorization` header injection that respects a caller-set header (so the 401 matrix can send missing/empty/wrong credentials). New `tests/test_api_token_auth.py`: the claim matrix (below). Existing suite untouched otherwise. |
| `.github/workflows/ci.yml` | frontend-tests job only: its throwaway backend runs with `GLOSSA_API_AUTH=off` + a comment naming Spec 082 and removal task T010. Backend-tests needs no switch (conftest seam). |

**Claim tests** (each maps to a falsifier): route-family matrix — projects,
spec-studies, studies (POST), terminal run, settings, shutdown (POST),
indus-evidence, jobs — × {no header, wrong token, empty bearer} → 401, and
× {install token} → not 401; health open without a token and carrying the
auth mode; `/openapi.json` + `/docs` → 401 without the token; token string
absent from every response body and from the app log during the matrix;
token file perms `0600` (POSIX-only assertion); two generated tokens differ
and are ≥ 43 chars; rotation: old → 401, new → 200, data dir otherwise
byte-identical.

## Step 2 — consumers (PR: `feat/082-consumers`)

| Surface | Change |
|---|---|
| Tray (`tray/glossa_tray/main.py`) | Resolves the token (env → installed data-dir path per platform → repo `backend/data` dev path), read per use so rotation is picked up. Shutdown POST carries the header. *Open Glossa Lab* opens `<frontend>#token=<token>` (omits the fragment and logs a named line if no token resolves — the backend will have generated one at startup, so this is a shouldn't-happen path). New menu item **Copy API Token** (tkinter clipboard, consistent with the port dialog; failure logged to tray.log, named). Health poll unchanged (open route). Headless tests follow the `test_tray_supervision.py` import pattern (`tests/test_tray_token_auth.py`). |
| `setup-os.cmd` | `install`: after task registration, ensure the token via the venv console python (`-m glossa_lab.auth ensure` with `GLOSSA_MODE=installed` + `PYTHONPATH`); nonzero exit refuses the install loudly, success prints the token **path** only. `do_stop_silent`: the shutdown curl reads `%LOCALAPPDATA%\GlossaLab\data\api_token` when present and sends the header (never echoed); absent file ⇒ bare curl as today, with the bounded kill fallback behind it (comment states this). |
| `services/linux/healthcheck.py` | Resolves the token (`GLOSSA_API_TOKEN` → `GLOSSA_TOKEN_FILE` → `GLOSSA_DATA_DIR` → platform installed default → repo-tree `backend/data` candidate); sends it on the `/docs` and `/openapi.json` legs only (health stays bare). Unresolvable token + authed backend ⇒ failed check whose errors name the paths tried (FR-005). All waits stay bounded (H11). |
| `services/linux/install.sh` | Its post-install healthcheck invocation exports `GLOSSA_TOKEN_FILE` pointing at the backend's data-dir token for the layout it installs (repo `backend/data` — the supervised layout's data dir today), so install-time identity verification works against the authed backend. |
| `scripts/verify_desktop_host.py` | No change needed: all identity traffic flows through `healthcheck.check_once`. Stated here so the absence is a decision, not an oversight. |
| `tray/README.md` | Documents the token: where it lives, Copy API Token, rotation procedure pointer. (H8 — docs in the same cycle.) |

## Step 3 — MCP skill (workspace, not a repo PR)

`~/workspace/custom-skills/local-glossa-lab-mcp/`: `bin/glossa_mcp.py` forwards
`GLOSSA_API_TOKEN` to the server child explicitly and, when the env is unset,
seeds it from the first resolvable token file (running-backend candidates);
`SKILL.md` gains the requirement: the backend is token-authenticated (Spec 082)
— set `GLOSSA_API_TOKEN` or keep the install's token file in place; the cutover
sets it for the desktop target.

## Step 4 — proof kit (in step 2's PR)

`tools/auth-proof/check_auth.py` — stdlib only, bounded (H11), markers +
exit code in the migration staging style. Against a base URL + token file:
health 200 with `auth: token`; data route no-token → 401; wrong token → 401;
install token → 200; POST shutdown-less state-changing probe (a harmless
POST route) no-token → 401. Prints one `AUTH_PROOF …` line per leg and
`AUTH_PROOF_RESULT PASS|FAIL`. The cutover owner runs it on the desktop
install; the cutover's "final" gate consumes its exit code.

## Rotation procedure (operator documentation; FR-004)

1. Run `<venv python> -m glossa_lab.auth rotate` in the install's environment
   (on the desktop: from the repo's `backend\venv`). It prints the new
   fingerprint and the token file path — never the value.
2. The running backend picks the new token up on the file's mtime change —
   no restart. The old token is refused (401) from that moment.
3. Consumers: tray and healthcheck read the file per use — nothing to do.
   The web UI: open it from the tray once (fresh fragment handoff) or paste
   the new token (tray → Copy API Token) into Settings. MCP: if the token is
   carried via `GLOSSA_API_TOKEN` env, update the env and restart the MCP
   server process; file-carried consumers need nothing.

## Risks and guards

| Risk | Guard |
|---|---|
| Existing backend tests call the API without credentials | conftest seam (env test token + respectful default-header injection); the full suite is the CI gate, run per-PR |
| Playwright job drives a pre-contract frontend | the named, health-visible `GLOSSA_API_AUTH=off` switch, CI-job-scoped only, removal filed as T010 |
| Tray stop path silently degrades to kill-only | shutdown carries the token (step 2); the kill fallback remains as the documented last resort, and the tray logs which path stopped the backend |
| Token file location drifts from the backend's real data dir | single source of truth: the backend resolves from `Settings.data_dir`; consumers mirror the documented candidate list, with `GLOSSA_TOKEN_FILE` as the explicit override for supervised layouts |
| A future route ships unprotected | enforcement is middleware-level (FR-001); the claim test enumerates route families from the built app, not from a hand list |
