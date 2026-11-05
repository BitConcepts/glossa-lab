import { handleRequest } from "./worker";
import type { Env } from "./types";

// Amendment 5 (T055): the GlossaFront Durable Object export is gone —
// the Worker has no container role; the origin is the desktop reached
// through the GLOSSA_ORIGIN Workers VPC binding (src/types.ts).

export default {
  fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    return handleRequest(request, env, ctx);
  },
} satisfies ExportedHandler<Env>;
