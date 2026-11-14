# Spec 092 Stage 1 — stage record (2026-11-14)

Stage 1 (credential encryption at rest) is complete: the code legs
(T101–T103) landed in PR #569 (merge `3cb7382c`, CI 10/10,
delivery-checker RESOLVED on the parent's own run), and the live
leg (T104) was executed by the parent against the one production
store the same day, after the merge. Claims discharged:
C092-1..5 and the store leg of C092-7 (its library leg is Stage
2's, per the plan).

## Code legs (PR #569)

- **Registered credential set** — `CREDENTIAL_KEYS` in
  `api/settings.py`, data beside `KNOWN_KEYS`, 16 names:
  `mistral_api_key`, `openai_api_key`, `anthropic_api_key`,
  `google_api_key`, `serp_api_key`, `news_api_key`,
  `brave_search_api_key`, `semantic_scholar_api_key`,
  `core_api_key`, `uspto_api_key`, `academia_session_cookie`,
  `smtp_password`, `ms_graph_refresh_token`, `resend_api_key`,
  `hf_api_token`, `glossa_service_credential`. Left plaintext by
  recorded reasoning: configuration (hosts, ports, toggles,
  intervals, `_provider_prefs`, `study_loop_daily`), identifiers
  the providers require in cleartext query parameters
  (`openalex_email`, `unpaywall_email`), and non-secret Graph
  identifiers (`ms_graph_client_id`, `ms_graph_tenant_id`,
  `smtp_username`).
- **Store format v2** — credential entries are envelope objects
  `{v: 2, alg: "AES-256-GCM", nonce, ct}` with a fresh nonce per
  value per save; every other entry is byte-for-byte the v1
  shape. `_load_keys` decrypts inside the store functions;
  callers see plaintext exactly as before.
- **Key custody (D-092-1 as adopted, option (a))** — a 32-byte
  key, base64-encoded in a 0600 file outside `{data_dir}`:
  default `{data_dir.parent}/glossa-lab-credential.key`, env
  override `GLOSSA_CREDENTIAL_KEY_FILE`. Operator-created; the
  loader never creates it and nothing logs it. Typed failure
  modes: `CredentialKeyMissing` / `CredentialKeyUnreadable` /
  `CredentialKeyMalformed` / `CredentialKeyWrongLength`;
  store-side states `credential_store_undecryptable`,
  `credential_store_corrupt`,
  `credential_store_migration_failed`. The legacy loader's
  silent-empty behaviour is retired for any existing-but-
  unreadable store (C092-3).
- **KNOWN_KEYS standing decision** — `glossa_service_credential`
  is in the encrypted set but deliberately NOT in `KNOWN_KEYS`:
  the masked GET shape and the PUT writable set are the
  C092-5-frozen surface, and provisioning stays an operator act.
  A store holding it encrypts it and `get_key` serves it.
- **Save path** — the verified construction inside the store
  module (temp in the target's directory, 0600 before rename,
  fsync, atomic rename, read-back verification); Stage 2 lifts
  it into the library and re-proves this leg.
- **Battery** — `backend/tests/test_settings_credential_
  encryption.py`, 23 tests, synthetic fixture values only:
  byte sweep finds no stored credential value in plaintext,
  base64, hex, or any contiguous substring of 12+ characters
  (C092-1); a data-dir-only copy cannot decrypt and the fixture
  key is swept absent from the data dir and the repo tree
  (C092-2); wrong-key, missing-key, and bit-flipped-ciphertext
  fixtures raise the named state and serve nothing (C092-3);
  legacy fixtures migrate value-identical and exactly once,
  and failed migrations leave the original byte-untouched
  (C092-4); the consumer contract battery passes identically
  against v1 and v2 stores with no consumer-module diffs beyond
  the authorized database-init tolerance (C092-5). Two existing
  tests were updated on the PR's face (disclosed in its body):
  the Spec 083 posture fixture now provisions a synthetic key
  beside its tmp data dir, and the disk-full `_save_keys` test
  gained a fixture key; neither assertion was weakened.

## Live leg (T104) — executed 2026-11-14, parent-run

**Adaptation of record.** The plan's T104 text names the desktop
install and the gatekeeper; that text predates the re-stand-up.
The one production store now lives on the mini-server (backend
unit `glossa-lab-backend`, checkout `/home/tpierson/glossa-lab`),
so the live leg ran there under the origin discipline (pull
--ff-only + restart). The plan's premise — exactly one
production store — holds.

**Before census** (names and counts, never values; read
2026-11-14 ~05:06 EST): store
`/home/tpierson/glossa-lab/backend/data/.keys.json`, mode 0600,
107 bytes, SHA-256 `9e7dde0e…`, 2 entries, both plaintext
strings: `glossa_service_credential` (length 43),
`study_loop_daily` (length 1).

**The act.** (1) The key file was created on the box at the
built default custody location
(`backend/glossa-lab-credential.key`, mode 0600, 44 bytes) by a
command that generated the 32 random bytes on the box itself;
the key material was never printed, transmitted, or seen by the
operator agent. The repo `.gitignore` covers `*.key`. (2) The
`cryptography` dependency the stage adds (50.0.2, inside the
pinned `>=44,<51`) was installed into the backend venv — it was
absent, and a restart without it would have failed the settings
import; it was installed BEFORE the restart. (3) The origin was
pulled --ff-only `a165746c` → `3cb7382c` (the incoming range
touches no path under `outputs/` or `reports/`, so the pull
could not disturb the runtime-dirty live stores) and the
backend restarted.

**After census** (same day): store mode 0600, 231 bytes,
SHA-256 `cc83575e…`; `glossa_service_credential` is a v2
envelope object (keys `alg`, `ct`, `nonce`, `v`);
`study_loop_daily` remains a plain string of length 1.
`get_key` in the backend's own environment resolves the
credential at length 43 — the pre-migration length — and the
config value as `1`. A second restart left the store's SHA-256
unchanged: migration ran exactly once (C092-4, live leg).
Backend health, read through the VM forwarder after its
standing restore, is the exact six-key identity payload
(`healthy`, `0.1.0`, uptime advancing, `glossa-lab-backend`,
`dev`, `token`), and the MCP foundation check reads **17/17
PASS, 0 fail, 0 warn** against the migrated store (C092-1,
live leg).

**Custody note.** The key file exists only on the mini-server.
Under D-092-1 that is the designed posture: losing it means the
store reads as the named `credential_key_missing` state and the
one stored credential is re-provisioned by an operator act (it
was placed by one in the first place). No copy was made to any
other machine or record.

## What this does not establish

Nothing about any other install (there is none), nothing about
the library form of the write construction (Stage 2), and no
claim beyond C092-1..5 and C092-7's store leg. Stage 2 is next
in the owner's priority order when commissioned.

**AI disclosure:** executed by an AI agent (Muse, via Muse) at
the direction of Tristen Pierson, per constitution sec. VI.
