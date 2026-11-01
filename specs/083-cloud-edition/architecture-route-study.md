# Spec 083 — Architecture Route Study: the full working tool, hosted in the cloud

**Date:** 2026-10-30 · **Phase 1 (design only — no build)** · **Status:** for owner approval
**Order being answered:** the owner, 2026-10-30 — Glossa Lab gets a BitConcepts
subdomain (`glossa.bitconcepts.tech`), hosted the way his other properties are
hosted (GitHub as source, Cloudflare as host, staging → production), **not**
hosted from his desktop; the **full working tool** for invited users, with user
accounts, an admin dashboard, himself as the `glassbreak` admin, and invite
codes; and **robots kept away** (no search indexing) until he says otherwise.

**How this study was made.** The backend's constraints were inventoried from the
code at `main` `124a1ac3` (module, dependency, storage, and background-work
evidence in §1). Every platform figure in §2 was read from Cloudflare's official
documentation on 2026-10-30; the load-bearing lines are quoted with their page.
§3 scores the candidate routes on that evidence. §4 is the recommendation and
§5 records the losers' disqualifiers plainly.

---

## 1. What the backend actually is (evidence)

Glossa Lab's backend is not a small API in front of a database. It is a
research workbench that happens to speak HTTP:

| Dimension | Evidence from the code |
|---|---|
| Size | 425 Python modules, **147,360 lines** in `backend/glossa_lab/`; ~57 routers; **320 route decorators**; 42 frontend components |
| Framework | FastAPI app factory (`glossa_lab/main.py`), uvicorn, served same-origin with the built SPA (`frontend/dist`, 1.1 MB) |
| Assessor | `applied-epistemic-engineering` **≥1.5.0,<1.6** — a pure-Python library; `glossa_lab/aee_core.py` is the single adapter (claims JSON → claim graph → scoring engine). The version is load-bearing: under AEE 1.0.4 vs 1.5.x, 16 of 23 regression claims scored differently (0.0 vs 0.1625 — the GAP-ENV finding). Any route that changes the assessor changes the program's verdicts. |
| Numeric/native deps | **numpy** (core), **matplotlib**, **reportlab**, **psutil** (core); optional cupy (GPU), pymupdf/pdfplumber/pytesseract (OCR), Pillow |
| Relational state | One SQLite file (aiosqlite; `database.py` is 3,019 lines) in the install data dir: ~27 tables (jobs, studies, hypotheses, notebooks, citations, anchor_sets, projects, discovery, providers, model scores, signs, …). Production snapshot: 6.9 MB |
| File state | **There is no claims table.** Claims of record are JSON files in the repo checkout (`glossa-indus/claims/…`). API code also writes phase-state, dismissals, settings, foundation config/anchors/reports, research-loop staging/archive JSONs, a RAG TF-IDF index cache, sign images, and user uploads. **265 modules reference `open(`/`Path(`** — the filesystem is a load-bearing part of the architecture. Corpora on disk: 42 MB (`glossa-corpus`) + 4.6 MB (`glossa-indus`) |
| Background work | An in-process engine loop polls the jobs table and runs ~30 pipeline modules (decipherment, beam search, simulated annealing, graph experiments, study loop, research loop); resource-gated on live CPU/RAM/VRAM readings; jobs are expected to run long — the engine's own comment: *"an SA node can run for hours."* Plus schedulers (discovery, study loop), provider probes, model-intelligence sync, RAG index build, foundation auto-check |
| Processes | The backend **spawns subprocesses**: `ollama serve` at startup when installed, the terminal's OS-command fallback, the paper-search MCP stdio client. The terminal (`GlossaShell`, sandboxed to the repo root) is a shell over the host by design |
| Streaming | SSE throughout (events, AI chat, experiment runs, loops, terminal) via fetch-streaming; no WebSocket endpoints |
| Host-local surfaces | Terminal, environment setup/rebuild/upgrade (pip installs on the host), shutdown, psutil system metrics, Ollama management, the tray, the stdio MCP server |
| Auth today | Spec 082: one per-install bearer token in middleware; open routes are health, the SPA bundle, and published sign glyphs. No accounts, no sessions — by deliberate design for a single-operator local tool |
| Restricted material | CISI-class scans are local files, **served by no route** (Leg C C-10 removed the one mount that could have exposed them); custody rule: statistics publishable, scans never redistributed |

**The three constraints every route must answer:**

1. **Compute shape.** Work arrives as multi-hour, CPU/RAM-hungry batch jobs
   inside a stateful in-process engine — not as short request/response calls.
2. **State shape.** A SQLite file *plus* a checkout full of JSON state and
   corpora, written from hundreds of places — not a stateless API over a
   managed database.
3. **Assessor identity.** Scores are only meaningful if the cloud runs the
   *same* AEE library (pinned ≥1.5.0) through the *same* adapter. A re-implemented
   assessor is a new instrument whose readings would need re-validation against
   every existing verdict.

## 2. Platform facts (Cloudflare official docs, read 2026-10-30)

**Workers** — `developers.cloudflare.com/workers/platform/limits/`:
"CPU time | 10 ms | 5 min" (Free | Paid); "Memory | 128 MB | 128 MB";
"Subrequests | 50/request | 10,000/request"; "Worker size | 64 MiB";
"Worker startup time | 1 second". Request body size follows the zone plan
(Free/Pro 100 MB). There is no hard wall-clock duration limit on an HTTP
request, but CPU time is the binding constraint. Pricing
(`…/workers/platform/pricing/`): Paid is a $5/month account minimum including
10M requests and 30M CPU-milliseconds.

**D1** — `developers.cloudflare.com/d1/platform/limits/`: "Maximum database
size | 10 GB (Workers Paid) / 500 MB (Free)"; "Maximum string, `BLOB` or table
row size | 2,000,000 bytes"; "Maximum SQL statement length | 100,000 bytes";
"Maximum SQL query duration | 30 seconds"; "Queries per Worker invocation |
1000 (Workers Paid)". And `…/d1/reference/faq/`: "Each individual D1 database
is inherently single-threaded, and processes queries one at a time."

**Python Workers** — GA since Cloudflare's 2026-09-21 announcement; FastAPI is
a documented, supported framework (`…/workers/languages/python/packages/`
shows `fastapi` as the example dependency; supported packages are "pure and
PyEmscripten Python packages on PyPI" plus "packages that are included in
Pyodide" — numpy is a Pyodide package). The runtime is Pyodide (CPython on
WebAssembly) inside the same isolate limits as any Worker.
`…/workers/languages/python/stdlib/`: `multiprocessing` and `threading` "can
be imported, but are not functional"; and under *In-memory filesystem*:
"Python Workers have access to an ephemeral, in-memory filesystem… all data
is **lost when the Worker isolate is destroyed**… Use KV, R2, or Durable
Objects for durable storage." There is no subprocess facility.

**Containers** — `developers.cloudflare.com/containers/platform/limits/`
(updated 2026-10-29): instance types from `lite` (1/16 vCPU, 256 MiB, 2 GB
disk) to `standard-4` (4 vCPU, 12 GiB, 20 GB); custom types cap at 4 vCPU /
12 GiB / 20 GB disk; "Image size | Same as instance disk space"; snapshots
max 20 GB, 30-day retention. Lifecycle
(`…/containers/concepts/architecture/` and `…/containers/faq/`): "**All disk
is ephemeral by default. When a Container instance goes to sleep, the next
time it starts, it uses a fresh disk from the container image.**" A container
is reached only through a Durable Object; instances stop on an inactivity
timeout and start on demand. Pricing (`…/containers/platform/pricing/`):
memory $0.0000025 per GiB-second (25 GiB-hours/month included), CPU
$0.000020 per vCPU-second of *active* use (375 vCPU-minutes included), disk
$0.00000007 per GB-second (200 GB-hours included), billing "starts when a
request is sent to the container" and stops when it sleeps.

**Pages** — `developers.cloudflare.com/pages/platform/limits/`: 20,000 files
per deployment (100,000 on paid plans), 25 MiB maximum per file; Functions
count against the Workers quotas above.

For scale against all of this: today's entire publishable dataset is ≈50 MB,
the production database is 6.9 MB, and the SPA is 1.1 MB. Storage ceilings are
not the problem anywhere. **Compute shape and state shape are.**

## 3. The routes, on the evidence

### (a) Workers (TypeScript) API + D1, assessor ported to TypeScript

*Fits:* the request/response surface conceptually maps (REST + D1's SQLite
dialect is close to the app's); Pages serves the SPA unchanged; accounts and
invites are natural D1 tables.
*Breaks:* **everything load-bearing.** The assessor would be a new TypeScript
instrument: AEE's scoring (graph propagation over evidence) re-implemented
line-by-line, with every existing verdict hostage to porting fidelity — in a
program that already caught a *version bump* changing 16 of 23 scores, a
*language port* is not a risk, it is a certainty of divergence until proven
otherwise across the whole register. The pipelines fare worse: 5 minutes of
CPU per invocation against jobs designed to run for hours (Workflows can
chain steps, but each pipeline would have to be re-architected into resumable
steps around a 128 MB isolate and a 30-second-per-query, single-threaded
database); numpy has no full equivalent in the JS runtime for the corpus
statistics the pipelines run on. Subprocess surfaces (terminal, Ollama,
paper-search) have no existence at all.
*Cost:* a ground-up rewrite — ~300 endpoints, ~30 pipelines, the assessor,
the storage layer — plus a permanent second implementation to keep honest
against the desktop original. The largest build by a multiple.
*Risk:* the program's epistemic core forks. Even a perfect port leaves two
assessors to reconcile forever.

### (b) Python Workers (Pyodide) running the FastAPI app

*Fits:* real progress since this was last possible to say — Python Workers
are GA, FastAPI is supported, numpy ships with Pyodide, and AEE is pure
Python, so the assessor itself could in principle run unmodified. The SPA
and the API's *shape* survive.
*Breaks:* the runtime's documented limits cut the app at the joints.
Filesystem state is in-memory and dies with the isolate — but the app's
claims, corpora, phase state, anchors, uploads, and caches *are* files,
written from hundreds of call sites; every one would need re-plumbing to
R2/D1/KV behind a storage abstraction the codebase does not have. Threading
is non-functional and subprocesses do not exist — the terminal, the Ollama
lifecycle, the env endpoints, and the paper-search client cannot run.
psutil does not exist, so the engine's resource gating has no inputs. The
128 MB isolate ceiling sits under an app whose import graph alone (425
modules pulling numpy/matplotlib) plus corpus work runs far above it, and
the 5-minute CPU ceiling still forbids the hours-long jobs the engine
exists to run; isolate state loss between requests dissolves the in-process
engine, the loop sessions, and every scheduler, all of which would need
re-invention on Durable Objects/Workflows. SQLite becomes D1 through a
driver shim the 3,019-line aiosqlite layer was never written against.
*Cost:* not a rewrite of the endpoints, but a re-platforming of everything
underneath them — storage, engine, processes — comparable in size to (a)
once the engine is honestly included, with a hard ceiling at the end:
the long-running compute still cannot be made whole.
*Risk:* a long tail of "imports fine, fails at runtime" Pyodide gaps across
425 modules; and the finished thing is *not* the full tool — the terminal,
env management, and local-model surfaces are gone, and jobs are capped.

### (c) Cloudflare Containers running the existing FastAPI app, state externalized — **RECOMMENDED**

*Fits:* a container is a real Linux process environment: CPython with native
numpy/matplotlib/reportlab wheels, subprocesses, threads, a filesystem,
uvicorn exactly as today. The app — all ~300 routes, the engine, the loops,
the assessor at its pinned version — runs essentially unmodified; the
`standard-1` instance (½ vCPU, 4 GiB, 8 GB) already dwarfs today's ~50 MB
dataset and 6.9 MB database, and types scale to 4 vCPU / 12 GiB / 20 GB.
This is the only route where "the full working tool" is a description
rather than an aspiration: the cloud edition *is* the tool, same code, same
assessor, same verdicts.
*What has to be built around it* (the honest work list):
- **An edge Worker + Durable Object front** (containers are only reachable
  through one): TLS termination point for the subdomain, session
  authentication, the noindex header on *every* response, and waking /
  routing to the single named container instance.
- **Identity in D1**: users, invites, sessions, memberships, audit — small,
  new, and authoritative at the edge, so auth never depends on the
  container being awake.
- **State discipline for the ephemeral disk**: the research dataset (app
  SQLite + checkout file state) becomes a versioned **bundle in R2**,
  produced by the publish pipeline (§4 of the spec); the container hydrates
  from the bundle manifest on start (hash-verified), works on its local
  disk, and exports changed state back to R2 on a cadence and on orderly
  stop; the platform snapshot facility (≤20 GB, 30-day retention) is the
  belt-and-braces copy. Nothing precious lives only on the container disk —
  that is a design rule, stated as spec claim C083-13.
- **Sleep policy coordinated with jobs**: the instance sleeps when idle,
  but not while jobs run; the first request after sleep pays a container
  start (seconds), which the Status surface states honestly rather than
  hiding.
*Breaks / degrades, stated plainly:* no GPU exists in Containers (instance
types are CPU-only) — the two GPU pipelines run their existing CPU fallback,
as they already do on any machine without CUDA. The Ollama provider has no
local server to manage unless one is bundled (spec decision: not bundled —
model weights against a 20 GB disk with no GPU buys nothing; external
providers already cover the AI surfaces, and the provider simply reports
offline, the same behavior as a desktop without Ollama). Host-management
endpoints whose meaning *is* the local machine (env pip installs, process
shutdown) are excluded from the cloud edition — the spec lists them with
reasons; everything a researcher *does* in the tool is present.
*Cost:* the smallest build of the three by a wide margin — one edge Worker,
one D1 schema, one container image + deploy pipeline, one publish/hydrate
pipeline, the accounts/admin layer, and role gates in the SPA. The
application itself changes only at its edges (session identity in, a few
host-local routes out).
*Risk:* Containers is Cloudflare's newest of these surfaces (its
durable-object scheduling policy is still labelled public beta; the base
platform and limits pages are current and priced). The single-instance
model is a serialization point — which matches the tool's existing
single-process design and an invited-team scale, and is stated as a limit,
not hidden. Estimated running cost from the official rates: a
`standard-1` instance awake around the clock prices at roughly **$35–40/month**
(memory ≈ $26, disk ≈ $1.50, active CPU ≈ $5, plus the $5 Workers Paid
minimum); with idle sleep doing its work, materially less. This is an
estimate from published rates, not a quote.

### (d) Hybrids considered

- **(d1) Pages/Workers for reads + Containers for the tool** — this is not
  a rival to (c); it is (c)'s shape. The recommendation already puts the
  SPA, auth, and identity at the edge and the tool in the container.
- **(d2) Workers + Hyperdrive to an external Postgres** — moves the
  database problem, keeps every compute problem, and takes the data off
  the owner's Cloudflare pattern onto a second vendor. Nothing bought.
- **(d3) One Durable Object per program with SQLite storage** — elegant
  for new apps; here it inherits route (a)'s full rewrite and assessor
  port. Nothing bought over (a).

## 4. Recommendation

**Route (c): Cloudflare Containers running the existing FastAPI application,
fronted by an edge Worker + Durable Object that own identity (D1) and the
noindex/login perimeter, with the research dataset moving as hash-verified
bundles through R2 between the repo/desktop side and the container.**

It is the only route that satisfies all three constraints from §1 at once:
the compute runs in its native shape, the state keeps its native shape
(behind an explicit publish/hydrate discipline instead of a rewrite), and
the assessor is bit-identical because it is literally the same library at
the same pinned version running the same adapter code. It is also the only
route whose build effort goes into the features the owner ordered
(accounts, invites, admin, hosting) instead of into re-creating the tool.

## 5. The losers' disqualifiers, plainly

- **Route (a) — TS rewrite + assessor port:** disqualified by assessor
  identity (§1, constraint 3) and by the 5-minute CPU ceiling against
  hours-long jobs. It forks the epistemic core of a program whose entire
  discipline is that verdicts are comparable across time.
- **Route (b) — Python Workers:** disqualified by the platform's own
  documented limits — non-functional threading, no subprocesses, an
  in-memory filesystem that dies with the isolate, a 128 MB ceiling —
  against an app whose state *is* files, whose engine *is* a resident
  process, and whose jobs run for hours. It could one day host a read API;
  it cannot host this tool.
- **Route (d2)/(d3):** disqualified as strictly worse versions of (a)/(c)
  on the same evidence.

*Platform facts verified 2026-10-30 from the Cloudflare documentation pages
cited in §2. If any figure has moved by build time, the Phase 2 plan
re-verifies before the first deploy — the route decision does not rest on
any single number except the structural ones (isolate memory/filesystem
model, D1's query ceiling, container ephemerality), which are architectural,
not pricing, facts.*
