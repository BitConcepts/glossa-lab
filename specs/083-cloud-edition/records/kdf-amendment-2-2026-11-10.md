# Spec 083 — KDF amendment 2: PBKDF2 iteration count capped by the Workers runtime

Date: 2026-11-10 (ET) · Follows: `kdf-amendment-2026-11-10.md` (PR #549)

## What happened

Amendment 1 replaced the hash-wasm Argon2id hasher (which can never
run on Workers: dynamic WebAssembly compilation is disallowed) with
WebCrypto PBKDF2-HMAC-SHA512 at 210,000 iterations, the OWASP
Password Storage Cheat Sheet recommendation. That change merged
(PR #549) and deployed, and the live first-run `POST /setup` still
answered 500 `internal_error`.

The PR #550 error mirror (handleRequest's catch writes the exception
into the D1 audit log as `edge_error`) captured the throw on the
next probe, audit row ts `2026-11-11T03:55:13.829Z`, target
`POST /setup`:

```
NotSupportedError: Pbkdf2 failed: iteration counts above 100000 are
not supported (requested 210000).
    at deriveKey → Pbkdf2Hasher.hash → handleSetup
```

The Workers WebCrypto implementation caps PBKDF2 iteration counts
at 100,000. The amendment-1 parameters exceeded the platform cap, so
`hash()` threw on every call and setup could never complete.

## The proof of the cap (two-sided, production runtime)

A throwaway probe Worker (`glossa-probe-pbkdf2`, uploaded only for
this measurement and deleted immediately after) ran `deriveBits`
with PBKDF2-HMAC-SHA512 on the production account:

- n=100000 → ok, 32 bytes derived
- n=100001 → NotSupportedError (same message)
- n=210000 → NotSupportedError (the production failure reproduced)

The cap is exactly 100,000, and 100,000 works.

## The change

- `PBKDF2_PARAMS.iterations`: 210000 → **100000**, the platform
  maximum — the strongest setting the runtime can execute.
- `DUMMY_PASSWORD_HASH` regenerated at i=100000.
- `password.test.ts` pins updated to the new parameters.
- `verify()` is unchanged: it derives with the iteration count
  parsed from the stored string. (No stored hashes exist yet —
  setup never completed under either parameter set.)

## Why the amendment-1 gate did not catch this

Two evidence tiers both said 210,000 was fine, and both were the
wrong runtime. The edge suite runs under Node (vitest), whose
WebCrypto accepts 210,000. PR #549's workerd proof ran under the
LOCAL workerd build (`wrangler dev --local`), which also accepts
210,000 — its result is recorded in the root LEDGER.md entry for
amendment 1, and it was real, for that runtime. The production
Workers runtime enforces the 100,000 cap; the local build does not.
Standing lesson, added to the Spec 083 record set: a claim about a
runtime limit is only proven on the production runtime itself. This
amendment's proof is the two-sided production probe above plus,
after deploy, the live setup completion itself
(setup_state.completed_at set, one user row, a successful login) —
the first full exercise of the production path.

## Completion note (2026-11-10, later the same evening)

PR #551 landed the parameter change in `password.ts` and
`password.test.ts` and passed the PR CI profile 10/10 — but a third
pin lived in `identity.test.ts` (the T015 block:
`PBKDF2_PARAMS.iterations` and the encoded-prefix assertion), and
PR CI's cloud smoke job does not run that file. The deploy
workflow's pre-deploy step runs the FULL edge suite; it caught the
stale pin (deploy run 42958581801 failed at the test step, 108/109
edge tests passed, production untouched — the deploy never ran).
This follow-on PR updates the two remaining pins and the
`cloud/edge/README.md` parameter text. Standing lesson: for edge
changes, the deploy workflow's test step is part of the gate
profile, and parameter changes are swept repo-wide by code search,
not file by file.
