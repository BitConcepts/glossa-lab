// CSPRNG helpers (Spec 083, Step 2). Every secret the edge mints —
// invite codes, session tokens, setup codes — comes from
// crypto.getRandomValues (the platform CSPRNG) and is encoded
// base64url without padding. Plaintext secrets are returned to the
// caller exactly once and never stored or logged; only their SHA-256
// hashes reach D1 (see src/session.ts sha256Hex).

/** Encode bytes as unpadded base64url. */
export function base64Url(bytes: Uint8Array): string {
  let binary = "";
  for (const b of bytes) binary += String.fromCharCode(b);
  return btoa(binary)
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

/** A CSPRNG secret of `byteLength` bytes (×8 bits of entropy). */
export function randomSecret(byteLength: number): string {
  return base64Url(crypto.getRandomValues(new Uint8Array(byteLength)));
}

/** Invite codes: 24 bytes = 192 bits (FR-002 floor is 128 bits). */
export const INVITE_CODE_BYTES = 24;
export function newInviteCode(): string {
  return randomSecret(INVITE_CODE_BYTES);
}

/** Session tokens: 32 bytes = 256 bits (FR-004 floor). */
export const SESSION_TOKEN_BYTES = 32;
export function newSessionToken(): string {
  return randomSecret(SESSION_TOKEN_BYTES);
}

/** Setup codes: 32 bytes = 256 bits, single-use, 24-hour expiry. */
export const SETUP_CODE_BYTES = 32;
export function newSetupCode(): string {
  return randomSecret(SETUP_CODE_BYTES);
}

/** Row ids: prefixed UUIDs, e.g. `usr_…`, `inv_…`, `ws_…`. */
export function newId(prefix: string): string {
  return `${prefix}_${crypto.randomUUID()}`;
}
