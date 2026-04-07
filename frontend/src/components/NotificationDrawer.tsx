/**
 * NotificationCenter — compact dropdown anchored to the bell button.
 * Does NOT cover the AI chat bubble or take over the screen.
 * Familiar GitHub/LinkedIn-style pattern; appropriate for researchers.
 */
import { useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { type ToastType, useToast } from "../hooks/useToast";

const TYPE_ICONS: Record<ToastType, string> = {
  success: "✓",
  error: "✗",
  warning: "⚠",
  info: "ℹ",
};

const TYPE_COLORS: Record<ToastType, { bg: string; text: string; dot: string }> = {
  success: { bg: "#f0fdf4", text: "#16a34a", dot: "#16a34a" },
  error:   { bg: "#fef2f2", text: "#dc2626", dot: "#dc2626" },
  warning: { bg: "#fef3c7", text: "#d97706", dot: "#d97706" },
  info:    { bg: "#eff6ff", text: "#2563eb", dot: "#2563eb" },
};

function fmtTime(ts: number): string {
  const d = new Date(ts);
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return "just now";
  if (diffMin < 60) return `${diffMin}m ago`;
  if (diffMin < 1440) return `${Math.floor(diffMin / 60)}h ago`;
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric" }) + " " +
    d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
}

// ── Self-contained NotificationCenter (bell + dropdown) ──────────────────────
// Replaces the old full-side-panel drawer with a compact GitHub/LinkedIn-style
// dropdown. Does not cover the AI chat bubble (z-index 7000 < bubble 8400).

export function NotificationBell({ onClick }: { onClick: () => void }) {
  const { unreadCount } = useToast();
  return (
    <button
      onClick={onClick}
      title={`Notifications${unreadCount > 0 ? ` (${unreadCount} unread)` : ""}`}
      style={{ position: "relative", padding: "4px 10px", border: "1px solid #e5e7eb",
        borderRadius: 6, background: "#f9fafb", cursor: "pointer", fontSize: 15, color: "#6b7280" }}
    >
      🔔
      {unreadCount > 0 && (
        <span style={{ position: "absolute", top: -4, right: -4, minWidth: 16, height: 16,
          borderRadius: 8, background: "#dc2626", color: "#fff", fontSize: 9, fontWeight: 700,
          display: "flex", alignItems: "center", justifyContent: "center", padding: "0 3px" }}>
          {unreadCount > 99 ? "99+" : unreadCount}
        </span>
      )}
    </button>
  );
}

/** @deprecated no longer used */
export function NotificationDrawer(_: { open: boolean; onClose: () => void }) {
  return null;
}

/**
 * NotificationCenter — drop this anywhere in the tree once.
 * Renders its own bell + dropdown; no props needed from parent.
 */
export function NotificationCenter() {
  const { notifications, unreadCount, markAllRead, clearNotification, clearAllNotifications } = useToast();
  const [open, setOpen] = useState(false);
  const bellRef = useRef<HTMLButtonElement>(null);
  const dropRef = useRef<HTMLDivElement>(null);
  const [pos, setPos] = useState({ top: 48, right: 12 });

  const openDropdown = useCallback(() => {
    if (bellRef.current) {
      const r = bellRef.current.getBoundingClientRect();
      // Anchor below the bell, aligned to its right edge
      setPos({ top: r.bottom + 8, right: window.innerWidth - r.right });
    }
    setOpen(true);
  }, []);

  useEffect(() => { if (open) markAllRead(); }, [open, markAllRead]);

  useEffect(() => {
    if (!open) return;
    const h = (e: MouseEvent) => {
      if (dropRef.current && !dropRef.current.contains(e.target as Node) &&
          bellRef.current && !bellRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    const t = setTimeout(() => document.addEventListener("mousedown", h), 50);
    return () => { clearTimeout(t); document.removeEventListener("mousedown", h); };
  }, [open]);

  return (
    <>
      {/* Bell button */}
      <button
        ref={bellRef}
        onClick={() => open ? setOpen(false) : openDropdown()}
        title={`Notifications${unreadCount > 0 ? ` (${unreadCount} unread)` : ""}`}
        style={{ position: "relative", padding: "4px 10px", border: "1px solid #e5e7eb",
          borderRadius: 6, background: open ? "#eff6ff" : "#f9fafb",
          cursor: "pointer", fontSize: 15, color: open ? "#2563eb" : "#6b7280" }}
      >
        🔔
        {unreadCount > 0 && (
          <span style={{ position: "absolute", top: -4, right: -4, minWidth: 16, height: 16,
            borderRadius: 8, background: "#dc2626", color: "#fff", fontSize: 9, fontWeight: 700,
            display: "flex", alignItems: "center", justifyContent: "center", padding: "0 3px" }}>
            {unreadCount > 99 ? "99+" : unreadCount}
          </span>
        )}
      </button>

      {/* Dropdown — rendered via portal at document.body so z-9500 is never
           bounded by the sticky header's stacking context (z-100) */}
      {open && createPortal(
        <div
          ref={dropRef}
          style={{
            position: "fixed", top: pos.top, right: pos.right,
            width: 380, maxHeight: 460,
            background: "#fff", borderRadius: 10,
            boxShadow: "0 8px 32px rgba(0,0,0,0.14), 0 0 0 1px rgba(0,0,0,0.06)",
            zIndex: 9500, display: "flex", flexDirection: "column",
            animation: "notifFadeIn 0.14s ease",
          }}
        >
          {/* Header row */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center",
            padding: "12px 14px 10px", borderBottom: "1px solid #f3f4f6" }}>
            <span style={{ fontWeight: 700, fontSize: 13, color: "#111827" }}>Notifications</span>
            <div style={{ display: "flex", gap: 6 }}>
              {notifications.length > 0 && (
                <button onClick={clearAllNotifications}
                  style={{ padding: "2px 8px", border: "1px solid #e5e7eb", borderRadius: 4,
                    background: "none", cursor: "pointer", fontSize: 10, color: "#6b7280" }}>
                  Clear all
                </button>
              )}
              <button onClick={() => setOpen(false)}
                style={{ border: "none", background: "none", cursor: "pointer",
                  fontSize: 16, color: "#9ca3af", padding: "0 2px", lineHeight: 1 }}>×</button>
            </div>
          </div>

          {/* Notification list */}
          <div style={{ flex: 1, overflowY: "auto" }}>
            {notifications.length === 0 && (
              <div style={{ textAlign: "center", padding: "2rem 1rem", color: "#9ca3af" }}>
                <div style={{ fontSize: 24, marginBottom: 6 }}>🔔</div>
                <div style={{ fontSize: 12 }}>No notifications</div>
              </div>
            )}
            {notifications.map((n) => {
              const c = TYPE_COLORS[n.type] ?? TYPE_COLORS.info;
              return (
                <div key={n.id} style={{ display: "flex", gap: 10, padding: "10px 14px",
                  borderBottom: "1px solid #f9fafb",
                  background: n.read ? "#fff" : "#f8f9ff", alignItems: "flex-start" }}>
                  <div style={{ width: 22, height: 22, borderRadius: "50%", background: c.bg,
                    display: "flex", alignItems: "center", justifyContent: "center",
                    flexShrink: 0, fontSize: 11, fontWeight: 700, color: c.text, marginTop: 1 }}>
                    {TYPE_ICONS[n.type]}
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 12, color: "#111827", lineHeight: 1.45,
                      wordBreak: "break-word", fontWeight: n.read ? 400 : 500 }}>{n.message}</div>
                    <div style={{ fontSize: 10, color: "#9ca3af", marginTop: 2 }}>{fmtTime(n.timestamp)}</div>
                  </div>
                  <button onClick={() => clearNotification(n.id)}
                    style={{ border: "none", background: "none", cursor: "pointer",
                      color: "#d1d5db", fontSize: 13, flexShrink: 0, padding: "0 2px",
                      lineHeight: 1 }}>×</button>
                </div>
              );
            })}
          </div>
        </div>
      , document.body)}
      <style>{`@keyframes notifFadeIn { from { opacity:0; transform:translateY(-6px); } to { opacity:1; transform:translateY(0); } }`}</style>
    </>
  );
}
