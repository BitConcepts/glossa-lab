# UI Contract — Spec 082 API Token (for the Spec 081 Phase 2 frontend build)

**Published**: 2026-10-29, with the Spec 082 spec PR — before the backend lands, so the
frontend build can implement against it in parallel.
**Server side**: `Authorization: Bearer <token>` is the only credential form the API
accepts. A missing/wrong token on any protected route returns `401` with JSON body
`{"detail": "API token required or invalid"}` and a `WWW-Authenticate: Bearer` header.
`GET /api/v1/health` is open and its payload includes `"auth": "token"` (enforcing)
or `"auth": "disabled"` (the named CI/dev switch) — the UI may surface this in its
Status screen's identity block.

## How the web UI obtains the token (the whole contract — keep it this simple)

1. **Tray handoff (primary path).** The tray's *Open Glossa Lab* menu item opens
   `http://localhost:<port>/#token=<install-token>`. The token is in the URL
   **fragment**: fragments are never sent to the server, never appear in server or
   proxy logs, and are not shared with any other origin.
2. **On load**, if `location.hash` carries `#token=…`, the SPA must, before any API
   call:
   - read the token once and store it in **`sessionStorage`** under the key
     `glossa_api_token` (sessionStorage, not localStorage: it dies with the tab,
     which matches the single-operator session model);
   - strip the fragment from the address bar with `history.replaceState` (so the
     token does not persist in browser history or get bookmarked/shared by accident).
3. **Every API call** sends `Authorization: Bearer <token from sessionStorage>`.
   This includes streaming endpoints: use fetch-based streaming with the header.
   **Never** put the token in a query string (query strings are logged) and never
   use `EventSource` for authenticated streams (it cannot set headers).
4. **Manual paste (secondary path, for direct browser access).** The Settings
   screen carries an *API token* field where the operator can paste a token
   (obtained via the tray's *Copy API Token* menu item). Pasting stores it in the
   same `sessionStorage` key. The field and every other surface show token state
   as **present/absent plus a fingerprint** — the first 8 hex characters of the
   token's SHA-256 — and **never the token value itself**, not even masked with a
   reveal toggle: the tray is the token's display surface, the UI is not.
5. **On any `401`**: clear the stored token, and show the named empty state —
   "API token needed" — with the paste field offered. Do not retry-loop, do not
   silently render an empty app (an unauthenticated app that looks merely empty
   is the failure shape this spec exists to remove).

## What the backend guarantees in return

- The header is accepted on every protected route and method, including SSE
  streams, with no additional handshake.
- CORS (dev mode) already allows the `Authorization` header from the dev origins;
  the served SPA is same-origin and needs no CORS at all.
- Health stays open, so the service chip / status surfaces can render identity
  (including the `auth` mode word) before any token exists.

## Dev / CI note

Until this contract is implemented in the SPA, CI's frontend-tests job runs its
throwaway backend with the named switch `GLOSSA_API_AUTH=off` (health reports
`auth: disabled`, startup logs the warning). Local dev may do the same, or set
`GLOSSA_API_TOKEN` and seed `sessionStorage` manually. Removing the CI switch is
Spec 082 task T010, owned by the Phase 2 landing.

## Addendum — the routed fragment form (2026-10-30, Spec 081 step 8)

The tray gained a second door in Spec 081 step 8 (wireframe 15):
"View status & session log" opens the web Status screen directly.
A URL fragment can carry only one value, so the tray's status
door uses the routed form `#/status#token=<value>`: the route
first, the token segment after it. The SPA's intake accepts both
shapes — it finds the `#token=` segment wherever it sits in the
fragment, stores the token, and strips ONLY the token segment
(the route survives in the address bar). The bare form
(`#token=<value>`, the tray's Open action) is unchanged, as is
everything else in this contract: query-string tokens remain
refused, and the token still never reaches the server.
