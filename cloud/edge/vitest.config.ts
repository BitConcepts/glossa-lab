import { defineConfig } from "vitest/config";

// Plain vitest with mocks (see README "Testing"): the Phase 1 proofs
// exercise the Worker's perimeter logic against a fake SessionStore and
// a fake Durable Object stub. The GlossaFront container itself needs a
// Docker-backed runtime, so it is covered by the Step 5 proof battery
// against the local production-shaped build instead.
export default defineConfig({
  test: {
    environment: "node",
    include: ["test/**/*.test.ts"],
  },
});
