// Session cookie reading + token hashing (Spec 083, FR-004).
//
// Sessions are opaque tokens of at least 256 bits (issued in Phase 2,
// T016). The edge never sees a session's plaintext beyond the presented
// cookie value: lookups are by SHA-256 hash, matching the `token_hash`
// column in D1, so a leaked identity database yields no usable session.

export const SESSION_COOKIE_NAME = "glossa_session";

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
