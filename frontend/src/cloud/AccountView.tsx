/**
 * Spec 083 (Step 3, T026) — Account & security (wireframe 08).
 * Self-service for the one identity each user owns: profile,
 * password, sessions, and their own slice of the audit log.
 * Username is immutable — it is the attribution anchor (C083-11) —
 * and the screen says so where a user would try to change it.
 */

import { useEffect, useState, type FormEvent } from "react";
import {
  CloudApiError,
  changeEmail,
  changePassword,
  getAccount,
  revokeSession,
} from "./api";
import type { AccountView as AccountData } from "./types";
import { activityTitle } from "./auditText";
import { fmtDay, fmtWhenLong, fmtWhenShort } from "./fmt";
import { useCloudSession } from "./session";

export function AccountView() {
  const cloud = useCloudSession();
  const [data, setData] = useState<AccountData | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [email, setEmail] = useState("");
  const [profileMsg, setProfileMsg] = useState<string | null>(null);
  const [profileError, setProfileError] = useState<string | null>(null);
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");
  const [repeat, setRepeat] = useState("");
  const [pwMsg, setPwMsg] = useState<string | null>(null);
  const [pwError, setPwError] = useState<string | null>(null);
  const [sessionError, setSessionError] = useState<string | null>(null);

  const reload = async () => {
    const view = await getAccount();
    setData(view);
    setEmail(view.user.email ?? "");
  };

  useEffect(() => {
    let live = true;
    getAccount()
      .then((view) => {
        if (!live) return;
        setData(view);
        setEmail(view.user.email ?? "");
      })
      .catch((e) => {
        if (live) setLoadError(e instanceof Error ? e.message : "Your account could not be loaded.");
      });
    return () => { live = false; };
  }, []);

  if (loadError) {
    return (
      <div className="cl-root"><div className="cl-screen">
        <h1>Account &amp; security</h1>
        <div className="cl-form-error">{loadError}</div>
      </div></div>
    );
  }
  if (!data) {
    return (
      <div className="cl-root"><div className="cl-screen">
        <div className="cl-loading">Loading your account…</div>
      </div></div>
    );
  }

  const user = data.user;

  const saveProfile = async (e: FormEvent) => {
    e.preventDefault();
    setProfileMsg(null);
    setProfileError(null);
    try {
      await changeEmail(email.trim());
      await reload();
      await cloud.refresh();
      setProfileMsg("Profile saved.");
    } catch (err) {
      setProfileError(err instanceof Error ? err.message : "The email could not be saved.");
    }
  };

  const submitPassword = async (e: FormEvent) => {
    e.preventDefault();
    setPwMsg(null);
    setPwError(null);
    if (next !== repeat) {
      setPwError("The two new passwords don't match.");
      return;
    }
    try {
      await changePassword(current, next);
      setCurrent("");
      setNext("");
      setRepeat("");
      await reload();
      setPwMsg("Password changed. Your other sessions have been signed out.");
    } catch (err) {
      if (err instanceof CloudApiError && err.code === "current_password_invalid") {
        setPwError("The current password did not match.");
      } else if (err instanceof CloudApiError && err.code === "invalid_password") {
        setPwError("Choose a password of at least 8 characters.");
      } else {
        setPwError(err instanceof Error ? err.message : "The password could not be changed.");
      }
    }
  };

  const revoke = async (sessionId: string) => {
    setSessionError(null);
    try {
      await revokeSession(sessionId);
      await reload();
    } catch (err) {
      setSessionError(err instanceof Error ? err.message : "That session could not be revoked.");
    }
  };

  return (
    <div className="cl-root">
      <div className="cl-screen" style={{ maxWidth: 760 }}>
        <h1>Account &amp; security</h1>
        <p className="cl-sub">
          Your identity in this Glossa Lab: how you sign in, where you are signed in, and what
          your account has done. Workspace and tool settings live on the Settings screen, as before.
        </p>

        <div className="cl-card">
          <h2>Profile</h2>
          <form onSubmit={saveProfile}>
            <div className="cl-field">
              <label htmlFor="cl-acct-username">Username</label>
              <input id="cl-acct-username" value={user.username} disabled />
              <div className="cl-hint">Fixed when the account was created; it is the name your work is attributed to.</div>
            </div>
            <div className="cl-field">
              <label htmlFor="cl-acct-email">Email</label>
              <input
                id="cl-acct-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="No email on file"
              />
              <div className="cl-hint">The address admins use to reach you about this account.</div>
            </div>
            <div className="cl-field" style={{ marginBottom: 6 }}>
              <label>Role &amp; memberships</label>
              <div className="cl-small" style={{ lineHeight: 1.9 }}>
                <span className="cl-chip">{user.global_type}</span>
                {cloud.implicitAdmin && (
                  <span className="cl-muted"> · workspace admin in every workspace (implicit, from the global type)</span>
                )}
                {cloud.workspaces.map((w) => (
                  <div key={w.id}>
                    {w.name} <span className="cl-chip grey">{w.role}</span>
                    {w.role_source === "implicit" && <span className="cl-muted"> implicit</span>}
                  </div>
                ))}
                {cloud.workspaces.length === 0 && (
                  <div className="cl-muted">No workspace memberships yet — an admin grants them.</div>
                )}
              </div>
              <div className="cl-hint">Granted by admins; shown here so you can see your own standing.</div>
            </div>
            {profileError && <div className="cl-form-error">{profileError}</div>}
            {profileMsg && <div className="cl-banner-ok">{profileMsg}</div>}
            <button className="cl-btn primary" style={{ width: "auto" }} type="submit">
              Save profile
            </button>
          </form>
        </div>

        <div className="cl-card">
          <h2>Password</h2>
          <form onSubmit={submitPassword}>
            <div className="cl-field">
              <label htmlFor="cl-acct-current">Current password</label>
              <input
                id="cl-acct-current" type="password" autoComplete="current-password"
                value={current} onChange={(e) => setCurrent(e.target.value)} required
              />
            </div>
            <div className="cl-field">
              <label htmlFor="cl-acct-next">New password</label>
              <input
                id="cl-acct-next" type="password" autoComplete="new-password"
                value={next} onChange={(e) => setNext(e.target.value)} required
              />
              <div className="cl-hint">At least 8 characters.</div>
            </div>
            <div className="cl-field">
              <label htmlFor="cl-acct-repeat">Repeat new password</label>
              <input
                id="cl-acct-repeat" type="password" autoComplete="new-password"
                value={repeat} onChange={(e) => setRepeat(e.target.value)} required
              />
            </div>
            {pwError && <div className="cl-form-error">{pwError}</div>}
            {pwMsg && <div className="cl-banner-ok">{pwMsg}</div>}
            <button className="cl-btn primary" style={{ width: "auto" }} type="submit">
              Change password
            </button>
            <span className="cl-small cl-muted" style={{ marginLeft: 10 }}>
              Changing your password signs out your other sessions.
            </span>
          </form>
        </div>

        <div className="cl-card">
          <h2>Sessions</h2>
          <p className="cl-card-sub">Where this account is signed in right now.</p>
          {sessionError && <div className="cl-form-error">{sessionError}</div>}
          {data.sessions.map((s) => (
            <div
              key={s.id}
              style={{
                display: "flex", alignItems: "center", gap: 10, padding: "8px 0",
                borderBottom: "1px solid #f3f4f6",
              }}
            >
              <div style={{ flex: 1 }}>
                <strong className="cl-small">{s.current ? "This device" : "Session"}</strong>
                {s.current && <> <span className="cl-chip green">current</span></>}
                <div className="cl-muted cl-small">
                  Signed in {fmtDay(s.created_at)} · {s.current ? "active now" : `last active ${fmtWhenShort(s.last_seen_at)}`}
                </div>
              </div>
              {!s.current && (
                <button className="cl-btn ghost small" onClick={() => void revoke(s.id)}>
                  Revoke
                </button>
              )}
            </div>
          ))}
          {data.sessions.length === 0 && <div className="cl-empty">No live sessions.</div>}
          <p className="cl-small cl-muted" style={{ marginBottom: 0, lineHeight: 1.55 }}>
            Sessions last 30 days and extend with use. If a session isn't yours, revoke it and
            change your password — both events land in the audit log.
          </p>
        </div>

        <div className="cl-card">
          <h2>Your recent activity</h2>
          {data.activity.map((e) => (
            <div
              key={e.id}
              style={{
                display: "flex", justifyContent: "space-between", gap: 12,
                padding: "7px 0", borderBottom: "1px solid #f3f4f6", fontSize: 13,
              }}
            >
              <span>{activityTitle(e.event)}</span>
              <span className="cl-muted" style={{ whiteSpace: "nowrap" }}>{fmtWhenLong(e.ts)}</span>
            </div>
          ))}
          {data.activity.length === 0 && <div className="cl-empty">Nothing yet.</div>}
          <p className="cl-small cl-muted" style={{ marginBottom: 0 }}>
            Your slice of the audit log — admins see the whole log on the Audit tab.
          </p>
        </div>
      </div>
    </div>
  );
}
