# T053 — Tunnel + VPC Service configuration checklist (Amendment 5)

**Status: BLOCKED at gate 2 (Cloudflare scopes), 2026-11-05.** Every
repo-side and read-side step that does not need the missing scopes is
done; the Cloudflare-side creation steps below wait on the token
scope extension named in §1. This checklist is the configuration
record T053 requires: it is executed top to bottom once the scopes
land, and its two ID slots are filled in at that time (IDs are
recorded; the tunnel token is NEVER recorded anywhere).

Topology being configured (Amendment 5, §2): the named tunnel
`glossa-desktop` runs on TRISTEN-DESKTOP via cloudflared (T052,
installed by the Desktop Access chat as a windowless persistent
service) and forwards to the desktop install at **127.0.0.1:8001**
(HTTP). The Workers VPC Service `glossa-desktop-origin` binds that
tunnel as its network; the edge Worker binds the service as
`GLOSSA_ORIGIN`. The tunnel publishes **no** hostname and **no**
application route.

## 1. Gate 2 — the exact missing scopes (measured 2026-11-05)

Probed read-only against the BitConcepts Cloudflare account
(`2df9ae83aa3913feaeec0fd96cbf3614`, zone `bitconcepts.tech`
`167534fd53e0f7a88f20211d60045f32`) with the stored BitConcepts Ops
account token (id `1682058e702cc76acb831aa3e280f9be`, verified
active). The token HAS D1 Read/Write, Pages, Zero Trust, and more —
the gaps are exactly these four:

| # | Missing scope | API evidence (2026-11-05) | Blocks |
|---|---|---|---|
| 1 | Workers Scripts Read/Write (account) — no Workers permission group in any policy | `GET /accounts/{acct}/workers/domains` → 403 (code 10000); `GET /accounts/{acct}/workers/subdomain` → 403 (10000); `GET /zones/{zone}/workers/routes` → 403 | T054 domain verification; T055 deploy (the edge Worker cannot be deployed, and its Custom Domain state cannot even be read, with this token) |
| 2 | DNS Read/Write (zone) — zone policy is Zone Read + Dynamic URL Redirects only | `GET /zones/{zone}/dns_records?name=glossa.bitconcepts.tech` → 403 (code 10000) | T054's DNS verification leg |
| 3 | Tunnel write (Cloudflare Tunnel Write / Cloudflare One Connectors Write) | `GET /accounts/{acct}/cfd_tunnel` → 200 with **zero** tunnels: `glossa-desktop` does not exist and cannot be created with this token | T053 tunnel creation + the token staging in §3 |
| 4 | Connectivity Directory Admin + Bind (+ Read) | `GET /accounts/{acct}/connectivity/directory/services` → 403 (code 10000) | T053 VPC Service registration (`glossa-desktop-origin`); per Cloudflare's workers-sdk issue #11884, deploying a Worker with `vpc_services` bindings also requires Connectivity Directory Read + Bind on the deploying token |

**Owner act that clears gate 2:** extend the BitConcepts Ops token
(or mint a deployment token) with — account: Workers Scripts Write +
Read, a Tunnel write scope, Connectivity Directory Admin + Bind
(+ Read); zone `bitconcepts.tech`: DNS Write. Nothing else is
missing: the D1 leg is already discharged (§2, step 0).

## 2. Configuration steps (execute in order once §1 lands)

0. **D1 (DONE 2026-11-05).** Database `glossa-identity` created via
   API; id `5de6e49e-bc67-4eaf-94da-728ae9b1d8a7` committed in
   `cloud/edge/wrangler.toml`. Migrations are NOT hand-applied: the
   deploy workflow applies them (`wrangler d1 migrations apply
   --remote`) so wrangler's migration bookkeeping stays true.
1. **Create the tunnel** (Workers → Tunnel/Connectivity Directory, or
   `POST /accounts/{acct}/cfd_tunnel` with `{"name": "glossa-desktop",
   "config_src": "cloudflare"}` — a remotely-managed tunnel, so its
   ingress is configured centrally, never by a desktop config file).
   Record the returned Tunnel ID in §5.
2. **Set the tunnel ingress** to exactly one rule: hostname-less
   (catch-all) service `http://127.0.0.1:8001` — a Workers VPC
   tunnel's privately-routable target — plus the mandatory final
   `http_status:404` catch-all. **No published application route**
   (Public Hostname) is created, and **no DNS record** of any type
   points at `<Tunnel ID>.cfargotunnel.com` (asserted in §4).
3. **Stage the tunnel token for the desktop** (§3) — the token is
   issued at tunnel creation; Desktop Access's launcher consumes it.
4. **Register the VPC Service**: Connectivity Directory →
   `POST /accounts/{acct}/connectivity/directory/services` with
   `{"name": "glossa-desktop-origin", "type": "tunnel",
   "host": {"type": "ipv4", "ipv4": "127.0.0.1"}, "http_port": 8001,
   "service_id"/tunnel reference per the API's tunnel-service shape}`.
   Record the returned VPC Service ID in §5.
5. **Fill `cloud/edge/wrangler.toml`**: replace the all-zeros
   placeholder in the `[[vpc_services]]` block with the VPC Service
   ID (a config value, not a secret; committed through the normal PR
   path). The deploy workflow refuses to run while the placeholder
   stands.
6. **Set the edge secret**: `wrangler secret put SERVICE_CREDENTIAL`
   with an operator-generated value; the SAME value is provisioned
   into the desktop install's protected credential storage
   (`.keys.json` key `glossa_service_credential`, via the desktop's
   own settings surface — T056/T024). Neither copy is ever committed
   or recorded.
7. **Custom Domain**: `glossa.bitconcepts.tech` is a Worker Custom
   Domain on `glossa-edge` (Amendment 5) — confirm/attach it at
   deploy (`wrangler deploy` with the `[[routes]]` custom_domain
   entry does this); Cloudflare creates the proxied DNS record
   itself. If the name currently carries any other record, remove it
   first (DNS Write, §1 row 2). Verify per §4.
8. **Deploy** via `.github/workflows/deploy-cloud.yml`
   (workflow_dispatch) in the go-live sequence (T060), then run the
   T059 proofs against the real route.

## 3. Tunnel token staging (gatekeeper grab pattern)

The tunnel token lives ONLY in the desktop's service configuration
(Amendment 5 record). Route, mirroring the Arcturus tunnel-secret
staging:

1. At tunnel creation (§2 step 1), write the token to a one-shot
   file in the gatekeeper's grab staging area on this VM — never to
   the repo, a record, a PR, or a chat message.
2. Submit a gatekeeper grab job (explicit `--cwd`, windowless) that
   carries the file to the desktop.
3. The Desktop Access chat places the file's content at the
   `GlossaCloudflared` launcher's token path
   (`C:\Users\trist\Development\Syncyard\services\cloudflared`,
   installed under their T052 leg) and deletes the staged copies on
   both ends.
4. The tunnel then connects with no further install work (their
   launcher is persistent and self-restarting).
5. Verify from records only: tunnel status reads `healthy`/connected
   in the Connectivity Directory; the token value appears in NO
   record at any step.

## 4. Negative assertions (verify after §2, record results in T060)

- [ ] Tunnel has NO published application route (no Public Hostname entries).
- [ ] NO DNS record named `glossa` (or any name) is a CNAME to `<Tunnel ID>.cfargotunnel.com`.
- [ ] `glossa.bitconcepts.tech` resolves as the Worker's Custom Domain (proxied), served by `glossa-edge`.
- [ ] The desktop origin answers ONLY through the tunnel: the desktop backend's port is not publicly reachable (no other ingress exists — the tunnel is the sole route; no Cloudflare Access application fronts it either, per Amendment 5).
- [ ] Edge behavior with the desktop down answers the edge's own noindex 503 (T059 proof P7 runs this against the real route).

## 5. Recorded IDs (fill at creation; IDs are not secrets)

- Tunnel name: `glossa-desktop`
- Tunnel ID: _(pending gate 2 — §1 row 3)_
- VPC Service name: `glossa-desktop-origin`
- VPC Service ID: _(pending gate 2 — §1 row 4)_
- Custom Domain: `glossa.bitconcepts.tech` → Worker `glossa-edge` (state not readable until §1 row 1 lands)
- Desktop install revision: cloudflared 2026.10.7, sha256-pinned, `GlossaCloudflared` logon task (Desktop Access chat, T052 — their completion record governs)
- D1 database: `glossa-identity` = `5de6e49e-bc67-4eaf-94da-728ae9b1d8a7` (created 2026-11-05)

## 6. Token rotation (spec §2.3 — standing procedure)

1. Rotate the tunnel's token in the Connectivity Directory
   (regenerate the tunnel token).
2. Re-stage the new token exactly as §3 and reinstall/restart the
   desktop's `GlossaCloudflared` service with it.
3. Force-disconnect the old token's connectors
   (`DELETE /accounts/{acct}/cfd_tunnel/{id}/connections`) so no
   connector running the old token remains.
4. Confirm the tunnel reads healthy on the new token; record the
   rotation date here (never the token).
