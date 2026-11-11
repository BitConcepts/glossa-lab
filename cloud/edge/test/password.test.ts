// The REAL production hasher (src/password.ts defaultHasher).
//
// Every flow test injects FakeHasher for speed, which is exactly how
// the hash-wasm Argon2id defect shipped: the real hash-creation path
// was never the thing under test on the production runtime shape.
// This file pins the real implementation's contract directly:
// encoded form, right/wrong password, foreign and malformed strings
// verifying false (never throwing), the stored-iteration-count rule,
// and the dummy hash being a live encoding in the current format.
// (Runtime-shape proof under workerd is recorded in
// specs/083-cloud-edition/records/kdf-amendment-2026-11-10.md.)

import { describe, expect, it } from "vitest";
import {
  defaultHasher,
  DUMMY_PASSWORD_HASH,
  PBKDF2_PARAMS,
  Pbkdf2Hasher,
} from "../src/password";

describe("defaultHasher — real PBKDF2 implementation", () => {
  it("is the Pbkdf2Hasher with the OWASP parameters", () => {
    expect(defaultHasher).toBeInstanceOf(Pbkdf2Hasher);
    expect(PBKDF2_PARAMS.digest).toBe("SHA-512");
    expect(PBKDF2_PARAMS.iterations).toBe(210000);
    expect(PBKDF2_PARAMS.saltLength).toBe(16);
    expect(PBKDF2_PARAMS.keyLength).toBe(32);
  });

  it("hashes to the $pbkdf2-sha512$i=210000$ encoded form and verifies", async () => {
    const encoded = await defaultHasher.hash("correct horse battery staple");
    expect(encoded.startsWith("$pbkdf2-sha512$i=210000$")).toBe(true);
    expect(encoded).not.toContain("correct horse");
    const parts = encoded.split("$");
    // ["", "pbkdf2-sha512", "i=210000", salt, derived]
    expect(parts).toHaveLength(5);
    expect(atob(parts[3])).toHaveLength(16);
    expect(atob(parts[4])).toHaveLength(32);
    await expect(
      defaultHasher.verify("correct horse battery staple", encoded),
    ).resolves.toBe(true);
  });

  it("rejects a wrong password", async () => {
    const encoded = await defaultHasher.hash("the-right-password");
    await expect(
      defaultHasher.verify("the-wrong-password", encoded),
    ).resolves.toBe(false);
  });

  it("salts independently: two hashes of one password differ, both verify", async () => {
    const a = await defaultHasher.hash("same-password-twice");
    const b = await defaultHasher.hash("same-password-twice");
    expect(a).not.toBe(b);
    await expect(defaultHasher.verify("same-password-twice", a)).resolves.toBe(true);
    await expect(defaultHasher.verify("same-password-twice", b)).resolves.toBe(true);
  });

  it("verify returns false (never throws) for malformed and foreign strings", async () => {
    const bad = [
      "",
      "not-a-hash",
      "$pbkdf2-sha512$",
      "$pbkdf2-sha512$i=210000$",
      "$pbkdf2-sha512$i=210000$AAAA",
      "$pbkdf2-sha512$i=abc$AAAA$AAAA",
      "$pbkdf2-sha512$i=0$AAAA$AAAA",
      "$pbkdf2-sha512$i=210000$!!!not-base64!!!$AAAA",
      "$pbkdf2-sha512$i=210000$AAAA$AAAA$EXTRA",
      // The retired Argon2id format is foreign and must not verify.
      "$argon2id$v=19$m=19456,t=2,p=1$t1iz/zBYRf7RTfwTdFCRKQ$lNLWCmdnBx6TI3Jr43uoUmTaU+z011YiSOWOwFEe+m0",
      "fake$0123456789abcdef",
    ];
    for (const encoded of bad) {
      await expect(defaultHasher.verify("any-password", encoded)).resolves.toBe(false);
    }
  });

  it("verify derives with the iteration count stored in the string", async () => {
    // A hash minted at a lower count (as a future bump would leave
    // behind) still verifies: the count comes from the string.
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const key = await crypto.subtle.importKey(
      "raw",
      new TextEncoder().encode("legacy-count-password"),
      "PBKDF2",
      false,
      ["deriveBits"],
    );
    const bits = await crypto.subtle.deriveBits(
      { name: "PBKDF2", hash: "SHA-512", salt, iterations: 1000 },
      key,
      256,
    );
    const b64 = (u8: Uint8Array) => {
      let s = "";
      for (const byte of u8) s += String.fromCharCode(byte);
      return btoa(s);
    };
    const legacy = `$pbkdf2-sha512$i=1000$${b64(salt)}$${b64(new Uint8Array(bits))}`;
    await expect(defaultHasher.verify("legacy-count-password", legacy)).resolves.toBe(true);
    await expect(defaultHasher.verify("other-password", legacy)).resolves.toBe(false);
  });

  it("the dummy hash is a live encoding in the current format", () => {
    expect(DUMMY_PASSWORD_HASH.startsWith("$pbkdf2-sha512$i=210000$")).toBe(true);
  });

  it("the dummy hash does not verify for an arbitrary password", async () => {
    await expect(
      defaultHasher.verify("not-the-dummy-password", DUMMY_PASSWORD_HASH),
    ).resolves.toBe(false);
  });
});
