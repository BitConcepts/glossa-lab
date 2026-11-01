import { Container } from "@cloudflare/containers";

/**
 * GlossaFront — the single Durable Object in front of the single
 * container instance (Spec 083, Step 1 / T009).
 *
 * Every container-bound request from the edge Worker is routed to the
 * one named instance of this class ("glossa-lab"), so all traffic to
 * the application funnels through one serialization point — matching
 * the application's single-instance design (spec Assumptions). The
 * `Container` base class owns the container lifecycle: it starts the
 * instance on the first request, blocks until the app is listening on
 * `defaultPort`, and proxies the request to it.
 */
export class GlossaFront extends Container {
  /**
   * The application port inside the container image. Must match the
   * port the repo-root Dockerfile serves (the backend's configured
   * port, 8001).
   */
  defaultPort = 8001;

  /**
   * Idle time before the instance sleeps. FR-010's job-aware sleep
   * suppression (never sleep while jobs run) is enforced with the
   * container's job-state work in a later step; Phase 1 keeps a
   * conservative idle window.
   */
  sleepAfter = "10m";

  /**
   * Environment handed to the container at start. GLOSSA_CLOUD=1 turns
   * on the cloud configuration switch (T007): the host-management
   * endpoints are not registered and Ollama is not probed.
   */
  envVars = {
    GLOSSA_CLOUD: "1",
  };

  override onStart() {
    console.log("glossa-front: container instance started");
  }

  override onStop() {
    console.log("glossa-front: container instance stopped");
  }

  override onError(error: unknown) {
    console.error("glossa-front: container error", error);
  }
}
