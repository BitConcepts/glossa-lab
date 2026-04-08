/**
 * CollaborationPanel — per-study threaded messages.
 *
 * Displays pinned messages first, then chronological thread.
 * Each message shows: author, timestamp, text, pin toggle, delete.
 * Supports AI-driven "Suggest next steps" that injects pinned messages
 * into the AI Chat context.
 */

import React, { useCallback, useEffect, useRef, useState } from "react";
import {
  listCollabMessages,
  createCollabMessage,
  updateCollabMessage,
  deleteCollabMessage,
  type CollabMessage,
} from "../api";
import { useAIChat } from "../hooks/useAIChat";

// ── Helpers ───────────────────────────────────────────────────────────────────

function fmtTime(iso: string): string {
  try {
    const d = new Date(iso);
    const today = new Date();
    const sameDay =
      d.getFullYear() === today.getFullYear() &&
      d.getMonth() === today.getMonth() &&
      d.getDate() === today.getDate();
    return sameDay
      ? d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" })
      : d.toLocaleDateString(undefined, { month: "short", day: "numeric" }) +
          " " +
          d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
  } catch {
    return iso.slice(0, 16).replace("T", " ");
  }
}

// ── MessageRow ─────────────────────────────────────────────────────────────────

interface MessageRowProps {
  msg: CollabMessage;
  studyId: string;
  onUpdated: (msg: CollabMessage) => void;
  onDeleted: (id: string) => void;
  darkMode: boolean;
}

function MessageRow({ msg, studyId, onUpdated, onDeleted, darkMode }: MessageRowProps) {
  const [confirmDel, setConfirmDel] = useState(false);
  const sBg    = darkMode ? "#0f172a" : "#f8fafc";
  const sBdr   = darkMode ? "#1e293b" : "#e5e7eb";
  const sText  = darkMode ? "#cbd5e1" : "#1e293b";
  const sMuted = darkMode ? "#64748b" : "#94a3b8";
  const pinClr = msg.pinned ? "#f59e0b" : (darkMode ? "#334155" : "#d1d5db");

  const togglePin = async () => {
    const updated = await updateCollabMessage(studyId, msg.id, { pinned: msg.pinned ? 0 : 1 });
    onUpdated(updated);
  };

  const handleDelete = async () => {
    if (!confirmDel) { setConfirmDel(true); setTimeout(() => setConfirmDel(false), 3000); return; }
    await deleteCollabMessage(studyId, msg.id);
    onDeleted(msg.id);
  };

  return (
    <div style={{
      padding: "7px 9px", borderRadius: 6, marginBottom: 5,
      background: msg.pinned ? (darkMode ? "#1a1a0a" : "#fffbeb") : sBg,
      border: `1px solid ${msg.pinned ? "#f59e0b40" : sBdr}`,
      fontSize: 12,
    }}>
      {/* Header row */}
      <div style={{ display: "flex", alignItems: "center", gap: 5, marginBottom: 3 }}>
        {msg.author && (
          <span style={{ fontWeight: 700, color: darkMode ? "#93c5fd" : "#2563eb", fontSize: 11 }}>
            {msg.author}
          </span>
        )}
        <span style={{ color: sMuted, fontSize: 10 }}>{fmtTime(msg.created_at)}</span>
        <div style={{ flex: 1 }} />
        <button
          onClick={() => void togglePin()}
          title={msg.pinned ? "Unpin" : "Pin"}
          style={{ border: "none", background: "none", cursor: "pointer", fontSize: 13, color: pinClr, padding: "0 2px", lineHeight: 1 }}>
          📌
        </button>
        <button
          onClick={() => void handleDelete()}
          title={confirmDel ? "Confirm delete?" : "Delete"}
          style={{ border: "none", background: "none", cursor: "pointer", fontSize: 11, color: confirmDel ? "#f87171" : sMuted, padding: "0 2px", lineHeight: 1 }}>
          {confirmDel ? "!" : "×"}
        </button>
      </div>
      {/* Message body */}
      <div style={{ color: sText, lineHeight: 1.5, whiteSpace: "pre-wrap", wordBreak: "break-word" }}>
        {msg.message}
      </div>
    </div>
  );
}

// ── Main CollaborationPanel ───────────────────────────────────────────────────

interface Props {
  studyId: string | null;
  studyName?: string;
  darkMode?: boolean;
  /** Start the panel collapsed. Default false (open). */
  initialCollapsed?: boolean;
}

export function CollaborationPanel({ studyId, studyName, darkMode = true, initialCollapsed = false }: Props) {
  const [messages, setMessages] = useState<CollabMessage[]>([]);
  const [loading, setLoading]   = useState(false);
  const [newAuthor, setNewAuthor] = useState(() => localStorage.getItem("glossa_collab_author") ?? "");
  const [newMsg, setNewMsg]     = useState("");
  const [sending, setSending]   = useState(false);
  const [collapsed, setCollapsed] = useState(initialCollapsed);
  const listRef = useRef<HTMLDivElement>(null);
  const { openChat } = useAIChat();

  const sBg    = darkMode ? "#0f172a" : "#f8fafc";
  const sBg2   = darkMode ? "#1e293b" : "#ffffff";
  const sText  = darkMode ? "#e2e8f0" : "#1e293b";
  const sMuted = darkMode ? "#94a3b8" : "#64748b";
  const sFaint = darkMode ? "#64748b" : "#9ca3af";
  const sBdr   = darkMode ? "#1e293b" : "#e5e7eb";
  const iStyle: React.CSSProperties = {
    width: "100%", boxSizing: "border-box", padding: "4px 7px",
    border: `1px solid ${darkMode ? "#334155" : "#d1d5db"}`,
    borderRadius: 5, fontSize: 11, outline: "none",
    background: darkMode ? "#0f172a" : "#ffffff",
    color: sText,
    fontFamily: "inherit",
  };

  const load = useCallback(async () => {
    if (!studyId) { setMessages([]); return; }
    setLoading(true);
    try { setMessages(await listCollabMessages(studyId)); }
    catch { /* backend not running — silently skip */ }
    finally { setLoading(false); }
  }, [studyId]);

  useEffect(() => { void load(); }, [load]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (listRef.current) listRef.current.scrollTop = listRef.current.scrollHeight;
  }, [messages.length]);

  const handleSend = async () => {
    if (!studyId || !newMsg.trim()) return;
    setSending(true);
    try {
      const created = await createCollabMessage(studyId, {
        author: newAuthor.trim(),
        message: newMsg.trim(),
      });
      setMessages(prev => [...prev, created]);
      setNewMsg("");
      localStorage.setItem("glossa_collab_author", newAuthor);
    } catch { /* ignore if offline */ }
    finally { setSending(false); }
  };

  const handleUpdated = (updated: CollabMessage) =>
    setMessages(prev => {
      const next = prev.map(m => m.id === updated.id ? updated : m);
      // re-sort: pinned first then chronological
      return [...next].sort((a, b) => b.pinned - a.pinned || a.created_at.localeCompare(b.created_at));
    });

  const handleDeleted = (id: string) => setMessages(prev => prev.filter(m => m.id !== id));

  const suggestNextSteps = () => {
    const pinned = messages.filter(m => m.pinned);
    const all    = messages;
    const msgs   = (pinned.length > 0 ? pinned : all).slice(-8);
    const ctx    = msgs.map(m => `${m.author ? m.author + ": " : ""}${m.message}`).join("\n");
    openChat({
      contextType: "study",
      contextId: studyId ?? "",
      initialPrompt: `Based on the following collaboration messages from study "${studyName ?? studyId}":\n\n${ctx}\n\nWhat are the recommended next steps for this research?`,
    });
  };

  const pinnedCount = messages.filter(m => m.pinned).length;
  const totalCount  = messages.length;

  return (
    <div style={{
      background: sBg, borderTop: `1px solid ${sBdr}`,
      display: "flex", flexDirection: "column", flexShrink: 0,
      maxHeight: collapsed ? 28 : 320,
      transition: "max-height 0.2s ease",
      overflow: "hidden",
    }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 5, padding: "3px 8px", background: sBg2, borderBottom: collapsed ? "none" : `1px solid ${sBdr}`, flexShrink: 0, cursor: "pointer" }}
        onClick={() => setCollapsed(v => !v)}>
        <span style={{ fontSize: 11, color: sMuted }}>{collapsed ? "▶" : "▼"}</span>
        <span style={{ fontSize: 10, fontWeight: 700, color: sMuted, textTransform: "uppercase", letterSpacing: 0.5, flex: 1 }}>
          💬 Collaboration{totalCount > 0 ? ` (${totalCount})` : ""}{pinnedCount > 0 ? ` · ${pinnedCount} 📌` : ""}
        </span>
        {!collapsed && messages.length > 0 && (
          <button
            onClick={e => { e.stopPropagation(); suggestNextSteps(); }}
            title="Ask AI to suggest next steps based on pinned messages"
            style={{ border: `1px solid ${sBdr}`, borderRadius: 4, background: "none", color: sMuted, cursor: "pointer", fontSize: 9, padding: "1px 5px", fontWeight: 600 }}>
            ✨ Next Steps
          </button>
        )}
        {!collapsed && (
          <button onClick={e => { e.stopPropagation(); void load(); }} title="Reload messages" style={{ border: "none", background: "none", color: sFaint, cursor: "pointer", fontSize: 11, padding: "0 2px" }}>⟳</button>
        )}
      </div>

      {!collapsed && (
        <>
          {/* Message list */}
          <div ref={listRef} style={{ flex: 1, overflowY: "auto", padding: "6px 8px", minHeight: 0 }}>
            {loading && <div style={{ color: sFaint, fontSize: 10, textAlign: "center", padding: 8 }}>Loading…</div>}
            {!loading && !studyId && (
              <div style={{ color: sFaint, fontSize: 10, textAlign: "center", padding: 12 }}>Select a study to see collaboration messages.</div>
            )}
            {!loading && studyId && messages.length === 0 && (
              <div style={{ color: sFaint, fontSize: 10, textAlign: "center", padding: 12 }}>
                No messages yet. Add the first one below.
              </div>
            )}
            {messages.map(msg => (
              <MessageRow
                key={msg.id}
                msg={msg}
                studyId={studyId!}
                onUpdated={handleUpdated}
                onDeleted={handleDeleted}
                darkMode={darkMode}
              />
            ))}
          </div>

          {/* Compose area */}
          <div style={{ padding: "5px 8px", borderTop: `1px solid ${sBdr}`, background: sBg2, flexShrink: 0 }}>
            <input
              value={newAuthor}
              onChange={e => setNewAuthor(e.target.value)}
              placeholder="Your name (optional)"
              style={{ ...iStyle, marginBottom: 4 }}
            />
            <div style={{ display: "flex", gap: 4 }}>
              <textarea
                value={newMsg}
                onChange={e => setNewMsg(e.target.value)}
                onKeyDown={e => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) void handleSend(); }}
                placeholder="Add a message… (Ctrl+Enter to send)"
                rows={2}
                disabled={!studyId}
                style={{ ...iStyle, flex: 1, resize: "none" }}
              />
              <button
                onClick={() => void handleSend()}
                disabled={sending || !studyId || !newMsg.trim()}
                style={{
                  border: "none", borderRadius: 5, padding: "0 10px",
                  background: sending || !studyId || !newMsg.trim() ? (darkMode ? "#1e293b" : "#e5e7eb") : "#2563eb",
                  color: sending || !studyId || !newMsg.trim() ? sFaint : "#fff",
                  cursor: sending || !studyId || !newMsg.trim() ? "not-allowed" : "pointer",
                  fontSize: 12, fontWeight: 600, flexShrink: 0,
                }}>
                {sending ? "…" : "Send"}
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
