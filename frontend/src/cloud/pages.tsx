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

function Shell({ children, wide, foot }: { children: ReactNode; wide?: boolean; foot?: string }) {
  return (
    <div className="cl-auth-wrap">
      <div className={`cl-auth-card${wide ? " wide" : ""}`}>
        <Brand />
        {children}
      </div>
      {foot && <div className="cl-page-foot">{foot}</div>}
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
      // no hint which part was wrong or whether the account exists
      // (wireframe 01's specimen sentence, verbatim).
      setError("That username and password don't match our records. Check them and try again.");
      setBusy(false);
    }
  };

  return (
    <Shell foot="glossa.bitconcepts.tech · This site is deliberately not indexed by search engines, and there is no public registration — accounts are created from invite links only.">
      <h1>Sign in</h1>
      <p className="cl-lede">
        Glossa Lab is invitation-only. Sign in with the username and
        password you set when you accepted your invite.
      </p>
      {error && <div className="cl-form-error">{error}</div>}
      <form onSubmit={submit}>
        <div className="cl-field">
          <label htmlFor="cl-login-username">Username</label>
          <input
            id="cl-login-username"
            autoComplete="username"
            placeholder="your username"
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
            placeholder="your password"
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
// this form. The username therefore renders pre-filled AND disabled
// (wireframe 03's annotation imagines it editable at this one
// moment; the Phase 2 seed contract + Amendment 3 fix it — named
// deviation in the BUILD-RECORD). The seed's email is not a form
// field at all, as the wireframe shows.
const SETUP_USERNAME = "glassbreak";

export function SetupPage() {
  const [open, setOpen] = useState<boolean | null>(null);
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
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
    <Shell wide foot="glossa.bitconcepts.tech · Setup is part of the deployment record: its completion (not the code, not the password) is written to the audit log.">
      <h1>First-run setup</h1>
      <p className="cl-lede">
        This deployment has no users yet. This screen creates its one
        administrator account — and then it closes, permanently. It
        can be completed only with the one-time setup code from the
        deployment terminal.
      </p>
      {error && <div className="cl-form-error">{error}</div>}
      <form onSubmit={submit}>
        <div className="cl-field">
          <label htmlFor="cl-setup-code">
            Setup code <span className="cl-label-hint">— shown once, where the deployment was run</span>
          </label>
          <input
            id="cl-setup-code"
            className="cl-code-input"
            autoComplete="off"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            required
          />
          <div className="cl-hint">
            In the real flow the owner pastes the code here; nothing about it is ever
            sent by email or chat, and it stops working 24 hours after it was issued.
          </div>
        </div>
        <div className="cl-field">
          <label htmlFor="cl-setup-username">Admin username</label>
          <input id="cl-setup-username" value={SETUP_USERNAME} disabled />
          <div className="cl-hint">Fixed by the deployment seed. This account is the recovery path if every admin is locked out.</div>
        </div>
        <div className="cl-field">
          <label htmlFor="cl-setup-password">Set the admin password</label>
          <input
            id="cl-setup-password"
            type="password"
            autoComplete="new-password"
            placeholder="a password only you know"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <div className="cl-hint">At least 8 characters. There is no email recovery for this account — keep it somewhere safe.</div>
        </div>
        <div className="cl-field">
          <label htmlFor="cl-setup-confirm">Repeat the password</label>
          <input
            id="cl-setup-confirm"
            type="password"
            autoComplete="new-password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            required
          />
        </div>
        <div className="cl-callout warn">
          <strong>Once, only.</strong> When this account exists, this page is gone —
          there is no second setup and no back door. If the code expires unused,
          the operator issues a new one from the deployment side.
        </div>
        <button className="cl-btn primary" type="submit" disabled={busy} style={{ marginTop: 14 }}>
          {busy ? "Creating the admin account…" : "Create the admin account"}
        </button>
      </form>
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
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);

  useEffect(() => {
    let live = true;
    getInvitePreview(code)
      .then((p) => {
        if (!live) return;
        setPreview(p);
        // The email arrives pre-filled from the invite (wireframe
        // 02) and stays editable on screen; the edge's binding check
        // decides at redemption (a mismatch never spends the invite).
        if (p.email) setEmail(p.email);
      })
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
        ...(email.trim() ? { email: email.trim() } : {}),
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

  const grants = preview.workspaces ?? [];
  const inviter = preview.created_by;
  const joinPhrase =
    grants.length === 1
      ? `join the ${grants[0].name} program as a ${grants[0].role}`
      : grants.length > 1
        ? `join ${grants.map((g) => `${g.name} (${g.role})`).join(" and ")}`
        : "join Glossa Lab";
  const expiresNote = preview.expires_at
    ? ` · Invitation links are single-use and expire — this one was set to expire on ${new Date(preview.expires_at).toLocaleDateString(undefined, { month: "short", day: "numeric" })}`
    : "";
  return (
    <Shell wide foot={`glossa.bitconcepts.tech${expiresNote}.`}>
      <h1>You've been invited</h1>
      <p className="cl-lede">
        {inviter && (
          <>
            <strong>{inviter.username}</strong> ({inviter.global_type}) invited you to{" "}
          </>
        )}
        {joinPhrase}. Choose your username and password to create
        your account — this link works once.
      </p>
      {error && <div className="cl-form-error">{error}</div>}
      <form onSubmit={submit}>
        <div className="cl-field">
          <label htmlFor="cl-invite-username">Choose a username</label>
          <input
            id="cl-invite-username"
            autoComplete="username"
            placeholder="e.g. j-mensah"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="cl-field">
          <label htmlFor="cl-invite-email">
            Email{" "}
            <span className="cl-label-hint">
              {preview.email
                ? "— from the invite; change it if you were reached at a different address"
                : "— optional; it identifies your account to admins"}
            </span>
          </label>
          <input
            id="cl-invite-email"
            type="email"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="cl-field">
          <label htmlFor="cl-invite-password">Set a password</label>
          <input
            id="cl-invite-password"
            type="password"
            autoComplete="new-password"
            placeholder="a password only you know"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div className="cl-field">
          <label htmlFor="cl-invite-confirm">Repeat the password</label>
          <input
            id="cl-invite-confirm"
            type="password"
            autoComplete="new-password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            required
          />
        </div>
        <button className="cl-btn primary" type="submit" disabled={busy}>
          {busy
            ? "Creating your account…"
            : grants.length >= 1
              ? `Create account & join ${grants[0].name}`
              : "Create my account"}
        </button>
      </form>
      <div className="cl-auth-foot">
        Your work in the program is attributed to your username —
        claims you register and digestion acts you complete carry
        your name.
      </div>
    </Shell>
  );
}
