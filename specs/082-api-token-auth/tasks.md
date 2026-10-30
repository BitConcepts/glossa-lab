# Tasks: Per-Install API Token Authentication (Spec 082)

## Step 0 — spec (PR: `spec/082-api-token-auth`)

- [x] T001 Spec package: spec.md (problem, stories, FR-001…008, open-routes table, assumptions), plan.md, tasks.md, aee-claims.json (C082-1…6 with evidence + falsifiers, normalized format)
- [x] T002 Claims bundle verified: loads + assesses under the pinned AEE 1.5.3 assessor (`aee validate` + `aee assess --no-ledger`), output recorded in the PR body
- [x] T003 ui-contract.md published in this folder (frontend token contract for the Spec 081 Phase 2 build) + LEDGER.md entry (H1)

## Step 1 — backend enforcement (PR: `feat/082-backend-auth`)

- [x] T004 `backend/glossa_lab/auth.py`: resolution (env → file → generate+persist), CSPRNG, 0600, atomic write, mtime-cached re-read, constant-time compare, fingerprint, CLI (`ensure|rotate|path|fingerprint`, never prints the value)
- [x] T005 Middleware in `create_app()`: pure ASGI, open-list per spec, 401 JSON + `WWW-Authenticate`, `GLOSSA_API_AUTH=off` named switch with startup warning; health payload gains the `auth` mode field
- [x] T006 `backend/glossa_mcp/server.py`: Authorization header on all backend calls (env token, file fallback); 401 surfaces as a named JSON tool error
- [x] T007 Tests: conftest seam (env test token + respectful header injection); `tests/test_api_token_auth.py` — route-family 401 matrix, health posture, docs/openapi gating, token non-disclosure (responses + logs), file perms, generation entropy, rotation semantics
- [x] T008 CI: frontend-tests job's throwaway backend runs `GLOSSA_API_AUTH=off` (comment names this spec + T010); LEDGER.md entry

## Step 2 — consumers + proof kit (PR: `feat/082-consumers`)

- [x] T009 Tray: token resolution per use; shutdown header; Open Glossa Lab fragment handoff; Copy API Token menu item; named tray-log lines on resolution failure; `tests/test_tray_token_auth.py` headless tests; tray/README.md token section
- [x] T010 (filed, owned by Spec 081 Phase 2 landing) Remove the CI `GLOSSA_API_AUTH=off` accommodation once the SPA implements ui-contract.md — *not* part of this spec's PRs; recorded here so the switch has a named death — **done 2026-10-30 with Spec 081 PR-6**: ci.yml's frontend-tests backend now runs a throwaway `GLOSSA_API_TOKEN` and the e2e fixtures seed it; the SPA implements the contract.
- [x] T011 `setup-os.cmd`: install-time token ensure (fail-loud, path-only output); stop path sends the token header when the file exists
- [x] T012 `services/linux/healthcheck.py`: token resolution + authenticated /docs & /openapi.json legs + named failure listing paths tried; `services/linux/install.sh` passes `GLOSSA_TOKEN_FILE` for its install-time check
- [x] T013 Proof kit: `tools/auth-proof/check_auth.py` (stdlib, bounded, marker output, exit code) + a local end-to-end run against a test instance recorded in the PR body

## Step 3 — MCP skill (workspace change, no repo PR)

- [ ] T014 `custom-skills/local-glossa-lab-mcp`: bin client forwards/seeds `GLOSSA_API_TOKEN` for the server child; SKILL.md states the Spec 082 env requirement

## Cutover gate (owned by the migration worker, recorded here)

- [ ] T015 Desktop install: proof kit passes against the running authed install (health `auth: token`; 401 matrix; install token 200) — required before the cutover is declared final
