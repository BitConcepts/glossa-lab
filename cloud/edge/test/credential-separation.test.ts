// T024 / C083-8 / FR-008 — credential separation at the edge.
//
// The Spec 082 install token is NOT a cloud credential. Presented in
// any position — as the session cookie, as some other cookie, as an
// Authorization header, or as a query parameter — it yields NO
// authenticated access at the edge. Only the glossa_session cookie
// authenticates, and Authorization headers are never consulted for
// session auth. (The token value below is a test fixture string, not
// a real install token.)

import { describe, expect, it } from "vitest";
import { makeHarness, seedUser } from "./harness";

const INSTALL_TOKEN = "spec082-install-token-TEST-FIXTURE-NOT-REAL";

describe("Spec 082 install token yields no authenticated access (T024)", () => {
  it("as the session cookie value", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    const res = await h.call("/api/claims", { cookie: INSTALL_TOKEN });
    expect(res.status).toBe(401);
    expect(h.front).not.toHaveBeenCalled();
  });

  it("as another cookie (install_token / token cookie names)", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    for (const cookieHeader of [
      `install_token=${INSTALL_TOKEN}`,
      `token=${INSTALL_TOKEN}`,
      `glossa_install=${INSTALL_TOKEN}`,
    ]) {
      const res = await h.call("/api/claims", {
        headers: { Cookie: cookieHeader },
      });
      expect(res.status, cookieHeader).toBe(401);
    }
    expect(h.front).not.toHaveBeenCalled();
  });

  it("as an Authorization header (Bearer and raw)", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    for (const authorization of [
      `Bearer ${INSTALL_TOKEN}`,
      INSTALL_TOKEN,
      `Token ${INSTALL_TOKEN}`,
    ]) {
      const api = await h.call("/api/claims", {
        headers: { Authorization: authorization },
      });
      expect(api.status, authorization).toBe(401);
      const page = await h.call("/claims", {
        headers: { Authorization: authorization },
      });
      expect(page.status, authorization).toBe(302);
      expect(page.headers.get("Location")).toContain("/login");
    }
    expect(h.front).not.toHaveBeenCalled();
  });

  it("as a query parameter (token / install_token / access_token)", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    for (const param of ["token", "install_token", "access_token", "api_key"]) {
      const res = await h.call(`/api/claims?${param}=${INSTALL_TOKEN}`);
      expect(res.status, param).toBe(401);
    }
    expect(h.front).not.toHaveBeenCalled();
  });

  it("in every position at once still yields nothing", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    const res = await h.call(`/api/claims?token=${INSTALL_TOKEN}`, {
      cookie: INSTALL_TOKEN,
      headers: { Authorization: `Bearer ${INSTALL_TOKEN}` },
    });
    expect(res.status).toBe(401);
    expect(h.front).not.toHaveBeenCalled();
  });

  it("a real session still works — and only via the cookie", async () => {
    const h = makeHarness();
    await seedUser(h, "alice", "member");
    const token = await h.cookieFor("alice");
    // The session token itself, moved into an Authorization header or
    // a query parameter, does NOT authenticate: cookie position only.
    const asHeader = await h.call("/api/claims", {
      headers: { Authorization: `Bearer ${token}` },
    });
    expect(asHeader.status).toBe(401);
    const asQuery = await h.call(`/api/claims?token=${token}`);
    expect(asQuery.status).toBe(401);
    const asCookie = await h.call("/api/claims", { cookie: token });
    expect(asCookie.status).toBe(200);
  });

  it("X-Glossa-* spoofing with the install token stays stripped (Phase 1 contract)", async () => {
    const h = makeHarness();
    const res = await h.call("/login", {
      headers: {
        "X-Glossa-User-Id": "usr_attacker",
        "X-Glossa-Global-Type": "owner",
        "X-Glossa-Service-Credential": INSTALL_TOKEN,
      },
    });
    expect(res.status).toBe(200);
    const fwd = h.frontRequests[0];
    expect(fwd.headers.get("X-Glossa-User-Id")).toBeNull();
    expect(fwd.headers.get("X-Glossa-Global-Type")).toBeNull();
    expect(fwd.headers.get("X-Glossa-Service-Credential")).toBe(
      "test-only-service-credential",
    );
    expect(fwd.headers.get("X-Glossa-Service-Credential")).not.toBe(INSTALL_TOKEN);
  });
});
