// Password hashing (Spec 083, Step 2 / T015, T017; KDF amended
// 2026-11-10 — see
// specs/083-cloud-edition/records/kdf-amendment-2026-11-10.md).
//
// Original implementation choice (T015/T017): Argon2id via
// `hash-wasm`. hash-wasm ships the Argon2 WASM as an inlined base64
// module and compiles it at runtime — and Cloudflare Workers
// forbids dynamic WebAssembly compilation, so the production
// hasher's hash() throws `CompileError: WebAssembly.compile():
// Wasm code generation disallowed by embedder` on every call
// (reproduced under workerd, 2026-11-10; this is what made the live
// first-run /setup answer 500). The unit suite never caught it
// because every flow test injects FakeHasher and the Argon2 tests
// ran under Node, where the compilation is allowed.
//
// Current implementation: PBKDF2 via WebCrypto (`crypto.subtle`),
// native to the Workers runtime — no WASM, no native binding, no
// network fetch. Parameters are the OWASP Password Storage Cheat
// Sheet recommendation for PBKDF2-HMAC-SHA512:
//   iterations 210,000, salt 16 random bytes, output 32 bytes.
// The encoded hash string
// ($pbkdf2-sha512$i=210000$<base64 salt>$<base64 derived key>)
// carries the iteration count and salt, so verification needs
// nothing else stored, and verify() derives with the count parsed
// from the stored string so a future iteration bump keeps older
// hashes verifiable. The trade is recorded in the amendment: PBKDF2
// is not memory-hard the way Argon2id is; it is the strongest KDF
// the Workers runtime can actually execute.

export const PBKDF2_PARAMS = {
  digest: "SHA-512",
  iterations: 210000,
  saltLength: 16,
  keyLength: 32,
} as const;

const ENCODED_PREFIX = "$pbkdf2-sha512$";

export interface PasswordHasher {
  hash(password: string): Promise<string>;
  verify(password: string, encodedHash: string): Promise<boolean>;
}

function bytesToBase64(bytes: Uint8Array): string {
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary);
}

function base64ToBytes(text: string): Uint8Array | null {
  try {
    const binary = atob(text);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    return bytes;
  } catch {
    return null;
  }
}

async function deriveKey(
  password: string,
  salt: Uint8Array,
  iterations: number,
  keyLength: number,
): Promise<Uint8Array> {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(password),
    "PBKDF2",
    false,
    ["deriveBits"],
  );
  const bits = await crypto.subtle.deriveBits(
    {
      name: "PBKDF2",
      hash: PBKDF2_PARAMS.digest,
      salt: salt as BufferSource,
      iterations,
    },
    key,
    keyLength * 8,
  );
  return new Uint8Array(bits);
}

/** Parse "$pbkdf2-sha512$i=<n>$<b64 salt>$<b64 key>"; null if foreign/malformed. */
function parseEncoded(
  encodedHash: string,
): { iterations: number; salt: Uint8Array; expected: Uint8Array } | null {
  if (!encodedHash.startsWith(ENCODED_PREFIX)) return null;
  const parts = encodedHash.slice(ENCODED_PREFIX.length).split("$");
  if (parts.length !== 3) return null;
  const iterMatch = /^i=([1-9][0-9]*)$/.exec(parts[0]);
  if (!iterMatch) return null;
  const iterations = Number(iterMatch[1]);
  const salt = base64ToBytes(parts[1]);
  const expected = base64ToBytes(parts[2]);
  if (!salt || salt.length === 0 || !expected || expected.length === 0) {
    return null;
  }
  return { iterations, salt, expected };
}

export class Pbkdf2Hasher implements PasswordHasher {
  async hash(password: string): Promise<string> {
    const salt = crypto.getRandomValues(
      new Uint8Array(PBKDF2_PARAMS.saltLength),
    );
    const derived = await deriveKey(
      password,
      salt,
      PBKDF2_PARAMS.iterations,
      PBKDF2_PARAMS.keyLength,
    );
    return (
      `${ENCODED_PREFIX}i=${PBKDF2_PARAMS.iterations}$` +
      `${bytesToBase64(salt)}$${bytesToBase64(derived)}`
    );
  }

  async verify(password: string, encodedHash: string): Promise<boolean> {
    try {
      const parsed = parseEncoded(encodedHash);
      if (!parsed) return false;
      const derived = await deriveKey(
        password,
        parsed.salt,
        parsed.iterations,
        parsed.expected.length,
      );
      // Constant-time comparison: accumulate every byte difference.
      let diff = derived.length ^ parsed.expected.length;
      for (let i = 0; i < derived.length; i++) {
        diff |= derived[i] ^ parsed.expected[i];
      }
      return diff === 0;
    } catch {
      // A malformed stored hash is a failed verification, never a
      // distinguishable error (login failures stay indistinguishable).
      return false;
    }
  }
}

export const defaultHasher: PasswordHasher = new Pbkdf2Hasher();

/**
 * A real PBKDF2 hash of a throwaway password, with the production
 * parameters. Login verifies against this when the username does not
 * exist (or the account cannot sign in), so an unknown user costs the
 * same KDF work as a wrong password and the two failures stay
 * indistinguishable in body and in timing shape (T016).
 */
export const DUMMY_PASSWORD_HASH =
  "$pbkdf2-sha512$i=210000$4RRy+TQvyeHh9vU7z2OKEw==$3jpvMgL5Iz9R3hucJChLJBFP09z4SFcKtiMLghW12+I=";

/** Minimum accepted password length at setup / invite redemption. */
export const MIN_PASSWORD_LENGTH = 8;
export const MAX_PASSWORD_LENGTH = 128;

export function isAcceptablePassword(password: unknown): password is string {
  return (
    typeof password === "string" &&
    password.length >= MIN_PASSWORD_LENGTH &&
    password.length <= MAX_PASSWORD_LENGTH
  );
}
