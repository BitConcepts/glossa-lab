// Shared harness for Step 2 identity tests: a Worker env backed by
// the in-memory identity store and a recording fake GlossaFront.

import { vi } from "vitest";
import { handleRequest } from "../src/worker";
import type { Env } from "../src/types";
import { InMemoryIdentityStore, FakeHasher } from "./fake-identity";
import { sha256Hex } from "../src/session";
import type { PasswordHasher } from "../src/password";

export const HOST = "https://glossa.bitconcepts.tech";
export const SERVICE_CREDENTIAL = "test-only-service-credential";
export const T0 = new Date("2026-10-30T12:00:00.000Z");

export interface Harness {
  store: InMemoryIdentityStore;
  front: ReturnType<typeof vi.fn>;
  frontRequests: Request[];
  call: (
    path: string,
    init?: RequestInit & { cookie?: string },
  ) => Promise<Response>;
  flush: () => Promise<void>;
  setNow: (d: Date) => void;
  cookieFor: (username: string) => Promise<string>;
}

export function makeHarness(opts: {
  hasher?: PasswordHasher;
  frontStatus?: number;
} = {}): Harness {
  const store = new InMemoryIdentityStore();
  const frontRequests: Request[] = [];
  const front = vi.fn(async (r: Request) => {
    frontRequests.push(r);
    return new Response("container-body", {
      status: opts.frontStatus ?? 200,
      headers: { "Content-Type": "text/plain" },
    });
  });
  const env = {
    DB: {} as D1Database,
    DATASETS: {} as R2Bucket,
    SERVICE_CREDENTIAL,
    GLOSSA_FRONT: {
      getByName: () => ({ fetch: front }),
    } as unknown as DurableObjectNamespace,
  } as Env;

  let now = T0;
  const pending: Promise<unknown>[] = [];
  const ctx = {
    waitUntil: (p: Promise<unknown>) => pending.push(p),
    passThroughOnException: () => undefined,
  } as unknown as ExecutionContext;

  const hasher = opts.hasher ?? new FakeHasher();

  async function call(
    path: string,
    init: RequestInit & { cookie?: string } = {},
  ): Promise<Response> {
    const headers = new Headers(init.headers);
    if (init.cookie) headers.set("Cookie", `glossa_session=${init.cookie}`);
    const { cookie: _drop, ...rest } = init;
    const request = new Request(`${HOST}${path}`, { ...rest, headers });
    return handleRequest(request, env, ctx, {
      store,
      identityStore: store,
      hasher,
      now: () => now,
    });
  }

  return {
    store,
    front,
    frontRequests,
    call,
    flush: async () => {
      await Promise.all(pending.splice(0));
    },
    setNow: (d: Date) => {
      now = d;
    },
    cookieFor: async (username: string) => {
      const res = await call("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          password: PASSWORDS[username] ?? "correct-horse-9",
        }),
      });
      if (res.status !== 200) {
        throw new Error(`login for ${username} failed: ${res.status}`);
      }
      return sessionTokenFromResponse(res);
    },
  };
}

export const PASSWORDS: Record<string, string> = {
  glassbreak: "glassbreak-pass-1",
  admin2: "admin2-pass-123",
  alice: "alice-pass-1234",
  bob: "bob-pass-12345",
  carol: "carol-pass-1234",
  gwen: "gwen-pass-12345",
};

export function sessionTokenFromResponse(res: Response): string {
  const cookie = res.headers.get("Set-Cookie") ?? "";
  const match = cookie.match(/glossa_session=([^;]+)/);
  if (!match) throw new Error(`no session cookie in: ${cookie}`);
  return match[1];
}

export function jsonBody(res: Response): Promise<Record<string, never>> {
  return res.json() as Promise<Record<string, never>>;
}

export async function seedUser(
  h: Harness,
  username: string,
  globalType: "owner" | "admin" | "member" | "guest",
  password = PASSWORDS[username] ?? "correct-horse-9",
  hasher: PasswordHasher = new FakeHasher(),
) {
  const user = {
    id: `usr_${username}`,
    username,
    email: null,
    passwordHash: await hasher.hash(password),
    globalType,
    status: "active" as const,
    createdAt: T0.toISOString(),
    removedAt: null,
  };
  await h.store.createUser(user);
  return user;
}

export async function seedWorkspace(
  h: Harness,
  id = "ws_indus",
  name = "Indus Script",
) {
  const ws = {
    id,
    name,
    slug: name.toLowerCase().replace(/[^a-z0-9]+/g, "-"),
    archivedAt: null,
    createdBy: "usr_glassbreak",
    createdAt: T0.toISOString(),
  };
  await h.store.createWorkspace(ws);
  return ws;
}

export { sha256Hex };
