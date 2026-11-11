# Spec 083 — KDF amendment record: password hasher moves from Argon2id (hash-wasm) to PBKDF2 (WebCrypto) (2026-11-10)

**State: FIX BUILT; supersedes the T015/T017 implementation choice
on the KDF only.** The PasswordHasher interface, the encoded-string
custody rule (the encoded hash is the only password residue in D1),
and the T016 dummy-hash timing discipline are unchanged. T015's
parameter verdict as recorded in the 2026-10-30 password-hashing
audit (Argon2id, OWASP parameters, no defects) is superseded on
implementation only: the parameters were sound, but the
implementation cannot execute on the production runtime at all.

## 1. Symptom

The live first-run setup could not complete. A POST to
`https://glossa.bitconcepts.tech/setup` with the correct seeded
setup code and a valid password answered **HTTP 500
`internal_error`**, repeatedly (owner attempts, 2026-11-10). The
setup transaction never landed: D1 `setup_state.completed_at`
stayed NULL and the `users` table stayed at 0 rows, because
`handleSetup` calls `hasher.hash(password)` before `completeSetup`
and user creation. The same failure would meet every registration
path — invite redemption hashes the new password through the same
`defaultHasher` — so no account of any kind could be created on the
live deployment. Login could never be reached: there was no user
to log in as.

## 2. Root cause, reproduced

`cloud/edge/src/password.ts` implemented `hash()` with Argon2id via
`hash-wasm`. hash-wasm inlines its Argon2 WASM as a base64 module
and compiles it at runtime with `WebAssembly.compile()`.
Cloudflare Workers forbids dynamic WebAssembly compilation
(WASM may only ship as a static module import), so the call throws:

```
CompileError: WebAssembly.compile(): Wasm code generation disallowed by embedder
```

Reproduced locally under workerd (`wrangler dev`) on 2026-11-10 by
calling the production `defaultHasher.hash()`: the same
CompileError. `verify()` happens to survive in the runtime (its
code path reaches the embedded module differently), which made the
defect one-sided and quiet: nothing about the deployed Worker's
reads suggested the write path was dead. Hash creation, however,
can never succeed on this runtime, in any isolate, for any caller.

## 3. Why the test suite missed it

Every flow test injects `FakeHasher`
(`cloud/edge/test/fake-identity.ts`) — deliberately, for speed and
determinism — so the setup/invite/login flows were exercised
end-to-end without the real hasher ever being called. The suite's
own real-hasher tests (`identity.test.ts`, the T015 describe block)
instantiated `Argon2idHasher` under Node, where
`WebAssembly.compile` is permitted and hash-wasm works. No test ran
the production hasher under workerd. The defect class is therefore
"production path never exercised on the production runtime shape,"
the same family as the Stage 2 VPC-scheme and SPA-fallback defects,
both likewise latent from the original build and found only when
the re-stand-up drove the live path.

Fix-side guard: `cloud/edge/test/password.test.ts` now pins the
real `defaultHasher` contract directly (encoded prefix, right and
wrong password, malformed/foreign strings verifying false without
throwing, the stored-iteration-count rule, the dummy hash being a
live encoding in the current format), and §5 records the workerd
proof for this landing.

## 4. The fix

`cloud/edge/src/password.ts` is rewritten on WebCrypto PBKDF2,
which is native to the Workers runtime — no WASM, no native
binding, no fetch:

- KDF: PBKDF2 via `crypto.subtle.importKey` + `deriveBits`,
  digest SHA-512, **210,000 iterations** (the OWASP Password
  Storage Cheat Sheet recommendation for PBKDF2-HMAC-SHA512),
  salt 16 bytes from `crypto.getRandomValues`, derived key
  32 bytes.
- Encoded format: `$pbkdf2-sha512$i=210000$<base64 salt>$<base64
  derived key>` (standard base64), carrying salt and iteration
  count in the string, as the Argon2id encoding did.
- `verify()` parses the iteration count from the stored string and
  derives with the stored salt and count, so a future iteration
  bump keeps hashes minted at older counts verifiable. Comparison
  is constant-time (XOR accumulation). `verify()` returns false —
  never throws — for malformed strings and for foreign formats,
  including retired `$argon2id$` strings.
- `DUMMY_PASSWORD_HASH` is replaced with a real encoding in the
  new format of a throwaway password, generated with the new
  implementation, preserving the T016 timing discipline (unknown
  user costs the same KDF work as a wrong password).
- The `hash-wasm` dependency is removed from
  `cloud/edge/package.json` (the Worker now has no runtime
  dependencies).
- Test-side mirrors updated: the `FakeHasher` foreign-format guard
  keys on `$pbkdf2-sha512$`; the T015 describe block in
  `identity.test.ts` asserts the new parameters and prefix; the
  `cloud/edge/README.md` password section is corrected.

## 5. Verification

- Edge suite (vitest) and `tsc --noEmit`: tallies recorded in the
  landing PR.
- Workerd proof: a scratch probe (not committed) importing the new
  `password.ts`, served by `wrangler dev --local`, called
  `hash()` and `verify()` inside workerd — the runtime that
  refused the old implementation — and both succeeded; outputs
  recorded in the landing PR.
- Live re-proof after deploy (owner-gated deploy act): the seeded
  setup completes, `setup_state.completed_at` is set, and the
  glassbreak owner row exists. This record will be updated by the
  T060 rollout amendment when the launch completes.

## 6. Security trade, stated plainly

What is given up: Argon2id's memory-hardness. PBKDF2's work factor
is purely computational, so a leaked hash database falls to GPU
attack faster per guess than Argon2id at the audited parameters
would. What is kept: a salted, iterated KDF at the OWASP
recommended work factor for this algorithm, constant-time
comparison, indistinguishable login failures, and hash-only storage
in D1. The alternative was not Argon2id — on this runtime the
alternative was no working hasher at all. If Cloudflare ever
permits a memory-hard KDF on Workers (or a static-WASM Argon2
module proves out under the isolate budget), restoring Argon2id
is a hasher-class swap behind the unchanged interface plus a
verify-both-formats window; that is future work, not this
amendment.

**No migration is needed:** the `users` table is empty — no live
password hash exists in any format — because the defect prevented
the first account from ever being created. The one stored encoded
value the old code shipped, the dummy hash constant, is replaced
in the same change.

**AI disclosure:** executed by an AI agent (Muse, via Muse)
at the direction of Tristen Pierson, per constitution sec. VI.
