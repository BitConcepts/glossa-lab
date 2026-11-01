import { handleRequest } from "./worker";
import type { Env } from "./types";

export { GlossaFront } from "./front";

export default {
  fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    return handleRequest(request, env, ctx);
  },
} satisfies ExportedHandler<Env>;
