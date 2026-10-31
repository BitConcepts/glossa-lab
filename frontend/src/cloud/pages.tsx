/**
 * Spec 083 (Step 3, T025) — the public auth surfaces:
 * login (wireframe 01), invite acceptance (02), glassbreak
 * first-run setup (03). These are the ONLY screens an anonymous
 * visitor can reach; they render no program data.
 *
 * Failure language follows the wireframes exactly: sign-in failures
 * are undifferentiated (no hint which part was wrong, or whether
 * the account exists), and invite failures name the family of the
 * problem — spent, expired, revoked, invalid — without ever
 * confirming whether a guessed code existed.
 */

import { useEffect, useState, type FormEvent, type ReactNode } from "react";
import {
  CloudApiError,
  completeSetup,
  getInvitePreview,
  login,
  probeSetupOpen,
  redeemInvite,
} from "./api";
import type { InvitePreview } from "./types";

function Brand() {
  return (
    <div className="cl-brand">
      <div className="cl-brand-mark">G</div>
      <div>
        <div className="cl-brand-name">Glossa Lab</div>
        <div className="cl-brand-sub">Epistemic research workbench</div>
      </div>
    </div>
  );
}

function fmtWhen(iso: string): string {
  const d = new Date(iso);
  return Number.isNaN(d.getTime())
    ? iso
    : d.toLocaleString(undefined, {
        month: "short", day: "numeric", year: "numeric",
        hour: "numeric", minute: "2-digit",
      });
}

function Shell({ children, wide }: { children: ReactNode; wide?: boolean }) {
  return (
    <div className="cl-auth-wrap">
      <div className={`cl-auth-card${wide ? " wide" : ""}`}>
        <Brand />
        {children}
      </div>
    </div>
  );
}

// ── Wireframe 01 — login ────────────────────────────────────────────────────

export function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [setupOpen, setSetupOpen] = useState(false);

  useEffect(() => {
    void probeSetupOpen().then(setSetupOpen);
  }, []);

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await login(username.trim(), password);
      const next = new URLSearchParams(window.location.search).get("next");
      const dest = next && next.startsWith("/") && !next.startsWith("//") ? next : "/";
      window.location.assign(dest);
    } catch {
      // One undifferentiated message, whatever the edge answered:
      // no hint which part was wrong or whether the account exists.
      setError("Those details don't match an account, or the account is disabled.");
      setBusy(false);
    }
  };

  return (
    <Shell>
      <h1>Sign in</h1>
      <p className="cl-lede">
        Glossa Lab is members-only. Sign in with the username and
        password from your invite — there is no public sign-up.
      </p>
      {error && <div className="cl-form-error">{error}</div>}
      <form onSubmit={submit}>
        <div className="cl-field">
          <label htmlFor="cl-login-username">Username</label>
          <input
            id="cl-login-username"
            autoComplete="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="cl-field">
          <label htmlFor="cl-login-password">Password</label>
          <input
            id="cl-login-password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button className="cl-btn primary" type="submit" disabled={busy}>
          {busy ? "Signing in…" : "Sign in"}
        </button>
      </form>
      {setupOpen && (
        <div className="cl-callout info" style={{ marginTop: 14 }}>
          <strong>First time here?</strong> This deployment has not been
          set up yet. If you were given a one-time setup code,{" "}
          <a href="/setup">finish setup</a> first.
        </div>
      )}
      <div className="cl-auth-foot">
        Forgot your password? Ask an admin to disable and re-invite
        your account — passwords are never recoverable by email in
        this edition.
      </div>
    </Shell>
  );
}

// ── Wireframe 03 — glassbreak first-run setup ───────────────────────────────

// The setup identity is fixed by the deployment's seed record
// (Amendment 3); the edge takes it from that record and never from
// this form — the fields render disabled, as the wireframe shows.
const SETUP_USERNAME = "glassbreak";
const SETUP_EMAIL = "tristen.pierson@gmail.com";

export function SetupPage() {
  const [open, setOpen] = useState<boolean | null>(null);
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [ack, setAck] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    void probeSetupOpen().then(setOpen);
  }, []);

  if (open === null) {
    return (
      <Shell>
        <p className="cl-lede">Checking whether setup is still open…</p>
      </Shell>
    );
  }

  if (!open) {
    return (
      <Shell>
        <h1>Setup is closed</h1>
        <p className="cl-lede">
          The owner account for this deployment already exists, so the
          one-time setup can never run again. If you are the owner,{" "}
          <a href="/login">sign in</a> with the glassbreak account.
        </p>
        <div className="cl-auth-foot">
          Seeing this page by mistake? Setup closes itself the moment
          it completes — there is nothing to fix.
        </div>
      </Shell>
    );
  }

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    if (password !== confirm) {
      setError("The two passwords don't match.");
      return;
    }
    if (password.length < 8) {
      setError("Choose a password of at least 8 characters.");
      return;
    }
    setBusy(true);
    try {
      await completeSetup(code.trim(), password);
      window.location.assign("/");
    } catch (err) {
      setBusy(false);
      if (err instanceof CloudApiError && err.status === 404) {
        // The code was wrong, expired, or setup just closed.
        setOpen(false);
        return;
      }
      if (err instanceof CloudApiError && err.code === "invalid_password") {
        setError("Choose a password of at least 8 characters.");
        return;
      }
      if (err instanceof CloudApiError && err.code === "setup_code_invalid") {
        setError("That code is not valid. Check it and try again — a mistyped code is the usual cause.");
        return;
      }
      if (err instanceof CloudApiError && err.code === "setup_expired") {
        setError("That code has expired — codes live 24 hours. Ask whoever deployed this to issue a fresh one.");
        return;
      }
      setError("Something interrupted setup. Check the code and try again.");
    }
  };

  return (
    <Shell wide>
      <h1>Set up the owner account</h1>
      <p className="cl-lede">
        This deployment has no accounts yet. Setup creates the
        break-glass owner — <strong>glassbreak</strong> — exactly
        once, and then closes forever. You need the one-time setup
        code from whoever deployed this.
      </p>
      {error && <div className="cl-form-error">{error}</div>}
      <form onSubmit={submit}>
        <div className="cl-field">
          <label htmlFor="cl-setup-username">Username</label>
          <input id="cl-setup-username" value={SETUP_USERNAME} disabled />
          <div className="cl-hint">Fixed by the deployment. This account is the recovery path if every admin is locked out.</div>
        </div>
        <div className="cl-field">
          <label htmlFor="cl-setup-email">Email</label>
          <input id="cl-setup-email" value={SETUP_EMAIL} disabled />
        </div>
        <div className="cl-field">
          <label htmlFor="cl-setup-code">One-time setup code</label>
          <input
            id="cl-setup-code"
            type="password"
            autoComplete="off"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            required
          />
          <div className="cl-hint">Single use, and it expires 24 hours after it was issued.</div>
        </div>
        <div className="cl-field">
          <label htmlFor="cl-setup-password">New password</label>
          <input
            id="cl-setup-password"
            type="password"
            autoComplete="new-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <div className="cl-hint">At least 8 characters. There is no email recovery for this account — keep it somewhere safe.</div>
        </div>
        <div className="cl-field">
          <label htmlFor="cl-setup-confirm">Confirm password</label>
          <input
            id="cl-setup-confirm"
            type="password"
            autoComplete="new-password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            required
          />
        </div>
        <label className="cl-check">
          <input type="checkbox" checked={ack} onChange={(e) => setAck(e.target.checked)} />
          <span>I understand this account is the break-glass owner: it can manage every user and workspace, and its password cannot be recovered by email.</span>
        </label>
        <button className="cl-btn primary" type="submit" disabled={busy || !ack}>
          {busy ? "Creating the owner account…" : "Create the owner account"}
        </button>
      </form>
      <div className="cl-auth-foot">
        Already set up? <a href="/login">Sign in</a> instead — setup
        closes itself the moment it completes.
      </div>
    </Shell>
  );
}

// ── Wireframe 02 — invite acceptance ────────────────────────────────────────

const SPENT_COPY: Record<string, { title: string; body: string }> = {
  invalid: {
    title: "This invite link isn't valid",
    body: "The link may have been mistyped, or the invite behind it was revoked or has already been used. Ask whoever invited you to send a fresh link.",
  },
  redeemed: {
    title: "This invite has already been used",
    body: "Each invite creates exactly one account, and this one has done its job. If that account is yours, sign in. If you never used this link, tell whoever sent it — they can revoke the account and issue a fresh invite.",
  },
  revoked: {
    title: "This invite was revoked",
    body: "Whoever issued this invite withdrew it before it was used. Ask them to send a fresh one if you still need access.",
  },
  expired: {
    title: "This invite has expired",
    body: "Invites live for seven days by default. Ask whoever invited you to send a fresh link.",
  },
};

export function InvitePage({ code }: { code: string }) {
  const [preview, setPreview] = useState<InvitePreview | null>(null);
  const [loadFailed, setLoadFailed] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [consent, setConsent] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);

  useEffect(() => {
    let live = true;
    getInvitePreview(code)
      .then((p) => { if (live) setPreview(p); })
      .catch(() => { if (live) setLoadFailed(true); });
    return () => { live = false; };
  }, [code]);

  if (loadFailed) {
    return (
      <Shell>
        <h1>We couldn't check that invite</h1>
        <p className="cl-lede">
          Something went wrong reading the invite. Reload the page to
          try again — the invite itself has not been used.
        </p>
      </Shell>
    );
  }

  if (!preview) {
    return (
      <Shell>
        <p className="cl-lede">Checking your invite…</p>
      </Shell>
    );
  }

  if (preview.state !== "open") {
    const copy = SPENT_COPY[preview.state] ?? SPENT_COPY.invalid;
    return (
      <Shell>
        <h1>{copy.title}</h1>
        <p className="cl-lede">{copy.body}</p>
        <div className="cl-auth-foot">
          Already have an account? <a href="/login">Sign in</a>.
        </div>
      </Shell>
    );
  }

  if (done) {
    return (
      <Shell>
        <h1>You're in</h1>
        <p className="cl-lede">
          Your account is ready and you're signed in. You'll land in
          the workspace you were invited to; everything else stays
          invisible until someone grants it.
        </p>
        <button className="cl-btn primary" onClick={() => window.location.assign("/")}>
          Open Glossa Lab →
        </button>
      </Shell>
    );
  }

  const addressedTo = preview.email ?? null;

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    if (password !== confirm) {
      setError("The two passwords don't match.");
      return;
    }
    setBusy(true);
    try {
      await redeemInvite(code, {
        username: username.trim(),
        ...(addressedTo ? { email: addressedTo } : email.trim() ? { email: email.trim() } : {}),
        password,
      });
      setDone(true);
    } catch (err) {
      setBusy(false);
      if (err instanceof CloudApiError) {
        switch (err.code) {
          case "username_taken":
            setError("That username is taken — choose another.");
            return;
          case "invalid_username":
            setError("Usernames are 3–32 characters: lowercase letters, numbers, and _ . - only.");
            return;
          case "invite_email_mismatch":
            setError("This invite was addressed to a different email address. Use the address the invite was sent to.");
            return;
          case "invalid_password":
            setError("Choose a password of at least 8 characters.");
            return;
          case "invite_expired":
            setError("This invite has expired since the page loaded. Ask for a fresh link.");
            return;
          case "invite_revoked":
            setError("This invite was revoked since the page loaded. Ask for a fresh link.");
            return;
          case "invite_redeemed":
            setError("This invite has already been used. If that account is yours, sign in instead.");
            return;
          default:
            break;
        }
      }
      setError("Something interrupted sign-up. Check the details and try again.");
    }
  };

  return (
    <Shell wide>
      <h1>You've been invited</h1>
      <p className="cl-lede">
        Create your account to join Glossa Lab. This invite works
        once — when you're done, the link is spent.
      </p>
      <div className="cl-kv">
        {preview.created_by && (
          <div className="cl-kv-row">
            <span className="cl-kv-k">Invited by</span>
            <span className="cl-kv-v">
              {preview.created_by.username}{" "}
              <span className="cl-chip grey">{preview.created_by.global_type}</span>
            </span>
          </div>
        )}
        {addressedTo && (
          <div className="cl-kv-row">
            <span className="cl-kv-k">Email</span>
            <span className="cl-kv-v">{addressedTo}</span>
          </div>
        )}
        {(preview.workspaces ?? []).map((w) => (
          <div className="cl-kv-row" key={w.id}>
            <span className="cl-kv-k">Workspace</span>
            <span className="cl-kv-v">
              {w.name} <span className="cl-chip">{w.role}</span>
            </span>
          </div>
        ))}
        {preview.expires_at && (
          <div className="cl-kv-row">
            <span className="cl-kv-k">Invite expires</span>
            <span className="cl-kv-v">{fmtWhen(preview.expires_at)}</span>
          </div>
        )}
      </div>
      {error && <div className="cl-form-error">{error}</div>}
      <form onSubmit={submit}>
        <div className="cl-field">
          <label htmlFor="cl-invite-username">Choose a username</label>
          <input
            id="cl-invite-username"
            autoComplete="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <div className="cl-hint">Lowercase letters, numbers, and _ . - — this is how your work will be attributed.</div>
        </div>
        {!addressedTo && (
          <div className="cl-field">
            <label htmlFor="cl-invite-email">Email (optional)</label>
            <input
              id="cl-invite-email"
              type="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <div className="cl-hint">Only used to identify your account to admins. There is no email password reset in this edition.</div>
          </div>
        )}
        <div className="cl-field">
          <label htmlFor="cl-invite-password">Password</label>
          <input
            id="cl-invite-password"
            type="password"
            autoComplete="new-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <div className="cl-hint">At least 8 characters.</div>
        </div>
        <div className="cl-field">
          <label htmlFor="cl-invite-confirm">Confirm password</label>
          <input
            id="cl-invite-confirm"
            type="password"
            autoComplete="new-password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            required
          />
        </div>
        <label className="cl-check">
          <input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} />
          <span>I understand my name will be attached to the records I create and change, and that admins can see an audit log of sign-ins and changes.</span>
        </label>
        <button className="cl-btn primary" type="submit" disabled={busy || !consent}>
          {busy ? "Creating your account…" : "Create my account"}
        </button>
      </form>
      <div className="cl-auth-foot">
        Already have an account? <a href="/login">Sign in</a> — don't
        use this link; it would create a second account.
      </div>
    </Shell>
  );
}
