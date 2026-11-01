/**
 * Spec 082 — the API token surfaces (ui-contract.md §4/§5).
 *
 * ApiTokenField is shared by Settings (Tool — service) and the
 * "API token needed" gate: a paste field whose value is never
 * displayed after saving. State is shown honestly — present/absent
 * plus the stored token's SHA-256 fingerprint (first 8 hex chars) —
 * so a person can confirm WHICH token the app holds without the
 * token itself ever rendering.
 */
import { useState, useSyncExternalStore } from "react";
import {
  clearApiToken,
  getAuthState,
  setApiToken,
  subscribeAuth,
  type AuthState,
} from "../auth";
import { Card, CardTitle, palette, PrimaryButton, QuietButton } from "./ui081";

export function useAuthState(): AuthState {
  return useSyncExternalStore(subscribeAuth, getAuthState);
}

export function ApiTokenField({ darkMode }: { darkMode: boolean }) {
  const p = palette(darkMode);
  const auth = useAuthState();
  const [draft, setDraft] = useState("");
  const [saved, setSaved] = useState(false);

  const save = async () => {
    if (!draft.trim()) return;
    await setApiToken(draft);
    setDraft("");
    setSaved(true);
  };

  return (
    <div>
      <div style={{ fontSize: 13, color: p.fg, marginBottom: 4 }}>
        {auth.authMode === "disabled"
          ? "This backend has token authentication disabled — no token is needed."
          : auth.hasToken
            ? <>Token present — fingerprint <code style={{ fontFamily: "monospace" }}>{auth.fingerprint || "…"}</code> (SHA-256, first 8). The value itself is never shown.</>
            : "No token stored. Paste the token from the tray's “Copy API token” action — the app cannot read the token file itself."}
      </div>
      {auth.authMode !== "disabled" && (
        <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap", marginTop: 8 }}>
          <input
            type="password"
            value={draft}
            onChange={(e) => { setDraft(e.target.value); setSaved(false); }}
            onKeyDown={(e) => { if (e.key === "Enter") void save(); }}
            placeholder="Paste API token"
            aria-label="API token"
            autoComplete="off"
            style={{
              flex: "1 1 260px", padding: "8px 10px", borderRadius: 6,
              border: `1px solid ${p.border}`, background: p.inputBg, color: p.fg,
              fontSize: 13, fontFamily: "monospace",
            }}
          />
          <PrimaryButton onClick={() => void save()} disabled={!draft.trim()}>
            Save token
          </PrimaryButton>
          {auth.hasToken && (
            <QuietButton onClick={() => { void clearApiToken("manual"); }}>
              Remove token
            </QuietButton>
          )}
          {saved && (
            <span style={{ fontSize: 12, color: "#15803d" }}>Saved — the app will use it on the next call.</span>
          )}
        </div>
      )}
    </div>
  );
}

/**
 * The named state the app enters when the backend requires a token
 * and none works (contract §5). Rendered in place of the tab content;
 * the shell stays visible so Settings remains reachable.
 */
export function ApiTokenGate({ darkMode }: { darkMode: boolean }) {
  const p = palette(darkMode);
  return (
    <div style={{ padding: 24, maxWidth: 640, margin: "0 auto" }}>
      <Card p={p}>
        <CardTitle p={p} sub="The backend on this machine requires its API token before it will answer. This is the token's own check working — nothing is broken.">
          API token needed
        </CardTitle>
        <div style={{ fontSize: 13, color: p.muted, marginBottom: 12 }}>
          The tray normally opens this app with the token included. If you
          arrived another way, copy the token from the tray's “Copy API
          token” action and paste it here. It is kept only for this
          browser session and is never shown again after saving.
        </div>
        <ApiTokenField darkMode={darkMode} />
      </Card>
    </div>
  );
}
