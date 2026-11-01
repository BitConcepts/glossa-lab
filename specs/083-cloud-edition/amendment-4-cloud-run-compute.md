# Amendment 4 to Spec 083 — Compute moves to Google Cloud Run; bundles to Google Cloud Storage (owner, 2026-10-30)

**Status**: Adopted by the owner's decision of 2026-10-30. When the
coordinator put the cost question to the owner ("how to get around
needing a paid plan?"), the owner picked the swap recorded here:
**Cloud Run's free tier replaces Cloudflare Containers**. Supersedes
the compute and bundle legs of decision D-0 and every Containers / R2
reference they govern, in the base spec, plan.md, tasks.md and claims
C083-10, C083-13 and C083-14. Where this amendment and the earlier text
differ, **this amendment governs**. Amendments 1–3 are unaffected;
Amendment 2's production-only rollout is unchanged and now binds the
Google side as well (no staging service, job, or bucket either).

## 1. The decision

D-0 chose Cloudflare Containers because they run the existing app
unmodified — but Containers require the **Workers Paid plan** ($5/month
minimum), and the owner declines a paid plan for this deployment. The
compute therefore moves to Google's platform, whose free tier covers
this tool's shape (§3):

- **The app runs as a Google Cloud Run service** — the same image the
  Phase 1 Dockerfile already builds — in region **us-central1**,
  request-based billing, **maximum instances 1**, minimum instances 0.
- **The engine and the pipelines run as Cloud Run Jobs**: executions of
  the same image with a runner entrypoint, dispatched on job submission
  and by Cloud Scheduler for the periodic set (§2, items 2–4).
- **Dataset bundles live in Google Cloud Storage** — one bucket,
  us-central1, same Google account and project as the service —
  replacing R2. The Phase 1 bundle discipline (manifest, per-artifact
  SHA-256, verify-then-atomic-swap, never a mixture) is unchanged; only
  the transport changes: the bundle library gains a GCS adapter beside
  its R2 plumbing (delta task T045), and the publisher's upload target
  in Step 4 becomes the bucket. R2 is never enabled; nothing migrates,
  because no bundle has ever been published (Step 4 has not run).
- **The edge does not move.** The Cloudflare Worker, the GlossaFront
  Durable Object, the Pages shell and the D1 identity store stay
  exactly as designed and built. They never required the paid plan —
  the paid requirement came only from Containers (and from R2's
  enablement on this account, verified absent 2026-10-30).
- **Deploys**: GitHub Actions builds the image, pushes it to Artifact
  Registry, deploys the service and updates the Job definitions; the
  edge still deploys by wrangler and D1 migrations still run from the
  same workflow, with the fail-closed property kept — any leg failing
  deploys nothing.
- **DNS does not move**: `glossa.bitconcepts.tech` stays on Cloudflare
  (§4).

## 2. The fit-check

The route study's backend inventory (architecture-route-study.md §2)
tested against Cloud Run's documented model. Platform facts are quoted
from Google's official Cloud Run documentation, read 2026-10-30
(quotas; container contract; billing settings; pricing; free tier).

> **THE ONE FINDING IN RED: the resident in-process engine does not
> fit Cloud Run's service model at all — not degraded, absent.** Under
> request-based billing, "CPU is only allocated during request
> processing" (billing-settings doc); an idle instance "won't be kept
> idle for longer than 15 minutes" (container contract); and no
> service setting makes an instance resident except minimum instances,
> whose idle time is billed at the published idle rates ($0.0000025
> per vCPU-second + $0.0000025 per GiB-second) — ≈ **$32/month** at
> this app's size (1 vCPU / 4 GiB), roughly six times the $5 plan this
> swap exists to avoid. **If the program required the engine to stay
> resident in the web process, this route would fail.** It does not:
> the engine's work is draining a job queue, which is exactly what
> Cloud Run Jobs execute (item 2). With that one re-shape — and only
> with it — every inventoried behavior fits. No other load-bearing
> behavior fails to fit, with or without adaptation.

| # | Backend behavior (route study §2) | Cloud Run fact (docs, 2026-10-30) | Verdict / smallest adaptation |
|---|---|---|---|
| 1 | Interactive API, ~320 routes, FastAPI/uvicorn | A service is a real Linux container listening on the injected `$PORT`; ceilings are 8 vCPU / 32 GiB per instance | **Fits.** The image must honor `$PORT` (today's Dockerfile fixes 8001; delta T044) |
| 2 | In-process engine loop draining the jobs table (~30 pipelines behind it) | CPU only while requests process (request-based billing); idle instances die within 15 minutes; instance-based billing lengthens CPU allocation but an instance still "will never stay idle for more than 15 minutes … unless it is kept active using minimum instances" | **Does not fit as-is.** Job submission dispatches a **Cloud Run Job execution** (same image, runner entrypoint: hydrate → drain the queued job rows → export → exit); the service keeps a dispatcher, not an engine. The `GLOSSA_CLOUD` switch grows an engine-mode gate beside its existing host-local gates; the desktop edition is untouched |
| 3 | Pipelines that "can run for hours" (an SA node) | Job task timeout: default 10 minutes, maximum **168 hours (7 days)**; no cap on a whole execution's span | **Fits**, inside Jobs. The 1-hour cap on GPU tasks is irrelevant: GPU pipelines already run their CPU fallback in this edition |
| 4 | Schedulers: discovery, study loop, provider probes, model-intel sync, RAG index build, foundation auto-check | Same residency facts as item 2 — resident timers get no CPU between requests | **Do not fit as resident timers.** Each periodic behavior becomes a Scheduler-triggered Job execution; provider probes become lazy/on-request. Cloud Scheduler itself: 3 jobs free per billing account, then $0.10 per job per month — recorded so the periodic set's true price is on paper |
| 5 | SSE streaming throughout (events, AI chat, runs, loops, terminal); no WebSocket endpoints anywhere in the app | Streaming responses are supported, but **every request still ends at the request timeout: 60 minutes maximum** (3,600 s) | **Fits with a ceiling.** Streams are views, not state: job/loop progress is read from job records (written by Job executions into the dataset), and the app's fetch-streaming surfaces already reconnect. Nothing load-bearing may live inside a single stream. Terminal sessions are best-effort resident: an active session's traffic keeps its instance alive; an idle terminal dies with its instance — the terminal operates on the hydrated working copy, which is never the only copy of anything |
| 6 | Subprocesses: paper-search MCP stdio client; the terminal's OS-command fallback | A service/job is a real container process environment — the property whose absence disqualified Python Workers in the route study | **Fits.** The stdio server spawns per use inside the service instance or the Job, as applicable. `ollama serve` remains excluded (not bundled), as specced |
| 7 | File state everywhere: one SQLite file + checkout JSON + corpora (~50 MB publishable); 265 modules touch the filesystem | The writable filesystem "is an in-memory file system, so writing to it uses the instance's memory" and "data written to the file system doesn't persist when the instance stops"; shutdown is **SIGTERM, then 10 seconds before SIGKILL** | **Fits the bundle discipline, with the export trigger changed.** Instance memory must cover the RAM-backed dataset (size the service at 4 GiB — two orders of magnitude of headroom today). Orderly-stop export is demoted: 10 seconds flushes only the small state journal. Primary discipline: export on cadence, on job completion, and incrementally (journal) — C083-10 / FR-010 restated accordingly |
| 8 | Single-process design; the spec's single-instance assumption | Autoscaling is configurable: concurrency up to 1,000 per instance (default 80); maximum instances is a service setting | **Fits by configuration:** maximum instances = 1. The Durable Object's single-backend serialization now fronts a single-instance service; the platform, not the Object, owns instance lifecycle (the spec's "the Durable Object starts it if stopped" clause is superseded by item 9) |
| 9 | Always-on local process (desktop heritage) vs. scale-to-zero | Instances scale to zero after ≤15 idle minutes; the next request pays container start (4-minute startup budget; startup CPU boost exists) + the 425-module import + dataset hydration from GCS | **Accepted, with eyes open.** The edge's hold-and-wake pattern carries over from the container-sleep design (it now waits on platform start + hydration instead of starting a named instance); the Status surface states cold start honestly, as it already did for container sleep. Minimum instances stay 0 — see the red finding for what 1 would cost |
| 10 | Engine resource gating on live psutil readings (CPU/RAM/VRAM) | Job CPU/memory are configuration; a container sees its own cgroup envelope | **Degrades gracefully.** Gating moves with the engine into Job executions, where the configured envelope *is* the resource budget; VRAM reads "no GPU," which is already this edition's CPU-fallback path. No claim depends on the readings themselves |
| 11 | Uploads (evidence documents, sign images) | HTTP/1 request ceiling 32 MiB | **Fits.** The app's uploads sit far under it |

## 3. Free-tier arithmetic (pricing + free-tier docs, read 2026-10-30)

- **A billing account is required to access the Free Tier at all** —
  Google's free-tier page says so in those words. That requirement is
  the new go-live gate (§5).
- **Services** (request-based): the first **180,000 vCPU-seconds +
  360,000 GiB-seconds + 2M requests** per month, per billing account,
  applied as a spending-based discount priced at Tier 1. us-central1
  is a Tier 1 region (the free allotments are priced on us-central1
  rates) — one reason for the region choice. At 2 vCPU, the compute
  allotment is ~25 instance-hours of active request processing a
  month — ample for an invite-only tool.
- **Jobs**: a **separate pool** — the first **240,000 vCPU-seconds +
  450,000 GiB-seconds** per month. Pipeline compute draws here, not
  against the service pool. A gauge, stated plainly: one 2-vCPU
  pipeline running ten hours consumes 72,000 vCPU-seconds — about a
  third of the month's free job pool. A heavy pipeline month *can*
  exhaust it.
- **Cloud Storage** (Always Free, us-central1 among the listed
  regions): 5 GB-months of regional storage + 5,000 Class A + 50,000
  Class B operations monthly. The ~50 MB bundle set sits two orders of
  magnitude under the storage line.
- **Past the allotments**, usage bills at the published per-second
  rates — the free tier is an **allotment, not a cap**. The deploy
  checklist therefore includes a **Cloud Billing budget with a spend
  cap**, which Google documents as pausing Cloud Run workloads when
  hit (services answer 5xx; new job tasks fail): the free-tier intent
  enforced by the platform rather than by vigilance. If the cap ever
  trips, the Status surface says so plainly — a paused tool, never a
  silent bill.

## 4. DNS and the public surface — why there is no domain mapping

Cloud Run serves a custom domain only through a **domain mapping**
(CNAME to `ghs.googlehosted.com`, the record necessarily DNS-only) or
behind a Google load balancer. Either takes the hostname's traffic
*out of* the Cloudflare edge — and the edge is where sessions
terminate and where the noindex header is set on every response
(C083-7's falsifier is an edge-header check). So the hostname stays on
Cloudflare exactly as built, and the Worker fetches the service at its
stable `*.run.app` URL as its **origin**. The run.app URL is an origin,
not a public surface: the service refuses any request that does not
arrive through the edge carrying the injected identity and the
per-deployment service credential (C083-8 — the Phase 2 design already
gates this hop for exactly this reason), so a direct hit on the origin
meets the same wall as the front door. Restricting the service by
Google IAM invoker is recorded as an **available later hardening, not
a claim requirement**: a Worker cannot present Google credentials
without holding a service-account key, and where such a key may live
is a coordinator decision for a later step, not this amendment's.

## 5. The new go-live gate (replaces plan Step 5(e)'s gate)

- **Owner act, at deploy time only: a Google Cloud account + project
  with billing enabled** (the Free Tier requires an active billing
  account), with the §3 spend-cap budget set as part of the first real
  deploy. **Nothing in Steps 1–4 may require it earlier**: the service
  and Job definitions, the GCS adapter, and the retargeted workflow
  are all buildable and testable without the account (the adapter
  tests against a local stand-in, exactly as Phase 1's R2 plumbing
  did).
- The Cloudflare half of the old gate **shrinks but survives**: the
  BitConcepts Ops token's write scopes (Workers/D1 deploys, the DNS
  record) still need confirming or minting at the same gate, through
  the venue that owns that zone. The old gate's paid items are **dead**:
  no Workers Paid plan, no R2 enablement, no container registry.

## 6. Claim and requirement deltas

- **C083-10 — REVISED** (text, evidence, falsifier): job durability
  moves from container-instance restarts to the Jobs model — pipelines
  execute as Cloud Run Job executions; state is journaled to the
  bundle store on cadence and at completion; a scheduled stall-watchdog
  pass fails heartbeat-less executions with the reason recorded; the
  SIGTERM handler flushes the journal inside the 10-second grace. The
  claim's semantics are unchanged: terminal state reached, stalls
  detected and reasoned, no job lost silently.
- **C083-13 — evidence venue updated**: bundles are stored in Google
  Cloud Storage. The mechanism (manifest, hash-verify, atomic swap,
  never a mixture) is identical.
- **C083-14 — falsifier venue extended**: "no staging environment"
  now enumerates both platforms — no staging Cloudflare project,
  database or bucket, and no second Cloud Run service, job, or storage
  bucket. (FR-014's own text is venue-neutral and needs no edit; only
  the falsifier's enumeration named one platform.)
- **C083-8 — evidence noun updated**: the service-credential hop is
  now edge → Cloud Run service. The mechanism — credential only in
  platform secret stores, identity injected by the edge, the Spec 082
  token refused at the edge — is identical.
- **C083-6, C083-7, C083-9 — unchanged in substance.** C083-9's "cloud
  image" is the same Dockerfile output, now deployed to Cloud Run (the
  AEE-pin image smoke is untouched). C083-6's publisher target becomes
  the GCS bucket; its planted-canary falsifier does not change.
  C083-7 remains an edge-header property, which is why §4 keeps the
  hostname on the edge.
- **FR-010 revised** in spec.md (execution model + export discipline,
  as C083-10). The spec's Status line, route paragraph, design-summary
  bullets, User Story 5 acceptance wording, single-instance assumption
  and confidence note carry Amendment 4 pointers; decisions-for-owner
  D-0 carries the SUPERSEDED note (its edge and identity legs stand).
- **Delta tasks T044–T051** (tasks.md) carry the build consequences
  for the Phase 3+ coordinator; the Phase 1 delta is summarized in the
  amendment worker's report.

## 7. What does not change

Identity, invites, the glassbreak account and its setup prompt,
workspaces and the two-axis access model, the admin dashboard, the
noindex perimeter, the login wall, the data boundary and its canary,
the production-only rollout, and the desktop edition — all exactly as
adopted. The only things that moved are where the compute runs, where
the bundles sit, and which owner's account act opens the gate.
