// Session cookie reading + token hashing (Spec 083, FR-004).
//
// Sessions are opaque tokens of at least 256 bits (issued in Phase 2,
// T016). The edge never sees a session's plaintext beyond the presented
// cookie value: lookups are by SHA-256 hash, matching the `token_hash`
// column in D1, so a leaked identity database yields no usable session.

export const SESSION_COOKIE_NAME = "glossa_session";

/** Sliding session lifetime: 30 days from last activity (D-3, T016). */
export const SESSION_TTL_MS = 30 * 24 * 60 * 60 * 1000;

export function sessionExpiryIso(from: Date): string {
  return new Date(from.getTime() + SESSION_TTL_MS).toISOString();
}

/**
 * The session cookie, per the Phase 1 conventions (FR-004):
 * HttpOnly; Secure; SameSite=Lax, path-wide, 30-day Max-Age matching
 * the sliding server-side expiry.
 */
export function sessionCookieHeader(token: string): string {
  const maxAgeSeconds = Math.floor(SESSION_TTL_MS / 1000);
  return `${SESSION_COOKIE_NAME}=${token}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAgeSeconds}`;
}

/** Clear the session cookie (logout). */
export function clearedSessionCookieHeader(): string {
  return `${SESSION_COOKIE_NAME}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0`;
}

/**
 * Extract the session token from the request's Cookie header.
 * Returns null when the cookie is absent or empty. No other credential
 * position is read: the Spec 082 install token is not a cloud
 * credential in any position (FR-008), and an Authorization header is
 * never treated as a session.
 */
export function readSessionCookie(request: Request): string | null {
  const header = request.headers.get("Cookie");
  if (!header) return null;
  for (const part of header.split(";")) {
    const eq = part.indexOf("=");
    if (eq === -1) continue;
    if (part.slice(0, eq).trim() === SESSION_COOKIE_NAME) {
      const value = part.slice(eq + 1).trim();
      return value.length > 0 ? value : null;
    }
  }
  return null;
}

/** SHA-256 of a string, lowercase hex (the D1 hash-at-rest form). */
export async function sha256Hex(value: string): Promise<string> {
  const digest = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(value),
  );
  return [...new Uint8Array(digest)]
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}
