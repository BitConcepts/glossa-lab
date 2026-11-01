# Amendment 5 to Spec 083 — Host on the owner's desktop; Cloudflare Tunnel + Workers VPC route (owner, 2026-10-30)

**Status**: Adopted by the owner's decision of 2026-10-30. **Amendment 4
is superseded in full** — its Cloud Run service, Cloud Run Jobs, Google
Cloud Storage bundles, and Google Cloud go-live gate are retired, and
decision D-0's compute and bundle legs are superseded again (§3). Where
this amendment and any earlier text differ, **this amendment governs**.
Amendments 1–3 are unaffected: workspaces are the tenancy unit, there
is no staging, and the glassbreak seed record stands. No Cloudflare
Access is added at any point in this design.

## 1. The decision, in the owner's terms

The owner, later on 2026-10-30, changed the hosting plan again, in his
words: *"change plan, host on the desktop (Tristen-desktop) and route
to the cloudflare subdomain. but again, only allow members to log in
and use."*

So:

- **The application and its data live on TRISTEN-DESKTOP** — the
  Spec 080 production install, the same install the owner uses locally.
- **The public route is `glossa.bitconcepts.tech`**, served through
  Cloudflare.
- **Only members may log in and use it.** The application's own member
  login — the edge's accounts, invites, and sessions — is the gate.
  Cloudflare Access is **not** added; there is no second identity
  system in front of the app's own.

## 2. The topology, fact-checked against Cloudflare's documentation

The composition below is the supported one. It differs from the
natural first sketch — "publish the tunnel at the subdomain and put
the Worker in front" — in one load-bearing way, stated plainly in
§2.2: **the tunnel does not publish the hostname.** If it did, the
edge Worker would not be the public entry, and the session perimeter
would not be the thing standing in front of the desktop.

### 2.1 The route

```
member's browser
  -> glossa.bitconcepts.tech  (Worker Custom Domain — the edge Worker
     is the origin for the hostname; Cloudflare creates the DNS
     records and the certificate)
  -> edge Worker: robots/noindex perimeter, session termination
     against D1 (accounts, invites, sessions, workspace grants,
     audit), login wall
  -> Workers VPC Service binding fetch() — only after the session
     and route authorization checks pass (anonymous traffic reaches
     the origin only for the exact public surface: login, setup
     while open, invite acceptance, and the shell assets)
  -> named Cloudflare Tunnel "glossa-desktop" (cloudflared on
     TRISTEN-DESKTOP, outbound-only connections; no public origin
     IP, no inbound ports)
  -> http://127.0.0.1:8001 — the Spec 080 production Glossa backend
     on the desktop, which serves the built SPA and the API from
     the desktop-resident dataset
```

- **Public entry — Worker Custom Domain.** `glossa.bitconcepts.tech`
  is attached to the edge Worker as a Custom Domain (the Phase 1
  wrangler configuration already declares it this way). Cloudflare's
  Custom Domains documentation: a Custom Domain makes the Worker the
  origin for the hostname, and Cloudflare creates the DNS records and
  issues the certificate on the operator's behalf; the created DNS
  records point directly to the Worker.
  (https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)
- **Origin transport — Workers VPC Service over a named Tunnel.** A
  remotely managed Cloudflare Tunnel named **`glossa-desktop`** runs
  on TRISTEN-DESKTOP via `cloudflared`. Exactly one HTTP **VPC
  Service**, **`glossa-desktop-origin`**, is registered against it:
  type `http`, that tunnel's ID, host IPv4 **`127.0.0.1`**, HTTP port
  **`8001`**, and no HTTPS port (the last hop is loopback on the
  desktop; traffic is encrypted in flight until it reaches the
  desktop's network via the tunnel). The Worker binds the service as
  **`GLOSSA_ORIGIN`** through a `vpc_services` binding and calls the
  binding's `fetch()` for origin-bound requests. Workers VPC's own
  documentation describes exactly this pattern — "bind to a specific
  host and port in your private network" through Cloudflare Tunnel —
  and its private-API example is this shape end to end: create the
  tunnel, create the HTTP VPC Service, add the binding, call
  `fetch()`, and answer 503 when the private service is unavailable.
  (https://developers.cloudflare.com/workers-vpc/ ·
  https://developers.cloudflare.com/workers-vpc/configuration/vpc-services/ ·
  https://developers.cloudflare.com/workers-vpc/examples/private-api/)
- **The binding, not the URL, chooses the target.** Per the Workers
  VPC binding API, a VPC Service binding always routes to its
  pre-registered host and port; the host and port in the Worker's
  `fetch()` call do not control routing (the host only populates the
  Host header / SNI). The Worker therefore constructs an internal
  request preserving method, path, query, and body, and the
  registered service configuration is the only thing that can aim it
  at the desktop backend. There is no "tunnel hostname" origin URL
  anywhere in the design.
  (https://developers.cloudflare.com/workers-vpc/api/)
- **Identity crosses the hop exactly as claim C083-8 designs.** The
  edge terminates the user session, deletes every client-supplied
  `X-Glossa-*` header, and injects the authenticated identity plus
  the per-deployment edge-to-origin service credential onto the
  binding request. The desktop application accepts that identity
  only when the service credential validates (T056). The Spec 082
  per-install token is a separate, local credential: the edge refuses
  it in every position, and it never becomes a browser or public-edge
  credential.
- **The GlossaFront container role is retired from the request
  path.** Nothing in the production route starts, names, or proxies
  to a Cloudflare Container or a Cloud Run service. The edge's
  session/perimeter code and the D1 identity store are unchanged in
  role; only the origin pointer moves (T055).
- **Availability.** Tunnel is available on all Cloudflare plans and
  Workers VPC is available on Free and Paid Workers plans, per the
  products' own documentation pages — no paid plan is required by
  this topology. (https://developers.cloudflare.com/tunnel/ ·
  https://developers.cloudflare.com/workers-vpc/)
- **Desktop offline behavior.** When Workers VPC cannot establish
  the connection, the binding's `fetch()` throws (VPC Services
  documentation, above). The edge turns that — and a refused
  loopback connection from a stopped backend — into **its own 503
  response**: noindex, a plain "the host is offline" message, and no
  project data. There is no cached dataset at the edge to fall back
  to, because no cloud dataset exists (§4); project-data responses
  are not cached. When the desktop returns, the same resident state
  serves again — nothing was copied anywhere in the meantime.

### 2.2 What the tunnel does *not* do here (the DNS distinction)

Cloudflare Tunnel's ordinary published-application route maps a
public hostname to a local service; adding that route through the
dashboard automatically creates a **proxied CNAME to
`<UUID>.cfargotunnel.com`**, and the tunnel's routing documentation
notes that DNS and tunnel are independent (a stopped tunnel leaves
the record in place and visitors see error 1016).
(https://developers.cloudflare.com/tunnel/concepts/routing/)

That pattern is **not used** for `glossa.bitconcepts.tech`:

- There is **no `glossa` CNAME to `<UUID>.cfargotunnel.com`**.
- There is **no published application route** for
  `glossa.bitconcepts.tech` in the tunnel's configuration.
- The hostname's DNS is the Worker Custom Domain's, pointing at the
  Worker. The tunnel is reachable only as the VPC Service's private
  transport, callable only by the bound Worker.

This is what keeps the edge — sessions, login wall, noindex — in
front of the desktop by construction rather than by convention, and
it is falsifiable by configuration audit (C083-14, T059).

### 2.3 The tunnel credential

A remotely managed tunnel runs on a token; Cloudflare's tunnel-token
documentation is blunt that anyone with the token can run the
tunnel. The token is therefore a host credential: it lives only in
the `cloudflared` service configuration on TRISTEN-DESKTOP, never in
the repository, logs, chat, or the rollout record (which records the
Tunnel ID, never the token). Rotation follows the documented
procedure — rotate, reinstall the service with the new token,
force-disconnect old connections — and is part of the T053 checklist.
(https://developers.cloudflare.com/tunnel/reference/tunnel-tokens/)

## 3. What this supersedes

- **D-0's compute leg** now reads: origin = the owner's Spec 080
  production desktop install on TRISTEN-DESKTOP; public entry = the
  edge Worker at `glossa.bitconcepts.tech`; origin transport = the
  named Cloudflare Tunnel consumed through a Workers VPC Service
  binding. The edge and D1 identity legs of D-0 stand as built.
- **Amendment 4 is historical record only.** Cloud Run (service and
  Jobs), Artifact Registry deploys, Google Cloud Storage, dataset
  bundles, and the spend-cap budget are all retired from the design.
  **The Google Cloud account + billing go-live gate is dead** — no
  Google account, project, or billing act is required at any point.
- **The bundle/hydration machinery is retired from the design** (R2
  first, then GCS): no publisher, no manifest, no bundle store, no
  hydration. Phase 1's bundle code is not deleted by this amendment;
  it simply has no production role (T058).
- **D-4's reviewed-import premise is retired.** There are not two
  datasets to move work between: hosted members and the owner's local
  use are two doors into the one desktop dataset.
- **Step 4 of the plan (the data-boundary publisher) is retired**;
  tasks T030–T035 are superseded (§7), as are Amendment 4's delta
  tasks T044–T051.

## 4. The data boundary, restated honestly for this shape

- **No cloud dataset exists.** Project and research data are resident
  only on TRISTEN-DESKTOP, in the Spec 080 production install (its
  database and checkout file state). Nothing in this design copies
  them anywhere.
- **The edge stores identity data only**: accounts and their Argon2id
  password hashes, invite codes (hash only), sessions (hash only),
  workspace and workspace-access records, setup state, and the audit
  log — the D1 schema as built. Worker code, configuration, and
  secrets are not project data.
- **Restricted material (the CISI class: scans and their
  derivatives) is never copied** into D1, Worker storage, a bundle
  store, or any other cloud storage. It remains on the desktop under
  the program's existing custody restrictions, and it can be returned
  through the hosted route **only inside an authenticated,
  workspace-authorized member session, under the desktop
  application's existing restrictions**. The custody rule —
  statistics publishable, scans never redistributed — does not soften;
  this route changes where the application runs, not what a member is
  allowed to receive.
- Claim **C083-6 is restated** to say exactly this, with falsifiers
  that audit the cloud side and probe the route. Claim **C083-13 is
  superseded** (§6): dataset versioning and atomic hydration no longer
  exist to be claimed.

## 5. The hosted route's trust rules

- The member login is the only gate in front of the tool. Anonymous
  requests receive exactly the Amendment 2 surface — login, setup
  while open, invite acceptance, `robots.txt`, and the shell assets —
  and the edge does not call the desktop origin for project data
  before authentication.
- Identity headers are believed by the desktop application **only**
  on a request carrying the valid per-deployment service credential.
  A direct local request that forges `X-Glossa-*` headers without the
  credential is not a member request; local use continues under the
  Spec 082 token, unchanged.
- **Host-management surfaces are not reachable through the hosted
  route.** Environment setup/rebuild/upgrade and the shutdown
  endpoint are local-machine operations: edge-authenticated requests
  cannot invoke them, whatever the member's role. The terminal
  remains a global Admin/Owner facility (D-5). The owner's local
  desktop behavior is unchanged except for the edge-identity
  acceptance this route requires (T056).
- The desktop backend stays bound to loopback (127.0.0.1:8001). No
  inbound port is opened and no desktop address is published; the
  tunnel is outbound-only.

## 6. Claim deltas

- **C083-6 — RESTATED** (text, evidence, falsifiers): desktop
  residency and the cloud-storage exclusion of §4 replace the
  publish-pipeline boundary.
- **C083-8 — REVISED** (text, evidence, falsifiers): the credential
  hop is now edge → desktop origin through the Workers VPC binding
  and the named Tunnel; the desktop accepts edge identity only with
  the service credential; the Spec 082 token remains refused at the
  edge in every position.
- **C083-9 — evidence noun corrected only**: the hosted route serves
  the desktop install itself, so assessor identity is anchored in
  that install's pinned AEE version and adapter. Substance unchanged.
- **C083-10 — REVISED** (text, evidence, falsifier): the engine is
  resident again, in the desktop install; job durability is stated
  across ordinary desktop-backend restarts under the app's existing
  stall semantics. Cloud Run Jobs, scale-to-zero, journal export, and
  the scheduled cloud watchdog are retired.
- **C083-13 — SUPERSEDED** (status `superseded`, with the reason in
  its text): dataset versioning, bundle manifests, and atomic
  hydration are retired because no dataset moves. Its former
  dependent, C083-15, is re-anchored to the desktop dataset (below)
  and no longer depends on it. Step 5 checks C083-13 as a retirement
  audit — no production bundle path exists — and never executes its
  old hydration falsifiers.
- **C083-14 — REVISED** (text, evidence, falsifiers): production-only
  now means exactly one public hosted route (Worker Custom Domain →
  VPC Service → named Tunnel → desktop), no staging anywhere, no
  published Tunnel application or `cfargotunnel.com` CNAME for the
  hostname, and no second public origin or bypass.
- **Consequential venue-noun updates, substance unchanged**:
  C083-4 (project data is fetched from the desktop origin only after
  authentication; "hydration" wording removed), C083-5, C083-11, and
  C083-17 (the enforcing API is the desktop API, not a container API),
  C083-12 (dataset publishes leave the audit event list; hosted-route
  configuration changes join it), and C083-15 (the primary workspace's
  state assignment is verified in the desktop-resident dataset,
  replacing the first-publish mechanism).

## 7. Delta-task replacement map

Tasks T044–T051 are superseded and replaced by **T052–T060**
(tasks.md): T044 (Cloud Run image contract) and T047 (Jobs +
Scheduler) are superseded outright — the resident desktop application
needs neither; T045 (GCS adapter) is superseded by T058 (bundle
production path retired); T046 (Cloud Run service definition) is
replaced by T052–T054 (desktop service, Tunnel/VPC, Custom Domain);
T048 (edge retarget to `run.app`) is replaced by T055 (edge retarget
to the VPC Service binding); T049 (Google deploy workflow) is
superseded — the surviving deploy legs are the edge's own; T050
(Step 5 proof deltas) is replaced by T059; T051 (records) is replaced
by T060. Step 4's T030–T035 are superseded as recorded in tasks.md;
T034's substance (primary-workspace assignment) is replaced by T057.

## 8. Go-live gates

Go-live requires all three. Nothing else substitutes for any of them,
and the retired Google gate is not one of them.

1. **Spec 080 cutover-final first.** The hosted route rides the
   production desktop install. The route is not declared final
   against a pre-cutover or stale desktop stack.
2. **BitConcepts Cloudflare write/configuration scopes**, through the
   venue that owns that account and zone: DNS / Worker Custom Domain
   configuration; Workers and D1 deployment scopes; a Cloudflare
   Tunnel write scope (Tunnel Edit, or one of Cloudflare One
   Connectors Write / Connector: cloudflared Write / Tunnel Write);
   and the Workers VPC roles the documentation names —
   **Connectivity Directory Admin** to create and update the VPC
   Service, **Connectivity Directory Bind** to bind it to the Worker.
3. **The desktop service installation through Desktop Access.**
   `cloudflared` becomes a durable service on TRISTEN-DESKTOP through
   the venue's screened service path, under the sole-registrar regime
   for desktop task/service registration. This is a coordination step
   for the Desktop Access venue; the Glossa build does not install it
   directly.

## 9. What does not change

Accounts, invites, the glassbreak account and its setup prompt,
workspaces and the two-axis access model, the admin dashboard, the
noindex perimeter, the login wall, the production-only rollout, and
the owner's local desktop edition — all exactly as adopted. The only
things that moved are where the application and its data live (the
desktop, again), how the edge reaches them (Tunnel through Workers
VPC), and which gates open the launch.
