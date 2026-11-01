// Password hashing (Spec 083, Step 2 / T015, T017).
//
// Implementation choice: Argon2id via `hash-wasm` (recorded in
// cloud/edge/README.md). hash-wasm ships the Argon2 WASM as an inlined
// base64 module, so it runs inside the Workers isolate with no native
// binding, no network fetch, and no extra service — unlike Node-native
// Argon2 packages, which cannot load in workerd.
//
// Parameters (OWASP Password Storage Cheat Sheet, first
// recommendation for Argon2id, inside the 128 MB isolate budget):
//   memory 19,456 KiB (19 MiB), iterations 2, parallelism 1,
//   salt 16 random bytes, output 32 bytes.
// The encoded hash string ($argon2id$v=19$m=19456,t=2,p=1$…) carries
// the parameters and salt, so verification needs nothing else stored.

import { argon2id, argon2Verify } from "hash-wasm";

export const ARGON2_PARAMS = {
  memorySizeKiB: 19456,
  iterations: 2,
  parallelism: 1,
  hashLength: 32,
  saltLength: 16,
} as const;

export interface PasswordHasher {
  hash(password: string): Promise<string>;
  verify(password: string, encodedHash: string): Promise<boolean>;
}

export class Argon2idHasher implements PasswordHasher {
  async hash(password: string): Promise<string> {
    const salt = crypto.getRandomValues(
      new Uint8Array(ARGON2_PARAMS.saltLength),
    );
    return argon2id({
      password,
      salt,
      parallelism: ARGON2_PARAMS.parallelism,
      iterations: ARGON2_PARAMS.iterations,
      memorySize: ARGON2_PARAMS.memorySizeKiB,
      hashLength: ARGON2_PARAMS.hashLength,
      outputType: "encoded",
    });
  }

  async verify(password: string, encodedHash: string): Promise<boolean> {
    try {
      return await argon2Verify({ password, hash: encodedHash });
    } catch {
      // A malformed stored hash is a failed verification, never a
      // distinguishable error (login failures stay indistinguishable).
      return false;
    }
  }
}

export const defaultHasher: PasswordHasher = new Argon2idHasher();

/**
 * A real Argon2id hash of a throwaway password, with the production
 * parameters. Login verifies against this when the username does not
 * exist (or the account cannot sign in), so an unknown user costs the
 * same Argon2 work as a wrong password and the two failures stay
 * indistinguishable in body and in timing shape (T016).
 */
export const DUMMY_PASSWORD_HASH =
  "$argon2id$v=19$m=19456,t=2,p=1$t1iz/zBYRf7RTfwTdFCRKQ$lNLWCmdnBx6TI3Jr43uoUmTaU+z011YiSOWOwFEe+m0";

/** Minimum accepted password length at setup / invite redemption. */
export const MIN_PASSWORD_LENGTH = 8;
export const MAX_PASSWORD_LENGTH = 128;

export function isAcceptablePassword(password: unknown): password is string {
  return (
    typeof password === "string" &&
    password.length >= MIN_PASSWORD_LENGTH &&
    password.length <= MAX_PASSWORD_LENGTH
  );
}
