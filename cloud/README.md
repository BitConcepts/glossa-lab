# Glossa Lab — cloud edition (Spec 083)

The cloud edition's deployment artifacts live here and in
`.github/workflows/deploy-cloud.yml`:

| Piece | Where | What it is |
|---|---|---|
| Edge Worker + Durable Object | `edge/` | The perimeter: session termination, the login wall, the noindex header on every response, routing through the single `GlossaFront` instance to the container. See `edge/README.md` for the header contract. |
| Identity schema | `edge/migrations/` | D1 migrations for `glossa-identity` (users, invites, sessions, workspaces, workspace_roles, audit_log, setup_state). Hash-only secrets; the audit log is append-only by trigger, not by convention. |
| Wrangler config | `edge/wrangler.toml` | Production only (Amendment 2): one Worker, one custom domain (`glossa.bitconcepts.tech`), one container instance. |
| Deploy workflow | `.github/workflows/deploy-cloud.yml` | Manual or `cloud-*` tag: gates on the Cloudflare secrets, applies D1 migrations, builds + pushes the container image, `wrangler deploy`. Fails closed until the account gate clears. |
| Local production-shaped build | `docker-compose.yml` | The verification fixture below. It is not a deployment. |

## The local production-shaped build

Amendment 2 puts all pre-launch verification in two places: this local
build and ephemeral preview deployments. The compose file reproduces
the production topology on one machine — the real edge Worker under
`wrangler dev` (local D1/R2 persistence stand-ins, same bindings, same
migrations) in front of the real container image built from the
repository-root Dockerfile with `GLOSSA_CLOUD=1`:

```sh
docker compose -f cloud/docker-compose.yml build
docker compose -f cloud/docker-compose.yml up
# once, to create the local identity schema:
docker compose -f cloud/docker-compose.yml exec edge \
  npx wrangler d1 migrations apply glossa-identity --local
```

The edge answers at `http://localhost:8787`. The app service's port is
published on localhost only for image smoke checks (T008's AEE pin +
regression run); every application-level proof goes through the edge,
mirroring production, where the container is reachable only through
the Durable Object.

## How the Step 3 / Step 5 proofs run against it

- **Step 3 (frontend verification):** Playwright drives the build
  through `http://localhost:8787` — the login wall, invite, setup, and
  admin screens are exercised exactly as a browser meets them in
  production, screenshots compared against the approved wireframes at
  desktop 1440 and mobile 390.
- **Step 5 (pre-launch proof battery):** the acceptance script
  (Stories 1–5 as amended), the C083-1…19 falsifier suites, the
  adversarial pass, and the noindex checks all target
  `http://localhost:8787` on this build first, then an ephemeral
  preview deployment (`wrangler deploy --name glossa-edge-preview-<suffix>`
  from `edge/`, torn down after the run). Anonymous-surface checks are
  meaningful here precisely because the topology matches: edge in
  front, container behind the Durable Object, identity in (local) D1.
- Production go-live follows those proofs directly (plan Step 5); the
  deploy workflow above is the only path to production.
