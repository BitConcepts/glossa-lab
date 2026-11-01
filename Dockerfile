# syntax=docker/dockerfile:1
# ─────────────────────────────────────────────────────────────────────
# Spec 083 (T006) — Glossa Lab cloud-edition container image.
#
# ONE immutable image: the existing FastAPI backend + the built SPA,
# served by the backend exactly as on the desktop (glossa_lab.main
# mounts frontend/dist via StaticFiles). The running instance is
# never mutated: no pip installs, no rebuilds inside the container —
# under GLOSSA_CLOUD=1 the env-mutation and shutdown routers are not
# even registered (T007).
#
# Image identity scheme (recorded for the rollout record, C083-9):
# the image is tagged with the full git SHA of the commit it was
# built from — `glossa-lab:<git-sha>` — and the same SHA is stamped
# into the image as the org.opencontainers.image.revision label via
# the GIT_SHA build arg. CI (cloud-image-smoke job) builds and tags
# exactly this way. The dataset is NOT baked into the image: it
# arrives as an R2 bundle hydrated into GLOSSA_DATA_DIR (T011).
#
#   docker build --build-arg GIT_SHA=$(git rev-parse HEAD) \
#       -t glossa-lab:$(git rev-parse HEAD) .
#   docker run -p 8001:8001 glossa-lab:<git-sha>
# ─────────────────────────────────────────────────────────────────────

# ── Stage 1: build the SPA from frontend/ (mirrors the CI pattern:
# npm ci from the lockfile, then `npm run build` → frontend/dist) ────
FROM node:24-slim AS frontend
WORKDIR /build/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ── Stage 2: backend runtime (Python 3.12, per the repo CI) ─────────
FROM python:3.12-slim AS runtime

ARG GIT_SHA=unknown
LABEL org.opencontainers.image.title="glossa-lab" \
      org.opencontainers.image.revision=$GIT_SHA \
      org.opencontainers.image.description="Glossa Lab cloud edition (Spec 083): backend + built SPA in one immutable image"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    GLOSSA_CLOUD=1 \
    GLOSSA_DATA_DIR=/data \
    PYTHONPATH=/app/backend

WORKDIR /app

# Backend source (pyproject.toml carries the dependency pin set,
# including applied-epistemic-engineering>=1.5.0,<1.6). The package
# is installed from the source tree; PYTHONPATH above keeps the
# in-tree copy authoritative at runtime, so the app resolves its
# repo-root-relative paths (frontend/dist, backend/static, claims)
# exactly as it does from a checkout.
COPY backend/ ./backend/
RUN pip install --upgrade pip && pip install ./backend

# The built SPA, at the path glossa_lab.main serves it from.
COPY --from=frontend /build/frontend/dist ./frontend/dist

# The GAP-ENV regression set's claim records (Spec 083 T008 smoke;
# also the live extracted-claims store the AEE adapter scores). The
# research dataset itself is NOT in the image — it hydrates from R2
# into /data at startup time (backend/glossa_lab/cloud_bundles.py).
COPY glossa-indus/claims ./glossa-indus/claims

RUN mkdir -p /data && \
    useradd --create-home --uid 10001 glossa && \
    chown -R glossa:glossa /app /data
USER glossa

EXPOSE 8001

# Hydration (when a bundle is configured) runs before this CMD in the
# platform entrypoint; job state restored by hydration is in place
# before the engine resumes (cloud_bundles.py documents the order).
CMD ["python", "-m", "uvicorn", "glossa_lab.main:app", "--host", "0.0.0.0", "--port", "8001"]
