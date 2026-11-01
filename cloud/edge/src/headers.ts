// The edge-to-container header contract (Spec 083, FR-011 / FR-008).
// Documented in full in cloud/edge/README.md.
//
// The container trusts ONLY these headers, and only because the edge
// sets them: the Worker deletes every client-supplied `X-Glossa-*`
// header before forwarding, so a value on a container-bound request is
// the edge's own assertion, never the client's.

export const HEADER_USER_ID = "X-Glossa-User-Id";
export const HEADER_USER_NAME = "X-Glossa-User-Name";
export const HEADER_GLOBAL_TYPE = "X-Glossa-Global-Type";
/** JSON object: { "<workspace_id>": "<role>", ... } */
export const HEADER_WORKSPACE_ROLES = "X-Glossa-Workspace-Roles";
/**
 * Per-deployment edge-to-container service credential. Its value comes
 * from the Worker secret SERVICE_CREDENTIAL — never from code or
 * config — and it is set on container-bound requests only.
 */
export const HEADER_SERVICE_CREDENTIAL = "X-Glossa-Service-Credential";

export const NOINDEX_HEADER = "X-Robots-Tag";
export const NOINDEX_VALUE = "noindex, nofollow";

/**
 * Stamp the noindex perimeter header (FR-007, C083-7) on a response.
 * Applied to EVERY response the Worker returns — pass-through, error,
 * redirect, and edge-generated alike — overwriting any value the
 * container may have set, so the perimeter cannot be weakened from
 * inside.
 */
export function withNoindex(response: Response): Response {
  const nullBodyStatus =
    response.status === 204 ||
    response.status === 205 ||
    response.status === 304;
  const out = new Response(nullBodyStatus ? null : response.body, response);
  out.headers.set(NOINDEX_HEADER, NOINDEX_VALUE);
  return out;
}
